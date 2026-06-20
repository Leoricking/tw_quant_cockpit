# MOPS Provider v1.4.2

**Release:** v1.4.2 MOPS Provider
**Base Release:** v1.4.1 TPEx Provider
**Safety:** Research Only. No Real Orders. No Broker. No Auto Download. Not Investment Advice.

---

## Overview

The MOPS Provider adds official Market Observation Post System (公開資訊觀測站) financial disclosure
data access to TW Quant Cockpit. MOPS is the primary source for listed company financial disclosures
in Taiwan, operated by the TWSE.

**Data domain:** Financial disclosure (not market price data).
**Provider ID:** `mops_official`
**Official source only:** YES. No mock fallback in real mode.

---

## Safety Invariants

- `NO_REAL_ORDERS = True` — hardcoded, never changes
- `BROKER_EXECUTION_ENABLED = False` — hardcoded, never changes
- `PRODUCTION_TRADING_BLOCKED = True` — hardcoded, never changes
- `MOPS_MOCK_FALLBACK_ENABLED = False` — hardcoded, never changes
- `MOPS_AUTO_DOWNLOAD_ENABLED = False` — hardcoded, never changes
- `MOPS_REALTIME_AVAILABLE = False` — MOPS publishes after filing deadline, not real-time
- `MOPS_BROKER_EXECUTION_AVAILABLE = False` — hardcoded, never changes
- `OFFICIAL_SOURCE_ONLY = True` — hardcoded, never changes

These invariants appear in every module docstring and are tested by 12 safety checks in the health check.

---

## Architecture

### Module Structure (`data/providers/mops/`)

| Module | Description |
|--------|-------------|
| `__init__.py` | Safety constants and package identity |
| `models_v142.py` | All dataclasses and enums |
| `capabilities_v142.py` | MOPSCapabilityMatrix — 13 capabilities |
| `endpoints_v142.py` | MOPSEndpointRegistry — 10 POST/GET endpoints |
| `client_v142.py` | MOPSHttpClient — GET + POST form, maintenance detection |
| `parser_v142.py` | MOPSParser — HTML table parsing, charset detection, ROC date |
| `normalizer_v142.py` | MOPSNormalizer — units, markets, periods, amounts |
| `company_profile_v142.py` | MOPSCompanyProfileFetcher — market conflict detection |
| `monthly_revenue_v142.py` | MOPSMonthlyRevenueFetcher — revision detection |
| `financial_reports_v142.py` | MOPSFinancialReportFetcher |
| `balance_sheet_v142.py` | MOPSBalanceSheetParser — balance check (tolerance 1.0) |
| `income_statement_v142.py` | MOPSIncomeStatementParser |
| `cash_flow_v142.py` | MOPSCashFlowParser — mismatch check (tolerance 1.0) |
| `equity_statement_v142.py` | MOPSEquityStatementIndex |
| `material_information_v142.py` | MOPSMaterialInformationFetcher — correction detection |
| `investor_conference_v142.py` | MOPSInvestorConferenceFetcher |
| `xbrl_index_v142.py` | MOPSXBRLIndexFetcher — taxonomy detection |
| `revision_lineage_v142.py` | MOPSRevisionLineageService |
| `point_in_time_v142.py` | MOPSPointInTimeService — injectable clock |
| `derived_metrics_v142.py` | MOPSDerivedFinancialMetrics |
| `cache_policy_v142.py` | MOPSCachePolicy — real/mock isolation |
| `store_v142.py` | MOPSStore |
| `query_v142.py` | MOPSQueryService |
| `provider_v142.py` | MOPSProviderV142 — main provider class |
| `health_v142.py` | MOPSProviderHealthCheck — 35 offline checks |

### Key Architectural Differences from TWSE/TPEx

MOPS uses **POST form submissions** and returns **HTML table responses** (not JSON APIs).

| Aspect | TWSE/TPEx | MOPS |
|--------|-----------|------|
| HTTP method | GET | POST (form) + GET (XBRL) |
| Response format | JSON | HTML tables |
| Charset | UTF-8 | Big5 or UTF-8 (auto-detected) |
| Maintenance detection | N/A | Detects 系統維護 keyword |
| Data type | Market price | Financial disclosure |
| ROC year | N/A | Used throughout (YYY + 1911 = CE) |

