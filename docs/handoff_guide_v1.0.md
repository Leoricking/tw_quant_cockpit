# TW Quant Cockpit Handoff Guide v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Project Location

```
C:/Users/Rossi/Documents/Claude/trading_master
```

Current version: **v1.0.5 — Documentation & User Guide Polish**
Base version: **v1.0.0 — Research Trading Cockpit Stable**
Git user: Leoricking
Main branch: main

---

## Safety Constraints

| Constraint | Rule |
|------------|------|
| No real trading | This system is research-only. No broker API. No live orders. |
| No broker execution | BROKER_EXECUTION_ENABLED = False always |
| No auto trading | Production trading is explicitly blocked |
| VALIDATED grade | Research only — does not enable trading |
| Paper trading | Simulation only — not real orders |
| Mock realtime | Simulation only — not live data |

---

## Critical Development Rules

### 1. git -C Rule

Always use `git -C "path" command` format. Never use `cd path` then git.

Correct:
```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" status
git -C "C:/Users/Rossi/Documents/Claude/trading_master" log --oneline -5
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add release/version_info.py
```

Incorrect (do not use):
```
cd C:/Users/Rossi/Documents/Claude/trading_master
git status
```

### 2. No git add .

Always add files individually by name:

Correct:
```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add release/version_info.py
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add documentation/__init__.py
```

Incorrect (do not use):
```
git -C "..." add .
```

### 3. No Runtime Output Commits

Do NOT commit:
- `.csv` files (backtest results, manifests)
- `.json` files (state files, experiment outputs)
- `.md` report files (generated reports in reports/)
- `.db` files (SQLite databases)

These are all gitignored. Only commit source code, documentation, and configuration.

### 4. No Chain Commands

Do NOT use `&&`, `;`, `||`, or `|` to chain commands. Run each command separately.

Correct:
```
python main.py version-info
python main.py research-cockpit-stable --mode real
```

Incorrect (do not use — chain command operators are forbidden):
Run commands one at a time. Never join two commands with chain operators.

### 5. No Heredoc in Git Commit

Do NOT use heredoc (`<<EOF`) in git commit messages. Use multiple `-m` flags instead:

Correct:
```
git -C "..." commit -m "docs: update user guide v1.0.5" -m "Add user guide and safety guide."
```

Incorrect (do not use):
```
git -C "..." commit -m "$(cat <<EOF
message
EOF
)"
```

---

## Key CLI Smoke Tests

Run these before any release to verify the system is working:

```
python main.py version-info
python main.py research-cockpit-stable --mode real
python main.py stable-v060-check --mode real
python main.py safety-scan --target all
python main.py release-gate-health --mode real
python main.py regression-run --suite release_gate --mode real
python main.py mock-realtime --duration 10
python main.py paper
```

---

## Release Process Steps

1. Read the current `release/version_info.py`
2. Update VERSION and RELEASE_NAME
3. Add any new feature flags (e.g., DOCUMENTATION_POLISH_RELEASE = True)
4. Create new modules/files as needed
5. Update checklists (research_cockpit_stable_checklist, stable_release_checklist_v060, intelligence_stable_checklist)
6. Update regression suite (suite_registry.py)
7. Update report pack (report_registry.py, report_collector.py)
8. Update GUI navigation (tab_registry.py) with new keywords
9. Update .gitignore for new runtime outputs
10. Update docs/index.md, docs/roadmap.md, docs/release_notes_v1.0.md
11. Update README.md
12. Validate imports: `python -c "from release.version_info import VERSION; print(VERSION)"`
13. Run all smoke tests
14. Run regression suite
15. Run safety scan
16. Commit with individual file adds and multiple -m flags
17. Tag with `git -C "..." tag -a vX.X.X -m "vX.X.X: Release Name"`
18. Push: `git -C "..." push origin main`
19. Push tag: `git -C "..." push origin vX.X.X`
20. Verify: `git -C "..." log --oneline --decorate -5`

---

## How to Create Next Version Prompt

For each new version:
1. State the current state (VERSION, commit hash, test results)
2. List all files to create/modify with their full content or change description
3. List all validation commands to run
4. List the exact git commands for commit and tag
5. Specify safety constraints that must be maintained
6. List known WARNs that are acceptable

---

## Known Warnings (Acceptable)

| Warning | Classification |
|---------|---------------|
| cp950 encoding warning | KNOWN_CP950_WARNING — non-critical |
| paper_state.json missing | KNOWN_PAPER_SMOKE_WARNING — non-critical |
| ENV_LIMITED report status | KNOWN_REPORT_PACK_OPTIONAL — non-critical |
| no_real_orders flag check WARN | KNOWN_NO_REAL_ORDERS_FLAG_CHECK — known |

