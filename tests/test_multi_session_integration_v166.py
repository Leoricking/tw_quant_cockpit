"""
test_multi_session_integration_v166.py — Integration tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
import uuid
from datetime import datetime, timezone


def _make_desc(session_id="s1"):
    from paper_trading.multi_session.models_v166 import SessionDescriptor
    from paper_trading.multi_session.enums_v166 import SessionType, SessionPriority, SessionLifecycleState
    return SessionDescriptor(
        session_id=session_id,
        session_type=SessionType.PAPER,
        name=f"session_{session_id}",
        owner="test_owner",
        created_at=datetime.now(timezone.utc),
        registered_at=datetime.now(timezone.utc),
        lifecycle_state=SessionLifecycleState.REGISTERED,
        priority=SessionPriority.NORMAL,
        capabilities=["trading"],
        symbols=["2330"],
        strategies=["mean_reversion"],
        data_sources=["fixture"],
        resource_requirements={},
        risk_budget=0.05,
        capital_budget=100000.0,
        policy_version="1.6.6",
        code_version="1.6.6",
    )


def _make_policy():
    from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
    return make_default_policy()


def _make_context(sessions=None, seed=42):
    from paper_trading.multi_session.coordinator_v166 import CoordinationContext
    if sessions is None:
        sessions = [_make_desc()]
    return CoordinationContext(
        sessions=sessions,
        policy=_make_policy(),
        virtual_clock=datetime.now(timezone.utc),
        seed=seed,
    )


class TestCoordinatorIntegration:
    def test_coordinator_instantiation(self):
        from paper_trading.multi_session.coordinator_v166 import MultiSessionCoordinator
        c = MultiSessionCoordinator()
        assert c is not None

    def test_coordinate_with_context_returns_result(self):
        from paper_trading.multi_session.coordinator_v166 import MultiSessionCoordinator
        from paper_trading.multi_session.models_v166 import CoordinationResult
        c = MultiSessionCoordinator()
        ctx = _make_context()
        result = c.coordinate(ctx)
        assert isinstance(result, CoordinationResult)

    def test_coordinate_result_has_coordination_id(self):
        from paper_trading.multi_session.coordinator_v166 import MultiSessionCoordinator
        c = MultiSessionCoordinator()
        ctx = _make_context()
        result = c.coordinate(ctx)
        assert result.coordination_id

    def test_coordinate_sessions_considered_populated(self):
        from paper_trading.multi_session.coordinator_v166 import MultiSessionCoordinator
        c = MultiSessionCoordinator()
        ctx = _make_context([_make_desc("s1"), _make_desc("s2")])
        result = c.coordinate(ctx)
        assert len(result.sessions_considered) == 2

    def test_coordinate_reproducibility_hash_set(self):
        from paper_trading.multi_session.coordinator_v166 import MultiSessionCoordinator
        c = MultiSessionCoordinator()
        ctx = _make_context()
        result = c.coordinate(ctx)
        assert result.reproducibility_hash

    def test_get_decisions_returns_list(self):
        from paper_trading.multi_session.coordinator_v166 import MultiSessionCoordinator
        c = MultiSessionCoordinator()
        ctx = _make_context()
        c.coordinate(ctx)
        decisions = c.get_decisions()
        assert isinstance(decisions, list)


class TestReproducibility:
    def test_compute_input_hash_deterministic(self):
        from paper_trading.multi_session.reproducibility_v166 import compute_input_hash
        h1 = compute_input_hash(["s1", "s2"], "policy_v1", "2026-01-01T00:00:00", 42)
        h2 = compute_input_hash(["s1", "s2"], "policy_v1", "2026-01-01T00:00:00", 42)
        assert h1 == h2

    def test_compute_output_hash_deterministic(self):
        from paper_trading.multi_session.reproducibility_v166 import compute_output_hash
        h1 = compute_output_hash(["s1"], [], 0, {"status": "ok"})
        h2 = compute_output_hash(["s1"], [], 0, {"status": "ok"})
        assert h1 == h2

    def test_compute_input_hash_returns_string(self):
        from paper_trading.multi_session.reproducibility_v166 import compute_input_hash
        h = compute_input_hash(["s1"], "policy", "2026-01-01", 1)
        assert isinstance(h, str)

    def test_compute_output_hash_returns_string(self):
        from paper_trading.multi_session.reproducibility_v166 import compute_output_hash
        h = compute_output_hash([], [], 0, {})
        assert isinstance(h, str)

    def test_different_seeds_produce_different_hashes(self):
        from paper_trading.multi_session.reproducibility_v166 import compute_input_hash
        h1 = compute_input_hash(["s1"], "p", "2026-01-01", 1)
        h2 = compute_input_hash(["s1"], "p", "2026-01-01", 2)
        assert h1 != h2

    def test_validate_reproducibility_match(self):
        from paper_trading.multi_session.reproducibility_v166 import compute_output_hash, validate_reproducibility
        h = compute_output_hash(["s1"], [], 0, {})
        result = validate_reproducibility("input_hash", h, h)
        assert result["reproducible"] is True


class TestLineage:
    def test_record_returns_lineage_node(self):
        from paper_trading.multi_session.lineage_v166 import CoordinationLineage, LineageNode
        lin = CoordinationLineage()
        node = lin.record("coordination_start", ["s1"])
        assert isinstance(node, LineageNode)

    def test_all_nodes_returns_list(self):
        from paper_trading.multi_session.lineage_v166 import CoordinationLineage
        lin = CoordinationLineage()
        lin.record("ev1", ["s1"])
        nodes = lin.all_nodes()
        assert isinstance(nodes, list)
        assert len(nodes) == 1

    def test_get_chain_returns_list(self):
        from paper_trading.multi_session.lineage_v166 import CoordinationLineage
        lin = CoordinationLineage()
        node = lin.record("ev1", ["s1"])
        chain = lin.get_chain(node.node_id)
        assert isinstance(chain, list)

    def test_is_complete_returns_bool(self):
        from paper_trading.multi_session.lineage_v166 import CoordinationLineage
        lin = CoordinationLineage()
        node = lin.record("ev1", ["s1"])
        result = lin.is_complete(node.node_id, ["ev1"])
        assert isinstance(result, bool)

    def test_is_complete_true_for_single_event(self):
        from paper_trading.multi_session.lineage_v166 import CoordinationLineage
        lin = CoordinationLineage()
        n1 = lin.record("start", ["s1"])
        result = lin.is_complete(n1.node_id, ["start"])
        assert result is True

    def test_multiple_nodes_accumulate(self):
        from paper_trading.multi_session.lineage_v166 import CoordinationLineage
        lin = CoordinationLineage()
        lin.record("ev1", ["s1"])
        lin.record("ev2", ["s2"])
        lin.record("ev3", ["s1", "s2"])
        assert len(lin.all_nodes()) == 3


class TestReplay:
    def test_record_and_get_log(self):
        from paper_trading.multi_session.replay_v166 import CoordinationReplay
        rp = CoordinationReplay()
        ctx = _make_context()
        from paper_trading.multi_session.coordinator_v166 import MultiSessionCoordinator
        c = MultiSessionCoordinator()
        result = c.coordinate(ctx)
        rp.record(ctx, result)
        log = rp.get_log()
        assert isinstance(log, list)
        assert len(log) == 1

    def test_get_log_empty_initially(self):
        from paper_trading.multi_session.replay_v166 import CoordinationReplay
        rp = CoordinationReplay()
        assert rp.get_log() == []


class TestReconciliation:
    def test_reconciler_instantiation(self):
        from paper_trading.multi_session.reconciliation_v166 import CoordinationReconciler
        r = CoordinationReconciler()
        assert r is not None

    def test_reconcile_returns_reconciliation_result(self):
        from paper_trading.multi_session.reconciliation_v166 import CoordinationReconciler, ReconciliationResult
        r = CoordinationReconciler()
        result = r.reconcile({}, {})
        assert isinstance(result, ReconciliationResult)

    def test_reconcile_empty_dicts_passes(self):
        from paper_trading.multi_session.reconciliation_v166 import CoordinationReconciler
        r = CoordinationReconciler()
        result = r.reconcile({}, {})
        assert result.passed is True


class TestPanelIntegration:
    def test_load_all_tabs(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel, PANEL_TABS
        p = MultiSessionCoordinationPanel()
        for tab in PANEL_TABS:
            r = p.render_tab(tab)
            assert isinstance(r, dict)

    def test_render_all_returns_dict(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel
        p = MultiSessionCoordinationPanel()
        r = p.render_all()
        assert isinstance(r, dict)

    def test_render_text_summary_returns_string(self):
        from gui.multi_session_coordination_panel import MultiSessionCoordinationPanel
        p = MultiSessionCoordinationPanel()
        s = p.render_text_summary()
        assert isinstance(s, str)

    def test_loaded_tab_count_is_26(self):
        from gui.multi_session_coordination_panel import PANEL_TABS
        assert len(PANEL_TABS) == 26


class TestCoordinationPolicy:
    def test_make_default_policy_returns_valid_policy(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        from paper_trading.multi_session.models_v166 import CoordinationPolicy
        p = make_default_policy()
        assert isinstance(p, CoordinationPolicy)

    def test_forbidden_actions_contains_real_order_creation(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert "real_order_creation" in p.forbidden_actions

    def test_forbidden_actions_contains_broker_execution(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert "broker_execution" in p.forbidden_actions

    def test_default_forbidden_actions_list_non_empty(self):
        from paper_trading.multi_session.coordination_policy_v166 import DEFAULT_FORBIDDEN_ACTIONS
        assert len(DEFAULT_FORBIDDEN_ACTIONS) > 0

    def test_policy_version_is_166(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert p.version == "1.6.6"


class TestVersionConsistency:
    def test_enums_module_version_consistent(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert s.version == "1.6.6"

    def test_health_check_version_is_166(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        assert CHECK_VERSION == "1.6.6"

    def test_gate_version_is_166(self):
        from release.multi_session_coordination_release_gate_v166 import GATE_VERSION
        assert GATE_VERSION == "1.6.6"

    def test_panel_version_is_166(self):
        from gui.multi_session_coordination_panel import PANEL_VERSION
        assert PANEL_VERSION == "1.6.6"

    def test_policy_version_is_166(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert p.version == "1.6.6"
