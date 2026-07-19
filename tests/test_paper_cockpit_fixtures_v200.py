"""
tests/test_paper_cockpit_fixtures_v200.py
v2.0.0 Paper Cockpit — Fixture Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v200 import FIXTURES

_REQUIRED_SAFETY_FIELDS = [
    "paper_only", "research_only", "simulate_only", "validation_only",
    "unified_paper_cockpit_only", "decision_console_only", "dashboard_only",
    "report_only", "audit_only", "no_real_orders", "no_broker", "no_margin",
    "no_leverage", "no_production_strategy_mutation", "no_automatic_rollback",
    "no_live_strategy_activation", "no_real_portfolio_rebalancing",
    "not_investment_advice", "human_review_required", "demo_only",
    "not_for_production", "production_trading_blocked",
]


def test_fixtures_count_80():
    assert len(FIXTURES) == 80

def test_fixtures_is_list():
    assert isinstance(FIXTURES, list)

def test_all_fixtures_are_dicts():
    assert all(isinstance(f, dict) for f in FIXTURES)

def test_all_fixtures_have_id():
    assert all("id" in f for f in FIXTURES)

def test_all_fixtures_have_fixture_id():
    assert all("fixture_id" in f for f in FIXTURES)

def test_all_fixture_ids_unique():
    ids = [f["id"] for f in FIXTURES]
    assert len(set(ids)) == 80

def test_all_fixture_fixture_ids_unique():
    ids = [f["fixture_id"] for f in FIXTURES]
    assert len(set(ids)) == 80

def test_all_fixtures_schema_version_200():
    assert all(f["schema_version"] == "200" for f in FIXTURES)

def test_all_fixtures_paper_only_true():
    assert all(f["paper_only"] is True for f in FIXTURES)

def test_all_fixtures_research_only_true():
    assert all(f["research_only"] is True for f in FIXTURES)

def test_all_fixtures_simulate_only_true():
    assert all(f["simulate_only"] is True for f in FIXTURES)

def test_all_fixtures_validation_only_true():
    assert all(f["validation_only"] is True for f in FIXTURES)

def test_all_fixtures_unified_paper_cockpit_only_true():
    assert all(f["unified_paper_cockpit_only"] is True for f in FIXTURES)

def test_all_fixtures_decision_console_only_true():
    assert all(f["decision_console_only"] is True for f in FIXTURES)

def test_all_fixtures_dashboard_only_true():
    assert all(f["dashboard_only"] is True for f in FIXTURES)

def test_all_fixtures_report_only_true():
    assert all(f["report_only"] is True for f in FIXTURES)

def test_all_fixtures_audit_only_true():
    assert all(f["audit_only"] is True for f in FIXTURES)

def test_all_fixtures_no_real_orders_true():
    assert all(f["no_real_orders"] is True for f in FIXTURES)

def test_all_fixtures_no_broker_true():
    assert all(f["no_broker"] is True for f in FIXTURES)

def test_all_fixtures_no_margin_true():
    assert all(f["no_margin"] is True for f in FIXTURES)

def test_all_fixtures_no_leverage_true():
    assert all(f["no_leverage"] is True for f in FIXTURES)

def test_all_fixtures_no_production_strategy_mutation_true():
    assert all(f["no_production_strategy_mutation"] is True for f in FIXTURES)

def test_all_fixtures_no_automatic_rollback_true():
    assert all(f["no_automatic_rollback"] is True for f in FIXTURES)

def test_all_fixtures_no_live_strategy_activation_true():
    assert all(f["no_live_strategy_activation"] is True for f in FIXTURES)

def test_all_fixtures_no_real_portfolio_rebalancing_true():
    assert all(f["no_real_portfolio_rebalancing"] is True for f in FIXTURES)

def test_all_fixtures_not_investment_advice_true():
    assert all(f["not_investment_advice"] is True for f in FIXTURES)

def test_all_fixtures_human_review_required_true():
    assert all(f["human_review_required"] is True for f in FIXTURES)

def test_all_fixtures_demo_only_true():
    assert all(f["demo_only"] is True for f in FIXTURES)

def test_all_fixtures_not_for_production_true():
    assert all(f["not_for_production"] is True for f in FIXTURES)

def test_all_fixtures_production_trading_blocked_true():
    assert all(f["production_trading_blocked"] is True for f in FIXTURES)

def test_all_fixtures_have_all_safety_fields():
    for f in FIXTURES:
        for field in _REQUIRED_SAFETY_FIELDS:
            assert field in f, f"Fixture {f.get('id')} missing field '{field}'"

def test_all_fixtures_have_name():
    assert all("name" in f for f in FIXTURES)

def test_fixture_pcfix200_001_default_input():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-001")
    assert f["capital_twd"] == 300000.0
    assert f["market_regime"] == "BULL"

def test_fixture_pcfix200_002_empty_watchlist():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-002")
    assert f["expected_valid"] is False

def test_fixture_pcfix200_003_a_pullback():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-003")
    assert f["expected_abc_type"] == "A_PULLBACK_10MA"

def test_fixture_pcfix200_004_b_breakout():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-004")
    assert f["expected_abc_type"] == "B_BREAKOUT_BASE"

def test_fixture_pcfix200_005_c_reclaim():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-005")
    assert f["expected_abc_type"] == "C_RECLAIM_20MA"

def test_fixture_pcfix200_006_no_entry():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-006")
    assert f["expected_abc_type"] == "NO_ENTRY"

def test_fixture_pcfix200_007_portfolio_risk_ok():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-007")
    assert f["expected_overall_ok"] is True

def test_fixture_pcfix200_008_portfolio_risk_exceeded():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-008")
    assert f["expected_overall_ok"] is False

def test_fixture_pcfix200_011_sizing_ok():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-011")
    assert f["expected_sizing_ok"] is True
    assert f["expected_max_loss"] == 4500.0

def test_fixture_pcfix200_012_sizing_wide_stop():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-012")
    assert f["expected_sizing_ok"] is False

def test_fixture_pcfix200_014_signal_score_all_100():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-014")
    assert f["expected_grade"] == "A"
    assert f["expected_tradable"] is True

def test_fixture_pcfix200_015_signal_score_all_zero():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-015")
    assert f["expected_grade"] == "F"
    assert f["expected_tradable"] is False

def test_fixture_pcfix200_018_watchlist_30():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-018")
    assert f["expected_valid"] is True
    assert f["expected_count"] == 30

def test_fixture_pcfix200_019_watchlist_oversized():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-019")
    assert f["expected_valid"] is False

def test_fixture_pcfix200_031_cockpit_summary():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-031")
    assert f["expected_models"] == 23
    assert f["expected_cli"] == 17
    assert f["expected_gui_tabs"] == 3

def test_fixture_pcfix200_042_baseline_tests():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-042")
    assert f["expected_baseline"] == 31925

def test_fixture_pcfix200_043_min_new_tests():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-043")
    assert f["expected_min_new"] == 500

def test_fixture_pcfix200_080_model_count():
    f = next(x for x in FIXTURES if x["id"] == "PCFIX200-080")
    assert f["expected_model_count"] == 23

def test_fixtures_ids_start_with_pcfix200():
    assert all(f["id"].startswith("PCFIX200-") for f in FIXTURES)

def test_fixtures_ids_sequential():
    ids = sorted(f["id"] for f in FIXTURES)
    assert ids[0] == "PCFIX200-001"
    assert ids[-1] == "PCFIX200-080"

def test_fixture_ids_match_fixture_ids():
    assert all(f["id"] == f["fixture_id"] for f in FIXTURES)
