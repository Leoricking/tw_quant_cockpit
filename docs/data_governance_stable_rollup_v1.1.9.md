# Data Governance Stable Rollup v1.1.9

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] No Auto Store Repair. No Auto Data Repair. No Auto Download. No Auto Import.
> [!] No Auto Research Execution. No Trade Execution. Not Investment Advice.

---

## Goals

v1.1.9 is the stable rollup for the entire v1.1.x Data Governance line. It adds:

1. **Cross-Module Consistency** — verifies version flags, schema contracts, and safety guards across all v1.1.x modules
2. **Schema & Qualification Normalization** — normalizes schema fields and qualification labels (FORMAL/OBSERVATIONAL/BLOCKED) for consistency
3. **Cross-Machine Path Normalization** — produces portable relative paths so governance stores work across computers
4. **Store Inventory & Validation** — enumerates all runtime stores, validates record counts, schema versions, and audit chains
5. **Corrupted Tail Recovery (Dry Run)** — detects and previews recovery plans for stores with corrupted tail records (no auto-execute)
6. **Index Rebuild** — rebuilds lookup indexes for governance stores (preview by default; --execute --allow-write required to apply)
7. **Metadata Migration** — migrates legacy schema fields to current format (preview by default; --execute --allow-write required to apply)
8. **Health Aggregation** — aggregates per-module health into a single governance health matrix
9. **CLI/GUI/Docs Surface Audits** — verifies command coverage, tab completeness, and doc coverage
10. **Final Reports** — governance rollup report with comparison across runs

---

## v1.1.x Architecture Summary

| Version | Module             | Key Feature                                     |
|---------|--------------------|-------------------------------------------------|
| v1.1.0  | universe/          | Data Universe Expansion, tier registry          |
| v1.1.1  | import_onboarding/ | Data Import UX & Batch Onboarding               |
| v1.1.2  | coverage_repair/   | Coverage Repair Workflow (dry_run=True default) |
| v1.1.3  | data_freshness/    | Data Freshness Monitor, SLA tracking            |
| v1.1.4  | quality_gates/     | Coverage Quality Gates (FORMAL/OBSERVATIONAL)   |
| v1.1.5  | gate_enforcement/  | Quality Gate Enforcement & Audit                |
| v1.1.6  | governance_ops/    | Data Governance Operations Dashboard            |
| v1.1.7  | governance_alerts/ | Governance Alerts & Daily Operations            |
| v1.1.8  | research_registry/ | Research Run Registry                           |
| v1.1.9  | governance_rollup/ | Data Governance Stable Rollup (this release)    |

---

## Schema Normalization

The `GovernanceSchemaNormalizer` normalizes field names across all governance stores:

- `run_id` / `run-id` / `runId` → `run_id`
- `ts` / `timestamp` / `created_at` → `ts`
- Qualification labels: `FORMAL` / `formal` / `FORMAL_BACKTEST` → `FORMAL`
- Status labels: `PASS` / `pass` / `passed` → `PASS`

Normalization is **read-only** — it produces normalized views without modifying stored files.

---

## Qualification Consistency

The `CrossModuleConsistencyChecker` verifies that qualification labels are consistent across modules. A run registered as `FORMAL` in the research registry must have a corresponding FORMAL gate pass in gate_enforcement.

---

## Cross-Machine Path Normalization

The `CrossMachinePathNormalizer` produces portable relative paths:

- Converts absolute paths to relative form (`data/governance_rollup/...`)
- Paths are resolved relative to the repo root `BASE_DIR`
- Cross-machine portability: paths stored in governance stores will work on any machine that has the same repo structure

---

## Store Inventory & Validation

The `GovernanceStoreInventory` enumerates all governance runtime stores:

- `data/governance_ops/` — governance operations
- `data/governance_alerts/` — alert history
- `data/research_registry/` — research run registry
- `data/quality_gate_enforcement/` — gate enforcement
- `data/coverage_repair_results/` — repair results
- `data/freshness_reports/` — freshness snapshots

The `GovernanceStoreValidator` validates each store:

- Schema version check
- Record count check (empty store = WARN)
- Audit chain integrity check
- No future-date records allowed

---

## Corrupted Tail Recovery (Dry Run)

The `GovernanceStoreRecoveryPlanner`:

1. Detects stores with corrupted tail records (truncated JSONL, invalid JSON, schema mismatch)
2. Generates a recovery plan (plan_id, affected records, proposed action)
3. **Preview only** — no store modification without `--allow-write`
4. Execute requires: `governance-store-recovery-execute --plan-id <id> --allow-write`

