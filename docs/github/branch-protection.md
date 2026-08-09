# ブランチ保護の設定

**読み手**: リポジトリの設定を変更できる権限を持つ人。

**CI は既定ではマージを止めない。** required status check として指定して初めて門になる。ブランチ保護はリポジトリの設定であってファイルではないため、テンプレートには同梱できない。リポジトリごとに設定する必要がある。

**順序に注意。** workflow が既定ブランチに入る前に required check を設定すると、報告されないチェックを待ち続けて変更提案が固まる。先に workflow をマージしてから設定すること。

## 設定

```
gh api -X PUT repos/{owner}/{repo}/branches/main/protection --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["gitleaks", "skillspector"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

Web UI なら Settings → Branches → Add branch protection rule で、Require status checks to pass before merging に上記のチェックを指定する。

## 各項目の意図

- `allow_force_pushes` と `allow_deletions` を false にしているのは、`AGENTS.md` の「バージョン管理の履歴を書き換えない」を規約だけでなく機械的にも守らせるため
- `required_pull_request_reviews` を `null` にしているのは、**個人アカウントのリポジトリでは自分の変更提案を承認できず、レビュー必須にすると自分でマージできなくなる**ため。**複数人で運用する組織のリポジトリでは、ここを設定すべき**。例: `{"required_approving_review_count": 1}`
- `enforce_admins` を false にしているのは緊急時の逃げ道を残すため。厳格に運用するなら true にする

## 注意

`contexts` の値は workflow の job id と一致している必要がある。job の名前を変えると、指定したチェックが永久に報告されず変更提案がマージできなくなる。

`security.yml` の job を減らした場合は、`contexts` からも該当名を外すこと。
