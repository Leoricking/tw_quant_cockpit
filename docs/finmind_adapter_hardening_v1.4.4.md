# FinMind Adapter Hardening v1.4.4

> **[!] Research Only. No Real Orders. Not Investment Advice.**
> **[!] SECONDARY_AGGREGATOR — cannot override TWSE/TPEx/MOPS primary sources.**

## Overview

Version 1.4.4 introduces a hardened FinMind adapter as a **secondary aggregator** data provider. FinMind is a third-party data aggregation service for Taiwan stock market data. It is **not** an official primary source and cannot override TWSE, TPEx, or MOPS data.

| Attribute | Value |
| --- | --- |
| Provider ID | `finmind` |
| Authoritative Level | `SECONDARY_AGGREGATOR` |
| Official | `False` |
| API Version | v4 |
| Base URL | `https://api.finmindtrade.com/api/v4/data` |
| Can Override Primary | `False` |
| Token Required | `False` (optional, increases quota) |

## Safety Invariants

All safety invariants from previous releases are preserved. FinMind-specific invariants:

| Invariant | Value |
| --- | --- |
| `NO_REAL_ORDERS` | `True` |
| `BROKER_EXECUTION_ENABLED` | `False` |
| `PRODUCTION_TRADING_BLOCKED` | `True` |
| `FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER` | `False` |
| `FINMIND_SILENT_FALLBACK_ENABLED` | `False` |
| `FINMIND_MOCK_FALLBACK_ENABLED` | `False` |
| `FINMIND_AUTO_DOWNLOAD_ENABLED` | `False` |
| `FINMIND_AUTO_DISCOVERY_ENABLED` | `False` |
| `FINMIND_REALTIME_FORMAL_USE_ALLOWED` | `False` |
| `FINMIND_BROKER_EXECUTION_AVAILABLE` | `False` |
| `FINMIND_TOKEN_OPTIONAL` | `True` |
| `FINMIND_TOKEN_STORAGE_SECURE` | `True` |

## Architecture

### Module Layout

```
data/providers/finmind/
├── __init__.py
├── models_v144.py          — enums and dataclasses
├── capabilities_v144.py    — capability registry
├── datasets_v144.py        — dataset allowlist manager
├── auth_v144.py            — secure token handling
├── quota_v144.py           — quota tracking
├── error_classifier_v144.py — error classification
├── client_v144.py          — HTTP client (injectable transport)
├── rate_limit_v144.py      — retry and rate-limit handling
├── parser_v144.py          — API response parser
├── normalizer_v144.py      — field normalization
├── schema_registry_v144.py — schema definitions
├── schema_drift_v144.py    — drift detection
├── authority_policy_v144.py — authority and formal-use policy
├── conflict_detection_v144.py — primary vs. FinMind comparison
├── point_in_time_v144.py   — PIT classification and guard
├── cache_policy_v144.py    — cache key and TTL policy
├── query_v144.py           — composed query service
├── health_v144.py          — health checks
└── provider_v144.py        — FinMindAdapterV144 entry point
```

### Authority Model

FinMind is a `SECONDARY_AGGREGATOR`. This means:

- Formal conclusions (regulatory, compliance, trading signals) require primary source validation.
- In any conflict between FinMind and TWSE/TPEx/MOPS data, the **primary source always wins**.
- FinMind data is preserved as secondary evidence for research purposes only.
- No auto-repair of conflicts. All conflicts are logged for manual review.

### Token Handling

- Token is read from environment variables `FINMIND_API_TOKEN` or `FINMIND_TOKEN`.
- Token is **never** logged, displayed, or stored in reports.
- Only the first 8 characters of the SHA256 hash of the token are used as a fingerprint for diagnostic purposes.
- Anonymous mode (no token) is allowed; authenticated mode increases quota limits.

### Quota Management

- Anonymous users: ~300 requests/hour (subject to FinMind policy changes).
- Authenticated users: ~600 requests/hour (subject to FinMind policy changes).
- `plan_unknown=True` by default — FinMind does not expose plan tier in the API.
- On `QUOTA_EXCEEDED`: stop non-essential prefetch, no retry, no token rotation, no mock fallback.

### Error Classification

The error classifier handles:

| Condition | Error Code |
| --- | --- |
| HTTP 401 | `INVALID_TOKEN` |
| HTTP 404 or `id not found` in body | `DATA_ID_NOT_FOUND` |
| HTTP 429 | `RATE_LIMITED` |
| HTTP 5xx | `SERVICE_UNAVAILABLE` |
| Payload `status=402` + "limit" in message | `QUOTA_EXCEEDED` |
| HTML content type | `SERVICE_UNAVAILABLE` |
| JSON decode failure | `MALFORMED_RESPONSE` |
| Empty data array | `EMPTY_DATA` |

Note: FinMind returns quota errors as HTTP 200 with `status=402` in the JSON payload. The classifier handles this correctly.

### Dataset Allowlist

Only explicitly approved datasets may be queried. No wildcard allowlist, no auto-approve, no auto-discovery.

