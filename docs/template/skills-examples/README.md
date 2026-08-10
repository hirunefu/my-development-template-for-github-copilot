# プロジェクト skill の例

**読み手**: `docs/skills-authoring.md` を読んで、実際に書き始める人。

3 つの型の実例。**ここに置いてある限り skill としては読み込まれない。** 動かすには `.claude/skills/` にコピーする必要がある。

| ディレクトリ | 型 | 何を見せているか |
| --- | --- | --- |
| `order-cancellation/` | ドメイン知識 | 用語を再定義せず `CONTEXT.md` を参照する書き方 |
| `database-migration/` | 独自ルール | 規約を守れないときの逃げ道を書く書き方 |
| `public-api-compat/` | レビュー観点 | 見るものを列挙し、見つけた後の扱いまで決める書き方 |

## 使い方

```
mkdir -p .claude/skills
cp -r docs/template/skills-examples/order-cancellation .claude/skills/
```

`.claude/skills/` はテンプレートには無い（自分で作る）。

コピーしたら**中身を全部書き換える。** 注文も課金も API もこのテンプレートの想定であって、あなたのドメインではない。例のままの語彙が残った skill を置くと、エージェントが他プロジェクトの用語を正典として扱う。

書き換える箇所。

- `name` — ディレクトリ名と一致させる
- `description` — **いつ**その skill を使うかを書く。ここが起動を決める
- 本文中の `CONTEXT.md` / `docs/adr/` への参照 — 実在するファイルに向ける。例のパスはそのままでは存在しない

## この例自体の扱い

`docs/template/` はテンプレート自身の記録なので、導入後に削除する（`docs/checklist.md` の項目 2）。例が不要になったらディレクトリごと消えてよい。
