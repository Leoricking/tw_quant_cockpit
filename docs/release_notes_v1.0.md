# TW Quant Cockpit — Release Notes v1.0

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] VALIDATED does not enable trading. Broker Execution Disabled.**
> **[!] Not Investment Advice.**

---

## v1.0.0 — Research Trading Cockpit Stable

**Released:** 2026-06-10

### Overview

v1.0.0 is the first stable research cockpit release of TW Quant Cockpit.
It consolidates all research modules from v0.5 through v0.9.3 into a unified
Research Trading Cockpit — still Research Only, No Real Orders, Production Trading BLOCKED.

No BUY/SELL/ORDER. No trading actions. Broker Execution: Disabled.
`read_only=True`, `no_real_orders=True`, `production_blocked=True`,
`VALIDATED_DOES_NOT_ENABLE_TRADING=True`.

### New in v1.0.0

#### release/version_info.py — v1.0.0 Module Constants

Added module-level constants:

```python
VERSION                           = "1.0.0"
RELEASE_NAME                      = "Research Trading Cockpit Stable"
RELEASE_STAGE                     = "STABLE"
RELEASE_TRACK                     = "research"
TRADING_MODE                      = "research_only"
REAL_ORDERS_ENABLED               = False
BROKER_EXECUTION_ENABLED          = False
PRODUCTION_TRADING_BLOCKED        = True
VALIDATED_DOES_NOT_ENABLE_TRADING = True
PAPER_TRADING_IS_SIMULATION       = True
MOCK_REALTIME_IS_SIMULATION       = True
NO_REAL_ORDERS                    = True
read_only                         = True
production_blocked                = True
```

#### release/research_cockpit_manifest.py — ResearchCockpitManifestBuilder

Builds and saves the v1.0.0 manifest JSON covering:
- 14 system modules with availability status
- CLI commands, GUI tabs, reports, safety guards, regression suites
- Known warnings list
- Full safety flags

#### release/research_cockpit_stable_checklist.py — ResearchCockpitStableChecklist

25-item release checklist:

| # | Check | Category |
|---|-------|----------|
| 1 | version_info_v100 | version |
| 2 | no_real_orders_global_guard | safety |
| 3 | production_trading_blocked | safety |
| 4 | broker_execution_disabled | safety |
| 5 | validated_does_not_enable_trading | safety |
| 6 | strategy_lab_dashboard_available | modules |
| 7 | strategy_validation_available | modules |
| 8 | evidence_graph_ux_available | modules |
| 9 | crash_reversal_available | modules |
| 10 | training_metrics_available | modules |
| 11 | backtest_coach_available | modules |
| 12 | strategy_memory_available | modules |
| 13 | research_intelligence_available | modules |
| 14 | report_pack_available | modules |
| 15 | data_coverage_available | modules |
| 16 | mock_realtime_available | modules |
| 17 | paper_available | modules |
| 18 | gui_import_available | gui |
| 19 | gui_navigation_available | gui |
| 20 | regression_release_gate_available | regression |
| 21 | forbidden_action_scan_passed | safety |
| 22 | runtime_output_gitignore_passed | hygiene |
| 23 | docs_index_available | docs |
| 24 | README_v100_available | docs |
| 25 | release_notes_v100_available | docs |

#### reports/research_trading_cockpit_stable_report.py

11-section Markdown report:
1. 總覽 (Overview)
2. System Modules (14 modules)
3. Strategy Research Workflow
4. Crash Reversal Workflow (6 rules)
5. Validation Workflow (grades + VALIDATED note)
6. Dashboard Summary
7. Release Checklist v1.0.0
8. Regression Summary
9. Known Warnings
10. Safety Declaration
11. Next Roadmap

#### CLI Commands (6 new)

| Command | Description |
|---------|-------------|
| `version-info` | Show v1.0.0 version info banner (updated) |
| `research-cockpit-stable` | Run checklist and print banner |
| `research-cockpit-stable-summary` | Print summary from checklist |
| `research-cockpit-stable-checks` | Run and print all checks |
| `research-cockpit-stable-manifest` | Build and save manifest |
| `research-cockpit-stable-report` | Generate Markdown report |

