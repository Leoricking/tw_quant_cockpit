"""tests/test_paper_simulation_fixtures_v180.py — v1.8.0 Paper Simulation fixture tests"""
from __future__ import annotations

import json
import os

import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "paper_simulation")

_ALL_JSON_FILES = sorted(
    [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")]
    if os.path.isdir(FIXTURE_DIR)
    else []
)
_FIRST_5 = _ALL_JSON_FILES[:5]


# ---------------------------------------------------------------------------
# Directory-level checks
# ---------------------------------------------------------------------------

def test_fixture_dir_exists() -> None:
    assert os.path.isdir(FIXTURE_DIR)


def test_fixture_count_at_least_70() -> None:
    json_files = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")]
    assert len(json_files) >= 70


def test_fixture_count_equals_70() -> None:
    json_files = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")]
    assert len(json_files) == 70


# ---------------------------------------------------------------------------
# Named fixture existence
# ---------------------------------------------------------------------------

def test_fix_paper_entry_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_paper_entry_001.json"))


def test_fix_blocked_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_blocked_001.json"))


def test_fix_observe_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_observe_001.json"))


def test_fix_wait_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_wait_001.json"))


def test_fix_plan_ready_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_plan_ready_001.json"))


def test_fix_reduce_risk_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_reduce_risk_001.json"))


def test_fix_review_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_review_001.json"))


def test_fix_no_trade_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_no_trade_001.json"))


def test_fix_add_allowed_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_add_allowed_001.json"))


def test_fix_benchmark_001_exists() -> None:
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "fix_benchmark_001.json"))


# ---------------------------------------------------------------------------
# First-5 parametrize: valid JSON
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename", _FIRST_5)
def test_first_5_files_are_valid_json(filename: str) -> None:
    path = os.path.join(FIXTURE_DIR, filename)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# First-5 parametrize: fixture_id key present
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename", _FIRST_5)
def test_first_5_have_fixture_id_key(filename: str) -> None:
    path = os.path.join(FIXTURE_DIR, filename)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    assert "fixture_id" in data


# ---------------------------------------------------------------------------
# First-5 parametrize: demo_only == true
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename", _FIRST_5)
def test_first_5_demo_only_true(filename: str) -> None:
    path = os.path.join(FIXTURE_DIR, filename)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    assert data.get("demo_only") is True


# ---------------------------------------------------------------------------
# Specific fixture: fix_paper_entry_001.json schema checks
# ---------------------------------------------------------------------------

def _load(filename: str) -> dict:
    with open(os.path.join(FIXTURE_DIR, filename), encoding="utf-8") as fh:
        return json.load(fh)


def test_paper_entry_001_has_fixture_meta() -> None:
    data = _load("fix_paper_entry_001.json")
    assert "_fixture_meta" in data
    assert data["_fixture_meta"]["TEST_FIXTURE"] is True


def test_paper_entry_001_paper_only_true() -> None:
    data = _load("fix_paper_entry_001.json")
    assert data["paper_only"] is True


def test_paper_entry_001_no_real_orders_true() -> None:
    data = _load("fix_paper_entry_001.json")
    assert data["no_real_orders"] is True


def test_paper_entry_001_expected_action() -> None:
    data = _load("fix_paper_entry_001.json")
    assert data["expected_action"] == "PAPER_ENTRY_ALLOWED"


# ---------------------------------------------------------------------------
# Specific fixture: expected_action values
# ---------------------------------------------------------------------------

def test_fix_blocked_001_expected_action_blocked() -> None:
    data = _load("fix_blocked_001.json")
    assert data["expected_action"] == "BLOCKED"


def test_fix_observe_001_expected_action_observe() -> None:
    data = _load("fix_observe_001.json")
    assert data["expected_action"] == "OBSERVE"


def test_fix_wait_001_expected_action_wait() -> None:
    data = _load("fix_wait_001.json")
    assert data["expected_action"] == "WAIT"


def test_fix_plan_ready_001_expected_action() -> None:
    data = _load("fix_plan_ready_001.json")
    assert data["expected_action"] == "PAPER_PLAN_READY"


def test_fix_reduce_risk_001_expected_action() -> None:
    data = _load("fix_reduce_risk_001.json")
    assert data["expected_action"] == "REDUCE_RISK"


def test_fix_review_001_expected_action() -> None:
    data = _load("fix_review_001.json")
    assert data["expected_action"] == "REVIEW_REQUIRED"


def test_fix_no_trade_001_expected_action() -> None:
    data = _load("fix_no_trade_001.json")
    assert data["expected_action"] == "NO_TRADE"


def test_fix_add_allowed_001_expected_action() -> None:
    data = _load("fix_add_allowed_001.json")
    assert data["expected_action"] == "PAPER_ADD_ALLOWED"


def test_fix_benchmark_001_expected_action() -> None:
    data = _load("fix_benchmark_001.json")
    assert data["expected_action"] == "PAPER_ENTRY_ALLOWED"


# ---------------------------------------------------------------------------
# All fixtures: no BUY as expected_action
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename", _ALL_JSON_FILES)
def test_no_fixture_has_buy_as_expected_action(filename: str) -> None:
    path = os.path.join(FIXTURE_DIR, filename)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    assert data.get("expected_action") != "BUY"
