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

## v0.8.1 — Strategy Memory UX

**Released:** 2026-06-05

### Overview

v0.8.1 is a UX polish release for the Strategy Research Memory system. It adds a full status lifecycle flow, actionable UX fields, safe command labelling, new CLI views (validation-queue, active-threads, repeated-patterns), and enhanced GUI detail panel with 7 tabs. Backward compatible. No existing functionality removed. Research Only. No Real Orders. ACCEPTED ≠ trading enabled.

### Modified Files

| File | Change |
|------|--------|
| `strategy_memory/strategy_memory_schema.py` | 9 new optional fields on StrategyMemoryItem; 3 new fields on StrategyMemoryLink; accepted_is_research_only invariant enforced |
| `strategy_memory/memory_query.py` | search_advanced(), sort_memories(), get_validation_queue(), get_active_research_threads(), get_repeated_patterns(); optional store= constructor |
| `strategy_memory/memory_store.py` | Protected statuses in upsert; last_action_at tracking; accepted_is_research_only=True on ACCEPTED |
| `strategy_memory/strategy_memory_engine.py` | today_focus, active_threads_count, validation_queue_count, needs_action_count in run() result |
| `strategy_memory/memory_linker.py` | Conservative duplicate detection; target_title, why_linked, suggested_next_step on links |
| `strategy_memory/memory_extractor.py` | needs_action=True for P0/P1 signals; reduced NOT_GENERATED noise |
| `reports/strategy_memory_report.py` | 10-section format with today_focus, validation queue, repeated patterns, why_linked |
| `gui/strategy_memory_panel.py` | 7-tab detail panel; status action buttons; source module filter; needs_action/validation_ready columns; closeEvent cleanup |
| `gui/strategy_memory_adapter.py` | 7 new methods: search_advanced, get_validation_queue, get_active_research_threads, get_repeated_patterns, load_memory_detail, load_memory_links, load_safe_commands |
| `main.py` | 3 new CLI commands; enhanced summary/list/search/show/update-status output |
| `research_intelligence/recommendation_engine.py` | memory_summary parameter; P3 seen-before "(seen)" tagging |
| `backtest_coach/coach_task_builder.py` | memory_items parameter; _deduplicate_tasks(); related_memory_id lookup |
| `regression/suite_registry.py` | 6 new research_os test cases; 2 release gate test cases |
| `stable_release/stable_release_checklist_v060.py` | 3 new v0.8.1 check methods |
| `intelligence_stable/intelligence_stable_checklist.py` | 2 new v0.8.1 safety checks |
| `stable_release/capability_matrix.py` | strategy_memory_ux StableCapability; strategy_research_memory updated |
| `intelligence_stable/intelligence_capability_matrix.py` | sm_ux_v081 IntelligenceStableCapability |
| `reports/intelligence_stable_report.py` | Strategy Memory Layer section updated with v0.8.1 status |
| `gui/navigation/tab_registry.py` | memory ux, validation queue, active threads, repeated patterns keywords |
| `docs/strategy_research_memory.md` | Updated to v0.8.1 |
| `docs/strategy_memory_ux_v0.8.1.md` | New: full v0.8.1 UX documentation |

### New CLI Commands (3)

```
python main.py strategy-memory-validation-queue   # VALIDATING-status memories ready for decision
python main.py strategy-memory-active-threads     # REVIEWING-status active research threads
python main.py strategy-memory-repeated-patterns  # Memories seen more than once
```

### New UX Fields on StrategyMemoryItem

`display_title`, `needs_action`, `validation_ready`, `status_hint`, `next_step`, `last_action_at`, `safe_command_count`, `blocked_command_count`, `accepted_is_research_only`

### Safety

- `accepted_is_research_only=True` always enforced in `__post_init__` and `from_dict`
- `load_safe_commands()` blocks BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE keywords
- Status action button for ACCEPTED shows explicit research-only reminder dialog
- 3 new checklist checks verify invariants at release time

### Known Limitations

- Status flow is manual — no auto-advance from REVIEWING → VALIDATING
- Memory items do not persist GUI edits without an explicit save/update-status call
- `related_memory_id` computed but not yet stored as StrategyMemoryItem field in CoachTrainingTask

---

> **[!] No real orders. Research Only. Production Trading: BLOCKED. Not Investment Advice.**
