# このテンプレートから作ったリポジトリで `/setup-matt-pocock-skills` を実行しない

上流の README は「リポジトリごとに 1 回 `/setup-matt-pocock-skills` を実行する」よう指示しているが、このテンプレートを複写したリポジトリでは実行しない。

## 背景

`setup-matt-pocock-skills` は issue tracker、triage ラベル、ドメイン文書の配置を対話的に決めて `docs/agents/` を生成する skill である。issue tracker の選択肢は GitHub / GitLab / ローカル markdown / その他の 4 つ。

このテンプレートの `docs/agents/issue-tracker.md` は、そのどれでもない**二層構成**になっている。

- `.scratch/`（git 管理外）— 調査・設計・`/wayfinder` の探索
- GitHub Issues — 実装タスクと triage

skill 名で保存先を明示的に振り分ける表を持ち、`gh` が使えない環境でも設計作業が止まらないように設計してある。この構成は標準の選択肢に無い。

## 決定

複写したリポジトリで `/setup-matt-pocock-skills` を実行しない。`docs/agents/` はテンプレートが持っているものをそのまま使う。

構成を変えたい場合は `docs/agents/` を直接編集する。

## 帰結

- **上流の公式手順に反する指示である。** 根拠を残さなければ、善意で実行されて設定が失われる。この ADR はそのために存在する。
- 実行してしまった場合、`docs/agents/issue-tracker.md` は標準テンプレートで上書きされ、skill 名の振り分け表が消える。git 履歴から戻すこと。
- テンプレートを使わず一から始めるリポジトリでは、上流の手順どおり実行してよい。この決定はこのテンプレートの複写先に限った話である。
