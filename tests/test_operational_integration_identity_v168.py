"""
tests/test_operational_integration_identity_v168.py — Identity Bridge tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.identity_bridge_v168 import (
    IdentityBridge, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.enums_v168 import IdentityStatus


class TestIdentitySafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIdentityBridgeCore:
    def setup_method(self):
        self.bridge = IdentityBridge()

    def test_register_returns_record(self):
        rec = self.bridge.register(
            entity_type="session",
            entity_id="S001",
            component_id="market_data_session",
            session_id="SESS_001",
        )
        assert rec is not None

    def test_register_paper_only(self):
        rec = self.bridge.register(
            entity_type="strategy",
            entity_id="STRAT_001",
            component_id="paper_strategy",
            session_id="SESS_001",
        )
        assert rec.paper_only is True

    def test_register_status_valid(self):
        rec = self.bridge.register(
            entity_type="portfolio",
            entity_id="PORT_001",
            component_id="portfolio_research",
            session_id="SESS_001",
        )
        assert rec.status == IdentityStatus.VALID

    def test_check_duplicates_no_dups(self):
        self.bridge.register("session", "S001", "comp1", "sess1")
        self.bridge.register("strategy", "T001", "comp2", "sess2")
        dups = self.bridge.check_duplicates("session")
        assert isinstance(dups, list)

    def test_check_duplicates_detects_dup(self):
        self.bridge.register("session", "S001", "comp1", "sess1")
        self.bridge.register("session", "S001", "comp1", "sess1")
        dups = self.bridge.check_duplicates("session")
        assert len(dups) > 0

    def test_check_missing_all_found(self):
        rec = self.bridge.register("portfolio", "P001", "comp1", "sess1")
        missing = self.bridge.check_missing([], "portfolio")
        assert missing == []

    def test_check_conflicts_empty(self):
        conflicts = self.bridge.check_conflicts("session")
        assert isinstance(conflicts, list)

    def test_check_session_collision_no_overlap(self):
        self.bridge.register("strategy", "S1", "comp_a", "sess_A")
        self.bridge.register("strategy", "S2", "comp_b", "sess_B")
        result = self.bridge.check_session_collision("sess_A", "sess_B")
        assert result is False

    def test_check_session_collision_with_overlap(self):
        self.bridge.register("strategy", "S1", "comp_shared", "sess_X")
        self.bridge.register("strategy", "S2", "comp_shared", "sess_Y")
        result = self.bridge.check_session_collision("sess_X", "sess_Y")
        assert result is True

    def test_normalize_symbol_basic(self):
        result = self.bridge.normalize_symbol("2330.TW")
        assert isinstance(result, str)

    def test_summarize_returns_dict(self):
        self.bridge.register("session", "S001", "c1", "sess1")
        result = self.bridge.summarize()
        assert isinstance(result, dict)

    def test_summarize_paper_only(self):
        self.bridge.register("strategy", "T001", "c1", "sess1")
        result = self.bridge.summarize()
        assert result.get("paper_only") is True

    def test_identity_id_format(self):
        rec = self.bridge.register("session", "S001", "comp_x", "sess_x")
        assert "session" in rec.identity_id

    def test_no_real_orders_on_record(self):
        rec = self.bridge.register("strategy", "T001", "c1", "sess1")
        assert rec.no_real_orders is True

    def test_register_multiple_entity_types(self):
        self.bridge.register("session", "S001", "c1", "sess1")
        self.bridge.register("strategy", "T001", "c2", "sess1")
        self.bridge.register("portfolio", "P001", "c3", "sess1")
        assert len(self.bridge._records) == 3

    def test_entity_index_populated(self):
        self.bridge.register("test_type", "E001", "comp1", "sess1")
        assert "test_type" in self.bridge._entity_index

    def test_not_for_production_on_record(self):
        rec = self.bridge.register("portfolio", "P001", "c1", "sess1")
        assert rec.not_for_production is True

    def test_session_id_stored(self):
        rec = self.bridge.register("session", "S001", "comp1", "my_session")
        assert rec.session_id == "my_session"

    def test_component_id_stored(self):
        rec = self.bridge.register("strategy", "T001", "my_component", "sess1")
        assert rec.component_id == "my_component"
