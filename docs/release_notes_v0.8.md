# TW Quant Cockpit — Release Notes v0.8.x

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] All versions in this file are research intelligence stable releases only.**

---

## v0.8.0 — Research Intelligence Stable

**Released:** 2026-06-05

### Overview

v0.8.0 introduces Research Intelligence Stable — a comprehensive stabilization layer that validates all Research Intelligence capabilities built across v0.7.0 through v0.7.3. The stable release defines 29 capabilities across 5 categories, runs a 7-category stable checklist, generates a release manifest (JSON + Markdown), and produces a full Markdown report. 6 CLI commands, GUI panel (Intelligence Stable tab), CSV store, safety audit. No BUY/SELL/ORDER. No trading actions. Production Trading: BLOCKED.

### New Files

| File | Description |
|------|-------------|
| `intelligence_stable/__init__.py` | Package docstring and safety flags (READ_ONLY, NO_REAL_ORDERS, PRODUCTION_BLOCKED) |
| `intelligence_stable/intelligence_stable_schema.py` | Dataclasses: IntelligenceStableCapability, IntelligenceStableCheck, IntelligenceStableSummary |
| `intelligence_stable/intelligence_capability_matrix.py` | 29 hardcoded capabilities in 5 categories |
| `intelligence_stable/intelligence_stable_checklist.py` | 7-category stable checklist runner |
| `intelligence_stable/intelligence_stable_store.py` | CSV persistence for capabilities, checks, summary |
| `intelligence_stable/intelligence_stable_engine.py` | Master orchestration engine |
| `intelligence_stable/intelligence_release_manifest.py` | Release manifest builder (JSON + Markdown) |
| `reports/intelligence_stable_report.py` | Markdown report generator (11 sections) |
| `gui/intelligence_stable_adapter.py` | GUI ↔ backend bridge |
| `gui/intelligence_stable_panel.py` | PySide6 Intelligence Stable tab |
| `docs/research_intelligence_stable_v0.8.0.md` | Full documentation |
| `docs/release_notes_v0.8.md` | This release notes file |

### Modified Files

| File | Change |
|------|--------|
| `release/version_info.py` | version → v0.8.0, release_name → Research Intelligence Stable, 15 new major features |
| `main.py` | Banner, 6 CLI command handlers, 6 parsers, 6 command_map entries |
| `report_pack/report_pack_schema.py` | REPORT_INTELLIGENCE_STABLE constant, ALL_REPORT_TYPES, OPTIONAL_REPORT_TYPES |
| `report_pack/report_registry.py` | intelligence_stable in PACK_DAILY, PACK_WEEKLY, PACK_FULL |
| `report_pack/report_collector.py` | intelligence_stable pattern map |
| `regression/suite_registry.py` | 2 release gate test cases for intelligence stable |
| `stable_release/stable_release_checklist_v060.py` | 2 new check methods for intelligence stable |
| `stable_release/capability_matrix.py` | research_intelligence_stable StableCapability entry |
| `release/stable_release_checklist.py` | 3 new check methods for intelligence stable |
| `reports/auto_report_center.py` | include_intelligence_stable flag, run_intelligence_stable_summary() |
| `reports/auto_report_index.py` | 5 intelligence_stable manifest fields |
| `experiments/snapshot_builder.py` | build_intelligence_stable_snapshot() method |
| `gui/dashboard.py` | IntelligenceStablePanel import and tab registration |
| `gui/navigation/tab_registry.py` | GUITabMetadata for intelligence_stable |
| `data_coverage/data_coverage_schema.py` | DOMAIN_INTELLIGENCE_STABLE constant |
| `data_coverage/data_coverage_registry.py` | 3 intelligence_stable coverage items |
| `os_planning/module_inventory.py` | research_intelligence_stable module entry |
| `os_planning/regression_audit.py` | research_intelligence_stable regression coverage entry |
| `docs/roadmap.md` | v0.7.3 + v0.8.0 marked Done, new next steps table |

### Capabilities (29 total)

#### Research Intelligence (8)
- ai_review_signal_generator, market_pattern_library, pattern_signal_bridge, intelligence_daily_summary, intelligence_weekly_plan, research_intelligence_cli, research_intelligence_gui, research_intelligence_report

#### Strategy Memory (7)
- strategy_memory_store, strategy_memory_status_tracker, strategy_memory_search, strategy_memory_lifecycle, strategy_memory_report, strategy_memory_cli, strategy_memory_gui

#### Backtest Coach (6)
- backtest_signal_extractor, coach_task_builder, coach_daily_plan, coach_weekly_plan, backtest_coach_report, backtest_coach_gui

#### Supporting (8)
- regression_suite, data_coverage_registry, report_pack_integration, snapshot_builder, auto_report_center, module_inventory, os_planning_integration, stable_release_checklist

### Stable Checklist Categories (7)
1. Import Health — schema, engine, store, checklist, manifest imports
2. CLI Health — all 6 intelligence-stable CLI commands importable
3. Report Health — report builder importable and functional
4. Safety — no forbidden keywords (BUY/SELL/ORDER/EXECUTE/etc.) in all capabilities
5. Regression — suite registry has intelligence stable test cases
6. Runtime — store loads or creates output directory gracefully
7. Stable Integration — version info reflects v0.8.0

### CLI Commands (6)

```
python main.py intelligence-stable              # Full pipeline: validate → store → report
python main.py intelligence-stable-summary      # Show latest stable summary
python main.py intelligence-stable-capabilities # List all 29 capabilities
python main.py intelligence-stable-checks       # Show latest checklist results
python main.py intelligence-stable-manifest     # Build or show release manifest
python main.py intelligence-stable-report       # Generate Markdown report
```

### Safety

- `_FORBIDDEN = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"]`
- All capabilities have `no_real_orders=True` and `production_blocked=True`
- Safety banner on every CLI command and GUI panel
- All outputs: `[!] No real orders. Research Only. Production Trading BLOCKED.`

### Known Limitations

- Release manifest requires git subprocess; may show fallback values in CI environments without git
- Stable checklist WARN status expected if upstream CSVs not yet generated
- Capability status is statically defined (STABLE/USABLE) based on code presence, not runtime metrics
- No LLM-assisted capability scoring (planned for v0.8.1)

---

> **[!] No real orders. Research Only. Production Trading: BLOCKED. Not Investment Advice.**
