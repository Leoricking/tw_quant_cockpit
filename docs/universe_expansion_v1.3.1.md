# Universe Expansion Foundation — v1.3.1

**Release:** v1.3.1 Universe Expansion Foundation
**Date:** 2026-06-19
**Status:** Done
**Baseline:** 730 passed → 826 passed, 0 failed, 0 errors

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] Universe Ready ≠ Tradeable. Not Investment Advice.
> [!] No real market API. No auto-download. No mock fallback.

---

## Overview

v1.3.1 introduces the **Universe Expansion Foundation** — a local-only, research-grade universe management system for Taiwan stock symbols. It provides symbol registry, coverage analysis, batch quality scanning, file import, and CLI commands, all behind strict safety walls.

This release builds on:
- v1.3.0 Real Data Quality Foundation (DataCompletenessGate — unchanged, sealed)
- v1.2.9 Replay Training Stable Rollup (sealed, backward-compatible)
- v1.1.2 Coverage Repair (sealed)

---

## Safety Invariants (Permanent — Never Modify)

| Flag | Value |
|------|-------|
| `NO_REAL_ORDERS` | `True` |
| `BROKER_DISABLED` | `True` |
| `PRODUCTION_TRADING_BLOCKED` | `True` |
| `DRY_RUN_DEFAULT` | `True` |
| `MOCK_FALLBACK_ENABLED` | `False` |
| `UNIVERSE_REAL_API_CONNECTED` | `False` |
| `UNIVERSE_AUTO_DOWNLOAD_ENABLED` | `False` |
| `UNIVERSE_READY_MEANS_TRADEABLE` | `False` |

---

## New Modules

### `universe/models.py`

Core data models for universe management.

**Enums:**
- `UniverseMarket`: TWSE, TPEx, EMERGING, UNKNOWN
- `SecurityType`: STOCK, ETF, WARRANT, REIT, PREFERRED, DR, UNKNOWN
- `ListingStatus`: LISTED, SUSPENDED, DELISTED, UNKNOWN
- `UniverseTier`: CORE, RESEARCH, EXTENDED, WATCHLIST, EXCLUDED
- `CoverageStatus`: READY, PARTIAL, MISSING, STALE, BLOCKED, UNAVAILABLE, DEMO_ONLY, EXCLUDED

**Dataclasses:**
- `UniverseSymbol` — full symbol record with 25+ fields
- `UniverseMembership` — symbol-to-universe assignment with tier
- `UniverseDefinition` — universe metadata (id, name, description, source)
- `UniverseCoverageRecord` — per-symbol coverage result (missing values = `None`, not 0)
- `UniverseSummary` — aggregate counts across a universe

### `universe/symbol_normalizer.py`

Taiwan stock symbol normalization and validation.

**Rules:**
- Accepts: 4–6 digit numeric symbols (e.g., `2330`, `00878`, `910708`)
- Rejects: Chinese names, foreign alphabetic tickers (labeled UNSUPPORTED, not invalid), empty strings
- Extension suffixes: `.TW` → TWSE, `.TWO` → TPEx
- Prefix forms: `TWSE:2330`, `TPEx:2454`, `TPEX:2454`
- Leading-digit market inference: 1,2,3,8 → TWSE; 4,5,6 → TPEx; ambiguous → UNKNOWN (never guess)
- Result: `NormalizedSymbolResult(normalized_symbol, detected_market, is_valid, warning)`

### `universe/registry_v131.py`

Lightweight JSON-backed symbol registry (runtime only — not committed).

**Features:**
- `register_symbol(dict) -> (bool, str)`: market conflict → BLOCKED; same-market duplicate → safe merge
- `update_symbol(symbol, updates) -> (bool, str)`: preserves source and registered_at
- `assign_tier(symbol, universe_id, tier, ...)`: creates/updates UniverseMembership
- `get_symbol(symbol)`, `list_symbols(tier, market)`, `list_memberships(universe_id)`
- JSON persistence: `symbols.json`, `memberships.json` (schema version 1.3.1)
- Forward-compatible: unknown JSON fields are silently ignored on load

**Storage location (runtime only, gitignored):**
```
data/universe_registry_runtime/
```

### `universe/definitions_v131.py`

Built-in seed universe definitions. All labeled `BUILT_IN_SEED` — not real market master data.

