#!/usr/bin/env python3
"""導入後の確認を機械的に実行する。

docs/checklist.md と docs/github/checklist.md の項目を自動化したもの。
標準ライブラリのみを使う。

使い方:
    python3 scripts/verify.py

終了コード:
    0 = すべて通過（またはスキップ）
    1 = 1 件以上の失敗
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# このリポジトリがテンプレート本体か。setup.py が消す。
# 本体では「雛形のまま」が正しい状態なので、いくつかの検査は判定が反転する。
IS_TEMPLATE = (ROOT / ".template-repo").exists()

PASS, FAIL, SKIP, WARN = "pass", "fail", "skip", "warn"

MARK = {PASS: "✓", FAIL: "✗", SKIP: "−", WARN: "!"}


def width(s: str) -> int:
    """表示幅を求める。日本語は 1 文字で 2 桁を占める。"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s: str, to: int) -> str:
    return s + " " * max(0, to - width(s))


@dataclass
class Result:
    name: str
    status: str
    detail: str = ""
    fix: str = ""


def md_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.md"):
        parts = p.relative_to(ROOT).parts
        if parts and parts[0] in {".git", ".jj", "node_modules"}:
            continue
        out.append(p)
    return out


def run(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.SubprocessError):
        return 127, ""


# --- コア（ホスティング非依存） ---------------------------------------------


def check_template_prose() -> Result:
    """テンプレート自身の説明が残っていないか。"""
    if IS_TEMPLATE:
        return Result("テンプレートの説明が残っていない", SKIP, "テンプレート本体なので残っていてよい")
    needles = ["エージェント向け開発テンプレート", "まだ実案件で運用されていない"]
    hits = []
    for p in md_files():
        if p.name in {"verify.py", "checklist.md"}:
            continue
        if p.relative_to(ROOT).parts[0] == "docs" and "template" in p.parts:
            continue
        text = p.read_text(encoding="utf-8")
        if any(n in text for n in needles):
            hits.append(str(p.relative_to(ROOT)))
    if hits:
        return Result("テンプレートの説明が残っていない", FAIL, ", ".join(hits),
                      "README をこのプロジェクトの説明に書き換える")
    return Result("テンプレートの説明が残っていない", PASS)


def check_template_dir() -> Result:
    """2. テンプレート自身の記録が残っていないか。"""
    d = ROOT / "docs" / "template"
    if not d.exists():
        return Result("テンプレート自身の記録が消えている", PASS)
    n = len(list(d.rglob("*")))
    if IS_TEMPLATE:
        return Result("テンプレート自身の記録が消えている", SKIP, f"テンプレート本体の記録 {n} 件")
    return Result("テンプレート自身の記録が消えている", WARN, f"docs/template/ に {n} 件残っている",
                  "自分のプロジェクトのドメインではないので削除する（残すこと自体は選択可能）")


