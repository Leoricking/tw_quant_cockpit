# TW Quant Cockpit — Release Notes v0.9.x

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] All versions in this file are Strategy Lab Stable releases only.**

---

## v0.9.3 — Strategy Lab Dashboard Polish

**Released:** 2026-06-10

### Overview

v0.9.3 introduces the Strategy Lab Dashboard — a unified single-view dashboard that
summarizes validation grades, evidence graph health, crash reversal risks, training metrics,
coach tasks, strategy memories, and research intelligence into one place.

No BUY/SELL/ORDER. No trading actions. Production Trading: BLOCKED.
`read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`.

### New Modules

| Module | Description |
|--------|-------------|
| `strategy_lab/strategy_lab_dashboard_schema.py` | Dataclasses: StrategyLabDashboardCard, StrategyLabDashboardRow, StrategyLabActionItem, StrategyLabDashboardSummary; `_guard()` |
| `strategy_lab/strategy_lab_dashboard_engine.py` | Collects context from all sub-stores and builds cards, rows, actions, summary |
| `strategy_lab/strategy_lab_dashboard_store.py` | CSV persistence for cards, rows, actions, summary |
| `strategy_lab/strategy_lab_dashboard_query.py` | Query helpers: list_cards, list_rows, list_actions, top_priorities, needs_backtest, needs_replay, needs_data, conflicted, explain_dashboard |
| `reports/strategy_lab_dashboard_report.py` | Markdown report generator with 9 sections |

### GUI

- `gui/strategy_lab_dashboard_panel.py` — StrategyLabDashboardPanel: Strategy Lab Dashboard tab with summary cards, filter bar, 6 tabs, action buttons
- `gui/strategy_lab_dashboard_adapter.py` — StrategyLabDashboardAdapter: GUI ↔ backend bridge

### CLI Commands (9)

| Command | Description |
|---------|-------------|
| `strategy-lab-dashboard` | Run full Strategy Lab Dashboard engine |
| `strategy-lab-dashboard-summary` | Print summary from store |
| `strategy-lab-dashboard-cards` | List dashboard cards |
| `strategy-lab-dashboard-actions` | List dashboard action items |
| `strategy-lab-dashboard-priorities` | Show top priority actions |
| `strategy-lab-dashboard-needs-backtest` | Strategies needing more backtest |
| `strategy-lab-dashboard-needs-replay` | Strategies needing more replay |
| `strategy-lab-dashboard-needs-data` | Strategies with data gaps |
| `strategy-lab-dashboard-report` | Generate Markdown report |

### Safety

- `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`
- `_guard()` rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE
- No BUY/SELL/ORDER output in any command or report
- Research Only. Not Investment Advice.

---

## v0.9.2 — Strategy Validation Score

**Released:** 2026-06-09

### Overview

v0.9.2 introduces Strategy Validation Score — a cross-module confidence scoring system that grades
each tracked strategy as INSUFFICIENT / OBSERVATIONAL / VALIDATING / VALIDATED / CONFLICTED / REJECTED
based on evidence collected from backtest metrics, replay scores, coach tasks, training metrics, and
evidence graph support. VALIDATED = Research Validated Only and does NOT enable or imply real trading.
No BUY/SELL/ORDER. No trading actions. Production Trading: BLOCKED.
`read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`.

### New Modules

| Module | Description |
|--------|-------------|
| `strategy_validation/strategy_validation_schema.py` | Dataclasses: StrategyValidationScore, StrategyValidationSummary, StrategyValidationComponent; grade constants; `_guard()` |
| `strategy_validation/strategy_validation_collector.py` | Collects evidence from backtest, replay, coach, training_metrics, evidence_graph |
| `strategy_validation/strategy_validation_scorer.py` | Computes component scores and final validation grade |
| `strategy_validation/strategy_validation_context_builder.py` | Builds context dict for each strategy |
| `strategy_validation/strategy_validation_engine.py` | Master orchestration engine (read_only, no real orders, validated_does_not_enable_trading=True) |
| `strategy_validation/strategy_validation_store.py` | CSV persistence for scores, components, summary |
| `strategy_validation/strategy_validation_query.py` | Query helpers: list_scores, top_validated, needs_backtest, needs_replay, conflicted, explain_score |
| `reports/strategy_validation_report.py` | Markdown report generator |

