# datetime.utcnow() Deprecation Debt — v1.4.9

> Status: **Non-Blocking Known Limitation**
> Identified in: v1.4.9 Provider Stable Rollup
> Cleanup planned: v1.5.x or dedicated hotfix

---

## Summary

The full test suite reports approximately **1935 DeprecationWarning** instances
in v1.4.8.1/v1.4.9. All originate from `datetime.datetime.utcnow()` calls, which
is deprecated in Python 3.12 and scheduled for removal in a future Python release.

None of these warnings currently constitute a **blocking defect** (see classification
below). They are inventoried here as non-blocking known technical debt.

---

## Affected Modules

| Module | Category | Approx. Warnings |
|--------|----------|-----------------|
| `data/providers/forum/aggregation_v147.py` | Forum aggregation | ~450 |
| `release/research_foundation_release_gate_v139.py` | Release gate | ~120 |
| `release/provider_stable_release_gate_v149.py` | Stable release gate | ~90 |
| `release/provider_stable_health_v149.py` | Health check | ~80 |
| `data/stable/capability_manifest_v149.py` | Stable manifest | ~60 |
| `data/stable/provider_registry_v149.py` | Provider registry | ~60 |
| `data/stable/compatibility_contract_v149.py` | Compat contracts | ~60 |
| `data/stable/schema_version_registry_v149.py` | Schema registry | ~60 |
| `data/stable/policy_version_registry_v149.py` | Policy registry | ~60 |
| `data/stable/baseline_snapshot_v149.py` | Baseline snapshot | ~60 |
| `data/stable/collection_integrity_v149.py` | Collection integrity | ~60 |
| `data/stable/health_baseline_v149.py` | Health baseline | ~60 |
| `data/stable/provider_stable_profiles_v149.py` | Stable profiles | ~60 |
| `reports/provider_stable_rollup_report.py` | Report builder | ~45 |
| Other provider/release/report modules | Various | ~510 |

**Total: ~1935 DeprecationWarnings**

All instances use the pattern:
```python
datetime.datetime.utcnow().isoformat() + "Z"
```

---

## Risk Classification

### Non-Blocking (inventory only required)

All 1935 warnings fall into this category:

- `datetime.utcnow()` returns a **naive UTC datetime**
- All uses are for **audit timestamps** (`checked_at`, `generated_at`, `fetched_at` in
  report metadata) stored as ISO-8601 strings
- These timestamps are **never compared** against timezone-aware datetimes in the same
  code path
- No PIT (point-in-time) isolation logic depends on these audit timestamps
- No backtest engine reads these audit timestamps as data inputs
- Asia/Taipei market hours are not computed from these timestamps

### Blocking Defect Criteria (none currently triggered)

Per v1.4.9 spec, a warning becomes a **blocking defect** if it:

1. Affects PIT isolation (fetched_at / available_from semantics)
2. Causes naive/aware datetime comparison errors at runtime
3. Affects Asia/Taipei timezone correctness
4. Affects data availability computation
5. Affects formal research report output values (not just metadata timestamps)

**Current status: 0 blocking defects.**

---

## Timezone-Aware Replacement Policy

When remediated, all `datetime.utcnow()` calls should be replaced with:

```python
import datetime
datetime.datetime.now(datetime.timezone.utc)
```

Or equivalently:
```python
from datetime import datetime, timezone
datetime.now(timezone.utc)
```

The `.isoformat() + "Z"` suffix pattern should become:
```python
datetime.now(timezone.utc).isoformat()
# already includes +00:00; if "Z" suffix is required:
datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
```

---

## Migration Target

- **Target version**: v1.5.0 or dedicated `v1.4.9.1 DateTime Awareness Hotfix`
- **Priority**: Low (no runtime failures; pure deprecation warning)
- **Scope**: All modules listed above; do not mix partial migration

---

## Regression Requirements for Migration

When the migration is executed:

1. Full suite must pass with 0 warnings of this type after fix
2. All health checks must pass
3. PIT semantics for `fetched_at` and `available_from` must be verified via
   existing PIT hardening tests
4. Forum aggregation timestamps must be verified for chronological ordering
5. No naive/aware comparison `TypeError` may appear in the test run

---

## Planned Cleanup Version

**v1.5.0** — after `v1.4.9 Provider Stable Rollup` is certified stable.

Do not attempt bulk replacement during Stable Rollup. Only fix instances that
trigger the blocking defect criteria above.

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
