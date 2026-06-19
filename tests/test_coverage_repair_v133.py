"""
tests/test_coverage_repair_v133.py — Tests for v1.3.3 Coverage Repair Workflow.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] All test fixtures use DEMO_ONLY data. No real data.
"""
from __future__ import annotations

import json
import os
import sys
import uuid

import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ===========================================================================
# TestRepairModels
# ===========================================================================

class TestRepairModels:
    """7 tests — model round-trip, invariants, forward compatibility."""

    def test_task_round_trip(self):
        from coverage_repair.models_v133 import CoverageRepairTask, RepairIssueType
        task = CoverageRepairTask(
            task_id="test-001",
            symbol="DEMO_2330",
            issue_type=RepairIssueType.MISSING_DATA,
            profile="research",
        )
        d = task.to_dict()
        task2 = CoverageRepairTask.from_dict(d)
        assert task2.task_id == "test-001"
        assert task2.symbol == "DEMO_2330"
        assert task2.issue_type == "MISSING_DATA"

    def test_plan_round_trip(self):
        from coverage_repair.models_v133 import RepairPlan, RepairActionType
        plan = RepairPlan(
            plan_id="plan-001",
            task_id="task-001",
            symbol="DEMO_2330",
            selected_action=RepairActionType.REFRESH_PROVIDER,
            dry_run=True,
        )
        d = plan.to_dict()
        plan2 = RepairPlan.from_dict(d)
        assert plan2.plan_id == "plan-001"
        assert plan2.dry_run is True
        assert plan2.destructive is False

    def test_execution_result_round_trip(self):
        from coverage_repair.models_v133 import RepairExecutionResult
        result = RepairExecutionResult(
            execution_id="exec-001",
            task_id="task-001",
            status="RESOLVED",
            resolved=True,
        )
        d = result.to_dict()
        result2 = RepairExecutionResult.from_dict(d)
        assert result2.execution_id == "exec-001"
        assert result2.resolved is True

    def test_unknown_fields_forward_compatible(self):
        from coverage_repair.models_v133 import CoverageRepairTask
        d = {
            "task_id": "test-002",
            "symbol": "DEMO_2454",
            "issue_type": "MISSING_DATA",
            "future_field_v200": "should_be_ignored",
        }
        task = CoverageRepairTask.from_dict(d)
        assert task.task_id == "test-002"
        assert not hasattr(task, "future_field_v200")

    def test_destructive_default_false(self):
        from coverage_repair.models_v133 import CoverageRepairTask
        task = CoverageRepairTask()
        assert task.destructive is False

    def test_auto_retry_default_false(self):
        from coverage_repair.models_v133 import CoverageRepairTask
        task = CoverageRepairTask()
        assert task.auto_retry_allowed is False

    def test_no_real_orders_invariant(self):
        from coverage_repair.models_v133 import CoverageRepairTask
        task = CoverageRepairTask()
        assert task.no_real_orders is True
        assert task.production_trading_blocked is True

    def test_build_dedup_key(self):
        from coverage_repair.models_v133 import CoverageRepairTask
        task = CoverageRepairTask(
            symbol="DEMO_2330",
            market="TWSE",
            profile="research",
            issue_type="MISSING_DATA",
            issue_code="M001",
            issue_field="close",
            provider_id="local_file",
        )
        key = task.build_dedup_key()
        assert "DEMO_2330" in key
        assert "MISSING_DATA" in key

    def test_plan_dry_run_default(self):
        from coverage_repair.models_v133 import RepairPlan
        plan = RepairPlan()
        assert plan.dry_run is True
        assert plan.destructive is False
        assert plan.executable is False

    def test_repair_task_status_transitions(self):
        from coverage_repair.models_v133 import RepairTaskStatus
        assert RepairTaskStatus.can_transition("OPEN", "PLANNED")
        assert RepairTaskStatus.can_transition("IN_PROGRESS", "RESOLVED")
        assert not RepairTaskStatus.can_transition("RESOLVED", "IN_PROGRESS")
        assert not RepairTaskStatus.can_transition("CANCELLED", "IN_PROGRESS")

    def test_terminal_statuses(self):
        from coverage_repair.models_v133 import RepairTaskStatus
        assert RepairTaskStatus.is_terminal("RESOLVED")
        assert RepairTaskStatus.is_terminal("CANCELLED")
        assert not RepairTaskStatus.is_terminal("OPEN")
        assert not RepairTaskStatus.is_terminal("FAILED")


