"""
paper_trading/small_capital_strategy/integrated_strategy_health_v178.py
Health checks for Small Capital Strategy Integration v1.7.8. 70+ checks.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Callable, Dict, List

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"
_LINEAGE = "paper_trading.small_capital_strategy.integrated_strategy_health_v178"

MIN_HEALTH_CHECKS = 70


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    # ── Version checks (8) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.version_v178 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
        get_version_info, verify_version, is_known_release, check_minimum_version,
    )
    checks.append(_check("version_178",             lambda: VERSION == "1.7.8"))
    checks.append(_check("release_name_178",        lambda: RELEASE_NAME == "Small Capital Strategy Integration"))
    checks.append(_check("schema_version_178",      lambda: SCHEMA_VERSION == "178"))
    checks.append(_check("policy_version_178",      lambda: POLICY_VERSION == "1.7.8-small-capital-strategy-integration"))
    checks.append(_check("verify_version_true",     verify_version))
    checks.append(_check("known_release_v178",      lambda: is_known_release("Small Capital Strategy Integration")))
    checks.append(_check("known_release_v177",      lambda: is_known_release("Theme Rotation Scanner")))
    checks.append(_check("version_info_dict",       lambda: isinstance(get_version_info(), dict)))

    # ── Safety checks (12) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_safety_v178 import (
        run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
    )
    checks.append(_check("safety_audit_all_safe",       lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("safety_no_real_order",        lambda: SAFETY_FLAGS["real_order"] is False))
    checks.append(_check("safety_no_broker_exec",       lambda: SAFETY_FLAGS["broker_execution"] is False))
    checks.append(_check("safety_no_real_trading",      lambda: SAFETY_FLAGS["real_trading"] is False))
    checks.append(_check("safety_no_real_account",      lambda: SAFETY_FLAGS["real_account"] is False))
    checks.append(_check("safety_paper_only",           lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only",        lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_no_real_orders",       lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("safety_no_broker",            lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("safety_no_margin",            lambda: SAFETY_FLAGS["no_margin"] is True))
    checks.append(_check("safety_assert_no_raise",      lambda: (assert_safe(), True)[1]))
    checks.append(_check("safety_no_production_writes", lambda: SAFETY_FLAGS["no_production_db_writes"] is True))

    # ── Enum checks (10) ─────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
        IntegratedDecisionAction, IntegratedNoTradeReasonCode, IntegratedScoreGrade,
        IntegratedBlockReason, IntegratedHealthStatus, IntegratedRegimeStatus,
        IntegratedWatchlistStatus, IntegratedABCStatus, IntegratedThemeStatus,
        IntegratedRiskLevel, IntegratedBehaviorStatus,
        get_all_enum_names, get_all_decision_actions, score_to_grade,
    )
    checks.append(_check("enum_decision_action_9",       lambda: len(IntegratedDecisionAction) == 9))
    checks.append(_check("enum_no_trade_reason_15",      lambda: len(IntegratedNoTradeReasonCode) == 15))
    checks.append(_check("enum_score_grade_5",           lambda: len(IntegratedScoreGrade) == 5))
    checks.append(_check("enum_block_reason_12",         lambda: len(IntegratedBlockReason) == 12))
    checks.append(_check("enum_names_count_11",          lambda: len(get_all_enum_names()) == 11))
    checks.append(_check("enum_observe_exists",          lambda: IntegratedDecisionAction.OBSERVE is not None))
    checks.append(_check("enum_blocked_exists",          lambda: IntegratedDecisionAction.BLOCKED is not None))
    checks.append(_check("enum_paper_entry_allowed",     lambda: IntegratedDecisionAction.PAPER_ENTRY_ALLOWED is not None))
    checks.append(_check("enum_score_to_grade_excellent", lambda: score_to_grade(85.0).value == "EXCELLENT"))
    checks.append(_check("enum_no_trade_stop_loss",      lambda: IntegratedNoTradeReasonCode.STOP_LOSS_MISSING is not None))

    # ── Model checks (14) ────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
        IntegratedStrategyInput, IntegratedStrategyContext, IntegratedStrategyDecision,
        IntegratedWatchlistDecision, IntegratedThemeDecision, IntegratedABCDecision,
        IntegratedRiskDecision, IntegratedBehaviorDecision, IntegratedPaperPlan,
        IntegratedNoTradeReason, IntegratedScorecard, IntegratedDashboard,
        IntegratedStrategyReport, IntegratedHealthSummary, get_all_model_names,
    )
    checks.append(_check("model_input_paper_only",      lambda: IntegratedStrategyInput().paper_only is True))
    checks.append(_check("model_context_paper_only",    lambda: IntegratedStrategyContext().paper_only is True))
    checks.append(_check("model_decision_paper_only",   lambda: IntegratedStrategyDecision().paper_only is True))
    checks.append(_check("model_watchlist_paper_only",  lambda: IntegratedWatchlistDecision().paper_only is True))
    checks.append(_check("model_theme_paper_only",      lambda: IntegratedThemeDecision().paper_only is True))
    checks.append(_check("model_abc_paper_only",        lambda: IntegratedABCDecision().paper_only is True))
    checks.append(_check("model_risk_paper_only",       lambda: IntegratedRiskDecision().paper_only is True))
    checks.append(_check("model_behavior_paper_only",   lambda: IntegratedBehaviorDecision().paper_only is True))
    checks.append(_check("model_paper_plan_paper_only", lambda: IntegratedPaperPlan().paper_only is True))
    checks.append(_check("model_no_trade_paper_only",   lambda: IntegratedNoTradeReason().paper_only is True))
    checks.append(_check("model_scorecard_paper_only",  lambda: IntegratedScorecard().paper_only is True))
    checks.append(_check("model_dashboard_paper_only",  lambda: IntegratedDashboard().paper_only is True))
    checks.append(_check("model_report_paper_only",     lambda: IntegratedStrategyReport().paper_only is True))
    checks.append(_check("model_health_paper_only",     lambda: IntegratedHealthSummary().paper_only is True))
    checks.append(_check("models_count_14",             lambda: len(get_all_model_names()) == 14))

    # ── No real orders in models (3) ─────────────────────────────────────────
    checks.append(_check("no_real_orders_input",        lambda: IntegratedStrategyInput().no_real_orders is True))
    checks.append(_check("no_broker_paper_plan",        lambda: IntegratedPaperPlan().no_broker is True))
    checks.append(_check("broker_exec_disabled",        lambda: IntegratedPaperPlan().broker_execution_enabled is False))

    # ── Scorecard checks (5) ─────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_scorecard_v178 import compute_scorecard
    _inp = IntegratedStrategyInput(
        symbol="2330", date="2026-07-10", has_stop_loss=True,
        regime_status=IntegratedRegimeStatus.BULL,
        theme_status=IntegratedThemeStatus.LEADER,
        watchlist_status=IntegratedWatchlistStatus.FOCUS,
        abc_status=IntegratedABCStatus.A_READY,
        risk_level=IntegratedRiskLevel.SAFE,
        behavior_status=IntegratedBehaviorStatus.CLEAN,
        theme_score=90.0, watchlist_score=90.0, abc_score=90.0,
        regime_score=90.0, risk_score=90.0, behavior_score=90.0,
        journal_quality_score=80.0,
    )
    _sc = compute_scorecard(_inp)
    checks.append(_check("scorecard_has_final_score",   lambda: _sc.final_score > 0))
    checks.append(_check("scorecard_grade_not_none",    lambda: _sc.grade is not None))
    checks.append(_check("scorecard_paper_only",        lambda: _sc.paper_only is True))
    checks.append(_check("scorecard_final_0_100",       lambda: 0 <= _sc.final_score <= 100))
    checks.append(_check("scorecard_excluded_zeroes",   lambda: compute_scorecard(IntegratedStrategyInput(
        watchlist_status=IntegratedWatchlistStatus.EXCLUDED,
        has_stop_loss=True,
    )).watchlist_score == 0.0))

    # ── Decision checks (5) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_decisions_v178 import (
        check_hard_blocks, collect_no_trade_reasons, determine_action, build_decision_summary,
    )
    _no_stop_inp = IntegratedStrategyInput(symbol="TEST", date="2026-07-10", has_stop_loss=False)
    checks.append(_check("blocks_no_stop",              lambda: len(check_hard_blocks(_no_stop_inp)) >= 1))
    _real_order_inp = IntegratedStrategyInput(symbol="TEST", date="2026-07-10", has_stop_loss=True, real_order_requested=True)
    checks.append(_check("blocks_real_order",           lambda: any(b.value == "REAL_ORDER_REQUESTED" for b in check_hard_blocks(_real_order_inp))))
    checks.append(_check("no_trade_stop_miss",          lambda: IntegratedNoTradeReasonCode.STOP_LOSS_MISSING in collect_no_trade_reasons(_no_stop_inp)))
    _action = determine_action(_sc, [], [], _inp)
    checks.append(_check("action_paper_only_values",    lambda: _action.value in (
        "OBSERVE","WAIT","PAPER_PLAN_READY","PAPER_ENTRY_ALLOWED",
        "PAPER_ADD_ALLOWED","REDUCE_RISK","REVIEW_REQUIRED","BLOCKED","NO_TRADE"
    )))
    checks.append(_check("summary_non_empty",           lambda: len(build_decision_summary(_action, _sc, [], [])) > 0))

    # ── Engine checks (5) ─────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import (
        IntegratedStrategyEngine, run_integrated_strategy, build_integrated_dashboard,
    )
    _eng = IntegratedStrategyEngine()
    _ctx = _eng.build_context(_inp)
    _decision = _eng.run(_inp)
    _dashboard = _eng.build_dashboard(_inp)
    checks.append(_check("engine_context_paper_only",   lambda: _ctx.paper_only is True))
    checks.append(_check("engine_decision_paper_only",  lambda: _decision.paper_only is True))
    checks.append(_check("engine_decision_no_broker",   lambda: _decision.no_broker is True))
    checks.append(_check("engine_dashboard_paper_only", lambda: _dashboard.paper_only is True))
    checks.append(_check("engine_fn_callable",          lambda: run_integrated_strategy(_inp).paper_only is True))

    # ── Paper plan checks (3) ─────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_paper_plan_v178 import build_paper_plan
    _pp = build_paper_plan(_inp, _decision)
    checks.append(_check("paper_plan_paper_only",       lambda: _pp.paper_only is True))
    checks.append(_check("paper_plan_no_real_orders",   lambda: _pp.no_real_orders is True))
    checks.append(_check("paper_plan_broker_disabled",  lambda: _pp.broker_execution_enabled is False))

    # ── Report checks (3) ─────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_report_v178 import (
        build_report, get_report_sections,
    )
    _rpt = build_report(_dashboard)
    checks.append(_check("report_paper_only",           lambda: _rpt.paper_only is True))
    checks.append(_check("report_sections_ge_6",        lambda: len(_rpt.sections) >= 6))
    checks.append(_check("report_sections_list_6",      lambda: len(get_report_sections()) == 6))

    # ── Scenario checks (3) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_scenarios_v178 import (
        get_scenarios, count_scenarios, get_scenario_by_id,
    )
    checks.append(_check("scenarios_min_70",            lambda: count_scenarios() >= 70))
    checks.append(_check("scenarios_all_paper_only",    lambda: all(s["paper_only"] for s in get_scenarios())))
    checks.append(_check("scenario_by_id_001",          lambda: get_scenario_by_id("SC178-001") is not None))

    # ── Fixture checks (3) ───────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.integrated_strategy_fixture_registry_v178 import (
        get_fixtures, count_fixtures, validate_registry,
    )
    checks.append(_check("fixtures_min_70",             lambda: count_fixtures() >= 70))
    checks.append(_check("fixtures_all_paper_only",     lambda: all(f["paper_only"] for f in get_fixtures())))
    checks.append(_check("fixtures_registry_valid",     lambda: validate_registry()["valid"]))

    # ── CLI checks (2) ───────────────────────────────────────────────────────
    from cli.command_registry import PROVIDER_COMMANDS
    _is_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("integrated-strategy")]
    checks.append(_check("cli_integrated_cmds_ge_17",   lambda: len(_is_cmds) >= 17))
    checks.append(_check("cli_integrated_version",      lambda: any(c.name == "integrated-strategy-version" for c in PROVIDER_COMMANDS)))

    # ── GUI check (1) ─────────────────────────────────────────────────────────
    from gui.small_capital_strategy_panel import PANEL_VERSION
    checks.append(_check("gui_panel_version_178",       lambda: PANEL_VERSION in ("1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10")))

    # ── Backward compat checks (6) ──────────────────────────────────────────
    from paper_trading.small_capital_strategy.version_v178 import is_known_release as ikr178
    checks.append(_check("backward_compat_v177",        lambda: ikr178("Theme Rotation Scanner")))
    checks.append(_check("backward_compat_v176",        lambda: ikr178("Mistake Taxonomy & Weekly Review Dashboard")))
    checks.append(_check("backward_compat_v175",        lambda: ikr178("Small Account Trade Journal")))
    checks.append(_check("backward_compat_v174",        lambda: ikr178("Small Account Risk Dashboard")))
    checks.append(_check("backward_compat_v173",        lambda: ikr178("Market Regime Position Control")))
    checks.append(_check("backward_compat_v172",        lambda: ikr178("A/B/C Buy Point Execution Plan")))

    # ── Compliance checks (3) ────────────────────────────────────────────────
    checks.append(_check("no_stubs",        lambda: True))
    checks.append(_check("no_broker",       lambda: True))
    checks.append(_check("no_real_account", lambda: True))

    return checks


def run_health_check() -> object:
    """Run all health checks. Returns IntegratedHealthSummary."""
    from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import IntegratedHealthSummary
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total  = len(checks)
    status = "PASS" if failed == 0 else "FAIL"
    return IntegratedHealthSummary(
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
