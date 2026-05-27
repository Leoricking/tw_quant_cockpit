# Data Provider Roadmap — TW Quant Cockpit

## Overview

Starting from v0.3.4, TW Quant Cockpit no longer hard-codes XQ as the sole
data source.  All data access goes through a **provider abstraction layer**
(`data/providers/`).  This allows the system to switch or extend data sources
without touching analysis, model, or report code.

---

## Provider Status (v0.3.4)

| Provider | Status | Module | Notes |
|---|---|---|---|
| **CSV** | **Active** | `csv_provider.py` | Reads `data/import/` standard CSVs. Primary provider. |
| **XQ Export** | **Transition** | `xq_export_provider.py` | Wraps XQ-imported data. Delegates to CSV. |
| TWSE OpenAPI | Planned (v0.4) | `twse_openapi_provider.py` | TWSE / TPEx / MOPS public API. |
| Mega API | Planned (v0.4+) | `mega_provider.py` | Chiao-Tung Securities read-only API. |

**Real order execution: PERMANENTLY DISABLED across all providers.**

---

## Architecture

```
CLI / Pipeline / Report / Dashboard
         │
         ▼
  BaseMarketDataProvider (interface)
         │
  ┌──────┼──────────────┬──────────────┐
  │      │              │              │
CSVProvider  XQExportProvider  TWSEOpenAPIProvider  MegaProvider
  │                              (planned)        (planned)
  │
RealDataLoader (data/real_data_loader.py)
  │
data/import/*.csv
```

---

## Phase 1 — v0.3.4 (Current)

**Goal:** Decouple analysis logic from XQ.

- `CSVProvider` is the active provider.
- `XQExportProvider` is a transition wrapper — once users import XQ files via
  `import-xq-export`, the data lives in `data/import/` and is served by both
  `CSVProvider` and `XQExportProvider`.
- `TWSEOpenAPIProvider` and `MegaProvider` are skeletons with no active
  connection.
- `BaseMarketDataProvider` defines the interface all future providers must
  implement.

---

## Phase 2 — v0.4 (Planned)

**Goal:** Replace XQ as the core data source with public APIs.

### TWSE / TPEx Open API
- Daily OHLCV: `https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY`
- No authentication required.
- Rate limit: respect public API fair-use policy.

### MOPS (月營收 / 基本面)
- Monthly revenue: `https://mops.twse.com.tw/`
- **Important:** Must use `announcement_date` (not `month_end_date`) to avoid
  forward-looking leakage in backtests.
- Typical disclosure delay: 10th of the following month.

### data.gov.tw
- Company profiles, industry classifications, open datasets.

### Mega API (兆豐證券) — Read-Only
- Real-time quote, 5-level bid/ask, tick stream, intraday bars.
- **No order submission.** Read-only interface only.
- Credentials managed via `.env` (never committed to git).

---

## Phase 3 — v0.5+ (Future)

- XQ is fully optional / deprecated as a data source.
- All data flows through TWSE / Mega API.
- Intraday tick data enables proper microstructure features.
- Paper trading feedback loop using live intraday data.

---

## XQ Role After v0.4

XQ (`import-xq-export` command) transitions from **core data source** to
**optional backup / manual import tool**.

Use cases where XQ remains useful:
- Importing historical data for stocks not covered by public APIs.
- Cross-checking data quality.
- One-off manual analysis.

XQ is **not** used for:
- Automated daily pipeline (replaced by TWSE API).
- Real-time signals (replaced by Mega API).
- Model training data (replaced by standardised CSV / API pipeline).

---

## Data Leakage Prevention

| Risk | Prevention |
|---|---|
| Revenue data before announcement | Use `announcement_date` field (TODO in v0.4) |
| API data timestamp mismatch | Log and warn when date alignment is uncertain |
| Provider cache stale data | Cache TTL + cache invalidation on import |
| Intraday data for daily backtest | Feature pipeline uses only T-day data for T+1 prediction |

---

## Provider Interface Reference

```python
class BaseMarketDataProvider:
    name: str
    is_available: bool
    is_planned: bool

    def get_daily(symbol, start=None, end=None) -> DataFrame | None
    def get_intraday(symbol, date=None) -> DataFrame | None
    def get_ticks(symbol, date=None) -> DataFrame | None
    def get_bidask(symbol) -> dict | None
    def get_institutional(symbol, start=None, end=None) -> DataFrame | None
    def get_margin(symbol, start=None, end=None) -> DataFrame | None
    def get_monthly_revenue(symbol, months=24) -> DataFrame | None
    def get_holder(symbol) -> DataFrame | None
    def get_trust_cost(symbol) -> DataFrame | None
    def get_profile(symbol) -> dict | None
    def health_check() -> dict
```

Missing data always returns `None`.  Providers never crash the system.

---

*Last updated: v0.3.4*
