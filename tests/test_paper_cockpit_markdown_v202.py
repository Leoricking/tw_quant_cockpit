"""
tests/test_paper_cockpit_markdown_v202.py
v2.0.2 Paper Cockpit — Markdown Report Tests (40+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# MarkdownReport dataclass tests
# ---------------------------------------------------------------------------

def test_markdown_report_defaults():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MarkdownReport
    obj = MarkdownReport()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.no_real_orders is True
    assert obj.human_review_required is True


def test_markdown_report_fields_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MarkdownReport, MARKDOWN_SECTIONS
    obj = MarkdownReport()
    for section in MARKDOWN_SECTIONS:
        assert hasattr(obj, section), f"Missing section field: {section}"


def test_markdown_sections_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert len(MARKDOWN_SECTIONS) == 10


def test_markdown_section_title_in_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "title" in MARKDOWN_SECTIONS


def test_markdown_section_summary_in_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "summary" in MARKDOWN_SECTIONS


def test_markdown_section_top_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "top_candidates" in MARKDOWN_SECTIONS


def test_markdown_section_blocked_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "blocked_candidates" in MARKDOWN_SECTIONS


def test_markdown_section_abc_setup_table():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "abc_setup_table" in MARKDOWN_SECTIONS


def test_markdown_section_risk_budget_table():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "risk_budget_table" in MARKDOWN_SECTIONS


def test_markdown_section_decision_ticket_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "decision_ticket_section" in MARKDOWN_SECTIONS


def test_markdown_section_human_review_required_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "human_review_required_section" in MARKDOWN_SECTIONS


def test_markdown_section_safety_guard_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "safety_guard_section" in MARKDOWN_SECTIONS


def test_markdown_section_final_action_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import MARKDOWN_SECTIONS
    assert "final_action_summary" in MARKDOWN_SECTIONS


# ---------------------------------------------------------------------------
# export_markdown output tests
# ---------------------------------------------------------------------------

def test_markdown_title_has_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "v2.0.2" in result.title or "2.0.2" in result.title


def test_markdown_title_starts_with_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.title.startswith("#")


def test_markdown_summary_has_report_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "Report ID" in result.summary


def test_markdown_summary_has_run_date():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "Run Date" in result.summary


def test_markdown_summary_has_source():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "Source" in result.summary


def test_markdown_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "Paper Only" in result.summary or "paper_only" in result.summary.lower()


def test_markdown_top_candidates_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "##" in result.top_candidates


def test_markdown_top_candidates_empty_message():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "No candidates" in result.top_candidates or "-" in result.top_candidates


def test_markdown_top_candidates_with_symbols():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown, ReportExportInput
    inp = ReportExportInput(candidates=["2330", "2454"])
    result = export_markdown(inp)
    assert "2330" in result.top_candidates
    assert "2454" in result.top_candidates


def test_markdown_abc_table_has_columns():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "Symbol" in result.abc_setup_table
    assert "Setup" in result.abc_setup_table


def test_markdown_risk_budget_table_has_columns():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "Metric" in result.risk_budget_table
    assert "Value" in result.risk_budget_table


def test_markdown_risk_budget_normal_status():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "NORMAL" in result.risk_budget_table


def test_markdown_decision_ticket_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "Paper Only" in result.decision_ticket_section or "paper" in result.decision_ticket_section.lower()


def test_markdown_human_review_section_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "human_review_required" in result.human_review_required_section or \
           "human review" in result.human_review_required_section.lower()


def test_markdown_safety_guard_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "NO_REAL_ORDERS" in result.safety_guard_section


def test_markdown_safety_guard_broker_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "BROKER_EXECUTION_ENABLED" in result.safety_guard_section


def test_markdown_safety_guard_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "PRODUCTION_TRADING_BLOCKED" in result.safety_guard_section


def test_markdown_final_action_summary_has_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "candidates" in result.final_action_summary.lower()


def test_markdown_final_action_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert "human review" in result.final_action_summary.lower() or \
           "Human review" in result.final_action_summary


def test_markdown_full_markdown_contains_all_sections():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    md = result.full_markdown
    assert "Top Candidates" in md
    assert "Blocked Candidates" in md
    assert "Risk Budget" in md
    assert "Decision Ticket" in md
    assert "Human Review" in md
    assert "Safety Guard" in md
    assert "Final Action" in md


def test_markdown_full_markdown_no_forbidden_words():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    md = result.full_markdown.upper()
    # These should not appear as standalone action words
    forbidden = [" EXECUTE ", " SUBMIT_ORDER ", " AUTO_TRADE ", " LIVE_TRADE ", " BROKER_ORDER "]
    for word in forbidden:
        assert word not in md, f"Forbidden word '{word}' found in markdown"


def test_markdown_export_with_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown, ReportExportInput
    inp = ReportExportInput(
        report_id="PC202-RPT-TEST",
        run_date="2026-07-20",
        candidates=["2330"],
    )
    result = export_markdown(inp)
    assert result.summary
    assert "2330" in result.top_candidates
