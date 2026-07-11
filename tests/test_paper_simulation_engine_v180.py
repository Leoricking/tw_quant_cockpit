"""tests/test_paper_simulation_engine_v180.py — v1.8.0 Paper Simulation engine tests"""
from __future__ import annotations
import pytest
from paper_trading.small_capital_strategy.paper_simulation_engine_v180 import (
    ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, get_action_for_input,
    run_paper_simulation, validate_action, get_engine_info,
)
from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
    PaperSimulationInput,
)


# ---------------------------------------------------------------------------
# ALLOWED_OUTPUT_ACTIONS membership
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("action", [
    "PAPER_ENTRY_ALLOWED",
    "BLOCKED",
    "OBSERVE",
    "WAIT",
    "PAPER_PLAN_READY",
    "PAPER_ADD_ALLOWED",
    "REDUCE_RISK",
    "REVIEW_REQUIRED",
    "NO_TRADE",
])
def test_allowed_output_actions_contains(action):
    assert action in ALLOWED_OUTPUT_ACTIONS


def test_allowed_output_actions_is_frozenset():
    assert isinstance(ALLOWED_OUTPUT_ACTIONS, frozenset)


def test_allowed_output_actions_not_empty():
    assert len(ALLOWED_OUTPUT_ACTIONS) > 0


# ---------------------------------------------------------------------------
# FORBIDDEN_OUTPUT_WORDS membership
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("word", [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
])
def test_forbidden_output_words_contains(word):
    assert word in FORBIDDEN_OUTPUT_WORDS


def test_forbidden_output_words_is_frozenset():
    assert isinstance(FORBIDDEN_OUTPUT_WORDS, frozenset)


def test_forbidden_output_words_not_empty():
    assert len(FORBIDDEN_OUTPUT_WORDS) > 0


# ---------------------------------------------------------------------------
# No forbidden word appears in any allowed action
# ---------------------------------------------------------------------------

def test_no_forbidden_word_in_any_allowed_action():
    for action in ALLOWED_OUTPUT_ACTIONS:
        for word in FORBIDDEN_OUTPUT_WORDS:
            assert word not in action, f"Forbidden word {word!r} found in action {action!r}"


# ---------------------------------------------------------------------------
# validate_action()
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("action", ["PAPER_ENTRY_ALLOWED", "BLOCKED", "OBSERVE", "WAIT"])
def test_validate_action_allowed_actions(action):
    assert validate_action(action) is True


@pytest.mark.parametrize("word", ["BUY", "SELL", "ORDER"])
def test_validate_action_forbidden_words(word):
    assert validate_action(word) is False


def test_validate_action_unknown_string_is_false():
    assert validate_action("COMPLETELY_UNKNOWN_ACTION_XYZ") is False


def test_validate_action_returns_bool_for_allowed():
    result = validate_action("BLOCKED")
    assert isinstance(result, bool)


def test_validate_action_returns_bool_for_forbidden():
    result = validate_action("BUY")
    assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# get_action_for_input() — PAPER_ENTRY_ALLOWED path
# ---------------------------------------------------------------------------

def test_get_action_bull_leader_core_a_entry_allowed():
    inp = PaperSimulationInput(
        market_regime="BULL",
        theme_rank="LEADER",
        watchlist_rank="CORE",
        abc_buy_point="A",
        integrated_decision="PAPER_ENTRY_ALLOWED",
    )
    assert get_action_for_input(inp) == "PAPER_ENTRY_ALLOWED"


# ---------------------------------------------------------------------------
# get_action_for_input() — BLOCKED paths
# ---------------------------------------------------------------------------

def test_get_action_risk_off_regime_blocked():
    inp = PaperSimulationInput(market_regime="RISK_OFF")
    assert get_action_for_input(inp) == "BLOCKED"


def test_get_action_integrated_decision_blocked():
    inp = PaperSimulationInput(integrated_decision="BLOCKED")
    assert get_action_for_input(inp) == "BLOCKED"


def test_get_action_watchlist_excluded_blocked():
    inp = PaperSimulationInput(watchlist_rank="EXCLUDED")
    assert get_action_for_input(inp) == "BLOCKED"


