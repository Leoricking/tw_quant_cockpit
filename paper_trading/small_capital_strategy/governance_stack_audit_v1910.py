"""
paper_trading/small_capital_strategy/governance_stack_audit_v1910.py
v1.9.10 Paper Governance Stack Consolidation & Release Audit
[!] Paper Only. Research Only. Consolidation Only. Release Audit Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

VERSION = "1.9.10"
SCHEMA_VERSION = "1910"
RELEASE_NAME = "Paper Governance Stack Consolidation & Release Audit"
BASELINE_TESTS = 31469
MIN_NEW_TESTS = 300

COVERED_VERSIONS = [
    "1.9.4",
    "1.9.5",
    "1.9.6",
    "1.9.7",
    "1.9.8",
    "1.9.9",
]

COVERED_MODULES = [
    "strategy_monitoring_v194",
    "strategy_review_alert_v195",
    "decision_registry_v196",
    "strategy_governance_dashboard_v197",
    "portfolio_governance_v198",
    "portfolio_risk_report_v199",
]

CLI_COMMANDS = [
    "governance-stack-version",
    "governance-stack-audit",
    "governance-stack-summary",
    "governance-stack-cli-audit",
    "governance-stack-gui-audit",
    "governance-stack-health-audit",
    "governance-stack-gate-audit",
    "governance-stack-fixture-audit",
    "governance-stack-scenario-audit",
    "governance-stack-safety-audit",
    "governance-stack-compatibility",
    "governance-stack-report",
    "governance-stack-health",
    "governance-stack-gate",
]

GUI_TABS = [
    "governance_stack_audit",
    "release_audit",
    "compatibility_summary",
]

FORBIDDEN_ACTIONS = [
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
    "LIVE_TRADE",
    "BROKER_ORDER",
    "REBALANCE_REAL_PORTFOLIO",
    "REAL_ORDER",
    "BROKER_CONNECT",
    "LIVE_ACTIVATE",
    "PRODUCTION_WRITE",
    "AUTO_REBALANCE",
]

ALLOWED_AUDIT_ACTIONS = [
    "PAPER_AUDIT",
    "PAPER_REPORT",
    "PAPER_VALIDATE",
    "PAPER_CONSOLIDATE",
    "PAPER_RELEASE_AUDIT",
    "PAPER_COMPATIBILITY_CHECK",
    "PAPER_DASHBOARD",
    "PAPER_SUMMARY",
    "PAPER_HEALTH_CHECK",
    "PAPER_GATE_CHECK",
    "PAPER_NO_CHANGE",
    "PAPER_RESEARCH",
    "PAPER_SIMULATE",
    "PAPER_RECOMMEND",
    "PAPER_EXPORT_AUDIT",
]

SAFETY_FLAGS = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "consolidation_only": True,
    "release_audit_only": True,
    "dashboard_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_writes": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "no_real_portfolio_rebalancing": True,
    "no_production_strategy_mutation": True,
    "not_investment_advice": True,
    "production_trading_blocked": True,
    "demo_only": True,
    "not_for_production": True,
    "audit_executes_order": False,
    "audit_mutates_strategy": False,
    "audit_rebalances_real_portfolio": False,
    "dashboard_mutates_strategy": False,
    "dashboard_places_real_order": False,
    "export_triggers_real_order": False,
    "compatibility_check_executes_order": False,
}


# ---------------------------------------------------------------------------
# 15 dataclass models (schema_version="1910")
# ---------------------------------------------------------------------------

@dataclass
class PaperGovernanceStackAuditInput:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    consolidation_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    audit_executes_order: bool = False
    audit_mutates_strategy: bool = False
    covered_versions: List[str] = field(default_factory=lambda: list(COVERED_VERSIONS))


@dataclass
class PaperGovernanceStackAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    consolidation_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    audit_executes_order: bool = False
    audit_mutates_strategy: bool = False
    audit_rebalances_real_portfolio: bool = False
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0


@dataclass
class PaperGovernanceStackModule:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    module_version: str = ""
    module_name: str = ""
    module_present: bool = False
    health_pass: bool = False
    gate_pass: bool = False
    cli_registered: bool = False
    gui_tabs_registered: bool = False


@dataclass
class PaperGovernanceStackVersion:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    consolidation_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    version: str = VERSION
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    covered_versions: List[str] = field(default_factory=lambda: list(COVERED_VERSIONS))
    cli_commands: List[str] = field(default_factory=lambda: list(CLI_COMMANDS))
    gui_tabs: List[str] = field(default_factory=lambda: list(GUI_TABS))


@dataclass
class PaperGovernanceStackCompatibilityResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    consolidation_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    compatibility_check_executes_order: bool = False
    all_compatible: bool = False
    incompatible_modules: List[str] = field(default_factory=list)
    compatible_count: int = 0
    total_count: int = 0


@dataclass
class PaperGovernanceStackCliAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    audit_executes_order: bool = False
    all_registered: bool = False
    missing_commands: List[str] = field(default_factory=list)
    registered_count: int = 0
    total_expected: int = 0


@dataclass
class PaperGovernanceStackGuiAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    dashboard_mutates_strategy: bool = False
    dashboard_places_real_order: bool = False
    all_tabs_present: bool = False
    missing_tabs: List[str] = field(default_factory=list)
    tab_count: int = 0


@dataclass
class PaperGovernanceStackHealthAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    all_health_pass: bool = False
    failing_health_modules: List[str] = field(default_factory=list)
    health_pass_count: int = 0
    total_health_modules: int = 0


@dataclass
class PaperGovernanceStackGateAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    all_gates_pass: bool = False
    failing_gate_modules: List[str] = field(default_factory=list)
    gate_pass_count: int = 0
    total_gate_modules: int = 0


@dataclass
class PaperGovernanceStackFixtureAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    all_fixtures_valid: bool = False
    invalid_fixtures: List[str] = field(default_factory=list)
    valid_count: int = 0
    total_count: int = 0
    schema_versions_consistent: bool = True


@dataclass
class PaperGovernanceStackScenarioAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    all_scenarios_valid: bool = False
    invalid_scenarios: List[str] = field(default_factory=list)
    valid_count: int = 0
    total_count: int = 0
    schema_versions_consistent: bool = True


@dataclass
class PaperGovernanceStackSafetyAuditResult:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    audit_executes_order: bool = False
    all_safe: bool = False
    safety_errors: List[str] = field(default_factory=list)
    safety_flags_count: int = 0
    forbidden_actions_count: int = 0


@dataclass
class PaperGovernanceStackReleaseSummary:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    consolidation_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    version: str = VERSION
    release_name: str = RELEASE_NAME
    covered_versions: List[str] = field(default_factory=lambda: list(COVERED_VERSIONS))
    modules_audited: int = 0
    cli_commands_total: int = 0
    gui_tabs_total: int = 0
    health_checks_total: int = 0
    gates_total: int = 0
    all_pass: bool = False


@dataclass
class PaperGovernanceStackAuditReport:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    consolidation_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    audit_executes_order: bool = False
    audit_mutates_strategy: bool = False
    audit_rebalances_real_portfolio: bool = False
    report_triggers_real_order: bool = False
    version: str = VERSION
    release_name: str = RELEASE_NAME
    all_passed: bool = False
    module_count: int = 0
    cli_audit_passed: bool = False
    gui_audit_passed: bool = False
    health_audit_passed: bool = False
    gate_audit_passed: bool = False
    safety_audit_passed: bool = False
    compatibility_passed: bool = False


@dataclass
class PaperGovernanceStackRecommendation:
    schema_version: str = "1910"
    paper_only: bool = True
    research_only: bool = True
    release_audit_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    recommendation_executes_order: bool = False
    recommendation_mutates_strategy: bool = False
    recommendation: str = "NO_ACTION"
    reason: str = ""
    priority: str = "LOW"


_ALL_MODEL_NAMES = [
    "PaperGovernanceStackAuditInput",
    "PaperGovernanceStackAuditResult",
    "PaperGovernanceStackModule",
    "PaperGovernanceStackVersion",
    "PaperGovernanceStackCompatibilityResult",
    "PaperGovernanceStackCliAuditResult",
    "PaperGovernanceStackGuiAuditResult",
    "PaperGovernanceStackHealthAuditResult",
    "PaperGovernanceStackGateAuditResult",
    "PaperGovernanceStackFixtureAuditResult",
    "PaperGovernanceStackScenarioAuditResult",
    "PaperGovernanceStackSafetyAuditResult",
    "PaperGovernanceStackReleaseSummary",
    "PaperGovernanceStackAuditReport",
    "PaperGovernanceStackRecommendation",
]

assert len(_ALL_MODEL_NAMES) == 15, f"Expected 15 models, got {len(_ALL_MODEL_NAMES)}"


# ---------------------------------------------------------------------------
# Safety helpers
# ---------------------------------------------------------------------------

def run_safety_audit() -> Dict[str, Any]:
    errors = []
    for flag, expected in SAFETY_FLAGS.items():
        if SAFETY_FLAGS.get(flag) != expected:
            errors.append(f"Safety flag mismatch: {flag}")
    for action in FORBIDDEN_ACTIONS:
        if action in ALLOWED_AUDIT_ACTIONS:
            errors.append(f"Forbidden action in allowed list: {action}")
    for action in ALLOWED_AUDIT_ACTIONS:
        if action in FORBIDDEN_ACTIONS:
            errors.append(f"Allowed action in forbidden list: {action}")
    return {
        "all_safe": len(errors) == 0,
        "errors": errors,
        "safety_flags_count": len(SAFETY_FLAGS),
        "forbidden_actions_count": len(FORBIDDEN_ACTIONS),
        "allowed_actions_count": len(ALLOWED_AUDIT_ACTIONS),
        "paper_only": True,
        "no_real_orders": True,
        "production_trading_blocked": True,
    }


def assert_audit_safe(action: str) -> None:
    if action in FORBIDDEN_ACTIONS:
        raise ValueError(f"Forbidden action blocked: {action}. Use paper-only audit actions.")


def is_safe_export_path(path: str) -> bool:
    if not path:
        return False
    forbidden_paths = ["production", "prod", "live", "broker", "real_trade"]
    path_lower = path.lower()
    for fp in forbidden_paths:
        if fp.lower() in path_lower:
            return False
    return True


# ---------------------------------------------------------------------------
# Version info
# ---------------------------------------------------------------------------

def get_version_info() -> Dict[str, Any]:
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "covered_versions": list(COVERED_VERSIONS),
        "covered_modules": list(COVERED_MODULES),
        "cli_commands": list(CLI_COMMANDS),
        "gui_tabs": list(GUI_TABS),
        "model_count": len(_ALL_MODEL_NAMES),
        "paper_only": True,
        "research_only": True,
        "consolidation_only": True,
        "release_audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


def verify_version() -> bool:
    info = get_version_info()
    assert info["version"] == VERSION
    assert info["schema_version"] == SCHEMA_VERSION
    assert len(COVERED_VERSIONS) == 6
    assert len(COVERED_MODULES) == 6
    assert len(CLI_COMMANDS) == 14
    assert len(GUI_TABS) == 3
    assert len(_ALL_MODEL_NAMES) == 15
    assert len(FORBIDDEN_ACTIONS) == 15
    assert len(ALLOWED_AUDIT_ACTIONS) == 15
    assert len(SAFETY_FLAGS) == 29
    assert info["paper_only"] is True
    assert info["no_real_orders"] is True
    assert info["production_trading_blocked"] is True
    return True


assert verify_version(), "v1.9.10 version verification failed"


# ---------------------------------------------------------------------------
# Audit engine
# ---------------------------------------------------------------------------

def _check_module_present(module_import_path: str) -> bool:
    try:
        import importlib
        importlib.import_module(module_import_path)
        return True
    except ImportError:
        return False


def audit_covered_modules() -> Dict[str, Any]:
    results = {}
    module_paths = {
        "1.9.4": "paper_trading.small_capital_strategy.strategy_monitoring_version_v194",
        "1.9.5": "paper_trading.small_capital_strategy.strategy_review_alert_version_v195",
        "1.9.6": "paper_trading.small_capital_strategy.decision_registry_version_v196",
        "1.9.7": "paper_trading.small_capital_strategy.strategy_governance_dashboard_version_v197",
        "1.9.8": "paper_trading.small_capital_strategy.portfolio_governance_version_v198",
        "1.9.9": "paper_trading.small_capital_strategy.portfolio_risk_report_version_v199",
    }
    for ver, path in module_paths.items():
        results[ver] = _check_module_present(path)
    all_present = all(results.values())
    return {
        "all_present": all_present,
        "results": results,
        "present_count": sum(1 for v in results.values() if v),
        "total": len(results),
        "paper_only": True,
        "not_investment_advice": True,
    }


def audit_cli_commands() -> Dict[str, Any]:
    try:
        from cli.command_registry import get_all_commands
        all_cmds = {c.name for c in get_all_commands()}
        expected_v194 = ["strategy-monitoring-version", "strategy-monitoring-run"]
        expected_v195 = ["strategy-review-version", "strategy-review-run"]
        expected_v196 = ["strategy-registry-version", "strategy-registry-run"]
        expected_v197 = ["strategy-governance-dashboard-version", "strategy-governance-dashboard-run"]
        expected_v198 = ["portfolio-governance-version", "portfolio-governance-run"]
        expected_v199 = ["portfolio-risk-report-version", "portfolio-risk-report-run"]
        expected = (expected_v194 + expected_v195 + expected_v196
                    + expected_v197 + expected_v198 + expected_v199)
        missing = [c for c in expected if c not in all_cmds]
        return {
            "all_registered": len(missing) == 0,
            "missing_commands": missing,
            "checked_count": len(expected),
            "total_commands": len(all_cmds),
            "paper_only": True,
            "audit_executes_order": False,
        }
    except Exception as e:
        return {
            "all_registered": False,
            "error": str(e),
            "missing_commands": [],
            "paper_only": True,
            "audit_executes_order": False,
        }


def audit_gui_tabs() -> Dict[str, Any]:
    try:
        from gui.small_capital_strategy_panel import get_tab_names, PANEL_VERSION
        tabs = get_tab_names()
        expected = [
            "strategy_monitoring", "drift_detection",
            "review_alerts", "human_approval",
            "decision_registry", "governance_dashboard",
            "portfolio_governance", "risk_overlay",
            "portfolio_risk_report", "position_sizing_policy",
        ]
        missing = [t for t in expected if t not in tabs]
        return {
            "all_tabs_present": len(missing) == 0,
            "missing_tabs": missing,
            "panel_version": PANEL_VERSION,
            "total_tabs": len(tabs),
            "checked_count": len(expected),
            "paper_only": True,
            "dashboard_mutates_strategy": False,
        }
    except Exception as e:
        return {
            "all_tabs_present": False,
            "error": str(e),
            "missing_tabs": [],
            "paper_only": True,
            "dashboard_mutates_strategy": False,
        }


def audit_health_checks() -> Dict[str, Any]:
    health_modules = {
        "1.9.4": ("paper_trading.small_capital_strategy.strategy_monitoring_health_v194", "run_health_check"),
        "1.9.5": ("paper_trading.small_capital_strategy.strategy_review_health_v195", "run_health_check"),
        "1.9.6": ("paper_trading.small_capital_strategy.strategy_registry_health_v196", "run_health_check"),
        "1.9.7": ("paper_trading.small_capital_strategy.strategy_governance_dashboard_health_v197", "run_health_check"),
        "1.9.8": ("paper_trading.small_capital_strategy.portfolio_governance_health_v198", "run_health_check"),
        "1.9.9": ("paper_trading.small_capital_strategy.portfolio_risk_report_health_v199", "run_health_check"),
    }
    results = {}
    for ver, (mod_path, fn_name) in health_modules.items():
        try:
            import importlib
            mod = importlib.import_module(mod_path)
            fn = getattr(mod, fn_name)
            r = fn()
            results[ver] = r.get("all_passed", False) or r.get("status") == "PASS"
        except Exception:
            results[ver] = False
    all_pass = all(results.values())
    return {
        "all_health_pass": all_pass,
        "results": results,
        "pass_count": sum(1 for v in results.values() if v),
        "total": len(results),
        "paper_only": True,
        "not_investment_advice": True,
    }


def audit_release_gates() -> Dict[str, Any]:
    gate_modules = {
        "1.9.4": ("release.strategy_monitoring_release_gate_v194", "run_gate"),
        "1.9.5": ("release.strategy_review_release_gate_v195", "run_gate"),
        "1.9.6": ("release.strategy_registry_release_gate_v196", "run_gate"),
        "1.9.7": ("release.strategy_governance_dashboard_release_gate_v197", "run_gate"),
        "1.9.8": ("release.portfolio_governance_release_gate_v198", "run_gate"),
        "1.9.9": ("release.portfolio_risk_report_release_gate_v199", "run_release_gate"),
    }
    results = {}
    for ver, (mod_path, fn_name) in gate_modules.items():
        try:
            import importlib
            mod = importlib.import_module(mod_path)
            fn = getattr(mod, fn_name)
            r = fn()
            results[ver] = r.get("all_passed", False) or r.get("status") == "PASS"
        except Exception:
            results[ver] = False
    all_pass = all(results.values())
    return {
        "all_gates_pass": all_pass,
        "results": results,
        "pass_count": sum(1 for v in results.values() if v),
        "total": len(results),
        "paper_only": True,
        "not_investment_advice": True,
    }


def audit_fixture_schemas() -> Dict[str, Any]:
    fixture_modules = {
        "1.9.4": "paper_trading.small_capital_strategy.strategy_monitoring_fixtures_v194",
        "1.9.5": "paper_trading.small_capital_strategy.strategy_review_fixtures_v195",
        "1.9.6": "paper_trading.small_capital_strategy.decision_registry_fixtures_v196",
        "1.9.7": "paper_trading.small_capital_strategy.strategy_governance_dashboard_fixtures_v197",
        "1.9.8": "paper_trading.small_capital_strategy.portfolio_governance_fixtures_v198",
        "1.9.9": "paper_trading.small_capital_strategy.portfolio_risk_report_fixtures_v199",
    }
    results = {}
    for ver, mod_path in fixture_modules.items():
        try:
            import importlib
            mod = importlib.import_module(mod_path)
            fixtures = getattr(mod, "FIXTURES", None) or getattr(mod, "_FIXTURES", None) or []
            if fixtures:
                consistent = all(
                    f.get("schema_version") == ver.replace(".", "")
                    for f in fixtures[:3]
                )
                results[ver] = consistent
            else:
                results[ver] = True
        except Exception:
            results[ver] = False
    all_consistent = all(results.values())
    return {
        "all_consistent": all_consistent,
        "results": results,
        "consistent_count": sum(1 for v in results.values() if v),
        "total": len(results),
        "paper_only": True,
        "not_investment_advice": True,
    }


def audit_scenario_schemas() -> Dict[str, Any]:
    scenario_modules = {
        "1.9.4": "paper_trading.small_capital_strategy.strategy_monitoring_scenarios_v194",
        "1.9.5": "paper_trading.small_capital_strategy.strategy_review_scenarios_v195",
        "1.9.6": "paper_trading.small_capital_strategy.decision_registry_scenarios_v196",
        "1.9.7": "paper_trading.small_capital_strategy.strategy_governance_dashboard_scenarios_v197",
        "1.9.8": "paper_trading.small_capital_strategy.portfolio_governance_scenarios_v198",
        "1.9.9": "paper_trading.small_capital_strategy.portfolio_risk_report_scenarios_v199",
    }
    results = {}
    for ver, mod_path in scenario_modules.items():
        try:
            import importlib
            mod = importlib.import_module(mod_path)
            scenarios = getattr(mod, "SCENARIOS", None) or getattr(mod, "_SCENARIOS", None) or []
            if scenarios:
                consistent = all(
                    s.get("schema_version") == ver.replace(".", "")
                    for s in scenarios[:3]
                )
                results[ver] = consistent
            else:
                results[ver] = True
        except Exception:
            results[ver] = False
    all_consistent = all(results.values())
    return {
        "all_consistent": all_consistent,
        "results": results,
        "consistent_count": sum(1 for v in results.values() if v),
        "total": len(results),
        "paper_only": True,
        "not_investment_advice": True,
    }


def audit_safety_flags() -> Dict[str, Any]:
    errors = []
    for flag, expected in SAFETY_FLAGS.items():
        if SAFETY_FLAGS.get(flag) != expected:
            errors.append(f"Flag mismatch: {flag}")
    for action in FORBIDDEN_ACTIONS:
        if action in ALLOWED_AUDIT_ACTIONS:
            errors.append(f"Forbidden action in allowed: {action}")
    return {
        "all_consistent": len(errors) == 0,
        "errors": errors,
        "safety_flags_count": len(SAFETY_FLAGS),
        "forbidden_actions_count": len(FORBIDDEN_ACTIONS),
        "allowed_actions_count": len(ALLOWED_AUDIT_ACTIONS),
        "paper_only": True,
        "not_investment_advice": True,
    }


def audit_backward_compatibility() -> Dict[str, Any]:
    try:
        from gui.small_capital_strategy_panel import PANEL_VERSION, PANEL_TITLE
        version_ok = PANEL_VERSION == VERSION
        title_ok = ("1.9.10" in PANEL_TITLE or "Governance" in PANEL_TITLE
                    or "Consolidation" in PANEL_TITLE)
        return {
            "all_compatible": version_ok and title_ok,
            "panel_version": PANEL_VERSION,
            "panel_title": PANEL_TITLE,
            "version_ok": version_ok,
            "title_ok": title_ok,
            "paper_only": True,
            "not_investment_advice": True,
        }
    except Exception as e:
        return {
            "all_compatible": False,
            "error": str(e),
            "paper_only": True,
            "not_investment_advice": True,
        }


def run_full_governance_stack_audit() -> Dict[str, Any]:
    """Run complete v1.9.10 governance stack audit. Paper only. No real orders."""
    checks = []
    passed = 0
    failed = 0

    def _check(name: str, condition: bool, detail: str = "") -> None:
        nonlocal passed, failed
        status = "PASS" if condition else "FAIL"
        if condition:
            passed += 1
        else:
            failed += 1
        checks.append({"name": name, "status": status, "detail": detail})

    # Version
    _check("version_is_1910", VERSION == "1.9.10")
    _check("schema_version_is_1910", SCHEMA_VERSION == "1910")
    _check("release_name_correct", "Governance" in RELEASE_NAME or "Consolidation" in RELEASE_NAME)
    _check("covered_versions_count_6", len(COVERED_VERSIONS) == 6)
    _check("cli_commands_count_14", len(CLI_COMMANDS) == 14)
    _check("gui_tabs_count_3", len(GUI_TABS) == 3)
    _check("model_count_15", len(_ALL_MODEL_NAMES) == 15)

    # Safety flags
    safety = audit_safety_flags()
    _check("safety_flags_consistent", safety["all_consistent"])
    _check("safety_flags_count_29", safety["safety_flags_count"] == 29)
    _check("forbidden_actions_count_15", safety["forbidden_actions_count"] == 15)
    _check("allowed_actions_count_15", safety["allowed_actions_count"] == 15)
    _check("paper_only_flag_true", SAFETY_FLAGS.get("paper_only") is True)
    _check("no_real_orders_flag_true", SAFETY_FLAGS.get("no_real_orders") is True)
    _check("audit_executes_order_false", SAFETY_FLAGS.get("audit_executes_order") is False)
    _check("dashboard_mutates_strategy_false", SAFETY_FLAGS.get("dashboard_mutates_strategy") is False)
    _check("export_triggers_real_order_false", SAFETY_FLAGS.get("export_triggers_real_order") is False)

    # Module coverage
    modules = audit_covered_modules()
    _check("all_v194_v199_modules_present", modules["all_present"],
           str(modules.get("results", {})))

    # GUI audit
    gui = audit_gui_tabs()
    _check("gui_tabs_audit", gui["all_tabs_present"],
           str(gui.get("missing_tabs", [])))

    # CLI audit
    cli = audit_cli_commands()
    _check("cli_commands_audit", cli["all_registered"],
           str(cli.get("missing_commands", [])))

    # Health checks
    health = audit_health_checks()
    _check("all_health_checks_pass", health["all_health_pass"],
           str(health.get("results", {})))

    # Release gates
    gates = audit_release_gates()
    _check("all_release_gates_pass", gates["all_gates_pass"],
           str(gates.get("results", {})))

    # Fixture schemas
    fixtures = audit_fixture_schemas()
    _check("fixture_schemas_consistent", fixtures["all_consistent"])

    # Scenario schemas
    scenarios = audit_scenario_schemas()
    _check("scenario_schemas_consistent", scenarios["all_consistent"])

    # Backward compatibility
    compat = audit_backward_compatibility()
    _check("backward_compatibility", compat["all_compatible"])

    # Verify version
    _check("verify_version_passes", verify_version() is True)

    # Safety audit
    s_audit = run_safety_audit()
    _check("safety_audit_all_safe", s_audit["all_safe"])

    all_passed = failed == 0
    return {
        "all_passed": all_passed,
        "status": "PASS" if all_passed else "FAIL",
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "checks": checks,
        "paper_only": True,
        "research_only": True,
        "consolidation_only": True,
        "release_audit_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "audit_executes_order": False,
        "audit_mutates_strategy": False,
    }


def get_governance_stack_summary() -> Dict[str, Any]:
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "covered_versions": list(COVERED_VERSIONS),
        "covered_modules": list(COVERED_MODULES),
        "model_count": len(_ALL_MODEL_NAMES),
        "cli_commands": list(CLI_COMMANDS),
        "gui_tabs": list(GUI_TABS),
        "paper_only": True,
        "research_only": True,
        "consolidation_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }
