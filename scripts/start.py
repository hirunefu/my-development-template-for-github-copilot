#!/usr/bin/env python3
"""このプロジェクトで作業できる状態にする。

参加した人が最初に 1 回、新しいマシンに移ったときにもう 1 回実行する。
標準ライブラリのみを使う。

使い方:
    python3 scripts/start.py            # 準備して案内を出す
    python3 scripts/start.py --check    # 変更せず、準備できているかだけ見る
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OK, NG, INFO, WARN = "✓", "✗", "·", "!"


def width(s: str) -> int:
    """表示幅を求める。日本語は 1 文字で 2 桁を占める。"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s: str, to: int) -> str:
    return s + " " * max(0, to - width(s))


def run(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.SubprocessError):
        return 127, ""


class Report:
    def __init__(self) -> None:
        self.lines: list[tuple[str, str, str]] = []
        self.todo: list[str] = []
        self.notes: list[str] = []

    def add(self, mark: str, what: str, detail: str = "") -> None:
        self.lines.append((mark, what, detail))

    def need(self, instruction: str) -> None:
        self.todo.append(instruction)

    def note(self, text: str) -> None:
        self.notes.append(text)


def ensure_hooks(rep: Report, check_only: bool) -> None:
    hooks_dir = ROOT / ".githooks"
    if not hooks_dir.exists():
        rep.add(INFO, "git hook", ".githooks/ が無いので設定しない")
        return
    inside, _ = run(["git", "rev-parse", "--git-dir"])
    if inside != 0:
        rep.add(INFO, "git hook", "git リポジトリではないので設定しない")
        return
    code, out = run(["git", "config", "--get", "core.hooksPath"])
    current = out.strip()
    if current == ".githooks":
        if (ROOT / ".jj").exists():
            rep.add(WARN, "git hook", "設定済み。ただし jj からの push には効かない")
            rep.note("`jj git push` は git hook を実行しない。jj を使う場合、"
                     "既定ブランチへの直接 push と履歴の書き換えは自分で避けること")
        else:
            rep.add(OK, "git hook", "履歴の書き換えと既定ブランチへの直接 push を止める")
        return
    if check_only:
        rep.add(NG, "git hook", "未設定")
        rep.need("git config core.hooksPath .githooks")
        return
    code, _ = run(["git", "config", "core.hooksPath", ".githooks"])
    if code == 0:
        for h in hooks_dir.iterdir():
            if h.is_file():
                h.chmod(h.stat().st_mode | 0o111)
        rep.add(OK, "git hook", "設定した")
    else:
        rep.add(NG, "git hook", "設定できなかった")
        rep.need("git config core.hooksPath .githooks")


def ensure_scratch(rep: Report, check_only: bool) -> None:
    d = ROOT / ".scratch"
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    if "/.scratch/" not in gi:
        rep.add(NG, "探索領域", ".gitignore に /.scratch/ が無い")
        rep.need("`.gitignore` に `/.scratch/` を足す（調査中のメモがコミットされてしまう）")
        return
    if d.exists():
        rep.add(OK, "探索領域", ".scratch/（バージョン管理外）")
        return
    if check_only:
        rep.add(INFO, "探索領域", "まだ作られていない（使うときに作られる）")
        return
    d.mkdir(exist_ok=True)
    (d / ".gitkeep").touch()
    rep.add(OK, "探索領域", ".scratch/ を作った")


def check_skills(rep: Report) -> None:
    personal = Path.home() / ".agents" / "skills"
    n = len([x for x in personal.iterdir() if x.is_dir()]) if personal.exists() else 0
    if n:
        rep.add(OK, "個人 skill", f"{n} 件が導入済み")
    else:
        rep.add(NG, "個人 skill", "未導入")
        rep.need("npx skills@1.5.22 add mattpocock/skills -g   （詳細は docs/skills.md）")

    proj = ROOT / ".claude" / "skills"
    if proj.exists():
        m = len([x for x in proj.iterdir() if x.is_dir()])
        rep.add(OK, "プロジェクト skill", f"{m} 件（clone に含まれる。導入は不要）")


def check_agents(rep: Report) -> None:
    found = [n for n, c in (("Copilot CLI", "copilot"), ("Claude Code", "claude")) if shutil.which(c)]
    if found:
        rep.add(OK, "エージェント", " / ".join(found))
    else:
        rep.add(INFO, "エージェント", "この端末では見つからない（エディタ内で使うなら問題ない）")


def check_guide_usable(rep: Report) -> None:
    """参加者ガイドが使える状態か。

    検査の実体は verify.py にある。ここで書き直すと片方だけ古くなる。
    ガイドが白紙のまま「準備できた」と言うと、参加者は準備が終わったと
    信じたまま何も分からない状態に置かれる。
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import verify  # noqa: E402
    except Exception:
        rep.add(INFO, "参加者ガイド", "scripts/verify.py が読めないので確認しない")
        return
    r = verify.check_onboarding_filled()
    if r.status == verify.PASS:
        rep.add(OK, "参加者ガイド", r.detail or "使える状態")
    elif r.status == verify.SKIP:
        rep.add(INFO, "参加者ガイド", r.detail)
    elif r.status == verify.WARN:
        rep.add(OK, "参加者ガイド", r.detail)
    else:
        rep.add(NG, "参加者ガイド", r.detail)
        rep.need("**このリポジトリはまだ参加者を受け入れられる状態ではない。** "
                 "メンテナに docs/onboarding.md を埋めてもらうこと")


def check_instructions(rep: Report) -> None:
    if (ROOT / "AGENTS.md").exists():
        rep.add(OK, "エージェント設定", "AGENTS.md（起動時に自動で読まれる）")
    else:
        rep.add(NG, "エージェント設定", "AGENTS.md が無い")
        rep.need("**AGENTS.md が無い。** エージェントはこのプロジェクトの前提を何も知らない状態で動く。"
                 "メンテナに確認すること")


def where_work_goes() -> str:
    return """作業の置き場所は 2 つだけ。

  やることが決まっていない  →  .scratch/          あなたのマシンにしか無い。消えてよい
  やることが決まった        →  タスク管理         チームに見える

  用語が固まったら CONTEXT.md、設計判断が固まったら docs/adr/ に移す。
  迷ったら .scratch/ に置く。後から動かせる。"""


def main() -> int:
    ap = argparse.ArgumentParser(description="このプロジェクトで作業できる状態にする")
    ap.add_argument("--check", action="store_true", help="変更せず、準備できているかだけ見る")
    args = ap.parse_args()

    rep = Report()
    check_instructions(rep)
    check_guide_usable(rep)
    check_agents(rep)
    check_skills(rep)
    ensure_hooks(rep, args.check)
    ensure_scratch(rep, args.check)

    print("準備の状態\n")
    w = max(width(x[1]) for x in rep.lines) + 2
    for mark, what, detail in rep.lines:
        print(f"  {mark} {pad(what, w)}{detail}")

    if rep.notes:
        print("\n注意")
        for n in rep.notes:
            print(f"  · {n}")

    if rep.todo:
        print("\nやること")
        for i, t in enumerate(rep.todo, 1):
            print(f"  {i}. {t}")
        print("\n  済んだらもう一度 python3 scripts/start.py を実行すること。")
        return 1

    print("\n準備できた。\n")
    print(where_work_goes())
    print("\n  作業を始めるときは、エージェントにタスクをそのまま伝えればよい。")
    print("  進め方はエージェント側が知っている（AGENTS.md と skill を読む）。")
    print("\n  困ったとき、詳しい流れ: docs/onboarding.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
