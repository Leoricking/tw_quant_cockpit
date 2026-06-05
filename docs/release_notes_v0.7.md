# TW Quant Cockpit — Release Notes v0.7.x

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] All versions in this file are research intelligence upgrades only.**

---

## v0.7.0 — Research Intelligence Upgrade

**Released:** 2026-06-05

### Overview

v0.7.0 introduces the Research Intelligence subsystem — a full pipeline that aggregates signals from all Research OS modules, generates ranked research recommendations, builds P0/P1/P2/P3 priority boards, and produces daily (7 items) and weekly (12 items) research plans.

### New Files

| File | Description |
|------|-------------|
| `research_intelligence/__init__.py` | Package docstring |
| `research_intelligence/research_intelligence_schema.py` | Dataclasses, constants, forbidden action guard |
| `research_intelligence/signal_aggregator.py` | Collects signals from 8 source modules |
| `research_intelligence/recommendation_engine.py` | Converts signals to ranked recommendations |
| `research_intelligence/priority_planner.py` | Builds P0/P1/P2/P3 priority board |
| `research_intelligence/research_intelligence_store.py` | CSV persistence (6 output files) |
| `research_intelligence/research_intelligence_engine.py` | Master pipeline engine |
| `reports/research_intelligence_report.py` | Markdown report generator (9 sections) |
| `gui/research_intelligence_adapter.py` | GUI ↔ backend bridge |
| `gui/research_intelligence_panel.py` | PySide6 Research Intelligence tab |

### Modified Files

| File | Change |
|------|--------|
| `gui/dashboard.py` | Added ResearchIntelligencePanel tab (guarded import) |
| `gui/navigation/tab_registry.py` | Added research_intelligence tab metadata |
| `regression/suite_registry.py` | Added 4 research intelligence regression tests |
| `stable_release/capability_matrix.py` | Added `research_intelligence_upgrade` StableCapability |
| `report_pack/report_pack_schema.py` | Added `REPORT_RESEARCH_INTELLIGENCE` constant |
| `report_pack/report_registry.py` | Added to full pack |
| `report_pack/report_collector.py` | Added pattern map for research_intelligence |
| `reports/auto_report_center.py` | Added research intelligence to full/daily profiles |
| `data_coverage/data_coverage_schema.py` | Added `DOMAIN_RESEARCH_INTELLIGENCE` constant |
| `data_coverage/data_coverage_registry.py` | Added 2 research intelligence coverage items |
| `stable_release/stable_release_checklist_v060.py` | Added v0.7.0 import checks |
| `main.py` | Added 9 CLI commands + handlers |
| `.gitignore` | Added research intelligence runtime outputs |
| `docs/index.md` | Updated version, added v0.7 doc entries |
| `README.md` | Added v0.7.0 section |

### New CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py research-intelligence` | Run full pipeline |
| `python main.py research-intelligence-summary` | Show latest summary |
| `python main.py research-intelligence-signals` | Show latest signals |
| `python main.py research-intelligence-recommendations` | Show latest recommendations |
| `python main.py research-intelligence-priority` | Show priority board |
| `python main.py research-intelligence-daily-plan` | Show daily plan (7 items) |
| `python main.py research-intelligence-weekly-plan` | Show weekly plan (12 items) |
| `python main.py research-intelligence-report` | Generate Markdown report |

### Safety Constraints

- `_validate_action()` in schema blocks all FORBIDDEN_ACTION_TYPES: `BUY`, `SELL`, `ORDER`, `EXECUTE`, `SUBMIT_ORDER`, `AUTO_TRADE`
- All recommendations are research actions: `REVIEW`, `RESEARCH`, `PRACTICE`, `FIX_DATA`, `GENERATE_REPORT`, `RUN_REGRESSION`, `RUN_BACKTEST`, `READ_REPORT`, `WAIT`
- `read_only=True`, `no_real_orders=True`, `production_blocked=True` on all classes
- `real_order_ready=False` explicitly set

### Signal Sources

| Source Module | Signal Categories |
|--------------|-------------------|
| `data_coverage` | `DATA_GAP`, `PROVIDER_LIMITATION` |
| `report_pack` | `REPORT_GAP` |
| `replay_training` | `REPLAY_MISTAKE`, `TRAINING_TASK` |
| `journal` | `JOURNAL_PATTERN` |
| `rule_governance` | `RULE_REVIEW` |
| `strategy_knowledge` | `STRATEGY_RESEARCH` |
| `regression` | `SYSTEM_RISK`, `REGRESSION_WARNING` |
| `stable_release` | `STABLE_RELEASE_NOTE` |

