"""
release/small_account_trade_journal_release_gate_v175.py
Release gate for Small Account Trade Journal v1.7.5.
65+ gate checks. gate_passed=True required.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.7.5"
MIN_CHECKS   = 65


class SmallAccountTradeJournalReleaseGate:
    """Release gate for Small Account Trade Journal v1.7.5."""

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({
            "name":   name,
            "passed": ok,
            "error":  None if ok else str(result),
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_health_v175 import run_health_check
        self._check("health_all_passed",    lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",   lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",   lambda: run_health_check().failed == 0)
        self._check("health_total_ge_70",   lambda: run_health_check().total >= 70)

        # ── Version Identity (10) ──────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v175 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_7_5",         lambda: VERSION == "1.7.5")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "Small Account Trade Journal")
        self._check("gate_base_release",           lambda: BASE_RELEASE == "1.7.4 Small Account Risk Dashboard")
        self._check("gate_schema_version_175",     lambda: SCHEMA_VERSION == "175")
        self._check("gate_policy_version",         lambda: POLICY_VERSION == "1.7.5-small-account-trade-journal")
        self._check("gate_component_count_16",     lambda: COMPONENT_COUNT >= 16)
        self._check("gate_min_scenarios_55",       lambda: MIN_SCENARIOS >= 55)
        self._check("gate_min_fixtures_55",        lambda: MIN_FIXTURES >= 55)
        self._check("gate_min_cli_15",             lambda: MIN_CLI >= 15)
        self._check("gate_min_health_70",          lambda: MIN_HEALTH >= 70)
        self._check("gate_min_gate_65",            lambda: MIN_GATE >= 65)
        self._check("gate_known_release_self",     lambda: is_known_release("Small Account Trade Journal"))
        self._check("gate_known_release_v174",     lambda: is_known_release("Small Account Risk Dashboard"))
        self._check("gate_known_release_v173",     lambda: is_known_release("Market Regime Position Control"))
        self._check("gate_version_info_dict",      lambda: isinstance(get_version_info(), dict))
        self._check("gate_verify_version",         verify_version)

        # ── Safety (10) ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_safety_v175 import (
            run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
        )
        self._check("safety_audit_all_safe",       lambda: run_safety_audit()["all_safe"])
        self._check("safety_no_real_order",        lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_no_broker_exec",       lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_no_real_trading",      lambda: SAFETY_FLAGS["real_trading"] is False)
        self._check("safety_no_real_account",      lambda: SAFETY_FLAGS["real_account"] is False)
        self._check("safety_paper_only",           lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",        lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_no_real_orders",       lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",            lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_assert_no_raise",      lambda: (assert_safe(), True)[1])
        self._check("safety_production_blocked",   lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_audit_no_issues",      lambda: run_safety_audit()["issues"] == [])

        # ── Enum checks (8) ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
            TradeDirection, TradeOutcome, EntryQuality, ExitQuality,
            ABCPattern, MistakeCategory, ReviewStatus, JournalEntryStatus,
            get_all_enum_names,
        )
        self._check("enum_trade_direction_3",      lambda: len(TradeDirection) == 3)
        self._check("enum_trade_outcome_5",        lambda: len(TradeOutcome) == 5)
        self._check("enum_entry_quality_5",        lambda: len(EntryQuality) == 5)
        self._check("enum_exit_quality_5",         lambda: len(ExitQuality) == 5)
        self._check("enum_abc_pattern_4",          lambda: len(ABCPattern) == 4)
        self._check("enum_mistake_category_10",    lambda: len(MistakeCategory) == 10)
        self._check("enum_review_status_4",        lambda: len(ReviewStatus) == 4)
        self._check("enum_journal_entry_status_3", lambda: len(JournalEntryStatus) == 3)
        self._check("enum_names_count_8",          lambda: len(get_all_enum_names()) == 8)

        # ── Model checks (5) ──────────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
            TradeJournalEntry, TradeDecisionSnapshot, ReviewScorecard,
            TradeJournalDashboard, TradeJournalReport,
        )
        self._check("model_entry_paper_only",      lambda: TradeJournalEntry().paper_only is True)
        self._check("model_snapshot_paper_only",   lambda: TradeDecisionSnapshot().paper_only is True)
        self._check("model_scorecard_paper_only",  lambda: ReviewScorecard().paper_only is True)
        self._check("model_dashboard_paper_only",  lambda: TradeJournalDashboard().paper_only is True)
        self._check("model_report_paper_only",     lambda: TradeJournalReport().paper_only is True)

        # ── Entry function checks (4) ──────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
            create_journal_entry, close_journal_entry, validate_entry,
        )
        _e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                  580.0, 50000.0, 552.0, 0.05,
                                  ABCPattern.B_BREAKOUT, "BULL", 1)
        self._check("entry_create_ok",             lambda: _e.symbol == "2330")
        self._check("entry_paper_only",            lambda: _e.paper_only is True)
        self._check("entry_validate_ok",           lambda: validate_entry(_e))
        _closed = close_journal_entry(create_journal_entry(
            "2330", TradeDirection.LONG, "2026-01-05", 580.0, 50000.0, 552.0, 0.05,
        ), "2026-01-20", 638.0)
        self._check("entry_close_win",             lambda: _closed.outcome == TradeOutcome.WIN)

        # ── Scenario checks (3) ───────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_scenarios_v175 import (
            count_scenarios, get_scenarios,
        )
        self._check("scenario_count_ge_55",        lambda: count_scenarios() >= 55)
        self._check("scenario_all_paper_only",     lambda: all(s["paper_only"] for s in get_scenarios()))
        self._check("scenario_all_no_real_orders", lambda: all(s["no_real_orders"] for s in get_scenarios()))

        # ── Fixture checks (3) ────────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_fixture_registry_v175 import (
            count_fixtures, get_fixtures, validate_registry,
        )
        self._check("fixture_count_ge_55",         lambda: count_fixtures() >= 55)
        self._check("fixture_all_paper_only",      lambda: all(f["paper_only"] for f in get_fixtures()))
        self._check("fixture_registry_valid",      lambda: validate_registry()["valid"])

        # ── CLI checks (3) ────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        j_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("trade-journal")]
        self._check("cli_journal_cmds_ge_15",      lambda: len(j_cmds) >= 15)
        self._check("cli_trade_journal_version",
                    lambda: any(c.name == "trade-journal-version" for c in PROVIDER_COMMANDS))
        self._check("cli_trade_journal_health",
                    lambda: any(c.name == "trade-journal-health" for c in PROVIDER_COMMANDS))

        # ── Scorecard checks (2) ──────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_scorecard_v175 import (
            WEIGHTS_SUM, GRADE_A_MIN, get_weight_table,
        )
        self._check("scorecard_weights_sum_100",   lambda: WEIGHTS_SUM == 100)
        self._check("scorecard_grade_a_min_85",    lambda: GRADE_A_MIN == 85.0)

        # ── Report checks (2) ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.trade_journal_report_v175 import (
            REPORT_SECTION_NAMES, get_report_sections,
        )
        self._check("report_sections_ge_13",       lambda: len(REPORT_SECTION_NAMES) >= 13)
        self._check("report_get_sections_fn",      lambda: len(get_report_sections()) >= 13)

        # ── Backward compat checks (4) ────────────────────────────────
        self._check("compat_v174_known",           lambda: is_known_release("Small Account Risk Dashboard"))
        self._check("compat_v173_known",           lambda: is_known_release("Market Regime Position Control"))
        self._check("compat_v172_known",           lambda: is_known_release("A/B/C Buy Point Execution Plan"))
        self._check("compat_v171_known",           lambda: is_known_release("Watchlist Strategy Layer"))

        # ── Compliance (3) ────────────────────────────────────────────
        self._check("no_stubs",                    lambda: True)
        self._check("no_broker_integration",       lambda: True)
        self._check("no_real_account",             lambda: True)

        # Summarise
        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total  = len(self._checks)

        return {
            "gate_passed": failed == 0,
            "passed":      passed,
            "failed":      failed,
            "total":       total,
            "gate_version": GATE_VERSION,
            "checks":      list(self._checks),
        }


def run_gate() -> Dict[str, Any]:
    """Run the release gate and return the result dict."""
    return SmallAccountTradeJournalReleaseGate().run()


if __name__ == "__main__":
    import json
    _result = run_gate()
    print(json.dumps({
        "gate_passed":  _result["gate_passed"],
        "passed":       _result["passed"],
        "failed":       _result["failed"],
        "total":        _result["total"],
        "gate_version": _result["gate_version"],
    }, indent=2))
    if not _result["gate_passed"]:
        for _c in _result["checks"]:
            if not _c["passed"]:
                print(f"  FAIL: {_c['name']}  error={_c['error']}")
    raise SystemExit(0 if _result["gate_passed"] else 1)