### Modules Consolidated

All modules from v0.5 through v0.9.3 are included in v1.0.0:

| Module | Since |
|--------|-------|
| Strategy Lab Dashboard | v0.9.3 |
| Strategy Validation Score | v0.9.2 |
| Evidence Graph UX | v0.9.1 |
| Crash Reversal Strategy Pack | v0.9.0.1 |
| Strategy Lab Stable | v0.9.0 |
| Research Intelligence Evidence Graph | v0.8.3 |
| Backtest Training Metrics | v0.8.2 |
| Strategy Memory UX | v0.8.1 |
| Research Intelligence Stable | v0.8.0 |
| Backtest-to-Coach Loop | v0.7.3 |
| Strategy Research Memory | v0.7.2 |
| Intelligence UX Polish | v0.7.1 |
| Research Intelligence | v0.7.0 |
| Research OS Stable Release | v0.6.0 |
| Data Coverage Expansion | v0.6.2 |
| CLI Alias / Command UX | v0.5.1 |
| GUI Tab Grouping / Navigation | v0.5.2 |
| Regression Suite Consolidation | v0.5.3 |
| Report Pack Consolidation | v0.5.4 |
| Paper Trading (simulation) | v0.5.x |
| Mock Realtime (simulation) | v0.5.x |

### Safety Declaration

> **Research Only** — All outputs are for research and learning purposes only.
>
> **No Real Orders** — This system does not and cannot place real trading orders.
>
> **Production Trading BLOCKED** — Production trading is permanently blocked.
>
> **Broker Execution Disabled** — There is no connection to any broker API.
>
> **VALIDATED does not enable trading** — VALIDATED grade is research-validated only.
>
> **Paper trading is simulation only** — Paper trades are simulated, not real.
>
> **Mock realtime is simulation only** — Mock realtime is not live market data.
>
> **Not Investment Advice** — Nothing in this system constitutes investment advice.

### Known Warnings

- cp950 subprocess encoding warning (Windows only — non-critical)
- Paper smoke test may WARN if paper_state.json missing (non-critical)
- no_real_orders flag pre-existing check is advisory only
- Optional report_pack modules may show ENV_LIMITED (non-critical)

### Next Roadmap

| Version | Feature | Priority |
|---------|---------|---------|
| v1.0.x | Maintenance releases — bug fixes, warning cleanup | P1 |
| v1.1 | Data Quality / Universe Expansion | P2 |
| broker-api-branch | Broker API (only if explicitly requested, separate branch) | ON_REQUEST |

---

---

## v1.0.1 — Maintenance & Polish

**Released:** 2026-06-11

**Base Release:** v1.0.0 Research Trading Cockpit Stable

v1.0.1 is a maintenance and polish release based on v1.0.0. No new features, no broker API, no live trading.

### Changes in v1.0.1

- **CLI consistency:** `version-info` now shows `Base Release: 1.0.0 Research Trading Cockpit Stable`
- **Stable checklist hardening:** v1.0.x version check accepts maintenance releases; added `version_info_v101`, `research_cockpit_maintenance_safe`, `no_real_orders_false_positive_guard`, `maintenance_v101_import`, `maintenance_v101_no_forbidden_actions` checks to stable_release_checklist_v060
- **Intelligence stable checklist:** Added `maintenance_v101_safe` check
- **GUI navigation keywords:** Added `maintenance`, `polish`, `v1.0.1`, `research cockpit stable`, `no real orders`, `維護版` to tab_registry
- **Regression suite:** Added `gui-nav-search --keyword maintenance`, `gui-nav-search --keyword 維護版`, `gui-nav-search --keyword research cockpit stable` tests
- **Docs:** Added `docs/maintenance_v1.0.1.md`, updated roadmap, index, release notes
- **No functional trading changes** — all safety flags preserved

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

