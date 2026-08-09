# エージェント向け指示ファイルを 2 つに複製する

> **Status: superseded by [0006](./0006-limit-copilot-surfaces.md)**
> 対象サーフェスを Copilot CLI と VS Code Chat に限定した結果、二重化の根拠が失われた。
> 記録として残すが、現在の構成には適用されない。

`AGENTS.md` と `.github/copilot-instructions.md` に同一内容を置き、CI で byte-identical を強制する。

## 背景

Copilot が読む指示ファイルは、サーフェス（Copilot CLI、GitHub.com の cloud agent、code review、各 IDE の Chat）ごとに異なる。`.github/copilot-instructions.md` は全サーフェスが読むが、`AGENTS.md` は JetBrains / Visual Studio / Xcode / Eclipse の **Chat** では読まれない。逆に `AGENTS.md` は Copilot 以外のツール（Zed、Codex、Claude Code）が読む事実上の標準になっている。どちらか一方だけでは穴が空く。

## 決定

両方を実体として置き、内容を byte-identical に保つ。`.github/workflows/sync-instructions.yml` が差分を検出して CI を失敗させる。Copilot CLI は複数の指示ファイルを読んで結合するが、内容が完全一致する重複は除去するため、指示が二重に注入されることはない。

## 却下した選択肢

- **symlink（`ln -s AGENTS.md .github/copilot-instructions.md`）** — Windows では symlink の作成に管理者権限または Developer Mode が必要で、テンプレートを複写した Windows 利用者の環境が壊れる。
- **`.github/copilot-instructions.md` に一本化** — Zed や Codex など `AGENTS.md` 規格を読むツールが何も読まなくなる。
- **`AGENTS.md` に一本化** — JetBrains / Visual Studio / Xcode / Eclipse の Chat 利用者に指示が届かない。
- **役割を分担して内容を重複させない** — 共通ルールを `AGENTS.md` にしか書かないと、上記 IDE の Chat 利用者に共通ルールが届かない。

## 帰結

- 指示を変更するときは 2 ファイルを必ず同時に更新する。片方だけの変更は CI で落ちる。
- `CLAUDE.md` はこの複製に含めない。Claude Code は `AGENTS.md` を読まないため、`AGENTS.md` を取り込む 1 行だけを置いている。これは Claude Code の公式ドキュメントが推奨する形。
