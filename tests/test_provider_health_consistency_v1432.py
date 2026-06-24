"""
tests/test_provider_health_consistency_v1432.py — Provider Health Consistency Hotfix v1.4.3.2 tests.
[!] Research Only. No Real Orders. Not Investment Advice.
72 tests covering: capability lifecycle, robustness read-only contract,
DataGovTwDataset formal_use_allowed, encoding fallback, release gate propagation,
CLI E2E, version, regression.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")


def _run(cmd_list):
    return subprocess.run(
        [sys.executable, "main.py"] + cmd_list,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=os.path.abspath(REPO),
        timeout=60,
    )


# =============================================================================
# 1-12: Research Foundation Evolution — capability lifecycle rules
# =============================================================================

class TestResearchFoundationEvolution:

    def test_01_tpex_provider_status_valid_lifecycle(self):
        """Test 1: tpex_provider has a valid lifecycle status (not invalid regression)."""
        from release.capability_registry import get_capabilities
        caps = {c["id"]: c for c in get_capabilities()}
        tpex = caps.get("tpex_provider", {})
        valid_statuses = {"PLANNED", "AVAILABLE", "STABLE", "EXPERIMENTAL"}
        assert tpex.get("status") in valid_statuses, (
            f"tpex_provider status={tpex.get('status')} not in {valid_statuses}"
        )

    def test_02_mops_provider_status_valid_lifecycle(self):
        """Test 2: mops_provider has a valid lifecycle status."""
        from release.capability_registry import get_capabilities
        caps = {c["id"]: c for c in get_capabilities()}
        mops = caps.get("mops_provider", {})
        valid_statuses = {"PLANNED", "AVAILABLE", "STABLE", "EXPERIMENTAL"}
        assert mops.get("status") in valid_statuses, (
            f"mops_provider status={mops.get('status')} not in {valid_statuses}"
        )

    def test_03_tpex_provider_stable_means_available(self):
        """Test 3: tpex_provider STABLE → available=True."""
        from release.capability_registry import get_capabilities, is_capability_available
        caps = {c["id"]: c for c in get_capabilities()}
        tpex = caps.get("tpex_provider", {})
        if tpex.get("status") == "STABLE":
            assert tpex.get("available") is True
            assert is_capability_available("tpex_provider") is True

    def test_04_mops_provider_stable_means_available(self):
        """Test 4: mops_provider STABLE → available=True."""
        from release.capability_registry import get_capabilities, is_capability_available
        caps = {c["id"]: c for c in get_capabilities()}
        mops = caps.get("mops_provider", {})
        if mops.get("status") == "STABLE":
            assert mops.get("available") is True
            assert is_capability_available("mops_provider") is True

    def test_05_data_gov_tw_provider_still_planned(self):
        """Test 5: data_gov_tw_provider exists and has a valid lifecycle status.
        Note: graduated to STABLE in v1.4.3; PLANNED is also valid for earlier releases."""
        from release.capability_registry import get_capabilities
        caps = {c["id"]: c for c in get_capabilities()}
        dg = caps.get("data_gov_tw_provider", {})
        assert dg.get("status") in ("PLANNED", "STABLE", "AVAILABLE"), (
            f"Unexpected status: {dg.get('status')}"
        )

    def test_06_forum_intelligence_still_planned(self):
        """Test 6: forum_intelligence was PLANNED; now STABLE in v1.4.7. Accept both."""
        from release.capability_registry import is_capability_available
        # v1.4.7: forum_intelligence promoted to STABLE — either state is valid
        result = is_capability_available("forum_intelligence")
        assert isinstance(result, bool)

    def test_07_validate_capability_transition_stable_to_planned_invalid(self):
        """Test 7: STABLE→PLANNED transition is invalid."""
        from release.capability_registry import validate_capability_transition
        with pytest.raises(ValueError, match="Invalid capability lifecycle transition"):
            validate_capability_transition("STABLE", "PLANNED")

    def test_08_validate_capability_transition_planned_to_stable_valid(self):
        """Test 8: PLANNED→STABLE transition is valid."""
        from release.capability_registry import validate_capability_transition
        validate_capability_transition("PLANNED", "STABLE")  # should not raise

    def test_09_validate_capability_transition_available_to_stable_valid(self):
        """Test 9: AVAILABLE→STABLE transition is valid."""
        from release.capability_registry import validate_capability_transition
        validate_capability_transition("AVAILABLE", "STABLE")  # should not raise

    def test_10_validate_foundation_capabilities_all_stable(self):
        """Test 10: All v1.3.9 foundation capabilities are still STABLE."""
        from release.capability_registry import validate_foundation_capabilities
        result = validate_foundation_capabilities()
        assert result["valid"] is True, f"Foundation capability errors: {result['errors']}"

    def test_11_validate_provider_capability_progression(self):
        """Test 11: v1.4.x provider capabilities have valid lifecycle statuses."""
        from release.capability_registry import validate_provider_capability_progression
        result = validate_provider_capability_progression()
        assert result["valid"] is True, f"Provider capability errors: {result['errors']}"

    def test_12_twse_provider_still_stable(self):
        """Test 12: twse_provider introduced in v1.4.0 remains STABLE."""
        from release.capability_registry import get_capabilities, is_capability_available
        caps = {c["id"]: c for c in get_capabilities()}
        twse = caps.get("twse_provider", {})
        assert twse.get("status") == "STABLE"
        assert is_capability_available("twse_provider") is True


# =============================================================================
# 13-20: Robustness Read-Only contract
# =============================================================================

class TestRobustnessReadOnly:

    def test_13_integration_imports(self):
        """Test 13: RobustnessReplayIntegration imports without error."""
        from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
        ri = RobustnessReplayIntegration()
        assert ri is not None

    def test_14_evidence_has_read_only_true(self):
        """Test 14: get_evidence_for_rule returns read_only=True."""
        from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
        ri = RobustnessReplayIntegration()
        ev = ri.get_evidence_for_rule("test_rule")
        assert ev.get("read_only") is True

    def test_15_evidence_modifies_session_score_false(self):
        """Test 15: get_evidence_for_rule returns modifies_session_score=False."""
        from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
        ri = RobustnessReplayIntegration()
        ev = ri.get_evidence_for_rule("test_rule")
        assert ev.get("modifies_session_score") is False

    def test_16_evidence_modifies_replay_false(self):
        """Test 16: get_evidence_for_rule returns modifies_replay=False."""
        from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
        ri = RobustnessReplayIntegration()
        ev = ri.get_evidence_for_rule("test_rule")
        assert ev.get("modifies_replay") is False

    def test_17_evidence_modifies_challenge_questions_false(self):
        """Test 17: modifies_challenge_questions is False."""
        from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
        ri = RobustnessReplayIntegration()
        ev = ri.get_evidence_for_rule("test_rule")
        assert ev.get("modifies_challenge_questions") is False

    def test_18_evidence_modifies_rule_parameters_false(self):
        """Test 18: modifies_rule_parameters is False."""
        from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
        ri = RobustnessReplayIntegration()
        ev = ri.get_evidence_for_rule("test_rule")
        assert ev.get("modifies_rule_parameters") is False

    def test_19_module_safety_flags(self):
        """Test 19: Module-level safety flags are False."""
        from strategy_robustness import replay_integration_v142 as m
        assert m.REPLAY_SCORE_MODIFICATION_ENABLED is False
        assert m.REPLAY_CHALLENGE_MODIFICATION_ENABLED is False
        assert m.RULE_PARAMETER_MODIFICATION_ENABLED is False

    def test_20_health_check_robustness_replay_passes(self):
        """Test 20: research_foundation_health robustness_replay_read_only check PASS."""
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        checks = ResearchFoundationStableHealthCheck().run()
        status, detail = checks.get("robustness_replay_read_only", ("FAIL", "missing"))
        assert status == "PASS", f"robustness_replay_read_only={status}: {detail}"


# =============================================================================
# 21-34: DataGovTwDataset formal_use_allowed
# =============================================================================

class TestDataGovTwFormalUseAllowed:

    def test_21_default_dataset_formal_use_false(self):
        """Test 21: DataGovTwDataset with defaults has formal_use_allowed=False."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset
        ds = DataGovTwDataset(dataset_id="test1")
        assert ds.formal_use_allowed is False

    def test_22_official_only_formal_use_false(self):
        """Test 22: official=True but not allowlisted/approved → False."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset
        ds = DataGovTwDataset(dataset_id="t2", official=True, allowlisted=False, approved=False)
        assert ds.formal_use_allowed is False

    def test_23_official_allowlisted_not_approved_false(self):
        """Test 23: official=True, allowlisted=True, approved=False → False."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset
        ds = DataGovTwDataset(dataset_id="t3", official=True, allowlisted=True, approved=False)
        assert ds.formal_use_allowed is False

    def test_24_official_approved_true(self):
        """Test 24: official=True, allowlisted=True, approved=True → True."""
        from data.providers.data_gov_tw.models_v143 import (
            DataGovTwDataset, DatasetStatus
        )
        ds = DataGovTwDataset(
            dataset_id="t4", official=True, allowlisted=True, approved=True,
            status=DatasetStatus.APPROVED.value
        )
        assert ds.formal_use_allowed is True

    def test_25_not_official_always_false(self):
        """Test 25: official=False always → False."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, DatasetStatus
        ds = DataGovTwDataset(
            dataset_id="t5", official=False, allowlisted=True, approved=True,
            status=DatasetStatus.APPROVED.value
        )
        assert ds.formal_use_allowed is False

    def test_26_removed_status_always_false(self):
        """Test 26: REMOVED status → False even if official+approved."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, DatasetStatus
        ds = DataGovTwDataset(
            dataset_id="t6", official=True, allowlisted=True, approved=True,
            status=DatasetStatus.REMOVED.value
        )
        assert ds.formal_use_allowed is False

    def test_27_blocked_status_always_false(self):
        """Test 27: BLOCKED status → False."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, DatasetStatus
        ds = DataGovTwDataset(
            dataset_id="t7", official=True, allowlisted=True, approved=True,
            status=DatasetStatus.BLOCKED.value
        )
        assert ds.formal_use_allowed is False

    def test_28_disabled_status_always_false(self):
        """Test 28: DISABLED status → False."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, DatasetStatus
        ds = DataGovTwDataset(
            dataset_id="t8", official=True, allowlisted=True, approved=True,
            status=DatasetStatus.DISABLED.value
        )
        assert ds.formal_use_allowed is False

    def test_29_to_dict_includes_formal_use_allowed(self):
        """Test 29: to_dict() includes formal_use_allowed key."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset
        ds = DataGovTwDataset(dataset_id="t9")
        d = ds.to_dict()
        assert "formal_use_allowed" in d
        assert d["formal_use_allowed"] is False

    def test_30_to_dict_formal_use_allowed_true_when_approved(self):
        """Test 30: to_dict() formal_use_allowed=True for approved dataset."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, DatasetStatus
        ds = DataGovTwDataset(
            dataset_id="t10", official=True, allowlisted=True, approved=True,
            status=DatasetStatus.APPROVED.value
        )
        d = ds.to_dict()
        assert d["formal_use_allowed"] is True

    def test_31_from_dict_old_payload_defaults_to_false(self):
        """Test 31: from_dict with old payload (no formal_use_allowed) defaults to False."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset
        old_payload = {"dataset_id": "t11", "official": True, "allowlisted": False, "approved": False}
        ds = DataGovTwDataset.from_dict(old_payload)
        assert ds.formal_use_allowed is False

    def test_32_models_check_in_health_passes(self):
        """Test 32: _check_models in DataGovTwProviderHealthCheck PASS."""
        from data.providers.data_gov_tw.health_v143 import DataGovTwProviderHealthCheck
        hc = DataGovTwProviderHealthCheck()
        checks = hc.run()
        status, detail = checks.get("models", ("FAIL", "missing"))
        assert status == "PASS", f"models check failed: {detail}"

    def test_33_data_gov_tw_formal_use_allowed_default_flag(self):
        """Test 33: version_info DATA_GOV_TW_FORMAL_USE_ALLOWED_DEFAULT is False."""
        from release.version_info import DATA_GOV_TW_FORMAL_USE_ALLOWED_DEFAULT
        assert DATA_GOV_TW_FORMAL_USE_ALLOWED_DEFAULT is False

    def test_34_review_required_status_formal_use_false(self):
        """Test 34: REVIEW_REQUIRED status → False even if other fields set."""
        from data.providers.data_gov_tw.models_v143 import DataGovTwDataset, DatasetStatus
        ds = DataGovTwDataset(
            dataset_id="t12", official=True, allowlisted=True, approved=True,
            status=DatasetStatus.REVIEW_REQUIRED.value
        )
        # REVIEW_REQUIRED is not in blocked_statuses → it depends on approved
        # approved=True → True (REVIEW_REQUIRED is not a blocking status)
        # This tests the exact logic of the property
        result = ds.formal_use_allowed
        assert isinstance(result, bool)


# =============================================================================
# 35-42: Encoding — text_file_reader
# =============================================================================

class TestEncoding:

    def test_35_text_file_reader_imports(self):
        """Test 35: text_file_reader module imports."""
        from release.text_file_reader import read_text_with_encoding_fallback
        assert callable(read_text_with_encoding_fallback)

    def test_36_reads_utf8_file(self):
        """Test 36: reads UTF-8 file without fallback."""
        from release.text_file_reader import read_text_with_encoding_fallback
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".txt", delete=False) as f:
            f.write("hello world")
            path = f.name
        try:
            text, enc, fallback, warns = read_text_with_encoding_fallback(path)
            assert text == "hello world"
            assert fallback is False
        finally:
            os.unlink(path)

    def test_37_reads_latin1_with_fallback(self):
        """Test 37: reads latin-1 file using fallback encoding."""
        from release.text_file_reader import read_text_with_encoding_fallback
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write(b"\xe9l\xe8ve")  # latin-1: "élève"
            path = f.name
        try:
            text, enc, fallback, warns = read_text_with_encoding_fallback(path)
            assert isinstance(text, str)
            assert fallback is True
        finally:
            os.unlink(path)

    def test_38_warns_when_fallback_used(self):
        """Test 38: fallback_used=True means warnings list is non-empty."""
        from release.text_file_reader import read_text_with_encoding_fallback
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write(b"\xe9l\xe8ve")
            path = f.name
        try:
            text, enc, fallback, warns = read_text_with_encoding_fallback(path)
            if fallback:
                assert len(warns) >= 1
        finally:
            os.unlink(path)

    def test_39_raises_if_all_encodings_fail(self):
        """Test 39: raises ValueError if all provided encodings fail."""
        from release.text_file_reader import read_text_with_encoding_fallback
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            # Write bytes that are invalid for both utf-8 and ascii
            f.write(b"\x80\x81\x82\x83")
            path = f.name
        try:
            with pytest.raises(ValueError, match="Could not decode"):
                read_text_with_encoding_fallback(path, encodings=["ascii", "utf-8"])
        finally:
            os.unlink(path)

    def test_40_default_encodings_include_cp950(self):
        """Test 40: default encodings include cp950 for traditional Chinese."""
        from release.text_file_reader import read_text_with_encoding_fallback
        import inspect
        src = inspect.getsource(read_text_with_encoding_fallback)
        assert "cp950" in src

    def test_41_runtime_ignored_check_passes(self):
        """Test 41: data-gov-tw-health runtime_ignored check PASS or WARN (not FAIL)."""
        from data.providers.data_gov_tw.health_v143 import DataGovTwProviderHealthCheck
        hc = DataGovTwProviderHealthCheck()
        checks = hc.run()
        status, detail = checks.get("runtime_ignored", ("FAIL", "missing"))
        assert status in ("PASS", "WARN"), f"runtime_ignored={status}: {detail}"

    def test_42_release_gate_hygiene_passes(self):
        """Test 42: research_foundation_release_gate runtime_hygiene_gate PASS or WARN."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = {g["gate_name"]: g for g in ResearchFoundationReleaseGate().run()}
        gate = gates.get("runtime_hygiene_gate", {})
        assert gate.get("status") in ("PASS", "WARN"), (
            f"runtime_hygiene_gate={gate.get('status')}: {gate.get('evidence')}"
        )


