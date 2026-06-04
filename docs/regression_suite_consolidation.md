# Regression Suite Consolidation — TW Quant Cockpit v0.5.3

> **[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

---

## v0.5.3 目標 (Goals)

Consolidate all regression tests scattered across `release/regression_suite.py` and
`release/stable_release_checklist.py` into a unified, named-suite system with:

- Named test suites: quick / full / gui / report / safety / data / strategy / replay / research_os / release_gate
- Coverage matrix for all 23 known modules
- Regression runner with safe subprocess execution (no shell=True)
- Regression store (CSV persistence)
- Regression consolidation Markdown report
- GUI panel (RegressionSuitePanel)
- 4 new CLI commands

---

## Why Consolidation Was Needed

Before v0.5.3:
- Tests were spread across `release/regression_suite.py` (inline test methods)
- No ability to run a named subset of tests (e.g. "only GUI tests", "only data tests")
- No coverage matrix showing which modules are tested vs untested
- No unified Markdown report

After v0.5.3:
- All suites defined declaratively in `RegressionSuiteRegistry`
- Runner uses subprocess (no shell=True) with timeout and forbidden keyword guard
- Coverage matrix auto-generated from suite contents
- Consolidation report saved to `reports/regression_consolidation_report_YYYY-MM-DD.md`

---

## Suite Descriptions

| Suite | Tests | Description |
|-------|-------|-------------|
| `quick` | 11 | Fast smoke tests: version-info, summaries, cli-list, etc. |
| `full` | ~40 | All suites combined (quick + data + strategy + replay + research_os + report) |
| `gui` | 10 | GUI panel import checks via `python -c "import gui.xxx"` |
| `report` | 10 | Report generation: auto-report, strategy-filter, research-os-report, etc. |
| `safety` | 6 | Safety checks: stable-release-check, no_real_orders flag, safe command registry |
| `data` | 6 | Data layer: data-quality-gate, provider-health, api-fetch-diagnostics, compileall |
| `provider` | 6 | Alias for data suite |
| `strategy` | 7 | Strategy layer: strategy-filter, rule-governance, signal-quality, ML knowledge |
| `replay` | 6 | Intraday replay: intraday-replay, replay-session-list, intraday-pipeline |
| `research_os` | 9 | Research OS: audit, summary, modules, cli, gui, safety, workflow, coach, review |
| `release_gate` | ~28 | Release gate = data + quick + safety + gui + report smoke |

---

## Coverage Matrix

The coverage matrix checks 23 modules across 7 dimensions:

- **CLI covered**: CLI command present in quick/data/strategy/replay/research_os suite
- **GUI covered**: GUI import test present in gui suite
- **Report covered**: Report generation test present in report suite
- **Safety covered**: Safety check present in safety suite
- **Data covered**: Data check present in data suite
- **Strategy covered**: Strategy check present in strategy suite
- **Replay covered**: Replay check present in replay suite

Coverage score = (covered dimensions / 7) × 100%.

---

## required vs optional Tests

- `required=True` (default): `returncode != 0` → STATUS_FAIL → overall suite FAIL
- `required=False`: `returncode != 0` → STATUS_WARNING → overall suite WARNING (not FAIL)

Examples of optional tests:
- `quick_paper` (paper trading smoke test)
- `safety_safe_command_registry` (checks CLIAliasMap.blocked_keywords, may not exist)
- `gui_regression_suite_panel_import` (v0.5.3 new panel, PySide6 optional)

---

## Flaky / Timeout Handling

- Each test has a `timeout_seconds` field (default 60s)
- On `subprocess.TimeoutExpired` → STATUS_TIMEOUT
- Timeout tests count as warnings (not failures) unless they are required
- `RegressionRunner` has a global `timeout_seconds=180` override

---

## CLI Usage Examples

```bash
# List all suites
python main.py regression-list-suites

# Run the quick suite
python main.py regression-run --suite quick

# Run the safety suite
python main.py regression-run --suite safety

# Show coverage matrix
python main.py regression-coverage

# Generate consolidation report
python main.py regression-report --mode real

# Legacy (still works)
python main.py regression-suite
python main.py regression-suite --full
```

---

## GUI Usage

1. Launch cockpit: `python main.py cockpit`
2. Open the **Regression Suite** tab (in release_qa group)
3. Click **Run Quick Suite** for a fast smoke test
4. Click **Run Safety Suite** for safety checks
5. View test results in the table (green=PASS, red=FAIL, yellow=WARNING)
6. View coverage matrix in the right panel
7. Click **Generate Report** to save a Markdown report

---

## Safety Declaration

- **Regression Only** — All tests are regression/smoke tests only
- **Research Only** — No production trading, no broker API
- **No Real Orders** — `no_real_orders=True` on all RegressionTestCase instances
- **No Broker Execution** — Forbidden keywords: buy, sell, order, submit_order, broker, shioaji
- **No Auto Trading** — `production_blocked=True` on all classes
- **Safe Subprocess** — `shell=False` on all subprocess.run calls
- **No Token Leak** — No credentials in test commands

---

## Package Structure

```
regression/
    __init__.py                  # Package exports
    regression_schema.py         # RegressionTestCase, RegressionTestResult dataclasses
    suite_registry.py            # RegressionSuiteRegistry with all suite builders
    regression_runner.py         # RegressionRunner (subprocess, no shell=True)
    coverage_matrix.py           # RegressionCoverageMatrix
    regression_store.py          # CSV persistence (results, summary, coverage)

reports/
    regression_consolidation_report.py  # 7-section Markdown report generator

gui/
    regression_suite_panel.py    # QWidget GUI panel (PySide6)
    regression_suite_adapter.py  # Non-GUI adapter (no PySide6 dependency)
```

---

*TW Quant Cockpit v0.5.3 — Regression Suite Consolidation — Research Only — Not Investment Advice*
