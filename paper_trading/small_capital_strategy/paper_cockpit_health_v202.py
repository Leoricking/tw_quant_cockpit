"""
paper_trading/small_capital_strategy/paper_cockpit_health_v202.py
v2.0.2 Paper Cockpit Report Export & Audit Pack — Health Check
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("D:/code/Claude/tw_quant_cockpit"))

HEALTH_VERSION = "2.0.2"
HEALTH_RELEASE = "Paper Cockpit Report Export & Audit Pack"


def run_health_check():
    """Run all health checks for v2.0.2 paper cockpit. Returns result dict."""
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

    # --- module import ---
    chk("import_paper_cockpit_v202", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v202",
        fromlist=["VERSION"]))

    # --- version/title ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_202", lambda: None if VERSION == "2.0.2" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.2 got {VERSION}")))
    chk("schema_version_is_202", lambda: None if SCHEMA_VERSION == "202" else (_ for _ in ()).throw(
        AssertionError(f"Expected 202 got {SCHEMA_VERSION}")))
    chk("release_name_correct", lambda: None if "Export" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Export': {RELEASE_NAME}")))

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

    # --- export formats (4) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    chk("export_formats_count_4", lambda: None if len(EXPORT_FORMATS) == 4 else (_ for _ in ()).throw(
        AssertionError(f"Expected 4 EXPORT_FORMATS, got {len(EXPORT_FORMATS)}")))
    for fmt in ["json", "markdown", "csv", "audit_summary"]:
        chk(f"export_format_{fmt}", lambda f=fmt: None if f in EXPORT_FORMATS else (_ for _ in ()).throw(
            AssertionError(f"Missing export format: {f}")))

    # --- CSV names (5) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    chk("csv_names_count_5", lambda: None if len(CSV_EXPORT_NAMES) == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected 5 CSV_EXPORT_NAMES, got {len(CSV_EXPORT_NAMES)}")))
    for name in ["candidates.csv", "decision_tickets.csv", "no_entry_reasons.csv",
                 "risk_overlay.csv", "final_actions.csv"]:
        chk(f"csv_name_{name}", lambda n=name: None if n in CSV_EXPORT_NAMES else (_ for _ in ()).throw(
            AssertionError(f"Missing CSV name: {n}")))

    # --- audit pack fields (11) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    chk("audit_pack_fields_count_11", lambda: None if len(AUDIT_PACK_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 AUDIT_PACK_FIELDS, got {len(AUDIT_PACK_FIELDS)}")))
    for field_name in ["run_metadata", "input_snapshot", "decision_snapshot", "risk_snapshot",
                       "ticket_snapshot", "blocked_reason_snapshot", "human_review_snapshot",
                       "safety_snapshot", "reproducibility_hash", "export_format", "export_status"]:
        chk(f"audit_field_{field_name}", lambda fn=field_name: None if fn in AUDIT_PACK_FIELDS else (_ for _ in ()).throw(
            AssertionError(f"Missing audit pack field: {fn}")))

    # --- models (12) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import (
        ReportExportInput, ReportExportOutput, AuditPackSchema, MarkdownReport,
        CSVExportResult, JSONExportResult, AuditPackResult, ExportStatusSummary,
        ReportCandidateRow, ReportTicketRow, V202HealthSummary, V202ReleaseSummary,
        _ALL_MODEL_NAMES_V202,
    )
    chk("model_ReportExportInput", lambda: ReportExportInput())
    chk("model_ReportExportOutput", lambda: ReportExportOutput())
    chk("model_AuditPackSchema", lambda: AuditPackSchema())
    chk("model_MarkdownReport", lambda: MarkdownReport())
    chk("model_CSVExportResult", lambda: CSVExportResult())
    chk("model_JSONExportResult", lambda: JSONExportResult())
    chk("model_AuditPackResult", lambda: AuditPackResult())
    chk("model_ExportStatusSummary", lambda: ExportStatusSummary())
    chk("model_ReportCandidateRow", lambda: ReportCandidateRow())
    chk("model_ReportTicketRow", lambda: ReportTicketRow())
    chk("model_V202HealthSummary", lambda: V202HealthSummary())
    chk("model_V202ReleaseSummary", lambda: V202ReleaseSummary())
    chk("model_count_12", lambda: None if len(_ALL_MODEL_NAMES_V202) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V202)}")))

    # --- report engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import (
        export_json, export_markdown, export_csv, build_audit_pack, export_all,
        get_report_export_summary, get_version_info_v202, verify_version_v202,
        build_full_report, get_cockpit_summary_v202,
        build_report_candidate_row, build_report_ticket_row,
    )
    chk("fn_export_json", lambda: export_json())
    chk("fn_export_markdown", lambda: export_markdown())
    chk("fn_export_csv", lambda: export_csv())
    chk("fn_build_audit_pack", lambda: build_audit_pack())
    chk("fn_export_all", lambda: export_all())
    chk("fn_get_report_export_summary", lambda: get_report_export_summary())
    chk("fn_get_version_info_v202", lambda: get_version_info_v202())
    chk("fn_verify_version_v202", lambda: None if verify_version_v202() is True else (_ for _ in ()).throw(
        AssertionError("verify_version_v202() failed")))
    chk("fn_build_full_report", lambda: build_full_report())
    chk("fn_get_cockpit_summary_v202", lambda: get_cockpit_summary_v202())
    chk("fn_build_report_candidate_row", lambda: build_report_candidate_row())
    chk("fn_build_report_ticket_row", lambda: build_report_ticket_row())

    # --- JSON export callable ---
    chk("json_export_callable", lambda: None if export_json() is not None else (_ for _ in ()).throw(
        AssertionError("export_json() returned None")))
    chk("json_export_is_valid", lambda: None if export_json().is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_json().is_valid must be True")))
    chk("json_export_paper_only", lambda: None if export_json().paper_only is True else (_ for _ in ()).throw(
        AssertionError("json result paper_only must be True")))

    # --- Markdown export callable ---
    chk("markdown_export_callable", lambda: None if export_markdown() is not None else (_ for _ in ()).throw(
        AssertionError("export_markdown() returned None")))
    chk("markdown_has_title", lambda: None if export_markdown().title else (_ for _ in ()).throw(
        AssertionError("export_markdown().title must be non-empty")))
    chk("markdown_has_full_markdown", lambda: None if export_markdown().full_markdown else (_ for _ in ()).throw(
        AssertionError("export_markdown().full_markdown must be non-empty")))

    # --- CSV export callable ---
    chk("csv_export_callable", lambda: None if export_csv() is not None else (_ for _ in ()).throw(
        AssertionError("export_csv() returned None")))
    chk("csv_export_ok", lambda: None if export_csv().export_ok is True else (_ for _ in ()).throw(
        AssertionError("export_csv().export_ok must be True")))

    # --- audit pack callable ---
    chk("audit_pack_callable", lambda: None if build_audit_pack() is not None else (_ for _ in ()).throw(
        AssertionError("build_audit_pack() returned None")))
    chk("audit_pack_has_hash", lambda: None if build_audit_pack().reproducibility_hash else (_ for _ in ()).throw(
        AssertionError("audit pack reproducibility_hash must be non-empty")))
    chk("audit_pack_export_status_ok", lambda: None if build_audit_pack().export_status == "ok" else (_ for _ in ()).throw(
        AssertionError("audit pack export_status must be 'ok'")))

    # --- CLI commands (7) ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    chk("cli_commands_count_7", lambda: None if len(CLI_COMMANDS_V202) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 CLI_COMMANDS_V202, got {len(CLI_COMMANDS_V202)}")))
    for cmd in [
        "paper-cockpit-v202-report-json",
        "paper-cockpit-v202-report-md",
        "paper-cockpit-v202-report-csv",
        "paper-cockpit-v202-audit-pack",
        "paper-cockpit-v202-export-all",
        "paper-cockpit-v202-health",
        "paper-cockpit-v202-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V202 else (_ for _ in ()).throw(
            AssertionError(f"Missing CLI command: {c}")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    chk("panel_version_202", lambda: None if PANEL_VERSION_V202 == "2.0.2" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V202 2.0.2, got {PANEL_VERSION_V202}")))

    # --- PANEL_VERSION unchanged ---
    from gui.small_capital_strategy_panel import PANEL_VERSION
    chk("panel_version_unchanged_200", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must remain 2.0.0, got {PANEL_VERSION}")))

    # --- GUI tabs ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v202_tab_names
    tab_names = get_tab_names()
    for tab in ["report_export_v202", "audit_pack_v202", "export_status_v202"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v202_tab_names_3", lambda: None if len(get_v202_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v202 tab names, got {len(get_v202_tab_names())}")))

    # --- export schema complete ---
    chk("export_schema_complete", lambda: None if all(
        f in AUDIT_PACK_FIELDS for f in [
            "run_metadata", "input_snapshot", "decision_snapshot", "risk_snapshot",
            "ticket_snapshot", "blocked_reason_snapshot", "human_review_snapshot",
            "safety_snapshot", "reproducibility_hash", "export_format", "export_status",
        ]) else (_ for _ in ()).throw(AssertionError("Audit pack schema incomplete")))

    # --- paper-only guard enabled ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    chk("safety_paper_only_guard", lambda: None if SAFETY_FLAGS_V202.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("SAFETY_FLAGS_V202 paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V202.get("no_broker") is True else (_ for _ in ()).throw(
        AssertionError("SAFETY_FLAGS_V202 no_broker must be True")))
    chk("safety_export_is_paper_only", lambda: None if SAFETY_FLAGS_V202.get("export_is_paper_only") is True else (_ for _ in ()).throw(
        AssertionError("SAFETY_FLAGS_V202 export_is_paper_only must be True")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V202.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS_V202.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("safety_cockpit_executes_order_false", lambda: None if SAFETY_FLAGS_V202.get("cockpit_executes_order") is False else (_ for _ in ()).throw(
        AssertionError("cockpit_executes_order must be False")))

    # --- broker execution disabled ---
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))

    # --- production trading blocked ---
    chk("production_trading_blocked", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- no real orders ---
    chk("no_real_orders", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))

    # --- no real account sync ---
    chk("no_real_account_sync_flag", lambda: None if SAFETY_FLAGS_V202.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync flag must be True")))

    # --- no automatic rebalance ---
    chk("no_automatic_rebalance_flag", lambda: None if SAFETY_FLAGS_V202.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance flag must be True")))

    # --- backward compat with v2.0.1 ---
    chk("import_v201_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201",
        fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION as V201
    chk("v201_version_unchanged", lambda: None if V201 == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.1 VERSION changed to {V201}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    chk("v201_workflow_callable", lambda: None if run_daily_workflow() is not None else (_ for _ in ()).throw(
        AssertionError("run_daily_workflow() returned None")))
    chk("v201_workflow_paper_only", lambda: None if run_daily_workflow().paper_only is True else (_ for _ in ()).throw(
        AssertionError("v201 workflow paper_only must be True")))

    # --- backward compat with v2.0.0 ---
    chk("import_v200_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v200",
        fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION as V200
    chk("v200_version_unchanged", lambda: None if V200 == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.0 VERSION changed to {V200}")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v202 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_202", lambda: None if all(
        s["schema_version"] == "202" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v202 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_202", lambda: None if all(
        f["schema_version"] == "202" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    # --- covered versions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import COVERED_VERSIONS
    chk("covered_versions_include_201", lambda: None if "2.0.1" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("COVERED_VERSIONS must include 2.0.1")))
    chk("covered_versions_include_200", lambda: None if "2.0.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("COVERED_VERSIONS must include 2.0.0")))

    # --- test files exist ---
    import os as _os
    chk("test_v202_exists", lambda: None if _os.path.exists(
        _os.path.normpath("D:/code/Claude/tw_quant_cockpit/tests/test_paper_cockpit_v202.py")
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v202.py not found")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v202] {passed}/{total} passed")
    return {
        "all_passed": all_passed,
        "passed": passed,
        "failed": failed,
        "total": total,
        "errors": errors,
        "version": HEALTH_VERSION,
        "release": HEALTH_RELEASE,
    }


if __name__ == "__main__":
    result = run_health_check()
    if not result["all_passed"]:
        for e in result["errors"]:
            print(e)
        sys.exit(1)
    sys.exit(0)
