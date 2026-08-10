# 導入後の確認

**読み手**: 導入作業を終えた人。

テンプレートから作った、あるいは既存プロジェクトに持ち込んだ後に一度だけ通す。**この確認は自動化されていない。** 抜けたまま運用されるのを防ぐ仕組みは無いので、必ず目視で通すこと。

GitHub を使う場合は、これに加えて `docs/github/checklist.md` も通す。

## 1. テンプレートの説明が残っていないか

```
grep -rln "エージェント向け開発テンプレート\|まだ実案件で運用されていない" --include='*.md' --exclude=checklist.md .
```

何もヒットしないこと。ヒットしたら、そのファイルはテンプレート自身の説明のまま残っている。README は自分のプロジェクトの説明に書き換える。

**書き換えるとき、「CI の検査」「analyzer の劣化で落ちたとき」「ツールのバージョン更新」の 3 節は残すこと。** CI が落ちたときの唯一の対処手順がここにある。

## 2. テンプレート自身の記録が残っていないか

```
ls docs/template/ 2>/dev/null
```

何も出ないこと。`docs/template/` はテンプレートの設計記録で、このプロジェクトのドメインではない。残すとエージェントが他プロジェクトの語彙を正典として扱う。

削除したら、それを指す記述も消えているか確認する。

```
grep -rn "docs/template" --include='*.md' --include='*.py' --include='*.yml' --exclude=checklist.md .
```

残ってよいのは「存在する場合は」のような条件付きの記述だけ。断定形で存在を前提にした記述が残っていたら直す。

## 3. 用語集が自分のものか

```
cat CONTEXT.md
```

他プロジェクトの用語が残っていないこと。雛形のまま（案内の引用ブロックだけ）でよい。**先回りして埋めない。**

## 4. ADR が空か

```
ls docs/adr/
```

`README.md` だけがあること。テンプレート由来の ADR が残っていたら消す。番号は `0001` から自分の決定に使う。

## 5. 探索領域が除外されているか

```
grep -n "scratch" .gitignore
```

`/.scratch/` があること。無いと調査中のメモがコミットされる。

## 6. 帰属表示が残っているか

```
ls NOTICE
```

`docs/agents/` などテンプレート由来のファイルを残しているなら `NOTICE` も残す。MIT の条件は複写のたびに引き継がれる。

## 7. 参加者ガイドが埋まっているか

```
grep -n "（このプロジェクト\|（何を作って\|（相談先" docs/onboarding.md
```

何もヒットしないこと。ヒットしたら空欄が残っている。埋める箇所は 4 つ。

- 「このプロジェクト」— 何を作っているのか
- 「2. 開発環境」— 立ち上げ方と、**コードがどのディレクトリにあるか**
- 「作業する」の表 — タスク管理がどこか
- 「詰まったら」— 相談先

**参加者が最初に読むファイルなので、空欄のまま渡さない。** 空欄は消すのではなく埋めること。消すと参加者は何も分からなくなる。

埋めたら、**そのプロジェクトを知らない人に読ませて、実際に環境を立ち上げてもらう。** 立ち上がらなければ、そのガイドはまだ完成していない。

## 8. 相対リンクが切れていないか

```
grep -rn --include='*.md' --exclude=checklist.md -o ']([^)#]*)' . | while IFS= read -r line; do
  f=${line%%:*}; link=${line##*](}; t=${link%)}
  case "$t" in http*|mailto:*|"") continue;; esac
  [ -e "$(dirname "$f")/$t" ] || echo "切れ: $f -> $t"
done
```

**bash で実行すること**（zsh では `](` の展開に失敗する）。

何も出ないこと。**文書を移動・削除したときに残る。** 飛ばすと、参加者が案内された先に何も無い状態になる。

## 9. git hook が有効か

```
git config --get core.hooksPath
```

`.githooks` が出ること。出なければ次を実行する。

```
git config core.hooksPath .githooks
chmod +x .githooks/*
```

**`core.hooksPath` は clone ごとの設定。** 参加者全員が実行する必要があるので `docs/onboarding.md` に書いてある。

## 10. skill が見えているか

skill を使う場合のみ。

```
copilot skill list
```

Personal skills として一覧が出ること（`code-review` や `domain-modeling` など）。Claude Code なら `/` を入力して候補に出るか確認する。導入手順は `docs/skills.md`。

自分で書いた skill を `.claude/skills/` に置いた場合は、同じ一覧に Project skills として並ぶ。テンプレート付属の例（`order-cancellation` / `database-migration` / `public-api-compat`）を名前も中身も書き換えずに置いていないか確認する。書き方は `docs/skills-authoring.md`。
