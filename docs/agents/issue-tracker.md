# Issue tracker: ローカル markdown

このリポジトリの issue と spec（PRD と呼ぶこともある）は、`.scratch/` 配下の markdown ファイルとして管理する。

## 規約

- 1 feature = 1 ディレクトリ: `.scratch/<feature-slug>/`
- spec は `.scratch/<feature-slug>/spec.md`
- 実装 issue は 1 チケット 1 ファイルで `.scratch/<feature-slug>/issues/<NN>-<slug>.md`。`01` から連番。複数チケットを 1 ファイルにまとめてはいけない
- triage の状態は各 issue ファイル冒頭付近の `Status:` 行に記録する（ロール文字列は `triage-labels.md` を参照）
- コメントや会話履歴はファイル末尾の `## Comments` 見出しの下に追記する

## skill が「issue tracker に publish する」と言ったとき

`.scratch/<feature-slug>/` 配下に新しいファイルを作る（ディレクトリが無ければ作成する）。

## skill が「該当チケットを取得する」と言ったとき

参照されたパスのファイルを読む。通常はユーザーがパスか issue 番号を直接渡す。

## Wayfinding operations

`/wayfinder` が使う。**map** は 1 チケットにつき 1 つの **child** ファイルを持つファイル。

- **Map**: `.scratch/<effort>/map.md` — Notes / Decisions-so-far / Fog の本体。
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`。`01` から連番で、本文に問いを書く。`Type:` 行にチケット種別（`research`/`prototype`/`grilling`/`task`）、`Status:` 行に `claimed`/`resolved` を記録する。
- **Blocking**: 冒頭付近の `Blocked by: NN, NN` 行。列挙された全ファイルが `resolved` になった時点でブロック解除。
- **Frontier**: `.scratch/<effort>/issues/` を走査し、open かつ unblocked かつ unclaimed のファイルを探す。番号の小さいものが優先。
- **Claim**: 作業前に必ず `Status: claimed` に設定して保存する。
- **Resolve**: `## Answer` 見出しの下に答えを追記し、`Status: resolved` に設定。その後 `map.md` の Decisions-so-far に context pointer（要約とリンク）を追記する。
