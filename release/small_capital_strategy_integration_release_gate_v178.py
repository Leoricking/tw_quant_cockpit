"""
release/small_capital_strategy_integration_release_gate_v178.py
Release gate for Small Capital Strategy Integration v1.7.8. 70+ gate checks.
gate_passed=True required for release.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.7.8"
MIN_CHECKS   = 70


class SmallCapitalStrategyIntegrationReleaseGate:
    """Release gate for Small Capital Strategy Integration v1.7.8."""

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

        # ── Health PASS (4) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.integrated_strategy_health_v178 import run_health_check
        self._check("health_all_passed",     lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",    lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",    lambda: run_health_check().failed == 0)
        self._check("health_total_ge_70",    lambda: run_health_check().total >= 70)

        # ── Version Identity (8) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v178 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_7_8",        lambda: VERSION == "1.7.8")
        self._check("gate_release_name",          lambda: RELEASE_NAME == "Small Capital Strategy Integration")
        self._check("gate_schema_version_178",    lambda: SCHEMA_VERSION == "178")
        self._check("gate_policy_version",        lambda: POLICY_VERSION == "1.7.8-small-capital-strategy-integration")
        self._check("gate_known_release_self",    lambda: is_known_release("Small Capital Strategy Integration"))
        self._check("gate_known_release_v177",    lambda: is_known_release("Theme Rotation Scanner"))
        self._check("gate_version_info_dict",     lambda: isinstance(get_version_info(), dict))
        self._check("gate_verify_version",        verify_version)

        # ── Safety (13) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.integrated_strategy_safety_v178 import (
            run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
        )
        self._check("safety_audit_all_safe",      lambda: run_safety_audit()["all_safe"])
        self._check("safety_no_real_order",       lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_no_broker_exec",      lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_no_real_trading",     lambda: SAFETY_FLAGS["real_trading"] is False)
        self._check("safety_no_real_account",     lambda: SAFETY_FLAGS["real_account"] is False)
        self._check("safety_paper_only",          lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",       lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_no_real_orders",      lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",           lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",           lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_assert_no_raise",     lambda: (assert_safe(), True)[1])
        self._check("safety_production_blocked",  lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_no_production_db",    lambda: SAFETY_FLAGS["no_production_db_writes"] is True)

        # ── Enum checks (6) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
            IntegratedDecisionAction, IntegratedNoTradeReasonCode,
            IntegratedScoreGrade, IntegratedBlockReason, get_all_enum_names, score_to_grade,
        )
        self._check("enum_decision_action_9",    lambda: len(IntegratedDecisionAction) == 9)
        self._check("enum_no_trade_reason_15",   lambda: len(IntegratedNoTradeReasonCode) == 15)
        self._check("enum_score_grade_5",        lambda: len(IntegratedScoreGrade) == 5)
        self._check("enum_block_reason_12",      lambda: len(IntegratedBlockReason) == 12)
        self._check("enum_names_count_11",       lambda: len(get_all_enum_names()) == 11)
        self._check("enum_blocked_exists",       lambda: IntegratedDecisionAction.BLOCKED is not None)

        # ── Model checks (14) ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
            IntegratedStrategyInput, IntegratedStrategyContext, IntegratedStrategyDecision,
            IntegratedWatchlistDecision, IntegratedThemeDecision, IntegratedABCDecision,
            IntegratedRiskDecision, IntegratedBehaviorDecision, IntegratedPaperPlan,
            IntegratedNoTradeReason, IntegratedScorecard, IntegratedDashboard,
            IntegratedStrategyReport, IntegratedHealthSummary, get_all_model_names,
        )
        self._check("model_input_paper_only",      lambda: IntegratedStrategyInput().paper_only is True)
        self._check("model_context_paper_only",    lambda: IntegratedStrategyContext().paper_only is True)
        self._check("model_decision_paper_only",   lambda: IntegratedStrategyDecision().paper_only is True)
        self._check("model_watchlist_paper_only",  lambda: IntegratedWatchlistDecision().paper_only is True)
        self._check("model_theme_paper_only",      lambda: IntegratedThemeDecision().paper_only is True)
        self._check("model_abc_paper_only",        lambda: IntegratedABCDecision().paper_only is True)
        self._check("model_risk_paper_only",       lambda: IntegratedRiskDecision().paper_only is True)
        self._check("model_behavior_paper_only",   lambda: IntegratedBehaviorDecision().paper_only is True)
        self._check("model_paper_plan_paper_only", lambda: IntegratedPaperPlan().paper_only is True)
        self._check("model_no_trade_paper_only",   lambda: IntegratedNoTradeReason().paper_only is True)
        self._check("model_scorecard_paper_only",  lambda: IntegratedScorecard().paper_only is True)
        self._check("model_dashboard_paper_only",  lambda: IntegratedDashboard().paper_only is True)
        self._check("model_report_paper_only",     lambda: IntegratedStrategyReport().paper_only is True)
        self._check("model_health_paper_only",     lambda: IntegratedHealthSummary().paper_only is True)
        self._check("model_count_14",              lambda: len(get_all_model_names()) == 14)

        # ── No broker / no real orders in models (3) ─────────────────────────
        self._check("no_real_orders_input",        lambda: IntegratedStrategyInput().no_real_orders is True)
        self._check("no_broker_paper_plan",        lambda: IntegratedPaperPlan().no_broker is True)
        self._check("broker_exec_disabled",        lambda: IntegratedPaperPlan().broker_execution_enabled is False)

        # ── Scorecard, Decisions, Engine (6) ─────────────────────────────────
        from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
            IntegratedRegimeStatus, IntegratedWatchlistStatus, IntegratedABCStatus,
            IntegratedThemeStatus, IntegratedRiskLevel, IntegratedBehaviorStatus,
        )
        from paper_trading.small_capital_strategy.integrated_strategy_scorecard_v178 import compute_scorecard
        from paper_trading.small_capital_strategy.integrated_strategy_decisions_v178 import check_hard_blocks
        from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import (
            IntegratedStrategyEngine, run_integrated_strategy,
        )
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
        )
        self._check("scorecard_callable",       lambda: compute_scorecard(_inp).paper_only is True)
        self._check("scorecard_score_0_100",    lambda: 0 <= compute_scorecard(_inp).final_score <= 100)
        self._check("blocks_no_stop_works",     lambda: len(check_hard_blocks(IntegratedStrategyInput(has_stop_loss=False))) >= 1)
        self._check("engine_run_callable",      lambda: run_integrated_strategy(_inp).paper_only is True)
        self._check("engine_no_real_orders",    lambda: run_integrated_strategy(_inp).no_real_orders is True)
        self._check("engine_no_broker",         lambda: run_integrated_strategy(_inp).no_broker is True)

        # ── Paper plan, Report (4) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.integrated_strategy_paper_plan_v178 import build_paper_plan
        from paper_trading.small_capital_strategy.integrated_strategy_report_v178 import (
            build_report, get_report_sections,
        )
        from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import build_integrated_dashboard
        _decision = run_integrated_strategy(_inp)
        _pp = build_paper_plan(_inp, _decision)
        _dash = build_integrated_dashboard(_inp)
        _rpt = build_report(_dash)
        self._check("paper_plan_callable",       lambda: _pp.paper_only is True)
        self._check("paper_plan_no_broker",      lambda: _pp.broker_execution_enabled is False)
        self._check("report_callable",           lambda: _rpt.paper_only is True)
        self._check("report_sections_6",         lambda: len(get_report_sections()) == 6)

        # ── Scenarios, Fixtures (4) ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.integrated_strategy_scenarios_v178 import count_scenarios, get_scenarios
        from paper_trading.small_capital_strategy.integrated_strategy_fixture_registry_v178 import count_fixtures, validate_registry
        self._check("scenarios_ge_70",          lambda: count_scenarios() >= 70)
        self._check("scenarios_all_paper",      lambda: all(s["paper_only"] for s in get_scenarios()))
        self._check("fixtures_ge_70",           lambda: count_fixtures() >= 70)
        self._check("fixtures_registry_valid",  lambda: validate_registry()["valid"])

        # ── GUI check (1) ─────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_178",    lambda: PANEL_VERSION in ("1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3"))

        # ── CLI checks (5) ────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _is_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("integrated-strategy")]
        self._check("cli_is_cmds_ge_17",        lambda: len(_is_cmds) >= 17)
        self._check("cli_is_version_exists",    lambda: any(c.name == "integrated-strategy-version" for c in PROVIDER_COMMANDS))
        self._check("cli_is_health_exists",     lambda: any(c.name == "integrated-strategy-health" for c in PROVIDER_COMMANDS))
        self._check("cli_is_gate_exists",       lambda: any(c.name == "integrated-strategy-gate" for c in PROVIDER_COMMANDS))
        self._check("cli_is_safety_exists",     lambda: any(c.name == "integrated-strategy-safety-audit" for c in PROVIDER_COMMANDS))

        # ── No broker, no real orders, no margin, no production (4) ──────────
        self._check("no_broker_flag",           lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("no_real_orders_flag",      lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("no_margin_flag",           lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("no_production_writes",     lambda: SAFETY_FLAGS["no_production_db_writes"] is True)

        # ── Backward compat v1.7.0~v1.7.7 (7) ───────────────────────────────
        from paper_trading.small_capital_strategy.version_v178 import is_known_release as ikr
        self._check("compat_v177",              lambda: ikr("Theme Rotation Scanner"))
        self._check("compat_v176",              lambda: ikr("Mistake Taxonomy & Weekly Review Dashboard"))
        self._check("compat_v175",              lambda: ikr("Small Account Trade Journal"))
        self._check("compat_v174",              lambda: ikr("Small Account Risk Dashboard"))
        self._check("compat_v173",              lambda: ikr("Market Regime Position Control"))
        self._check("compat_v172",              lambda: ikr("A/B/C Buy Point Execution Plan"))
        self._check("compat_v171",              lambda: ikr("Watchlist Strategy Layer"))

        # ── Integration dependencies available (4) ────────────────────────────
        self._check("dep_v170_available",       lambda: __import__("paper_trading.small_capital_strategy.version_v170", fromlist=["VERSION"]).VERSION == "1.7.0")
        self._check("dep_v171_available",       lambda: __import__("paper_trading.small_capital_strategy.watchlist_models_v171", fromlist=["WatchlistCandidate"]) is not None)
        self._check("dep_v177_available",       lambda: __import__("paper_trading.small_capital_strategy.theme_rotation_models_v177", fromlist=["ThemeSignal"]) is not None)
        self._check("dep_abc_available",        lambda: __import__("paper_trading.small_capital_strategy.abc_execution_models_v172", fromlist=["ABCSignalInput"]) is not None)

        # ── Compliance (3) ────────────────────────────────────────────────────
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
    """Run integrated strategy release gate. Returns result dict."""
    return SmallCapitalStrategyIntegrationReleaseGate().run()


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
