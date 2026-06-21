# Provider Quality Gates v1.4.6

[!] Research Only. No Real Orders. Not Investment Advice.
[!] QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False (always).
[!] AUTO_PROVIDER_PROMOTION_ENABLED = False (always).
[!] AUTO_QUARANTINE_RELEASE_ENABLED = False (always).
[!] MOCK_FALLBACK_ENABLED = False (always).

---

## Overview

Provider Quality Gates v1.4.6 is the Central Quality Decision Layer for TW Quant Cockpit.
It decides:

- Is a Provider eligible for formal use?
- Is a Dataset admitted for formal research?
- Is a batch eligible for backtesting?
- Is data suitable for a formal report?
- Should a source be ACTIVE, DEGRADED, RESTRICTED, QUARANTINED, or BLOCKED?
- Which authority source wins in a conflict?
- Does a Quality Gate failure stop formal use?

---

## Module Map (29 modules under `data/governance/quality/`)

| Module | Purpose |
|---|---|
| `__init__.py` | Safety constants package entry |
| `models_v146.py` | All enums and dataclasses |
| `gate_registry_v146.py` | Registry of 15 quality gates |
| `decision_engine_v146.py` | Central quality decision engine |
| `provider_gate_v146.py` | Provider operational evaluation |
| `dataset_gate_v146.py` | Dataset admission gate |
| `endpoint_gate_v146.py` | Endpoint readiness gate |
| `batch_gate_v146.py` | Batch ingestion gate |
| `formal_research_gate_v146.py` | Formal research eligibility |
| `backtest_gate_v146.py` | Backtest input eligibility |
| `report_gate_v146.py` | Report section gate |
| `quality_gate_v146.py` | Quality score → gate status |
| `freshness_gate_v146.py` | Data freshness check |
| `coverage_gate_v146.py` | Symbol/date coverage check |
| `provenance_gate_v146.py` | Provenance completeness (wraps v1.4.5) |
| `pit_gate_v146.py` | Point-in-time integrity |
| `schema_gate_v146.py` | Schema drift gate |
| `authority_gate_v146.py` | Authority hierarchy (uses v1.4.5) |
| `conflict_gate_v146.py` | Conflict resolution (uses v1.4.5) |
| `rate_limit_gate_v146.py` | Rate limit readiness |
| `quota_gate_v146.py` | Quota readiness |
| `safety_gate_v146.py` | Safety invariants gate |
| `score_v146.py` | Quality score engine |
| `quarantine_v146.py` | Quarantine manager |
| `audit_v146.py` | Append-only audit service |
| `policy_v146.py` | Policy manager |
| `store_v146.py` | SQLite store (8 tables) |
| `query_v146.py` | Query service |
| `health_v146.py` | Health check (50+ checks) |

---

## Key Enums

### ProviderQualityState
`ACTIVE | DEGRADED | RESTRICTED | QUARANTINED | BLOCKED | DISABLED | UNKNOWN`

### QualityScope
`PROVIDER | HOST | ENDPOINT | DATASET | SYMBOL | DATE_RANGE | FETCH_RUN | BATCH | RECORD | REPORT_SECTION | BACKTEST_INPUT`

### GateStatus
`PASS | WARN | FAIL | BLOCKED | NOT_APPLICABLE | UNKNOWN`

### QualityDecisionResult
`ALLOW | ALLOW_WITH_WARNING | RESTRICT | QUARANTINE | BLOCK | DISABLE`

---

## Safety Invariants (always enforced)

```python
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False
AUTO_PROVIDER_PROMOTION_ENABLED = False
AUTO_PRIMARY_OVERRIDE_ENABLED = False
SILENT_PROVIDER_FALLBACK_ENABLED = False
AUTO_QUARANTINE_RELEASE_ENABLED = False
MOCK_FALLBACK_ENABLED = False
AUTO_RATE_LIMIT_BYPASS_ENABLED = False
```

---

## Blocking Rules (non-negotiable)

1. **Blocking failures always override score** — a score of 99 cannot override a blocking failure.
2. **`score_overrode_blocking` is always False** — enforced by `QualityDecision.__post_init__`.
3. **`auto_release_allowed` is always False** — enforced by `QuarantineRecord.__post_init__`.
4. **`can_override_blocking` is always False** — enforced by `QualityScore.__post_init__`.
5. **Future leakage always BLOCKS** — no exception in `PITGate` or `BacktestInputEligibilityGate`.
6. **Breaking schema drift always BLOCKS** — `BREAKING_*` → `BLOCKED` in `SchemaDriftGate`.
7. **MOCK/TEST_FIXTURE/UNKNOWN authority blocks formal use** — enforced in `AuthorityGate`.
8. **Unresolved primary-source VALUE_CONFLICT blocks formal use** — enforced in `ConflictGate`.
9. **Dataset not in allowlist is immediately BLOCKED** — enforced in `DatasetAdmissionGate`.
10. **Provider not registered is immediately BLOCKED** — enforced in `ProviderOperationalGate`.

