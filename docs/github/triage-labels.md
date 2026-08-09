# GitHub でのラベル作成

`docs/agents/triage-labels.md` が定める 5 つの標準ロールを、GitHub のラベルとして作る手順。

## 作成

リポジトリを作った直後に一度だけ実行する。

```
gh label create needs-triage    --description "メンテナが評価する必要がある"
gh label create needs-info      --description "報告者からの追加情報を待っている"
gh label create ready-for-agent --description "仕様が確定し、AFK エージェントに渡せる"
gh label create ready-for-human --description "人間による実装が必要"
gh label create wontfix         --description "対応しない" --force
```

`wontfix` だけ `--force` が付いているのは、GitHub が新規リポジトリに同名のラベルを既定で作るため。既存のものを上書きする。他の 4 つは既定に存在しないので不要。

## 付与

```
gh issue edit <number> --add-label "<ラベル>"
```

## 確認

```
gh label list
```

5 つすべてが並んでいれば設定完了。
