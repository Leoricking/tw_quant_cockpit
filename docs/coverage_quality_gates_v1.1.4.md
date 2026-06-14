# Coverage Quality Gates v1.1.4

**TW Quant Cockpit — Research Only. No Real Orders.**

> Quality Gate does NOT enable trading. Mock/Stale/Conflict/Invalid data cannot pass FORMAL gate. Override is DISABLED by default.

---

## Overview

Coverage Quality Gates (v1.1.4) provides a systematic data-eligibility evaluation layer for the TW Quant Cockpit research workflow. Every symbol and dataset is evaluated against named gates before being admitted to research pipelines. The gate produces an eligibility decision — it does not execute orders, repair data, or trigger automated actions.

**Gate Levels:**
- `FORMAL` — Full research eligibility. Real source, ≥240 rows, ≥98% completeness, no invalid OHLC, no conflict, no future/regression date, FRESH/ACCEPTABLE freshness.
- `OBSERVATIONAL` — Limited research use. ≥120 rows, ≥90% completeness, no invalid OHLC/conflict/future date.
- `DEMO` — Demo and dry-run only.
- `BLOCKED` — Ineligible. Symbol cannot proceed through research pipeline.

---

## Safety Guarantees

| Constraint | Value |
|---|---|
| `NO_REAL_ORDERS` | `True` |
| `BROKER_DISABLED` | `True` |
| `MOCK_DATA_FORMAL_GATE_ALLOWED` | `False` |
| `STALE_DATA_FORMAL_GATE_ALLOWED` | `False` |
| `CONFLICT_DATA_FORMAL_GATE_ALLOWED` | `False` |
| `INVALID_DATA_FORMAL_GATE_ALLOWED` | `False` |
| `QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT` | `True` |
| Override max level | `OBSERVATIONAL` (never FORMAL) |
| Override scope | Audit-only, research-only |

---

## 12 Named Gates

| Gate Name | Primary Dataset | Description |
|---|---|---|
| `price_backtest` | daily_price | Price history for backtest eligibility |
| `buy_point` | daily_price | Buy-point pattern detection readiness |
| `screener` | daily_price | Screener eligibility |
| `strategy_knowledge` | daily_price | Strategy knowledge base readiness |
| `kd_advanced` | daily_price | KD stochastic advanced analysis |
| `short_interest` | short_interest | Short interest data coverage |
| `bottom_reversal` | daily_price | Bottom reversal pattern analysis |
| `sector_rotation` | daily_price | Sector rotation readiness |
| `fundamental_quality` | fundamentals | Fundamental data quality gate |
| `stock_report` | daily_price | Stock report generation readiness |
| `local_assistant` | daily_price | Local assistant dataset eligibility |
| `kb_context` | daily_price | Knowledge base context readiness |

---

## Decision Codes

| Code | Level | Meaning |
|---|---|---|
| `ELIGIBLE_FORMAL` | FORMAL | Full eligibility |
| `ELIGIBLE_OBSERVATIONAL` | OBSERVATIONAL | Limited research use |
| `DEMO_ONLY` | DEMO | Demo and dry-run only |
| `BLOCKED_DATA_QUALITY` | BLOCKED | General data quality block |
| `BLOCKED_MOCK_DATA` | BLOCKED | Mock/fixture source — cannot be overridden to FORMAL |
| `BLOCKED_STALE_DATA` | BLOCKED | Data too stale |
| `BLOCKED_INVALID_DATA` | BLOCKED | Invalid OHLC or data integrity failure |
| `BLOCKED_CONFLICT` | BLOCKED | Conflicting rows — cannot be overridden to FORMAL |
| `BLOCKED_MISSING_REQUIRED` | BLOCKED | Required dataset missing |
| `BLOCKED_FUTURE_DATE` | BLOCKED | Future-dated rows detected |
| `BLOCKED_DATE_REGRESSION` | BLOCKED | Date regression detected |

---

## Confidence Levels

