"""
tests/test_paper_cockpit_scenarios_v205.py
v2.0.5 Scenarios & Fixtures Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


def test_scenarios_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205

def test_scenarios_count():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    ids = {s["id"] for s in SCENARIOS}
    assert len(ids) == 80

def test_scenarios_schema_version_205():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for s in SCENARIOS:
        assert s["schema_version"] == "205", f"Scenario {s['id']} has wrong schema_version"

def test_scenarios_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for s in SCENARIOS:
        assert s["paper_only"] is True, f"Scenario {s['id']} missing paper_only"

def test_scenarios_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for s in SCENARIOS:
        assert s["no_real_orders"] is True, f"Scenario {s['id']} missing no_real_orders"

def test_scenarios_have_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for s in SCENARIOS:
        assert "scenario_id" in s, f"Scenario {s['id']} missing scenario_id"

def test_scenarios_have_name():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for s in SCENARIOS:
        assert "name" in s, f"Scenario {s['id']} missing name"

def test_scenarios_have_expected_result():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for s in SCENARIOS:
        assert "expected_result" in s, f"Scenario {s['id']} missing expected_result"

def test_scenarios_first_is_rotation_engine():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    assert SCENARIOS[0]["id"] == "PC205-001"
    assert "watchlist_rotation" in SCENARIOS[0]["name"]

def test_scenarios_have_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for s in SCENARIOS:
        assert s["should_auto_apply"] is False, f"Scenario {s['id']} should_auto_apply must be False"

def test_scenarios_ids_sequential():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    for i, s in enumerate(SCENARIOS, 1):
        expected_id = f"PC205-{i:03d}"
        assert s["id"] == expected_id, f"Expected id {expected_id}, got {s['id']}"

def test_fixtures_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205

def test_fixtures_count():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    ids = {f["id"] for f in FIXTURES}
    assert len(ids) == 80

def test_fixtures_schema_version_205():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    for f in FIXTURES:
        assert f["schema_version"] == "205", f"Fixture {f['id']} has wrong schema_version"

def test_fixtures_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    for f in FIXTURES:
        assert f["paper_only"] is True, f"Fixture {f['id']} missing paper_only"

def test_fixtures_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    for f in FIXTURES:
        assert "fixture_id" in f, f"Fixture {f['id']} missing fixture_id"

def test_fixtures_have_model():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    for f in FIXTURES:
        assert "model" in f, f"Fixture {f['id']} missing model"

def test_fixtures_have_data():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    for f in FIXTURES:
        assert "data" in f, f"Fixture {f['id']} missing data"

def test_fixtures_auto_apply_fixtures_all_false():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    for f in FIXTURES:
        if "should_auto_apply" in f.get("data", {}):
            assert f["data"]["should_auto_apply"] is False, f"Fixture {f['id']} has should_auto_apply=True"

def test_fixtures_first_is_default_rotation_input():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    assert FIXTURES[0]["id"] == "PC205-F001"
    assert "rotation_input" in FIXTURES[0]["name"]
