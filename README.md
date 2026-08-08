# my-development-template-for-github-copilot

コーディングエージェント（GitHub Copilot、Claude Code など）にプロジェクトの前提を伝える設定を、再利用可能な形でまとめた開発テンプレート。コードそのものではなく「エージェントとの働き方」を配布する。

技術スタックには依存しない。どの言語・どのフレームワークのプロジェクトにも適用できる。

## 使い方

1. GitHub の **Use this template** から新しいリポジトリを作る
2. triage ラベルを作成する（コマンドは `docs/agents/triage-labels.md` にある）
3. `AGENTS.md` をプロジェクトに合わせて調整する。**変更したら `.github/copilot-instructions.md` にも同じ内容をコピーする**（CI が一致を検査する）
4. 用語が固まったら `CONTEXT.md`、設計を決めたら `docs/adr/` に追記する。先回りして空のファイルを作る必要はない

## 収録物

| パス | 内容 |
| --- | --- |
| `AGENTS.md` | エージェント向け指示の実体。言語ルール、リポジトリ構成、制約、コミット規約 |
| `.github/copilot-instructions.md` | 上と同一内容。IDE の Copilot Chat が読むのはこちらだけ |
| `CLAUDE.md` | `AGENTS.md` を取り込む 1 行。Claude Code 専用 |
| `CONTEXT.md` | ドメイン用語集 |
| `docs/adr/` | 設計決定とその理由の記録 |
| `docs/agents/` | issue tracker、triage ラベル、ドメイン文書の運用規約 |
| `.github/workflows/sync-instructions.yml` | 指示ファイル 2 つの同期を検査する CI |

なぜ指示ファイルが 2 つあるのかは `docs/adr/0001-duplicate-instruction-files.md` に記録してある。

## 意図的に入れていないもの

| 対象 | 理由 |
| --- | --- |
| `.github/instructions/*.instructions.md` | `applyTo` で紐づける対象のコードがテンプレートに存在しない。プロジェクトにコードが入った時点で追加する |
| `.github/workflows/copilot-setup-steps.yml` | インストールする依存が存在しない。スタックが決まった時点で追加する |
| `.claude/settings.json` | 制約は規約として書く方針にした。機械的な強制が必要になったら追加する |

## ドキュメントの言語

日本語で書く。想定利用者が日本語話者のチームだから。公開リポジトリだが、公開は配布手段であって言語を英語にする理由にはならない。詳細は `AGENTS.md` の「言語」節を参照。
