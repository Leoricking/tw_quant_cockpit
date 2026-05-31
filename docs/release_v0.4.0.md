# TW Quant Cockpit v0.4.0 — Research Platform Stable Release

> [!] Research Only. Backtest Only. No Real Orders. Production Trading: BLOCKED.

## Overview

v0.4.0 is the stable release of the TW Quant Cockpit research platform, consolidating v0.3.x features into a verified, documented, and regression-tested research tool for Taiwan stock market analysis.

This is not a production trading system. No real orders. No broker connections.

## What Is Stable

All v0.3.x features are now stable and regression-tested:

| Feature | Version | Status |
|---------|---------|--------|
| Daily Workflow Engine | v0.3.21 | Stable |
| Data Quality Gate | v0.3.20 | Stable |
| Provider Reliability & Fallback | v0.3.24 | Stable |
| Universe Manager | v0.3.25 | Stable |
| Hardened Backtest Engine | v0.3.26 | Stable |
| Intraday / Tick Data Pipeline | v0.3.27 | Stable |
| Strategy Rule Governance | v0.3.28 | Stable |
| Research Notebook / Experiment Registry | v0.3.29 | Stable |
| Auto Report Center | v0.3.16 | Stable |
| Signal Quality Dashboard | v0.3.14 | Stable |
| Rule Weight Tuning Lab | v0.3.15 | Stable |
| Portfolio Cockpit | v0.3.13 | Stable |
| Automation Scheduler | v0.3.17 | Stable |
| Usability QA | v0.3.22 | Stable |
| Release Status & Regression Suite | v0.4.0 | New |

## What Is NOT Production Trading

- No Shioaji connection
- No Mega Broker connection
- No real order submission
- No automatic weight application
- `production_blocked = True`
- `real_order_ready = False`

## Daily Workflow

```bash
python main.py daily-workflow --mode real --profile standard
```

## GUI Overview

```bash
python main.py cockpit --mode real
```

Tabs available: Portfolio Cockpit, Signal Quality, Rule Weight Tuning, Auto Report Center, Automation Scheduler, Provider Health, Data Provider Fetch, Data Quality Gate, Daily Workflow, Usability QA, Provider Reliability, Universe Manager, Hardened Backtest, Intraday Pipeline, Rule Governance, Experiment Registry, Release Status

## Regression Checklist

```bash
python main.py regression-suite --mode real --quick
python main.py regression-suite --mode real --full
python main.py stable-release-check --mode real
```

## Safety Model

| Flag | Value |
|------|-------|
| read_only | True |
| no_real_orders | True |
| production_blocked | True |
| real_order_ready | False |
| no_broker_connection | True |

## Known Limitations

- Research only — not for production trading
- Sample universe size affects signal quality
- Provider reliability depends on FinMind/TWSE API availability
- Intraday tick/bidask planned for v0.4+
- No ML model training in stable release

## Upgrade Notes from v0.3.x

No breaking changes. All v0.3.x CLI commands preserved. All GUI tabs preserved. New additions only.

## Next Roadmap

- v0.4.1: API Fetch Productionization
- v0.4.2: ML Feature Store v1
- v0.4.3: Model Monitoring
- v0.4.4: Intraday Replay Cockpit
- v0.4.5: Notification Center
