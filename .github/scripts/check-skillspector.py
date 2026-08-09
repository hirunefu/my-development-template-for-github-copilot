#!/usr/bin/env python3
"""SkillSpector の JSON レポートを読み、CI を通すかどうかを判定する。

SkillSpector の終了コードは score が 50 を超えたときしか 1 にならない。
検査の半分が劣化していても SAFE / 終了コード 0 を返すため、終了コードだけを
見る CI は「偽の緑」を通してしまう。判断の根拠は
docs/template/adr/0003-gate-on-analyzer-degradation.md を参照。
"""

import json
import sys


def load(path):
    """レポートを読む。読めなければ (None, エラー文言) を返す。"""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"レポートを読めなかった ({exc})。スキャン自体が失敗した可能性がある"


def judge(report):
    """レポートを判定し、(失敗理由のリスト, 警告のリスト, 表示用の要約) を返す。"""
    failures = []
    warnings = []

    if not report.get("execution_successful", False):
        failures.append("スキャンが正常終了しなかった (execution_successful が false)")

    risk = report.get("risk_assessment", {})
    recommendation = risk.get("recommendation", "UNKNOWN")
    score = risk.get("score", "?")
    if recommendation == "DO_NOT_INSTALL":
        failures.append(f"リスク判定が DO_NOT_INSTALL (score={score})")
    elif recommendation != "SAFE":
        warnings.append(f"リスク判定が {recommendation} (score={score})")

    completeness = report.get("analysis_completeness", {})
    statuses = completeness.get("analyzer_statuses", [])
    degraded = [a for a in statuses if a.get("status") == "degraded"]
    if degraded:
        names = ", ".join(sorted(a.get("analyzer_id", "?") for a in degraded))
        failures.append(
            f"劣化した analyzer が {len(degraded)} 件ある: {names}"
        )
        failures.append(
            "検査が不完全なまま SAFE と報告されうるため通さない。"
            "対象にバイナリなど解析できないファイルが混ざっていないか確認すること"
        )

    summary = [
        f"recommendation : {recommendation} (score={score})",
        f"coverage       : {completeness.get('coverage_percent')}%",
        f"analyzer       : 全 {len(statuses)} 件中 degraded {len(degraded)} 件",
    ]
    return failures, warnings, summary


def main(argv):
    if len(argv) != 2:
        print("usage: check-skillspector.py <report.json>", file=sys.stderr)
        return 2

    report, error = load(argv[1])
    if error:
        print(f"::error::{error}")
        return 1

    failures, warnings, summary = judge(report)
    for line in summary:
        print(line)
    for warning in warnings:
        print(f"::warning::{warning}")
    for failure in failures:
        print(f"::error::{failure}")

    if failures:
        return 1
    print("判定: 通過")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
