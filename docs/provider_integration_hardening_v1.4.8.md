# Provider Integration Hardening v1.4.8

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] No new providers. No authority drift. No silent fallback.

## Version Positioning

v1.4.8 is the cross-provider integration and stability hardening layer.

- **Version:** 1.4.8
- **Release:** Provider Integration Hardening
- **Base Release:** 1.4.7 Forum Intelligence & Market Sentiment
- **Replay Stable Baseline:** 1.2.9
- **Next:** v1.4.9 Provider Stable Rollup

## Provider Contracts

All six providers have validated contracts:

| Provider | Authority | Role |
|---|---|---|
| twse_official | PRIMARY | Listed stock official data |
| tpex_official | PRIMARY | OTC stock official data |
| mops_official | PRIMARY | Financial disclosure official data |
| data_gov_tw_official | PRIMARY | Government open data |
| finmind | SECONDARY | Secondary aggregation only |
| ptt_stock_public | SUPPLEMENTARY | Forum sentiment only |

Each contract validates: provider_id uniqueness, authority level, capabilities, health check, lineage bridge, quality profile, request/retry/cache policy, PIT policy, formal-use policy, CLI commands, query service, storage mapping, and safety flags.

## E2E Scenarios

Eight offline E2E scenarios (A–H):

- **A:** Listed stock full research chain (TWSE + MOPS + data.gov.tw + FinMind + PTT)
- **B:** OTC stock full research chain (TPEx + MOPS + data.gov.tw + FinMind + PTT)
- **C:** FinMind vs official conflict — official wins, FinMind kept as secondary evidence
- **D:** Forum sentiment vs official contradiction — PTT = WARN only, no official override
- **E:** MOPS revision — old lineage preserved, as-of uses correct version, no leakage
- **F:** Partial provider outage — PARTIAL result, no mock fallback, official data preserved
- **G:** Storage migration upgrade — additive only, idempotent, all old data readable
- **H:** Runtime DB corruption — BLOCKED state, fail-closed, original preserved

## Symbol Identity

Cross-provider symbol identity covers:
- Listed, OTC, ETF, delisted, suspended, renamed company, market transfer
- Duplicate alias, ambiguous alias
- Forum fuzzy alias never treated as formal symbol

Rules:
- Listed ≠ OTC even if same numeric code
- ETF never treated as common stock
- Historical company name maps only to correct period
- Current universe never backfills all history

## Date Alignment

- All timestamps Asia/Taipei (UTC+8)
- Trade date vs publication date vs available_from vs fetched_at strictly separated
- date-only precision (MOPS, FinMind) never promoted to exact timestamp
- Forum index date never used as exact article time
- fetched_at ≠ available_from (enforced by governance layer)

## PIT Hardening

`CrossProviderPITValidator` blocks:
- Future financial data (any provider)
- Future revisions (MOPS)
- Future forum comments or article edits
- Current Universe backfilling history
- Current alias mapping to wrong period
- Current delisting status backfilling past
- fetched_at replacing available_from

## Lineage Hardening

`CrossProviderLineageValidator` requires full traceability:
```
report section → normalized record → transformation → provider response → request → source identity
```

Blocking: orphan normalized records, orphan caches, orphan conflicts, orphan report sections, missing parser/schema versions, missing source/normalized hashes.

## Conflict Hardening

Conflict types: VALUE, DATE, UNIT, SYMBOL, MARKET, PERIOD, REVISION, AUTHORITY, SCHEMA_INCOMPARABLE, FORUM_CLAIM.

Rules:
- Authority hierarchy always wins (PRIMARY > SECONDARY > SUPPLEMENTARY)
- No auto-override
- Conflict history always preserved
- Unresolved blocking conflict prevents formal use
- Forum claim conflict = warning/risk only, never modifies official values

## Storage Migration Hardening

Migration registry with 5 migrations (m001–m005):
- All additive, non-destructive, idempotent, reversible
- Deterministic order
- Partially applied migration is detectable
- Old lineage, quality decisions, and forum data remain readable after migration

## Partial Failure Recovery

`PartialFailureRecoveryService` ensures:
- Successful chunks retained before failure
- Failed chunks recorded with error detail
- Fetch run marked PARTIAL_SUCCESS
- Resume uses request fingerprint (no duplicate writes)
- No infinite retry
- No mock fallback
- GUI cancel triggers clean partial recording

## Lock Recovery

Cross-process lock rules:
- Active lock (live PID, valid lease) = never deleted
- Stale lock (dead PID or expired lease) = recoverable with audit
- No permanent deadlock (deterministic acquisition order)
- Thread lock alone insufficient; DB-row or file lock required for cross-process protection

## Rate Recovery

