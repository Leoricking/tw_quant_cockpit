# TW Quant Cockpit — Roadmap

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## Completed Milestones

| Version | Feature | Status |
|---------|---------|--------|
| v0.3.1–v0.3.8 | Core infrastructure, data pipeline, signal engine | Done |
| v0.3.9 | Public data API layer (TWSE public endpoints) | Done |
| v0.3.10 | Intraday OHLC fix, microstructure display fix | Done |
| v0.3.11 | Long-term strategy validation (multi-year backtest) | Done |
| v0.3.12 | Portfolio & risk simulation | Done |
| v0.3.13 | GUI Portfolio Cockpit tab | Done |
| v0.3.14 | Signal Quality Dashboard | Done |
| v0.3.15 | Rule Weight Tuning Lab | Done |
| v0.3.16 | Auto Report Center | Done |
| v0.3.17 | Automation Scheduler | Done |
| v0.3.18 | API Provider Hardening | Done |
| v0.3.19 | Data Provider Auto Fetch | Done |
| v0.3.20 | Data Quality Gate | Done |
| v0.3.21 | Daily Workflow Engine | Done |
| v0.3.22 | Usability QA & Error Message Polish | Done |
| v0.3.23 | Documentation & Release Notes Pack | Done |
| v0.3.24 | Data Provider Reliability & Fallback Matrix | Done |
| v0.3.25 | Universe Expansion & Sector Classification | Done |
| v0.3.26 | Backtest Engine Hardening | Done |
| v0.3.27 | Intraday / Tick Data Pipeline | Done |
| v0.3.28 | Strategy Rule Governance | Done |
| v0.3.29 | Research Notebook / Experiment Registry | Done |
| v0.4.0 | Research Platform Stable Release | Done |
| v0.4.1 | API Fetch Productionization | Done |
| v0.4.1.1 | Strategy Knowledge Ingestion from Transcripts | Done |
| v0.4.2 | ML Feature Store v1 | Done |
| v0.4.2.1 | ML Feature Store Knowledge Integration | Done |
| v0.4.3 | Model Monitoring Framework | Done |
| v0.4.4 | Intraday Replay Cockpit | Done |
| v0.4.5 | Notification Center | Done |
| v0.4.6 | Portfolio Journal & Trade Review | Done |
| v0.4.7 | Research Review Dashboard | Done |
| v0.4.8 | Research Assistant / Coach | Done |
| v0.4.9 | Research Workflow Automation | Done |
| v0.5.0 | Research OS Planning / Stabilization | Done |
| v0.5.1 | CLI Alias / Command UX Polish | Done |
| v0.5.1.1 | Strategy Filter Pack — Financial Turnaround & Trend Discipline | Done |
| v0.5.2 | GUI Tab Grouping / Navigation Polish | Done |
| v0.5.2.1 | Strategy Filter GUI Navigation Integration | Done |
| v0.5.3 | Regression Suite Consolidation | Done |
| v0.5.4 | Report Pack Consolidation | Done |
| v0.5.5 | Data / Feature Store Stabilization | Done |
| v0.5.6 | TW Replay Training Cockpit — AI Review & Tape Reading Practice | Done |
| v0.5.6.2 | Stabilize Data and Feature Store Health | Done |
| v0.6.0 | Research OS Stable Release | Done |
| v0.6.1 | Stable UX Polish | Done |
| v0.6.2 | Data Coverage Expansion | Done |
| v0.6.3 | Replay Training UI Enhancement | Done |
| v0.7.0 | Research Intelligence Upgrade | Done |
| v0.7.1 | Intelligence UX Polish | Done |
| v0.7.2 | Strategy Research Memory | Done |
| v0.7.3 | Backtest-to-Coach Loop | Done |
| v0.8.0 | Research Intelligence Stable | Done |
| v0.8.1 | Strategy Memory UX | Done |
| v0.8.2 | Backtest Training Metrics | Done |
| v0.8.3 | Research Intelligence Evidence Graph | Done |
| v0.9.0 | Strategy Lab Stable | Done |
| v0.9.0.1 | Crash Reversal & Risk Discipline Strategy Pack | Done |
| v0.9.1 | Evidence Graph UX | Done |
| v0.9.2 | Strategy Validation Score | Done |
| v0.9.3 | Strategy Lab Dashboard Polish | Done |
| v1.0.0 | Research Trading Cockpit Stable | Done |
| v1.0.1 | Maintenance & Polish | Done |
| v1.0.2 | Data & Report Hygiene | Done |
| v1.0.3 | GUI Stability & Usability Polish | Done |
| v1.0.4 | Regression & Release Gate Hardening | Done |
| v1.0.5 | Documentation & User Guide Polish | Done |
| v1.0.6 | Example Workflows & Templates | Done |
| v1.0.7 | Knowledge Base Search Polish | Done |
| v1.0.8 | Local Research Assistant Polish | Done |
| v1.0.9 | Final Maintenance Rollup | Done |
| v1.1.0 | Data Universe Expansion | Done |
| v1.1.1 | Data Import UX & Batch Onboarding | Done |
| v1.1.2 | Coverage Repair Workflow | Done |
| v1.1.3 | Data Freshness Monitor | Done |
| v1.1.4 | Coverage Quality Gates | Done |
| v1.1.5 | Quality Gate Enforcement & Audit | Done |
| v1.1.6 | Data Governance Operations Dashboard | Done |
| v1.1.7 | Governance Alerts & Daily Operations | Done |
| v1.1.8 | Research Run Registry | Done |

---

### v1.1.8 — Research Run Registry ✅

- **Version:** 1.1.8 — feature release based on v1.1.7 Governance Alerts & Daily Operations
- **Type:** Append-only Research Run Registry — run lifecycle, qualification levels, artifact catalog, lineage graph, duplicate detection, run comparator, registry health checks. No broker, no trading, no auto-rerun, no auto-execution.
- **Changes:** research_registry/ package (registry_schema, run_classifier, run_capture, run_lineage, artifact_catalog, duplicate_detector, run_comparator, registry_store, registry_query, registry_engine, registry_health, __init__), reports/research_run_registry_report.py, gui/research_run_registry_panel.py, gui/research_run_registry_adapter.py, 20 new CLI commands (research-registry-health/summary/runs/run/run-artifacts/run-lineage/run-verify/run-duplicates/run-duplicate-check/run-compare/run-search/run-latest-successful/run-latest-formal/run-missing-artifacts/registry-backfill/registry-rebuild-index/registry-report/registry-audit/registry-audit-verify), GUI nav tab (research_run_registry, research group), 5 new report types in report pack, stable checklist checks (5 new), v060 checklist checks (5 new), intelligence checklist check (research_run_registry_v118_safe), 13 regression tests, tests/fixtures/research_registry/ (18 fixtures), docs/research_run_registry_v1.1.8.md, .gitignore updates, governance_alerts integration (8 new alert policies + detect_from_research_registry), README/docs refresh
- **Safety:** Auto Rerun DISABLED, Auto Execution DISABLED, Trade Execution DISABLED, Mock always DEMO_ONLY, Backfill requires explicit allow_write=True, Sensitive fields redacted, Registry failure is non-fatal, No Real Orders, Broker Disabled, Production Trading BLOCKED

**Next:**
- v1.2.0: Replay Training UX

---

### v1.1.7 — Governance Alerts & Daily Operations ✅

- **Version:** 1.1.7 — feature release based on v1.1.6 Data Governance Operations Dashboard
- **Type:** Governance Alert Detection & Daily Ops — alert lifecycle, dedup, snooze, escalation, digests, checklists, notification preview. No broker, no trading, no external notification send.
- **Changes:** governance_alerts/ package (alert_schema, alert_policy, alert_sources, alert_detector, alert_deduplicator, alert_lifecycle, escalation_engine, digest_builder, daily_checklist, notification_preview, alert_store, alert_query, alert_health, daily_operations_engine, __init__), reports/governance_alerts_daily_operations_report.py, gui/governance_alerts_panel.py, gui/governance_alerts_adapter.py, gui/data_governance_operations_panel.py (v1.1.7 governance alerts summary section), 22 new CLI commands (governance-alerts-health/scan/alerts/alert/alert-history/alert-ack/alert-snooze/alert-resolve/alert-reopen/alert-escalations/digest/checklist/checklist-complete/notification-preview/alert-trend/alert-compare/daily-operations/alerts-report/alert-audit/alert-audit-verify), GUI nav tab (governance_alerts, data group), 6 new report types in report pack, stable checklist checks (5 new), v060 checklist checks (5 new), intelligence checklist check (governance_alerts_v117_safe), 10 regression tests, tests/fixtures/governance_alerts/ (16 fixtures), docs/governance_alerts_daily_operations_v1.1.7.md, .gitignore updates, README/docs refresh
- **Safety:** External Notification Send DISABLED, Auto Repair DISABLED, Auto Import DISABLED, Auto Download DISABLED, Gate Override DISABLED, Trade Execution DISABLED, P0 never suppressed, AUDIT_CHAIN_FAILURE never suppressed, Suggested commands allowlist only, No Real Orders, Production Trading BLOCKED

**Next:**
- v1.1.8: Research Run Registry — Done
- v1.2.0: Replay Training UX

---

### v1.1.6 — Data Governance Operations Dashboard ✅

- **Version:** 1.1.6 — feature release based on v1.1.5 Quality Gate Enforcement & Audit
- **Type:** Data Governance Operations Dashboard — unified governance view, no strategy changes, no broker API, no trading
- **Changes:** governance_ops/ package (governance_schema, governance_adapters, priority_engine, action_queue, governance_aggregator, operations_store, operations_engine, operations_query, operations_health, __init__), reports/data_governance_operations_report.py, 18 new CLI commands (governance-health/dashboard/summary/module-health/symbols/symbol/actions/top-actions/source-health/gate-summary/audit-summary/runs/history/report/compare/action-ack/action-defer/action-resolve), GUI panel + adapter, GUI nav tab (data group), 4 new report types in report pack, stable checklist checks (5 new), v060 checklist checks (5 new), intelligence checklist check (governance_ops_v116_safe), regression tests (7 new), tests/fixtures/governance_ops/ (13 fixtures), docs/data_governance_operations_dashboard_v1.1.6.md, .gitignore updates, README/docs refresh
- **Safety:** Auto Repair DISABLED, Auto Download DISABLED, Gate Override DISABLED, Trade Execution DISABLED, Priority based only on data governance issues, Actions are metadata-only, No Real Orders, Production Trading BLOCKED

