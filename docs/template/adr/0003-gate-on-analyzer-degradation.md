# SkillSpector の終了コードだけでなく analyzer の劣化件数でも CI を落とす

`.github/scripts/check-skillspector.py` が JSON レポートを読み、`recommendation` と劣化した analyzer の件数の両方で判定する。終了コードだけを見る単純な構成には**しない**。

## 背景

SkillSpector の終了コードは score が 50 を超えたとき（`DO_NOT_INSTALL`）にしか 1 にならない。`SAFE` と `CAUTION` はどちらも 0 を返す。

このリポジトリで実測したところ、次の 2 つはどちらも `recommendation: SAFE` / 終了コード 0 だった。

| 対象 | coverage | 劣化した analyzer |
| --- | --- | --- |
| クリーンなチェックアウト | 100.0% | 0 件 |
| 解析できないバイナリを含む状態 | 59.2% | **14 件** |

劣化していたのは `static_patterns_prompt_injection`、`static_patterns_data_exfiltration`、`static_patterns_memory_poisoning` など、検査の中核をなす analyzer である。つまり**検査の大半が実行できていない状態でも緑になる**。これを「偽の緑」と呼ぶ（`CONTEXT.md` を参照）。

`analysis_completeness.is_complete` は判定に使えない。`--no-llm` を指定すると LLM 系の analyzer 3 件が `disabled` になり、coverage が 100% でも常に `false` を返すため、条件にすると CI が永久に落ち続ける。

## 決定

判定スクリプトが以下のいずれかに該当したとき失敗させる。

1. レポートが読めない、または `execution_successful` が false（スキャン自体の失敗。終了コード 2 に相当）
2. `risk_assessment.recommendation` が `DO_NOT_INSTALL`
3. `analyzer_statuses` に `degraded` が 1 件以上

`CAUTION` は警告として出力するが失敗させない。判断を要する信号であり、実コードを持つプロジェクトで頻発してノイズになるため。

## 却下した選択肢

- **終了コードだけを見る** — 実装は最小だが、上記のとおり検査が半分死んだ状態を黙って通す。
- **`CAUTION` でも落とす** — 最も厳格だが、下流のプロジェクトで誤検知によるブロックが増え、workflow ごと削除される方向に働く。
- **`coverage_percent` に閾値を課す** — 劣化と重複する指標であり、対象ファイルの構成で変動して閾値の根拠が持ちにくい。`degraded` は「検査が失敗した」という事実そのものなので、判断の余地がない。

## 帰結

- **この判定を「終了コードで十分では」と単純化してはいけない。** 上の実測がその反例である。
- 対象にバイナリ（画像、フォント、コンパイル済み成果物など）を多く含むリポジトリでは `degraded` が出て CI が落ちうる。その場合はスキャン対象のパスを絞る。対処は `README.md` に記載してある。
- 判定ロジックは workflow に直接埋め込まず独立したスクリプトにしてある。実際のレポートを入力として手元で検証できるようにするため。
- **承知の上で受け入れている検出が 3 件ある。** `scripts/gen-skills-catalog.py` の `subprocess` 呼び出し 2 件は、指摘が求める緩和策（シェルを介さず引数リストで渡す）を既に満たしており、上流を取得する以上避けられない。`LICENSE` の `EA3 Scope Creep` 1 件は **MIT ライセンスの標準文面**（`INCLUDING BUT NOT LIMITED TO`）が一致したもので、書き換えれば標準の MIT ではなくなる。**いずれも「直す」ことはしない。**
