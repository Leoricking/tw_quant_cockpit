"""
release/drawdown_risk_controls_release_gate_v153.py — Drawdown & Risk Controls Release Gate v1.5.3.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
30 gate checks.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
GATE_VERSION  = "1.5.3"


class DrawdownRiskControlsReleaseGate:
    """30-check release gate for Drawdown & Risk Controls v1.5.3."""

    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        results: List[Dict] = []
        passed_count = 0
        failed_count = 0

        def check(name: str, fn) -> bool:
            nonlocal passed_count, failed_count
            try:
                ok, detail = fn()
            except Exception as e:
                ok, detail = False, str(e)
            results.append({"check": name, "passed": ok, "detail": detail})
            if ok:
                passed_count += 1
            else:
                failed_count += 1
            return ok

        # 1. PACKAGE_FLAGS_VALID
        def _flags():
            from portfolio.risk_controls import (
                DRAWDOWN_RISK_CONTROLS_AVAILABLE, DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY,
                RISK_CONTROL_RESEARCH_ONLY, RISK_CONTROL_AUTO_APPLY_ENABLED,
                RISK_CONTROL_AUTO_REDUCE_ENABLED, RISK_CONTROL_AUTO_STOP_ENABLED,
                RISK_CONTROL_AUTO_REBALANCE_ENABLED, RISK_CONTROL_ORDER_CREATION_ENABLED,
                RISK_CONTROL_ORDER_EXECUTION_ENABLED, RISK_CONTROL_BROKER_ENABLED,
                RISK_CONTROL_HEDGING_EXECUTION_ENABLED, RISK_CONTROL_LEDGER_WRITE_ENABLED,
                RISK_CONTROL_LIVE_ACCOUNT_SYNC_ENABLED,
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            )
            assert DRAWDOWN_RISK_CONTROLS_AVAILABLE is True
            assert DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY is True
            assert RISK_CONTROL_RESEARCH_ONLY is True
            assert RISK_CONTROL_AUTO_APPLY_ENABLED is False
            assert RISK_CONTROL_AUTO_REDUCE_ENABLED is False
            assert RISK_CONTROL_AUTO_STOP_ENABLED is False
            assert RISK_CONTROL_AUTO_REBALANCE_ENABLED is False
            assert RISK_CONTROL_ORDER_CREATION_ENABLED is False
            assert RISK_CONTROL_ORDER_EXECUTION_ENABLED is False
            assert RISK_CONTROL_BROKER_ENABLED is False
            assert RISK_CONTROL_HEDGING_EXECUTION_ENABLED is False
            assert RISK_CONTROL_LEDGER_WRITE_ENABLED is False
            assert RISK_CONTROL_LIVE_ACCOUNT_SYNC_ENABLED is False
            assert NO_REAL_ORDERS is True
            assert BROKER_EXECUTION_ENABLED is False
            assert PRODUCTION_TRADING_BLOCKED is True
            return True, "all package flags valid"
        check("PACKAGE_FLAGS_VALID", _flags)

        # 2. ENUMS_VALID
        def _enums():
            from portfolio.risk_controls.enums_v153 import (
                DrawdownStatus, RiskControlStatus, RiskControlType,
                RiskActionType, DrawdownEpisodeStatus, AttributionType,
                StressScenarioType,
            )
            assert DrawdownStatus.IN_DRAWDOWN == "IN_DRAWDOWN"
            assert RiskControlStatus.BREACH == "BREACH"
            assert RiskControlType.VOLATILITY_LIMIT == "VOLATILITY_LIMIT"
            assert RiskActionType.NO_ACTION == "NO_ACTION"
            assert DrawdownEpisodeStatus.OPEN == "OPEN"
            assert AttributionType.POSITION == "POSITION"
            assert StressScenarioType.COMBINED == "COMBINED"
            return True, "all enums valid"
        check("ENUMS_VALID", _enums)

        # 3. MODELS_RESEARCH_ONLY
        def _models():
            from portfolio.risk_controls.models_v153 import (
                DrawdownAnalysisRequest, RiskControlPolicy, RiskControlCheck,
                RiskControlEvaluation, SizingRiskImpact,
            )
            from portfolio.risk_controls.enums_v153 import RiskControlType
            req = DrawdownAnalysisRequest(
                request_id="RG001", portfolio_id="P1",
                as_of="2026-06-22", available_from="2026-01-01",
            )
            assert req.research_only is True
            pol = RiskControlPolicy(
                policy_id="P1", control_type=RiskControlType.VOLATILITY_LIMIT, name="T"
            )
            assert pol.research_only is True
            assert pol.executable is False
            assert pol.order_created is False
            return True, "models have research_only=True, executable=False"
        check("MODELS_RESEARCH_ONLY", _models)

        # 4. EQUITY_CURVE_BUILDER
        def _equity():
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            curve = PortfolioEquityCurveBuilder().build_demo()
            assert len(curve) > 0
            return True, f"equity curve built: {len(curve)} points"
        check("EQUITY_CURVE_BUILDER", _equity)

        # 5. UNDERWATER_CURVE
        def _uw():
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
            curve = PortfolioEquityCurveBuilder().build_demo()
            uw = UnderwaterCurveCalculator().calculate(curve)
            assert len(uw) > 0
            assert all(-1.0 <= p.drawdown_pct <= 0.001 for p in uw)
            return True, "underwater curve valid"
        check("UNDERWATER_CURVE", _uw)

        # 6. MAX_DRAWDOWN
        def _mdd():
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
            from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
            curve = PortfolioEquityCurveBuilder().build_demo()
            uw = UnderwaterCurveCalculator().calculate(curve)
            summary = MaxDrawdownCalculator().calculate("P1", "2026-06-21", uw)
            assert summary.research_only is True
            assert summary.max_drawdown_pct <= 0
            return True, f"max drawdown: {summary.max_drawdown_pct:.2%}"
        check("MAX_DRAWDOWN", _mdd)

        # 7. EPISODE_DETECTION
        def _episodes():
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
            from portfolio.risk_controls.drawdown_episode_v153 import DrawdownEpisodeDetector
            curve = PortfolioEquityCurveBuilder().build_demo()
            uw = UnderwaterCurveCalculator().calculate(curve)
            episodes = DrawdownEpisodeDetector().detect(uw)
            assert isinstance(episodes, list)
            return True, f"episodes detected: {len(episodes)}"
        check("EPISODE_DETECTION", _episodes)

        # 8. VOLATILITY_LIMIT
        def _vol():
            from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            c = VolatilityLimitChecker().check("C1", "P1", 0.18)
            assert c.status == RiskControlStatus.PASS
            assert c.research_only is True
            assert c.order_created is False
            c2 = VolatilityLimitChecker().check("C2", "P1", 0.35)
            assert c2.status == RiskControlStatus.BREACH
            return True, "volatility limit PASS/BREACH correct"
        check("VOLATILITY_LIMIT", _vol)

        # 9. LOSS_LIMITS
        def _loss():
            from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            lc = LossLimitChecker()
            assert lc.check_daily("C1", "P1", -0.005).status == RiskControlStatus.PASS
            assert lc.check_daily("C2", "P1", -0.05).status == RiskControlStatus.BREACH
            assert lc.check_weekly("C3", "P1", -0.02).status == RiskControlStatus.PASS
            assert lc.check_monthly("C4", "P1", -0.12).status == RiskControlStatus.BREACH
            return True, "loss limits PASS/BREACH correct"
        check("LOSS_LIMITS", _loss)

        # 10. CONCENTRATION_LIMITS
        def _conc():
            from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            cc = ConcentrationLimitChecker()
            c = cc.check_single_name("C1", "P1", {"A": 0.15, "B": 0.10})
            assert c.status == RiskControlStatus.PASS
            c2 = cc.check_single_name("C2", "P1", {"A": 0.40, "B": 0.10})
            assert c2.status == RiskControlStatus.BREACH
            return True, "concentration limits correct"
        check("CONCENTRATION_LIMITS", _conc)

        # 11. CORRELATION_LIMITS
        def _corr():
            from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            cc = CorrelationLimitChecker()
            c = cc.check_max_pairwise("C1", "P1", 1, 10)
            assert c.status == RiskControlStatus.PASS
            c2 = cc.check_max_pairwise("C2", "P1", 8, 10)
            assert c2.status == RiskControlStatus.BREACH
            return True, "correlation limits correct"
        check("CORRELATION_LIMITS", _corr)

        # 12. LIQUIDITY_LIMITS
        def _liq():
            from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            lc = LiquidityLimitChecker()
            assert lc.check_illiquid_fraction("C1", "P1", 0.10).status == RiskControlStatus.PASS
            assert lc.check_illiquid_fraction("C2", "P1", 0.50).status == RiskControlStatus.BREACH
            return True, "liquidity limits correct"
        check("LIQUIDITY_LIMITS", _liq)

        # 13. CASH_RESERVE
        def _cash():
            from portfolio.risk_controls.cash_reserve_limit_v153 import CashReserveLimitChecker
            from portfolio.risk_controls.enums_v153 import RiskControlStatus
            cc = CashReserveLimitChecker()
            assert cc.check("C1", "P1", 0.10).status == RiskControlStatus.PASS
            assert cc.check("C2", "P1", 0.01).status == RiskControlStatus.BREACH
            return True, "cash reserve correct"
        check("CASH_RESERVE", _cash)

        # 14. CONSTRAINT_ENGINE
        def _engine():
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            e = RiskControlConstraintEngine().build_demo_evaluation()
            assert e.research_only is True
            assert e.executable is False
            assert e.order_created is False
            assert e.ledger_persisted is False
            assert e.auto_applied is False
            return True, f"constraint engine: {e.overall_status.value}"
        check("CONSTRAINT_ENGINE", _engine)

        # 15. RISK_BUDGET
        def _budget():
            from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
            r = PortfolioRiskBudgetEngine().evaluate("P1", "2026-06-21", -0.05, 0.18)
            assert r["research_only"] is True
            assert r["executable"] is False
            return True, "risk budget engine valid"
        check("RISK_BUDGET", _budget)

        # 16. ATTRIBUTION
        def _attr():
            from portfolio.risk_controls.drawdown_attribution_v153 import DrawdownAttributionCalculator
            results = DrawdownAttributionCalculator().attribute_by_position(
                {"A": 0.5, "B": 0.5}, {"A": -5000.0, "B": -3000.0}, 1_000_000.0
            )
            assert len(results) == 2
            assert all(r.research_only is True for r in results)
            return True, "attribution by position valid"
        check("ATTRIBUTION", _attr)

        # 17. STRESS_SCENARIOS
        def _stress():
            from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
            results = DrawdownStressAnalyzer().run_all("P1", 1_000_000.0)
            assert len(results) == 8
            assert all(r.research_only is True for r in results)
            assert all(r.executable is False for r in results)
            assert all(r.projected_drawdown_pct < 0 for r in results)
            return True, "all 8 stress scenarios ran"
        check("STRESS_SCENARIOS", _stress)

        # 18. ELIGIBILITY_GATE
        def _elig():
            from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
            from portfolio.risk_controls.models_v153 import DrawdownAnalysisRequest
            req = DrawdownAnalysisRequest(
                request_id="E1", portfolio_id="P1",
                as_of="2026-06-22", available_from="2026-01-01",
            )
            r = DrawdownRiskControlsEligibilityGate().evaluate(req, {"broker_linked": False}, 120)
            assert r["eligibility_status"] == "ELIGIBLE"
            r2 = DrawdownRiskControlsEligibilityGate().evaluate(req, {"broker_linked": True}, 120)
            assert r2["eligibility_status"] == "INELIGIBLE"
            return True, "eligibility gate valid"
        check("ELIGIBILITY_GATE", _elig)

        # 19. PIT_VALIDATOR
        def _pit():
            from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
            from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
            curve = PortfolioEquityCurveBuilder().build_demo()
            v = DrawdownRiskControlsPITValidator()
            r = v.validate_equity_curve(curve, "2026-06-21")
            assert r["valid"] is True
            return True, "PIT validator valid"
        check("PIT_VALIDATOR", _pit)

        # 20. LINEAGE
        def _lineage():
            from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            ev = RiskControlConstraintEngine().build_demo_evaluation()
            lin = DrawdownRiskControlsLineageTracker().build_lineage(ev)
            assert lin["lineage_valid"] is True
            assert lin["evaluation_id"] == ev.evaluation_id
            return True, "lineage valid"
        check("LINEAGE", _lineage)

        # 21. EXPLAINABILITY
        def _explain():
            from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            ev = RiskControlConstraintEngine().build_demo_evaluation()
            exp = DrawdownRiskControlsExplainer().explain(ev)
            assert exp["research_only"] is True
            assert "safety_text" in exp
            assert len(exp.get("limitations", [])) > 0
            return True, "explainability valid"
        check("EXPLAINABILITY", _explain)

        # 22. STORE
        def _store():
            from portfolio.risk_controls.store_v153 import DrawdownRiskControlsStore
            from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
            ev = RiskControlConstraintEngine().build_demo_evaluation()
            store = DrawdownRiskControlsStore(":memory:")
            eid = store.save_evaluation(ev)
            got = store.get_evaluation(eid)
            assert got is not None
            assert not hasattr(store, "_orders")
            return True, "store save/get valid"
        check("STORE", _store)

        # 23. QUERY_SERVICE_NO_BLOCKED_METHODS
        def _query():
            from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
            svc = DrawdownRiskControlsQueryService()
            for blocked in ["optimize_weights", "rebalance_portfolio", "submit_order",
                            "execute_order", "sync_broker", "apply_risk_control", "execute_stop"]:
                assert not hasattr(svc, blocked), f"Query has blocked method: {blocked}"
            return True, "no blocked methods on query service"
        check("QUERY_NO_BLOCKED_METHODS", _query)

        # 24. SIZING_IMPACT
        def _sizing():
            from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
            si = SizingRiskImpactAnalyzer().build_demo()
            assert si.research_only is True
            assert si.executable is False
            assert si.order_created is False
            assert si.ledger_persisted is False
            return True, "sizing impact research-only"
        check("SIZING_IMPACT", _sizing)

        # 25. HEALTH_CHECK
        def _health():
            from portfolio.risk_controls.health_v153 import DrawdownRiskControlsHealthCheck
            result = DrawdownRiskControlsHealthCheck().run()
            assert result["overall"] == "PASS", f"Health failed: {result['failed']} failures"
            return True, f"health: {result['passed']}/{result['total']}"
        check("HEALTH_CHECK", _health)

        # 26. VERSION_INFO_UPDATED
        def _version():
            from release.version_info import (
                VERSION, DRAWDOWN_RISK_CONTROLS_BASELINE,
                DRAWDOWN_RISK_CONTROLS_AVAILABLE, DRAWDOWN_RISK_CONTROLS_STAGE,
            )
            from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
            assert DRAWDOWN_RISK_CONTROLS_BASELINE == "1.5.3", f"Expected baseline 1.5.3, got {DRAWDOWN_RISK_CONTROLS_BASELINE}"
            assert DRAWDOWN_RISK_CONTROLS_AVAILABLE is True, "DRAWDOWN_RISK_CONTROLS_AVAILABLE must be True"
            assert DRAWDOWN_RISK_CONTROLS_STAGE == "STABLE", f"Expected STABLE, got {DRAWDOWN_RISK_CONTROLS_STAGE}"
            compat = CompatibilityRegistryV159().is_compatible(VERSION)
            assert compat["compatible"], f"VERSION {VERSION} not in compatible range: {compat['reason']}"
            return True, f"baseline=1.5.3 stage=STABLE VERSION={VERSION} compat={compat['reason']}"
        check("VERSION_INFO_UPDATED", _version)

        # 27. CAPABILITY_REGISTRY_UPDATED
        def _cap():
            from release.capability_registry import is_capability_available
            assert is_capability_available("drawdown_risk_controls") is True
            return True, "capability registry updated"
        check("CAPABILITY_REGISTRY_UPDATED", _cap)

        # 28. GUI_PANEL_EXISTS
        def _gui():
            import os
            path = os.path.join(
                os.path.dirname(__file__), "..", "gui",
                "drawdown_risk_controls_panel.py"
            )
            assert os.path.exists(os.path.abspath(path))
            return True, "GUI panel exists"
        check("GUI_PANEL_EXISTS", _gui)

        # 29. REPORT_EXISTS
        def _report():
            import os
            path = os.path.join(
                os.path.dirname(__file__), "..", "reports",
                "drawdown_risk_controls_report.py"
            )
            assert os.path.exists(os.path.abspath(path))
            return True, "report module exists"
        check("REPORT_EXISTS", _report)

        # 30. RESULT_LABELS_VALID
        def _labels():
            from portfolio.risk_controls import RESULT_LABELS
            for lbl in ["RESEARCH_ONLY", "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NOT_AN_ORDER"]:
                assert lbl in RESULT_LABELS, f"Missing label: {lbl}"
            return True, "all result labels present"
        check("RESULT_LABELS_VALID", _labels)

        overall = "PASS" if failed_count == 0 else "FAIL"
        return {
            "gate_version":  GATE_VERSION,
            "overall":       overall,
            "passed":        passed_count,
            "failed":        failed_count,
            "total":         len(results),
            "checks":        results,
            "research_only": True,
        }
