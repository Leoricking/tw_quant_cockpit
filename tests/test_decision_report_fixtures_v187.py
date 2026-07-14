"""
tests/test_decision_report_fixtures_v187.py
Tests for decision_report_fixtures_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import json
import os
import pytest
from paper_trading.small_capital_strategy.decision_report_fixtures_v187 import (
    get_fixture_dir, get_fixture_count, get_fixture_info,
)


def test_get_fixture_dir_returns_str():
    assert isinstance(get_fixture_dir(), str)


def test_get_fixture_dir_is_valid_path():
    d = get_fixture_dir()
    assert os.path.isdir(d), f"Fixture dir does not exist: {d}"


def test_get_fixture_count_returns_75():
    assert get_fixture_count() == 75


def test_get_fixture_info_returns_dict():
    info = get_fixture_info()
    assert isinstance(info, dict)


def test_get_fixture_info_paper_only():
    assert get_fixture_info()["paper_only"] is True


def test_get_fixture_info_research_only():
    assert get_fixture_info()["research_only"] is True


def test_get_fixture_info_no_real_orders():
    assert get_fixture_info()["no_real_orders"] is True


def test_get_fixture_info_not_investment_advice():
    assert get_fixture_info()["not_investment_advice"] is True


def test_get_fixture_info_production_trading_blocked():
    assert get_fixture_info()["production_trading_blocked"] is True


def test_get_fixture_info_schema_version():
    assert get_fixture_info()["schema_version"] == "187"


def test_get_fixture_info_expected_count():
    assert get_fixture_info()["expected_count"] == 75


def test_get_fixture_info_fixture_dir_field():
    info = get_fixture_info()
    assert "fixture_dir" in info
    assert isinstance(info["fixture_dir"], str)


def test_fixture_dir_has_json_files():
    d = get_fixture_dir()
    files = [f for f in os.listdir(d) if f.endswith(".json")]
    assert len(files) >= 75


def test_fixture_dr_001_exists():
    d = get_fixture_dir()
    assert os.path.isfile(os.path.join(d, "dr_001.json"))


def test_fixture_dr_005_exists():
    d = get_fixture_dir()
    assert os.path.isfile(os.path.join(d, "dr_005.json"))


def test_fixture_dr_006_exists():
    d = get_fixture_dir()
    assert os.path.isfile(os.path.join(d, "dr_006.json"))


def test_fixture_dr_075_exists():
    d = get_fixture_dir()
    assert os.path.isfile(os.path.join(d, "dr_075.json"))


def test_fixture_dr_001_is_valid_json():
    d = get_fixture_dir()
    with open(os.path.join(d, "dr_001.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_fixture_dr_006_is_valid_json():
    d = get_fixture_dir()
    with open(os.path.join(d, "dr_006.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_fixture_dr_075_is_valid_json():
    d = get_fixture_dir()
    with open(os.path.join(d, "dr_075.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_all_fixtures_have_paper_only():
    d = get_fixture_dir()
    for i in range(1, 76):
        fname = os.path.join(d, f"dr_{i:03d}.json")
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        assert data.get("paper_only") is True, f"{fname} missing paper_only"


def test_all_fixtures_have_no_real_orders():
    d = get_fixture_dir()
    for i in range(1, 76):
        fname = os.path.join(d, f"dr_{i:03d}.json")
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        assert data.get("no_real_orders") is True, f"{fname} missing no_real_orders"


def test_all_fixtures_have_schema_version():
    d = get_fixture_dir()
    for i in range(1, 76):
        fname = os.path.join(d, f"dr_{i:03d}.json")
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        assert data.get("schema_version") == "187", f"{fname} wrong schema_version"


def test_all_fixtures_have_fixture_id():
    d = get_fixture_dir()
    for i in range(1, 76):
        fname = os.path.join(d, f"dr_{i:03d}.json")
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        assert data.get("fixture_id") == f"dr_{i:03d}", f"{fname} wrong fixture_id"


def test_all_fixtures_have_input():
    d = get_fixture_dir()
    for i in range(1, 76):
        fname = os.path.join(d, f"dr_{i:03d}.json")
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        assert "input" in data, f"{fname} missing input"


def test_all_fixtures_have_expected():
    d = get_fixture_dir()
    for i in range(1, 76):
        fname = os.path.join(d, f"dr_{i:03d}.json")
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        assert "expected" in data, f"{fname} missing expected"