*TW Quant Cockpit v1.0.1 — Maintenance & Polish — Research Only — Not Investment Advice*

---

## v1.0.2 — Data & Report Hygiene

**Released:** 2026-06-11

**Base Release:** v1.0.0 Research Trading Cockpit Stable

v1.0.2 adds a review-only Data & Report Hygiene module. No new broker API, no trading actions.

### New in v1.0.2

- **maintenance/data_report_hygiene_engine.py** — DataReportHygieneEngine: scans reports/, data/backtest_results/, logs/, experiments/, data_cache/, journal_data/ for runtime outputs. Review-only, never deletes/moves/archives files.
- **maintenance/data_report_hygiene_schema.py** — HygieneInventoryItem, HygieneReportManifest, HygieneSummary dataclasses with to_dict/from_dict.
- **maintenance/data_report_hygiene_store.py** — DataReportHygieneStore: saves/loads inventory, report manifest, summary as CSV.
- **maintenance/data_report_hygiene_query.py** — DataReportHygieneQuery: filters inventory, lists stale/large files, explains items.
- **reports/data_report_hygiene_report.py** — DataReportHygieneReportBuilder: generates Markdown hygiene report with 8 sections.
- **gui/data_report_hygiene_panel.py** — DataReportHygienePanel (PySide6): safety banner, summary cards, 6-tab view, scan worker, no delete/archive buttons.
- **gui/data_report_hygiene_adapter.py** — DataReportHygieneAdapter: load_summary(), load_safe_commands().
- **9 new CLI commands:** data-report-hygiene, data-report-hygiene-summary, data-report-hygiene-inventory, data-report-hygiene-reports, data-report-hygiene-gitignore, data-report-hygiene-tracked, data-report-hygiene-stale, data-report-hygiene-large-files, data-report-hygiene-report
- **release/version_info.py:** VERSION=1.0.2, RELEASE_NAME="Data & Report Hygiene", DATA_CLEANUP_REVIEW_ONLY=True, ARCHIVE_SUGGESTIONS_ONLY=True
- **Checklist updates:** +5 checks in research_cockpit_stable_checklist (checks 26-30), +4 in stable_release_checklist_v060, +1 in intelligence_stable_checklist
- **Regression suite:** 16 new test cases in release_gate suite
- **GUI navigation:** data_report_hygiene tab added to tab_registry and dashboard
- **Report pack:** data_report_hygiene_report in registry and collector
- **.gitignore:** Added data/backtest_results/maintenance/ and reports/data_report_hygiene_report_*.md

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **Data Cleanup is Review Only** — **Archive Suggestions Only**
> **No automatic deletion** — **No file moves** — **No archive**
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

*TW Quant Cockpit v1.0.2 — Data & Report Hygiene — Research Only — Not Investment Advice*

---

## v1.0.3 — GUI Stability & Usability Polish

**Released:** 2026-06-11

**Base Release:** v1.0.0 Research Trading Cockpit Stable

v1.0.3 adds shared GUI stability and usability helpers. No new broker API, no trading actions, no strategy logic changes.

### New in v1.0.3

- **gui/common/__init__.py** — GUI common helpers package
- **gui/common/gui_safety.py** — Safety banners, forbidden text scanner, safe label builders
- **gui/common/gui_threading.py** — SafeWorker, run_in_qthread, cleanup_thread for safe QThread lifecycle
- **gui/common/table_utils.py** — Table defaults, column sizing, ellipsis delegate, tooltip, empty row
- **gui/common/empty_state.py** — Friendly empty state descriptors
- **gui/common/copy_utils.py** — Copy safety: blocks forbidden trading actions from clipboard
- **gui/gui_health_check.py** — GuiHealthCheck: 8-category GUI health check
- **reports/gui_usability_report.py** — GuiUsabilityReportBuilder: Markdown GUI usability report
- **2 new CLI commands:** gui-health-check, gui-usability-report
- **release/version_info.py:** VERSION=1.0.3, RELEASE_NAME="GUI Stability & Usability Polish", GUI_POLISH_RELEASE=True, GUI_STABILITY_FOCUS=True
- **Checklist updates:** +4 checks in research_cockpit_stable_checklist (checks 31-34), +3 in stable_release_checklist_v060, +1 in intelligence_stable_checklist
- **Regression suite:** 11 new test cases in release_gate suite
- **GUI navigation:** gui_stability_usability tab added, v1.0.3 keywords added to strategy_lab_dashboard tab
- **Report pack:** gui_usability_report in registry and collector
- **.gitignore:** Added reports/gui_usability_report_*.md
- **Docs:** gui_stability_usability_v1.0.3.md

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **GUI does not enable trading** — GUI panels are research-only displays
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

