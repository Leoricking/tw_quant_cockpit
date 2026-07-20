"""
tests/test_paper_cockpit_csv_v202.py
v2.0.2 Paper Cockpit — CSV Export Tests (40+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# CSVExportResult dataclass tests
# ---------------------------------------------------------------------------

def test_csv_export_result_defaults():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.no_real_orders is True
    assert obj.export_ok is True
    assert obj.human_review_required is True


def test_csv_export_result_csv_names_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert len(obj.csv_names) == 5


def test_csv_export_result_has_candidates_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert "candidates.csv" in obj.csv_names


def test_csv_export_result_has_decision_tickets_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert "decision_tickets.csv" in obj.csv_names


def test_csv_export_result_has_no_entry_reasons_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert "no_entry_reasons.csv" in obj.csv_names


def test_csv_export_result_has_risk_overlay_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert "risk_overlay.csv" in obj.csv_names


def test_csv_export_result_has_final_actions_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSVExportResult
    obj = CSVExportResult()
    assert "final_actions.csv" in obj.csv_names


# ---------------------------------------------------------------------------
# export_csv tests
# ---------------------------------------------------------------------------

def test_export_csv_returns_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result is not None


def test_export_csv_export_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.export_ok is True


def test_export_csv_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.schema_version == "202"


def test_export_csv_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.paper_only is True


def test_export_csv_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.no_real_orders is True


def test_export_csv_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.human_review_required is True


def test_export_csv_csv_names_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert len(result.csv_names) == 5


def test_export_csv_candidates_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert "symbol" in result.candidates_csv
    assert "final_action" in result.candidates_csv


def test_export_csv_decision_tickets_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert "ticket_id" in result.decision_tickets_csv
    assert "symbol" in result.decision_tickets_csv


def test_export_csv_no_entry_reasons_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert "symbol" in result.no_entry_reasons_csv
    assert "reason_code" in result.no_entry_reasons_csv


def test_export_csv_risk_overlay_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert "symbol" in result.risk_overlay_csv
    assert "risk_overlay_status" in result.risk_overlay_csv


def test_export_csv_final_actions_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert "symbol" in result.final_actions_csv
    assert "final_action" in result.final_actions_csv


def test_export_csv_empty_candidates_rows_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.candidates_rows == 0


def test_export_csv_with_3_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330", "2454", "2317"])
    result = export_csv(inp)
    assert result.candidates_rows == 3
    assert result.decision_tickets_rows == 3
    assert result.risk_overlay_rows == 3
    assert result.final_actions_rows == 3


def test_export_csv_candidates_csv_contains_symbol():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "2330" in result.candidates_csv


def test_export_csv_decision_tickets_contains_symbol():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "2330" in result.decision_tickets_csv


def test_export_csv_risk_overlay_contains_symbol():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "2330" in result.risk_overlay_csv


def test_export_csv_final_actions_contains_symbol():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "2330" in result.final_actions_csv


def test_export_csv_final_actions_no_entry():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "NO_ENTRY" in result.final_actions_csv


def test_export_csv_candidates_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "True" in result.candidates_csv or "human_review_required" in result.candidates_csv


def test_export_csv_decision_tickets_has_risk_amount():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "4500.0" in result.decision_tickets_csv


def test_export_csv_risk_overlay_normal():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330"])
    result = export_csv(inp)
    assert "NORMAL" in result.risk_overlay_csv


def test_export_csv_no_entry_reasons_empty_by_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.no_entry_reasons_rows == 0


def test_export_csv_candidates_has_rank():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv, ReportExportInput
    inp = ReportExportInput(candidates=["2330", "2454"])
    result = export_csv(inp)
    assert "1" in result.candidates_csv
    assert "2" in result.candidates_csv


def test_export_csv_candidates_csv_is_string():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert isinstance(result.candidates_csv, str)


def test_export_csv_decision_tickets_csv_is_string():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert isinstance(result.decision_tickets_csv, str)


def test_export_csv_risk_overlay_csv_is_string():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert isinstance(result.risk_overlay_csv, str)


def test_export_csv_final_actions_csv_is_string():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert isinstance(result.final_actions_csv, str)


def test_export_csv_no_entry_reasons_csv_is_string():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert isinstance(result.no_entry_reasons_csv, str)


def test_csv_export_names_constant():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CSV_EXPORT_NAMES
    expected = {"candidates.csv", "decision_tickets.csv", "no_entry_reasons.csv",
                "risk_overlay.csv", "final_actions.csv"}
    assert set(CSV_EXPORT_NAMES) == expected
