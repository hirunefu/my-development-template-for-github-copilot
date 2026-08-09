# エージェント向け指示

コーディングエージェント（GitHub Copilot、Claude Code など）にこのリポジトリの前提を伝えるファイル。エージェントは起動時にこれを自動で読み込む。

## 言語

- ドキュメント、コミットメッセージ、コード内コメントはすべて**日本語**で書く
- 例外として、機械が照合する文字列は英語のまま維持する。ラベル名（`needs-triage` など）、`Status:` のような見出し語、識別子が該当する

## リポジトリ構成

| パス | 役割 |
| --- | --- |
| `AGENTS.md` | エージェント向け指示。このファイル |
| `CLAUDE.md` | `AGENTS.md` を取り込むだけ。Claude Code は `AGENTS.md` を読まないため |
| `CONTEXT.md` | このプロジェクトのドメイン用語集 |
| `docs/adr/` | このプロジェクトの設計決定とその理由 |
| `docs/agents/` | issue tracker とドメイン文書の運用規約（ホスティング非依存） |
| `docs/github/` | GitHub を使う場合の具体的な手順。使わないなら削除してよい |
| `docs/template/` | このテンプレート自体の設計記録。**プロジェクトの内容ではない** |

探索を始める前に `CONTEXT.md` と、触る領域に関わる `docs/adr/` を読む。存在しない、または中身が空の場合は黙って先に進む。詳細は `docs/agents/domain.md` を参照。

**`docs/template/` はこのテンプレート自身についての記録であり、このプロジェクトのドメインではない。** 用語や設計決定を探すときにここを参照しないこと。

## エージェントへの制約

以下は強制ではなく規約。守れない状況になったら作業を止めて人間に確認する。

- **バージョン管理の履歴を書き換えない** — force push、`git reset --hard`、`git clean -fdx`、push 済みコミットの rebase や amend
- **既定ブランチには変更提案（pull request / merge request）経由で入れる** — 直接 push しない
- **テスト・型チェック・lint を通すために無効化や条件緩和をしない** — 失敗はそのまま報告する
- **認証情報を出力・送信しない** — API キー、トークン、`.env` の中身を含む

## コミットメッセージ

Conventional Commits の形式に日本語の説明を組み合わせる。

```
<type>(<scope>): <日本語の要約>

<日本語の本文（任意）>
```

- `type` は `feat` / `fix` / `docs` / `refactor` / `test` / `chore` のいずれか
- `scope` は任意。変更範囲を示す（`docs(agents):` など）
- 要約は 1 行で、何を変えたかが分かる粒度にする

例:

```
feat: エージェント向け設定を追加
docs(agents): issue tracker を二層構成に変更
fix: カタログ生成が未知のカテゴリで停止しない問題を修正
```

## Agent skills

### Issue tracker

二層構成。探索（調査・設計）は `.scratch/`（バージョン管理外）、確定した実装タスクはプロジェクトのタスク管理に置く。skill ごとの振り分けは `docs/agents/issue-tracker.md` を参照。

### Triage labels

5 つの標準ロール（`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`）を使う。詳細は `docs/agents/triage-labels.md` を参照。

### Domain docs

single-context 構成。ルートの `CONTEXT.md` と `docs/adr/` を使う。詳細は `docs/agents/domain.md` を参照。
