# Skill のセットアップと使い方

このテンプレートは [mattpocock/skills](https://github.com/mattpocock/skills) の skill 群を前提にしている。`docs/agents/` にある設定は、それらの skill が読むために置かれている。

skill を入れていなくてもリポジトリは壊れないが、`docs/agents/issue-tracker.md` の振り分け表に並ぶ `/to-spec` や `/wayfinder` といったコマンドは存在しないままになる。

skill の一覧は [skills-catalog.md](./skills-catalog.md) にある。

## 導入

上流は 3 通りの導入方法を提示していて、**どれか一つを選ぶ**よう明記している。複数の方法で入れると skill が二重に登録される。

このテンプレートが前提にするのは次の方法。

```
npx skills@1.5.22 add mattpocock/skills -g
```

`-g` はグローバル導入で、`~/.agents/skills/` に実体が置かれる。対話的に skill とエージェントを選ぶ形式なので、少なくとも `setup-matt-pocock-skills` を含めて選ぶこと。

上流の README はバージョンを固定しない形を示しているが、ここでは固定している。固定しなければ、上流が侵害された場合に悪意ある更新をそのまま取り込む経路になり、このリポジトリが gitleaks や SkillSpector をピン留めしている方針とも矛盾するため。更新時は `README.md` の「ツールのバージョン更新」に従って上げる。

### 一度の導入で Claude Code と Copilot CLI の両方に効く

`~/.agents/skills/` は両者が共通して読む個人 skill ディレクトリになっている。エージェントごとに入れ直す必要はない。

| エージェント | 読み込む場所 |
| --- | --- |
| Claude Code | `~/.claude/skills/`（`~/.agents/skills/` へのシンボリックリンクが張られる） |
| GitHub Copilot | `~/.copilot/skills/` と `~/.agents/skills/` |

導入後、`copilot skill list` を実行すると Personal skills として並ぶ。Claude Code 側は `/` を入力すればコマンドとして出てくる。

### 採らなかった方法

- `claude plugins install mattpocock-skills` — 読み取り専用で自動更新される利点はあるが、**Claude Code 専用**で Copilot には効かない。Copilot を主要な対象に含むこのテンプレートとは相性が悪い
- プロジェクトレベル導入（`.claude/skills/` にコミット）— clone するだけで揃う反面、skill 一式をこのリポジトリに同梱することになり、上流への追従が手作業になる

## `/setup-matt-pocock-skills` は実行しない

上流の README は「リポジトリごとに 1 回実行する」よう指示しているが、**このテンプレートから作ったリポジトリでは実行しないこと。**

`docs/agents/` の設定は既に入っている。加えて `issue-tracker.md` の二層構成（`.scratch/` と GitHub Issues を skill 名で振り分ける）は、あの skill が提示する 4 択（GitHub / GitLab / ローカル markdown / その他）には存在しない独自設定で、実行すると標準テンプレートで上書きされて失われる。

理由の詳細は [adr/0005-do-not-rerun-setup-skill.md](./adr/0005-do-not-rerun-setup-skill.md) を参照。

issue tracker やラベルの構成を変えたくなった場合は、`docs/agents/` を直接編集する。

## このリポジトリの設定がどう使われるか

| ファイル | 読まれ方 |
| --- | --- |
| `docs/agents/issue-tracker.md` | `/triage` と `/code-review` がパスで直接参照する。他の skill は `AGENTS.md` の `## Agent skills` ブロックから辿る |
| `docs/agents/triage-labels.md` | `/triage` が使うラベル語彙。GitHub 上の実ラベルと対応する |
| `docs/agents/domain.md` | `CONTEXT.md` と `docs/adr/` の読み方を定める。`/domain-modeling` `/diagnosing-bugs` `/tdd` `/codebase-design` `/improve-codebase-architecture` などが対象 |

どの skill を使えばよいか分からないときは `/ask-matt` が案内する。

## 更新

skill 本体の更新。

```
npx skills@1.5.22 update
```

カタログの再生成。上流のリビジョンが変わったときに実行する。

```
python3 .github/scripts/gen-skills-catalog.py
```

出力は決定的で、上流が動いていなければ差分は出ない。上流のディレクトリ構成や frontmatter の形式が変わった場合は、誤った内容を書き出さずにエラーで停止する。

**カタログの更新を検査する CI は置いていない。** 理由は [adr/0004-skills-catalog-generated-not-enforced.md](./adr/0004-skills-catalog-generated-not-enforced.md) を参照。上流が変わったことに自動では気づけないため、カタログを信頼する前に冒頭のリビジョンを確認すること。
