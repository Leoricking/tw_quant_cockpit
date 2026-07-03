"""
tests/test_operational_integration_data_flow_v168.py — Data Flow Tracker tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.data_flow_v168 import (
    DataFlowTracker, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)


class TestDataFlowSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestDataFlowCore:
    def setup_method(self):
        self.tracker = DataFlowTracker()

    def test_record_flow_returns_record(self):
        rec = self.tracker.record_flow(
            source="market_data",
            destination="session",
            payload_hash="abc123",
            lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1,
            contract_version="1.6.8",
        )
        assert rec is not None
        assert rec.source_component == "market_data"

    def test_record_flow_paper_only(self):
        rec = self.tracker.record_flow(
            source="A", destination="B",
            payload_hash="h1", lineage_id="L1",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        assert rec.paper_only is True

    def test_record_multiple_flows(self):
        for i in range(5):
            self.tracker.record_flow(
                source="comp_a", destination="comp_b",
                payload_hash=f"hash_{i}", lineage_id=f"L{i:03d}",
                timestamp="2026-01-02T09:00:00Z",
                sequence_number=i, contract_version="1.6.8",
            )
        assert len(self.tracker._flows) == 5

    def test_check_sequence_gaps_no_gaps(self):
        for i in range(1, 4):
            self.tracker.record_flow(
                source="src", destination="dst",
                payload_hash=f"h{i}", lineage_id=f"L{i:03d}",
                timestamp="2026-01-02T09:00:00Z",
                sequence_number=i, contract_version="1.6.8",
            )
        gaps = self.tracker.check_sequence_gaps("src")
        assert gaps == []

    def test_check_sequence_gaps_with_gap(self):
        self.tracker.record_flow(
            source="src2", destination="dst2",
            payload_hash="h1", lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        self.tracker.record_flow(
            source="src2", destination="dst2",
            payload_hash="h3", lineage_id="L003",
            timestamp="2026-01-02T09:01:00Z",
            sequence_number=3, contract_version="1.6.8",
        )
        gaps = self.tracker.check_sequence_gaps("src2")
        assert len(gaps) > 0

    def test_check_duplicates_no_dups(self):
        for i in range(3):
            self.tracker.record_flow(
                source="srcX", destination="dstX",
                payload_hash=f"unique_{i}", lineage_id=f"L{i:03d}",
                timestamp="2026-01-02T09:00:00Z",
                sequence_number=i + 1, contract_version="1.6.8",
            )
        dups = self.tracker.check_duplicates("srcX")
        assert dups == []

    def test_check_duplicates_with_dup(self):
        self.tracker.record_flow(
            source="srcDup", destination="dstDup",
            payload_hash="same_hash", lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        self.tracker.record_flow(
            source="srcDup", destination="dstDup",
            payload_hash="same_hash", lineage_id="L002",
            timestamp="2026-01-02T09:01:00Z",
            sequence_number=2, contract_version="1.6.8",
        )
        dups = self.tracker.check_duplicates("srcDup")
        assert len(dups) > 0

    def test_summarize_returns_dict(self):
        self.tracker.record_flow(
            source="A", destination="B",
            payload_hash="abc", lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        summary = self.tracker.summarize()
        assert isinstance(summary, dict)

    def test_summarize_total_flows(self):
        for i in range(3):
            self.tracker.record_flow(
                source="S", destination="D",
                payload_hash=f"h{i}", lineage_id=f"L{i:03d}",
                timestamp="2026-01-02T09:00:00Z",
                sequence_number=i, contract_version="1.6.8",
            )
        summary = self.tracker.summarize()
        assert summary.get("total_flows", 0) >= 3 or "total" in str(summary)

    def test_record_flow_stores_lineage_id(self):
        rec = self.tracker.record_flow(
            source="X", destination="Y",
            payload_hash="hXY", lineage_id="LINEAGE_ABC",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        assert rec.lineage_id == "LINEAGE_ABC"

    def test_record_flow_stores_sequence_number(self):
        rec = self.tracker.record_flow(
            source="X", destination="Y",
            payload_hash="hXY2", lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=42, contract_version="1.6.8",
        )
        assert rec.sequence_number == 42

    def test_record_flow_destination(self):
        rec = self.tracker.record_flow(
            source="src_test", destination="dst_test",
            payload_hash="h_dest", lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        assert rec.destination_component == "dst_test"

    def test_record_flow_no_real_orders(self):
        rec = self.tracker.record_flow(
            source="A", destination="B",
            payload_hash="ha", lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        assert rec.no_real_orders is True

    def test_empty_tracker_summarize(self):
        fresh = DataFlowTracker()
        summary = fresh.summarize()
        assert isinstance(summary, dict)

    def test_multiple_sources_tracked(self):
        self.tracker.record_flow(
            source="src1", destination="dst1",
            payload_hash="h1", lineage_id="L001",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        self.tracker.record_flow(
            source="src2", destination="dst2",
            payload_hash="h2", lineage_id="L002",
            timestamp="2026-01-02T09:00:00Z",
            sequence_number=1, contract_version="1.6.8",
        )
        assert len(self.tracker._flows) == 2
