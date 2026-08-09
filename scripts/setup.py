#!/usr/bin/env python3
"""テンプレートを自分のプロジェクトのものにする。

README の「使い方」の手順を機械的に実行する。標準ライブラリのみを使う。

使い方:
    python3 scripts/setup.py                  # 対話的に尋ねる
    python3 scripts/setup.py --dry-run        # 何をするかだけ表示する
    python3 scripts/setup.py --name "受注管理" --desc "..." --no-github

実行後は python3 scripts/verify.py で確認すること。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

README_TEMPLATE = """# {name}

{desc}

## 開発に参加する

はじめての人は [docs/onboarding.md](docs/onboarding.md) を読むこと。

## 開発環境

（依存のインストール、テストの実行方法、ローカルでの起動方法を書く。）

## ライセンス

（このプロジェクトのライセンスを書く。）
"""

CONTEXT_TEMPLATE = """# {name}

**読み手**: エージェントと、ドメインの用語を決める人。

{desc}

## Language

> **この節はまだ空。** 用語が実際に問題になった時点で追記する。書き方の指針は次のとおり\
（書き始めたらこの引用ブロックを消す）。
>
> - 一般的なプログラミング用語は入れない。このプロジェクトに固有の概念だけを書く
> - 同じ概念を指す言葉が複数あるときは、使う語を 1 つ決めて残りを `_Avoid_` に列挙する
> - 定義は 1〜2 文。それが何で「ある」かを書き、何を「する」かは書かない
> - **先回りして埋めない**
>
> 書式の例。
>
> ```
> **注文**:
> 顧客が商品の購入を確定させた記録。支払いの成否とは独立して存在する。
> _Avoid_: オーダー、購入、トランザクション
> ```
>
> 詳細は `docs/agents/domain.md` を参照。
"""


class Plan:
    def __init__(self, dry: bool) -> None:
        self.dry = dry
        self.done: list[str] = []

    def rm(self, rel: str) -> None:
        p = ROOT / rel
        if not p.exists():
            return
        n = len(list(p.rglob("*"))) if p.is_dir() else 1
        self.done.append(f"削除 {rel}（{n} 件）")
        if not self.dry:
            shutil.rmtree(p) if p.is_dir() else p.unlink()

    def write(self, rel: str, text: str) -> None:
        self.done.append(f"書き換え {rel}")
        if not self.dry:
            (ROOT / rel).write_text(text, encoding="utf-8")

    def edit(self, rel: str, old: str, new: str, label: str) -> None:
        p = ROOT / rel
        if not p.exists():
            return
        t = p.read_text(encoding="utf-8")
        if old not in t:
            return
        self.done.append(f"{label} {rel}")
        if not self.dry:
            p.write_text(t.replace(old, new), encoding="utf-8")


def ask(prompt: str, default: str = "") -> str:
    try:
        v = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip()
    except EOFError:
        return default
    return v or default


def main() -> int:
    ap = argparse.ArgumentParser(description="テンプレートを自分のプロジェクトのものにする")
    ap.add_argument("--name", help="プロジェクト名")
    ap.add_argument("--desc", help="プロジェクトの説明（1〜2 文）")
    ap.add_argument("--no-github", action="store_true", help="GitHub 層を削除する")
    ap.add_argument("--keep-template-docs", action="store_true",
                    help="docs/template/ を残す（既定は削除）")
    ap.add_argument("--dry-run", action="store_true", help="実行せず、何をするかだけ表示する")
    args = ap.parse_args()

    interactive = sys.stdin.isatty() and not (args.name and args.desc)
    name = args.name or (ask("プロジェクト名") if interactive else "")
    desc = args.desc or (ask("何をするプロジェクトか（1〜2 文）") if interactive else "")
    if not name:
        print("プロジェクト名が必要。--name で渡すか、対話的に実行すること。", file=sys.stderr)
        return 2

    use_github = not args.no_github
    if interactive and not args.no_github:
        use_github = ask("GitHub を使うか (y/n)", "y").lower().startswith("y")

    p = Plan(args.dry_run)

    # 1. テンプレート本体の目印を消す。
    #    残すと verify.py がテンプレート向けの判定のままになり、
    #    雛形が埋まっていなくても緑になってしまう。
    p.rm(".template-repo")

    # 2. テンプレート自身の記録を消す
    if not args.keep_template_docs:
        p.rm("docs/template")

    # 2. README を自分のものにする
    p.write("README.md", README_TEMPLATE.format(name=name, desc=desc or "（何をするプロジェクトかを書く。）"))

    # 3. 用語集を自分のものにする（空の雛形。先回りして埋めない）
    p.write("CONTEXT.md", CONTEXT_TEMPLATE.format(name=name, desc=desc or "（このプロジェクトが何であり、なぜ存在するのかを 1〜2 文で書く。）"))

    # 4. ADR を空にする
    for f in sorted((ROOT / "docs" / "adr").glob("*.md")):
        if f.name != "README.md":
            p.rm(f"docs/adr/{f.name}")

    # 5. GitHub 層
    if not use_github:
        p.rm("docs/github")
        p.rm(".github/workflows/security.yml")
        p.rm(".github/scripts/check-skillspector.py")

    # 参加者ガイドの空欄は**自動で埋めない**。何を書くかは人間しか知らない。
    # 案内の引用ブロックもそのまま残す。埋める人への指示になっているため。

    # 6. AGENTS.md の構成表から、消したものの行を落とす
    removed_paths = ["`docs/template/`"] if not args.keep_template_docs else []
    if not use_github:
        removed_paths += ["`docs/github/`", "`.github/`"]
    if removed_paths:
        a = ROOT / "AGENTS.md"
        if a.exists():
            lines = a.read_text(encoding="utf-8").split("\n")
            kept = [ln for ln in lines if not (ln.startswith("| ") and any(x in ln for x in removed_paths))]
            if len(kept) != len(lines):
                p.done.append(f"AGENTS.md の構成表から {len(lines) - len(kept)} 行を削除")
                if not args.dry_run:
                    a.write_text("\n".join(kept), encoding="utf-8")

    head = "実行する内容（--dry-run）" if args.dry_run else "実行した内容"
    print(f"{head}\n")
    for d in p.done:
        print(f"  {d}")
    print(f"\n  {len(p.done)} 件")

    print("\n次にやること")
    n = 1
    print(f"  {n}. docs/onboarding.md の空欄 3 つ（説明・環境の立ち上げ方・相談先）を埋める"); n += 1
    print(f"  {n}. skill を導入する（docs/skills.md）"); n += 1
    print(f"     /setup-matt-pocock-skills は実行しないこと。この設定を上書きしてしまう"); 
    if use_github:
        print(f"  {n}. docs/github/ の手順でラベルとブランチ保護を設定する"); n += 1
    print(f"  {n}. python3 scripts/verify.py が通ることを確認する")
    print("\n  用語（CONTEXT.md）と設計決定（docs/adr/）は先回りして埋めないこと。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
