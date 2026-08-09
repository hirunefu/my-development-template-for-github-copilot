#!/usr/bin/env python3
"""上流の skill リポジトリから docs/skills-catalog.md を生成する。

使い方:

    python3 scripts/gen-skills-catalog.py
    python3 scripts/gen-skills-catalog.py --source <既存のチェックアウト>

出力は決定的で、上流が動いていなければ再実行しても差分は出ない。生成日時では
なく上流のコミット日時を埋め込んでいるのはそのため。

標準ライブラリのみで動く。frontmatter の解析に PyYAML を使わないのは、複写した
利用者の環境に入っているとは限らないため。そのぶん解析できる形式は限られるので、
未対応の形式を見つけたら黙って誤読せず失敗する。

SkillSpector は下の git 呼び出しを `AST4 subprocess module call` として検出するが、
その指摘が求める緩和策（シェルを介さず引数リストで渡す）は既に満たしている。
上流を取得する以上この呼び出しは避けられないため、承知の上で受け入れている。
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

UPSTREAM = "https://github.com/mattpocock/skills.git"
OUTPUT = "docs/skills-catalog.md"

# カテゴリの表示順と説明。上流に新しいカテゴリが増えたら失敗させる。
CATEGORIES = {
    "engineering": "開発の流れそのものを扱う。このリポジトリの `docs/agents/` が前提にしているのはここ",
    "productivity": "考えを整理する、教わる、引き継ぐといった作業を扱う",
    "misc": "特定の場面向けの単発ツール",
    "in-progress": "上流で作りかけのもの。挙動が変わる前提で扱う",
}


class UnsupportedFormat(Exception):
    """frontmatter が想定した形式でないときに送出する。"""


def parse_frontmatter(text, rel_path):
    """SKILL.md の先頭 frontmatter から name と description を取り出す。

    複数行やブロックスカラーの description は解釈しない。見つけた時点で
    誤読を避けるため例外にする。
    """
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        raise UnsupportedFormat(f"{rel_path}: frontmatter が見つからない")

    lines = match.group(1).split("\n")
    fields = {}
    for index, line in enumerate(lines):
        field = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not field:
            continue
        key, raw = field.group(1), field.group(2).strip()

        if key in ("name", "description"):
            if raw in ("", "|", ">", "|-", ">-"):
                raise UnsupportedFormat(
                    f"{rel_path}: {key} が複数行形式になっている。"
                    "このスクリプトは 1 行の値しか解釈しない"
                )
            following = lines[index + 1] if index + 1 < len(lines) else ""
            if following.startswith((" ", "\t")):
                raise UnsupportedFormat(
                    f"{rel_path}: {key} が次の行に続いている。"
                    "このスクリプトは 1 行の値しか解釈しない"
                )

        # クォートの除去は全フィールド共通で行う。name と description だけに
        # 適用していたころは、`disable-model-invocation: "true"` を黙って
        # false と誤読していた。
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
            raw = raw[1:-1]

        fields[key] = raw

    for required in ("name", "description"):
        if required not in fields:
            raise UnsupportedFormat(f"{rel_path}: {required} が無い")

    flag = fields.get("disable-model-invocation")
    if flag is not None and flag.lower() not in ("true", "false"):
        raise UnsupportedFormat(
            f"{rel_path}: disable-model-invocation が '{flag}' で真偽値として解釈できない"
        )

    return fields


def collect(source_root):
    """skills/<カテゴリ>/<名前>/SKILL.md を走査して一覧を返す。"""
    skills_root = os.path.join(source_root, "skills")
    if not os.path.isdir(skills_root):
        raise UnsupportedFormat(
            f"{skills_root} が無い。上流のディレクトリ構成が変わった可能性がある"
        )

    collected = []
    for dirpath, _dirnames, filenames in os.walk(skills_root):
        if "SKILL.md" not in filenames:
            continue
        path = os.path.join(dirpath, "SKILL.md")
        rel = os.path.relpath(path, source_root)
        # skills/<カテゴリ>/<名前>/SKILL.md を想定しているので 3 要素になる
        parts = os.path.relpath(path, skills_root).split(os.sep)
        if len(parts) != 3:
            raise UnsupportedFormat(
                f"{rel}: 想定と違う階層にある（skills/<カテゴリ>/<名前>/SKILL.md を想定）"
            )
        category = parts[0]
        if category not in CATEGORIES:
            raise UnsupportedFormat(
                f"{rel}: 未知のカテゴリ '{category}'。CATEGORIES に追記が必要"
            )
        fields = parse_frontmatter(open(path, encoding="utf-8").read(), rel)
        collected.append(
            {
                "category": category,
                "name": fields["name"],
                "description": fields["description"],
                "user_only": str(fields.get("disable-model-invocation", "")).lower()
                == "true",
            }
        )
    if not collected:
        raise UnsupportedFormat("SKILL.md が 1 件も見つからなかった")
    return collected


def git(args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def render(skills, revision, revision_date):
    total = len(skills)
    user_only = sum(1 for s in skills if s["user_only"])

    out = [
        "<!-- このファイルは生成物です。手で編集しないでください。 -->",
        "<!-- 更新: python3 scripts/gen-skills-catalog.py -->",
        "",
        "# Skill カタログ",
        "",
        "**読み手**: どの skill があるかを探す人。導入方法は [skills.md](./skills.md) を参照。",
        "",
        "[mattpocock/skills](https://github.com/mattpocock/skills) が提供する skill の一覧。",
        "",
        "各 skill の説明文は上流の `SKILL.md` から機械的に抽出したもの。",
        "Copyright (c) 2026 Matt Pocock、MIT License。詳細はリポジトリ直下の `NOTICE` を参照。",
        "",
        f"- 上流のリビジョン: `{revision}`（{revision_date}）",
        f"- 収録数: {total} 件。うち {user_only} 件はユーザーが明示的に呼び出す skill",
        "",
        "**このカタログは自動では更新されない。** 上流が変われば黙って古くなるため、",
        "内容を信頼する前に上のリビジョンを確認すること。",
        "",
        "凡例: (ユーザー呼び出し) はモデルが自動起動せず、スラッシュコマンドで明示的に呼ぶもの。",
    ]

    for category, note in CATEGORIES.items():
        members = sorted(
            (s for s in skills if s["category"] == category), key=lambda s: s["name"]
        )
        if not members:
            continue
        out += ["", f"## {category}（{len(members)} 件）", "", note, ""]
        for skill in members:
            mark = " **(ユーザー呼び出し)**" if skill["user_only"] else ""
            out.append(f"### `/{skill['name']}`{mark}")
            out.append("")
            out.append(skill["description"])
            out.append("")

    return "\n".join(out).rstrip() + "\n"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        help="上流の既存チェックアウト。省略すると一時ディレクトリに shallow clone する",
    )
    parser.add_argument("--output", default=OUTPUT, help=f"出力先（既定: {OUTPUT}）")
    args = parser.parse_args(argv[1:])

    with tempfile.TemporaryDirectory() as tmp:
        if args.source:
            source = args.source
        else:
            source = os.path.join(tmp, "upstream")
            print(f"上流を取得する: {UPSTREAM}", file=sys.stderr)
            subprocess.run(
                ["git", "clone", "--quiet", "--depth", "1", UPSTREAM, source],
                check=True,
            )

        revision = git(["rev-parse", "--short", "HEAD"], source)
        revision_date = git(["log", "-1", "--format=%cs"], source)
        skills = collect(source)

    text = render(skills, revision, revision_date)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(text)

    print(
        f"{args.output} を生成した（{len(skills)} 件 / 上流 {revision} {revision_date}）",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except UnsupportedFormat as error:
        print(f"エラー: {error}", file=sys.stderr)
        print(
            "上流の形式が変わった可能性がある。スクリプトを直すまで生成物は更新しないこと。",
            file=sys.stderr,
        )
        sys.exit(1)
