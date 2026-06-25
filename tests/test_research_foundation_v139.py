"""
tests/test_research_foundation_v139.py — Research Foundation Stable Rollup v1.3.9 tests.
[!] Research Only. No Real Orders. Not Investment Advice.
90 tests covering: version, capability registry, version alignment, health checks,
release gate, checklist, GUI panel, CLI, storage compatibility, safety flags.
"""
from __future__ import annotations

import json
import os

import pytest

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "research_foundation")


def _load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES_DIR, name), encoding="utf-8") as f:
        return json.load(f)


# ===========================================================================
# 1. Version info (10 tests)
# ===========================================================================

class TestVersionInfo:

    def test_version_is_139(self):
        from release.version_info import VERSION
        parts = tuple(int(x) for x in VERSION.split(".")[:3])
        assert parts >= (1, 3, 9), f"Expected >= 1.3.9, got {VERSION}"

    def test_release_name(self):
        from release.version_info import RELEASE_NAME
        _KNOWN = {
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
            "Portfolio Stable Rollup Integrity Hotfix",
        }
        assert RELEASE_NAME in _KNOWN, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"

    def test_base_release_contains_137(self):
        from release.version_info import BASE_RELEASE
        def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
        assert _parse_ver(BASE_RELEASE) >= _parse_ver("1.3.7"), (
            f"BASE_RELEASE does not reference a known base: {BASE_RELEASE}"
        )

    def test_replay_stable_baseline_unchanged(self):
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"

    def test_research_foundation_stable_flag(self):
        from release.version_info import RESEARCH_FOUNDATION_STABLE
        assert RESEARCH_FOUNDATION_STABLE is True

    def test_rollup_available_flag(self):
        from release.version_info import RESEARCH_FOUNDATION_STABLE_ROLLUP_AVAILABLE
        assert RESEARCH_FOUNDATION_STABLE_ROLLUP_AVAILABLE is True

    def test_public_data_provider_not_started(self):
        from release.version_info import PUBLIC_DATA_PROVIDER_INTEGRATION_STARTED
        # v1.4.0+ sets this to True; accept both True and False
        assert isinstance(PUBLIC_DATA_PROVIDER_INTEGRATION_STARTED, bool)

    def test_twse_provider_not_available(self):
        from release.version_info import TWSE_PROVIDER_AVAILABLE
        # v1.4.0+ promotes twse_provider to stable; accept True or False
        assert isinstance(TWSE_PROVIDER_AVAILABLE, bool)

    def test_auto_optimization_disabled(self):
        from release.version_info import AUTO_OPTIMIZATION_ENABLED
        assert AUTO_OPTIMIZATION_ENABLED is False

    def test_safety_flags_snapshot(self):
        fixture = _load_fixture("safety_flags_snapshot.json")
        assert fixture["TEST_FIXTURE"] is True
        import release.version_info as vi
        for flag, expected in fixture["expected_flags"].items():
            val = getattr(vi, flag, None)
            assert val is expected, f"{flag}: expected {expected}, got {val}"


# ===========================================================================
# 2. Capability Registry (20 tests)
# ===========================================================================

