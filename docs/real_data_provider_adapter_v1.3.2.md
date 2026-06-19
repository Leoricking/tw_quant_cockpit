# Real Data Provider Adapter Foundation — v1.3.2

**[!] Research Only. No Real Orders. No Broker. Not Investment Advice.**  
**[!] Provider ≠ Broker. No order methods. No credentials stored.**  
**[!] Real Mode NEVER falls back to mock. Mock mode always labeled DEMO_ONLY.**

---

## What Is a Provider Adapter?

A **Provider Adapter** is a unified interface that allows the application to read market data from different local sources (CSV files, local databases) through a consistent API.

Key properties:
- **Read-only** — no order submission, no broker connection
- **Traceable** — every response carries full provenance
- **Queryable** — capabilities can be inspected before requesting data
- **Error-classified** — every error has a specific category with retry rules
- **Cache-consistent** — TTL varies by data type; stale ≠ fresh

---

## Provider vs. Broker

| Aspect | Provider | Broker |
|--------|----------|--------|
| Role | Read market data | Execute trades |
| Orders | NEVER | Would (but disabled here) |
| Credentials stored | NEVER | Would need |
| Mock fallback | NEVER in Real mode | N/A |
| This version | YES | NOT in this version |

**Provider AVAILABLE ≠ Broker Connected.**  
**Provider Connected ≠ can generate precise prices.**  
**Universe Ready ≠ can trade.**

---

## Provider Registry

`RealDataProviderRegistryV132` maintains a registry of all known provider adapters.

- Providers are registered with `register(adapter)`
- Only **enabled** providers are returned by `resolve_provider()`
- MOCK / TEST_FIXTURE providers are **never** selected in REAL mode
- AUTH_REQUIRED providers are not treated as AVAILABLE
- Priority is numeric — lower value = higher priority

---

## Capability Matrix

`ProviderCapabilityMatrix` builds a full matrix of `{provider_id: {capability: support_status}}`.

Support statuses: `SUPPORTED`, `PARTIAL`, `UNSUPPORTED`, `DISABLED`, `AUTH_REQUIRED`, `UNKNOWN`.

**Never use True/False only — status must be explicit.**

---

## Local File Adapter

`LocalFileProviderAdapter` reads from local CSV/JSON files.

Rules:
- Only reads from explicitly configured `base_dir`
- Never recursively scans entire disk
- Checks file existence before reading
- Schema mismatch → `SCHEMA_MISMATCH` error
- Fixture paths → `BLOCKED` in REAL mode
- NaN is **NOT** converted to 0
- Missing institutional data is **NOT** set to 0

---

## Local Repository Adapter

`LocalRepositoryProviderAdapter` wraps an existing local database/directory.

Rules:
- Does **NOT** create a new database
- If no database found → graceful `UNAVAILABLE` (not error crash)
- Never falls back to mock

---

## Provider Request / Response

**ProviderRequest** specifies what data is needed:
- `provider_id`, `capability`, `symbols`, `market`, `start_date`, `end_date`
- `force_refresh` bypasses cache

**ProviderResponse** carries the result:
- `status` (ProviderStatus), `data_mode`, `records`, `record_count`
- `cache_status`, `provenance`, `warnings`, `errors`, `retryable`

---

## Error Classification

`ProviderErrorCategory` provides specific error types:

| Category | Retryable | Notes |
|----------|-----------|-------|
| NETWORK | Yes | Transient network issue |
| TIMEOUT | Yes | Request timed out |
| DNS | Yes | DNS resolution failure |
| RATE_LIMIT | Yes (with retry-after) | Respect retry-after header |
| AUTHENTICATION | **No** | Never infinite retry |
| INVALID_SYMBOL | **No** | Symbol doesn't exist |
| UNSUPPORTED_CAPABILITY | **No** | Adapter doesn't support this |
| SCHEMA_MISMATCH | **No** | Data format incompatible |
| MALFORMED_RESPONSE | **No** | Cannot return as success |
| EMPTY_RESPONSE | Context | True empty vs. source anomaly |

---

## Retry Policy

`ProviderRetryPolicy` configures conservative retry:
- `max_attempts = 3`
- Exponential backoff with jitter
- Respects `retry_after_seconds`
- Non-retryable categories never retried
- No infinite retry. No high-frequency bombardment.

Preset: `CONSERVATIVE_POLICY` for production, `TEST_POLICY` (delay=0) for tests.

---

## Cache Policy

`InMemoryProviderCache` with TTL by capability:
- DAILY_OHLCV: 3600s
- INTRADAY_OHLCV: 60s
- MONTHLY_REVENUE / FINANCIAL_STATEMENT: 86400s
- Default: 1800s

