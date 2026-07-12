"""
tests/test_monte_carlo_fixtures_v183.py
Tests for Monte Carlo fixture registry and JSON fixture files v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
import pathlib
import pytest

from paper_trading.small_capital_strategy.monte_carlo_fixtures_v183 import (
    get_fixture_dir,
    get_fixture_count,
    get_fixture_info,
)


# ---------------------------------------------------------------------------
# get_fixture_dir()
# ---------------------------------------------------------------------------

def test_get_fixture_dir_returns_path():
    assert isinstance(get_fixture_dir(), pathlib.Path)


def test_get_fixture_dir_name():
    assert get_fixture_dir().name == "monte_carlo"


def test_get_fixture_dir_exists():
    assert get_fixture_dir().exists() is True


def test_fixture_dir_contains_ge_75_json_files():
    files = list(get_fixture_dir().glob("*.json"))
    assert len(files) >= 75


# ---------------------------------------------------------------------------
# get_fixture_count()
# ---------------------------------------------------------------------------

def test_get_fixture_count_returns_int():
    assert isinstance(get_fixture_count(), int)


def test_get_fixture_count_ge_75():
    assert get_fixture_count() >= 75


# ---------------------------------------------------------------------------
# get_fixture_info()
# ---------------------------------------------------------------------------

def test_get_fixture_info_returns_dict():
    info = get_fixture_info()
    assert isinstance(info, dict)


def test_get_fixture_info_version():
    assert get_fixture_info()["version"] == "1.8.3"


def test_get_fixture_info_paper_only():
    assert get_fixture_info()["paper_only"] is True


def test_get_fixture_info_monte_carlo_only():
    assert get_fixture_info()["monte_carlo_only"] is True


def test_get_fixture_info_schema_version():
    assert get_fixture_info()["schema_version"] == "183"


def test_get_fixture_info_count_ge_75():
    assert get_fixture_info()["count"] >= 75


# ---------------------------------------------------------------------------
# fix_mc_robust_001.json contents
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def robust_001_data():
    f = get_fixture_dir() / "fix_mc_robust_001.json"
    return json.loads(f.read_text())


def test_robust_001_paper_only(robust_001_data):
    assert robust_001_data["paper_only"] is True


def test_robust_001_monte_carlo_only(robust_001_data):
    assert robust_001_data["monte_carlo_only"] is True


def test_robust_001_no_real_orders(robust_001_data):
    assert robust_001_data["no_real_orders"] is True


def test_robust_001_production_trading_blocked(robust_001_data):
    assert robust_001_data["production_trading_blocked"] is True


def test_robust_001_fixture_meta_version(robust_001_data):
    assert robust_001_data["_fixture_meta"]["version"] == "1.8.3"


def test_robust_001_fixture_meta_paper_only(robust_001_data):
    assert robust_001_data["_fixture_meta"]["paper_only"] is True


def test_robust_001_expected_paper_only(robust_001_data):
    assert robust_001_data["expected_paper_only"] is True


def test_robust_001_expected_action(robust_001_data):
    assert robust_001_data["expected_action"] == "MONTE_CARLO_ONLY"


# ---------------------------------------------------------------------------
# fix_mc_blocked_001.json contents
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def blocked_001_data():
    fb = get_fixture_dir() / "fix_mc_blocked_001.json"
    return json.loads(fb.read_text())


def test_blocked_001_expected_action(blocked_001_data):
    assert blocked_001_data["expected_action"] == "BLOCKED"


def test_blocked_001_paper_only(blocked_001_data):
    assert blocked_001_data["paper_only"] is True
