# Data Freshness Monitor — v1.3.4

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> Auto External Refresh: DISABLED. Auto Repair: DISABLED. Mock Fallback: DISABLED.
> Future timestamp does not count as fresh. Not Investment Advice.

## Overview

Data Freshness Monitor v1.3.4 provides trading-calendar-aware freshness evaluation for all
Taiwan stock market datasets. It tracks staleness, provider SLA compliance, and alert deduplication
without triggering any data refresh, repair, or broker actions.

## Architecture

- `data_freshness/models_v134.py` — Core models: FreshnessRecord, FreshnessPolicy, FreshnessAlert, ProviderSLARecord, DailyFreshnessSummary
- `data_freshness/policy_v134.py` — DataFreshnessPolicyRegistry with default policies for all DatasetTypes
- `data_freshness/evaluator_v134.py` — DataFreshnessEvaluator: evaluate freshness from timestamps
- `data_freshness/scanner_v134.py` — DataFreshnessScanner: scan symbols, tiers, universes
- `data_freshness/sla_monitor_v134.py` — ProviderSLAMonitor: track provider SLA compliance
- `data_freshness/alert_engine_v134.py` — FreshnessAlertEngine: dedup, ack, resolve alerts
- `data_freshness/snapshot_store_v134.py` — FreshnessSnapshotStore: persist runtime state
- `data_freshness/repair_integration_v134.py` — FreshnessRepairIntegration: map to CoverageRepairQueue
- `data_freshness/health_v134.py` — DataFreshnessHealthCheckV134: 20+ health checks
- `data_freshness/report_v134.py` — DataFreshnessReport: text and markdown reports

## Freshness Status Values

| Status | Meaning |
|--------|---------|
| FRESH | Data age within near-stale threshold |
| NEAR_STALE | Data age between 80% and 100% of stale_after |
| STALE | Age exceeds stale_after but not critical_after |
| CRITICALLY_STALE | Age exceeds critical_after |
| NEVER_RECEIVED | No timestamp available |
| FUTURE_TIMESTAMP | Timestamp is in the future (never counts as FRESH) |
| INVALID_TIMESTAMP | Naive or unparseable timestamp |
| MARKET_CLOSED_VALID | Trading day but market not yet open; yesterday's data present |
| NON_TRADING_DAY_VALID | Non-trading day (weekend/holiday); last trading day data present |
| PROVIDER_DELAYED | HTTP 200 but source timestamp stale |
| PROVIDER_UNAVAILABLE | Provider not reachable |
| DEMO_ONLY | Data mode is MOCK/DEMO — not real data |
| BLOCKED | Explicitly blocked |
| UNKNOWN | Status could not be determined |

## Default Policies

| Dataset Type | Stale After | Critical After | Blocks |
|-------------|------------|----------------|--------|
| DAILY_OHLCV | 86400s (1d) | 172800s (2d) | precise_price, backtest, abc |
| INTRADAY_OHLCV | 300s (5m) | 900s (15m) | precise_price |
| QUOTE | 60s | 300s | precise_price |
| INSTITUTIONAL | 86400s | 172800s | backtest |
| MARGIN | 86400s | 172800s | backtest |
| MONTHLY_REVENUE | 2592000s (30d) | 5184000s (60d) | backtest |
| FINANCIAL_STATEMENT | 7776000s (90d) | 15552000s (180d) | backtest |
| SHAREHOLDER_DISTRIBUTION | 604800s (7d) | 1209600s (14d) | — |
| ETF_CONSTITUENTS | 86400s | 172800s | — |
| CORPORATE_ACTIONS | 2592000s | 5184000s | backtest |
| TECHNICAL_INDICATORS | 86400s | 172800s | abc |
| PROVIDER_HEALTH | 3600s (1h) | 7200s (2h) | — |
| CACHE_ENTRY | 3600s | 7200s | — |

## CLI Commands

```
freshness-health                    Run v1.3.4 health check
freshness-status                    Show overall freshness status
freshness-show --symbol 2330        Show symbol freshness details
freshness-scan --symbol 2330        Scan freshness
freshness-scan --tier core          Scan a tier
freshness-scan --dataset DAILY_OHLCV Scan a dataset type
freshness-summary                   Show freshness summary
freshness-alerts                    Show active alerts
freshness-alert-show --alert-id X   Show alert details
freshness-alert-ack --alert-id X    Acknowledge alert
freshness-alert-resolve --alert-id X Resolve alert
provider-sla-status                 Show provider SLA status
provider-sla-show --provider X      Show provider SLA details
freshness-create-repair             Preview repair candidates
```

## Safety Rules

1. Future timestamps are NEVER classified as FRESH
2. Naive (timezone-unaware) timestamps produce INVALID_TIMESTAMP
3. Mock/fixture/demo data produces DEMO_ONLY
4. source_timestamp preferred over fetched_at for age calculation
5. Non-trading days: last trading day's data is NON_TRADING_DAY_VALID (not stale)
6. Market closed valid: if today is trading day but market not yet open, yesterday's data is MARKET_CLOSED_VALID
7. TECHNICAL_INDICATORS: use the base OHLCV timestamp, not indicator calculation time
8. Precise-price profile: NEAR_STALE or worse blocks precise price
9. Backtest profile: STALE CORPORATE_ACTIONS blocks backtest
10. ABC profile: STALE underlying OHLCV blocks abc

## Blocking Profiles

- `precise_price`: Blocks precise price analysis when freshness is NEAR_STALE or worse
- `backtest`: Blocks backtest when freshness is STALE or worse
- `abc`: Blocks A/B/C buy point analysis when freshness is STALE or worse

## Provider SLA Monitor

- HTTP 200 but source timestamp stale → DELAYED (not HEALTHY)
- Cache hit does not indicate provider is healthy
- Auth required → no infinite retry
- Disabled provider → suppress repeated alerts
- 3 consecutive failures → BREACHED status

## Alert Deduplication

Dedup key: `symbol + dataset_type + provider_id + freshness_status + policy_id`

- Same stale issue does not create a new alert on each scan
- Status worsening updates existing alert severity
- Recovery resolves the alert
- Recurrence reopens the alert
- Alerts never trigger trade actions

## Runtime Data (gitignored)

```
data/freshness/           # snapshot store
data/freshness_alerts/    # alert persistence
reports/data_freshness_*.md
```

## Not Investment Advice

This module is for research and data quality monitoring only.
No trading signals are generated. No broker connection. No real orders.
```
```
