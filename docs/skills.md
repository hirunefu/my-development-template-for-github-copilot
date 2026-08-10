# Skill のセットアップと使い方

**読み手**: skill を導入する人。プロジェクトごとに一度だけ通る。

このテンプレートは [mattpocock/skills](https://github.com/mattpocock/skills) の skill 群を前提にしている。`docs/agents/` にある設定は、それらの skill が読むために置かれている。

skill を入れていなくてもリポジトリは壊れないが、`docs/agents/issue-tracker.md` の振り分け表に並ぶ `/to-spec` や `/wayfinder` といったコマンドは存在しないままになる。

skill の一覧は [skills-catalog.md](./skills-catalog.md) にある。**このプロジェクト固有の知識・規約・レビュー観点を自分で skill にする**話は [skills-authoring.md](./skills-authoring.md) にある。

## 導入

上流は導入方法を 2 通り示していて、**どちらか一方を選ぶ**よう明記している（"Two ways in, two philosophies. ... Pick one — installing both leaves you with every skill twice."）。両方で入れると skill が二重に登録される。

このテンプレートが前提にするのは次の方法。

```
npx skills@latest add mattpocock/skills -g
```

`-g` はグローバル導入で、`~/.agents/skills/` に実体が置かれる。対話的に skill とエージェントを選ぶ形式。

**`setup-matt-pocock-skills` は選ばなくてよい。** このテンプレートでは実行しない方針で（理由は下の「`/setup-matt-pocock-skills` は実行しない」節）、入れても使い道が無い。

**取り込む内容を事前に検証する手段は無い。** インストーラも skill 本体も、実行した時点の上流がそのまま入る。skill はエージェントが読む指示そのものなので、**供給網としてはここが最も重要なのに塞げていない**。これは既知の限界として受け入れている。

以前はインストーラの版だけを固定していたが、やめた。**skill の中身が固定できていない以上、インストーラだけ固定しても守れる範囲がほとんど無い**割に、版を上げる手作業だけが残るため。

緩和になるのは、導入時に `~/.agents/.skill-lock.json` が skill ごとのハッシュを記録することだけ。何が入ったかは後から確認できるが、入る前に検証はできない。**組織で採用する際は、この点を承知の上で判断すること。**

### 一度の導入で Claude Code と Copilot CLI の両方に効く

`~/.agents/skills/` は両者が共通して読む個人 skill ディレクトリになっている。エージェントごとに入れ直す必要はない。

| エージェント | 読み込む場所 |
| --- | --- |
| Claude Code | `~/.claude/skills/`（`~/.agents/skills/` へのシンボリックリンクが張られる） |
| GitHub Copilot | `~/.copilot/skills/` と `~/.agents/skills/` |

導入後、`copilot skill list` を実行すると Personal skills として並ぶ。Claude Code 側は `/` を入力すればコマンドとして出てくる。

### 採らなかった方法

- `claude plugins install mattpocock-skills` — 読み取り専用で自動更新される利点はあるが、**Claude Code 専用**で Copilot には効かない。Copilot を主要な対象に含むこのテンプレートとは相性が悪い
- 上流 skill 一式のプロジェクトレベル導入（`mattpocock/skills` を `.claude/skills/` にコミット）— clone するだけで揃う反面、skill 一式をこのリポジトリに同梱することになり、上流への追従が手作業になる

退けたのは**上流の skill を同梱すること**であって、`.claude/skills/` というディレクトリ自体ではない。このプロジェクト向けに自分で書く skill はそこに置く。書き方は [skills-authoring.md](./skills-authoring.md) を参照。

## `/setup-matt-pocock-skills` は実行しない

上流の README は「リポジトリごとに 1 回実行する」よう指示しているが、**このテンプレートから作ったリポジトリでは実行しないこと。**

`docs/agents/` の設定は既に入っている。加えて `issue-tracker.md` の二層構成（探索領域とタスク管理を skill 名で振り分ける）は、あの skill が提示する 4 択（GitHub / GitLab / ローカル markdown / その他）には存在しない独自設定で、実行すると標準テンプレートで上書きされて失われる。

**実行してしまった場合は git 履歴から `docs/agents/` を戻すこと。** 判断の経緯はテンプレート側の ADR-0005 に記録されているが、複写先には含まれないことがある。

issue tracker やラベルの構成を変えたくなった場合は、`docs/agents/` を直接編集する。

## このリポジトリの設定がどう使われるか

| ファイル | 読まれ方 |
| --- | --- |
| `docs/agents/issue-tracker.md` | `/code-review` がパスで直接参照する。`/triage` を含む他の skill は `AGENTS.md` の `## Agent skills` ブロックから辿る |
| `docs/agents/triage-labels.md` | `/triage` が使うラベル語彙。実際のラベル作成手順はトラッカーごとの層に置く |
| `docs/agents/domain.md` | `CONTEXT.md` と `docs/adr/` の読み方を定める。`/domain-modeling` `/diagnosing-bugs` `/tdd` `/codebase-design` `/improve-codebase-architecture` などが対象 |

どの skill を使えばよいか分からないときは `/ask-matt` が案内する。

## 更新

skill 本体の更新。

```
npx skills@latest update
```

カタログの再生成。上流のリビジョンが変わったときに実行する。

```
python3 scripts/gen-skills-catalog.py
```

出力は決定的で、上流が動いていなければ差分は出ない。上流のディレクトリ構成や frontmatter の形式が変わった場合は、誤った内容を書き出さずにエラーで停止する。

**カタログの更新を検査する CI は置いていない。** 第三者リポジトリへのネットワークアクセスを CI に持ち込まないための判断で、代償として上流が変わったことに自動では気づけない。**カタログを信頼する前に冒頭のリビジョンを確認すること。**