| Dataset | Status | PIT Class |
| --- | --- | --- |
| `TaiwanStockPrice` | SUPPORTED | DATE_ONLY |
| `TaiwanStockInstitutionalInvestorsBuySell` | SUPPORTED | DATE_ONLY |
| `TaiwanStockInstitutionalInvestorsBuySellWide` | EXPERIMENTAL | DATE_ONLY |
| `TaiwanStockMarginPurchaseShortSale` | SUPPORTED | DATE_ONLY |
| `TaiwanStockMonthRevenue` | SUPPORTED | DATE_ONLY |
| `TaiwanStockFinancialStatements` | SUPPORTED | DATE_ONLY |

Allowlist configuration: `config/finmind_dataset_allowlist.json`

### Schema Drift Detection

| Drift Type | Behavior |
| --- | --- |
| Additive (new fields) | WARN — not blocking |
| Missing required field | BLOCKING |
| Type change | BLOCKING |
| Key change | BLOCKING |

### Point-in-Time (PIT) Guard

All FinMind daily datasets are classified as `DATE_ONLY`. The PIT guard:

- Blocks formal historical conclusions when PIT class is `UNKNOWN`.
- Validates `as_of` dates against `available_from` to prevent lookahead.
- Never infers minute-level PIT from daily data.

### Cache Policy

- Cache keys include `token_mode` ("anonymous" or "authenticated") and `mode` ("real" or "mock").
- Real and mock caches are isolated.
- The actual token value is never stored in cache keys.

| Dataset Type | TTL |
| --- | --- |
| Daily OHLCV | 24 hours |
| Monthly Revenue | 7 days |
| Financial Statements | 30 days |

## CLI Commands

Access FinMind adapter diagnostics via the CLI:

```
finmind-health             Run all health checks
finmind-capabilities       List adapter capabilities
finmind-datasets           List all allowlisted datasets
finmind-dataset            Show details for a specific dataset
finmind-schema             Show schema for a dataset
finmind-schema-drift       Check schema drift for a dataset
finmind-quota              Show current quota status
finmind-auth-status        Show authentication status (no token display)
finmind-plan               Dry-run request plan (no download)
finmind-fetch              Fetch dataset (dry-run by default)
finmind-price              Fetch price data for a symbol
finmind-institutional      Fetch institutional investor data
finmind-margin             Fetch margin/short-sale data
finmind-compare-primary    Compare FinMind vs primary source
finmind-conflicts          Show logged conflicts
finmind-coverage           Show dataset coverage summary
finmind-lineage            Show provider lineage
finmind-cache-status       Show cache status
finmind-adapter-report     Generate full adapter report
```

## GUI Panel

The FinMind Adapter panel is registered as:

- Tab ID: `finmind_adapter`
- Display Name: `FinMind Adapter`
- Group: `data`
- Priority: `P1`

The panel displays: adapter status, safety banner, authentication status (no token), quota status, dataset registry, capabilities, request planner (dry-run only), schema drift status, and lineage.

The GUI panel enforces the same safety invariants as the rest of the system.

## Testing

Test suite: `tests/test_finmind_adapter_hardening_v144.py`

166 tests covering:

1. Registration — version, flags, capability registry
2. Token security — no logging, fingerprint only, anonymous mode
3. Quota management — tracking, exhaustion, response update
4. Error classification — all error types including payload 402
5. Dataset allowlist — allowed/blocked datasets
6. Schema registry and drift detection
7. Price field normalization
8. Institutional investor normalization (narrow and wide)
9. Margin/short-sale normalization
10. Authority policy — formal use always blocked for SECONDARY_AGGREGATOR
11. Point-in-time guard — DATE_ONLY classification, lookahead prevention
12. Retry logic — rate limit, respects Retry-After header
13. Cache policy — key isolation, TTL mapping
14. Request planner — dry-run, no auto-download
15. Data quality and freshness
16. CLI command registration
17. GUI panel data structure
18. Regression — safety invariants preserved across all modules

Fixtures: `tests/fixtures/finmind_adapter/` (21 JSON/HTML files)

## Known Limitations

1. `plan_unknown=True` — FinMind does not expose plan tier; actual quota may differ from defaults.
2. `DATE_ONLY` PIT class — no intraday precision; formal conclusions require primary source.
3. SECONDARY_AGGREGATOR — all formal conclusions require TWSE/TPEx/MOPS cross-check.
4. Token is optional but recommended for higher quota limits.
5. `TaiwanStockInstitutionalInvestorsBuySellWide` format is EXPERIMENTAL.
6. Not all FinMind datasets are in the allowlist — only explicitly approved ones.

## Release Notes

**v1.4.4 — FinMind Adapter Hardening**

- New: FinMind API v4 adapter with 20 hardened modules
- New: Secure token handling with SHA256 fingerprint only
- New: Quota tracking with `plan_unknown=True` guard
- New: Payload-level error classification (HTTP 200 with status=402)
- New: Dataset allowlist (6 datasets, no wildcard)
- New: Schema drift detection with blocking on breaking changes
- New: Point-in-time guard for DATE_ONLY datasets
- New: Primary-source conflict detection (primary always wins)
- New: Injectable transport for offline testing
- New: 19 CLI diagnostic commands
- New: GUI adapter panel
- New: Adapter report with 12 sections
- New: 166-test regression suite with 21 fixtures
- Safety: All trading safety invariants preserved
- Safety: `can_override_primary_provider=False`
- Safety: No silent fallback, no mock fallback, no auto-download

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
