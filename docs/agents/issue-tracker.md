# Issue tracker: 二層構成

このプロジェクトは作業の置き場所を 2 つ使い分ける。

- **探索領域** — `.scratch/`。バージョン管理外（`.gitignore` 済み）。答えがまだ確定していない調査・設計・プロトタイプを置く
- **タスク管理** — 実装タスクと triage の対象。プロジェクトが使うトラッカー（GitHub Issues、GitLab Issues、Jira など）

**タスク管理側の具体的な操作方法は、使用するトラッカーごとのファイルに書く。** GitHub Issues を使う場合は `docs/github/issue-tracker.md`。

## skill ごとの振り分け

| skill | 保存先 |
| --- | --- |
| `/to-spec` | 探索領域 |
| `/wayfinder` | 探索領域 |
| `/grilling` | 探索領域 |
| `/to-tickets` | タスク管理 |
| `/triage` | タスク管理 |

**この表にない skill が「issue tracker に publish する」と言った場合は、自分で判断せず人間に確認する。**

## skill が「issue tracker に publish する」と言ったとき

上の表で保存先を決める。探索領域なら `.scratch/<slug>/` 配下にファイルを作る（ディレクトリが無ければ作成する）。タスク管理ならトラッカー側のファイルに書かれた作成手順に従う。

## skill が「該当チケットを取得する」と言ったとき

参照がパスならそのファイルを読む。チケット番号ならトラッカー側の参照手順に従う。

---

## 探索領域（`.scratch/`）の規約

バージョン管理外なので、コミットもプッシュもしない。個人のマシン上にのみ存在する。ここで確定した内容は、用語なら `CONTEXT.md`、設計決定なら `docs/adr/`、実装作業ならタスク管理に移す。

- 1 つの取り組みにつき 1 ディレクトリ: `.scratch/<slug>/`
- spec（PRD と呼ぶこともある）は `.scratch/<slug>/spec.md`
- コメントや会話履歴はファイル末尾の `## Comments` 見出しの下に追記する

### Wayfinding operations

`/wayfinder` が使う。**map** は 1 チケットにつき 1 つの **child** ファイルを持つファイル。

- **Map**: `.scratch/<slug>/map.md` — Notes / Decisions-so-far / Fog の本体
- **Child ticket**: `.scratch/<slug>/issues/NN-<slug>.md`。`01` から連番で、本文に問いを書く。`Type:` 行にチケット種別（`research`/`prototype`/`grilling`/`task`）、`Status:` 行に `claimed`/`resolved` を記録する
- **Blocking**: 冒頭付近の `Blocked by: NN, NN` 行。列挙された全ファイルが `resolved` になった時点でブロック解除
- **Frontier**: `.scratch/<slug>/issues/` を走査し、open かつ unblocked かつ unclaimed のファイルを探す。番号の小さいものが優先
- **Claim**: 作業前に必ず `Status: claimed` に設定して保存する
- **Resolve**: `## Answer` 見出しの下に答えを追記し、`Status: resolved` に設定。その後 `map.md` の Decisions-so-far に context pointer（要約とリンク）を追記する
