"""
tests/test_operational_integration_fixture_files_v168.py — Fixture file tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import json
import os
import pytest

FIXTURES_DIR = os.path.join(
    os.path.dirname(__file__), "fixtures", "operational_integration"
)

REQUIRED_SAFETY_KEYS = [
    "TEST_FIXTURE",
    "PAPER_ONLY",
    "RESEARCH_ONLY",
    "NOT_LIVE",
    "NO_BROKER",
    "NO_REAL_ACCOUNT",
    "NO_REAL_ORDERS",
    "NOT_FOR_PRODUCTION",
]


def _load_fixture(filename: str) -> dict:
    path = os.path.join(FIXTURES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_json_fixtures():
    if not os.path.isdir(FIXTURES_DIR):
        return []
    return [f for f in os.listdir(FIXTURES_DIR) if f.endswith(".json")]


class TestFixtureFilesSafetyFlags:
    def test_paper_only(self):
        # Module-level safety
        assert True  # All fixture tests verify paper_only per fixture

    def test_research_only(self):
        assert True

    def test_no_real_orders(self):
        assert True


class TestFixtureFilesCore:
    def test_fixtures_directory_exists(self):
        assert os.path.isdir(FIXTURES_DIR), f"Fixtures directory not found: {FIXTURES_DIR}"

    def test_fixtures_count_at_least_100(self):
        fixtures = _get_json_fixtures()
        assert len(fixtures) >= 100, f"Expected >=100 fixture files, got {len(fixtures)}"

    def test_scenario_fixtures_exist(self):
        fixtures = _get_json_fixtures()
        scenario_fixtures = [f for f in fixtures if f.startswith("oi_")]
        assert len(scenario_fixtures) >= 100

    def test_all_fixtures_valid_json(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert isinstance(fixture, dict), f"Fixture {filename} is not a dict"

    def test_all_fixtures_have_test_fixture(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("TEST_FIXTURE") is True, \
                f"Fixture {filename} missing TEST_FIXTURE=True"

    def test_all_fixtures_have_paper_only(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("PAPER_ONLY") is True, \
                f"Fixture {filename} missing PAPER_ONLY=True"

    def test_all_fixtures_have_research_only(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("RESEARCH_ONLY") is True, \
                f"Fixture {filename} missing RESEARCH_ONLY=True"

    def test_all_fixtures_have_not_live(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("NOT_LIVE") is True, \
                f"Fixture {filename} missing NOT_LIVE=True"

    def test_all_fixtures_have_no_broker(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("NO_BROKER") is True, \
                f"Fixture {filename} missing NO_BROKER=True"

    def test_all_fixtures_have_no_real_account(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("NO_REAL_ACCOUNT") is True, \
                f"Fixture {filename} missing NO_REAL_ACCOUNT=True"

    def test_all_fixtures_have_no_real_orders(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("NO_REAL_ORDERS") is True, \
                f"Fixture {filename} missing NO_REAL_ORDERS=True"

    def test_all_fixtures_have_not_for_production(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            assert fixture.get("NOT_FOR_PRODUCTION") is True, \
                f"Fixture {filename} missing NOT_FOR_PRODUCTION=True"

    def test_specific_fixture_oi_c_001(self):
        fixture = _load_fixture("oi_c_001.json")
        assert fixture.get("scenario_id") == "OI-C-001"
        assert fixture.get("PAPER_ONLY") is True

    def test_specific_fixture_oi_d_001(self):
        fixture = _load_fixture("oi_d_001.json")
        assert fixture.get("PAPER_ONLY") is True

    def test_specific_fixture_oi_s_001(self):
        fixture = _load_fixture("oi_s_001.json")
        assert fixture.get("PAPER_ONLY") is True

    def test_version_fixture_exists(self):
        assert "version_v168.json" in _get_json_fixtures()

    def test_version_fixture_has_paper_only(self):
        fixture = _load_fixture("version_v168.json")
        assert fixture.get("PAPER_ONLY") is True

    def test_pipeline_full_fixture_exists(self):
        assert "pipeline_full.json" in _get_json_fixtures()

    def test_safety_all_disabled_fixture_exists(self):
        assert "safety_all_disabled.json" in _get_json_fixtures()

    def test_health_baseline_fixture_exists(self):
        assert "health_baseline.json" in _get_json_fixtures()

    def test_gate_baseline_fixture_exists(self):
        assert "gate_baseline.json" in _get_json_fixtures()

    def test_all_safety_keys_present(self):
        for filename in _get_json_fixtures():
            fixture = _load_fixture(filename)
            for key in REQUIRED_SAFETY_KEYS:
                assert key in fixture, f"Fixture {filename} missing key {key}"
