"""
tests/test_operational_integration_models_v168.py — Model tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.models_v168 import (
    IntegrationContext, IntegrationContract, ComponentDescriptor,
    DataFlowRecord, LineageRecord, IntegrationFailure, IntegrationScore,
    IntegrationSnapshot, IntegrationRun, ReconciliationResult,
    DeterminismResult, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.enums_v168 import (
    IntegrationMode, IntegrationStatus, IntegrationStage,
    FailureSeverity, FailureDomain, ReconciliationStatus, SnapshotType,
    DeterminismStatus,
)


class TestModelSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIntegrationContext:
    def test_create_context(self):
        ctx = IntegrationContext(
            run_id="R001",
            session_id="S001",
            component_id="market_data",
            period_start="2026-01-02",
            period_end="2026-01-03",
        )
        assert ctx.run_id == "R001"
        assert ctx.paper_only is True

    def test_context_default_mode(self):
        ctx = IntegrationContext(
            run_id="R001", session_id="S001", component_id="c1",
            period_start="2026-01-02", period_end="2026-01-03",
        )
        assert ctx.mode == IntegrationMode.RESEARCH_ONLY

    def test_context_reversed_period_raises(self):
        with pytest.raises(ValueError):
            IntegrationContext(
                run_id="R001", session_id="S001", component_id="c1",
                period_start="2026-01-03", period_end="2026-01-02",
            )

    def test_context_research_only_flag(self):
        ctx = IntegrationContext(
            run_id="R001", session_id="S001", component_id="c1",
            period_start="2026-01-02", period_end="2026-01-03",
        )
        assert ctx.research_only is True
        assert ctx.no_real_orders is True


class TestIntegrationContract:
    def test_create_contract(self):
        c = IntegrationContract(
            contract_id="C001",
            from_component="market_data",
            to_component="session",
            contract_version="1.6.8",
        )
        assert c.paper_only is True
        assert c.deterministic is True

    def test_contract_default_schema(self):
        c = IntegrationContract(
            contract_id="C001", from_component="A", to_component="B",
            contract_version="1.6.8",
        )
        assert c.schema_version == "1.6.8"


class TestComponentDescriptor:
    def test_create_descriptor(self):
        d = ComponentDescriptor(
            component_id="market_data_session",
            component_name="Market Data Session",
            component_version="1.6.1",
        )
        assert d.paper_only is True
        assert d.research_only is True

    def test_descriptor_capabilities_default_empty(self):
        d = ComponentDescriptor(
            component_id="c1", component_name="C1", component_version="1.0",
        )
        assert isinstance(d.capabilities, list)


class TestIntegrationFailure:
    def test_create_failure(self):
        f = IntegrationFailure(
            failure_id="F001",
            component_id="market_data",
            stage=IntegrationStage.CONTRACT_VALIDATE,
            domain=FailureDomain.CONTRACT,
            severity=FailureSeverity.HIGH,
            message="Contract validation failed",
        )
        assert f.paper_only is True
        assert f.failure_id == "F001"

    def test_failure_not_recoverable_by_default(self):
        f = IntegrationFailure(
            failure_id="F002", component_id="c1",
            stage=IntegrationStage.STAGE_VALIDATE,
            domain=FailureDomain.UNKNOWN,
            severity=FailureSeverity.MEDIUM,
            message="test",
        )
        assert f.recoverable is False


class TestReconciliationResult:
    def test_create_reconciliation(self):
        r = ReconciliationResult(
            reconciliation_id="RC001",
            component_id="reconciler",
            dimension="pnl",
            expected=100.0,
            actual=100.0,
            residual=0.0,
            tolerance=1e-6,
            status=ReconciliationStatus.RECONCILED,
        )
        assert r.paper_only is True
        assert r.status == ReconciliationStatus.RECONCILED


class TestIntegrationScore:
    def test_create_score(self):
        s = IntegrationScore(run_id="R001", total_score=95.0, grade="A")
        assert s.not_for_real_trading is True
        assert s.paper_only is True

    def test_score_not_for_real_trading(self):
        s = IntegrationScore(run_id="R001", total_score=80.0)
        assert s.not_for_real_trading is True


class TestIntegrationSnapshot:
    def test_create_snapshot(self):
        snap = IntegrationSnapshot(
            snapshot_id="SNAP001",
            run_id="R001",
            snapshot_type=SnapshotType.FULL,
        )
        assert snap.paper_only is True
        assert snap.snapshot_type == SnapshotType.FULL

    def test_snapshot_components_default_empty(self):
        snap = IntegrationSnapshot(
            snapshot_id="SNAP001", run_id="R001", snapshot_type=SnapshotType.FULL,
        )
        assert isinstance(snap.components, dict)
