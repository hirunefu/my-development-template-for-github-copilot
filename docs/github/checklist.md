# GitHub 層のセットアップ確認

**読み手**: GitHub 層を導入した人。`docs/checklist.md` と併せて通す。

GitHub を使う場合に、`docs/checklist.md`（ホスティング非依存の確認）に加えて通す項目。

## 1. workflow が動いているか

```
gh run list --limit 5
```

`security.yml` の実行が並んでいること。1 件も無ければ、まだ push していないか、`.github/workflows/` に置かれていない。

## 2. ラベルが作られているか

```
gh label list
```

`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix` の 5 つが並んでいること。手順は `triage-labels.md`。

## 3. ブランチ保護が効いているか

```
gh api repos/{owner}/{repo}/branches/main/protection --jq '.required_status_checks.contexts'
```

`security.yml` の job 名が並んでいること。**404 が返るなら保護が設定されていない。** その状態では CI が赤くてもマージできる。手順は `branch-protection.md`。

## 4. required check の名前が一致しているか

```
gh api repos/{owner}/{repo}/branches/main/protection --jq '.required_status_checks.contexts[]'
awk '/^jobs:/{j=1;next} j && /^[a-zA-Z]/{exit} j && /^  [a-z0-9_-]+:$/{gsub(/[ :]/,"");print}' .github/workflows/security.yml
```

2 つの出力が一致すること。**食い違っていると、報告されないチェックを待って変更提案が永久にマージできなくなる。**

**job を減らしたときは required check からも外すこと。** 順序を誤ると同じ状態になる。逆に job を増やしたときは、**その job が実際に緑になってから** required に加える。

## 5. CI が実際に緑になるか

required status check にする**前に**、変更提案を 1 つ作って CI を走らせ、緑になることを確認する。既存プロジェクトに導入した場合はとくに重要で、既存のバイナリ資産が原因で `skillspector` が落ちることがある。対処は `README.md` の「analyzer の劣化で落ちたとき」を参照。
