"""
tests/test_stable_rollup_integration_v179.py
Integration tests for Small Capital Strategy Stable Rollup v1.7.9.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_version_v179 import (
    get_version_info, VERSION,
)
from paper_trading.small_capital_strategy.stable_rollup_safety_v179 import (
    run_safety_audit, get_safety_flags,
)
from paper_trading.small_capital_strategy.stable_rollup_manifest_v179 import (
    get_manifest, validate_manifest,
)
from paper_trading.small_capital_strategy.stable_rollup_health_v179 import run_health_check
from paper_trading.small_capital_strategy.stable_rollup_compatibility_v179 import (
    run_compatibility_check, get_compatible_versions,
)
from paper_trading.small_capital_strategy.stable_rollup_report_v179 import build_report
from release.stable_rollup_release_gate_v179 import run_release_gate
from gui.small_capital_strategy_panel import PANEL_VERSION, render_stable_rollup_tab


def test_integration_version_matches_panel():
    # Stable rollup VERSION is pinned at 1.7.9; PANEL_VERSION advances with each new release
    assert VERSION == "1.7.9"
    assert PANEL_VERSION in ("1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4")


def test_integration_version_info_and_safety_agree():
    version_info = get_version_info()
    safety_flags = get_safety_flags()
    assert version_info["paper_only"] == safety_flags["paper_only"]
    assert version_info["no_real_orders"] == safety_flags["no_real_orders"]


def test_integration_manifest_version_matches_version_module():
    manifest = get_manifest()
    assert manifest["version"] == VERSION


def test_integration_manifest_cli_count_matches_audit():
    from paper_trading.small_capital_strategy.stable_rollup_cli_audit_v179 import run_cli_audit
    manifest = get_manifest()
    cli_audit = run_cli_audit()
    assert len(manifest["required_cli_commands"]) == cli_audit["total_required"]


def test_integration_health_all_passed_gate_passes():
    health = run_health_check()
    gate = run_release_gate()
    assert health.all_passed is True
    assert gate["gate_passed"] is True


def test_integration_safety_audit_passes_gate():
    safety = run_safety_audit()
    gate = run_release_gate()
    assert safety["all_safe"] is True
    assert gate["gate_passed"] is True


def test_integration_compat_all_pass():
    compat = run_compatibility_check()
    assert compat["all_compatible"] is True
    assert compat["versions_checked"] == 9


def test_integration_compat_versions_list_length():
    compatible = get_compatible_versions()
    assert len(compatible) == 9


def test_integration_report_reflects_compat():
    compat = run_compatibility_check()
    report = build_report()
    compat_section = next(
        (s for s in report["sections"] if s["section"] == "compatibility"), None
    )
    assert compat_section is not None
    assert compat_section["all_compatible"] == compat["all_compatible"]


def test_integration_report_reflects_safety():
    safety = run_safety_audit()
    report = build_report()
    safety_section = next(
        (s for s in report["sections"] if s["section"] == "safety_audit"), None
    )
    assert safety_section is not None
    assert safety_section["all_safe"] == safety["all_safe"]


def test_integration_report_all_audits_pass():
    report = build_report()
    assert report["all_audits_pass"] is True


def test_integration_gate_total_ge_50():
    gate = run_release_gate()
    assert gate["total"] >= 50


def test_integration_render_stable_rollup_tab_safety_consistent():
    flags = get_safety_flags()
    tab = render_stable_rollup_tab()
    assert tab["paper_only"] == flags["paper_only"]
    assert tab["no_real_orders"] == flags["no_real_orders"]


def test_integration_validate_manifest_and_health_pass():
    manifest_valid = validate_manifest()
    health = run_health_check()
    assert manifest_valid is True
    assert health.all_passed is True


def test_integration_gui_audit_and_gate_agree():
    from paper_trading.small_capital_strategy.stable_rollup_gui_audit_v179 import run_gui_audit
    gui = run_gui_audit()
    gate = run_release_gate()
    assert gui["all_tabs_present"] is True
    assert gate["gate_passed"] is True


def test_integration_fixture_audit_and_scenario_audit_pass():
    from paper_trading.small_capital_strategy.stable_rollup_fixture_audit_v179 import run_fixture_audit
    from paper_trading.small_capital_strategy.stable_rollup_scenario_audit_v179 import run_scenario_audit
    fixture_result = run_fixture_audit()
    scenario_result = run_scenario_audit()
    assert fixture_result["all_safe"] is True
    assert scenario_result["all_clean"] is True


def test_integration_regression_audit_and_gate_both_clean():
    from paper_trading.small_capital_strategy.stable_rollup_regression_audit_v179 import run_regression_audit
    regression = run_regression_audit()
    gate = run_release_gate()
    assert regression["all_clean"] is True
    assert gate["gate_passed"] is True


def test_integration_end_to_end_full_rollup_pass():
    health = run_health_check()
    gate = run_release_gate()
    compat = run_compatibility_check()
    safety = run_safety_audit()
    manifest_valid = validate_manifest()
    report = build_report()
    assert health.all_passed is True
    assert gate["gate_passed"] is True
    assert compat["all_compatible"] is True
    assert safety["all_safe"] is True
    assert manifest_valid is True
    assert report["all_audits_pass"] is True


def test_integration_no_real_flags_everywhere():
    """Confirm no_real_orders is True across all major outputs."""
    version_info = get_version_info()
    safety_flags = get_safety_flags()
    manifest = get_manifest()
    compat = run_compatibility_check()
    report = build_report()
    assert version_info["no_real_orders"] is True
    assert safety_flags["no_real_orders"] is True
    assert manifest["no_real_orders"] is True
    assert compat["no_real_orders"] is True
    assert report["no_real_orders"] is True
