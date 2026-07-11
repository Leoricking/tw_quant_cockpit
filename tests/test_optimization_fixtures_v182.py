"""
tests/test_optimization_fixtures_v182.py
Tests for all 75 optimization fixture files v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
import pathlib
import pytest

FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures" / "optimization"

_VALID_ACTIONS = {
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "READ_REPORT", "SIMULATE_ONLY", "STRESS_TEST_ONLY", "VALIDATION_ONLY",
}

_FIXTURE_NAMES = [
    "fix_param_valid_001", "fix_param_valid_002", "fix_param_valid_003",
    "fix_param_valid_004", "fix_param_valid_005", "fix_param_valid_006",
    "fix_param_valid_007", "fix_param_valid_008", "fix_param_valid_009",
    "fix_param_valid_010",
    "fix_param_blocked_001", "fix_param_blocked_002", "fix_param_blocked_003",
    "fix_param_blocked_004", "fix_param_blocked_005", "fix_param_blocked_006",
    "fix_param_blocked_007", "fix_param_blocked_008", "fix_param_blocked_009",
    "fix_param_blocked_010", "fix_param_blocked_011", "fix_param_blocked_012",
    "fix_walk_forward_pass_001", "fix_walk_forward_pass_002", "fix_walk_forward_pass_003",
    "fix_walk_forward_pass_004", "fix_walk_forward_pass_005", "fix_walk_forward_pass_006",
    "fix_walk_forward_pass_007", "fix_walk_forward_pass_008",
    "fix_walk_forward_fail_001", "fix_walk_forward_fail_002", "fix_walk_forward_fail_003",
    "fix_walk_forward_fail_004", "fix_walk_forward_fail_005", "fix_walk_forward_fail_006",
    "fix_walk_forward_fail_007", "fix_walk_forward_fail_008",
    "fix_overfitting_low_001", "fix_overfitting_low_002", "fix_overfitting_low_003",
    "fix_overfitting_low_004", "fix_overfitting_low_005", "fix_overfitting_low_006",
    "fix_overfitting_low_007",
    "fix_overfitting_high_001", "fix_overfitting_high_002", "fix_overfitting_high_003",
    "fix_overfitting_high_004", "fix_overfitting_high_005", "fix_overfitting_high_006",
    "fix_overfitting_high_007",
    "fix_stability_001", "fix_stability_002", "fix_stability_003",
    "fix_stability_004", "fix_stability_005", "fix_stability_006",
    "fix_stability_007", "fix_stability_008",
    "fix_sensitivity_001", "fix_sensitivity_002", "fix_sensitivity_003",
    "fix_sensitivity_004", "fix_sensitivity_005", "fix_sensitivity_006",
    "fix_sensitivity_007",
    "fix_regime_dep_001", "fix_regime_dep_002", "fix_regime_dep_003",
    "fix_regime_dep_004", "fix_regime_dep_005",
    "fix_robustness_rank_001", "fix_robustness_rank_002", "fix_robustness_rank_003",
]


def _load(fixture_name: str) -> dict:
    path = FIXTURE_DIR / f"{fixture_name}.json"
    return json.loads(path.read_text())


# -- Directory-level checks --

def test_fixture_dir_exists():
    assert FIXTURE_DIR.exists()

def test_fixture_count_ge_75():
    files = list(FIXTURE_DIR.glob("*.json"))
    assert len(files) >= 75

def test_fixture_count_equals_75():
    files = list(FIXTURE_DIR.glob("*.json"))
    assert len(files) == 75


# -- Parametrized: 20 tests x 75 fixtures --

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
def test_fixture_validation_only(fixture_name):
    data = _load(fixture_name)
    assert data.get("validation_only") is True

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
def test_fixture_demo_only(fixture_name):
    data = _load(fixture_name)
    assert data.get("demo_only") is True

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_not_for_production(fixture_name):
    data = _load(fixture_name)
    assert data.get("not_for_production") is True

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
def test_fixture_has_meta(fixture_name):
    data = _load(fixture_name)
    assert "_fixture_meta" in data

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_meta_version_182(fixture_name):
    data = _load(fixture_name)
    assert data["_fixture_meta"]["version"] == "1.8.2"

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_meta_schema_182(fixture_name):
    data = _load(fixture_name)
    assert data["_fixture_meta"]["schema"] == "182"

@pytest.mark.parametrize("fixture_name", _FIXTURE_NAMES)
def test_fixture_scenario_id_starts_with_op182(fixture_name):
    data = _load(fixture_name)
    assert data["scenario_id"].startswith("OP182-")