**Built-in universes:**
| Universe ID | Name | Size |
|-------------|------|------|
| `core_14` | Core 14 | 14 symbols |
| `research_19` | Research 19 | 19 symbols |
| `extended` | Extended | 30 symbols |
| `watchlist` | Watchlist (config/watchlist.csv) | variable |
| `excluded` | Excluded | empty (placeholder) |

**Core 14 symbols:** 2330, 2308, 2345, 2454, 6669, 3661, 3228, 5274, 2376, 2383, 6213, 2382, 2356, 3706

> All built-in definitions have `source="BUILT_IN_SEED"` and clearly labeled as NOT REAL_MARKET_MASTER.

### `universe/importer_v131.py`

Local file importer for universe metadata (CSV, JSON). No network access.

**Methods:**
- `preview(path, fmt)` — inspect file structure, no changes
- `validate(path, fmt)` — validate all rows, detect conflicts/duplicates, no changes
- `dry_run(path, fmt)` — show what would happen, no changes
- `execute(path, fmt, registry)` — import into registry (labels as IMPORT_FILE, not REAL_MARKET_MASTER)

**Supported formats:** CSV (with header), JSON (`{"symbols": [...]}` or list)

**Rules:**
- Default: dry-run
- No destructive replace, no deleting existing registrations
- Market conflict → BLOCKED
- Invalid symbol → skipped with error logged
- Unknown security type → mapped to UNKNOWN
- Imported symbols labeled "NOT REAL_MARKET_MASTER"

### `universe/coverage_analyzer_v131.py`

Per-symbol and per-universe coverage analysis, integrated with DataCompletenessGate (v1.3.0).

**Methods:**
- `analyze_symbol(symbol, profile, registry, quality_gate) -> UniverseCoverageRecord`
- `analyze_universe(universe_id, profile, ...) -> List[UniverseCoverageRecord]`

**Coverage profiles:**
| Profile | Use Case |
|---------|----------|
| `default` | General purpose |
| `stock_screening` | Broad scan, relaxed thresholds |
| `precise_price` | Precise OHLCV, tight thresholds |
| `backtest` | Full historical coverage |
| `abc_buy_point` | ABC pattern detection |

**CoverageStatus mapping from DataQualityStatus:**
- PASS → READY
- WARN → PARTIAL
- FAIL → BLOCKED
- Missing data → UNAVAILABLE
- Demo data → DEMO_ONLY
- Excluded → EXCLUDED

### `universe/scanner.py`

Batch quality scanner across universe, tier, or symbol list.

**Features:**
- `scan_symbol(symbol, profile)` → single scan
- `scan_universe(universe_id, profile)` → full universe batch
- `scan_tier(tier, profile)` → all symbols of a tier
- `scan_symbols(symbols, profile)` → arbitrary list
- `summarize(records)` → aggregate counts
- `cancel()` — graceful cancellation
- `list_ready/partial/blocked/unavailable/demo_only(records)` — filter helpers
- `MAX_SCAN_DEFAULT = 500` (safety cap)

---

## New CLI Commands

All commands are research-only. No writes without explicit `--execute` flag.

### `universe-list-v131`

List universe definitions.

```bash
python main.py universe-list-v131
python main.py universe-list-v131 --tier core
python main.py universe-list-v131 --market TWSE
```

Options:
- `--tier` — filter by tier (core, research, extended, watchlist, excluded)
- `--market` — filter by market (TWSE, TPEx, EMERGING)

### `universe-show-v131`

Show detail for one symbol.

```bash
python main.py universe-show-v131 --symbol 2330
```

### `universe-summary-v131`

Print summary stats for a universe.

```bash
python main.py universe-summary-v131
python main.py universe-summary-v131 --universe-id core_14
```

### `universe-coverage-v131`

Analyze coverage for a universe or symbol.

```bash
python main.py universe-coverage-v131 --symbol 2330
python main.py universe-coverage-v131 --universe-id core_14 --profile backtest
python main.py universe-coverage-v131 --profile stock_screening
python main.py universe-coverage-v131 --profile stock-screening  # dash form OK
```

Profile choices: `default`, `stock_screening`, `precise_price`, `backtest`, `abc_buy_point` (and dash forms)

### `universe-quality-scan`

Batch quality scan across all registered symbols.

```bash
python main.py universe-quality-scan
python main.py universe-quality-scan --profile precise_price
python main.py universe-quality-scan --universe-id research_19
```

### `universe-import`

Import a universe file (dry-run by default).