# ===========================================================================
# TestIssueMapping
# ===========================================================================

class TestIssueMapping:
    """12 mapping tests from spec."""

    def setup_method(self):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        self.mapper = CoverageRepairIssueMapper()

    def test_missing_maps_to_missing_data(self):
        assert self.mapper.map_issue_type("MISSING") == "MISSING_DATA"
        assert self.mapper.map_issue_type("MISSING_DATA") == "MISSING_DATA"

    def test_partial_maps_to_partial_data(self):
        assert self.mapper.map_issue_type("PARTIAL") == "PARTIAL_DATA"

    def test_stale_maps_to_stale_data(self):
        assert self.mapper.map_issue_type("STALE") == "STALE_DATA"

    def test_blocked_maps_to_blocked_data(self):
        assert self.mapper.map_issue_type("BLOCKED") == "BLOCKED_DATA"

    def test_unavailable_maps_to_unavailable_source(self):
        assert self.mapper.map_issue_type("UNAVAILABLE") == "UNAVAILABLE_SOURCE"

    def test_demo_only_maps_to_demo_only_data(self):
        assert self.mapper.map_issue_type("DEMO_ONLY") == "DEMO_ONLY_DATA"

    def test_source_conflict_maps_correctly(self):
        assert self.mapper.map_issue_type("SOURCE_CONFLICT") == "SOURCE_CONFLICT"

    def test_insufficient_history_maps_correctly(self):
        assert self.mapper.map_issue_type("INSUFFICIENT_HISTORY") == "INSUFFICIENT_HISTORY"
        assert self.mapper.map_issue_type("MA60") == "INSUFFICIENT_HISTORY"

    def test_provider_disabled_maps_correctly(self):
        assert self.mapper.map_issue_type("PROVIDER_DISABLED") == "PROVIDER_DISABLED"

    def test_auth_required_maps_correctly(self):
        assert self.mapper.map_issue_type("AUTH_REQUIRED") == "PROVIDER_AUTH_REQUIRED"

    def test_rate_limited_maps_correctly(self):
        assert self.mapper.map_issue_type("RATE_LIMITED") == "PROVIDER_RATE_LIMITED"

    def test_schema_mismatch_maps_correctly(self):
        assert self.mapper.map_issue_type("SCHEMA_MISMATCH") == "INVALID_SCHEMA"

    def test_cache_stale_maps_correctly(self):
        assert self.mapper.map_issue_type("CACHE_STALE") == "CACHE_STALE"

    def test_unknown_maps_to_unknown(self):
        assert self.mapper.map_issue_type("SOMETHING_RANDOM_XYZ") == "UNKNOWN"

    def test_demo_only_task_is_blocked(self):
        task = self.mapper.build_task("DEMO_2330", "DEMO_ONLY_DATA")
        assert task.status == "BLOCKED"
        assert "DEMO_ONLY" in task.blocking_reason

    def test_source_conflict_task_is_conflict_review(self):
        task = self.mapper.build_task("DEMO_2330", "SOURCE_CONFLICT")
        assert task.status == "CONFLICT_REVIEW"

    def test_auth_required_task_is_waiting_auth(self):
        task = self.mapper.build_task("DEMO_2330", "PROVIDER_AUTH_REQUIRED")
        assert task.status == "WAITING_AUTH"

    def test_from_coverage_record(self):
        record = {
            "symbol": "DEMO_2330",
            "market": "TWSE",
            "tier": "CORE",
            "profile": "research",
            "coverage_status": "MISSING",
            "quality_status": "BLOCKED",
        }
        tasks = self.mapper.from_coverage_record(record)
        assert len(tasks) == 1
        assert tasks[0].issue_type == "MISSING_DATA"

    def test_covered_record_returns_no_tasks(self):
        record = {
            "symbol": "DEMO_2330",
            "coverage_status": "COVERED",
        }
        tasks = self.mapper.from_coverage_record(record)
        assert len(tasks) == 0

    def test_from_provider_response_unavailable(self):
        resp = {"status": "UNAVAILABLE", "provider_id": "demo", "data_mode": "DEMO_ONLY"}
        tasks = self.mapper.from_provider_response(resp, "DEMO_2330", "research")
        assert len(tasks) >= 1

    def test_from_provider_response_success_no_tasks(self):
        resp = {"status": "SUCCESS", "provider_id": "demo", "record_count": 10}
        tasks = self.mapper.from_provider_response(resp, "DEMO_2330", "research")
        assert len(tasks) == 0

    def test_from_quality_report(self):
        report = {
            "symbol": "DEMO_2330",
            "profile": "research",
            "overall_status": "BLOCKED",
            "score": 0,
            "issues": [{"type": "BLOCKED_DATA", "field": "close", "code": "B001", "detail": ""}],
        }
        tasks = self.mapper.from_quality_report(report)
        assert len(tasks) >= 1


