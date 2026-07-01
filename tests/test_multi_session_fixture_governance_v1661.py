"""
test_multi_session_fixture_governance_v1661.py — Fixture Governance tests v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker.
Tests all 80 actual fixture files for JSON validity, marker completeness, and IDs.
"""
import json
import os
import pytest

FIXTURE_DIR = "tests/fixtures/multi_session"
REQUIRED_MARKERS = [
    "test_fixture", "demo_only", "paper_only", "research_only", "not_live",
    "no_broker", "no_real_account", "no_real_orders", "not_for_production",
    "multi_session_only",
]


def _load_all():
    files = sorted(f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json"))
    fixtures = []
    for fname in files:
        path = os.path.join(FIXTURE_DIR, fname)
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        fixtures.append((fname, data))
    return fixtures


class TestAllFixturesLoad:
    def test_fixture_dir_exists(self):
        assert os.path.isdir(FIXTURE_DIR)

    def test_exactly_80_fixture_files(self):
        files = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")]
        assert len(files) == 80

    def test_all_80_valid_json(self):
        fixtures = _load_all()
        assert len(fixtures) == 80

    def test_all_80_have_test_id(self):
        for fname, data in _load_all():
            assert "test_id" in data, f"{fname}: missing 'test_id'"

    def test_all_80_unique_ids(self):
        ids = [data.get("test_id") for _, data in _load_all()]
        assert len(ids) == len(set(ids)), f"Duplicate test_ids: {[x for x in set(ids) if ids.count(x)>1]}"

    def test_all_80_have_version(self):
        for fname, data in _load_all():
            assert "version" in data, f"{fname}: missing 'version'"


class TestAllFixturesHaveAllMarkers:
    def test_all_80_have_test_fixture(self):
        for fname, data in _load_all():
            assert data.get("test_fixture") is True, f"{fname}: test_fixture not True"

    def test_all_80_have_demo_only(self):
        for fname, data in _load_all():
            assert data.get("demo_only") is True, f"{fname}: demo_only not True"

    def test_all_80_have_paper_only(self):
        for fname, data in _load_all():
            assert data.get("paper_only") is True, f"{fname}: paper_only not True"

    def test_all_80_have_research_only(self):
        for fname, data in _load_all():
            assert data.get("research_only") is True, f"{fname}: research_only not True"

    def test_all_80_have_not_live(self):
        for fname, data in _load_all():
            assert data.get("not_live") is True, f"{fname}: not_live not True"

    def test_all_80_have_no_broker(self):
        for fname, data in _load_all():
            assert data.get("no_broker") is True, f"{fname}: no_broker not True"

    def test_all_80_have_no_real_account(self):
        for fname, data in _load_all():
            assert data.get("no_real_account") is True, f"{fname}: no_real_account not True"

    def test_all_80_have_no_real_orders(self):
        for fname, data in _load_all():
            assert data.get("no_real_orders") is True, f"{fname}: no_real_orders not True"

    def test_all_80_have_not_for_production(self):
        for fname, data in _load_all():
            assert data.get("not_for_production") is True, f"{fname}: not_for_production not True"

    def test_all_80_have_multi_session_only(self):
        for fname, data in _load_all():
            assert data.get("multi_session_only") is True, f"{fname}: multi_session_only not True"

    def test_all_10_markers_present_in_all_80(self):
        for fname, data in _load_all():
            for marker in REQUIRED_MARKERS:
                assert marker in data, f"{fname}: missing marker '{marker}'"
                assert data[marker] is True, f"{fname}: marker '{marker}' is not True (got {data[marker]!r})"

    def test_marker_values_are_boolean_not_string(self):
        for fname, data in _load_all():
            for marker in REQUIRED_MARKERS:
                val = data.get(marker)
                assert isinstance(val, bool), f"{fname}: {marker!r} is {type(val)}, expected bool"

    def test_marker_values_are_boolean_not_int(self):
        for fname, data in _load_all():
            for marker in REQUIRED_MARKERS:
                val = data.get(marker)
                assert type(val) is bool, f"{fname}: {marker!r} is int not bool"


class TestFixtureSchemaValidation:
    def test_schema_validates_all_80(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers, fixture_safety_summary
        fixtures = [data for _, data in _load_all()]
        summary = fixture_safety_summary(fixtures)
        assert summary["valid"] == 80
        assert summary["invalid"] == 0
        assert summary["all_valid"] is True

    def test_schema_missing_by_marker_all_zero(self):
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        fixtures = [data for _, data in _load_all()]
        summary = fixture_safety_summary(fixtures)
        for marker, count in summary["missing_by_marker"].items():
            assert count == 0, f"marker {marker!r} missing from {count} fixtures"

    def test_schema_invalid_values_all_zero(self):
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        fixtures = [data for _, data in _load_all()]
        summary = fixture_safety_summary(fixtures)
        for marker, count in summary["invalid_values_by_marker"].items():
            assert count == 0, f"marker {marker!r} has {count} invalid values"


class TestNegativeCases:
    def test_missing_marker_fails_validation(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = {m: True for m in REQUIRED_MARKERS}
        del fx["not_live"]
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False
        assert len(violations) == 1

    def test_false_marker_fails_validation(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = {m: True for m in REQUIRED_MARKERS}
        fx["no_broker"] = False
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_null_marker_fails_validation(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = {m: True for m in REQUIRED_MARKERS}
        fx["demo_only"] = None
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_string_true_marker_fails_validation(self):
        from paper_trading.multi_session.fixture_schema_v1661 import validate_fixture_markers
        fx = {m: True for m in REQUIRED_MARKERS}
        fx["test_fixture"] = "true"
        is_valid, violations = validate_fixture_markers(fx)
        assert is_valid is False

    def test_missing_registry_entry_fails(self):
        from paper_trading.multi_session.fixture_registry_v1661 import validate_fixture_reference
        ok, _ = validate_fixture_reference("__does_not_exist__")
        assert ok is False

    def test_full_valid_dataset_passes(self):
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        fixtures = [data for _, data in _load_all()]
        summary = fixture_safety_summary(fixtures)
        assert summary["all_valid"] is True

    def test_governance_summary_deterministic(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        s1 = fixture_usage_summary()
        s2 = fixture_usage_summary()
        assert s1["total"] == s2["total"]
        assert s1["referenced"] == s2["referenced"]
        assert s1["unused"] == s2["unused"]
