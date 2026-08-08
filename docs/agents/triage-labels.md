# Triage labels

skill 群は 5 つの標準 triage ロールで会話する。このファイルは、それらのロールをこのリポジトリの GitHub Issues で実際に使うラベル文字列に対応づける。

| mattpocock/skills のラベル | このリポジトリでのラベル | 意味                                    |
| -------------------------- | ------------------------ | --------------------------------------- |
| `needs-triage`             | `needs-triage`           | メンテナが評価する必要がある            |
| `needs-info`               | `needs-info`             | 報告者からの追加情報を待っている        |
| `ready-for-agent`          | `ready-for-agent`        | 仕様が確定し、AFK エージェントに渡せる  |
| `ready-for-human`          | `ready-for-human`        | 人間による実装が必要                    |
| `wontfix`                  | `wontfix`                | 対応しない                              |

skill がロール名に言及したとき（例:「AFK-ready の triage ラベルを付ける」）は、この表の対応するラベル文字列を使う。

ラベルは GitHub 上の実体で、`gh issue edit <number> --add-label "<ラベル>"` で付与する。

## 新しいリポジトリでのラベル作成

このテンプレートから作ったリポジトリでは、最初に以下を実行してラベルを作る。

```
gh label create needs-triage    --description "メンテナが評価する必要がある"
gh label create needs-info      --description "報告者からの追加情報を待っている"
gh label create ready-for-agent --description "仕様が確定し、AFK エージェントに渡せる"
gh label create ready-for-human --description "人間による実装が必要"
gh label create wontfix         --description "対応しない" --force
```

`wontfix` は GitHub が新規リポジトリに既定で作るラベルなので、`--force` を付けて既存のものを上書きする。他の 4 つは既定に存在しないため `--force` は不要。

## 適用範囲

triage は GitHub Issues のみを対象とする。`.scratch/` 配下のファイルは triage の対象外（`issue-tracker.md` を参照）。

語彙を変えたい場合は表の右側の列を書き換える。
