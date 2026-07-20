"""
paper_trading/small_capital_strategy/paper_cockpit_v202.py
v2.0.2 Paper Cockpit Report Export & Audit Pack
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage. Not Investment Advice.
[!] Report Export Engine. Audit Pack Schema. Markdown Report. CSV Export.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

VERSION = "2.0.2"
SCHEMA_VERSION = "202"
RELEASE_NAME = "Paper Cockpit Report Export & Audit Pack"
BASELINE_TESTS = 32820
MIN_NEW_TESTS = 300

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

CLI_COMMANDS_V202: List[str] = [
    "paper-cockpit-v202-report-json",
    "paper-cockpit-v202-report-md",
    "paper-cockpit-v202-report-csv",
    "paper-cockpit-v202-audit-pack",
    "paper-cockpit-v202-export-all",
    "paper-cockpit-v202-health",
    "paper-cockpit-v202-gate",
]

assert len(CLI_COMMANDS_V202) == 7, f"Expected 7 CLI_COMMANDS_V202, got {len(CLI_COMMANDS_V202)}"

GUI_TABS_V202: List[str] = [
    "report_export_v202",
    "audit_pack_v202",
    "export_status_v202",
]

assert len(GUI_TABS_V202) == 3, f"Expected 3 GUI_TABS_V202, got {len(GUI_TABS_V202)}"

CSV_EXPORT_NAMES: List[str] = [
    "candidates.csv",
    "decision_tickets.csv",
    "no_entry_reasons.csv",
    "risk_overlay.csv",
    "final_actions.csv",
]

assert len(CSV_EXPORT_NAMES) == 5, f"Expected 5 CSV_EXPORT_NAMES, got {len(CSV_EXPORT_NAMES)}"

EXPORT_FORMATS: List[str] = ["json", "markdown", "csv", "audit_summary"]

assert len(EXPORT_FORMATS) == 4, f"Expected 4 EXPORT_FORMATS, got {len(EXPORT_FORMATS)}"

AUDIT_PACK_FIELDS: List[str] = [
    "run_metadata",
    "input_snapshot",
    "decision_snapshot",
    "risk_snapshot",
    "ticket_snapshot",
    "blocked_reason_snapshot",
    "human_review_snapshot",
    "safety_snapshot",
    "reproducibility_hash",
    "export_format",
    "export_status",
]

assert len(AUDIT_PACK_FIELDS) == 11, f"Expected 11 AUDIT_PACK_FIELDS, got {len(AUDIT_PACK_FIELDS)}"

MARKDOWN_SECTIONS: List[str] = [
    "title",
    "summary",
    "top_candidates",
    "blocked_candidates",
    "abc_setup_table",
    "risk_budget_table",
    "decision_ticket_section",
    "human_review_required_section",
    "safety_guard_section",
    "final_action_summary",
]

assert len(MARKDOWN_SECTIONS) == 10, f"Expected 10 MARKDOWN_SECTIONS, got {len(MARKDOWN_SECTIONS)}"

SAFETY_FLAGS_V202: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "report_export_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "human_review_required": True,
    "production_trading_blocked": True,
    "broker_execution_enabled": False,
    "cockpit_executes_order": False,
    "cockpit_mutates_strategy": False,
    "cockpit_rebalances_real_portfolio": False,
    "no_automatic_rebalance": True,
    "no_real_account_sync": True,
    "export_is_paper_only": True,
    "no_sensitive_data": True,
}

assert len(SAFETY_FLAGS_V202) == 20, f"Expected 20 SAFETY_FLAGS_V202, got {len(SAFETY_FLAGS_V202)}"

COVERED_VERSIONS: List[str] = [
    "1.7.0", "1.7.1", "1.7.2", "1.7.3", "1.7.5", "1.7.6",
    "1.7.7", "1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2",
    "1.8.3", "1.8.4", "1.8.6", "1.8.7", "1.8.8", "1.8.9",
    "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5",
    "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0",
    "2.0.1",
]

assert len(COVERED_VERSIONS) == 31, f"Expected 31 COVERED_VERSIONS, got {len(COVERED_VERSIONS)}"


# ---------------------------------------------------------------------------
# Dataclasses — 12 new models, schema_version="202"
# ---------------------------------------------------------------------------

@dataclass
class ReportExportInput:
    """Report export input specification. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    human_review_required: bool = True
    report_format: str = "json"
    report_id: str = "PC202-RPT-001"
    run_date: str = "2026-07-20"
    watchlist_symbols: List[str] = field(default_factory=list)
    candidates: List[str] = field(default_factory=list)
    include_audit_pack: bool = True
    include_markdown: bool = True
    include_csv: bool = True
    source: str = "paper_cockpit"


