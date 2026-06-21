# Portfolio Research Foundation v1.5.0

**Release:** Portfolio Research Foundation  
**Version:** 1.5.0  
**Base Release:** 1.4.9 Provider Stable Rollup  
**Status:** Stable

> [!] Research Only. No Real Orders. Not Investment Advice.

## Overview

v1.5.0 introduces the Portfolio Research Foundation — a research-only portfolio data and calculation layer built on top of the v1.4.9 Provider Stable Rollup. It provides:

- Append-only Portfolio Ledger with deterministic replay
- Point-in-Time (PIT) position and valuation queries
- Cost basis calculation (Weighted Average and FIFO)
- Portfolio valuation with price authority tiers
- PnL (unrealized and realized) calculation
- Return calculation (TWR; MWR is experimental stub)
- Exposure analysis (market, asset type, industry, themes)
- Concentration analysis (HHI, effective N, warnings)
- Turnover calculation
- Benchmark comparison (default: 0050.TW)
- Immutable snapshot builder with SHA-256 integrity
- Hypothetical what-if analysis (no orders, no persistence)
- 17-check data eligibility gate
- Portfolio lineage chain tracking
- 21-method query service

## Safety Constraints (Permanent)

| Flag | Value |
|------|-------|
| RESEARCH_ONLY | True |
| BROKER_LINKED | False |
| REAL_ORDER_ENABLED | False |
| POSITION_SIZING_AVAILABLE | False |
| AUTO_REBALANCE_ENABLED | False |
| ORDER_EXECUTION_ENABLED | False |
| PRODUCTION_TRADING_BLOCKED | True |

These flags are hardcoded and cannot be changed at runtime.

## Module Structure

```
portfolio/
├── __init__.py                 # Safety flags, VERSION="1.5.0"
├── enums_v150.py               # All enums
├── models_v150.py              # Frozen dataclasses
├── validation_v150.py          # Input validation helpers
├── ledger_v150.py              # Append-only ledger
├── position_v150.py            # Position service
├── cash_v150.py                # Cash balance service
├── transaction_v150.py         # Transaction builder
├── cost_basis_v150.py          # Weighted Average & FIFO
├── valuation_v150.py           # Valuation engine
├── pnl_v150.py                 # PnL calculator
├── returns_v150.py             # TWR / MWR (experimental)
├── exposure_v150.py            # Exposure analysis
├── concentration_v150.py       # HHI & concentration
├── turnover_v150.py            # Turnover calculation
├── benchmark_v150.py           # Benchmark comparison
├── snapshot_v150.py            # Immutable snapshot builder
├── what_if_v150.py             # Hypothetical what-if
├── eligibility_v150.py         # Data eligibility gate (17+ checks)
├── point_in_time_v150.py       # PIT validator
├── lineage_v150.py             # Lineage chain tracker
├── store_v150.py               # Storage layer
├── query_v150.py               # 21-method query service
└── health_v150.py              # 32 offline health checks
```

## CLI Commands (v1.5.0 adds 17 commands)

| Command | Description |
|---------|-------------|
| portfolio-health | Run portfolio research health check |
| portfolio-create | Create a research portfolio |
| portfolio-add-txn | Add a research transaction |
| portfolio-positions | Show positions as-of date |
| portfolio-cash | Show cash balances as-of date |
| portfolio-valuation | Show portfolio valuation |
| portfolio-pnl | Show PnL summary |
| portfolio-exposure | Show portfolio exposure |
| portfolio-concentration | Show concentration analysis |
| portfolio-turnover | Show turnover metrics |
| portfolio-returns | Show return calculations |
| portfolio-benchmark | Show benchmark comparison |
| portfolio-snapshot | Take a portfolio snapshot |
| portfolio-eligibility | Run data eligibility gate |
| portfolio-what-if | Run hypothetical what-if analysis |
| portfolio-lineage | Show portfolio lineage chain |
| portfolio-report | Generate full portfolio research report |

## Key Design Decisions

### Point-in-Time (PIT)
All queries are PIT-aware: `transaction.effective_at <= as_of AND transaction.available_from <= as_of`. Price `available_from` is also validated.

### Cost Basis
- Default: Weighted Average (appropriate for TW stocks)
- Formula: `new_avg = (old_total_cost + buy_gross + allocated_fee) / (old_qty + buy_qty)`
- FIFO available as alternative

### Price Authority Tiers
- PRIMARY: TWSE, TPEx
- SECONDARY: FinMind
- MOCK/FIXTURE/TEST: Blocked for formal use (ValuationStatus=BLOCKED)

### Valuation Status
- VALID: All positions valued with PRIMARY/SECONDARY prices
- PARTIAL: Some positions missing prices
- STALE: Price data exceeds freshness threshold
- MISSING: No prices available
- BLOCKED: MOCK prices or PIT violations

### What-If
All what-if simulations are HYPOTHETICAL_ONLY. No orders created, no transactions persisted, no broker calls.

## Not Included in v1.5.0

The following are explicitly excluded and reserved for future releases:
- Position Sizing Engine → v1.5.1
- Correlation & Exposure → v1.5.2
- Drawdown & Risk Controls → v1.5.3
- Portfolio Walk-forward Backtest → v1.5.4
- PPO/RL, broker connection, real orders (permanently blocked)
