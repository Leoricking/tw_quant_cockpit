# TW Quant Cockpit Release Notes v1.1.x

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] Not Investment Advice.

---

## v1.1.0 — Data Universe Expansion (2026-06-13)

### Summary

v1.1.0 是 v1.0.9 Final Maintenance Rollup 之後的第一個功能版本。專注於真實股票樣本擴充與 universe coverage 驗證，讓既有策略驗證、回測、篩選器的統計基礎更可信。

### New Modules

- `universe/universe_schema.py` — UniverseSymbol, UniverseDefinition, UniverseCoverageSummary dataclasses
- `universe/universe_tier_registry.py` — UniverseTierRegistry with CORE_10 / RESEARCH_30 / EXPANDED_50 / BROAD_100
- `universe/universe_builder.py` — UniverseBuilder: build_tier, intersect_with_real_data, validate_symbol
- `universe/universe_coverage.py` — UniverseCoverageAnalyzer: per-symbol OHLC/volume/chips/revenue coverage
- `universe/universe_health.py` — UniverseHealthCheck: ~16 safety checks
- `universe/universe_store.py` — UniverseStore: save/load registry and coverage CSVs
- `universe/universe_query.py` — UniverseQuery: list_tiers, list_symbols, summarize_tier
- `reports/data_universe_expansion_report.py` — DataUniverseExpansionReportBuilder (9-chapter Markdown)
- `gui/universe_panel.py` — optional PySide6 UniversePanel
- `gui/universe_adapter.py` — UniverseAdapter

### New CLI Commands

```bash
python main.py universe-build --tier core10
python main.py universe-build --tier research30
python main.py universe-build --tier expanded50
python main.py universe-summary
python main.py universe-summary --tier research30
python main.py universe-health
python main.py universe-coverage --tier research30
python main.py universe-symbol --stock 2454
python main.py universe-missing --tier research30
python main.py universe-report --tier research30 --mode real
```

### Modified Files

