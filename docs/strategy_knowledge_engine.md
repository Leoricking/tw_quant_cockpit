# Strategy Knowledge Engine — Documentation

**TW Quant Cockpit v0.3.6 (core) + v0.3.6 Phase 2**

---

## Overview

The Strategy Knowledge Engine aggregates rule-based trading signals from 8 老王 teaching modules into a unified `strategy_signals` dict. It is a research and analysis aid only — it does NOT connect to any brokerage API and does NOT execute orders.

**No real-money trading. No API connections. Research use only.**

---

## Module List

### v0.3.6 Core

| Module | File | Teaching Basis |
|--------|------|----------------|
| Capital Allocation | `risk/position_sizing.py` | 20201112 資金如何分批佈局 |
| Holding Period | `analysis/holding_period_analyzer.py` | 20201119 短線與波段操作的依據 |
| Volume Behavior | `features/volume_behavior.py` | 20220406 成交量(上) |
| MACD Bull Pullback | `features/macd_strategy_features.py` | 20220504 MACD 關鍵買進訊號這樣用 |
| MACD Bear Rebound | `features/macd_strategy_features.py` | 20220518 MACD 出現這狀況要小心 |
| Valuation River | `analysis/valuation_river_analyzer.py` | 20220601 本益比河流圖 |
| Exit Point | `analysis/exit_point_analyzer.py` | 20201028 如何短線賣高點回檔不急著買 |
| Big Swing MA | `analysis/holding_period_analyzer.py` | 20201105 大波段不只看 X 日均線 |

### v0.3.6 Phase 2

| Module | File | Purpose |
|--------|------|---------|
| KD Advanced | `features/kd_advanced.py` | KD high/low golden-death cross, sticky, divergence |
| Short Interest | `features/short_interest_features.py` | Short squeeze fuel, weak-stock short increase |
| Bottom Reversal | `analysis/bottom_reversal_analyzer.py` | Breakdown reversal / deep-pullback rebound |
| Sector Rotation | `analysis/sector_rotation_analyzer.py` | Leader-laggard, sector linkage, parent-child theme |
| Fundamental Quality | `analysis/fundamental_quality_analyzer.py` | Revenue/EPS/margin earnings guard |

### Aggregator

| Module | File | Role |
|--------|------|------|
| Strategy Knowledge Engine | `analysis/strategy_knowledge_engine.py` | Combines all sub-engines into unified dict |

---

## Data Requirements Per Module

| Module | Required | Optional | Fallback |
|--------|----------|----------|---------|
| Volume Behavior | `close`, `volume` (5+ bars) | `high`, `low` | Returns zeros |
| MACD Strategy | `close` (30+ bars) | — | Returns NEUTRAL |
| KD Advanced | `close` (9+ bars) | `high`, `low`, `k`, `d` | Estimates from close only |
| Short Interest | `close` (3+ bars) | `margin_df.short_balance` | Returns UNAVAILABLE |
| Bottom Reversal | `close`, `high`, `low` (10+ bars) | — | Returns NONE |
| Sector Rotation | `close` (20+ bars) | `sector_peers`, `leader_df` | Returns UNAVAILABLE |
| Fundamental Quality | Any of: `monthly_revenue_rows`, `eps_ttm`, `gross_margin` | all fields | Returns PARTIAL |
| Valuation River | `current_price` + (`estimated_eps` or `trailing_eps`) | PE bands | Returns UNAVAILABLE |
| Holding Period | `close` (5+ bars) | `entry_price`, `institution_buying` | Returns UNKNOWN |
| Exit Point | `close`, `open`, `high`, `low`, `volume` (3+ bars) | `take_profit_price`, `institution_net` | Returns minimal |
| Capital Allocation | `portfolio_value`, `n_positions` | `entry_price`, `atr` | Returns estimates |

---

## Fallback Behavior

All modules follow this convention:

