"""
tests/test_coverage_repair_regression.py — Regression fixtures for Coverage Repair v1.1.2.

Safety checks:
  - dry_run=True default
  - execute without allow_write → DRY_RUN status
  - INVALID OHLC → BLOCKED
  - CONFLICT → MANUAL_REVIEW
  - DUPLICATE (identical) → AUTO_SAFE
  - MISSING → SOURCE_REQUIRED
  - onboarding package (v1.1.1) still intact

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Fixtures must NOT be written to production data paths.
"""
from __future__ import annotations

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"


def _run(label: str, fn) -> str:
    try:
        fn()
        print(f"  [PASS] {label}")
        return PASS
    except Exception as exc:
        print(f"  [FAIL] {label}: {exc}")
        return FAIL


def test_package_import():
    import coverage_repair
    assert getattr(coverage_repair, "NO_REAL_ORDERS", False) is True
    assert getattr(coverage_repair, "DRY_RUN_DEFAULT", False) is True
    assert getattr(coverage_repair, "DESTRUCTIVE_REPAIR_DISABLED", False) is True
    assert getattr(coverage_repair, "SYNTHETIC_OHLC_REPAIR_DISABLED", False) is True
    assert getattr(coverage_repair, "INVALID_OHLC_AUTO_MODIFY_DISABLED", False) is True
    assert getattr(coverage_repair, "CONFLICT_AUTO_OVERWRITE_ENABLED", True) is False


def test_schema_import():
    from coverage_repair.coverage_repair_schema import (
        CoverageIssue, CoverageRepairTask, RepairPlan, RepairResult,
        RepairSummary, RepairRetryManifest,
        ISSUE_MISSING, ISSUE_DUPLICATE, ISSUE_CONFLICT, ISSUE_INVALID,
        ACTION_AUTO_SAFE, ACTION_MANUAL_REVIEW, ACTION_SOURCE_REQUIRED, ACTION_BLOCKED,
        PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    )


def test_task_builder_invalid_is_blocked():
    from coverage_repair.coverage_repair_schema import (
        CoverageIssue, ISSUE_INVALID, ACTION_BLOCKED, PRIORITY_P1,
    )
    from coverage_repair.repair_task_builder import RepairTaskBuilder
    issue = CoverageIssue(
        issue_id="test_invalid",
        symbol="TEST",
        dataset="daily",
        issue_type=ISSUE_INVALID,
        description="High < Low",
        row_count=5,
    )
    builder = RepairTaskBuilder()
    tasks = builder.build([issue])
    assert len(tasks) == 1
    assert tasks[0].action == ACTION_BLOCKED, f"Expected BLOCKED, got {tasks[0].action}"
    assert tasks[0].priority == PRIORITY_P1


def test_task_builder_conflict_is_manual_review():
    from coverage_repair.coverage_repair_schema import (
        CoverageIssue, ISSUE_CONFLICT, ACTION_MANUAL_REVIEW, PRIORITY_P1,
    )
    from coverage_repair.repair_task_builder import RepairTaskBuilder
    issue = CoverageIssue(
        issue_id="test_conflict",
        symbol="TEST",
        dataset="daily",
        issue_type=ISSUE_CONFLICT,
        description="Conflicting rows",
        row_count=5,
        affected_dates=["2024-01-02"],
    )
    builder = RepairTaskBuilder()
    tasks = builder.build([issue])
    assert len(tasks) == 1
    assert tasks[0].action == ACTION_MANUAL_REVIEW, f"Expected MANUAL_REVIEW, got {tasks[0].action}"


def test_task_builder_missing_is_source_required():
    from coverage_repair.coverage_repair_schema import (
        CoverageIssue, ISSUE_MISSING, ACTION_SOURCE_REQUIRED, PRIORITY_P0,
    )
    from coverage_repair.repair_task_builder import RepairTaskBuilder
    issue = CoverageIssue(
        issue_id="test_missing",
        symbol="TEST",
        dataset="daily",
        issue_type=ISSUE_MISSING,
        description="No data",
        row_count=0,
    )
    builder = RepairTaskBuilder()
    tasks = builder.build([issue])
    assert len(tasks) == 1
    assert tasks[0].action == ACTION_SOURCE_REQUIRED
    assert tasks[0].priority == PRIORITY_P0


