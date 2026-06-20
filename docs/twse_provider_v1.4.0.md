# TWSE Provider v1.4.0

> **[!] Research Only. No Real Orders. Official Public Data. Not Real-Time. Not Investment Advice.**
> **[!] NO_REAL_ORDERS=True. BROKER_EXECUTION_ENABLED=False. PRODUCTION_TRADING_BLOCKED=True.**
> **[!] TWSE_REALTIME_AVAILABLE=False. TWSE_MOCK_FALLBACK_ENABLED=False. OFFICIAL_SOURCE_ONLY=True.**

---

## Overview

v1.4.0 introduces the official TWSE (Taiwan Stock Exchange) public data provider. This is the first module in the v1.4.x Public Data Provider Integration phase. The provider uses TWSE OpenAPI endpoints (official public data, no auth required) and is fully testable offline via injectable transport.

**Capability:** `twse_provider` — promoted from PLANNED → STABLE in v1.4.0.

---

## Architecture

### Package: `data/providers/twse/`

| Module | Purpose |
|--------|---------|
| `__init__.py` | Safety constants, package marker |
| `models_v140.py` | Enums and dataclasses (TWSESecurity, TWSEDailyBar, TWSEInstitutionalFlow, TWSEMarginRecord, TWSEMarketSummary, TWSEIndexRecord, TWSETradingDay, TWSECorporateActionPreview, TWSEProvenance) |
| `endpoints_v140.py` | TWSEEndpointRegistry with 9 registered endpoints |
| `capabilities_v140.py` | TWSECapabilityMatrix — is_supported(), is_broker_capability() (always False) |
| `client_v140.py` | TWSEHttpClient with injectable transport (url, params) → (status_code, bytes) |
| `parser_v140.py` | TWSEParser — ROC date conversion, OHLC validation, number parsing |
| `normalizer_v140.py` | TWSENormalizer — canonical_symbol(), is_common_stock(), is_etf() |
| `trading_calendar_v140.py` | TWSETradingCalendar — heuristic, always approximate=True, injectable clock |
| `security_master_v140.py` | Security master service |
| `daily_ohlcv_v140.py` | Daily OHLCV service — dry_run=True default |
| `institutional_v140.py` | Institutional flow service |
| `margin_v140.py` | Margin lending/shorting service |
| `market_summary_v140.py` | Market summary service |
| `indices_v140.py` | Index (TAIEX) service |
| `corporate_actions_v140.py` | Corporate actions service |
| `cache_policy_v140.py` | TTL constants, cache key builder (twse:real: / twse:mock: prefixes) |
| `provider_v140.py` | TWSEProviderV140 — provider_id="twse_official", RealDataProviderAdapter compatible |
| `health_v140.py` | TWSEProviderHealthCheck — 25 checks |
| `query_v140.py` | TWSEQueryService — unified query interface |

---

## Safety Constants

```python
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
TWSE_REALTIME_AVAILABLE = False
TWSE_MOCK_FALLBACK_ENABLED = False
OFFICIAL_SOURCE_ONLY = True
```

These constants are present on both the package (`data/providers/twse/__init__.py`) and the panel (`gui/twse_provider_panel.py`).

---

## Key Design Decisions

### Injectable Transport
`TWSEHttpClient` accepts an optional `transport` callable `(url: str, params: dict) -> (int, bytes)`. When provided, the HTTP layer is bypassed entirely — all 126 tests use this pattern so they run offline with zero network calls.

### ROC Date Conversion
TWSE uses Republic of China calendar years (民國年). `TWSEParser.parse_roc_date("1130101")` returns `"2024-01-01"` (adds 1911 to the year component).

### OHLC Validation
In `parse_daily_ohlcv`, any bar where `high < low` is rejected (not returned) and added to a `warnings` list. This prevents silent data corruption.

### Cache Key Isolation
- Real data: `twse:real:<endpoint>:<date>`
- Mock data: `twse:mock:<endpoint>:<date>`

These prefixes prevent mock and real cache entries from ever colliding.

### Trading Calendar (Heuristic)
`TWSETradingCalendar` always sets `approximate=True` on returned `TWSETradingDay` objects. The calendar uses a heuristic (weekdays minus known Taiwan holidays) — it is never authoritative. An injectable clock (`inject_clock(fn)`) supports deterministic testing.

### No Mock Fallback
`TWSE_MOCK_FALLBACK_ENABLED = False`. If the real TWSE endpoint is unavailable, the provider returns an error — it never silently substitutes mock data. This is consistent with the project-wide real-data-only policy.

