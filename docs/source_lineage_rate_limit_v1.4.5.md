# Source Lineage & Rate Limit v1.4.5

[!] Research Only. No Real Orders. Not Investment Advice.

## Overview

v1.4.5 introduces a centralized governance layer that unifies source lineage, rate limiting, request auditing, and authority hierarchy across all data providers (TWSE, TPEx, MOPS, data.gov.tw, FinMind).

This is a governance infrastructure layer — it does not modify any existing provider modules.

## Safety Invariants

All safety flags are enforced and must remain unchanged:

| Flag | Value |
|------|-------|
| `NO_REAL_ORDERS` | `True` |
| `BROKER_EXECUTION_ENABLED` | `False` |
| `PRODUCTION_TRADING_BLOCKED` | `True` |
| `RATE_LIMIT_AUTO_BYPASS_ENABLED` | `False` |
| `TOKEN_ROTATION_ENABLED` | `False` |
| `PROXY_ROTATION_ENABLED` | `False` |
| `PRIMARY_SOURCE_OVERRIDE_ENABLED` | `False` |

## Architecture

### Source Authority Hierarchy

Sources are ranked by authority level (highest to lowest):

1. `PRIMARY_OFFICIAL` — Official exchange data (TWSE, TPEx, MOPS)
2. `PRIMARY_DOMAIN_OFFICIAL` — Official government open data (data.gov.tw)
3. `SECONDARY_OFFICIAL` — Official secondary sources
4. `SECONDARY_AGGREGATOR` — Aggregators (FinMind)
5. `SUPPLEMENTARY` — Supplementary sources
6. `TEST_FIXTURE` — Test-only fixture data
7. `MOCK` — Mock data (blocked in real mode)
8. `UNKNOWN` — Unknown/unregistered sources

### Core Modules

| Module | Purpose |
|--------|---------|
| `data/governance/models_v145.py` | Core dataclasses with `to_dict()`/`from_dict()` |
| `data/governance/source_authority_v145.py` | Authority registry and comparison |
| `data/governance/request_fingerprint_v145.py` | SHA-256 deterministic fingerprinting (secrets excluded) |
| `data/governance/lineage_registry_v145.py` | Source lineage registry (in-memory, BFS root tracing) |
| `data/governance/provenance_v145.py` | Provenance completeness gate (PASS/PARTIAL/FAIL/BLOCKED) |
| `data/governance/request_ledger_v145.py` | Append-only request ledger (no token storage) |
| `data/governance/fetch_run_audit_v145.py` | Fetch run lifecycle audit |
| `data/governance/rate_limit_manager_v145.py` | Token bucket rate limiting |
| `data/governance/host_policy_v145.py` | Per-host rate limit policies (confidence=LOW) |
| `data/governance/provider_budget_v145.py` | Per-provider request budgets |
| `data/governance/endpoint_policy_v145.py` | Per-endpoint request policies |
| `data/governance/quota_evidence_v145.py` | Quota evidence extraction (allowlisted headers only) |
| `data/governance/retry_evidence_v145.py` | Retry evidence with exponential backoff |
| `data/governance/cross_process_lock_v145.py` | File-based cross-process lock with stale recovery |
| `data/governance/cache_lineage_v145.py` | Cache entry lineage tracking |
| `data/governance/conflict_lineage_v145.py` | Data conflict detection and resolution |
| `data/governance/store_v145.py` | In-memory or SQLite storage (11 tables, additive migrations) |
| `data/governance/query_v145.py` | Unified query service with `governance_report()` |
| `data/governance/health_v145.py` | Health check (41 checks) |

### Provider Bridges

Lightweight read-only mappings from providers to governance models. These do not modify provider modules.

| Bridge | Provider | Authority |
|--------|----------|-----------|
| `bridge_twse_v145.py` | TWSE | `PRIMARY_OFFICIAL` |
| `bridge_tpex_v145.py` | TPEx | `PRIMARY_OFFICIAL` |
| `bridge_mops_v145.py` | MOPS | `PRIMARY_OFFICIAL` |
| `bridge_data_gov_tw_v145.py` | data.gov.tw | `PRIMARY_DOMAIN_OFFICIAL` |
| `bridge_finmind_v145.py` | FinMind | `SECONDARY_AGGREGATOR` |

Note: `FINMIND_CAN_OVERRIDE_PRIMARY = False` — FinMind cannot override PRIMARY_OFFICIAL sources.

## Rate Limit Policies

All policies use `confidence=LOW` (conservative estimates, actual limits not published):

| Host | Min Interval | Max RPM |
|------|-------------|---------|
| `openapi.twse.com.tw` | 2000ms | 30 |
| `www.twse.com.tw` | 3000ms | 20 |
| `www.tpex.org.tw` | 3000ms | 20 |
| `mops.twse.com.tw` | 4000ms | 15 |
| `data.gov.tw` | 2000ms | 30 |
| `api.finmindtrade.com` | 6000ms | 10 |

## Provider Request Budgets

| Provider | Per-Run | Hourly | Daily |
|----------|---------|--------|-------|
| twse | 50 | 200 | 500 |
| tpex | 50 | 150 | 400 |
| mops | 30 | 100 | 300 |
| data_gov_tw | 50 | 200 | 500 |
| finmind | 20 | 60 | 200 |

Cache hits do not consume budget.

## CLI Commands

All 21 commands are in the `source_governance` group, introduced in v1.4.5:

```
source-governance-health       — Health check (41 checks)
source-lineage-sources         — List registered sources
source-lineage-show            — Show lineage record
source-lineage-trace           — Trace lineage to root
source-lineage-record          — Record a lineage entry
source-lineage-incomplete      — List incomplete lineage
request-ledger-list            — List request ledger entries
request-ledger-show            — Show ledger entry
fetch-run-list                 — List fetch runs
fetch-run-show                 — Show fetch run details
rate-limit-status              — Rate limit manager status
rate-limit-host                — Host policy details
rate-limit-provider            — Provider budget status
rate-limit-endpoint            — Endpoint policy details
request-budget-status          — Request budget overview
quota-evidence-list            — List quota evidence
retry-evidence-list            — List retry evidence
cache-lineage-show             — Show cache lineage
conflict-lineage-list          — List data conflicts
conflict-lineage-show          — Show conflict details
source-governance-report       — Full governance report
```

## GUI Panel

- Tab ID: `source_governance`
- Group: `data`
- Priority: `P1`
- 8 sections: source_authority, lineage_registry, provenance_gate, request_ledger, fetch_run_audit, rate_limit_manager, budget_status, conflict_lineage

## Storage

- **Runtime**: In-memory by default; SQLite optional (`data/governance.db`)
- **Gitignored**: All runtime governance data (see `.gitignore`)
- **Committed**: Test fixtures only (`tests/fixtures/source_governance/*.json`)

## Request Fingerprinting

- SHA-256 hash of sorted request parameters
- Secret parameters excluded: `token`, `key`, `cookie`, `auth`, `authorization`, `password`, `secret`, `access_token`, `api_key`
- Parameter order independent

## Provenance Gate Results

| Result | Condition |
|--------|-----------|
| `PASS` | All mandatory fields present, real source, no issues |
| `PARTIAL` | Some optional fields missing |
| `FAIL` | source_content_hash missing, parser_version missing, or cache hit without source lineage |
| `BLOCKED` | MOCK or TEST_FIXTURE authority in real mode |

## Changelog

- **v1.4.5**: Initial release — Source Lineage & Rate Limit governance layer
- Capability `provider_lineage_rate_limit` graduated from PLANNED to STABLE