*TW Quant Cockpit v1.0.3 — GUI Stability & Usability Polish — Research Only — Not Investment Advice*

---

## v1.0.4 — Regression & Release Gate Hardening

**Release Date:** 2026-06-11
**Base Release:** v1.0.0 Research Trading Cockpit Stable

v1.0.4 hardens the regression and release gate infrastructure. No new broker API, no trading actions, no strategy logic changes.

### New in v1.0.4

- **regression_hardening/__init__.py** — New package
- **regression_hardening/safety_scanner.py** — SafetyScanner with expanded whitelist and context-aware forbidden detection
- **regression_hardening/encoding_utils.py** — Windows cp950 encoding warning detection and classification
- **regression_hardening/regression_summary.py** — Known vs unknown warning/blocked classification for release gate results
- **regression_hardening/release_gate_health.py** — ReleaseGateHealth: checks suites, known warns, known blocked, false positive guard
- **reports/regression_hardening_report.py** — RegressionHardeningReportBuilder: Markdown regression hardening report
- **4 new CLI commands:** release-gate-health, safety-scan, regression-hardening-summary, regression-hardening-report
- **release/version_info.py:** VERSION=1.0.4, RELEASE_NAME="Regression & Release Gate Hardening", REGRESSION_HARDENING_RELEASE=True, RELEASE_GATE_HARDENING=True, SAFETY_SCANNER_HARDENING=True
- **Checklist updates:** +5 checks in research_cockpit_stable_checklist (checks 35–39), +5 in stable_release_checklist_v060, +1 in intelligence_stable_checklist
- **Regression suite:** 16 new test cases in release_gate suite
- **Report pack:** regression_hardening_report in registry and collector
- **GUI navigation:** regression hardening keywords added to gui_stability_usability tab
- **.gitignore:** Added reports/regression_hardening_report_*.md, data/backtest_results/regression_hardening/
- **Docs:** regression_release_gate_hardening_v1.0.4.md

### Known Warning Classifications

| Classification | Description |
|----------------|-------------|
| KNOWN_CP950_WARNING | Windows cp950 subprocess encoding — non-critical |
| KNOWN_PAPER_SMOKE_WARNING | paper_state.json missing — non-critical |
| KNOWN_REPORT_PACK_OPTIONAL | ENV_LIMITED / NOT_GENERATED optional reports |
| KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE | no_real_orders flag pre-existing check |
| KNOWN_NO_REAL_ORDERS_FLAG_CHECK | Known BLOCKED — pre-existing advisory |

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **Regression does not enable trading** — Regression checks are research-only
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

## v1.0.5 — Documentation & User Guide Polish

**Released:** 2026-06-11

**Base Release:** v1.0.0 Research Trading Cockpit Stable

v1.0.5 is a documentation polish release. No broker API, no trading, no strategy changes.

### What Is New in v1.0.5

#### documentation/ Package
- `documentation/__init__.py` — Documentation health and indexing package
- `documentation/docs_health_check.py` — DocumentationHealthCheck (8 checks)
- `documentation/docs_indexer.py` — DocumentationIndexer (manifest, categories, missing links)
- `documentation/docs_summary.py` — DocumentationSummaryBuilder

