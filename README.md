# エージェント向け開発テンプレート

コーディングエージェント（GitHub Copilot、Claude Code など）を使うチームが、**プロジェクト固有の前提をエージェントに毎回説明し直さずに済む**ようにするための土台。

エージェントは優秀だが、このプロジェクトで「注文」が何を指すか、なぜその設計を選んだかは知らない。**知らないまま素直に実装すると、過去の判断を静かに壊す。** そこを埋めるための置き場所と、いくつかの検査をひと揃いにしてある。

コードは含まない。技術スタックにも依存しない。配るのは「エージェントとの働き方」だけ。

## 何が変わるか

| | |
| --- | --- |
| **新しく参加した人が読むもの** | 1 ページ（約 1,900 字）。残りはエージェントが読む |
| **「なぜこうなっているか」** | `docs/adr/` に残る。同じ議論を繰り返さない |
| **既定ブランチへの直接 push・履歴の書き換え** | git hook が実際に止める。人間にもエージェントにも効く |
| **秘密の混入・エージェントが読む資産の危険** | CI が毎回検査する |

## 向くチーム・向かないチーム

**向く**

- コーディングエージェントを日常的に使っている
- 日本語で運用している
- 用語や設計判断を書き残す気がある。**効果が出るのはここ**（下の「確かめたこと・確かめていないこと」を参照）

**向かない**

- エージェントを使わない。この設定は全部エージェント向け
- 英語で運用している。**すべて日本語で書かれている**
- 用語も設計判断も当分書くつもりが無い。空の置き場所だけが残る

**実案件での運用実績はまだ無い。** 机上で埋められる穴は埋めてあるが、実際に回して初めて分かる問題は未知のまま。

## 導入に要るもの

