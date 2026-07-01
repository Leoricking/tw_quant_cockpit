"""
test_multi_session_store_query_v166.py — Store & Query tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
import uuid


def _make_result():
    from paper_trading.multi_session.models_v166 import CoordinationResult
    from paper_trading.multi_session.enums_v166 import CoordinationOutcome
    return CoordinationResult(
        coordination_id=str(uuid.uuid4()),
        sessions_considered=["s1"],
        sessions_admitted=["s1"],
        sessions_blocked=[],
        sessions_paused=[],
        sessions_degraded=[],
        conflicts_detected=0,
        conflicts_resolved=0,
        conflicts_unresolved=0,
        resource_allocations={},
        risk_result=CoordinationOutcome.PASS,
        capital_result=CoordinationOutcome.PASS,
        ordering_result=CoordinationOutcome.PASS,
        reconciliation_result=CoordinationOutcome.PASS,
        final_state={},
        warnings=[],
        failures=[],
        lineage=[],
        reproducibility_hash="abc123",
    )


class TestCoordinationStore:
    def test_append_returns_dict(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        result = store.append("decision", {"session_id": "s1", "action": "admit"})
        assert isinstance(result, dict)

    def test_query_all_returns_list(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        store.append("decision", {"a": 1})
        result = store.query()
        assert isinstance(result, list)

    def test_count_zero_initially(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        assert store.count() == 0

    def test_count_increments_on_append(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        store.append("decision", {})
        store.append("conflict", {})
        assert store.count() == 2

    def test_clear_removes_all_records(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        store.append("decision", {})
        store.clear()
        assert store.count() == 0

    def test_summary_returns_dict(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        store.append("decision", {})
        store.append("conflict", {})
        summary = store.summary()
        assert isinstance(summary, dict)

    def test_summary_counts_by_type(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        store.append("decision", {})
        store.append("decision", {})
        store.append("conflict", {})
        summary = store.summary()
        assert summary["decision"] == 2
        assert summary["conflict"] == 1

    def test_query_by_type_returns_filtered(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        store.append("decision", {"id": "d1"})
        store.append("conflict", {"id": "c1"})
        decisions = store.query("decision")
        assert len(decisions) == 1
        assert decisions[0]["id"] == "d1"

    def test_append_records_record_type(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        r = store.append("snapshot", {"data": "test"})
        assert r["record_type"] == "snapshot"

    def test_append_records_stored_at(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        r = store.append("decision", {})
        assert "stored_at" in r

    def test_count_by_type(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        store = CoordinationStore()
        store.append("reservation", {})
        store.append("reservation", {})
        store.append("snapshot", {})
        assert store.count("reservation") == 2
        assert store.count("snapshot") == 1


class TestCoordinationQuery:
    def test_get_decisions_returns_list(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        from paper_trading.multi_session.query_v166 import CoordinationQuery
        store = CoordinationStore()
        q = CoordinationQuery(store)
        assert isinstance(q.get_decisions(), list)

    def test_get_conflicts_returns_list(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        from paper_trading.multi_session.query_v166 import CoordinationQuery
        store = CoordinationStore()
        q = CoordinationQuery(store)
        assert isinstance(q.get_conflicts(), list)

    def test_get_reservations_returns_list(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        from paper_trading.multi_session.query_v166 import CoordinationQuery
        store = CoordinationStore()
        q = CoordinationQuery(store)
        assert isinstance(q.get_reservations(), list)

    def test_get_snapshots_returns_list(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        from paper_trading.multi_session.query_v166 import CoordinationQuery
        store = CoordinationStore()
        q = CoordinationQuery(store)
        assert isinstance(q.get_snapshots(), list)

    def test_get_for_session_filters(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        from paper_trading.multi_session.query_v166 import CoordinationQuery
        store = CoordinationStore()
        store.append("decision", {"session_id": "s1", "action": "admit"})
        store.append("decision", {"session_id": "s2", "action": "block"})
        q = CoordinationQuery(store)
        results = q.get_for_session("s1")
        assert all(r["session_id"] == "s1" for r in results)

    def test_summary_returns_dict(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        from paper_trading.multi_session.query_v166 import CoordinationQuery
        store = CoordinationStore()
        store.append("decision", {})
        q = CoordinationQuery(store)
        summary = q.summary()
        assert isinstance(summary, dict)

    def test_get_decisions_populated(self):
        from paper_trading.multi_session.store_v166 import CoordinationStore
        from paper_trading.multi_session.query_v166 import CoordinationQuery
        store = CoordinationStore()
        store.append("decision", {"id": "d1"})
        store.append("decision", {"id": "d2"})
        q = CoordinationQuery(store)
        decisions = q.get_decisions()
        assert len(decisions) == 2


class TestCoordinationMetrics:
    def test_compute_empty_returns_total_zero(self):
        from paper_trading.multi_session.metrics_v166 import CoordinationMetrics
        m = CoordinationMetrics()
        result = m.compute([])
        assert result["total_coordinations"] == 0

    def test_compute_with_results_returns_admission_rate(self):
        from paper_trading.multi_session.metrics_v166 import CoordinationMetrics
        m = CoordinationMetrics()
        r = _make_result()
        result = m.compute([r])
        assert "admission_rate" in result

    def test_compute_total_coordinations_correct(self):
        from paper_trading.multi_session.metrics_v166 import CoordinationMetrics
        m = CoordinationMetrics()
        results = [_make_result(), _make_result(), _make_result()]
        out = m.compute(results)
        assert out["total_coordinations"] == 3

    def test_compute_total_admitted_correct(self):
        from paper_trading.multi_session.metrics_v166 import CoordinationMetrics
        m = CoordinationMetrics()
        r1 = _make_result()
        r2 = _make_result()
        out = m.compute([r1, r2])
        assert out["total_admitted"] == 2

    def test_compute_avg_admitted_per_coord(self):
        from paper_trading.multi_session.metrics_v166 import CoordinationMetrics
        m = CoordinationMetrics()
        r = _make_result()
        out = m.compute([r])
        assert "avg_admitted_per_coord" in out


class TestCoordinationExplainer:
    def test_explain_decision_returns_string(self):
        from paper_trading.multi_session.explain_v166 import CoordinationExplainer
        from paper_trading.multi_session.coordination_decision_v166 import make_coordination_decision
        from paper_trading.multi_session.enums_v166 import DecisionType
        exp = CoordinationExplainer()
        d = make_coordination_decision(
            session_ids=["s1"],
            decision_type=DecisionType.ADMIT,
            reason="test",
            actor="test",
            input_state_hash="abc",
            policy_version="1.6.6",
            selected_action="admit_session",
        )
        text = exp.explain_decision(d)
        assert isinstance(text, str)
        assert len(text) > 0

    def test_explain_conflict_returns_string(self):
        from paper_trading.multi_session.explain_v166 import CoordinationExplainer
        from paper_trading.multi_session.models_v166 import SessionConflict
        from paper_trading.multi_session.enums_v166 import ConflictType, ConflictSeverity
        from datetime import datetime, timezone
        exp = CoordinationExplainer()
        c = SessionConflict(
            conflict_id=str(uuid.uuid4()),
            session_ids=["s1"],
            conflict_type=ConflictType.SYMBOL_OVERLAP,
            severity=ConflictSeverity.WARN,
            resource_key=None,
            symbol="2330",
            strategy=None,
            detected_at=datetime.now(timezone.utc),
            evidence={},
            resolution_options=[],
            blocking=False,
            policy_version="1.6.6",
        )
        text = exp.explain_conflict(c)
        assert isinstance(text, str)

    def test_explain_result_returns_string(self):
        from paper_trading.multi_session.explain_v166 import CoordinationExplainer
        exp = CoordinationExplainer()
        r = _make_result()
        text = exp.explain_result(r)
        assert isinstance(text, str)

    def test_explain_all_returns_list(self):
        from paper_trading.multi_session.explain_v166 import CoordinationExplainer
        exp = CoordinationExplainer()
        results = [_make_result(), _make_result()]
        texts = exp.explain_all(results)
        assert isinstance(texts, list)
        assert len(texts) == 2
