"""
tests/test_decision_journal_engine_v189.py
Tests for decision_journal_engine_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_journal_models_v189 import (
    DecisionJournalEntry, DecisionJournalBook, DecisionReviewInput,
)
from paper_trading.small_capital_strategy.decision_journal_engine_v189 import (
    validate_journal_action, validate_journal_state, validate_quality_grade,
    validate_mistake_tag, validate_review_dimension,
    create_journal_entry, validate_journal_entry, create_journal_book,
    run_review, build_daily_review, build_weekly_review, build_monthly_review,
    build_quality_score, build_evidence_link, build_audit_trail,
    build_evidence_pack, build_export_manifest, build_dashboard,
    build_review_checklist, get_engine_info,
)


def _entry(**kw) -> DecisionJournalEntry:
    defaults = dict(
        entry_id="E-TEST", date_label="2026-W01-D1", state="OBSERVE",
        symbol="TSMC", rationale="Test rationale", evidence_refs=["ev1"],
        workflow_id="WF-001", market_regime="BULL",
    )
    defaults.update(kw)
    return create_journal_entry(**defaults)


def _rev_input(**kw) -> DecisionReviewInput:
    book = kw.pop("book", None)
    defaults = dict(
        review_type="daily_review", date_label="2026-W01-D1",
        source_workflow_id="WF-001", market_regime="BULL",
        total_exposure_pct=20.0, cash_reserve_pct=80.0,
    )
    defaults.update(kw)
    ri = DecisionReviewInput(**defaults)
    ri.journal_book = book
    return ri


# ── validate_journal_action ────────────────────────────────────────────────────

def test_validate_action_observe():
    assert validate_journal_action("OBSERVE") is True


def test_validate_action_wait():
    assert validate_journal_action("WAIT") is True


def test_validate_action_paper_plan_ready():
    assert validate_journal_action("PAPER_PLAN_READY") is True


def test_validate_action_paper_entry_allowed():
    assert validate_journal_action("PAPER_ENTRY_ALLOWED") is True


def test_validate_action_reduce_risk():
    assert validate_journal_action("REDUCE_RISK") is True


def test_validate_action_blocked():
    assert validate_journal_action("BLOCKED") is True


def test_validate_action_no_trade():
    assert validate_journal_action("NO_TRADE") is True


def test_validate_action_audit_only():
    assert validate_journal_action("AUDIT_ONLY") is True


def test_validate_action_buy_false():
    assert validate_journal_action("BUY") is False


def test_validate_action_sell_false():
    assert validate_journal_action("SELL") is False


def test_validate_action_broker_order_false():
    assert validate_journal_action("BROKER_ORDER") is False


# ── validate_journal_state ─────────────────────────────────────────────────────

def test_validate_state_observe():
    assert validate_journal_state("OBSERVE") is True


def test_validate_state_paper_plan_ready():
    assert validate_journal_state("PAPER_PLAN_READY") is True


def test_validate_state_invalid_false():
    assert validate_journal_state("INVALID_STATE") is False


def test_validate_state_buy_false():
    assert validate_journal_state("BUY") is False


# ── validate_quality_grade ─────────────────────────────────────────────────────

def test_validate_grade_excellent():
    assert validate_quality_grade("EXCELLENT") is True


def test_validate_grade_poor():
    assert validate_quality_grade("POOR") is True


def test_validate_grade_invalid():
    assert validate_quality_grade("INVALID") is True


def test_validate_grade_unknown_false():
    assert validate_quality_grade("UNKNOWN_GRADE") is False


# ── validate_mistake_tag ───────────────────────────────────────────────────────

def test_validate_mistake_tag_chase_high():
    assert validate_mistake_tag("CHASE_HIGH") is True


def test_validate_mistake_tag_no_mistake():
    assert validate_mistake_tag("NO_MISTAKE_FOUND") is True


def test_validate_mistake_tag_unknown_false():
    assert validate_mistake_tag("INVALID_TAG") is False


# ── validate_review_dimension ──────────────────────────────────────────────────

def test_validate_dimension_market_regime():
    assert validate_review_dimension("market_regime_alignment") is True


def test_validate_dimension_audit_traceability():
    assert validate_review_dimension("audit_traceability") is True


def test_validate_dimension_unknown_false():
    assert validate_review_dimension("unknown_dimension") is False


# ── create_journal_entry ───────────────────────────────────────────────────────

def test_create_entry_paper_only():
    assert _entry().paper_only is True


def test_create_entry_journal_only():
    assert _entry().journal_only is True


def test_create_entry_no_real_orders():
    assert _entry().no_real_orders is True


def test_create_entry_no_broker():
    assert _entry().no_broker is True


def test_create_entry_state_preserved():
    e = _entry(state="PAPER_PLAN_READY")
    assert e.state == "PAPER_PLAN_READY"


def test_create_entry_invalid_state_defaults_observe():
    e = _entry(state="INVALID_STATE")
    assert e.state == "OBSERVE"


def test_create_entry_symbol_preserved():
    e = _entry(symbol="MEDIATEK")
    assert e.symbol == "MEDIATEK"


def test_create_entry_auto_id_when_empty():
    e = create_journal_entry(date_label="2026-W01-D1", symbol="TSMC")
    assert "TSMC" in e.entry_id or e.entry_id != ""


# ── validate_journal_entry ─────────────────────────────────────────────────────

def test_validate_entry_valid():
    e = _entry()
    result = validate_journal_entry(e)
    assert result.is_valid is True


def test_validate_entry_not_blocked():
    e = _entry()
    result = validate_journal_entry(e)
    assert result.blocked is False


def test_validate_entry_invalid_state_blocked():
    e = DecisionJournalEntry(state="BUY")
    result = validate_journal_entry(e)
    assert result.blocked is True


def test_validate_entry_missing_paper_only_blocked():
    e = DecisionJournalEntry(paper_only=False)
    result = validate_journal_entry(e)
    assert result.blocked is True


def test_validate_entry_missing_journal_only_blocked():
    e = DecisionJournalEntry(journal_only=False)
    result = validate_journal_entry(e)
    assert result.blocked is True


# ── create_journal_book ────────────────────────────────────────────────────────

def test_create_book_paper_only():
    b = create_journal_book("BK-1", "2026-W01", [_entry()])
    assert b.paper_only is True


def test_create_book_entry_count():
    entries = [_entry(), _entry(entry_id="E-002", state="BLOCKED")]
    b = create_journal_book("BK-1", "2026-W01", entries)
    assert b.entry_count == 2


def test_create_book_paper_plan_count():
    entries = [_entry(state="PAPER_PLAN_READY"), _entry(state="OBSERVE")]
    b = create_journal_book("BK-1", "2026-W01", entries)
    assert b.paper_plan_count == 1


def test_create_book_blocked_count():
    entries = [_entry(state="BLOCKED"), _entry(state="BLOCKED")]
    b = create_journal_book("BK-1", "2026-W01", entries)
    assert b.blocked_decisions == 2


def test_create_book_empty():
    b = create_journal_book("BK-EMPTY", "2026-W01")
    assert b.entry_count == 0


# ── run_review ─────────────────────────────────────────────────────────────────

def test_run_review_paper_only():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    r = run_review(ri)
    assert r.paper_only is True


def test_run_review_not_blocked():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    r = run_review(ri)
    assert r.blocked is False


def test_run_review_blocked_when_no_workflow_id():
    ri = DecisionReviewInput(review_type="daily_review", date_label="2026-W01-D1",
                              source_workflow_id="")
    r = run_review(ri)
    assert r.blocked is True


def test_run_review_grade_is_valid():
    from paper_trading.small_capital_strategy.decision_journal_version_v189 import QUALITY_GRADES
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    r = run_review(ri)
    assert r.review_grade in QUALITY_GRADES


def test_run_review_quality_score_between_0_and_1():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    r = run_review(ri)
    assert 0.0 <= r.quality_score <= 1.0


def test_run_review_dimension_scores_20():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    r = run_review(ri)
    assert len(r.dimension_scores) == 20


def test_run_review_over_concentration_finding():
    ri = _rev_input(total_exposure_pct=85.0,
                    book=create_journal_book("BK", "2026-W01", [_entry()]))
    r = run_review(ri)
    assert any("OVER_CONCENTRATION" in f for f in r.findings)


def test_run_review_low_cash_finding():
    ri = _rev_input(cash_reserve_pct=5.0, total_exposure_pct=95.0,
                    book=create_journal_book("BK", "2026-W01", [_entry()]))
    r = run_review(ri)
    assert any("LOW_CASH_RESERVE" in f for f in r.findings)


# ── build_daily_review ─────────────────────────────────────────────────────────

def test_build_daily_review_paper_only():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    dr = build_daily_review(ri)
    assert dr.paper_only is True


def test_build_daily_review_journal_only():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    dr = build_daily_review(ri)
    assert dr.journal_only is True


def test_build_daily_review_total_decisions():
    entries = [_entry(), _entry(entry_id="E2")]
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", entries))
    dr = build_daily_review(ri)
    assert dr.total_decisions == 2


# ── build_weekly_review ────────────────────────────────────────────────────────

def test_build_weekly_review_paper_only():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    dr = build_daily_review(ri)
    wr = build_weekly_review([dr])
    assert wr.paper_only is True


def test_build_weekly_review_total_decisions():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry(), _entry(entry_id="E2")]))
    dr = build_daily_review(ri)
    wr = build_weekly_review([dr, dr])
    assert wr.total_decisions == 4


def test_build_weekly_review_grade_valid():
    from paper_trading.small_capital_strategy.decision_journal_version_v189 import QUALITY_GRADES
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    dr = build_daily_review(ri)
    wr = build_weekly_review([dr])
    assert wr.weekly_grade in QUALITY_GRADES


def test_build_weekly_review_recurring_mistakes():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    dr = build_daily_review(ri)
    wr = build_weekly_review([dr, dr, dr])
    assert isinstance(wr.recurring_mistakes, list)


# ── build_monthly_review ───────────────────────────────────────────────────────

def test_build_monthly_review_paper_only():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    dr = build_daily_review(ri)
    wr = build_weekly_review([dr])
    mr = build_monthly_review([wr], "2026-01")
    assert mr.paper_only is True


def test_build_monthly_review_month_label():
    ri = _rev_input(book=create_journal_book("BK", "2026-W01", [_entry()]))
    dr = build_daily_review(ri)
    wr = build_weekly_review([dr])
    mr = build_monthly_review([wr], "2026-01")
    assert mr.month_label == "2026-01"


# ── build_quality_score ────────────────────────────────────────────────────────

def test_build_quality_score_paper_only():
    e = _entry()
    ri = _rev_input()
    qs = build_quality_score(e, ri)
    assert qs.paper_only is True


def test_build_quality_score_dimension_count():
    e = _entry()
    ri = _rev_input()
    qs = build_quality_score(e, ri)
    assert len(qs.dimension_scores) == 20


def test_build_quality_score_between_0_and_1():
    e = _entry()
    ri = _rev_input()
    qs = build_quality_score(e, ri)
    assert 0.0 <= qs.score <= 1.0


def test_build_quality_score_grade_valid():
    from paper_trading.small_capital_strategy.decision_journal_version_v189 import QUALITY_GRADES
    e = _entry()
    ri = _rev_input()
    qs = build_quality_score(e, ri)
    assert qs.grade in QUALITY_GRADES


# ── build_audit_trail ──────────────────────────────────────────────────────────

def test_build_audit_trail_paper_only():
    e = _entry()
    at = build_audit_trail("2026-W01", [e])
    assert at.paper_only is True


def test_build_audit_trail_event_count():
    e = _entry()
    at = build_audit_trail("2026-W01", [e])
    assert at.event_count == 1


def test_build_audit_trail_is_complete():
    e = _entry()
    at = build_audit_trail("2026-W01", [e])
    assert at.is_complete is True


# ── build_evidence_pack ────────────────────────────────────────────────────────

def test_build_evidence_pack_paper_only():
    e = _entry()
    ep = build_evidence_pack("2026-W01", [e], ["WF-001"])
    assert ep.paper_only is True


def test_build_evidence_pack_entry_ids():
    e = _entry()
    ep = build_evidence_pack("2026-W01", [e], ["WF-001"])
    assert e.entry_id in ep.entry_ids


# ── build_export_manifest ──────────────────────────────────────────────────────

def test_build_export_manifest_paper_only():
    em = build_export_manifest("2026-W01", "reports/journal/", [_entry()], 1, 1, 1)
    assert em.paper_only is True


def test_build_export_manifest_safe_path():
    em = build_export_manifest("2026-W01", "production_db/exports/", [_entry()], 0, 0, 0)
    assert em.export_path == "reports/"


def test_build_export_manifest_entry_count():
    entries = [_entry(), _entry(entry_id="E2")]
    em = build_export_manifest("2026-W01", "reports/", entries, 1, 2, 3)
    assert em.entry_count == 2


# ── build_dashboard ────────────────────────────────────────────────────────────

def test_build_dashboard_paper_only():
    book = create_journal_book("BK", "2026-W01", [_entry()])
    db = build_dashboard("2026-W01", book)
    assert db.paper_only is True


def test_build_dashboard_total_entries():
    book = create_journal_book("BK", "2026-W01", [_entry(), _entry(entry_id="E2")])
    db = build_dashboard("2026-W01", book)
    assert db.total_entries == 2


# ── build_review_checklist ─────────────────────────────────────────────────────

def test_build_checklist_paper_only():
    ri = _rev_input()
    cl = build_review_checklist(ri)
    assert cl.paper_only is True


def test_build_checklist_all_complete():
    ri = _rev_input()
    cl = build_review_checklist(ri)
    assert cl.all_complete is True


def test_build_checklist_review_type():
    ri = _rev_input(review_type="weekly_review")
    cl = build_review_checklist(ri)
    assert cl.review_type == "weekly_review"


# ── get_engine_info ────────────────────────────────────────────────────────────

def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True


def test_engine_info_version():
    assert get_engine_info()["version"] == "1.8.9"


def test_engine_info_journal_only():
    assert get_engine_info()["journal_only"] is True


def test_engine_info_no_real_orders():
    assert get_engine_info()["no_real_orders"] is True


def test_engine_info_review_dimensions_count():
    assert get_engine_info()["review_dimensions_count"] == 20


def test_engine_info_mistake_tags_count():
    assert get_engine_info()["mistake_tags_count"] == 18
