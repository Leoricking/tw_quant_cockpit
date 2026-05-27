# 台股時光機核心特徵說明 — Time Machine Features

TW Quant Cockpit v0.3.4 integrates two advanced feature groups inspired by
the "台股時光機" (Taiwan Stock Time Machine) concept:

1. **Volume Profile (分價量)** — `features/volume_profile.py`
2. **Opening Microstructure (開盤 15 分鐘微觀特徵)** — `features/microstructure.py`

---

## 1. Volume Profile (分價量)

### Concept

Volume Profile distributes historical trading volume across price levels
rather than across time.  The price level with the most accumulated volume is
the **Point of Control (POC)**.  The 70% volume concentration zone is the
**Value Area (VA)**.

### Features Produced

| Column | Description |
|---|---|
| `vp_peak_price` | POC — price level with maximum accumulated volume |
| `vp_peak_volume` | Volume at the POC |
| `vp_distance_to_peak` | (close − POC) / close — positive = above POC |
| `vp_cluster_strength` | POC volume / total window volume (concentration) |
| `vp_support_score` | Fraction of volume below current close (support depth) |
| `vp_pressure_score` | Fraction of volume above current close (resistance depth) |
| `support_pressure_score` | Net score = support_score − pressure_score |
| `vp_poc_pct` | POC position within 52-week price range (0–1) |
| `vp_value_area_high` | Upper bound of Value Area (70% of volume) |
| `vp_value_area_low` | Lower bound of Value Area (70% of volume) |
| `vp_price_in_value_area` | 1 if close is inside Value Area, else 0 |

### Interpretation

| Condition | Signal |
|---|---|
| `close < vp_peak_price` and `distance_to_peak` close to 0 | Approaching overhead resistance |
| `close > vp_peak_price` with volume > 1.5× avg | Breakout above resistance — increased confidence |
| `support_pressure_score` strongly positive | Strong volume floor below price |
| `support_pressure_score` strongly negative | Heavy volume ceiling above price |
| `vp_price_in_value_area = 1` | Price in fair-value zone — less directional signal |

### Data Leakage Prevention

**Risk:** Computing POC over the full dataset and back-filling history creates
forward-looking bias.

**Solution (implemented):**
- Each row uses only a **rolling lookback window** of the past N days
  (default 60 bars).
- Row T includes bars `[T − lookback + 1 … T]` — never future data.
- Global POC calculation is strictly prohibited in the feature pipeline.

---

## 2. Opening Microstructure (開盤 15 分鐘微觀特徵)

### Concept

The first 15 minutes of each trading session reveal smart-money intent before
retail participants fully engage.  Strong opening microstructure (high
buy-side pressure, volume above average) increases confidence in directional
moves.  Weak microstructure despite a price surge is a red flag for fake
breakouts.

### Features Produced

| Column | Description | Source |
|---|---|---|
| `opening_return_15m` | Return from open to 15-min window | Intraday (proxy if daily only) |
| `opening_volume_ratio` | Opening volume vs N-day avg | Intraday (proxy if daily only) |
| `opening_high_break` | 1 if opening breaks above prev-day high | Daily OHLCV |
| `opening_low_break` | 1 if opening breaks below prev-day low | Daily OHLCV |
| `large_trade_ratio` | Fraction of large-lot volume | Tick (proxy if no tick) |
| `buy_sell_pressure` | (close − low) / (high − low) — buy-side proxy | Daily OHLCV |
| `microstructure_score` | Composite [0, 1] — higher = stronger buy pressure | All above |
| `ms_fake_breakout_risk` | 1 if gap-up but close near open with weak volume | Daily OHLCV |
| `ms_no_chase_flag` | 1 if price +2%+ but microstructure_score < 0.4 | All above |

### Microstructure Score Components

```
microstructure_score =
    0.40 × buy_sell_pressure
  + 0.30 × large_trade_ratio (normalised)
  + 0.30 × opening_volume_ratio (normalised, capped at 1.0)
```

Range: `[0, 1]`.  Score ≥ 0.7 indicates strong buy-side confirmation.
Score < 0.4 indicates weak buying, increasing fake-breakout risk.

### Operating Modes

**Mode 1 — Daily OHLCV only (default, always available):**
- All features use end-of-day proxies.
- `opening_return_15m` = half of (high − open) / open.
- `opening_volume_ratio` = today's volume / 20-day avg.
- `large_trade_ratio` = volume / (2 × avg_volume), capped at 1.0.
- Labels: proxy values, not true intraday measurements.

**Mode 2 — Intraday per-minute bars (when available):**
- `opening_return_15m` = true return from 09:00 to 09:15.
- `opening_volume_ratio` = annualised 15-min volume / avg daily volume.
- `buy_sell_pressure` = actual buy_volume / (buy_volume + sell_volume).

**Mode 3 — Tick data (when available):**
- `large_trade_ratio` = lot-size-filtered buy volume / total volume.
- `buy_sell_pressure` = tick-classified buy/sell imbalance.

### Fallback When Data Is Missing

| Missing Data | Fallback Behaviour |
|---|---|
| No intraday / tick | All features use daily OHLCV proxies |
| No `buy_volume` / `sell_volume` cols | Use Williams %R proxy from OHLC |
| No bidask data | `bid_ask_imbalance = NaN` |
| Insufficient history (< 5 bars) | Features remain NaN |
| `intraday_df = None` | System continues without crash |

The trainer, ensemble, selector, and reports handle `NaN` / missing
microstructure columns gracefully.

### Data Leakage Prevention

**Risk 1 — Opening window leakage:**
Using data after 09:15 to compute opening microstructure.

**Solution:** Intraday features use only bars with `datetime <= open_time + 15min`.

**Risk 2 — Daily proxy for intraday:**
Daily OHLCV is known only at market close, so `opening_return_15m` from daily
data is a **proxy** (not the true opening signal).  In backtests, this feature
is already available at the close of each bar — it does not look forward.

**Risk 3 — Backtest time-slice alignment:**
When replaying history, each bar's features use only data available up to and
including that bar's close.  No future bars are touched.

---

## Integration with Strategy Selector

| Condition | Selector Action |
|---|---|
| `market_regime == bull` AND `microstructure_score >= 0.7` | Increase breakout / momentum score |
| `near_volume_pressure` (close approaching POC from below) | Reduce chase score; add warning |
| `close > vp_peak_price` AND `volume > 1.5× avg` | Increase breakout score; note confirmation |
| `return_today > 3%` AND `microstructure_score < 0.4` | Flag fake breakout; reduce chase score |

---

## Integration with Reports & Dashboard

Reports include:
- Volume Profile support/pressure table (POC, distance, score)
- Opening 15-min microstructure metrics (score, fake-breakout flag)
- Model recommendation reasons citing volume and microstructure signals
- No-chase reasons with specific volume/microstructure basis
- Model review section (看對/看錯復盤) with signal vs actual return

Dashboard panels:
- 分價量支撐壓力表
- 開盤 15 分鐘強弱榜
- 模型推薦理由
- 真假突破風險提示

When data is unavailable, UI shows "No intraday data yet" / "Microstructure
unavailable" rather than crashing.

---

*Last updated: v0.3.4*
