# Replay Dataset & Session Registry — v1.2.8

> [!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
> [!] All write operations require explicit preview + execute + --allow-write.

---

## Overview

v1.2.8 introduces a complete **Replay Dataset & Session Registry** system for the TW Quant Cockpit.

Key capabilities:
- **Dataset Catalog** — Register, version, fingerprint, qualify, validate, and archive replay datasets
- **Session Registry** — Register, bind, and track replay sessions with dataset bindings
- **Dataset Versioning** — Semantic versioning (MAJOR.MINOR.PATCH); frozen versions are immutable
- **Deterministic Fingerprinting** — SHA-256 path-independent fingerprints (excludes absolute paths, machine names, timestamps)
- **Dataset Lineage** — DAG-based parent/child lineage; cycle detection via DFS
- **Session Lineage** — root / fork / duplicate / challenge / import / restore types
- **Portable Packages** — RELATIVE_ONLY path mode; no secrets, no broker credentials
- **Registry Repair** — Preview by default; execute requires `--allow-write`
- **Audit Log** — Append-only JSONL audit trail

---

## Safety Invariants

| Flag | Value |
|------|-------|
| `NO_REAL_ORDERS` | `True` |
| `RESEARCH_ONLY` | `True` |
| `AUTO_DATASET_OVERWRITE_ENABLED` | `False` |
| `AUTO_DATASET_REPAIR_ENABLED` | `False` |
| `AUTO_SESSION_REBIND_ENABLED` | `False` |
| `AUTO_PACKAGE_IMPORT_ENABLED` | `False` |
| `AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED` | `False` |
| `AUTO_REGISTRY_REPAIR_ENABLED` | `False` |

---

## Dataset Qualification Levels

| Level | Description |
|-------|-------------|
| `VERIFIED_REAL` | Real data with verified point-in-time policy |
| `REAL_UNVERIFIED` | Real data, PIT policy not fully verified |
| `MOCK_DEMO_ONLY` | Mock/generated data — demo use only |
| `INSUFFICIENT` | Insufficient rows or coverage |
| `BLOCKED` | Mock contamination, future leak, or corrupted |
| `INCOMPATIBLE` | Incompatible schema or timeframe |

Rules:
- Mock datasets can **never** be `VERIFIED_REAL`
- Real datasets with mock contamination → `BLOCKED`
- Future data leak detected → `BLOCKED`
- Frozen datasets: any hash mismatch → `CORRUPTED` (no silent update)

---

## Dataset Lifecycle

```
ACTIVE → FROZEN (immutable) → ARCHIVED
       → MISSING
       → CORRUPTED (after freeze hash mismatch)
```

---

## Session Status

| Status | Description |
|--------|-------------|
| `ACTIVE` | Session in progress |
| `PAUSED` | Session paused |
| `COMPLETED` | Session completed (binding locked) |
| `ARCHIVED` | Session archived |
| `ORPHANED` | Dataset no longer available |
| `BLOCKED` | Binding blocked |
| `INSUFFICIENT` | Insufficient dataset qualification |

Rules:
- Session-Dataset binding locked after session creation
- `COMPLETED` sessions cannot be directly rebound
- Challenge attempts must inherit the challenge dataset binding

---

## CLI Commands

### Health
```bash
python main.py replay-registry-health
```

### Dataset Registry
```bash
python main.py replay-dataset-list
python main.py replay-dataset-search --query "TW50"
python main.py replay-dataset-show --dataset-id DS-001
python main.py replay-dataset-versions --dataset-id DS-001
python main.py replay-dataset-lineage --dataset-id DS-001
python main.py replay-dataset-register-preview --dataset-id DS-001
python main.py replay-dataset-register --dataset-id DS-001 --execute --allow-write
python main.py replay-dataset-validate --dataset-id DS-001
python main.py replay-dataset-integrity --dataset-id DS-001
python main.py replay-dataset-freeze-preview --dataset-id DS-001
python main.py replay-dataset-freeze --dataset-id DS-001 --execute --allow-write
python main.py replay-dataset-create-version-preview --dataset-id DS-001
python main.py replay-dataset-create-version --dataset-id DS-001 --execute --allow-write
```

### Session Registry
```bash
python main.py replay-session-registry-list
python main.py replay-session-registry-show --session-id SESS-001
python main.py replay-session-registry-search --query "SCN-001"
python main.py replay-session-bindings --session-id SESS-001
python main.py replay-session-lineage --session-id SESS-001
python main.py replay-session-bind-preview --session-id SESS-001 --dataset-id DS-001
python main.py replay-session-bind --session-id SESS-001 --dataset-id DS-001 --execute --allow-write
python main.py replay-session-rebind-preview --session-id SESS-001 --dataset-id DS-002
python main.py replay-session-rebind --session-id SESS-001 --dataset-id DS-002 --execute --allow-write
```

### Package (Import/Export)
```bash
python main.py replay-package-export-preview --dataset-id DS-001
python main.py replay-package-export --dataset-id DS-001 --execute --allow-write
python main.py replay-package-import-preview --package-path /path/to/package.zip
python main.py replay-package-import --package-path /path/to/package.zip --execute --allow-write
```

### Registry Maintenance
```bash
python main.py replay-registry-repair-preview
python main.py replay-registry-repair --execute --allow-write
python main.py replay-registry-audit
python main.py replay-dataset-summary
python main.py replay-session-registry-summary
python main.py replay-dataset-registry-report
python main.py replay-session-registry-report
python main.py replay-registry-integrity-report
```

---

## Storage Layout

```
data/replay_registry/
  datasets.jsonl           — dataset registry (append-only)
  sessions.jsonl           — session registry (append-only)
  session_bindings.jsonl   — session-dataset bindings (append-only)
  registry_audit.jsonl     — audit log (append-only)
```

---

## Package Safety

Packages must **never** contain:
- `.env` files
- API tokens or secrets
- Broker credentials (`shioaji`, `megabroker`)
- Absolute paths (only `RELATIVE_ONLY` path mode allowed)

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