@dataclass
class ReportExportOutput:
    """Report export output with all required fields. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    report_id: str = "PC202-RPT-001"
    report_version: str = "2.0.2"
    generated_at: str = "2026-07-20T00:00:00"
    source: str = "paper_cockpit"
    watchlist_summary: str = ""
    candidate_ranking: List[str] = field(default_factory=list)
    abc_entry_status: str = "NO_ENTRY"
    no_entry_reasons: List[str] = field(default_factory=list)
    risk_overlay_status: str = "NORMAL"
    position_sizing_suggestion: str = ""
    paper_decision_tickets: List[str] = field(default_factory=list)
    human_review_flags: List[str] = field(default_factory=list)
    final_actions: List[str] = field(default_factory=list)
    paper_only_safety_flags: Dict[str, Any] = field(default_factory=dict)
    export_ok: bool = True
    human_review_required: bool = True


@dataclass
class AuditPackSchema:
    """Audit pack with all 11 required fields. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    run_metadata: Dict[str, Any] = field(default_factory=dict)
    input_snapshot: Dict[str, Any] = field(default_factory=dict)
    decision_snapshot: Dict[str, Any] = field(default_factory=dict)
    risk_snapshot: Dict[str, Any] = field(default_factory=dict)
    ticket_snapshot: Dict[str, Any] = field(default_factory=dict)
    blocked_reason_snapshot: Dict[str, Any] = field(default_factory=dict)
    human_review_snapshot: Dict[str, Any] = field(default_factory=dict)
    safety_snapshot: Dict[str, Any] = field(default_factory=dict)
    reproducibility_hash: str = ""
    export_format: str = "json"
    export_status: str = "ok"


@dataclass
class MarkdownReport:
    """Markdown report with all 10 required sections. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    title: str = ""
    summary: str = ""
    top_candidates: str = ""
    blocked_candidates: str = ""
    abc_setup_table: str = ""
    risk_budget_table: str = ""
    decision_ticket_section: str = ""
    human_review_required_section: str = ""
    safety_guard_section: str = ""
    final_action_summary: str = ""
    full_markdown: str = ""
    human_review_required: bool = True


@dataclass
class CSVExportResult:
    """CSV export result with csv names and row counts. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    candidates_csv: str = ""
    candidates_rows: int = 0
    decision_tickets_csv: str = ""
    decision_tickets_rows: int = 0
    no_entry_reasons_csv: str = ""
    no_entry_reasons_rows: int = 0
    risk_overlay_csv: str = ""
    risk_overlay_rows: int = 0
    final_actions_csv: str = ""
    final_actions_rows: int = 0
    csv_names: List[str] = field(default_factory=lambda: list(CSV_EXPORT_NAMES))
    export_ok: bool = True
    human_review_required: bool = True


@dataclass
class JSONExportResult:
    """JSON export result with schema_version and validity flag. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    json_str: str = ""
    is_valid: bool = True
    export_format: str = "json"
    source: str = "paper_cockpit"
    report_version: str = "2.0.2"
    human_review_required: bool = True


@dataclass
class AuditPackResult:
    """Audit pack result with all snapshot fields. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    pack_id: str = "PC202-PACK-001"
    run_metadata: Dict[str, Any] = field(default_factory=dict)
    input_snapshot: Dict[str, Any] = field(default_factory=dict)
    decision_snapshot: Dict[str, Any] = field(default_factory=dict)
    risk_snapshot: Dict[str, Any] = field(default_factory=dict)
    ticket_snapshot: Dict[str, Any] = field(default_factory=dict)
    blocked_reason_snapshot: Dict[str, Any] = field(default_factory=dict)
    human_review_snapshot: Dict[str, Any] = field(default_factory=dict)
    safety_snapshot: Dict[str, Any] = field(default_factory=dict)
    reproducibility_hash: str = ""
    export_format: str = "json"
    export_status: str = "ok"
    human_review_required: bool = True


