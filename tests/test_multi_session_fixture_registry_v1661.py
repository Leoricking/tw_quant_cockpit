"""
test_multi_session_fixture_registry_v1661.py — Fixture Registry tests v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestFixtureRegistryCount:
    def test_total_fixtures_is_80(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        assert len(list_fixtures()) == 80

    def test_all_fixtures_referenced(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_unreferenced_fixtures
        assert list_unreferenced_fixtures() == []

    def test_usage_summary_registered_80(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["registered"] == 80

    def test_usage_summary_referenced_80(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["referenced"] == 80

    def test_usage_summary_unused_0(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["unused"] == 0

    def test_no_duplicate_ids(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["duplicate_ids"] == []

    def test_no_duplicate_paths(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["duplicate_paths"] == []

    def test_no_missing_purposes(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["missing_purpose"] == []

    def test_no_invalid_purposes(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["invalid_purpose"] == []

    def test_all_referenced_flag_true(self):
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["all_referenced"] is True


class TestFixtureEntries:
    def test_each_entry_has_fixture_id(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        for entry in list_fixtures():
            assert entry.fixture_id and isinstance(entry.fixture_id, str)

    def test_each_entry_has_filename(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        for entry in list_fixtures():
            assert entry.filename.endswith(".json")

    def test_each_entry_has_category(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures, VALID_CATEGORIES
        for entry in list_fixtures():
            assert entry.category in VALID_CATEGORIES, f"{entry.fixture_id}: bad category {entry.category!r}"

    def test_each_entry_has_purpose(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures, VALID_PURPOSES
        for entry in list_fixtures():
            assert entry.purpose in VALID_PURPOSES, f"{entry.fixture_id}: bad purpose {entry.purpose!r}"

    def test_each_entry_has_description(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        for entry in list_fixtures():
            assert entry.description and len(entry.description) > 5

    def test_each_entry_has_referenced_by(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        for entry in list_fixtures():
            assert entry.referenced_by, f"{entry.fixture_id} has empty referenced_by"

    def test_fixture_ids_are_unique(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        ids = [e.fixture_id for e in list_fixtures()]
        assert len(ids) == len(set(ids))

    def test_paths_are_unique(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        paths = [e.path for e in list_fixtures()]
        assert len(paths) == len(set(paths))

    def test_all_entries_are_referenced(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        for entry in list_fixtures():
            assert entry.is_referenced(), f"{entry.fixture_id} is not referenced"


class TestGetFixture:
    def test_get_known_fixture(self):
        from paper_trading.multi_session.fixture_registry_v1661 import get_fixture
        entry = get_fixture("chk_create")
        assert entry is not None
        assert entry.fixture_id == "chk_create"

    def test_get_unknown_fixture_returns_none(self):
        from paper_trading.multi_session.fixture_registry_v1661 import get_fixture
        assert get_fixture("__nonexistent_fixture__") is None

    def test_get_res_renew(self):
        from paper_trading.multi_session.fixture_registry_v1661 import get_fixture
        entry = get_fixture("res_renew")
        assert entry is not None
        assert entry.category == "resource"


class TestValidateFixtureReference:
    def test_registered_and_referenced_passes(self):
        from paper_trading.multi_session.fixture_registry_v1661 import validate_fixture_reference
        ok, msg = validate_fixture_reference("reg_single")
        assert ok is True
        assert msg == ""

    def test_unknown_fixture_fails(self):
        from paper_trading.multi_session.fixture_registry_v1661 import validate_fixture_reference
        ok, msg = validate_fixture_reference("__unknown_fixture_xyz__")
        assert ok is False
        assert "not registered" in msg

    def test_duplicate_fixture_detection(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        ids = [e.fixture_id for e in list_fixtures()]
        assert len(ids) == len(set(ids)), "Duplicate fixture IDs detected"

    def test_missing_registry_entry_fails(self):
        from paper_trading.multi_session.fixture_registry_v1661 import validate_fixture_reference
        ok, _ = validate_fixture_reference("does_not_exist_v999")
        assert ok is False


class TestListReferencedFixtures:
    def test_all_80_referenced(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_referenced_fixtures
        assert len(list_referenced_fixtures()) == 80

    def test_no_unreferenced_fixtures(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_unreferenced_fixtures
        assert len(list_unreferenced_fixtures()) == 0

    def test_list_is_deterministic(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_referenced_fixtures
        r1 = [e.fixture_id for e in list_referenced_fixtures()]
        r2 = [e.fixture_id for e in list_referenced_fixtures()]
        assert r1 == r2


class TestFixtureCategories:
    def test_checkpoint_recovery_category_exists(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        cats = {e.category for e in list_fixtures()}
        assert "checkpoint_recovery" in cats

    def test_coordination_category_exists(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        cats = {e.category for e in list_fixtures()}
        assert "coordination" in cats

    def test_capital_risk_category_exists(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        cats = {e.category for e in list_fixtures()}
        assert "capital_risk" in cats

    def test_event_ordering_category_exists(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        cats = {e.category for e in list_fixtures()}
        assert "event_ordering" in cats

    def test_lifecycle_category_exists(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        cats = {e.category for e in list_fixtures()}
        assert "lifecycle" in cats

    def test_resource_category_exists(self):
        from paper_trading.multi_session.fixture_registry_v1661 import list_fixtures
        cats = {e.category for e in list_fixtures()}
        assert "resource" in cats
