# TW Quant Cockpit — Troubleshooting (v0.3.23)

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## §1 — FINMIND_TOKEN not configured

**Phenomenon:** Command output shows `FINMIND_TOKEN not configured` or `Token NOT_CONFIGURED`.

**Cause:** The `.env` file is missing the `FINMIND_TOKEN` key, or the token is empty.

**Can ignore?** Yes. Research can continue using cached data. Data may be stale.

**Fix:**
1. Obtain a FinMind API token at the FinMind website
2. Add to `.env` in the project root:
   ```
   FINMIND_TOKEN=your_token_here
   ```
3. Re-run the command

**Verification:**
```bash
python main.py provider-health
# Should show: finmind | CONFIGURED
```

---

## §2 — Data freshness STALE

**Phenomenon:** Data Quality Gate shows `freshness: STALE` or Production Readiness below 75.

**Cause:** Data files are older than the expected freshness threshold (typically 2 trading days).

**Can ignore?** Depends on use case. Research with stale data produces valid analysis but may miss recent market moves.

**Fix:**
```bash
python main.py update-data --mode real
```

If data is still stale after update-data:
1. Check `python main.py provider-health` — confirm tokens are CONFIGURED
2. Check network connectivity
3. Check if market was closed (holiday) — expected staleness on non-trading days

**Verification:**
```bash
python main.py data-quality-gate --mode real
# Check freshness sub-score
```

---

## §3 — Production Readiness WEAK or BLOCKED

**Phenomenon:** Production Readiness Score below 60 (WEAK) or below 40 (BLOCKED).

**Cause:** Multiple data sources are stale, missing, or have low coverage.

**Can ignore?** WEAK: proceed with caution. BLOCKED: investigate before using results.

**Fix:**
1. Run `python main.py data-quality-gate --mode real` to see specific blockers
2. Check each blocker's `next_step` field
3. Address missing data sources: run `update-data`, check tokens
4. `PRODUCTION_BLOCKED` blocker is always present (FATAL) — this is expected and does not require a fix

**Verification:**
```bash
python main.py data-quality-gate --mode real
# Target: Production Readiness >= 75
```

---

## §4 — PRODUCTION_BLOCKED in data quality gate

**Phenomenon:** Data Quality Gate always shows a `PRODUCTION_BLOCKED` blocker with FATAL severity.

**Cause:** This is a hard-coded safety invariant. It is expected and correct behavior.

**Can ignore?** Yes. `can_continue_research=True` for this blocker. Research always proceeds normally.

**Explanation:** PRODUCTION_BLOCKED=True means real orders are permanently blocked. It appears in the gate report to confirm the safety invariant is active. It is not a data problem.

**No fix needed.**

---

## §5 — UnicodeDecodeError or garbled output

**Phenomenon:** CLI output shows garbled characters or `UnicodeDecodeError`.

**Cause:** Windows terminal uses cp950 encoding; some Unicode characters cannot be encoded.

**Can ignore?** Yes. The `CLIOutput` formatter uses ASCII fallback for unencodable characters. Content is preserved.

**Fix:** Non-blocking. No action required. If specific characters are important, view reports in `reports/` directory (Markdown files display correctly in editors).

**Verification:** Run any command and confirm content is correct despite any `?` substitutions.

---

## §6 — GUI tab is empty / "No Data Available"

**Phenomenon:** A GUI tab shows "No Data Available" or an empty state message.

**Cause:** The corresponding command has not been run yet, or results are from a different date.

**Can ignore?** Yes. Empty state is expected until data is populated.

**Fix:** Follow the next_steps shown in the empty state widget. Typically:
```bash
python main.py run-research --mode real --profile standard
# Then refresh the GUI tab
```

**Verification:** After running the command, click the tab's Refresh button (if available) or reopen the cockpit.

---

## §7 — PySide6 not installed / GUI won't open

**Phenomenon:** `python main.py cockpit` fails with `ModuleNotFoundError: No module named 'PySide6'`.

**Cause:** PySide6 is not installed in the Python environment.

**Can ignore?** Yes for CLI-only use. No if GUI is required.

**Fix:**
```bash
pip install PySide6
```

**Verification:**
```bash
python -c "import PySide6; print(PySide6.__version__)"
python main.py cockpit --mode real
```

---

## §8 — GUI shows blank/grey screen

**Phenomenon:** Cockpit opens but tabs are blank or show a grey rectangle.

**Cause:** A GUI panel raised an exception during initialization, or PySide6 rendering issue.

**Can ignore?** Usually. Check the terminal for error output.

**Fix:**
1. Check terminal for `ImportError` or traceback after opening the GUI
2. Run `python main.py usability-smoke-test` to identify which panel is failing
3. If a specific panel import fails, the tab is disabled; CLI commands still work

---

## §9 — update-data returns 0 rows

**Phenomenon:** `[update-data] daily_price: OK (0 rows)` — no data fetched.

**Cause:** Provider API returned empty response. Possible causes:
- Market was closed (holiday, weekend)
- Token invalid or rate-limited
- Network timeout

**Can ignore?** Yes if market was closed. Investigate if market was open.

**Fix:**
1. Confirm market was open on the target date
2. Check `python main.py provider-health`
3. Try `python main.py fetch-provider --provider finmind --dataset daily_price`
4. Check FinMind API status

---

## §10 — Smoke test shows FAIL for a CLI test

**Phenomenon:** `python main.py usability-smoke-test` shows FAIL status for a test.

**Cause:** A CLI command returned a non-zero exit code for a reason other than token configuration.

**Can ignore?** Depends on the test. Token-related failures are WARN (can_ignore=True).

**Fix:**
1. Note the test name and run the command manually
2. Read the error output carefully
3. Check if it is a data issue, token issue, or code issue

---

## §11 — Backtest Readiness Score capped at 60

**Phenomenon:** Backtest Readiness shows ≤ 60 with a `MOCK_CONTAMINATION` note.

**Cause:** Mock data files are present alongside real data files. The gate detected contamination.

**Can ignore?** Yes for research. Capped score reflects reduced confidence in backtest accuracy.

**Fix:**
1. Run with `--mode mock` if intentionally using mock data
2. If using real data, check that `data/` directory does not contain mock-generated files
3. Clean mock data: remove any files with `mock` in the filename from the data directories

---

## §12 — Signal quality recommendations not updating

**Phenomenon:** Signal Quality tab or report shows the same BOOST/KEEP/REDUCE as yesterday.

**Cause:** `run-research` or `signal-quality` was not run today, or report is cached.

**Fix:**
```bash
python main.py run-research --mode real --profile standard
```

Then refresh the GUI tab or check `reports/auto_report_center/YYYY-MM-DD/` for today's date.

---

## §13 — Portfolio simulation shows NaN or extreme values

**Phenomenon:** Sharpe, MaxDD, or Profit Factor shows NaN, inf, or an extreme value (e.g., Sharpe = 999).

**Cause:** Insufficient trade history, all trades are winners/losers, or a data quality issue.

**Can ignore?** Investigate before using the values.

**Fix:**
1. Check `data-quality-gate` — low coverage or mock contamination can cause this
2. Check the trade log in Portfolio Cockpit — are there enough trades?
3. Run with a broader date range if data allows

---

## Getting More Help

- Check [User Guide](user_guide.md) for score interpretation
- Check [CLI Reference](cli_reference.md) for command details
- Check [Safety & Limitations](safety_and_limitations.md) for known limitations
- Run `python main.py usability-smoke-test --report` for a full diagnostic

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