Rate-limit recovery rules:
- HTTP 429 → honour Retry-After (seconds or date)
- Quota exhausted → no retry
- Process restart preserves cooldown (cross-process ledger)
- Host and provider rate budgets isolated
- No token rotation
- No proxy rotation
- Unknown policy → maximum conservative wait

## Runtime Corruption Recovery

Fail-closed for all corruption scenarios:
- Corrupt SQLite, corrupt JSON, truncated cache, invalid policy, malformed lock
- Original files never deleted or overwritten
- No fake success
- Recovery plan always available
- Runtime failure never affects tracked source files

## CLI/GUI Consistency

`CliGuiConsistencyValidator` ensures:
- CLI and GUI derive capabilities from same version_info flags
- Authority, quality state, safety flags, dataset status, rate state, PIT state, conflict count all identical
- No CLI PASS / GUI FAIL divergence
- No dangerous GUI actions (repair production DB, delete lock, increase rate limit, enable fallback, override authority, buy/sell/order/auto_trade)
- GUI write actions default dry_run=True

## Headless GUI Stability

`gui/provider_integration_hardening_panel.py`:
- Import safe without QApplication
- No QWidget instantiated on import
- Headless stub available when PySide6 not installed
- Worker cancellation on close
- No QThread leak
- No native crash on import

## Performance

Conservative thresholds (offline, no network):

| Operation | Threshold (ms) |
|---|---|
| Provider registry load | 2,000 |
| CLI startup | 3,000 |
| Health aggregate | 5,000 |
| Source lineage query | 1,000 |
| Stable report generation | 10,000 |
| 1,000 records normalization | 5,000 |
| 10,000 lineage records | 10,000 |

## Memory

- Streaming/pagination required for all bulk operations
- Response size cap enforced per provider
- Article/comment/query limits enforced
- GUI table rows limited with pagination
- No unbounded cache growth
- No unbounded list growth

## Collection Integrity

`ProviderIntegrationCollectionIntegrityCheck`:
- Baseline: 3,426 (v1.4.7)
- v1.4.8 adds 171 new tests → new baseline ≥ 3,597
- No native crash, no hidden deselection, no partial suite misreported as full

## Release Gate

New gates added to existing Release Gate:

```
PROVIDER_CONTRACTS_VALID
CROSS_PROVIDER_E2E_VALID
CROSS_PROVIDER_PIT_VALID
CROSS_PROVIDER_LINEAGE_VALID
CROSS_PROVIDER_CONFLICT_VALID
STORAGE_MIGRATIONS_VALID
PARTIAL_FAILURE_RECOVERY_VALID
LOCK_RECOVERY_VALID
RATE_LIMIT_RECOVERY_VALID
RUNTIME_CORRUPTION_RECOVERY_VALID
CLI_GUI_CONSISTENCY_VALID
GUI_HEADLESS_STABILITY_VALID
PROVIDER_PERFORMANCE_BUDGET_VALID
PROVIDER_MEMORY_BUDGET_VALID
COLLECTION_INTEGRITY_VALID
NO_PROVIDER_AUTHORITY_DRIFT
NO_HIDDEN_FALLBACK
```

## No New Provider

This version does NOT add any new data providers. The six providers from v1.4.0–1.4.7 remain unchanged.

## No Authority Drift

Authority hierarchy is frozen:
- twse_official, tpex_official, mops_official, data_gov_tw_official = PRIMARY
- finmind = SECONDARY (cannot override PRIMARY)
- ptt_stock_public = SUPPLEMENTARY (cannot override PRIMARY or SECONDARY)

## No Fallback

All fallback flags remain False:
- PROVIDER_INTEGRATION_AUTO_FALLBACK_ENABLED = False
- PROVIDER_INTEGRATION_AUTO_OVERRIDE_ENABLED = False
- PROVIDER_INTEGRATION_AUTO_REPAIR_ENABLED = False
- MOCK_FALLBACK_ENABLED = False (all providers)
- SILENT_FALLBACK_ENABLED = False

## No Broker

- BROKER_EXECUTION_ENABLED = False
- NO_REAL_ORDERS = True
- PRODUCTION_TRADING_BLOCKED = True

## Known Limitations

- E2E scenarios are offline structural checks, not live integration tests
- Performance thresholds are conservative offline baselines (not CI benchmarks)
- GUI headless tests skipped when PySide6 not installed
- FinMind and PTT providers require network for actual data fetch (all offline in tests)

## Roadmap

| Version | Release | Status |
|---|---|---|
| v1.4.6 | Provider Quality Gates | Done |
| v1.4.7 | Forum Intelligence & Market Sentiment | Done |
| **v1.4.8** | **Provider Integration Hardening** | **Done** |
| v1.4.9 | Provider Stable Rollup | Next |
