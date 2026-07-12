"""
tests/test_position_sizing_fixtures_v184.py
Tests for position_sizing_fixtures_v184 module and JSON fixture files.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
import os
import json
from paper_trading.small_capital_strategy.position_sizing_fixtures_v184 import (
    get_fixture_dir, get_fixture_count, get_fixture_info,
)


def test_get_fixture_count_ge_75():
    assert get_fixture_count() >= 75

def test_get_fixture_count_is_75():
    assert get_fixture_count() == 75

def test_get_fixture_dir_returns_str():
    assert isinstance(get_fixture_dir(), str)

def test_get_fixture_dir_is_position_sizing():
    assert "position_sizing" in get_fixture_dir()

def test_get_fixture_info_returns_dict():
    assert isinstance(get_fixture_info(), dict)

def test_get_fixture_info_paper_only():
    assert get_fixture_info()["paper_only"] is True

def test_get_fixture_info_allocation_only():
    assert get_fixture_info()["allocation_only"] is True

def test_get_fixture_info_no_real_orders():
    assert get_fixture_info()["no_real_orders"] is True

def test_get_fixture_info_expected_count():
    assert get_fixture_info()["expected_count"] == 75

def test_fixture_dir_exists():
    assert os.path.isdir(get_fixture_dir())

def test_fixture_files_count_ge_75():
    d = get_fixture_dir()
    files = [f for f in os.listdir(d) if f.endswith(".json")]
    assert len(files) >= 75

def _load_fixture(name: str) -> dict:
    d = get_fixture_dir()
    with open(os.path.join(d, name), encoding="utf-8") as f:
        return json.load(f)

def test_fix_ps_safe_001_exists():
    d = get_fixture_dir()
    assert os.path.isfile(os.path.join(d, "fix_ps_safe_001.json"))

def test_fix_ps_blocked_001_exists():
    d = get_fixture_dir()
    assert os.path.isfile(os.path.join(d, "fix_ps_blocked_001.json"))

def test_fix_ps_abc_001_exists():
    d = get_fixture_dir()
    assert os.path.isfile(os.path.join(d, "fix_ps_abc_001.json"))

def _v184_fixtures(d):
    return [fn for fn in os.listdir(d) if fn.startswith("fix_ps_") and fn.endswith(".json")]

def test_all_fixtures_have_fixture_meta():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert "_fixture_meta" in data, f"Missing _fixture_meta in {fn}"

def test_all_fixtures_paper_only():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert data["_fixture_meta"]["paper_only"] is True, f"{fn} missing paper_only"

def test_all_fixtures_allocation_only():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert data["_fixture_meta"]["allocation_only"] is True, f"{fn} missing allocation_only"

def test_all_fixtures_no_real_orders():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert data["_fixture_meta"]["no_real_orders"] is True, f"{fn} missing no_real_orders"

def test_all_fixtures_production_trading_blocked():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert data["_fixture_meta"]["production_trading_blocked"] is True, f"{fn} missing production_trading_blocked"

def test_all_fixtures_no_broker():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert data["_fixture_meta"]["no_broker"] is True, f"{fn} missing no_broker"

def test_all_fixtures_no_margin():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert data["_fixture_meta"]["no_margin"] is True, f"{fn} missing no_margin"

def test_all_fixtures_have_schema_version():
    d = get_fixture_dir()
    for fn in _v184_fixtures(d):
        data = _load_fixture(fn)
        assert data["_fixture_meta"]["schema_version"] == "184", f"{fn} wrong schema_version"

def test_safe_fixture_has_capital():
    data = _load_fixture("fix_ps_safe_001.json")
    assert "capital" in data

def test_blocked_fixture_category():
    data = _load_fixture("fix_ps_blocked_001.json")
    assert "blocked" in data["_fixture_meta"]["category"]
