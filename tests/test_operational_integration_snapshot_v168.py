"""
tests/test_operational_integration_snapshot_v168.py — State Snapshot Manager tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.state_snapshot_v168 import (
    StateSnapshotManager, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import IntegrationSnapshot
from paper_trading.operational_integration.enums_v168 import SnapshotType


class TestSnapshotSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestStateSnapshotManagerCore:
    def setup_method(self):
        self.manager = StateSnapshotManager()

    def test_take_snapshot_returns_snapshot(self):
        snap = self.manager.take_snapshot("R001", {"comp": "val"})
        assert isinstance(snap, IntegrationSnapshot)

    def test_take_snapshot_paper_only(self):
        snap = self.manager.take_snapshot("R001", {"comp": "val"})
        assert snap.paper_only is True

    def test_take_snapshot_run_id(self):
        snap = self.manager.take_snapshot("MY_RUN", {"comp": "val"})
        assert snap.run_id == "MY_RUN"

    def test_take_snapshot_components_stored(self):
        components = {"market_data": "active", "session": "ready"}
        snap = self.manager.take_snapshot("R001", components)
        assert snap.components == components

    def test_take_snapshot_default_full_type(self):
        snap = self.manager.take_snapshot("R001", {})
        assert snap.snapshot_type == SnapshotType.FULL

    def test_take_snapshot_partial_type(self):
        snap = self.manager.take_snapshot("R001", {}, snapshot_type=SnapshotType.PARTIAL)
        assert snap.snapshot_type == SnapshotType.PARTIAL

    def test_take_snapshot_id_generated(self):
        snap = self.manager.take_snapshot("R001", {})
        assert snap.snapshot_id is not None
        assert len(snap.snapshot_id) > 0

    def test_restore_snapshot_returns_snapshot(self):
        snap = self.manager.take_snapshot("R001", {"comp": "val"})
        restored = self.manager.restore_snapshot(snap.snapshot_id)
        assert restored is not None
        assert restored.snapshot_id == snap.snapshot_id

    def test_restore_snapshot_missing_returns_none(self):
        result = self.manager.restore_snapshot("NONEXISTENT_SNAP")
        assert result is None

    def test_list_snapshots_returns_list(self):
        self.manager.take_snapshot("R001", {"comp": "val"})
        snaps = self.manager.list_snapshots()
        assert isinstance(snaps, list)
        assert len(snaps) > 0

    def test_list_snapshots_has_snapshot_id(self):
        snap = self.manager.take_snapshot("R001", {})
        snaps = self.manager.list_snapshots()
        ids = [s["snapshot_id"] for s in snaps]
        assert snap.snapshot_id in ids

    def test_list_snapshots_has_run_id(self):
        self.manager.take_snapshot("MY_RUN_LIST", {})
        snaps = self.manager.list_snapshots()
        assert any(s.get("run_id") == "MY_RUN_LIST" for s in snaps)

    def test_compare_snapshots_identical(self):
        comp = {"comp_a": "val1", "comp_b": "val2"}
        snap1 = self.manager.take_snapshot("R001", comp)
        snap2 = self.manager.take_snapshot("R001", comp.copy())
        result = self.manager.compare_snapshots(snap1.snapshot_id, snap2.snapshot_id)
        assert result["identical"] is True

    def test_compare_snapshots_different(self):
        snap1 = self.manager.take_snapshot("R001", {"comp": "val1"})
        snap2 = self.manager.take_snapshot("R001", {"comp": "val2"})
        result = self.manager.compare_snapshots(snap1.snapshot_id, snap2.snapshot_id)
        assert result["identical"] is False
        assert "comp" in result["changed_components"]

    def test_compare_snapshots_missing_first(self):
        snap2 = self.manager.take_snapshot("R001", {})
        result = self.manager.compare_snapshots("MISSING_SNAP", snap2.snapshot_id)
        assert "error" in result

    def test_compare_snapshots_missing_second(self):
        snap1 = self.manager.take_snapshot("R001", {})
        result = self.manager.compare_snapshots(snap1.snapshot_id, "MISSING_SNAP")
        assert "error" in result

    def test_multiple_snapshots_same_run(self):
        for i in range(3):
            self.manager.take_snapshot("R_MULTI", {"comp": f"val{i}"})
        snaps = self.manager.list_snapshots()
        multi_snaps = [s for s in snaps if s.get("run_id") == "R_MULTI"]
        assert len(multi_snaps) == 3

    def test_snapshot_not_for_production(self):
        snap = self.manager.take_snapshot("R001", {})
        assert snap.not_for_production is True

    def test_compare_snapshots_paper_only(self):
        snap1 = self.manager.take_snapshot("R001", {"x": 1})
        snap2 = self.manager.take_snapshot("R001", {"x": 1})
        result = self.manager.compare_snapshots(snap1.snapshot_id, snap2.snapshot_id)
        assert result.get("paper_only") is True