def check_onboarding_filled() -> Result:
    """参加者向けガイドの空欄が埋まっているか。

    案内文ではなく**実際の空欄**を見る。案内文は消し忘れても実害が小さいが、
    空欄が残ったガイドを新人に渡すと、その人は何も分からないまま放り出される。
    """
    p = ROOT / "docs" / "onboarding.md"
    if not p.exists():
        return Result("参加者ガイドの空欄が埋まっている", SKIP, "docs/onboarding.md が無い")
    text = p.read_text(encoding="utf-8")

    # 空欄を「消す」ことで検査を通せてしまわないよう、先に節の存在を見る。
    required = ["## このプロジェクト", "## 準備", "## 作業する", "## 出す", "## 詰まったら"]
    missing = [h for h in required if h not in text]
    if missing:
        return Result("参加者ガイドの空欄が埋まっている", FAIL,
                      "節が無い: " + ", ".join(h.lstrip("# ") for h in missing),
                      "空欄は消すのではなく埋める。消すと参加者が何も分からなくなる")

    blanks = {
        "プロジェクトの説明": "何を作っているプロジェクトなのか",
        "環境の立ち上げ方": "このプロジェクトのセットアップ手順を書く",
        "相談先": "相談先を書く",
    }
    left = [k for k, needle in blanks.items() if needle in text]

    if IS_TEMPLATE:
        # 本体では空欄が 3 つとも残っているのが正しい。埋まっていたら配布物が壊れている。
        gone = [k for k in blanks if k not in left]
        if gone:
            return Result("参加者ガイドの雛形が壊れていない", FAIL, "空欄が消えている: " + ", ".join(gone),
                          "複写先が何を埋めればよいか分からなくなる")
        return Result("参加者ガイドの雛形が壊れていない", PASS, "空欄 3 つと節 5 つが揃っている")
    if left:
        return Result("参加者ガイドの空欄が埋まっている", FAIL, "未記入: " + ", ".join(left),
                      "参加者が最初に読むファイル。空欄のまま渡さない")
    if "このガイドは雛形として配布されている" in text:
        return Result("参加者ガイドの空欄が埋まっている", WARN, "雛形の案内が残っている",
                      "空欄は埋まっているので、案内の引用ブロックを消せばよい")
    return Result("参加者ガイドの空欄が埋まっている", PASS)


def check_context() -> Result:
    """3. 用語集が自分のものか。"""
    p = ROOT / "CONTEXT.md"
    if not p.exists():
        return Result("用語集が自分のもの", FAIL, "CONTEXT.md が無い", "雛形を置く")
    text = p.read_text(encoding="utf-8")
    foreign = ["サーフェス", "指示ファイル", "偽の緑", "プロジェクト skill"]
    hits = [w for w in foreign if f"**{w}**" in text]
    if hits:
        return Result("用語集が自分のもの", FAIL, "テンプレート由来の用語: " + ", ".join(hits),
                      "自分のドメインの用語に置き換える")
    return Result("用語集が自分のもの", PASS, "雛形のままでよい（先回りして埋めない）")


def check_adr_empty() -> Result:
    """4. ADR が空か。"""
    d = ROOT / "docs" / "adr"
    if not d.exists():
        return Result("ADR が自分のものだけ", FAIL, "docs/adr/ が無い", "README.md を置いて作る")
    others = sorted(x.name for x in d.iterdir() if x.name != "README.md")
    if IS_TEMPLATE:
        return Result("ADR が自分のものだけ", SKIP, f"テンプレート本体（docs/template/adr/ に記録）")
    tmpl = [n for n in others if re.match(r"^00(0[1-9]|1[0-9])-", n)]
    if tmpl:
        return Result("ADR が自分のものだけ", WARN, "テンプレート由来の番号: " + ", ".join(tmpl),
                      "自分の決定でなければ消す。番号は 0001 から使う")
    return Result("ADR が自分のものだけ", PASS, f"{len(others)} 件")


def check_gitignore() -> Result:
    """5. 探索領域が除外されているか。"""
    p = ROOT / ".gitignore"
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    missing = [x for x in ("/.scratch/", ".claude/settings.local.json") if x not in text]
    if "/.scratch/" in missing:
        return Result("探索領域が除外されている", FAIL, ".gitignore に /.scratch/ が無い",
                      "調査中のメモがコミットされる。追記する")
    if missing:
        return Result("探索領域が除外されている", WARN, "推奨項目が無い: " + ", ".join(missing))
    return Result("探索領域が除外されている", PASS)


def check_notice() -> Result:
    """6. 帰属表示が残っているか。"""
    derived = (ROOT / "docs" / "agents").exists()
    if not derived:
        return Result("帰属表示がある", SKIP, "テンプレート由来のファイルを残していない")
    if (ROOT / "NOTICE").exists():
        return Result("帰属表示がある", PASS)
    return Result("帰属表示がある", FAIL, "NOTICE が無い", "MIT の条件は複写のたびに引き継がれる")