```bash
# Preview only (default — dry-run)
python main.py universe-import --path data/my_symbols.csv

# Validate without importing
python main.py universe-import --path data/my_symbols.csv --validate

# Execute import (with explicit flag)
python main.py universe-import --path data/my_symbols.json --format json --execute
```

> [!] `--execute` performs import into runtime registry only (gitignored, not committed).
> [!] All imported symbols are labeled IMPORT_FILE — NOT REAL_MARKET_MASTER.

### `universe-health-v131`

Health check for the universe subsystem.

```bash
python main.py universe-health-v131
```

---

## New Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `tests/test_universe_registry.py` | 12 | Registry CRUD, conflict blocking, tier assignment, JSON persistence |
| `tests/test_universe_normalizer.py` | 11 | Symbol normalization, extension parsing, market inference, rejection rules |
| `tests/test_universe_coverage.py` | 22 | Coverage analyzer (14), scanner (8) |
| `tests/test_universe_cli.py` | 13 | All 7 CLI commands via subprocess |
| `tests/test_universe_gui.py` | 8 | GUI import (4), universe panel widget (4) |
| `tests/test_universe_regression.py` | 30 | Definitions (9), importer (10), safety invariants (11) |

**Total new tests: 96**
**Suite result: 826 passed, 0 failed, 0 errors**

---

## Test Fixtures

Location: `tests/fixtures/universe/` (committed — exception to gitignore)

| File | Purpose |
|------|---------|
| `valid_universe.csv` | 5 valid TWSE symbols |
| `valid_universe.json` | Same 5 symbols in JSON format |
| `market_conflict.csv` | 2330 listed as both TWSE and TPEx |
| `invalid_symbol.csv` | Empty symbol, foreign ticker (AAPL), Chinese name |
| `duplicate_symbols.csv` | 2330 and 2308 each listed twice |

---

## Gitignore Additions (Runtime — Not Committed)

```gitignore
# v1.3.1 Universe Expansion Foundation
data/universe_registry_runtime/
data/universe_import_runtime/
universe_registry_runtime/
reports/universe_expansion_*.md
reports/universe_coverage_scan_*.md
reports/universe_quality_scan_*.md
# v1.3.1 Universe fixtures ARE committed (exception)
!tests/fixtures/universe/*.csv
!tests/fixtures/universe/*.json
```

---

## Version Info

```python
from release.version_info import (
    VERSION,                               # "1.3.1"
    RELEASE_NAME,                          # "Universe Expansion Foundation"
    UNIVERSE_REGISTRY_AVAILABLE,           # True
    UNIVERSE_COVERAGE_AVAILABLE,           # True
    UNIVERSE_BATCH_QUALITY_SCAN_AVAILABLE, # True
    UNIVERSE_REAL_API_CONNECTED,           # False
    UNIVERSE_AUTO_DOWNLOAD_ENABLED,        # False
    MOCK_FALLBACK_ENABLED,                 # False
    REAL_ORDERS_ENABLED,                   # False
)
```

---

## Backward Compatibility

All previous functionality remains intact:

- v1.2.9 Replay Training (sealed, all regression tests pass)
- v1.1.2 Coverage Repair (sealed, all regression tests pass)
- v1.1.1 Data Onboarding (sealed)
- v1.3.0 DataCompletenessGate (unchanged — universe coverage uses it, does not replace it)
- All CLI commands from prior releases continue to work unchanged

---

## What "Universe Ready" Does NOT Mean

| Claim | True? |
|-------|-------|
| Symbol is available for research/analysis | Yes (if READY) |
| Symbol has real-time price feed | **NO** |
| Symbol can be traded | **NO** |
| Symbol data is from official market master | **NO** (BUILT_IN_SEED or IMPORT_FILE) |
| Coverage means investment advice | **NO** |

---

## Related Documentation

- `docs/roadmap.md` — full release history and future roadmap
- `docs/real_data_quality_v1.3.0.md` — v1.3.0 DataCompletenessGate (foundation this release builds on)
- `docs/data_universe_expansion_v1.1.0.md` — earlier universe expansion design
- `docs/coverage_repair_workflow_v1.1.2.md` — v1.1.2 Coverage Repair (sealed)
- `docs/replay_training_stable_rollup_v1.2.9.md` — v1.2.9 Replay Training (sealed)

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
*[!] Universe Ready ≠ Tradeable. All data is local and research-grade only.*
