# Data Governance Operations Dashboard — v1.1.6

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> Auto Repair DISABLED. Auto Download DISABLED. Trade Execution DISABLED.

## Overview

v1.1.6 adds the Data Governance Operations Dashboard — a unified view of data health, module status, action queue, and daily governance history across all data tiers. It integrates the outputs of all prior v1.1.x releases (universe expansion, import onboarding, coverage repair, freshness monitor, quality gates, gate enforcement) into a single read-only operations surface.

**Key capabilities:**

- Multi-module health aggregation (8 governance adapters)
- Per-symbol governance status matrix (coverage + freshness + gate + repair status)
- Prioritized action queue (P0/P1/P2/P3, metadata-only — no data modification)
- Daily governance history (append-only JSONL, never overwritten)
- Run audit summary (gate enforcement pass/fail, bypass = 0 enforced)
- CLI commands: `governance-health`, `governance-dashboard`, `governance-summary`, `governance-module-health`, `governance-symbols`, `governance-symbol`, `governance-actions`, `governance-top-actions`, `governance-source-health`, `governance-gate-summary`, `governance-audit-summary`, `governance-runs`, `governance-history`, `governance-report`, `governance-compare`, `governance-action-ack`, `governance-action-defer`, `governance-action-resolve`
- GUI: Governance Ops tab in Dashboard (PySide6)
- Reports: `data_governance_operations_report`, `governance_action_queue_report`, `governance_module_health_report`, `governance_audit_summary_report`

## Priority Levels

| Priority | Trigger Condition |
|---|---|
| P0 | Missing data + blocked_invalid simultaneously |
| P1 | Stale data, SLA breach, or source interruption |
| P2 | Gate blocked, conflicted data, or repair needed |
| P3 | Audit warning, download needed, or low severity |

Priority is based **only on data governance issues** — never on price movements, trading signals, or market conditions.

## Action Queue Operations

Actions are **metadata-only**. No data is modified by acknowledging, deferring, or resolving an action.

| Operation | CLI Command | Effect |
|---|---|---|
| Acknowledge | `governance-action-ack --action-id <id>` | Status → acknowledged, audit event appended |
| Defer | `governance-action-defer --action-id <id> --reason <reason>` | Status → deferred, audit event appended |
| Resolve | `governance-action-resolve --action-id <id> --note <note>` | Status → resolved, audit event appended |

## Module Health Statuses

| Status | Meaning |
|---|---|
| HEALTHY | Module available and all checks pass |
| DEGRADED | Module available but some checks warn or fail |
| UNAVAILABLE | Module could not be imported |
| UNKNOWN | Module health could not be determined |

## Safety Flags

```python
GOVERNANCE_AUTO_REPAIR_ENABLED     = False   # never auto-modifies data
GOVERNANCE_AUTO_DOWNLOAD_ENABLED   = False   # never auto-fetches external data
GOVERNANCE_GATE_OVERRIDE_ENABLED   = False   # never bypasses quality gates
GOVERNANCE_TRADE_EXECUTION_ENABLED = False   # never enables trading
NO_REAL_ORDERS                     = True
RESEARCH_ONLY                      = True
```

## Quick Start

```bash
# Run governance health check
python main.py governance-health

# Show full dashboard (research30 tier)
python main.py governance-dashboard --tier research30

# Show action queue (open P0/P1 only)
python main.py governance-actions --priority P0
python main.py governance-actions --priority P1

# Show per-symbol detail
python main.py governance-symbol --stock 2330

# Generate Markdown report
python main.py governance-report --tier research30 --report-dir reports
```

## Runtime Store

All runtime outputs are stored under `data/governance_ops/` and are excluded from git (`.gitignore`):

| File | Description |
|---|---|
| `governance_summary.json` | Latest dashboard summary |
| `module_health.csv` | Module health table |
| `symbol_status.csv` | Per-symbol status matrix |
| `action_queue.csv` | Current action queue |
| `action_audit.jsonl` | Append-only action audit log |
| `enforcement_runs.csv` | Gate enforcement run history |
| `audit_summary.csv` | Audit summary table |
| `daily_history.jsonl` | Append-only daily snapshots |
| `dashboard_state.json` | Last GUI state |

Test fixtures are committed to `tests/fixtures/governance_ops/`.

---
*[!] Research Only. No Real Orders. Not Investment Advice. Auto Repair DISABLED. Trade Execution DISABLED.*
