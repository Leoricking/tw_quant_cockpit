# GUI Tab Grouping / Navigation Polish — v0.5.2

> **[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

---

## Overview

v0.5.2 adds tab grouping, navigation metadata, search, favorites/recent, and a GUI Navigation panel to TW Quant Cockpit. No tabs are deleted or renamed. All 24+ existing tabs are preserved.

---

## Goals

1. **Tab Registry** — catalog all GUI tabs with group, priority, keywords, CLI mapping, maturity
2. **8 Tab Groups** — logical grouping for easier navigation
3. **Tab Search** — full-text search across name, description, keywords, CLI commands
4. **Favorites & Recent** — runtime navigation state (not committed to git)
5. **GUI Navigation Panel** — new "GUI Navigation" tab in cockpit dashboard
6. **5 CLI commands** — `gui-nav-summary`, `gui-nav-tabs`, `gui-nav-groups`, `gui-nav-search`, `gui-nav-report`
7. **Backward compatibility** — no tab deletion, no dashboard changes that remove existing tabs

---

## Tab Groups (A–H)

### A. Daily Research (`daily_research`)
Daily research workflow, reports, coaching, review.

| Tab | Priority |
|-----|----------|
| Daily Workflow | P0 |
| Auto Report Center | P0 |
| Research Workflow | P1 |
| Research Coach | P1 |
| Research Review | P1 |
| Notification Center | P2 |

### B. Data & Providers (`data_providers`)
API fetch, provider health, data quality, universe.

| Tab | Priority |
|-----|----------|
| Data Quality Gate | P0 |
| API Fetch Status | P1 |
| Provider Health | P1 |
| Provider Reliability | P1 |
| Data Provider Fetch | P2 |
| Universe Manager | P2 |

### C. Strategy & Rules (`strategy_rules`)
Strategy filter, rule governance, signal quality, strategy knowledge, ML knowledge integration.

| Tab | Priority |
|-----|----------|
| Strategy Filter | P1 |
| Rule Governance | P0 |
| Signal Quality | P0 |
| Rule Weight Tuning | P1 |
| Strategy Knowledge | P1 |
| ML Knowledge Integration | P1 |

### D. Backtest & Simulation (`backtest_simulation`)
Hardened backtest, portfolio cockpit, intraday replay.

| Tab | Priority |
|-----|----------|
| Hardened Backtest | P0 |
| Intraday Replay | P0 |
| Portfolio Cockpit | P1 |
| Intraday Pipeline | P1 |

### E. ML & Monitoring (`ml_monitoring`)
ML feature store, model monitoring.

| Tab | Priority |
|-----|----------|
| ML Feature Store | P1 |
| Model Monitoring | P1 |

### F. Journal & Review (`journal_review`)
Portfolio journal, experiment registry.

| Tab | Priority |
|-----|----------|
| Portfolio Journal | P1 |
| Experiment Registry | P1 |

### G. Research OS (`research_os`)
OS planning, CLI UX, GUI navigation.

| Tab | Priority |
|-----|----------|
| Research OS Planning | P1 |
| CLI UX | P2 |
| GUI Navigation | P2 |

### H. Release & QA (`release_qa`)
Release status, usability QA.

| Tab | Priority |
|-----|----------|
| Release Status | P1 |
| Usability QA | P2 |

---

## Sidebar Navigation

`NavigationSidebar` (PySide6 widget) shows the 8 groups as a clickable list.
Clicking a group emits `group_selected(group_id)` signal.

`NavigationBreadcrumb` shows the current group > tab path.

---

## Tab Search

`GUITabSearch.search(query)` performs case-insensitive full-text search across:
- `tab_id`, `display_name`, `description`
- `keywords` list
- `related_cli_commands` list
- `group` name

`GUITabSearch.suggest_tabs(intent_text)` extracts words from free-text and searches each.

---

## Favorites & Recent

`NavigationState` persists to `config/gui_navigation_state.json` (gitignored).

- `set_favorite(tab_id, enabled)` — add/remove from favorites
- `record_recent(tab_id)` — prepend to recent list (max 20)
- `get_favorites()` — return favorite tab_id list
- `get_recent_tabs(limit)` — return recent tab_ids

State is never committed. `config/gui_navigation_state.example.json` is committed as reference.

---

## Backward Compatibility

- No existing tab is deleted, renamed, or reordered in `gui/dashboard.py`
- `GUITabInventoryBuilder.build_inventory()` is unchanged
- New `build_inventory_with_navigation()` merges hardcoded inventory with `GUITabRegistry` metadata
- All 24+ tabs in `GUITabRegistry` match tabs already in the dashboard

---

## No Real Orders

This entire module is GUI UX Only. No broker connection. No real orders. No auto trading.

| Safety Flag | Value |
|-------------|-------|
| read_only | True |
| no_real_orders | True |
| production_blocked | True |
| real_order_ready | False |

---

## CLI Commands (v0.5.2)

```bash
python main.py gui-nav-summary      # Print GUI navigation summary
python main.py gui-nav-tabs         # List all registered tabs
python main.py gui-nav-groups       # List all tab groups
python main.py gui-nav-search --keyword daily  # Search tabs by keyword
python main.py gui-nav-report       # Generate GUI navigation report
```

---

---

## v0.5.2.1 — Strategy Filter GUI Navigation Integration

Added in v0.5.2.1 to integrate the v0.5.1.1 Strategy Filter Pack into GUI Navigation.

### Changes
- **Strategy Filter** tab registered in GUI Navigation registry under `strategy_rules` group (priority P1)
- **Search keywords** added: `strategy`, `filter`, `financial`, `turnaround`, `EPS`, `Q1 EPS`, `revenue`,
  `財報`, `財報翻多`, `EPS 成長`, `月營收`, `毛利率`, `營益率`, `低位階`, `底部翻多`, `趨勢紀律`,
  `第二波買點`, `回測不破`, `不追高`, `汰弱換強`, `月線`, `季線`
- **Aliases**: `financial-turnaround`, `trend-discipline`, `strategy-filter`, `財報翻多`, `第二波買點`
- **CLI commands** linked: `strategy-filter`, `strategy-filter-pack`, `rule-governance`, `signal-quality`,
  `strategy-knowledge-summary`
- **Safety**: `RESEARCH_ONLY`, `no_real_orders=True`, `production_blocked=True`

### Search Examples (v0.5.2.1+)
```bash
python main.py gui-nav-search --keyword strategy     # finds Strategy Filter
python main.py gui-nav-search --keyword EPS          # finds Strategy Filter
python main.py gui-nav-search --keyword 財報         # finds Strategy Filter
python main.py gui-nav-search --keyword 底部翻多      # finds Strategy Filter
python main.py gui-nav-search --keyword 第二波買點    # finds Strategy Filter
```

### No Real Orders
- Strategy Filter is research-only. No BUY/SELL orders. No broker connection. No auto trading.
- All GUI Navigation metadata is read-only. No real orders. Production trading: BLOCKED.

---

*TW Quant Cockpit v0.5.2.1 — Strategy Filter GUI Navigation Integration — Research Only — Not Investment Advice*