def test_get_action_theme_excluded_blocked():
    inp = PaperSimulationInput(theme_rank="EXCLUDED")
    assert get_action_for_input(inp) == "BLOCKED"


def test_get_action_risk_dashboard_blocked():
    inp = PaperSimulationInput(risk_dashboard_status="BLOCKED")
    assert get_action_for_input(inp) == "BLOCKED"


def test_get_action_abc_blocked():
    inp = PaperSimulationInput(abc_buy_point="BLOCKED")
    assert get_action_for_input(inp) == "BLOCKED"


def test_get_action_no_stop_loss_mistake_blocked():
    inp = PaperSimulationInput(mistake_taxonomy_effect="no_stop_loss")
    assert get_action_for_input(inp) == "BLOCKED"


# ---------------------------------------------------------------------------
# get_action_for_input() — OBSERVE paths
# ---------------------------------------------------------------------------

def test_get_action_bear_regime_observe():
    inp = PaperSimulationInput(
        market_regime="BEAR",
        integrated_decision="OBSERVE",
    )
    assert get_action_for_input(inp) == "OBSERVE"


def test_get_action_unknown_regime_observe():
    inp = PaperSimulationInput(
        market_regime="UNKNOWN",
        integrated_decision="OBSERVE",
    )
    assert get_action_for_input(inp) == "OBSERVE"


# ---------------------------------------------------------------------------
# get_action_for_input() — WAIT paths
# ---------------------------------------------------------------------------

def test_get_action_not_ready_abc_wait():
    inp = PaperSimulationInput(
        abc_buy_point="NOT_READY",
        integrated_decision="WAIT",
    )
    assert get_action_for_input(inp) == "WAIT"


def test_get_action_integrated_decision_wait():
    inp = PaperSimulationInput(integrated_decision="WAIT")
    assert get_action_for_input(inp) == "WAIT"


# ---------------------------------------------------------------------------
# get_action_for_input() — REDUCE_RISK paths
# ---------------------------------------------------------------------------

def test_get_action_oversized_position_reduce_risk():
    inp = PaperSimulationInput(
        mistake_taxonomy_effect="oversized_position",
        integrated_decision="REDUCE_RISK",
    )
    assert get_action_for_input(inp) == "REDUCE_RISK"


def test_get_action_overtrading_reduce_risk():
    inp = PaperSimulationInput(
        mistake_taxonomy_effect="overtrading",
        integrated_decision="REDUCE_RISK",
    )
    assert get_action_for_input(inp) == "REDUCE_RISK"


def test_get_action_integrated_decision_reduce_risk():
    inp = PaperSimulationInput(integrated_decision="REDUCE_RISK")
    assert get_action_for_input(inp) == "REDUCE_RISK"


# ---------------------------------------------------------------------------
# get_action_for_input() — REVIEW_REQUIRED paths
# ---------------------------------------------------------------------------

def test_get_action_revenge_trade_review_required():
    inp = PaperSimulationInput(
        mistake_taxonomy_effect="revenge_trade",
        integrated_decision="REVIEW_REQUIRED",
    )
    assert get_action_for_input(inp) == "REVIEW_REQUIRED"


def test_get_action_integrated_decision_review_required():
    inp = PaperSimulationInput(integrated_decision="REVIEW_REQUIRED")
    assert get_action_for_input(inp) == "REVIEW_REQUIRED"


# ---------------------------------------------------------------------------
# get_action_for_input() — NO_TRADE, PAPER_ADD_ALLOWED, PAPER_PLAN_READY
# ---------------------------------------------------------------------------

def test_get_action_no_trade():
    inp = PaperSimulationInput(integrated_decision="NO_TRADE")
    assert get_action_for_input(inp) == "NO_TRADE"


def test_get_action_paper_add_allowed():
    inp = PaperSimulationInput(integrated_decision="PAPER_ADD_ALLOWED")
    assert get_action_for_input(inp) == "PAPER_ADD_ALLOWED"


def test_get_action_paper_plan_ready():
    # RANGE regime with ABC ready causes PAPER_PLAN_READY (not BULL, so PAPER_ENTRY_ALLOWED path skipped)
    inp = PaperSimulationInput(
        integrated_decision="PAPER_PLAN_READY",
        market_regime="RANGE",
        abc_buy_point="B",
    )
    assert get_action_for_input(inp) == "PAPER_PLAN_READY"


# ---------------------------------------------------------------------------
# get_action_for_input() — result is always in ALLOWED_OUTPUT_ACTIONS
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("regime,decision", [
    ("BULL", "PAPER_ENTRY_ALLOWED"),
    ("BEAR", "OBSERVE"),
    ("RISK_OFF", "PAPER_ENTRY_ALLOWED"),
    ("UNKNOWN", "OBSERVE"),
    ("RANGE", "WAIT"),
])
def test_get_action_always_in_allowed_set(regime, decision):
    inp = PaperSimulationInput(market_regime=regime, integrated_decision=decision)
    action = get_action_for_input(inp)
    assert action in ALLOWED_OUTPUT_ACTIONS


# ---------------------------------------------------------------------------
# run_paper_simulation() — safety flags on result
# ---------------------------------------------------------------------------

def test_run_paper_simulation_paper_only():
    result = run_paper_simulation(PaperSimulationInput())
    assert result.paper_only is True


def test_run_paper_simulation_no_real_orders():
    result = run_paper_simulation(PaperSimulationInput())
    assert result.no_real_orders is True


def test_run_paper_simulation_trade_count_non_negative():
    result = run_paper_simulation(PaperSimulationInput())
    assert result.trade_count >= 0


def test_run_paper_simulation_entry_allowed_has_trades():
    inp = PaperSimulationInput(
        integrated_decision="PAPER_ENTRY_ALLOWED",
        market_regime="BULL",
        theme_rank="LEADER",
        watchlist_rank="CORE",
        abc_buy_point="A",
    )
    result = run_paper_simulation(inp)
    assert result.trade_count > 0


def test_run_paper_simulation_final_capital_positive():
    result = run_paper_simulation(PaperSimulationInput())
    assert result.final_capital > 0


def test_run_paper_simulation_total_return_pct_is_float():
    result = run_paper_simulation(PaperSimulationInput())
    assert isinstance(result.total_return_pct, float)


def test_run_paper_simulation_trades_list_length_matches_count():
    result = run_paper_simulation(PaperSimulationInput())
    assert len(result.trades) == result.trade_count


def test_run_paper_simulation_all_trades_paper_only():
    inp = PaperSimulationInput(
        integrated_decision="PAPER_ENTRY_ALLOWED",
        market_regime="BULL",
        theme_rank="LEADER",
        watchlist_rank="CORE",
        abc_buy_point="A",
    )
    result = run_paper_simulation(inp)
    for trade in result.trades:
        assert trade.paper_only is True


def test_run_paper_simulation_blocked_has_zero_trades():
    inp = PaperSimulationInput(integrated_decision="BLOCKED")
    result = run_paper_simulation(inp)
    assert result.trade_count == 0


def test_run_paper_simulation_result_research_only():
    result = run_paper_simulation(PaperSimulationInput())
    assert result.research_only is True


# ---------------------------------------------------------------------------
# get_engine_info()
# ---------------------------------------------------------------------------

def test_get_engine_info_returns_dict():
    info = get_engine_info()
    assert isinstance(info, dict)


def test_get_engine_info_paper_only():
    info = get_engine_info()
    assert info["paper_only"] is True


def test_get_engine_info_no_real_orders():
    info = get_engine_info()
    assert info["no_real_orders"] is True


def test_get_engine_info_research_only():
    info = get_engine_info()
    assert info["research_only"] is True


def test_get_engine_info_production_trading_blocked():
    info = get_engine_info()
    assert info["production_trading_blocked"] is True


def test_get_engine_info_allowed_output_actions_is_list():
    info = get_engine_info()
    assert isinstance(info["allowed_output_actions"], list)


def test_get_engine_info_forbidden_output_words_is_list():
    info = get_engine_info()
    assert isinstance(info["forbidden_output_words"], list)


def test_get_engine_info_not_investment_advice():
    info = get_engine_info()
    assert info["not_investment_advice"] is True
