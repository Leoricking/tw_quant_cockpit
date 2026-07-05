"""
tests/test_stable_rollup_validator_v169.py
Tests for stable_validator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.stable_validator_v169 import StableValidator, run_all_validations


def test_validator_instantiable():
    v = StableValidator()
    assert v is not None


def test_validate_version_returns_result():
    v = StableValidator()
    r = v.validate_version()
    assert hasattr(r, "validator_name")
    assert r.validator_name == "version_validator"


def test_validate_version_passes():
    v = StableValidator()
    r = v.validate_version()
    assert r.passed is True


def test_validate_safety_returns_result():
    v = StableValidator()
    r = v.validate_safety()
    assert r.validator_name == "safety_validator"


def test_validate_safety_passes():
    v = StableValidator()
    r = v.validate_safety()
    assert r.passed is True


def test_validate_manifest_returns_result():
    v = StableValidator()
    r = v.validate_manifest()
    assert r.validator_name == "manifest_validator"


def test_validate_manifest_passes():
    v = StableValidator()
    r = v.validate_manifest()
    assert r.passed is True


def test_validate_lineage_returns_result():
    v = StableValidator()
    r = v.validate_lineage()
    assert r.validator_name == "lineage_validator"


def test_validate_lineage_passes():
    v = StableValidator()
    r = v.validate_lineage()
    assert r.passed is True


def test_validate_all_returns_list():
    v = StableValidator()
    results = v.validate_all()
    assert isinstance(results, list)
    assert len(results) == 4


def test_validate_all_all_pass():
    v = StableValidator()
    results = v.validate_all()
    for r in results:
        assert r.passed is True, f"{r.validator_name} failed: {r.issues}"


def test_run_all_validations_returns_dict():
    result = run_all_validations()
    assert isinstance(result, dict)
    assert "status" in result


def test_run_all_validations_pass():
    result = run_all_validations()
    assert result["status"] == "PASS"
    assert result["all_pass"] is True


def test_run_all_validations_total_4():
    result = run_all_validations()
    assert result["total"] == 4


def test_run_all_validations_paper_only():
    result = run_all_validations()
    assert result.get("paper_only") is True


def test_run_all_validations_no_real_orders():
    result = run_all_validations()
    assert result.get("no_real_orders") is True