---

## v0.7.1 — Intelligence UX Polish

**Released:** 2026-06-05

### Overview

v0.7.1 polishes the Research Intelligence UX. Key additions: Today Focus card, Why Now / Risk If Ignored columns in Priority Board and plans, `classify_command_safety()` with six safety labels, Copy Command button, priority/category/source filters in GUI, improved CLI output for all 8 research-intelligence commands.

### Schema Changes (`research_intelligence_schema.py`)

| Addition | Description |
|----------|-------------|
| `CMD_SAFE_READ_ONLY` … `CMD_BLOCKED_TRADING` | Six command safety label constants |
| `_FORBIDDEN_CMD_KEYWORDS` | Set of keywords that trigger BLOCKED_FOR_TRADING |
| `classify_command_safety(command)` | Returns one of six safety labels |
| `ResearchSignal.display_label` | User-friendly signal label |
| `ResearchSignal.user_friendly_reason` | Plain-language reason |
| `ResearchSignal.safe_action_hint` | e.g. "Safe: read-only command" |
| `ResearchRecommendation.why_now` | Time-sensitive reason |
| `ResearchRecommendation.risk_if_ignored` | Risk description |
| `ResearchRecommendation.command_safety` | One of six safety labels |
| `ResearchRecommendation.safe_command_label` | Display form of safety |
| `ResearchRecommendation.display_order` | Explicit display ordering |
| `ResearchRecommendation.optional` | Whether recommendation is optional |
| `ResearchRecommendation.dismissible` | Whether recommendation is dismissible |
| `ResearchIntelligenceSummary.today_focus` | One-liner top priority focus |
| `ResearchIntelligenceSummary.top_p0_title` | Top P0 item title |
| `ResearchIntelligenceSummary.top_p1_title` | Top P1 item title |
| `ResearchIntelligenceSummary.safe_command_count` | Count of safe commands |
| `ResearchIntelligenceSummary.blocked_trading_action_count` | Always 0 by design |
| `ResearchIntelligenceSummary.optional_recommendation_count` | Count of optional items |

### Report Changes (`reports/research_intelligence_report.py`)

| Section | Change |
|---------|--------|
| `_section_today_focus` | NEW — Today Focus summary table |
| `_section_priority_board` | UPDATED — Why Now / Risk If Ignored / Safe Command columns |
| `_section_daily_plan` | UPDATED — Why Now / Risk If Ignored columns |
| `_section_weekly_plan` | UPDATED — Why Now / Risk If Ignored columns |
| `_section_signals_by_module` | NEW — signals grouped by source module |
| `_section_command_safety` | NEW — safe commands count, blocked count, command list |
| `_section_what_not_to_do` | NEW — static forbidden action table |

### GUI Changes (`gui/research_intelligence_panel.py`)

- Summary cards: Today Focus, P0, P1, Safe Commands, Blocked Trading (always 0)
- Priority Board columns: Why Now, Risk If Ignored, Safe Command, Safety Label, Due
- Plan table columns: Command, Safety Label, Why Now, Risk If Ignored
- Filter controls: Priority, Category, Source Module dropdowns
- Selected Command display field + Copy Command button
- Filter auto-populates after Run Intelligence

### CLI Changes (`main.py`)

| Command | Change |
|---------|--------|
| `research-intelligence-summary` | Shows Today Focus, Top P0, Top P1, Safe Commands, Blocked Trading |
| `research-intelligence-recommendations` | Shows Priority/Action/Safety/Title/Command/Why Now columns |
| `research-intelligence-priority` | Shows P0/P1/P2/P3 with Why Now and Command+Safety label |
| `research-intelligence-daily-plan` | Shows max 7 items with Command/Safety/Why Now |
| `research-intelligence-weekly-plan` | Shows max 12 items with Command/Safety/Why Now |
| `research-intelligence-report` | Shows report path, Status, Today Focus, Signals, Safe Commands |

### New Checks

| Check | Location |
|-------|----------|
| `research_intelligence_ux_safety` | `stable_release_checklist_v060.py` — BLOCKED_FOR_TRADING classification |
| `recommendations_no_forbidden_actions` | `stable_release_checklist_v060.py` — no BUY/SELL/ORDER in output |
| 4 new regression tests | `regression/suite_registry.py` — recommendations, priority, daily-plan, report |

### New Capability

- `intelligence_ux_polish` added to `capability_matrix.py` as STABLE in v0.7.1

---

> [!] All recommendations are research actions only. No BUY/SELL/ORDER generated. Not investment advice.
