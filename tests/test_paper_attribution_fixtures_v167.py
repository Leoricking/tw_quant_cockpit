"""
tests/test_paper_attribution_fixtures_v167.py
Tests for paper attribution fixture schema and registry v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import json
import os
import pytest
from paper_trading.performance_attribution.fixture_schema_v167 import (
    REQUIRED_FIXTURE_MARKERS,
    FORBIDDEN_FIXTURE_FIELDS,
    validate_fixture_markers,
    validate_fixture_forbidden_fields,
    validate_fixture_metadata,
    validate_fixture_full,
    build_fixture_template,
    assert_fixture_safe,
)
from paper_trading.performance_attribution.fixture_registry_v167 import FixtureRegistry


FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), "fixtures", "paper_attribution"
)


class TestRequiredMarkers:
    def test_count_is_10(self):
        assert len(REQUIRED_FIXTURE_MARKERS) == 10

    def test_test_fixture_present(self):
        assert "test_fixture" in REQUIRED_FIXTURE_MARKERS

    def test_demo_only_present(self):
        assert "demo_only" in REQUIRED_FIXTURE_MARKERS

    def test_paper_only_present(self):
        assert "paper_only" in REQUIRED_FIXTURE_MARKERS

    def test_research_only_present(self):
        assert "research_only" in REQUIRED_FIXTURE_MARKERS

    def test_not_live_present(self):
        assert "not_live" in REQUIRED_FIXTURE_MARKERS

    def test_no_broker_present(self):
        assert "no_broker" in REQUIRED_FIXTURE_MARKERS

    def test_no_real_account_present(self):
        assert "no_real_account" in REQUIRED_FIXTURE_MARKERS

    def test_no_real_orders_present(self):
        assert "no_real_orders" in REQUIRED_FIXTURE_MARKERS

    def test_not_for_production_present(self):
        assert "not_for_production" in REQUIRED_FIXTURE_MARKERS

    def test_paper_attribution_only_present(self):
        assert "paper_attribution_only" in REQUIRED_FIXTURE_MARKERS

    def test_all_values_are_true(self):
        for k, v in REQUIRED_FIXTURE_MARKERS.items():
            assert v is True, f"{k} should be True"


class TestForbiddenFields:
    def test_nonempty(self):
        assert len(FORBIDDEN_FIXTURE_FIELDS) >= 10

    def test_broker_session_forbidden(self):
        assert "broker_session" in FORBIDDEN_FIXTURE_FIELDS

    def test_real_account_token_forbidden(self):
        assert "real_account_token" in FORBIDDEN_FIXTURE_FIELDS

    def test_api_secret_forbidden(self):
        assert "api_secret" in FORBIDDEN_FIXTURE_FIELDS

    def test_shioaji_login_forbidden(self):
        assert "shioaji_login" in FORBIDDEN_FIXTURE_FIELDS

    def test_is_frozenset(self):
        assert isinstance(FORBIDDEN_FIXTURE_FIELDS, frozenset)


class TestValidateFixtureMarkers:
    def _good(self):
        return {
            "test_fixture": True, "demo_only": True, "paper_only": True,
            "research_only": True, "not_live": True, "no_broker": True,
            "no_real_account": True, "no_real_orders": True,
            "not_for_production": True, "paper_attribution_only": True,
        }

    def test_all_markers_valid(self):
        r = validate_fixture_markers(self._good())
        assert r["valid"] is True

    def test_missing_one_marker_invalid(self):
        fx = self._good()
        del fx["test_fixture"]
        r = validate_fixture_markers(fx)
        assert r["valid"] is False

    def test_marker_set_to_false_invalid(self):
        fx = self._good()
        fx["paper_only"] = False
        r = validate_fixture_markers(fx)
        assert r["valid"] is False

    def test_all_10_missing_fails_with_10_errors(self):
        r = validate_fixture_markers({})
        assert len(r["errors"]) == 10


class TestValidateFixtureForbiddenFields:
    def test_clean_fixture_passes(self):
        r = validate_fixture_forbidden_fields({"run_id": "safe"})
        assert r["clean"] is True
        assert r["blocked"] is False

    def test_broker_session_blocks(self):
        r = validate_fixture_forbidden_fields({"broker_session": "live"})
        assert r["blocked"] is True

    def test_none_value_not_blocked(self):
        r = validate_fixture_forbidden_fields({"broker_session": None})
        assert r["blocked"] is False

    def test_false_value_not_blocked(self):
        r = validate_fixture_forbidden_fields({"broker_session": False})
        assert r["blocked"] is False


class TestBuildFixtureTemplate:
    def test_returns_dict(self):
        tmpl = build_fixture_template("fx_t1", "testing", "test")
        assert isinstance(tmpl, dict)

    def test_all_10_markers_present(self):
        tmpl = build_fixture_template("fx_t2", "testing", "test")
        for marker in REQUIRED_FIXTURE_MARKERS:
            assert marker in tmpl, f"Missing marker: {marker}"

    def test_all_markers_are_true(self):
        tmpl = build_fixture_template("fx_t3", "testing", "test")
        for marker in REQUIRED_FIXTURE_MARKERS:
            assert tmpl[marker] is True

    def test_fixture_id_set(self):
        tmpl = build_fixture_template("my_fx", "purpose", "cat")
        assert tmpl["fixture_id"] == "my_fx"

    def test_purpose_set(self):
        tmpl = build_fixture_template("fx_p", "my purpose", "cat")
        assert tmpl["purpose"] == "my purpose"

    def test_forbidden_fields_stripped(self):
        tmpl = build_fixture_template("fx_clean", "test", "test",
                                       extra={"broker_session": "live", "safe_field": "ok"})
        assert "broker_session" not in tmpl
        assert tmpl.get("safe_field") == "ok"

    def test_template_passes_full_validation(self):
        tmpl = build_fixture_template("fx_valid", "valid test", "test")
        r = validate_fixture_full(tmpl)
        assert r["valid"] is True


class TestValidateFixtureFull:
    def test_full_valid_fixture(self):
        tmpl = build_fixture_template("fx_full", "full test", "test")
        r = validate_fixture_full(tmpl)
        assert r["valid"] is True
        assert r["blocked"] is False

    def test_forbidden_field_blocks(self):
        tmpl = build_fixture_template("fx_blk", "blocked", "test")
        tmpl["broker_session"] = "live"
        r = validate_fixture_full(tmpl)
        assert r["blocked"] is True

    def test_missing_marker_invalid(self):
        tmpl = build_fixture_template("fx_missing", "missing", "test")
        del tmpl["test_fixture"]
        r = validate_fixture_full(tmpl)
        assert r["valid"] is False

    def test_missing_fixture_id_invalid(self):
        tmpl = build_fixture_template("fx_noid", "no id", "test")
        del tmpl["fixture_id"]
        r = validate_fixture_full(tmpl)
        assert r["valid"] is False


class TestAssertFixtureSafe:
    def test_safe_fixture_no_raise(self):
        tmpl = build_fixture_template("fx_safe", "safe test", "test")
        assert_fixture_safe(tmpl)  # should not raise

    def test_invalid_fixture_raises(self):
        with pytest.raises(ValueError):
            assert_fixture_safe({"fixture_id": "bad", "purpose": "oops"})

    def test_blocked_fixture_raises(self):
        tmpl = build_fixture_template("fx_blk2", "blocked", "test")
        tmpl["broker_session"] = "live"
        with pytest.raises(ValueError):
            assert_fixture_safe(tmpl)


class TestFixtureRegistry:
    def setup_method(self):
        self.reg = FixtureRegistry()

    def test_register_valid_fixture(self):
        tmpl = build_fixture_template("reg_fx1", "registry test 1", "test")
        r = self.reg.register(tmpl)
        assert r["registered"] is True

    def test_register_invalid_fixture_fails(self):
        bad = {"fixture_id": "bad_fx", "purpose": "bad"}
        r = self.reg.register(bad)
        assert r["registered"] is False

    def test_register_blocked_fixture_fails(self):
        tmpl = build_fixture_template("blk_fx", "blocked", "test")
        tmpl["broker_session"] = "live"
        r = self.reg.register(tmpl)
        assert r["registered"] is False

    def test_get_registered_fixture(self):
        tmpl = build_fixture_template("get_fx", "get test", "test")
        self.reg.register(tmpl)
        f = self.reg.get("get_fx")
        assert f is not None
        assert f["fixture_id"] == "get_fx"

    def test_get_nonexistent_returns_none(self):
        f = self.reg.get("no_such_fixture")
        assert f is None

    def test_list_ids_sorted(self):
        for fid in ("z_fx", "a_fx", "m_fx"):
            self.reg.register(build_fixture_template(fid, "test", "test"))
        ids = self.reg.list_ids()
        assert ids == sorted(ids)

    def test_count_after_registrations(self):
        for i in range(3):
            self.reg.register(build_fixture_template(f"cnt_fx_{i}", "test", "test"))
        assert self.reg.count() == 3

    def test_validate_registered(self):
        tmpl = build_fixture_template("val_fx", "validate test", "test")
        self.reg.register(tmpl)
        r = self.reg.validate("val_fx")
        assert r["valid"] is True

    def test_validate_all_no_failures(self):
        for i in range(3):
            self.reg.register(build_fixture_template(f"all_fx_{i}", "test", "test"))
        r = self.reg.validate_all()
        assert r["failures"] == 0

    def test_delete_removes_fixture(self):
        tmpl = build_fixture_template("del_fx", "delete test", "test")
        self.reg.register(tmpl)
        r = self.reg.delete("del_fx")
        assert r["deleted"] is True
        assert self.reg.get("del_fx") is None

    def test_delete_nonexistent_not_deleted(self):
        r = self.reg.delete("ghost_fx")
        assert r["deleted"] is False

    def test_list_by_category(self):
        for i in range(3):
            self.reg.register(build_fixture_template(f"cat_fx_{i}", "test", "reconciliation"))
        self.reg.register(build_fixture_template("other_fx", "test", "safety"))
        cats = self.reg.list_by_category("reconciliation")
        assert len(cats) == 3

    def test_export_manifest(self):
        tmpl = build_fixture_template("manifest_fx", "manifest test", "test")
        self.reg.register(tmpl)
        manifest = self.reg.export_manifest()
        assert len(manifest) == 1
        assert manifest[0]["fixture_id"] == "manifest_fx"


class TestJsonFixtureFiles:
    """Verify all JSON fixtures on disk pass full validation."""

    @pytest.mark.skipif(
        not os.path.isdir(FIXTURE_DIR),
        reason="Fixture directory not found"
    )
    def test_all_json_fixtures_have_10_markers(self):
        files = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json") and not f.startswith("_")]
        assert len(files) >= 90, f"Expected >=90 fixtures, got {len(files)}"
        for fname in files:
            path = os.path.join(FIXTURE_DIR, fname)
            with open(path) as fh:
                data = json.load(fh)
            for marker in REQUIRED_FIXTURE_MARKERS:
                assert marker in data, f"{fname} missing marker: {marker}"
                assert data[marker] is True, f"{fname}: {marker} != True"

    @pytest.mark.skipif(
        not os.path.isdir(FIXTURE_DIR),
        reason="Fixture directory not found"
    )
    def test_all_json_fixtures_no_forbidden_fields(self):
        files = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json") and not f.startswith("_")]
        for fname in files:
            path = os.path.join(FIXTURE_DIR, fname)
            with open(path) as fh:
                data = json.load(fh)
            r = validate_fixture_forbidden_fields(data)
            assert not r["blocked"], f"{fname} has forbidden fields: {r['violations']}"
