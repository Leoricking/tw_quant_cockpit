"""
tests/test_stable_rollup_snapshot_v169.py
Snapshot tests for Live Paper Trading Stable Rollup v1.6.9.
"""
import pytest
from paper_trading.stable_rollup.stable_snapshot_v169 import (
    StableSnapshot, CURRENT_SNAPSHOT, VERSION, RELEASE_NAME,
)
from paper_trading.stable_rollup.enums_v169 import RollupStatus, SealStatus
from paper_trading.stable_rollup.models_v169 import StableRollupSnapshot


def test_module_importable():
    import paper_trading.stable_rollup.stable_snapshot_v169
    assert True


def test_version_is_169():
    assert VERSION == "1.6.9"


def test_release_name():
    assert RELEASE_NAME == "Live Paper Trading Stable Rollup"


def test_current_snapshot_exists():
    assert isinstance(CURRENT_SNAPSHOT, dict)


def test_current_snapshot_version():
    assert CURRENT_SNAPSHOT["release_version"] == "1.6.9"


def test_current_snapshot_schema_version():
    assert CURRENT_SNAPSHOT["schema_version"] == "169"


def test_current_snapshot_policy_version():
    assert CURRENT_SNAPSHOT["policy_version"] == "1.6.9-live-paper-stable-rollup"


def test_current_snapshot_paper_only():
    assert CURRENT_SNAPSHOT["paper_only"] is True


def test_current_snapshot_research_only():
    assert CURRENT_SNAPSHOT["research_only"] is True


def test_current_snapshot_no_real_orders():
    assert CURRENT_SNAPSHOT["no_real_orders"] is True


def test_current_snapshot_not_for_production():
    assert CURRENT_SNAPSHOT["not_for_production"] is True


def test_current_snapshot_read_only():
    assert CURRENT_SNAPSHOT["read_only"] is True


def test_current_snapshot_rollup_status_ready():
    assert CURRENT_SNAPSHOT["rollup_status"] == "READY"


def test_current_snapshot_total_releases():
    assert CURRENT_SNAPSHOT["total_releases"] == 13


def test_current_snapshot_component_count():
    assert CURRENT_SNAPSHOT["component_count"] == 32


def test_current_snapshot_capability_count():
    assert CURRENT_SNAPSHOT["capability_count"] == 20


def test_current_snapshot_safety_items():
    assert CURRENT_SNAPSHOT["safety_items"] == 20


def test_current_snapshot_compatibility_edges():
    assert CURRENT_SNAPSHOT["compatibility_edges"] == 11


def test_stable_snapshot_instantiable():
    s = StableSnapshot()
    assert s is not None


def test_take_returns_snapshot_object():
    s = StableSnapshot()
    snap = s.take()
    assert isinstance(snap, StableRollupSnapshot)


def test_take_snapshot_version():
    s = StableSnapshot()
    snap = s.take()
    assert snap.release_version == "1.6.9"


def test_take_snapshot_paper_only():
    s = StableSnapshot()
    snap = s.take()
    assert snap.paper_only is True


def test_take_snapshot_no_real_orders():
    s = StableSnapshot()
    snap = s.take()
    assert snap.no_real_orders is True


def test_take_snapshot_not_for_production():
    s = StableSnapshot()
    snap = s.take()
    assert snap.not_for_production is True


def test_take_snapshot_schema_version():
    s = StableSnapshot()
    snap = s.take()
    assert snap.schema_version == "169"


def test_take_snapshot_policy_version():
    s = StableSnapshot()
    snap = s.take()
    assert snap.policy_version == "1.6.9-live-paper-stable-rollup"


def test_take_snapshot_has_id():
    s = StableSnapshot()
    snap = s.take()
    assert snap.snapshot_id != ""
    assert "1.6.9" in snap.snapshot_id


def test_take_default_rollup_status():
    s = StableSnapshot()
    snap = s.take()
    assert snap.rollup_status == RollupStatus.READY


def test_take_default_seal_status():
    s = StableSnapshot()
    snap = s.take()
    assert snap.seal_status == SealStatus.NOT_SEALED


def test_take_custom_rollup_status():
    s = StableSnapshot()
    snap = s.take(rollup_status=RollupStatus.COMPLETE)
    assert snap.rollup_status == RollupStatus.COMPLETE


def test_validate_snapshot_valid():
    s = StableSnapshot()
    snap = s.take()
    result = s.validate_snapshot(snap)
    assert result["valid"] is True
    assert len(result["issues"]) == 0


def test_validate_snapshot_returns_dict():
    s = StableSnapshot()
    snap = s.take()
    result = s.validate_snapshot(snap)
    assert isinstance(result, dict)
    assert "valid" in result
    assert "issues" in result
    assert "snapshot_id" in result


def test_validate_snapshot_wrong_version():
    s = StableSnapshot()
    snap = s.take()
    snap.release_version = "1.6.0"
    result = s.validate_snapshot(snap)
    assert result["valid"] is False
    assert len(result["issues"]) > 0
