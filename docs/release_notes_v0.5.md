# Release Notes — v0.5.x

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## v0.5.2.1 — Strategy Filter GUI Navigation Integration (2026-06-04)

### Summary
Small integration patch. Adds Strategy Filter tab to GUI Navigation registry under `strategy_rules` group with full keyword/alias metadata. GUI nav search now finds Strategy Filter via strategy, EPS, 財報, 底部翻多, 趨勢紀律, 第二波買點 etc. No v0.5.2 redo. No tab deletion. No real orders.

### Changes

| File | Change |
|------|--------|
| `gui/navigation/tab_registry.py` | Added `strategy_filter` GUITabMetadata with 20+ keywords and aliases |
| `gui/navigation/tab_groups.py` | Updated `strategy_rules` description to include Strategy Filter |
| `release/stable_release_checklist.py` | Added `_check_strategy_filter_in_gui_navigation` and `_check_strategy_filter_searchable` checks |
| `release/regression_suite.py` | Added `_test_strategy_filter_gui_nav_searchable` to full suite |
| `docs/gui_tab_grouping_navigation.md` | Added v0.5.2.1 section: Strategy Filter in Strategy & Rules group |
| `docs/release_notes_v0.5.md` | This entry |
| `docs/roadmap.md` | Marked v0.5.2.1 as Done |
| `README.md` | Added v0.5.2.1 section |

### Search Keywords Added
`strategy`, `filter`, `financial`, `turnaround`, `EPS`, `Q1 EPS`, `revenue`,
`財報`, `財報翻多`, `EPS 成長`, `Q1 EPS × 4`, `月營收`, `毛利率`, `營益率`,
`低位階`, `底部翻多`, `趨勢紀律`, `第二波買點`, `回測不破`, `不追高`, `汰弱換強`, `月線`, `季線`

### Aliases Added
`financial-turnaround`, `trend-discipline`, `strategy-filter`, `財報翻多`, `第二波買點`

### Safety
- [!] Research Only. No Real Orders. No broker connection. Production Trading: BLOCKED.
- `no_real_orders=True`, `production_blocked=True`, `safety_level=RESEARCH_ONLY`
- Strategy Filter tab `maturity=EXPERIMENTAL` — no BUY/SELL/ORDER output.

---

## v0.5.1.1 — Strategy Filter Pack: Financial Turnaround & Trend Discipline (2026-06-04)

### Summary
Small-version insert between v0.5.1 and v0.5.2. Adds a strategy filter framework derived from 6 investment transcript knowledge sources. No v0.5.1 tag overwritten. No v0.5.2 roadmap changes. Research only — no real orders, no automatic weight changes, no ML activation.

### New Package: `strategy_filters/`

| Module | Purpose |
|--------|---------|
| `__init__.py` | Package init, exports FinancialTurnaroundFilter, StrategyFilterPack |
| `financial_turnaround_filter.py` | Main filter: 6-dimension scoring, 3 scenario archetypes, deduction logic |
| `strategy_filter_pack.py` | Unified manager: run_all(), run_financial_turnaround(), batch run, summary |

### New Report
- `reports/strategy_filter_report.py` — 6-section Markdown report (single-stock and pack)

### New Docs
- `docs/strategy_filter_pack.md`

### Updated Files

| File | Change |
|------|--------|
| `main.py` | Added `strategy-filter` and `strategy-filter-pack` CLI commands |
| `analysis/signal_quality_engine.py` | Added `load_strategy_filter_quality()` as read-only signal metadata |
| `governance/rule_registry.py` | Added 7 NEEDS_REVIEW candidate rules |
| `knowledge/knowledge_extractor.py` | Added Financial Turnaround keywords to 4 keyword lists |
| `reports/auto_report_center.py` | Added `run_strategy_filter_summary()` to full and daily profiles |
| `gui/dashboard.py` | Added Strategy Filter tab (inline) |
| `README.md` | Added v0.5.1.1 section |
| `.gitignore` | Added `reports/strategy_filter_report_*.md` and `data/backtest_results/strategy_filter/` |

### New CLI Commands

| Command | Description |
|---------|-------------|
| `strategy-filter --stock 2454 --mode real` | Single-stock filter with score + scenario |
| `strategy-filter --stock 2454 --mode real --report` | Same + save Markdown report |
| `strategy-filter-pack --mode real` | Full pack across universe stocks |

