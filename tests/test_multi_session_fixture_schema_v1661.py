"""
test_multi_session_fixture_schema_v1661.py — Fixture Schema validation tests v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestRequiredFixtureMarkers:
    def test_required_markers_dict_exists(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert isinstance(REQUIRED_FIXTURE_MARKERS, dict)

    def test_required_markers_count_is_10(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS, MARKER_COUNT
        assert len(REQUIRED_FIXTURE_MARKERS) == 10
        assert MARKER_COUNT == 10

    def test_all_required_marker_values_are_true(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        for key, val in REQUIRED_FIXTURE_MARKERS.items():
            assert val is True, f"marker {key!r} must be True, got {val!r}"

    def test_required_marker_keys(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        expected = {
            "test_fixture", "demo_only", "paper_only", "research_only", "not_live",
            "no_broker", "no_real_account", "no_real_orders", "not_for_production",
            "multi_session_only",
        }
        assert set(REQUIRED_FIXTURE_MARKERS.keys()) == expected

    def test_test_fixture_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "test_fixture" in REQUIRED_FIXTURE_MARKERS

    def test_demo_only_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "demo_only" in REQUIRED_FIXTURE_MARKERS

    def test_paper_only_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "paper_only" in REQUIRED_FIXTURE_MARKERS

    def test_research_only_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "research_only" in REQUIRED_FIXTURE_MARKERS

    def test_not_live_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "not_live" in REQUIRED_FIXTURE_MARKERS

    def test_no_broker_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "no_broker" in REQUIRED_FIXTURE_MARKERS

    def test_no_real_account_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "no_real_account" in REQUIRED_FIXTURE_MARKERS

    def test_no_real_orders_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "no_real_orders" in REQUIRED_FIXTURE_MARKERS

    def test_not_for_production_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "not_for_production" in REQUIRED_FIXTURE_MARKERS

    def test_multi_session_only_in_markers(self):
        from paper_trading.multi_session.fixture_schema_v1661 import REQUIRED_FIXTURE_MARKERS
        assert "multi_session_only" in REQUIRED_FIXTURE_MARKERS


class TestValidateFixtureMarkers:
    def _valid_fixture(self):
        return {
            "test_fixture": True, "demo_only": True, "paper_only": True,
            "research_only": True, "not_live": True, "no_broker": True,
            "no_real_account": True, "no_real_orders": True,
            "not_for_production": True, "multi_session_only": True,
            "test_id": "test_x", "version": "1.6.6.1",
        }

    def test_valid_fixture_passes(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        is_valid, violations = validate_fixture_markers(self._valid_fixture())
        assert is_valid is True
        assert violations == []

    def test_missing_test_fixture_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        del fx["test_fixture"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False
        assert any("test_fixture" in v for v in violations)

    def test_missing_demo_only_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        del fx["demo_only"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_missing_not_live_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        del fx["not_live"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_missing_no_broker_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        del fx["no_broker"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_missing_no_real_account_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        del fx["no_real_account"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_missing_not_for_production_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        del fx["not_for_production"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_missing_multi_session_only_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        del fx["multi_session_only"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_false_marker_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        fx["paper_only"] = False
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False
        assert any("paper_only" in v for v in violations)

    def test_null_marker_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        fx["research_only"] = None
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_string_true_marker_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        fx["no_real_orders"] = "true"
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_integer_1_marker_fails(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = self._valid_fixture()
        fx["not_live"] = 1
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_violations_list_per_missing_marker(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = {
            "test_fixture": True, "demo_only": True, "paper_only": True,
            "research_only": True,
        }
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False
        assert len(violations) == 6  # 6 missing markers

    def test_empty_fixture_has_10_violations(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        is_valid, violations = validate_fixture_markers({})
        assert is_valid is False
        assert len(violations) == 10


class TestFindMissingMarkers:
    def test_no_missing_on_valid_fixture(self):
        from paper_trading.multi_session.fixture_schema_v1661 import find_missing_markers
        fx = {k: True for k in [
            "test_fixture","demo_only","paper_only","research_only","not_live",
            "no_broker","no_real_account","no_real_orders","not_for_production","multi_session_only"
        ]}
        assert find_missing_markers(fx) == []

    def test_returns_missing_keys(self):
        from paper_trading.multi_session.fixture_schema_v1661 import find_missing_markers
        missing = find_missing_markers({"paper_only": True})
        assert "test_fixture" in missing
        assert "paper_only" not in missing

    def test_returns_all_10_when_empty(self):
        from paper_trading.multi_session.fixture_schema_v1661 import find_missing_markers
        assert len(find_missing_markers({})) == 10


class TestFindInvalidMarkerValues:
    def test_no_invalid_on_valid_fixture(self):
        from paper_trading.multi_session.fixture_schema_v1661 import find_invalid_marker_values
        fx = {k: True for k in [
            "test_fixture","demo_only","paper_only","research_only","not_live",
            "no_broker","no_real_account","no_real_orders","not_for_production","multi_session_only"
        ]}
        assert find_invalid_marker_values(fx) == []

    def test_detects_false_value(self):
        from paper_trading.multi_session.fixture_schema_v1661 import find_invalid_marker_values
        fx = {k: True for k in [
            "test_fixture","demo_only","paper_only","research_only","not_live",
            "no_broker","no_real_account","no_real_orders","not_for_production","multi_session_only"
        ]}
        fx["paper_only"] = False
        invalid = find_invalid_marker_values(fx)
        assert len(invalid) == 1
        assert invalid[0][0] == "paper_only"


class TestFixtureSafetySummary:
    def _make_valid(self, test_id: str):
        return {
            "test_fixture": True, "demo_only": True, "paper_only": True,
            "research_only": True, "not_live": True, "no_broker": True,
            "no_real_account": True, "no_real_orders": True,
            "not_for_production": True, "multi_session_only": True,
            "test_id": test_id,
        }

    def test_all_valid_returns_all_valid(self):
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        fixtures = [self._make_valid(f"id_{i}") for i in range(5)]
        summary = fixture_safety_summary(fixtures)
        assert summary["total"] == 5
        assert summary["valid"] == 5
        assert summary["invalid"] == 0
        assert summary["all_valid"] is True

    def test_one_invalid_detected(self):
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        fixtures = [self._make_valid(f"id_{i}") for i in range(3)]
        fixtures[1]["paper_only"] = False
        summary = fixture_safety_summary(fixtures)
        assert summary["invalid"] == 1
        assert summary["all_valid"] is False

    def test_missing_by_marker_counts(self):
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        fx1 = self._make_valid("id_1")
        fx2 = {"test_id": "id_2"}  # missing all markers
        summary = fixture_safety_summary([fx1, fx2])
        assert summary["missing_by_marker"]["test_fixture"] == 1

    def test_summary_deterministic(self):
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        fixtures = [self._make_valid(f"id_{i}") for i in range(10)]
        s1 = fixture_safety_summary(fixtures)
        s2 = fixture_safety_summary(fixtures)
        assert s1 == s2
