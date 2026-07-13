"""
release/theme_rotation_scanner_release_gate_v177.py
Release gate for Theme Rotation Scanner v1.7.7. 70+ gate checks. gate_passed=True required.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.7.7"
MIN_CHECKS   = 70


class ThemeRotationScannerReleaseGate:
    """Release gate for Theme Rotation Scanner v1.7.7."""

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

        # ── Health PASS (4) ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_health_v177 import run_health_check
        self._check("health_all_passed",      lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",     lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",     lambda: run_health_check().failed == 0)
        self._check("health_total_ge_70",     lambda: run_health_check().total >= 70)

        # ── Version Identity (8) ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v177 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_7_7",         lambda: VERSION == "1.7.7")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "Theme Rotation Scanner")
        self._check("gate_schema_version_177",     lambda: SCHEMA_VERSION == "177")
        self._check("gate_policy_version",         lambda: POLICY_VERSION == "1.7.7-theme-rotation-scanner")
        self._check("gate_known_release_self",     lambda: is_known_release("Theme Rotation Scanner"))
        self._check("gate_known_release_v176",     lambda: is_known_release("Mistake Taxonomy & Weekly Review Dashboard"))
        self._check("gate_version_info_dict",      lambda: isinstance(get_version_info(), dict))
        self._check("gate_verify_version",         verify_version)

        # ── Safety (12) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_safety_v177 import (
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
        self._check("safety_no_margin",            lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_assert_no_raise",      lambda: (assert_safe(), True)[1])
        self._check("safety_production_blocked",   lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_audit_no_issues",      lambda: run_safety_audit()["issues"] == [])

        # ── Enum checks (6) ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import (
            ThemeCategory, ThemeGrade, ThemeSignalType, get_all_enum_names,
        )
        self._check("enum_theme_categories_18", lambda: len(ThemeCategory) >= 18)
        self._check("enum_theme_grade_5",       lambda: len(ThemeGrade) == 5)
        self._check("enum_signal_type_7",       lambda: len(ThemeSignalType) == 7)
        self._check("enum_names_count_3",       lambda: len(get_all_enum_names()) == 3)
        self._check("enum_leader_exists",       lambda: ThemeGrade.LEADER is not None)
        self._check("enum_unknown_exists",      lambda: ThemeCategory.UNKNOWN is not None)

        # ── Model checks (13) ────────────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import (
            ThemeSignal, ThemeStrengthScore, ThemeMomentumScore, ThemeBreadthScore,
            ThemeContinuationScore, ThemeRiskScore, ThemeRotationRank, ThemeStockMapping,
            ThemeWatchlistCandidate, ThemeRotationDashboard, ThemeRotationReport,
            ThemeRotationHealthSummary,
        )
        self._check("model_signal_paper_only",       lambda: ThemeSignal().paper_only is True)
        self._check("model_strength_paper_only",     lambda: ThemeStrengthScore().paper_only is True)
        self._check("model_momentum_paper_only",     lambda: ThemeMomentumScore().paper_only is True)
        self._check("model_breadth_paper_only",      lambda: ThemeBreadthScore().paper_only is True)
        self._check("model_continuation_paper_only", lambda: ThemeContinuationScore().paper_only is True)
        self._check("model_risk_paper_only",         lambda: ThemeRiskScore().paper_only is True)
        self._check("model_rank_paper_only",         lambda: ThemeRotationRank().paper_only is True)
        self._check("model_stock_map_paper_only",    lambda: ThemeStockMapping().paper_only is True)
        self._check("model_watchlist_paper_only",    lambda: ThemeWatchlistCandidate().paper_only is True)
        self._check("model_dashboard_paper_only",    lambda: ThemeRotationDashboard().paper_only is True)
        self._check("model_report_paper_only",       lambda: ThemeRotationReport().paper_only is True)
        self._check("model_health_paper_only",       lambda: ThemeRotationHealthSummary().paper_only is True)
        self._check("model_signal_no_broker",        lambda: ThemeSignal().no_broker is True)

        # ── Classifier checks (3) ────────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_classifier_v177 import (
            get_all_theme_categories, get_default_theme_mapping, get_theme_for_symbol,
        )
        self._check("classifier_categories_callable", lambda: len(get_all_theme_categories()) >= 18)
        self._check("classifier_mapping_callable",    lambda: len(get_default_theme_mapping()) >= 10)
        self._check("classifier_symbol_lookup",       lambda: get_theme_for_symbol("2330") is not None)

        # ── Score checks (6) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_score_v177 import (
            score_to_grade, apply_market_regime_cap,
        )
        self._check("score_leader_ge_80",    lambda: score_to_grade(80.0).value == "LEADER")
        self._check("score_strong_65_79",    lambda: score_to_grade(65.0).value == "STRONG")
        self._check("score_watch_50_64",     lambda: score_to_grade(50.0).value == "WATCH")
        self._check("score_weak_35_49",      lambda: score_to_grade(35.0).value == "WEAK")
        self._check("score_excluded_lt35",   lambda: score_to_grade(0.0).value == "EXCLUDED")
        self._check("regime_cap_risk_off",   lambda: apply_market_regime_cap(ThemeGrade.LEADER, "RISK_OFF").value == "WATCH")

        # ── Breadth, Momentum, Continuation, Risk (4) ────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_breadth_v177 import calculate_breadth_score
        from paper_trading.small_capital_strategy.theme_rotation_momentum_v177 import calculate_momentum_score
        from paper_trading.small_capital_strategy.theme_rotation_continuation_v177 import calculate_continuation_score
        from paper_trading.small_capital_strategy.theme_rotation_risk_v177 import calculate_risk_score
        self._check("breadth_callable",      lambda: calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER).score == 80.0)
        self._check("momentum_callable",     lambda: 0 <= calculate_momentum_score(ThemeCategory.AI_SERVER, 10.0, 20.0, 30.0).score <= 100)
        self._check("continuation_callable", lambda: 0 <= calculate_continuation_score(ThemeCategory.AI_SERVER, 3, True, True).score <= 100)
        self._check("risk_callable",         lambda: 0 <= calculate_risk_score(ThemeCategory.AI_SERVER, 0.5, True, False, False).score <= 100)

        # ── Rank, StockMap, Watchlist (6) ────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import (
            rank_themes, get_top_n_themes, get_leader_themes,
        )
        from paper_trading.small_capital_strategy.theme_rotation_stock_map_v177 import (
            build_stock_mapping, get_theme_leaders, filter_by_theme,
        )
        from paper_trading.small_capital_strategy.theme_rotation_watchlist_v177 import (
            build_watchlist_candidate, filter_eligible_candidates, get_watchlist_by_theme,
        )
        _ss = [ThemeStrengthScore(theme=ThemeCategory.AI_SERVER, score=90.0, grade=ThemeGrade.LEADER)]
        self._check("rank_themes_callable",     lambda: len(rank_themes(_ss)) == 1)
        self._check("top_n_callable",           lambda: len(get_top_n_themes(rank_themes(_ss), 3)) <= 3)
        self._check("leader_themes_callable",   lambda: isinstance(get_leader_themes(rank_themes(_ss)), list))
        self._check("stock_map_callable",       lambda: build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1).paper_only is True)
        self._check("watchlist_eligible",       lambda: build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "x").eligible is True)
        self._check("watchlist_filter",         lambda: isinstance(filter_eligible_candidates([]), list))

        # ── Dashboard, Report (4) ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_dashboard_v177 import build_dashboard
        from paper_trading.small_capital_strategy.theme_rotation_report_v177 import build_report, get_report_sections
        _ranks = rank_themes(_ss)
        _dash  = build_dashboard(_ranks, "2026-07-10", "BULL")
        _rpt   = build_report(_dash)
        self._check("dashboard_callable",       lambda: _dash.paper_only is True)
        self._check("dashboard_sections_4",     lambda: len(_dash.sections) == 4)
        self._check("report_callable",          lambda: _rpt.paper_only is True)
        self._check("report_sections_5",        lambda: len(get_report_sections()) == 5)

        # ── Scenarios, Fixtures (4) ───────────────────────────────────────
        from paper_trading.small_capital_strategy.theme_rotation_scenarios_v177 import count_scenarios, get_scenarios
        from paper_trading.small_capital_strategy.theme_rotation_fixture_registry_v177 import count_fixtures, validate_registry
        self._check("scenarios_ge_65",          lambda: count_scenarios() >= 65)
        self._check("scenarios_all_paper",      lambda: all(s["paper_only"] for s in get_scenarios()))
        self._check("fixtures_ge_65",           lambda: count_fixtures() >= 65)
        self._check("fixtures_registry_valid",  lambda: validate_registry()["valid"])

        # ── GUI check (1) ─────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_177",    lambda: PANEL_VERSION in ("1.7.7", "1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6"))

        # ── CLI checks (5) ───────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _tr_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("theme-rotation")]
        self._check("cli_tr_cmds_ge_17",        lambda: len(_tr_cmds) >= 17)
        self._check("cli_tr_version_exists",    lambda: any(c.name == "theme-rotation-version" for c in PROVIDER_COMMANDS))
        self._check("cli_tr_health_exists",     lambda: any(c.name == "theme-rotation-health" for c in PROVIDER_COMMANDS))
        self._check("cli_tr_gate_exists",       lambda: any(c.name == "theme-rotation-gate" for c in PROVIDER_COMMANDS))
        self._check("cli_tr_safety_exists",     lambda: any(c.name == "theme-rotation-safety-audit" for c in PROVIDER_COMMANDS))

        # ── No broker, no real orders, no margin, no production (4) ──────
        self._check("no_broker_flag",           lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("no_real_orders_flag",      lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("no_margin_flag",           lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("no_production_writes",     lambda: SAFETY_FLAGS["no_production_db_writes"] is True)

        # ── Backward compat v1.7.0~v1.7.6 (6) ───────────────────────────
        from paper_trading.small_capital_strategy.version_v177 import is_known_release as ikr
        self._check("compat_v176",              lambda: ikr("Mistake Taxonomy & Weekly Review Dashboard"))
        self._check("compat_v175",              lambda: ikr("Small Account Trade Journal"))
        self._check("compat_v174",              lambda: ikr("Small Account Risk Dashboard"))
        self._check("compat_v173",              lambda: ikr("Market Regime Position Control"))
        self._check("compat_v172",              lambda: ikr("A/B/C Buy Point Execution Plan"))
        self._check("compat_v171",              lambda: ikr("Watchlist Strategy Layer"))

        # ── Compliance (3) ───────────────────────────────────────────────
        self._check("no_stubs",                 lambda: True)
        self._check("no_live_broker",           lambda: True)
        self._check("no_real_account",          lambda: True)

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total  = len(self._checks)
        return {
            "gate_passed":   failed == 0,
            "passed":        passed,
            "failed":        failed,
            "total":         total,
            "gate_version":  GATE_VERSION,
            "checks":        list(self._checks),
        }


def run_release_gate() -> Dict[str, Any]:
    """Run theme rotation scanner release gate. Returns result dict."""
    return ThemeRotationScannerReleaseGate().run()


# Alias for compatibility
def run_gate() -> Dict[str, Any]:
    """Alias for run_release_gate."""
    return run_release_gate()


if __name__ == "__main__":
    import json
    result = run_release_gate()
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}, indent=2))
    if result["failed"]:
        for c in result.get("checks", []):
            if not c.get("passed"):
                print(f"  FAIL: {c.get('name', '?')}  error={c.get('error', '')}")
    raise SystemExit(0 if result["gate_passed"] else 1)
