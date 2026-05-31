# Intraday / Tick Data Pipeline — v0.3.27

> **[!] Research Only / Intraday Research Only / No Real Orders / Not Investment Advice**
> **Production Trading: BLOCKED**

---

## Table of Contents

1. [v0.3.27 Goals](#1-v0327-goals)
2. [1min / 5min Standard Schema](#2-1min--5min-standard-schema)
3. [XQ Import Flow](#3-xq-import-flow)
4. [How to Read Intraday Quality Scores](#4-how-to-read-intraday-quality-scores)
5. [Opening Range Features](#5-opening-range-features)
6. [VWAP Features](#6-vwap-features)
7. [Fake Breakout Detection](#7-fake-breakout-detection)
8. [Intraday Volume Profile](#8-intraday-volume-profile)
9. [Tick / BidAsk Placeholder Status](#9-tick--bidask-placeholder-status)
10. [CLI Usage](#10-cli-usage)
11. [GUI Usage](#11-gui-usage)
12. [Safety Statement](#12-safety-statement)

---

## 1. v0.3.27 Goals

Version 0.3.27 introduces the **Intraday / Tick Data Pipeline** (`intraday/` package).
Key goals for this release:

- Define a standard intraday schema for 1-minute and 5-minute bar data.
- Provide a data standardization pipeline that normalizes raw XQ exports
  into a consistent, analysis-ready format.
- Implement intraday data quality checks (session coverage, missing bars,
  duplicate detection, price/volume anomalies).
- Build intraday analytical features:
  - Opening range (return, volume ratio, high/low break).
  - VWAP (intraday VWAP, price relative to VWAP, slope, reclaim/lost).
  - Fake breakout detection (risk classification, chase risk).
  - Volume profile (POC, value area, cluster strength).
- Lay the groundwork for future tick and bid/ask data integration
  (schema definitions and readiness flags only — no provider connected yet).
- Expose all results through a PySide6 GUI panel and a Markdown report builder.

**What is NOT in v0.3.27:**
- Live tick data feed.
- Live bid/ask (Level 2) data.
- Any real order or signal execution.

---

## 2. 1min / 5min Standard Schema

### Required columns (both 1min and 5min)

| Column   | Type    | Description                              |
|----------|---------|------------------------------------------|
| symbol   | str     | Stock code (e.g. "2454")                 |
| date     | str     | Trading date — "YYYY-MM-DD"              |
| time     | str     | Bar time — "HH:MM" or "HH:MM:SS"        |
| datetime | str     | Combined — "YYYY-MM-DD HH:MM:SS"         |
| freq     | str     | Frequency label — "1min" or "5min"       |
| open     | float   | Bar open price                           |
| high     | float   | Bar high price                           |
| low      | float   | Bar low price                            |
| close    | float   | Bar close price                          |
| volume   | int64   | Bar volume (shares / lots)               |
| source   | str     | File or provider name                    |

### Optional columns (both 1min and 5min)

| Column      | Type  | Description                        |
|-------------|-------|------------------------------------|
| name        | str   | Stock name (Chinese name)          |
| amount      | float | Bar turnover amount (TWD)          |
| vwap        | float | Volume-weighted average price      |
| fetched_at  | str   | Timestamp when data was fetched    |
| imported_at | str   | Timestamp when data was imported   |

---

## 3. XQ Import Flow

XQ (嘉實 XQ 全球贏家) exports intraday data as CSV or XLSX with Traditional
Chinese column headers. The pipeline automatically maps these headers.

### Step-by-step import

1. **Export from XQ**
   - In XQ, select a stock and export 1-minute or 5-minute historical bars.
   - Save the file to:
     ```
     data/import/intraday/{freq}/
     ```
     For example:
     ```
     data/import/intraday/1min/2454_1min.csv
     data/import/intraday/5min/2454_5min.csv
     ```
   - Accepted filename patterns:
     - `2454_1min.csv`
     - `2454 聯發科 1min.xlsx`
     - `2454_聯發科_1min.xlsx`

2. **Column mapping (automatic)**

   The pipeline maps XQ Traditional Chinese headers to standard names:

   | XQ Header | Standard Column |
   |-----------|----------------|
   | 開盤價     | open           |
   | 最高價     | high           |
   | 最低價     | low            |
   | 收盤價     | close          |
   | 成交量     | volume         |
   | 成交金額   | amount         |
   | 日期       | date           |
   | 時間       | time           |
   | 商品代號   | symbol         |
   | 股票代號   | symbol         |
   | 名稱       | name           |
   | 代碼       | symbol         |

3. **Run the pipeline**
   ```bash
   python -c "
   from intraday.intraday_pipeline import IntradayDataPipeline
   p = IntradayDataPipeline(freq='1min')
   print(p.run())
   "
   ```

4. **Standard output location**
   ```
   data/import/intraday_standard/1min/2454_1min.csv
   data/import/intraday_standard/5min/2454_5min.csv
   ```

---

## 4. How to Read Intraday Quality Scores

Quality scores are computed per symbol/freq. Score range: **0–100**.

### Quality status definitions

| Status         | Meaning                                                  |
|----------------|----------------------------------------------------------|
| OK             | All checks passed; data is clean and complete            |
| PARTIAL        | Session coverage < 80% (many bars missing)               |
| MISSING        | No standardized file found for this symbol               |
| STALE          | Latest date is more than 5 trading days old              |
| INSUFFICIENT   | Less than 50 rows — not enough for analysis              |
| DUPLICATED     | More than 5 duplicate (symbol, date, time) rows          |
| PRICE_ANOMALY  | At least 1 row where high < low or close outside range   |
| VOLUME_ANOMALY | More than 10 rows with zero volume or extreme spikes     |

### Score deductions

| Issue                    | Deduction                        |
|--------------------------|----------------------------------|
| Coverage < 80%           | −30 × (1 − coverage ratio)       |
| Missing bars > 10        | −10                              |
| Duplicate rows > 0       | −10                              |
| Price anomaly count > 0  | −20                              |
| Stale data               | −40                              |
| Insufficient rows        | −50                              |

### Expected bars per trading day

| Frequency | Expected bars |
|-----------|--------------|
| 1min      | 270 (09:00–13:30) |
| 5min      | 54            |

---

## 5. Opening Range Features

The opening range is defined as the first **15 minutes** of each trading session
(09:00–09:14 inclusive for 1-minute data).

### Feature definitions

| Feature                    | Description                                                        |
|----------------------------|--------------------------------------------------------------------|
| `opening_return_5m`        | (close at 5m − first_open) / first_open                           |
| `opening_return_15m`       | (close at 15m − first_open) / first_open                          |
| `opening_return_30m`       | (close at 30m − first_open) / first_open                          |
| `opening_volume_ratio_15m` | opening 15m volume / expected average 15m volume                  |
| `opening_high`             | Highest high during opening 15m                                    |
| `opening_low`              | Lowest low during opening 15m                                      |
| `opening_range_pct`        | (opening_high − opening_low) / opening_low                         |
| `opening_high_break`       | True if latest close > opening_high after the opening period       |
| `opening_low_break`        | True if latest close < opening_low after the opening period        |
| `opening_range_position`   | (latest_close − opening_low) / (opening_high − opening_low)        |
| `opening_strength_score`   | 0–100; combines return, volume ratio, and range position           |

### Interpretation

- **opening_strength_score > 70**: Strong opening — price up, volume confirming.
- **opening_strength_score 40–70**: Neutral — mixed signals.
- **opening_strength_score < 40**: Weak opening — possible distribution or gap down.
- **opening_high_break = True + volume confirmed**: Potential breakout setup (but verify).
- **opening_low_break = True**: Bearish intraday signal.

---

## 6. VWAP Features

VWAP (Volume Weighted Average Price) is computed per trading session.

### Feature definitions

| Feature               | Description                                                              |
|-----------------------|--------------------------------------------------------------------------|
| `intraday_vwap`       | Session VWAP at the most recent bar (last computed value)                |
| `price_vs_vwap_pct`   | (latest_close − vwap) / vwap × 100 %                                    |
| `vwap_slope`          | Linear regression slope of VWAP over the last 30 bars                   |
| `above_vwap_ratio`    | Fraction of all bars where close > VWAP (0–1)                           |
| `vwap_reclaim`        | True if price was below VWAP at some point and is now above              |
| `vwap_lost`           | True if price was above VWAP at some point and is now below              |
| `vwap_support_score`  | 0–100; based on above_vwap_ratio, slope, reclaim/lost status             |

### Interpretation

- **price_vs_vwap_pct > 0**: Price above VWAP (relatively bullish intraday).
- **vwap_reclaim = True**: Price reclaimed VWAP — potential shift in intraday momentum.
- **vwap_lost = True**: Price lost VWAP support — potential weakening.
- **vwap_support_score > 65**: Strong VWAP support; price holding above.
- **vwap_support_score < 35**: Price struggling below VWAP.

---

## 7. Fake Breakout Detection

Fake breakouts are detected relative to the opening range high/low
(calculated from the first 15 bars).

### Feature definitions

| Feature                    | Description                                                              |
|----------------------------|--------------------------------------------------------------------------|
| `intraday_high_break`      | True if close exceeded opening_range_high after the opening period       |
| `intraday_low_break`       | True if close fell below opening_range_low after the opening period      |
| `breakout_volume_confirmed`| True if volume at breakout bar > 1.5× mean bar volume                   |
| `breakout_failed`          | True if price broke out then returned inside the opening range           |
| `fake_breakout_risk`       | HIGH / MEDIUM / LOW / NONE                                               |
| `fake_breakout_score`      | 0–100 (higher = greater fake breakout risk)                              |
| `chase_risk_score`         | 0–100 (higher = riskier to buy/chase the breakout)                      |
| `breakout_quality`         | STRONG / WEAK / FAILED / NONE                                            |

### Risk levels

| Risk   | Condition                                                        |
|--------|------------------------------------------------------------------|
| HIGH   | Breakout failed AND not volume confirmed                         |
| MEDIUM | Breakout failed OR (high break without volume confirmation)      |
| LOW    | Breakout occurred AND volume confirmed                           |
| NONE   | No breakout detected                                             |

### Practical use

- **STRONG breakout + chase_risk_score < 30**: Relatively cleaner setup for analysis.
- **HIGH fake_breakout_risk**: Avoid chasing; likely stop-hunt.
- **FAILED breakout**: Opening range may act as resistance again.

> All outputs are for research only. No trading decisions should be made based on these features alone.

---

## 8. Intraday Volume Profile

The volume profile distributes session volume across price bins to identify
key price levels where trading activity was concentrated.

### Key concepts

| Term               | Definition                                                               |
|--------------------|--------------------------------------------------------------------------|
| POC (Point of Control) | Price bin with the highest traded volume                            |
| Value Area         | Price range containing `value_area_pct` (default 70%) of session volume  |
| Value Area High    | Upper bound of the value area                                            |
| Value Area Low     | Lower bound of the value area                                            |

### Feature definitions

| Feature                           | Description                                               |
|-----------------------------------|-----------------------------------------------------------|
| `intraday_poc_price`              | Mid-price of the highest-volume bin                       |
| `intraday_value_area_high`        | Upper bound of the 70% value area                         |
| `intraday_value_area_low`         | Lower bound of the 70% value area                         |
| `intraday_price_vs_poc_pct`       | (latest_close − poc_price) / poc_price × 100 %           |
| `intraday_volume_cluster_strength`| Top-3 bins' volume as % of total session volume (0–100)   |
| `intraday_support_pressure_score` | 0–100; price position within value area + cluster strength |

### Interpretation

- **price_vs_poc_pct > 0**: Price above POC — buyers in control (intraday).
- **price inside value area**: Fair value zone; expect mean reversion tendencies.
- **price above value_area_high**: Breakout above fair value — monitor for continuation.
- **price below value_area_low**: Breakdown below fair value — monitor for further weakness.
- **volume_cluster_strength > 60**: Volume heavily concentrated; price levels well-defined.

---

## 9. Tick / BidAsk Placeholder Status

In **v0.3.27**, tick (transaction-level) and bid/ask (Level 2) data are **NOT available**.

| Data Type | v0.3.27 Status | Plan              |
|-----------|---------------|-------------------|
| 1min bars | Available     | XQ CSV import     |
| 5min bars | Available     | XQ CSV import     |
| Tick data | **PLANNED**   | Future version    |
| BidAsk    | **PLANNED**   | Future version    |

The `TickBidAskSchema` class (`intraday/tick_bidask_schema.py`) defines the schema
for future integration:

- `tick_api_ready = False`
- `bidask_api_ready = False`
- Use `TickBidAskSchema().get_readiness_status()` to query current status.
- Use `TickBidAskSchema().create_empty_tick_df()` to obtain an empty DataFrame
  matching the expected tick schema.

When tick/bid-ask providers are integrated in a future version, data should
conform to the schemas defined in `tick_bidask_schema.py`.

---

## 10. CLI Usage

All commands are run from the project root.

### Run intraday pipeline (dry run)

```python
from intraday.intraday_pipeline import IntradayDataPipeline

pipeline = IntradayDataPipeline(freq="1min", dry_run=True)
result = pipeline.run()
print(result)
```

### Run intraday pipeline (write output)

```python
from intraday.intraday_pipeline import IntradayDataPipeline

pipeline = IntradayDataPipeline(freq="1min", dry_run=False)
result = pipeline.run()
print(f"Standardized {result['files_standardized']} files")
print(f"Symbols: {result['symbols_covered']}")
```

### Check data quality

```python
from intraday.intraday_quality import IntradayQualityChecker

checker = IntradayQualityChecker()
result = checker.run()
print(f"Overall quality score: {result['overall_quality_score']}")
for r in result["results"]:
    print(f"  {r['symbol']} {r['freq']}: {r['quality_status']} ({r['quality_score']:.1f})")
```

### Build features for a symbol

```python
import pandas as pd
from intraday.opening_range_features import OpeningRangeFeatureBuilder
from intraday.vwap_features import VWAPFeatureBuilder
from intraday.fake_breakout_detector import FakeBreakoutDetector
from intraday.intraday_volume_profile import IntradayVolumeProfile

df = pd.read_csv("data/import/intraday_standard/1min/2454_1min.csv")

opening = OpeningRangeFeatureBuilder().build(df)
vwap    = VWAPFeatureBuilder().build(df)
bkout   = FakeBreakoutDetector().detect(df)
vprofile = IntradayVolumeProfile().build(df)

print("Opening strength:", opening["opening_strength_score"])
print("Price vs VWAP %:", vwap["price_vs_vwap_pct"])
print("Fake BK risk:", bkout["fake_breakout_risk"])
print("POC price:", vprofile["intraday_poc_price"])
```

### Generate intraday pipeline report

```python
from reports.intraday_pipeline_report import IntradayPipelineReportBuilder

builder = IntradayPipelineReportBuilder(
    pipeline_result=result,     # from IntradayDataPipeline.run()
    quality_result=quality,     # from IntradayQualityChecker.run()
)
path = builder.build()
print(f"Report written to: {path}")
```

### Check tick/bidask readiness

```python
from intraday.tick_bidask_schema import TickBidAskSchema

status = TickBidAskSchema().get_readiness_status()
print(status)
# {'tick_ready': False, 'bidask_ready': False,
#  'tick_planned': True, 'bidask_planned': True, 'note': '...'}
```

---

## 11. GUI Usage

The intraday pipeline GUI panel is accessible from the main TW Quant Cockpit window.

### Panel: Intraday Pipeline (`gui/intraday_pipeline_panel.py`)

**Safety banner** — Always visible at the top:
> INTRADAY PIPELINE — Research Only | Intraday Research Only | No Real Orders | Production: BLOCKED

**Controls:**

| Button            | Action                                                    |
|-------------------|-----------------------------------------------------------|
| Freq combo        | Select "1min" or "5min"                                   |
| Run Dry Run       | Simulate pipeline without writing files                   |
| Run Standardize   | Run pipeline and write standardized output files          |
| Check Quality     | Run intraday data quality check                           |
| Generate Report   | Write `intraday_pipeline_report_YYYY-MM-DD.md`            |

**Summary cards** (top row):
- Symbols covered
- Files standardized
- Overall quality score
- Total missing minutes
- Fake breakout warnings
- Tick/BidAsk readiness (always "PLANNED" in v0.3.27)

**Sub-tabs:**
- **Quality** — per-symbol quality table
- **Features** — opening strength, VWAP, fake breakout, POC, support score
- **Tick/BidAsk** — current status and planning note

All background operations run in `QThread` workers; buttons are disabled
during execution and re-enabled when the worker completes.

---

## 12. Safety Statement

> **[!] Research Only / Intraday Research Only / No Real Orders**
> **Not Investment Advice / Production Trading: BLOCKED**

- All intraday data, features, scores, and reports produced by this pipeline
  are for **research and analysis purposes only**.
- **No signals** or outputs from this system should be used to execute actual trades.
- This system has no connection to any broker, order management system, or
  live trading infrastructure.
- All classes in the `intraday/` package carry safety flags:
  `read_only=True`, `no_real_orders=True`, `production_blocked=True`.
- Past intraday patterns do not guarantee future results.
- Always consult a qualified financial professional before making any investment decision.
