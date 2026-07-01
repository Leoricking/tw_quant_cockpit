"""
test_multi_session_capital_risk_v166.py — Capital Risk tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _make_desc(name, capital=0.0, risk=0.0, symbols=None, strategies=None, session_id=None):
    from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
    return make_session_descriptor(
        name, "owner",
        capital_budget=capital,
        risk_budget=risk,
        symbols=symbols or [],
        strategies=strategies or [],
        session_id=session_id or name,
    )


class TestCapitalAllocator:
    def test_instantiation(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        ca = CapitalAllocator()
        assert ca is not None

    def test_allocate_returns_dict(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        ca = CapitalAllocator()
        s1 = _make_desc("s1", capital=100_000.0)
        result = ca.allocate([s1], global_paper_budget=1_000_000.0, rules={})
        assert isinstance(result, dict)

    def test_allocate_within_budget_passes(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        ca = CapitalAllocator()
        s1 = _make_desc("s1", capital=100_000.0)
        result = ca.allocate([s1], global_paper_budget=1_000_000.0, rules={})
        assert result["outcome"] == CoordinationOutcome.PASS.value

    def test_no_real_capital_movement_flag(self):
        import paper_trading.multi_session.capital_allocator_v166 as m
        assert m.NO_REAL_CAPITAL_MOVEMENT is True

    def test_paper_capital_only_flag(self):
        import paper_trading.multi_session.capital_allocator_v166 as m
        assert m.PAPER_CAPITAL_ONLY is True

    def test_allocate_over_budget_returns_block_or_warn(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        ca = CapitalAllocator()
        s1 = _make_desc("s1", capital=600_000.0)
        s2 = _make_desc("s2", capital=600_000.0)
        result = ca.allocate([s1, s2], global_paper_budget=500_000.0,
                             rules={"partial_grant_allowed": False})
        assert result["outcome"] in [CoordinationOutcome.BLOCK.value, CoordinationOutcome.WARN.value]

    def test_allocate_partial_grant_produces_warn(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        ca = CapitalAllocator()
        s1 = _make_desc("s1", capital=600_000.0)
        s2 = _make_desc("s2", capital=600_000.0)
        result = ca.allocate([s1, s2], global_paper_budget=500_000.0,
                             rules={"partial_grant_allowed": True})
        assert result["outcome"] == CoordinationOutcome.WARN.value

    def test_allocate_has_allocations_key(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        ca = CapitalAllocator()
        s1 = _make_desc("s1", capital=100_000.0)
        result = ca.allocate([s1], global_paper_budget=1_000_000.0, rules={})
        assert "allocations" in result

    def test_allocate_has_requested_key(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        ca = CapitalAllocator()
        s1 = _make_desc("s1", capital=100_000.0)
        result = ca.allocate([s1], global_paper_budget=1_000_000.0, rules={})
        assert result["requested"] == 100_000.0

    def test_allocate_empty_sessions(self):
        from paper_trading.multi_session.capital_allocator_v166 import CapitalAllocator
        ca = CapitalAllocator()
        result = ca.allocate([], global_paper_budget=1_000_000.0, rules={})
        assert result["requested"] == 0.0


class TestRiskAggregator:
    def test_instantiation(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        ra = RiskAggregator()
        assert ra is not None

    def test_aggregate_returns_dict(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        ra = RiskAggregator()
        result = ra.aggregate([], {})
        assert isinstance(result, dict)

    def test_aggregate_pass_on_empty_sessions(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        ra = RiskAggregator()
        result = ra.aggregate([], {"aggregate_gross_limit": 1.0})
        assert result["outcome"] == CoordinationOutcome.PASS.value

    def test_aggregate_pass_on_zero_risk(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        ra = RiskAggregator()
        s1 = _make_desc("s1", risk=0.0)
        result = ra.aggregate([s1], {"aggregate_gross_limit": 1.0})
        assert result["outcome"] == CoordinationOutcome.PASS.value

    def test_aggregate_has_outcome_key(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        ra = RiskAggregator()
        result = ra.aggregate([], {})
        assert "outcome" in result

    def test_aggregate_has_total_risk_budget_key(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        ra = RiskAggregator()
        result = ra.aggregate([], {})
        assert "total_risk_budget" in result

    def test_aggregate_blocks_on_excessive_risk(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        from paper_trading.multi_session.enums_v166 import CoordinationOutcome
        ra = RiskAggregator()
        s1 = _make_desc("s1", risk=200.0)
        result = ra.aggregate([s1], {"aggregate_gross_limit": 1.0})
        assert result["outcome"] == CoordinationOutcome.BLOCK.value

    def test_no_auto_risk_modification_flag(self):
        import paper_trading.multi_session.risk_aggregator_v166 as m
        assert m.NO_AUTO_RISK_MODIFICATION is True

    def test_aggregate_two_sessions_risk_summed(self):
        from paper_trading.multi_session.risk_aggregator_v166 import RiskAggregator
        ra = RiskAggregator()
        s1 = _make_desc("s1", risk=10.0)
        s2 = _make_desc("s2", risk=20.0)
        result = ra.aggregate([s1, s2], {"aggregate_gross_limit": 1.0})
        assert result["total_risk_budget"] == 30.0


class TestSymbolExposureCoordinator:
    def test_compute_returns_dict(self):
        from paper_trading.multi_session.symbol_exposure_v166 import SymbolExposureCoordinator
        sec = SymbolExposureCoordinator()
        result = sec.compute([])
        assert isinstance(result, dict)

    def test_compute_has_overlapping_key(self):
        from paper_trading.multi_session.symbol_exposure_v166 import SymbolExposureCoordinator
        sec = SymbolExposureCoordinator()
        result = sec.compute([])
        assert "overlapping" in result

    def test_compute_detects_overlap(self):
        from paper_trading.multi_session.symbol_exposure_v166 import SymbolExposureCoordinator
        sec = SymbolExposureCoordinator()
        s1 = _make_desc("s1", symbols=["2330"])
        s2 = _make_desc("s2", symbols=["2330"])
        result = sec.compute([s1, s2])
        assert "2330" in result["overlapping"]

    def test_detect_direction_conflict_returns_list(self):
        from paper_trading.multi_session.symbol_exposure_v166 import SymbolExposureCoordinator
        sec = SymbolExposureCoordinator()
        positions = {"s1": {"2330": "LONG"}, "s2": {"2330": "SHORT"}}
        conflicts = sec.detect_direction_conflict(positions)
        assert isinstance(conflicts, list)
        assert len(conflicts) == 1

    def test_detect_no_direction_conflict_same_direction(self):
        from paper_trading.multi_session.symbol_exposure_v166 import SymbolExposureCoordinator
        sec = SymbolExposureCoordinator()
        positions = {"s1": {"2330": "LONG"}, "s2": {"2330": "LONG"}}
        conflicts = sec.detect_direction_conflict(positions)
        assert conflicts == []

    def test_no_portfolio_ledger_writes_flag(self):
        import paper_trading.multi_session.symbol_exposure_v166 as m
        assert m.NO_PORTFOLIO_LEDGER_WRITES is True


class TestStrategyConflictDetector:
    def test_detect_returns_list(self):
        from paper_trading.multi_session.strategy_conflict_v166 import StrategyConflictDetector
        scd = StrategyConflictDetector()
        result = scd.detect([])
        assert isinstance(result, list)

    def test_detect_finds_duplicate_strategy(self):
        from paper_trading.multi_session.strategy_conflict_v166 import StrategyConflictDetector
        scd = StrategyConflictDetector()
        s1 = _make_desc("s1", strategies=["value"])
        s2 = _make_desc("s2", strategies=["value"])
        conflicts = scd.detect([s1, s2])
        assert len(conflicts) == 1
        assert conflicts[0]["type"] == "duplicate_strategy"

    def test_detect_no_conflict_unique_strategies(self):
        from paper_trading.multi_session.strategy_conflict_v166 import StrategyConflictDetector
        scd = StrategyConflictDetector()
        s1 = _make_desc("s1", strategies=["momentum"])
        s2 = _make_desc("s2", strategies=["value"])
        conflicts = scd.detect([s1, s2])
        dup = [c for c in conflicts if c["type"] == "duplicate_strategy"]
        assert len(dup) == 0

    def test_no_auto_strategy_change_flag(self):
        import paper_trading.multi_session.strategy_conflict_v166 as m
        assert m.NO_AUTO_STRATEGY_CHANGE is True
