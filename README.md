# エージェント向け開発テンプレート

**読み手**: このテンプレートの採用を検討している人、および導入作業をする人。

コーディングエージェント（GitHub Copilot、Claude Code など）にプロジェクトの前提を伝える設定を、再利用可能な形でまとめたテンプレート。コードそのものではなく「エージェントとの働き方」を配布する。

技術スタックには依存しない。前提にしているのは **Copilot CLI と VS Code Chat が指示ファイルと skill をどう読むか**だけで、issue tracker・CI・ホスティングはプロジェクトごとに差し替えられる。

**このテンプレートはまだ実案件で運用されていない。** 机上で埋められる穴は埋めてあるが、実際に回して初めて分かる問題は未知のままである。採用する際はそのつもりで。

## 構成

### コア（ホスティング非依存）

| パス | 内容 |
| --- | --- |
| `AGENTS.md` | エージェント向け指示の実体。言語ルール、リポジトリ構成、制約、コミット規約 |
| `CLAUDE.md` | `AGENTS.md` を取り込む 1 行。Claude Code は `AGENTS.md` を読まないため |
| `CONTEXT.md` | ドメイン用語集の雛形 |
| `docs/adr/` | 設計決定の置き場所。空で始まる |
| `docs/agents/` | issue tracker とドメイン文書の運用規約 |
| `docs/skills.md` | skill の導入手順 |
| `docs/skills-authoring.md` | プロジェクト固有の skill を自分で書く手順 |
| `docs/skills-catalog.md` | 上流 skill の一覧（生成物） |
| `docs/adopt-existing.md` | 既存プロジェクトへの導入手順 |
| `docs/checklist.md` | 導入後の確認項目 |
| `docs/onboarding.md` | プロジェクトに参加した人向けのガイド（雛形） |
| `scripts/gen-skills-catalog.py` | カタログの生成 |

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

## 使い方（新規リポジトリ）

1. **Use this template** から新しいリポジトリを作る
2. **この README のうち、テンプレートの説明部分を差し替える。** 冒頭の説明と「構成」節は自分のプロジェクトの内容にする。**「CI の検査」「analyzer の劣化で落ちたとき」「ツールのバージョン更新」の 3 節は残す** — CI が落ちたときの唯一の対処手順がここにある
3. `docs/template/` を削除する。あわせて `docs/checklist.md` の項目 2 に従い、それを指す記述が残っていないか確認する
4. skill を導入する（`docs/skills.md`）。**`/setup-matt-pocock-skills` は実行しないこと** — このテンプレートの設定を上書きしてしまう
5. `AGENTS.md` をプロジェクトに合わせて調整する。とくに「リポジトリ構成」表から、削除したものの行を消す
6. GitHub を使うなら `docs/github/` の手順を上から実行する（ラベル作成 → CI をマージ → **緑を確認** → ブランチ保護）
7. `docs/checklist.md` で抜けが無いか確認する。GitHub を使うなら `docs/github/checklist.md` も
8. `docs/onboarding.md` の雛形部分（プロジェクトの説明、環境の立ち上げ方、相談先）を埋める。参加者が最初に読むファイルになる
9. 用語が固まったら `CONTEXT.md`、設計を決めたら `docs/adr/` に追記する。先回りして空のファイルを埋めない

既存のリポジトリに入れる場合は `docs/adopt-existing.md` を参照。

## CI の検査（GitHub 層）

| job | 何を見るか | 落ちる条件 |
| --- | --- | --- |
| `gitleaks` | 履歴全体への秘密の混入 | 秘密を検出した |
| `skillspector` | エージェントが読む資産の prompt injection やデータ持ち出しの兆候 | 判定が `DO_NOT_INSTALL`、または analyzer が 1 件でも劣化した |

どちらも API キーを必要としない。SkillSpector は `--no-llm` で静的解析のみを行う。結果は Job Summary に出る。

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
| skills CLI | `docs/skills.md` の導入コマンドと更新コマンド |
| skill カタログ | `python3 scripts/gen-skills-catalog.py` |

## 意図的に入れていないもの

| 対象 | 理由 |
| --- | --- |
| `.github/instructions/*.instructions.md` | `applyTo` で紐づける対象のコードがテンプレートに存在しない |
| `.github/workflows/copilot-setup-steps.yml` | インストールする依存が存在しない |
| `.claude/settings.json` | 制約は規約として書く方針にした |
| SARIF の Security タブ連携 | private リポジトリで有料ライセンスが必要になる |
| 定期実行（cron） | ツールのバージョンを固定しているため、同じ履歴を同じルールで再検査するだけになる |
| インストーラ | 導入は手順書で行う方針にした |

## 解決していない問題

採用する前に知っておくべきこと。

- **複写後に更新が届かない。** テンプレート側を改善しても、既に複写されたリポジトリには反映されない。反映は各リポジトリで手作業になる
- **セットアップの抜けを自動検出できない。** 確認はチェックリストによる目視のみ。とくにブランチ保護の設定漏れは無言で通り、CI が赤くてもマージできる状態が続く
- **skill の中身が固定できていない。** 導入コマンドで固定できるのはインストーラ CLI までで、skill 本体は取得時点の上流が入る（`docs/skills.md` を参照）
- **SkillSpector の依存ツリーが固定されていない。** SkillSpector 本体はコミット SHA で固定しているが、`pip install` が引く 100 個近い依存は毎回解決される。上流の lockfile を使えば塞げるが、CI に別のパッケージマネージャを持ち込むことになるため見送っている
- **日本語で書かれている。** 想定利用者が日本語話者のチームであることを前提にしている

## ライセンス

MIT。`LICENSE` を参照。

このリポジトリには [mattpocock/skills](https://github.com/mattpocock/skills)（MIT、Copyright (c) 2026 Matt Pocock）から派生した内容が含まれる。詳細は `NOTICE` を参照。
