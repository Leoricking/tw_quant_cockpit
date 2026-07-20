"""
tests/test_paper_cockpit_report_export_v202.py
v2.0.2 Paper Cockpit — Report Export Engine Tests (60+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
import pytest


# ---------------------------------------------------------------------------
# export_json tests
# ---------------------------------------------------------------------------

def test_export_json_returns_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result is not None


def test_export_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.is_valid is True


def test_export_json_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.schema_version == "202"


def test_export_json_report_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.report_version == "2.0.2"


def test_export_json_source():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.source == "paper_cockpit"


def test_export_json_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.paper_only is True


def test_export_json_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.no_real_orders is True


def test_export_json_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.human_review_required is True


def test_export_json_export_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.export_format == "json"


def test_export_json_str_non_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.json_str


def test_export_json_str_parseable():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    assert isinstance(parsed, dict)


def test_export_json_str_has_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    assert parsed["schema_version"] == "202"


def test_export_json_str_has_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    assert parsed["paper_only"] is True


def test_export_json_str_has_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    assert parsed["no_real_orders"] is True


def test_export_json_str_has_report_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    assert "report_id" in parsed


def test_export_json_str_has_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    assert parsed["human_review_required"] is True


def test_export_json_str_has_safety_flags():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    assert "paper_only_safety_flags" in parsed


def test_export_json_str_safety_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    flags = parsed["paper_only_safety_flags"]
    assert flags["NO_REAL_ORDERS"] is True


def test_export_json_str_safety_broker_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    parsed = json.loads(result.json_str)
    flags = parsed["paper_only_safety_flags"]
    assert flags["BROKER_EXECUTION_ENABLED"] is False


def test_export_json_with_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json, ReportExportInput
    inp = ReportExportInput(candidates=["2330", "2454"])
    result = export_json(inp)
    assert result.is_valid is True
    parsed = json.loads(result.json_str)
    assert "2330" in parsed["candidate_ranking"]


# ---------------------------------------------------------------------------
# export_markdown tests
# ---------------------------------------------------------------------------

def test_export_markdown_returns_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result is not None


def test_export_markdown_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.schema_version == "202"


def test_export_markdown_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.paper_only is True


def test_export_markdown_has_title():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.title
    assert "2.0.2" in result.title


def test_export_markdown_has_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.summary


def test_export_markdown_has_top_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.top_candidates
    assert "Top Candidates" in result.top_candidates


def test_export_markdown_has_blocked_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.blocked_candidates
    assert "Blocked Candidates" in result.blocked_candidates


def test_export_markdown_has_abc_setup_table():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.abc_setup_table
    assert "A/B/C" in result.abc_setup_table


def test_export_markdown_has_risk_budget_table():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.risk_budget_table
    assert "Risk Budget" in result.risk_budget_table


def test_export_markdown_has_decision_ticket_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.decision_ticket_section
    assert "Decision Ticket" in result.decision_ticket_section


def test_export_markdown_has_human_review_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.human_review_required_section
    assert "Human Review" in result.human_review_required_section


def test_export_markdown_has_safety_guard_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.safety_guard_section
    assert "Safety Guard" in result.safety_guard_section


def test_export_markdown_has_final_action_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.final_action_summary
    assert "Final Action" in result.final_action_summary


def test_export_markdown_has_full_markdown():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.full_markdown
    assert len(result.full_markdown) > 100


def test_export_markdown_full_md_has_title():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "# Paper Cockpit Report" in result.full_markdown


def test_export_markdown_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.human_review_required is True


def test_export_markdown_with_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown, ReportExportInput
    inp = ReportExportInput(candidates=["2330", "2454"])
    result = export_markdown(inp)
    assert "2330" in result.top_candidates


# ---------------------------------------------------------------------------
# build_full_report tests
# ---------------------------------------------------------------------------

def test_build_full_report_returns_output():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result is not None


def test_build_full_report_report_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result.report_version == "2.0.2"


def test_build_full_report_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result.paper_only is True


def test_build_full_report_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result.no_real_orders is True


def test_build_full_report_source():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result.source == "paper_cockpit"


def test_build_full_report_export_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result.export_ok is True


def test_build_full_report_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result.human_review_required is True


def test_build_full_report_has_safety_flags():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_full_report
    result = build_full_report()
    assert result.paper_only_safety_flags["NO_REAL_ORDERS"] is True


def test_build_report_candidate_row():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_report_candidate_row
    row = build_report_candidate_row(symbol="2330", name="TSMC", rank=1, total_score=90.0)
    assert row.symbol == "2330"
    assert row.rank == 1
    assert row.paper_only is True


def test_build_report_ticket_row():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_report_ticket_row
    row = build_report_ticket_row(
        ticket_id="PC202-TKT-001", symbol="2330",
        entry_price_plan=580.0, risk_amount=4500.0
    )
    assert row.ticket_id == "PC202-TKT-001"
    assert row.entry_price_plan == 580.0
    assert row.paper_only is True


def test_export_all_returns_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result is not None
    assert result.export_ok is True


def test_export_all_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.paper_only is True


def test_export_all_formats_available():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert len(result.formats_available) == 4


def test_export_all_json_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.json_ok is True


def test_export_all_markdown_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.markdown_ok is True


def test_export_all_csv_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.csv_ok is True


def test_export_all_audit_pack_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.audit_pack_ok is True


def test_export_all_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.broker_execution_disabled is True


def test_export_all_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_all
    result = export_all()
    assert result.production_trading_blocked is True
