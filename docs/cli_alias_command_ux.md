# CLI Alias / Command UX Polish — v0.5.1

> **[!] Research Only — No Real Orders — Production Trading: BLOCKED**
> `read_only=True` | `no_real_orders=True` | `production_blocked=True` | `real_order_ready=False`

---

## v0.5.1 目標 (Goals)

v0.5.1 introduces a full CLI alias and command UX polish for the TW Quant Cockpit.
Key goals:

1. **One authoritative command registry** — every command is registered in `CLICommandRegistry` with name, category, purpose, aliases, safety level, and examples.
2. **Short alias map** — frequently-used commands have memorable 1–3 word aliases (`daily`, `dq`, `gui`, `version`, …).
3. **Discovery layer** — keyword search and intent-based suggestion via `CLICommandDiscovery`.
4. **Curated examples** — grouped quick-start, daily, weekly, safety, and alias examples via `CLIHelpExamples`.
5. **Automated UX audit** — `CLIUXReportBuilder` and `CLIUXReport` track coverage, conflicts, and safety invariants.
6. **GUI panel** — `CLIUXPanel` exposes registry, alias map, search, and report generation in the Cockpit GUI.

---

## Why CLI Aliases?

The cockpit has accumulated 100+ CLI commands across 17 categories. Without aliases:

- Users must remember long command names (`research-workflow`, `data-quality-gate`, …)
- Daily workflows require typing verbose flags every time
- New researchers cannot discover relevant commands without reading source code

With aliases:

```bash
python main.py daily        # → run-research --profile daily --mode real
python main.py dq           # → data-quality-gate
python main.py gui          # → cockpit
python main.py version      # → version-info
```

Aliases are **transparent** — they inject default args, are documented in the alias map, and are audited for safety on every build.

---

## Command Categories

All 17 command categories:

| # | Category      | Description |
|---|---------------|-------------|
| 1  | `utility`     | Version info, OS summary, CLI introspection tools |
| 2  | `data`        | Download, import, audit, freshness checks |
| 3  | `provider`    | Data provider health, reliability, API cache |
| 4  | `quality`     | Data quality gate, CSV cleaning |
| 5  | `strategy`    | Strategy preview, knowledge base, rule governance |
| 6  | `backtest`    | Backtest simulations, screener, buy-point validation |
| 7  | `portfolio`   | Paper trading, portfolio simulation, stock reports |
| 8  | `ml`          | Feature store, leakage checks, model monitoring, drift |
| 9  | `replay`      | Intraday replay sessions, training summaries |
| 10 | `journal`     | Research journal: add, list, review, summarize |
| 11 | `notification`| Notification scan, list, report, clear |
| 12 | `review`      | Daily/weekly research review sessions |
| 13 | `coach`       | AI research coach: checklist, rule queue, data repair |
| 14 | `workflow`    | Run-research, research-workflow, update-data |
| 15 | `os_planning` | Research OS audit, module/CLI/GUI coverage |
| 16 | `release`     | Stable release check, regression suite, scheduler |
| 17 | `gui`         | Cockpit GUI launcher |

---

## Alias Map

Full alias reference table:

| Alias | Target Command | Default Args | Category |
|-------|---------------|--------------|----------|
| `daily` | `run-research` | `--profile daily --mode real` | workflow |
| `quick` | `run-research` | `--profile quick --mode real` | workflow |
| `workflow-daily` | `research-workflow` | `--type daily_research` | workflow |
| `workflow-weekly` | `research-workflow` | `--type weekly_review` | workflow |
| `coach-daily` | `research-coach` | `--period daily` | coach |
| `review-daily` | `research-review` | `--period daily` | review |
| `dq` | `data-quality-gate` | — | quality |
| `quality` | `data-quality-gate` | — | quality |
| `freshness` | `data-freshness` | — | data |
| `api-check` | `api-token-check` | — | provider |
| `api-diag` | `api-fetch-diagnostics` | — | provider |
| `provider` | `provider-health` | — | provider |
| `providers` | `provider-reliability` | — | provider |
| `rules` | `rule-governance` | — | strategy |
| `signals` | `signal-quality` | — | strategy |
| `weights` | `tune-rule-weights` | — | strategy |
| `strategy-knowledge` | `strategy-knowledge-summary` | — | strategy |
| `ml-summary` | `ml-knowledge-feature-summary` | — | ml |
| `ml-leakage` | `ml-knowledge-leakage-check` | — | ml |
| `feature-store` | `ml-feature-store-report` | — | ml |
| `replay` | `intraday-replay` | — | replay |
| `replay-report` | `intraday-replay-report` | — | replay |
| `replay-sessions` | `replay-session-list` | — | replay |
| `journal` | `journal-summary` | — | journal |
| `notes` | `journal-list` | — | journal |
| `notify` | `notification-list` | — | notification |
| `alerts` | `notification-list` | — | notification |
| `os` | `research-os-summary` | — | os_planning |
| `os-audit` | `research-os-audit` | — | os_planning |
| `version` | `version-info` | — | utility |
| `release-check` | `stable-release-check` | — | release |
| `regress` | `regression-suite` | `--quick` | release |
| `gui` | `cockpit` | — | gui |
| `dashboard` | `cockpit` | — | gui |
| `open` | `cockpit` | — | gui |