---

## Capabilities (13)

| Capability | Status |
|-----------|--------|
| COMPANY_PROFILE | Supported |
| MONTHLY_REVENUE | Supported |
| FINANCIAL_REPORT_FILING | Supported |
| BALANCE_SHEET | Supported |
| INCOME_STATEMENT | Supported |
| CASH_FLOW_STATEMENT | Supported |
| EQUITY_STATEMENT | Supported |
| MATERIAL_INFORMATION | Supported |
| INVESTOR_CONFERENCE | Supported |
| XBRL_DOCUMENT | Supported |
| REVISION_LINEAGE | Supported |
| POINT_IN_TIME | Supported |
| DERIVED_METRICS | Supported |

Not supported (MOPS is financial disclosure, not market data):
- DAILY_OHLCV, MARGIN_TRADING, INDEX_DATA, INSTITUTIONAL_FLOW, REALTIME_QUOTE

---

## Data Models

All models implement `to_dict()` and `from_dict()`. Missing values are `None`, never `0` or `""`.
Forward-compatible: `from_dict()` ignores unrecognized fields.

### Key enums

- `MOPSCapability` — 13 values
- `MOPSFetchStatus` — 11 values including `MAINTENANCE`, `REVISION_DETECTED`, `MARKET_CONFLICT`
- `MOPSDocumentType` — BALANCE_SHEET, INCOME_STATEMENT, CASH_FLOW, EQUITY_STATEMENT
- `MOPSReportPeriod` — Q1, Q2, Q3, Q4, ANNUAL, MONTHLY
- `MOPSMarket` — TWSE, TPEX, MOPS, UNKNOWN

---

## Financial Validation

### Balance Sheet Check

```
is_balanced = abs(total_assets - (total_liabilities + total_equity)) <= 1.0
```

Tolerance: 1.0 (TWD thousands) to handle rounding in published data.

### Cash Flow Mismatch Check

```
expected = operating_cash_flow + investing_cash_flow + financing_cash_flow
is_mismatch = abs(expected - net_change_in_cash) > 1.0
```

FCF = operating_cash_flow - abs(capex)

---

## Point-in-Time Availability

Filing deadlines (data is only "available" after these dates):

| Period | Available After |
|--------|----------------|
| Q1 | May 15 of same year |
| Q2 | August 14 of same year |
| Q3 | November 14 of same year |
| Q4 / Annual | March 31 of next year |
| Monthly Revenue | Day 10 of the following month |

The `MOPSPointInTimeService` accepts an injectable `clock` parameter for deterministic testing.

---

## XBRL Taxonomy

Financial industry codes (`_FINANCIAL_INDUSTRY_CODES = {"M", "N", "K", "I", "J"}`):
- Use `financial_industry` taxonomy (XBRL schema)

All other industry codes:
- Use `general_industry` taxonomy

---

## Cache Key Isolation

Real data: `mops:real:{endpoint_id}:{symbol}:{fiscal_period}:{sha256[:16]}`
Mock data: `mops:mock:{endpoint_id}:{symbol}:{fiscal_period}:{sha256[:16]}`

Real and mock data are always in separate namespaces.

---

## CLI Commands

```
python main.py mops-health
python main.py mops-endpoints
python main.py mops-capabilities
python main.py mops-company-profile --symbol 2330
python main.py mops-revenue --symbol 2330 --year-month 2024-01
python main.py mops-balance-sheet --symbol 2330
python main.py mops-income-statement --symbol 2330
python main.py mops-cash-flow --symbol 2330
python main.py mops-material-info --symbol 2330
python main.py mops-investor-conference --symbol 2330
python main.py mops-xbrl-index --symbol 2330
python main.py mops-revision-lineage --symbol 2330
python main.py mops-point-in-time --symbol 2330 --period Q2
python main.py mops-derived-metrics --symbol 2330
python main.py mops-coverage
python main.py mops-cache-status
python main.py mops-provider-report
```

---

## Test Coverage

212 tests in `tests/test_mops_provider_v142.py`, organized in 21 test classes.
All tests are offline (no network required).
Fixtures: `tests/fixtures/mops_provider/` (22 files).

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
*[!] Official MOPS Public Disclosure Data Only.*
*[!] No Mock Fallback. No Auto Download. No Broker.*
