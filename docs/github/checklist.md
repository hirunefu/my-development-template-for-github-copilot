# GitHub 層のセットアップ確認

導入後に一度だけ実行して、手順の抜けが無いかを確かめる。**この確認は自動化されていない。** 抜けたまま運用されることを防ぐ仕組みは無いので、必ず目視で通すこと。

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

上の出力と、`.github/workflows/security.yml` の `jobs:` 直下のキーを見比べる。食い違っていると、変更提案が永久にマージできなくなる。

## 5. テンプレートの残りカスが消えているか

```
grep -rl "my-development-template-for-github-copilot" --include='*.md' .
ls docs/template/ 2>/dev/null
```

前者は README のタイトルなどにテンプレート名が残っていないかの確認。後者は `docs/template/`（テンプレート自身の設計記録）を消したかの確認。**複写先には不要なので削除する。**

## 6. 用語集と ADR が空か

```
cat CONTEXT.md
ls docs/adr/
```

`CONTEXT.md` に他プロジェクトの用語が残っていないこと。`docs/adr/` に `README.md` 以外が無いこと。残っていると、エージェントが他プロジェクトの語彙をこのプロジェクトの正典として扱う。
