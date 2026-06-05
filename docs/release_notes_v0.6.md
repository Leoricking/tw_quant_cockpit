# TW Quant Cockpit — Release Notes v0.6

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**

---

## v0.6.2 — Data Coverage Expansion (2026-06-05)

### Summary

v0.6.2 adds a comprehensive data coverage tracking and auditing system. It tracks coverage across
12 domains and 35+ data items, classifies gaps as READY / ENV_LIMITED / NOT_GENERATED / MISSING,
and provides CLI commands, a GUI panel, store CSVs, and a Markdown report.

### New Files

- `data_coverage/` package: schema, registry (35 items), scanner, engine, store
- `reports/data_coverage_report.py` — Markdown report generator
- `gui/data_coverage_panel.py` — PySide6 GUI panel with coverage matrix table
- `gui/data_coverage_adapter.py` — GUI-to-backend adapter
- `docs/data_coverage_expansion.md` — documentation

### New CLI Commands

```bash
python main.py data-coverage --mode real
python main.py data-coverage-summary
python main.py data-coverage-items
python main.py data-coverage-report --mode real
python main.py data-coverage-gaps
```

### Modified Files

- `main.py` — 5 new commands
- `report_pack/report_pack_schema.py` — REPORT_DATA_COVERAGE constant + OPTIONAL set
- `report_pack/report_registry.py` — data_coverage in PACK_FULL
- `report_pack/report_collector.py` — data_coverage pattern map
- `regression/suite_registry.py` — data suite + report suite + release_gate
- `stable_release/stable_release_checklist_v060.py` — v0.6.2 import check
- `stable_release/capability_matrix.py` — Data Coverage Expansion capability
- `reports/auto_report_center.py` — optional data_coverage in full profile
- `gui/dashboard.py` — Data Coverage tab
- `gui/navigation/tab_registry.py` — data_coverage tab entry
- `.gitignore` — exclude runtime outputs

### Safety

All outputs: Data Coverage Only / Research Only / No Real Orders / Production BLOCKED.

---

## v0.6.1 — Stable UX Polish (2026-06-05)

### Summary

v0.6.1 is a targeted UX polish release — no new trading features, no trading functionality changes.
All outputs remain research-only.

### Changes

- `main.py` — `report-pack` and `report-pack-items`: added `--type` as alias for `--pack-type`;
  added `--mode` parameter (accepted, no-op, prints informational message)
- `report_pack/report_pack_schema.py` — added `STATUS_ENV_LIMITED`, `STATUS_NOT_GENERATED`,
  `STATUS_MISSING_OPT`, `STATUS_MISSING_REQ`; added `OPTIONAL_REPORT_TYPES` and
  `ENV_LIMITED_REPORT_TYPES` sets
- `report_pack/report_collector.py` — smarter missing classification: ENV_LIMITED for provider,
  NOT_GENERATED for optional types, MISSING only for required
- `report_pack/report_health_checker.py` — ENV_LIMITED and NOT_GENERATED do not count as critical
  failures; HEALTHY if failed=0 and required_missing=0; improved recommendation wording
- `report_pack/report_pack_builder.py` — added "Optional missing reports are not release failures"
  and "Environment-limited reports require provider tokens" to index output
- `gui/report_pack_panel.py` — ENV_LIMITED shown as "環境限制 (需設定 token)"; NOT_GENERATED shown
  as "尚未產生 (optional)"; empty state hint added
- `gui/stable_release_panel.py` — added explanatory note about optional missing and provider tokens
- `stable_release/stable_release_checklist_v060.py` — added `_check_report_pack_partial` check;
  PARTIAL pack with 0 failed / no required missing is PASS, not failure; ENV_LIMITED is warning not fail
- `reports/stable_release_v060_report.py` — added Report Coverage Notes section to Known Limitations
- `regression/suite_registry.py` — added `report-pack --type full --mode real` and
  `report-pack-items --type full` test cases
- `docs/` — updated release notes, roadmap, report_pack_consolidation, research_os_stable_release_v0.6.0,
  README, added `docs/stable_ux_polish_v0.6.1.md`

### New CLI Behavior

```bash
# --type is now an alias for --pack-type
python main.py report-pack --type full --mode real
python main.py report-pack --pack-type full
python main.py report-pack-items --type full
```

### Safety