### Scoring (Financial Turnaround Trend Score, 0–100)

| Dimension | Max |
|-----------|-----|
| 財報 / EPS 成長 | 25 |
| 月營收 / 毛利率 / 營益率 | 15 |
| 低位階 / 底部翻多 | 15 |
| 技術轉強 / 站回均線 | 15 |
| 法人 / 籌碼支持 | 15 |
| 風控健康度 / 融資未失控 | 10 |
| 避雷扣分 (max -30) | -30 |

### New Rule Candidates (NEEDS_REVIEW)
- `STRATEGY.FINANCIAL_TURNAROUND.V1`
- `STRATEGY.LOW_BASE_BREAKOUT.V1`
- `RISK.GOOD_FUNDAMENTAL_BUT_EXTENDED.V1`
- `RISK.RELATIVE_WEAKNESS_MARKET_HIGH.V1`
- `RISK.TOP_PATTERN_WITH_WEAK_FUNDAMENTAL.V1`
- `RISK.MA20_BREAK_THREE_DAYS.V1`
- `RISK.MA60_BREAK_TREND_WEAK.V1`

### Safety
- [!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.
- `suggested_action` restricted to: WATCH, WAIT_PULLBACK, SECOND_WAVE_CANDIDATE, REDUCE_RISK, AVOID, ROTATE_TO_STRONGER. No BUY / SELL / ORDER.
- `read_only=True, no_real_orders=True, production_blocked=True` on all new classes.
- `reports/strategy_filter_report_*.md` and `data/backtest_results/strategy_filter/` are gitignored.

---

## v0.5.2 — GUI Tab Grouping / Navigation Polish (2026-06-04)

### Summary
GUI UX polish release. Adds tab registry (24 tabs), 8 tab groups, tab search, favorites/recent navigation state, GUI Navigation panel, and 5 CLI commands. No tab deletion. All existing tabs preserved. No real-order functionality.

### New Package: `gui/navigation/`

| Module | Purpose |
|--------|---------|
| `tab_registry.py` | GUITabMetadata + GUITabRegistry (24 tabs, 8 groups) |
| `tab_groups.py` | GUITabGroupConfig (8 ordered groups) |
| `navigation_state.py` | Favorites + recently used tabs, persisted to config/ |
| `tab_search.py` | Full-text search across name, description, keywords, CLI |
| `navigation_widgets.py` | PySide6 sidebar, search box, fav/recent, breadcrumb |
| `navigation_report_data.py` | Summary, group table, tab table, keyword data |

### New Files
- `gui/gui_navigation_panel.py` — GUI Navigation panel (Group Table, Tab Registry, Search, Fav & Recent, Audit Log)
- `gui/gui_navigation_adapter.py` — bridge for CLI and GUI
- `reports/gui_navigation_report.py` — 7-section Markdown report
- `docs/gui_tab_grouping_navigation.md`
- `config/gui_navigation_state.example.json`

### New CLI Commands
```bash
python main.py gui-nav-summary
python main.py gui-nav-tabs
python main.py gui-nav-groups
python main.py gui-nav-search --keyword <kw>
python main.py gui-nav-report
```

### Safety
- [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
- `read_only=True, no_real_orders=True, production_blocked=True, real_order_ready=False` on all new classes.
- `config/gui_navigation_state.json` is gitignored.

---

## v0.5.1 — CLI Alias / Command UX Polish (2026-06-03)

### Summary
CLI UX polish release. Adds command registry, 35 safe aliases, command discovery, help examples, CLI UX report and GUI panel. No new strategies. All existing commands preserved. No real-order functionality.

### New Package: `cli/`

| Module | Purpose |
|--------|---------|
| `command_registry.py` | 126 commands across 17 categories |
| `alias_map.py` | 35 safe aliases, 0 conflicts, blocked-keyword guard |
| `command_discovery.py` | Keyword search and intent suggestion |
| `help_examples.py` | Quick start, daily, weekly, safety example groups |
| `cli_ux_report.py` | CLI UX audit data builder |

### New Report
- `reports/cli_ux_report.py` — 8-section Markdown report

### New GUI
- `gui/cli_ux_panel.py` — CLI UX panel (5 sub-tabs)
- `gui/cli_ux_adapter.py` — bridge

### New Docs
- `docs/cli_alias_command_ux.md`

### New CLI (6 commands + 17 aliases)

**Commands:**

| Command | Description |
|---------|-------------|
| `cli-list` | List all commands in registry |
| `cli-search --keyword X` | Search commands by keyword |
| `cli-aliases` | Show all aliases |
| `cli-examples` | Show help examples |
| `cli-ux-report` | Generate CLI UX report |
| `cli-resolve --alias X` | Resolve alias (display only) |

**Aliases:**

| Alias | Target |
|-------|--------|
| `daily` | `run-research --profile daily` |
| `quick` | `run-research --profile quick` |
| `dq` | `data-quality-gate` |
| `quality` | `data-quality-gate` |
| `providers` | `provider-reliability` |
| `rules` | `rule-governance` |
| `signals` | `signal-quality` |
| `journal` | `journal-summary` |
| `notify` | `notification-list` |
| `coach-daily` | `research-coach --period daily` |
| `review-daily` | `research-review --period daily` |
| `workflow-daily` | `research-workflow --type daily_research` |
| `workflow-weekly` | `research-workflow --type weekly_review` |
| `os` | `research-os-summary` |
| `version` | `version-info` |
| `gui` | `cockpit` |
| `dashboard` | `cockpit` |

### Safety
- 0 trading aliases (buy/sell/order/broker/shioaji all blocked)
- All existing commands preserved, none removed or renamed
- All safety invariants maintained

---

## v0.5.0 — Research OS Planning / Stabilization (2026-06-03)

### Summary
Stabilization release. Full inventory and audit of the Research OS — no new strategies, no real-order functionality.

### New Package: `os_planning/`

| Module | Purpose |
|--------|---------|
| `module_inventory.py` | 27 modules across 6 layers, maturity tagging, feature matrix |
| `cli_inventory.py` | 106 CLI commands across 13 categories, naming-inconsistency detector |
| `gui_tab_inventory.py` | 31 GUI tabs across 7 groups, grouping suggestions |
| `regression_audit.py` | 5-dimension coverage audit (command, import, GUI, report, safety) |
| `artifact_hygiene_audit.py` | .gitignore hygiene checks for 15+ patterns |
| `safety_matrix.py` | Safety invariant verification for 16 modules |

### New Report
- `reports/research_os_stabilization_report.py` — 7-section Markdown report

### New GUI
- `gui/research_os_planning_panel.py` — Research OS Planning panel (6 sub-tabs)
- `gui/research_os_planning_adapter.py` — Bridge to os_planning subsystem

### New Docs
- `docs/research_os_planning.md`
- `docs/release_notes_v0.5.md` (this file)

### New CLI Commands (7)

| Command | Description |
|---------|-------------|
| `research-os-audit` | Full OS audit |
| `research-os-report` | Generate stabilization report |
| `research-os-summary` | Print OS summary |
| `research-os-modules` | List all modules |
| `research-os-cli` | List all CLI commands |
| `research-os-gui` | List all GUI tabs |
| `research-os-safety` | Show safety matrix |

### Integrations
- `auto_report_center.py` — `run_research_os_summary()` added
- `auto_report_index.py` — 5 OS manifest fields added
- `snapshot_builder.py` — `build_research_os_planning_snapshot()` added
- `dashboard.py` — Research OS Planning tab added
- `regression_suite.py` — 2 new OS tests
- `stable_release_checklist.py` — 4 new OS checks
- `version_info.py` — Updated to v0.5.0

### v0.5.x Roadmap

| Version | Focus |
|---------|-------|
| v0.5.1 | CLI Alias Polish |
| v0.5.2 | GUI Tab Grouping |
| v0.5.3 | Regression Consolidation |
| v0.5.4 | Report Pack |
| v0.5.5 | Data / Feature Pipeline Hardening |
| v0.5.6 | Replay / Journal / Coach Integration |
| v0.6.0 | Stable Release |

### Safety
All safety invariants maintained: `read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`.

---

*For v0.4.x history, see [release_notes_v0.4.md](release_notes_v0.4.md).*
