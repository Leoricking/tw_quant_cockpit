"""
portfolio/risk_controls/health_v153.py — Drawdown Risk Controls Health Check v1.5.3.
50+ checks covering all modules. All pass offline.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from typing import Any, Dict

RESEARCH_ONLY = True
EXPECTED_VERSION = "1.5.3"


class DrawdownRiskControlsHealthCheck:
    """50+ health checks for the Drawdown & Risk Controls module."""

    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        checks: Dict[str, Dict[str, Any]] = {}

        def add(name: str, passed: bool, detail: str = "") -> None:
            checks[name] = {"status": "PASS" if passed else "FAIL", "detail": detail}

        # --- Module imports ---
        for mod in [
            "enums_v153", "models_v153", "validation_v153",
            "equity_curve_v153", "underwater_v153", "drawdown_v153",
            "drawdown_episode_v153", "drawdown_duration_v153",
            "drawdown_recovery_v153", "drawdown_attribution_v153",
            "risk_budget_v153", "volatility_limit_v153", "loss_limit_v153",
            "concentration_limit_v153", "correlation_limit_v153",
            "liquidity_limit_v153", "cash_reserve_limit_v153",
            "constraint_engine_v153", "sizing_impact_v153", "stress_v153",
            "eligibility_v153", "point_in_time_v153", "lineage_v153",
            "explain_v153", "store_v153", "query_v153",
        ]:
            try:
                __import__(f"portfolio.risk_controls.{mod}")
                add(f"import_{mod}", True)
            except Exception as e:
                add(f"import_{mod}", False, str(e))

        # --- Package flags ---
        try:
            from portfolio.risk_controls import (
                DRAWDOWN_RISK_CONTROLS_AVAILABLE,
                DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY,
                RISK_CONTROL_RESEARCH_ONLY,
                RISK_CONTROL_AUTO_APPLY_ENABLED,
                RISK_CONTROL_AUTO_REDUCE_ENABLED,
                RISK_CONTROL_AUTO_STOP_ENABLED,
                RISK_CONTROL_AUTO_REBALANCE_ENABLED,
                RISK_CONTROL_ORDER_CREATION_ENABLED,
                RISK_CONTROL_ORDER_EXECUTION_ENABLED,
                RISK_CONTROL_BROKER_ENABLED,
                RISK_CONTROL_HEDGING_EXECUTION_ENABLED,
                RISK_CONTROL_LEDGER_WRITE_ENABLED,
                RISK_CONTROL_LIVE_ACCOUNT_SYNC_ENABLED,
                NO_REAL_ORDERS,
                BROKER_EXECUTION_ENABLED,
                PRODUCTION_TRADING_BLOCKED,
            )
            add("flag_available",              DRAWDOWN_RISK_CONTROLS_AVAILABLE is True)
            add("flag_research_only",          DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY is True)
            add("flag_risk_control_ro",        RISK_CONTROL_RESEARCH_ONLY is True)
            add("flag_no_auto_apply",          RISK_CONTROL_AUTO_APPLY_ENABLED is False)
            add("flag_no_auto_reduce",         RISK_CONTROL_AUTO_REDUCE_ENABLED is False)
            add("flag_no_auto_stop",           RISK_CONTROL_AUTO_STOP_ENABLED is False)
            add("flag_no_auto_rebalance",      RISK_CONTROL_AUTO_REBALANCE_ENABLED is False)
            add("flag_no_order_creation",      RISK_CONTROL_ORDER_CREATION_ENABLED is False)
            add("flag_no_order_execution",     RISK_CONTROL_ORDER_EXECUTION_ENABLED is False)
            add("flag_no_broker",              RISK_CONTROL_BROKER_ENABLED is False)
            add("flag_no_hedging",             RISK_CONTROL_HEDGING_EXECUTION_ENABLED is False)
            add("flag_no_ledger_write",        RISK_CONTROL_LEDGER_WRITE_ENABLED is False)
            add("flag_no_live_sync",           RISK_CONTROL_LIVE_ACCOUNT_SYNC_ENABLED is False)
            add("flag_no_real_orders",         NO_REAL_ORDERS is True)
            add("flag_broker_exec_false",      BROKER_EXECUTION_ENABLED is False)
            add("flag_production_blocked",     PRODUCTION_TRADING_BLOCKED is True)
        except Exception as e:
            add("safety_flags", False, str(e))

        # --- Enums ---
        try:
            from portfolio.risk_controls.enums_v153 import (
                DrawdownStatus, RiskControlStatus, RiskControlType,
                RiskActionType, DrawdownEpisodeStatus, AttributionType,
                StressScenarioType,
            )
            add("enum_drawdown_status",    DrawdownStatus.IN_DRAWDOWN == "IN_DRAWDOWN")
            add("enum_risk_control_status", RiskControlStatus.BREACH == "BREACH")
            add("enum_risk_control_type",  RiskControlType.VOLATILITY_LIMIT == "VOLATILITY_LIMIT")
            add("enum_risk_action_type",   RiskActionType.NO_ACTION == "NO_ACTION")
            add("enum_episode_status",     DrawdownEpisodeStatus.OPEN == "OPEN")
            add("enum_attribution_type",   AttributionType.POSITION == "POSITION")
            add("enum_stress_type",        StressScenarioType.COMBINED == "COMBINED")
        except Exception as e:
            add("enum_checks", False, str(e))

        # --- Models ---
        try:
            from portfolio.risk_controls.models_v153 import DrawdownAnalysisRequest
            req = DrawdownAnalysisRequest(
                request_id="HC001", portfolio_id="P1",
                as_of="2026-06-22", available_from="2026-01-01",
            )
            add("model_request_research_only", req.research_only is True)
        except Exception as e:
            add("model_checks", False, str(e))

        # --- Model safety assertions ---
        try:
            from portfolio.risk_controls.models_v153 import (
                RiskControlPolicy, RiskControlCheck, RiskControlEvaluation,
                SizingRiskImpact, DrawdownStressResult,
            )
            from portfolio.risk_controls.enums_v153 import (
                RiskControlType, RiskControlStatus, RiskActionType,
                StressScenarioType,
            )
            policy = RiskControlPolicy(
                policy_id="P1", control_type=RiskControlType.VOLATILITY_LIMIT,
                name="Test",
            )
            add("policy_research_only",    policy.research_only is True)
            add("policy_not_executable",   policy.executable is False)
            add("policy_no_order",         policy.order_created is False)

            check = RiskControlCheck(
                check_id="C1", policy_id="P1",
                control_type=RiskControlType.DAILY_LOSS_LIMIT,
            )
            add("check_research_only",     check.research_only is True)
            add("check_not_executable",    check.executable is False)
            add("check_no_order",          check.order_created is False)
            add("check_no_ledger",         check.ledger_persisted is False)
            add("check_no_auto_apply",     check.auto_applied is False)
        except Exception as e:
            add("model_safety_checks", False, str(e))

        # --- Equity curve ---
        try:
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            curve = PortfolioEquityCurveBuilder().build_demo()
            add("equity_curve_demo",      len(curve) > 0)
            add("equity_curve_no_future", all(p.date <= "2026-06-22" for p in curve))
        except Exception as e:
            add("equity_curve_checks", False, str(e))

        # --- Underwater curve ---
        try:
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
            curve = PortfolioEquityCurveBuilder().build_demo()
            uw = UnderwaterCurveCalculator().calculate(curve)
            add("underwater_curve",       len(uw) > 0)
            add("underwater_range",       all(-1.0 <= p.drawdown_pct <= 0.001 for p in uw))
        except Exception as e:
            add("underwater_checks", False, str(e))

        # --- Max drawdown ---
        try:
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
            from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
            curve = PortfolioEquityCurveBuilder().build_demo()
            uw = UnderwaterCurveCalculator().calculate(curve)
            summary = MaxDrawdownCalculator().calculate("P1", "2026-06-21", uw)
            add("max_drawdown_valid",     summary.max_drawdown_pct <= 0)
            add("max_drawdown_research",  summary.research_only is True)
        except Exception as e:
            add("max_drawdown_checks", False, str(e))

        # --- Episode detection ---
        try:
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
            from portfolio.risk_controls.drawdown_episode_v153 import DrawdownEpisodeDetector
            curve = PortfolioEquityCurveBuilder().build_demo()
            uw = UnderwaterCurveCalculator().calculate(curve)
            episodes = DrawdownEpisodeDetector().detect(uw)
            add("episodes_list",         isinstance(episodes, list))
        except Exception as e:
            add("episode_checks", False, str(e))

        # --- Volatility limit ---
        try:
            from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            c = VolatilityLimitChecker().check("CHK001", "POL001", 0.18)
            add("vol_limit_pass",   c.status == RiskControlStatus.PASS)
            c2 = VolatilityLimitChecker().check("CHK002", "POL001", 0.35)
            add("vol_limit_breach", c2.status == RiskControlStatus.BREACH)
            add("vol_limit_ro",     c.research_only is True)
            add("vol_limit_no_ord", c.order_created is False)
        except Exception as e:
            add("vol_limit_checks", False, str(e))

        # --- Loss limits ---
        try:
            from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            c = LossLimitChecker().check_daily("CHK003", "POL002", -0.005)
            add("daily_loss_pass",   c.status == RiskControlStatus.PASS)
            c2 = LossLimitChecker().check_daily("CHK004", "POL002", -0.05)
            add("daily_loss_breach", c2.status == RiskControlStatus.BREACH)
        except Exception as e:
            add("loss_limit_checks", False, str(e))

        # --- Constraint engine ---
        try:
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            eval_result = RiskControlConstraintEngine().build_demo_evaluation()
            add("constraint_engine_eval",    eval_result.research_only is True)
            add("constraint_engine_no_ord",  eval_result.order_created is False)
            add("constraint_engine_no_exec", eval_result.executable is False)
        except Exception as e:
            add("constraint_engine_checks", False, str(e))

        # --- Stress scenarios ---
        try:
            from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
            from portfolio.risk_controls.enums_v153 import StressScenarioType
            result = DrawdownStressAnalyzer().run(
                "P1", 1_000_000.0, StressScenarioType.BEAR_MARKET
            )
            add("stress_research_only",    result.research_only is True)
            add("stress_no_order",         result.order_created is False)
            add("stress_negative_dd",      result.projected_drawdown_pct < 0)
            results = DrawdownStressAnalyzer().run_all("P1", 1_000_000.0)
            add("stress_all_8_types",      len(results) == 8)
        except Exception as e:
            add("stress_checks", False, str(e))

        # --- Eligibility ---
        try:
            from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
            from portfolio.risk_controls.models_v153 import DrawdownAnalysisRequest
            req = DrawdownAnalysisRequest(
                request_id="E1", portfolio_id="P1",
                as_of="2026-06-22", available_from="2026-01-01",
            )
            result = DrawdownRiskControlsEligibilityGate().evaluate(
                req, {"broker_linked": False}, 120
            )
            add("eligibility_eligible",   result.get("eligibility_status") == "ELIGIBLE")
            add("eligibility_no_broker",  "BROKER_LINKED_TRUE" not in result.get("blockers", []))
            req2 = DrawdownAnalysisRequest(
                request_id="E2", portfolio_id="P1",
                as_of="2026-06-22", available_from="2026-01-01",
            )
            result2 = DrawdownRiskControlsEligibilityGate().evaluate(
                req2, {"broker_linked": True}, 120
            )
            add("eligibility_blocks_broker", result2.get("eligibility_status") == "INELIGIBLE")
        except Exception as e:
            add("eligibility_checks", False, str(e))

        # --- PIT validator ---
        try:
            from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            curve = PortfolioEquityCurveBuilder().build_demo()
            v = DrawdownRiskControlsPITValidator()
            r = v.validate_equity_curve(curve, "2026-06-21")
            add("pit_valid_curve",  r["valid"] is True)
            # inject a future date point
            from portfolio.risk_controls.models_v153 import EquityCurvePoint
            bad_curve = list(curve) + [EquityCurvePoint(date="2027-01-01", portfolio_value=999)]
            r2 = v.validate_equity_curve(bad_curve, "2026-06-21")
            add("pit_blocks_future", r2["valid"] is False)
        except Exception as e:
            add("pit_checks", False, str(e))

        # --- Lineage ---
        try:
            from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            evaluation = RiskControlConstraintEngine().build_demo_evaluation()
            lin = DrawdownRiskControlsLineageTracker().build_lineage(evaluation)
            add("lineage_valid",      lin.get("lineage_valid") is True)
            add("lineage_has_eval",   lin.get("evaluation_id") == evaluation.evaluation_id)
        except Exception as e:
            add("lineage_checks", False, str(e))

        # --- Explainability ---
        try:
            from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            evaluation = RiskControlConstraintEngine().build_demo_evaluation()
            exp = DrawdownRiskControlsExplainer().explain(evaluation)
            add("explain_research_only",  exp.get("research_only") is True)
            add("explain_safety_text",    "safety_text" in exp)
            add("explain_limitations",    len(exp.get("limitations", [])) > 0)
            add("explain_no_order",       exp.get("order_created") is False)
        except Exception as e:
            add("explain_checks", False, str(e))

        # --- Store ---
        try:
            from portfolio.risk_controls.store_v153 import DrawdownRiskControlsStore
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            evaluation = RiskControlConstraintEngine().build_demo_evaluation()
            store = DrawdownRiskControlsStore(":memory:")
            eid = store.save_evaluation(evaluation)
            got = store.get_evaluation(eid)
            lst = store.list_evaluations("demo_portfolio")
            add("store_save_get",        got is not None)
            add("store_list",            len(lst) >= 1)
            add("store_no_order_table",  not hasattr(store, "_orders"))
            add("store_research_only",   DrawdownRiskControlsStore.RESEARCH_ONLY is True)
            # Idempotent
            eid2 = store.save_evaluation(evaluation)
            add("store_idempotent",      eid2 == eid)
        except Exception as e:
            add("store_checks", False, str(e))

        # --- Query service ---
        try:
            from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
            svc = DrawdownRiskControlsQueryService()
            add("query_service_created", True)
            for blocked in ["optimize_weights", "rebalance_portfolio", "submit_order",
                            "execute_order", "sync_broker", "apply_risk_control", "execute_stop"]:
                add(f"query_no_{blocked}", not hasattr(svc, blocked))
        except Exception as e:
            add("query_service_checks", False, str(e))

        # --- Labels ---
        try:
            from portfolio.risk_controls import RESULT_LABELS
            for lbl in ["RESEARCH_ONLY", "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NOT_AN_ORDER"]:
                add(f"label_{lbl}", lbl in RESULT_LABELS)
        except Exception as e:
            add("label_checks", False, str(e))

        # --- CLI check ---
        import os
        cli_path = os.path.join(os.path.dirname(__file__), "..", "..", "cli", "command_registry.py")
        add("cli", os.path.exists(os.path.abspath(cli_path)))

        # --- GUI import check ---
        import importlib.util as _ilu
        _gui_path = os.path.join(os.path.dirname(__file__), "..", "..", "gui", "drawdown_risk_controls_panel.py")
        if os.path.exists(os.path.abspath(_gui_path)):
            try:
                spec = _ilu.spec_from_file_location("drawdown_risk_controls_panel", os.path.abspath(_gui_path))
                mod = _ilu.module_from_spec(spec)
                spec.loader.exec_module(mod)
                add("gui_import", getattr(mod, "RESEARCH_ONLY", False) is True)
            except Exception as e:
                add("gui_import", False, str(e))
        else:
            add("gui_import", False, "gui/drawdown_risk_controls_panel.py not found")

        # Tally
        total  = len(checks)
        passed = sum(1 for c in checks.values() if c["status"] == "PASS")
        failed = total - passed
        overall = "PASS" if failed == 0 else "FAIL"

        return {
            "version":      EXPECTED_VERSION,
            "overall":      overall,
            "passed":       passed,
            "total":        total,
            "failed":       failed,
            "checks":       checks,
            "research_only": True,
        }
