# Quality Gate Enforcement & Audit — v1.1.5

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> FORMAL eligible does NOT enable trading. VALIDATED does NOT mean tradable.

## Overview

v1.1.5 adds run-level quality gate enforcement with immutable audit logging, reproducibility hashing, and a GUI enforcement panel. It extends the Coverage Quality Gates (v1.1.4) into a full enforcement layer.

**Key capabilities:**

- Symbol-level gate filtering (FORMAL / OBSERVATIONAL / DEMO / BLOCKED)
- Immutable audit log with hash chain
- Run snapshots (gate state at run time — no secrets/tokens)
- Reproducibility hashes (SHA-256, canonical JSON, same payload = same hash)
- Research-only override auditing (disabled by default)
- CLI commands: `gate-enforcement-health`, `gate-enforcement-preview`, `gate-enforcement-run`, `gate-enforcement-policy`, `gate-enforcement-audit-query`, `gate-enforcement-audit-verify`, `gate-enforcement-snapshot`, `gate-enforcement-hash`, `gate-enforcement-runs`, `gate-enforcement-compare`, `gate-enforcement-report`
- GUI: Quality Gate Enforcement tab in Dashboard
- Reports: `quality_gate_enforcement_audit_report`, `gate_run_summary_report`, `gate_exclusion_summary_report`, `gate_reproducibility_summary_report`

## Gate Decision Levels

| Decision | Formal Run | Observational Run | Demo Run |
|---|---|---|---|
| ELIGIBLE_FORMAL | Included | Included | Included |
| ELIGIBLE_OBSERVATIONAL | **Excluded** | Included | Included |
| DEMO_ONLY | **Excluded** | **Excluded** | Included |
| BLOCKED_INVALID | **Excluded** | **Excluded** | **Excluded** |
| BLOCKED_CONFLICT | **Excluded** | **Excluded** | **Excluded** |
| BLOCKED_FUTURE_DATE | **Excluded** | **Excluded** | **Excluded** |

> Formal eligible does NOT enable trading. All modes are research-only.

## Gate Quality Modes

- `enforce` (default): Filter symbols by gate decision
- `audit_only`: Log gate decisions but preserve all symbols; warning appended
- `off`: No gate filtering; non-qualified symbols labeled, not removed
- `auto`: Engine selects mode by command

## CLI Usage

```bash
# Health check
python main.py gate-enforcement-health

# Preview policy for a command
python main.py gate-enforcement-preview --command validate-score

# Run enforcement for a symbol list
python main.py gate-enforcement-run --command validate-score \
    --symbols 2330 2454 --quality-gate PRICE_BACKTEST_GATE --gate-mode enforce

# List policy mappings
python main.py gate-enforcement-policy

# Query audit log
python main.py gate-enforcement-audit-query

# Verify audit chain
python main.py gate-enforcement-audit-verify

# Get run snapshot
python main.py gate-enforcement-snapshot --run-id <run_id>

# Get reproducibility hash
python main.py gate-enforcement-hash --run-id <run_id>

# List recent enforcement runs
python main.py gate-enforcement-runs --limit 20

# Compare two runs
python main.py gate-enforcement-compare --run-id-a <run_a> --run-id-b <run_b>

# Build audit report
python main.py gate-enforcement-report
```

## --quality-gate Flag on Existing Commands

The `--quality-gate` and `--gate-mode` flags are available on:

- `validate-score`
- `backtest-buy-points`
- `backtest-screener`
- `backtest-strategy-knowledge`

Example:

```bash
python main.py validate-score --symbols 2330 2454 \
    --quality-gate PRICE_BACKTEST_GATE --gate-mode enforce
```

## Gate Names

| Gate Name | Default Command |
|---|---|
| PRICE_BACKTEST_GATE | validate-score, backtest-buy-points |
| BUY_POINT_GATE | backtest-buy-points |
| SCREENER_GATE | backtest-screener |
| STRATEGY_KNOWLEDGE_GATE | backtest-strategy-knowledge |
| STOCK_REPORT_GATE | stock-report (research) |
| LOCAL_ASSISTANT_GATE | local-assistant |
| KB_CONTEXT_GATE | kb-search |

## Override Policy

Override is disabled by default (`QUALITY_GATE_BYPASS_ALLOWED=False`).

To use an explicit research override:

```bash
python main.py gate-enforcement-run --command validate-score \
    --symbols 2330 --allow-research-override --override-id "manual-override-001"
```

Override requirements:
- `--allow-research-override` must be set explicitly
- `--override-id` must be provided
- Override is audited and cannot enable trading

## Audit Log

The audit log is append-only JSONL at `data/quality_gate_audit/enforcement_audit.jsonl`.

Each event includes:
- `event_id`, `run_id`, `event_type`, `timestamp`
- `immutable_hash` (SHA-256 of event payload)
- `chain_prev_hash` (hash of preceding event, forming a chain)

Audit failure raises `RuntimeError` — it is never silent.

## Reproducibility Hash

The reproducibility hash is SHA-256 of canonical JSON (stable key sort). Same symbols + same gate decisions + same arguments = same hash across runs.

Saved to `data/quality_gate_enforcement/run_hashes.csv`.

## Run Snapshot

Captures gate state at run time:
- Coverage decisions, freshness status, repair status, onboarding status
- Does NOT capture secrets, tokens, or credentials

Saved to `data/quality_gate_enforcement/run_snapshots.jsonl`.

## Safety

- `NO_REAL_ORDERS = True`
- `BROKER_DISABLED = True`
- `RESEARCH_ONLY = True`
- `PRODUCTION_TRADING_BLOCKED = True`
- `QUALITY_GATE_BYPASS_ALLOWED = False`
- `MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED = False`

FORMAL eligibility does NOT enable trading. VALIDATED does NOT mean tradable.

## Architecture

```
gate_enforcement/
  __init__.py              — package init with safety constants
  enforcement_schema.py    — dataclasses: GateEnforcementRequest, GateEnforcementResult,
                             SymbolExclusionRecord, RunGateSnapshot, EnforcementAuditEvent
  enforcement_policy.py    — QualityGateEnforcementPolicy: command->gate mapping
  run_gate_resolver.py     — RunGateResolver: parse CLI args to GateEnforcementRequest
  symbol_filter.py         — QualityGateSymbolFilter: include/exclude by level
  run_snapshot.py          — RunGateSnapshotBuilder: capture gate state at run time
  reproducibility.py       — RunReproducibilityHasher: SHA-256 canonical hash
  audit_log.py             — QualityGateAuditLog: append-only JSONL with hash chain
  enforcement_engine.py    — QualityGateEnforcementEngine: 10-step enforcement flow
  enforcement_store.py     — EnforcementStore: runtime CSV/JSONL output
  enforcement_query.py     — EnforcementQuery: query runs, snapshots, hashes, audit
  enforcement_health.py    — QualityGateEnforcementHealthCheck: 24 health checks
```

## Related

- [Coverage Quality Gates v1.1.4](coverage_quality_gates_v1.1.4.md)
- [Data Freshness Monitor v1.1.3](data_freshness_monitor_v1.1.3.md)
- [Coverage Repair Workflow v1.1.2](coverage_repair_workflow_v1.1.2.md)
- [Data Import UX & Batch Onboarding v1.1.1](data_import_onboarding_v1.1.1.md)

---

*v1.1.5 — Quality Gate Enforcement & Audit. Research Only. No Real Orders.*