Rules:
- Stale ≠ fresh — `CacheStatus.STALE` is returned explicitly
- `force_refresh=True` → `CacheStatus.BYPASSED`
- Corrupt entries → `CacheStatus.INVALID`
- Credentials are **never** cached
- Runtime cache is **never** committed to git
- Tests use `tmp_path` (temp directory)

---

## Provenance

`ProviderProvenanceRecord` tracks the full origin of every response:
- `provider_id`, `provider_type`, `capability`, `request_id`
- `source_reference` (file path or "local_db" — NO credentials)
- `fetched_at`, `source_timestamp`, `market_timestamp`
- `cache_status`, `attempt_count`, `fallback_from`
- `raw_field_availability`, `transformations`, `content_hash`

Rules:
- No credentials recorded
- No full API response stored in git
- `fallback_from` is **never** "mock" or "test_fixture"
- Multi-source merges list **all** sources

---

## Multi-Source Conflict

`ProviderResponseMerger` handles responses from multiple providers:
- Price tolerance: 1% — conflicts above this create `SOURCE_CONFLICT`
- Core price conflict → `precise_price_blocked = True`
- Primary value is kept, secondary is recorded as observation
- Never silently averages prices
- Adjusted vs. unadjusted mismatch is flagged

---

## Data Quality Integration

Provider errors can be converted to `DataQualityIssue` objects:
- `CORE_PRICE_SOURCE_CONFLICT` → blocks precise prices
- Provider UNAVAILABLE → coverage UNAVAILABLE
- Provider only MOCK → DEMO_ONLY
- Provider error → does NOT fall back to mock

---

## Universe Integration

`UniverseCoverageRecord` (v1.3.2+) includes provider fields:
- `provider_id`, `provider_status`, `provider_capabilities`
- `last_provider_success_at`, `last_provider_failure_at`
- `provider_warnings`

Rules:
- No provider → UNAVAILABLE
- Provider disabled → not enabled
- Provider only mock → DEMO_ONLY
- Provider error → no mock fallback
- Provider AVAILABLE ≠ coverage READY

---

## How to Run Provider CLI

```bash
# List all providers
python main.py provider-list

# Show a specific provider
python main.py provider-show --provider local_file

# Show capability matrix
python main.py provider-capabilities

# Show provider status
python main.py provider-status-v132

# Run provider health checks
python main.py provider-health-v132

# Request data (read-only)
python main.py provider-request --capability daily-ohlcv --symbol 2330

# Request fixture in Real mode (expected: BLOCKED)
python main.py provider-request --provider test_fixture --symbol 2330

# Check cache status
python main.py provider-cache-status

# Show provenance for a request
python main.py provider-provenance --request-id <uuid>
```

---

## GUI Provider Panel

The **Real Data Providers** tab in the cockpit GUI shows:
- Safety banner at top
- Provider Status table (all registered providers)
- Capability Matrix tab
- Request Inspector (read-only, runs in worker thread)

The panel enforces:
- No Broker Connect / Account Login / Order / Buy / Sell / Submit buttons
- No credential input
- Worker thread safety — no QThread leak on close
- Provider failure does NOT crash the panel

---

## Why This Version Does Not Connect Real Commercial APIs

v1.3.2 establishes the **adapter architecture foundation** only. Live connections to commercial APIs require:
1. Explicit terms agreement
2. Credential management (out of scope — credentials never stored in git)
3. Rate limit management
4. API-specific normalization

These are planned for future versions.

---

## Why Credentials Are Never Stored

- Credentials in git = security risk
- `ProviderMetadata` deliberately excludes password, API secret, access token, refresh token fields
- `REAL_DATA_PROVIDER_CREDENTIAL_STORAGE_ENABLED = False` (always)

---

## Safety Summary

| Flag | Value |
|------|-------|
| No Real Orders | True |
| Broker Execution Enabled | False |
| Production Trading BLOCKED | True |
| Mock Fallback Enabled | False |
| Provider Live Connection Available | False |
| Provider Auto Download Enabled | False |
| Provider Credential Storage Enabled | False |

---

## Roadmap

| Version | Name |
|---------|------|
| v1.3.0 | Real Data Quality Foundation |
| v1.3.1 | Universe Expansion Foundation |
| **v1.3.2** | **Real Data Provider Adapter Foundation** (this version) |
| v1.3.3 | Coverage Repair Workflow |
| v1.3.4 | Data Freshness Monitor |
| v1.4.0 | Strategy Knowledge Empirical Backtest |
