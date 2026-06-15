# Research Run Registry v1.1.8

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] Not Investment Advice.

---

## Overview

The Research Run Registry is an append-only, audit-chained registry for all research runs executed in the TW Quant Cockpit. It provides full lifecycle tracking, artifact cataloging, lineage graphs, duplicate detection, run comparison, and health checks.

**Key properties:**
- Append-only storage — no run is ever deleted or overwritten
- Immutable audit hash chain (SHA-256 prev_hash chaining) — tampering is detectable
- All registry failures are non-fatal — the underlying research command always proceeds
- Mock mode always results in `DEMO_ONLY` qualification
- Sensitive fields are always redacted before storage

---

## Run Lifecycle

```
CREATED → RUNNING → COMPLETED
                  → COMPLETED_WITH_WARNINGS
                  → BLOCKED
                  → FAILED
                  → CANCELLED
```

---

## Qualification Levels

| Level | Description |
|-------|-------------|
| `FORMALLY_QUALIFIED` | Passed all gate requirements, real data, clean git, full coverage |
| `OBSERVATIONAL_ONLY` | Real data but not all gate requirements met |
| `DEMO_ONLY` | Mock mode — always DEMO_ONLY regardless of other parameters |
| `NOT_QUALIFIED` | Failed or incomplete run |
| `BLOCKED` | Gate failure blocked execution |
| `UNKNOWN` | Qualification cannot be determined |

---

## Run Types

`BACKTEST`, `VALIDATION`, `SCREENER`, `REPORT`, `PREVIEW`, `GATE_ENFORCEMENT`, `GOVERNANCE`, `GOVERNANCE_ALERTS`, `DATA_IMPORT`, `DATA_REPAIR`, `DATA_FRESHNESS`, `QUALITY_GATE`, `PAPER_SIMULATION`, `MOCK_SIMULATION`, `SYSTEM_HEALTH`, `OTHER`

---

## Package Structure

```
research_registry/
  __init__.py            — exports + safety flags
  registry_schema.py     — ResearchRunRecord, RunArtifact, RunLineage, RunComparison, RegistrySummary
  run_classifier.py      — command → run_type and qualification mapping
  run_capture.py         — lifecycle methods + sensitive field redaction
  run_lineage.py         — ResearchRunLineageManager (cycle detection, tree traversal)
  artifact_catalog.py    — ArtifactCatalog (discover, register, checksum, validate)
  duplicate_detector.py  — RunDuplicateDetector (fingerprint, exact/near dup)
  run_comparator.py      — RunComparator (diff two runs, markdown render)
  registry_store.py      — RegistryStore (JSONL append, CSV index, atomic JSON state)
  registry_query.py      — RegistryQuery (30+ query methods)
  registry_engine.py     — ResearchRunRegistryEngine (orchestrates all components)
  registry_health.py     — ResearchRunRegistryHealthCheck (27 checks)
```

---

## Storage Layout