def test_task_builder_duplicate_is_auto_safe():
    from coverage_repair.coverage_repair_schema import (
        CoverageIssue, ISSUE_DUPLICATE, ACTION_AUTO_SAFE, PRIORITY_P3,
    )
    from coverage_repair.repair_task_builder import RepairTaskBuilder
    issue = CoverageIssue(
        issue_id="test_dup",
        symbol="TEST",
        dataset="daily",
        issue_type=ISSUE_DUPLICATE,
        description="Identical duplicates",
        row_count=10,
        affected_dates=["2024-01-02"],
        details={"duplicate_count": 1},
    )
    builder = RepairTaskBuilder()
    tasks = builder.build([issue])
    assert len(tasks) == 1
    assert tasks[0].action == ACTION_AUTO_SAFE
    assert tasks[0].priority == PRIORITY_P3


def test_executor_dry_run_default():
    """execute() without allow_write must produce only DRY_RUN/BLOCKED/MANUAL/SKIPPED statuses."""
    from coverage_repair.coverage_repair_schema import (
        RepairPlan, CoverageRepairTask,
        ACTION_AUTO_SAFE, PRIORITY_P3, ISSUE_DUPLICATE,
        REPAIR_STATUS_DRY_RUN, REPAIR_STATUS_BLOCKED,
        REPAIR_STATUS_MANUAL, REPAIR_STATUS_SKIPPED,
    )
    from coverage_repair.repair_executor import CoverageRepairExecutor
    from datetime import datetime
    task = CoverageRepairTask(
        task_id="test_task_dry",
        issue_id="test_issue_dry",
        symbol="TEST",
        dataset="daily",
        issue_type=ISSUE_DUPLICATE,
        action=ACTION_AUTO_SAFE,
        priority=PRIORITY_P3,
        description="Dry run test",
        dry_run=True,
    )
    plan = RepairPlan(
        plan_id="test_plan_dry",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_issues=1, total_tasks=1,
        p0_count=0, p1_count=0, p2_count=0, p3_count=1,
        auto_safe_count=1, manual_review_count=0,
        source_required_count=0, blocked_count=0,
        tasks=[task],
        dry_run=True,
    )
    executor = CoverageRepairExecutor()
    summary = executor.execute(plan, allow_write=False)
    assert summary.dry_run is True
    SAFE_STATUSES = {REPAIR_STATUS_DRY_RUN, REPAIR_STATUS_BLOCKED, REPAIR_STATUS_MANUAL, REPAIR_STATUS_SKIPPED}
    for r in summary.results:
        assert r.status in SAFE_STATUSES, f"Unexpected status: {r.status}"


def test_executor_invalid_always_blocked():
    """INVALID tasks must always be BLOCKED regardless of allow_write."""
    from coverage_repair.coverage_repair_schema import (
        RepairPlan, CoverageRepairTask,
        ACTION_BLOCKED, PRIORITY_P1, ISSUE_INVALID,
        REPAIR_STATUS_BLOCKED,
    )
    from coverage_repair.repair_executor import CoverageRepairExecutor
    from datetime import datetime
    task = CoverageRepairTask(
        task_id="test_task_invalid",
        issue_id="test_issue_invalid",
        symbol="TEST",
        dataset="daily",
        issue_type=ISSUE_INVALID,
        action=ACTION_BLOCKED,
        priority=PRIORITY_P1,
        description="Invalid OHLC",
        blocked_reason="Must not auto-modify OHLC.",
    )
    plan = RepairPlan(
        plan_id="test_plan_invalid",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_issues=1, total_tasks=1,
        p0_count=0, p1_count=1, p2_count=0, p3_count=0,
        auto_safe_count=0, manual_review_count=0,
        source_required_count=0, blocked_count=1,
        tasks=[task],
    )
    executor = CoverageRepairExecutor()
    # Even with allow_write=True, INVALID must be BLOCKED
    summary = executor.execute(plan, allow_write=True)
    for r in summary.results:
        assert r.status == REPAIR_STATUS_BLOCKED, f"INVALID task must be BLOCKED, got {r.status}"