---

## What NOT To Do

- Do NOT add broker API integration
- Do NOT enable real order execution
- Do NOT add auto-trading logic
- Do NOT skip safety checks in releases
- Do NOT commit runtime outputs
- Do NOT use `git add .`
- Do NOT chain commands with `&&`
- Do NOT ignore BLOCKED status from safety scanner

---

## v1.0.6 Note — Templates Available

v1.0.6 adds workflow examples and templates. For handoff, use:
- `docs/templates/handoff_summary_template.md` — Fill in the handoff summary
- `docs/templates/release_prompt_template.md` — For release process rules

These templates enforce: `git -C "path"`, no chain commands, no `git add .`, no heredoc in commits.

---

*TW Quant Cockpit v1.1.0 — Data Universe Expansion — Research Only — Not Investment Advice*

---

## v1.0.9 Handoff Notes

- **v1.0 Maintenance Line: COMPLETE**
- Final rollup CLI: `python main.py final-rollup-health`
- Long-term maintenance SOP: see `docs/final_maintenance_rollup_v1.0.9.md`
- **[!] No Real Orders. No broker API. Not Investment Advice.**

---

## v1.1.0 Handoff Notes

- **Data Universe Expansion: COMPLETE** (commit `d38907f`, tag `v1.1.0`)
- 4 universe tiers: CORE_10 / RESEARCH_30 / EXPANDED_50 / BROAD_100
- New modules: `universe/universe_tier_registry.py`, `universe/universe_coverage.py`, `universe/universe_builder.py`, `universe/universe_health.py`, `universe/universe_store.py`, `universe/universe_query.py`, `universe/universe_schema.py`
- Universe health: `python main.py universe-health` → 16/16 PASS
- Coverage analysis: `python main.py universe-coverage --tier research30 --mode real`
- Real data required: `REAL_DATA_COVERAGE_REQUIRED=True`, `MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False`
- Full docs: `docs/data_universe_expansion_v1.1.0.md`, `docs/release_notes_v1.1.md`
- Next: v1.1.1 Data Import UX (do not proceed without explicit plan)
- **[!] No Real Orders. No broker API. Research Only. Not Investment Advice.**

---

## v1.1.1 Handoff Notes

- **Data Import UX & Batch Onboarding: COMPLETE** (commit `c0c2fb6`, tag `v1.1.1`)
- New package: `data_onboarding/` (12 modules)
- New GUI: `gui/import_onboarding_panel.py`, `gui/import_onboarding_adapter.py`
- New report: `reports/data_import_onboarding_report.py`
- New fixtures: `tests/fixtures/import_onboarding/*.csv` (6 files)
- Import health: `python main.py import-onboarding-health` → 18/19 PASS (1 optional WARN)
- Batch dry-run: `python main.py import-batch --path <dir> --dry-run`
- Full docs: `docs/data_import_onboarding_v1.1.1.md`, `docs/release_notes_v1.1.md`
- Safety: `dry_run=True` by default, `REPLACE_EXPLICIT` blocked, conflicts always → REVIEW
- **[!] No Real Orders. No broker API. DESTRUCTIVE_IMPORT_DISABLED=True. Not Investment Advice.**

## v1.1.2 Handoff Notes

- **Coverage Repair Workflow: COMPLETE** (tag `v1.1.2`)
- New package: `coverage_repair/` (repair_schema, issue_detector, task_builder, repair_prioritizer, repair_planner, safe_repair_executor, repair_validator, repair_store, repair_query, repair_health + existing modules)
- New GUI: `gui/coverage_repair_panel.py`, `gui/coverage_repair_adapter.py`
- New report: `reports/coverage_repair_report.py`
- New fixtures: `tests/fixtures/coverage_repair/*.csv` (8 files using TST1/TST2 symbols)
- New CLI: 13 commands (`coverage-repair-scan`, `-issues`, `-tasks`, `-plan`, `-run`, `-result`, `-unresolved`, `-source-required`, `-health`, `-report`, etc.)
- Coverage repair health: `python main.py coverage-repair-health` → should PASS
- Full docs: `docs/coverage_repair_workflow_v1.1.2.md`, `docs/release_notes_v1.1.md`
- Safety: `dry_run=True` by default, `INVALID OHLC` always BLOCKED, conflicts always MANUAL, `SYNTHETIC_PRICE_REPAIR_ENABLED=False`, `EXTERNAL_DATA_DOWNLOAD_ENABLED=False`
- Next: v1.1.3 Data Freshness Monitor (do not proceed without explicit plan)
- **[!] No Real Orders. No broker API. DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT=True. Not Investment Advice.**
