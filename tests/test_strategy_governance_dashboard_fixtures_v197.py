"""
tests/test_strategy_governance_dashboard_fixtures_v197.py
Tests for strategy_governance_dashboard_fixtures_v197.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_governance_dashboard_fixtures_v197 import (
    get_all_fixtures, get_fixture_count, get_fixture_by_id,
)


# ── count ──────────────────────────────────────────────────────────────────────
def test_fixture_count_75(): assert get_fixture_count() == 75
def test_all_fixtures_length_75(): assert len(get_all_fixtures()) == 75
def test_all_fixtures_returns_list(): assert isinstance(get_all_fixtures(), list)

# ── safety flags in all fixtures ──────────────────────────────────────────────
def test_all_fixtures_paper_only(): assert all(f["paper_only"] is True for f in get_all_fixtures())
def test_all_fixtures_no_real_orders(): assert all(f["no_real_orders"] is True for f in get_all_fixtures())
def test_all_fixtures_not_investment_advice(): assert all(f["not_investment_advice"] is True for f in get_all_fixtures())
def test_all_fixtures_no_broker(): assert all(f["no_broker"] is True for f in get_all_fixtures())
def test_all_fixtures_production_trading_blocked(): assert all(f["production_trading_blocked"] is True for f in get_all_fixtures())
def test_all_fixtures_governance_analytics_only(): assert all(f["governance_analytics_only"] is True for f in get_all_fixtures())
def test_all_fixtures_demo_only(): assert all(f["demo_only"] is True for f in get_all_fixtures())
def test_all_fixtures_schema_version_197(): assert all(f["schema_version"] == "197" for f in get_all_fixtures())

# ── required fields ───────────────────────────────────────────────────────────
def test_all_fixtures_have_id(): assert all("id" in f for f in get_all_fixtures())
def test_all_fixtures_have_fixture_id(): assert all("fixture_id" in f for f in get_all_fixtures())
def test_all_fixtures_have_name(): assert all("name" in f for f in get_all_fixtures())

# ── unique IDs ────────────────────────────────────────────────────────────────
def test_fixture_ids_unique():
    ids = [f["fixture_id"] for f in get_all_fixtures()]
    assert len(ids) == len(set(ids))

def test_fixture_ids_prefix_smf197():
    assert all(f["fixture_id"].startswith("SMF197-") for f in get_all_fixtures())

# ── get_fixture_by_id ─────────────────────────────────────────────────────────
def test_get_fixture_by_id_001(): assert get_fixture_by_id("SMF197-001") is not None
def test_get_fixture_by_id_075(): assert get_fixture_by_id("SMF197-075") is not None
def test_get_fixture_by_id_missing(): assert get_fixture_by_id("SMF197-999") is None
def test_get_fixture_by_id_returns_dict(): assert isinstance(get_fixture_by_id("SMF197-001"), dict)

# ── specific fixture content ──────────────────────────────────────────────────
def test_fixture_001_version_197():
    f = get_fixture_by_id("SMF197-001")
    assert f["version"] == "1.9.7"

def test_fixture_002_release_name():
    f = get_fixture_by_id("SMF197-002")
    assert f["release_name"] == "Paper Strategy Governance Dashboard & Decision Quality Analytics Lab"

def test_fixture_006_metric_evidence_coverage():
    f = get_fixture_by_id("SMF197-006")
    assert f["metric_name"] == "evidence_coverage_score"

def test_fixture_018_grade_excellent():
    f = get_fixture_by_id("SMF197-018")
    assert f["grade"] == "EXCELLENT"

def test_fixture_022_grade_invalid():
    f = get_fixture_by_id("SMF197-022")
    assert f["grade"] == "INVALID"

def test_fixture_023_window_daily():
    f = get_fixture_by_id("SMF197-023")
    assert f["window_type"] == "DAILY"

def test_fixture_027_window_full_history():
    f = get_fixture_by_id("SMF197-027")
    assert f["window_type"] == "FULL_HISTORY"

def test_fixture_028_panel_quality_overview():
    f = get_fixture_by_id("SMF197-028")
    assert f["panel_name"] == "quality_overview"

def test_fixture_040_safety_flags_all_set():
    f = get_fixture_by_id("SMF197-040")
    assert f["all_safety_flags_set"] is True

def test_fixture_044_analytics_not_execute():
    f = get_fixture_by_id("SMF197-044")
    assert f["analytics_executes_decision"] is False

def test_fixture_048_hard_block_real_order():
    f = get_fixture_by_id("SMF197-048")
    assert f["block_condition"] == "real_order_requested"
    assert f["blocked"] is True

def test_fixture_057_hard_block_unsafe_path():
    f = get_fixture_by_id("SMF197-057")
    assert f["block_condition"] == "unsafe_export_path"

def test_fixture_060_grade_excellent_engine():
    f = get_fixture_by_id("SMF197-060")
    assert f["expected_grade"] == "EXCELLENT"

def test_fixture_063_grade_weak_engine():
    f = get_fixture_by_id("SMF197-063")
    assert f["expected_grade"] == "WEAK"

def test_fixture_068_report_sections_12():
    f = get_fixture_by_id("SMF197-068")
    assert f["report_section_count"] == 12

def test_fixture_075_full_pack_no_auto_rollback():
    f = get_fixture_by_id("SMF197-075")
    assert f["auto_rollback"] is False
    assert f["analytics_executes_decision"] is False