- **Data missing entirely** → signal field = `"UNAVAILABLE"`, score = 0.0, reason explains what is missing
- **Partial data** → signal field = `"PARTIAL"`, score is conservative, reason notes what is estimated
- **Module exception** → logged as WARNING, empty dict returned, section shows `"unavailable"`
- **No crash** — every module wraps its computation in try/except

---

## Data Leakage Prevention

These rules are enforced throughout:

1. **KD divergence**: Only uses past bars (t-1 and earlier). No look-ahead into future highs/lows.
2. **Bottom reversal**: Confirmation requires the "next day" to already be in the data (`last - 1`). Today's bar (`last`) is treated as unconfirmed.
3. **Sector correlation**: Only uses rolling 60-day past data. Never uses full-period correlation.
4. **Support/resistance**: Only uses rolling windows (20-day, 60-day), not all-time extremes.
5. **Fundamental data**: **TODO** — future versions must use `announcement_date` to ensure no post-announcement data is used for pre-announcement decisions. Until then, all fundamental scores are marked PARTIAL.
6. **Feature / label separation**: `future_return` is never a feature. Scalers must NOT be fit on the full dataset.

---

## How to Run strategy-preview

```bash
# Real mode (uses CSV data from data/import/)
python main.py strategy-preview --stock 2454 --mode real

# Mock mode (uses seeded random prices for demo)
python main.py strategy-preview --stock 2454 --mode mock
```

**Real mode**: If CSV data is insufficient, shows `[WARN] real data insufficient` and exits cleanly. Does NOT fall back to mock prices.

**Mock mode**: Uses seeded random OHLCV data. Only for demonstration.

### Output Sections

1. **Position Plan** — batch sizing, take-profit half, trailing stop
2. **Holding Period** — mode (SHORT_TERM / SWING / TRUST_TREND), trailing MA rule
3. **Volume Behavior** — breakout confirmation, roll-up score, spike risk
4. **MACD** — bull pullback buy, wait confirm, fake reclaim, rebound status
5. **Valuation** — PE zone, fair value, warning
6. **Phase 2: KD Advanced** — signal, sticky, divergence
7. **Phase 2: Short Interest** — squeeze fuel score, signal
8. **Phase 2: Bottom Reversal** — signal, entry, stop, target
9. **Phase 2: Sector Rotation** — signal, leader, linkage score
10. **Phase 2: Fundamental Quality** — score, warnings
11. **Exit / Re-entry** — relative high signal, pullback rebuy conditions
12. **No Chase / No Panic Sell / Do Not Rebuy Yet** — compiled reasons
13. **Final Strategy Decision** — aggregated decision + warnings

---

## How to See Results in stock-report

```bash
python main.py stock-report --stock 2454 --mode real
```

Section 9 of the report is "策略知識引擎判斷（v0.3.6）". It displays all sub-module outputs. If a module lacks data, it shows `unavailable` or `partial` for that section only — the rest of the section still renders.

---

## Important Limitations

- **Not investment advice.** All outputs are research-only signals.
- **No real-order execution.** `TWQC_ENABLE_REAL_ORDER` is always disabled.
- **No Shioaji, no Mega API.** This tool does not connect to any broker.
- **Fundamental data is time-sensitive.** Use `announcement_date` guards once API is available (v0.4+).
- **All PE / EPS conclusions are PARTIAL** until real-time earnings API is integrated.
- **Mock mode prices are random seeds.** Never use them for actual trading decisions.

---

## Version History

| Version | Changes |
|---------|---------|
| v0.3.6 core | Volume behavior, MACD strategy, holding period, valuation river, exit point, capital allocation |
| v0.3.6 Phase 2 | KD advanced, short interest, bottom reversal, sector rotation, fundamental quality; real-mode fix; provider-status fix |
| v0.3.7 (planned) | Strategy Knowledge Backtest — validate each rule against historical data |
| v0.4 (planned) | TWSE / TPEx / MOPS / data.gov.tw API integration |
