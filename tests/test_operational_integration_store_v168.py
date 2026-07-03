"""
tests/test_operational_integration_store_v168.py — Integration Store tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_store_v168 import (
    IntegrationStore, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import (
    IntegrationRun, IntegrationSnapshot,
)
from paper_trading.operational_integration.enums_v168 import (
    IntegrationMode, IntegrationStatus, SnapshotType,
)


def _make_run(run_id: str = "R001", session_id: str = "S001"):
    return IntegrationRun(
        run_id=run_id,
        session_id=session_id,
        mode=IntegrationMode.RESEARCH_ONLY,
        status=IntegrationStatus.COMPLETE,
    )


def _make_snapshot(snapshot_id: str = "SNAP001", run_id: str = "R001"):
    return IntegrationSnapshot(
        snapshot_id=snapshot_id,
        run_id=run_id,
        snapshot_type=SnapshotType.FULL,
        components={"comp": "value"},
    )


class TestStoreSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIntegrationStoreCore:
    def setup_method(self):
        self.store = IntegrationStore()

    def test_save_run_returns_run_id(self):
        run = _make_run()
        run_id = self.store.save_run(run)
        assert run_id == "R001"

    def test_load_run_returns_run(self):
        run = _make_run("R_LOAD")
        self.store.save_run(run)
        loaded = self.store.load_run("R_LOAD")
        assert loaded is not None
        assert loaded.run_id == "R_LOAD"

    def test_load_run_missing_returns_none(self):
        loaded = self.store.load_run("NONEXISTENT_RUN")
        assert loaded is None

    def test_list_runs_returns_list(self):
        self.store.save_run(_make_run("R_LIST1"))
        self.store.save_run(_make_run("R_LIST2"))
        runs = self.store.list_runs()
        assert isinstance(runs, list)
        assert "R_LIST1" in runs
        assert "R_LIST2" in runs

    def test_save_snapshot_returns_id(self):
        snap = _make_snapshot("SNAP_SAVE")
        snap_id = self.store.save_snapshot(snap)
        assert snap_id == "SNAP_SAVE"

    def test_load_snapshot_returns_snapshot(self):
        snap = _make_snapshot("SNAP_LOAD")
        self.store.save_snapshot(snap)
        loaded = self.store.load_snapshot("SNAP_LOAD")
        assert loaded is not None
        assert loaded.snapshot_id == "SNAP_LOAD"

    def test_load_snapshot_missing_returns_none(self):
        loaded = self.store.load_snapshot("NONEXISTENT_SNAP")
        assert loaded is None

    def test_save_run_dict(self):
        run_dict = {"run_id": "R_DICT", "status": "COMPLETE", "paper_only": True}
        run_id = self.store.save_run_dict(run_dict)
        assert run_id == "R_DICT"

    def test_query_by_component_returns_list(self):
        run = _make_run("R_COMP")
        run.components = ["market_data_session"]
        self.store.save_run(run)
        results = self.store.query_by_component("market_data_session")
        assert isinstance(results, list)
        assert "R_COMP" in results

    def test_query_by_status_complete(self):
        run = _make_run("R_STATUS")
        self.store.save_run(run)
        results = self.store.query_by_status("COMPLETE")
        assert isinstance(results, list)
        assert "R_STATUS" in results

    def test_query_by_session_returns_list(self):
        run = _make_run("R_SESSION", "MY_SESSION")
        self.store.save_run(run)
        results = self.store.query_by_session("MY_SESSION")
        assert isinstance(results, list)
        assert "R_SESSION" in results

    def test_multiple_runs_stored(self):
        for i in range(5):
            self.store.save_run(_make_run(f"R_MULTI_{i}"))
        runs = self.store.list_runs()
        for i in range(5):
            assert f"R_MULTI_{i}" in runs

    def test_run_paper_only_preserved(self):
        run = _make_run("R_PAPER")
        self.store.save_run(run)
        loaded = self.store.load_run("R_PAPER")
        assert loaded.paper_only is True

    def test_snapshot_paper_only_preserved(self):
        snap = _make_snapshot("SNAP_PAPER")
        self.store.save_snapshot(snap)
        loaded = self.store.load_snapshot("SNAP_PAPER")
        assert loaded.paper_only is True

    def test_list_runs_sorted(self):
        self.store.save_run(_make_run("R_Z"))
        self.store.save_run(_make_run("R_A"))
        runs = self.store.list_runs()
        assert runs == sorted(runs)

    def test_run_status_complete(self):
        run = _make_run("R_STATUS_CHECK")
        self.store.save_run(run)
        loaded = self.store.load_run("R_STATUS_CHECK")
        assert loaded.status == IntegrationStatus.COMPLETE

    def test_save_run_dict_preserves_data(self):
        run_dict = {
            "run_id": "R_DICT_DATA",
            "status": "COMPLETE",
            "session_id": "SESS_001",
            "paper_only": True,
        }
        self.store.save_run_dict(run_dict)
        runs = self.store.list_runs()
        assert "R_DICT_DATA" in runs
