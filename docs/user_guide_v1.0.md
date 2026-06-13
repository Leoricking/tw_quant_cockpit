# TW Quant Cockpit User Guide v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## 一、System Overview (系統概覽)

TW Quant Cockpit is a **Research Trading Cockpit** — a quantitative research platform for Taiwan equity markets.

| Safety Flag | Value |
|-------------|-------|
| Research Only | True |
| No Real Orders | True |
| Production Trading BLOCKED | True |
| Broker Execution Disabled | True |
| VALIDATED does not enable trading | True |
| Paper Trading | Simulation Only |
| Mock Realtime | Simulation Only |
| Not Investment Advice | True |

### What This System Does

- Backtests strategies on historical data
- Tracks strategy validation status (INSUFFICIENT → VALIDATED)
- Displays evidence chains from multiple research modules
- Provides daily workflow guidance and coaching
- Generates research reports

### What This System Does NOT Do

- No real trading actions of any kind
- No connection to any broker API
- No automated position management
- No investment recommendations

---

## 二、Daily Usage Flow (每日使用流程)

Recommended daily flow:

1. **Open GUI** — `python main.py cockpit`
2. **Research Cockpit Stable** — check overall system health
3. **Strategy Lab Dashboard** — view strategy grade distribution
4. **Strategy Validation** — review VALIDATED / VALIDATING / OBSERVATIONAL strategies
5. **Evidence Graph** — trace evidence chains, check for contradictions
6. **Crash Reversal** — review crash reversal conditions if relevant
7. **Data Hygiene** — check for stale or missing data
8. **Reports** — generate daily/weekly/full report pack
9. **Paper / Mock simulation** — run paper or mock realtime to observe behavior

Each step is research-only. No real trading at any step.

---

## 三、Main Modules (主要模組)

| Module | Purpose |
|--------|---------|
| Research Intelligence | Priority board, daily/weekly research plan, signal aggregation |
| Strategy Memory | Memory types, status lifecycle, validation queue |
| Evidence Graph UX | Thread quality, gap view, contradiction detection |
| Strategy Validation Score | Cross-module confidence scoring (INSUFFICIENT→VALIDATED) |
| Crash Reversal | Crash cause classification, stabilization checklist, post-crash filters |
| Strategy Lab Dashboard | Unified single-view dashboard — validation board, evidence board, action board |
| Backtest Coach | Coach tasks from backtest weaknesses and replay mistakes |
| Training Metrics | Tracks training effectiveness across all modules |
| Data Report Hygiene | Inventory of runtime outputs, stale data detection |
| Regression Hardening | Safety scanner, release gate health, known warning classification |
| Documentation Health | Core doc presence, safety phrase checks, docs indexer |

---

## 四、Status Interpretation (狀態解讀)

| Status | Meaning |
|--------|---------|
| INSUFFICIENT | Not enough data to form any judgment |
| OBSERVATIONAL | Some signal observed, not yet validated |
| VALIDATING | Under active validation process |
| VALIDATED | Research-validated across multiple evidence sources |
| CONFLICTED | Contradicting evidence sources — review required |
| REJECTED | Evidence consistently against the strategy |

**IMPORTANT: VALIDATED does not enable trading.**
VALIDATED means the strategy has passed research validation criteria.
It does NOT mean it is ready for real trading, live positions, or broker execution.

---

## 五、Daily Decision Framework (每日決策框架)

Allowed research actions:

| Action | Description |
|--------|-------------|
| REVIEW | Review strategy details, evidence, or reports |
| READ_REPORT | Read generated Markdown reports |
| BACKTEST_MORE | Run additional backtests for more evidence |
| PRACTICE_REPLAY | Practice with intraday replay cockpit |
| REVIEW_RISK | Review risk parameters in reports |
| WAIT | Wait for more data or market observations |
| KEEP_OBSERVING | Continue tracking a strategy in OBSERVATIONAL state |
| DO_NOT_CHASE | Flag to avoid chasing a price action |

These are research actions only. None of these actions result in real trading.

---

## 六、Safety Declaration (安全聲明)

> **No Real Orders** — This system does not and cannot place real trading actions.
>
> **No broker execution** — There is no connection to any broker API (Shioaji, Mega, or any other).
>
> **No auto trading** — No automatic trading, no automatic rule weight changes.
>
> **Broker Execution Disabled** — Broker execution is explicitly disabled in all code paths.
>
> **VALIDATED does not enable trading** — VALIDATED grade is research-only.
>
> **Not Investment Advice** — Nothing in this system constitutes investment advice.

---

## 七、Examples & Templates (v1.0.6)

TW Quant Cockpit v1.0.6 adds example workflows and fillable templates to help with common research tasks.

### Example Workflows

Example workflows are located in `docs/examples/`. Each example shows safe CLI commands for a specific scenario:

- `daily_operation_example.md` — Daily research session
- `weekend_review_example.md` — Weekend review
- `claude_code_maintenance_example.md` — Maintenance with git -C rules
- (and 7 more)

### Fillable Templates

Templates are located in `docs/templates/`. Each template is a fillable form:

- `daily_review_template.md` — Daily review form
- `release_prompt_template.md` — Release checklist
- `handoff_summary_template.md` — Handoff form
- (and 5 more)

### Workflow Commands

```
python main.py workflow-templates-health
python main.py workflow-templates-summary
python main.py workflow-templates-report --mode real
```

---

*TW Quant Cockpit v1.0.9 — Final Maintenance Rollup — Research Only — Not Investment Advice*

---

## v1.0.9 — Final Maintenance Rollup

### Final Rollup CLI Commands

```
python main.py final-rollup
python main.py final-rollup-history
python main.py final-rollup-health
python main.py final-rollup-maintenance-plan
python main.py final-rollup-smoke
python main.py final-rollup-report --mode real
```

**[!] Research Only. No Real Orders. Not Investment Advice. v1.0 Maintenance Line Complete.**
