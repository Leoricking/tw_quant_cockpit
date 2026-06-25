# Paper Strategy Orchestration v1.6.2

> [!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.

## Overview

Version 1.6.2 adds the **Paper Strategy Orchestration** layer on top of the v1.6.0 Live Paper Trading Foundation. It provides a complete research-only framework for evaluating trading signals, running them through a 19-step decision pipeline, and generating paper order proposals.

**No real orders are placed. No broker is connected. No real capital is at risk.**

## Safety Model

All strategy instances, signals, decisions, and proposals carry permanent safety labels:

| Flag | Value |
|---|---|
| `paper_only` | `True` |
| `research_only` | `True` |
| `simulation_only` | `True` |
| `not_a_real_order` | `True` |
| `no_broker_call` | `True` |
| `no_real_account` | `True` |
| `broker_execution_enabled` | `False` |
| `production_trading_blocked` | `True` |
| `short_selling_enabled` | `False` |
| `margin_enabled` | `False` |

## Signal Types

Permitted: `ENTRY_LONG`, `EXIT_LONG`, `HOLD`, `REDUCE_RESEARCH`, `BLOCK`, `ALERT`

**Permanently forbidden**: `ENTRY_SHORT`, `SELL_SHORT`, `MARGIN_LONG`, `MARGIN_SHORT`

## Decision Pipeline (19 Steps)

| Step | Check |
|---|---|
| 01 | Validate strategy (registered, running) |
| 02 | Validate signal (type, safety flags) |
| 03 | Check duplicate (dedup window) |
| 04 | Check cooldown (per-ticker) |
| 05 | Check rate limits (signals/minute) |
| 06 | Build context |
| 07 | Check market state |
| 08 | Check data quality |
| 09 | Check PIT validity |
| 10 | Check eligibility |
| 11 | Run sizing |
| 12 | Run correlation |
| 13 | Run risk controls |
| 14 | Resolve conflicts |
| 15 | Apply approval policy |
| 16 | Build proposal |
| 17 | Submit to paper order machine |
| 18 | Journal |
| 19 | Create lineage |

Steps 17–19 are handled by the orchestrator after the pipeline returns `APPROVED`.

## Approval Modes

- **`MANUAL_REQUIRED`** (default): Pipeline returns `DEFERRED`. Human must explicitly approve.
- **`AUTO_PAPER_ONLY`**: Auto-approved only when all safety conditions are met. Disabled by default (`AUTO_PAPER_ONLY_ENABLED_BY_DEFAULT = False`).

## Conflict Resolution

Default policy: **`MOST_CONSERVATIVE`** — prefer `EXIT_LONG` / `BLOCK` over `ENTRY_LONG`.

Other policies: `FIRST_WINS`, `HIGHEST_STRENGTH`, `LATEST_WINS`, `BLOCK_ALL`.

## Module Structure

```
paper_trading/strategy/
  __init__.py                    # Safety flags
  enums_v162.py                  # All enumerations
  models_v162.py                 # Data models (dataclasses)
  validation_v162.py             # Input validation
  strategy_base_v162.py          # Abstract base class
  strategy_registry_v162.py      # Thread-safe registry
  strategy_config_v162.py        # Config builder/loader
  strategy_state_v162.py         # Runtime state tracker
  strategy_lifecycle_v162.py     # Lifecycle manager
  signal_v162.py                 # Signal creation helpers
  signal_normalizer_v162.py      # [-1, 1] normalization
  signal_dedup_v162.py           # Sliding-window dedup
  trigger_v162.py                # Trigger engine
  decision_context_v162.py       # Context builder
  decision_pipeline_v162.py      # 19-step pipeline
  eligibility_adapter_v162.py    # Eligibility checks
  sizing_adapter_v162.py         # Position sizing (v1.5.1 integration)
  correlation_adapter_v162.py    # Correlation checks (v1.5.2 integration)
  risk_adapter_v162.py           # Risk controls (v1.5.3/v1.5.9 integration)
  approval_v162.py               # Approval policy
  conflict_resolution_v162.py    # Conflict resolver
  cooldown_v162.py               # Per-ticker cooldown
  rate_limit_v162.py             # Sliding-window rate limiter
  proposal_v162.py               # Proposal builder
  order_bridge_v162.py           # Bridge to paper order machine
  journal_v162.py                # Strategy journal
  checkpoint_v162.py             # Checkpoint manager
  replay_v162.py                 # Signal replay
  recovery_v162.py               # State recovery
  lineage_v162.py                # Lineage tracker
  reproducibility_v162.py        # Reproducibility verifier
  explain_v162.py                # Decision explainer
  store_v162.py                  # In-memory + file store
  query_v162.py                  # Query service
  health_v162.py                 # Health check (34 checks)
```

## Version Info

```
VERSION = "1.6.2"
RELEASE_NAME = "Paper Strategy Orchestration"
BASE_RELEASE = "1.6.1.1 Market Data Session Warning Hygiene Hotfix"
```

---

*[!] NOT INVESTMENT ADVICE. Research and simulation only.*
