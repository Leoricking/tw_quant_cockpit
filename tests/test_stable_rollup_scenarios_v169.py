"""
tests/test_stable_rollup_scenarios_v169.py
Scenario-driven tests using fixture data.
"""
import os
import json
import pytest
from paper_trading.stable_rollup.scenario_registry_v169 import get_registry, get_scenario, get_by_category


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "stable_rollup")


def load_fixture(fixture_id: str) -> dict:
    path = os.path.join(FIXTURE_DIR, f"{fixture_id}.json")
    with open(path) as f:
        return json.load(f)


def test_all_scenarios_have_fixture():
    registry = get_registry()
    for scenario in registry:
        fid = scenario.get("fixture_id", "")
        if fid:
            path = os.path.join(FIXTURE_DIR, f"{fid}.json")
            assert os.path.exists(path), f"Fixture {fid}.json not found for scenario {scenario['scenario_id']}"


def test_sr_001_fixture_valid():
    f = load_fixture("sr_001")
    assert f["test_fixture"] is True
    assert f["paper_only"] is True
    assert f["no_real_orders"] is True


def test_sr_001_markers():
    f = load_fixture("sr_001")
    assert f["not_for_production"] is True
    assert f["no_broker"] is True
    assert f["stable_rollup_only"] is True


def test_sr_001_schema_version():
    f = load_fixture("sr_001")
    assert f["schema_version"] == "169"


def test_sr_001_policy_version():
    f = load_fixture("sr_001")
    assert f["policy_version"] == "1.6.9-live-paper-stable-rollup"


def test_sr_001_expected_status_pass():
    f = load_fixture("sr_001")
    assert f["expected_status"] == "PASS"


def test_all_fixtures_have_required_markers():
    required_markers = [
        "test_fixture", "paper_only", "research_only", "not_live",
        "no_broker", "no_real_account", "no_real_orders", "not_for_production",
        "stable_rollup_only",
    ]
    for i in range(1, 81):
        fid = f"sr_{str(i).zfill(3)}"
        f = load_fixture(fid)
        for marker in required_markers:
            assert f.get(marker) is True, f"Fixture {fid} missing marker {marker}"


def test_all_fixtures_have_schema_169():
    for i in range(1, 81):
        fid = f"sr_{str(i).zfill(3)}"
        f = load_fixture(fid)
        assert f["schema_version"] == "169", f"Fixture {fid} schema_version != 169"


def test_all_fixtures_have_fixture_id():
    for i in range(1, 81):
        fid = f"sr_{str(i).zfill(3)}"
        f = load_fixture(fid)
        assert f["fixture_id"] == fid


def test_all_fixtures_have_scenario_id():
    for i in range(1, 81):
        fid = f"sr_{str(i).zfill(3)}"
        f = load_fixture(fid)
        assert f["scenario_id"]


def test_all_fixtures_have_deterministic_seed():
    for i in range(1, 81):
        fid = f"sr_{str(i).zfill(3)}"
        f = load_fixture(fid)
        assert f["deterministic_seed"] == 42


def test_get_by_category_release_identity():
    scenarios = get_by_category("release_identity")
    assert len(scenarios) == 8


def test_get_by_category_capability():
    scenarios = get_by_category("capability")
    assert len(scenarios) == 8


def test_get_by_category_safety():
    scenarios = get_by_category("safety")
    assert len(scenarios) == 8


def test_get_scenario_by_id():
    s = get_scenario("sr_ri_001")
    assert s is not None
    assert s["scenario_id"] == "sr_ri_001"


def test_get_scenario_nonexistent():
    s = get_scenario("sr_nonexistent_999")
    assert s is None


def test_all_scenarios_expected_pass():
    registry = get_registry()
    non_pass = [s["scenario_id"] for s in registry if s["expected_status"] != "PASS"]
    assert len(non_pass) == 0