@dataclass
class ExportStatusSummary:
    """Export status summary for all available formats. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    formats_available: List[str] = field(default_factory=lambda: list(EXPORT_FORMATS))
    json_ok: bool = True
    markdown_ok: bool = True
    csv_ok: bool = True
    audit_pack_ok: bool = True
    export_ok: bool = True
    human_review_required: bool = True
    paper_only_guard_enabled: bool = True
    broker_execution_disabled: bool = True
    production_trading_blocked: bool = True


@dataclass
class ReportCandidateRow:
    """One row in the report candidate table. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    symbol: str = ""
    name: str = ""
    rank: int = 0
    total_score: float = 0.0
    abc_type: str = "NO_ENTRY"
    final_action: str = "NO_ENTRY"
    entry_allowed: bool = False
    block_reason: str = ""
    human_review_required: bool = True


@dataclass
class ReportTicketRow:
    """One row for a decision ticket in reports. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    ticket_id: str = ""
    symbol: str = ""
    name: str = ""
    setup_type: str = "NO_ENTRY"
    final_action: str = "NO_ENTRY"
    entry_price_plan: float = 0.0
    stop_loss_price: float = 0.0
    risk_amount: float = 0.0
    position_size: float = 0.0
    no_entry_reasons: List[str] = field(default_factory=list)
    human_review_required: bool = True


@dataclass
class V202HealthSummary:
    """Health summary for v2.0.2. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    all_passed: bool = False
    passed: int = 0
    failed: int = 0
    total: int = 0
    version: str = "2.0.2"
    export_formats_count: int = 4
    csv_names_count: int = 5
    audit_pack_fields_count: int = 11
    cli_commands_count: int = 7
    gui_tabs_count: int = 3


@dataclass
class V202ReleaseSummary:
    """Release summary for v2.0.2. v2.0.2."""
    schema_version: str = "202"
    paper_only: bool = True
    no_real_orders: bool = True
    version: str = "2.0.2"
    release_name: str = RELEASE_NAME
    baseline_tests: int = BASELINE_TESTS
    min_new_tests: int = MIN_NEW_TESTS
    models_count: int = 12
    cli_count: int = 7
    gui_tabs_count: int = 3
    scenarios_count: int = 80
    fixtures_count: int = 80
    export_formats_count: int = 4
    csv_names_count: int = 5
    audit_pack_fields_count: int = 11
    all_sealed: bool = False


_ALL_MODEL_NAMES_V202: List[str] = [
    "ReportExportInput",
    "ReportExportOutput",
    "AuditPackSchema",
    "MarkdownReport",
    "CSVExportResult",
    "JSONExportResult",
    "AuditPackResult",
    "ExportStatusSummary",
    "ReportCandidateRow",
    "ReportTicketRow",
    "V202HealthSummary",
    "V202ReleaseSummary",
]

assert len(_ALL_MODEL_NAMES_V202) == 12, f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V202)}"


# ---------------------------------------------------------------------------
# Core engine functions
# ---------------------------------------------------------------------------

def _make_reproducibility_hash(data: str) -> str:
    """Generate a reproducibility hash using md5 on deterministic string."""
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def export_json(report_input: Optional[ReportExportInput] = None) -> JSONExportResult:
    """Export report as JSON string. Paper only, in-memory."""
    if report_input is None:
        report_input = ReportExportInput()

    payload: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "report_version": VERSION,
        "source": report_input.source,
        "report_id": report_input.report_id,
        "run_date": report_input.run_date,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "human_review_required": True,
        "watchlist_summary": f"watchlist_symbols={report_input.watchlist_symbols}",
        "candidate_ranking": report_input.candidates,
        "abc_entry_status": "NO_ENTRY",
        "no_entry_reasons": [],
        "risk_overlay_status": "NORMAL",
        "position_sizing_suggestion": "PAPER_ALLOW_NORMAL_SIZE",
        "paper_decision_tickets": [],
        "human_review_flags": ["human_review_required=True"],
        "final_actions": [],
        "paper_only_safety_flags": {
            "NO_REAL_ORDERS": True,
            "BROKER_EXECUTION_ENABLED": False,
            "PRODUCTION_TRADING_BLOCKED": True,
        },
    }

    import json
    json_str = json.dumps(payload, indent=2, ensure_ascii=False)

    return JSONExportResult(
        json_str=json_str,
        is_valid=True,
        export_format="json",
        source=report_input.source,
        report_version=VERSION,
    )


