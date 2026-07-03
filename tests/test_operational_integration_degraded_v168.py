"""
tests/test_operational_integration_degraded_v168.py — Degraded Mode Handler tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from datetime import datetime, timezone, timedelta

from paper_trading.operational_integration.degraded_mode_v168 import (
    DegradedModeHandler, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import DegradedState
from paper_trading.operational_integration.enums_v168 import DegradedReason, FailureSeverity


class TestDegradedSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestDegradedModeHandlerCore:
    def setup_method(self):
        self.handler = DegradedModeHandler()

    def test_check_stale_market_data_returns_state(self):
        state = self.handler.check_stale_market_data({
            "component_id": "market_data",
            "last_update": "2020-01-01T00:00:00Z",
            "max_age_seconds": 3600,
        })
        assert isinstance(state, DegradedState)

    def test_check_stale_market_data_stale(self):
        state = self.handler.check_stale_market_data({
            "component_id": "market_data",
            "last_update": "2020-01-01T00:00:00Z",
            "max_age_seconds": 3600,
        })
        assert DegradedReason.STALE_MARKET_DATA in state.reasons

    def test_check_stale_market_data_fresh(self):
        recent = (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat()
        state = self.handler.check_stale_market_data({
            "component_id": "market_data",
            "last_update": recent,
            "max_age_seconds": 3600,
        })
        assert DegradedReason.STALE_MARKET_DATA not in state.reasons

    def test_check_stale_market_data_paper_only(self):
        state = self.handler.check_stale_market_data({
            "component_id": "market_data",
            "last_update": "2020-01-01T00:00:00Z",
        })
        assert state.paper_only is True

    def test_can_upgrade_to_complete_no_reasons(self):
        state = DegradedState(component_id="c1", reasons=[])
        assert self.handler.can_upgrade_to_complete(state) is True

    def test_can_upgrade_to_complete_with_reasons(self):
        state = DegradedState(
            component_id="c1",
            reasons=[DegradedReason.STALE_MARKET_DATA],
        )
        assert self.handler.can_upgrade_to_complete(state) is False

    def test_check_missing_benchmark_missing(self):
        state = self.handler.check_missing_benchmark({
            "component_id": "attribution",
        })
        assert DegradedReason.MISSING_BENCHMARK in state.reasons

    def test_check_missing_benchmark_present(self):
        state = self.handler.check_missing_benchmark({
            "component_id": "attribution",
            "benchmark_return": 0.05,
        })
        assert DegradedReason.MISSING_BENCHMARK not in state.reasons

    def test_check_partial_execution_partial(self):
        executions = [{"status": "PARTIAL_FILL"}, {"status": "FILLED"}]
        state = self.handler.check_partial_execution(executions)
        assert DegradedReason.PARTIAL_EXECUTION in state.reasons

    def test_check_partial_execution_all_filled(self):
        executions = [{"status": "FILLED"}, {"status": "FILLED"}]
        state = self.handler.check_partial_execution(executions)
        assert DegradedReason.PARTIAL_EXECUTION not in state.reasons

    def test_propagate_returns_state(self):
        upstream = DegradedState(
            component_id="upstream",
            reasons=[DegradedReason.STALE_MARKET_DATA],
        )
        downstream = self.handler.propagate(upstream, "downstream_comp")
        assert isinstance(downstream, DegradedState)
        assert downstream.component_id == "downstream_comp"

    def test_propagate_empty_reasons(self):
        upstream = DegradedState(component_id="upstream", reasons=[])
        downstream = self.handler.propagate(upstream, "downstream_comp")
        assert downstream.reasons == []

    def test_summarize_returns_dict(self):
        states = [
            DegradedState(component_id="c1", reasons=[DegradedReason.STALE_MARKET_DATA]),
            DegradedState(component_id="c2", reasons=[]),
        ]
        summary = self.handler.summarize(states)
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        summary = self.handler.summarize([])
        assert summary.get("paper_only") is True

    def test_check_incomplete_lineage_broken(self):
        state = self.handler.check_incomplete_lineage({
            "component_id": "lineage",
            "chain_complete": False,
            "broken": True,
        })
        assert DegradedReason.INCOMPLETE_LINEAGE in state.reasons

    def test_check_incomplete_lineage_complete(self):
        state = self.handler.check_incomplete_lineage({
            "component_id": "lineage",
            "chain_complete": True,
            "broken": False,
        })
        assert DegradedReason.INCOMPLETE_LINEAGE not in state.reasons

    def test_degraded_state_paper_only_default(self):
        state = DegradedState(component_id="test")
        assert state.paper_only is True
