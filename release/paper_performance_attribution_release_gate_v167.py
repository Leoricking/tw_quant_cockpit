"""
release/paper_performance_attribution_release_gate_v167.py
Release Gate for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 50+ gate checks. All must PASS before release.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

TARGET_VERSION    = "1.6.7"
RELEASE_NAME      = "Paper Performance Attribution"


def _pass(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "PASS", "detail": detail}


def _fail(name: str, detail: str = "") -> Dict[str, Any]:
    return {"check": name, "status": "FAIL", "detail": detail}


class PaperAttributionReleaseGate:
    """
    50+ release gate checks for Paper Performance Attribution v1.6.7.
    All checks must PASS before the version is committed.
    """

    def run(self) -> Dict[str, Any]:
        checks: List[Dict[str, Any]] = []

        checks.extend(self._check_version())
        checks.extend(self._check_package_safety())
        checks.extend(self._check_modules_importable())
        checks.extend(self._check_enums())
        checks.extend(self._check_models())
        checks.extend(self._check_reconciler())
        checks.extend(self._check_scorecard())
        checks.extend(self._check_validator())
        checks.extend(self._check_store_query())
        checks.extend(self._check_fixture_governance())
        checks.extend(self._check_scenario_registry())
        checks.extend(self._check_report_engine())
        checks.extend(self._check_health_subsystem())
        checks.extend(self._check_no_forbidden_patterns())

        passed = sum(1 for c in checks if c["status"] == "PASS")
        failed = sum(1 for c in checks if c["status"] == "FAIL")
        total  = len(checks)

        return {
            "gate":          "paper_performance_attribution_release_gate_v167",
            "target_version": TARGET_VERSION,
            "release_name":  RELEASE_NAME,
            "status":        "PASS" if failed == 0 else "FAIL",
            "passed":        passed,
            "failed":        failed,
            "total":         total,
            "checks":        checks,
            "paper_only":    True,
            "research_only": True,
            "no_real_orders": True,
        }

    # ── Check groups ──────────────────────────────────────────────────────────

    def _check_version(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.version_v167 import (
                VERSION, RELEASE_NAME as RN, verify_version, is_known_release,
            )
            results.append(_pass("gate_version_1_6_7") if VERSION == "1.6.7" else
                           _fail("gate_version_1_6_7", f"got {VERSION}"))
            results.append(_pass("gate_release_name") if RN == "Paper Performance Attribution" else
                           _fail("gate_release_name", f"got {RN!r}"))
            results.append(_pass("gate_verify_version") if verify_version() else
                           _fail("gate_verify_version"))
            results.append(_pass("gate_v166_is_known") if is_known_release("Multi-session Coordination") else
                           _fail("gate_v166_is_known"))
            results.append(_pass("gate_v167_is_known") if is_known_release("Paper Performance Attribution") else
                           _fail("gate_v167_is_known"))
        except Exception as e:
            results.append(_fail("gate_version_module", str(e)))
        return results

    def _check_package_safety(self) -> List[Dict[str, Any]]:
        results = []
        try:
            import paper_trading.performance_attribution as pkg
            results.append(_pass("gate_pkg_available") if getattr(pkg, "PAPER_ATTRIBUTION_AVAILABLE", False) else
                           _fail("gate_pkg_available"))
            results.append(_pass("gate_pkg_real_disabled") if getattr(pkg, "REAL_PERFORMANCE_ATTRIBUTION_ENABLED", True) is False else
                           _fail("gate_pkg_real_disabled"))
            results.append(_pass("gate_pkg_paper_only") if getattr(pkg, "PAPER_ATTRIBUTION_PAPER_ONLY", False) is True else
                           _fail("gate_pkg_paper_only"))
            results.append(_pass("gate_pkg_no_real_orders") if getattr(pkg, "NO_REAL_ORDERS", False) is True else
                           _fail("gate_pkg_no_real_orders"))
        except Exception as e:
            results.append(_fail("gate_package_safety", str(e)))
        return results

    def _check_modules_importable(self) -> List[Dict[str, Any]]:
        results = []
        modules = [
            "enums_v167",
            "version_v167",
            "safety_v167",
            "models_v167",
            "attribution_input_v167",
            "return_decomposition_v167",
            "pnl_attribution_v167",
            "selection_attribution_v167",
            "allocation_attribution_v167",
            "timing_attribution_v167",
            "execution_attribution_v167",
            "cost_attribution_v167",
            "slippage_attribution_v167",
            "turnover_attribution_v167",
            "exposure_attribution_v167",
            "risk_attribution_v167",
            "drawdown_attribution_v167",
            "regime_attribution_v167",
            "benchmark_attribution_v167",
            "factor_attribution_v167",
            "strategy_attribution_v167",
            "session_attribution_v167",
            "symbol_attribution_v167",
            "sector_attribution_v167",
            "industry_attribution_v167",
            "position_attribution_v167",
            "trade_attribution_v167",
            "portfolio_attribution_v167",
            "contribution_engine_v167",
            "attribution_reconciler_v167",
            "attribution_validator_v167",
            "attribution_scorecard_v167",
            "attribution_store_v167",
            "attribution_query_v167",
            "attribution_report_v167",
            "scenario_registry_v167",
            "fixture_schema_v167",
            "fixture_registry_v167",
            "health_v167",
        ]
        import importlib
        for mod_name in modules:
            try:
                importlib.import_module(f"paper_trading.performance_attribution.{mod_name}")
                results.append(_pass(f"gate_import_{mod_name}"))
            except Exception as e:
                results.append(_fail(f"gate_import_{mod_name}", str(e)))
        return results

    def _check_enums(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.enums_v167 import (
                AttributionLevel, AttributionDimension, ReconciliationStatus,
                AttributionStatus, ConfidenceLevel, RegimeType, FORBIDDEN_FIELDS,
            )
            results.append(_pass("gate_enum_attribution_level", f"{len(AttributionLevel)} values"))
            results.append(_pass("gate_enum_dimensions", f"{len(AttributionDimension)} values"))
            results.append(_pass("gate_enum_reconciliation_status"))
            results.append(_pass("gate_enum_confidence_level"))
            results.append(_pass("gate_enum_regime_type"))
            if len(FORBIDDEN_FIELDS) >= 10:
                results.append(_pass("gate_forbidden_fields_populated"))
            else:
                results.append(_fail("gate_forbidden_fields_populated", f"only {len(FORBIDDEN_FIELDS)}"))
        except Exception as e:
            results.append(_fail("gate_enums", str(e)))
        return results

    def _check_models(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.models_v167 import (
                AttributionPeriod, AttributionReconciliation, AttributionScore,
                AttributionRun, AttributionReport,
            )
            period = AttributionPeriod(
                period_start="2024-01-01",
                period_end="2024-01-31",
            )
            results.append(_pass("gate_model_period_instantiate"))
            results.append(_pass("gate_model_reconciliation_importable"))
            results.append(_pass("gate_model_score_importable"))
            results.append(_pass("gate_model_run_importable"))
            results.append(_pass("gate_model_report_importable"))
        except Exception as e:
            results.append(_fail("gate_models", str(e)))
        return results

    def _check_reconciler(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.attribution_reconciler_v167 import (
                AttributionReconciler,
            )
            from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus

            r = AttributionReconciler()
            rec = r.reconcile("gate", 100.0, 100.0)
            results.append(_pass("gate_reconciler_exact") if rec.status == ReconciliationStatus.RECONCILED else
                           _fail("gate_reconciler_exact", str(rec.status)))
            rec_f = r.reconcile("gate", 100.0, 50.0)
            results.append(_pass("gate_reconciler_fails_large_residual") if rec_f.status == ReconciliationStatus.FAILED else
                           _fail("gate_reconciler_fails_large_residual"))
            results.append(_pass("gate_reconciler_residual_visible") if rec_f.residual != 0.0 else
                           _fail("gate_reconciler_residual_visible"))
        except Exception as e:
            results.append(_fail("gate_reconciler", str(e)))
        return results

    def _check_scorecard(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.attribution_scorecard_v167 import (
                AttributionScorecardEngine, SCORE_WEIGHTS,
            )
            from paper_trading.performance_attribution.enums_v167 import (
                ReconciliationStatus, DataQualityStatus,
            )
            results.append(_pass("gate_scorecard_weights_100") if sum(SCORE_WEIGHTS.values()) == 100 else
                           _fail("gate_scorecard_weights_100"))
            engine = AttributionScorecardEngine()
            sc = engine.compute(
                entity_id="gate",
                reconciliation_status=ReconciliationStatus.RECONCILED,
                residual_pct=0.0,
                data_quality=DataQualityStatus.COMPLETE,
                has_execution_data=True,
                execution_simulated=True,
                cost_quality="KNOWN",
                has_benchmark=True,
                benchmark_stale=False,
                has_risk_data=True,
                risk_data_complete=True,
                has_source_lineage=True,
                deterministic=True,
                has_real_markers=True,
                has_credentials=False,
                fixture_only=False,
            )
            results.append(_pass("gate_scorecard_blocks_real") if sc.total_score == 0.0 else
                           _fail("gate_scorecard_blocks_real", f"score={sc.total_score}"))
        except Exception as e:
            results.append(_fail("gate_scorecard", str(e)))
        return results

    def _check_validator(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.attribution_validator_v167 import (
                AttributionValidator,
            )
            v = AttributionValidator()
            r = v.validate_input({
                "paper_only": True, "research_only": True,
                "no_real_orders": True, "not_for_production": True,
            })
            results.append(_pass("gate_validator_valid_input") if r.get("valid") else
                           _fail("gate_validator_valid_input", str(r.get("errors"))))
            r2 = v.validate_input({
                "broker_session": "live", "paper_only": True,
                "research_only": True, "no_real_orders": True, "not_for_production": True,
            })
            results.append(_pass("gate_validator_blocks_broker_session") if r2.get("blocked") else
                           _fail("gate_validator_blocks_broker_session"))
        except Exception as e:
            results.append(_fail("gate_validator", str(e)))
        return results

    def _check_store_query(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.attribution_store_v167 import AttributionStore
            from paper_trading.performance_attribution.attribution_query_v167 import AttributionQueryAPI
            store = AttributionStore()
            run_data = {
                "paper_only": True, "research_only": True,
                "portfolio_id": "gate_P1",
                "portfolio_attribution": {"active_return": 0.02, "reconciled": True, "confidence": "MEDIUM"},
            }
            store.save_run("gate_run", run_data)
            q = AttributionQueryAPI(store)
            pr = q.get_portfolio_attribution("gate_run")
            results.append(_pass("gate_store_query_round_trip") if pr.get("active_return") == 0.02 else
                           _fail("gate_store_query_round_trip", str(pr)))
            nf = q.get_portfolio_attribution("nonexistent")
            results.append(_pass("gate_query_not_found_handled") if "error" in nf else
                           _fail("gate_query_not_found_handled"))
        except Exception as e:
            results.append(_fail("gate_store_query", str(e)))
        return results

    def _check_fixture_governance(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.fixture_schema_v167 import (
                REQUIRED_FIXTURE_MARKERS, validate_fixture_full, build_fixture_template,
            )
            results.append(_pass("gate_fixture_10_markers") if len(REQUIRED_FIXTURE_MARKERS) == 10 else
                           _fail("gate_fixture_10_markers"))
            tmpl = build_fixture_template("gate_fx", "gate test", "test")
            r = validate_fixture_full(tmpl)
            results.append(_pass("gate_fixture_template_valid") if r["valid"] else
                           _fail("gate_fixture_template_valid", str(r["errors"])))
            bad = dict(tmpl)
            bad["broker_session"] = "live"
            r2 = validate_fixture_full(bad)
            results.append(_pass("gate_fixture_forbidden_blocked") if r2["blocked"] else
                           _fail("gate_fixture_forbidden_blocked"))
        except Exception as e:
            results.append(_fail("gate_fixture_governance", str(e)))
        return results

    def _check_scenario_registry(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.scenario_registry_v167 import (
                ScenarioRegistry, _SCENARIOS,
            )
            results.append(_pass("gate_scenarios_80plus", f"{len(_SCENARIOS)}") if len(_SCENARIOS) >= 80 else
                           _fail("gate_scenarios_80plus", f"only {len(_SCENARIOS)}"))
            reg = ScenarioRegistry()
            s = reg.get("SF-001")
            results.append(_pass("gate_scenario_safety_category") if s and s["expected_status"] == "BLOCKED" else
                           _fail("gate_scenario_safety_category"))
        except Exception as e:
            results.append(_fail("gate_scenario_registry", str(e)))
        return results

    def _check_report_engine(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.attribution_report_v167 import (
                AttributionReportEngine, REPORT_SECTIONS,
            )
            results.append(_pass("gate_report_31_sections") if len(REPORT_SECTIONS) == 31 else
                           _fail("gate_report_31_sections", f"{len(REPORT_SECTIONS)}"))
            engine = AttributionReportEngine({
                "run_id": "gate_rpt",
                "portfolio_id": "gate_P",
                "period_start": "2024-01-01",
                "period_end": "2024-01-31",
                "status": "COMPLETE",
                "paper_only": True,
                "research_only": True,
                "portfolio_attribution": {"active_return": 0.02},
            })
            gui = engine.to_gui_model()
            results.append(_pass("gate_report_gui_31_tabs") if gui["tab_count"] == 31 else
                           _fail("gate_report_gui_31_tabs", f"{gui['tab_count']}"))
            md = engine.to_markdown()
            results.append(_pass("gate_report_markdown_not_for_real") if "NOT FOR REAL TRADING" in md else
                           _fail("gate_report_markdown_not_for_real"))
        except Exception as e:
            results.append(_fail("gate_report_engine", str(e)))
        return results

    def _check_health_subsystem(self) -> List[Dict[str, Any]]:
        results = []
        try:
            from paper_trading.performance_attribution.health_v167 import (
                PaperAttributionHealthCheck,
            )
            hc = PaperAttributionHealthCheck()
            r = hc.run()
            results.append(_pass("gate_health_run_returns_dict") if isinstance(r, dict) else
                           _fail("gate_health_run_returns_dict"))
            results.append(_pass("gate_health_has_checks") if len(r.get("checks", [])) >= 60 else
                           _fail("gate_health_has_checks", f"only {len(r.get('checks', []))} checks"))
            results.append(_pass("gate_health_has_status") if "status" in r else
                           _fail("gate_health_has_status"))
        except Exception as e:
            results.append(_fail("gate_health_subsystem", str(e)))
        return results

    def _check_no_forbidden_patterns(self) -> List[Dict[str, Any]]:
        """Verify safety module rejects live/real data patterns."""
        results = []
        try:
            from paper_trading.performance_attribution.safety_v167 import (
                validate_attribution_safety,
                check_forbidden_fields,
            )
            bad = {"shioaji_login": True, "paper_only": True, "research_only": True}
            r = validate_attribution_safety(bad)
            results.append(_pass("gate_safety_shioaji_blocked") if r.get("blocked") else
                           _fail("gate_safety_shioaji_blocked"))
            r2 = check_forbidden_fields({"broker_api_key": "secret_key"})
            results.append(_pass("gate_safety_broker_api_key_blocked") if len(r2) > 0 else
                           _fail("gate_safety_broker_api_key_blocked"))
        except Exception as e:
            results.append(_fail("gate_no_forbidden_patterns", str(e)))
        return results