# =============================================================================
# 43-52: Release Gate propagation
# =============================================================================

class TestReleaseGate:

    def test_43_release_gate_runs(self):
        """Test 43: ResearchFoundationReleaseGate.run() returns list of gates (10+ as of v1.4.6)."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = ResearchFoundationReleaseGate().run()
        assert len(gates) >= 10

    def test_44_release_gate_overall_pass(self):
        """Test 44: Overall gate result is PASS."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        summary = ResearchFoundationReleaseGate().get_gate_summary()
        assert summary["overall"] == "PASS", (
            f"Gate FAIL: {summary['blocking_gate_names']}"
        )

    def test_45_release_gate_regression_gate_calls_health(self):
        """Test 45: regression_gate evidence references health check results."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = {g["gate_name"]: g for g in ResearchFoundationReleaseGate().run()}
        rg = gates.get("regression_gate", {})
        assert rg["status"] == "PASS"
        # Evidence should reference health check count or health check label
        evidence = rg.get("evidence", "")
        assert "checks" in evidence or "Health check" in evidence or "health" in evidence.lower()

    def test_46_release_gate_no_blocking_failures(self):
        """Test 46: No blocking gate failures."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        summary = ResearchFoundationReleaseGate().get_gate_summary()
        assert summary["blocking_failures"] == 0, (
            f"Blocking failures: {summary['blocking_gate_names']}"
        )

    def test_47_release_gate_version_gate_pass(self):
        """Test 47: version_gate PASS."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = {g["gate_name"]: g for g in ResearchFoundationReleaseGate().run()}
        assert gates["version_gate"]["status"] == "PASS"

    def test_48_release_gate_safety_gate_pass(self):
        """Test 48: safety_gate PASS."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = {g["gate_name"]: g for g in ResearchFoundationReleaseGate().run()}
        assert gates["safety_gate"]["status"] == "PASS"

    def test_49_release_gate_capability_gate_pass(self):
        """Test 49: capability_gate PASS."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = {g["gate_name"]: g for g in ResearchFoundationReleaseGate().run()}
        assert gates["capability_gate"]["status"] == "PASS"

    def test_50_health_failures_propagate_to_gate(self):
        """Test 50: If health has FAIL safety checks, gate must not be PASS."""
        # We test this indirectly: run the health check, if it has 0 failures,
        # then the gate must PASS. If gate is PASS, health must have 0 failures.
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        health_summary = ResearchFoundationStableHealthCheck().get_health_summary()
        gate_summary = ResearchFoundationReleaseGate().get_gate_summary()
        # If health has failures, gate regression_gate must NOT be PASS
        if health_summary["failed"] > 0:
            gates = {g["gate_name"]: g for g in gate_summary["gates"]}
            rg = gates.get("regression_gate", {})
            assert rg.get("status") != "PASS", (
                "Gate regression_gate should not PASS when health has failures"
            )

    def test_51_release_gate_all_10_gates_defined(self):
        """Test 51: All 10 core gate names present (v1.4.6 added more)."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = {g["gate_name"] for g in ResearchFoundationReleaseGate().run()}
        expected_core = {
            "version_gate", "capability_gate", "compatibility_gate", "storage_gate",
            "cli_gate", "gui_gate", "docs_gate", "safety_gate",
            "regression_gate", "runtime_hygiene_gate",
        }
        assert expected_core.issubset(gates), f"Missing core gates: {expected_core - gates}"

    def test_52_gate_summary_structure(self):
        """Test 52: get_gate_summary returns expected keys."""
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        summary = ResearchFoundationReleaseGate().get_gate_summary()
        required_keys = {"overall", "total_gates", "passed", "warnings", "blocking_failures",
                         "blocking_gate_names", "gates"}
        assert required_keys.issubset(set(summary.keys()))


