# TW Quant Cockpit — Daily Research SOP (v0.3.23)

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## Overview

This SOP defines step-by-step procedures for daily research using TW Quant Cockpit. All operations are read-only. No orders are placed at any step.

---

## Standard After-Market Flow (收盤後標準流程)

**Trigger:** After 16:30 market close (Taiwan time)

### Step 1 — Update Data

```bash
python main.py update-data --mode real
```

**What it does:**
- Fetches today's OHLCV prices from configured providers
- Updates institutional (法人) buy/sell data
- Updates margin trading (融資融券) data
- Updates monthly revenue (月營收) if available

**Expected output:**
```
[update-data] daily_price      : OK    (1523 rows)
[update-data] institutional    : OK    (1523 rows)
[update-data] margin           : OK    (1523 rows)
[update-data] monthly_revenue  : OK    (847 rows)
```

**If warnings appear:**
- `Token NOT_CONFIGURED` — provider skipped; data uses cache. Research can continue.
- `0 rows returned` — check provider health (`python main.py provider-health`)
- `STALE` warning — data may be from prior day; non-blocking for research

**Dry-run option:** `--dry-run` to preview without writing.

---

### Step 2 — Run Research

```bash
python main.py run-research --mode real --profile standard
```

**What it does:**
- Calculates signal quality scores for all active rules
- Runs portfolio simulation with current signals
- Generates BOOST/KEEP/REDUCE recommendations
- Saves results to `reports/auto_report_center/YYYY-MM-DD/`

**Expected output:**
```
[run-research] data_quality_gate    : OK
[run-research] signal_quality       : OK
[run-research] portfolio_simulation : OK
[run-research] auto_report          : OK
Status: OK | Steps: 4/4
```

**If a step fails:**
- Check the `User Message` column — it explains what went wrong in plain language
- Check `Can Ignore` — if True, research can continue despite the warning
- Steps with `SKIPPED` status are non-critical and can be ignored

---

### Step 3 — Review Results

```bash
python main.py open-cockpit --mode real
```

Or review reports directly:

```
reports/auto_report_center/YYYY-MM-DD/
  daily_summary_YYYY-MM-DD.md
  signal_quality_report_YYYY-MM-DD.md
  portfolio_simulation_report_YYYY-MM-DD.md
  data_quality_gate_report_YYYY-MM-DD.md
```

**Review checklist:**
- [ ] Production Readiness Score ≥ 75 (READY_FOR_RESEARCH or higher)
- [ ] No FAIL-severity blockers (PRODUCTION_BLOCKED is always present; ignore it)
- [ ] Signal quality: note any REDUCE or DISABLE recommendations
- [ ] Portfolio KPIs: Sharpe > 1.5, MaxDD < 20%, Profit Factor > 1.5
- [ ] Candidate stocks reviewed in daily_summary

---

## One-Command Shortcut

```bash
python main.py daily-workflow --mode real --profile standard
```

Runs Steps 1–2 automatically and saves the workflow summary.

---

## Quick Check Flow (快速檢查流程)

Use when you only need a fast status check (< 1 minute).

```bash
python main.py run-research --mode real --profile quick
```

**Steps run:** data_quality_gate + auto_report only.

**Use case:** Mid-day check, or when update-data was already run.

---

## Weekend Full Research Flow (週末完整研究)

Use on weekends for comprehensive analysis.

```bash
python main.py daily-workflow --mode real --profile full
```

**Additional steps vs. standard:**
- Long-term strategy validation (multi-year backtest)
- Rule weight comparison across 7 configurations
- Extended portfolio simulation

**Expected time:** ~10 minutes.

**Review checklist (extended):**
- [ ] All standard checklist items
- [ ] Long-term validation: strategy performance stable across years?
- [ ] Rule weight tuning: any rules consistently REDUCE/DISABLE?
- [ ] Weight adjustment candidates identified (manual review required before any change)

---

## Mock Mode Flow (開發/測試)

For testing or development without real data dependencies.

```bash
python main.py daily-workflow --mode mock --profile standard
```

**Note:** Mock data is used. Backtest Readiness Score capped when mock contamination detected. Do not use mock mode for investment research.

---

## Data Quality Gate Review

After running research, review the data quality gate report:

```bash
python main.py data-quality-gate --mode real
```

**Interpretation:**

| Production Readiness | Action |
|---------------------|--------|
| STRONG (90–100) | Proceed normally |
| READY_FOR_RESEARCH (75–89) | Proceed; note sub-score gaps |
| PARTIAL (60–74) | Proceed with caution; check missing data |
| WEAK (40–59) | Investigate blockers before using results |
| BLOCKED (0–39) | Do not rely on results; fix data issues first |

**Always expected blockers:**
- `PRODUCTION_BLOCKED` (FATAL, can_continue_research=True) — This is a safety invariant, not an error. Research can always continue.

---

## Signal Quality Review

Review signal recommendations (research only; do not auto-apply):

| Label | What to do |
|-------|-----------|
| BOOST | Note rule as positive contributor; review context before weight change |
| KEEP | No action needed |
| REDUCE | Flag rule for manual review; do not reduce weight without analysis |
| DISABLE | Flag rule for deeper review; confirm consistently negative before disabling |

**Rule:** Never apply weight changes based solely on a single day's recommendation.

---

## Troubleshooting Common Issues

| Problem | Quick fix |
|---------|-----------|
| `FINMIND_TOKEN not configured` | Set token in `.env`; re-run update-data |
| Data freshness STALE | Check provider health; re-run fetch-provider |
| Production Readiness BLOCKED | Check data_quality_gate report for specific blockers |
| GUI won't open | Verify PySide6 installed: `pip install PySide6` |
| UnicodeDecodeError in output | Expected on Windows cp950; non-blocking |

See [Troubleshooting](troubleshooting.md) for full solutions.

---

## Research Review Notes Template

After each research session, consider noting:

```
Date: YYYY-MM-DD
Production Readiness: XX (CLASSIFICATION)
Top candidates: [list]
Signal quality changes: [any new REDUCE/DISABLE]
Portfolio KPIs: Sharpe=X.X | MaxDD=X% | PF=X.X
Action items: [any manual follow-up]
```

**Reminder:** These notes are research observations, not investment decisions.

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
