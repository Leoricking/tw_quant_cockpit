# TW Quant Cockpit v1.3.3 — Coverage Repair Workflow

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] dry_run=True default. Destructive repair DISABLED.
> [!] Auto Execution DISABLED. Conflict resolution is MANUAL.
> [!] No mock fallback. DEMO_ONLY_DATA cannot be converted to REAL data.
> [!] Not Investment Advice.

---

## Overview

The Coverage Repair Workflow (v1.3.3) provides a structured, audit-friendly system for:

1. Detecting coverage and quality issues in the data universe
2. Building prioritized repair task queues
3. Planning safe, read-only repair actions
4. Executing approved repair actions (read-only, dry-run default)
5. Tracking resolution status and provenance

**Safety invariants:**
- `no_real_orders = True` — no trading
- `production_trading_blocked = True` — always
- `destructive = False` — always
- `auto_retry_allowed = False` — always false by default
- `COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED = False`
- `COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED = False`
- `COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED = False`

---

## Architecture

### Core Modules

| Module | Class | Purpose |
|--------|-------|---------|
| `coverage_repair/models_v133.py` | `CoverageRepairTask`, `RepairPlan`, `RepairExecutionResult` | Rich data models |
| `coverage_repair/issue_mapper.py` | `CoverageRepairIssueMapper` | Maps raw signals to tasks |
| `coverage_repair/priority_engine.py` | `CoverageRepairPriorityEngine` | Deterministic priority scoring |
| `coverage_repair/queue.py` | `CoverageRepairQueue` | In-memory + JSON task queue |
| `coverage_repair/planner.py` | `CoverageRepairPlanner` | Builds dry-run repair plans |
| `coverage_repair/executor.py` | `CoverageRepairExecutor` | Safe plan execution |
| `coverage_repair/store.py` | `CoverageRepairStore` | Versioned JSON persistence |
| `coverage_repair/query.py` | `CoverageRepairQueryService` | Read-only query interface |
| `coverage_repair/health.py` | `CoverageRepairHealthV133` | Health checks |
| `coverage_repair/report.py` | `CoverageRepairReport` | Report generation |

---

## Issue Types

| Issue Type | Description | Suggested Actions |
|------------|-------------|-------------------|
| `MISSING_DATA` | Data completely absent | `REFRESH_PROVIDER`, `WAIT_FOR_SOURCE` |
| `PARTIAL_DATA` | Incomplete data | `REFRESH_PROVIDER`, `RETRY_PROVIDER` |
| `STALE_DATA` | Data outdated | `REFRESH_PROVIDER`, `REBUILD_CACHE` |
| `BLOCKED_DATA` | Access blocked | `MANUAL_REVIEW`, `NO_SAFE_ACTION` |
| `UNAVAILABLE_SOURCE` | Source unavailable | `WAIT_FOR_SOURCE`, `ENABLE_CONFIGURED_PROVIDER` |
| `SOURCE_CONFLICT` | Conflicting sources | `REVIEW_SOURCE_CONFLICT` (manual) |
| `DEMO_ONLY_DATA` | Demo data in real profile | `NO_SAFE_ACTION` (BLOCKED) |
| `INVALID_SCHEMA` | Schema mismatch | `FIX_SCHEMA`, `MANUAL_REVIEW` |
| `CACHE_STALE` | Cache needs refresh | `REBUILD_CACHE`, `INVALIDATE_CACHE` |
| `CACHE_CORRUPTION` | Cache corrupted | `INVALIDATE_CACHE`, `REBUILD_CACHE` |
| `INSUFFICIENT_HISTORY` | Not enough history | `EXTEND_HISTORY` |
| `PROVIDER_AUTH_REQUIRED` | Auth needed | `REQUEST_AUTH_CONFIGURATION` |
| `PROVIDER_RATE_LIMITED` | Rate limited | `WAIT_FOR_RATE_LIMIT` |
| `MARKET_CONFLICT` | Market data conflict | `REVIEW_MARKET_CONFLICT` (manual) |
| `DUPLICATE_BAR` | Duplicate OHLCV bars | `MANUAL_REVIEW`, `REVALIDATE_QUALITY` |

---

## Task Status Lifecycle

