"""
tests/test_provider_quality_gates_v146.py — Provider Quality Gates Tests v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All tests are offline. No real HTTP calls. Temp SQLite for storage tests.
181 tests across 16+ test classes.
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure project root is on path
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


# ===========================================================================
# CLASS 1: Safety Invariant Constants
# ===========================================================================
class TestSafetyInvariants(unittest.TestCase):
    """Tests that all safety constants are correctly set across the quality package."""

    def test_package_no_real_orders(self):
        from data.governance.quality import NO_REAL_ORDERS as v
        self.assertTrue(v)

    def test_package_broker_execution_disabled(self):
        from data.governance.quality import BROKER_EXECUTION_ENABLED as v
        self.assertFalse(v)

    def test_package_production_trading_blocked(self):
        from data.governance.quality import PRODUCTION_TRADING_BLOCKED as v
        self.assertTrue(v)

    def test_quality_score_cannot_override_blocking(self):
        from data.governance.quality import QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE as v
        self.assertFalse(v)

    def test_auto_provider_promotion_disabled(self):
        from data.governance.quality import AUTO_PROVIDER_PROMOTION_ENABLED as v
        self.assertFalse(v)

    def test_auto_quarantine_release_disabled(self):
        from data.governance.quality import AUTO_QUARANTINE_RELEASE_ENABLED as v
        self.assertFalse(v)

    def test_mock_fallback_disabled(self):
        from data.governance.quality import MOCK_FALLBACK_ENABLED as v
        self.assertFalse(v)

    def test_auto_primary_override_disabled(self):
        from data.governance.quality import AUTO_PRIMARY_OVERRIDE_ENABLED as v
        self.assertFalse(v)

    def test_silent_provider_fallback_disabled(self):
        from data.governance.quality import SILENT_PROVIDER_FALLBACK_ENABLED as v
        self.assertFalse(v)


# ===========================================================================
# CLASS 2: Models — Enums
# ===========================================================================
class TestModelsEnums(unittest.TestCase):
    """Tests for enums in models_v146.py."""

    def test_provider_quality_state_enum_values(self):
        from data.governance.quality.models_v146 import ProviderQualityState
        values = [s.value for s in ProviderQualityState]
        for expected in ["ACTIVE", "BLOCKED", "QUARANTINED", "DEGRADED", "RESTRICTED",
                         "DISABLED", "UNKNOWN"]:
            self.assertIn(expected, values)

    def test_gate_status_enum_values(self):
        from data.governance.quality.models_v146 import GateStatus
        values = [s.value for s in GateStatus]
        for expected in ["PASS", "WARN", "FAIL", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"]:
            self.assertIn(expected, values)

    def test_quality_decision_result_enum(self):
        from data.governance.quality.models_v146 import QualityDecisionResult
        values = [s.value for s in QualityDecisionResult]
        for expected in ["ALLOW", "BLOCK", "ALLOW_WITH_WARNING", "RESTRICT", "QUARANTINE"]:
            self.assertIn(expected, values)

    def test_quality_scope_enum(self):
        from data.governance.quality.models_v146 import QualityScope
        values = [s.value for s in QualityScope]
        for expected in ["PROVIDER", "DATASET", "BATCH", "BACKTEST_INPUT", "REPORT_SECTION"]:
            self.assertIn(expected, values)

    def test_freshness_status_has_unknown(self):
        from data.governance.quality.models_v146 import FreshnessStatus
        self.assertIn("UNKNOWN", [s.value for s in FreshnessStatus])

    def test_coverage_status_enum(self):
        from data.governance.quality.models_v146 import CoverageStatus
        values = [s.value for s in CoverageStatus]
        self.assertIn("COMPLETE", values)
        self.assertIn("INSUFFICIENT", values)

    def test_operational_readiness_enum(self):
        from data.governance.quality.models_v146 import OperationalReadiness
        values = [s.value for s in OperationalReadiness]
        self.assertIn("READY", values)
        self.assertIn("QUOTA_EXHAUSTED", values)


# ===========================================================================
# CLASS 3: Models — QualityDecision
# ===========================================================================
class TestModelsQualityDecision(unittest.TestCase):

    def test_score_overrode_blocking_raises(self):
        """score_overrode_blocking=True must raise ValueError."""
        from data.governance.quality.models_v146 import QualityDecision
        with self.assertRaises(ValueError):
            QualityDecision(
                decision_id="d1", scope="PROVIDER", subject_id="test",
                decision="BLOCK", quality_state="BLOCKED",
                formal_research_allowed=False, backtest_allowed=False,
                report_allowed=False, ingestion_allowed=False,
                blocking_failures=[], warnings=[], gate_results=[],
                quality_score=None, score_overrode_blocking=True,
            )

    def test_blocking_failures_with_formal_allowed_raises(self):
        """Blocking failures present with formal_research_allowed=True must raise."""
        from data.governance.quality.models_v146 import QualityDecision
        with self.assertRaises(ValueError):
            QualityDecision(
                decision_id="d2", scope="PROVIDER", subject_id="test",
                decision="ALLOW", quality_state="ACTIVE",
                formal_research_allowed=True, backtest_allowed=False,
                report_allowed=False, ingestion_allowed=False,
                blocking_failures=["some_failure"], warnings=[], gate_results=[],
                quality_score=90, score_overrode_blocking=False,
            )

    def test_valid_allow_decision(self):
        from data.governance.quality.models_v146 import QualityDecision
        d = QualityDecision(
            decision_id="d3", scope="PROVIDER", subject_id="twse_official",
            decision="ALLOW", quality_state="ACTIVE",
            formal_research_allowed=True, backtest_allowed=True,
            report_allowed=True, ingestion_allowed=True,
            blocking_failures=[], warnings=[], gate_results=[],
            quality_score=88, score_overrode_blocking=False,
        )
        self.assertEqual(d.decision, "ALLOW")
        self.assertTrue(d.formal_research_allowed)

    def test_valid_block_decision(self):
        from data.governance.quality.models_v146 import QualityDecision
        d = QualityDecision(
            decision_id="d4", scope="PROVIDER", subject_id="bad_provider",
            decision="BLOCK", quality_state="BLOCKED",
            formal_research_allowed=False, backtest_allowed=False,
            report_allowed=False, ingestion_allowed=False,
            blocking_failures=["not_registered"], warnings=[], gate_results=[],
            quality_score=10, score_overrode_blocking=False,
        )
        self.assertFalse(d.formal_research_allowed)
        self.assertFalse(d.score_overrode_blocking)

    def test_to_dict_contains_score_override_false(self):
        from data.governance.quality.models_v146 import QualityDecision
        d = QualityDecision(
            decision_id="d5", scope="PROVIDER", subject_id="twse_official",
            decision="ALLOW", quality_state="ACTIVE",
            formal_research_allowed=True, backtest_allowed=True,
            report_allowed=True, ingestion_allowed=True,
            blocking_failures=[], warnings=[], gate_results=[],
            quality_score=88, score_overrode_blocking=False,
        )
        dct = d.to_dict()
        self.assertFalse(dct["score_overrode_blocking"])


# ===========================================================================
# CLASS 4: Models — QuarantineRecord
# ===========================================================================
class TestModelsQuarantineRecord(unittest.TestCase):

    def test_auto_release_true_raises(self):
        from data.governance.quality.models_v146 import QuarantineRecord
        with self.assertRaises(ValueError):
            QuarantineRecord(
                quarantine_id="qr1", provider_id="finmind",
                reason="test", triggered_by_gate="safety_gate",
                quarantined_at="2026-01-01T00:00:00Z",
                auto_release_allowed=True,
            )

    def test_auto_release_false_valid(self):
        from data.governance.quality.models_v146 import QuarantineRecord
        r = QuarantineRecord(
            quarantine_id="qr2", provider_id="finmind",
            reason="test", triggered_by_gate="safety_gate",
            quarantined_at="2026-01-01T00:00:00Z",
            auto_release_allowed=False,
        )
        self.assertFalse(r.auto_release_allowed)

    def test_to_dict_always_false_auto_release(self):
        from data.governance.quality.models_v146 import QuarantineRecord
        r = QuarantineRecord(
            quarantine_id="qr3", provider_id="finmind",
            reason="test", triggered_by_gate="safety_gate",
            quarantined_at="2026-01-01T00:00:00Z",
        )
        self.assertFalse(r.to_dict()["auto_release_allowed"])


# ===========================================================================
# CLASS 5: Models — QualityScore
# ===========================================================================
class TestModelsQualityScore(unittest.TestCase):

    def test_can_override_blocking_true_raises(self):
        from data.governance.quality.models_v146 import QualityScore
        with self.assertRaises(ValueError):
            QualityScore(
                score=90, provider_id="test", subject_id="test",
                can_override_blocking=True,
            )

    def test_can_override_blocking_false_valid(self):
        from data.governance.quality.models_v146 import QualityScore
        s = QualityScore(score=88, provider_id="twse_official", subject_id="twse_official")
        self.assertFalse(s.can_override_blocking)

    def test_score_clamped_to_100(self):
        from data.governance.quality.models_v146 import QualityScore
        s = QualityScore(score=150, provider_id="t", subject_id="t")
        self.assertEqual(s.score, 100.0)

    def test_score_clamped_to_0(self):
        from data.governance.quality.models_v146 import QualityScore
        s = QualityScore(score=-10, provider_id="t", subject_id="t")
        self.assertEqual(s.score, 0.0)


# ===========================================================================
# CLASS 6: Models — QualityDecisionAudit
# ===========================================================================
class TestModelsAudit(unittest.TestCase):

    def test_compute_evidence_hash_returns_hex(self):
        hash_val = __import__("data.governance.quality.models_v146", fromlist=["QualityDecisionAudit"]).QualityDecisionAudit.compute_evidence_hash(
            decision_id="d1", decision="ALLOW",
            blocking_failures=[], audited_at="2026-01-01T00:00:00Z"
        )
        self.assertIsInstance(hash_val, str)
        self.assertEqual(len(hash_val), 64)

    def test_compute_evidence_hash_deterministic(self):
        from data.governance.quality.models_v146 import QualityDecisionAudit
        h1 = QualityDecisionAudit.compute_evidence_hash(
            "d1", "ALLOW", ["gate_x"], "2026-01-01T00:00:00Z"
        )
        h2 = QualityDecisionAudit.compute_evidence_hash(
            "d1", "ALLOW", ["gate_x"], "2026-01-01T00:00:00Z"
        )
        self.assertEqual(h1, h2)

    def test_compute_evidence_hash_varies_with_input(self):
        from data.governance.quality.models_v146 import QualityDecisionAudit
        h1 = QualityDecisionAudit.compute_evidence_hash(
            "d1", "ALLOW", [], "2026-01-01T00:00:00Z"
        )
        h2 = QualityDecisionAudit.compute_evidence_hash(
            "d2", "BLOCK", ["gate_x"], "2026-01-02T00:00:00Z"
        )
        self.assertNotEqual(h1, h2)


# ===========================================================================
# CLASS 7: Gate Registry
# ===========================================================================
class TestGateRegistry(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.gate_registry_v146 import QualityGateRegistry
        self.reg = QualityGateRegistry()

    def test_list_gates_non_empty(self):
        gates = self.reg.list_gates()
        self.assertGreater(len(gates), 0)

    def test_list_mandatory_gates_non_empty(self):
        mandatory = self.reg.list_mandatory_gates()
        self.assertGreater(len(mandatory), 0)

    def test_get_policy_version(self):
        ver = self.reg.get_policy_version()
        self.assertIn("1.4.6", ver)

    def test_validate_registry_valid(self):
        result = self.reg.validate_registry()
        self.assertTrue(result["valid"], msg=str(result))

    def _get_gate_id(self, gate):
        return gate.gate_id if hasattr(gate, "gate_id") else gate["gate_id"]

    def test_registry_has_safety_gate(self):
        gate_ids = [self._get_gate_id(g) for g in self.reg.list_gates()]
        self.assertIn("safety_invariants", gate_ids)

    def test_registry_has_freshness_gate(self):
        gate_ids = [self._get_gate_id(g) for g in self.reg.list_gates()]
        self.assertIn("freshness", gate_ids)

    def test_registry_has_pit_gate(self):
        gate_ids = [self._get_gate_id(g) for g in self.reg.list_gates()]
        self.assertIn("point_in_time", gate_ids)

    def test_registry_has_authority_gate(self):
        gate_ids = [self._get_gate_id(g) for g in self.reg.list_gates()]
        self.assertIn("authority_hierarchy", gate_ids)

    def test_mandatory_gates_subset_of_all(self):
        all_ids = {self._get_gate_id(g) for g in self.reg.list_gates()}
        mandatory_ids = {self._get_gate_id(g) for g in self.reg.list_mandatory_gates()}
        self.assertTrue(mandatory_ids.issubset(all_ids))

    def test_no_duplicate_gate_ids(self):
        gates = self.reg.list_gates()
        ids = [self._get_gate_id(g) for g in gates]
        self.assertEqual(len(ids), len(set(ids)))


# ===========================================================================
# CLASS 8: Decision Engine
# ===========================================================================
class TestDecisionEngine(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.decision_engine_v146 import QualityDecisionEngine
        from data.governance.quality.models_v146 import QualityGateResult, GateStatus
        self.engine = QualityDecisionEngine()
        self.GateStatus = GateStatus
        self.QualityGateResult = QualityGateResult

    def _make_result(self, gate_id, status, blocking=False):
        return self.QualityGateResult(
            gate_id=gate_id, gate_name=gate_id, scope="PROVIDER",
            subject_id="test", status=status, passed=(status == "PASS"),
            blocking=blocking, evidence="", evaluated_at="",
        )

    def test_blocking_gate_produces_block(self):
        gate_results = [
            self._make_result("pit_gate", self.GateStatus.BLOCKED.value, blocking=True),
        ]
        decision = self.engine.decide("PROVIDER", "test_provider", gate_results, quality_score=95)
        self.assertEqual(decision.decision, "BLOCK")
        self.assertFalse(decision.formal_research_allowed)
        self.assertFalse(decision.backtest_allowed)

    def test_score_does_not_override_blocking(self):
        gate_results = [
            self._make_result("safety_gate", self.GateStatus.BLOCKED.value, blocking=True),
        ]
        decision = self.engine.decide("PROVIDER", "test_provider", gate_results, quality_score=99)
        self.assertEqual(decision.decision, "BLOCK")
        self.assertFalse(decision.score_overrode_blocking)

    def test_all_pass_allows(self):
        gate_results = [
            self._make_result("freshness_gate", self.GateStatus.PASS.value),
            self._make_result("coverage_gate", self.GateStatus.PASS.value),
        ]
        decision = self.engine.decide("PROVIDER", "twse_official", gate_results, quality_score=85)
        self.assertIn(decision.decision, ["ALLOW", "ALLOW_WITH_WARNING"])

    def test_warn_produces_allow_with_warning(self):
        gate_results = [
            self._make_result("coverage_gate", self.GateStatus.WARN.value),
        ]
        decision = self.engine.decide("PROVIDER", "twse_official", gate_results, quality_score=72)
        self.assertEqual(decision.decision, "ALLOW_WITH_WARNING")
        self.assertFalse(decision.score_overrode_blocking)

    def test_blocking_failures_always_false_score_override(self):
        gate_results = [
            self._make_result("safety_gate", self.GateStatus.BLOCKED.value, blocking=True),
        ]
        decision = self.engine.decide("PROVIDER", "provider", gate_results, quality_score=100)
        self.assertFalse(decision.score_overrode_blocking)


# ===========================================================================
# CLASS 9: Provider Gate
# ===========================================================================
class TestProviderGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.provider_gate_v146 import ProviderOperationalGate
        self.gate = ProviderOperationalGate()

    def test_twse_is_active(self):
        profile = self.gate.evaluate("twse_official")
        self.assertEqual(profile.quality_state, "ACTIVE")

    def test_tpex_is_active(self):
        profile = self.gate.evaluate("tpex_official")
        self.assertEqual(profile.quality_state, "ACTIVE")

    def test_mops_is_active(self):
        profile = self.gate.evaluate("mops_official")
        self.assertEqual(profile.quality_state, "ACTIVE")

    def test_unknown_provider_is_blocked(self):
        profile = self.gate.evaluate("unknown_xyz_provider_999")
        self.assertEqual(profile.quality_state, "BLOCKED")

    def test_twse_allows_formal_research(self):
        profile = self.gate.evaluate("twse_official")
        self.assertTrue(profile.formal_research_allowed)

    def test_unknown_provider_blocks_formal_research(self):
        profile = self.gate.evaluate("unknown_xyz_provider_999")
        self.assertFalse(profile.formal_research_allowed)

    def test_profile_has_authority_level(self):
        profile = self.gate.evaluate("twse_official")
        self.assertIsNotNone(profile.authority_level)
        self.assertNotEqual(profile.authority_level, "")

    def test_profile_to_dict(self):
        profile = self.gate.evaluate("twse_official")
        d = profile.to_dict()
        self.assertIn("provider_id", d)
        self.assertIn("quality_state", d)
        self.assertIn("authority_level", d)

    def test_twse_has_gate_results(self):
        profile = self.gate.evaluate("twse_official")
        self.assertIsInstance(profile.gate_results, list)
        self.assertGreater(len(profile.gate_results), 0)


# ===========================================================================
# CLASS 10: Dataset Gate
# ===========================================================================
class TestDatasetGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.dataset_gate_v146 import DatasetAdmissionGate
        self.gate = DatasetAdmissionGate()

    def test_unknown_dataset_not_admitted(self):
        result = self.gate.evaluate("unknown_dataset_xyz_999", "unknown_provider")
        self.assertFalse(result.admitted)

    def test_unknown_dataset_not_formal_use(self):
        result = self.gate.evaluate("unknown_dataset_xyz_999", "unknown_provider")
        self.assertFalse(result.formal_use_allowed)

    def test_unknown_dataset_has_blocking_failures(self):
        result = self.gate.evaluate("unknown_dataset_xyz_999", "unknown_provider")
        self.assertGreater(len(result.blocking_failures), 0)

    def test_dataset_result_has_provider_id(self):
        result = self.gate.evaluate("twse_daily_prices", "twse_official")
        self.assertEqual(result.provider_id, "twse_official")

    def test_dataset_result_has_dataset_id(self):
        result = self.gate.evaluate("twse_daily_prices", "twse_official")
        self.assertEqual(result.dataset_id, "twse_daily_prices")


# ===========================================================================
# CLASS 11: Freshness Gate
# ===========================================================================
class TestFreshnessGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.freshness_gate_v146 import FreshnessGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = FreshnessGate()
        self.GateStatus = GateStatus

    def test_fresh_data_passes(self):
        result = self.gate.evaluate("twse_official", context={"freshness_status": "FRESH"})
        self.assertEqual(result.status, self.GateStatus.PASS.value)

    def test_stale_data_fails(self):
        result = self.gate.evaluate("twse_official", context={"freshness_status": "STALE"})
        self.assertEqual(result.status, self.GateStatus.FAIL.value)

    def test_quota_exhausted_is_not_fail(self):
        """quota_exhausted must not produce FAIL — data is not stale."""
        result = self.gate.evaluate("twse_official", context={
            "freshness_status": "FRESH", "quota_exhausted": True
        })
        self.assertNotEqual(result.status, self.GateStatus.FAIL.value)

    def test_rate_limited_is_not_fail(self):
        """rate_limited must not produce FAIL."""
        result = self.gate.evaluate("twse_official", context={
            "freshness_status": "FRESH", "rate_limited": True
        })
        self.assertNotEqual(result.status, self.GateStatus.FAIL.value)

    def test_unknown_freshness_is_not_pass(self):
        """UNKNOWN freshness must NOT be PASS."""
        result = self.gate.evaluate("twse_official", context={"freshness_status": "UNKNOWN"})
        self.assertNotEqual(result.status, self.GateStatus.PASS.value)

    def test_unknown_freshness_is_fail(self):
        result = self.gate.evaluate("twse_official", context={"freshness_status": "UNKNOWN"})
        self.assertEqual(result.status, self.GateStatus.FAIL.value)

    def test_result_has_gate_id(self):
        result = self.gate.evaluate("twse_official", context={"freshness_status": "FRESH"})
        self.assertIsNotNone(result.gate_id)


# ===========================================================================
# CLASS 12: Coverage Gate
# ===========================================================================
class TestCoverageGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.coverage_gate_v146 import CoverageGate, _PASS_PCT, _BACKTEST_PASS_PCT
        from data.governance.quality.models_v146 import GateStatus
        self.gate = CoverageGate()
        self.GateStatus = GateStatus
        self.pass_pct = _PASS_PCT
        self.backtest_pct = _BACKTEST_PASS_PCT

    def test_high_coverage_passes(self):
        result = self.gate.evaluate("twse_official", context={"coverage_pct": 0.99})
        self.assertEqual(result.status, self.GateStatus.PASS.value)

    def test_low_coverage_fails(self):
        result = self.gate.evaluate("twse_official", context={"coverage_pct": 0.70})
        self.assertEqual(result.status, self.GateStatus.FAIL.value)

    def test_backtest_pass_threshold_stricter_than_normal(self):
        self.assertGreater(self.backtest_pct, self.pass_pct)

    def test_coverage_below_backtest_threshold_warns_or_fails(self):
        # below backtest threshold (0.98) but above normal (0.95)
        result = self.gate.evaluate("twse_official", context={
            "coverage_pct": 0.96, "is_backtest": True
        })
        self.assertIn(result.status, [
            self.GateStatus.WARN.value, self.GateStatus.FAIL.value
        ])

    def test_full_coverage_passes_normal(self):
        result = self.gate.evaluate("twse_official", context={"coverage_pct": 0.99})
        self.assertEqual(result.status, self.GateStatus.PASS.value)

    def test_full_coverage_passes_backtest(self):
        result = self.gate.evaluate("twse_official", context={
            "coverage_pct": 0.99, "is_backtest": True
        })
        self.assertEqual(result.status, self.GateStatus.PASS.value)


# ===========================================================================
# CLASS 13: PIT Gate
# ===========================================================================
class TestPITGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.pit_gate_v146 import PointInTimeGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = PointInTimeGate()
        self.GateStatus = GateStatus

    def test_no_leakage_no_block(self):
        result = self.gate.evaluate("twse_official", context={
            "pit_available": True, "revision_frozen": True,
            "future_leakage": False, "lookahead_leakage": False
        })
        self.assertNotEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_future_leakage_blocked(self):
        result = self.gate.evaluate("twse_official", context={"future_leakage": True})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_lookahead_leakage_warns_or_blocks(self):
        """lookahead_leakage may produce WARN or BLOCKED depending on implementation."""
        result = self.gate.evaluate("twse_official", context={"lookahead_leakage": True})
        self.assertIn(result.status, [self.GateStatus.BLOCKED.value, self.GateStatus.WARN.value])

    def test_future_leakage_is_blocking(self):
        result = self.gate.evaluate("twse_official", context={"future_leakage": True})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)
        self.assertTrue(result.blocking)

    def test_no_pit_not_pass(self):
        """No PASS when pit_available=False."""
        result = self.gate.evaluate("twse_official", context={
            "pit_available": False, "revision_frozen": False,
            "future_leakage": False, "lookahead_leakage": False
        })
        self.assertNotEqual(result.status, self.GateStatus.PASS.value)


# ===========================================================================
# CLASS 14: Schema Gate
# ===========================================================================
class TestSchemaGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.schema_gate_v146 import SchemaDriftGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = SchemaDriftGate()
        self.GateStatus = GateStatus

    def test_no_change_passes(self):
        result = self.gate.evaluate("twse_official", context={"schema_drift_status": "NO_CHANGE"})
        self.assertEqual(result.status, self.GateStatus.PASS.value)

    def test_additive_warns(self):
        result = self.gate.evaluate("twse_official", context={"schema_drift_status": "ADDITIVE"})
        self.assertEqual(result.status, self.GateStatus.WARN.value)

    def test_breaking_removal_blocked(self):
        result = self.gate.evaluate("twse_official", context={"schema_drift_status": "BREAKING_MISSING_FIELD"})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_breaking_type_change_blocked(self):
        result = self.gate.evaluate("twse_official", context={"schema_drift_status": "BREAKING_TYPE_CHANGE"})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_breaking_key_change_blocked(self):
        result = self.gate.evaluate("twse_official", context={"schema_drift_status": "BREAKING_KEY_CHANGE"})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_unknown_fails(self):
        result = self.gate.evaluate("twse_official", context={"schema_drift_status": "UNKNOWN"})
        self.assertEqual(result.status, self.GateStatus.FAIL.value)

    def test_no_context_defaults_to_unknown_fail(self):
        result = self.gate.evaluate("twse_official")
        self.assertEqual(result.status, self.GateStatus.FAIL.value)


# ===========================================================================
# CLASS 15: Authority Gate
# ===========================================================================
class TestAuthorityGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.authority_gate_v146 import AuthorityGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = AuthorityGate()
        self.GateStatus = GateStatus

    def test_known_provider_returns_result(self):
        result = self.gate.evaluate("twse_official")
        self.assertIsNotNone(result.status)

    def test_secondary_override_of_primary_fails_for_formal(self):
        result = self.gate.evaluate("twse_official", context={
            "challenger_authority_level": "SECONDARY_AGGREGATOR",
            "incumbent_authority_level": "PRIMARY_OFFICIAL",
            "formal_use": True,
        })
        self.assertIn(result.status, [
            self.GateStatus.FAIL.value, self.GateStatus.BLOCKED.value
        ])

    def test_mock_authority_blocked_for_formal(self):
        """Provider with MOCK authority is blocked for formal use."""
        result = self.gate.evaluate("mock_provider_xyz", context={"formal_use": True})
        # MOCK provider is unknown, which also maps to blocked
        self.assertIn(result.status, [
            self.GateStatus.BLOCKED.value, self.GateStatus.FAIL.value
        ])

    def test_no_formal_use_passes(self):
        result = self.gate.evaluate("twse_official", context={"formal_use": False})
        self.assertEqual(result.status, self.GateStatus.PASS.value)


# ===========================================================================
# CLASS 16: Conflict Gate
# ===========================================================================
class TestConflictGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.conflict_gate_v146 import ConflictGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = ConflictGate()
        self.GateStatus = GateStatus

    def test_no_conflicts_passes(self):
        result = self.gate.evaluate("twse_official", context={"conflicts": []})
        self.assertEqual(result.status, self.GateStatus.PASS.value)

    def test_within_tolerance_warns(self):
        result = self.gate.evaluate("twse_official", context={"conflicts": [
            {"conflict_type": "WITHIN_TOLERANCE", "reviewed": False, "formal_use_blocked": True,
             "conflict_id": "c1"}
        ]})
        self.assertEqual(result.status, self.GateStatus.WARN.value)

    def test_unresolved_value_conflict_blocked(self):
        result = self.gate.evaluate("twse_official", context={"conflicts": [
            {"conflict_type": "VALUE_CONFLICT", "reviewed": False, "formal_use_blocked": True,
             "conflict_id": "c2"}
        ]})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_reviewed_value_conflict_not_blocked(self):
        result = self.gate.evaluate("twse_official", context={"conflicts": [
            {"conflict_type": "VALUE_CONFLICT", "reviewed": True, "formal_use_blocked": False,
             "conflict_id": "c3"}
        ]})
        self.assertNotEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_date_conflict_fails(self):
        result = self.gate.evaluate("twse_official", context={"conflicts": [
            {"conflict_type": "DATE_CONFLICT", "reviewed": False, "formal_use_blocked": True,
             "conflict_id": "c4"}
        ]})
        self.assertIn(result.status, [self.GateStatus.FAIL.value, self.GateStatus.BLOCKED.value])


# ===========================================================================
# CLASS 17: Quality Score
# ===========================================================================
class TestQualityScore(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.score_v146 import QualityScoreEngine, _DEFAULT_WEIGHTS
        from data.governance.quality.models_v146 import QualityGateResult, GateStatus
        self.engine = QualityScoreEngine()
        self.weights = _DEFAULT_WEIGHTS
        self.GateStatus = GateStatus
        self.QualityGateResult = QualityGateResult

    def _make_result(self, gate_id, status, passed=True):
        return self.QualityGateResult(
            gate_id=gate_id, gate_name=gate_id, scope="DATASET",
            subject_id="twse_official", status=status, passed=passed,
            blocking=False, evidence="", evaluated_at="",
        )

    def test_weights_sum_to_100(self):
        total = sum(self.weights.values())
        self.assertEqual(total, 100)

    def test_weight_data_quality(self):
        self.assertEqual(self.weights.get("data_quality"), 20)

    def test_weight_freshness(self):
        self.assertEqual(self.weights.get("freshness"), 15)

    def test_weight_coverage(self):
        self.assertEqual(self.weights.get("coverage"), 15)

    def test_weight_provenance(self):
        self.assertEqual(self.weights.get("provenance"), 15)

    def test_weight_pit(self):
        self.assertEqual(self.weights.get("pit"), 10)

    def test_weight_schema(self):
        self.assertEqual(self.weights.get("schema"), 10)

    def test_weight_authority_conflict(self):
        self.assertEqual(self.weights.get("authority_conflict"), 10)

    def test_weight_operational(self):
        self.assertEqual(self.weights.get("operational"), 5)

    def test_score_cannot_override_blocking(self):
        gate_results = [
            self._make_result("freshness", self.GateStatus.PASS.value),
        ]
        score = self.engine.compute("twse_official", "twse_official", gate_results)
        self.assertFalse(score.can_override_blocking)

    def test_score_in_valid_range(self):
        gate_results = [
            self._make_result("freshness", self.GateStatus.PASS.value),
        ]
        score = self.engine.compute("twse_official", "twse_official", gate_results)
        self.assertGreaterEqual(score.score, 0)
        self.assertLessEqual(score.score, 100)


# ===========================================================================
# CLASS 18: Safety Gate
# ===========================================================================
class TestSafetyGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.safety_gate_v146 import SafetyGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = SafetyGate()
        self.GateStatus = GateStatus

    def test_clean_context_passes(self):
        result = self.gate.evaluate("twse_official", context={})
        self.assertEqual(result.status, self.GateStatus.PASS.value)

    def test_token_in_plaintext_blocks(self):
        result = self.gate.evaluate("twse_official", context={"token_in_plaintext": True})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_auth_header_stored_blocks(self):
        result = self.gate.evaluate("twse_official", context={"auth_header_stored": True})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_rate_bypass_blocks(self):
        result = self.gate.evaluate("twse_official", context={"rate_bypass": True})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_has_broker_blocks(self):
        result = self.gate.evaluate("twse_official", context={"has_broker": True})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_has_orders_blocks(self):
        result = self.gate.evaluate("twse_official", context={"has_orders": True})
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_module_safety_invariants_pass(self):
        """Module-level invariants must all pass."""
        result = self.gate.evaluate("twse_official", context={})
        self.assertEqual(result.status, self.GateStatus.PASS.value)


# ===========================================================================
# CLASS 19: Rate Limit Gate
# ===========================================================================
class TestRateLimitGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.rate_limit_gate_v146 import RateLimitReadinessGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = RateLimitReadinessGate()
        self.GateStatus = GateStatus

    def test_unknown_policy_large_batch_blocked(self):
        result = self.gate.evaluate("unknown_provider", context={
            "policy_known": False, "request_count": 100
        })
        self.assertEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_unknown_policy_small_query_not_blocked(self):
        result = self.gate.evaluate("unknown_provider", context={
            "policy_known": False, "request_count": 5
        })
        self.assertNotEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_known_policy_returns_result(self):
        result = self.gate.evaluate("twse_official", context={
            "policy_known": True, "request_count": 5
        })
        self.assertIsNotNone(result.status)


# ===========================================================================
# CLASS 20: Quota Gate
# ===========================================================================
class TestQuotaGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.quota_gate_v146 import QuotaReadinessGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = QuotaReadinessGate()
        self.GateStatus = GateStatus

    def test_quota_available_not_blocked(self):
        result = self.gate.evaluate("twse_official", context={"quota_exhausted": False})
        self.assertNotEqual(result.status, self.GateStatus.BLOCKED.value)

    def test_quota_exhausted_blocks_new_fetch(self):
        result = self.gate.evaluate("finmind", context={"quota_exhausted": True})
        self.assertIn(result.status, [self.GateStatus.BLOCKED.value, self.GateStatus.FAIL.value])

    def test_quota_exhausted_evidence_mentions_existing_data(self):
        """Evidence must clarify quota exhaustion does NOT invalidate existing data."""
        result = self.gate.evaluate("finmind", context={"quota_exhausted": True})
        self.assertIn("NOT invalidated", result.evidence)


# ===========================================================================
# CLASS 21: Provenance Gate
# ===========================================================================
class TestProvenanceGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.provenance_gate_v146 import ProvenanceGate
        from data.governance.quality.models_v146 import GateStatus
        self.gate = ProvenanceGate()
        self.GateStatus = GateStatus

    def test_gate_wraps_v145(self):
        """ProvenanceGate must wrap v1.4.5 ProvenanceCompletenessGate."""
        self.assertTrue(hasattr(self.gate, "_v145_gate"))

    def test_empty_provenance_not_pass(self):
        result = self.gate.evaluate("unknown", context={})
        self.assertNotEqual(result.status, self.GateStatus.PASS.value)

    def test_result_has_gate_id(self):
        result = self.gate.evaluate("twse_official")
        self.assertIsNotNone(result.gate_id)


# ===========================================================================
# CLASS 22: Quarantine Manager
# ===========================================================================
class TestQuarantineManager(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.quarantine_v146 import ProviderQuarantineManager
        self.mgr = ProviderQuarantineManager()

    def test_quarantine_provider(self):
        record = self.mgr.quarantine("finmind", "test_reason", "safety_gate")
        self.assertEqual(record.provider_id, "finmind")
        self.assertFalse(record.auto_release_allowed)

    def test_quarantined_appears_in_list(self):
        self.mgr.quarantine("finmind", "test", "safety_gate")
        quarantined = self.mgr.list_quarantined()
        pids = [r.provider_id for r in quarantined]
        self.assertIn("finmind", pids)

    def test_auto_release_always_false(self):
        record = self.mgr.quarantine("finmind", "test", "safety_gate")
        self.assertFalse(record.auto_release_allowed)

    def test_release_requires_operator_argument(self):
        self.mgr.quarantine("tpex_official", "test", "safety_gate")
        released = self.mgr.release("tpex_official", released_by="operator_manual",
                                    release_reason="resolved")
        self.assertIsNotNone(released)
        self.assertTrue(released.released)

    def test_release_readiness_has_auto_release_allowed_false(self):
        self.mgr.quarantine("finmind", "test", "safety_gate")
        readiness = self.mgr.evaluate_release_readiness("finmind")
        self.assertIn("auto_release_allowed", readiness)
        self.assertFalse(readiness["auto_release_allowed"])

    def test_restrict_provider(self):
        record = self.mgr.restrict("finmind", "test_restriction", "coverage_gate")
        self.assertEqual(record.provider_id, "finmind")

    def test_block_provider(self):
        record = self.mgr.block("finmind", "test_block", "safety_gate")
        self.assertEqual(record.provider_id, "finmind")


# ===========================================================================
# CLASS 23: Audit Service
# ===========================================================================
class TestAuditService(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.audit_v146 import QualityDecisionAuditService
        from data.governance.quality.models_v146 import QualityDecision
        self.svc = QualityDecisionAuditService()
        self.QualityDecision = QualityDecision

    def _make_decision(self, decision_id="d1", decision="ALLOW"):
        return self.QualityDecision(
            decision_id=decision_id, scope="PROVIDER", subject_id="twse_official",
            decision=decision, quality_state="ACTIVE",
            formal_research_allowed=(decision == "ALLOW"),
            backtest_allowed=(decision == "ALLOW"),
            report_allowed=(decision == "ALLOW"),
            ingestion_allowed=(decision == "ALLOW"),
            blocking_failures=[] if decision == "ALLOW" else ["gate_x"],
            warnings=[], gate_results=[], quality_score=88,
            score_overrode_blocking=False,
        )

    def test_record_returns_audit_entry(self):
        decision = self._make_decision()
        entry = self.svc.record(decision, provider_id="twse_official")
        self.assertIsNotNone(entry.audit_id)

    def test_list_grows_after_record(self):
        before = len(self.svc.list_all())
        self.svc.record(self._make_decision("d2"), provider_id="twse_official")
        after = len(self.svc.list_all())
        self.assertEqual(after, before + 1)

    def test_evidence_hash_is_deterministic(self):
        from data.governance.quality.models_v146 import QualityDecisionAudit
        h1 = QualityDecisionAudit.compute_evidence_hash("d1", "ALLOW", [], "2026-01-01T00:00:00Z")
        h2 = QualityDecisionAudit.compute_evidence_hash("d1", "ALLOW", [], "2026-01-01T00:00:00Z")
        self.assertEqual(h1, h2)

    def test_get_by_decision_id(self):
        self.svc.record(self._make_decision("d_search"), provider_id="twse_official")
        results = self.svc.get_by_decision_id("d_search")
        self.assertGreater(len(results), 0)

    def test_audit_summary_append_only_true(self):
        summary = self.svc.summary()
        self.assertTrue(summary["append_only"])

    def test_audit_summary_no_credentials(self):
        summary = self.svc.summary()
        self.assertTrue(summary["no_credentials_stored"])


# ===========================================================================
# CLASS 24: Policy Manager
# ===========================================================================
class TestPolicyManager(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.policy_v146 import QualityPolicyManager
        self.mgr = QualityPolicyManager()

    def test_get_policy_version(self):
        ver = self.mgr.get_policy_version()
        self.assertIn("1.4.6", ver)

    def test_default_policy_no_mock_formal_conclusion(self):
        policy = self.mgr.get_policy("twse_official")
        self.assertFalse(policy.get("mock_formal_conclusion_allowed", True))

    def test_default_policy_no_auto_release(self):
        policy = self.mgr.get_policy("twse_official")
        self.assertFalse(policy.get("auto_release_allowed", True))

    def test_default_policy_score_cannot_override(self):
        policy = self.mgr.get_policy("twse_official")
        self.assertFalse(policy.get("score_can_override_blocking", True))

    def test_list_provider_policies(self):
        policies = self.mgr.list_provider_policies()
        self.assertIsInstance(policies, list)
        self.assertGreater(len(policies), 0)

    def test_validate_policy_rejects_auto_release(self):
        result = self.mgr.validate_policy({"auto_release_allowed": True})
        self.assertFalse(result["valid"])

    def test_validate_policy_rejects_score_override(self):
        result = self.mgr.validate_policy({"score_can_override_blocking": True})
        self.assertFalse(result["valid"])

    def test_validate_policy_rejects_mock_formal(self):
        result = self.mgr.validate_policy({"mock_formal_conclusion_allowed": True})
        self.assertFalse(result["valid"])

    def test_provider_policy_stricter_data_quality(self):
        default_policy = self.mgr.get_policy("__no_override__")
        twse_policy = self.mgr.get_policy("twse_official")
        default_min = default_policy.get("data_quality_pass_threshold", 0)
        twse_min = twse_policy.get("data_quality_pass_threshold", 0)
        self.assertGreaterEqual(twse_min, default_min)


# ===========================================================================
# CLASS 25: Health Check
# ===========================================================================
class TestHealthCheck(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.health_v146 import ProviderQualityGatesHealthCheck
        self.hc = ProviderQualityGatesHealthCheck()

    def test_health_check_runs(self):
        results = self.hc.run()
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)

    def test_health_summary_has_required_keys(self):
        summary = self.hc.get_health_summary()
        for key in ["total", "passed", "failed", "warned"]:
            self.assertIn(key, summary)

    def test_health_summary_totals_consistent(self):
        summary = self.hc.get_health_summary()
        total = summary["total"]
        accounted = summary["passed"] + summary["failed"] + summary["warned"]
        self.assertEqual(total, accounted)

    def test_no_safety_check_failures(self):
        results = self.hc.run()
        # results may be a dict {check_name: (status, msg)} or list
        if isinstance(results, dict):
            safety_checks = {k: v for k, v in results.items() if "safety" in k.lower()}
            failed = [k for k, v in safety_checks.items() if v[0] == "FAIL"]
        else:
            safety_checks = [r for r in results if "safety" in str(r.get("check_name", "")).lower()]
            failed = [r for r in safety_checks if r.get("status") == "FAIL"]
        self.assertEqual(len(failed), 0, msg=str(failed))

    def test_score_check_present(self):
        results = self.hc.run()
        if isinstance(results, dict):
            score_checks = [k for k in results if "score" in k.lower()]
        else:
            score_checks = [r for r in results if "score" in str(r.get("check_name", "")).lower()]
        self.assertGreater(len(score_checks), 0)


# ===========================================================================
# CLASS 26: Storage (in-memory SQLite)
# ===========================================================================
class TestQualityStore(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.store_v146 import QualityGateStore
        self.store = QualityGateStore()
        self.store.setup()  # in-memory

    def tearDown(self):
        self.store.close()

    def test_upsert_and_get_provider_profile(self):
        self.store.upsert_provider_profile({
            "provider_id": "twse_official",
            "quality_state": "ACTIVE",
            "authority_level": "PRIMARY_OFFICIAL",
            "formal_research_allowed": True,
            "backtest_allowed": True,
            "report_allowed": True,
            "ingestion_allowed": True,
        })
        profile = self.store.get_provider_profile("twse_official")
        self.assertIsNotNone(profile)

    def test_get_unknown_provider_returns_none(self):
        profile = self.store.get_provider_profile("no_such_provider_999")
        self.assertIsNone(profile)

    def test_save_and_get_decision(self):
        self.store.save_decision({
            "decision_id": "dec_001",
            "scope": "PROVIDER",
            "subject_id": "twse_official",
            "decision": "ALLOW",
            "quality_state": "ACTIVE",
            "formal_research_allowed": True,
            "backtest_allowed": True,
            "report_allowed": True,
            "ingestion_allowed": True,
        })
        decision = self.store.get_decision("dec_001")
        self.assertIsNotNone(decision)

    def test_append_audit_grows(self):
        self.store.append_audit({
            "audit_id": "aud_001",
            "decision_id": "d1",
            "scope": "PROVIDER",
            "subject_id": "twse_official",
            "decision": "ALLOW",
            "quality_state": "ACTIVE",
            "evidence_hash": "abc123",
            "audited_at": "2026-01-01T00:00:00Z",
        })
        self.store.append_audit({
            "audit_id": "aud_002",
            "decision_id": "d2",
            "scope": "PROVIDER",
            "subject_id": "bad_provider",
            "decision": "BLOCK",
            "quality_state": "BLOCKED",
            "evidence_hash": "def456",
            "audited_at": "2026-01-01T00:01:00Z",
        })
        entries = self.store.list_audit()
        self.assertEqual(len(entries), 2)

    def test_list_provider_profiles(self):
        self.store.upsert_provider_profile({
            "provider_id": "twse_official",
            "quality_state": "ACTIVE",
            "authority_level": "PRIMARY_OFFICIAL",
            "formal_research_allowed": True,
            "backtest_allowed": True,
            "report_allowed": True,
            "ingestion_allowed": True,
        })
        profiles = self.store.list_provider_profiles()
        self.assertIsInstance(profiles, list)
        self.assertGreater(len(profiles), 0)


# ===========================================================================
# CLASS 27: Query Service
# ===========================================================================
class TestQueryService(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.query_v146 import ProviderQualityQueryService
        self.svc = ProviderQualityQueryService()

    def test_get_provider_quality_state_returns_dict(self):
        state = self.svc.get_provider_quality_state("twse_official")
        self.assertIsInstance(state, dict)

    def test_list_provider_profiles_returns_list(self):
        profiles = self.svc.list_provider_profiles()
        self.assertIsInstance(profiles, list)

    def test_list_blocked_providers_returns_list(self):
        blocked = self.svc.list_blocked_providers()
        self.assertIsInstance(blocked, list)

    def test_quality_summary_report_returns_dict(self):
        report = self.svc.quality_summary_report()
        self.assertIsInstance(report, dict)

    def test_explain_decision_nonexistent_returns_error(self):
        result = self.svc.explain_decision("nonexistent_decision_id_xyz_999")
        self.assertIn("error", result)


# ===========================================================================
# CLASS 28: Formal Research Gate
# ===========================================================================
class TestFormalResearchGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.formal_research_gate_v146 import FormalResearchEligibilityGate
        self.gate = FormalResearchEligibilityGate()

    def test_all_conditions_met_eligible(self):
        result = self.gate.evaluate("twse_official", "twse_daily_prices", context={
            "authority_level": "PRIMARY_OFFICIAL",
            "dataset_admitted": True,
            "provenance_complete": True,
            "pit_compliant": True,
            "schema_valid": True,
            "no_unresolved_conflicts": True,
            "real_data": True,
        })
        self.assertTrue(result.eligible)
        self.assertEqual(len(result.blocking_failures), 0)

    def test_mock_authority_not_eligible(self):
        result = self.gate.evaluate("mock_provider", "mock_dataset", context={
            "authority_level": "MOCK",
            "dataset_admitted": True,
            "provenance_complete": True,
            "pit_compliant": True,
            "schema_valid": True,
            "no_unresolved_conflicts": True,
            "real_data": True,
        })
        self.assertFalse(result.eligible)

    def test_no_context_not_eligible(self):
        result = self.gate.evaluate("unknown_xyz", "unknown_dataset")
        self.assertFalse(result.eligible)
        self.assertGreater(len(result.blocking_failures), 0)

    def test_missing_pit_compliance_blocks(self):
        result = self.gate.evaluate("twse_official", "twse_daily_prices", context={
            "authority_level": "PRIMARY_OFFICIAL",
            "dataset_admitted": True,
            "provenance_complete": True,
            "pit_compliant": False,
            "schema_valid": True,
            "no_unresolved_conflicts": True,
            "real_data": True,
        })
        self.assertFalse(result.eligible)
        self.assertIn("pit_not_compliant", result.blocking_failures)


# ===========================================================================
# CLASS 29: Backtest Gate
# ===========================================================================
class TestBacktestGate(unittest.TestCase):

    def setUp(self):
        from data.governance.quality.backtest_gate_v146 import BacktestInputEligibilityGate
        self.gate = BacktestInputEligibilityGate()

    def test_future_leakage_blocks(self):
        result = self.gate.evaluate("twse_official", "twse_daily_prices", context={
            "future_leakage": True,
        })
        self.assertFalse(result.eligible)
        self.assertTrue(any("future_leakage" in f for f in result.blocking_failures))

    def test_lookahead_leakage_blocks(self):
        result = self.gate.evaluate("twse_official", "twse_daily_prices", context={
            "lookahead_leakage": True,
        })
        self.assertFalse(result.eligible)

    def test_clean_data_with_authority_eligible(self):
        result = self.gate.evaluate("twse_official", "twse_daily_prices", context={
            "pit_available": True,
            "revision_frozen": True,
            "future_leakage": False,
            "lookahead_leakage": False,
            "coverage_pct": 0.99,
            "authority_level": "PRIMARY_OFFICIAL",
        })
        self.assertTrue(result.eligible)

    def test_no_pit_not_eligible(self):
        result = self.gate.evaluate("finmind", "finmind_financials", context={
            "pit_available": False,
            "revision_frozen": False,
            "future_leakage": False,
            "lookahead_leakage": False,
        })
        self.assertFalse(result.eligible)


# ===========================================================================
# CLASS 30: GUI Panel
# ===========================================================================
class TestProviderQualityGatesPanel(unittest.TestCase):

    def setUp(self):
        from gui.provider_quality_gates_panel import ProviderQualityGatesPanel
        self.panel = ProviderQualityGatesPanel()

    def test_tab_id(self):
        self.assertEqual(self.panel.tab_id, "provider_quality_gates")

    def test_group_is_data(self):
        self.assertEqual(self.panel.group, "data")

    def test_priority_is_p1(self):
        self.assertEqual(self.panel.priority, "P1")

    def test_read_only(self):
        self.assertTrue(self.panel.read_only)

    def test_no_real_orders(self):
        self.assertTrue(self.panel.no_real_orders)

    def test_production_blocked(self):
        self.assertTrue(self.panel.production_blocked)

    def test_quality_score_cannot_override_blocking(self):
        self.assertFalse(self.panel.quality_score_can_override_blocking)

    def test_get_sections_contains_overview(self):
        self.assertIn("Overview", self.panel.get_sections())

    def test_get_sections_contains_gate_results(self):
        self.assertIn("Gate Results", self.panel.get_sections())

    def test_get_sections_contains_quarantine(self):
        self.assertIn("Quarantine", self.panel.get_sections())

    def test_get_actions_no_forbidden_terms(self):
        actions = self.panel.get_actions()
        forbidden = {"override", "promote", "release_all", "buy", "sell", "order", "auto_trade"}
        for action in actions:
            for f in forbidden:
                self.assertNotIn(f, action.lower())

    def test_safety_banner_contains_no_real_orders(self):
        banner = self.panel.get_safety_banner()
        self.assertIn("No Real Orders", banner)

    def test_render_overview_is_read_only(self):
        result = self.panel.render_overview()
        self.assertTrue(result.get("read_only"))
        self.assertTrue(result.get("no_real_orders"))

    def test_render_quarantine_no_auto_release(self):
        result = self.panel.render_quarantine()
        self.assertFalse(result.get("auto_release_allowed"))

    def test_on_refresh_returns_dict(self):
        result = self.panel.on_refresh()
        self.assertIsInstance(result, dict)


# ===========================================================================
# CLASS 31: Report
# ===========================================================================
class TestProviderQualityGatesReport(unittest.TestCase):

    def setUp(self):
        from reports.provider_quality_gates_report import ProviderQualityGatesReport
        self.report = ProviderQualityGatesReport()

    def test_render_returns_string(self):
        result = self.report.render()
        self.assertIsInstance(result, str)

    def test_render_contains_version(self):
        result = self.report.render()
        self.assertIn("1.4.6", result)

    def test_render_contains_research_only(self):
        result = self.report.render()
        self.assertIn("Research Only", result)

    def test_render_contains_no_real_orders(self):
        result = self.report.render()
        self.assertIn("No Real Orders", result)

    def test_render_contains_safety_invariants_section(self):
        result = self.report.render()
        self.assertIn("Safety Invariants", result)

    def test_render_contains_quality_score_override_false(self):
        result = self.report.render()
        self.assertIn("QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE", result)


# ===========================================================================
# CLASS 32: Fixture Validation
# ===========================================================================
class TestFixtureFiles(unittest.TestCase):
    FIXTURE_DIR = Path(__file__).parent / "fixtures" / "provider_quality_gates"
    REQUIRED_FIELDS = [
        "_fixture_type",
        "_demo_only",
        "_not_real_data",
        "_not_for_formal_conclusion",
    ]

    def test_fixtures_directory_exists(self):
        self.assertTrue(self.FIXTURE_DIR.exists(), f"Missing: {self.FIXTURE_DIR}")

    def test_fixture_files_present(self):
        files = list(self.FIXTURE_DIR.glob("*.json"))
        self.assertGreater(len(files), 0, "No fixture files found")

    def test_all_fixtures_have_required_fields(self):
        files = list(self.FIXTURE_DIR.glob("*.json"))
        for f in files:
            with self.subTest(fixture=f.name):
                data = json.loads(f.read_text(encoding="utf-8"))
                for field in self.REQUIRED_FIELDS:
                    self.assertIn(field, data, f"{f.name} missing field: {field}")

    def test_all_fixtures_are_demo_only(self):
        files = list(self.FIXTURE_DIR.glob("*.json"))
        for f in files:
            with self.subTest(fixture=f.name):
                data = json.loads(f.read_text(encoding="utf-8"))
                self.assertTrue(data.get("_demo_only"), f"{f.name}: _demo_only must be true")

    def test_all_fixtures_fixture_type_is_test_fixture(self):
        files = list(self.FIXTURE_DIR.glob("*.json"))
        for f in files:
            with self.subTest(fixture=f.name):
                data = json.loads(f.read_text(encoding="utf-8"))
                self.assertEqual(
                    data.get("_fixture_type"), "TEST_FIXTURE",
                    f"{f.name}: _fixture_type must be TEST_FIXTURE"
                )

    def test_no_real_data_flag(self):
        files = list(self.FIXTURE_DIR.glob("*.json"))
        for f in files:
            with self.subTest(fixture=f.name):
                data = json.loads(f.read_text(encoding="utf-8"))
                self.assertTrue(data.get("_not_real_data"), f"{f.name}: _not_real_data must be true")


# ===========================================================================
# CLASS 33: Integration — End-to-End Decision Flow
# ===========================================================================
class TestEndToEndDecisionFlow(unittest.TestCase):

    def test_twse_full_decision_allows(self):
        from data.governance.quality.provider_gate_v146 import ProviderOperationalGate
        from data.governance.quality.decision_engine_v146 import QualityDecisionEngine
        from data.governance.quality.models_v146 import QualityGateResult

        gate = ProviderOperationalGate()
        engine = QualityDecisionEngine()

        profile = gate.evaluate("twse_official")
        gate_result_objs = [
            QualityGateResult(**r) if isinstance(r, dict) else r
            for r in profile.gate_results
        ]
        # Use engine with profile data
        decision = engine.decide(
            "PROVIDER", "twse_official",
            gate_result_objs if gate_result_objs else [],
            quality_score=profile.quality_score or 80.0,
        )
        self.assertIn(decision.decision, ["ALLOW", "ALLOW_WITH_WARNING"])

    def test_unknown_provider_full_decision_blocks(self):
        from data.governance.quality.provider_gate_v146 import ProviderOperationalGate

        gate = ProviderOperationalGate()
        profile = gate.evaluate("nonexistent_provider_xyz_999")
        self.assertEqual(profile.quality_state, "BLOCKED")
        self.assertFalse(profile.formal_research_allowed)

    def test_score_99_does_not_override_blocking_failure(self):
        from data.governance.quality.decision_engine_v146 import QualityDecisionEngine
        from data.governance.quality.models_v146 import QualityGateResult, GateStatus

        engine = QualityDecisionEngine()
        gate_results = [
            QualityGateResult(
                gate_id="safety_gate", gate_name="Safety", scope="PROVIDER",
                subject_id="any_provider", status=GateStatus.BLOCKED.value,
                passed=False, blocking=True, evidence="violation", evaluated_at="",
            ),
        ]
        decision = engine.decide("PROVIDER", "any_provider", gate_results, quality_score=99)
        self.assertEqual(decision.decision, "BLOCK")
        self.assertFalse(decision.score_overrode_blocking)


# ===========================================================================
# CLASS 34: CLI Command Registry
# ===========================================================================
class TestCLICommandRegistry(unittest.TestCase):

    def test_quality_gates_commands_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = [c.name for c in PROVIDER_COMMANDS]
        self.assertIn("provider-quality-health", names)
        self.assertIn("provider-quality-gates", names)
        self.assertIn("provider-quality-evaluate-provider", names)

    def test_quality_commands_have_correct_group(self):
        from cli.command_registry import PROVIDER_COMMANDS
        for cmd in PROVIDER_COMMANDS:
            if cmd.name.startswith("provider-quality"):
                self.assertEqual(cmd.group, "provider_quality_gates",
                                 f"{cmd.name} has wrong group: {cmd.group}")

    def test_quality_commands_introduced_in_146(self):
        from cli.command_registry import PROVIDER_COMMANDS
        for cmd in PROVIDER_COMMANDS:
            if cmd.name.startswith("provider-quality"):
                self.assertEqual(cmd.introduced_in, "1.4.6",
                                 f"{cmd.name} introduced_in: {cmd.introduced_in}")

    def test_at_least_20_quality_commands(self):
        from cli.command_registry import PROVIDER_COMMANDS
        quality_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("provider-quality")]
        self.assertGreaterEqual(len(quality_cmds), 20)


# ===========================================================================
# CLASS 35: Version Info
# ===========================================================================
class TestVersionInfo(unittest.TestCase):

    def test_version_is_146(self):
        from release.version_info import VERSION
        # v1.4.6 feature; accept hotfix and successor releases
        self.assertTrue(
            VERSION[:5] in ("1.4.6", "1.4.7") or VERSION.startswith("1.4.") or VERSION.startswith("1.5."),
            msg=f"Expected 1.4.x or 1.5.x release, got {VERSION}"
        )

    def test_release_name_provider_quality_gates(self):
        from release.version_info import RELEASE_NAME
        _KNOWN = (
            "Provider Quality Gates",
            "Full-Suite Collection Integrity Hotfix",
            "Forum Intelligence & Market Sentiment",
            "Provider Integration Hardening",
            "Provider Integration Test Integrity Hotfix",
            "Provider Stable Rollup",
            "Portfolio Research Foundation",
            "Portfolio Research Foundation Integrity Hotfix",
        )
        self.assertTrue(
            any(name in RELEASE_NAME for name in _KNOWN),
            msg=f"Expected v1.4.x-series RELEASE_NAME, got: {RELEASE_NAME}"
        )

    def test_provider_quality_gates_available(self):
        from release.version_info import PROVIDER_QUALITY_GATES_AVAILABLE
        self.assertTrue(PROVIDER_QUALITY_GATES_AVAILABLE)

    def test_no_real_orders_flag(self):
        from release.version_info import NO_REAL_ORDERS
        self.assertTrue(NO_REAL_ORDERS)


# ===========================================================================
# CLASS 36: Capability Registry
# ===========================================================================
class TestCapabilityRegistry(unittest.TestCase):

    def _get_pqg(self):
        from release.capability_registry import get_capabilities
        caps = get_capabilities()
        for cap in caps:
            if cap.get("id") == "provider_quality_gates":
                return cap
        return None

    def test_provider_quality_gates_is_stable(self):
        pqg = self._get_pqg()
        self.assertIsNotNone(pqg, "provider_quality_gates not found in capabilities")
        self.assertEqual(pqg.get("status"), "STABLE")
        self.assertTrue(pqg.get("available"))

    def test_provider_quality_gates_has_health_check(self):
        pqg = self._get_pqg()
        self.assertIsNotNone(pqg)
        self.assertIn("health_check", pqg)
        self.assertIn("health_v146", pqg["health_check"])


# ===========================================================================
# Entrypoint
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
