"""
empirical_backtest/health_v140.py — Strategy Empirical Backtest Health Check for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations


class StrategyEmpiricalBacktestHealthCheck:
    """31 health checks for the empirical backtest package."""

    def run(self) -> dict:
        checks = {}

        # 1. version_info_1_4_0
        try:
            from release.version_info import VERSION
            ok = VERSION.startswith("1.4.")
            checks["version_info_1_4_0"] = ("PASS" if ok else "FAIL", f"VERSION={VERSION}")
        except Exception as exc:
            checks["version_info_1_4_0"] = ("FAIL", str(exc))

        # 2. package_import
        try:
            import empirical_backtest
            ok = empirical_backtest.NO_REAL_ORDERS is True
            checks["package_import"] = ("PASS" if ok else "FAIL", "empirical_backtest imported")
        except Exception as exc:
            checks["package_import"] = ("FAIL", str(exc))

        # 3. rule_registry
        try:
            from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
            reg = StrategyKnowledgeRuleRegistry()
            checks["rule_registry"] = ("PASS", "StrategyKnowledgeRuleRegistry instantiated")
        except Exception as exc:
            checks["rule_registry"] = ("FAIL", str(exc))

        # 4. rule_registry_has_builtin_rules
        try:
            from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
            reg = StrategyKnowledgeRuleRegistry()
            count = len(reg.list())
            ok = count >= 11
            checks["rule_registry_has_builtin_rules"] = ("PASS" if ok else "FAIL", f"{count} rules registered")
        except Exception as exc:
            checks["rule_registry_has_builtin_rules"] = ("FAIL", str(exc))

        # 5. rule_registry_backtestable_count
        try:
            from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
            reg = StrategyKnowledgeRuleRegistry()
            count = len(reg.list_backtestable())
            ok = count >= 7
            checks["rule_registry_backtestable_count"] = ("PASS" if ok else "FAIL", f"{count} backtestable rules")
        except Exception as exc:
            checks["rule_registry_backtestable_count"] = ("FAIL", str(exc))

        # 6. rule_registry_manual_only_count
        try:
            from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
            reg = StrategyKnowledgeRuleRegistry()
            count = len(reg.list_manual_only())
            ok = count >= 3
            checks["rule_registry_manual_only_count"] = ("PASS" if ok else "FAIL", f"{count} manual-only rules")
        except Exception as exc:
            checks["rule_registry_manual_only_count"] = ("FAIL", str(exc))

        # 7. data_gate_available
        try:
            from empirical_backtest.data_gate_v140 import StrategyBacktestDataGate
            gate = StrategyBacktestDataGate()
            checks["data_gate_available"] = ("PASS", "StrategyBacktestDataGate available")
        except Exception as exc:
            checks["data_gate_available"] = ("FAIL", str(exc))

        # 8. lookahead_guard_available
        try:
            from empirical_backtest.lookahead_guard_v140 import LookaheadBiasGuard
            guard = LookaheadBiasGuard()
            checks["lookahead_guard_available"] = ("PASS", "LookaheadBiasGuard available")
        except Exception as exc:
            checks["lookahead_guard_available"] = ("FAIL", str(exc))

        # 9. corporate_action_guard_available
        try:
            from empirical_backtest.corporate_action_guard_v140 import CorporateActionGuard
            guard = CorporateActionGuard()
            checks["corporate_action_guard_available"] = ("PASS", "CorporateActionGuard available")
        except Exception as exc:
            checks["corporate_action_guard_available"] = ("FAIL", str(exc))

        # 10. signal_engine_available
        try:
            from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
            from empirical_backtest.signal_engine_v140 import StrategyKnowledgeSignalEngine
            reg = StrategyKnowledgeRuleRegistry()
            engine = StrategyKnowledgeSignalEngine(reg)
            checks["signal_engine_available"] = ("PASS", "StrategyKnowledgeSignalEngine available")
        except Exception as exc:
            checks["signal_engine_available"] = ("FAIL", str(exc))

        # 11. execution_model_available
        try:
            from empirical_backtest.models_v140 import ExecutionModelType
            ok = hasattr(ExecutionModelType, "NEXT_OPEN")
            checks["execution_model_available"] = ("PASS" if ok else "FAIL", "ExecutionModelType available")
        except Exception as exc:
            checks["execution_model_available"] = ("FAIL", str(exc))

        # 12. cost_model_available
        try:
            from empirical_backtest.cost_model_v140 import TaiwanTransactionCostModel
            model = TaiwanTransactionCostModel()
            checks["cost_model_available"] = ("PASS", "TaiwanTransactionCostModel available")
        except Exception as exc:
            checks["cost_model_available"] = ("FAIL", str(exc))

        # 13. slippage_model_available
        try:
            from empirical_backtest.cost_model_v140 import SlippageModel
            model = SlippageModel()
            checks["slippage_model_available"] = ("PASS", "SlippageModel available")
        except Exception as exc:
            checks["slippage_model_available"] = ("FAIL", str(exc))

        # 14. metrics_available
        try:
            from empirical_backtest.backtest_engine_v140 import StrategyKnowledgeBacktestEngine
            from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
            reg = StrategyKnowledgeRuleRegistry()
            engine = StrategyKnowledgeBacktestEngine(reg)
            metrics = engine.calculate_metrics([], None)
            ok = "total_return" in metrics
            checks["metrics_available"] = ("PASS" if ok else "FAIL", "metrics calculation available")
        except Exception as exc:
            checks["metrics_available"] = ("FAIL", str(exc))

        # 15. confidence_evaluator_available
        try:
            from empirical_backtest.confidence_v140 import BacktestConfidenceEvaluator
            ev = BacktestConfidenceEvaluator()
            checks["confidence_evaluator_available"] = ("PASS", "BacktestConfidenceEvaluator available")
        except Exception as exc:
            checks["confidence_evaluator_available"] = ("FAIL", str(exc))

        # 16. period_split_available
        try:
            from empirical_backtest.period_split_v140 import BacktestPeriodSplitter
            sp = BacktestPeriodSplitter()
            checks["period_split_available"] = ("PASS", "BacktestPeriodSplitter available")
        except Exception as exc:
            checks["period_split_available"] = ("FAIL", str(exc))

        # 17. walk_forward_available
        try:
            from empirical_backtest.period_split_v140 import WalkForwardValidator
            wf = WalkForwardValidator()
            checks["walk_forward_available"] = ("PASS", "WalkForwardValidator available")
        except Exception as exc:
            checks["walk_forward_available"] = ("FAIL", str(exc))

        # 18. parameter_guard_available
        try:
            from empirical_backtest.parameter_guard_v140 import ParameterSearchGuard
            guard = ParameterSearchGuard()
            checks["parameter_guard_available"] = ("PASS", "ParameterSearchGuard available")
        except Exception as exc:
            checks["parameter_guard_available"] = ("FAIL", str(exc))

        # 19. benchmark_available
        try:
            from empirical_backtest.benchmark_v140 import BenchmarkCalculator
            bc = BenchmarkCalculator()
            checks["benchmark_available"] = ("PASS", "BenchmarkCalculator available")
        except Exception as exc:
            checks["benchmark_available"] = ("FAIL", str(exc))

        # 20. regime_classifier_available
        try:
            from empirical_backtest.regime_classifier_v140 import MarketRegimeClassifier
            rc = MarketRegimeClassifier()
            checks["regime_classifier_available"] = ("PASS", "MarketRegimeClassifier available")
        except Exception as exc:
            checks["regime_classifier_available"] = ("FAIL", str(exc))

        # 21. store_available
        try:
            from empirical_backtest.store_v140 import EmpiricalBacktestStore
            store = EmpiricalBacktestStore()
            checks["store_available"] = ("PASS", "EmpiricalBacktestStore available")
        except Exception as exc:
            checks["store_available"] = ("FAIL", str(exc))

        # 22. query_service_available
        try:
            from empirical_backtest.store_v140 import EmpiricalBacktestStore, EmpiricalBacktestQueryService
            store = EmpiricalBacktestStore()
            qs = EmpiricalBacktestQueryService(store)
            checks["query_service_available"] = ("PASS", "EmpiricalBacktestQueryService available")
        except Exception as exc:
            checks["query_service_available"] = ("FAIL", str(exc))

        # 23. comparison_available
        try:
            from empirical_backtest.comparison_v140 import StrategyKnowledgeComparison
            comp = StrategyKnowledgeComparison()
            checks["comparison_available"] = ("PASS", "StrategyKnowledgeComparison available")
        except Exception as exc:
            checks["comparison_available"] = ("FAIL", str(exc))

        # 24. report_available
        try:
            from empirical_backtest.report_v140 import EmpiricalBacktestReport
            rpt = EmpiricalBacktestReport()
            checks["report_available"] = ("PASS", "EmpiricalBacktestReport available")
        except Exception as exc:
            checks["report_available"] = ("FAIL", str(exc))

        # 25. coverage_repair_integration
        try:
            import coverage_repair
            checks["coverage_repair_integration"] = ("PASS", "coverage_repair package accessible")
        except Exception as exc:
            checks["coverage_repair_integration"] = ("FAIL", str(exc))

        # 26. freshness_integration
        try:
            import data_freshness
            checks["freshness_integration"] = ("PASS", "data_freshness package accessible")
        except Exception as exc:
            checks["freshness_integration"] = ("FAIL", str(exc))

        # 27. replay_integration_read_only
        try:
            import replay
            checks["replay_integration_read_only"] = ("PASS", "replay package accessible (read-only)")
        except Exception as exc:
            checks["replay_integration_read_only"] = ("FAIL", str(exc))

        # 28. no_mock_formal_conclusion
        try:
            from empirical_backtest import BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED
            ok = BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED is False
            checks["no_mock_formal_conclusion"] = (
                "PASS" if ok else "FAIL",
                f"BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED={BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED}"
            )
        except Exception as exc:
            checks["no_mock_formal_conclusion"] = ("FAIL", str(exc))

        # 29. no_auto_optimization
        try:
            from empirical_backtest import BACKTEST_AUTO_OPTIMIZATION_ENABLED
            ok = BACKTEST_AUTO_OPTIMIZATION_ENABLED is False
            checks["no_auto_optimization"] = (
                "PASS" if ok else "FAIL",
                f"BACKTEST_AUTO_OPTIMIZATION_ENABLED={BACKTEST_AUTO_OPTIMIZATION_ENABLED}"
            )
        except Exception as exc:
            checks["no_auto_optimization"] = ("FAIL", str(exc))

        # 30. no_auto_trading
        try:
            from empirical_backtest import BACKTEST_AUTO_TRADING_ENABLED
            ok = BACKTEST_AUTO_TRADING_ENABLED is False
            checks["no_auto_trading"] = (
                "PASS" if ok else "FAIL",
                f"BACKTEST_AUTO_TRADING_ENABLED={BACKTEST_AUTO_TRADING_ENABLED}"
            )
        except Exception as exc:
            checks["no_auto_trading"] = ("FAIL", str(exc))

        # 31. production_trading_blocked
        try:
            from empirical_backtest import PRODUCTION_TRADING_BLOCKED
            ok = PRODUCTION_TRADING_BLOCKED is True
            checks["production_trading_blocked"] = (
                "PASS" if ok else "FAIL",
                f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED}"
            )
        except Exception as exc:
            checks["production_trading_blocked"] = ("FAIL", str(exc))

        return checks

    def get_health_summary(self) -> dict:
        checks = self.run()
        total = len(checks)
        passed = sum(1 for v in checks.values() if v[0] == "PASS")
        failed = total - passed
        all_pass = failed == 0

        formatted_checks = {
            name: {"status": status, "detail": detail}
            for name, (status, detail) in checks.items()
        }

        safety_flags = {
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "mock_formal_conclusion_allowed": False,
            "auto_optimization_enabled": False,
            "auto_trading_enabled": False,
        }

        return {
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "all_pass": all_pass,
            "schema_version": "1.4.0",
            "checks": formatted_checks,
            "safety_flags": safety_flags,
        }
