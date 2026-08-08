# Domain docs

エンジニアリング系 skill が、コードベースを探索するときにこのリポジトリのドメインドキュメントをどう読むべきかを定める。

ここで言うドメインドキュメントは 2 種類ある。

- **`CONTEXT.md`** — このプロジェクト固有の用語集。同じ概念を指す言葉が複数あるとき、どれを使うかを決めてある
- **`docs/adr/`** — 設計決定とその理由の記録（Architecture Decision Record）。「なぜこうなっているのか」を後から読む人に伝えるためのもの

## 探索の前に読むもの

- ルートの **`CONTEXT.md`**、または
- ルートに **`CONTEXT-MAP.md`** があればそれ（context ごとの `CONTEXT.md` を指している）。トピックに関係するものをすべて読む。
- **`docs/adr/`** — これから触る領域に関わる ADR を読む。multi-context リポジトリでは `src/<context>/docs/adr/` の context 固有の決定も確認する。

これらのファイルが存在しない場合は**黙って先に進む**。不在を指摘したり、先回りして作成を提案したりしない。`/domain-modeling` skill（`/grill-with-docs` や `/improve-codebase-architecture` から到達する）が、用語や決定が実際に確定した時点で遅延的に作成する。

## ファイル構成

このリポジトリは **single-context** 構成:

```
/
├── CONTEXT.md
├── docs/adr/
│   └── 0001-duplicate-instruction-files.md
└── src/
```

将来リポジトリが複数の context に分かれたら、ルートに `CONTEXT-MAP.md` を置き、`src/<context>/CONTEXT.md` と `src/<context>/docs/adr/` に分割する（その場合ルートの `docs/adr/` はシステム全体の決定を持つ）。

## glossary の語彙を使う

出力がドメイン概念に言及するとき（issue のタイトル、リファクタ提案、仮説、テスト名など）は、`CONTEXT.md` で定義された用語を使う。glossary が明示的に避けている同義語に流れないこと。

必要な概念が glossary に無い場合、それはシグナル。プロジェクトが使っていない語彙を発明しているか（再考せよ）、本当にギャップがあるか（`/domain-modeling` 用に記録せよ）のどちらか。

## ADR との衝突を明示する

出力が既存の ADR と矛盾する場合、黙って上書きせず明示的に指摘する:

> _ADR-0001（指示ファイルの複製）と矛盾する。ただし再検討の価値があるのは……_