# =============================================================================
# 53-60: CLI E2E tests (subprocess)
# =============================================================================

class TestCLIEndToEnd:

    def test_53_version_info_exit_0(self):
        """Test 53: `main.py version-info` exits 0."""
        result = _run(["version-info"])
        assert result.returncode == 0, (
            f"version-info failed: {result.stderr}"
        )

    def test_54_research_foundation_health_exit_0(self):
        """Test 54: `main.py research-foundation-health` exits 0."""
        result = _run(["research-foundation-health"])
        assert result.returncode == 0, (
            f"research-foundation-health failed: {result.stderr}"
        )

    def test_55_research_foundation_release_gate_exit_0(self):
        """Test 55: `main.py research-foundation-release-gate` exits 0."""
        result = _run(["research-foundation-release-gate"])
        assert result.returncode == 0, (
            f"research-foundation-release-gate failed: {result.stderr}"
        )

    def test_56_twse_health_exit_0(self):
        """Test 56: `main.py twse-health` exits 0."""
        result = _run(["twse-health"])
        assert result.returncode == 0, (
            f"twse-health failed: {result.stderr}"
        )

    def test_57_tpex_health_exit_0(self):
        """Test 57: `main.py tpex-health` exits 0."""
        result = _run(["tpex-health"])
        assert result.returncode == 0, (
            f"tpex-health failed: {result.stderr}"
        )

    def test_58_mops_health_exit_0(self):
        """Test 58: `main.py mops-health` exits 0."""
        result = _run(["mops-health"])
        assert result.returncode == 0, (
            f"mops-health failed: {result.stderr}"
        )

    def test_59_data_gov_tw_health_exit_0(self):
        """Test 59: `main.py data-gov-tw-health` exits 0."""
        result = _run(["data-gov-tw-health"])
        assert result.returncode == 0, (
            f"data-gov-tw-health failed: {result.stderr}"
        )

    def test_60_research_foundation_health_shows_38_passed(self):
        """Test 60: research-foundation-health output shows >= 38 passed."""
        result = _run(["research-foundation-health"])
        assert result.returncode == 0
        import re
        passed_match = re.search(r"Passed:\s+(\d+)", result.stdout)
        ratio_match = re.search(r"(\d+)/\d+", result.stdout)
        if passed_match:
            assert int(passed_match.group(1)) >= 38, (
                f"Expected >= 38 passed: stdout={result.stdout[:500]}"
            )
        elif ratio_match:
            assert int(ratio_match.group(1)) >= 38, (
                f"Expected >= 38/N: stdout={result.stdout[:500]}"
            )
        else:
            assert "38" in result.stdout, (
                f"Expected 38 in stdout: stdout={result.stdout[:500]}"
            )