---

## Quality Score Weights (sum = 100)

| Category | Weight |
|---|---|
| data_quality | 20 |
| freshness | 15 |
| coverage | 15 |
| provenance | 15 |
| pit | 10 |
| schema | 10 |
| authority_conflict | 10 |
| operational | 5 |

---

## Gate Registry (15 gates)

| Gate ID | Category | Blocking |
|---|---|---|
| provider_registration | onboarding | Yes |
| provider_health | onboarding | Yes |
| dataset_admission | admission | Yes |
| endpoint_readiness | operational | Yes |
| batch_ingestion | operational | Yes |
| formal_research_eligibility | formal_research | Yes |
| backtest_input_eligibility | backtest | Yes |
| safety_invariants | safety | Yes |
| schema_drift | schema | Yes (breaking) |
| authority_hierarchy | authority | Yes (formal) |
| conflict_resolution | conflict | Yes (unresolved) |
| freshness | freshness | No |
| coverage | coverage | No |
| provenance_completeness | provenance | No |
| point_in_time | pit | Yes (leakage) |

---

## Freshness Edge Cases

- `quota_exhausted = True` → WARN only, NOT stale, does NOT block
- `rate_limited = True` → WARN only, NOT stale, does NOT block
- `freshness_status = UNKNOWN` → FAIL (not PASS)
- `freshness_status = STALE` → FAIL

---

## Coverage Thresholds

| Mode | Pass Threshold |
|---|---|
| Normal | 95% |
| Backtest | 98% (stricter) |
| Acceptable (warn) | 80% |
| Backtest acceptable | 90% |

---

## v1.4.5 Integration Points

- `ProvenanceGate` wraps `v1.4.5 ProvenanceCompletenessGate` via `self._v145_gate`
- `AuthorityGate` uses `v1.4.5 SourceAuthorityLevel` and `SourceAuthorityRegistry`
- `ConflictGate` uses `v1.4.5 ConflictLineage` and `ConflictType`
- `store_v146.py` does NOT touch v1.4.5 SQLite tables

---

## CLI Commands (20, group=provider_quality_gates, introduced_in=1.4.6)

```
provider-quality-health
provider-quality-gates
provider-quality-evaluate-provider
provider-quality-evaluate-dataset
provider-quality-evaluate-endpoint
provider-quality-evaluate-fetch-run
provider-quality-profiles
provider-quality-datasets
provider-quality-quarantine-list
provider-quality-blocked-list
provider-quality-decision
provider-quality-explain
provider-quality-audit
provider-quality-score
provider-quality-policy
provider-quality-formal-research
provider-quality-backtest
provider-quality-safety
provider-quality-report
provider-quality-gate-detail
```

---

## GUI Panel

File: `gui/provider_quality_gates_panel.py`
- `tab_id = "provider_quality_gates"`
- `group = "data"`, `priority = "P1"`
- `read_only = True`, `no_real_orders = True`
- `quality_score_can_override_blocking = False`
- 7 sections: Overview, Provider Profiles, Dataset Profiles, Gate Results, Quarantine, Decisions, Audit
- 8 actions: refresh, evaluate_provider, evaluate_dataset, evaluate_endpoint, evaluate_fetch_run, explain_decision, view_audit, export_report
- NO override/promote/release-all/buy/sell/order/auto-trade controls

---

## Report

File: `reports/provider_quality_gates_report.py`
- Class: `ProviderQualityGatesReport`
- 8 sections: Header, Safety Banner, Health Summary, Provider Profiles, Gate Registry, Quarantine Status, Decision Summary, Score Summary, Policy Summary, Safety Invariants, Footer

---

## Tests

File: `tests/test_provider_quality_gates_v146.py`
- 36 test classes, 206+ tests
- All offline (no real HTTP)
- In-memory SQLite for storage tests
- Fixtures in `tests/fixtures/provider_quality_gates/` (45 JSON files)

---

## Release Gate

Added 13 new checks to `ResearchFoundationReleaseGate` in
`release/research_foundation_release_gate_v139.py`:
- provider_quality_gate_registry_gate
- provider_onboarding_gates_gate
- dataset_admission_gates_gate
- formal_research_gate_gate
- backtest_input_gate_gate
- provenance_gate_gate
- pit_gate_gate
- schema_drift_gate_gate
- authority_gate_gate
- conflict_gate_gate
- quarantine_policy_gate
- quality_audit_gate
- no_hidden_blocking_failure_gate

---

[!] Research Only. No Real Orders. Not Investment Advice.
[!] This documentation does NOT enable trading or override gates.
