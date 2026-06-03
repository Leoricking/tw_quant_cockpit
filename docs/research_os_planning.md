# Research OS Planning & Stabilization — v0.5.0

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

**Version:** v0.5.0  
**Released:** 2026-06-03  

---

## Overview

v0.5.0 is a stabilization release. No new trading strategies or real-order functionality.
The goal is to inventory, audit, and plan the entire Research OS for the v0.5.x cycle.

---

## os_planning Package

| Module | Purpose |
|--------|---------|
| `module_inventory.py` | Inventory of all 27 modules across 6 layers |
| `cli_inventory.py` | Inventory of 106 CLI commands across 13 categories |
| `gui_tab_inventory.py` | Inventory of 31 GUI tabs across 7 groups |
| `regression_audit.py` | Coverage audit across all modules |
| `artifact_hygiene_audit.py` | .gitignore and artifact hygiene checks |
| `safety_matrix.py` | Safety invariant verification for all modules |

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py research-os-audit` | Run full OS audit (module, CLI, GUI, regression, artifact, safety) |
| `python main.py research-os-report` | Generate Research OS Stabilization Report |
| `python main.py research-os-summary` | Print OS inventory summary |
| `python main.py research-os-modules` | List all modules with maturity status |
| `python main.py research-os-cli` | List all CLI commands with categories |
| `python main.py research-os-gui` | List all GUI tabs with groups |
| `python main.py research-os-safety` | Show safety matrix for all modules |

### Examples

```bash
python main.py research-os-audit --mode real
python main.py research-os-report --mode real
python main.py research-os-summary
python main.py research-os-modules
python main.py research-os-cli
python main.py research-os-gui
python main.py research-os-safety
```

---

## GUI Panel

The **Research OS Planning** tab is added to the Cockpit dashboard. It shows:

- Summary cards: Modules, CLI Commands, GUI Tabs, Regression Coverage, Safety Score
- **Modules** tab: Full module inventory table
- **CLI Commands** tab: All 106 commands with categories
- **GUI Tabs** tab: All 31 tabs with groups
- **Regression Audit** tab: Per-module coverage status
- **Safety Matrix** tab: Per-module safety invariant status
- **Audit Log** tab: Live audit output

---

## Report

`reports/research_os_stabilization_report_YYYY-MM-DD.md` — 7 sections:

1. Module Inventory
2. CLI Command Inventory
3. GUI Tab Inventory
4. Regression Coverage Audit
5. Artifact Hygiene Audit
6. Safety Matrix
7. Recommendations

---

## v0.5.x Roadmap

| Version | Focus |
|---------|-------|
| v0.5.1 | CLI Alias Polish |
| v0.5.2 | GUI Tab Grouping |
| v0.5.3 | Regression Consolidation |
| v0.5.4 | Report Pack |
| v0.5.5 | Data / Feature Pipeline Hardening |
| v0.5.6 | Replay / Journal / Coach Integration |
| v0.6.0 | Stable Release |

---

## Safety Summary

| Invariant | Value |
|-----------|-------|
| Read Only | **True** |
| No Real Orders | **True** |
| Production Trading | **BLOCKED** |
| REAL_ORDER_READY | **False (never)** |

*v0.5.0 Research OS Planning / Stabilization.*
