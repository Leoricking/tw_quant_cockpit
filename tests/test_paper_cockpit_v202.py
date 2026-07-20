"""
tests/test_paper_cockpit_v202.py
v2.0.2 Paper Cockpit — Main Tests (50+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

# ---------------------------------------------------------------------------
# Version and constants
# ---------------------------------------------------------------------------

def test_version_is_202():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import VERSION
    assert VERSION == "2.0.2"


def test_schema_version_is_202():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "202"


def test_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import RELEASE_NAME
    assert "Export" in RELEASE_NAME
    assert "Audit" in RELEASE_NAME


def test_baseline_tests():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import BASELINE_TESTS
    assert BASELINE_TESTS == 32820


def test_min_new_tests():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300


def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True


def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False


def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# ---------------------------------------------------------------------------
# CLI commands (7)
# ---------------------------------------------------------------------------

def test_cli_commands_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert len(CLI_COMMANDS_V202) == 7


def test_cli_command_report_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-report-json" in CLI_COMMANDS_V202


def test_cli_command_report_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-report-md" in CLI_COMMANDS_V202


def test_cli_command_report_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-report-csv" in CLI_COMMANDS_V202


def test_cli_command_audit_pack():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-audit-pack" in CLI_COMMANDS_V202


def test_cli_command_export_all():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-export-all" in CLI_COMMANDS_V202


def test_cli_command_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-health" in CLI_COMMANDS_V202


def test_cli_command_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-gate" in CLI_COMMANDS_V202


# ---------------------------------------------------------------------------
# GUI tabs (3)
# ---------------------------------------------------------------------------

def test_gui_tabs_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import GUI_TABS_V202
    assert len(GUI_TABS_V202) == 3


def test_gui_tab_report_export():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import GUI_TABS_V202
    assert "report_export_v202" in GUI_TABS_V202


def test_gui_tab_audit_pack():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import GUI_TABS_V202
    assert "audit_pack_v202" in GUI_TABS_V202


def test_gui_tab_export_status():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import GUI_TABS_V202
    assert "export_status_v202" in GUI_TABS_V202


# ---------------------------------------------------------------------------
# Export formats (4)
# ---------------------------------------------------------------------------

def test_export_formats_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    assert len(EXPORT_FORMATS) == 4


def test_export_format_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    assert "json" in EXPORT_FORMATS


def test_export_format_markdown():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    assert "markdown" in EXPORT_FORMATS


def test_export_format_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    assert "csv" in EXPORT_FORMATS


def test_export_format_audit_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    assert "audit_summary" in EXPORT_FORMATS


# ---------------------------------------------------------------------------
# CSV names (5)
# ---------------------------------------------------------------------------

def test_csv_names_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    assert len(CSV_EXPORT_NAMES) == 5


def test_csv_name_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    assert "candidates.csv" in CSV_EXPORT_NAMES


def test_csv_name_decision_tickets():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    assert "decision_tickets.csv" in CSV_EXPORT_NAMES


def test_csv_name_no_entry_reasons():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    assert "no_entry_reasons.csv" in CSV_EXPORT_NAMES


def test_csv_name_risk_overlay():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    assert "risk_overlay.csv" in CSV_EXPORT_NAMES


def test_csv_name_final_actions():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    assert "final_actions.csv" in CSV_EXPORT_NAMES


# ---------------------------------------------------------------------------
# Audit pack fields (11)
# ---------------------------------------------------------------------------

def test_audit_pack_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    assert len(AUDIT_PACK_FIELDS) == 11


def test_audit_pack_field_run_metadata():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    assert "run_metadata" in AUDIT_PACK_FIELDS


def test_audit_pack_field_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    assert "safety_snapshot" in AUDIT_PACK_FIELDS


def test_audit_pack_field_reproducibility_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    assert "reproducibility_hash" in AUDIT_PACK_FIELDS


def test_audit_pack_field_export_status():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    assert "export_status" in AUDIT_PACK_FIELDS


# ---------------------------------------------------------------------------
# Models (12)
# ---------------------------------------------------------------------------

def test_model_names_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import _ALL_MODEL_NAMES_V202
    assert len(_ALL_MODEL_NAMES_V202) == 12


def test_model_report_export_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import ReportExportInput
    obj = ReportExportInput()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.no_real_orders is True
    assert obj.source == "paper_cockpit"


def test_model_report_export_output():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import ReportExportOutput
    obj = ReportExportOutput()
    assert obj.schema_version == "202"
    assert obj.report_version == "2.0.2"
    assert obj.paper_only is True
    assert obj.human_review_required is True


def test_model_audit_pack_schema():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackSchema
    obj = AuditPackSchema()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.export_status == "ok"


def test_model_markdown_report():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MarkdownReport
    obj = MarkdownReport()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.human_review_required is True


def test_model_csv_export_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert obj.schema_version == "202"
    assert obj.export_ok is True
    assert len(obj.csv_names) == 5


def test_model_json_export_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import JSONExportResult
    obj = JSONExportResult()
    assert obj.schema_version == "202"
    assert obj.is_valid is True
    assert obj.report_version == "2.0.2"


def test_model_audit_pack_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackResult
    obj = AuditPackResult()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.export_status == "ok"


def test_model_export_status_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import ExportStatusSummary
    obj = ExportStatusSummary()
    assert obj.schema_version == "202"
    assert obj.export_ok is True
    assert len(obj.formats_available) == 4


def test_model_report_candidate_row():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import ReportCandidateRow
    obj = ReportCandidateRow()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.final_action == "NO_ENTRY"


def test_model_report_ticket_row():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import ReportTicketRow
    obj = ReportTicketRow()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.human_review_required is True


def test_model_v202_health_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202HealthSummary
    obj = V202HealthSummary()
    assert obj.version == "2.0.2"
    assert obj.export_formats_count == 4
    assert obj.csv_names_count == 5


def test_model_v202_release_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import V202ReleaseSummary
    obj = V202ReleaseSummary()
    assert obj.version == "2.0.2"
    assert obj.models_count == 12
    assert obj.baseline_tests == 32820


# ---------------------------------------------------------------------------
# Verify version
# ---------------------------------------------------------------------------

def test_verify_version_v202():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import verify_version_v202
    assert verify_version_v202() is True


def test_get_version_info_v202():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import get_version_info_v202
    info = get_version_info_v202()
    assert info["version"] == "2.0.2"
    assert info["schema_version"] == "202"
    assert info["paper_only"] is True
    assert info["no_real_orders"] is True


def test_get_report_export_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import get_report_export_summary
    summary = get_report_export_summary()
    assert summary["version"] == "2.0.2"
    assert len(summary["export_formats"]) == 4
    assert len(summary["csv_export_names"]) == 5
    assert summary["paper_only"] is True


def test_get_cockpit_summary_v202():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import get_cockpit_summary_v202
    summary = get_cockpit_summary_v202()
    assert summary["version"] == "2.0.2"
    assert summary["paper_only"] is True
    assert len(summary["models"]) == 12


def test_covered_versions_includes_201():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import COVERED_VERSIONS
    assert "2.0.1" in COVERED_VERSIONS


def test_covered_versions_includes_200():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import COVERED_VERSIONS
    assert "2.0.0" in COVERED_VERSIONS


def test_covered_versions_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import COVERED_VERSIONS
    assert len(COVERED_VERSIONS) == 31


def test_safety_flags_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["paper_only"] is True


def test_safety_flags_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_broker"] is True


def test_safety_flags_export_is_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["export_is_paper_only"] is True


def test_safety_flags_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202["no_real_orders"] is True


def test_safety_flags_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert len(SAFETY_FLAGS_V202) == 20
