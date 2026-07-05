"""
tests/test_stable_rollup_manifest_v169.py
Tests for release_manifest_v169 module.
"""
import pytest
from paper_trading.stable_rollup.release_manifest_v169 import (
    RELEASE_MANIFEST, get_manifest, get_release, get_all_versions, validate_manifest,
)


def test_manifest_is_list():
    assert isinstance(RELEASE_MANIFEST, list)


def test_manifest_count():
    assert len(RELEASE_MANIFEST) == 13


def test_get_manifest_returns_list():
    m = get_manifest()
    assert isinstance(m, list)
    assert len(m) == 13


def test_get_manifest_returns_copy():
    m1 = get_manifest()
    m2 = get_manifest()
    assert m1 is not m2
    assert m1 == m2


def test_all_versions_contains_160():
    versions = get_all_versions()
    assert "1.6.0" in versions


def test_all_versions_contains_169():
    versions = get_all_versions()
    assert "1.6.9" in versions


def test_all_versions_count():
    versions = get_all_versions()
    assert len(versions) == 13


def test_all_versions_unique():
    versions = get_all_versions()
    assert len(set(versions)) == len(versions)


def test_get_release_169():
    entry = get_release("1.6.9")
    assert entry is not None
    assert entry["version"] == "1.6.9"
    assert entry["release_name"] == "Live Paper Trading Stable Rollup"


def test_get_release_160():
    entry = get_release("1.6.0")
    assert entry is not None
    assert entry["version"] == "1.6.0"
    assert entry["parent_version"] is None


def test_get_release_nonexistent():
    entry = get_release("9.9.9")
    assert entry is None


def test_validate_manifest_status():
    result = validate_manifest()
    assert result["status"] == "PASS"


def test_validate_manifest_no_issues():
    result = validate_manifest()
    assert result["issues"] == []


def test_validate_manifest_total():
    result = validate_manifest()
    assert result["total"] == 13


def test_manifest_parent_chain_169_to_168():
    entry = get_release("1.6.9")
    assert entry["parent_version"] == "1.6.8"


def test_manifest_parent_chain_168_to_167():
    entry = get_release("1.6.8")
    assert entry["parent_version"] == "1.6.7"


def test_manifest_hotfixes_sealed():
    for entry in get_manifest():
        if entry.get("release_category") == "hotfix":
            assert entry["sealed_status"] == "SEALED", f"{entry['version']} hotfix not SEALED"


def test_manifest_v169_not_sealed():
    entry = get_release("1.6.9")
    assert entry["sealed_status"] == "NOT_SEALED"


def test_manifest_each_has_version():
    for entry in get_manifest():
        assert "version" in entry
        assert entry["version"]


def test_manifest_each_has_release_name():
    for entry in get_manifest():
        assert "release_name" in entry
        assert entry["release_name"]


def test_manifest_each_has_safety_boundaries():
    for entry in get_manifest():
        assert "safety_boundaries" in entry
        assert isinstance(entry["safety_boundaries"], list)
