# Replay Training Maintenance Baseline v1.2.9

> **[!] Research Only. No Real Orders. Not Investment Advice.**
> **[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.**

---

## Purpose

This document defines the maintenance baseline for the Replay Training v1.2
line (v1.2.0–v1.2.9). It covers:

- Ongoing maintenance SOP for the stable rollup
- Health check runbook
- Dependency upgrade SOP
- Rollback SOP (to any v1.2.x)
- Known safe-to-modify vs. frozen zones
- Long-term maintenance readiness checklist

`LONG_TERM_MAINTENANCE_READY = True` as of v1.2.9.

---

## 1. Stable Rollup Freeze Boundary

The v1.2 Replay Training line is **complete** and **frozen** as of v1.2.9:

- **No new replay training features** will be added to this line.
- Bug fixes and dependency patches are the only permitted changes.
- All schema changes require a new minor version (v1.3.x).
- The future data firewall, process/outcome separation, and hidden outcome
  invariants are **hard-frozen** — no modification without a new major
  version review.

### Frozen Modules (no changes except critical bug fixes)

| Module | File | Freeze Status |
|--------|------|---------------|
| replay_foundation | replay/replay_schema.py | FROZEN |
| scenario_manager | replay/scenario_schema.py | FROZEN |
| session_manager | replay/session_schema.py | FROZEN |
| decision_journal | replay/decision_journal_schema.py | FROZEN |
| scoring_mistake_taxonomy | replay/scoring_schema.py | FROZEN |
| strategy_knowledge | replay/strategy_knowledge_schema.py | FROZEN |
| multi_timeframe | replay/multi_timeframe_schema.py | FROZEN |
| review_dashboard | replay/review_schema.py | FROZEN |
| challenge_mode | replay/challenge_schema.py | FROZEN |
| dataset_registry | replay/dataset_registry_schema.py | FROZEN |
| session_registry | replay/session_registry_schema.py | FROZEN |
| stable_rollup | replay/stable_*.py | FROZEN |

### Safe-to-Modify (documentation, reports, UI text)

- `docs/` — documentation updates do not affect schemas
- `reports/` — report templates may be updated without schema changes
- `gui/` display strings — cosmetic changes only, no behavioral change
- `tests/fixtures/replay_stable/` — fixture updates require version bump

---

## 2. Routine Health Check SOP

Run after every dependency change, OS upgrade, or environment change.

### Step 1 — Core Health Check

```
python main.py replay-stable-health
```

Expected: `FAIL: 0`. Any FAIL is a blocking issue.
WARN count should be reviewed but does not block maintenance.

### Step 2 — Legacy Module Health Checks

```
python main.py replay-health
python main.py replay-scenario-health
python main.py replay-session-health
python main.py replay-journal-health
python main.py replay-scoring-health
python main.py replay-strategy-health
python main.py replay-multitf-health
python main.py replay-review-health
python main.py replay-challenge-health
python main.py replay-dataset-health
python main.py replay-registry-health
```

All should return PASS or WARN. No FAIL.

### Step 3 — Contract and Compatibility Check

```
python main.py replay-stable-contracts
python main.py replay-stable-compatibility
```

### Step 4 — Safety Audit

```
python main.py replay-stable-safety-audit
```

Ensure all safety flags are correct. Any FAIL here is a critical issue.

### Step 5 — Regression Suite

```
python main.py regression-run --suite replay_stable --mode real
python main.py regression-run --suite quick --mode real
```

### Step 6 — Version Info

```
python main.py version-info
```

Confirm `VERSION = "1.2.9"`, `STABLE_ROLLUP = True`,
`REPLAY_TRAINING_LINE_COMPLETE = True`.

---

## 3. Dependency Upgrade SOP

When upgrading Python, pandas, numpy, or other dependencies:

1. Create a feature branch: `git checkout -b maintenance/deps-upgrade-YYYY-MM-DD`
2. Apply dependency changes.
3. Run `python -m compileall replay/ gui/ tests/` — must have 0 errors.
4. Run full health check SOP (Section 2 above).
5. Run `python -m pytest tests/test_replay_training_stable_rollup.py -v`
   — all tests must pass.
6. Run `python main.py research-cockpit-stable --mode real`
   — must return PASS.
7. Run `python main.py stable-v060-check --mode real`
   — must return PASS.
8. Merge to main only if all checks pass.
9. Do **not** increment VERSION for pure dependency upgrades that pass all
   checks. Increment VERSION only if a fix changes behavior.

### Forbidden During Dependency Upgrades

- Do not modify any schema `@dataclass` field names or types.
- Do not change `NO_REAL_ORDERS`, `RESEARCH_ONLY`, or any safety flag values.
- Do not add new imports to frozen modules.
- Do not change store JSONL format (append-only contract).

---

## 4. Rollback SOP

### Rollback to a Previous v1.2.x Tag

If a maintenance change introduces a regression, roll back to the previous
annotated tag.

```
git -C "C:/Users/Rossi/Documents/Claude/tw_quant_cockpit" tag --list "v1.2.*"
```

To roll back to v1.2.8:

```
git -C "C:/Users/Rossi/Documents/Claude/tw_quant_cockpit" checkout v1.2.8
```

Then create a new branch from that tag to investigate:

```
git -C "C:/Users/Rossi/Documents/Claude/tw_quant_cockpit" checkout -b fix/rollback-from-v1.2.9
```

### Data Store Compatibility

JSONL stores are append-only and backward compatible. Rolling back the code
to v1.2.8 does not corrupt v1.2.9 JSONL data — older code will simply ignore
fields it does not know. However:

- Do not roll back `dataset_registry_schema.py` if datasets were registered
  with v1.2.9 fingerprints — re-registration will be required.
- Session packages exported under v1.2.9 may not import cleanly under v1.2.7
  (session_registry did not exist in v1.2.7).

### Rollback Checklist

- [ ] Confirm target tag exists: `git tag --list "v1.2.*"`
- [ ] Check out the target tag or branch.
- [ ] Run `python main.py replay-health` on the rolled-back code.
- [ ] Run `python main.py version-info` and confirm expected VERSION.
- [ ] Run safety audit: `python main.py replay-stable-safety-audit` (if
  rolling back to v1.2.9) or the equivalent health check for the target
  version.
- [ ] Confirm `NO_REAL_ORDERS = True` and `REAL_ORDERS_ENABLED = False` in
  `release/version_info.py` on the rolled-back code.
- [ ] Document the rollback reason in the decision journal or commit message.

---

## 5. Adding a New Replay Training Feature (v1.3.x)

The v1.2 line is complete. New features must target v1.3.x.

When starting v1.3.x development:

1. Create branch: `git checkout -b feat/v1.3.0-description`
2. Update `VERSION = "1.3.0"` in `release/version_info.py`.
3. Set `STABLE_ROLLUP = False` until the new line is complete.
4. Add new schema files in `replay/` (do not modify v1.2 frozen schemas).
5. New schemas must include `NO_REAL_ORDERS = True`, `RESEARCH_ONLY = True`.
6. New features must not add broker connectivity, auto-decision, or
   auto-execution logic.
7. Update backward compatibility range when certifying v1.3.x rollup.

---

## 6. Long-Term Maintenance Readiness Checklist

The following criteria were verified at v1.2.9 freeze:

- [x] All 12 modules have import-based health checks (`health_command` field).
- [x] All 10 JSONL stores are append-only with documented paths.
- [x] All 16 capabilities are documented in the capability matrix.
- [x] Backward compatibility verified for v1.2.0–v1.2.8 (9 versions).
- [x] 16 cross-module contracts checked by `ReplayStableContractChecker`.
- [x] Safety audit covers all 13 required version_info flags.
- [x] Dangerous keyword scan covers all `.py` files in `replay/`.
- [x] Regression suite (`replay_stable`) has 17 test cases including
  expected_block semantics.
- [x] CLI audit verifies 24 commands in `main.py`.
- [x] GUI audit verifies 8 panel imports.
- [x] `.gitignore` excludes all runtime data directories and report outputs.
- [x] All fixture files use TST symbols and fixed clocks (no real data).
- [x] `LONG_TERM_MAINTENANCE_READY = True` in `release/version_info.py`.

---

## 7. Monitoring and Alerting

There is no automated monitoring or alerting in this system (research-only,
no production deployment). However, the following manual checks are
recommended:

| Frequency | Check |
|-----------|-------|
| After any code change | `python main.py replay-stable-health` |
| After dependency upgrade | Full SOP (Section 2) |
| Monthly | `python main.py replay-stable-safety-audit` |
| Before any release | `python main.py regression-run --suite release_gate --mode real` |
| Before any release | `python main.py research-cockpit-stable --mode real` |

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
