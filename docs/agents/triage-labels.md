# Triage labels

skill 群は 5 つの標準 triage ロールで会話する。

| ロール | 意味 |
| --- | --- |
| `needs-triage` | メンテナが評価する必要がある |
| `needs-info` | 報告者からの追加情報を待っている |
| `ready-for-agent` | 仕様が確定し、AFK エージェントに渡せる |
| `ready-for-human` | 人間による実装が必要 |
| `wontfix` | 対応しない |

skill がロール名に言及したとき（例:「AFK-ready の triage ラベルを付ける」）は、この表のロール名をそのまま使う。

**トラッカー上で違う名前を使っている場合は、右側に対応列を足して読み替えを書く。** 既存プロジェクトに導入するときは、たいていこの作業が要る。

```
| ロール          | このプロジェクトでの名前 |
| --------------- | ------------------------ |
| `needs-triage`  | `triage/pending`         |
```

## 適用範囲

triage の対象はタスク管理側だけ。探索領域（`.scratch/`）のファイルは対象外（`issue-tracker.md` を参照）。

ラベルを実際に作成・付与する手順は、使用するトラッカーごとのファイルに書く。GitHub の場合は `docs/github/triage-labels.md`。
