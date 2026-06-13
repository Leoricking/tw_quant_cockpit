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

*TW Quant Cockpit v1.1.0 — Data Universe Expansion — Research Only — Not Investment Advice*

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

---

## v1.1.0 — Data Universe Expansion

v1.1.0 adds a tiered universe management system and per-symbol real data coverage analysis.

### Universe Tiers

| Tier | Symbols | Description |
|------|---------|-------------|
| CORE_10 | 10 | 高流動性核心股 (台積電/聯發科…) |
| RESEARCH_30 | 30 (累積) | Core + 20 研究股 |
| EXPANDED_50 | 50 (累積) | Research + 20 擴展股 |
| BROAD_100 | ≤100 (累積) | Schema 支援；手動添加 |

### Data Coverage Requirements

- `REAL_DATA_COVERAGE_REQUIRED = True` — Real data CSV required for analysis
- `MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False` — Mock data cannot produce formal conclusions

### v1.1.0 CLI Commands

```
python main.py universe-build --tier core10
python main.py universe-summary --tier research30
python main.py universe-health
python main.py universe-coverage --tier research30 --mode real
python main.py universe-symbol --stock 2454
python main.py universe-missing --tier expanded50
python main.py universe-report --tier research30
```

See `docs/data_universe_expansion_v1.1.0.md` for full details.

**[!] Real Data Required. Mock Formal Conclusion BLOCKED. Research Only. No Real Orders.**

---

## v1.1.1 — Data Import UX & Batch Onboarding

v1.1.1 adds a complete data import pipeline: file discovery, column auto-mapping, duplicate/conflict detection, safe merge planning, dry-run validation, batch execution, retry manifests, and universe coverage refresh.

### Import Modes

| Mode | Default | Description |
|------|---------|-------------|
| `MERGE_SAFE` | Yes | Merges rows not already present |
| `APPEND_SAFE` | No | Appends only; fails if any overlap |
| `DRY_RUN` | Yes (batch) | Simulates all operations without writing |
| `REPLACE_EXPLICIT` | **BLOCKED** | Disabled by default; never auto-overwrite |

### Conflict Policy

- Duplicate identical rows → skipped (no error)
- Conflicting rows (same date, different values) → routed to `REVIEW`
- `REPLACE_EXPLICIT` is **blocked** unless `--allow-replace` is set
- Conflicts are never auto-overwritten

### Supported File Types

| Type | Detection |
|------|-----------|
| `XQ_CSV` | Chinese headers: 時間, 開盤價, 最高價, 最低價, 收盤價, 成交量 |
| `XQ_EXCEL` | `.xlsx` with XQ column markers |
| `STANDARD_CSV` | English OHLCV headers |
| `EXCEL` | `.xlsx` without XQ markers |
| `UNKNOWN` | Cannot detect schema → BLOCKED |

### v1.1.1 CLI Commands

```
python main.py import-discover --path <dir>
python main.py import-preview --file <file>
python main.py import-validate --path <dir>
python main.py import-plan --path <dir>
python main.py import-batch --path <dir> --dry-run
python main.py import-batch --path <dir> --execute --allow-write
python main.py import-retry-manifest [--output-dir data/import_reports]
python main.py import-onboarding-health
python main.py import-onboarding-report [--mode real]
```

### Recommended Import SOP

1. `import-discover --path <dir>` — find all importable files
2. `import-validate --path <dir>` — check OHLC integrity, column coverage
3. `import-plan --path <dir>` — preview MERGE_SAFE / BLOCKED / REVIEW plan
4. `import-batch --path <dir> --dry-run` — full dry-run (no writes)
5. Review plan; resolve BLOCKED and REVIEW items manually
6. `import-batch --path <dir> --execute --allow-write` — execute safe items
7. `universe-coverage --tier research30 --mode real` — verify coverage updated

See `docs/data_import_onboarding_v1.1.1.md` for full details.

**[!] dry_run=True by default. REPLACE_EXPLICIT BLOCKED. Conflicts → REVIEW. No Real Orders.**