#### reports/documentation_health_report.py
- DocumentationHealthReportBuilder — 7-section Markdown report

#### 4 New CLI Commands
- `docs-health-check` — Run documentation health check
- `docs-index` — Index all docs and save CSV manifest
- `docs-summary` — Print documentation summary
- `documentation-report --mode real` — Generate documentation health report

#### New Documentation Files (docs/ v1.0 guides)
- `docs/user_guide_v1.0.md` — User Guide
- `docs/gui_user_guide_v1.0.md` — GUI User Guide
- `docs/cli_cookbook_v1.0.md` — CLI Cookbook
- `docs/daily_workflow_sop_v1.0.md` — Daily Workflow SOP
- `docs/troubleshooting_v1.0.md` — Troubleshooting Guide
- `docs/safety_guide_v1.0.md` — Safety Guide
- `docs/version_map_v1.0.md` — Version Map
- `docs/handoff_guide_v1.0.md` — Handoff Guide

#### Checklist Updates
- `release/research_cockpit_stable_checklist.py` — +5 checks (40-44): documentation_health_available, user_guide_available, safety_guide_available, handoff_guide_available, docs_no_forbidden_actions
- `stable_release/stable_release_checklist_v060.py` — +3 checks: documentation_health_import, documentation_health_no_forbidden_actions, version_info_v105
- `intelligence_stable/intelligence_stable_checklist.py` — +1 check: documentation_v105_safe

#### Regression Suite
- `regression/suite_registry.py` — +13 test cases (v1.0.5 release gate suite)

#### Report Pack
- `report_pack/report_registry.py` — documentation_health_report in daily/weekly/full packs
- `report_pack/report_collector.py` — documentation_health_report pattern

#### Other Updates
- `release/version_info.py` — VERSION=1.0.5, DOCUMENTATION_POLISH_RELEASE=True, USER_GUIDE_FOCUS=True, HANDOFF_GUIDE_AVAILABLE=True
- `main.py` — version-info updated, 4 new commands, subparsers added
- `gui/navigation/tab_registry.py` — documentation keywords added
- `.gitignore` — documentation_health_report, data/backtest_results/documentation/
- `README.md` — Refreshed with all new chapters
- `docs/index.md` — Reorganized into A-E categories
- `docs/roadmap.md` — v1.0.5 added, next steps v1.0.6/v1.1.0/v1.2.0
- `docs/release_notes_v1.0.md` — v1.0.5 section added

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **Documentation does not enable trading** — Documentation polish is research-only
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

*TW Quant Cockpit v1.0.5 — Documentation & User Guide Polish — Research Only — Not Investment Advice*

---

## v1.0.6 — Example Workflows & Templates

**Released:** 2026-06-11

### Overview

v1.0.6 adds example workflows and reusable templates to TW Quant Cockpit.
It provides 10 example workflow documents and 8 fillable template documents for common research scenarios.
Still Research Only, No Real Orders, Production Trading BLOCKED.

No real trading actions. No broker API. Templates do not enable trading.
`EXAMPLE_WORKFLOWS_RELEASE=True`, `WORKFLOW_TEMPLATES_AVAILABLE=True`, `TEMPLATE_GUIDE_AVAILABLE=True`.

### New in v1.0.6

#### workflows/ Package

New package with 4 modules:
- `workflow_template_schema.py` — WorkflowTemplateItem dataclass, CATEGORIES list
- `workflow_template_indexer.py` — WorkflowTemplateIndexer, indexes examples and templates
- `workflow_template_health.py` — WorkflowTemplateHealthCheck, health checks for all workflow files
- `workflow_template_summary.py` — WorkflowTemplateSummaryBuilder, console summary

#### reports/workflow_templates_report.py

WorkflowTemplatesReportBuilder — 6-section Markdown report covering overview, examples, templates, health, usage guide, and safety declaration.

#### docs/examples/ — 10 Example Workflows