- `release/version_info.py` — VERSION="1.1.0", DATA_UNIVERSE_EXPANSION_RELEASE=True
- `backtest/stat_confidence.py` — Added `for_universe_coverage()` static method
- `gui/navigation/tab_registry.py` — Added data_universe tab
- `gui/dashboard.py` — Added UniversePanel import
- `report_pack/report_registry.py` — Added REPORT_DATA_UNIVERSE_EXPANSION
- `report_pack/report_collector.py` — Added universe patterns
- `release/research_cockpit_stable_checklist.py` — Added 5 checks (checks #65-69)
- `stable_release/stable_release_checklist_v060.py` — Added 3 checks (universe_import, real_mock_separation, v110)
- `intelligence_stable/intelligence_stable_checklist.py` — Added data_universe_v110_safe check
- `regression/suite_registry.py` — Added 10 universe test cases
- `.gitignore` — Added data/backtest_results/universe/, reports/data_universe_expansion_report_*.md

### Safety Guarantees

- No Real Orders
- Broker Execution Disabled
- Real Data Coverage Required
- Mock Data Formal Conclusion: DISABLED
- VALIDATED does not enable trading
- Not Investment Advice

### Notes

- v1.0.9 Final Maintenance Rollup preserved intact
- All existing CLI commands unchanged
- No strategy logic modified
- No broker API added

---

---

## v1.1.1 — Data Import UX & Batch Onboarding (2026-06-14)

### Summary

v1.1.1 adds a complete **Data Import UX & Batch Onboarding** system. Covers XQ Excel/CSV,
standard CSV, column auto-mapping, duplicate/conflict detection, safe merge planning, dry-run
validation, retry manifests, and universe coverage refresh integration.

### New Package: `data_onboarding/`

- `data_onboarding/__init__.py` — package safety flags
- `data_onboarding/onboarding_schema.py` — ImportPlan, ImportPlanItem, ImportResult, BatchImportSummary, RetryManifest dataclasses
- `data_onboarding/file_discovery.py` — ImportFileDiscovery
- `data_onboarding/schema_detector.py` — ColumnMappingDetector
- `data_onboarding/file_validator.py` — ImportFileValidator
- `data_onboarding/duplicate_detector.py` — DuplicateDetector
- `data_onboarding/import_planner.py` — ImportPlanner
- `data_onboarding/batch_executor.py` — BatchImportExecutor
- `data_onboarding/retry_manifest.py` — RetryManifestBuilder
- `data_onboarding/onboarding_store.py` — OnboardingStore
- `data_onboarding/onboarding_query.py` — OnboardingQuery
- `data_onboarding/onboarding_health.py` — OnboardingHealthCheck

### New Files

- `reports/data_import_onboarding_report.py` — DataImportOnboardingReportBuilder
- `gui/import_onboarding_adapter.py` — ImportOnboardingAdapter
- `gui/import_onboarding_panel.py` — ImportOnboardingPanel (PySide6 + stub)
- `tests/fixtures/import_onboarding/*.csv` — 6 fixture files
- `docs/data_import_onboarding_v1.1.1.md` — full documentation

### New CLI Commands

```bash
python main.py import-discover --path <dir>
python main.py import-preview --file <file>
python main.py import-validate --path <dir>
python main.py import-plan --path <dir>
python main.py import-batch --path <dir> [--dry-run] [--execute] [--allow-write]
python main.py import-retry-manifest [--output-dir data/import_reports]
python main.py import-onboarding-health
python main.py import-onboarding-report [--mode real|mock]
```

### Modified Files

- `release/version_info.py` — VERSION="1.1.1", DATA_IMPORT_ONBOARDING_RELEASE=True, DRY_RUN_DEFAULT=True, DESTRUCTIVE_IMPORT_DISABLED=True, CONFLICT_AUTO_OVERWRITE_ENABLED=False
- `main.py` — 7 new handlers + subparsers; --path added to import-plan
- `gui/navigation/tab_registry.py` — Added data_import_onboarding tab
- `gui/dashboard.py` — Added ImportOnboardingPanel import
- `report_pack/report_registry.py` — Added REPORT_DATA_IMPORT_ONBOARDING
- `report_pack/report_collector.py` — Added import onboarding patterns
- `release/research_cockpit_stable_checklist.py` — Added 5 checks
- `stable_release/stable_release_checklist_v060.py` — Added 3 checks
- `intelligence_stable/intelligence_stable_checklist.py` — Added data_import_onboarding_v111_safe
- `regression/suite_registry.py` — Added 8 import onboarding test cases
- `.gitignore` — Added onboarding report patterns + fixture exceptions

### Safety Guarantees

- dry_run=True by default
- REPLACE_EXPLICIT blocked by default
- Conflicts always → REVIEW (never auto-overwrite)
- No Real Orders
- Broker Execution Disabled
- Not Investment Advice

---

---

## v1.1.2 — Coverage Repair Workflow (2026-06-14)

### Summary

v1.1.2 adds a complete **Coverage Repair Workflow** on top of v1.1.1 Data Import UX & Batch
Onboarding. Detects 18 coverage issue types, builds prioritized repair tasks (P0–P3), supports
dry-run repair planning, safe metadata normalization, manual conflict review, source requirements
workflow, and before/after validation.

### New Package: `coverage_repair/`

- `coverage_repair/__init__.py` — package safety flags (NO_REAL_ORDERS, DRY_RUN_DEFAULT, etc.)
- `coverage_repair/repair_schema.py` — CoverageIssue, CoverageRepairTask, CoverageRepairPlan, CoverageRepairResult (18 issue types, 5 severities, 9 statuses, 5 repairabilities)
- `coverage_repair/issue_detector.py` — CoverageIssueDetector (detect_all, detect_for_tier, detect_for_symbol, etc.)
- `coverage_repair/task_builder.py` — CoverageRepairTaskBuilder (build_tasks, classify_repairability, build_source_requirement)
- `coverage_repair/repair_prioritizer.py` — CoverageRepairPrioritizer (score_task, prioritize, group_by_priority, group_by_symbol)
- `coverage_repair/repair_planner.py` — CoverageRepairPlanner (build_plan, list_source_requirements, list_manual_reviews)
- `coverage_repair/safe_repair_executor.py` — SafeCoverageRepairExecutor (execute, deduplicate_identical, normalize_schema, reimport_safe, refresh_coverage, rollback_task)
- `coverage_repair/repair_validator.py` — CoverageRepairValidator (capture_before, capture_after, compare_coverage, validate_task_result, validate_no_data_loss, validate_no_new_conflict, validate_no_mock_rows)
- `coverage_repair/repair_store.py` — RepairStore (save/load plan/summary/retry)
- `coverage_repair/repair_query.py` — RepairQuery (list_open_issues, list_tasks, list_blocked, list_source_required, compare_before_after)
- `coverage_repair/repair_health.py` — CoverageRepairHealthCheck (22+ checks)

### New CLI Commands

```bash
python main.py coverage-repair-scan --tier research30
python main.py coverage-repair-issues
python main.py coverage-repair-issues --priority P1
python main.py coverage-repair-tasks
python main.py coverage-repair-tasks --stock 2454
python main.py coverage-repair-plan --tier research30
python main.py coverage-repair-run --tier research30 --dry-run
python main.py coverage-repair-run --tier research30 --execute --allow-write
python main.py coverage-repair-result --plan-id latest
python main.py coverage-repair-unresolved
python main.py coverage-repair-source-required
python main.py coverage-repair-health
python main.py coverage-repair-report --plan-id latest --mode real
```

### Safety

- INVALID OHLC → always BLOCKED (never auto-modify prices)
- CONFLICT → always MANUAL_REVIEW (never auto-overwrite)
- Synthetic price repair: DISABLED
- External data download: DISABLED
- dry_run=True default
- --execute without --allow-write → BLOCKED
- destructive repair DISABLED by default
- No Real Orders
- Broker Execution Disabled
- Not Investment Advice

---

## Roadmap

| Version | Target |
|---------|--------|
| v1.1.3  | Data Freshness Monitor |
| v1.1.4  | Coverage Quality Gates |
| v1.2.0  | Replay Training UX |

---

*TW Quant Cockpit v1.1.x — Data Universe & Import & Coverage Repair Series — Research Only — Not Investment Advice*