### GUI

- `gui/strategy_validation_panel.py` — StrategyValidationPanel: Strategy Validation Score tab with grade summary cards, scores table, component breakdown, safety notice

### CLI Commands (10)

| Command | Description |
|---------|-------------|
| `strategy-validation` | Run full Strategy Validation Score engine |
| `strategy-validation-summary` | Print summary from store |
| `strategy-validation-scores` | List all validation scores (filter by --grade, --limit) |
| `strategy-validation-components` | List validation components |
| `strategy-validation-top` | Show top validated strategies |
| `strategy-validation-needs-backtest` | Strategies needing more backtest |
| `strategy-validation-needs-replay` | Strategies needing more replay |
| `strategy-validation-conflicted` | Conflicted strategies |
| `strategy-validation-report` | Generate Markdown report |
| `strategy-validation-explain` | Explain a strategy's validation score |

### Safety

- `validated_does_not_enable_trading=True` — VALIDATED grade is research-only, never enables trading
- `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`
- No BUY/SELL/ORDER output in any command or report
- Research Only. Not Investment Advice.

### Modified Files

| File | Change |
|------|--------|
| `main.py` | 10 CLI command handlers, 10 parsers, 10 command_map entries |
| `report_pack/report_registry.py` | REPORT_STRATEGY_VALIDATION constant; added to PACK_DAILY, PACK_WEEKLY, PACK_FULL |
| `report_pack/report_collector.py` | strategy_validation import and pattern map entries |
| `regression/suite_registry.py` | quick suite (2), research_os suite (4), release_gate suite (2) |
| `stable_release/stable_release_checklist_v060.py` | 2 new checks: strategy_validation_import, strategy_validation_no_forbidden |
| `intelligence_stable/intelligence_stable_checklist.py` | v0.9.2 strategy_validation_safe check in _check_stable_integration |
| `gui/navigation/tab_registry.py` | strategy_validation GUITabMetadata entry |
| `gui/dashboard.py` | _STRATEGY_VALIDATION_AVAILABLE guard + Strategy Validation tab |
| `docs/` | README, roadmap, release_notes_v0.9, index updated |
| `.gitignore` | strategy_validation runtime output patterns |

---

## v0.9.0 — Strategy Lab Stable

**Released:** 2026-06-09

### Overview

v0.9.0 introduces Strategy Lab Stable — a unified validation wrapper that covers all Research OS
modules built across v0.7.0 through v0.8.3 (Research Intelligence, Strategy Memory, Backtest Coach,
Training Metrics, Evidence Graph). The stable release defines 47 capabilities across 6 groups, runs
a 7-category stable checklist (A-G: Import Health, CLI Health, Report Health, Safety, Regression,
Runtime, Integration), generates a release manifest (JSON + Markdown), and produces a full 13-section
Markdown report. 6 CLI commands, GUI panel (Strategy Lab tab), CSV store, safety audit.
No BUY/SELL/ORDER. No trading actions. Production Trading: BLOCKED.
`read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`.
Does NOT modify any module status, weights, memory, coach tasks, metrics, or evidence graph.

### New Files

| File | Description |
|------|-------------|
| `strategy_lab/__init__.py` | Package docstring and safety flags (read_only, no_real_orders, production_blocked, real_order_ready=False) |
| `strategy_lab/strategy_lab_schema.py` | Dataclasses: StrategyLabCapability, StrategyLabCheck, StrategyLabSummary; `_guard()` function |
| `strategy_lab/strategy_lab_capability_matrix.py` | 47 hardcoded capabilities in 6 groups (RI/SM/BC/TM/EG/Supporting) |
| `strategy_lab/strategy_lab_checklist.py` | 7-category (A-G) stable checklist runner |
| `strategy_lab/strategy_lab_store.py` | CSV persistence for capabilities, checks, summary |
| `strategy_lab/strategy_lab_engine.py` | Master orchestration engine (read_only, no real orders) |
| `strategy_lab/strategy_lab_release_manifest.py` | Release manifest builder (JSON + Markdown) |
| `reports/strategy_lab_stable_report.py` | Markdown report generator (13 sections) |
| `gui/strategy_lab_adapter.py` | GUI ↔ backend bridge |
| `gui/strategy_lab_panel.py` | PySide6 Strategy Lab tab (8 summary cards, capability table, checklist table, safety audit, layer status, reports) |
| `docs/strategy_lab_stable_v0.9.0.md` | Full documentation |
| `docs/release_notes_v0.9.md` | This release notes file |

