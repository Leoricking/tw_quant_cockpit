"""
tests/test_paper_cockpit_no_entry_v201.py
v2.0.1 Paper Cockpit — No-Entry Reason Tests (40+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
    NO_ENTRY_REASONS, NoEntryReasonDetail, evaluate_no_entry_reasons,
)


# --- NO_ENTRY_REASONS list tests ---

def test_no_entry_reasons_is_list():
    assert isinstance(NO_ENTRY_REASONS, list)

def test_no_entry_reasons_count():
    assert len(NO_ENTRY_REASONS) == 13

def test_no_entry_reason_trend_broken():
    assert "trend_broken" in NO_ENTRY_REASONS

def test_no_entry_reason_below_20ma():
    assert "below_20ma" in NO_ENTRY_REASONS

def test_no_entry_reason_below_60ma():
    assert "below_60ma" in NO_ENTRY_REASONS

def test_no_entry_reason_volume_overheated():
    assert "volume_overheated" in NO_ENTRY_REASONS

def test_no_entry_reason_volume_dry_up_failed():
    assert "volume_dry_up_failed" in NO_ENTRY_REASONS

def test_no_entry_reason_institutional_selling():
    assert "institutional_selling" in NO_ENTRY_REASONS

def test_no_entry_reason_margin_overheated():
    assert "margin_overheated" in NO_ENTRY_REASONS

def test_no_entry_reason_market_risk_high():
    assert "market_risk_high" in NO_ENTRY_REASONS

def test_no_entry_reason_risk_budget_exceeded():
    assert "risk_budget_exceeded" in NO_ENTRY_REASONS

def test_no_entry_reason_position_size_too_large():
    assert "position_size_too_large" in NO_ENTRY_REASONS

def test_no_entry_reason_stop_loss_too_wide():
    assert "stop_loss_too_wide" in NO_ENTRY_REASONS

def test_no_entry_reason_missing_required_signal():
    assert "missing_required_signal" in NO_ENTRY_REASONS

def test_no_entry_reason_human_review_required():
    assert "human_review_required" in NO_ENTRY_REASONS

def test_all_reasons_are_strings():
    assert all(isinstance(r, str) for r in NO_ENTRY_REASONS)

def test_all_reasons_are_unique():
    assert len(set(NO_ENTRY_REASONS)) == len(NO_ENTRY_REASONS)


# --- NoEntryReasonDetail dataclass tests ---

def test_no_entry_reason_detail_default():
    d = NoEntryReasonDetail()
    assert d.schema_version == "201"
    assert d.paper_only is True
    assert d.no_real_orders is True
    assert d.is_valid_reason is False

def test_no_entry_reason_detail_valid_trend_broken():
    d = NoEntryReasonDetail(reason_code="trend_broken")
    assert d.is_valid_reason is True

def test_no_entry_reason_detail_valid_below_20ma():
    d = NoEntryReasonDetail(reason_code="below_20ma")
    assert d.is_valid_reason is True

def test_no_entry_reason_detail_valid_below_60ma():
    d = NoEntryReasonDetail(reason_code="below_60ma")
    assert d.is_valid_reason is True

def test_no_entry_reason_detail_valid_volume_overheated():
    d = NoEntryReasonDetail(reason_code="volume_overheated")
    assert d.is_valid_reason is True

def test_no_entry_reason_detail_valid_institutional_selling():
    d = NoEntryReasonDetail(reason_code="institutional_selling")
    assert d.is_valid_reason is True

def test_no_entry_reason_detail_valid_market_risk_high():
    d = NoEntryReasonDetail(reason_code="market_risk_high")
    assert d.is_valid_reason is True

def test_no_entry_reason_detail_valid_human_review_required():
    d = NoEntryReasonDetail(reason_code="human_review_required")
    assert d.is_valid_reason is True

def test_no_entry_reason_detail_invalid_code():
    d = NoEntryReasonDetail(reason_code="invalid_code_xyz")
    assert d.is_valid_reason is False

def test_no_entry_reason_detail_default_severity():
    d = NoEntryReasonDetail(reason_code="trend_broken")
    assert d.severity == "HIGH"

def test_no_entry_reason_detail_default_recommendation():
    d = NoEntryReasonDetail()
    assert d.recommendation == "PAPER_BLOCK_NEW_ENTRY"

def test_no_entry_reason_detail_human_review_recommendation():
    d = NoEntryReasonDetail(
        reason_code="human_review_required",
        recommendation="PAPER_REQUIRE_HUMAN_REVIEW",
    )
    assert d.recommendation == "PAPER_REQUIRE_HUMAN_REVIEW"


# --- evaluate_no_entry_reasons tests ---

def test_evaluate_no_entry_reasons_no_args():
    reasons = evaluate_no_entry_reasons()
    assert isinstance(reasons, list)
    # human_review_required always appended
    codes = [r.reason_code for r in reasons]
    assert "human_review_required" in codes

def test_evaluate_no_entry_reasons_empty():
    reasons = evaluate_no_entry_reasons({}, {})
    assert len(reasons) == 1  # only human_review_required
    assert reasons[0].reason_code == "human_review_required"

def test_evaluate_no_entry_reasons_trend_broken():
    reasons = evaluate_no_entry_reasons({"trend_broken": True})
    codes = [r.reason_code for r in reasons]
    assert "trend_broken" in codes

def test_evaluate_no_entry_reasons_below_20ma():
    reasons = evaluate_no_entry_reasons({"below_20ma": True})
    codes = [r.reason_code for r in reasons]
    assert "below_20ma" in codes

def test_evaluate_no_entry_reasons_below_60ma():
    reasons = evaluate_no_entry_reasons({"below_60ma": True})
    codes = [r.reason_code for r in reasons]
    assert "below_60ma" in codes

def test_evaluate_no_entry_reasons_volume_overheated():
    reasons = evaluate_no_entry_reasons({"volume_overheated": True})
    codes = [r.reason_code for r in reasons]
    assert "volume_overheated" in codes

def test_evaluate_no_entry_reasons_volume_dry_up_failed():
    reasons = evaluate_no_entry_reasons({"volume_dry_up_failed": True})
    codes = [r.reason_code for r in reasons]
    assert "volume_dry_up_failed" in codes

def test_evaluate_no_entry_reasons_institutional_selling():
    reasons = evaluate_no_entry_reasons({"institutional_selling": True})
    codes = [r.reason_code for r in reasons]
    assert "institutional_selling" in codes

def test_evaluate_no_entry_reasons_margin_overheated():
    reasons = evaluate_no_entry_reasons({"margin_overheated": True})
    codes = [r.reason_code for r in reasons]
    assert "margin_overheated" in codes

def test_evaluate_no_entry_reasons_market_risk_high():
    reasons = evaluate_no_entry_reasons({}, {"market_risk_high": True})
    codes = [r.reason_code for r in reasons]
    assert "market_risk_high" in codes

def test_evaluate_no_entry_reasons_risk_budget_exceeded():
    reasons = evaluate_no_entry_reasons({}, {"risk_budget_exceeded": True})
    codes = [r.reason_code for r in reasons]
    assert "risk_budget_exceeded" in codes

def test_evaluate_no_entry_reasons_position_size_too_large():
    reasons = evaluate_no_entry_reasons({}, {"position_size_too_large": True})
    codes = [r.reason_code for r in reasons]
    assert "position_size_too_large" in codes

def test_evaluate_no_entry_reasons_stop_loss_too_wide():
    reasons = evaluate_no_entry_reasons({}, {"stop_loss_too_wide": True})
    codes = [r.reason_code for r in reasons]
    assert "stop_loss_too_wide" in codes

def test_evaluate_no_entry_reasons_missing_required_signal():
    reasons = evaluate_no_entry_reasons({"missing_required_signal": True})
    codes = [r.reason_code for r in reasons]
    assert "missing_required_signal" in codes

def test_evaluate_no_entry_reasons_all_codes_are_valid():
    technical_data = {
        "trend_broken": True, "below_20ma": True, "below_60ma": True,
        "volume_overheated": True, "volume_dry_up_failed": True,
        "institutional_selling": True, "margin_overheated": True,
        "missing_required_signal": True,
    }
    risk_data = {
        "market_risk_high": True, "risk_budget_exceeded": True,
        "position_size_too_large": True, "stop_loss_too_wide": True,
    }
    reasons = evaluate_no_entry_reasons(technical_data, risk_data)
    for r in reasons:
        assert r.is_valid_reason is True, f"Invalid reason code: {r.reason_code}"

def test_evaluate_no_entry_reasons_false_flags_not_added():
    reasons = evaluate_no_entry_reasons({"trend_broken": False})
    codes = [r.reason_code for r in reasons]
    assert "trend_broken" not in codes

def test_evaluate_no_entry_reasons_returns_list_of_detail():
    reasons = evaluate_no_entry_reasons({"trend_broken": True})
    assert all(isinstance(r, NoEntryReasonDetail) for r in reasons)