- `RELIABLE` — High confidence, full formal eligibility.
- `OBSERVATIONAL` — Moderate confidence, limited research use.
- `INSUFFICIENT` — Below minimum thresholds.
- `DEMO_ONLY` — Demo use only.
- `UNKNOWN` — Cannot determine confidence.

---

## CLI Commands

```bash
# Health check
python main.py quality-gate-health

# Evaluate a single symbol
python main.py quality-gate-symbol --stock 2454 --gate price_backtest

# Evaluate a tier
python main.py quality-gate-universe --tier research30 --gate price_backtest

# Build full gate matrix
python main.py quality-gate-matrix --tier core10

# Show latest summary
python main.py quality-gate-summary

# List formal eligible symbols
python main.py quality-gate-formal

# List observational symbols
python main.py quality-gate-observational

# List blocked symbols
python main.py quality-gate-blocked

# Filter by reason code
python main.py quality-gate-reasons --reason PRICE_DATA_MISSING

# Explain a specific decision
python main.py quality-gate-explain --decision-id <id>

# Build report
python main.py quality-gate-report --tier research30

# Override request (disabled by default, audit-only)
python main.py quality-gate-override-request \
  --decision-id <id> --level OBSERVATIONAL \
  --reason "Interim research access" \
  --allow-research-override
```

---

## Python API

```python
from quality_gates.gate_decision_engine import CoverageQualityGateEngine

engine = CoverageQualityGateEngine()

# Evaluate single symbol
dec = engine.evaluate_symbol("2454", "price_backtest")
print(dec.gate_level, dec.decision, dec.confidence)

# Evaluate universe
result = engine.run(tier="research30", gate_name="price_backtest")
print(result["decisions"])

# Build gate matrix
matrix = engine.build_gate_matrix(tier="core10")

# Get formal eligible symbols
formal = engine.allowed_symbols(result["decision_objects"])

# Health check
from quality_gates.gate_health import CoverageQualityGateHealthCheck
checker = CoverageQualityGateHealthCheck()
report = checker.run_all()
print(checker.format_report(report))
```

---

## FORMAL Gate Thresholds (price_backtest)

| Criterion | FORMAL Threshold | OBSERVATIONAL Threshold |
|---|---|---|
| Source | Real (not mock) | Any non-mock |
| Minimum rows | ≥240 | ≥120 |
| Completeness | ≥98% | ≥90% |
| Invalid OHLC | 0 | 0 |
| Conflicting rows | 0 | 0 |
| Future-dated rows | 0 | 0 |
| Date regression | 0 | 0 |
| Freshness | FRESH or ACCEPTABLE | Any non-CRITICAL |
| Source interruption | None | — |
| Critical repairs | 0 | — |

---

## Override Policy

- Override is **DISABLED by default** (`QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT = True`)
- `BLOCKED_MOCK_DATA`, `BLOCKED_INVALID_DATA`, `BLOCKED_CONFLICT` **cannot be overridden to FORMAL**
- Maximum override level: `OBSERVATIONAL`
- All overrides are `audit_only=True` and `research_only=True`
- Override does **NOT** affect broker execution or enable trading

---

## Data Persistence

Runtime outputs are saved to `data/quality_gate_reports/` (gitignored):

| File | Content |
|---|---|
| `symbol_gate_decisions.csv` | Per-symbol gate decisions |
| `universe_gate_summary.csv` | Universe-level summary |
| `gate_matrix.csv` | Full gate matrix |
| `gate_execution_filter.csv` | Eligibility filter dict |
| `gate_overrides.csv` | Override records |
| `gate_run_history.csv` | Run history log |
| `gate_reason_codes.csv` | Reason code metadata |

---

## Integration Notes

- **v1.1.3 Data Freshness Monitor**: Freshness status feeds into gate freshness evaluation.
- **v1.1.2 Coverage Repair**: Repair history feeds into critical-repair check.
- **v1.1.1 Data Import Onboarding**: Import source type feeds into mock-source detection.
- **v1.1.0 Universe Expansion**: Tier definitions feed into universe gate evaluation.

---

*v1.1.4 — Coverage Quality Gates — Research Only. No Real Orders.*