Safety: recovery execution is gated by `--allow-write` flag. Default is preview-only.

---

## Index Rebuild

The `GovernanceIndexRebuilder` rebuilds lookup indexes for governance stores:

- Research registry run_id index
- Gate enforcement run index
- Governance ops action queue index
- Alert dedup index

**Default**: preview only.
**Execute**: requires `--execute --allow-write`.

---

## Metadata Migration

The `GovernanceMetadataMigrator` migrates legacy schema fields:

- Detects fields from prior schema versions
- Generates a migration plan with field mapping
- **Default**: preview only.
- **Execute**: requires `--execute --allow-write`.

---

## Consistency Checker

The `CrossModuleConsistencyChecker` verifies:

1. Version flags across all v1.1.x `__init__.py` files
2. Safety flags: `NO_REAL_ORDERS`, `BROKER_DISABLED`, `TRADE_EXECUTION_ENABLED=False`
3. Schema contract: required fields present in each store's schema
4. Qualification label consistency: FORMAL runs have gate pass evidence

---

## Health Aggregation

The `GovernanceHealthAggregator` builds a health matrix:

- Per-module health status (PASS/WARN/FAIL/UNKNOWN)
- Overall governance health (worst-case aggregation)
- History trend (last 7 rollup runs)

---

## Stable Freeze Criteria

v1.1.9 is considered stable when:

1. `governance-rollup-health` → PASS
2. `governance-rollup-consistency` → PASS (zero FAIL)
3. `governance-rollup-store-validate` → PASS (zero FAIL)
4. `stable-v060-check --mode real` → PASS
5. `safety-scan --target all` → no forbidden actions
6. All safety flags confirmed: `NO_REAL_ORDERS=True`, `TRADE_EXECUTION_ENABLED=False`

---

## CLI Standard Operating Procedure

### Daily health check

```bash
python main.py governance-rollup-health
python main.py governance-rollup-consistency
python main.py governance-rollup-health-matrix
```

### Store validation

```bash
python main.py governance-rollup-store-inventory
python main.py governance-rollup-store-validate
python main.py governance-rollup-audits
```

### Path portability check (before pushing to another machine)

```bash
python main.py governance-rollup-paths
```

### Index and migration preview

```bash
python main.py governance-index-rebuild --module research_registry --dry-run
python main.py governance-metadata-migrate --module research_registry --dry-run
```

### Recovery preview (for store issues)

```bash
python main.py governance-store-recovery-preview --store-id <store_id>
```

### Full rollup run

```bash
python main.py governance-rollup-run
python main.py governance-rollup-summary
python main.py governance-rollup-report
```

---

## GUI Standard Operating Procedure

1. Open TW Quant Cockpit → Data tab → **Governance Rollup** tab
2. Review Overall Health (PASS/WARN/FAIL)
3. Check Module Health Matrix — any RED module needs attention
4. Review Store Inventory — any empty or corrupted store is highlighted
5. Check Consistency section — any FAIL requires manual investigation
6. Review recovery plans and migration plans (all preview-only)

---

## Dual-Computer Workflow

When syncing between computers:

1. On source machine: `python main.py governance-rollup-paths` — verify all paths are portable
2. Commit and push governance module code only (not `data/governance_rollup/`)
3. On target machine: pull and run `python main.py governance-rollup-store-inventory` to rebuild
4. Run `python main.py governance-rollup-health` to verify

Note: `data/governance_rollup/` is excluded from git (see `.gitignore`). Only source code and fixtures are committed.

---

## Safety Guarantees

| Guarantee                              | Value  |
|----------------------------------------|--------|
| `NO_REAL_ORDERS`                       | True   |
| `BROKER_DISABLED`                      | True   |
| `AUTO_STORE_REPAIR_ENABLED`            | False  |
| `AUTO_DATA_REPAIR_ENABLED`             | False  |
| `AUTO_DATA_DOWNLOAD_ENABLED`           | False  |
| `AUTO_DATA_IMPORT_ENABLED`             | False  |
| `AUTO_RESEARCH_EXECUTION_ENABLED`      | False  |
| `AUTO_RESEARCH_RERUN_ENABLED`          | False  |
| `TRADE_EXECUTION_ENABLED`              | False  |

**No Real Orders. Not Investment Advice.**
