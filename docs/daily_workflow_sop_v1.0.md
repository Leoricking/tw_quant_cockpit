# TW Quant Cockpit Daily Workflow SOP v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Before Market Open

1. Run version check:
   ```
   python main.py version-info
   ```

2. Run system health:
   ```
   python main.py research-cockpit-stable --mode real
   ```

3. Check strategy dashboard:
   ```
   python main.py strategy-lab-dashboard --mode real
   ```

4. Review daily report:
   ```
   python main.py report-pack --type daily --mode real
   ```

---

## During Market Hours

- Review strategy validation scores: `python main.py strategy-validation-summary`
- Check crash reversal conditions if relevant: `python main.py crash-reversal-summary`
- Review evidence graph for contradictions: `python main.py evidence-graph-summary`
- All actions are research and review only — no real trading

---

## After Market Close

1. Run full strategy dashboard:
   ```
   python main.py strategy-lab-dashboard --mode real
   ```

2. Update evidence graph:
   ```
   python main.py evidence-graph --mode real
   ```

3. Run data hygiene check:
   ```
   python main.py data-report-hygiene-summary --mode real
   ```

4. Generate weekly report (on Fridays):
   ```
   python main.py report-pack --type weekly --mode real
   ```

---

## Weekend Review

1. Run full report pack:
   ```
   python main.py report-pack --type full --mode real
   ```

2. Run regression suite:
   ```
   python main.py regression-run --suite release_gate --mode real
   ```

3. Run stable checklist:
   ```
   python main.py research-cockpit-stable --mode real
   ```

4. Review strategy memories validation queue:
   ```
   python main.py strategy-memory-validation-queue
   ```

---

## Monthly Check

1. Run safety scan:
   ```
   python main.py safety-scan --target all
   ```

2. Run documentation health check:
   ```
   python main.py docs-health-check
   ```

3. Run stable v0.6.0 check:
   ```
   python main.py stable-v060-check --mode real
   ```

---

## When WARN Appears

- WARN is non-critical — the system continues to operate
- Known WARNs: cp950 encoding, paper_state.json missing, ENV_LIMITED reports
- Investigate unknown WARNs in reports
- Do not force-pass WARNs without understanding them

---

## When Data Is Insufficient

- Status INSUFFICIENT is normal for new strategies
- Add more backtest data: `python main.py regression-run --suite full --mode real`
- Practice replay: `python main.py intraday-replay --mode real`
- Insufficient data does NOT mean the strategy is wrong — just needs more evidence

---

## When CONFLICTED Status Appears

- CONFLICTED means multiple evidence sources disagree
- Review the evidence graph: `python main.py evidence-graph --mode real`
- Review each evidence source independently
- Do NOT force-resolve CONFLICTED — investigate first
- CONFLICTED is a research finding, not an error

---

## When Too Many Reports Accumulate

- Run data hygiene: `python main.py data-report-hygiene-summary --mode real`
- Review stale files list
- Archive suggestions only — no automatic deletion

---

## When GUI Freezes

- Wait for QThread operation to complete
- If unresponsive after 2 minutes, close and reopen
- Run the corresponding CLI command instead
- GUI freeze does not indicate data corruption

---

## What NOT to Do

- Do NOT chain CLI commands with `&&` or `;`
- Do NOT use `git add .` for commits
- Do NOT commit runtime outputs (.csv, .json, .md reports, .db)
- Do NOT interpret VALIDATED as trading-ready
- Do NOT act on research outputs as investment advice
- Do NOT connect any broker API to this system

---

*TW Quant Cockpit v1.0.5 — Documentation & User Guide Polish — Research Only — Not Investment Advice*
