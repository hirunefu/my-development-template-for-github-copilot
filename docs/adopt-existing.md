# 既存プロジェクトへの導入

既に動いているリポジトリにこのテンプレートを持ち込む手順。新規リポジトリを作る場合は `README.md` の「使い方」を参照。

**この手順は自動化されていない。** ファイルを手で置き、既存の運用と噛み合わない部分を手で直す。抜けを検出する仕組みは無いので、最後の確認は目視で行う。

## 方針

**全部を持ち込まない。** 既存プロジェクトには既に独自の運用があり、テンプレートの規約と衝突する。持ち込むのは次の 3 つだけにする。

| 持ち込む | パス |
| --- | --- |
| エージェント向け指示 | `AGENTS.md`、`CLAUDE.md` |
| ドメイン文書の置き場所 | `CONTEXT.md`（雛形）、`docs/adr/` |
| 運用規約の汎用部分 | `docs/agents/` |

残りは任意。CI（`.github/`）と GitHub 層（`docs/github/`）と skill の導入手順（`docs/skills.md`）は、必要になった時点で足す。

## 手順

### 1. コアを置く

このテンプレートから 4 つをコピーする。

```
AGENTS.md
CLAUDE.md
CONTEXT.md
docs/agents/
docs/adr/README.md
```

**`docs/template/` はコピーしない。** テンプレート自身の設計記録であり、あなたのプロジェクトのドメインではない。

### 2. 既存の指示ファイルと突き合わせる

既に `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md`、`.cursorrules` などがある場合は、**上書きせずに内容を統合する**。既存の記述の方がそのプロジェクトの実態に合っている可能性が高い。

とくに次の 3 節は必ず読み合わせる。

- **言語** — テンプレートは日本語固定。プロジェクトの慣習に合わせて書き換える
- **エージェントへの制約** — 既存の運用と矛盾しないか確認する。例えば既定ブランチへの直接 push を許している運用なら、その行を消すか運用を変えるかを決める
- **コミットメッセージ** — 既存の履歴と規約が違うなら、既存に合わせる

### 3. issue tracker の記述を実態に合わせる

`docs/agents/issue-tracker.md` は「探索領域」と「タスク管理」の二層を定義している。

- **タスク管理側** — 使っているトラッカーの操作方法を書く。GitHub Issues なら `docs/github/issue-tracker.md` をコピーする。それ以外なら同じ形式で自分で書く
- **ラベル** — `docs/agents/triage-labels.md` の 5 ロールを、既存のラベル名に読み替える表を足す。既存プロジェクトではたいていこの作業が要る

### 4. `.scratch/` を `.gitignore` に足す

```
/.scratch/
```

既存の `.gitignore` に追記する。これを忘れると探索中のメモがコミットされる。

### 5. `CONTEXT.md` を埋めない

雛形のまま置く。**先回りして用語を書かない。** 用語が実際に問題になった時点で `/domain-modeling` が追記する。

既にドメイン用語をまとめた文書がプロジェクトにあるなら、`CONTEXT.md` に移すか、`AGENTS.md` の構成表からそちらを指すように書き換える。

### 6. skill を導入する（任意）

`docs/skills.md` を参照。skill を使わない場合でも `AGENTS.md` と `CONTEXT.md` は機能するが、`docs/agents/` の振り分け表は意味を持たなくなる。

### 7. CI を足す（任意）

`.github/workflows/security.yml` と `.github/scripts/check-skillspector.py` をコピーする。既存の CI がある場合は、ジョブを追加する形にする。

追加したら `docs/github/branch-protection.md` に従って required status check を設定する。**これを省くと CI は赤い印を付けるだけで、マージを止められない。**

## 確認

`docs/github/checklist.md` の項目を上から通す。GitHub 以外を使っている場合は該当項目を読み替える。
