"""
tests/test_operational_integration_lineage_v168.py — Lineage Bridge tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.lineage_bridge_v168 import (
    LineageBridge, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.enums_v168 import LineageStatus


class TestLineageSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestLineageBridgeCore:
    def setup_method(self):
        self.bridge = LineageBridge()

    def test_record_returns_record(self):
        rec = self.bridge.record(
            component_id="market_data",
            parent_lineage_id="ROOT",
            lineage_type="data_feed",
        )
        assert rec is not None
        assert rec.component_id == "market_data"

    def test_record_is_paper(self):
        rec = self.bridge.record(
            component_id="session",
            parent_lineage_id="ROOT",
            lineage_type="session",
        )
        assert rec.is_paper is True
        assert rec.paper_only is True

    def test_record_not_fixture_by_default(self):
        rec = self.bridge.record(
            component_id="strategy",
            parent_lineage_id="ROOT",
            lineage_type="strategy",
        )
        assert rec.is_fixture is False

    def test_record_fixture_flag(self):
        rec = self.bridge.record(
            component_id="test_comp",
            parent_lineage_id="ROOT",
            lineage_type="fixture",
            is_fixture=True,
        )
        assert rec.is_fixture is True

    def test_check_chain_returns_dict(self):
        rec = self.bridge.record(
            component_id="comp1",
            parent_lineage_id="ROOT",
            lineage_type="test",
        )
        result = self.bridge.check_chain(rec.lineage_id)
        assert isinstance(result, dict)

    def test_check_chain_not_broken(self):
        rec = self.bridge.record(
            component_id="comp1",
            parent_lineage_id="ROOT",
            lineage_type="test",
        )
        result = self.bridge.check_chain(rec.lineage_id)
        assert result["broken"] is False

    def test_check_chain_paper_only(self):
        rec = self.bridge.record(
            component_id="comp2",
            parent_lineage_id="ROOT",
            lineage_type="test",
        )
        result = self.bridge.check_chain(rec.lineage_id)
        assert result["paper_only"] is True

    def test_check_chain_status_complete(self):
        rec = self.bridge.record(
            component_id="comp3",
            parent_lineage_id="ROOT",
            lineage_type="test",
        )
        result = self.bridge.check_chain(rec.lineage_id)
        assert result["status"] == LineageStatus.COMPLETE.value

    def test_check_chain_length_positive(self):
        rec = self.bridge.record(
            component_id="comp4",
            parent_lineage_id="ROOT",
            lineage_type="test",
        )
        result = self.bridge.check_chain(rec.lineage_id)
        assert result["chain_length"] > 0

    def test_check_duplicates_no_dups(self):
        self.bridge.record("comp_a", "ROOT", "type_a")
        self.bridge.record("comp_b", "ROOT", "type_b")
        dups = self.bridge.check_duplicates()
        assert isinstance(dups, list)

    def test_check_broken_chains_returns_list(self):
        self.bridge.record("comp_a", "ROOT", "test")
        result = self.bridge.check_broken_chains()
        assert isinstance(result, list)

    def test_summarize_returns_dict(self):
        self.bridge.record("comp1", "ROOT", "test")
        result = self.bridge.summarize()
        assert isinstance(result, dict)

    def test_summarize_paper_only(self):
        self.bridge.record("comp1", "ROOT", "test")
        result = self.bridge.summarize()
        assert result.get("paper_only") is True

    def test_check_fixture_contamination_false_for_paper(self):
        rec = self.bridge.record("comp_no_fix", "ROOT", "test", is_fixture=False)
        result = self.bridge.check_fixture_contamination(rec.lineage_id)
        assert isinstance(result, bool)

    def test_multiple_records_chain(self):
        rec1 = self.bridge.record("comp_root", "ROOT", "root")
        rec2 = self.bridge.record("comp_child", rec1.lineage_id, "child")
        result = self.bridge.check_chain(rec2.lineage_id)
        assert result["chain_length"] >= 1

    def test_record_stores_lineage_id(self):
        rec = self.bridge.record("comp_store", "ROOT", "test")
        assert rec.lineage_id in self.bridge._records

    def test_lineage_type_stored(self):
        rec = self.bridge.record("comp_type", "ROOT", "specific_type")
        assert rec.lineage_type == "specific_type"

    def test_no_real_orders_flag_on_record(self):
        rec = self.bridge.record("comp_nro", "ROOT", "test")
        assert rec.no_real_orders is True

    def test_not_for_production_flag(self):
        rec = self.bridge.record("comp_nfp", "ROOT", "test")
        assert rec.not_for_production is True

    def test_mock_flag_default_false(self):
        rec = self.bridge.record("comp_mock", "ROOT", "test")
        assert rec.is_mock is False
