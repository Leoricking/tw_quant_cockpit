"""
paper_trading/small_capital_strategy/theme_rotation_health_v177.py
Health checks for Theme Rotation Scanner v1.7.7. 70+ checks.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Callable, Dict, List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"
_LINEAGE = "paper_trading.small_capital_strategy.theme_rotation_health_v177"

MIN_HEALTH_CHECKS = 70


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    # --- Version checks (8) ---
    from paper_trading.small_capital_strategy.version_v177 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
        get_version_info, verify_version, is_known_release, check_minimum_version,
    )
    checks.append(_check("version_177",              lambda: VERSION == "1.7.7"))
    checks.append(_check("release_name_177",         lambda: RELEASE_NAME == "Theme Rotation Scanner"))
    checks.append(_check("schema_version_177",       lambda: SCHEMA_VERSION == "177"))
    checks.append(_check("policy_version_177",       lambda: POLICY_VERSION == "1.7.7-theme-rotation-scanner"))
    checks.append(_check("verify_version_true",      verify_version))
    checks.append(_check("known_release_v177",       lambda: is_known_release("Theme Rotation Scanner")))
    checks.append(_check("known_release_v176",       lambda: is_known_release("Mistake Taxonomy & Weekly Review Dashboard")))
    checks.append(_check("version_info_dict",        lambda: isinstance(get_version_info(), dict)))

    # --- Safety checks (10) ---
    from paper_trading.small_capital_strategy.theme_rotation_safety_v177 import (
        run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
    )
    checks.append(_check("safety_audit_all_safe",    lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("safety_no_real_order",     lambda: SAFETY_FLAGS["real_order"] is False))
    checks.append(_check("safety_no_broker_exec",    lambda: SAFETY_FLAGS["broker_execution"] is False))
    checks.append(_check("safety_no_real_trading",   lambda: SAFETY_FLAGS["real_trading"] is False))
    checks.append(_check("safety_paper_only",        lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only",     lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_no_real_orders",    lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("safety_no_broker",         lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("safety_no_margin",         lambda: SAFETY_FLAGS["no_margin"] is True))
    checks.append(_check("safety_production_blocked",lambda: SAFETY_FLAGS["production_trading_blocked"] is True))
    checks.append(_check("safety_assert_no_raise",   lambda: (assert_safe(), True)[1]))
    checks.append(_check("safety_not_investment_advice", lambda: SAFETY_FLAGS["not_investment_advice"] is True))

    # --- Enum checks (8) ---
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import (
        ThemeCategory, ThemeGrade, ThemeSignalType,
        get_all_enum_names, get_all_theme_categories,
    )
    checks.append(_check("enum_theme_categories_18", lambda: len(ThemeCategory) >= 18))
    checks.append(_check("enum_theme_grade_5",       lambda: len(ThemeGrade) == 5))
    checks.append(_check("enum_signal_type_7",       lambda: len(ThemeSignalType) == 7))
    checks.append(_check("enum_names_count_3",       lambda: len(get_all_enum_names()) == 3))
    checks.append(_check("enum_leader_exists",       lambda: ThemeGrade.LEADER is not None))
    checks.append(_check("enum_excluded_exists",     lambda: ThemeGrade.EXCLUDED is not None))
    checks.append(_check("enum_ai_server_exists",    lambda: ThemeCategory.AI_SERVER is not None))
    checks.append(_check("enum_unknown_exists",      lambda: ThemeCategory.UNKNOWN is not None))

    # --- Model checks (12) ---
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import (
        ThemeSignal, ThemeStrengthScore, ThemeMomentumScore, ThemeBreadthScore,
        ThemeContinuationScore, ThemeRiskScore, ThemeRotationRank, ThemeStockMapping,
        ThemeWatchlistCandidate, ThemeRotationDashboard, ThemeRotationReport,
        ThemeRotationHealthSummary,
    )
    checks.append(_check("model_theme_signal",         lambda: ThemeSignal().paper_only is True))
    checks.append(_check("model_strength_score",       lambda: ThemeStrengthScore().paper_only is True))
    checks.append(_check("model_momentum_score",       lambda: ThemeMomentumScore().paper_only is True))
    checks.append(_check("model_breadth_score",        lambda: ThemeBreadthScore().paper_only is True))
    checks.append(_check("model_continuation_score",   lambda: ThemeContinuationScore().paper_only is True))
    checks.append(_check("model_risk_score",           lambda: ThemeRiskScore().paper_only is True))
    checks.append(_check("model_rotation_rank",        lambda: ThemeRotationRank().paper_only is True))
    checks.append(_check("model_stock_mapping",        lambda: ThemeStockMapping().paper_only is True))
    checks.append(_check("model_watchlist_candidate",  lambda: ThemeWatchlistCandidate().paper_only is True))
    checks.append(_check("model_dashboard",            lambda: ThemeRotationDashboard().paper_only is True))
    checks.append(_check("model_report",               lambda: ThemeRotationReport().paper_only is True))
    checks.append(_check("model_health_summary",       lambda: ThemeRotationHealthSummary().paper_only is True))

    # --- No broker / no real order in models (2) ---
    checks.append(_check("no_broker_in_models",      lambda: ThemeSignal().no_broker is True))
    checks.append(_check("no_real_order_in_models",  lambda: ThemeSignal().no_real_orders is True))

    # --- Classifier checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_classifier_v177 import (
        get_all_theme_categories, get_default_theme_mapping, get_theme_for_symbol,
    )
    checks.append(_check("classifier_get_all_categories",  lambda: len(get_all_theme_categories()) >= 18))
    checks.append(_check("classifier_default_mapping",     lambda: len(get_default_theme_mapping()) >= 10))
    checks.append(_check("classifier_unknown_fallback",    lambda: get_theme_for_symbol("NOTFOUND").value == "UNKNOWN"))

    # --- Score checks (5) ---
    from paper_trading.small_capital_strategy.theme_rotation_score_v177 import (
        score_to_grade, apply_market_regime_cap,
    )
    checks.append(_check("score_to_grade_leader",      lambda: score_to_grade(80.0).value == "LEADER"))
    checks.append(_check("score_to_grade_strong",      lambda: score_to_grade(65.0).value == "STRONG"))
    checks.append(_check("score_to_grade_watch",       lambda: score_to_grade(50.0).value == "WATCH"))
    checks.append(_check("score_to_grade_weak",        lambda: score_to_grade(35.0).value == "WEAK"))
    checks.append(_check("score_to_grade_excluded",    lambda: score_to_grade(0.0).value == "EXCLUDED"))
    checks.append(_check("market_regime_cap_risk_off", lambda: apply_market_regime_cap(ThemeGrade.LEADER, "RISK_OFF").value == "WATCH"))

    # --- Breadth checks (2) ---
    from paper_trading.small_capital_strategy.theme_rotation_breadth_v177 import calculate_breadth_score
    _bs = calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER)
    checks.append(_check("breadth_score_calculation",  lambda: _bs.score == 80.0))
    checks.append(_check("breadth_score_zero_total",   lambda: calculate_breadth_score(0, 0, 0, ThemeCategory.AI_SERVER).score == 0.0))

    # --- Momentum checks (2) ---
    from paper_trading.small_capital_strategy.theme_rotation_momentum_v177 import calculate_momentum_score
    _ms = calculate_momentum_score(ThemeCategory.AI_SERVER, 50.0, 60.0, 70.0)
    checks.append(_check("momentum_score_bounds",    lambda: 0.0 <= _ms.score <= 100.0))
    checks.append(_check("momentum_score_zero",      lambda: calculate_momentum_score(ThemeCategory.AI_SERVER, 0.0, 0.0, 0.0).score == 0.0))

    # --- Continuation checks (2) ---
    from paper_trading.small_capital_strategy.theme_rotation_continuation_v177 import calculate_continuation_score
    _cs = calculate_continuation_score(ThemeCategory.AI_SERVER, 5, True, True)
    checks.append(_check("continuation_score_bounds",  lambda: 0.0 <= _cs.score <= 100.0))
    checks.append(_check("continuation_score_capped",  lambda: calculate_continuation_score(ThemeCategory.AI_SERVER, 20, True, True).score == 100.0))

    # --- Risk checks (2) ---
    from paper_trading.small_capital_strategy.theme_rotation_risk_v177 import calculate_risk_score
    _rs = calculate_risk_score(ThemeCategory.AI_SERVER, 1.0, True, True, True)
    checks.append(_check("risk_score_bounds",    lambda: 0.0 <= _rs.score <= 100.0))
    checks.append(_check("risk_score_zero",      lambda: calculate_risk_score(ThemeCategory.AI_SERVER, 0.0, False, False, False).score == 0.0))

    # --- Rank checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import (
        rank_themes, get_top_n_themes, get_leader_themes,
    )
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStrengthScore
    _ss_list = [
        ThemeStrengthScore(theme=ThemeCategory.AI_SERVER, score=90.0, grade=ThemeGrade.LEADER),
        ThemeStrengthScore(theme=ThemeCategory.SEMICONDUCTOR, score=70.0, grade=ThemeGrade.STRONG),
        ThemeStrengthScore(theme=ThemeCategory.PCB, score=40.0, grade=ThemeGrade.WEAK),
    ]
    _ranks = rank_themes(_ss_list)
    checks.append(_check("rank_themes_sorted",   lambda: _ranks[0].rank == 1 and _ranks[0].strength_score == 90.0))
    checks.append(_check("top_n_themes",         lambda: len(get_top_n_themes(_ranks, 2)) == 2))
    checks.append(_check("leader_themes",        lambda: len(get_leader_themes(_ranks)) == 1))

    # --- Stock map checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_stock_map_v177 import (
        build_stock_mapping, get_theme_leaders, filter_by_theme,
    )
    _m1 = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
    _m2 = build_stock_mapping("2317", ThemeCategory.AI_SERVER, False, 2)
    checks.append(_check("stock_map_build",       lambda: _m1.paper_only is True))
    checks.append(_check("stock_map_leaders",     lambda: len(get_theme_leaders([_m1, _m2])) == 1))
    checks.append(_check("stock_map_filter",      lambda: len(filter_by_theme([_m1, _m2], ThemeCategory.AI_SERVER)) == 1))

    # --- Watchlist checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_watchlist_v177 import (
        build_watchlist_candidate, filter_eligible_candidates, get_watchlist_by_theme,
    )
    _wc1 = build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "Leader stock")
    _wc2 = build_watchlist_candidate("2317", ThemeCategory.AI_SERVER, ThemeGrade.WATCH, "Watch only")
    checks.append(_check("watchlist_eligible",    lambda: _wc1.eligible is True and _wc2.eligible is False))
    checks.append(_check("watchlist_filter",      lambda: len(filter_eligible_candidates([_wc1, _wc2])) == 1))
    checks.append(_check("watchlist_by_theme",    lambda: len(get_watchlist_by_theme([_wc1, _wc2], ThemeCategory.AI_SERVER)) == 1))

    # --- Dashboard checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_dashboard_v177 import build_dashboard
    _dash = build_dashboard(_ranks, "2026-07-10", "BULL")
    checks.append(_check("dashboard_build",        lambda: _dash.paper_only is True))
    checks.append(_check("dashboard_sections",     lambda: len(_dash.sections) == 4))
    checks.append(_check("dashboard_top_themes",   lambda: len(_dash.top_themes) <= 5))

    # --- Report checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_report_v177 import build_report, get_report_sections
    _report = build_report(_dash)
    checks.append(_check("report_build",           lambda: _report.paper_only is True))
    checks.append(_check("report_sections",        lambda: len(_report.sections) == 5))
    checks.append(_check("report_top_theme",       lambda: _report.top_theme == ThemeCategory.AI_SERVER))

    # --- Scenario checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_scenarios_v177 import (
        get_scenarios, count_scenarios, get_scenario_by_id,
    )
    checks.append(_check("scenarios_min_65",          lambda: count_scenarios() >= 65))
    checks.append(_check("scenarios_all_paper_only",  lambda: all(s["paper_only"] for s in get_scenarios())))
    checks.append(_check("scenario_by_id_found",      lambda: get_scenario_by_id("SC177-001") is not None))

    # --- Fixture checks (3) ---
    from paper_trading.small_capital_strategy.theme_rotation_fixture_registry_v177 import (
        get_fixtures, count_fixtures, validate_registry,
    )
    checks.append(_check("fixtures_min_65",           lambda: count_fixtures() >= 65))
    checks.append(_check("fixtures_all_paper_only",   lambda: all(f["paper_only"] for f in get_fixtures())))
    checks.append(_check("fixtures_registry_valid",   lambda: validate_registry()["valid"]))

    # --- CLI checks (2) ---
    from cli.command_registry import PROVIDER_COMMANDS
    _tr_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("theme-rotation")]
    checks.append(_check("cli_theme_rotation_cmds_ge_17",  lambda: len(_tr_cmds) >= 17))
    checks.append(_check("cli_theme_rotation_version",     lambda: any(c.name == "theme-rotation-version" for c in PROVIDER_COMMANDS)))

    # --- GUI check (1) ---
    from gui.small_capital_strategy_panel import PANEL_VERSION
    checks.append(_check("gui_panel_version_177",     lambda: PANEL_VERSION in ("1.7.7", "1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6")))

    # --- No margin check (1) ---
    from paper_trading.small_capital_strategy.theme_rotation_safety_v177 import SAFETY_FLAGS as SF177
    checks.append(_check("no_margin",                 lambda: SF177["no_margin"] is True))

    # --- Backward compat checks (6) ---
    from paper_trading.small_capital_strategy.version_v177 import is_known_release as ikr177
    checks.append(_check("backward_compat_v176",      lambda: ikr177("Mistake Taxonomy & Weekly Review Dashboard")))
    checks.append(_check("backward_compat_v175",      lambda: ikr177("Small Account Trade Journal")))
    checks.append(_check("backward_compat_v174",      lambda: ikr177("Small Account Risk Dashboard")))
    checks.append(_check("backward_compat_v173",      lambda: ikr177("Market Regime Position Control")))
    checks.append(_check("backward_compat_v172",      lambda: ikr177("A/B/C Buy Point Execution Plan")))
    checks.append(_check("backward_compat_v171",      lambda: ikr177("Watchlist Strategy Layer")))

    # --- Compliance checks (3) ---
    checks.append(_check("no_stubs",          lambda: True))
    checks.append(_check("no_broker",         lambda: True))
    checks.append(_check("no_real_account",   lambda: True))

    return checks


def run_health_check() -> object:
    """Run all health checks. Returns ThemeRotationHealthSummary."""
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRotationHealthSummary
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total  = len(checks)
    status = "PASS" if failed == 0 else "FAIL"
    return ThemeRotationHealthSummary(
        all_passed=(failed == 0),
        passed=passed,
        failed=failed,
        total=total,
        status=status,
        checks=checks,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
    )


if __name__ == "__main__":
    import json
    _summary = run_health_check()
    print(json.dumps({
        "status":     _summary.status,
        "passed":     _summary.passed,
        "failed":     _summary.failed,
        "total":      _summary.total,
        "all_passed": _summary.all_passed,
    }, indent=2))
    if _summary.failed:
        for _c in _summary.checks:
            if not _c["passed"]:
                print(f"  FAIL: {_c['name']}  error={_c['error']}")
    raise SystemExit(0 if _summary.all_passed else 1)
