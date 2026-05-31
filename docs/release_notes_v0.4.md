# TW Quant Cockpit — Release Notes v0.4

> [!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.

---

## v0.4.0 — Research Platform Stable Release

**Status:** Current

### Summary

v0.4.0 consolidates all v0.3.x features into a verified, regression-tested, documented stable research platform. No new strategies. No production trading. Research only.

### New Files

- `release/__init__.py` — package init
- `release/version_info.py` — `VersionInfo` class; version=v0.4.0; `get_version_info()`, `print_version_info()`, `get_safety_banner()`, `get_feature_summary()`
- `release/stable_release_checklist.py` — `StableReleaseChecklist`: 18-item checklist (compileall, import health, GUI health, workflow, quality gate, provider reliability, intraday, backtest, rule governance, experiment registry, auto report, usability, paper, mock realtime, git safety, artifact ignore, token leak, real order check)
- `release/regression_suite.py` — `RegressionSuite`: quick (7 tests) + full (14 tests) suites; writes CSV; PASS/PARTIAL/FAIL status
- `reports/stable_release_report.py` — `StableReleaseReportBuilder`: 7-section Markdown report
- `gui/release_status_panel.py` — `ReleaseStatusPanel`: PySide6 GUI with version cards, feature coverage table, regression table, actions; QThread workers
- `gui/release_status_adapter.py` — `ReleaseStatusAdapter`: GUI bridge
- `docs/release_v0.4.0.md` — release overview documentation
- `docs/release_checklist.md` — manual release checklist
- `docs/release_notes_v0.4.md` — this file

### Modified Files

- `main.py` — 4 new CLI commands: `version-info`, `stable-release-check`, `regression-suite`, `stable-release-report`
- `gui/dashboard.py` — guarded import + "Release Status" tab
- `README.md` — updated to v0.4.0 as current version
- `docs/roadmap.md` — v0.4.0 marked Done; v0.4.1 API Fetch Productionization planned
- `docs/index.md` — added release_v0.4.0.md, release_checklist.md, release_notes_v0.4.md
- `.gitignore` — stable_release report artifacts excluded

### Safety

- `read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False` in all new classes
- No broker connections. No auto weight apply. No real orders.
- Token leak check in StableReleaseChecklist — BLOCKED status if any token found hardcoded

### Stable Features (from v0.3.x)

All 15 major features verified and regression-tested. See `docs/release_v0.4.0.md` for full feature table.

---

*Previous release notes: see `docs/release_notes_v0.3.md`*
