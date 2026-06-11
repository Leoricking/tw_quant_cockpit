# Regression & Release Gate Hardening v1.0.4

> **Research Only** | **No Real Orders** | **Production Trading BLOCKED**
> **Broker Execution Disabled** | **VALIDATED does not enable trading**
> **Not Investment Advice**

---

## v1.0.4 目標 (Goals)

v1.0.4 hardens the regression and release gate infrastructure with:

1. A `regression_hardening` package (safety scanner, release gate health, regression summary classification, encoding utilities)
2. Known warning / known blocked classification — so pre-existing non-critical warnings do not mask real failures
3. Windows cp950 encoding warning detection and classification
4. Expanded safety scanner whitelist to prevent false positives on research-safety phrases
5. 5 new stable checks (research_cockpit_stable_checklist checks 35–39)
6. 5 new stable-v060 checks
7. 1 new intelligence_stable check
8. 16 new release_gate regression test cases
9. CLI commands: `release-gate-health`, `safety-scan`, `regression-hardening-summary`, `regression-hardening-report`

---

## Release Gate Hardening

The `ReleaseGateHealth` class (in `regression_hardening/release_gate_health.py`) checks:

- release_gate suite registered in `regression/suite_registry.py`
- quick suite registered
- `StableReleaseChecklistV060` importable
- Known WARN categories: 4 (cp950, paper smoke, no_real_orders false positive, report_pack optional)
- Known BLOCKED categories: 1 (no_real_orders flag check)
- No Real Orders false positive correctly whitelisted
- paper smoke WARN classified
- cp950 WARN classified
- report_pack optional missing classified

---

## Safety Scanner

`regression_hardening/safety_scanner.py` — `SafetyScanner` class:

### Forbidden Actions (9 patterns)
- BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE, REAL_TRADE, LIVE_TRADE, BROKER_ORDER

### Whitelist Phrases (false-positive prevention)
The following phrases are whitelisted and will NOT trigger BLOCKED status:
- "No Real Orders" — the safety disclaimer
- "Broker Execution Disabled" — safety flag
- "No broker execution" — safety phrase
- "no_real_orders" — Python variable name
- "NO_REAL_ORDERS" — Python constant
- "order count", "order by", "sort order" — data operations
- "execution disabled", "no execution" — safety states
- "VALIDATED does not enable trading" — validation disclaimer
- "No auto trading", "No automatic trading" — safety phrases
- "RESEARCH_ONLY", "[RESEARCH_ONLY]" — research mode markers
- And more — see `WHITELIST_PHRASES` in `safety_scanner.py`

---

## Known Warning Classification

`regression_hardening/regression_summary.py`:

| Classification | Trigger | Action |
|----------------|---------|--------|
| KNOWN_CP950_WARNING | "cp950", "charmap", "UnicodeDecodeError" | WARN — non-critical |
| KNOWN_PAPER_SMOKE_WARNING | "paper_state.json missing" | WARN — non-critical |
| KNOWN_REPORT_PACK_OPTIONAL | "ENV_LIMITED", "NOT_GENERATED" | WARN — non-critical |
| KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE | "no_real_orders flag", "pre-existing check" | WARN — advisory only |

---

## Known Blocked Classification

| Classification | Trigger | Action |
|----------------|---------|--------|
| KNOWN_NO_REAL_ORDERS_FLAG_CHECK | "no_real_orders flag check" | BLOCKED — known pre-existing, not a real failure |
| KNOWN_RESEARCH_ONLY_BLOCK | "research only block", "RESEARCH_ONLY" | BLOCKED — expected |

---

## Windows cp950 Warning

On Windows, subprocess output may produce encoding warnings (cp950, charmap) due to the system default encoding. These are:
- **Non-critical** — the system still functions correctly
- **Classified** as `KNOWN_CP950_WARNING`
- **NOT** counted as unknown failures
- Handled by `regression_hardening/encoding_utils.py` → `is_windows_cp950_warning()`, `mark_cp950_warning_as_known()`

---

## Paper Smoke Warning

When `data/paper_state.json` is missing, the paper trading smoke test produces a WARN. This is:
- **Non-critical** — paper trading initializes with empty state
- **Classified** as `KNOWN_PAPER_SMOKE_WARNING`
- **NOT** counted as unknown failures

---

## No Real Orders False Positive

The phrase "No Real Orders" contains the word "ORDER" (part of BROKER_ORDER pattern). The safety scanner whitelist explicitly prevents this from being flagged:
- "No Real Orders" is in `WHITELIST_PHRASES`
- "no_real_orders" is in `_SAFE_PATTERNS`
- Verified by check 37 in `research_cockpit_stable_checklist` and `_check_no_real_orders_false_positive_guard_v104` in `stable_release_checklist_v060`

---

## CLI Usage

```bash
# Check release gate health
python main.py release-gate-health

# Scan for forbidden actions
python main.py safety-scan --target reports
python main.py safety-scan --target gui
python main.py safety-scan --target docs
python main.py safety-scan --target all

# Regression hardening summary
python main.py regression-hardening-summary

# Generate regression hardening report
python main.py regression-hardening-report --mode real

# Run full release gate regression suite
python main.py regression-run --suite release_gate --mode real
```

---

## Report Usage

The `RegressionHardeningReportBuilder` in `reports/regression_hardening_report.py` generates a Markdown report covering:
- Overview (version, safety flags, hardening flags)
- Release Gate Health (component status)
- Safety Scanner status
- Known Warning Classification table
- Regression Summary status
- Hardening Actions list
- Safety Declaration

Reports are saved to `reports/regression_hardening_report_{date}.md` (excluded from git via `.gitignore`).

---

## Safety Declaration

> **No Real Orders** — This system does not and cannot place real trading actions.
>
> **No broker execution** — There is no connection to any broker API.
>
> **No auto trading** — No automatic trading, no automatic rule weight changes.
>
> **Regression does not enable trading** — Regression checks are research-only.
>
> **VALIDATED does not enable trading** — VALIDATED grade is research-only.
>
> **Not Investment Advice** — Nothing in this system constitutes investment advice.

---

*TW Quant Cockpit v1.0.4 — Regression & Release Gate Hardening — Research Only — Not Investment Advice*