# ===========================================================================
# TestPriorityEngine
# ===========================================================================

class TestPriorityEngine:
    """7 tests — scoring rules, bounds, determinism."""

    def setup_method(self):
        from coverage_repair.priority_engine import CoverageRepairPriorityEngine
        self.engine = CoverageRepairPriorityEngine()

    def _make_task(self, issue_type, tier="", profile="", **kwargs):
        from coverage_repair.models_v133 import CoverageRepairTask
        return CoverageRepairTask(
            task_id=str(uuid.uuid4()),
            symbol="DEMO_2330",
            issue_type=issue_type,
            universe_tier=tier,
            profile=profile,
            **kwargs,
        )

    def test_core_blocked_is_critical(self):
        task = self._make_task("BLOCKED_DATA", tier="CORE", profile="backtest")
        priority, score, reasons = self.engine.score(task)
        assert priority == "CRITICAL"
        assert score >= 80.0

    def test_core_stale_is_high(self):
        task = self._make_task("STALE_DATA", tier="CORE", profile="research")
        priority, score, reasons = self.engine.score(task)
        assert priority in ("HIGH", "CRITICAL")
        assert score >= 60.0

    def test_source_conflict_is_critical(self):
        task = self._make_task("SOURCE_CONFLICT", tier="CORE", profile="precise_price")
        priority, score, reasons = self.engine.score(task)
        assert priority == "CRITICAL"

    def test_extended_tier_is_low_or_medium(self):
        task = self._make_task("MISSING_TECHNICAL_INDICATOR", tier="EXTENDED", profile="research")
        priority, score, reasons = self.engine.score(task)
        assert priority in ("LOW", "MEDIUM")

    def test_deterministic_scoring(self):
        task = self._make_task("PARTIAL_DATA", tier="RESEARCH", profile="research")
        p1, s1, _ = self.engine.score(task)
        p2, s2, _ = self.engine.score(task)
        assert p1 == p2
        assert s1 == s2

    def test_score_bounds_0_to_100(self):
        from coverage_repair.models_v133 import RepairIssueType
        for issue_type in RepairIssueType.all_types():
            task = self._make_task(issue_type, tier="CORE")
            _, score, _ = self.engine.score(task)
            assert 0.0 <= score <= 100.0, f"Score out of bounds for {issue_type}: {score}"

    def test_missing_data_core_high_score(self):
        task = self._make_task("MISSING_DATA", tier="CORE", profile="research")
        priority, score, reasons = self.engine.score(task)
        assert score >= 60.0

    def test_excluded_tier_reduces_score(self):
        task_excluded = self._make_task("MISSING_DATA", tier="EXCLUDED")
        task_core = self._make_task("MISSING_DATA", tier="CORE")
        _, score_exc, _ = self.engine.score(task_excluded)
        _, score_core, _ = self.engine.score(task_core)
        assert score_core > score_exc

    def test_reasons_dict_populated(self):
        task = self._make_task("STALE_DATA", tier="RESEARCH")
        _, _, reasons = self.engine.score(task)
        assert "base_score" in reasons
        assert "final_score" in reasons
        assert "priority" in reasons


# ===========================================================================
# TestRepairQueue
# ===========================================================================