def export_markdown(report_input: Optional[ReportExportInput] = None) -> MarkdownReport:
    """Export report as Markdown. Paper only, in-memory."""
    if report_input is None:
        report_input = ReportExportInput()

    title = f"# Paper Cockpit Report v{VERSION} — {RELEASE_NAME}"
    summary = (
        f"**Report ID**: {report_input.report_id}  \n"
        f"**Run Date**: {report_input.run_date}  \n"
        f"**Source**: {report_input.source}  \n"
        f"**Schema Version**: {SCHEMA_VERSION}  \n"
        f"**Paper Only**: True | **No Real Orders**: True"
    )
    top_candidates = (
        "## Top Candidates\n"
        + (("\n".join(f"- {s}" for s in report_input.candidates))
           if report_input.candidates else "_No candidates_")
    )
    blocked_candidates = "## Blocked Candidates\n_None blocked at this time._"
    abc_setup_table = (
        "## A/B/C Setup Table\n"
        "| Symbol | Setup | Action |\n"
        "|--------|-------|--------|\n"
        + (("\n".join(f"| {s} | NO_ENTRY | NO_ENTRY |" for s in report_input.candidates))
           if report_input.candidates else "| — | — | — |")
    )
    risk_budget_table = (
        "## Risk Budget Table\n"
        "| Metric | Value |\n"
        "|--------|-------|\n"
        "| Risk Budget Remaining | 100% |\n"
        "| Status | NORMAL |"
    )
    decision_ticket_section = (
        "## Decision Ticket Section\n"
        "_[!] Paper Only. No real orders will be placed._\n"
        "_Human review required before any action._"
    )
    human_review_section = (
        "## Human Review Required\n"
        "**ALL candidates require human review before any paper action.**\n"
        "- human_review_required = True\n"
        "- No automatic execution."
    )
    safety_guard_section = (
        "## Safety Guard Section\n"
        "- NO_REAL_ORDERS = True\n"
        "- BROKER_EXECUTION_ENABLED = False\n"
        "- PRODUCTION_TRADING_BLOCKED = True\n"
        "- paper_only_guard_enabled = True"
    )
    final_action_summary = (
        "## Final Action Summary\n"
        f"- Total candidates: {len(report_input.candidates)}\n"
        "- All actions: paper-only plans\n"
        "- Human review required: True"
    )

    full_markdown = "\n\n".join([
        title, summary, top_candidates, blocked_candidates,
        abc_setup_table, risk_budget_table, decision_ticket_section,
        human_review_section, safety_guard_section, final_action_summary,
    ])

    return MarkdownReport(
        title=title,
        summary=summary,
        top_candidates=top_candidates,
        blocked_candidates=blocked_candidates,
        abc_setup_table=abc_setup_table,
        risk_budget_table=risk_budget_table,
        decision_ticket_section=decision_ticket_section,
        human_review_required_section=human_review_section,
        safety_guard_section=safety_guard_section,
        final_action_summary=final_action_summary,
        full_markdown=full_markdown,
    )


def export_csv(report_input: Optional[ReportExportInput] = None) -> CSVExportResult:
    """Export report as CSV strings. Paper only, in-memory."""
    if report_input is None:
        report_input = ReportExportInput()

    candidates = report_input.candidates or []
    n = len(candidates)

    # candidates.csv
    cand_header = "symbol,name,rank,total_score,abc_type,final_action,entry_allowed,human_review_required\n"
    cand_rows = "".join(
        f"{s},{s}_name,{i + 1},0.0,NO_ENTRY,NO_ENTRY,False,True\n"
        for i, s in enumerate(candidates)
    )
    candidates_csv = cand_header + cand_rows

    # decision_tickets.csv
    dt_header = "ticket_id,symbol,setup_type,final_action,entry_price_plan,stop_loss_price,risk_amount,human_review_required\n"
    dt_rows = "".join(
        f"PC202-TKT-{i + 1:03d},{s},NO_ENTRY,NO_ENTRY,0.0,0.0,4500.0,True\n"
        for i, s in enumerate(candidates)
    )
    decision_tickets_csv = dt_header + dt_rows

    # no_entry_reasons.csv
    ner_header = "symbol,reason_code,reason_label,severity,recommendation\n"
    no_entry_reasons_csv = ner_header

    # risk_overlay.csv
    ro_header = "symbol,risk_overlay_status,portfolio_risk_pct,risk_budget_remaining_pct,risk_budget_ok\n"
    ro_rows = "".join(
        f"{s},NORMAL,0.0,100.0,True\n"
        for s in candidates
    )
    risk_overlay_csv = ro_header + ro_rows

    # final_actions.csv
    fa_header = "symbol,final_action,paper_only,human_review_required\n"
    fa_rows = "".join(
        f"{s},NO_ENTRY,True,True\n"
        for s in candidates
    )
    final_actions_csv = fa_header + fa_rows

    return CSVExportResult(
        candidates_csv=candidates_csv,
        candidates_rows=n,
        decision_tickets_csv=decision_tickets_csv,
        decision_tickets_rows=n,
        no_entry_reasons_csv=no_entry_reasons_csv,
        no_entry_reasons_rows=0,
        risk_overlay_csv=risk_overlay_csv,
        risk_overlay_rows=n,
        final_actions_csv=final_actions_csv,
        final_actions_rows=n,
        export_ok=True,
    )