**Next:**
- v1.2.0: Replay Training UX

---

### v1.1.5 — Quality Gate Enforcement & Audit ✅

- **Version:** 1.1.5 — feature release based on v1.1.4 Coverage Quality Gates
- **Type:** Quality Gate Enforcement & Audit — run-level enforcement layer, no strategy changes, no broker API, no trading
- **Changes:** gate_enforcement/ package (enforcement_schema, enforcement_policy, run_gate_resolver, symbol_filter, run_snapshot, reproducibility, audit_log, enforcement_engine, enforcement_store, enforcement_query, enforcement_health, __init__), reports/quality_gate_enforcement_audit_report.py, 11 new CLI commands (gate-enforcement-health/preview/run/policy/audit-query/audit-verify/snapshot/hash/runs/compare/report), --quality-gate/--gate-mode flags on validate-score/backtest-buy-points/backtest-screener/backtest-strategy-knowledge, GUI panel + adapter, GUI nav tab (data group), 4 new report types in report pack, stable checklist checks (5 new), v060 checklist checks (5 new), intelligence checklist check (gate_enforcement_v115_safe), regression tests (9 new), tests/fixtures/gate_enforcement/ (11 fixtures), docs/quality_gate_enforcement_audit_v1.1.5.md, .gitignore updates
- **Safety:** FORMAL eligible does NOT enable trading, Gate bypass DISABLED, Mock data formal enforcement BLOCKED, Audit log raises RuntimeError on failure, Override requires explicit flag and is audited, Override cannot enable trading, No Real Orders, Production Trading BLOCKED

**Next:**
- v1.2.0: Replay Training UX

---

### v1.1.4 — Coverage Quality Gates ✅

- **Version:** 1.1.4 — feature release based on v1.1.3 Data Freshness Monitor
- **Type:** Coverage Quality Gates — data eligibility evaluation only, no strategy changes, no broker API, no trading
- **Changes:** quality_gates/ package (gate_schema, gate_policy, symbol_gate_evaluator, universe_gate_evaluator, gate_decision_engine, gate_override, gate_store, gate_query, gate_health, __init__), reports/coverage_quality_gate_report.py, 12 new CLI commands (quality-gate-health/symbol/universe/matrix/summary/formal/observational/blocked/reasons/explain/report/override-request), GUI panel + adapter, GUI nav tab (data group), report pack entry, stable checklist checks (5 new), v060 checklist checks (5 new), intelligence checklist check (coverage_quality_gate_v114_safe), regression tests (20 new), tests/fixtures/quality_gates/ (12 CSVs), docs/coverage_quality_gates_v1.1.4.md, .gitignore updates, README/docs refresh
- **Safety:** Mock/Invalid/Stale/Conflict data cannot pass FORMAL gate, Override DISABLED by default, Override max level OBSERVATIONAL, Gate does NOT enable trading, No Real Orders, Production Trading BLOCKED

---

### v1.1.3 — Data Freshness Monitor ✅

- **Version:** 1.1.3 — feature release based on v1.1.2 Coverage Repair Workflow
- **Type:** Data Freshness Monitor — no strategy logic changes, no broker API, no trading
- **Changes:** data_freshness/ package (freshness_schema, trading_calendar, freshness_policy, freshness_detector, source_monitor, freshness_prioritizer, freshness_engine, freshness_store, freshness_query, freshness_health), reports/data_freshness_report.py, 10 new CLI commands (freshness-scan, -summary, -alerts, -stale, -missing, -source-health, -history, -repair-handoff, -health, -report), GUI panel + adapter, GUI nav tab (data group), report pack entry, stable checklist checks (5 new), v060 checklist checks (4 new including version_info_v113), intelligence checklist check (data_freshness_v113_safe), regression tests (~18), tests/fixtures/data_freshness/ (9 CSVs), docs/data_freshness_monitor_v1.1.3.md, .gitignore updates, README/docs refresh
- **Safety:** Auto external refresh DISABLED, Stale auto repair DISABLED, Future date NOT fresh, Mock formal freshness DISABLED, No Real Orders, Production Trading BLOCKED

---

### v1.1.2 — Coverage Repair Workflow ✅

- **Version:** 1.1.2 — feature release based on v1.1.1 Data Import UX & Batch Onboarding
- **Type:** Coverage Repair Workflow — no strategy logic changes, no broker API, no trading
- **Changes:** coverage_repair/ package (repair_schema, issue_detector, task_builder, repair_prioritizer, repair_planner, safe_repair_executor, repair_validator, repair_store, repair_query, repair_health), reports/coverage_repair_report.py, 13 new CLI commands (coverage-repair-scan, -issues, -tasks, -plan, -run, -result, -unresolved, -source-required, -health, -report, etc.), GUI panel + adapter, GUI nav tab (data group), report pack entry, stable checklist checks (5 new), v060 checklist checks (4 new including version_info_v112), intelligence checklist check (coverage_repair_v112_safe), regression tests (~20), tests/fixtures/coverage_repair/ (8 CSVs with TST1/TST2 symbols), docs/coverage_repair_workflow_v1.1.2.md, .gitignore updates, README/docs refresh
- **Safety:** INVALID OHLC → always BLOCKED (never auto-modify), CONFLICT → always MANUAL_REVIEW (never auto-overwrite), synthetic repair DISABLED, external data download DISABLED, dry_run=True default, destructive repair DISABLED by default, No Real Orders, Production Trading BLOCKED

**Next:**
- v1.1.3: Data Freshness Monitor
- v1.1.4: Coverage Quality Gates
- v1.2.0: Replay Training UX
- Broker API branch: only if explicitly planned

---

### v1.1.1 — Data Import UX & Batch Onboarding ✅

- **Version:** 1.1.1 — feature release based on v1.1.0 Data Universe Expansion
- **Type:** Data Import UX & Batch Onboarding — no strategy logic changes, no broker API, no trading
- **Changes:** data_onboarding/ package (12 modules), reports/data_import_onboarding_report.py, 7 new CLI commands (import-discover, import-preview, import-validate, import-plan, import-batch, import-retry-manifest, import-onboarding-health, import-onboarding-report), GUI panel + adapter, GUI nav tab (data group), report pack entry, stable checklist checks, v060 checklist checks, intelligence checklist check, regression tests (~8), tests/fixtures/import_onboarding/ (6 CSVs), docs/data_import_onboarding_v1.1.1.md, .gitignore updates, README/docs refresh
- **Safety:** dry_run=True by default, REPLACE_EXPLICIT blocked by default, conflicts → REVIEW (never auto-overwrite), No Real Orders, Production Trading BLOCKED

**Next:**
- v1.1.2: Coverage Repair Workflow
- v1.2.0: Replay Training UX
- Broker API branch: only if explicitly planned

---

### v1.1.0 — Data Universe Expansion ✅

