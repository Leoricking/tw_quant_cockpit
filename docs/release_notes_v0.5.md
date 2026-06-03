# Release Notes — v0.5.x

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

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
