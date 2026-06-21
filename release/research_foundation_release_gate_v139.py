"""
release/research_foundation_release_gate_v139.py — Release gate for v1.3.9.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
from typing import Any


def _make_gate(name: str, status: str, evidence: str, blocking: bool,
               warnings: list, remediation: str) -> dict:
    return {
        "gate_name": name,
        "status": status,
        "evidence": evidence,
        "blocking": blocking,
        "warnings": warnings,
        "remediation": remediation,
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


class ResearchFoundationReleaseGate:
    """
    10-gate release gate for Research Foundation Stable Rollup v1.3.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def run(self) -> list[dict]:
        gates = []
        gates.append(self._version_gate())
        gates.append(self._capability_gate())
        gates.append(self._compatibility_gate())
        gates.append(self._storage_gate())
        gates.append(self._cli_gate())
        gates.append(self._gui_gate())
        gates.append(self._docs_gate())
        gates.append(self._safety_gate())
        gates.append(self._regression_gate())
        gates.append(self._runtime_hygiene_gate())
        # v1.4.6 Provider Quality Gates
        gates.append(self._provider_quality_gate_registry_gate())
        gates.append(self._provider_onboarding_gates_gate())
        gates.append(self._dataset_admission_gates_gate())
        gates.append(self._formal_research_gate_gate())
        gates.append(self._backtest_input_gate_gate())
        gates.append(self._provenance_gate_gate())
        gates.append(self._pit_gate_gate())
        gates.append(self._schema_drift_gate_gate())
        gates.append(self._authority_gate_gate())
        gates.append(self._conflict_gate_gate())
        gates.append(self._quarantine_policy_gate())
        gates.append(self._quality_audit_gate())
        gates.append(self._no_hidden_blocking_failure_gate())
        return gates

    def _version_gate(self) -> dict:
        try:
            from release.version_info import VERSION, RELEASE_NAME, BASE_RELEASE, REPLAY_STABLE_BASELINE
            _KNOWN_NAMES = {
                "Research Foundation Stable Rollup",
                "TWSE Provider",
                "Strategy Robustness & Regime Validation",
                "TPEx Provider",
                "MOPS Provider",
                "data.gov.tw Provider",
                "Provider CLI Registration Hotfix",
                "Provider Health Consistency Hotfix",
                "FinMind Adapter Hardening",
                "Source Lineage & Rate Limit",
                "Provider Quality Gates",
                "Forum Intelligence & Market Sentiment",
                "Data Provider Stable Rollup",
                "Full-Suite Collection Integrity Hotfix",
            }
            parts = tuple(int(x) for x in VERSION.split(".")[:3])
            ok = (
                parts >= (1, 3, 9)
                and RELEASE_NAME in _KNOWN_NAMES
                and any(m in BASE_RELEASE for m in ("1.3.7", "1.3.9", "1.4.0", "1.4.1", "1.4.2", "1.4.3", "1.4.4", "1.4.5", "1.4.6"))
                and REPLAY_STABLE_BASELINE == "1.2.9"
            )
            return _make_gate(
                "version_gate", "PASS" if ok else "FAIL",
                f"VERSION={VERSION}, RELEASE_NAME={RELEASE_NAME}",
                not ok, [], "" if ok else "Update VERSION to >= 1.3.9"
            )
        except Exception as exc:
            return _make_gate("version_gate", "FAIL", str(exc), True, [], "Fix version_info import")

    def _capability_gate(self) -> dict:
        try:
            from release.capability_registry import (
                is_capability_available, list_planned_capabilities,
                validate_capability_dependencies
            )
            stable_caps = [
                "real_data_quality", "universe_expansion", "provider_adapter_foundation",
                "coverage_repair", "data_freshness", "empirical_backtest",
                "abc_validation", "strategy_robustness", "canonical_version_alignment",
            ]
            missing = [c for c in stable_caps if not is_capability_available(c)]
            planned_available = [c for c in list_planned_capabilities() if is_capability_available(c)]
            dep_result = validate_capability_dependencies()
            ok = len(missing) == 0 and len(planned_available) == 0 and dep_result["valid"]
            evidence = f"stable_missing={missing}, planned_available={planned_available}, dep_errors={dep_result['errors']}"
            return _make_gate(
                "capability_gate", "PASS" if ok else "FAIL",
                evidence, not ok, [], "" if ok else f"Register missing: {missing}"
            )
        except Exception as exc:
            return _make_gate("capability_gate", "FAIL", str(exc), True, [], "Fix capability_registry")

    def _compatibility_gate(self) -> dict:
        try:
            from release.version_alignment import load_snapshot_gracefully, is_known_release_lineage
            old_payloads = [
                {"application_version": "1.4.0"},
                {"application_version": "1.4.1"},
                {"application_version": "1.4.2"},
            ]
            errors = []
            for p in old_payloads:
                try:
                    result = load_snapshot_gracefully(p)
                    if "canonical_release_version" not in result:
                        errors.append(f"Missing canonical for {p['application_version']}")
                except Exception as e:
                    errors.append(str(e))
            ok = len(errors) == 0
            return _make_gate(
                "compatibility_gate", "PASS" if ok else "FAIL",
                f"old payload errors={errors}", not ok, [],
                "" if ok else f"Fix enrich_payload: {errors}"
            )
        except Exception as exc:
            return _make_gate("compatibility_gate", "FAIL", str(exc), True, [], "Fix version_alignment")

    def _storage_gate(self) -> dict:
        try:
            from release.version_alignment import validate_version_metadata
            result = validate_version_metadata({"application_version": "1.3.9"})
            ok = result["status"] in ("OK", "WARN")
            return _make_gate(
                "storage_gate", "PASS" if ok else "FAIL",
                f"metadata validation status={result['status']}", not ok,
                result.get("warnings", []), "" if ok else "Fix version metadata"
            )
        except Exception as exc:
            return _make_gate("storage_gate", "FAIL", str(exc), True, [], "Fix validate_version_metadata")

    def _cli_gate(self) -> dict:
        try:
            import main as m
            required = [
                "cmd_research_foundation_health",
                "cmd_research_foundation_summary",
                "cmd_version_info",
            ]
            missing = [r for r in required if not hasattr(m, r)]
            ok = len(missing) == 0
            return _make_gate(
                "cli_gate", "PASS" if ok else "FAIL",
                f"missing_commands={missing}", not ok, [],
                "" if ok else f"Add missing CLI commands: {missing}"
            )
        except Exception as exc:
            return _make_gate("cli_gate", "FAIL", str(exc), True, [], "Fix main.py imports")

    def _gui_gate(self) -> dict:
        try:
            import gui.research_foundation_summary_panel
            return _make_gate(
                "gui_gate", "PASS",
                "research_foundation_summary_panel imported", False, [], ""
            )
        except Exception as exc:
            return _make_gate(
                "gui_gate", "WARN",
                f"GUI panel import failed: {exc}", False,
                [str(exc)], "Verify gui/research_foundation_summary_panel.py"
            )

    def _docs_gate(self) -> dict:
        import os
        doc_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "docs", "research_foundation_stable_rollup_v1.3.9.md"
        )
        ok = os.path.exists(doc_path)
        return _make_gate(
            "docs_gate", "PASS" if ok else "WARN",
            f"doc_exists={ok} path={doc_path}", False,
            [] if ok else ["docs/research_foundation_stable_rollup_v1.3.9.md missing"],
            "" if ok else "Create docs/research_foundation_stable_rollup_v1.3.9.md"
        )

    def _safety_gate(self) -> dict:
        try:
            from release.version_info import (
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
                PRODUCTION_TRADING_BLOCKED, MOCK_FALLBACK_ENABLED,
            )
            ok = (
                NO_REAL_ORDERS is True
                and BROKER_EXECUTION_ENABLED is False
                and PRODUCTION_TRADING_BLOCKED is True
                and MOCK_FALLBACK_ENABLED is False
            )
            evidence = (
                f"NO_REAL_ORDERS={NO_REAL_ORDERS}, "
                f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED}, "
                f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED}"
            )
            return _make_gate(
                "safety_gate", "PASS" if ok else "FAIL",
                evidence, not ok, [],
                "" if ok else "Safety flags must be correct — do not change"
            )
        except Exception as exc:
            return _make_gate("safety_gate", "FAIL", str(exc), True, [], "Fix safety flags")

    def _regression_gate(self) -> dict:
        # Run the health check and propagate blocking failures to the gate.
        try:
            from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
            hc = ResearchFoundationStableHealthCheck()
            summary = hc.get_health_summary()
            failed = summary.get("failed", 0)
            checks_detail = summary.get("checks", {})
            # Safety-related checks that block the gate if they fail
            safety_keys = [
                "safety_no_real_orders",
                "safety_broker_execution_enabled",
                "safety_production_trading_blocked",
            ]
            safety_failures = [k for k in safety_keys
                               if checks_detail.get(k, {}).get("status") == "FAIL"]
            if safety_failures:
                return _make_gate(
                    "regression_gate", "FAIL",
                    f"Health safety checks FAILED: {safety_failures}", True,
                    [], f"Fix safety checks: {safety_failures}"
                )
            if failed > 0:
                failing_checks = [k for k, v in checks_detail.items()
                                  if v.get("status") == "FAIL"]
                return _make_gate(
                    "regression_gate", "FAIL",
                    f"Health check has {failed} failure(s): {failing_checks}", True,
                    [], f"Fix health check failures before release: {failing_checks}"
                )
            return _make_gate(
                "regression_gate", "PASS",
                f"Health check passed ({summary.get('total_checks', 0)} checks, "
                f"{summary.get('passed', 0)} passed). "
                "Full pytest suite must also be verified externally.", False,
                ["Run full pytest suite before release"], "Run: pytest tests/"
            )
        except Exception as exc:
            return _make_gate(
                "regression_gate", "FAIL",
                f"Could not run health check: {exc}", True,
                [], "Fix health check import"
            )

    def _runtime_hygiene_gate(self) -> dict:
        import os
        from release.text_file_reader import read_text_with_encoding_fallback
        gitignore_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".gitignore"
        )
        ok = os.path.exists(gitignore_path)
        warnings = []
        if ok:
            try:
                content, _enc, _fallback, _warns = read_text_with_encoding_fallback(gitignore_path)
                if "data/research_foundation/" not in content:
                    warnings.append("data/research_foundation/ not in .gitignore")
            except ValueError as exc:
                warnings.append(f".gitignore unreadable: {exc}")
        return _make_gate(
            "runtime_hygiene_gate", "PASS" if (ok and not warnings) else "WARN",
            f"gitignore_exists={ok}", False, warnings,
            "" if not warnings else "Add runtime paths to .gitignore"
        )

    # ------------------------------------------------------------------
    # v1.4.6 Provider Quality Gates
    # ------------------------------------------------------------------

    def _provider_quality_gate_registry_gate(self) -> dict:
        try:
            from data.governance.quality.gate_registry_v146 import QualityGateRegistry
            reg = QualityGateRegistry()
            result = reg.validate_registry()
            ok = result["valid"] and result["gate_count"] >= 15
            return _make_gate(
                "PROVIDER_QUALITY_GATE_REGISTRY_VALID",
                "PASS" if ok else "FAIL",
                f"gates={result['gate_count']}, valid={result['valid']}, errors={result['errors']}",
                not ok, result.get("warnings", []),
                "" if ok else f"Fix gate registry: {result['errors']}"
            )
        except Exception as exc:
            return _make_gate("PROVIDER_QUALITY_GATE_REGISTRY_VALID", "FAIL", str(exc), True, [],
                              "Fix gate_registry_v146 import")

    def _provider_onboarding_gates_gate(self) -> dict:
        try:
            from data.governance.quality.provider_gate_v146 import ProviderOperationalGate
            gate = ProviderOperationalGate()
            profile = gate.evaluate("twse")
            ok = profile.quality_state in ("ACTIVE", "DEGRADED")
            return _make_gate(
                "PROVIDER_ONBOARDING_GATES_PASS",
                "PASS" if ok else "FAIL",
                f"twse quality_state={profile.quality_state}",
                not ok, [],
                "" if ok else "Fix provider_gate_v146"
            )
        except Exception as exc:
            return _make_gate("PROVIDER_ONBOARDING_GATES_PASS", "FAIL", str(exc), True, [],
                              "Fix provider_gate_v146")

    def _dataset_admission_gates_gate(self) -> dict:
        try:
            from data.governance.quality.dataset_gate_v146 import DatasetAdmissionGate
            gate = DatasetAdmissionGate()
            profile = gate.evaluate("daily_ohlcv", "twse", {"schema_valid": True})
            ok = profile.admitted
            return _make_gate(
                "DATASET_ADMISSION_GATES_VALID",
                "PASS" if ok else "FAIL",
                f"twse:daily_ohlcv admitted={profile.admitted}",
                not ok, [],
                "" if ok else "Fix dataset_gate_v146"
            )
        except Exception as exc:
            return _make_gate("DATASET_ADMISSION_GATES_VALID", "FAIL", str(exc), True, [],
                              "Fix dataset_gate_v146")

    def _formal_research_gate_gate(self) -> dict:
        try:
            from data.governance.quality.formal_research_gate_v146 import FormalResearchEligibilityGate
            gate = FormalResearchEligibilityGate()
            result = gate.evaluate("twse", "daily_ohlcv", {
                "authority_level": "PRIMARY_OFFICIAL",
                "provenance_complete": True,
                "pit_compliant": True,
                "schema_valid": True,
                "no_unresolved_conflicts": True,
                "dataset_admitted": True,
                "real_data": True,
            })
            ok = result.eligible
            return _make_gate(
                "FORMAL_RESEARCH_GATE_VALID",
                "PASS" if ok else "FAIL",
                f"eligible={result.eligible}, blocking={result.blocking_failures}",
                not ok, result.warnings,
                "" if ok else f"Fix formal_research_gate: {result.blocking_failures}"
            )
        except Exception as exc:
            return _make_gate("FORMAL_RESEARCH_GATE_VALID", "FAIL", str(exc), True, [],
                              "Fix formal_research_gate_v146")

    def _backtest_input_gate_gate(self) -> dict:
        try:
            from data.governance.quality.backtest_gate_v146 import BacktestInputEligibilityGate
            gate = BacktestInputEligibilityGate()
            result = gate.evaluate("twse", "daily_ohlcv", {
                "pit_available": True, "lookahead_leakage": False, "future_leakage": False,
                "revision_frozen": True, "authority_level": "PRIMARY_OFFICIAL",
            })
            ok = result.eligible
            return _make_gate(
                "BACKTEST_INPUT_GATE_VALID",
                "PASS" if ok else "FAIL",
                f"eligible={result.eligible}",
                not ok, result.warnings,
                "" if ok else f"Fix backtest_gate: {result.blocking_failures}"
            )
        except Exception as exc:
            return _make_gate("BACKTEST_INPUT_GATE_VALID", "FAIL", str(exc), True, [],
                              "Fix backtest_gate_v146")

    def _provenance_gate_gate(self) -> dict:
        try:
            from data.governance.quality.provenance_gate_v146 import ProvenanceGate
            gate = ProvenanceGate()
            result = gate.evaluate("test_record", {})
            # Should fail gracefully (no lineage provided)
            ok = result.gate_id == "provenance_completeness"
            return _make_gate(
                "PROVENANCE_GATE_VALID",
                "PASS" if ok else "FAIL",
                f"ProvenanceGate wraps v1.4.5, gate_id={result.gate_id}",
                not ok, [],
                "" if ok else "Fix provenance_gate_v146"
            )
        except Exception as exc:
            return _make_gate("PROVENANCE_GATE_VALID", "FAIL", str(exc), True, [],
                              "Fix provenance_gate_v146")

    def _pit_gate_gate(self) -> dict:
        try:
            from data.governance.quality.pit_gate_v146 import PointInTimeGate
            gate = PointInTimeGate()
            result = gate.evaluate("test", {"future_leakage": True})
            ok = result.status == "BLOCKED"
            return _make_gate(
                "PIT_GATE_VALID",
                "PASS" if ok else "FAIL",
                f"future_leakage→BLOCKED={ok}",
                not ok, [],
                "" if ok else "Fix pit_gate_v146"
            )
        except Exception as exc:
            return _make_gate("PIT_GATE_VALID", "FAIL", str(exc), True, [],
                              "Fix pit_gate_v146")

    def _schema_drift_gate_gate(self) -> dict:
        try:
            from data.governance.quality.schema_gate_v146 import SchemaDriftGate
            from data.governance.models_v145 import SchemaDriftStatus
            gate = SchemaDriftGate()
            r1 = gate.evaluate("t", {"schema_drift_status": SchemaDriftStatus.BREAKING_MISSING_FIELD.value})
            r2 = gate.evaluate("t", {"schema_drift_status": SchemaDriftStatus.NO_CHANGE.value})
            ok = r1.status == "BLOCKED" and r2.status == "PASS"
            return _make_gate(
                "SCHEMA_DRIFT_GATE_VALID",
                "PASS" if ok else "FAIL",
                f"BREAKING→BLOCKED={r1.status=='BLOCKED'}, NO_CHANGE→PASS={r2.status=='PASS'}",
                not ok, [],
                "" if ok else "Fix schema_gate_v146"
            )
        except Exception as exc:
            return _make_gate("SCHEMA_DRIFT_GATE_VALID", "FAIL", str(exc), True, [],
                              "Fix schema_gate_v146")

    def _authority_gate_gate(self) -> dict:
        try:
            from data.governance.quality.authority_gate_v146 import AuthorityGate
            gate = AuthorityGate()
            r = gate.evaluate("mock", {"provider_id": "mock", "formal_use": True})
            ok = r.status in ("BLOCKED", "FAIL")
            return _make_gate(
                "AUTHORITY_GATE_VALID",
                "PASS" if ok else "FAIL",
                f"MOCK formal_use→BLOCKED={ok}",
                not ok, [],
                "" if ok else "Fix authority_gate_v146"
            )
        except Exception as exc:
            return _make_gate("AUTHORITY_GATE_VALID", "FAIL", str(exc), True, [],
                              "Fix authority_gate_v146")

    def _conflict_gate_gate(self) -> dict:
        try:
            from data.governance.quality.conflict_gate_v146 import ConflictGate
            gate = ConflictGate()
            r = gate.evaluate("test", {})
            ok = r.status == "PASS"
            return _make_gate(
                "CONFLICT_GATE_VALID",
                "PASS" if ok else "FAIL",
                f"no conflicts → PASS={ok}",
                not ok, [],
                "" if ok else "Fix conflict_gate_v146"
            )
        except Exception as exc:
            return _make_gate("CONFLICT_GATE_VALID", "FAIL", str(exc), True, [],
                              "Fix conflict_gate_v146")

    def _quarantine_policy_gate(self) -> dict:
        try:
            from data.governance.quality.quarantine_v146 import ProviderQuarantineManager
            mgr = ProviderQuarantineManager()
            rec = mgr.quarantine("test_p", "test reason", "test_gate")
            ok = rec.auto_release_allowed is False
            readiness = mgr.evaluate_release_readiness("test_p")
            ok = ok and readiness["auto_release_allowed"] is False
            return _make_gate(
                "QUARANTINE_POLICY_VALID",
                "PASS" if ok else "FAIL",
                f"auto_release_allowed=False confirmed",
                not ok, [],
                "" if ok else "Fix quarantine_v146: auto_release must be False"
            )
        except Exception as exc:
            return _make_gate("QUARANTINE_POLICY_VALID", "FAIL", str(exc), True, [],
                              "Fix quarantine_v146")

    def _quality_audit_gate(self) -> dict:
        try:
            from data.governance.quality.audit_v146 import QualityDecisionAuditService
            svc = QualityDecisionAuditService()
            summary = svc.summary()
            ok = summary.get("append_only") is True and summary.get("no_credentials_stored") is True
            return _make_gate(
                "QUALITY_AUDIT_VALID",
                "PASS" if ok else "FAIL",
                f"append_only={summary.get('append_only')}, no_credentials={summary.get('no_credentials_stored')}",
                not ok, [],
                "" if ok else "Fix audit_v146"
            )
        except Exception as exc:
            return _make_gate("QUALITY_AUDIT_VALID", "FAIL", str(exc), True, [],
                              "Fix audit_v146")

    def _no_hidden_blocking_failure_gate(self) -> dict:
        try:
            from data.governance.quality import QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE
            from data.governance.quality.decision_engine_v146 import QualityDecisionEngine
            from data.governance.quality.models_v146 import GateStatus, QualityGateResult, QualityScope
            ok = QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE is False
            # Verify engine enforces this
            eng = QualityDecisionEngine()
            blocking = QualityGateResult(
                gate_id="g", gate_name="g", scope=QualityScope.PROVIDER.value,
                subject_id="p", status=GateStatus.BLOCKED.value,
                passed=False, blocking=True, evidence="test",
            )
            decision = eng.decide(QualityScope.PROVIDER.value, "p", [blocking], quality_score=100.0)
            ok = ok and not decision.formal_research_allowed and not decision.score_overrode_blocking
            return _make_gate(
                "NO_HIDDEN_BLOCKING_FAILURE",
                "PASS" if ok else "FAIL",
                f"score_can_override=False, engine enforces blocking",
                not ok, [],
                "" if ok else "Score override is hidden — fix decision_engine_v146"
            )
        except Exception as exc:
            return _make_gate("NO_HIDDEN_BLOCKING_FAILURE", "FAIL", str(exc), True, [],
                              "Fix decision_engine_v146")

    def get_gate_summary(self) -> dict:
        gates = self.run()
        blocking = [g for g in gates if g["blocking"] and g["status"] == "FAIL"]
        warnings = [g for g in gates if g["status"] == "WARN"]
        passed = [g for g in gates if g["status"] == "PASS"]
        ok = len(blocking) == 0
        return {
            "overall": "PASS" if ok else "FAIL",
            "total_gates": len(gates),
            "passed": len(passed),
            "warnings": len(warnings),
            "blocking_failures": len(blocking),
            "blocking_gate_names": [g["gate_name"] for g in blocking],
            "gates": gates,
        }
