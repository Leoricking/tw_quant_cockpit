"""
tests/test_stable_rollup_registry_v169.py
Tests for release_registry_v169 module.
"""
import pytest
from paper_trading.stable_rollup.release_registry_v169 import ReleaseRegistry, get_registry


def test_get_registry_returns_instance():
    reg = get_registry()
    assert isinstance(reg, ReleaseRegistry)


def test_get_registry_singleton():
    reg1 = get_registry()
    reg2 = get_registry()
    assert reg1 is reg2


def test_list_releases_count():
    reg = get_registry()
    releases = reg.list_releases()
    assert len(releases) == 13


def test_get_release_169():
    reg = get_registry()
    entry = reg.get_release("1.6.9")
    assert entry is not None
    assert entry["version"] == "1.6.9"


def test_get_release_nonexistent():
    reg = get_registry()
    assert reg.get_release("9.9.9") is None


def test_get_parent_release_169():
    reg = get_registry()
    parent = reg.get_parent_release("1.6.9")
    assert parent is not None
    assert parent["version"] == "1.6.8"


def test_get_parent_release_root():
    reg = get_registry()
    parent = reg.get_parent_release("1.6.0")
    assert parent is None


def test_get_children_160():
    reg = get_registry()
    children = reg.get_children("1.6.0")
    assert len(children) >= 1
    assert any(c["version"] == "1.6.1" for c in children)


def test_validate_release_169():
    reg = get_registry()
    result = reg.validate_release("1.6.9")
    assert result["valid"] is True
    assert result["issues"] == []


def test_validate_release_nonexistent():
    reg = get_registry()
    result = reg.validate_release("9.9.9")
    assert result["valid"] is False


def test_validate_parent_chain():
    reg = get_registry()
    result = reg.validate_parent_chain()
    assert result["status"] == "PASS"
    assert result["issues"] == []


def test_validate_unique_versions():
    reg = get_registry()
    result = reg.validate_unique_versions()
    assert result["status"] == "PASS"
    assert result["duplicates"] == []


def test_validate_unique_commits():
    reg = get_registry()
    result = reg.validate_unique_commits()
    assert result["status"] == "PASS"


def test_validate_sealed_status():
    reg = get_registry()
    result = reg.validate_sealed_status()
    assert result["status"] == "PASS"


def test_release_summary():
    reg = get_registry()
    summary = reg.release_summary()
    assert isinstance(summary, dict)
    assert summary["total"] == 13
    assert "versions" in summary


def test_register_duplicate_raises():
    reg = ReleaseRegistry()
    with pytest.raises(ValueError, match="Duplicate version"):
        reg.register_release({"version": "1.6.9", "release_name": "Duplicate"})


def test_register_new_release():
    reg = ReleaseRegistry()
    reg.register_release({
        "version": "1.7.0",
        "release_name": "Future Release",
        "release_category": "test",
        "parent_version": "1.6.9",
        "commit": "test123",
        "sealed_status": "NOT_SEALED",
    })
    assert reg.get_release("1.7.0") is not None
