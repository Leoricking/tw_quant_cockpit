# Release Notes — v0.5.x

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

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
