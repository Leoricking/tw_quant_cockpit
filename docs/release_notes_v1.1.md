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

## Roadmap

| Version | Target |
|---------|--------|
| v1.1.2  | Coverage Repair Workflow |
| v1.2.0  | Replay Training UX |

---

*TW Quant Cockpit v1.1.x — Data Universe & Import Series — Research Only — Not Investment Advice*