def build_audit_pack(report_input: Optional[ReportExportInput] = None) -> AuditPackResult:
    """Build an audit pack with all snapshot fields. Paper only, in-memory."""
    if report_input is None:
        report_input = ReportExportInput()

    run_metadata = {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "run_date": report_input.run_date,
        "report_id": report_input.report_id,
        "source": report_input.source,
        "paper_only": True,
        "no_real_orders": True,
    }
    input_snapshot = {
        "report_format": report_input.report_format,
        "watchlist_symbols": report_input.watchlist_symbols,
        "candidates": report_input.candidates,
        "include_audit_pack": report_input.include_audit_pack,
        "include_markdown": report_input.include_markdown,
        "include_csv": report_input.include_csv,
    }
    decision_snapshot = {
        "abc_entry_status": "NO_ENTRY",
        "final_actions": [],
        "paper_only": True,
        "human_review_required": True,
    }
    risk_snapshot = {
        "risk_overlay_status": "NORMAL",
        "portfolio_risk_pct": 0.0,
        "risk_budget_remaining_pct": 100.0,
        "risk_budget_ok": True,
    }
    ticket_snapshot = {
        "paper_decision_tickets": [],
        "ticket_count": 0,
        "paper_only": True,
    }
    blocked_reason_snapshot = {
        "no_entry_reasons": [],
        "blocked_count": 0,
    }
    human_review_snapshot = {
        "human_review_required": True,
        "human_review_flags": ["all_candidates_require_review"],
        "no_automatic_execution": True,
    }
    safety_snapshot = {
        "NO_REAL_ORDERS": True,
        "BROKER_EXECUTION_ENABLED": False,
        "PRODUCTION_TRADING_BLOCKED": True,
        "paper_only_guard_enabled": True,
        "no_real_account_sync": True,
        "no_automatic_rebalance": True,
    }

    hash_str = (
        f"{VERSION}:{SCHEMA_VERSION}:{report_input.report_id}:"
        f"{report_input.run_date}:{report_input.candidates}"
    )
    reproducibility_hash = _make_reproducibility_hash(hash_str)

    return AuditPackResult(
        pack_id=f"PC202-PACK-{report_input.report_id}",
        run_metadata=run_metadata,
        input_snapshot=input_snapshot,
        decision_snapshot=decision_snapshot,
        risk_snapshot=risk_snapshot,
        ticket_snapshot=ticket_snapshot,
        blocked_reason_snapshot=blocked_reason_snapshot,
        human_review_snapshot=human_review_snapshot,
        safety_snapshot=safety_snapshot,
        reproducibility_hash=reproducibility_hash,
        export_format=report_input.report_format,
        export_status="ok",
    )


def export_all(report_input: Optional[ReportExportInput] = None) -> ExportStatusSummary:
    """Run all exports and return combined status. Paper only."""
    if report_input is None:
        report_input = ReportExportInput()

    json_result = export_json(report_input)
    md_result = export_markdown(report_input)
    csv_result = export_csv(report_input)
    audit_result = build_audit_pack(report_input)

    return ExportStatusSummary(
        formats_available=list(EXPORT_FORMATS),
        json_ok=json_result.is_valid,
        markdown_ok=bool(md_result.full_markdown),
        csv_ok=csv_result.export_ok,
        audit_pack_ok=(audit_result.export_status == "ok"),
        export_ok=True,
        paper_only_guard_enabled=True,
        broker_execution_disabled=not BROKER_EXECUTION_ENABLED,
        production_trading_blocked=PRODUCTION_TRADING_BLOCKED,
    )


