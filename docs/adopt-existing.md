# 既存プロジェクトへの導入

既に動いているリポジトリにこのテンプレートを持ち込む手順。新規リポジトリを作る場合は `README.md` の「使い方」を参照。

**この手順は自動化されていない。** ファイルを手で置き、既存の運用と噛み合わない部分を手で直す。抜けを検出する仕組みは無いので、最後の確認は目視で行う。

## 方針

**全部を持ち込まない。** 既存プロジェクトには既に独自の運用があり、テンプレートの規約と衝突する。持ち込むのは次の 3 分類だけにする。

| 持ち込む | パス |
| --- | --- |
| エージェント向け指示 | `AGENTS.md`、`CLAUDE.md` |
| ドメイン文書の置き場所 | `CONTEXT.md`（雛形）、`docs/adr/README.md` |
| 運用規約の汎用部分 | `docs/agents/`、`docs/skills.md`、`NOTICE` |

残りは任意。CI（`.github/`）と GitHub 層（`docs/github/`）は、必要になった時点で足す。

`docs/skills.md` をコアに含めるのは、`docs/agents/` が skill 名を前提にしているため。skill を使わない場合でも、**なぜその振り分け表があるのかを説明する文書が無いと `docs/agents/` が意味不明になる**。

## 手順

### 1. コアを置く

**先に、同名のファイルが既にあるかを確認する。**

```
ls AGENTS.md CLAUDE.md CONTEXT.md NOTICE .github/copilot-instructions.md 2>/dev/null
```

**存在するものは上書きしないこと。** 別名（`AGENTS.md.new` など）で置くか、いったん退避してから手順 2 で統合する。ここで上書きすると、統合すべき既存の内容が消える。

そのうえで次をコピーする。

```
AGENTS.md
CLAUDE.md
CONTEXT.md
NOTICE
docs/agents/
docs/adr/README.md
docs/checklist.md
docs/skills.md
```

`NOTICE` を含めるのは、`docs/agents/` が MIT の上流テンプレートからの派生物だから。**残す限り帰属表示も一緒に持ち込む必要がある。** 導入先に既に `NOTICE` がある場合は、その節を追記する形にする。

**`docs/template/` はコピーしない。** テンプレート自身の設計記録であり、あなたのプロジェクトのドメインではない。

### 2. 既存の指示ファイルと突き合わせる

既に `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md`、`.cursorrules` などがある場合は、**上書きせずに内容を統合する**。既存の記述の方がそのプロジェクトの実態に合っている可能性が高い。

とくに次の 4 節は必ず読み合わせる。

- **言語** — テンプレートは日本語固定。プロジェクトの慣習に合わせて書き換える
- **リポジトリ構成** — 表の行が導入先の実態と合わない。存在しないもの（`docs/github/`、`docs/template/`、`.github/` など）の行を消し、導入先に固有のディレクトリを足す
- **エージェントへの制約** — 既存の運用と矛盾しないか確認する。例えば既定ブランチへの直接 push を許している運用なら、その行を消すか運用を変えるかを決める
- **コミットメッセージ** — 既存の履歴と規約が違うなら、既存に合わせる

**統合が終わったら `.github/copilot-instructions.md` は削除する。** このテンプレートは `AGENTS.md` を唯一の実体とする構成で、両方を残すと同じ指示が二重に読み込まれる。削除できない事情がある場合は、内容を空にして `AGENTS.md` を指す 1 行だけにするか、両ファイルを完全に同一内容に保つ運用（テンプレートが以前採っていた形）に切り替える。

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

**required status check にする前に、まず変更提案として 1 回走らせて緑を確認すること。** 既存プロジェクトは画像やコンパイル済み成果物を含むことが多く、`skillspector` が analyzer の劣化で落ちやすい。対処は `README.md` の「analyzer の劣化で落ちたとき」を参照。scan の呼び出しは json 用と markdown 用の 2 つあるので、対象を絞るときは**両方を同時に**書き換える。

### 8. ブランチ保護を設定する（任意）

`docs/github/branch-protection.md` の手順を使う。**ただし既存リポジトリでは注意が要る。**

あの PUT は**設定全体の置換**で、既存のブランチ保護があると丸ごと上書きされる。必ず現状を保存してから、必要な項目だけを足した内容で投げること。

```
gh api repos/{owner}/{repo}/branches/main/protection > /tmp/bp-backup.json
```

既存の `required_status_checks.contexts` に `gitleaks` と `skillspector` を**追加**し、レビュー必須などの既存設定は保ったまま投げ直す。保護が未設定のリポジトリなら、そのまま `branch-protection.md` の内容を使ってよい。

## 確認

`docs/checklist.md` を通す。ただし**項目 1・2・4 は新規複写向け**なので、既存プロジェクトでは次のように読み替える。

- 項目 1（テンプレートの説明の残り）— 該当しない。README は元のまま
- 項目 2（`docs/template/` の残り）— コピーしていなければ該当しない
- 項目 4（`docs/adr/` が空か）— 既存の ADR があるならそのまま。番号の重複だけ確認する

GitHub 層を入れたなら `docs/github/checklist.md` も通す。
