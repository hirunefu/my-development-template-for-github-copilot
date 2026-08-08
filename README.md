# my-development-template-for-github-copilot

コーディングエージェント（GitHub Copilot、Claude Code など）にプロジェクトの前提を伝える設定を、再利用可能な形でまとめた開発テンプレート。コードそのものではなく「エージェントとの働き方」を配布する。

技術スタックには依存しない。どの言語・どのフレームワークのプロジェクトにも適用できる。

## 使い方

1. GitHub の **Use this template** から新しいリポジトリを作る
2. skill を導入する（`docs/skills.md` を参照）。**`/setup-matt-pocock-skills` は実行しないこと** — このテンプレートの設定を上書きしてしまう
3. triage ラベルを作成する（コマンドは `docs/agents/triage-labels.md` にある）
4. `AGENTS.md` をプロジェクトに合わせて調整する。**変更したら `.github/copilot-instructions.md` にも同じ内容をコピーする**（CI が一致を検査する）
5. **ブランチ保護を設定する**（下記参照）。これを省くと CI は赤い印を付けるだけで、マージを止められない
6. 用語が固まったら `CONTEXT.md`、設計を決めたら `docs/adr/` に追記する。先回りして空のファイルを作る必要はない

## 収録物

| パス | 内容 |
| --- | --- |
| `AGENTS.md` | エージェント向け指示の実体。言語ルール、リポジトリ構成、制約、コミット規約 |
| `.github/copilot-instructions.md` | 上と同一内容。IDE の Copilot Chat が読むのはこちらだけ |
| `CLAUDE.md` | `AGENTS.md` を取り込む 1 行。Claude Code 専用 |
| `CONTEXT.md` | ドメイン用語集 |
| `docs/adr/` | 設計決定とその理由の記録 |
| `docs/agents/` | issue tracker、triage ラベル、ドメイン文書の運用規約 |
| `docs/skills.md` | skill の導入手順と使い方 |
| `docs/skills-catalog.md` | 上流の skill 一覧（生成物） |
| `.github/workflows/sync-instructions.yml` | 指示ファイル 2 つの同期を検査する CI |
| `.github/workflows/security.yml` | gitleaks と SkillSpector による検査 |
| `.github/scripts/check-skillspector.py` | SkillSpector のレポートを読んで合否を判定する |
| `.github/scripts/gen-skills-catalog.py` | skill カタログを上流から生成する |

なぜ指示ファイルが 2 つあるのかは `docs/adr/0001-duplicate-instruction-files.md` に記録してある。

このテンプレートは [mattpocock/skills](https://github.com/mattpocock/skills) の skill 群を前提にしている。導入していなくてもリポジトリは壊れないが、`docs/agents/` の設定は使われないままになる。

## CI の検査

| job | 何を見るか | 落ちる条件 |
| --- | --- | --- |
| `sync-instructions` | `AGENTS.md` と `.github/copilot-instructions.md` の一致 | 内容が 1 バイトでも異なる |
| `gitleaks` | git 履歴全体への秘密の混入 | 秘密を検出した |
| `skillspector` | エージェントが読む資産の prompt injection やデータ持ち出しの兆候 | 判定が `DO_NOT_INSTALL`、または analyzer が 1 件でも劣化した |

いずれも API キーを必要としない。SkillSpector は `--no-llm` で静的解析のみを行う。

検査結果は各ジョブの **Job Summary** に出る。GitHub の Security タブ（SARIF）は使っていない。private リポジトリでは Code Security ライセンスが必要になり、テンプレートとして配布できないため。

### analyzer の劣化で落ちたとき

SkillSpector は解析できないファイル（バイナリなど）があると analyzer を劣化させるが、**その状態でも判定は `SAFE` を返す**。検査が実質行われていないのに緑になるのを防ぐため、劣化を検出したら CI を落とす設計にしてある。詳細は `docs/adr/0003-gate-on-analyzer-degradation.md`。

画像やコンパイル済み成果物を多く含むリポジトリでは落ちやすい。その場合は `security.yml` のスキャン対象を `.` から絞る。

```yaml
skillspector scan .claude/skills/ --no-llm --format json -o "$RUNNER_TEMP/skillspector.json"
```

## ブランチ保護の設定

**CI は既定ではマージを止めない。** required status check として指定して初めて門になる。ブランチ保護はリポジトリの設定であってファイルではないため、テンプレートには同梱できない。複写したリポジトリごとに設定する必要がある。

**順序に注意。** `security.yml` が既定ブランチに入る前に required check を設定すると、報告されないチェックを待ち続けて PR が固まる。先に workflow をマージしてから設定すること。

```
gh api -X PUT repos/{owner}/{repo}/branches/main/protection --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["sync-instructions", "gitleaks", "skillspector"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

`allow_force_pushes` と `allow_deletions` を false にしているのは、`AGENTS.md` の「git 履歴を書き換えない」を規約だけでなく機械的にも守らせるため。`required_pull_request_reviews` は `null` にしてある。個人リポジトリでは自分の PR を承認できず、レビュー必須にすると自分でマージできなくなるため。

Web UI なら Settings → Branches → Add branch protection rule で、Require status checks to pass before merging に上記 3 つを指定する。

`contexts` の値は workflow の job id と一致している必要がある。job の名前を変えると、指定したチェックが永久に報告されず PR がマージできなくなる。

## ツールのバージョン更新

ピン留めしているバージョンは Dependabot の追跡対象外で、放置すると黙って古くなる。更新は手動で行う。

| ツール | 場所 |
| --- | --- |
| gitleaks | `security.yml` の `GITLEAKS_VERSION` |
| SkillSpector | `security.yml` の `SKILLSPECTOR_VERSION` |
| actions/* | 各 workflow の `uses:` |
| skills CLI | `docs/skills.md` の導入コマンドと更新コマンド |

## 意図的に入れていないもの

| 対象 | 理由 |
| --- | --- |
| `.github/instructions/*.instructions.md` | `applyTo` で紐づける対象のコードがテンプレートに存在しない。プロジェクトにコードが入った時点で追加する |
| `.github/workflows/copilot-setup-steps.yml` | インストールする依存が存在しない。スタックが決まった時点で追加する |
| `.claude/settings.json` | 制約は規約として書く方針にした。機械的な強制が必要になったら追加する |
| SARIF の Security タブ連携 | private リポジトリで Code Security ライセンスが必要になり、配布物として成立しない |
| 定期実行（cron） | ツールのバージョンを固定しているため、同じ履歴を同じルールで再検査するだけになる |

## ドキュメントの言語

日本語で書く。想定利用者が日本語話者のチームだから。公開リポジトリだが、公開は配布手段であって言語を英語にする理由にはならない。詳細は `AGENTS.md` の「言語」節を参照。