def get_report_export_summary() -> Dict[str, Any]:
    """Return a summary dict of the report export engine. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "export_formats": EXPORT_FORMATS,
        "csv_export_names": CSV_EXPORT_NAMES,
        "audit_pack_fields": AUDIT_PACK_FIELDS,
        "markdown_sections": MARKDOWN_SECTIONS,
        "cli_commands": CLI_COMMANDS_V202,
        "gui_tabs": GUI_TABS_V202,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "human_review_required": True,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }


def get_version_info_v202() -> Dict[str, Any]:
    """Return version info dict for v2.0.2. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "human_review_required": True,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
        "models_count": len(_ALL_MODEL_NAMES_V202),
        "cli_commands_count": len(CLI_COMMANDS_V202),
        "gui_tabs_count": len(GUI_TABS_V202),
        "export_formats_count": len(EXPORT_FORMATS),
        "csv_names_count": len(CSV_EXPORT_NAMES),
        "audit_pack_fields_count": len(AUDIT_PACK_FIELDS),
    }


def verify_version_v202() -> bool:
    """Verify that VERSION == '2.0.2'. Returns True if OK."""
    return VERSION == "2.0.2" and SCHEMA_VERSION == "202"


def build_report_candidate_row(
    symbol: str = "",
    name: str = "",
    rank: int = 0,
    total_score: float = 0.0,
    abc_type: str = "NO_ENTRY",
    final_action: str = "NO_ENTRY",
    entry_allowed: bool = False,
    block_reason: str = "",
) -> ReportCandidateRow:
    """Build a ReportCandidateRow. Paper only."""
    return ReportCandidateRow(
        symbol=symbol,
        name=name,
        rank=rank,
        total_score=total_score,
        abc_type=abc_type,
        final_action=final_action,
        entry_allowed=entry_allowed,
        block_reason=block_reason,
    )


def build_report_ticket_row(
    ticket_id: str = "",
    symbol: str = "",
    name: str = "",
    setup_type: str = "NO_ENTRY",
    final_action: str = "NO_ENTRY",
    entry_price_plan: float = 0.0,
    stop_loss_price: float = 0.0,
    risk_amount: float = 0.0,
    position_size: float = 0.0,
    no_entry_reasons: Optional[List[str]] = None,
) -> ReportTicketRow:
    """Build a ReportTicketRow. Paper only."""
    if no_entry_reasons is None:
        no_entry_reasons = []
    return ReportTicketRow(
        ticket_id=ticket_id,
        symbol=symbol,
        name=name,
        setup_type=setup_type,
        final_action=final_action,
        entry_price_plan=entry_price_plan,
        stop_loss_price=stop_loss_price,
        risk_amount=risk_amount,
        position_size=position_size,
        no_entry_reasons=list(no_entry_reasons),
    )


def build_full_report(
    report_input: Optional[ReportExportInput] = None,
) -> ReportExportOutput:
    """Build a full ReportExportOutput. Paper only."""
    if report_input is None:
        report_input = ReportExportInput()

    safety_flags = {
        "NO_REAL_ORDERS": True,
        "BROKER_EXECUTION_ENABLED": False,
        "PRODUCTION_TRADING_BLOCKED": True,
        "paper_only_guard_enabled": True,
    }

    return ReportExportOutput(
        report_id=report_input.report_id,
        generated_at=f"{report_input.run_date}T00:00:00",
        source=report_input.source,
        watchlist_summary=f"symbols={report_input.watchlist_symbols}",
        candidate_ranking=list(report_input.candidates),
        abc_entry_status="NO_ENTRY",
        no_entry_reasons=[],
        risk_overlay_status="NORMAL",
        position_sizing_suggestion="PAPER_ALLOW_NORMAL_SIZE",
        paper_decision_tickets=[],
        human_review_flags=["human_review_required=True"],
        final_actions=["NO_ENTRY"] * len(report_input.candidates),
        paper_only_safety_flags=safety_flags,
        export_ok=True,
    )


def get_cockpit_summary_v202() -> Dict[str, Any]:
    """Return full cockpit summary for v2.0.2. Paper only."""
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "human_review_required": True,
        "models": _ALL_MODEL_NAMES_V202,
        "cli_commands": CLI_COMMANDS_V202,
        "gui_tabs": GUI_TABS_V202,
        "export_formats": EXPORT_FORMATS,
        "csv_names": CSV_EXPORT_NAMES,
        "audit_pack_fields": AUDIT_PACK_FIELDS,
        "markdown_sections": MARKDOWN_SECTIONS,
        "safety_flags": SAFETY_FLAGS_V202,
        "NO_REAL_ORDERS": NO_REAL_ORDERS,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }
