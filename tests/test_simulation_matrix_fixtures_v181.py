"""
tests/test_simulation_matrix_fixtures_v181.py
Tests for all 75 simulation matrix fixture files v1.8.1.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
import os
import pathlib
import pytest

FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures" / "simulation_matrix"

_VALID_ACTIONS = {
    "PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY", "OBSERVE", "WAIT",
    "BLOCKED", "REDUCE_RISK", "REVIEW_REQUIRED", "NO_TRADE",
    "PAPER_ADD_ALLOWED", "STRESS_TEST_ONLY",
}

_FIXTURE_NAMES = [
    "fix_blocked_001", "fix_blocked_002", "fix_blocked_003", "fix_blocked_004",
    "fix_blocked_005", "fix_blocked_006", "fix_blocked_007", "fix_blocked_008",
    "fix_blocked_009", "fix_blocked_010", "fix_blocked_011", "fix_blocked_012",
    "fix_entry_allowed_001", "fix_entry_allowed_002", "fix_entry_allowed_003",
    "fix_entry_allowed_004", "fix_entry_allowed_005", "fix_entry_allowed_006",
    "fix_entry_allowed_007", "fix_entry_allowed_008", "fix_entry_allowed_009",
    "fix_entry_allowed_010",
    "fix_observe_001", "fix_observe_002", "fix_observe_003", "fix_observe_004",
    "fix_observe_005", "fix_observe_006", "fix_observe_007", "fix_observe_008",
    "fix_plan_ready_001", "fix_plan_ready_002", "fix_plan_ready_003",
    "fix_plan_ready_004", "fix_plan_ready_005", "fix_plan_ready_006",
    "fix_plan_ready_007", "fix_plan_ready_008",
    "fix_reduce_risk_001", "fix_reduce_risk_002", "fix_reduce_risk_003",
    "fix_reduce_risk_004", "fix_reduce_risk_005", "fix_reduce_risk_006",
    "fix_reduce_risk_007",
    "fix_regime_shift_001", "fix_regime_shift_002",
    "fix_review_001", "fix_review_002", "fix_review_003", "fix_review_004",
    "fix_review_005", "fix_review_006", "fix_review_007",
    "fix_robustness_001", "fix_robustness_002", "fix_robustness_003", "fix_robustness_004",
    "fix_stress_001", "fix_stress_002", "fix_stress_003", "fix_stress_004",
    "fix_stress_005", "fix_stress_006", "fix_stress_007",
    "fix_wait_001", "fix_wait_002", "fix_wait_003", "fix_wait_004",
    "fix_wait_005", "fix_wait_006", "fix_wait_007", "fix_wait_008",
    "fix_wait_009", "fix_wait_010",
]


def _load(fixture_name: str) -> dict:
    path = FIXTURE_DIR / f"{fixture_name}.json"
    return json.loads(path.read_text())


# ── Directory-level checks ─────────────────────────────────────────────────────

def test_fixture_dir_exists():
    assert FIXTURE_DIR.exists()

def test_fixture_count_ge_75():
    files = list(FIXTURE_DIR.glob("*.json"))
    assert len(files) >= 75

def test_fixture_count_equals_75():
    files = list(FIXTURE_DIR.glob("*.json"))
    assert len(files) == 75


# ── Parametrized: each fixture file must load and have required fields ─────────

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_is_valid_json(fixture_name):
    data = _load(fixture_name)
    assert isinstance(data, dict)

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_has_fixture_id(fixture_name):
    data = _load(fixture_name)
    assert "fixture_id" in data

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_has_scenario_id(fixture_name):
    data = _load(fixture_name)
    assert "scenario_id" in data

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_has_expected_action(fixture_name):
    data = _load(fixture_name)
    assert "expected_action" in data

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_expected_action_valid(fixture_name):
    data = _load(fixture_name)
    assert data["expected_action"] in _VALID_ACTIONS, \
        f"{fixture_name}: invalid action {data['expected_action']}"

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_paper_only(fixture_name):
    data = _load(fixture_name)
    assert data.get("paper_only") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_research_only(fixture_name):
    data = _load(fixture_name)
    assert data.get("research_only") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_simulate_only(fixture_name):
    data = _load(fixture_name)
    assert data.get("simulate_only") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_stress_test_only(fixture_name):
    data = _load(fixture_name)
    assert data.get("stress_test_only") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_no_real_orders(fixture_name):
    data = _load(fixture_name)
    assert data.get("no_real_orders") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_not_investment_advice(fixture_name):
    data = _load(fixture_name)
    assert data.get("not_investment_advice") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_no_broker(fixture_name):
    data = _load(fixture_name)
    assert data.get("no_broker") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_production_trading_blocked(fixture_name):
    data = _load(fixture_name)
    assert data.get("production_trading_blocked") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_has_input(fixture_name):
    data = _load(fixture_name)
    assert "input" in data
    assert isinstance(data["input"], dict)

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_input_has_market_regime(fixture_name):
    data = _load(fixture_name)
    assert "market_regime" in data["input"]

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_input_has_abc_signal(fixture_name):
    data = _load(fixture_name)
    assert "abc_signal" in data["input"]

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_input_has_initial_capital(fixture_name):
    data = _load(fixture_name)
    assert data["input"].get("initial_capital", 0) > 0

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_has_meta(fixture_name):
    data = _load(fixture_name)
    assert "_fixture_meta" in data

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_meta_version_181(fixture_name):
    data = _load(fixture_name)
    assert data["_fixture_meta"]["version"] == "1.8.1"

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_meta_schema_181(fixture_name):
    data = _load(fixture_name)
    assert data["_fixture_meta"]["schema"] == "181"

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_scenario_id_starts_with_sm181(fixture_name):
    data = _load(fixture_name)
    assert data["scenario_id"].startswith("SM181-")


# ── Parametrized: run engine and check expected_action matches ─────────────────

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_engine_action_matches_expected(fixture_name):
    """Run each fixture through the engine and verify action matches expected."""
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import SimulationMatrixInput
    from paper_trading.small_capital_strategy.simulation_matrix_engine_v181 import run_matrix_cell

    data = _load(fixture_name)
    inp_data = data["input"]
    expected_action = data["expected_action"]

    inp = SimulationMatrixInput(
        initial_capital=inp_data.get("initial_capital", 300000.0),
        single_trade_risk_pct=inp_data.get("single_trade_risk_pct", 1.0),
        max_positions=inp_data.get("max_positions", 4),
        market_regime=inp_data.get("market_regime", "BULL"),
        theme_rank=inp_data.get("theme_rank", "LEADER"),
        watchlist_rank=inp_data.get("watchlist_rank", "CORE"),
        abc_signal=inp_data.get("abc_signal", "A"),
        behavior_risk=inp_data.get("behavior_risk", "PASS"),
        risk_dashboard=inp_data.get("risk_dashboard", "PASS"),
        mistake_injection=inp_data.get("mistake_injection", "NONE"),
    )
    cell = run_matrix_cell(inp)
    assert cell.action == expected_action, \
        f"{fixture_name}: expected {expected_action}, got {cell.action}"