### Modified Files

| File | Change |
|------|--------|
| `release/version_info.py` | version → v0.9.0, release_name → Strategy Lab Stable, 15 new major features |
| `main.py` | Banner, 6 CLI command handlers, 6 parsers, 6 command_map entries |
| `report_pack/report_pack_schema.py` | REPORT_STRATEGY_LAB_STABLE constant, ALL_REPORT_TYPES, OPTIONAL_REPORT_TYPES |
| `report_pack/report_collector.py` | strategy_lab_stable import and pattern map entries |
| `regression/suite_registry.py` | 4 release gate test cases for strategy lab |
| `stable_release/capability_matrix.py` | strategy_lab_stable StableCapability entry |
| `release/stable_release_checklist.py` | 3 new check methods for strategy lab |
| `intelligence_stable/intelligence_capability_matrix.py` | strategy_lab_stable IntelligenceStableCapability entry |
| `intelligence_stable/intelligence_stable_checklist.py` | strategy_lab_safe safety check (WARN if not installed, not FAIL) |
| `reports/auto_report_center.py` | run_strategy_lab_summary() method |
| `reports/auto_report_index.py` | 5 strategy_lab manifest fields |
| `gui/dashboard.py` | StrategyLabPanel import and tab registration |
| `.gitignore` | strategy_lab runtime output exclusions |
| `README.md` | v0.9.0 section with 6 CLI commands |
| `docs/roadmap.md` | v0.9.0 complete, next steps (v0.9.1–v1.0.0) |
| `docs/index.md` | version updated to v0.9.0, release_notes_v0.9 and strategy_lab_stable_v0.9.0 links |

### CLI Commands (6 new)

```bash
python main.py strategy-lab --mode real
python main.py strategy-lab-summary
python main.py strategy-lab-capabilities
python main.py strategy-lab-checks
python main.py strategy-lab-manifest
python main.py strategy-lab-report --mode real
```

### Safety

- `read_only = True`
- `no_real_orders = True`
- `production_blocked = True`
- `real_order_ready = False`
- `_guard()` rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE in all text fields
- Does NOT modify any module status, weights, memory, coach tasks, metrics, or evidence graph
- Broker connection: DISABLED
- Real order execution: BLOCKED
- Auto-trading: NOT IMPLEMENTED

### Known Limitations

1. No investment advice — all outputs are research tasks only
2. No automatic strategy activation
3. No live order execution — production trading is BLOCKED
4. Provider token environment limits may affect some reports
5. Optional reports may be missing if not yet generated
6. Backtest quality depends on data coverage and import completeness
7. Evidence graph quality depends on available research outputs
8. Training metrics may show INSUFFICIENT_DATA until enough history accumulates

### Next Steps

| Version | Feature | Priority |
|---------|---------|---------|
| v0.9.1 | Evidence Graph UX — node detail drill, thread visualization | P2 |
| v0.9.2 | Strategy Validation Score — cross-module confidence scoring | P2 |
| v0.9.3 | Strategy Lab Dashboard Polish — unified layer status board | P2 |
| v1.0.0 | Research Trading Cockpit Stable — still No Real Orders unless explicitly enabled | P1 |

---

## v0.9.0.1 — Crash Reversal & Risk Discipline Strategy Pack (2026-06-09)

### Overview
v0.9.0.1 adds the Crash Reversal & Risk Discipline Strategy Pack to Strategy Lab.
This version is Research Only / No Real Orders / Not Investment Advice.

### New Strategy Modules
- **Crash Cause Classifier**: Classify market crash as Fundamental Breakdown / Financial Deleveraging / Technical Overheat Correction / Systemic Crisis
- **Post-Crash Stabilization Checklist**: 8-condition checklist with weighted scoring (0–100)
- **Relative Strength After Crash Score**: Score stocks by crash resilience (0–100)
- **Sakata EPS-backed Dip Buy Filter**: Filter dip-buy candidates by EPS/revenue/position/technical criteria
- **Moving Average Profit Discipline**: 5/10/20/60 MA rules for position management
- **High-Risk Industry Exposure Guard**: Limit exposure to biotech/clinical/disposition/pure-theme stocks