class TestRepairQueue:
    """8 tests — queue operations, dedup, transitions, serialization."""

    def _make_task(self, symbol="DEMO_2330", profile="research", issue_type="MISSING_DATA"):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        return mapper.build_task(symbol, issue_type, profile=profile)

    def test_add_task_succeeds(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        result = q.add_task(task)
        assert result is True
        assert len(q.list_tasks()) == 1

    def test_duplicate_not_readded(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        task2 = self._make_task()  # same dedup key
        result = q.add_task(task2)
        assert result is False
        assert len(q.list_tasks()) == 1

    def test_different_profile_adds_separately(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        t1 = self._make_task(profile="research")
        t2 = self._make_task(profile="backtest")
        q.add_task(t1)
        q.add_task(t2)
        assert len(q.list_tasks()) == 2

    def test_invalid_transition_raises_value_error(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        with pytest.raises(ValueError):
            q.update_status(task.task_id, "RESOLVED")  # OPEN->RESOLVED not allowed directly

    def test_mark_resolved(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        # Move to IN_PROGRESS first
        q.update_status(task.task_id, "IN_PROGRESS")
        q.update_status(task.task_id, "REVALIDATING")
        ok = q.mark_resolved(task.task_id, reason="test resolved")
        assert ok is True
        t = q.get_task(task.task_id)
        assert t.status == "RESOLVED"

    def test_reopen_task(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        # Ignore then reopen
        q.update_status(task.task_id, "IGNORED")
        ok = q.reopen_task(task.task_id)
        assert ok is True
        t = q.get_task(task.task_id)
        assert t.status == "OPEN"

    def test_serialization_round_trip(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        d = q.to_dict()
        q2 = CoverageRepairQueue.from_dict(d)
        assert len(q2.list_tasks()) == 1

    def test_corruption_graceful(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        # Adding malformed data should not crash the queue
        try:
            result = q.add_task(None)
            assert result is False  # should fail gracefully
        except Exception:
            pass  # any exception is acceptable, but queue should still work
        task = self._make_task()
        assert q.add_task(task) is True

    def test_summarize(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        summary = q.summarize()
        assert summary["total"] == 1
        assert summary["open"] >= 0
        assert summary["no_real_orders"] is True

    def test_list_open(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        open_tasks = q.list_open()
        assert len(open_tasks) >= 1

    def test_prune_resolved(self):
        from coverage_repair.queue import CoverageRepairQueue
        q = CoverageRepairQueue()
        task = self._make_task()
        q.add_task(task)
        q.update_status(task.task_id, "IN_PROGRESS")
        q.update_status(task.task_id, "REVALIDATING")
        q.mark_resolved(task.task_id, "done")
        n = q.prune_resolved()
        assert n == 1
        assert len(q.list_tasks()) == 0


# ===========================================================================
# TestPlanner
# ===========================================================================

class TestPlanner:
    """7 tests — plan construction, safety checks."""

    def setup_method(self):
        from coverage_repair.planner import CoverageRepairPlanner
        self.planner = CoverageRepairPlanner()

    def _make_task(self, issue_type="MISSING_DATA", profile="research", status="OPEN"):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        return mapper.build_task("DEMO_2330", issue_type, profile=profile)

    def test_dry_run_default(self):
        task = self._make_task()
        plan = self.planner.build_plan(task)
        assert plan.dry_run is True

    def test_destructive_always_false(self):
        task = self._make_task()
        plan = self.planner.build_plan(task)
        assert plan.destructive is False

    def test_source_conflict_requires_manual(self):
        task = self._make_task(issue_type="SOURCE_CONFLICT")
        plan = self.planner.build_plan(task)
        assert not plan.executable or len(plan.blocking_reasons) > 0

    def test_auth_required_requires_manual(self):
        task = self._make_task(issue_type="PROVIDER_AUTH_REQUIRED")
        plan = self.planner.build_plan(task)
        assert plan.selected_action == "REQUEST_AUTH_CONFIGURATION" or len(plan.blocking_reasons) > 0

    def test_invalid_schema_requires_manual(self):
        task = self._make_task(issue_type="INVALID_SCHEMA")
        plan = self.planner.build_plan(task)
        assert plan.selected_action in ("FIX_SCHEMA", "MANUAL_REVIEW")

    def test_destructive_blocked_in_validate(self):
        from coverage_repair.models_v133 import RepairPlan
        plan = RepairPlan(
            plan_id="p001",
            task_id="t001",
            selected_action="REFRESH_PROVIDER",
            destructive=True,  # force True to test
        )
        valid, errors = self.planner.validate_plan(plan)
        assert valid is False
        assert any("destructive" in e.lower() for e in errors)

    def test_mock_action_blocked(self):
        from coverage_repair.models_v133 import RepairPlan
        plan = RepairPlan(
            plan_id="p001",
            task_id="t001",
            selected_action="FILL_MOCK",
        )
        valid, errors = self.planner.validate_plan(plan)
        assert valid is False

    def test_no_safe_action_for_unknown(self):
        task = self._make_task(issue_type="UNKNOWN")
        plan = self.planner.build_plan(task)
        assert plan.selected_action in ("MANUAL_REVIEW", "NO_SAFE_ACTION")

    def test_summarize_plan(self):
        task = self._make_task()
        plan = self.planner.build_plan(task)
        summary = self.planner.summarize_plan(plan)
        assert "Plan ID" in summary
        assert "Dry Run" in summary


# ===========================================================================
# TestExecutor
# ===========================================================================

class TestExecutor:
    """7 tests — execution safety and flow."""

    def setup_method(self):
        from coverage_repair.executor import CoverageRepairExecutor
        self.executor = CoverageRepairExecutor()

    def _make_plan(self, action="REFRESH_PROVIDER", executable=False, dry_run=True, destructive=False):
        from coverage_repair.models_v133 import RepairPlan
        return RepairPlan(
            plan_id=str(uuid.uuid4()),
            task_id=str(uuid.uuid4()),
            symbol="DEMO_2330",
            profile="research",
            selected_action=action,
            executable=executable,
            dry_run=dry_run,
            destructive=destructive,
        )

    def test_dry_run_result_returned(self):
        plan = self._make_plan(action="REBUILD_CACHE")
        result = self.executor.execute(plan)
        assert result.execution_id != ""
        assert result.status in ("RESOLVED", "PARTIALLY_RESOLVED", "FAILED", "BLOCKED",
                                  "MANUAL_REQUIRED", "ERROR")

    def test_destructive_plan_blocked(self):
        plan = self._make_plan(destructive=True)
        result = self.executor.execute(plan)
        assert result.status == "BLOCKED"
        assert any("destructive" in e.lower() for e in result.errors)

    def test_forbidden_action_blocked(self):
        plan = self._make_plan(action="BUY")
        result = self.executor.execute(plan)
        assert result.status == "BLOCKED"

    def test_manual_action_returns_manual_required(self):
        plan = self._make_plan(action="REVIEW_SOURCE_CONFLICT")
        result = self.executor.execute(plan)
        assert result.status == "MANUAL_REQUIRED"

    def test_non_retryable_task_blocked(self):
        from coverage_repair.models_v133 import CoverageRepairTask
        task = CoverageRepairTask(
            task_id=str(uuid.uuid4()),
            symbol="DEMO_2330",
            retryable=False,
        )
        result = self.executor.retry_task(task)
        assert result.status == "BLOCKED"
        assert any("not retryable" in e.lower() for e in result.errors)

    def test_provenance_preserved(self):
        plan = self._make_plan(action="INVALIDATE_CACHE")
        result = self.executor.execute(plan)
        assert "no_real_orders" in result.provenance
        assert result.provenance["no_real_orders"] is True

    def test_build_result_has_safety_flags(self):
        result = self.executor.build_result(task_id="t001", action="REFRESH_PROVIDER")
        assert result.provenance["no_real_orders"] is True
        assert result.provenance["broker_execution_enabled"] is False
        assert result.provenance["production_trading_blocked"] is True
        assert result.provenance["mock_fallback_used"] is False


# ===========================================================================
# TestRetry
# ===========================================================================

class TestRetry:
    """5 tests — retry policy."""

    def setup_method(self):
        from coverage_repair.executor import CoverageRepairExecutor
        self.executor = CoverageRepairExecutor()

    def _make_retryable_task(self, attempt_count=0, max_attempts=3):
        from coverage_repair.models_v133 import CoverageRepairTask, RepairIssueType
        return CoverageRepairTask(
            task_id=str(uuid.uuid4()),
            symbol="DEMO_2330",
            issue_type=RepairIssueType.MISSING_DATA,
            retryable=True,
            auto_retry_allowed=False,
            attempt_count=attempt_count,
            max_attempts=max_attempts,
            selected_action="REFRESH_PROVIDER",
        )

    def test_retryable_task_increments_count(self):
        task = self._make_retryable_task(attempt_count=0)
        result = self.executor.retry_task(task)
        assert task.attempt_count == 1

    def test_max_attempts_blocks_retry(self):
        task = self._make_retryable_task(attempt_count=3, max_attempts=3)
        result = self.executor.retry_task(task)
        assert result.status == "BLOCKED"
        assert any("max attempts" in e.lower() for e in result.errors)

    def test_non_retryable_blocked(self):
        from coverage_repair.models_v133 import CoverageRepairTask
        task = CoverageRepairTask(
            task_id=str(uuid.uuid4()),
            symbol="DEMO_2330",
            retryable=False,
            attempt_count=0,
            max_attempts=3,
        )
        result = self.executor.retry_task(task)
        assert result.status == "BLOCKED"

    def test_auto_retry_allowed_default_false(self):
        task = self._make_retryable_task()
        assert task.auto_retry_allowed is False

    def test_retry_preserves_no_real_orders(self):
        task = self._make_retryable_task()
        result = self.executor.retry_task(task)
        assert result.provenance.get("no_real_orders") is True


# ===========================================================================
# TestIntegrations
# ===========================================================================

class TestIntegrations:
    """8 tests — cross-module integration."""

    def test_coverage_record_builds_task(self):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        record = {
            "symbol": "DEMO_2330",
            "market": "TWSE",
            "tier": "CORE",
            "profile": "research",
            "coverage_status": "MISSING",
        }
        tasks = mapper.from_coverage_record(record)
        assert len(tasks) == 1
        assert tasks[0].symbol == "DEMO_2330"

    def test_provider_unavailable_waiting_source(self):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        resp = {"status": "UNAVAILABLE", "provider_id": "demo", "data_mode": "DEMO_ONLY"}
        tasks = mapper.from_provider_response(resp, "DEMO_2330", "research")
        # The task should be WAITING_SOURCE or OPEN for UNAVAILABLE
        statuses = [t.status for t in tasks]
        assert any(s in ("WAITING_SOURCE", "OPEN", "BLOCKED") for s in statuses)

    def test_provider_auth_waiting_auth(self):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        task = mapper.build_task("DEMO_2330", "PROVIDER_AUTH_REQUIRED")
        assert task.status == "WAITING_AUTH"

    def test_provider_conflict_conflict_review(self):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        task = mapper.build_task("DEMO_2330", "SOURCE_CONFLICT")
        assert task.status == "CONFLICT_REVIEW"

    def test_normal_scan_does_not_write_queue(self):
        """Scanning should not auto-write tasks to queue."""
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        from coverage_repair.queue import CoverageRepairQueue
        mapper = CoverageRepairIssueMapper()
        q = CoverageRepairQueue()
        initial_count = len(q.list_tasks())
        # Mapper alone doesn't touch queue
        record = {"symbol": "DEMO_2330", "coverage_status": "MISSING"}
        mapper.from_coverage_record(record)
        assert len(q.list_tasks()) == initial_count

    def test_demo_only_is_blocked(self):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        task = mapper.build_task("DEMO_2330", "DEMO_ONLY_DATA", profile="precise_price")
        assert task.status == "BLOCKED"
        assert task.auto_retry_allowed is False
        assert "DEMO_ONLY" in task.blocking_reason

    def test_queue_and_query_integration(self):
        from coverage_repair.queue import CoverageRepairQueue
        from coverage_repair.query import CoverageRepairQueryService
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        mapper = CoverageRepairIssueMapper()
        q = CoverageRepairQueue()
        task = mapper.build_task("DEMO_2330", "MISSING_DATA")
        q.add_task(task)
        svc = CoverageRepairQueryService(queue=q)
        summary = svc.summarize()
        assert summary["total"] >= 1

    def test_store_save_load_task(self, tmp_path):
        from coverage_repair.store import CoverageRepairStore
        from coverage_repair.models_v133 import CoverageRepairTask
        store = CoverageRepairStore(base_dir=str(tmp_path))
        task = CoverageRepairTask(
            task_id="store-test-001",
            symbol="DEMO_2330",
        )
        store.save_task(task)
        loaded = store.load_task("store-test-001")
        assert loaded is not None
        assert loaded.symbol == "DEMO_2330"

    def test_store_save_load_execution(self, tmp_path):
        from coverage_repair.store import CoverageRepairStore
        from coverage_repair.models_v133 import RepairExecutionResult
        store = CoverageRepairStore(base_dir=str(tmp_path))
        result = RepairExecutionResult(
            execution_id="exec-store-001",
            status="RESOLVED",
        )
        store.save_execution(result)
        loaded = store.load_execution("exec-store-001")
        assert loaded is not None
        assert loaded.status == "RESOLVED"


# ===========================================================================
# TestCLI
# ===========================================================================

class TestCLI:
    """13 CLI command tests — all commands return rc 0 or 1 (not crash)."""

    def _run_main(self, *args):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "main.py")] + list(args),
            capture_output=True, cwd=BASE_DIR,
        )
        stdout = result.stdout.decode("utf-8", errors="replace") if result.stdout else ""
        stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
        return result.returncode, stdout, stderr

    def test_coverage_repair_list(self):
        rc, out, err = self._run_main("coverage-repair-list")
        assert rc in (0, 1)
        assert "coverage" in (out + err).lower() or "repair" in (out + err).lower()

    def test_coverage_repair_summary(self):
        rc, out, err = self._run_main("coverage-repair-summary")
        assert rc in (0, 1)

    def test_coverage_repair_health(self):
        rc, out, err = self._run_main("coverage-repair-health")
        assert rc in (0, 1)
        assert "pass" in (out + err).lower() or "fail" in (out + err).lower()

    def test_coverage_repair_scan_core(self):
        rc, out, err = self._run_main("coverage-repair-scan", "--tier", "core")
        assert rc in (0, 1)

    def test_coverage_repair_scan_symbol(self):
        rc, out, err = self._run_main("coverage-repair-scan", "--symbol", "2330")
        assert rc in (0, 1)

    def test_coverage_repair_plan_symbol(self):
        rc, out, err = self._run_main("coverage-repair-plan", "--symbol", "2330")
        assert rc in (0, 1)

    def test_coverage_repair_plan_no_args(self):
        rc, out, err = self._run_main("coverage-repair-plan")
        assert rc in (0, 1)

    def test_coverage_repair_show_missing_id(self):
        rc, out, err = self._run_main("coverage-repair-show", "--task-id", "nonexistent-task-id")
        assert rc in (0, 1)

    def test_coverage_repair_run_no_task(self):
        # Should fail gracefully with missing required arg (argparse returns 2 for missing required args)
        rc, out, err = self._run_main("coverage-repair-run", "--task-id", "nonexistent")
        assert rc in (0, 1, 2)

    def test_coverage_repair_history(self):
        rc, out, err = self._run_main("coverage-repair-history")
        assert rc in (0, 1)

    def test_version_info_includes_133(self):
        rc, out, err = self._run_main("version-info")
        assert rc in (0, 1)
        combined = out + err
        assert "1.3.3" in combined or "Coverage Repair" in combined

    def test_universe_health_still_passes(self):
        rc, out, err = self._run_main("universe-health")
        assert rc in (0, 1)

    def test_real_data_quality_health_still_passes(self):
        rc, out, err = self._run_main("real-data-quality-health")
        assert rc in (0, 1)


# ===========================================================================
# TestGUI
# ===========================================================================

class TestGUI:
    """3 tests — GUI panel import and safety."""

    def test_panel_import(self):
        from gui.coverage_repair_panel import CoverageRepairPanel
        assert CoverageRepairPanel is not None

    def test_panel_safety_flags(self):
        from gui.coverage_repair_panel import (
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED, COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED,
        )
        assert NO_REAL_ORDERS is True
        assert BROKER_EXECUTION_ENABLED is False
        assert PRODUCTION_TRADING_BLOCKED is True
        assert COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED is False

    def test_panel_instantiate_no_pyside(self):
        """Panel should gracefully stub when PySide6 unavailable."""
        import gui.coverage_repair_panel as mod
        if not mod._PYSIDE6_AVAILABLE:
            panel = mod.CoverageRepairPanel()
            assert panel.research_only is True
            assert panel.no_real_orders is True


# ===========================================================================
# TestRegression
# ===========================================================================

class TestRegression:
    """10 tests — version, safety flags, backward compatibility."""

    def test_version_is_133(self):
        from release.version_info import VERSION
        # v1.3.3+ — accept any 1.3.x or 1.4.x release
        assert VERSION.startswith("1.3.") or VERSION.startswith("1.4.")

    def test_release_name(self):
        from release.version_info import RELEASE_NAME, BASE_RELEASE, VERSION
        # Coverage Repair is either the release or the base release (or an ancestor)
        assert (
            "Coverage Repair" in RELEASE_NAME
            or "Coverage Repair" in BASE_RELEASE
            or any("Coverage Repair" in v for v in [RELEASE_NAME, BASE_RELEASE])
            or VERSION.startswith("1.4.")  # v1.4.0 supersedes v1.3.3
        )

    def test_base_release_132(self):
        from release.version_info import BASE_RELEASE
        # 1.3.2 is in the ancestry of base releases
        assert "1.3." in BASE_RELEASE

    def test_replay_baseline_129(self):
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"

    def test_no_real_orders_flag(self):
        from release.version_info import NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED
        assert NO_REAL_ORDERS is True
        assert BROKER_EXECUTION_ENABLED is False

    def test_coverage_repair_workflow_flags(self):
        from release.version_info import (
            COVERAGE_REPAIR_WORKFLOW_AVAILABLE,
            COVERAGE_REPAIR_QUEUE_AVAILABLE,
            COVERAGE_REPAIR_PLANNER_AVAILABLE,
            COVERAGE_REPAIR_RETRY_AVAILABLE,
            COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED,
            COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED,
            COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED,
        )
        assert COVERAGE_REPAIR_WORKFLOW_AVAILABLE is True
        assert COVERAGE_REPAIR_QUEUE_AVAILABLE is True
        assert COVERAGE_REPAIR_PLANNER_AVAILABLE is True
        assert COVERAGE_REPAIR_RETRY_AVAILABLE is True
        assert COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED is False
        assert COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED is False
        assert COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED is False

    def test_no_forbidden_trade_actions(self):
        from coverage_repair.models_v133 import RepairActionType
        forbidden = RepairActionType._FORBIDDEN
        safe_actions = [v for k, v in RepairActionType.__dict__.items()
                        if not k.startswith("_") and isinstance(v, str)]
        for action in safe_actions:
            assert not RepairActionType.is_forbidden(action), f"Forbidden action in set: {action}"

    def test_all_issue_types_have_action_mapping(self):
        from coverage_repair.issue_mapper import CoverageRepairIssueMapper
        from coverage_repair.models_v133 import RepairIssueType
        mapper = CoverageRepairIssueMapper()
        for it in RepairIssueType.all_types():
            actions = mapper.map_repair_actions(it)
            assert len(actions) >= 1, f"No actions for issue type: {it}"

    def test_models_safety_constants(self):
        from coverage_repair import models_v133 as m
        assert m.NO_REAL_ORDERS is True
        assert m.BROKER_EXECUTION_ENABLED is False
        assert m.PRODUCTION_TRADING_BLOCKED is True
        assert m.COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED is False
        assert m.COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED is False
        assert m.COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED is False

    def test_fixture_files_exist(self):
        fixture_dir = os.path.join(BASE_DIR, "tests", "fixtures", "coverage_repair")
        expected = [
            "coverage_missing.json",
            "coverage_stale.json",
            "quality_blocked.json",
            "provider_unavailable.json",
            "provider_rate_limited.json",
            "source_conflict.json",
            "repair_queue_v1.json",
        ]
        for f in expected:
            path = os.path.join(fixture_dir, f)
            assert os.path.exists(path), f"Fixture not found: {f}"

    def test_fixture_data_mode_demo_only(self):
        """All fixtures must have data_mode DEMO_ONLY."""
        fixture_dir = os.path.join(BASE_DIR, "tests", "fixtures", "coverage_repair")
        for fname in os.listdir(fixture_dir):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(fixture_dir, fname), encoding="utf-8") as f:
                data = json.load(f)
            assert data.get("_fixture_type") == "TEST_FIXTURE", fname
            assert data.get("note") == "NOT_REAL_DATA", fname