```
OPEN -> PLANNED -> READY_TO_RETRY -> IN_PROGRESS -> RESOLVED (terminal)
     -> BLOCKED -> OPEN (reopen)
     -> CONFLICT_REVIEW -> OPEN / IN_PROGRESS
     -> WAITING_SOURCE -> READY_TO_RETRY
     -> WAITING_AUTH -> READY_TO_RETRY
     -> WAITING_RATE_LIMIT -> READY_TO_RETRY
     -> IN_PROGRESS -> REVALIDATING -> RESOLVED / PARTIALLY_RESOLVED
     -> FAILED -> OPEN / READY_TO_RETRY
     -> CANCELLED (terminal) -> OPEN (reopen only)
     -> IGNORED -> OPEN (reopen only)
```

Terminal states: `RESOLVED`, `CANCELLED`

---

## Priority Scoring

Scores are deterministic and bounded to [0, 100].

| Priority | Score Range | Examples |
|----------|-------------|---------|
| CRITICAL | 80-100 | SOURCE_CONFLICT, BLOCKED_DATA in backtest profile, DEMO_ONLY in precise_price |
| HIGH | 60-79 | CORE tier STALE_DATA, INSUFFICIENT_HISTORY, PROVIDER_AUTH_REQUIRED |
| MEDIUM | 40-59 | RESEARCH tier missing data, CACHE_STALE, PARTIAL_DATA in research |
| LOW | 0-39 | EXTENDED tier optional, EXCLUDED tier |

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `coverage-repair-list` | List all tasks in queue |
| `coverage-repair-show --task-id <id>` | Show task details |
| `coverage-repair-summary` | Queue summary |
| `coverage-repair-scan [--tier] [--symbol] [--profile]` | Scan for issues |
| `coverage-repair-plan [--task-id] [--symbol]` | Build dry-run plan |
| `coverage-repair-run --task-id <id> [--dry-run] [--execute]` | Run repair |
| `coverage-repair-retry --task-id <id>` | Retry retryable task |
| `coverage-repair-revalidate --task-id <id>` | Revalidate quality |
| `coverage-repair-resolve --task-id <id>` | Mark as resolved |
| `coverage-repair-ignore --task-id <id>` | Mark as ignored |
| `coverage-repair-reopen --task-id <id>` | Reopen task |
| `coverage-repair-history [--task-id <id>]` | View history events |
| `coverage-repair-health` | Run health checks |

---

## Safe vs Manual Actions

### Safe Auto Actions (no human required)
- `REFRESH_PROVIDER` — fetch from provider (read-only)
- `RETRY_PROVIDER` — retry provider request
- `REBUILD_CACHE` — rebuild from existing source
- `INVALIDATE_CACHE` — clear stale cache entries
- `RECALCULATE_INDICATORS` — recalculate technical indicators
- `REVALIDATE_QUALITY` — rerun quality validation
- `RECALCULATE_COVERAGE` — rerun coverage calculation

### Manual Required
- `REVIEW_SOURCE_CONFLICT` — human must resolve source conflict
- `REVIEW_MARKET_CONFLICT` — human must resolve market conflict
- `REQUEST_AUTH_CONFIGURATION` — operator must configure credentials
- `FIX_SCHEMA` — operator must correct schema
- `MARK_UNSUPPORTED` — human decides capability is unsupported
- `MARK_EXCLUDED` — human decides to exclude symbol
- `MANUAL_REVIEW` — catch-all for human judgment

### Never Allowed
- Any trading action: BUY, SELL, ORDER, SUBMIT_ORDER, AUTO_TRADE, BROKER_LOGIN, EXECUTE_TRADE
- Creating fake/mock data to fill gaps
- Auto-overwriting source conflicts
- Auto-deleting history
- Auto-rebuilding entire database

---

## RESOLVED Conditions

A task is RESOLVED only when ALL of the following are true:
1. Provider action completed successfully
2. DQ profile passes for the symbol/profile
3. Coverage status is not blocking
4. `blocking_reason` is empty
5. No new CRITICAL issues detected
6. No Mock fallback was used
7. Provenance is complete (provider_id, data_mode, fetched_at)

If provider succeeds but data is still insufficient → `PARTIALLY_RESOLVED` or stay `OPEN`.

---

## Safety Flags

```python
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED = False
COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED = False
COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED = False
```

---

## Version

- **Version:** 1.3.3
- **Release Name:** Coverage Repair Workflow
- **Base Release:** 1.3.2 Real Data Provider Adapter Foundation
- **Replay Stable Baseline:** 1.2.9

---

_[!] Research Only. Not Investment Advice. No Real Orders. Production Trading BLOCKED._