```
data/research_registry/
  runs.jsonl             — append-only full run history
  run_state.json         — latest state snapshot per run_id (atomic write)
  run_index.csv          — searchable index
  artifacts.jsonl        — artifact records
  artifact_index.csv     — artifact index
  lineage.jsonl          — lineage records
  comparisons.jsonl      — comparison records
  duplicate_index.csv    — duplicate map
  registry_summary.json  — aggregate summary
  registry_audit.jsonl   — immutable audit chain (never modified)
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `research-registry-health` | Run 27-check health suite |
| `research-registry-summary` | Registry aggregate summary |
| `research-runs` | List all runs (with optional filters) |
| `research-run --run-id ID` | Show single run detail |
| `research-run-artifacts --run-id ID` | List run artifacts |
| `research-run-lineage --run-id ID` | Show lineage tree |
| `research-run-verify --run-id ID` | Verify reproducibility hash |
| `research-run-duplicates` | List all detected duplicates |
| `research-run-duplicate-check --run-id ID` | Check if a run has duplicates |
| `research-run-compare --run-a ID --run-b ID` | Compare two runs |
| `research-run-search --query Q` | Search runs |
| `research-run-latest-successful` | Latest COMPLETED runs per type |
| `research-run-latest-formal` | Latest FORMALLY_QUALIFIED runs |
| `research-run-missing-artifacts` | Runs with missing artifact files |
| `research-registry-backfill --dry-run` | Preview backfill (dry-run always safe) |
| `research-registry-rebuild-index` | Rebuild all indexes from JSONL |
| `research-registry-report` | Build Markdown report |
| `research-registry-audit` | List audit events |
| `research-registry-audit-verify` | Verify audit hash chain integrity |

---

## Safety Invariants

| Flag | Value |
|------|-------|
| `NO_REAL_ORDERS` | `True` |
| `BROKER_DISABLED` | `True` |
| `RESEARCH_ONLY` | `True` |
| `REGISTRY_AUTO_RERUN_ENABLED` | `False` |
| `REGISTRY_AUTO_EXECUTION_ENABLED` | `False` |
| `REGISTRY_TRADE_EXECUTION_ENABLED` | `False` |

**Mock mode rule:** Any run with `mode="mock"` is always stored with `qualification=DEMO_ONLY`. This cannot be overridden.

**Backfill rule:** Backfill without explicit `allow_write=True` always results in `status=BLOCKED`. Default is `dry_run=True`.

**Registry failure rule:** If the registry fails to record a run, the underlying command still completes. The registry is non-fatal.

**Redacted fields:** `api_key`, `token`, `secret`, `password`, `cookie`, `authorization`, `bearer`, `private_key`, `access_key`, `secret_key` — always replaced with `[REDACTED]` before storage.

---

## Duplicate Detection

Duplicates are detected via a deterministic fingerprint: SHA-256 of canonical JSON of `{command_name, mode, tier, stock, included_symbols (sorted), gate_name, gate_policy_version, code_version, reproducibility_hash, snapshot_ids (sorted), arguments (sorted, normalized)}`.

- **Exact duplicate:** same fingerprint + same mode (mock vs real never count as exact duplicates)
- **Near duplicate:** ≥70% similarity score across key attributes

---

## Lineage

The lineage graph supports ROOT, CHILD, RERUN, DUPLICATE, DERIVED, REPORT_OF, VALIDATION_OF, GOVERNANCE_OF relations.

- Missing parent → WARN (non-fatal, registry continues)
- Cycles are detected via DFS and rejected
- Rerun does NOT overwrite the original run record
- Duplicate does NOT delete the duplicate run

---

## Health Checks

The `ResearchRunRegistryHealthCheck` runs 27 checks covering:
- Package and module import
- Schema, classifier, capture, lineage, artifact catalog, duplicate detector, comparator, store, query, engine
- Deterministic fingerprint (same inputs → same hash)
- Lineage cycle detection
- Artifact checksum computation
- Missing artifact graceful handling
- Append-only guarantee
- Audit chain validity
- Broken audit chain detection
- Argument redaction and secret exclusion
- Mock qualification enforcement
- Blocked run not counted as successful
- Auto-rerun, auto-execution, trade-execution all disabled
- Runtime output ignored from registry state
- No forbidden actions

---

## Test Fixtures

Located in `tests/fixtures/research_registry/`:

| File | Description |
|------|-------------|
| `formal_backtest.json` | Formally qualified backtest run |
| `observational_validation.json` | Observational-only validation |
| `demo_mock.json` | Mock mode → DEMO_ONLY |
| `blocked_run.json` | Gate-blocked run |
| `failed_run.json` | Failed run |
| `duplicate_run_a.json` | First of duplicate pair |
| `duplicate_run_b.json` | Exact duplicate of A |
| `near_duplicate.json` | Near-duplicate (~85% similarity) |
| `lineage_root.json` | Root of lineage tree |
| `lineage_child.json` | Child of lineage root |
| `lineage_cycle.json` | INVALID cycle — for cycle detection tests only |
| `missing_artifact.json` | Run with registered but missing artifact file |
| `artifact_sample.txt` | Sample artifact text file |
| `secret_arguments.json` | Redaction test fixture |
| `registry_audit_valid.jsonl` | Valid audit chain |
| `registry_audit_broken.jsonl` | Broken audit chain (tampered prev_hash) |
| `run_compare_a.json` | Comparison run A |
| `run_compare_b.json` | Comparison run B |

---

*TW Quant Cockpit v1.1.8 — Research Run Registry — Research Only — Not Investment Advice*
