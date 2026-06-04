# TW Quant Cockpit — Release Notes v0.6

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**

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
