"""
tests/test_version_alignment_v137.py — Version alignment tests for v1.3.7.

Verifies that the research validation releases (Empirical Backtest v1.3.5,
A/B/C Validation v1.3.6, Strategy Robustness v1.3.7) are correctly aligned
to the v1.3.x Research Foundation line, and that v1.4.x is reserved for
the Public Data Provider Integration roadmap.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import pytest


# ── Current Version ───────────────────────────────────────────────────────────

def test_current_version_is_137():
    """Test 1: Current version is at least 1.3.7 (v1.3.9+ stable rollup)."""
    from release.version_info import VERSION
    from release.version_alignment import is_version_at_least
    assert is_version_at_least(VERSION, "1.3.7"), f"Expected >= 1.3.7, got {VERSION}"


def test_current_release_name():
    """Test 2: Release name is a known release (v1.4.0+ adds public data provider releases)."""
    from release.version_info import RELEASE_NAME
    known_names = {
        "Strategy Robustness & Regime Validation",
        "Research Foundation Stable Rollup",
        "TWSE Provider",
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
    "Portfolio Stable Rollup Release Gate Hotfix",
    "Live Paper Trading Foundation",
            "Market Data Session Adapter",
            "Market Data Session Warning Hygiene Hotfix",
            "Paper Strategy Orchestration",
            "Paper Strategy Orchestration Integrity Hotfix",
            "Session Operations & Observability",
            "Session Operations Integrity Hotfix",
    }
    assert RELEASE_NAME in known_names, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"


def test_current_base_release():
    """Test 3: Base release is a known base (v1.4.1 base references v1.4.0)."""
    from release.version_info import BASE_RELEASE
    def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
    assert _parse_ver(BASE_RELEASE) >= _parse_ver("1.3.6"), (
        f"Unexpected BASE_RELEASE: {BASE_RELEASE}"
    )


def test_replay_stable_baseline():
    """Test 4: Replay stable baseline equals 1.2.9."""
    from release.version_info import REPLAY_STABLE_BASELINE
    assert REPLAY_STABLE_BASELINE == "1.2.9"


# ── Capability Preservation ───────────────────────────────────────────────────

def test_empirical_backtest_available():
    """Test 5: Empirical Backtest capability flag is True."""
    from release.version_info import STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE
    assert STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE is True


def test_abc_validation_available():
    """Test 6: A/B/C Validation capability flag is True."""
    from release.version_info import ABC_BUY_POINT_VALIDATION_AVAILABLE
    assert ABC_BUY_POINT_VALIDATION_AVAILABLE is True


def test_strategy_robustness_available():
    """Test 7: Strategy Robustness capability flag is True."""
    from release.version_info import STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE
    assert STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE is True


def test_data_freshness_available():
    """Test 8: Data Freshness Monitor capability flag is True."""
    from release.version_info import DATA_FRESHNESS_MONITOR_AVAILABLE
    assert DATA_FRESHNESS_MONITOR_AVAILABLE is True


def test_coverage_repair_available():
    """Test 9: Coverage Repair capability flag is True."""
    from release.version_info import COVERAGE_REPAIR_AVAILABLE
    assert COVERAGE_REPAIR_AVAILABLE is True


def test_provider_adapter_available():
    """Test 10: Provider Adapter capability flag is True."""
    from release.version_info import REAL_DATA_PROVIDER_ADAPTER_AVAILABLE
    assert REAL_DATA_PROVIDER_ADAPTER_AVAILABLE is True


def test_universe_expansion_available():
    """Test 11: Universe Expansion capability flag is True."""
    from release.version_info import UNIVERSE_REGISTRY_AVAILABLE
    assert UNIVERSE_REGISTRY_AVAILABLE is True


def test_real_data_quality_available():
    """Test 12: Real Data Quality capability flag is True."""
    from release.version_info import REAL_DATA_QUALITY_FOUNDATION
    assert REAL_DATA_QUALITY_FOUNDATION is True


# ── Canonical Mapping ─────────────────────────────────────────────────────────

def test_canonical_140_maps_to_135():
    """Test 13: Old 1.4.0 Empirical payload maps to canonical 1.3.5."""
    from release.version_alignment import canonical_version
    assert canonical_version("1.4.0") == "1.3.5"


def test_canonical_141_maps_to_136():
    """Test 14: Old 1.4.1 A/B/C payload maps to canonical 1.3.6."""
    from release.version_alignment import canonical_version
    assert canonical_version("1.4.1") == "1.3.6"


def test_canonical_142_maps_to_137():
    """Test 15: Old 1.4.2 Robustness payload maps to canonical 1.3.7."""
    from release.version_alignment import canonical_version
    assert canonical_version("1.4.2") == "1.3.7"


def test_freshness_hotfix_maps_to_1361():
    """Test 16: Freshness hotfix commit maps to 1.3.6.1."""
    from release.version_alignment import hotfix_canonical_version
    assert hotfix_canonical_version("f418de5") == "1.3.6.1"


def test_enrich_preserves_original_version():
    """Test 17: Original application_version is preserved in enriched payload."""
    from release.version_alignment import enrich_payload
    payload = {"application_version": "1.4.0", "result": "demo"}
    enriched = enrich_payload(payload)
    assert enriched["application_version"] == "1.4.0"


def test_enrich_does_not_modify_original():
    """Test 18: enrich_payload does not modify the original dict."""
    from release.version_alignment import enrich_payload
    payload = {"application_version": "1.4.1"}
    original_keys = set(payload.keys())
    _ = enrich_payload(payload)
    assert set(payload.keys()) == original_keys


def test_reproducibility_hash_not_changed():
    """Test 18b: Reproducibility hash is preserved verbatim through enrichment."""
    from release.version_alignment import enrich_payload
    payload = {
        "application_version": "1.4.2",
        "reproducibility_hash": "abc123",
    }
    enriched = enrich_payload(payload)
    assert enriched["reproducibility_hash"] == "abc123"


def test_unknown_future_version_loads_gracefully():
    """Test 19: Unknown future version loads without error."""
    from release.version_alignment import enrich_payload, canonical_version
    canonical_version("9.9.9")  # must not raise
    enrich_payload({"application_version": "9.9.9", "data": "x"})  # must not raise


def test_unknown_release_name_does_not_crash():
    """Test 20: Unknown release name does not crash canonical lookup."""
    from release.version_alignment import release_name_for_version
    result = release_name_for_version("99.0.0")
    assert result is None


# ── Snapshot Compatibility ────────────────────────────────────────────────────

def test_old_empirical_snapshot_loads():
    """Test 21: Old empirical snapshot (application_version=1.4.0) loads gracefully."""
    from release.version_alignment import load_snapshot_gracefully
    old = {"application_version": "1.4.0", "backtest_id": "bt_001", "result": "DEMO"}
    loaded = load_snapshot_gracefully(old)
    assert loaded["application_version"] == "1.4.0"
    assert loaded.get("canonical_release_version") == "1.3.5"


def test_old_abc_snapshot_loads():
    """Test 22: Old ABC snapshot (application_version=1.4.1) loads gracefully."""
    from release.version_alignment import load_snapshot_gracefully
    old = {"application_version": "1.4.1", "validation_id": "abc_001"}
    loaded = load_snapshot_gracefully(old)
    assert loaded["application_version"] == "1.4.1"
    assert loaded.get("canonical_release_version") == "1.3.6"


def test_old_robustness_result_loads():
    """Test 23: Old robustness result (application_version=1.4.2) loads gracefully."""
    from release.version_alignment import load_snapshot_gracefully
    old = {"application_version": "1.4.2", "robustness_id": "rb_001"}
    loaded = load_snapshot_gracefully(old)
    assert loaded["application_version"] == "1.4.2"
    assert loaded.get("canonical_release_version") == "1.3.7"


def test_old_freshness_snapshot_loads():
    """Test 24: Old freshness snapshot with no application_version loads gracefully."""
    from release.version_alignment import load_snapshot_gracefully
    old = {"freshness_status": "FRESH", "checked_at": "2024-01-01"}
    loaded = load_snapshot_gracefully(old)
    assert loaded["freshness_status"] == "FRESH"


def test_old_report_metadata_loads():
    """Test 25: Old report metadata loads and unknown fields are preserved."""
    from release.version_alignment import load_snapshot_gracefully
    old = {
        "application_version": "1.4.0",
        "report_version": "1.0",
        "extra_future_field": "preserved",
    }
    loaded = load_snapshot_gracefully(old)
    assert loaded["extra_future_field"] == "preserved"


def test_unknown_fields_forward_compatible():
    """Test 26: Unknown fields in any payload remain after enrichment."""
    from release.version_alignment import load_snapshot_gracefully
    old = {
        "application_version": "1.4.1",
        "new_field_from_future_version": [1, 2, 3],
    }
    loaded = load_snapshot_gracefully(old)
    assert loaded["new_field_from_future_version"] == [1, 2, 3]


# ── Roadmap ───────────────────────────────────────────────────────────────────

def _roadmap_text() -> str:
    import os
    path = os.path.join(os.path.dirname(__file__), "..", "docs", "roadmap.md")
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_roadmap_contains_137_strategy_robustness():
    """Test 27: Roadmap contains v1.3.7 Strategy Robustness."""
    text = _roadmap_text()
    assert "1.3.7" in text
    assert "Strategy Robustness" in text


def test_roadmap_contains_140_twse_provider():
    """Test 28: Roadmap contains v1.4.0 TWSE Provider."""
    text = _roadmap_text()
    assert "1.4.0" in text
    assert "TWSE" in text


def test_roadmap_contains_141_tpex_provider():
    """Test 29: Roadmap contains v1.4.1 TPEx Provider."""
    text = _roadmap_text()
    assert "1.4.1" in text
    assert "TPEx" in text


def test_roadmap_contains_142_mops_provider():
    """Test 30: Roadmap contains v1.4.2 MOPS Provider."""
    text = _roadmap_text()
    assert "1.4.2" in text
    assert "MOPS" in text


def test_roadmap_contains_143_datagov():
    """Test 31: Roadmap contains v1.4.3 data.gov.tw Provider."""
    text = _roadmap_text()
    assert "1.4.3" in text
    assert "data.gov.tw" in text


def test_roadmap_contains_144_finmind():
    """Test 32: Roadmap contains v1.4.4 FinMind Adapter Hardening."""
    text = _roadmap_text()
    assert "1.4.4" in text
    assert "FinMind" in text


def test_roadmap_contains_145_source_lineage():
    """Test 33: Roadmap contains v1.4.5 Source Lineage & Rate Limit."""
    text = _roadmap_text()
    assert "1.4.5" in text
    assert "Source Lineage" in text


def test_roadmap_contains_146_provider_quality_gates():
    """Test 34: Roadmap contains v1.4.6 Provider Quality Gates."""
    text = _roadmap_text()
    assert "1.4.6" in text
    assert "Provider Quality Gates" in text


def test_roadmap_contains_147_forum_intelligence():
    """Test 35: Roadmap contains v1.4.7 Forum Intelligence."""
    text = _roadmap_text()
    assert "1.4.7" in text
    assert "Forum Intelligence" in text


def test_roadmap_contains_149_stable_rollup():
    """Test 36: Roadmap contains v1.4.9 Stable Rollup."""
    text = _roadmap_text()
    assert "1.4.9" in text


# ── Regression Robustness ─────────────────────────────────────────────────────

def test_release_name_not_fragile_whitelist():
    """Test 37: Release name check must be capability-based, not a closed whitelist."""
    # This test verifies that version_alignment provides a semantic check
    from release.version_alignment import is_version_at_least
    # Any version >= 1.3.7 should be valid for current feature set
    assert is_version_at_least("1.3.7", "1.3.7") is True
    assert is_version_at_least("1.4.0", "1.3.7") is True
    assert is_version_at_least("1.3.6", "1.3.7") is False


def test_future_release_name_does_not_break_feature_tests():
    """Test 38: A future release name does not break empirical backtest capability test."""
    from release.version_info import STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE
    assert STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE is True


def test_semantic_version_comparison():
    """Test 39: Semantic version comparison works correctly."""
    from release.version_alignment import parse_version
    assert parse_version("1.3.7") > parse_version("1.3.6")
    assert parse_version("1.3.7") > parse_version("1.2.9")
    assert parse_version("1.4.0") > parse_version("1.3.7")
    assert parse_version("1.3.7") == parse_version("1.3.7")


def test_capability_checks_replace_version_equality():
    """Test 40: Capability flags, not version strings, verify feature availability."""
    from release.version_info import (
        STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE,
        ABC_BUY_POINT_VALIDATION_AVAILABLE,
        STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE,
    )
    assert STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE is True
    assert ABC_BUY_POINT_VALIDATION_AVAILABLE is True
    assert STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE is True


# ── Safety ────────────────────────────────────────────────────────────────────

def test_no_real_orders_remains_true():
    """Test 41: No Real Orders remains True."""
    from release.version_info import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True


def test_broker_execution_remains_false():
    """Test 42: Broker Execution Enabled remains False."""
    from release.version_info import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False


def test_production_trading_remains_blocked():
    """Test 43: Production Trading BLOCKED remains True."""
    from release.version_info import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


def test_mock_fallback_remains_false():
    """Test 44: Mock Fallback remains False."""
    from release.version_info import MOCK_FALLBACK_ENABLED
    assert MOCK_FALLBACK_ENABLED is False


def test_auto_optimization_remains_false():
    """Test 45: Auto Optimization remains False."""
    from release.version_info import ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED
    assert ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED is False


def test_auto_trading_remains_false():
    """Test 46: Auto Trading remains False."""
    from release.version_info import ROBUSTNESS_AUTO_TRADING_ENABLED
    assert ROBUSTNESS_AUTO_TRADING_ENABLED is False


def test_replay_score_unchanged():
    """Test 47: Replay integration never modifies session scores."""
    from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        integration = RobustnessReplayIntegration(base_dir=tmp)
        evidence = integration.get_evidence_for_rule("safety_check")
        assert evidence.get("modifies_session_score") is False
        assert evidence.get("modifies_replay") is False


def test_no_broker_code_introduced():
    """Test 48: version_alignment module does not contain broker execution code."""
    import release.version_alignment as va
    with open(va.__file__, encoding="utf-8") as _f:
        src = _f.read()
    # Check that no broker execution functions are present
    # (comments like "No Real Orders" are expected and allowed)
    forbidden_patterns = ["broker_api", "execute_trade", "place_order", "submit_order",
                          "broker_connect", "order_submit", "send_order"]
    for pattern in forbidden_patterns:
        assert pattern not in src.lower(), (
            f"Forbidden broker execution pattern '{pattern}' found in version_alignment.py"
        )


# ── Full Regression Smoke ─────────────────────────────────────────────────────

def test_empirical_backtest_package_imports():
    """Test 49: Empirical Backtest package still importable."""
    import empirical_backtest
    assert empirical_backtest.NO_REAL_ORDERS is True


def test_abc_validation_package_imports():
    """Test 50: ABC Validation package still importable."""
    import abc_validation
    assert abc_validation.NO_REAL_ORDERS is True


def test_robustness_package_imports():
    """Test 51: Strategy Robustness package still importable."""
    import strategy_robustness
    assert strategy_robustness.NO_REAL_ORDERS is True


def test_data_freshness_package_imports():
    """Test 52: Data Freshness package still importable."""
    import data_freshness
    assert data_freshness.NO_REAL_ORDERS is True


def test_coverage_repair_package_imports():
    """Test 53: Coverage Repair package still importable."""
    import coverage_repair
    assert coverage_repair.NO_REAL_ORDERS is True


def test_provider_adapter_imports():
    """Test 54: Provider Adapter capability flag is set (adapter implemented within real_data_quality)."""
    from release.version_info import REAL_DATA_PROVIDER_ADAPTER_AVAILABLE
    assert REAL_DATA_PROVIDER_ADAPTER_AVAILABLE is True


def test_universe_package_imports():
    """Test 55: Universe package still importable."""
    import universe
    assert universe.NO_REAL_ORDERS is True


def test_data_quality_package_imports():
    """Test 56: Data Quality package (real_data_quality) still importable."""
    import real_data_quality
    assert real_data_quality.NO_REAL_ORDERS is True


def test_cli_version_info_smoke():
    """Test 57 (CLI smoke): version-info imports without error (v1.3.9+ stable rollup)."""
    from release.version_info import VERSION, RELEASE_NAME, BASE_RELEASE, REPLAY_STABLE_BASELINE
    from release.version_alignment import is_version_at_least
    assert is_version_at_least(VERSION, "1.3.7"), f"Expected >= 1.3.7, got {VERSION}"
    assert RELEASE_NAME is not None
    assert BASE_RELEASE is not None
    assert REPLAY_STABLE_BASELINE == "1.2.9"


def test_gui_robustness_panel_smoke():
    """Test 58 (GUI smoke): Strategy Robustness Panel imports without error."""
    from gui.strategy_robustness_panel import StrategyRobustnessPanel
    assert StrategyRobustnessPanel is not None


def test_version_alignment_module_imports():
    """Test 59: version_alignment module imports cleanly."""
    from release import version_alignment
    assert hasattr(version_alignment, "canonical_version")
    assert hasattr(version_alignment, "enrich_payload")
    assert hasattr(version_alignment, "parse_version")
    assert hasattr(version_alignment, "is_version_at_least")


def test_full_suite_safety_invariants():
    """Test 60: All safety invariants hold after alignment (v1.3.9+ stable rollup)."""
    from release.version_info import (
        VERSION, NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
        PRODUCTION_TRADING_BLOCKED, MOCK_FALLBACK_ENABLED,
        ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED, ROBUSTNESS_AUTO_TRADING_ENABLED,
        REPLAY_STABLE_BASELINE,
    )
    from release.version_alignment import is_version_at_least
    assert is_version_at_least(VERSION, "1.3.7"), f"Expected >= 1.3.7, got {VERSION}"
    assert NO_REAL_ORDERS is True
    assert BROKER_EXECUTION_ENABLED is False
    assert PRODUCTION_TRADING_BLOCKED is True
    assert MOCK_FALLBACK_ENABLED is False
    assert ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED is False
    assert ROBUSTNESS_AUTO_TRADING_ENABLED is False
    assert REPLAY_STABLE_BASELINE == "1.2.9"
