# TW Quant Cockpit Troubleshooting Guide v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Import Errors

**Symptom:** `ImportError: No module named 'xxx'`
**Cause:** Missing Python package or module not found in path
**Resolution:**
- Ensure you are running from the project root: `C:/Users/Rossi/Documents/Claude/trading_master`
- Check the module exists in the package directory
- Run `python -c "import xxx; print('OK')"` to test

---

## cp950 Encoding Warning

**Symptom:** `UnicodeDecodeError` or `cp950 encoding` warning in console
**Cause:** Windows terminal default encoding (cp950) conflicts with subprocess output
**Classification:** KNOWN_CP950_WARNING — non-critical
**Resolution:** Non-critical. The system continues to work. Set `PYTHONIOENCODING=utf-8` if desired.

---

## paper_state.json Missing

**Symptom:** WARN about `paper_state.json not found`
**Cause:** Paper trading state file not yet created
**Classification:** KNOWN_PAPER_SMOKE_WARNING — non-critical
**Resolution:** Run `python main.py paper` once to create the state file.

---

## ENV_LIMITED Report Status

**Symptom:** Report shows `ENV_LIMITED` status
**Cause:** Data source not available in current environment (no live data, no API token)
**Classification:** KNOWN_REPORT_PACK_OPTIONAL — non-critical
**Resolution:** Normal behavior. ENV_LIMITED reports are optional and do not count as failures.

---

## No Data Available in GUI

**Symptom:** Tab shows "No data available"
**Cause:** Corresponding CLI command has not been run yet
**Resolution:** Run the CLI command for that module:
```
python main.py strategy-lab-dashboard --mode real
python main.py strategy-validation --mode real
python main.py evidence-graph --mode real
```

---

## GUI Does Not Start

**Symptom:** `python main.py cockpit` fails
**Cause:** PySide6 not installed or display not available
**Resolution:**
- Install PySide6: `pip install PySide6`
- On headless servers, use CLI commands instead of GUI

---

## Safety Scan Shows BLOCKED

**Symptom:** `python main.py safety-scan --target all` shows BLOCKED files
**Cause:** File contains forbidden trading keywords outside whitelist
**Resolution:**
- Review the blocked file(s)
- Ensure forbidden keywords are inside whitelisted phrases
- Add appropriate whitelist phrases if the content is legitimately safe

---

## Regression Suite Failures

**Symptom:** `regression-run --suite release_gate` shows FAIL
**Cause:** A module import, CLI command, or smoke test failed
**Resolution:**
- Check the specific failing test name
- Run that CLI command manually to see the error
- Fix the underlying issue

---

## Version Mismatch

**Symptom:** `version_info_v100` check fails
**Cause:** VERSION in version_info.py does not start with "1.0."
**Resolution:**
- Check `release/version_info.py` VERSION constant
- Ensure it follows `1.0.x` format

---

## Strategy Always INSUFFICIENT

**Symptom:** All strategies show INSUFFICIENT grade
**Cause:** Not enough backtest or replay data
**Resolution:**
- Run more backtests for the strategy
- Run replay training sessions
- Collect more journal entries
- This is normal for newly added strategies — wait for data to accumulate

---

## Research Cockpit Stable Shows WARN

**Symptom:** `research-cockpit-stable` overall status is WARNING
**Cause:** One or more checks returned WARN
**Classification:** Expected if known WARNs present
**Resolution:**
- Review which checks returned WARN
- Known WARNs (cp950, paper_state, ENV_LIMITED) are acceptable
- Unknown WARNs should be investigated

---

## Docs Health Check WARN

**Symptom:** `docs-health-check` shows missing docs
**Cause:** Expected v1.0.5 documentation files not created yet
**Resolution:** Create the missing files per the v1.0.5 specification.

---

*TW Quant Cockpit v1.0.5 — Documentation & User Guide Polish — Research Only — Not Investment Advice*