| File | Description |
|------|-------------|
| daily_operation_example.md | Daily research session |
| weekend_review_example.md | Weekend review session |
| single_stock_research_example.md | Single stock research |
| strategy_validation_example.md | Strategy validation workflow |
| crash_reversal_review_example.md | Crash reversal research |
| data_hygiene_example.md | Data hygiene workflow |
| gui_operation_example.md | GUI operation |
| claude_code_maintenance_example.md | Maintenance with git -C, no chain commands |
| troubleshooting_example.md | Common issue resolution |
| paper_mock_practice_example.md | Paper and mock simulation |

#### docs/templates/ — 8 Fillable Templates

| File | Description |
|------|-------------|
| daily_review_template.md | Daily review form |
| single_stock_research_template.md | Single stock research form |
| strategy_idea_template.md | Strategy hypothesis form |
| backtest_review_template.md | Backtest review form |
| weekly_retrospective_template.md | Weekly retrospective form |
| error_report_template.md | Error diagnosis form |
| release_prompt_template.md | Release checklist (git -C, no chain, no git add .) |
| handoff_summary_template.md | Project handoff form |

#### New CLI Commands (4)

- `workflow-templates-health` — WorkflowTemplateHealthCheck
- `workflow-templates-index` — WorkflowTemplateIndexer
- `workflow-templates-summary` — WorkflowTemplateSummaryBuilder
- `workflow-templates-report --mode real` — WorkflowTemplatesReportBuilder

#### Updated Files

- `release/version_info.py` — VERSION=1.0.6, EXAMPLE_WORKFLOWS_RELEASE=True, WORKFLOW_TEMPLATES_AVAILABLE=True, TEMPLATE_GUIDE_AVAILABLE=True
- `release/research_cockpit_stable_checklist.py` — +5 checks (45-49)
- `stable_release/stable_release_checklist_v060.py` — +3 checks
- `intelligence_stable/intelligence_stable_checklist.py` — +1 check: workflow_templates_v106_safe
- `regression/suite_registry.py` — +15 test cases (v1.0.6 release gate suite)
- `report_pack/report_registry.py` — workflow_templates_report in daily/weekly/full packs
- `report_pack/report_collector.py` — workflow_templates_report pattern
- `main.py` — version-info updated, 4 new commands, subparsers added
- `gui/navigation/tab_registry.py` — workflow templates keywords added
- `.gitignore` — workflow_templates_report, data/backtest_results/workflows/
- `README.md` — Refreshed with v1.0.6
- `docs/index.md` — Category F: Examples & Templates added
- `docs/roadmap.md` — v1.0.6 added, next steps v1.0.7/v1.1.0/v1.2.0

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **Templates do not enable trading** — All templates are research-only
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*

---

## v1.0.7 — Knowledge Base Search Polish

**Released:** 2026-06-12

### 概述
Knowledge Base Search Polish — 把累積的文件、範例、模板、報告、Strategy Memory、Evidence Graph 變成可搜尋、可導覽、可複用的研究知識庫入口。

### New in v1.0.7
- `knowledge_base/` package: kb_schema, kb_indexer, kb_search_engine, kb_store, kb_query, kb_summary, kb_health_check
- Local lightweight indexing and search across docs, examples, templates, reports, GUI registry, CLI metadata
- Safe search summary (research-only next steps only)
- CLI: kb-index, kb-summary, kb-health-check, kb-search, kb-explain, kb-report
- Optional GUI panel: KnowledgeBaseSearchPanel
- Knowledge Base Search Report
- No external API. No embedding API. No network.
- No strategy logic changes. No broker API. No real orders.
- Search does not enable trading.

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **Search does not enable trading** — Search is research-only
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

## v1.0.8 — Local Research Assistant Polish

**Released:** 2026-06-12

### 概述
Local Research Assistant Polish — 把 Knowledge Base Search 的搜尋結果整理成「本地研究助理摘要」。

