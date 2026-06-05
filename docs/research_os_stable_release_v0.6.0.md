# TW Quant Cockpit — Research OS Stable Release v0.6.0

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

---

## Overview

v0.6.0 is a **stable release consolidation** — not a new trading feature release. It audits, catalogues,
and stabilizes all v0.5.x modules into a formal Research OS baseline.

**Goals:**
- Consolidate all v0.5.x module maturity into a documented capability matrix
- Run a 16-point stable release checklist across 7 categories
- Produce a release manifest (JSON + Markdown)
- Document 11 known limitations with workarounds
- Add Stable Release GUI panel and 6 CLI commands

**Safety:** Research Only / No Real Orders / Production Trading BLOCKED

---

## v0.5.x Completion Summary

| Version | Feature | Status |
|---------|---------|--------|
| v0.5.0 | Research OS Planning / Stabilization | Done |
| v0.5.1 | CLI Alias / Command UX Polish | Done |
| v0.5.1.1 | Strategy Filter Pack — Financial Turnaround | Done |
| v0.5.2 | GUI Tab Grouping / Navigation Polish | Done |
| v0.5.2.1 | Strategy Filter GUI Navigation Integration | Done |
| v0.5.3 | Regression Suite Consolidation | Done |
| v0.5.4 | Report Pack Consolidation | Done |
| v0.5.5 | Data / Feature Store Stabilization | Done |
| v0.5.6 | TW Replay Training Cockpit — AI Review & Tape Reading | Done |
| v0.5.6.2 | Stabilize Data and Feature Store Health | Done |

---

## Stable Capability Matrix Overview

The `StableCapabilityMatrix` catalogues 30+ capabilities across 9 categories:

| Category | Examples |
|----------|---------|
| data | Data Quality Gate, Data Stabilization, Feature Store Health, Leakage Guard |
| provider | Provider Health, Provider Reliability, API Fetch Diagnostics |
| strategy | Strategy Filter Pack, Rule Governance, Signal Quality, Rule Weight Tuning |
| replay | TW Replay Training Cockpit, AI Replay Review, Replay Score, Replay Drills |
| journal | Portfolio Journal |
| review / coach / workflow | Research Review, Research Coach, Research Workflow, Notification Center |
| report | Auto Report Center, Report Pack Consolidation |
| regression | Regression Suite Consolidation |
| research_os | Research OS Planning, CLI UX, GUI Navigation, Release Status |
| gui / cli | All GUI tabs, CLI commands |
| safety | Paper Trading, Mock Realtime, Backtest Engine Hardening, No Real Orders Safety Layer, Production Trading BLOCKED |

**Status levels:** STABLE / USABLE / PARTIAL / EXPERIMENTAL / BLOCKED

---

## Checklist

The `StableReleaseChecklistV060` runs 16 checks across 7 categories:

| Category | Checks |
|----------|--------|
| version_git | version_info, git_status, compileall |
| safety | safety_flags, no_broker_imports |
| cli | main_exists, stable_v060_commands, core_imports |
| gui | gui_panel_exists, dashboard_tab |
| reports | stable_report_exists, report_registry |
| regression | regression_v060_tests |
| runtime_safety | capability_matrix_builds, known_limitations_builds, release_schema_builds |

Run it:
```bash
python main.py stable-v060-check --mode real
```

---

## CLI Commands

```bash
# Run stable release checklist
python main.py stable-v060-check --mode real

# Generate 9-section stable release Markdown report
python main.py stable-v060-report --mode real

# Build release manifest (JSON + Markdown)
python main.py stable-v060-manifest

# Show capability matrix summary
python main.py stable-v060-capabilities

# List known limitations
python main.py stable-v060-limitations

# Full summary (capabilities + checklist overview)
python main.py stable-v060-summary
```

---

## GUI Usage

The **Stable Release** tab is in the `release_qa` group in the GUI Navigation.
Open the cockpit GUI:
```bash
python main.py cockpit
```
Navigate to: **Stable Release** tab.

Features:
- Summary cards (version, capabilities, checklist status, safety status)
- Capability Matrix Table
- Checklist Table
- Known Limitations Table
- Release Manifest Panel
- Action buttons (Run Checklist, Generate Report, Build Manifest, Open Report, Refresh)

---

## Safety

| Flag | Value |
|------|-------|
| research_only | True |
| no_real_orders | True |
| production_blocked | True |
| real_order_ready | False |
| broker_api | NOT CONNECTED |
| auto_weight_apply | DISABLED |

---

## Known Limitations

| ID | Name | Impact |
|----|------|--------|
| LIM-001 | No Real-Time Data Feed | HIGH |
| LIM-002 | Manual Threshold Tuning | MEDIUM |
| LIM-003 | No Live Broker Connection | HIGH |
| LIM-004 | Bar Data Requires Manual Import | MEDIUM |
| LIM-005 | Rule-Based AI Review Only | LOW |
| LIM-006 | Universe Size (~14-50 symbols) | MEDIUM |
| LIM-007 | Strategy Filter Criteria Manually Defined | MEDIUM |
| LIM-008 | Walk-Forward Windows Not Auto-Tuned | MEDIUM |
| LIM-009 | No Multi-Currency Support | LOW |
| LIM-010 | Leakage Detection Is Heuristic | MEDIUM |
| LIM-011 | PySide6 Required for GUI | LOW |

---

## PARTIAL Report Pack Interpretation (v0.6.1)

A `PARTIAL` report pack status means some reports are ready and some are not.
This does **NOT** automatically imply a stable release failure.

**Pass criteria:**
- `failed_count == 0` — no report generation errors
- `required_missing_count == 0` — no `STATUS_MISSING` on required report types

**Non-failure statuses:**
- `ENV_LIMITED` — provider report requires API token (environment variable not set)
- `NOT_GENERATED` — optional report not yet generated (experiment, replay_training, etc.)
- `MISSING_OPTIONAL` — optional report missing

**Required report types** (absence = failure): `daily_market`, `auto_report`, `data_quality`, `signal_quality`

**Optional report types** (absence = NOT_GENERATED, not failure): `experiment`, `intraday_replay`,
`rule_governance`, `replay_training`, `stable_release_v060_report`, `release_manifest`

**Provider-limited** (absence = ENV_LIMITED, not failure): `provider`

---

## Release Process

1. `python main.py stable-v060-check --mode real` — verify all checks pass
2. `python main.py stable-v060-manifest` — generate release_manifest_v0.6.0.json
3. `python main.py stable-v060-report --mode real` — generate Markdown report
4. `git tag v0.6.0` — tag the release
5. `git push origin v0.6.0` — push tag

---

## No Real Orders Disclaimer

> **This system is a research and simulation platform only.**
> No real broker API connections. No automatic order placement.
> No auto-apply of strategy weights. All backtests are historical simulations.
> Not investment advice. production_blocked=True. real_order_ready=False.

---

*TW Quant Cockpit v0.6.0 — Research Only / No Real Orders / Production Trading BLOCKED*
