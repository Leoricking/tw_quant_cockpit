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

## v0.4.1 — API Fetch Productionization

**Status:** Current

### Summary

v0.4.1 adds a production-grade, read-only API data fetch layer on top of the stable v0.4.0 platform. Retry, cache, lineage, parser hardening, token safety — all read-only. No new strategies. No real orders.

### New Files

- `data/providers/token_setup_assistant.py` — `TokenSetupAssistant`: reads .env; masks tokens; never modifies .env
- `data/providers/retry_policy.py` — `RetryPolicy`: exponential backoff for safe fetches only; never used for orders
- `data/providers/api_cache.py` — `APICache`: SHA-256 keyed provider cache in `data_cache/api/`; TTL=24h
- `data/providers/data_lineage.py` — `DataLineageTracker`: LIN-XXXX IDs; masked URLs; CSV export
- `data/providers/api_diagnostics.py` — `APIFetchDiagnostics`: per-provider/dataset result aggregation; sanitized output
- `data/providers/twse_tpex_parser.py` — `TWSETPEXParser`: alias mapping, ROC year, comma numerics, schema status
- `data/providers/mops_financial_parser.py` — `MOPSFinancialParser`: estimated announcement dates, timing_quality
- `reports/api_fetch_production_report.py` — `APIFetchProductionReportBuilder`: 8-section Markdown report
- `gui/api_fetch_status_adapter.py` — `APIFetchStatusAdapter`: GUI bridge; lazy imports; no full token
- `gui/api_fetch_status_panel.py` — `APIFetchStatusPanel`: PySide6 GUI with QThread workers; safety banner
- `docs/api_fetch_productionization.md` — full documentation

### Modified Files

- `main.py` — 5 new CLI commands: `api-token-check`, `api-cache-status`, `api-fetch-diagnostics`, `api-cache-cleanup`, `api-fetch-production-report`
- `gui/dashboard.py` — guarded import + "API Fetch Status" tab
- `data/providers/provider_health.py` — `run_all()` adds `v041_components` availability dict
- `reports/auto_report_center.py` — `include_api_fetch_production` flag; `run_api_fetch_production_report()` method
- `release/regression_suite.py` — 3 new v0.4.1 tests added to full suite (api_fetch_imports, api_token_check, api_cache_stats)
- `release/stable_release_checklist.py` — 2 new v0.4.1 checks (api_token_safety, api_cache_ignored)
- `docs/roadmap.md` — v0.4.1 marked Done; v0.4.2 ML Feature Store planned
- `docs/index.md` — added api_fetch_productionization.md
- `.gitignore` — API fetch report and lineage artifacts excluded

### Safety

- `read_only=True`, `no_real_orders=True` in all new classes
- Tokens always masked; never committed; never displayed in full
- Cache keys never contain full token (SHA-256 of sanitized params)
- Lineage URLs masked (token query params replaced with ****)
- Production Trading: BLOCKED
- REAL_ORDER_READY: False

---

*Previous release notes: see `docs/release_notes_v0.3.md`*