### New Files
- strategy_rules/crash_reversal_pack.py
- reports/crash_reversal_strategy_report.py
- gui/crash_reversal_panel.py
- gui/crash_reversal_adapter.py
- docs/crash_reversal_risk_discipline.md

### CLI Commands
- python main.py crash-reversal --mode real
- python main.py crash-reversal-summary
- python main.py crash-reversal-report --mode real
- python main.py crash-reversal-score --stock 2330 --mode real
- python main.py crash-reversal-watchlist --mode real

### Safety
- No Real Orders
- Production Trading BLOCKED
- No BUY/SELL/ORDER outputs
- Not Investment Advice
- No broker connection

### Base: v0.9.0 Strategy Lab Stable (4a89bc7) — preserved

---

## v0.9.1 — Evidence Graph UX

**Release date:** 2026-06-09
**Base:** v0.9.0.1 Crash Reversal & Risk Discipline Strategy Pack

### Overview

v0.9.1 adds a full UX layer on top of the v0.8.3 Evidence Graph engine, providing interactive tools for exploring evidence thread quality, graph gaps, crash reversal evidence chains, and node/thread explanations. All features are Research Only — No Real Orders.

### New Features

#### EvidenceThread Quality Scoring
- New quality labels: STRONG / PARTIAL / NEEDS_DATA / NEEDS_BACKTEST / CONFLICTED / ORPHANED
- `EvidenceThread.quality_label` and `suggested_next_step` fields
- Thread Quality Board: sortable view of all threads by quality

#### EvidenceGraphGap Detection
- Gap types: ORPHAN_NODE / MISSING_DATA / MISSING_BACKTEST / CONTRADICTION / STALE_THREAD
- `EvidenceGraphGap` schema with `severity`, `suggested_next_step`, `source_module`
- Gaps stored to `data/backtest_results/evidence_graph/evidence_graph_gaps*.csv`

#### EvidenceGraphQuery New Methods
- `search_threads(keyword, quality_label, source_module, symbol)` — filter evidence threads
- `search_gaps(gap_type, keyword, source_module)` — filter graph gaps
- `get_crash_reversal_threads()` — retrieve crash reversal evidence threads
- `explain_node(node_id)` — explain a specific evidence node
- `explain_thread(thread_id)` — explain a specific evidence thread

#### GUI 6 Sub-Tabs (Evidence Graph tab update)
1. Graph Overview — node/edge/thread/gap counts
2. Thread Quality Board — quality labels and next steps
3. Crash Reversal Chain — 6-stage evidence chain view
4. Gap View — gap type breakdown with severity
5. Node Explorer — search and explain individual nodes
6. Thread Explorer — drill into any thread

#### 7 New CLI Commands
- `evidence-graph-ux` — full pipeline with thread quality and gaps
- `evidence-graph-thread-quality` — thread quality board
- `evidence-graph-gaps` — graph gap view
- `evidence-graph-crash-reversal` — crash reversal evidence chain
- `evidence-graph-explain-node` — explain a specific node
- `evidence-graph-explain-thread` — explain a specific thread
- `evidence-graph-search` — search threads and gaps

### Registry / Checklist / Docs Updates
- `strategy_lab/strategy_lab_capability_matrix.py` — 3 new Evidence Graph UX capabilities
- `strategy_lab/strategy_lab_checklist.py` — 3 new import health checks
- `report_pack/report_collector.py` — 2 new report patterns
- `regression/suite_registry.py` — quick/full/release_gate suite entries
- `stable_release/stable_release_checklist_v060.py` — 2 new checks
- `intelligence_stable/intelligence_stable_checklist.py` — stable integration check
- `gui/navigation/tab_registry.py` — extended evidence_graph keywords
- `docs/research_intelligence_evidence_graph.md` — updated to v0.9.1

### Safety
- No Real Orders
- Production Trading BLOCKED
- No BUY/SELL/ORDER outputs
- Not Investment Advice
- `read_only=True`, `no_real_orders=True`, `production_blocked=True` on all new classes

---

> *TW Quant Cockpit v0.9.1 — Evidence Graph UX — Research Only — Not Investment Advice*