- **Version:** 1.1.0 — feature release based on v1.0.9 Final Maintenance Rollup
- **Type:** Data Universe Expansion — no strategy logic changes, no broker API, no trading
- **Changes:** universe/ package (universe_schema, universe_tier_registry, universe_builder, universe_coverage, universe_health, universe_store, universe_query), reports/data_universe_expansion_report.py, 7 new CLI commands (universe-build, universe-summary, universe-health, universe-coverage, universe-symbol, universe-missing, universe-report), GUI panel + adapter, GUI nav tab (data group), report pack entry, stable checklist checks (#65-69), v060 checklist checks, intelligence checklist check, regression tests (~10), docs/data_universe_expansion_v1.1.0.md, .gitignore updates, README/docs refresh
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, Real Data Coverage Required, Mock Data Formal Conclusion DISABLED (unchanged from v1.0.0 core)

---

### v1.0.9 — Final Maintenance Rollup ✅

- **Version:** 1.0.9 — final maintenance release, v1.0.x maintenance line complete
- **Type:** Final Maintenance Rollup — no strategy logic changes, no broker API, no trading
- **Changes:** final_rollup/ package (rollup_schema, release_history, final_health_check, final_smoke_summary, maintenance_plan, final_rollup_engine, final_rollup_store), reports/final_maintenance_rollup_report.py, 6 new CLI commands, GUI panel + adapter, stable checklist checks, v060 checklist checks, intelligence checklist check, regression tests, docs/final_maintenance_rollup_v1.0.9.md, README/docs refresh
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, External API Disabled, VALIDATED does not enable trading (unchanged from v1.0.0)

**v1.0 Maintenance Line: COMPLETE**

---

### v1.0.8 — Local Research Assistant Polish ✅

- **Version:** 1.0.8 — maintenance release based on v1.0.0
- **Type:** Local Research Assistant Polish — no external API, no trading, no strategy changes
- **Changes:** local_assistant/ package (assistant_schema, research_router, research_summarizer, safe_answer_builder, local_assistant_engine, local_assistant_store, local_assistant_query, local_assistant_health), reports/local_research_assistant_report.py, 5 new CLI commands (local-assistant, local-assistant-summary, local-assistant-health, local-assistant-report, local-assistant-explain), GUI panel + adapter, GUI nav tab, report pack entry, stable checklist checks (55-59), v060 checklist checks, intelligence checklist check, regression tests, docs/local_research_assistant_v1.0.8.md, .gitignore updates, README/docs refresh
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, External API Disabled, Local assistant does not enable trading (unchanged from v1.0.0)

---

### v1.0.6 — Example Workflows & Templates ✅

- **Version:** 1.0.6 — maintenance release based on v1.0.0
- **Type:** Example Workflows & Templates — no broker API, no trading, no strategy changes
- **Changes:** workflows/ package (workflow_template_schema, workflow_template_indexer, workflow_template_health, workflow_template_summary), reports/workflow_templates_report.py, 4 new CLI commands (workflow-templates-health, workflow-templates-index, workflow-templates-summary, workflow-templates-report), +5 stable checklist checks (45-49), +3 v060 checklist checks, +1 intelligence checklist check, +15 regression tests, docs/examples/ (10 example files), docs/templates/ (8 template files), GUI nav keywords, report pack entry, .gitignore updates, README refresh, docs/index.md updated, roadmap and release notes updated
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, Templates do not enable trading (unchanged from v1.0.0)

**Next:**
- v1.0.8: Local Research Assistant Polish
- v1.1.0: Data Universe Expansion
- v1.2.0: Replay Training UX
- Broker API branch: only if explicitly requested

---

### v1.0.5 — Documentation & User Guide Polish ✅

- **Version:** 1.0.5 — maintenance release based on v1.0.0
- **Type:** Documentation & User Guide Polish — no broker API, no trading, no strategy changes
- **Changes:** documentation/ package (docs_health_check, docs_indexer, docs_summary), reports/documentation_health_report.py, 4 new CLI commands (docs-health-check, docs-index, docs-summary, documentation-report), +5 stable checklist checks (40-44), +3 v060 checklist checks, +1 intelligence checklist check, +13 regression tests, docs/ v1.0 guides (user_guide, gui_user_guide, cli_cookbook, daily_workflow_sop, troubleshooting, safety_guide, version_map, handoff_guide), GUI nav keywords, report pack entry, .gitignore updates, README refresh, docs/index.md reorganized, roadmap and release notes updated
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, Documentation does not enable trading (unchanged from v1.0.0)

**Next:**
- v1.0.6: Example Workflows & Templates — Done
- v1.1.0: Data Universe Expansion
- v1.2.0: Replay Training UX
- Broker API branch: only if explicitly requested

---

### v1.0.4 — Regression & Release Gate Hardening ✅

- **Version:** 1.0.4 — maintenance release based on v1.0.0
- **Type:** Regression & Release Gate Hardening — no broker API, no trading, no strategy changes
- **Changes:** regression_hardening package (safety_scanner, encoding_utils, regression_summary, release_gate_health), reports/regression_hardening_report.py, 4 new CLI commands (release-gate-health, safety-scan, regression-hardening-summary, regression-hardening-report), +5 stable checklist checks (35–39), +5 v060 checklist checks, +1 intelligence checklist check, +16 regression tests, GUI nav keywords, report pack entry, .gitignore updates, docs
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, Regression does not enable trading (unchanged from v1.0.0)

**Next:**
- v1.1: Data Quality / Universe Expansion

---

### v1.0.3 — GUI Stability & Usability Polish ✅

- **Version:** 1.0.3 — maintenance release based on v1.0.0
- **Type:** GUI Stability & Usability Polish — no broker API, no trading, no strategy changes
- **Changes:** gui/common/ package (gui_safety, gui_threading, table_utils, empty_state, copy_utils), gui/gui_health_check.py, reports/gui_usability_report.py, 2 new CLI commands (gui-health-check, gui-usability-report), +4 stable checklist checks, +3 v060 checklist checks, +1 intelligence checklist check, +11 regression tests, GUI nav entry, report pack entry, .gitignore updates, docs
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, GUI does not enable trading (unchanged from v1.0.0)

**Next:**
- v1.1: Data Quality / Universe Expansion

---

### v1.0.2 — Data & Report Hygiene ✅

- **Version:** 1.0.2 — maintenance release based on v1.0.0
- **Type:** Data & Report Hygiene — review-only inventory, no broker API, no trading
- **Changes:** DataReportHygieneEngine, DataReportHygieneStore, DataReportHygieneQuery, DataReportHygieneReportBuilder, DataReportHygienePanel, DataReportHygieneAdapter, 9 new CLI commands, 5 new stable checklist checks, 4 new v060 checklist checks, 1 new intelligence checklist check, regression suite updates, GUI nav entry, report pack entry, .gitignore updates
- **Safety:** No Real Orders, Production Trading BLOCKED, Data Cleanup Review Only, Archive Suggestions Only, No file deletion (unchanged from v1.0.0)

**Next:**
- v1.1: Data Quality / Universe Expansion

---

### v1.0.1 — Maintenance & Polish ✅

- **Version:** 1.0.1 — maintenance release based on v1.0.0
- **Type:** Polish / hardening — no new features, no broker API
- **Changes:** CLI version-info base release line, stable checklist v1.0.x acceptance, intelligence checklist maintenance check, GUI nav keywords (maintenance, 維護版), regression suite gui-nav-search tests, docs/maintenance_v1.0.1.md
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled (unchanged from v1.0.0)

**Next:**
- v1.1: Data Quality / Universe Expansion

---

### v1.0.0 — Research Trading Cockpit Stable ✅

- **Version:** 1.0.0 — first stable research cockpit release
- **Modules:** 14 modules: Strategy Lab Dashboard, Strategy Validation, Evidence Graph UX, Crash Reversal, Strategy Lab Stable, Training Metrics, Backtest Coach, Strategy Memory, Research Intelligence, Data Coverage, Report Pack, Regression Gate, Paper, Mock Realtime
- **CLI:** `version-info`, `research-cockpit-stable`, `research-cockpit-stable-summary`, `research-cockpit-stable-checks`, `research-cockpit-stable-manifest`, `research-cockpit-stable-report`
- **Safety:** No Real Orders, Production Trading BLOCKED, Broker Execution Disabled, VALIDATED does not enable trading
- **Checklist:** 25 checks — version, safety, modules, GUI, regression, docs, hygiene
- **Report:** `reports/research_trading_cockpit_stable_report_YYYY-MM-DD.md`

**Next:**
- v1.0.x: Maintenance releases — bug fixes, warning cleanup
- v1.1: Data Quality / Universe Expansion

---

### v0.9.2 — Strategy Validation Score ✅
- Cross-module confidence scoring: INSUFFICIENT / OBSERVATIONAL / VALIDATING / VALIDATED / CONFLICTED / REJECTED
- New modules: strategy_validation_schema, strategy_validation_collector, strategy_validation_scorer, strategy_validation_context_builder, strategy_validation_engine, strategy_validation_store, strategy_validation_query
- Report: reports/strategy_validation_report.py
- GUI: Strategy Validation Score tab (StrategyValidationPanel)
- 10 CLI commands: strategy-validation, strategy-validation-summary, strategy-validation-scores, strategy-validation-components, strategy-validation-top, strategy-validation-needs-backtest, strategy-validation-needs-replay, strategy-validation-conflicted, strategy-validation-report, strategy-validation-explain
- VALIDATED = Research Validated Only — does NOT enable trading
- Research Only — No Real Orders

**Next Steps:**
- v0.9.3: Strategy Lab Dashboard Polish — unified layer status board
- v1.0.0: Research Trading Cockpit Stable

---

### v0.9.1 — Evidence Graph UX ✅
- Evidence Thread Quality Board (STRONG/PARTIAL/NEEDS_DATA/NEEDS_BACKTEST/CONFLICTED/ORPHANED)
- Graph Gap View (orphans, missing data, contradictions)
- Crash Reversal Evidence Chain (6-stage: Crash Cause → Stabilization → Relative Strength → EPS Dip Filter → MA Discipline → Risk Guard)
- Evidence Path Explanations (explain-node, explain-thread)
- 7 new CLI commands: evidence-graph-ux, evidence-graph-thread-quality, evidence-graph-gaps, evidence-graph-crash-reversal, evidence-graph-explain-node, evidence-graph-explain-thread, evidence-graph-search
- Registry/checklist/docs updates: capability_matrix, checklist, suite_registry, stable_release_checklist, intelligence_stable_checklist, tab_registry
- Research Only — No Real Orders

**Next Steps:**
- v0.9.2: Strategy Validation Score — cross-module confidence scoring
- v0.9.3: Strategy Lab Dashboard Polish — unified layer status board
- v1.0.0: Research Trading Cockpit Stable

---

### v0.9.0.1 — Crash Reversal & Risk Discipline Strategy Pack ✅
- Crash Cause Classifier (Fundamental/Financial/Technical/Systemic)
- Post-Crash Stabilization Checklist (8 conditions)
- Relative Strength After Crash Score
- Sakata EPS-backed Dip Buy Filter
- Moving Average Profit Discipline
- High-Risk Industry Exposure Guard
- GUI Crash Reversal tab
- CLI: crash-reversal, crash-reversal-summary, crash-reversal-report, crash-reversal-score, crash-reversal-watchlist
- Research Only — No Real Orders

---

## Completed: v0.9.0 — Strategy Lab Stable

**Status:** Done

### Summary

Strategy Lab Stable v0.9.0 wraps all Research OS modules (Research Intelligence v0.7.0–v0.7.1,
Strategy Memory v0.7.2–v0.8.1, Backtest Coach v0.7.3, Training Metrics v0.8.2, Evidence Graph v0.8.3)
into a unified validation layer with a 47-capability matrix, stable checklist (7 categories A-G),
release manifest (JSON + Markdown), 13-section Markdown report, 6 CLI commands, and a GUI panel with
8 summary cards. Safety: `read_only=True`, `no_real_orders=True`, `production_blocked=True`,
`real_order_ready=False`. Does NOT modify any module status, weights, or evidence graph.

**New files:**
- `strategy_lab/` package (schema, capability_matrix, checklist, manifest, engine, store)
- `reports/strategy_lab_stable_report.py`
- `gui/strategy_lab_panel.py`, `gui/strategy_lab_adapter.py`

**Next Steps (updated):**
- v0.9.1: Evidence Graph UX — DONE
- v0.9.2: Strategy Validation Score — cross-module confidence scoring
- v0.9.3: Strategy Lab Dashboard Polish — unified layer status board
- v1.0.0: Research Trading Cockpit Stable

---

## Completed: v0.6.1 — Stable UX Polish

**Status:** Done

### Summary

v0.6.1 is a targeted UX polish release. Key changes: `--type` alias for `--pack-type` in CLI,
smarter report status classification (ENV_LIMITED / NOT_GENERATED), improved health wording so
optional missing and provider-limited reports do not count as release failures.

Research Only. No Real Orders. Production Trading: BLOCKED.

### Modified Files

- `main.py` — `--type` alias, `--mode` no-op for report-pack / report-pack-items
- `report_pack/report_pack_schema.py` — new status constants + OPTIONAL/ENV_LIMITED sets
- `report_pack/report_collector.py` — smarter missing classification
- `report_pack/report_health_checker.py` — optional missing ≠ critical failure
- `report_pack/report_pack_builder.py` — UX wording in index output
- `gui/report_pack_panel.py` — status display improvements
- `gui/stable_release_panel.py` — explanatory note
- `stable_release/stable_release_checklist_v060.py` — PARTIAL pack handling
- `reports/stable_release_v060_report.py` — Report Coverage Notes
- `regression/suite_registry.py` — new --type alias test cases
- `docs/` — updated release notes, roadmap, doc files, new stable_ux_polish_v0.6.1.md

---

## Completed: v0.6.2 — Data Coverage Expansion

**Status:** Done

### Summary

v0.6.2 adds a comprehensive data coverage tracking system across all research domains.
Key deliverables: DataCoverageRegistry (35 items), DataCoverageScanner, DataCoverageEngine,
DataCoverageStore, DataCoverageReport, DataCoveragePanel (GUI), 5 new CLI commands, integration
with report packs, regression suites, stable release checks, and auto report center.

Research Only. No Real Orders. Production Trading: BLOCKED.

### New Files

- `data_coverage/__init__.py`
- `data_coverage/data_coverage_schema.py`
- `data_coverage/data_coverage_registry.py`
- `data_coverage/data_coverage_scanner.py`
- `data_coverage/data_coverage_engine.py`
- `data_coverage/data_coverage_store.py`
- `reports/data_coverage_report.py`
- `gui/data_coverage_panel.py`
- `gui/data_coverage_adapter.py`
- `docs/data_coverage_expansion.md`

### Modified Files

- `main.py` — 5 new CLI commands: data-coverage, data-coverage-summary, data-coverage-items, data-coverage-report, data-coverage-gaps
- `report_pack/report_pack_schema.py` — REPORT_DATA_COVERAGE constant
- `report_pack/report_registry.py` — data_coverage in PACK_FULL
- `report_pack/report_collector.py` — data_coverage pattern map
- `regression/suite_registry.py` — data suite + report suite + release_gate
- `stable_release/stable_release_checklist_v060.py` — data_coverage_engine import check
- `stable_release/capability_matrix.py` — Data Coverage Expansion capability
- `reports/auto_report_center.py` — optional data_coverage in full profile
- `gui/dashboard.py` — Data Coverage tab
- `gui/navigation/tab_registry.py` — data_coverage tab entry
- `.gitignore` — exclude data_coverage runtime outputs

### Completed: v0.7.0 — Research Intelligence Upgrade

**Status:** Done

Research Intelligence pipeline: aggregate signals from 8 source modules → build recommendations →
daily plan (7 items) / weekly plan (12 items) → P0/P1/P2/P3 priority board → CSV persistence → Markdown report.
GUI tab with priority board, daily/weekly plan, all signals table. 9 new CLI commands.
Forbidden action guard (`_validate_action()`) blocks BUY/SELL/ORDER.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Completed: v0.7.1 — Intelligence UX Polish

**Status:** Done

Today Focus card, Why Now / Risk If Ignored columns, `classify_command_safety()` with six labels, Copy Command button, priority/category/source filters, improved CLI output.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Completed: v0.7.2 — Strategy Research Memory

**Status:** Done

Strategy Research Memory extracts and persists 10 memory types (STRATEGY_HYPOTHESIS, RULE_CANDIDATE, REPLAY_MISTAKE_PATTERN, JOURNAL_PATTERN, DATA_GAP, REPORT_GAP, REGRESSION_RISK, PROVIDER_LIMITATION, RESEARCH_CONCLUSION, FOLLOW_UP_TASK) from all Research OS modules. Upsert deduplication by normalized key, status/priority tracking (7 statuses, P0–P3), keyword-heuristic memory linking, 8 CLI commands, GUI panel with table/detail/links views, and 8-section Markdown report.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Completed: v0.7.3 — Backtest-to-Coach Loop

**Status:** Done

Backtest-to-Coach Loop converts backtest weaknesses, replay mistakes, journal patterns, rule issues, strategy memories, and data gaps into safe coach training tasks (PRACTICE_REPLAY, REVIEW_RULE, REVIEW_JOURNAL, FIX_DATA, BACKTEST_MORE, READ_REPORT, UPDATE_MEMORY, WAIT — no trading actions). 7 CLI commands, GUI panel, 8-section Markdown report.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Completed: v0.8.0 — Research Intelligence Stable

**Status:** Done

Research Intelligence Stable validates and stabilizes all Research Intelligence capabilities: Research Intelligence (v0.7.0-v0.7.1), Strategy Memory (v0.7.2), and Backtest-to-Coach Loop (v0.7.3). 29 capabilities across 5 categories (Research Intelligence, Strategy Memory, Backtest Coach, Supporting, Safety), 7-category stable checklist (Import Health, CLI Health, Report Health, Safety, Regression, Runtime, Stable Integration), release manifest (JSON + Markdown), and safety audit. 6 CLI commands, GUI panel (Intelligence Stable tab), Markdown report, CSV store.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Completed: v0.8.1 — Strategy Memory UX

**Status:** Done

Strategy Memory UX v0.8.1 polishes the Strategy Research Memory system: full status lifecycle flow (NEW→REVIEWING→VALIDATING→ACCEPTED/REJECTED/NEEDS_MORE_EVIDENCE), actionable UX fields (needs_action, validation_ready, status_hint, next_step, last_action_at), safe command labelling (SAFE_READ_ONLY/SAFE_REPORT/SAFE_REGRESSION/SAFE_REPLAY/SAFE_DATA_CHECK), 3 new CLI views (validation-queue, active-threads, repeated-patterns), enhanced GUI panel with 7-tab detail view, conservative duplicate detection, memory link improvements (why_linked, suggested_next_step), memory store protected statuses, and Research/Backtest Coach memory integration. All backward compatible. ACCEPTED = research only, never enables trading.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Completed: v0.8.2 — Backtest Training Metrics

**Status:** Done

Backtest Training Metrics v0.8.2 measures training effectiveness across all Research OS modules.
Collects 10 metric types (TASK_COMPLETION, REPLAY_SCORE, MISTAKE_REDUCTION, BACKTEST_ISSUE,
JOURNAL_IMPROVEMENT, MEMORY_VALIDATION, RULE_REVIEW, DATA_FIX_PROGRESS, TRAINING_STREAK,
QUALITY_SCORE) from backtest_coach, replay_training, strategy_memory, journal, and regression outputs.
Computes IMPROVING/STABLE/WORSENING trend per metric. INSUFFICIENT_DATA shown gracefully when source
module not yet run. Full CLI (5 commands), GUI tab, and Markdown report. Integrated into report_pack,
regression suite, stable_release_checklist, intelligence_stable_checklist, auto_report_center,
snapshot_builder, and data_coverage_registry.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Completed: v0.8.3 — Research Intelligence Evidence Graph

**Status:** Done

Research Intelligence Evidence Graph v0.8.3 links all research conclusions across all Research OS
modules into a traceable directed graph. 14 node types (RESEARCH_RECOMMENDATION, STRATEGY_MEMORY,
BACKTEST_COACH_TASK, TRAINING_METRIC, REPLAY_MISTAKE, JOURNAL_PATTERN, DATA_GAP, REPORT_RESULT,
REGRESSION_RESULT, RULE_CANDIDATE, STRATEGY_HYPOTHESIS, PROVIDER_LIMITATION, STABLE_CHECK,
MANUAL_NOTE). 12 edge relations (SUPPORTS, CONTRADICTS, DUPLICATES, REFINES, REQUIRES_DATA,
REQUIRES_BACKTEST, REQUIRES_REPLAY, REQUIRES_JOURNAL_REVIEW, GENERATED_FROM, VALIDATED_BY,
WEAKENED_BY, RELATED_TO). Evidence Threads via BFS max depth 3 from anchor nodes. Conservative
contradiction detection. Safety guard `_guard()` rejects all trading action tokens. Evidence Graph
does NOT auto-modify any module status, weights, or enabled flags. 9 CLI commands, GUI tab
(Evidence Graph), 9-section Markdown report.
Research Only. No Real Orders. Production Trading: BLOCKED.

### Next Steps (Planned)

| Version | Feature | Priority |
|---------|---------|---------|
| v0.9.1 | Evidence Graph UX — thread quality board, gap view, crash reversal chain | Done |
| v0.9.2 | Strategy Validation Score — cross-module confidence scoring | Done |
| v0.9.3 | Strategy Lab Dashboard Polish — unified layer status board | P2 |
| v1.0.0 | Research Trading Cockpit Stable — still No Real Orders unless explicitly enabled | P1 |

---

### Completed: v0.6.3 — Replay Training UI Enhancement

**Status:** Done

Replay Control (Play/Pause timer, speed, Jump/slider), session status bar, enhanced Market View
(OR high/low, VWAP, volume, marker count), marker reason/tags inputs, Drill Table, expanded
Mistake Table, strategy violations display, QThread closeEvent cleanup.
Research Only. No Real Orders. Production Trading: BLOCKED.

---

## Completed: v0.6.0 — Research OS Stable Release

**Status:** Done

### Summary

v0.6.0 consolidates all v0.5.x modules into a stable Research OS. This is NOT a new trading feature release.
Key deliverables: StableCapabilityMatrix (30+ capabilities), StableReleaseChecklistV060 (16 checks, 7 categories),
ReleaseManifestBuilder, KnownLimitationsRegistry (11 limitations), StableReleaseV060Report, GUI panel, 6 CLI commands.

Research Only. No Real Orders. Production Trading: BLOCKED.

### New Files

- `stable_release/__init__.py`
- `stable_release/stable_release_schema.py`
- `stable_release/capability_matrix.py`
- `stable_release/stable_release_checklist_v060.py`
- `stable_release/release_manifest_builder.py`
- `stable_release/known_limitations.py`
- `reports/stable_release_v060_report.py`
- `gui/stable_release_panel.py`
- `gui/stable_release_adapter.py`
- `docs/research_os_stable_release_v0.6.0.md`
- `docs/release_notes_v0.6.md`

### Next Steps (Planned)

| Version | Feature | Priority |
|---------|---------|---------|
| v0.6.1 | Stable UX Polish — CLI alias, status classification | Done |
| v0.6.2 | Data Coverage Expansion — more symbols, sectors, timeframes | P1 |
| v0.6.3 | Replay Training UI Enhancement — chart rendering, drill UI | P1 |
| v0.7.0 | Research Intelligence Upgrade — smarter AI review, pattern library | P2 |

---

## Completed: v0.4.8 — Research Assistant / Coach

**Status:** Done

### Summary

v0.4.8 adds the Research Assistant / Coach — reads Research Review Dashboard output and all subsystems to generate daily/weekly coaching recommendations. Includes daily checklist, weekly checklist, replay training plan, rule review queue, data repair priorities, journal/process coaching, and model/ML coaching.

Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.

### New Files

- `coach/__init__.py`
- `coach/coach_schema.py`
- `coach/checklist_builder.py`
- `coach/research_assistant_engine.py`
- `coach/replay_training_planner.py`
- `coach/rule_review_queue.py`
- `coach/data_repair_planner.py`
- `coach/coach_store.py`
- `reports/research_assistant_report.py`
- `gui/research_assistant_panel.py`
- `gui/research_assistant_adapter.py`
- `docs/research_assistant_coach.md`

### Modified Files

- `main.py` — 7 new CLI commands
- `journal/journal_analytics.py` — `coach_summary()`
- `notifications/notification_center.py` — `coach_summary()`
- `governance/rule_confidence.py` — `coach_rule_review_candidates()`
- `quality/data_quality_gate.py` — `coach_data_repair_candidates()`
- `data/providers/reliability_matrix.py` — `coach_provider_repair_candidates()`
- `notifications/notification_rules.py` — `evaluate_research_coach()`
- `experiments/snapshot_builder.py` — `build_research_coach_snapshot()`
- `reports/auto_report_center.py` — integrated coach summary
- `reports/auto_report_index.py` — 6 coach manifest fields
- `release/regression_suite.py` — 2 new v0.4.8 tests
- `release/stable_release_checklist.py` — 4 new v0.4.8 checks
- `gui/dashboard.py` — added Research Coach tab
- `.gitignore` — research_coach outputs

### Next Steps

v0.5.0 — Research OS Planning / Stabilization

---

## Completed: v0.4.9 — Research Workflow Automation

**Status:** Done

### Summary

v0.4.9 adds Research Workflow Automation — converts Research Coach / Research Review outputs into executable read-only research workflows. Produces daily/weekly research packages with workflow summaries, checklist summaries, report links, and action plans. Safe command registry blocks all forbidden commands (buy/sell/order/git/cd/compound). Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.

### New Files

- `workflow_automation/__init__.py`
- `workflow_automation/workflow_schema.py` — ResearchWorkflowTask / ResearchWorkflowRun schema
- `workflow_automation/safe_command_registry.py` — Allowed command whitelist + forbidden keyword blocking
- `workflow_automation/workflow_builder.py` — Builds workflows from coach/review outputs
- `workflow_automation/workflow_runner.py` — Executes research-only workflow tasks
- `workflow_automation/package_builder.py` — Generates daily/weekly research packages
- `workflow_automation/workflow_store.py` — Persists workflow runs/tasks/summaries to CSV
- `reports/research_workflow_report.py` — Markdown report generator
- `gui/research_workflow_panel.py` — PySide6 GUI panel
- `gui/research_workflow_adapter.py` — GUI bridge
- `docs/research_workflow_automation.md`

### Modified Files

- `main.py` — 5 new CLI commands (research-workflow, research-workflow-report, research-workflow-summary, research-workflow-tasks, research-workflow-package)
- `coach/coach_store.py` — `load_latest_recommendations()`, `load_latest_daily_checklist()`, `load_latest_weekly_checklist()`
- `review/review_store.py` — `get_workflow_summary()`
- `notifications/notification_rules.py` — `evaluate_research_workflow()`
- `experiments/snapshot_builder.py` — `build_research_workflow_snapshot()`
- `reports/auto_report_center.py` — `run_research_workflow_summary()`
- `reports/auto_report_index.py` — 5 workflow manifest fields
- `release/regression_suite.py` — 2 new v0.4.9 tests
- `release/stable_release_checklist.py` — 5 new v0.4.9 checks
- `gui/dashboard.py` — Research Workflow tab
- `.gitignore` — research_workflow outputs gitignored

### Next Steps

v0.5.2 — GUI Tab Grouping / Navigation Polish

---

## Completed: v0.5.1 — CLI Alias / Command UX Polish

**Status:** Done

### Summary

v0.5.1 adds CLI command registry (126 commands), alias map (35 aliases), command discovery, help examples, CLI UX report, and CLI UX GUI panel. No new strategies. No real-order functionality. All existing commands preserved.

### New Package: `cli/`

- `command_registry.py` — 126 commands across 17 categories
- `alias_map.py` — 35 safe aliases, 0 conflicts
- `command_discovery.py` — keyword search and suggest
- `help_examples.py` — quick start, daily, weekly, safety examples
- `cli_ux_report.py` — CLI UX audit builder

### New Report
- `reports/cli_ux_report.py` — 8-section Markdown report

### New GUI
- `gui/cli_ux_panel.py` — CLI UX panel (5 sub-tabs)
- `gui/cli_ux_adapter.py` — bridge

### New Docs
- `docs/cli_alias_command_ux.md`

### New CLI Commands (6 + 17 aliases = 23 total)
- `cli-list`, `cli-search`, `cli-aliases`, `cli-examples`, `cli-ux-report`, `cli-resolve`
- Aliases: `daily`, `quick`, `dq`, `quality`, `providers`, `rules`, `signals`, `journal`, `notify`, `coach-daily`, `review-daily`, `workflow-daily`, `workflow-weekly`, `os`, `version`, `gui`, `dashboard`

### Next Steps

v0.5.2 — GUI Tab Grouping / Navigation Polish — Done

---

## Completed: v0.5.2.1 — Strategy Filter GUI Navigation Integration

**Status:** Done

### Summary

Small integration patch. Strategy Filter tab registered in GUI Navigation registry under `strategy_rules` group with 20+ keywords and aliases. GUI nav search now finds Strategy Filter via strategy, EPS, 財報, 底部翻多, 趨勢紀律, 第二波買點. Stable release checklist and regression suite updated. No v0.5.2 redo. No tab deletion. No real orders.

### Changes
- `gui/navigation/tab_registry.py` — Added `strategy_filter` GUITabMetadata
- `gui/navigation/tab_groups.py` — Updated `strategy_rules` description
- `release/stable_release_checklist.py` — 2 new checks: `strategy_filter_in_gui_navigation`, `strategy_filter_searchable`
- `release/regression_suite.py` — 1 new test: `strategy_filter_gui_nav_searchable`
- `docs/gui_tab_grouping_navigation.md`, `docs/release_notes_v0.5.md`, `docs/roadmap.md`, `README.md` updated

### Next Steps

v0.5.3 — Regression Suite Consolidation

---

## Completed: v0.5.2 — GUI Tab Grouping / Navigation Polish

**Status:** Done

### Summary

GUI tab registry, 8 groups, search, favorites/recent, GUI Navigation tab, 5 CLI commands. No tab deletion — all 24+ existing tabs preserved. No real orders. GUI UX Only.

### New Package: `gui/navigation/`

- `__init__.py`
- `tab_registry.py` — GUITabMetadata + GUITabRegistry (24 tabs registered)
- `tab_groups.py` — GUITabGroupConfig (8 groups)
- `navigation_state.py` — favorites + recent, persisted to config/
- `tab_search.py` — full-text search across all tab metadata
- `navigation_widgets.py` — PySide6 sidebar/search/fav/recent/breadcrumb widgets
- `navigation_report_data.py` — report data builder

### New Files
- `gui/gui_navigation_panel.py` — GUI Navigation panel (5 sub-tabs)
- `gui/gui_navigation_adapter.py` — CLI/panel bridge
- `reports/gui_navigation_report.py` — 7-section Markdown report
- `docs/gui_tab_grouping_navigation.md`
- `config/gui_navigation_state.example.json`

### New CLI Commands (5)
- `gui-nav-summary`, `gui-nav-tabs`, `gui-nav-groups`, `gui-nav-search`, `gui-nav-report`

### Next Steps

v0.5.2.1 — Strategy Filter GUI Navigation Integration (Done)
v0.5.3 — Regression Suite Consolidation

---

## Completed: v0.5.0 — Research OS Planning / Stabilization

**Status:** Done

### Summary

v0.5.0 is a stabilization release. It inventories and audits the entire Research OS: 27 modules, 106 CLI commands, 31 GUI tabs, regression coverage, artifact hygiene, and safety matrix. No new trading strategies. No real-order functionality.

### New Package: `os_planning/`

- `module_inventory.py` — 27 modules, 6 layers, maturity tagging
- `cli_inventory.py` — 106 commands, 13 categories, naming checker
- `gui_tab_inventory.py` — 31 tabs, 7 groups, grouping suggestions
- `regression_audit.py` — 5-dimension coverage audit
- `artifact_hygiene_audit.py` — .gitignore hygiene
- `safety_matrix.py` — safety invariant verification

### New Files

- `reports/research_os_stabilization_report.py` — 7-section report
- `gui/research_os_planning_panel.py` — 6-sub-tab GUI panel
- `gui/research_os_planning_adapter.py` — bridge
- `docs/research_os_planning.md`
- `docs/release_notes_v0.5.md`

### Integrations

- `reports/auto_report_center.py` — `run_research_os_summary()`
- `reports/auto_report_index.py` — 5 OS manifest fields
- `release/regression_suite.py` — 2 new v0.5.0 tests
- `release/stable_release_checklist.py` — 4 new v0.5.0 checks
- `gui/dashboard.py` — Research OS Planning tab
- `.gitignore` — research_os_planning outputs gitignored

### v0.5.x Roadmap

| Version | Focus |
|---------|-------|
| v0.5.1 | CLI Alias Polish |
| v0.5.2 | GUI Tab Grouping |
| v0.5.3 | Regression Consolidation |
| v0.5.4 | Report Pack |
| v0.5.5 | Data / Feature Store Stabilization |
| v0.5.6 | TW Replay Training Cockpit |
| v0.6.0 | Stable Release |

---

## Completed: v0.4.7 — Research Review Dashboard

**Status:** Done

### Summary

v0.4.7 adds the Research Review Dashboard — a unified daily/weekly research review aggregator. Aggregates Notification Center, Portfolio Journal, Experiment Registry, Rule Governance, Model Monitoring, Intraday Replay, Data Quality Gate, Provider Reliability, Signal Quality, and ML Knowledge Integration into a single dashboard with Scorecard, Review Items, Top Mistakes, Weak Rules, Data Blockers, and Action Plan.

Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.

### New Files

- `review/__init__.py` — package init
- `review/review_schema.py` — `ReviewItem` dataclass; 12 review_type / 6 severity / 12 category / 5 status constants
- `review/review_aggregator.py` — `ResearchReviewAggregator`: collects from 9 subsystems, builds ReviewItems and dashboard summary
- `review/review_scorecard.py` — `ResearchReviewScorecard`: calculates 9 dimension scores (STRONG/GOOD/PARTIAL/WEAK/BLOCKED/UNKNOWN)
- `review/review_action_planner.py` — `ReviewActionPlanner`: converts ReviewItems to prioritized Action Plan (P0-P3); research-only commands
- `review/review_store.py` — `ResearchReviewStore`: saves/loads 4 CSV files to `data/backtest_results/research_review/` (gitignored)
- `reports/research_review_dashboard_report.py` — `ResearchReviewDashboardReport`: 10-section Markdown report
- `gui/research_review_dashboard_panel.py` — `ResearchReviewDashboardPanel`: PySide6 panel with 6 inner tabs, QThread workers
- `gui/research_review_dashboard_adapter.py` — `ResearchReviewDashboardAdapter`: GUI bridge

### Modified Files

- `main.py` — 4 new CLI commands: research-review, research-review-report, research-review-summary, research-review-actions
- `journal/journal_analytics.py` — added `build_review_summary()`
- `notifications/notification_center.py` — added `get_review_summary()`
- `governance/rule_confidence.py` — added `rules_needing_review()`
- `quality/data_quality_gate.py` — added `get_blockers_summary()`
- `data/providers/reliability_matrix.py` — added `get_warning_summary()`
- `analysis/signal_quality_engine.py` — added `get_weak_signal_summary()`
- `notifications/notification_rules.py` — added `evaluate_research_review()`
- `experiments/snapshot_builder.py` — added `build_research_review_snapshot()`
- `reports/auto_report_center.py` — integrated research review summary
- `reports/auto_report_index.py` — added research review manifest fields
- `release/regression_suite.py` — 2 new v0.4.7 tests
- `release/stable_release_checklist.py` — 3 new v0.4.7 checks
- `gui/dashboard.py` — added Research Review tab
- `README.md`, `docs/roadmap.md`, `docs/release_notes_v0.4.md`, `docs/index.md`

### Next Suggested

v0.4.8: Research Assistant / Coach
- Daily research checklist based on Review Dashboard results
- Replay training menu
- Rule review queue
- No buy/sell instructions, no real orders

---

## Completed: v0.4.6 — Portfolio Journal & Trade Review

**Status:** Done

**New files:**
- `journal/__init__.py`, `journal/journal_schema.py`, `journal/journal_store.py`, `journal/signal_outcome_tracker.py`, `journal/replay_training_notes.py`, `journal/mistake_taxonomy.py`, `journal/journal_analytics.py`
- `reports/portfolio_journal_report.py`
- `gui/portfolio_journal_adapter.py`, `gui/portfolio_journal_panel.py`
- `docs/portfolio_journal_trade_review.md`

**Modified files:**
- `main.py` — 7 new CLI commands (journal-add/list/show/review/summary/report/link-replay)
- `gui/dashboard.py` — "Portfolio Journal" tab
- `notifications/notification_rules.py` — `evaluate_portfolio_journal()` (review_required + repeated mistake tag alerts)
- `reports/auto_report_center.py` — `run_portfolio_journal_summary()`, `include_portfolio_journal` flag
- `reports/auto_report_index.py` — 4 new manifest fields
- `experiments/snapshot_builder.py` — `build_portfolio_journal_snapshot()`
- `release/regression_suite.py` — 2 new v0.4.6 tests
- `release/stable_release_checklist.py` — 3 new v0.4.6 checks
- `.gitignore` — journal output patterns
- `README.md`, `docs/roadmap.md`, `docs/release_notes_v0.4.md`, `docs/index.md`

**Safety:** Journal Only. No real orders. No broker connection. production_blocked=True. journal_data/ gitignored.

---

## Completed: v0.4.5 — Notification Center

**Status:** Done

**New files:**
- `notifications/__init__.py`, `notification_schema.py`, `notification_center.py`, `notification_rules.py`, `local_notifier.py`, `external_notifier_placeholder.py`, `notification_preferences.py`
- `reports/notification_center_report.py`
- `gui/notification_center_adapter.py`, `gui/notification_center_panel.py`
- `docs/notification_center.md`
- `config/notification_preferences.example.json`

**Modified files:**
- `main.py` — 5 new CLI commands (notification-scan/list/report/clear-read/test)
- `gui/dashboard.py` — "Notification Center" tab
- `reports/auto_report_center.py` — `run_notification_center_report()`, `include_notification_center` flag
- `reports/auto_report_index.py` — 4 new manifest fields
- `experiments/snapshot_builder.py` — `build_notification_snapshot()`
- `release/regression_suite.py` — 2 new v0.4.5 tests
- `release/stable_release_checklist.py` — 4 new v0.4.5 checks
- `.gitignore` — notification output patterns
- `README.md`, `docs/roadmap.md`, `docs/release_notes_v0.4.md`, `docs/index.md`

**Safety:** No real orders. external_enabled=False always. production_blocked=True is safe state.

---

## Completed: v0.3.26 — Backtest Engine Hardening

- `ExecutionModel`: signal_close / next_open / next_close / vwap_proxy entry; stop_loss, take_profit, trailing_stop, time_stop, combined exit
- `CostModel`: Taiwan defaults (0.1425%×0.6 commission, 0.3% tax, 5bps slippage, min 20 NTD); zero-cost preset
- `LiquidityFilter`: min volume 500, min turnover 10M NTD, max participation 5%; 0–100 liquidity score
- `GapRiskModel`: 5-category gap classifier; gap stop-loss; no-chase-gap logic
- `ValidationSplit`: walk_forward / out_of_sample / expanding_window / in_sample_only
- `MarketRegimeSplitter`: bull/bear/sideways/high_volatility via MA20/MA60 + rolling vol; proxy fallback
- `HardenedBacktester`: orchestrator; A/B/C/D confidence grade; saves 5 result files
- `HardenedBacktestReportBuilder`: 10-section Markdown report
- `HardenedBacktestPanel`: PySide6 GUI tab with controls, summary cards, assumption/metrics/split/regime tables
- `HardenedBacktestAdapter`: GUI bridge (no subprocess)
- CLI: `python main.py hardened-backtest [options]`
- `AutoReportCenter` full profile includes hardened backtest
- No real orders. Production BLOCKED.

---

## Completed: v0.3.25 — Universe Expansion & Sector Classification

- `UniverseRegistry`: 13 universe groups (core_14–core_200 + 8 theme groups); build_default_universes(), export_universe_manifest()
- `SectorClassifier`: 9-sector / 25+ theme taxonomy; classify_symbol(), classify_universe(), get_sector_summary()
- `UniverseQualityAnalyzer`: 0–100 score (6 components); readiness levels INSUFFICIENT → STRONG_RESEARCH_UNIVERSE
- `UniverseExpander`: propose_expansion() — proposals only, no auto-write; ranked by AI exposure + data availability
- `UniverseExpansionReportBuilder`: 8-section Markdown report
- `UniverseManagerPanel`: GUI tab (Universe Manager) with selector, symbol table, sector summary, quality cards
- `UniverseManagerAdapter`: GUI bridge (list_universes, load_universe, build_default_universes, analyze_quality, generate_report)
- CLI: `python main.py universe-list | universe-build-defaults | universe-show | universe-quality-score | universe-expand | universe-report`
- `DataProviderAutoFetcher` accepts `universe_name` parameter
- `DailyResearchWorkflow` accepts `universe_name` parameter
- `DataQualityGate` accepts `universe` parameter for symbol-level coverage scoring
- `AutoReportCenter` accepts `universe_name` parameter, records in manifest
- No mock fallback in real mode. No real orders. Production BLOCKED.

---

## Completed: v0.3.24 — Data Provider Reliability & Fallback Matrix

- `ProviderReliabilityMatrix`: builds dataset fallback chains, provider reliability scores, dataset confidence scores
- `ProviderMetricsCollector`: reads logs to compute success rates
- `DatasetConfidenceScorer`: 0–100 confidence per dataset (6-component weighted formula)
- `ProviderReliabilityReportBuilder`: Markdown report with 8 sections
- `ProviderReliabilityPanel`: GUI tab (Provider Reliability)
- CLI: `python main.py provider-reliability [--report] [--dataset X] [--provider X]`
- No mock fallback in real mode. No real orders. Production BLOCKED.

---

## Completed: v0.3.27 — Intraday / Tick Data Pipeline

- `IntradaySchema`: standard column spec, XQ column map, validation, Taiwan session filter
- `IntradayDataPipeline`: discovers raw intraday CSV/XLSX, normalizes to standard schema, writes `intraday_standard/{freq}/`
- `IntradayQualityChecker`: scans standardized files; quality statuses OK/PARTIAL/MISSING/STALE/DUPLICATED/PRICE_ANOMALY/VOLUME_ANOMALY/INSUFFICIENT; 0–100 quality score
- `OpeningRangeFeatureBuilder`: opening 5/15/30-min return, volume ratio, range %, high/low break, strength score
- `VWAPFeatureBuilder`: intraday VWAP, price-vs-VWAP%, slope, above-VWAP ratio, reclaim/lost, support score
- `FakeBreakoutDetector`: high/low break confirmation, volume confirmation, fake breakout risk/score, chase risk score
- `IntradayVolumeProfileBuilder`: volume by bar, cumulative VWAP, high-volume price zones, session volume distribution
- `MicrostructureQualityChecker`: tick_api_ready=False, bidask_api_ready=False; status INTRADAY_BAR_ONLY/TICK_PLANNED
- `TickBidaskSchema`: placeholder schema for future tick/bidask API (v0.4+)
- `IntradayPipelineReportBuilder`: Markdown report with quality, features, fake breakout, volume profile, tick readiness
- `IntradayPipelinePanel`: PySide6 GUI tab with quality table, feature preview, fake breakout, volume profile, tick status
- `IntradayPipelineAdapter`: GUI bridge (run_pipeline, check_quality, preview_features)
- CLI: `python main.py intraday-pipeline [--mode] [--freq] [--dry-run] [--report]`; `intraday-quality [--freq]`; `intraday-features --stock [--freq]`
- Integration: `DataFreshnessChecker` adds `intraday_1min`/`intraday_5min`; `DataQualityGate` uses `IntradayQualityChecker`; `AutoReportCenter` full/daily profiles include intraday pipeline; manifest records `intraday_quality_score`/`intraday_status`/`tick_bidask_readiness`; `features/microstructure.py` enriches last bar with opening range/VWAP/fake breakout; `features/indicators.py` prefers standardized path
- `IntradayDataImporter` adds `load_intraday_standard()` method
- No real orders. Production BLOCKED.

---

## Completed: v0.3.28 — Strategy Rule Governance

- `RuleMetadata`: dataclass with rule_id, category, version, status, confidence, sample_count, dependencies, safety_flags
- `RuleRegistry`: 53 built-in rules across 8 categories (buy_point, screener, strategy_knowledge, long_term, portfolio, signal_quality, intraday, governance/backtest assumption)
- `RuleDependencyGraph`: adjacency-list dependency graph; cycle detection; topological ordering; high-impact rule identification
- `RuleConfidenceScorer`: 0–100 scoring with degradation for experimental, low sample count, mock-only results; confidence levels HIGH/GOOD/PARTIAL/WEAK/LOW/UNKNOWN/PLANNED
- `RuleChangeLog`: append-only JSONL change log (runtime output → `logs/governance/`, not committed)
- `RuleSnapshotBuilder`: exports snapshot JSON + CSV to `data/backtest_results/` (not committed)
- `RuleGovernanceReportBuilder`: 8-section Markdown governance report
- `RuleGovernancePanel`: PySide6 GUI with safety banner, summary cards, rule table, dependency table, review queue, action buttons; QThread workers
- `RuleGovernanceAdapter`: GUI bridge (run_governance, generate_report, export_snapshot)
- CLI: `python main.py rule-governance [--mode] [--category] [--status] [--report] [--snapshot]`
- Integration: `AutoReportCenter` full profile includes rule governance; manifest records governance fields; `SignalQualityEngine` maps recommendations to rule_ids; `RuleWeightConfig` adds `rule_governance_refs`; `HardenedBacktester` outputs `assumption_rule_ids`; intraday feature builders output `feature_rule_id`
- Rule IDs follow format: CATEGORY.TIMEFRAME.NAME.VERSION (e.g. BUY.SHORT.PULLBACK_10MA.V1)
- Tick/bidask rules: status EXPERIMENTAL, confidence PLANNED — not pretending ready
- No auto-apply weights. No auto-enable rules. No real orders. Production BLOCKED.

---

## Completed: v0.3.29 — Research Notebook / Experiment Registry

- `ExperimentMetadata`: dataclass with experiment_id (EXP-YYYYMMDD-HHMMSS-shortuuid), name, type, status, mode, profile, git_commit, git_tag, universe, snapshots, reports; 6 status constants; 8 type constants
- `ExperimentRegistry`: create/register/list/get/update/archive experiments; stores `experiments/{id}/metadata.json`, snapshots/, reports/, notes.md; `registry.json` index; runtime outputs not committed
- `ExperimentSnapshotBuilder`: 10 snapshot types — config, universe, data_quality, provider_reliability, rule_governance, backtest, signal_quality, portfolio, intraday, reports; build_all(); summarizes only, no large data copies
- `ExperimentComparator`: compare_two() / compare() — scores/backtest/data_quality/rules/universe; IMPROVED/WORSENED/UNCHANGED/INSUFFICIENT_DATA; IMPROVED ≠ ready for real trading
- `ExperimentNotebookBuilder`: build_notebook() → `{id}/notebook.md`; 10 sections
- `ExperimentRegistryReportBuilder`: 6-section Markdown report → `reports/experiment_registry_report_YYYY-MM-DD.md`
- `ExperimentRegistryPanel`: PySide6 GUI with safety banner, summary cards, experiment table, snapshot table, compare panel, notebook preview, action buttons; QThread workers
- `ExperimentRegistryAdapter`: GUI bridge
- CLI: `python main.py experiment-create|register-latest|list|show|notebook|compare|report|snapshot`
- Integration: `DailyResearchWorkflow` accepts `register_experiment=False`; `AutoReportCenter` full profile includes experiment_registry; "Experiment Registry" tab in cockpit
- `experiments/` runtime excluded from git; `experiments/.gitkeep` committed
- No real orders. Production BLOCKED.

---

## Completed: v0.4.1.1 — Strategy Knowledge Ingestion from Transcripts

**Status:** Done

- `TranscriptSource` — source metadata (source_id, title, author, source_type, media_source, video_id, transcript_hash, source_confidence); from_file(), to_dict(), hash_text()
- `TranscriptLoader` — discovers `.txt`/`.md` files in 4 default dirs; parse_sections(), extract_metadata(), normalize_text(); no crash on missing dirs; no OCR; no network fetch
- `StrategyKnowledgeItem` — knowledge item dataclass with 17 fields; 11 category types; 5 polarity types; 6 timeframe types; to_dict()
- `StrategyKnowledgeExtractor` — rule-based keyword extraction (no external LLM API); 8 extraction methods covering entry/exit/avoid/risk/market_regime/position_sizing; handles 阪田戰法 + 獅公 long-cycle risk patterns; confidence capped at PARTIAL for transcript sources
- `RuleCandidateMapper` — maps knowledge items to Rule Governance rule_ids; generates `suggested_rule_id` for unknown rules; `auto_activated=False` always; `governance_status=CANDIDATE` for new rules
- `StrategyKnowledgeStore` — CSV persistence; 6 output files (sources, knowledge_items, rule_candidates, avoid_conditions, risk_conditions, factor_candidates); never writes tokens; build_summary()
- `StrategyKnowledgeIngestionPipeline` — 7-step orchestrator; supports dry_run; reports files_discovered/loaded/items_count/rule_candidates/etc.; `production_blocked=True`
- `StrategyKnowledgeIngestionReportBuilder` — 9-section Markdown report; not committed
- `StrategyKnowledgeIngestionPanel` — PySide6 GUI with safety banner, 6 summary cards, source table, knowledge items table, rule candidate table, risk/avoid notice; QThread workers
- `StrategyKnowledgeIngestionAdapter` — GUI bridge (run_ingestion, generate_report, load_latest_summary, load_latest_report_path, load_sources, load_items, load_rule_candidates)
- `RuleRegistry` — 6 new transcript-candidate risk rules (NEEDS_REVIEW, confidence=PLANNED): TOP_PATTERN, MARKET_NEW_HIGH_STOCK_LAG, CRASH_WATCH, REVENUE_NOT_SUPPORTING_THEME, OVER_CONCENTRATION, MARGIN_USAGE
- `RuleConfidenceScorer` — transcript-only rule confidence capped at PARTIAL; CRASH_WATCH capped at PLANNED
- `ExperimentSnapshotBuilder` — `build_strategy_knowledge_snapshot()` added
- `AutoReportCenter` — `run_strategy_knowledge_ingestion_summary()` added; full + daily profiles include `include_strategy_knowledge_ingestion`
- `AutoReportIndexBuilder` — manifest includes 4 new strategy knowledge fields
- `RegressionSuite` — 3 new v0.4.1.1 tests (imports, summary, dry_run)
- `StableReleaseChecklist` — 3 new v0.4.1.1 checks (import, no_auto_activate, artifacts_ignored)
- GUI: Strategy Knowledge tab added to cockpit dashboard
- CLI: `strategy-knowledge-ingest`, `strategy-knowledge-summary`
- Docs: `docs/strategy_knowledge_ingestion.md`
- Knowledge Only. Research Only. No Real Orders. auto_activated=False. Production BLOCKED.

---

## Completed: v0.4.0 — Research Platform Stable Release

- `VersionInfo`: centralized version class; version=v0.4.0; get_version_info(), print_version_info(), get_safety_banner(), get_feature_summary()
- `StableReleaseChecklist`: 18-item checklist (compileall, import health, GUI, workflow, quality gate, provider reliability, intraday, backtest, rule governance, experiment registry, auto report, usability, paper, mock realtime, git safety, artifact ignore, token leak, real order check); PASS/PARTIAL/BLOCKED
- `RegressionSuite`: quick (7 tests) + full (14 tests) suites; CSV output; PASS/PARTIAL/FAIL
- `StableReleaseReportBuilder`: 7-section Markdown stable release report
- `ReleaseStatusPanel`: PySide6 GUI with version cards, feature coverage table, regression table, actions; QThread workers
- `ReleaseStatusAdapter`: GUI bridge
- CLI: `python main.py version-info | stable-release-check | regression-suite | stable-release-report`
- `gui/dashboard.py` adds "Release Status" tab
- v0.3.x features verified and regression-tested; no new strategies; no production trading
- No real orders. Production BLOCKED.

---

## Completed: v0.4.1 — API Fetch Productionization

**Status:** Done

- `TokenSetupAssistant` — reads .env without modifying; masks tokens; validates safety; generates setup instructions
- `RetryPolicy` — exponential backoff for TIMEOUT/NETWORK/RATE_LIMIT/SERVER_ERROR; never used for orders
- `APICache` (providers) — SHA-256 keyed, token-sanitized, TTL=24h; stats/cleanup; stored in `data_cache/api/`
- `DataLineageTracker` — LIN-XXXXXXXXXX IDs; per-fetch/write records; URL masking; CSV export
- `APIFetchDiagnostics` — aggregates provider/dataset results; sanitized messages; recommended_action
- `TWSETPEXParser` — alias mapping, comma numerics, ROC year conversion, SCHEMA_CHANGED/PARTIAL
- `MOPSFinancialParser` — estimated announcement dates (Q1/Q2/Q3=45d, Q4=90d), timing_quality, announcement_date_is_estimated
- `APIFetchProductionReportBuilder` — 8-section Markdown report
- `APIFetchStatusPanel` / `APIFetchStatusAdapter` — GUI tab with QThread workers; never shows full token
- 5 new CLI commands: `api-token-check`, `api-cache-status`, `api-fetch-diagnostics`, `api-cache-cleanup`, `api-fetch-production-report`
- Still not production trading; no real orders

---

## Completed: v0.4.2 — ML Feature Store v1

**Status:** Done

- `FeatureCatalog` — 50+ built-in features across 16 categories; leakage_risk LOW/MEDIUM/HIGH; experimental flag
- `FeatureSnapshotBuilder` — extracts feature matrix from daily_k, institutional, fundamental, intraday sources
- `LabelGenerator` — fwd_return_Nd, classification (label_direction_Nd, label_up/down_3pct), triple barrier labels
- `MLSplitManager` — default time_series split (60/20/20 by date); symbol_grouped; walk_forward; random with leakage warning
- `DataLeakageChecker` — 7 finding types; status CLEAN/WARNING/LEAKAGE_RISK/BLOCKED_FOR_TRAINING
- `FeatureQualityChecker` — missing_ratio, constant_features, label_balance, feature_quality_score (0-100)
- `FeatureImportanceShell` — Pearson correlation; sklearn mutual info (optional, graceful fallback)
- `MLFeatureDatasetBuilder` — features + labels + split + metadata; writes model_ready_dataset_*.csv (not committed)
- `MLFeatureStoreReportBuilder` — 9-section Markdown report (not committed)
- `MLFeatureStoreAdapter` / `MLFeatureStorePanel` — GUI tab with QThread workers; safety banner
- 8 new CLI commands: `ml-feature-catalog`, `ml-feature-snapshot`, `ml-labels`, `ml-build-dataset`, `ml-leakage-check`, `ml-feature-quality`, `ml-feature-importance`, `ml-feature-store-report`
- Label columns always prefix `label_` or `fwd_` — never mixed with features
- No live prediction. No auto-trading. No real orders. Production BLOCKED.

---

## Completed: v0.4.2.1 — ML Feature Store Knowledge Integration

**Status:** Done

- `KnowledgeFeatureBridge` — converts v0.4.1.1 transcript CSVs (factor/rule/avoid/risk candidates) to ML feature metadata; auto_enabled=False; confidence capped at PARTIAL
- `KnowledgeFeatureCatalog` — manages transcript-derived feature catalog; register/list/get/export; enforces auto_enabled=False
- `KnowledgeFeatureReadinessChecker` — READY/PARTIAL/METADATA_ONLY/NEEDS_MAPPING/NEEDS_BACKTEST/BLOCKED/LEAKAGE_RISK/INSUFFICIENT_DATA assessment
- `KnowledgeLeakageChecker` — POST_EVENT_KNOWLEDGE, TIMING_ESTIMATED, LONG_CYCLE_RISK, PATTERN_INCOMPLETE, UNVALIDATED_CANDIDATE detection
- `KnowledgeDatasetExporter` — exports 4 output files: catalog.csv, readiness.csv, leakage.csv, model_ready_schema.json
- `MLKnowledgeIntegrationReport` — 7-section Markdown report
- `MLKnowledgeIntegrationPanel` / `MLKnowledgeIntegrationAdapter` — GUI tab with QThread workers, 6 summary cards, safety banner
- long_cycle_risk → METADATA_ONLY, not_for_short_term_label=True always
- model_ready_schema includes only READY/PARTIAL features with no critical leakage, excluded from training by default
- 3 new CLI commands: `ml-knowledge-integrate`, `ml-knowledge-leakage-check`, `ml-knowledge-feature-summary`
- `AutoReportCenter` — `run_ml_knowledge_integration_summary()` added; full + daily profiles include `include_ml_knowledge_integration`
- `AutoReportIndexBuilder` — manifest includes 5 new ML knowledge fields
- `RegressionSuite` — 2 new v0.4.2.1 tests (imports, bridge_empty)
- `StableReleaseChecklist` — 3 new v0.4.2.1 checks (import, auto_enabled_false, artifacts_ignored)
- GUI: ML Knowledge Integration tab added to cockpit dashboard
- No model training. No real orders. Production BLOCKED.

---

## Completed: v0.4.3 — Model Monitoring Framework

**Status:** Done

- `ModelRegistry` — model metadata storage; register/list/get/update; JSON files in `model_monitoring/`; not committed
- `PredictionLog` — append-only JSONL prediction records; load/filter/summarize; update_actuals from price data
- `HitMissReviewer` — hit rate, precision, recall, grouping by symbol/rule/model/source; INSUFFICIENT_DATA when no actuals
- `DriftDetector` — feature distribution drift, missing ratio drift, label drift, prediction score drift; STABLE/WATCH/DRIFT_WARNING/DRIFT_CRITICAL/INSUFFICIENT_DATA
- `SignalDegradationMonitor` — rule/signal quality/portfolio degradation checks; STABLE/WATCH/DEGRADED/SEVERE
- `RuleVsMLComparator` — agreement rate, disagreement cases, hit rate comparison; ML_NOT_AVAILABLE when no ML predictions
- `ModelMonitoringSummary` — orchestrates all monitors; next_actions list
- `ModelMonitoringReportBuilder` — 8-section Markdown report (not committed)
- `ModelMonitoringAdapter` / `ModelMonitoringPanel` — GUI tab with QThread workers; safety banner
- 9 new CLI commands: `model-monitoring`, `model-monitoring-report`, `model-registry-list`, `model-register`, `prediction-log`, `prediction-review`, `drift-check`, `signal-degradation`, `rule-vs-ml`
- No live prediction. No auto-trading. No real orders. Production BLOCKED.

---

## Completed: v0.4.4 — Intraday Replay Cockpit

**Status:** Done

- `ReplaySession` / `ReplaySessionManager` — session lifecycle (CREATED/RUNNING/PAUSED/COMPLETED/FAILED/ARCHIVED); stored in `replay_sessions/` (not committed)
- `IntradayReplayEngine` — discovers 1min/5min CSV at `data/import/intraday_standard/{freq}/`; INSUFFICIENT_INTRADAY_DATA on missing data; no future leakage
- `ReplayEventBuilder` — 12 event types; visible_at_index = bar_index (no lookahead)
- `OpeningRangeReplay` — 15-min opening range; 6 breakout/failed states
- `VWAPReplay` — cumulative VWAP = (close×vol).cumsum() / vol.cumsum(); price vs VWAP overlay
- `FakeBreakoutReplay` — 10-bar high breakout detection; failed breakout warning; 5-level risk
- `VolumeProfileReplay` — 20-bin volume profile; POC; value area (70%); support pressure state
- `StrategyReplayOverlay` — reads existing research data; NEVER calls broker/submit_order; signals labeled as training annotations
- `ReplayTrainingMode` — 6 question types (entry/exit/breakout/fake/vwap/volume); A–F grading; answers NOT trading instructions
- `ReplayMetrics` — bars_replayed, quiz_accuracy, training_score, grade; summarize_sessions()
- `IntradayReplayReportBuilder` — 8-section Markdown report (not committed)
- `IntradayReplayAdapter` / `IntradayReplayPanel` — GUI tab with QThread workers; safety banner
- 5 new CLI commands: `intraday-replay`, `intraday-replay-report`, `replay-session-list`, `replay-session-show`, `replay-training-summary`
- No live prediction. No broker connection. No real orders. Replay Training Only.

---

## Planned: v0.4.5 — Notification Center

**Target:** Research alerts, scheduled summary notifications, email/webhook (read-only)

---

## Planned: v0.3.28 (old roadmap — superseded)

**Target:** Signal quality improvements

- Multi-period signal quality scoring (not just latest day)
- Signal stability metric (how consistent is the recommendation over N days)
- Rule dependency analysis (correlated rules detection)

---

## Planned: v0.4.0

**Target:** Architecture consolidation

- Unified data model (replace ad-hoc dict structures with dataclasses)
- Plugin architecture for custom rules
- Config file support (`config.yaml`) for provider tokens and thresholds
- Full test suite (pytest) with real data fixtures

**Safety constraints remain unchanged in v0.4.x:**
- PRODUCTION_BLOCKED=True
- REAL_ORDER_READY=False
- No broker connections

---

## Non-Goals (Permanent)

The following are explicitly out of scope for all future versions:

| Non-Goal | Reason |
|----------|--------|
| Real order execution | Research platform only |
| Broker API integration (Shioaji, Mega, etc.) | Out of scope |
| Investment advice generation | Not a registered advisor; legal constraint |
| Auto weight application | Manual review required; safety constraint |
| Cloud deployment | Local research tool |
| Multi-user access | Single-user research tool |

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
