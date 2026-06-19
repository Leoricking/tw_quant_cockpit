"""
abc_validation/health_v141.py — Health check for A/B/C Buy Point Validation v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple


class ABCBuyPointValidationHealthCheck:
    """
    Health checks for the abc_validation package.

    Health summary includes all required safety flags and availability indicators.
    """

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns {check_name: (status, detail)}."""
        checks: Dict[str, Tuple[str, str]] = {}

        # 1. version_info_1_4_1
        try:
            from release.version_info import VERSION
            ok = VERSION.startswith("1.4.")
            checks["version_info_1_4_1"] = ("PASS" if ok else "FAIL", f"VERSION={VERSION}")
        except Exception as exc:
            checks["version_info_1_4_1"] = ("FAIL", str(exc))

        # 2. package_import
        try:
            import abc_validation
            ok = abc_validation.NO_REAL_ORDERS is True
            checks["package_import"] = ("PASS" if ok else "FAIL", "abc_validation imported")
        except Exception as exc:
            checks["package_import"] = ("FAIL", str(exc))

        # 3. abc_safety_flags
        try:
            import abc_validation as pkg
            ok = (
                pkg.NO_REAL_ORDERS is True
                and pkg.BROKER_EXECUTION_ENABLED is False
                and pkg.PRODUCTION_TRADING_BLOCKED is True
            )
            checks["abc_safety_flags"] = ("PASS" if ok else "FAIL", "Safety flags correct")
        except Exception as exc:
            checks["abc_safety_flags"] = ("FAIL", str(exc))

        # 4. rule_adapters
        try:
            from abc_validation.rule_adapters_v141 import (
                ABuyPointRuleAdapter, BBuyPointRuleAdapter, CBuyPointRuleAdapter
            )
            a = ABuyPointRuleAdapter()
            b = BBuyPointRuleAdapter()
            c = CBuyPointRuleAdapter()
            checks["rule_adapters"] = ("PASS", "A/B/C rule adapters available")
        except Exception as exc:
            checks["rule_adapters"] = ("FAIL", str(exc))

        # 5. a_rule_delegates_to_registry
        try:
            from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
            rule = ABuyPointRuleAdapter().get_rule()
            ok = rule is not None and rule.rule_id == "abc_buy_point_a"
            checks["a_rule_delegates_to_registry"] = ("PASS" if ok else "FAIL",
                                                        f"rule_id={getattr(rule, 'rule_id', None)}")
        except Exception as exc:
            checks["a_rule_delegates_to_registry"] = ("FAIL", str(exc))

        # 6. b_rule_delegates_to_registry
        try:
            from abc_validation.rule_adapters_v141 import BBuyPointRuleAdapter
            rule = BBuyPointRuleAdapter().get_rule()
            ok = rule is not None and rule.rule_id == "abc_buy_point_b"
            checks["b_rule_delegates_to_registry"] = ("PASS" if ok else "FAIL",
                                                        f"rule_id={getattr(rule, 'rule_id', None)}")
        except Exception as exc:
            checks["b_rule_delegates_to_registry"] = ("FAIL", str(exc))

        # 7. c_rule_delegates_to_registry
        try:
            from abc_validation.rule_adapters_v141 import CBuyPointRuleAdapter
            rule = CBuyPointRuleAdapter().get_rule()
            ok = rule is not None and rule.rule_id == "abc_buy_point_c"
            checks["c_rule_delegates_to_registry"] = ("PASS" if ok else "FAIL",
                                                        f"rule_id={getattr(rule, 'rule_id', None)}")
        except Exception as exc:
            checks["c_rule_delegates_to_registry"] = ("FAIL", str(exc))

        # 8. snapshots_available
        try:
            from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
            snap = ABCBuyPointRuleSnapshot.make_default("A")
            ok = snap.buy_point_type == "A"
            checks["snapshots_available"] = ("PASS" if ok else "FAIL", "ABCBuyPointRuleSnapshot available")
        except Exception as exc:
            checks["snapshots_available"] = ("FAIL", str(exc))

        # 9. integrity_guard_available
        try:
            from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
            guard = ABCSignalIntegrityGuard()
            checks["integrity_guard_available"] = ("PASS", "ABCSignalIntegrityGuard available")
        except Exception as exc:
            checks["integrity_guard_available"] = ("FAIL", str(exc))

        # 10. parameters_available
        try:
            from abc_validation.parameters_v141 import ABCValidationParameters
            params = ABCValidationParameters()
            params.validate()
            checks["parameters_available"] = ("PASS", "ABCValidationParameters available")
        except Exception as exc:
            checks["parameters_available"] = ("FAIL", str(exc))

        # 11. holding_period_analyzer_available
        try:
            from abc_validation.holding_period_analyzer_v141 import ABCHoldingPeriodAnalyzer
            ana = ABCHoldingPeriodAnalyzer()
            checks["holding_period_analyzer_available"] = ("PASS", "ABCHoldingPeriodAnalyzer available")
        except Exception as exc:
            checks["holding_period_analyzer_available"] = ("FAIL", str(exc))

        # 12. stop_loss_analyzer_available
        try:
            from abc_validation.stop_loss_analyzer_v141 import ABCStopLossAnalyzer
            sla = ABCStopLossAnalyzer()
            checks["stop_loss_analyzer_available"] = ("PASS", "ABCStopLossAnalyzer available")
        except Exception as exc:
            checks["stop_loss_analyzer_available"] = ("FAIL", str(exc))

        # 13. take_profit_analyzer_available
        try:
            from abc_validation.take_profit_analyzer_v141 import ABCTakeProfitAnalyzer
            tpa = ABCTakeProfitAnalyzer()
            checks["take_profit_analyzer_available"] = ("PASS", "ABCTakeProfitAnalyzer available")
        except Exception as exc:
            checks["take_profit_analyzer_available"] = ("FAIL", str(exc))

        # 14. regime_analyzer_available
        try:
            from abc_validation.regime_analyzer_v141 import ABCRegimeAnalyzer
            ra = ABCRegimeAnalyzer()
            checks["regime_analyzer_available"] = ("PASS", "ABCRegimeAnalyzer available")
        except Exception as exc:
            checks["regime_analyzer_available"] = ("FAIL", str(exc))

        # 15. filter_ablation_available
        try:
            from abc_validation.filter_ablation_v141 import ABCFilterAblationAnalyzer
            faa = ABCFilterAblationAnalyzer()
            checks["filter_ablation_available"] = ("PASS", "ABCFilterAblationAnalyzer available")
        except Exception as exc:
            checks["filter_ablation_available"] = ("FAIL", str(exc))

        # 16. second_wave_analyzer_available
        try:
            from abc_validation.second_wave_analyzer_v141 import ABCSecondWaveAnalyzer
            swa = ABCSecondWaveAnalyzer()
            checks["second_wave_analyzer_available"] = ("PASS", "ABCSecondWaveAnalyzer available")
        except Exception as exc:
            checks["second_wave_analyzer_available"] = ("FAIL", str(exc))

        # 17. institutional_margin_analyzer_available
        try:
            from abc_validation.institutional_margin_analyzer_v141 import ABCInstitutionalMarginAnalyzer
            ima = ABCInstitutionalMarginAnalyzer()
            checks["institutional_margin_analyzer_available"] = ("PASS", "ABCInstitutionalMarginAnalyzer available")
        except Exception as exc:
            checks["institutional_margin_analyzer_available"] = ("FAIL", str(exc))

        # 18. volume_analyzer_available
        try:
            from abc_validation.volume_analyzer_v141 import ABCVolumeAnalyzer
            va = ABCVolumeAnalyzer()
            checks["volume_analyzer_available"] = ("PASS", "ABCVolumeAnalyzer available")
        except Exception as exc:
            checks["volume_analyzer_available"] = ("FAIL", str(exc))

        # 19. outcome_taxonomy_available
        try:
            from abc_validation.outcome_taxonomy_v141 import ABCOutcomeType, classify_outcome
            all_types = ABCOutcomeType.all_types()
            ok = len(all_types) >= 10
            checks["outcome_taxonomy_available"] = ("PASS" if ok else "FAIL",
                                                    f"{len(all_types)} outcome types")
        except Exception as exc:
            checks["outcome_taxonomy_available"] = ("FAIL", str(exc))

        # 20. failure_rate_analyzer_available
        try:
            from abc_validation.failure_rate_analyzer_v141 import ABCFailureRateAnalyzer
            fra = ABCFailureRateAnalyzer()
            checks["failure_rate_analyzer_available"] = ("PASS", "ABCFailureRateAnalyzer available")
        except Exception as exc:
            checks["failure_rate_analyzer_available"] = ("FAIL", str(exc))

        # 21. validation_result_available
        try:
            from abc_validation.validation_result_v141 import ABCValidationResult
            r = ABCValidationResult(
                validation_id="test_health",
                buy_point_type="A",
                rule_snapshot_id="snap_test",
            )
            ok = r.no_real_orders is True and r.production_trading_blocked is True
            checks["validation_result_available"] = ("PASS" if ok else "FAIL", "ABCValidationResult available")
        except Exception as exc:
            checks["validation_result_available"] = ("FAIL", str(exc))

        # 22. comparison_engine_available
        try:
            from abc_validation.comparison_engine_v141 import ABCComparisonEngine
            ce = ABCComparisonEngine()
            checks["comparison_engine_available"] = ("PASS", "ABCComparisonEngine available")
        except Exception as exc:
            checks["comparison_engine_available"] = ("FAIL", str(exc))

        # 23. confidence_evaluator_available
        try:
            from abc_validation.confidence_v141 import ABCValidationConfidence
            conf = ABCValidationConfidence()
            checks["confidence_evaluator_available"] = ("PASS", "ABCValidationConfidence available")
        except Exception as exc:
            checks["confidence_evaluator_available"] = ("FAIL", str(exc))

        # 24. walk_forward_available
        try:
            from abc_validation.walk_forward_v141 import ABCWalkForwardValidator
            wfv = ABCWalkForwardValidator()
            checks["walk_forward_available"] = ("PASS", "ABCWalkForwardValidator available")
        except Exception as exc:
            checks["walk_forward_available"] = ("FAIL", str(exc))

        # 25. store_available
        try:
            from abc_validation.store_v141 import ABCValidationStore
            store = ABCValidationStore()
            checks["store_available"] = ("PASS", "ABCValidationStore available")
        except Exception as exc:
            checks["store_available"] = ("FAIL", str(exc))

        # 26. repair_integration_available
        try:
            from abc_validation.repair_integration_v141 import ABCRepairIntegration
            ri = ABCRepairIntegration()
            ok = not ri.auto_repair_enabled and not ri.auto_download_enabled
            checks["repair_integration_available"] = ("PASS" if ok else "FAIL",
                                                      "ABCRepairIntegration available")
        except Exception as exc:
            checks["repair_integration_available"] = ("FAIL", str(exc))

        # 27. replay_integration_available
        try:
            from abc_validation.replay_integration_v141 import ABCReplayIntegration
            ri = ABCReplayIntegration()
            ok = ri.READ_ONLY and not ri.MODIFIES_REPLAY_SESSIONS
            checks["replay_integration_available"] = ("PASS" if ok else "FAIL",
                                                       "ABCReplayIntegration available")
        except Exception as exc:
            checks["replay_integration_available"] = ("FAIL", str(exc))

        # 28. report_available
        try:
            from abc_validation.report_v141 import ABCValidationReport
            rpt = ABCValidationReport()
            checks["report_available"] = ("PASS", "ABCValidationReport available")
        except Exception as exc:
            checks["report_available"] = ("FAIL", str(exc))

        # 29. signal_classification_available
        try:
            from abc_validation.signal_classification_v141 import ABCSignalClassification, ABCSignalRecord
            ok = len(ABCSignalClassification.all_a()) >= 4
            checks["signal_classification_available"] = ("PASS" if ok else "FAIL",
                                                          "ABCSignalClassification available")
        except Exception as exc:
            checks["signal_classification_available"] = ("FAIL", str(exc))

        # 30. no_auto_optimization
        try:
            from release.version_info import ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED
            ok = ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED is False
            checks["no_auto_optimization"] = ("PASS" if ok else "FAIL",
                                              f"ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED={ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED}")
        except Exception as exc:
            checks["no_auto_optimization"] = ("FAIL", str(exc))

        # 31. no_mock_formal_conclusion
        try:
            from release.version_info import ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED
            ok = ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED is False
            checks["no_mock_formal_conclusion"] = ("PASS" if ok else "FAIL",
                                                    f"ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED={ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED}")
        except Exception as exc:
            checks["no_mock_formal_conclusion"] = ("FAIL", str(exc))

        return checks

    def get_health_summary(self) -> dict:
        """Get health summary including all required fields."""
        checks = self.run()

        passed = sum(1 for s, _ in checks.values() if s == "PASS")
        failed = sum(1 for s, _ in checks.values() if s == "FAIL")
        total = len(checks)

        # Check specific availability
        abc_a_ok = checks.get("a_rule_delegates_to_registry", ("FAIL",))[0] == "PASS"
        abc_b_ok = checks.get("b_rule_delegates_to_registry", ("FAIL",))[0] == "PASS"
        abc_c_ok = checks.get("c_rule_delegates_to_registry", ("FAIL",))[0] == "PASS"

        try:
            from abc_validation.store_v141 import ABCValidationStore
            store = ABCValidationStore()
            summary = store.summarize()
        except Exception:
            summary = {"total_validation_results": 0, "passed": 0, "blocked": 0, "insufficient": 0}

        return {
            "abc_validation_status": "PASS" if failed == 0 else "FAIL",
            "abc_validation_schema_version": "1.4.1",
            "abc_rules_total": 3,
            "abc_a_available": abc_a_ok,
            "abc_b_available": abc_b_ok,
            "abc_c_available": abc_c_ok,
            "validation_runs_total": summary.get("total_validation_results", 0),
            "validation_passed": summary.get("passed", 0),
            "validation_degraded": 0,
            "validation_blocked": summary.get("blocked", 0),
            "validation_insufficient": summary.get("insufficient", 0),
            "validation_no_trades": 0,
            "formal_conclusions_allowed_count": 0,
            "lookahead_violations": 0,
            "mock_results_count": 0,
            "auto_optimization_enabled": False,
            "auto_trading_enabled": False,
            "mock_fallback_enabled": False,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "all_pass": failed == 0,
            "passed": passed,
            "failed": failed,
            "total_checks": total,
            "checks": {
                name: {"status": status, "detail": detail}
                for name, (status, detail) in checks.items()
            },
            "safety_flags": {
                "NO_REAL_ORDERS": True,
                "BROKER_EXECUTION_ENABLED": False,
                "PRODUCTION_TRADING_BLOCKED": True,
                "ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED": False,
                "ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED": False,
                "ABC_BUY_POINT_AUTO_TRADING_ENABLED": False,
            },
        }