def test_executor_conflict_always_manual():
    """CONFLICT tasks must always be MANUAL_REVIEW."""
    from coverage_repair.coverage_repair_schema import (
        RepairPlan, CoverageRepairTask,
        ACTION_MANUAL_REVIEW, PRIORITY_P1, ISSUE_CONFLICT,
        REPAIR_STATUS_MANUAL,
    )
    from coverage_repair.repair_executor import CoverageRepairExecutor
    from datetime import datetime
    task = CoverageRepairTask(
        task_id="test_task_conflict",
        issue_id="test_issue_conflict",
        symbol="TEST",
        dataset="daily",
        issue_type=ISSUE_CONFLICT,
        action=ACTION_MANUAL_REVIEW,
        priority=PRIORITY_P1,
        description="Conflict",
    )
    plan = RepairPlan(
        plan_id="test_plan_conflict",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_issues=1, total_tasks=1,
        p0_count=0, p1_count=1, p2_count=0, p3_count=0,
        auto_safe_count=0, manual_review_count=1,
        source_required_count=0, blocked_count=0,
        tasks=[task],
    )
    executor = CoverageRepairExecutor()
    summary = executor.execute(plan, allow_write=True)
    for r in summary.results:
        assert r.status == REPAIR_STATUS_MANUAL, f"CONFLICT must be MANUAL, got {r.status}"


def test_health_check_pass():
    from coverage_repair.repair_health import CoverageRepairHealthCheck
    checker = CoverageRepairHealthCheck()
    result = checker.run()
    assert result["overall"] in ("PASS", "WARN"), f"Health overall: {result['overall']}"
    assert result["failed"] == 0, f"Failed checks: {[k for k,v in result['results'].items() if v == 'FAIL']}"


def test_onboarding_v111_intact():
    """v1.1.1 data_onboarding package must remain unbroken."""
    import data_onboarding
    assert getattr(data_onboarding, "NO_REAL_ORDERS", False) is True
    assert getattr(data_onboarding, "DRY_RUN_DEFAULT", False) is True
    assert getattr(data_onboarding, "DESTRUCTIVE_IMPORT_DISABLED", False) is True
    assert getattr(data_onboarding, "CONFLICT_AUTO_OVERWRITE_ENABLED", True) is False


def test_version_info_112():
    from release.version_info import VERSION, RELEASE_NAME, COVERAGE_REPAIR_RELEASE, COVERAGE_REPAIR_AVAILABLE
    # Application version is now 1.3.1 (bumped from 1.3.0); v1.1.2 Coverage Repair functionality must still be present
    assert VERSION in ("1.3.0", "1.3.1"), f"Expected 1.3.x, got {VERSION}"
    assert COVERAGE_REPAIR_RELEASE is True, "COVERAGE_REPAIR_RELEASE flag must be True"
    assert COVERAGE_REPAIR_AVAILABLE is True, "COVERAGE_REPAIR_AVAILABLE flag must be True"


def run_all() -> int:
    tests = [
        ("package_import",                  test_package_import),
        ("schema_import",                   test_schema_import),
        ("task_builder_invalid_blocked",    test_task_builder_invalid_is_blocked),
        ("task_builder_conflict_manual",    test_task_builder_conflict_is_manual_review),
        ("task_builder_missing_source_req", test_task_builder_missing_is_source_required),
        ("task_builder_duplicate_auto",     test_task_builder_duplicate_is_auto_safe),
        ("executor_dry_run_default",        test_executor_dry_run_default),
        ("executor_invalid_always_blocked", test_executor_invalid_always_blocked),
        ("executor_conflict_always_manual", test_executor_conflict_always_manual),
        ("health_check_pass",               test_health_check_pass),
        ("onboarding_v111_intact",          test_onboarding_v111_intact),
        ("version_info_112",                test_version_info_112),
    ]

    print("=" * 60)
    print("TW Quant Cockpit — Coverage Repair Regression v1.1.2")
    print("[!] Research Only. No Real Orders. Fixtures only.")
    print("=" * 60)

    results = []
    for label, fn in tests:
        r = _run(label, fn)
        results.append(r)

    total  = len(results)
    passed = results.count(PASS)
    failed = results.count(FAIL)
    warned = results.count(WARN)

    print()
    print(f"Total:  {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    overall = PASS if failed == 0 else FAIL
    print(f"Overall: {overall}")
    print("[!] Research Only. No Real Orders.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())