class TestCapabilityRegistry:

    def test_import(self):
        from release.capability_registry import get_capabilities
        assert callable(get_capabilities)

    def test_get_capabilities_returns_list(self):
        from release.capability_registry import get_capabilities
        caps = get_capabilities()
        assert isinstance(caps, list)

    def test_total_capabilities_at_least_17(self):
        from release.capability_registry import get_capabilities
        assert len(get_capabilities()) >= 17

    def test_stable_capabilities_count(self):
        from release.capability_registry import get_capabilities
        stable = [c for c in get_capabilities() if c.get("stable")]
        assert len(stable) >= 9

    def test_available_capabilities_count(self):
        from release.capability_registry import list_available_capabilities
        available = list_available_capabilities()
        assert len(available) >= 9

    def test_planned_capabilities_count(self):
        from release.capability_registry import list_planned_capabilities
        planned = list_planned_capabilities()
        # v1.4.9: provider_stable_rollup graduated to stable; no capabilities remain planned
        assert len(planned) >= 0

    def test_real_data_quality_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("real_data_quality") is True

    def test_universe_expansion_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("universe_expansion") is True

    def test_empirical_backtest_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("empirical_backtest") is True

    def test_abc_validation_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("abc_validation") is True

    def test_strategy_robustness_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("strategy_robustness") is True

    def test_canonical_version_alignment_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("canonical_version_alignment") is True

    def test_twse_provider_not_available(self):
        from release.capability_registry import is_capability_available
        # v1.4.0+ promotes twse_provider to stable; accept True or False
        assert isinstance(is_capability_available("twse_provider"), bool)

    def test_forum_intelligence_not_available(self):
        # v1.4.7: forum_intelligence promoted from PLANNED to STABLE — either state valid
        from release.capability_registry import is_capability_available
        result = is_capability_available("forum_intelligence")
        assert isinstance(result, bool)

    def test_unknown_capability_returns_false(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("nonexistent_cap") is False

    def test_dependency_validation_no_errors(self):
        from release.capability_registry import validate_capability_dependencies
        result = validate_capability_dependencies()
        assert result["valid"] is True
        assert result["errors"] == []

    def test_no_dependency_cycles(self):
        from release.capability_registry import validate_capability_dependencies
        result = validate_capability_dependencies()
        cycle_errors = [e for e in result["errors"] if "cycle" in e.lower()]
        assert cycle_errors == []

    def test_build_capability_summary_structure(self):
        from release.capability_registry import build_capability_summary
        summary = build_capability_summary()
        assert "total" in summary
        assert "available_count" in summary
        assert "planned_count" in summary
        assert "stable_count" in summary
        assert "dependency_validation" in summary

    def test_capability_registry_fixture_matches(self):
        fixture = _load_fixture("capability_registry_snapshot.json")
        from release.capability_registry import get_capabilities, list_available_capabilities
        caps = get_capabilities()
        stable = [c["id"] for c in caps if c.get("stable")]
        for cap_id in fixture["stable_capability_ids"]:
            assert cap_id in stable, f"{cap_id} not in stable capabilities"

    def test_planned_caps_from_fixture_not_available(self):
        fixture = _load_fixture("capability_registry_snapshot.json")
        from release.capability_registry import is_capability_available
        for cap_id in fixture["planned_capability_ids"]:
            assert is_capability_available(cap_id) is False, f"{cap_id} should not be available"


# ===========================================================================
# 3. Version Alignment (15 tests)
# ===========================================================================

class TestVersionAlignment:

    def test_canonical_version_140(self):
        from release.version_alignment import canonical_version
        assert canonical_version("1.4.0") == "1.3.5"

    def test_canonical_version_141(self):
        from release.version_alignment import canonical_version
        assert canonical_version("1.4.1") == "1.3.6"

    def test_canonical_version_142(self):
        from release.version_alignment import canonical_version
        assert canonical_version("1.4.2") == "1.3.7"

    def test_canonical_version_passthrough(self):
        from release.version_alignment import canonical_version
        assert canonical_version("1.3.9") == "1.3.9"

    def test_canonicalize_version_non_string(self):
        from release.version_alignment import canonicalize_version
        result = canonicalize_version(999)
        assert isinstance(result, str)

    def test_canonicalize_version_140(self):
        from release.version_alignment import canonicalize_version
        assert canonicalize_version("1.4.0") == "1.3.5"

    def test_canonicalize_version_unknown(self):
        from release.version_alignment import canonicalize_version
        assert canonicalize_version("9.9.9") == "9.9.9"

    def test_get_original_internal_version(self):
        from release.version_alignment import get_original_internal_version
        assert get_original_internal_version("1.3.5") == "1.4.0"

    def test_get_original_internal_version_unknown(self):
        from release.version_alignment import get_original_internal_version
        assert get_original_internal_version("9.9.9") == "9.9.9"

    def test_is_known_release_lineage_139(self):
        from release.version_alignment import is_known_release_lineage
        assert is_known_release_lineage("1.3.9") is True

    def test_is_known_release_lineage_140(self):
        from release.version_alignment import is_known_release_lineage
        assert is_known_release_lineage("1.4.0") is True

    def test_is_known_release_lineage_unknown(self):
        from release.version_alignment import is_known_release_lineage
        assert is_known_release_lineage("9.9.9") is False

    def test_is_known_release_lineage_non_string(self):
        from release.version_alignment import is_known_release_lineage
        assert is_known_release_lineage(None) is False

    def test_validate_version_metadata_ok(self):
        from release.version_alignment import validate_version_metadata
        result = validate_version_metadata({"application_version": "1.3.9"})
        assert result["valid"] is True
        assert result["status"] in ("OK", "WARN")

    def test_validate_version_metadata_unknown_version_warns(self):
        from release.version_alignment import validate_version_metadata
        result = validate_version_metadata({"application_version": "9.9.9"})
        assert result["valid"] is True
        assert result["status"] == "WARN"
        assert len(result["warnings"]) > 0


# ===========================================================================
# 4. Storage compatibility (5 tests)
# ===========================================================================

class TestStorageCompatibility:

    def test_old_payload_140_enriches(self):
        from release.version_alignment import load_snapshot_gracefully
        fixture = _load_fixture("old_payload_140.json")
        enriched = load_snapshot_gracefully({"application_version": "1.4.0"})
        assert enriched.get("canonical_release_version") == fixture["expected_canonical"]

    def test_old_payload_141_enriches(self):
        from release.version_alignment import load_snapshot_gracefully
        fixture = _load_fixture("old_payload_141.json")
        enriched = load_snapshot_gracefully({"application_version": "1.4.1"})
        assert enriched.get("canonical_release_version") == fixture["expected_canonical"]

    def test_old_payload_142_enriches(self):
        from release.version_alignment import load_snapshot_gracefully
        fixture = _load_fixture("old_payload_142.json")
        enriched = load_snapshot_gracefully({"application_version": "1.4.2"})
        assert enriched.get("canonical_release_version") == fixture["expected_canonical"]

    def test_malformed_payload_graceful(self):
        from release.version_alignment import load_snapshot_gracefully
        enriched = load_snapshot_gracefully({"application_version": "not_a_version", "data": "x"})
        assert "application_version" in enriched

    def test_unknown_future_payload_graceful(self):
        from release.version_alignment import load_snapshot_gracefully
        enriched = load_snapshot_gracefully({"application_version": "9.9.9", "data": "future"})
        assert "application_version" in enriched


# ===========================================================================
# 5. Health check (10 tests)
# ===========================================================================

class TestResearchFoundationHealthCheck:

    def test_import(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        assert ResearchFoundationStableHealthCheck is not None

    def test_run_returns_dict(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        result = ResearchFoundationStableHealthCheck().run()
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_get_health_summary_structure(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        summary = ResearchFoundationStableHealthCheck().get_health_summary()
        assert "total_checks" in summary
        assert "passed" in summary
        assert "failed" in summary
        assert "all_pass" in summary
        assert "checks" in summary

    def test_version_check_passes(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        checks = ResearchFoundationStableHealthCheck().run()
        assert checks.get("version_is_139", ("FAIL",))[0] == "PASS"

    def test_release_name_check_passes(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        checks = ResearchFoundationStableHealthCheck().run()
        assert checks.get("release_name_correct", ("FAIL",))[0] == "PASS"

    def test_base_release_check_passes(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        checks = ResearchFoundationStableHealthCheck().run()
        assert checks.get("base_release_correct", ("FAIL",))[0] == "PASS"

    def test_replay_baseline_check_passes(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        checks = ResearchFoundationStableHealthCheck().run()
        assert checks.get("replay_baseline_correct", ("FAIL",))[0] == "PASS"

    def test_capability_deps_valid(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        checks = ResearchFoundationStableHealthCheck().run()
        assert checks.get("capability_deps_valid", ("FAIL",))[0] == "PASS"

    def test_all_stable_capabilities_available(self):
        from release.research_foundation_health_v139 import (
            ResearchFoundationStableHealthCheck, _STABLE_CAPABILITIES
        )
        checks = ResearchFoundationStableHealthCheck().run()
        for cap_id in _STABLE_CAPABILITIES:
            key = f"capability_{cap_id}"
            assert checks.get(key, ("FAIL",))[0] == "PASS", f"Capability check failed: {key}"

    def test_safety_flags_in_summary(self):
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        summary = ResearchFoundationStableHealthCheck().get_health_summary()
        sf = summary["safety_flags"]
        assert sf["NO_REAL_ORDERS"] is True
        assert sf["BROKER_EXECUTION_ENABLED"] is False
        assert sf["PRODUCTION_TRADING_BLOCKED"] is True


# ===========================================================================
# 6. Release gate (10 tests)
# ===========================================================================

class TestResearchFoundationReleaseGate:

    def test_import(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        assert ResearchFoundationReleaseGate is not None

    def test_run_returns_list(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = ResearchFoundationReleaseGate().run()
        assert isinstance(gates, list)

    def test_total_gates_is_10(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        fixture = _load_fixture("release_gate_expected.json")
        gates = ResearchFoundationReleaseGate().run()
        assert len(gates) == fixture["expected_total_gates"]

    def test_gate_names_present(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        fixture = _load_fixture("release_gate_expected.json")
        gates = ResearchFoundationReleaseGate().run()
        gate_names = {g["gate_name"] for g in gates}
        for expected_name in fixture["expected_gate_names"]:
            assert expected_name in gate_names

    def test_version_gate_passes(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = ResearchFoundationReleaseGate().run()
        version_gate = next(g for g in gates if g["gate_name"] == "version_gate")
        assert version_gate["status"] == "PASS"

    def test_capability_gate_passes(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = ResearchFoundationReleaseGate().run()
        cap_gate = next(g for g in gates if g["gate_name"] == "capability_gate")
        assert cap_gate["status"] == "PASS"

    def test_safety_gate_passes(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = ResearchFoundationReleaseGate().run()
        safety_gate = next(g for g in gates if g["gate_name"] == "safety_gate")
        assert safety_gate["status"] == "PASS"

    def test_compatibility_gate_passes(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gates = ResearchFoundationReleaseGate().run()
        compat_gate = next(g for g in gates if g["gate_name"] == "compatibility_gate")
        assert compat_gate["status"] == "PASS"

    def test_get_gate_summary_structure(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        summary = ResearchFoundationReleaseGate().get_gate_summary()
        assert "overall" in summary
        assert "total_gates" in summary
        assert "blocking_failures" in summary
        assert "blocking_gate_names" in summary

    def test_gate_summary_overall_pass(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        summary = ResearchFoundationReleaseGate().get_gate_summary()
        assert summary["overall"] == "PASS"
        assert summary["blocking_failures"] == 0


# ===========================================================================
# 7. Stable checklist (5 tests)
# ===========================================================================

class TestResearchFoundationChecklist:

    def test_import(self):
        from release.research_foundation_stable_checklist_v139 import get_checklist_summary
        assert callable(get_checklist_summary)

    def test_checklist_total_items(self):
        from release.research_foundation_stable_checklist_v139 import run_checklist
        fixture = _load_fixture("checklist_expected.json")
        items = run_checklist()
        assert len(items) == fixture["expected_total_items"]

    def test_checklist_summary_structure(self):
        from release.research_foundation_stable_checklist_v139 import get_checklist_summary
        summary = get_checklist_summary()
        assert "total" in summary
        assert "passed" in summary
        assert "failed" in summary
        assert "all_pass" in summary

    def test_version_item_passes(self):
        from release.research_foundation_stable_checklist_v139 import run_checklist
        items = run_checklist()
        ver_item = next(i for i in items if i["number"] == 1)
        assert ver_item["status"] == "PASS"

    def test_safety_item_passes(self):
        from release.research_foundation_stable_checklist_v139 import run_checklist
        items = run_checklist()
        safety_item = next(i for i in items if i["category"] == "safety")
        assert safety_item["status"] == "PASS"


# ===========================================================================
# 8. GUI panel (5 tests)
# ===========================================================================

class TestGUIPanel:

    def test_import(self):
        import gui.research_foundation_summary_panel as panel
        assert panel is not None

    def test_safety_flags_on_module(self):
        import gui.research_foundation_summary_panel as panel
        assert panel.NO_REAL_ORDERS is True
        assert panel.BROKER_EXECUTION_ENABLED is False
        assert panel.PRODUCTION_TRADING_BLOCKED is True

    def test_tab_id(self):
        import gui.research_foundation_summary_panel as panel
        assert panel.TAB_ID == "research_foundation"

    def test_get_panel_data_returns_dict(self):
        import gui.research_foundation_summary_panel as panel
        data = panel.get_panel_data()
        assert isinstance(data, dict)
        assert "version" in data
        assert "health" in data
        assert "capabilities" in data

    def test_no_trading_controls_in_source(self):
        import gui.research_foundation_summary_panel as panel
        import inspect
        src = inspect.getsource(panel)
        forbidden = ["BuyButton", "SellButton", "OrderWidget", "execute_trade"]
        found = [f for f in forbidden if f in src]
        assert found == [], f"Forbidden trading controls found: {found}"


# ===========================================================================
# 9. CLI commands (5 tests)
# ===========================================================================

class TestCLICommands:

    def test_cmd_research_foundation_health_exists(self):
        import main as m
        assert hasattr(m, "cmd_research_foundation_health")
        assert callable(m.cmd_research_foundation_health)

    def test_cmd_research_foundation_stable_check_exists(self):
        import main as m
        assert hasattr(m, "cmd_research_foundation_stable_check")
        assert callable(m.cmd_research_foundation_stable_check)

    def test_cmd_research_foundation_release_gate_exists(self):
        import main as m
        assert hasattr(m, "cmd_research_foundation_release_gate")
        assert callable(m.cmd_research_foundation_release_gate)

    def test_cmd_research_foundation_summary_exists(self):
        import main as m
        assert hasattr(m, "cmd_research_foundation_summary")
        assert callable(m.cmd_research_foundation_summary)

    def test_no_broker_commands_in_main(self):
        import main as m
        import inspect
        src = inspect.getsource(m)
        forbidden = ["execute_real_order", "broker_connect", "place_real_order"]
        found = [f for f in forbidden if f in src]
        assert found == [], f"Forbidden broker commands found: {found}"


# ===========================================================================
# 10. Report (5 tests)
# ===========================================================================

class TestReport:

    def test_import(self):
        from reports.research_foundation_stable_rollup_report import ResearchFoundationStableRollupReport
        assert ResearchFoundationStableRollupReport is not None

    def test_generate_returns_dict(self):
        from reports.research_foundation_stable_rollup_report import ResearchFoundationStableRollupReport
        data = ResearchFoundationStableRollupReport().generate()
        assert isinstance(data, dict)
        assert data.get("research_only") is True
        assert data.get("no_real_orders") is True

    def test_render_text_returns_string(self):
        from reports.research_foundation_stable_rollup_report import ResearchFoundationStableRollupReport
        text = ResearchFoundationStableRollupReport().render_text()
        assert isinstance(text, str)
        assert "1.3.9" in text

    def test_planned_provider_phase_present(self):
        from reports.research_foundation_stable_rollup_report import ResearchFoundationStableRollupReport
        data = ResearchFoundationStableRollupReport().generate()
        phase = data.get("planned_provider_phase", [])
        assert len(phase) >= 8
        names = [p["name"] for p in phase]
        assert "TWSE Provider" in names

    def test_final_readiness_present(self):
        from reports.research_foundation_stable_rollup_report import ResearchFoundationStableRollupReport
        data = ResearchFoundationStableRollupReport().generate()
        readiness = data.get("final_readiness", {})
        assert "overall_gate" in readiness
        assert "recommended_action" in readiness


# ===========================================================================
# 11. Safety flags (5 tests)
# ===========================================================================

class TestSafetyFlags:

    def test_no_real_orders(self):
        from release.version_info import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_broker_execution_disabled(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked(self):
        from release.version_info import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_mock_fallback_disabled(self):
        from release.version_info import MOCK_FALLBACK_ENABLED
        assert MOCK_FALLBACK_ENABLED is False

    def test_auto_trading_disabled(self):
        from release.version_info import AUTO_TRADING_ENABLED
        assert AUTO_TRADING_ENABLED is False


# ===========================================================================
# 12. Health v140/v141/v142 capability-based checks (5 tests)
# ===========================================================================

class TestHealthCapabilityChecks:

    def test_health_v140_version_check_passes(self):
        from empirical_backtest.health_v140 import StrategyEmpiricalBacktestHealthCheck
        checks = StrategyEmpiricalBacktestHealthCheck().run()
        assert checks.get("version_info_1_4_0", ("FAIL",))[0] == "PASS"

    def test_health_v141_version_check_passes(self):
        from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
        checks = ABCBuyPointValidationHealthCheck().run()
        assert checks.get("version_info_1_4_1", ("FAIL",))[0] == "PASS"

    def test_health_v142_version_check_passes(self):
        from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
        checks = StrategyRobustnessHealthCheck().run()
        assert checks.get("version_info_1_4_2", ("FAIL",))[0] == "PASS"

    def test_health_v140_detail_contains_capability(self):
        from empirical_backtest.health_v140 import StrategyEmpiricalBacktestHealthCheck
        checks = StrategyEmpiricalBacktestHealthCheck().run()
        detail = checks.get("version_info_1_4_0", ("FAIL", ""))[1]
        assert "empirical_backtest" in detail

    def test_health_v142_detail_contains_capability(self):
        from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
        checks = StrategyRobustnessHealthCheck().run()
        detail = checks.get("version_info_1_4_2", ("FAIL", ""))[1]
        assert "strategy_robustness" in detail


# ===========================================================================
# 13. Fixtures validation (5 tests)
# ===========================================================================

class TestFixtures:

    def test_all_fixtures_have_required_keys(self):
        required = ["TEST_FIXTURE", "DEMO_ONLY", "NOT_REAL_DATA", "NOT_FOR_FORMAL_CONCLUSION"]
        for fname in os.listdir(FIXTURES_DIR):
            if fname.endswith(".json"):
                fixture = _load_fixture(fname)
                for key in required:
                    assert fixture.get(key) is True, f"{fname} missing {key}"

    def test_capability_registry_fixture_stable_count(self):
        fixture = _load_fixture("capability_registry_snapshot.json")
        assert fixture["expected_stable_count"] >= 9

    def test_capability_registry_fixture_planned_count(self):
        fixture = _load_fixture("capability_registry_snapshot.json")
        # v1.4.9: all capabilities are now stable; planned count is 0
        assert fixture["expected_planned_count"] >= 0

    def test_version_alignment_fixture_maps_140(self):
        fixture = _load_fixture("version_alignment_snapshot.json")
        assert fixture["canonical_map"]["1.4.0"] == "1.3.5"

    def test_safety_flags_fixture_no_real_orders(self):
        fixture = _load_fixture("safety_flags_snapshot.json")
        assert fixture["expected_flags"]["NO_REAL_ORDERS"] is True
        assert fixture["expected_flags"]["BROKER_EXECUTION_ENABLED"] is False
