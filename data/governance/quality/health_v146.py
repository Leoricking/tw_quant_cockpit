"""
data/governance/quality/health_v146.py — Provider Quality Gates Health Check v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] 50+ checks. Must work fully OFFLINE.
[!] Provider unavailability does not fail offline health.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False
AUTO_QUARANTINE_RELEASE_ENABLED = False
MOCK_FALLBACK_ENABLED = False

_PASS = "PASS"
_FAIL = "FAIL"
_WARN = "WARN"
_BLOCKED = "BLOCKED"


class ProviderQualityGatesHealthCheck:
    """
    Health checks for Provider Quality Gates v1.4.6.
    50+ offline checks covering all modules + safety invariants.
    Provider unavailability → WARN (not FAIL).
    """

    def run(self) -> Dict[str, Tuple[str, str]]:
        checks: Dict[str, Tuple[str, str]] = {}

        # Package integrity
        checks["package_import"] = self._safe_check(self._check_package_import)
        checks["models_import"] = self._safe_check(self._check_models_import)
        checks["gate_registry_import"] = self._safe_check(self._check_gate_registry_import)
        checks["decision_engine_import"] = self._safe_check(self._check_decision_engine_import)
        checks["provider_gate_import"] = self._safe_check(self._check_provider_gate_import)
        checks["dataset_gate_import"] = self._safe_check(self._check_dataset_gate_import)
        checks["endpoint_gate_import"] = self._safe_check(self._check_endpoint_gate_import)
        checks["batch_gate_import"] = self._safe_check(self._check_batch_gate_import)
        checks["formal_research_gate_import"] = self._safe_check(self._check_formal_research_gate_import)
        checks["backtest_gate_import"] = self._safe_check(self._check_backtest_gate_import)
        checks["report_gate_import"] = self._safe_check(self._check_report_gate_import)
        checks["quality_gate_import"] = self._safe_check(self._check_quality_gate_import)
        checks["freshness_gate_import"] = self._safe_check(self._check_freshness_gate_import)
        checks["coverage_gate_import"] = self._safe_check(self._check_coverage_gate_import)
        checks["provenance_gate_import"] = self._safe_check(self._check_provenance_gate_import)
        checks["pit_gate_import"] = self._safe_check(self._check_pit_gate_import)
        checks["schema_gate_import"] = self._safe_check(self._check_schema_gate_import)
        checks["authority_gate_import"] = self._safe_check(self._check_authority_gate_import)
        checks["conflict_gate_import"] = self._safe_check(self._check_conflict_gate_import)
        checks["rate_limit_gate_import"] = self._safe_check(self._check_rate_limit_gate_import)
        checks["quota_gate_import"] = self._safe_check(self._check_quota_gate_import)
        checks["safety_gate_import"] = self._safe_check(self._check_safety_gate_import)
        checks["score_import"] = self._safe_check(self._check_score_import)
        checks["quarantine_import"] = self._safe_check(self._check_quarantine_import)
        checks["audit_import"] = self._safe_check(self._check_audit_import)
        checks["policy_import"] = self._safe_check(self._check_policy_import)
        checks["store_import"] = self._safe_check(self._check_store_import)
        checks["query_import"] = self._safe_check(self._check_query_import)

        # Functional checks
        checks["enum_provider_quality_state"] = self._safe_check(self._check_enum_provider_quality_state)
        checks["enum_gate_status"] = self._safe_check(self._check_enum_gate_status)
        checks["enum_quality_decision_result"] = self._safe_check(self._check_enum_quality_decision_result)
        checks["gate_registry_validate"] = self._safe_check(self._check_gate_registry_validate)
        checks["gate_registry_count"] = self._safe_check(self._check_gate_registry_count)
        checks["decision_engine_blocking_wins"] = self._safe_check(self._check_decision_engine_blocking_wins)
        checks["quarantine_auto_release_false"] = self._safe_check(self._check_quarantine_auto_release_false)
        checks["score_no_override"] = self._safe_check(self._check_score_no_override)
        checks["policy_validation"] = self._safe_check(self._check_policy_validation)
        checks["store_memory_mode"] = self._safe_check(self._check_store_memory_mode)
        checks["audit_append_only"] = self._safe_check(self._check_audit_append_only)
        checks["dataset_not_allowlisted_blocked"] = self._safe_check(self._check_dataset_not_allowlisted_blocked)
        checks["future_leakage_blocked"] = self._safe_check(self._check_future_leakage_blocked)
        checks["schema_breaking_blocked"] = self._safe_check(self._check_schema_breaking_blocked)
        checks["mock_authority_blocked_formal"] = self._safe_check(self._check_mock_authority_blocked_formal)
        checks["freshness_unknown_not_pass"] = self._safe_check(self._check_freshness_unknown_not_pass)

        # Safety invariants (must all PASS)
        checks["safety_no_real_orders"] = self._safe_check(self._check_safety_no_real_orders)
        checks["safety_broker_disabled"] = self._safe_check(self._check_safety_broker_disabled)
        checks["safety_production_blocked"] = self._safe_check(self._check_safety_production_blocked)
        checks["safety_score_no_override"] = self._safe_check(self._check_safety_score_no_override)
        checks["safety_no_auto_promotion"] = self._safe_check(self._check_safety_no_auto_promotion)
        checks["safety_no_auto_release"] = self._safe_check(self._check_safety_no_auto_release)
        checks["safety_no_mock_fallback"] = self._safe_check(self._check_safety_no_mock_fallback)
        checks["safety_no_primary_override"] = self._safe_check(self._check_safety_no_primary_override)
        checks["safety_no_rate_bypass"] = self._safe_check(self._check_safety_no_rate_bypass)
        checks["safety_gate_invariants"] = self._safe_check(self._check_safety_gate_invariants)

        # v1.4.5 integration (offline check)
        checks["v145_authority_integration"] = self._safe_check(self._check_v145_authority_integration)
        checks["v145_provenance_integration"] = self._safe_check(self._check_v145_provenance_integration)
        checks["v145_conflict_integration"] = self._safe_check(self._check_v145_conflict_integration)

        # CLI registration
        checks["cli_registration"] = self._safe_check(self._check_cli_registration)

        # GUI import (WARN if unavailable)
        checks["gui_import"] = self._safe_check(self._check_gui_import)

        return checks

    def get_health_summary(self) -> Dict[str, Any]:
        checks = self.run()
        passed = sum(1 for s, _ in checks.values() if s == _PASS)
        failed = sum(1 for s, _ in checks.values() if s == _FAIL)
        warned = sum(1 for s, _ in checks.values() if s == _WARN)
        blocked = sum(1 for s, _ in checks.values() if s == _BLOCKED)
        return {
            "version": "1.4.6",
            "release_name": "Provider Quality Gates",
            "no_real_orders": True,
            "research_only": True,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "blocked": blocked,
            "total": len(checks),
            "checks": {
                name: {"status": status, "detail": detail}
                for name, (status, detail) in checks.items()
            },
        }

    def _safe_check(self, fn) -> Tuple[str, str]:
        try:
            return fn()
        except Exception as e:
            return (_FAIL, str(e))

    # ------------------------------------------------------------------
    # Import checks
    # ------------------------------------------------------------------

    def _check_package_import(self) -> Tuple[str, str]:
        from data.governance.quality import (
            NO_REAL_ORDERS as _NRO, BROKER_EXECUTION_ENABLED as _BEE
        )
        assert _NRO is True
        assert _BEE is False
        return (_PASS, "quality package importable, safety flags correct")

    def _check_models_import(self) -> Tuple[str, str]:
        from data.governance.quality.models_v146 import (
            ProviderQualityState, GateStatus, QualityDecisionResult,
            FreshnessStatus, CoverageStatus, OperationalReadiness,
        )
        assert len(ProviderQualityState) == 7
        assert len(GateStatus) == 6
        return (_PASS, "models_v146 importable")

    def _check_gate_registry_import(self) -> Tuple[str, str]:
        from data.governance.quality.gate_registry_v146 import QualityGateRegistry
        reg = QualityGateRegistry()
        assert len(reg.list_gates()) >= 15
        return (_PASS, f"gate_registry_v146 importable, {len(reg.list_gates())} gates")

    def _check_decision_engine_import(self) -> Tuple[str, str]:
        from data.governance.quality.decision_engine_v146 import QualityDecisionEngine
        eng = QualityDecisionEngine()
        assert eng is not None
        return (_PASS, "decision_engine_v146 importable")

    def _check_provider_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.provider_gate_v146 import ProviderOperationalGate
        g = ProviderOperationalGate()
        assert g is not None
        return (_PASS, "provider_gate_v146 importable")

    def _check_dataset_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.dataset_gate_v146 import DatasetAdmissionGate
        g = DatasetAdmissionGate()
        assert g is not None
        return (_PASS, "dataset_gate_v146 importable")

    def _check_endpoint_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.endpoint_gate_v146 import EndpointReadinessGate
        g = EndpointReadinessGate()
        assert g is not None
        return (_PASS, "endpoint_gate_v146 importable")

    def _check_batch_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.batch_gate_v146 import BatchIngestionGate
        g = BatchIngestionGate()
        assert g is not None
        return (_PASS, "batch_gate_v146 importable")

    def _check_formal_research_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.formal_research_gate_v146 import FormalResearchEligibilityGate
        g = FormalResearchEligibilityGate()
        assert g is not None
        return (_PASS, "formal_research_gate_v146 importable")

    def _check_backtest_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.backtest_gate_v146 import BacktestInputEligibilityGate
        g = BacktestInputEligibilityGate()
        assert g is not None
        return (_PASS, "backtest_gate_v146 importable")

    def _check_report_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.report_gate_v146 import ReportEligibilityGate
        g = ReportEligibilityGate()
        assert g is not None
        return (_PASS, "report_gate_v146 importable")

    def _check_quality_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.quality_gate_v146 import DataQualityGate
        g = DataQualityGate()
        assert g is not None
        return (_PASS, "quality_gate_v146 importable")

    def _check_freshness_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.freshness_gate_v146 import FreshnessGate
        g = FreshnessGate()
        assert g is not None
        return (_PASS, "freshness_gate_v146 importable")

    def _check_coverage_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.coverage_gate_v146 import CoverageGate
        g = CoverageGate()
        assert g is not None
        return (_PASS, "coverage_gate_v146 importable")

    def _check_provenance_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.provenance_gate_v146 import ProvenanceGate
        g = ProvenanceGate()
        assert g is not None
        return (_PASS, "provenance_gate_v146 importable, wraps v1.4.5")

    def _check_pit_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.pit_gate_v146 import PointInTimeGate
        g = PointInTimeGate()
        assert g is not None
        return (_PASS, "pit_gate_v146 importable")

    def _check_schema_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.schema_gate_v146 import SchemaDriftGate
        g = SchemaDriftGate()
        assert g is not None
        return (_PASS, "schema_gate_v146 importable")

    def _check_authority_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.authority_gate_v146 import AuthorityGate
        g = AuthorityGate()
        assert g is not None
        return (_PASS, "authority_gate_v146 importable")

    def _check_conflict_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.conflict_gate_v146 import ConflictGate
        g = ConflictGate()
        assert g is not None
        return (_PASS, "conflict_gate_v146 importable")

    def _check_rate_limit_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.rate_limit_gate_v146 import RateLimitReadinessGate
        g = RateLimitReadinessGate()
        assert g is not None
        return (_PASS, "rate_limit_gate_v146 importable")

    def _check_quota_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.quota_gate_v146 import QuotaReadinessGate
        g = QuotaReadinessGate()
        assert g is not None
        return (_PASS, "quota_gate_v146 importable")

    def _check_safety_gate_import(self) -> Tuple[str, str]:
        from data.governance.quality.safety_gate_v146 import SafetyGate
        g = SafetyGate()
        assert g is not None
        return (_PASS, "safety_gate_v146 importable")

    def _check_score_import(self) -> Tuple[str, str]:
        from data.governance.quality.score_v146 import QualityScoreEngine
        eng = QualityScoreEngine()
        assert eng is not None
        return (_PASS, "score_v146 importable")

    def _check_quarantine_import(self) -> Tuple[str, str]:
        from data.governance.quality.quarantine_v146 import ProviderQuarantineManager
        mgr = ProviderQuarantineManager()
        assert mgr is not None
        return (_PASS, "quarantine_v146 importable")

    def _check_audit_import(self) -> Tuple[str, str]:
        from data.governance.quality.audit_v146 import QualityDecisionAuditService
        svc = QualityDecisionAuditService()
        assert svc is not None
        return (_PASS, "audit_v146 importable")

    def _check_policy_import(self) -> Tuple[str, str]:
        from data.governance.quality.policy_v146 import QualityPolicyManager
        mgr = QualityPolicyManager()
        assert mgr is not None
        return (_PASS, "policy_v146 importable")

    def _check_store_import(self) -> Tuple[str, str]:
        from data.governance.quality.store_v146 import QualityGateStore
        store = QualityGateStore()
        store.setup(db_path=None)
        assert store.mode == "memory"
        store.close()
        return (_PASS, "store_v146 importable, memory mode works")

    def _check_query_import(self) -> Tuple[str, str]:
        from data.governance.quality.query_v146 import ProviderQualityQueryService
        svc = ProviderQualityQueryService()
        assert svc is not None
        return (_PASS, "query_v146 importable")

    # ------------------------------------------------------------------
    # Functional checks
    # ------------------------------------------------------------------

    def _check_enum_provider_quality_state(self) -> Tuple[str, str]:
        from data.governance.quality.models_v146 import ProviderQualityState
        expected = {"ACTIVE", "DEGRADED", "RESTRICTED", "QUARANTINED", "BLOCKED", "DISABLED", "UNKNOWN"}
        actual = {s.value for s in ProviderQualityState}
        assert actual == expected, f"Missing states: {expected - actual}"
        return (_PASS, "ProviderQualityState has all 7 values")

    def _check_enum_gate_status(self) -> Tuple[str, str]:
        from data.governance.quality.models_v146 import GateStatus
        expected = {"PASS", "WARN", "FAIL", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"}
        actual = {s.value for s in GateStatus}
        assert actual == expected, f"Missing: {expected - actual}"
        return (_PASS, "GateStatus has all 6 values")

    def _check_enum_quality_decision_result(self) -> Tuple[str, str]:
        from data.governance.quality.models_v146 import QualityDecisionResult
        expected = {"ALLOW", "ALLOW_WITH_WARNING", "RESTRICT", "QUARANTINE", "BLOCK", "DISABLE"}
        actual = {s.value for s in QualityDecisionResult}
        assert actual == expected
        return (_PASS, "QualityDecisionResult has all 6 values")

    def _check_gate_registry_validate(self) -> Tuple[str, str]:
        from data.governance.quality.gate_registry_v146 import QualityGateRegistry
        reg = QualityGateRegistry()
        result = reg.validate_registry()
        assert result["valid"] is True, f"Registry invalid: {result['errors']}"
        return (_PASS, "Gate registry validation passed")

    def _check_gate_registry_count(self) -> Tuple[str, str]:
        from data.governance.quality.gate_registry_v146 import QualityGateRegistry
        reg = QualityGateRegistry()
        count = len(reg.list_gates())
        assert count >= 15, f"Expected >= 15 gates, got {count}"
        return (_PASS, f"{count} gates registered")

    def _check_decision_engine_blocking_wins(self) -> Tuple[str, str]:
        from data.governance.quality.decision_engine_v146 import QualityDecisionEngine
        from data.governance.quality.models_v146 import GateStatus, QualityGateResult, QualityScope
        eng = QualityDecisionEngine()
        blocking_result = QualityGateResult(
            gate_id="test_gate", gate_name="Test", scope=QualityScope.PROVIDER.value,
            subject_id="test_provider", status=GateStatus.BLOCKED.value,
            passed=False, blocking=True, evidence="test block",
        )
        decision = eng.decide(
            QualityScope.PROVIDER.value, "test_provider",
            [blocking_result], quality_score=99.0
        )
        assert decision.formal_research_allowed is False, "Blocking failure must block formal research"
        assert decision.score_overrode_blocking is False
        assert len(decision.blocking_failures) > 0
        return (_PASS, "Blocking rules override score: confirmed")

    def _check_quarantine_auto_release_false(self) -> Tuple[str, str]:
        from data.governance.quality.quarantine_v146 import ProviderQuarantineManager
        mgr = ProviderQuarantineManager()
        rec = mgr.quarantine("test_provider", "test reason", "test_gate")
        assert rec.auto_release_allowed is False
        readiness = mgr.evaluate_release_readiness("test_provider")
        assert readiness["auto_release_allowed"] is False
        return (_PASS, "auto_release_allowed = False confirmed")

    def _check_score_no_override(self) -> Tuple[str, str]:
        from data.governance.quality.score_v146 import QualityScoreEngine
        from data.governance.quality.models_v146 import GateStatus, QualityGateResult
        eng = QualityScoreEngine()
        score = eng.compute("p", "p", [], blocking_failures=["gate_x"])
        assert score.can_override_blocking is False
        assert score.blocking_failures_present is True
        return (_PASS, "Score cannot override blocking: confirmed")

    def _check_policy_validation(self) -> Tuple[str, str]:
        from data.governance.quality.policy_v146 import QualityPolicyManager
        mgr = QualityPolicyManager()
        bad_policy = {"mock_formal_conclusion_allowed": True, "score_can_override_blocking": True}
        result = mgr.validate_policy(bad_policy)
        assert result["valid"] is False
        assert len(result["errors"]) >= 2
        return (_PASS, "Policy validation rejects forbidden features")

    def _check_store_memory_mode(self) -> Tuple[str, str]:
        from data.governance.quality.store_v146 import QualityGateStore
        store = QualityGateStore()
        store.setup(db_path=None)
        assert store.mode == "memory"
        store.upsert_provider_profile({
            "provider_id": "test_twse",
            "quality_state": "ACTIVE",
            "authority_level": "PRIMARY_OFFICIAL",
            "formal_research_allowed": True,
            "backtest_allowed": True,
            "report_allowed": True,
            "ingestion_allowed": True,
        })
        p = store.get_provider_profile("test_twse")
        assert p is not None
        assert p["provider_id"] == "test_twse"
        store.close()
        return (_PASS, "Store memory mode functional")

    def _check_audit_append_only(self) -> Tuple[str, str]:
        from data.governance.quality.audit_v146 import QualityDecisionAuditService
        from data.governance.quality.decision_engine_v146 import QualityDecisionEngine
        from data.governance.quality.models_v146 import QualityScope
        svc = QualityDecisionAuditService()
        eng = QualityDecisionEngine()
        d = eng.decide(QualityScope.PROVIDER.value, "twse", [])
        a1 = svc.record(d, provider_id="twse")
        a2 = svc.record(d, provider_id="twse")
        assert len(svc.list_all()) == 2
        return (_PASS, "Audit service is append-only")

    def _check_dataset_not_allowlisted_blocked(self) -> Tuple[str, str]:
        from data.governance.quality.dataset_gate_v146 import DatasetAdmissionGate
        gate = DatasetAdmissionGate()
        profile = gate.evaluate("unknown_dataset", "unknown_provider", {})
        assert not profile.admitted
        assert len(profile.blocking_failures) > 0
        return (_PASS, "Non-allowlisted dataset → BLOCKED")

    def _check_future_leakage_blocked(self) -> Tuple[str, str]:
        from data.governance.quality.backtest_gate_v146 import BacktestInputEligibilityGate
        gate = BacktestInputEligibilityGate()
        result = gate.evaluate("p", "d", {"future_leakage": True, "pit_available": True,
                                          "revision_frozen": True, "authority_level": "PRIMARY_OFFICIAL"})
        assert not result.eligible
        assert any("future_leakage" in f for f in result.blocking_failures)
        return (_PASS, "Future leakage → BLOCKED")

    def _check_schema_breaking_blocked(self) -> Tuple[str, str]:
        from data.governance.quality.schema_gate_v146 import SchemaDriftGate
        from data.governance.models_v145 import SchemaDriftStatus
        gate = SchemaDriftGate()
        result = gate.evaluate("dataset", {
            "schema_drift_status": SchemaDriftStatus.BREAKING_MISSING_FIELD.value
        })
        assert result.status == "BLOCKED"
        return (_PASS, "Breaking schema drift → BLOCKED")

    def _check_mock_authority_blocked_formal(self) -> Tuple[str, str]:
        from data.governance.quality.authority_gate_v146 import AuthorityGate
        gate = AuthorityGate()
        result = gate.evaluate("mock_provider", {
            "provider_id": "mock",
            "formal_use": True,
        })
        assert result.status in ("BLOCKED", "FAIL"), f"Expected BLOCKED/FAIL, got {result.status}"
        return (_PASS, "Mock authority blocked from formal use")

    def _check_freshness_unknown_not_pass(self) -> Tuple[str, str]:
        from data.governance.quality.freshness_gate_v146 import FreshnessGate
        gate = FreshnessGate()
        result = gate.evaluate("dataset", {"freshness_status": "UNKNOWN"})
        assert result.status != "PASS", f"UNKNOWN freshness should not PASS, got {result.status}"
        return (_PASS, "UNKNOWN freshness → not PASS")

    # ------------------------------------------------------------------
    # Safety invariants
    # ------------------------------------------------------------------

    def _check_safety_no_real_orders(self) -> Tuple[str, str]:
        from data.governance.quality import NO_REAL_ORDERS as _NRO
        assert _NRO is True
        return (_PASS, "NO_REAL_ORDERS = True")

    def _check_safety_broker_disabled(self) -> Tuple[str, str]:
        from data.governance.quality import BROKER_EXECUTION_ENABLED as _BEE
        assert _BEE is False
        return (_PASS, "BROKER_EXECUTION_ENABLED = False")

    def _check_safety_production_blocked(self) -> Tuple[str, str]:
        from data.governance.quality import PRODUCTION_TRADING_BLOCKED as _PTB
        assert _PTB is True
        return (_PASS, "PRODUCTION_TRADING_BLOCKED = True")

    def _check_safety_score_no_override(self) -> Tuple[str, str]:
        from data.governance.quality import QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE as _QSCO
        assert _QSCO is False
        return (_PASS, "QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False")

    def _check_safety_no_auto_promotion(self) -> Tuple[str, str]:
        from data.governance.quality import AUTO_PROVIDER_PROMOTION_ENABLED as _APE
        assert _APE is False
        return (_PASS, "AUTO_PROVIDER_PROMOTION_ENABLED = False")

    def _check_safety_no_auto_release(self) -> Tuple[str, str]:
        from data.governance.quality import AUTO_QUARANTINE_RELEASE_ENABLED as _AQR
        assert _AQR is False
        return (_PASS, "AUTO_QUARANTINE_RELEASE_ENABLED = False")

    def _check_safety_no_mock_fallback(self) -> Tuple[str, str]:
        from data.governance.quality import MOCK_FALLBACK_ENABLED as _MFE
        assert _MFE is False
        return (_PASS, "MOCK_FALLBACK_ENABLED = False")

    def _check_safety_no_primary_override(self) -> Tuple[str, str]:
        from data.governance.quality import AUTO_PRIMARY_OVERRIDE_ENABLED as _APO
        assert _APO is False
        return (_PASS, "AUTO_PRIMARY_OVERRIDE_ENABLED = False")

    def _check_safety_no_rate_bypass(self) -> Tuple[str, str]:
        from data.governance.quality import AUTO_RATE_LIMIT_BYPASS_ENABLED as _ARBE
        assert _ARBE is False
        return (_PASS, "AUTO_RATE_LIMIT_BYPASS_ENABLED = False")

    def _check_safety_gate_invariants(self) -> Tuple[str, str]:
        from data.governance.quality.safety_gate_v146 import SafetyGate
        gate = SafetyGate()
        result = gate.evaluate("self_test")
        assert result.status == "PASS", f"Safety gate self-test failed: {result.evidence}"
        return (_PASS, "Safety gate self-test PASS")

    # ------------------------------------------------------------------
    # v1.4.5 integration
    # ------------------------------------------------------------------

    def _check_v145_authority_integration(self) -> Tuple[str, str]:
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert reg.get_authority("twse") == SourceAuthorityLevel.PRIMARY_OFFICIAL
        assert not reg.can_override(SourceAuthorityLevel.SECONDARY_AGGREGATOR,
                                     SourceAuthorityLevel.PRIMARY_OFFICIAL)
        return (_PASS, "v1.4.5 SourceAuthorityRegistry accessible")

    def _check_v145_provenance_integration(self) -> Tuple[str, str]:
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        assert gate is not None
        return (_PASS, "v1.4.5 ProvenanceCompletenessGate accessible")

    def _check_v145_conflict_integration(self) -> Tuple[str, str]:
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        assert svc.list_blocking_conflicts() == []
        return (_PASS, "v1.4.5 ConflictLineageService accessible")

    # ------------------------------------------------------------------
    # CLI and GUI
    # ------------------------------------------------------------------

    def _check_cli_registration(self) -> Tuple[str, str]:
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "provider-quality-health" in names, "provider-quality-health not registered"
        assert "provider-quality-gates" in names, "provider-quality-gates not registered"
        return (_PASS, "provider_quality_gates CLI commands registered")

    def _check_gui_import(self) -> Tuple[str, str]:
        try:
            from gui.provider_quality_gates_panel import ProviderQualityGatesPanel
            return (_PASS, "provider_quality_gates_panel importable")
        except Exception as e:
            return (_WARN, f"GUI panel not importable (may require tkinter): {e}")
