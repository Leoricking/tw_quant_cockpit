# Research Foundation Stable Rollup v1.3.9

**[!] Research Only. No Real Orders. Not Investment Advice.**

## Overview

Version 1.3.9 "Research Foundation Stable Rollup" freezes and stabilises the v1.3.x Research Data & Strategy Validation Foundation line (v1.3.0–v1.3.7). It introduces a central capability registry, canonical version alignment utilities, and a 10-gate release gate infrastructure that will serve as the foundation for the upcoming v1.4.x Public Data Provider Integration roadmap phase.

## What is included

### Stable Capabilities (9)

| ID | Display Name | Canonical Version |
|----|-------------|------------------|
| real_data_quality | Real Data Quality Foundation | 1.3.0 |
| universe_expansion | Universe Expansion Foundation | 1.3.1 |
| provider_adapter_foundation | Real Data Provider Adapter Foundation | 1.3.2 |
| coverage_repair | Coverage Repair Workflow | 1.3.3 |
| data_freshness | Data Freshness Monitor | 1.3.4 |
| empirical_backtest | Strategy Knowledge Empirical Backtest | 1.3.5 |
| abc_validation | A/B/C Buy Point Validation | 1.3.6 |
| strategy_robustness | Strategy Robustness & Regime Validation | 1.3.7 |
| canonical_version_alignment | Canonical Version Alignment | 1.3.7 |

### Planned Capabilities (8, v1.4.x)

twse_provider, tpex_provider, mops_provider, data_gov_tw_provider, finmind_adapter_hardening, provider_lineage_rate_limit, provider_quality_gates, forum_intelligence

## New files

- `release/capability_registry.py` — Central capability registry (17 capabilities, dependency validation, cycle detection)
- `release/version_alignment.py` — Added: `canonicalize_version`, `get_original_internal_version`, `is_known_release_lineage`, `validate_version_metadata`
- `release/research_foundation_health_v139.py` — Unified health check (7 check categories, 40+ checks)
- `release/research_foundation_release_gate_v139.py` — 10-gate release gate
- `release/research_foundation_stable_checklist_v139.py` — 20-item stable rollup checklist
- `reports/research_foundation_stable_rollup_report.py` — Report generator
- `gui/research_foundation_summary_panel.py` — Research Foundation summary panel (PyQt5 + headless fallback)

## CLI Commands

```
python main.py research-foundation-health       # Run health check
python main.py research-foundation-stable-check # Run stable checklist
python main.py research-foundation-release-gate # Run 10-gate release gate
python main.py research-foundation-summary      # Show full report
```

## Version flags (version_info.py)

```python
RESEARCH_FOUNDATION_STABLE                  = True
RESEARCH_FOUNDATION_STABLE_ROLLUP_AVAILABLE = True
REAL_DATA_QUALITY_AVAILABLE                 = True
UNIVERSE_EXPANSION_AVAILABLE                = True
EMPIRICAL_BACKTEST_AVAILABLE                = True
STRATEGY_ROBUSTNESS_AVAILABLE               = True
CANONICAL_VERSION_ALIGNMENT_AVAILABLE       = True
PUBLIC_DATA_PROVIDER_INTEGRATION_STARTED    = False
TWSE_PROVIDER_AVAILABLE                     = False
TPEX_PROVIDER_AVAILABLE                     = False
MOPS_PROVIDER_AVAILABLE                     = False
DATA_GOV_TW_PROVIDER_AVAILABLE              = False
FORUM_INTELLIGENCE_AVAILABLE                = False
AUTO_OPTIMIZATION_ENABLED                   = False
```

## Canonical Version Mapping

The v1.4.0–1.4.2 internal labels were reassigned as part of roadmap alignment. The v1.4.x namespace is now reserved for Public Data Provider Integration.

| Internal Label | Canonical Version | Feature |
|----------------|------------------|---------|
| 1.4.0 | 1.3.5 | Strategy Knowledge Empirical Backtest |
| 1.4.1 | 1.3.6 | A/B/C Buy Point Validation |
| 1.4.2 | 1.3.7 | Strategy Robustness & Regime Validation |

## Safety

- `NO_REAL_ORDERS = True`
- `BROKER_EXECUTION_ENABLED = False`
- `PRODUCTION_TRADING_BLOCKED = True`
- `MOCK_FALLBACK_ENABLED = False`
- `AUTO_OPTIMIZATION_ENABLED = False`
- `AUTO_TRADING_ENABLED = False`
- `REPLAY_STABLE_BASELINE = "1.2.9"` (unchanged)

No broker commands introduced. No trading controls in GUI panel. All planned provider capabilities correctly unavailable. Research only.

## Next

v1.4.0: TWSE Provider — Public Data Provider Integration begins.
