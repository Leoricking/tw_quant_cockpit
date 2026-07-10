"""
paper_trading/small_capital_strategy/stable_rollup_manifest_v179.py
Manifest for Small Capital Strategy Stable Rollup v1.7.9.
Lists all required modules, CLI commands, GUI tabs, health checks, release gates,
fixtures, scenarios, and safety flags.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

VERSION      = "1.7.9"
RELEASE_NAME = "Small Capital Strategy Stable Rollup"
BASE_RELEASE = "1.7.8 Small Capital Strategy Integration"

INCLUDED_RELEASES: List[Dict[str, str]] = [
    {"version": "v1.7.0", "release_name": "Small Capital Growth Strategy Template"},
    {"version": "v1.7.1", "release_name": "Watchlist Strategy Layer"},
    {"version": "v1.7.2", "release_name": "A/B/C Buy Point Execution Plan"},
    {"version": "v1.7.3", "release_name": "Market Regime Position Control"},
    {"version": "v1.7.4", "release_name": "Small Account Risk Dashboard"},
    {"version": "v1.7.5", "release_name": "Small Account Trade Journal"},
    {"version": "v1.7.6", "release_name": "Mistake Taxonomy & Weekly Review Dashboard"},
    {"version": "v1.7.7", "release_name": "Theme Rotation Scanner"},
    {"version": "v1.7.8", "release_name": "Small Capital Strategy Integration"},
]

REQUIRED_MODULES: List[str] = [
    "paper_trading.small_capital_strategy.version_v170",
    "paper_trading.small_capital_strategy.version_v171",
    "paper_trading.small_capital_strategy.version_v172",
    "paper_trading.small_capital_strategy.version_v173",
    "paper_trading.small_capital_strategy.version_v174",
    "paper_trading.small_capital_strategy.version_v175",
    "paper_trading.small_capital_strategy.version_v176",
    "paper_trading.small_capital_strategy.version_v177",
    "paper_trading.small_capital_strategy.version_v178",
    "paper_trading.small_capital_strategy.stable_rollup_version_v179",
    "paper_trading.small_capital_strategy.stable_rollup_safety_v179",
    "paper_trading.small_capital_strategy.stable_rollup_models_v179",
    "paper_trading.small_capital_strategy.stable_rollup_manifest_v179",
    "paper_trading.small_capital_strategy.stable_rollup_compatibility_v179",
    "paper_trading.small_capital_strategy.stable_rollup_health_v179",
    "paper_trading.small_capital_strategy.stable_rollup_cli_audit_v179",
    "paper_trading.small_capital_strategy.stable_rollup_gui_audit_v179",
    "paper_trading.small_capital_strategy.stable_rollup_fixture_audit_v179",
    "paper_trading.small_capital_strategy.stable_rollup_scenario_audit_v179",
    "paper_trading.small_capital_strategy.stable_rollup_regression_audit_v179",
    "paper_trading.small_capital_strategy.stable_rollup_report_v179",
]

REQUIRED_CLI_COMMANDS: List[str] = [
    "small-capital-stable-version",
    "small-capital-stable-manifest",
    "small-capital-stable-health",
    "small-capital-stable-gate",
    "small-capital-stable-safety",
    "small-capital-stable-compat",
    "small-capital-stable-cli-audit",
    "small-capital-stable-gui-audit",
    "small-capital-stable-fixture-audit",
    "small-capital-stable-scenario-audit",
    "small-capital-stable-regression-audit",
    "small-capital-stable-report",
]

REQUIRED_GUI_TABS: List[str] = [
    "stable_rollup",
    "stable_health",
    "stable_report",
]

REQUIRED_HEALTH_CHECKS: List[str] = [
    "health_v170",
    "health_v171",
    "health_v172",
    "health_v173",
    "health_v174",
    "health_v175",
    "health_v176",
    "health_v177",
    "health_v178",
    "stability_version_179",
    "safety_audit_all_safe",
    "cli_all_registered",
    "gui_tabs_present",
    "fixtures_have_safety",
    "scenarios_deterministic",
    "no_broker",
    "no_real_orders",
    "no_margin",
]

REQUIRED_RELEASE_GATES: List[str] = [
    "release/small_capital_growth_strategy_release_gate_v170.py",
    "release/watchlist_strategy_layer_release_gate_v171.py",
    "release/abc_buy_point_execution_plan_release_gate_v172.py",
    "release/market_regime_position_control_release_gate_v173.py",
    "release/small_account_risk_dashboard_release_gate_v174.py",
    "release/small_account_trade_journal_release_gate_v175.py",
    "release/mistake_taxonomy_weekly_review_release_gate_v176.py",
    "release/theme_rotation_scanner_release_gate_v177.py",
    "release/small_capital_strategy_integration_release_gate_v178.py",
    "release/stable_rollup_release_gate_v179.py",
]

MIN_FIXTURES    = 50
MIN_SCENARIOS   = 50

SAFETY_FLAGS: Dict[str, Any] = {
    "paper_only":                 True,
    "research_only":              True,
    "no_real_orders":             True,
    "no_broker":                  True,
    "not_investment_advice":      True,
    "production_trading_blocked": True,
    "no_margin":                  True,
    "no_leverage":                True,
    "no_production_db_writes":    True,
    "demo_only":                  True,
    "not_for_production":         True,
}


def get_manifest() -> Dict[str, Any]:
    """Return full manifest dict."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "base_release": BASE_RELEASE,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "included_releases": INCLUDED_RELEASES,
        "required_modules": REQUIRED_MODULES,
        "required_cli_commands": REQUIRED_CLI_COMMANDS,
        "required_gui_tabs": REQUIRED_GUI_TABS,
        "required_health_checks": REQUIRED_HEALTH_CHECKS,
        "required_release_gates": REQUIRED_RELEASE_GATES,
        "min_fixtures": MIN_FIXTURES,
        "min_scenarios": MIN_SCENARIOS,
        "safety_flags": SAFETY_FLAGS,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "paper_only": True,
        "research_only": True,
        "demo_only": True,
        "not_for_production": True,
    }


def validate_manifest() -> bool:
    m = get_manifest()
    assert m["version"] == "1.7.9"
    assert m["no_real_orders"] is True
    assert m["no_broker"] is True
    assert m["no_margin"] is True
    assert len(m["included_releases"]) == 9
    assert len(m["required_cli_commands"]) >= 12
    assert len(m["required_gui_tabs"]) >= 3
    return True