### New in v1.0.8
- `local_assistant/` package: assistant_schema, research_router, research_summarizer, safe_answer_builder, local_assistant_engine, local_assistant_store, local_assistant_query, local_assistant_health
- Safe research answer synthesis from KB search results (local only, no external API)
- Module routing: Strategy Validation, Evidence Graph, Crash Reversal, Data Hygiene, etc.
- Unsafe query blocking (BLOCKED_UNSAFE_QUERY for trading queries)
- CLI: local-assistant, local-assistant-summary, local-assistant-health, local-assistant-report, local-assistant-explain
- Optional GUI panel: LocalResearchAssistantPanel
- Local Research Assistant Report
- No external API. No embedding API. No network. No LLM.
- No strategy logic changes. No broker API. No real orders.
- Local assistant does not enable trading.

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **External API Disabled** — **Local assistant does not enable trading**
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

*TW Quant Cockpit v1.0.8 — Local Research Assistant Polish — Research Only — Not Investment Advice*

---

## v1.0.9 — Final Maintenance Rollup

**Released:** 2026-06-13

### 概述
Final Maintenance Rollup — v1.0.x maintenance 線的總收尾版。整理 v1.0.0 ~ v1.0.8 功能總結、穩定性狀態、長期維護節奏、最終 smoke test、最終 release rollup report。v1.0 Maintenance Line Complete。

### New in v1.0.9

#### final_rollup/ package
- `rollup_schema.py`: ReleaseEntry, FinalMaintenanceStatus, LongTermMaintenanceTask dataclasses
- `release_history.py`: ReleaseHistoryBuilder — v1.0.0 ~ v1.0.9 release history
- `final_health_check.py`: FinalMaintenanceHealthCheck — 22 health checks
- `final_smoke_summary.py`: FinalSmokeSummaryBuilder — smoke test summary
- `maintenance_plan.py`: LongTermMaintenancePlanBuilder — Daily/Weekly/Monthly/Release/Incident SOP
- `final_rollup_engine.py`: FinalRollupEngine — orchestrates full rollup
- `final_rollup_store.py`: FinalRollupStore — saves CSV runtime outputs

#### reports/final_maintenance_rollup_report.py
- FinalMaintenanceRollupReportBuilder — 10-chapter Markdown report
- Output: `reports/final_maintenance_rollup_report_YYYY-MM-DD.md` (not committed)

#### CLI Commands (6 new)
```
python main.py final-rollup
python main.py final-rollup-history
python main.py final-rollup-health
python main.py final-rollup-maintenance-plan
python main.py final-rollup-smoke
python main.py final-rollup-report --mode real
```

#### GUI
- Optional `gui/final_rollup_panel.py` + `gui/final_rollup_adapter.py`
- GUI nav tab: `final_maintenance_rollup` (group: maintenance, P1)

#### Docs
- `docs/final_maintenance_rollup_v1.0.9.md`
- Updated: README.md, docs/index.md, docs/roadmap.md, docs/release_notes_v1.0.md
- Updated: docs/user_guide_v1.0.md, docs/handoff_guide_v1.0.md, docs/cli_cookbook_v1.0.md

#### Checklists & Regression
- `release/research_cockpit_stable_checklist.py`: +5 new checks (60-64)
- `stable_release/stable_release_checklist_v060.py`: +3 new checks
- `intelligence_stable/intelligence_stable_checklist.py`: +1 new check
- `regression/suite_registry.py`: +7 final_rollup regression tests

### What Changed
- No strategy logic changes
- No broker API
- No real orders
- No external API
- No modification to validation/evidence graph scoring
- No modification to crash reversal rules

### Safety (unchanged from v1.0.0)

> **Research Only** — **No Real Orders** — **Production Trading BLOCKED**
> **Broker Execution Disabled** — **VALIDATED does not enable trading**
> **External API Disabled** — **v1.0 Maintenance Line Complete**
> **Paper trading is simulation only** — **Mock realtime is simulation only**
> **Not Investment Advice**

---

*TW Quant Cockpit v1.0.9 — Final Maintenance Rollup — Research Only — Not Investment Advice*