| | |
| --- | --- |
| **必須** | git |
| **任意** | GitHub（CI とラベル運用を使う場合）、Copilot か Claude Code、Python 3（skill 一覧の再生成のみ） |
| **費用** | 無し。CI は API キーを必要とせず、**コードを外部に送らない**（静的解析のみ） |
| **ライセンス** | MIT。上流の [mattpocock/skills](https://github.com/mattpocock/skills)（MIT）由来の内容を含む |

**人にしか書けないものは 3 か所。** README を自分のプロジェクトの説明にする、参加者ガイドの空欄 4 つを埋める、skill を入れるかどうか。ほかは削除と設定作業で、GitHub のラベルとブランチ保護を使う場合はその分が加わる。

参加する人がやるのは、コマンド 2 つと 1 ページを読むこと。

## 確かめたこと・確かめていないこと

効果を 1 度だけ測ってある。**結果は控えめで、都合の悪い数字も含む。**

同じドメインに同じタスクを与え、構成だけを変えて 4 回ずつ実行した。タスクは意図的に ADR と矛盾させてある。成果物は 3 人の採点者が実際にコードを走らせて評価した。

| 構成 | 平均品質（10 点） | 既存 API の意味を保った |
| --- | --- | --- |
| `AGENTS.md` + `CONTEXT.md` + `docs/adr/` + skill | 9.0 | 4/4 |
| `AGENTS.md` のみ | 8.3 | 1/4 |
| 設定なし | 8.2 | 1/4 |

- **効いたのは用語と設計判断（`CONTEXT.md` と `docs/adr/`）だけ。** これがある構成だけが、ADR の定めどおり既存メソッドの意味を変えずに表示層を足した
- **進め方を文書に書くこと（`AGENTS.md`）は、実装の質を動かさなかった。** 何も置かない構成と区別できなかった。この結果を受けて `AGENTS.md` を 29% 削り、同じ実験を回し直して品質が変わらないことを確認してある
- どの構成でも、仕掛けた罠は 12 回とも回避された。**エージェントは想定より賢い**

**限界。** n=4、タスク 1 種、ドメイン 1 つ。品質差 0.8 点は統計的に主張できる大きさではない。**「初心者が経験者並みの成果を出せる」とは読まないこと。** 言えるのは「用語と設計判断を書き残す場所を持つことに効果がありそう」まで。

**同じ測定を自分のドメインでやり直せる。** 題材のコード、用語集、ADR、判定用のテスト、手順を `docs/template/eval/` に置いてある（`docs/template/` は導入時に削除するので、必要なら先に控えておくこと）。

## 使い方（新規リポジトリ）

1. **Use this template** から新しいリポジトリを作る
2. `docs/template/` を削除する
3. `README.md` を自分のプロジェクトの説明に書き換える。**「CI の検査」「analyzer の劣化で落ちたとき」「ツールのバージョン更新」の 3 節は残す** — CI が落ちたときの唯一の対処手順がここにある
4. `CONTEXT.md` の 1 行目をプロジェクト名にする。**Language 節は空のままでよい**
5. `docs/onboarding.md` の空欄 4 つ（説明、環境の立ち上げ方とコードの場所、タスク管理、相談先）を埋める。参加者が最初に読むファイルになる
6. skill を導入する（`docs/skills.md`）。**`setup-matt-pocock-skills` は選ばなくてよい** — 実行するとこのテンプレートの設定を上書きしてしまうため、使い道が無い
7. GitHub を使うなら `docs/github/` の手順を上から実行する（ラベル作成 → CI をマージ → **緑を確認** → ブランチ保護）
8. `docs/checklist.md` で抜けが無いか確認する。GitHub を使うなら `docs/github/checklist.md` も

用語が固まったら `CONTEXT.md`、設計を決めたら `docs/adr/` に追記する。**先回りして空のファイルを埋めない。**

既存のリポジトリに入れる場合は `docs/adopt-existing.md` を参照。

## 参加する人がやること

clone したら 2 つ。

```
git config core.hooksPath .githooks          # 規約を実際に効かせる
npx skills@latest add mattpocock/skills -g   # skill を導入する（未導入なら）
```

読むのは `docs/onboarding.md` の 1 ページだけでよい。

## 構成

### コア（ホスティング非依存）

| パス | 内容 |
| --- | --- |
| `AGENTS.md` | エージェント向け指示の実体。言語、書いたものの置き場所、守る範囲、コミット規約 |
| `CLAUDE.md` | `AGENTS.md` を取り込む 1 行。Claude Code は `AGENTS.md` を読まないため |
| `CONTEXT.md` | ドメイン用語集の雛形 |
| `docs/adr/` | 設計決定の置き場所。空で始まる |
| `docs/agents/` | issue tracker とドメイン文書の運用規約 |
| `docs/skills.md` | skill の導入手順 |
| `docs/skills-authoring.md` | プロジェクト固有の skill を自分で書く手順 |
| `docs/skills-catalog.md` | 上流 skill の一覧（生成物） |
| `docs/adopt-existing.md` | 既存プロジェクトへの導入手順 |
| `docs/onboarding.md` | 参加した人が読む 1 ページ（雛形）。**これだけで作業を始められる** |
| `docs/workflow.md` | 全体の流れ・役割・図。必要になったときだけ引く |
| `docs/checklist.md` | 導入後の確認項目 |
| `scripts/gen-skills-catalog.py` | カタログの生成 |
| `.githooks/pre-push` | 既定ブランチへの直接 push と履歴の書き換えを実際に止める |

### GitHub 層（任意）

GitHub を使わないなら `docs/github/` ごと削除し、`.github/` の中身も置き換える。

| パス | 内容 |
| --- | --- |
| `docs/github/issue-tracker.md` | GitHub Issues の操作 |
| `docs/github/triage-labels.md` | ラベルの作成 |
| `docs/github/branch-protection.md` | ブランチ保護の設定 |
| `docs/github/checklist.md` | セットアップ確認項目 |
| `.github/workflows/security.yml` | gitleaks と SkillSpector による検査 |
| `.github/scripts/check-skillspector.py` | SkillSpector の判定 |

### テンプレート自身の記録

`docs/template/` にはこのテンプレートの用語集と設計決定（ADR）が入っている。**これはテンプレートについての記録であり、あなたのプロジェクトのドメインではない。** 複写したら削除してよい。

## CI の検査（GitHub 層）

| job | 何を見るか | 落ちる条件 |
| --- | --- | --- |
| `gitleaks` | 履歴全体への秘密の混入 | 秘密を検出した |
| `skillspector` | エージェントが読む資産の prompt injection やデータ持ち出しの兆候 | 判定が `DO_NOT_INSTALL`、または analyzer が 1 件でも劣化した |

**required status check に追加するのは、その job が実際に緑になってから。** 順序を逆にすると、報告されない check を待って変更提案が永久にマージできなくなる。確認手順は `docs/github/checklist.md` の項目 4。

いずれも API キーを必要としない。SkillSpector は `--no-llm` で静的解析のみを行う。結果は Job Summary に出る。

**このテンプレートの判定は `CAUTION` で固定されている。** skill の導入コマンドが版を指定しない形なので、供給網のリスクとして 3 箇所が検出される。**意図した状態**であり、CI は警告を出して通す（落ちるのは `DO_NOT_INSTALL` か analyzer の劣化のみ）。理由は `docs/skills.md` を参照。

GitHub の Security タブ（SARIF）は使っていない。private リポジトリでは Code Security ライセンスが必要になり、配布物として成立しないため。

### analyzer の劣化で落ちたとき

SkillSpector は解析できないファイル（バイナリなど）があると analyzer を劣化させるが、**その状態でも判定は `SAFE` を返す**。検査が実質行われていないのに緑になるのを防ぐため、劣化を検出したら CI を落とす設計にしてある。

画像やコンパイル済み成果物を多く含むリポジトリでは落ちやすい。その場合は `security.yml` のスキャン対象を絞る。

```yaml
skillspector scan docs/ --no-llm --format json     -o "$RUNNER_TEMP/skillspector.json" || true
skillspector scan docs/ --no-llm --format markdown -o "$RUNNER_TEMP/skillspector.md"  || true
```

**注意が 2 つある。** scan の呼び出しは json 用と markdown 用の 2 つあるので、**両方を同時に書き換える**こと。片方だけ変えると Job Summary と判定結果が食い違う。そして**存在しないパスを指定すると scan が失敗してレポートが生成されず、CI が落ちる**。実在するパスを指定すること。

## ツールのバージョン更新

ピン留めしているバージョンは Dependabot の追跡対象外で、放置すると黙って古くなる。更新は手動で行う。

| ツール | 場所 |
| --- | --- |
| gitleaks | `security.yml` の `GITLEAKS_VERSION` |
| SkillSpector | `security.yml` の `SKILLSPECTOR_REVISION`（コミット SHA） |
| actions/* | 各 workflow の `uses:` |
| skill カタログ | `python3 scripts/gen-skills-catalog.py` |

## 意図的に入れていないもの

| 対象 | 理由 |
| --- | --- |
| `.github/instructions/*.instructions.md` | `applyTo` で紐づける対象のコードがテンプレートに存在しない |
| `.github/workflows/copilot-setup-steps.yml` | インストールする依存が存在しない |
| `.claude/settings.json` | Claude Code 専用。同じ制約を `.githooks/pre-push` で agent 非依存に効かせている |
| SARIF の Security タブ連携 | private リポジトリで有料ライセンスが必要になる |
| 定期実行（cron） | ツールのバージョンを固定しているため、同じ履歴を同じルールで再検査するだけになる |
| インストーラ | 導入は手順書で行う方針にした |

## 解決していない問題

採用する前に知っておくべきこと。

- **成果物そのものの質を機械で検査する段が無い。** CI が見ているのは秘密の混入と設定の抜けであって、変更が正しいか、設計判断が妥当かは見ていない。品質を担保しているのは人間のレビューと、エージェントがドメイン文書を読むかどうかである
- **「ドメインとの照合」は規約であって仕組みではない。** `AGENTS.md` は探索の前と変更提案を出す前の 2 回照合するよう求めるが、守らせる手段は無い。守られたかどうかも検出できない
- **複写後に更新が届かない。** テンプレート側を改善しても、既に複写されたリポジトリには反映されない。反映は各リポジトリで手作業になる
- **セットアップの抜けを自動検出できない。** 確認はチェックリストによる目視のみ。リンク切れ、required check 名の不一致、参加者ガイドの空欄は、誰かが `docs/checklist.md` を通さない限り気づかれない
- **skill の中身が固定できていない。** 導入コマンドで固定できるのはインストーラ CLI までで、skill 本体は取得時点の上流が入る（`docs/skills.md` を参照）
- **SkillSpector の依存ツリーが固定されていない。** SkillSpector 本体はコミット SHA で固定しているが、`pip install` が引く 100 個近い依存は毎回解決される。上流の lockfile を使えば塞げるが、CI に別のパッケージマネージャを持ち込むことになるため見送っている
- **日本語で書かれている。** 想定利用者が日本語話者のチームであることを前提にしている

## ライセンス

MIT。`LICENSE` を参照。

このリポジトリには [mattpocock/skills](https://github.com/mattpocock/skills)（MIT、Copyright (c) 2026 Matt Pocock）から派生した内容が含まれる。詳細は `NOTICE` を参照。
