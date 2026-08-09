# GitHub Issues をタスク管理に使う

`docs/agents/issue-tracker.md` が定める二層構成のうち、**タスク管理側**を GitHub Issues で実装する場合の具体的な操作。

GitHub を使わないプロジェクトでは、このファイルを削除して、使用するトラッカーの操作方法を同じ形式で書く。

## 操作

すべて `gh` CLI で行う。対象リポジトリは `git remote -v` から自動で解決される。

- **作成**: `gh issue create --title "..." --body "..."`。複数行の本文は heredoc を使う
- **読む**: `gh issue view <number> --comments`
- **一覧**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`。必要に応じて `--label` と `--state` で絞る
- **コメント**: `gh issue comment <number> --body "..."`
- **ラベルの付与と削除**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **クローズ**: `gh issue close <number> --comment "..."`

ラベルの語彙は `docs/agents/triage-labels.md`、作成手順は `triage-labels.md`（このディレクトリ）を参照。

## 参照の解決

skill が `#<番号>` の形で参照したときは `gh issue view <番号> --comments` を実行する。

GitHub は issue と pull request で番号空間を共有するので、裸の `#42` はどちらの可能性もある。`gh pr view 42` を試し、失敗したら `gh issue view 42` に落とす。

## pull request を要求の受信口として扱うか

**PRs as a request surface: no.** _(このリポジトリが外部 PR を機能要求として扱う場合は `yes` に変更する。`/triage` がこのフラグを読む。)_

`yes` にした場合、PR は issue と同じラベルと状態で処理される。`gh pr view` / `gh pr diff` / `gh pr comment` / `gh pr edit --add-label` / `gh pr close` を使う。