---

## TWSE Endpoints (v1.4.0)

| Endpoint ID | Official Name | Enabled |
|------------|--------------|---------|
| `security_master_listed` | Listed Securities Master | Yes |
| `daily_ohlcv_all` | Daily Price/Volume All Securities | Yes |
| `institutional_all` | Institutional Investors All Securities | Yes |
| `margin_all` | Margin Lending & Short Selling All | Yes |
| `market_summary` | Market Summary Statistics | Yes |
| `taiex_daily` | TAIEX Daily History | Yes |
| `trading_calendar` | Trading Calendar | Yes |
| `corporate_actions_ex` | Corporate Actions (Ex-Date) | No (disabled) |
| `valuation` | PE/PB Valuation | Yes |

---

## CLI Commands

All commands are dispatched via `main.py`. None connect to the network in test mode.

| Command | Function |
|---------|----------|
| `twse-health` | `cmd_twse_health` |
| `twse-endpoints` | `cmd_twse_endpoints` |
| `twse-capabilities` | `cmd_twse_capabilities` |
| `twse-security-master` | `cmd_twse_security_master` |
| `twse-daily-ohlcv` | `cmd_twse_daily_ohlcv` |
| `twse-institutional` | `cmd_twse_institutional` |
| `twse-margin` | `cmd_twse_margin` |
| `twse-market-summary` | `cmd_twse_market_summary` |
| `twse-index-history` | `cmd_twse_index_history` |
| `twse-corporate-actions` | `cmd_twse_corporate_actions` |
| `twse-trading-calendar` | `cmd_twse_trading_calendar` |
| `twse-coverage-summary` | `cmd_twse_coverage_summary` |
| `twse-cache-policy` | `cmd_twse_cache_policy` |
| `twse-provider-info` | `cmd_twse_provider_info` |
| `twse-query` | `cmd_twse_query` |
| `twse-report` | `cmd_twse_report` |

---

## GUI Panel

`gui/twse_provider_panel.py` — `TWSEProviderPanel` (Tab ID: `twse_provider`, Group: `data`, Priority: `P1`).

The panel uses a `QThread` worker (`_DataWorker`) to load provider health and endpoint data. It includes a `QApplication.instance() is None` guard in both `__init__` and `refresh()` so it can be safely imported in headless/test environments without hanging.

---

## Tests

`tests/test_twse_provider_v140.py` — 126 tests, all offline (zero network calls).

Test fixtures in `tests/fixtures/twse_provider/`:
- `security_master.json`
- `daily_ohlcv.json`
- `daily_ohlcv_missing.json`
- `daily_ohlcv_invalid_ohlc.json`
- `institutional.json`
- `margin.json`
- `market_summary.json`
- `index_history.json`
- `holiday_schedule.json`
- `corporate_actions.json`
- `malformed_response.json`
- `html_error_response.html`

All fixtures carry `TEST_FIXTURE=true`, `DEMO_ONLY=true`, `NOT_REAL_DATA=true`, `NOT_FOR_FORMAL_CONCLUSION=true`.

---

## Version Info Flags (v1.4.0)

New flags added to `release/version_info.py`:

```
PUBLIC_DATA_PROVIDER_INTEGRATION_STARTED = True
TWSE_PROVIDER_AVAILABLE = True
TWSE_REALTIME_AVAILABLE = False
TWSE_MOCK_FALLBACK_ENABLED = False
TWSE_OFFICIAL_SOURCE_ONLY = True
TWSE_BROKER_PROVIDER = False
TWSE_REQUIRES_AUTH = False
TWSE_MOCK_FORMAL_CONCLUSION_ALLOWED = False
TWSE_DRY_RUN_DEFAULT = True
TWSE_OHLC_VALIDATION_ENABLED = True
TWSE_ROC_DATE_CONVERSION_ENABLED = True
TWSE_TRADING_CALENDAR_APPROXIMATE = True
TWSE_CACHE_REAL_PREFIX = "twse:real:"
TWSE_CACHE_MOCK_PREFIX = "twse:mock:"
TWSE_PROVIDER_HEALTH_CHECK_MODULE = "data.providers.twse.health_v140"
```

---

*[!] Research Only. No Real Orders. Official Public Data. Historical Data Is Not Real-Time.*
*[!] No Buy/Sell/Order controls. No Broker Connect. Not Investment Advice.*
