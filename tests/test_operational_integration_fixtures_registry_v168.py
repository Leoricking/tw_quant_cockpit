"""
tests/test_operational_integration_fixtures_registry_v168.py — Fixture Registry tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.fixture_registry_v168 import (
    FixtureRegistry, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)


def _make_valid_fixture(fixture_id: str = "FX001") -> dict:
    return {
        "fixture_id": fixture_id,
        "TEST_FIXTURE": True,
        "DEMO_ONLY": True,
        "PAPER_ONLY": True,
        "RESEARCH_ONLY": True,
        "NOT_LIVE": True,
        "NO_BROKER": True,
        "NO_REAL_ACCOUNT": True,
        "NO_REAL_ORDERS": True,
        "NOT_FOR_PRODUCTION": True,
        "OPERATIONAL_INTEGRATION_ONLY": True,
        "scenario_id": "OI-C-001",
        "category": "contract",
        "expected_status": "PASS",
    }


class TestFixtureRegistrySafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestFixtureRegistryCore:
    def setup_method(self):
        self.registry = FixtureRegistry()

    def test_register_valid_fixture(self):
        fixture = _make_valid_fixture("FX001")
        result = self.registry.register(fixture)
        assert result["registered"] is True

    def test_register_returns_fixture_id(self):
        fixture = _make_valid_fixture("FX002")
        result = self.registry.register(fixture)
        assert result["fixture_id"] == "FX002"

    def test_register_paper_only_in_result(self):
        fixture = _make_valid_fixture("FX003")
        result = self.registry.register(fixture)
        assert result["paper_only"] is True

    def test_get_registered_fixture(self):
        fixture = _make_valid_fixture("FX_GET")
        self.registry.register(fixture)
        retrieved = self.registry.get("FX_GET")
        assert retrieved is not None
        assert retrieved["fixture_id"] == "FX_GET"

    def test_get_missing_returns_none(self):
        result = self.registry.get("NONEXISTENT_FIXTURE")
        assert result is None

    def test_list_ids_returns_list(self):
        self.registry.register(_make_valid_fixture("FX_LIST_1"))
        self.registry.register(_make_valid_fixture("FX_LIST_2"))
        ids = self.registry.list_ids()
        assert isinstance(ids, list)
        assert "FX_LIST_1" in ids
        assert "FX_LIST_2" in ids

    def test_list_ids_sorted(self):
        self.registry.register(_make_valid_fixture("FX_B"))
        self.registry.register(_make_valid_fixture("FX_A"))
        ids = self.registry.list_ids()
        assert ids == sorted(ids)

    def test_count_increases_after_register(self):
        initial = self.registry.count()
        self.registry.register(_make_valid_fixture("FX_COUNT"))
        assert self.registry.count() == initial + 1

    def test_validate_registered_fixture(self):
        self.registry.register(_make_valid_fixture("FX_VALIDATE"))
        result = self.registry.validate("FX_VALIDATE")
        assert result["valid"] is True

    def test_validate_missing_fixture(self):
        result = self.registry.validate("MISSING_FX")
        assert result["valid"] is False

    def test_validate_all_returns_dict(self):
        self.registry.register(_make_valid_fixture("FX_ALL_1"))
        result = self.registry.validate_all()
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_validate_all_total_count(self):
        initial_count = self.registry.count()
        self.registry.register(_make_valid_fixture("FX_TOTAL"))
        result = self.registry.validate_all()
        assert result["total"] == initial_count + 1

    def test_list_by_category(self):
        fixture = _make_valid_fixture("FX_CAT")
        fixture["category"] = "contract"
        self.registry.register(fixture)
        category_fixtures = self.registry.list_by_category("contract")
        assert any(f["fixture_id"] == "FX_CAT" for f in category_fixtures)

    def test_list_by_category_no_match(self):
        result = self.registry.list_by_category("nonexistent_category_xyz")
        assert result == []

    def test_summarize_returns_dict(self):
        self.registry.register(_make_valid_fixture("FX_SUM"))
        summary = self.registry.summarize()
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        summary = self.registry.summarize()
        assert summary.get("paper_only") is True

    def test_register_invalid_fixture_fails(self):
        # Missing required safety fields
        invalid = {"fixture_id": "BAD_FX"}
        result = self.registry.register(invalid)
        assert result["registered"] is False

    def test_register_missing_fixture_id_fails(self):
        fixture = _make_valid_fixture()
        del fixture["fixture_id"]
        result = self.registry.register(fixture)
        assert result["registered"] is False

    def test_summarize_total_fixtures(self):
        self.registry.register(_make_valid_fixture("FX_TOTAL_SUM"))
        summary = self.registry.summarize()
        assert "total_fixtures" in summary
        assert summary["total_fixtures"] > 0