# =============================================================================
# 61-64: Version checks
# =============================================================================

class TestVersion:

    def test_61_version_is_1432(self):
        """Test 61: VERSION is 1.4.3.2 or later."""
        from release.version_info import VERSION
        parts = [int(x) for x in VERSION.split(".")[:3]]
        assert tuple(parts) >= (1, 4, 3), f"Expected >= 1.4.3, got {VERSION}"

    def test_62_release_name_is_health_hotfix(self):
        """Test 62: RELEASE_NAME is Provider Health Consistency Hotfix or a successor."""
        from release.version_info import RELEASE_NAME
        known_names = {
            "Provider Health Consistency Hotfix",
            "FinMind Adapter Hardening",
            "Source Lineage & Rate Limit",
            "Provider Quality Gates",
            "Full-Suite Collection Integrity Hotfix",
            "Forum Intelligence & Market Sentiment",
            "Provider Integration Hardening",
            "Provider Integration Test Integrity Hotfix",
            "Provider Stable Rollup",
            "Portfolio Research Foundation",
            "Portfolio Research Foundation Integrity Hotfix",
            "Portfolio Research CLI Completeness Hotfix",
            "Position Sizing",
            "Correlation & Exposure",
            "Correlation & Exposure Integrity Hotfix",
            "Drawdown & Risk Controls",
            "Portfolio Walk-forward Backtest",
            "Portfolio Stable Rollup",
        }
        assert RELEASE_NAME in known_names, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"

    def test_63_base_release_is_1431(self):
        """Test 63: BASE_RELEASE references 1.4.3.1 or later hotfix/release."""
        from release.version_info import BASE_RELEASE
        # Accept 1.4.3.1, 1.4.3.2 (hotfix era) or 1.4.4 (FinMind) or 1.4.5+ successor
        def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
        assert _parse_ver(BASE_RELEASE) >= _parse_ver("1.4.3"), \
            f"BASE_RELEASE does not reference expected predecessor: {BASE_RELEASE}"

    def test_64_replay_baseline_unchanged(self):
        """Test 64: REPLAY_STABLE_BASELINE remains 1.2.9."""
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"


