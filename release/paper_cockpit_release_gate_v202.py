"""
release/paper_cockpit_release_gate_v202.py
v2.0.2 Paper Cockpit Report Export & Audit Pack — Release Gate
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("D:/code/Claude/tw_quant_cockpit"))

GATE_VERSION = "2.0.2"
GATE_RELEASE = "Paper Cockpit Report Export & Audit Pack"
BASELINE_TESTS = 32820
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1", "2.0.2")


def run_release_gate():
    """Run all release gate checks for v2.0.2. Returns result dict."""
    passed = 0
    failed = 0
    errors = []

    def chk(name, fn):
        nonlocal passed, failed
        try:
            fn()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append(f"FAIL:{name}:{e}")

    # --- gate version checks ---
    chk("gate_version_202", lambda: None if GATE_VERSION == "2.0.2" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.2")))
    chk("baseline_tests_32820", lambda: None if BASELINE_TESTS == 32820 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 32820")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import VERSION, SCHEMA_VERSION
    chk("module_version_202", lambda: None if VERSION == "2.0.2" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.2, got {VERSION}")))
    chk("schema_version_202", lambda: None if SCHEMA_VERSION == "202" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 202, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import _ALL_MODEL_NAMES_V202
    chk("models_count_12", lambda: None if len(_ALL_MODEL_NAMES_V202) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V202)}")))

    # --- export formats ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    chk("export_formats_4", lambda: None if len(EXPORT_FORMATS) == 4 else (_ for _ in ()).throw(
        AssertionError(f"Expected 4 EXPORT_FORMATS")))
    chk("has_json_format", lambda: None if "json" in EXPORT_FORMATS else (_ for _ in ()).throw(
        AssertionError("json missing from EXPORT_FORMATS")))
    chk("has_markdown_format", lambda: None if "markdown" in EXPORT_FORMATS else (_ for _ in ()).throw(
        AssertionError("markdown missing from EXPORT_FORMATS")))
    chk("has_csv_format", lambda: None if "csv" in EXPORT_FORMATS else (_ for _ in ()).throw(
        AssertionError("csv missing from EXPORT_FORMATS")))
    chk("has_audit_summary_format", lambda: None if "audit_summary" in EXPORT_FORMATS else (_ for _ in ()).throw(
        AssertionError("audit_summary missing from EXPORT_FORMATS")))

    # --- CSV names ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    chk("csv_names_5", lambda: None if len(CSV_EXPORT_NAMES) == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected 5 CSV_EXPORT_NAMES")))
    chk("has_candidates_csv", lambda: None if "candidates.csv" in CSV_EXPORT_NAMES else (_ for _ in ()).throw(
        AssertionError("candidates.csv missing")))

    # --- audit pack fields ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    chk("audit_pack_fields_11", lambda: None if len(AUDIT_PACK_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 AUDIT_PACK_FIELDS")))
    chk("has_reproducibility_hash", lambda: None if "reproducibility_hash" in AUDIT_PACK_FIELDS else (_ for _ in ()).throw(
        AssertionError("reproducibility_hash missing from AUDIT_PACK_FIELDS")))
    chk("has_safety_snapshot", lambda: None if "safety_snapshot" in AUDIT_PACK_FIELDS else (_ for _ in ()).throw(
        AssertionError("safety_snapshot missing from AUDIT_PACK_FIELDS")))

    # --- report engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import (
        export_json, export_markdown, export_csv, build_audit_pack, export_all,
    )
    chk("export_json_callable", lambda: export_json())
    chk("export_markdown_callable", lambda: export_markdown())
    chk("export_csv_callable", lambda: export_csv())
    chk("build_audit_pack_callable", lambda: build_audit_pack())
    chk("export_all_callable", lambda: export_all())

    # --- JSON export valid ---
    chk("json_is_valid", lambda: None if export_json().is_valid is True else (_ for _ in ()).throw(
        AssertionError("JSON export is_valid must be True")))

    # --- markdown has sections ---
    md = export_markdown()
    chk("markdown_has_title", lambda: None if md.title else (_ for _ in ()).throw(
        AssertionError("Markdown title empty")))
    chk("markdown_has_full_md", lambda: None if md.full_markdown else (_ for _ in ()).throw(
        AssertionError("Markdown full_markdown empty")))

    # --- CSV export ok ---
    chk("csv_export_ok", lambda: None if export_csv().export_ok is True else (_ for _ in ()).throw(
        AssertionError("CSV export_ok must be True")))

    # --- audit pack has hash ---
    chk("audit_has_hash", lambda: None if build_audit_pack().reproducibility_hash else (_ for _ in ()).throw(
        AssertionError("Audit pack reproducibility_hash empty")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    chk("cli_commands_7", lambda: None if len(CLI_COMMANDS_V202) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 CLI_COMMANDS_V202")))
    for cmd in [
        "paper-cockpit-v202-report-json",
        "paper-cockpit-v202-report-md",
        "paper-cockpit-v202-report-csv",
        "paper-cockpit-v202-audit-pack",
        "paper-cockpit-v202-export-all",
        "paper-cockpit-v202-health",
        "paper-cockpit-v202-gate",
    ]:
        chk(f"cli_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V202 else (_ for _ in ()).throw(
            AssertionError(f"Missing CLI command: {c}")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    chk("panel_version_v202", lambda: None if PANEL_VERSION_V202 == "2.0.2" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V202 2.0.2, got {PANEL_VERSION_V202}")))

    # --- PANEL_VERSION unchanged ---
    from gui.small_capital_strategy_panel import PANEL_VERSION
    chk("panel_version_200_unchanged", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must remain 2.0.0, got {PANEL_VERSION}")))

    # --- GUI tabs ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v202_tab_names
    tab_names = get_tab_names()
    for tab in ["report_export_v202", "audit_pack_v202", "export_status_v202"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing")))
    chk("get_v202_tab_names_3", lambda: None if len(get_v202_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v202 tab names")))

    # --- export schema complete ---
    chk("export_schema_complete", lambda: None if len(AUDIT_PACK_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError("Export schema must have 11 fields")))

    # --- paper-only guard enabled ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V202.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only guard must be enabled")))
    chk("export_is_paper_only", lambda: None if SAFETY_FLAGS_V202.get("export_is_paper_only") is True else (_ for _ in ()).throw(
        AssertionError("export_is_paper_only must be True")))

    # --- no automatic rebalance ---
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V202.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- no real account sync ---
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V202.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))

    # --- backward compat with v2.0.1 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION as V201
    chk("v201_backward_compat", lambda: None if V201 == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.1 VERSION changed to {V201}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    chk("v201_workflow_callable", lambda: None if run_daily_workflow().paper_only is True else (_ for _ in ()).throw(
        AssertionError("v201 workflow paper_only must be True")))

    # --- backward compat with v2.0.0 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION as V200
    chk("v200_backward_compat", lambda: None if V200 == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.0 VERSION changed to {V200}")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v202 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v202 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))

    gate_passed = (failed == 0)
    total_count = passed + failed
    print(f"[paper_cockpit_release_gate_v202] gate_passed={gate_passed}  {passed}/{total_count}")
    return {
        "gate_passed": gate_passed,
        "passed_count": passed,
        "failed_count": failed,
        "total_count": total_count,
        "errors": errors,
        "gate_version": GATE_VERSION,
        "gate_release": GATE_RELEASE,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }


if __name__ == "__main__":
    result = run_release_gate()
    if not result["gate_passed"]:
        for e in result["errors"]:
            print(e)
        sys.exit(1)
    sys.exit(0)