---

## Quick Start Examples

```bash
# Show version
python main.py version-info

# Research OS overview
python main.py research-os-summary

# Quick research run (no orders)
python main.py run-research --profile quick --mode real

# Auto-generate all daily reports
python main.py auto-report --mode real --profile daily

# Launch the GUI
python main.py cockpit --mode real
```

---

## Daily Research Examples

```bash
# Data quality gate
python main.py data-quality-gate --mode real

# Provider reliability check
python main.py provider-reliability --mode real

# Daily research coaching
python main.py research-coach --mode real --period daily

# Preview daily workflow (no execution)
python main.py research-workflow --mode real --type daily_research --dry-run

# Run full daily workflow
python main.py research-workflow --mode real --type daily_research
```

### Using aliases for daily research:

```bash
python main.py daily      # run-research --profile daily --mode real
python main.py dq         # data-quality-gate
python main.py providers  # provider-reliability
python main.py rules      # rule-governance
python main.py signals    # signal-quality
```

---

## Weekly Review Examples

```bash
# Weekly research review
python main.py research-review --mode real --period weekly

# Journal summary
python main.py journal-summary

# Rule governance audit
python main.py rule-governance --mode real

# Experiment list
python main.py experiment-list

# Weekly review workflow
python main.py research-workflow --mode real --type weekly_review
```

### Using aliases:

```bash
python main.py review-daily   # research-review --period daily
python main.py workflow-weekly # research-workflow --type weekly_review
python main.py journal         # journal-summary
python main.py notes           # journal-list
```

---

## Safety Examples

```bash
# Stable release gate
python main.py stable-release-check --mode real

# Quick regression suite
python main.py regression-suite --mode real --quick

# Research OS safety audit
python main.py research-os-safety

# CLI UX audit
python main.py cli-ux-report --mode real
```

### Using aliases:

```bash
python main.py release-check   # stable-release-check
python main.py regress         # regression-suite --quick
python main.py os-audit        # research-os-audit
```

---

## Backward Compatibility

All commands registered in previous versions (v0.4.x) are preserved unchanged:

- No command names have been removed.
- Old command names continue to work as canonical commands.
- Where short aliases are introduced, the full canonical name continues to work.
- Aliases inject default args **in addition** to any args the user provides — user-supplied args always take precedence.

Example:
```bash
# These are equivalent — alias just supplies defaults
python main.py daily
python main.py run-research --profile daily --mode real
```

---

## Safety Invariants

All classes in the `cli/` package enforce these safety invariants as class attributes:

```python
read_only          = True
no_real_orders     = True
production_blocked = True
real_order_ready   = False
```

### Blocked alias keywords

The following keywords are **permanently blocked** from appearing in any alias name or target command:

```
buy, sell, order, submit_order, place_order, broker, shioaji,
live_trade, auto_trade, execute_trade, margin, short_sell,
cover_order, .env, token, password, api_key, git, cd,
&&, ;, ||, |, >, <
```

Any alias entry containing a blocked keyword is:
1. Flagged `safety_blocked=True` in the alias map.
2. Disabled (`enabled=False`) automatically.
3. Logged as an error at module load time.

### Safety checklist

- [ ] No alias resolves to a real-money order command
- [ ] No alias name contains buy/sell/order/broker/shioaji
- [ ] No alias target contains buy/sell/order/broker/shioaji
- [ ] `CLIUXReportBuilder.build()["safety_status"] == "PASS"`
- [ ] All command classes carry `read_only=True`, `no_real_orders=True`, `production_blocked=True`

---

## Architecture

```
cli/
  __init__.py            — package exports
  command_registry.py    — CLICommand dataclass + CLICommandRegistry
  alias_map.py           — CLIAliasMap (short alias → canonical command)
  command_discovery.py   — CLICommandDiscovery (search + suggest)
  help_examples.py       — CLIHelpExamples (curated examples)
  cli_ux_report.py       — CLIUXReportBuilder (audit data builder)

reports/
  cli_ux_report.py       — CLIUXReport (generates .md report file)

gui/
  cli_ux_adapter.py      — CLIUXAdapter (GUI bridge, no PySide6 dependency)
  cli_ux_panel.py        — CLIUXPanel (PySide6 panel with 5-tab layout)

docs/
  cli_alias_command_ux.md  — This document
```

---

## Next UX Roadmap

| Version | Feature |
|---------|---------|
| v0.5.2  | GUI Tab Grouping — group Cockpit panels by command category |
| v0.5.3  | Regression Consolidation — unify regression and validation suites |
| v0.5.4  | CLI Autocomplete — shell completion scripts for bash/zsh |
| v0.5.5  | Command Deprecation Pipeline — automated legacy command cleanup |

---

> **[!] Safety Footer**
> This document describes research and simulation tooling only.
> No real orders are placed. No broker connection is made.
> Production trading is permanently blocked.
> `read_only=True` | `no_real_orders=True` | `production_blocked=True` | `real_order_ready=False`