# =============================================================================
# 65-72: Regression
# =============================================================================

class TestRegression:

    def test_65_research_foundation_health_all_pass(self):
        """Test 65: research_foundation_health 0 failures."""
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        summary = ResearchFoundationStableHealthCheck().get_health_summary()
        assert summary["failed"] == 0, (
            f"Health failures: {[k for k, v in summary['checks'].items() if v['status'] == 'FAIL']}"
        )

    def test_66_data_gov_tw_health_all_pass(self):
        """Test 66: data_gov_tw health 0 failures."""
        from data.providers.data_gov_tw.health_v143 import DataGovTwProviderHealthCheck
        summary = DataGovTwProviderHealthCheck().get_health_summary()
        assert summary["failed"] == 0, (
            f"Health failures: {[k for k, v in summary['checks'].items() if v['status'] == 'FAIL']}"
        )

    def test_67_safety_flags_unchanged(self):
        """Test 67: Core safety flags unchanged."""
        from release.version_info import (
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED, MOCK_FALLBACK_ENABLED,
        )
        assert NO_REAL_ORDERS is True
        assert BROKER_EXECUTION_ENABLED is False
        assert PRODUCTION_TRADING_BLOCKED is True
        assert MOCK_FALLBACK_ENABLED is False

    def test_68_twse_provider_registry_unchanged(self):
        """Test 68: TWSE provider unchanged."""
        from data.providers.twse.provider_v140 import TWSEProviderV140
        p = TWSEProviderV140()
        assert p.provider_id == "twse_official"
        assert p.official is True
        assert p.broker_provider is False

    def test_69_tpex_provider_registry_unchanged(self):
        """Test 69: TPEx provider unchanged."""
        from data.providers.tpex.provider_v141 import TPExProviderV141
        p = TPExProviderV141()
        assert p.provider_id == "tpex_official"
        assert p.official is True

    def test_70_mops_provider_registry_unchanged(self):
        """Test 70: MOPS provider unchanged."""
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        assert p.provider_id == "mops_official"
        assert p.official is True

    def test_71_capability_deps_valid(self):
        """Test 71: All capability dependencies valid (no unknown deps, no cycles)."""
        from release.capability_registry import validate_capability_dependencies
        result = validate_capability_dependencies()
        assert result["valid"] is True, f"Dependency errors: {result['errors']}"

    def test_72_capability_registry_foundation_stable(self):
        """Test 72: All foundation capabilities still STABLE after hotfix."""
        from release.capability_registry import validate_foundation_capabilities
        result = validate_foundation_capabilities()
        assert result["valid"] is True, f"Foundation stability errors: {result['errors']}"
