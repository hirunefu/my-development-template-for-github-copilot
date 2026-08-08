# Issue tracker: 二層構成

このリポジトリは issue の置き場所を 2 つ使い分ける。

- **`.scratch/`** — 個人の探索領域。git 管理外（`.gitignore` 済み）。答えがまだ確定していない調査・設計・プロトタイプを置く
- **GitHub Issues** — 実装タスクと triage の対象。`gh` CLI で操作する

## skill ごとの振り分け

| skill | 保存先 |
| --- | --- |
| `/to-spec` | `.scratch/` |
| `/wayfinder` | `.scratch/` |
| `/grilling` | `.scratch/` |
| `/to-tickets` | GitHub Issues |
| `/triage` | GitHub Issues |

**この表にない skill が「issue tracker に publish する」と言った場合は、自分で判断せず人間に確認する。**

## skill が「issue tracker に publish する」と言ったとき

上の表で保存先を決める。`.scratch/` なら `.scratch/<slug>/` 配下にファイルを作る（ディレクトリが無ければ作成する）。GitHub Issues なら `gh issue create` する。

## skill が「該当チケットを取得する」と言ったとき

参照が `#<番号>` の形なら `gh issue view <番号> --comments`。パスならそのファイルを読む。

---

## `.scratch/` の規約

git 管理外なので、コミットもプッシュもしない。個人のマシン上にのみ存在する。ここで確定した内容は、用語なら `CONTEXT.md`、設計決定なら `docs/adr/`、実装作業なら GitHub Issues に移す。

- 1 つの取り組みにつき 1 ディレクトリ: `.scratch/<slug>/`
- spec（PRD と呼ぶこともある）は `.scratch/<slug>/spec.md`
- コメントや会話履歴はファイル末尾の `## Comments` 見出しの下に追記する

### Wayfinding operations

`/wayfinder` が使う。**map** は 1 チケットにつき 1 つの **child** ファイルを持つファイル。

- **Map**: `.scratch/<effort>/map.md` — Notes / Decisions-so-far / Fog の本体
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`。`01` から連番で、本文に問いを書く。`Type:` 行にチケット種別（`research`/`prototype`/`grilling`/`task`）、`Status:` 行に `claimed`/`resolved` を記録する
- **Blocking**: 冒頭付近の `Blocked by: NN, NN` 行。列挙された全ファイルが `resolved` になった時点でブロック解除
- **Frontier**: `.scratch/<effort>/issues/` を走査し、open かつ unblocked かつ unclaimed のファイルを探す。番号の小さいものが優先
- **Claim**: 作業前に必ず `Status: claimed` に設定して保存する
- **Resolve**: `## Answer` 見出しの下に答えを追記し、`Status: resolved` に設定。その後 `map.md` の Decisions-so-far に context pointer（要約とリンク）を追記する

---

## GitHub Issues の規約

すべて `gh` CLI で操作する。対象リポジトリは `git remote -v` から自動で解決される。

- **作成**: `gh issue create --title "..." --body "..."`。複数行の本文は heredoc を使う
- **読む**: `gh issue view <number> --comments`
- **一覧**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`。必要に応じて `--label` と `--state` で絞る
- **コメント**: `gh issue comment <number> --body "..."`
- **ラベルの付与と削除**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **クローズ**: `gh issue close <number> --comment "..."`

triage ラベルの語彙は `triage-labels.md` を参照。

### PR を要求の受信口として扱うか

**PRs as a request surface: no.** _(このリポジトリが外部 PR を機能要求として扱う場合は `yes` に変更する。`/triage` がこのフラグを読む。)_

`yes` にした場合、PR は issue と同じラベルと状態で処理される。`gh pr view` / `gh pr diff` / `gh pr comment` / `gh pr edit --add-label` / `gh pr close` を使う。GitHub は issue と PR で番号空間を共有するので、裸の `#42` はどちらの可能性もある。`gh pr view 42` を試し、失敗したら `gh issue view 42` に落とす。

### Copilot cloud agent に渡す

`ready-for-agent` ラベルが付いた issue は、GitHub 上で Copilot を assignee に指定することで cloud agent が着手できる。agent はブランチを作り、必要に応じて pull request を作成する。
