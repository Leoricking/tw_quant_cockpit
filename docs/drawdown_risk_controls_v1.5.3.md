# Drawdown & Risk Controls v1.5.3

**Version:** 1.5.3  
**Status:** STABLE  
**Research Only:** Yes — No automated trading, no broker, no orders, no ledger write.

---

## Safety Invariants

All risk controls in this module are **RESEARCH ONLY**:

- `RISK_CONTROL_RESEARCH_ONLY = True`
- `RISK_CONTROL_AUTO_APPLY_ENABLED = False`
- `RISK_CONTROL_AUTO_REDUCE_ENABLED = False`
- `RISK_CONTROL_AUTO_STOP_ENABLED = False`
- `RISK_CONTROL_AUTO_REBALANCE_ENABLED = False`
- `RISK_CONTROL_ORDER_CREATION_ENABLED = False`
- `RISK_CONTROL_ORDER_EXECUTION_ENABLED = False`
- `RISK_CONTROL_BROKER_ENABLED = False`
- `NO_REAL_ORDERS = True`
- `PRODUCTION_TRADING_BLOCKED = True`

All evaluation results carry labels:
`RESEARCH_ONLY`, `NOT_AN_AUTOMATED_CONTROL`, `NOT_A_STOP_ORDER`, `NOT_AN_ORDER`, `NO_BROKER_CALL`, `NO_LEDGER_WRITE`

---

## Module Structure

```
portfolio/risk_controls/
    __init__.py                     Safety flags and constants
    enums_v153.py                   All enums
    models_v153.py                  All dataclass models
    validation_v153.py              Input validation
    equity_curve_v153.py            Equity curve builder
    underwater_v153.py              Underwater curve
    drawdown_v153.py                Max drawdown calculation
    drawdown_episode_v153.py        Episode detection
    drawdown_duration_v153.py       Duration analysis
    drawdown_recovery_v153.py       Recovery analysis
    drawdown_attribution_v153.py    Attribution by position/industry/theme/cluster
    risk_budget_v153.py             Risk budget engine
    volatility_limit_v153.py        Volatility limit check
    loss_limit_v153.py              Daily/weekly/monthly loss limits
    concentration_limit_v153.py     Concentration risk controls
    correlation_limit_v153.py       Correlation risk controls
    liquidity_limit_v153.py         Liquidity risk controls
    cash_reserve_limit_v153.py      Cash reserve controls
    constraint_engine_v153.py       21-step evaluation engine
    sizing_impact_v153.py           Position sizing risk impact
    stress_v153.py                  Stress scenarios (8 types)
    eligibility_v153.py             Eligibility gate
    point_in_time_v153.py           PIT validator
    lineage_v153.py                 Lineage tracking
    explain_v153.py                 Explainer
    store_v153.py                   Immutable store
    query_v153.py                   Query service
    health_v153.py                  Health check
```

---

## Enums

- `DrawdownStatus`: AT_HIGH_WATER_MARK, IN_DRAWDOWN, RECOVERING, RECOVERED, UNKNOWN
- `RiskControlStatus`: PASS, WARN, BREACH, BLOCKED, UNKNOWN
- `RiskControlType`: VOLATILITY_LIMIT, DAILY_LOSS_LIMIT, WEEKLY_LOSS_LIMIT, MONTHLY_LOSS_LIMIT, DRAWDOWN_LIMIT, CONCENTRATION_LIMIT, CORRELATION_LIMIT, LIQUIDITY_LIMIT, CASH_RESERVE, RISK_BUDGET
- `RiskActionType`: NO_ACTION, WARN_ONLY, REVIEW_RECOMMENDED, REDUCE_RECOMMENDED, HALT_RECOMMENDED
- `DrawdownEpisodeStatus`: OPEN, CLOSED, PARTIAL
- `AttributionType`: POSITION, INDUSTRY, THEME, CLUSTER
- `StressScenarioType`: HISTORICAL_REPEAT, VOLATILITY_SPIKE, CORRELATION_BREAKDOWN, LIQUIDITY_CRISIS, FLASH_CRASH, BEAR_MARKET, SECTOR_ROTATION, COMBINED

---

## CLI Commands (v1.5.3)

All commands use fixture/demo data, are offline, read-only, research-only.

```
python main.py drawdown-risk-health
python main.py risk-control-policies
python main.py risk-control-policy-show --policy-id POL_VOL_001
python main.py drawdown-eligibility --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-equity-curve --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-underwater --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-drawdown --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py drawdown-episodes --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py rolling-drawdown --portfolio-id demo_portfolio --window 60 --as-of 2026-06-21
python main.py drawdown-attribution --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-risk-budget --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-loss-limits --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-volatility-limit --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-concentration-limits --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-correlation-limits --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-liquidity-limit --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py portfolio-cash-reserve --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py risk-control-evaluate --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py sizing-risk-impact --proposal-id demo_proposal --as-of 2026-06-21
python main.py drawdown-stress --scenario tests/fixtures/drawdown_risk_controls/stress_combined.json
python main.py risk-control-explain --portfolio-id demo_portfolio --as-of 2026-06-21
python main.py risk-control-show --evaluation-id <id>
python main.py risk-control-list
python main.py risk-control-lineage --evaluation-id <id>
python main.py drawdown-risk-report --portfolio-id demo_portfolio --as-of 2026-06-21
```

---

## Not Investment Advice

This module provides descriptive analytics for research purposes only.
Historical drawdown does not predict future drawdown.
Risk control evaluations are advisory — they do not automatically trigger any portfolio action.
