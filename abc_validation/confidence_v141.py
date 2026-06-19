"""
abc_validation/confidence_v141.py — Confidence evaluator for A/B/C validation v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Formal conclusion requires: real data, non-fixture/mock, lookahead safe,
corporate action pass, sufficient trade count, multiple symbols, multiple regimes,
OOS or walk-forward, positive expectancy after costs, not highly parameter-sensitive.
Otherwise: formal_conclusion_allowed=False.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


MIN_TRADES_FOR_FORMAL = 30
MIN_SYMBOLS_FOR_FORMAL = 5
MIN_REGIMES_FOR_FORMAL = 2


class ABCValidationConfidence:
    """
    Confidence evaluator extending v1.4.0 BacktestConfidenceEvaluator pattern.

    Levels: HIGH, MEDIUM, LOW, INSUFFICIENT, BLOCKED.
    """

    LEVELS = ["HIGH", "MEDIUM", "LOW", "INSUFFICIENT", "BLOCKED"]

    def evaluate(self, validation_result: dict) -> Dict[str, Any]:
        """
        Evaluate confidence level and formal conclusion eligibility.

        Returns dict with: level, formal_conclusion_allowed, reasons, requirements_met.
        """
        reasons: List[str] = []
        blockers: List[str] = []
        requirements_met: List[str] = []
        requirements_failed: List[str] = []

        # 1. Real data required
        data_mode = validation_result.get("configuration", {}).get("data_mode", "mock")
        is_real_data = data_mode == "real"
        if not is_real_data:
            blockers.append(f"NOT_REAL_DATA: data_mode={data_mode!r}")
            requirements_failed.append("real_data")
        else:
            requirements_met.append("real_data")

        # 2. No fixture/mock data
        has_fixture = validation_result.get("quality_summary", {}).get("fixture_data_used", False)
        if has_fixture:
            blockers.append("FIXTURE_DATA_USED: fixture/mock data in results")
            requirements_failed.append("no_fixture_data")
        else:
            requirements_met.append("no_fixture_data")

        # 3. Lookahead safe
        lookahead_violations = validation_result.get("quality_summary", {}).get("lookahead_violations", 0)
        if lookahead_violations > 0:
            blockers.append(f"LOOKAHEAD_VIOLATIONS: {lookahead_violations}")
            requirements_failed.append("lookahead_safe")
        else:
            requirements_met.append("lookahead_safe")

        # 4. Corporate action pass
        corp_action_issues = validation_result.get("quality_summary", {}).get("corporate_action_issues", 0)
        if corp_action_issues > 0:
            reasons.append(f"CORPORATE_ACTION_ISSUES: {corp_action_issues}")
            requirements_failed.append("corporate_action_clean")
        else:
            requirements_met.append("corporate_action_clean")

        # 5. Sufficient trade count
        trade_count = validation_result.get("trade_count", 0)
        if trade_count < MIN_TRADES_FOR_FORMAL:
            reasons.append(f"INSUFFICIENT_TRADES: {trade_count} < {MIN_TRADES_FOR_FORMAL}")
            requirements_failed.append("sufficient_trades")
        else:
            requirements_met.append("sufficient_trades")

        # 6. Multiple symbols
        symbols_tested = len(validation_result.get("symbols_tested", []))
        if symbols_tested < MIN_SYMBOLS_FOR_FORMAL:
            reasons.append(f"INSUFFICIENT_SYMBOLS: {symbols_tested} < {MIN_SYMBOLS_FOR_FORMAL}")
            requirements_failed.append("multiple_symbols")
        else:
            requirements_met.append("multiple_symbols")

        # 7. Multiple regimes
        regime_results = validation_result.get("regime_results", {})
        regimes_with_trades = sum(
            1 for r in regime_results.values()
            if isinstance(r, dict) and r.get("trade_count", 0) > 0
        )
        if regimes_with_trades < MIN_REGIMES_FOR_FORMAL:
            reasons.append(f"INSUFFICIENT_REGIMES: {regimes_with_trades} < {MIN_REGIMES_FOR_FORMAL}")
            requirements_failed.append("multiple_regimes")
        else:
            requirements_met.append("multiple_regimes")

        # 8. OOS or walk-forward
        has_oos = validation_result.get("quality_summary", {}).get("has_oos_validation", False)
        has_wf = bool(validation_result.get("walk_forward_results"))
        if not has_oos and not has_wf:
            reasons.append("NO_OOS_OR_WALK_FORWARD: in-sample only")
            requirements_failed.append("oos_or_walk_forward")
        else:
            requirements_met.append("oos_or_walk_forward")

        # 9. Positive expectancy after costs
        hp_results = validation_result.get("holding_period_results", {})
        period_results = hp_results.get("period_results", {}) if isinstance(hp_results, dict) else {}
        period5 = period_results.get(5, {}) if period_results else {}
        expectancy = period5.get("expectancy")
        if expectancy is not None and expectancy <= 0:
            reasons.append(f"NON_POSITIVE_EXPECTANCY: {expectancy:.4f}")
            requirements_failed.append("positive_expectancy")
        elif expectancy is not None:
            requirements_met.append("positive_expectancy")

        # 10. Not highly parameter-sensitive
        ablation = validation_result.get("ablation_results", {})
        if isinstance(ablation, dict) and ablation.get("warnings"):
            reasons.append("OVER_FILTERING_DETECTED: parameter sensitivity concerns")
            requirements_failed.append("not_parameter_sensitive")
        else:
            requirements_met.append("not_parameter_sensitive")

        # Determine formal conclusion
        formal_conclusion_allowed = len(blockers) == 0 and len(requirements_failed) == 0

        # Determine level
        if blockers:
            level = "BLOCKED"
        elif not formal_conclusion_allowed:
            if trade_count == 0:
                level = "INSUFFICIENT"
            elif len(requirements_failed) >= 4:
                level = "LOW"
            elif len(requirements_failed) >= 2:
                level = "MEDIUM"
            else:
                level = "LOW"
        else:
            level = "HIGH" if len(requirements_met) >= 8 else "MEDIUM"

        return {
            "level": level,
            "formal_conclusion_allowed": formal_conclusion_allowed,
            "blockers": blockers,
            "reasons": reasons,
            "requirements_met": requirements_met,
            "requirements_failed": requirements_failed,
            "note": (
                "Formal conclusion requires real data, lookahead-safe, sufficient trades, "
                "multiple symbols/regimes, OOS/walk-forward, positive expectancy."
            ),
        }