- `research_only = True`
- `no_real_orders = True`
- `production_blocked = True`
- `real_order_ready = False`

---

## v0.6.0 — Research OS Stable Release (2026-06-04)

### Summary

v0.6.0 is a **stable consolidation release** — all v0.5.x modules are catalogued, checked, and documented.
No new trading features. All outputs remain research-only.

### New Files

| File | Description |
|------|-------------|
| `stable_release/__init__.py` | Package init |
| `stable_release/stable_release_schema.py` | `StableReleaseInfo`, `StableCapability` dataclasses |
| `stable_release/capability_matrix.py` | `StableCapabilityMatrix` — 30+ capabilities |
| `stable_release/stable_release_checklist_v060.py` | 16-point checklist, 7 categories |
| `stable_release/release_manifest_builder.py` | JSON + Markdown manifest builder |
| `stable_release/known_limitations.py` | 11 known limitations with workarounds |
| `reports/stable_release_v060_report.py` | 9-section Markdown report |
| `gui/stable_release_panel.py` | PySide6 GUI panel with QThread workers |
| `gui/stable_release_adapter.py` | GUI adapter bridge |
| `docs/research_os_stable_release_v0.6.0.md` | This release's documentation |
| `docs/release_notes_v0.6.md` | This file |

### Modified Files

| File | Change |
|------|--------|
| `release/version_info.py` | Updated to v0.6.0, release_name, release_stage=STABLE |
| `main.py` | Added 6 stable-v060-* CLI commands |
| `regression/suite_registry.py` | Added 3 v0.6.0 release gate tests |
| `report_pack/report_pack_schema.py` | Added REPORT_STABLE_RELEASE_V060, REPORT_RELEASE_MANIFEST |
| `report_pack/report_registry.py` | Added stable release reports to full pack |
| `reports/auto_report_center.py` | Added run_stable_release_v060_summary() |
| `reports/auto_report_index.py` | Added stable_release_* manifest fields |
| `experiments/snapshot_builder.py` | Added build_stable_release_snapshot() |
| `gui/dashboard.py` | Added StableReleasePanel tab import and setup |
| `gui/navigation/tab_registry.py` | Added stable_release tab entry |
| `os_planning/module_inventory.py` | Added stable_release_v060 module entry |
| `os_planning/regression_audit.py` | Added stable_release_v060 coverage entry |
| `README.md` | Added v0.6.0 section |
| `docs/roadmap.md` | Marked v0.6.0 as Done, added next steps |
| `docs/index.md` | Added v0.6.0 doc links |

### New CLI Commands

```bash
python main.py stable-v060-check --mode real       # Run 16-point checklist
python main.py stable-v060-report --mode real      # Generate Markdown report
python main.py stable-v060-manifest                # Build release manifest
python main.py stable-v060-capabilities            # Show capability matrix
python main.py stable-v060-limitations             # List known limitations
python main.py stable-v060-summary                 # Full summary
```

### Capability Matrix Highlights

- 30+ capabilities catalogued
- ~25 STABLE capabilities
- 4 USABLE/EXPERIMENTAL capabilities
- 1 BLOCKED (Production Trading — intentionally blocked)
- 11 known limitations documented

### Safety

- `research_only = True`
- `no_real_orders = True`
- `production_blocked = True`
- `real_order_ready = False`

---

## Completed v0.5.x Modules

| Version | Feature |
|---------|---------|
| v0.5.0 | Research OS Planning |
| v0.5.1 | CLI Alias / Command UX Polish |
| v0.5.1.1 | Strategy Filter Pack |
| v0.5.2 | GUI Tab Grouping / Navigation Polish |
| v0.5.2.1 | Strategy Filter GUI Integration |
| v0.5.3 | Regression Suite Consolidation |
| v0.5.4 | Report Pack Consolidation |
| v0.5.5 | Data / Feature Store Stabilization |
| v0.5.6 | TW Replay Training Cockpit |
| v0.5.6.2 | Data and Feature Store Health Stabilization |

---

## Next Releases

| Version | Feature | Priority |
|---------|---------|---------|
| v0.6.1 | Stable UX Polish | P1 |
| v0.6.2 | Data Coverage Expansion | P1 |
| v0.6.3 | Replay Training UI Enhancement | P1 |
| v0.7.0 | Research Intelligence Upgrade | P2 |

---

*Research Only / No Real Orders / Production Trading BLOCKED*