def check_example_skills() -> Result:
    """8. 例示 skill が書き換えられているか。"""
    d = ROOT / ".claude" / "skills"
    if not d.exists():
        return Result("例示 skill が残っていない", SKIP, ".claude/skills/ が無い")
    examples = {"order-cancellation", "database-migration", "public-api-compat"}
    hits = sorted(x.name for x in d.iterdir() if x.is_dir() and x.name in examples)
    if hits:
        return Result("例示 skill が残っていない", FAIL, ", ".join(hits),
                      "自分のドメインに書き換えて名前も変える")
    return Result("例示 skill が残っていない", PASS, f"{len(list(d.iterdir()))} 件のプロジェクト skill")


def check_links() -> Result:
    """追加: 相対リンクが切れていないか。"""
    bad = []
    for p in md_files():
        base = p.parent
        for m in re.finditer(r"\[[^\]]*\]\(([^)#]+)\)", p.read_text(encoding="utf-8")):
            t = m.group(1)
            if t.startswith(("http://", "https://", "mailto:")):
                continue
            if not (base / t).resolve().exists():
                bad.append(f"{p.relative_to(ROOT)} -> {t}")
    if bad:
        return Result("相対リンクが切れていない", FAIL, "; ".join(bad[:5]))
    return Result("相対リンクが切れていない", PASS)


def check_instruction_files() -> Result:
    """追加: 指示ファイルの整合。"""
    a = ROOT / "AGENTS.md"
    c = ROOT / "CLAUDE.md"
    if not a.exists():
        return Result("指示ファイルが揃っている", FAIL, "AGENTS.md が無い")
    if not c.exists():
        return Result("指示ファイルが揃っている", WARN, "CLAUDE.md が無い",
                      "Claude Code は AGENTS.md を読まない")
    if "@AGENTS.md" not in c.read_text(encoding="utf-8"):
        return Result("指示ファイルが揃っている", FAIL, "CLAUDE.md が AGENTS.md を取り込んでいない")
    return Result("指示ファイルが揃っている", PASS)


# --- GitHub 層 ---------------------------------------------------------------


def gh_available() -> bool:
    if not shutil.which("gh"):
        return False
    code, _ = run(["gh", "auth", "status"])
    return code == 0


def repo_slug() -> str | None:
    code, out = run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])
    return out.strip() if code == 0 and out.strip() else None


def check_workflow_ran() -> Result:
    code, out = run(["gh", "run", "list", "--limit", "5", "--json", "name"])
    if code != 0:
        return Result("workflow が動いている", SKIP, "gh run list が失敗した")
    try:
        runs = json.loads(out)
    except json.JSONDecodeError:
        return Result("workflow が動いている", SKIP, "出力を解釈できない")
    if not runs:
        return Result("workflow が動いている", FAIL, "実行履歴が無い", "まだ push していない可能性がある")
    return Result("workflow が動いている", PASS, f"{len(runs)} 件")


def check_labels() -> Result:
    want = {"needs-triage", "needs-info", "ready-for-agent", "ready-for-human", "wontfix"}
    code, out = run(["gh", "label", "list", "--json", "name", "-q", ".[].name"])
    if code != 0:
        return Result("triage ラベルがある", SKIP, "gh label list が失敗した")
    have = set(out.split())
    missing = sorted(want - have)
    if missing:
        return Result("triage ラベルがある", FAIL, "不足: " + ", ".join(missing),
                      "docs/github/triage-labels.md の手順で作る")
    return Result("triage ラベルがある", PASS)


