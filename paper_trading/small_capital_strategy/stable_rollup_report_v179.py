"""
paper_trading/small_capital_strategy/stable_rollup_report_v179.py
Report builder for Small Capital Strategy Stable Rollup v1.7.9.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"


def build_report() -> Dict[str, Any]:
    """Build a complete stable rollup report. Research only."""
    from paper_trading.small_capital_strategy.stable_rollup_version_v179 import get_version_info
    from paper_trading.small_capital_strategy.stable_rollup_manifest_v179 import get_manifest
    from paper_trading.small_capital_strategy.stable_rollup_compatibility_v179 import run_compatibility_check
    from paper_trading.small_capital_strategy.stable_rollup_safety_v179 import run_safety_audit
    from paper_trading.small_capital_strategy.stable_rollup_cli_audit_v179 import run_cli_audit
    from paper_trading.small_capital_strategy.stable_rollup_gui_audit_v179 import run_gui_audit
    from paper_trading.small_capital_strategy.stable_rollup_fixture_audit_v179 import run_fixture_audit
    from paper_trading.small_capital_strategy.stable_rollup_scenario_audit_v179 import run_scenario_audit
    from paper_trading.small_capital_strategy.stable_rollup_regression_audit_v179 import run_regression_audit

    version_info = get_version_info()
    manifest = get_manifest()
    compat = run_compatibility_check()
    safety = run_safety_audit()
    cli_audit = run_cli_audit()
    gui_audit = run_gui_audit()
    fixture_audit = run_fixture_audit()
    scenario_audit = run_scenario_audit()
    regression_audit = run_regression_audit()

    sections = [
        {"section": "executive_summary", "version": "1.7.9",
         "release_name": "Small Capital Strategy Stable Rollup",
         "paper_only": True, "research_only": True},
        {"section": "version_info", "data": version_info},
        {"section": "manifest_summary",
         "included_releases": len(manifest["included_releases"]),
         "required_modules": len(manifest["required_modules"]),
         "required_cli": len(manifest["required_cli_commands"]),
         "required_gui_tabs": len(manifest["required_gui_tabs"])},
        {"section": "compatibility",
         "all_compatible": compat["all_compatible"],
         "versions_checked": compat["versions_checked"]},
        {"section": "safety_audit",
         "all_safe": safety["all_safe"],
         "issues": safety["issues"]},
        {"section": "cli_audit",
         "all_registered": cli_audit["all_registered"],
         "registered_count": cli_audit["registered_count"]},
        {"section": "gui_audit",
         "all_tabs_present": gui_audit["all_tabs_present"],
         "render_clean": gui_audit["render_clean"],
         "total_tabs": gui_audit["total_tabs"]},
        {"section": "fixture_audit",
         "all_safe": fixture_audit["all_safe"],
         "total_fixtures": fixture_audit["total_fixtures"]},
        {"section": "scenario_audit",
         "all_clean": scenario_audit["all_clean"],
         "total_scenarios": scenario_audit["total_scenarios"]},
        {"section": "regression_audit",
         "all_clean": regression_audit["all_clean"],
         "issues": regression_audit["issues"]},
        {"section": "safety_disclaimer",
         "paper_only": True, "research_only": True, "no_real_orders": True,
         "no_broker": True, "not_investment_advice": True,
         "demo_only": True, "not_for_production": True},
    ]

    all_ok = (
        compat["all_compatible"] and
        safety["all_safe"] and
        cli_audit["all_registered"] and
        gui_audit["all_tabs_present"] and
        gui_audit["render_clean"] and
        fixture_audit["all_safe"] and
        scenario_audit["all_clean"] and
        regression_audit["all_clean"]
    )

    return {
        "version": "1.7.9",
        "release_name": "Small Capital Strategy Stable Rollup",
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "sections": sections,
        "section_count": len(sections),
        "all_audits_pass": all_ok,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
    }


def get_report_sections() -> List[str]:
    return [
        "executive_summary", "version_info", "manifest_summary",
        "compatibility", "safety_audit", "cli_audit", "gui_audit",
        "fixture_audit", "scenario_audit", "regression_audit",
        "safety_disclaimer",
    ]
