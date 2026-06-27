"""
tests/test_failure_validation_fixtures_v165.py — Fixture Validation tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import json
import os

import pytest

from paper_trading.failure_validation.fixtures_validator_v165 import (
    PAPER_ONLY,
    RESEARCH_ONLY,
    REQUIRED_SAFETY_MARKERS,
    validate_fixture_directory,
    validate_fixture_file,
    validate_fixture_safety_markers,
)

FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), "fixtures", "failure_injection"
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestFixtureSafetyFlags:
    def test_paper_only_true(self):
        assert PAPER_ONLY is True

    def test_research_only_true(self):
        assert RESEARCH_ONLY is True

    def test_required_markers_count(self):
        assert len(REQUIRED_SAFETY_MARKERS) == 10


# ---------------------------------------------------------------------------
# REQUIRED_SAFETY_MARKERS content
# ---------------------------------------------------------------------------

class TestRequiredSafetyMarkersList:
    def test_test_fixture_required(self):
        assert "TEST_FIXTURE" in REQUIRED_SAFETY_MARKERS

    def test_demo_only_required(self):
        assert "DEMO_ONLY" in REQUIRED_SAFETY_MARKERS

    def test_paper_only_required(self):
        assert "PAPER_ONLY" in REQUIRED_SAFETY_MARKERS

    def test_research_only_required(self):
        assert "RESEARCH_ONLY" in REQUIRED_SAFETY_MARKERS

    def test_not_live_required(self):
        assert "NOT_LIVE" in REQUIRED_SAFETY_MARKERS

    def test_no_broker_required(self):
        assert "NO_BROKER" in REQUIRED_SAFETY_MARKERS

    def test_no_real_account_required(self):
        assert "NO_REAL_ACCOUNT" in REQUIRED_SAFETY_MARKERS

    def test_no_real_order_required(self):
        assert "NO_REAL_ORDER" in REQUIRED_SAFETY_MARKERS

    def test_not_for_production_required(self):
        assert "NOT_FOR_PRODUCTION" in REQUIRED_SAFETY_MARKERS

    def test_failure_injection_only_required(self):
        assert "FAILURE_INJECTION_ONLY" in REQUIRED_SAFETY_MARKERS


# ---------------------------------------------------------------------------
# validate_fixture_safety_markers function
# ---------------------------------------------------------------------------

class TestValidateFixtureSafetyMarkers:
    def _valid_fixture(self):
        return {
            "TEST_FIXTURE": True,
            "DEMO_ONLY": True,
            "PAPER_ONLY": True,
            "RESEARCH_ONLY": True,
            "NOT_LIVE": True,
            "NO_BROKER": True,
            "NO_REAL_ACCOUNT": True,
            "NO_REAL_ORDER": True,
            "NOT_FOR_PRODUCTION": True,
            "FAILURE_INJECTION_ONLY": True,
            "scenario_name": "test_scenario",
        }

    def test_valid_fixture_passes(self):
        ok, missing = validate_fixture_safety_markers(self._valid_fixture())
        assert ok is True
        assert missing == []

    def test_missing_one_marker_fails(self):
        data = self._valid_fixture()
        del data["NO_BROKER"]
        ok, missing = validate_fixture_safety_markers(data)
        assert ok is False
        assert "NO_BROKER" in missing

    def test_false_marker_fails(self):
        data = self._valid_fixture()
        data["TEST_FIXTURE"] = False
        ok, missing = validate_fixture_safety_markers(data)
        assert ok is False
        assert "TEST_FIXTURE" in missing

    def test_missing_all_markers_fails(self):
        ok, missing = validate_fixture_safety_markers({"scenario_name": "x"})
        assert ok is False
        assert len(missing) == 10

    def test_extra_fields_do_not_affect_result(self):
        data = self._valid_fixture()
        data["extra_field"] = "extra_value"
        ok, missing = validate_fixture_safety_markers(data)
        assert ok is True


# ---------------------------------------------------------------------------
# Actual fixture directory validation
# ---------------------------------------------------------------------------

class TestFixtureDirectoryContents:
    def test_fixture_directory_exists(self):
        assert os.path.isdir(FIXTURE_DIR), f"Fixture directory not found: {FIXTURE_DIR}"

    def test_at_least_70_fixtures(self):
        fixtures = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")]
        assert len(fixtures) >= 70, f"Expected ≥70 fixtures, got {len(fixtures)}"

    def test_all_fixtures_are_valid_json(self):
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)  # Will raise if invalid JSON
                assert isinstance(data, dict), f"{fname}: not a JSON object"

    def test_all_fixtures_have_all_safety_markers(self):
        failed = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                ok, missing = validate_fixture_file(fpath)
                if not ok:
                    failed.append((fname, missing))
        assert failed == [], f"Fixtures missing safety markers: {failed[:3]}"

    def test_all_fixtures_have_scenario_name(self):
        missing_name = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "scenario_name" not in data:
                    missing_name.append(fname)
        assert missing_name == [], f"Fixtures missing scenario_name: {missing_name[:3]}"

    def test_all_fixtures_have_domain(self):
        missing_domain = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "domain" not in data:
                    missing_domain.append(fname)
        assert missing_domain == [], f"Fixtures missing domain: {missing_domain[:3]}"

    def test_all_fixtures_have_seed(self):
        missing_seed = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "seed" not in data:
                    missing_seed.append(fname)
        assert missing_seed == [], f"Fixtures missing seed: {missing_seed[:3]}"

    def test_all_fixture_seeds_are_integers(self):
        bad_seeds = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "seed" in data and not isinstance(data["seed"], int):
                    bad_seeds.append(fname)
        assert bad_seeds == [], f"Fixtures with non-integer seed: {bad_seeds[:3]}"

    def test_no_fixture_references_broker(self):
        bad = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # domain field should never be BROKER
                if str(data.get("domain", "")).upper() == "BROKER":
                    bad.append(fname)
        assert bad == [], f"Fixtures with BROKER domain: {bad}"

    def test_all_fixtures_no_broker_marker_true(self):
        bad = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not data.get("NO_BROKER", False):
                    bad.append(fname)
        assert bad == [], f"Fixtures without NO_BROKER=True: {bad[:3]}"

    def test_all_fixtures_no_real_order_marker_true(self):
        bad = []
        for fname in os.listdir(FIXTURE_DIR):
            if fname.endswith(".json"):
                fpath = os.path.join(FIXTURE_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not data.get("NO_REAL_ORDER", False):
                    bad.append(fname)
        assert bad == [], f"Fixtures without NO_REAL_ORDER=True: {bad[:3]}"


# ---------------------------------------------------------------------------
# validate_fixture_directory function
# ---------------------------------------------------------------------------

class TestValidateFixtureDirectory:
    def test_validate_directory_returns_dict(self):
        result = validate_fixture_directory(FIXTURE_DIR)
        assert isinstance(result, dict)

    def test_validate_directory_has_total(self):
        result = validate_fixture_directory(FIXTURE_DIR)
        assert "total" in result

    def test_validate_directory_total_ge_70(self):
        result = validate_fixture_directory(FIXTURE_DIR)
        assert result["total"] >= 70

    def test_validate_directory_all_pass(self):
        result = validate_fixture_directory(FIXTURE_DIR)
        assert result["failed"] == 0, (
            f"Fixture directory validation failures: "
            + str({k: v for k, v in result["files"].items() if not v["passed"]})
        )

    def test_validate_directory_passed_equals_total(self):
        result = validate_fixture_directory(FIXTURE_DIR)
        assert result["passed"] == result["total"]

    def test_validate_directory_has_files_key(self):
        result = validate_fixture_directory(FIXTURE_DIR)
        assert "files" in result