def parse_job_names(text: str) -> set[str]:
    """workflow の jobs: 配下のキーだけを取る。

    yaml を使わずに済ませるため。`on:` 配下の pull_request / push を
    job 名と誤認しないよう、jobs: ブロックの中だけを見る。
    """
    jobs: set[str] = set()
    inside = False
    for line in text.split("\n"):
        if re.match(r"^jobs:\s*$", line):
            inside = True
            continue
        if inside:
            if line and not line.startswith((" ", "\t", "#")):
                break  # 次のトップレベルキー
            m = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
            if m:
                jobs.add(m.group(1))
    return jobs


def check_branch_protection(slug: str) -> tuple[Result, Result]:
    code, out = run(["gh", "api", f"repos/{slug}/branches/main/protection"])
    if code != 0:
        r = Result("ブランチ保護が効いている", FAIL, "保護が設定されていない",
                   "CI が赤くてもマージできる状態。docs/github/branch-protection.md")
        return r, Result("required check の名前が一致", SKIP, "保護が無い")
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return (Result("ブランチ保護が効いている", SKIP, "応答を解釈できない"),
                Result("required check の名前が一致", SKIP))
    contexts = set(data.get("required_status_checks", {}).get("contexts", []))
    r1 = (Result("ブランチ保護が効いている", PASS, f"required: {', '.join(sorted(contexts)) or '(なし)'}")
          if contexts else
          Result("ブランチ保護が効いている", FAIL, "required status check が空",
                 "落ちた CI を無視してマージできる"))

    wf = ROOT / ".github" / "workflows" / "security.yml"
    if not wf.exists():
        return r1, Result("required check の名前が一致", SKIP, "security.yml が無い")
    jobs = parse_job_names(wf.read_text(encoding="utf-8"))
    extra = contexts - jobs
    lost = jobs - contexts
    if extra:
        r2 = Result("required check の名前が一致", FAIL, "workflow に無い check を待っている: " + ", ".join(sorted(extra)),
                    "変更提案が永久にマージできなくなる。required から外す")
    elif lost:
        r2 = Result("required check の名前が一致", WARN, "required になっていない job: " + ", ".join(sorted(lost)))
    else:
        r2 = Result("required check の名前が一致", PASS)
    return r1, r2


# --- 実行 --------------------------------------------------------------------


def main() -> int:
    core = [
        check_template_prose(), check_template_dir(), check_context(), check_adr_empty(), check_gitignore(), check_notice(),
        check_onboarding_filled(), check_example_skills(), check_links(),
        check_instruction_files(),
    ]

    github: list[Result] = []
    if (ROOT / ".github" / "workflows").exists():
        if gh_available():
            slug = repo_slug()
            github.append(check_workflow_ran())
            github.append(check_labels())
            if slug:
                a, b = check_branch_protection(slug)
                github += [a, b]
            else:
                github.append(Result("ブランチ保護が効いている", SKIP, "リポジトリを特定できない"))
        else:
            github.append(Result("GitHub 層の確認", SKIP, "gh が無い、または未認証"))

    col = max(width(r.name) for r in core + github) + 2
    print("導入後の確認\n")
    print("コア")
    for r in core:
        print(f"  {MARK[r.status]} {pad(r.name, col)}{r.detail}")
        if r.status == FAIL and r.fix:
            print(f"      → {r.fix}")
    if github:
        print("\nGitHub 層")
        for r in github:
            print(f"  {MARK[r.status]} {pad(r.name, col)}{r.detail}")
            if r.status == FAIL and r.fix:
                print(f"      → {r.fix}")

    all_r = core + github
    failed = [r for r in all_r if r.status == FAIL]
    warned = [r for r in all_r if r.status == WARN]
    print(f"\n通過 {sum(1 for r in all_r if r.status == PASS)} / "
          f"失敗 {len(failed)} / 注意 {len(warned)} / スキップ {sum(1 for r in all_r if r.status == SKIP)}")
    if failed:
        print("\n失敗した項目を直してから、もう一度実行すること。")
    print("\n自動で確認できないもの: 変更提案を 1 つ作り、CI が実際に緑になるかを見ること。")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
