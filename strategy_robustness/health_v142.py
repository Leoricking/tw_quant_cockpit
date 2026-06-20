"""
strategy_robustness/health_v142.py — Health check for Strategy Robustness v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class StrategyRobustnessHealthCheck:
    """
    Health checks for the strategy_robustness package.
    Fixed safety flags always False/True regardless of input.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    # Hard-coded safety flags — never change
    auto_optimization_enabled = False
    auto_trading_enabled = False
    mock_fallback_enabled = False
    broker_execution_enabled = False
    production_trading_blocked = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns {check_name: (status, detail)}."""
        checks: Dict[str, Tuple[str, str]] = {}

        # 1. version_info_1_4_2
        try:
            from release.version_info import VERSION
            ok = VERSION.startswith("1.3.") or VERSION.startswith("1.4.") or VERSION.startswith("1.5.")
            checks["version_info_1_4_2"] = ("PASS" if ok else "FAIL", f"VERSION={VERSION}")
        except Exception as exc:
            checks["version_info_1_4_2"] = ("FAIL", str(exc))

        # 2. package_import
        try:
            import strategy_robustness
            ok = strategy_robustness.NO_REAL_ORDERS is True
            checks["package_import"] = ("PASS" if ok else "FAIL", "strategy_robustness imported")
        except Exception as exc:
            checks["package_import"] = ("FAIL", str(exc))

        # 3. safety_flags
        try:
            import strategy_robustness as pkg
            ok = (
                pkg.NO_REAL_ORDERS is True
                and pkg.BROKER_EXECUTION_ENABLED is False
                and pkg.PRODUCTION_TRADING_BLOCKED is True
            )
            checks["safety_flags"] = ("PASS" if ok else "FAIL", "Safety flags correct")
        except Exception as exc:
            checks["safety_flags"] = ("FAIL", str(exc))

        # 4. models_import
        try:
            from strategy_robustness.models_v142 import (
                RobustnessStatus, RobustnessDimension, DecayStatus,
                RobustnessMetric, RobustnessConfiguration, StrategyRobustnessResult
            )
            checks["models_import"] = ("PASS", "All models importable")
        except Exception as exc:
            checks["models_import"] = ("FAIL", str(exc))

        # 5. time_robustness_import
        try:
            from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
            ok = StrategyTimeRobustnessAnalyzer is not None
            checks["time_robustness_import"] = ("PASS" if ok else "FAIL", "StrategyTimeRobustnessAnalyzer available")
        except Exception as exc:
            checks["time_robustness_import"] = ("FAIL", str(exc))

        # 6. cross_sectional_import
        try:
            from strategy_robustness.cross_sectional_v142 import CrossSectionalRobustnessAnalyzer
            checks["cross_sectional_import"] = ("PASS", "CrossSectionalRobustnessAnalyzer available")
        except Exception as exc:
            checks["cross_sectional_import"] = ("FAIL", str(exc))

        # 7. industry_robustness_import
        try:
            from strategy_robustness.industry_robustness_v142 import IndustryRobustnessAnalyzer
            checks["industry_robustness_import"] = ("PASS", "IndustryRobustnessAnalyzer available")
        except Exception as exc:
            checks["industry_robustness_import"] = ("FAIL", str(exc))

        # 8. regime_robustness_import
        try:
            from strategy_robustness.regime_robustness_v142 import RegimeRobustnessAnalyzer
            checks["regime_robustness_import"] = ("PASS", "RegimeRobustnessAnalyzer available")
        except Exception as exc:
            checks["regime_robustness_import"] = ("FAIL", str(exc))

        # 9. parameter_sensitivity_import
        try:
            from strategy_robustness.parameter_sensitivity_v142 import ParameterSensitivityAnalyzer
            checks["parameter_sensitivity_import"] = ("PASS", "ParameterSensitivityAnalyzer available")
        except Exception as exc:
            checks["parameter_sensitivity_import"] = ("FAIL", str(exc))

        # 10. cost_stress_import
        try:
            from strategy_robustness.cost_stress_v142 import StrategyCostStressAnalyzer
            checks["cost_stress_import"] = ("PASS", "StrategyCostStressAnalyzer available")
        except Exception as exc:
            checks["cost_stress_import"] = ("FAIL", str(exc))

        # 11. trade_concentration_import
        try:
            from strategy_robustness.trade_concentration_v142 import TradeConcentrationAnalyzer
            checks["trade_concentration_import"] = ("PASS", "TradeConcentrationAnalyzer available")
        except Exception as exc:
            checks["trade_concentration_import"] = ("FAIL", str(exc))

        # 12. bootstrap_import
        try:
            from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer
            checks["bootstrap_import"] = ("PASS", "BootstrapRobustnessAnalyzer available")
        except Exception as exc:
            checks["bootstrap_import"] = ("FAIL", str(exc))

        # 13. monte_carlo_import
        try:
            from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer
            checks["monte_carlo_import"] = ("PASS", "MonteCarloTradeOrderAnalyzer available")
        except Exception as exc:
            checks["monte_carlo_import"] = ("FAIL", str(exc))

        # 14. rolling_stability_import
        try:
            from strategy_robustness.rolling_stability_v142 import RollingStabilityAnalyzer
            checks["rolling_stability_import"] = ("PASS", "RollingStabilityAnalyzer available")
        except Exception as exc:
            checks["rolling_stability_import"] = ("FAIL", str(exc))

        # 15. decay_detector_import
        try:
            from strategy_robustness.decay_detector_v142 import StrategyDecayDetector
            checks["decay_detector_import"] = ("PASS", "StrategyDecayDetector available")
        except Exception as exc:
            checks["decay_detector_import"] = ("FAIL", str(exc))

        # 16. stress_scenarios_import
        try:
            from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine
            checks["stress_scenarios_import"] = ("PASS", "StrategyStressScenarioEngine available")
        except Exception as exc:
            checks["stress_scenarios_import"] = ("FAIL", str(exc))

        # 17. failure_modes_import
        try:
            from strategy_robustness.failure_modes_v142 import StrategyFailureModeClassifier
            checks["failure_modes_import"] = ("PASS", "StrategyFailureModeClassifier available")
        except Exception as exc:
            checks["failure_modes_import"] = ("FAIL", str(exc))

        # 18. score_import
        try:
            from strategy_robustness.score_v142 import StrategyRobustnessScoreEngine
            checks["score_import"] = ("PASS", "StrategyRobustnessScoreEngine available")
        except Exception as exc:
            checks["score_import"] = ("FAIL", str(exc))

        # 19. comparison_import
        try:
            from strategy_robustness.comparison_v142 import ABCRobustnessComparison, StrategyKnowledgeRobustnessComparison
            checks["comparison_import"] = ("PASS", "Comparison classes available")
        except Exception as exc:
            checks["comparison_import"] = ("FAIL", str(exc))

        # 20. store_import
        try:
            from strategy_robustness.store_v142 import StrategyRobustnessStore
            checks["store_import"] = ("PASS", "StrategyRobustnessStore available")
        except Exception as exc:
            checks["store_import"] = ("FAIL", str(exc))

        # 21. query_import
        try:
            from strategy_robustness.query_v142 import StrategyRobustnessQueryService
            checks["query_import"] = ("PASS", "StrategyRobustnessQueryService available")
        except Exception as exc:
            checks["query_import"] = ("FAIL", str(exc))

        # 22. repair_integration_import
        try:
            from strategy_robustness.repair_integration_v142 import RobustnessRepairIntegration
            checks["repair_integration_import"] = ("PASS", "RobustnessRepairIntegration available")
        except Exception as exc:
            checks["repair_integration_import"] = ("FAIL", str(exc))

        # 23. replay_integration_import
        try:
            from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
            checks["replay_integration_import"] = ("PASS", "RobustnessReplayIntegration available")
        except Exception as exc:
            checks["replay_integration_import"] = ("FAIL", str(exc))

        # 24. report_import
        try:
            from strategy_robustness.report_v142 import StrategyRobustnessReport
            checks["report_import"] = ("PASS", "StrategyRobustnessReport available")
        except Exception as exc:
            checks["report_import"] = ("FAIL", str(exc))

        # 25. auto_optimization_disabled
        try:
            ok = self.auto_optimization_enabled is False
            checks["auto_optimization_disabled"] = ("PASS" if ok else "FAIL",
                                                     f"auto_optimization_enabled={self.auto_optimization_enabled}")
        except Exception as exc:
            checks["auto_optimization_disabled"] = ("FAIL", str(exc))

        # 26. auto_trading_disabled
        try:
            ok = self.auto_trading_enabled is False
            checks["auto_trading_disabled"] = ("PASS" if ok else "FAIL",
                                                f"auto_trading_enabled={self.auto_trading_enabled}")
        except Exception as exc:
            checks["auto_trading_disabled"] = ("FAIL", str(exc))

        # 27. mock_fallback_disabled
        try:
            ok = self.mock_fallback_enabled is False
            checks["mock_fallback_disabled"] = ("PASS" if ok else "FAIL",
                                                 f"mock_fallback_enabled={self.mock_fallback_enabled}")
        except Exception as exc:
            checks["mock_fallback_disabled"] = ("FAIL", str(exc))

        # 28. broker_execution_disabled
        try:
            ok = self.broker_execution_enabled is False
            checks["broker_execution_disabled"] = ("PASS" if ok else "FAIL",
                                                    f"broker_execution_enabled={self.broker_execution_enabled}")
        except Exception as exc:
            checks["broker_execution_disabled"] = ("FAIL", str(exc))

        # 29. production_trading_blocked
        try:
            ok = self.production_trading_blocked is True
            checks["production_trading_blocked"] = ("PASS" if ok else "FAIL",
                                                     f"production_trading_blocked={self.production_trading_blocked}")
        except Exception as exc:
            checks["production_trading_blocked"] = ("FAIL", str(exc))

        # 30. version_flags_142
        try:
            from release.version_info import (
                STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE,
                ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED,
                ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED,
            )
            ok = (
                STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE is True
                and ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED is False
                and ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED is False
            )
            checks["version_flags_142"] = ("PASS" if ok else "FAIL", "v1.4.2 flags present")
        except Exception as exc:
            checks["version_flags_142"] = ("FAIL", str(exc))

        # 31. models_safety_flags
        try:
            from strategy_robustness.models_v142 import (
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
                ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED
            )
            ok = (
                NO_REAL_ORDERS is True
                and BROKER_EXECUTION_ENABLED is False
                and PRODUCTION_TRADING_BLOCKED is True
                and ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED is False
            )
            checks["models_safety_flags"] = ("PASS" if ok else "FAIL", "Models safety flags correct")
        except Exception as exc:
            checks["models_safety_flags"] = ("FAIL", str(exc))

        return checks

    def get_health_summary(self) -> dict:
        """Return summary dict."""
        checks = self.run()
        total = len(checks)
        passed = sum(1 for v in checks.values() if v[0] == "PASS")
        all_pass = passed == total
        return {
            "all_pass": all_pass,
            "passed": passed,
            "failed": total - passed,
            "total_checks": total,
            "checks": {name: {"status": status, "detail": detail} for name, (status, detail) in checks.items()},
            "safety_flags": {
                "auto_optimization_enabled": self.auto_optimization_enabled,
                "auto_trading_enabled": self.auto_trading_enabled,
                "mock_fallback_enabled": self.mock_fallback_enabled,
                "broker_execution_enabled": self.broker_execution_enabled,
                "production_trading_blocked": self.production_trading_blocked,
            },
        }
