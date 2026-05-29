# TW Quant Cockpit v1 — Taiwan Quantitative Trading Platform

> **[!] 第一版禁止實盤自動下單。本系統僅供研究、模擬交易與決策輔助，不構成投資建議。**
>
> **[!] v1: Real order execution is strictly prohibited. For research, simulation, and decision support only. Not investment advice.**

---

## Project Overview

This project has two layers:

### 1. Core Research Engine (original `trading_master`)
Historical quantitative research, ML training, backtesting, and strategy validation for Taiwan (TWSE) stocks.

### 2. TW Quant Cockpit v1 (new)
Taiwan bull-stock screening + short/mid/long-term analysis + simulated trading learning system.

**Core mission**: From 1000+ Taiwan stocks, use theme, fundamental, technical, and chip filters to narrow down to 3–8 stocks worth tracking, then run day-trade / short-term / mid-term / long-term analysis.

---

## KPI Targets (Research Engine)

| KPI | Target |
|-----|--------|
| Sharpe Ratio | > 1.5 |
| Max Drawdown | < 20% |
| Profit Factor | > 1.5 |

---

## Installation

```bash
pip install -r requirements.txt
```

Key dependencies: `pandas`, `numpy`, `lightgbm`, `xgboost`, `scikit-learn`, `streamlit`, `PySide6`, `plotly`, `pyarrow`, `python-dotenv`, `loguru`, `pydantic`

Optional (real broker): `shioaji` (not required for mock mode)

---

## Environment Setup (.env)

Copy `.env.example` to `.env` and fill in your settings:

```bash
cp .env.example .env
```

```env
# Shioaji (optional — mock mode works without this)
SHIOAJI_API_KEY=
SHIOAJI_SECRET_KEY=
SHIOAJI_PERSON_ID=
SHIOAJI_PASSWORD=

# System mode (default: mock)
TWQC_MODE=mock
TWQC_ENABLE_REAL_ORDER=false
```

> **`TWQC_ENABLE_REAL_ORDER` must remain `false`. Real order submission is blocked in v1.**

---

## Original trading_master Commands (fully preserved)

```bash
# Download historical price data from FinMind
python main.py download

# Compute technical features
python main.py features

# Train ML ensemble model (LightGBM + XGBoost)
python main.py train

# Run backtest
python main.py backtest --strategy momentum
python main.py backtest --strategy mean_reversion
python main.py backtest --strategy breakout
python main.py backtest --strategy momentum --walk-forward

# Run full daily pipeline
python main.py pipeline

# Show latest report
python main.py report

# Launch Streamlit research dashboard
python main.py ui
```

---

## TW Quant Cockpit v1 — New Commands

### Screener — 四層飆股篩選

```bash
python main.py screener
python main.py screener --top 5
```

Runs the 4-layer filter pipeline:
1. **Theme pool** (~100–200 symbols): AI server, CCL/PCB/ABF, ASIC/IC design, networking switch, thermal, power, robotics, active ETF overlap
2. **Fundamental filter** (~30–60): Monthly revenue YoY > 30%, EPS growth, gross margin
3. **Technical filter** (~10–20): MA alignment, breakout, volume surge, KD/RSI/MACD
4. **Chip confirmation** (3–8): Foreign + trust net buy, major holder ratio, margin risk

Outputs a scored table with `bull_stock_score` (0–100):

| Score | Signal |
|-------|--------|
| 80–100 | Bull candidate — look for entry |
| 65–79 | Strong — wait for pullback |
| 50–64 | Watch only |
| < 50 | Avoid |

Technical filter also runs **BuyPointAnalyzer** for each symbol and attaches:
- `buy_point_grade`: A / B / C / None
- `buy_point_type`: `A_PULLBACK_MA10` / `B_PULLBACK_MA5` / `C_PLATFORM_BREAKOUT`

---

### Cockpit GUI — 控盤介面

```bash
python main.py cockpit
```

Launches the PySide6 desktop GUI with:
- Market status bar (TAIEX, session state)
- Stock monitoring table (price, scores, decision, P&L)
- Bull candidates Top 3–8 panel
- 5-level order book (委買委賣)
- Score & decision panel (bull/daytrade/swing/risk scores)
- Paper positions & today's P&L
- System log window

Auto-refreshes every 5 seconds using mock data (no Shioaji account required).

---

### Paper Trading — 模擬單

```bash
python main.py paper
```

Shows simulated positions, realized P&L, and unrealized P&L.
Place simulated orders via the Cockpit GUI.

Simulated costs (Taiwan exchange):
- Buy commission: 0.1425%
- Sell commission: 0.1425%
- Securities tax: 0.30%
- Slippage: 0.10%

---

### Stock Report — 個股多週期分析

```bash
python main.py stock-report --stock 2330
python main.py stock-report --stock 2454
```

Generates a Markdown report with:
- Bull stock score breakdown
- Life-cycle positioning (初漲/主升/第二波/高檔震盪/轉弱/出貨)
- Day-trade strategy (entry, add, exit, stop-loss, no-entry conditions)
- Short-term strategy (5–20 days)
- Mid-term strategy (1–3 months)
- Long-term strategy (3–12 months)
- **Buy point grade section** (A/B/C grade, support/confirm/invalidation prices)
- Data completeness rating

Report saved to `data/reports/report_{symbol}_{date}.md`.

> If data is insufficient, the report explicitly states:
> **「資料不足，只能做盤中初估，不能當正式短中長線操作依據」**

---

### Buy Point Engine — 強勢股回測買點引擎

The `BuyPointAnalyzer` (`analysis/buy_point_analyzer.py`) classifies buy opportunities into three grades:

| Grade | Type | Condition |
|-------|------|-----------|
| **A** | `A_PULLBACK_MA10` | MA5 > MA10 > MA20, low touches MA10, close reclaims MA10, volume shrinks, KD turns up, no heavy institutional selling |
| **B** | `B_PULLBACK_MA5` | Low touches MA5, price reclaims MA5 and VWAP intraday, orderbook imbalance > 0 |
| **C** | `C_PLATFORM_BREAKOUT` | 10–20 day consolidation < 8% range, close breaks platform high, volume > 1.5× 20d average, no long upper wick |

Each grade outputs: `support_price`, `confirm_price`, `invalid_price`, `add_position_price`, `exit_price`, `stop_loss_price`.

**No-entry conditions** (auto-detected and blocked):
- Early surge > 5% — no chasing
- Limit-up then heavy-volume breakdown
- Heavy institutional selling (foreign/trust)
- Price below MA20
- Long upper wick candle
- Break MA10 with volume expansion

Buy point fields are surfaced in:
- Screener output (`screener/technical_filter.py`)
- `DaytradeAnalyzer` and `ShortTermAnalyzer` result dicts
- Stock report **七、買點分級判斷** section
- Cockpit dashboard table columns: 買點等級 / 買點型態 / 支撐價 / 確認價 / 失效價

---

### Mock Realtime — 模擬即時行情

```bash
python main.py mock-realtime
python main.py mock-realtime --duration 60 --interval 2
```

Simulates real-time tick data for watchlist stocks without a Shioaji account.
Shows price, change%, bid/ask spread, and volume — updates every N seconds.

---

## Mock Mode Demo (no real account required)

All new features work in mock mode:

```bash
# 1. Run screener
python main.py screener

# 2. Simulate realtime market
python main.py mock-realtime --duration 30

# 3. Generate stock report
python main.py stock-report --stock 2330

# 4. Check paper positions
python main.py paper

# 5. Launch full cockpit GUI
python main.py cockpit
```

---

## Project Structure

```
trading_master/
│
├── main.py                  # CLI entry point (all commands)
├── config.py                # Configuration
├── requirements.txt
├── .env.example             # Environment variable template
├── .gitignore
│
├── config/
│   ├── app.yaml
│   ├── watchlist.csv
│   └── theme_pools/         # 8 theme pool CSV files
│       ├── ai_server.csv
│       ├── ai_pcb_ccl.csv
│       ├── asic_ic_design.csv
│       ├── networking_switch.csv
│       ├── thermal.csv
│       ├── power_supply.csv
│       ├── robotics.csv
│       └── active_etf_overlap.csv
│
├── data/                    # Data layer (original)
├── features/                # Feature engineering (original + new)
│   ├── indicators.py
│   ├── microstructure.py
│   ├── volume_profile.py
│   ├── theme_features.py    # NEW
│   ├── fundamental_features.py  # NEW
│   ├── chip_features.py     # NEW
│   ├── orderbook_features.py    # NEW
│   └── pullback_features.py     # NEW — MA/KD/volume/VWAP/box features for buy point engine
│
├── models/                  # ML models (original)
├── strategies/              # Trading strategies (original)
├── risk/                    # Risk management (original)
├── backtest/                # Backtesting engine (original)
├── pipeline/                # Daily pipeline (original)
├── reports/                 # Report generation (original)
│
├── broker/                  # NEW — Broker interface
│   ├── mock_broker.py       # Mock market data generator
│   ├── shioaji_client.py    # Shioaji skeleton (no real orders)
│   ├── quote_subscriber.py  # Quote subscription interface
│   └── bidask_parser.py     # Order book parser
│
├── realtime/                # NEW — Real-time data engine
│   ├── tick_buffer.py
│   ├── bidask_buffer.py
│   ├── realtime_engine.py
│   └── market_snapshot.py
│
├── screener/                # NEW — 4-layer stock screener
│   ├── screener_pipeline.py
│   ├── theme_pool.py
│   ├── fundamental_filter.py
│   ├── technical_filter.py
│   ├── chip_filter.py
│   ├── margin_filter.py
│   ├── trust_cost_filter.py
│   └── breakout_screener.py
│
├── analysis/                # NEW — Multi-timeframe analysis
│   ├── daytrade_analyzer.py
│   ├── short_term_analyzer.py
│   ├── mid_term_analyzer.py
│   ├── long_term_analyzer.py
│   ├── stock_report_builder.py
│   ├── timeframe_requirements.py
│   └── buy_point_analyzer.py    # NEW — A/B/C buy point grading engine
│
├── sim/                     # NEW — Paper trading simulator
│   ├── simulator.py         # PaperTrader interface
│   ├── order_manager.py
│   ├── position_manager.py
│   └── performance.py
│
├── dataset/                 # NEW — AI training dataset builder
│   ├── labeler.py
│   ├── dataset_builder.py
│   └── feature_snapshot_builder.py
│
├── gui/                     # NEW — TW Quant Cockpit GUI (PySide6)
│   ├── dashboard.py         # Main cockpit window
│   ├── widgets.py
│   └── charts.py
│
└── ui/
    └── dashboard.py         # Original Streamlit dashboard (preserved)
```

---

## Strategies (Research Engine)

### Momentum
Ranks stocks by `0.1×ret_1d + 0.2×ret_5d + 0.3×ret_20d + 0.4×predicted_return`. Buys top 10 with equal weight, rebalances weekly.

### Mean Reversion
Entry: RSI(14) < 30 AND price < lower Bollinger Band. Exit: RSI > 55 OR price > SMA20.

### Breakout
Entry: price breaks 20-day high AND volume > 1.5× average. Stop: 2×ATR. Target: 3×ATR.

### Auto Selector
| Market Regime | Vol Regime | Strategy |
|---------------|------------|----------|
| Bull | Low | Momentum |
| Bull | High | Breakout |
| Bear | Any | Mean Reversion |
| Sideways | Any | Mean Reversion |

---

## Risk Management

| Parameter | Value |
|-----------|-------|
| Risk per trade | 1.5% of portfolio |
| Max position | 10% per stock |
| Stop-loss | 2× ATR below entry |
| Take-profit | 3× ATR above entry |
| Drawdown halt | 20% portfolio drawdown |

---

## Data Source

Historical data: [FinMind](https://finmindtrade.com/) (free tier available).
Set token in `config.py` or via `FINMIND_TOKEN` environment variable.

Data stored in SQLite (`trading_data.db`). Subsequent runs only fetch new data.

---

## v1 Restrictions

The following are **strictly prohibited** in v1:

1. Real order execution (auto-blocked, raises `NotImplementedError`)
2. Real capital usage
3. Subscribing to 1000+ real-time quotes at startup
4. High-frequency trading
5. Reinforcement learning auto-trading
6. AI-driven real-money buy/sell decisions

---

## Roadmap

### v0.2 Phase 2 — Real CSV Import (implemented)

Real data can be imported via CSV files placed in `data/import/` subdirectories.

#### CSV 格式 / Import Format

**Stock universe** — `data/import/profile/*.csv`
```
symbol,name,market,industry,theme_tags
2454,聯發科,TWSE,半導體,AI/手機晶片/車用
```

**Daily K-line** — `data/import/daily/*.csv`
```
date,symbol,open,high,low,close,volume
2024-01-02,2454,1040.0,1065.0,1035.0,1060.0,15420000
```

**Institutional flow** — `data/import/institutional/*.csv`
```
date,symbol,foreign_net_buy,trust_net_buy,dealer_net_buy
2024-01-02,2454,2500,800,200
```

**Margin** — `data/import/margin/*.csv`
```
date,symbol,margin_balance,margin_change,short_balance,short_change
2024-01-02,2454,45000,1200,-500,-50
```

**Monthly revenue** — `data/import/monthly_revenue/*.csv`
```
month,symbol,revenue,mom,yoy,accumulated_yoy
2023-10,2454,55200000000,3.5,28.4,22.1
```

**Holder structure** — `data/import/holder/*.csv`
```
date,symbol,major_holder_ratio,retail_holder_ratio,major_change,retail_change
2024-01-31,2454,69.8,30.2,1.3,-1.3
```

Sample CSVs are included in each directory. To add more stocks, append rows to any CSV or create new CSV files in the same folder.

#### Real Mode 資料防火牆 / Data Firewall Rules

| Condition | Result |
|-----------|--------|
| `--mode real` + CSV data present | 🟢 REAL DATA — full analysis |
| `--mode real` + no CSV/DB data | 🔴 Prices suppressed with `—` |
| `--mode real` + no daily K | No A/B/C buy point grade |
| `--mode mock` (any data) | 🟡 MOCK DATA — demo mode |

```bash
# Real mode with CSV data
python main.py stock-report --stock 2454 --mode real
python main.py screener --mode real --top 8

# Mock mode (always works, demo prices)
python main.py stock-report --stock 2454 --mode mock
python main.py screener --mode mock --top 8
```

#### RealDataLoader API
```python
from data.real_data_loader import RealDataLoader
loader = RealDataLoader()
all_data = loader.load_all('2454')
# Returns: {profile, daily_k, institutional, margin, monthly_revenue, holder}
```

### v0.2 Phase 4 — CSV 匯入工具與 data-check (implemented)

#### import-csv — 匯入真實 CSV

```bash
python main.py import-csv --type daily           --file D:\XQ\daily.csv
python main.py import-csv --type institutional   --file D:\XQ\institutional.csv
python main.py import-csv --type margin          --file D:\XQ\margin.csv
python main.py import-csv --type monthly_revenue --file D:\XQ\revenue.csv
python main.py import-csv --type holder          --file D:\XQ\holder.csv
python main.py import-csv --type trust_cost      --file D:\XQ\trust_cost.csv
python main.py import-csv --type profile         --file D:\XQ\profile.csv
python main.py import-csv --type daily           --file D:\XQ\daily.csv --replace
```

**參數：**
- `--type`：必填。支援 `profile` / `daily` / `institutional` / `margin` / `monthly_revenue` / `holder` / `trust_cost`
- `--file`：必填。輸入 CSV 路徑
- `--replace`：選填。覆蓋既有標準 CSV（預設：append 並去重）

**支援資料類型與標準欄位：**

| 類型 | 標準欄位 | 輸出路徑 |
|------|---------|---------|
| profile | symbol,name,market,industry,theme_tags,is_mainstream_theme,sector | data/import/profile/stock_profile.csv |
| daily | date,symbol,open,high,low,close,volume | data/import/daily/daily_k.csv |
| institutional | date,symbol,foreign_net_buy,trust_net_buy,dealer_net_buy | data/import/institutional/institutional.csv |
| margin | date,symbol,margin_balance,margin_change,short_balance,short_change | data/import/margin/margin.csv |
| monthly_revenue | month,symbol,revenue,mom,yoy,accumulated_yoy | data/import/monthly_revenue/monthly_revenue.csv |
| holder | date,symbol,major_holder_ratio,retail_holder_ratio,major_change,retail_change | data/import/holder/holder.csv |
| trust_cost | date,symbol,trust_buy_shares,trust_buy_amount,trust_avg_cost,close,price_vs_trust_cost_pct | data/import/trust_cost/trust_cost.csv |

**中文欄位別名（自動轉換）：**

```
股票代號 / 代號 / 證券代號  →  symbol
股票名稱 / 名稱             →  name
日期                        →  date
開盤價 / 開盤               →  open
收盤價 / 收盤               →  close
外資買賣超 / 外資           →  foreign_net_buy
投信買賣超 / 投信           →  trust_net_buy
年月 / 月份                 →  month
...（完整清單見 data/csv_schema.py）
```

#### data-check — 資料完整度檢查

```bash
python main.py data-check --stock 2383
python main.py data-check --all
```

單檔輸出範例：
```
TW Quant Cockpit Data Check

  股票：2383 台光電

  Profile:          OK
  Daily K:          120 rows  OK
  Institutional:     40 rows  OK
  Margin:            40 rows  OK
  Monthly Revenue:   12 rows  OK
  Holder:             4 rows  OK
  Trust Cost:        40 rows  OK

  正式判斷允許：
  當沖：否，缺 intraday / bidask
  短線：是
  中線：是
  長線：是
```

**正式判斷門檻：**

| 時間框架 | 條件 |
|---------|------|
| 當沖 | intraday + bidask（Phase 4 尚未支援，永遠 False） |
| 短線 | daily ≥ 20 + institutional ≥ 5 + margin ≥ 5 |
| 中線 | daily ≥ 60 + monthly_revenue ≥ 6 + institutional ≥ 5 + margin ≥ 5 + holder ≥ 2 |
| 長線 | daily ≥ 120 + monthly_revenue ≥ 12 + holder ≥ 2 |

#### Real / Mock 模式差異

| 模式 | 資料來源 | 標示 | 說明 |
|------|---------|------|------|
| `--mode real` + 標準 CSV | 使用者匯入 | 🟢 REAL DATA CSV | 允許依完整度進行正式判斷 |
| `--mode real` + sample CSV | 內建範例 | 🟡 REAL DATA SAMPLE | 僅供驗證資料流程，不代表真實市場 |
| `--mode real` + 無資料 | — | 🔴 REAL MODE — 缺真實資料 | 買點/操作價格顯示「—」 |
| `--mode mock` | 穩定亂數 | 🟡 MOCK DATA | 示範模式，固定隨機種子 |

#### sample CSV 與正式 CSV 差異

| 項目 | sample CSV | 正式 CSV |
|------|-----------|---------|
| 位置 | `data/import/{type}/{name}_sample.csv` | `data/import/{type}/{name}.csv` |
| 來源 | 內建示範資料 | 使用者以 `import-csv` 匯入 |
| 優先級 | 最低（fallback） | 最高（優先讀） |
| 用途 | 驗證資料流程 / 初始測試 | 實際研究 / 正式分析 |

> ⚠️ sample CSV 不代表真實市場數據。stock-report 報告會顯示警告。

#### 兆豐 API 尚未接入

Phase 4 **不**接兆豐 API。兆豐 API 計劃放入 v0.4：

> **v0.4（計畫中）**：Mega API / 即時行情 / 五檔 / Paper Trading Realtime

Phase 4 的重點是讓 XQ / Excel / 手動整理的 CSV 匯入、資料完整度檢查、與分析流程全部穩定，
再於 v0.4 接即時行情 API。

> ⚠️ **第一版仍禁止實盤自動下單。本系統僅供研究、模擬交易與決策輔助。**

### v0.2 Phase 5 — GUI 實戰控盤化 (implemented)

Upgraded PySide6 Cockpit GUI from demo dashboard to practical trading control tool.

#### Launch

```bash
python main.py cockpit              # default mock mode
python main.py cockpit --mode real  # real CSV data mode
```

#### New GUI panels

| Panel | Description |
|-------|-------------|
| ControlPanel | Top toolbar: mode switch (MOCK/REAL), refresh, data-check, report, import CSV |
| StockDetailPanel | Full detail for selected stock: price, data mode, bull score, lifecycle, buy point |
| DataStatusPanel | Data completeness check: row counts, formal judgment flags, missing data |
| StrategyPanel | Four-timeframe strategy tabs (當沖/短線/中線/長線): entry, stop-loss, no-entry conditions |
| ReportPanel | Generate and view stock analysis report in-app |
| ImportPanel | Modal dialog for CSV import (all 7 data types) |

#### Mode switching

- **MOCK mode**: All data from mock broker / screener. Always works offline.
- **REAL mode**: Loads from standard CSVs (imported via `import-csv`). No fallback to mock.
  - Prices/buy-points suppressed if real CSV data is missing for that symbol.
  - Data source labels: 🟢 REAL DATA CSV / 🟡 REAL DATA SAMPLE / 🔴 缺真實資料

#### Stock selection

Click any row in the Candidates List (left panel) to:
1. Update StockDetailPanel with price, scores, buy point info
2. Run DataQualityChecker → show in DataStatusPanel
3. Run StrategyAnalyzer → show 4-timeframe strategy in StrategyPanel
4. Update order book (五檔) and score panel

#### GUIState

All panels share a `GUIState` singleton:
- `current_mode`: 'mock' or 'real'
- `selected_symbol`: currently viewed stock
- `last_candidates`: latest screener results
- `last_data_check`: cached data-check results per symbol
- `last_report_path`: path of most recently generated report

### v0.2 (remaining planned)
- Connect real FinMind data for screener fundamental filter
- Integrate real chip data (foreign/trust/dealer net buy) via API
- Persist paper trading state across sessions
- Alert system for breakout candidates

### v0.3 — Backtest Validation & Score Effectiveness (implemented)

Three new CLI commands validate the scoring system and buy-point logic against historical forward returns.

#### New CLI Commands

| 指令 | 說明 |
|------|------|
| `python main.py validate-score --mode real --top 8` | 分數有效性驗證 |
| `python main.py backtest-buy-points --mode real` | A/B/C 買點回測 |
| `python main.py backtest-screener --mode real --top 8` | 選股系統回測 |

#### validate-score

```
python main.py validate-score [--mode mock|real] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--top N] [--output DIR]
```

Runs `ScoreValidator` against all symbols in the universe:
- **Score Bucket Performance**: 80-100 / 65-79 / 50-64 / <50 vs 5/10/20-day forward returns
- **Factor Effectiveness**: per-factor correlation with forward returns, top/bottom quantile spread
- **No-Entry Condition Effectiveness**: validates `-5%` stop-loss avoidance rules
- **Trust Cost Validation**: above/below trust cost line vs forward returns
- **Margin Risk Validation**: high/low margin ratio cohorts vs forward returns
- Generates `data/backtest_results/score_bucket_*.csv`, `factor_effectiveness_*.csv`, etc.
- Generates `reports/score_validation_report_{date}.md`

#### backtest-buy-points

```
python main.py backtest-buy-points [--mode mock|real] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--stock TICKER] [--output DIR]
```

Runs `BuyPointBacktester` — detects A/B/C buy-point signals and simulates 20-day trades:
- **Grade A**: MA10 回測（≤2% below MA10, price bouncing above MA20）
- **Grade B**: MA5 回測（≤1.5% below MA5, above MA10）
- **Grade C**: Platform breakout（close above 20-day rolling high, volume ratio ≥ 1.5×）
- Trade simulation: 20-day hold, stop-loss −5%, take-profit +10%
- Win rate, average/median return, drawdown, profit factor per grade
- Sample size warnings: n < 10 → no conclusion; n < 30 → insufficient sample

#### backtest-screener

```
python main.py backtest-screener [--mode mock|real] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--top N] [--output DIR]
```

Delegates to `ScreenerBacktester` (wraps `ScoreValidator`) — shows score bucket performance table.

#### Output Files

| 檔案 | 說明 |
|------|------|
| `data/backtest_results/score_bucket_*.csv` | Score bucket performance |
| `data/backtest_results/factor_effectiveness_*.csv` | Factor correlation |
| `data/backtest_results/no_entry_effectiveness_*.csv` | No-entry condition stats |
| `data/backtest_results/trust_cost_validation_*.csv` | Trust cost line stats |
| `data/backtest_results/margin_risk_validation_*.csv` | Margin risk stats |
| `data/backtest_results/buy_point_trades_*.csv` | Per-trade outcomes |
| `data/backtest_results/buy_point_grade_summary_*.csv` | Grade A/B/C summary |
| `reports/score_validation_report_{date}.md` | Score validation Markdown report |
| `reports/buy_point_validation_report_{date}.md` | Buy-point Markdown report |

> ⚠️ Backtest results and reports are excluded from the repository (generated artifacts). Run the commands locally to regenerate.

#### New Source Files

| 檔案 | 說明 |
|------|------|
| `backtest/score_validation.py` | `ScoreValidator` — rolling features, no look-ahead bias |
| `backtest/buy_point_backtester.py` | `BuyPointBacktester` — A/B/C signal detection + trade sim |
| `backtest/screener_backtester.py` | `ScreenerBacktester` — wraps ScoreValidator |
| `reports/score_validation_report.py` | `ScoreValidationReport` — Markdown report builder |
| `reports/buy_point_validation_report.py` | `BuyPointValidationReport` — Markdown report builder |

### v0.3.1 — Backtest Output Fix + Universe Expansion Preparation (implemented)

#### Why v0.3 results are not formal conclusions

v0.3 was built with only 3 real-data symbols. That sample size is in the **FUNCTIONAL_TEST** stage:
it confirms the code runs correctly but cannot validate strategy effectiveness.

#### Statistical Confidence Levels

| Level | Condition | Meaning |
|-------|-----------|---------|
| `INSUFFICIENT` | symbols < 10, signals < 30, or days < 60 | Confirms code works; no strategy conclusions |
| `OBSERVATIONAL` | symbols 10-49, signals 30-199 | Initial patterns visible; needs more data |
| `RELIABLE` | symbols >= 50, signals >= 200, days >= 120 | Usable as strategy-adjustment reference |

> RELIABLE still does not constitute investment advice. Live order execution remains disabled.

#### Universe Size Targets

| Symbol count | Stage | Usability |
|-------------|-------|-----------|
| < 10 | FUNCTIONAL_TEST | Code verification only |
| 10-49 | SMALL_SAMPLE | Observational only |
| 50-99 | BASIC_VALIDATION | Basic validation possible |
| 100-199 | BETTER_VALIDATION | Better validation quality |
| 200+ | PRODUCTION_LEVEL | Production-level sample |

#### New CLI Command: universe-check

```
python main.py universe-check
```

Shows current symbol count, confidence stage, missing data gaps, and recommended import order.

#### Updated CLI Output

All CLI output now uses Windows-safe plain-text labels:

```
DATA SOURCE: REAL CSV          (was: 🟢 REAL CSV)
DATA SOURCE: REAL CSV SAMPLE   (was: 🟡 SAMPLE CSV)
DATA SOURCE: MOCK DATA         (was: 🟡 MOCK)
```

Statistical confidence is shown in every validation output:

```
Statistical confidence: INSUFFICIENT
  - symbol_count 3 < 10 -> INSUFFICIENT
  - signal_count 132 < 200 -> OBSERVATIONAL
```

#### How to interpret validate-score results

```
python main.py validate-score --mode real
```

- Look at **Statistical confidence** first. If `INSUFFICIENT`, only read for curiosity.
- Score bucket `80-100` showing higher avg return than `<50` is **observed in sample**, not validated.
- `bucket_confidence` column per row shows per-bucket sample quality.
- Do not conclude "high score strategy is effective" until confidence reaches `RELIABLE`.

#### How to interpret backtest-buy-points results

```
python main.py backtest-buy-points --mode real
```

- Each grade (A/B/C) shows its own `grade_confidence`.
- `OBSERVATIONAL` (30-199 signals): patterns are emerging; watch with more data.
- `RELIABLE` (200+ signals): usable as strategy adjustment reference.
- Grade C with 3 signals: `INSUFFICIENT` — no conclusion.

#### How to scale to 50-200 symbols

1. Prepare a profile CSV with 50-200 symbols (`data/import/profile/stock_profile.csv`)
2. Run `python main.py import-csv --type profile --file your_profile.csv`
3. Import daily K (120+ days), institutional (40+ days), margin (40+ days),
   monthly revenue (12+ months), holder (4+ periods), trust cost (20-40+ days)
4. Run `python main.py data-check --all` to check completeness
5. Run `python main.py universe-check` to confirm confidence stage
6. Re-run validate-score and backtest-buy-points

#### Recommended Import Data Specs

| Data type | Min rows | Ideal |
|-----------|---------|-------|
| daily K | 120 days | 250+ |
| institutional | 40 days | 120+ |
| margin | 40 days | 120+ |
| monthly revenue | 12 months | 24+ |
| holder | 4 periods | 8+ |
| trust cost | 20 days | 40+ |

#### New Source Files (v0.3.1)

| File | Description |
|------|-------------|
| `utils/console_format.py` | Windows-safe plain-text CLI labels and formatters |
| `backtest/stat_confidence.py` | Statistical confidence evaluator (INSUFFICIENT/OBSERVATIONAL/RELIABLE) |
| `data/universe_expansion_guide.py` | Universe completeness checker and import planner |

### v0.3.2 — Universe Expansion & Batch Import (implemented)

#### 為什麼需要 50～200 檔？

少於 10 檔時，回測只能驗證功能；50 檔以上才具備基本驗證意義；100～200 檔可進行較系統性的策略研究。本版新增工具讓使用者可快速擴充樣本。

#### build-universe

```bash
# 使用內建 sample template（台積電、聯發科、鴻海等主要台股）
python main.py build-universe --template top50 --replace
python main.py build-universe --template top100 --replace
python main.py build-universe --template top200 --replace

# 使用自備 profile CSV
python main.py build-universe --file D:\XQ\profile.csv
python main.py build-universe --file D:\XQ\profile.csv --replace
```

Sample universe templates are stored in `config/universe/` and include:

- **top50_sample.csv** — 50 stocks: 台積電、聯發科、鴻海、廣達、富邦金 etc.
- **top100_sample.csv** — 100 stocks: top50 + 半導體、網通、傳產、金融
- **top200_sample.csv** — 200 stocks: top100 + more sectors as a starting template

#### batch-import

```bash
# Import all .csv files in a folder for one data type
python main.py batch-import --type daily --folder D:\XQ\daily
python main.py batch-import --type institutional --folder D:\XQ\institutional
python main.py batch-import --type margin --folder D:\XQ\margin
python main.py batch-import --type monthly_revenue --folder D:\XQ\revenue
python main.py batch-import --type holder --folder D:\XQ\holder
python main.py batch-import --type trust_cost --folder D:\XQ\trust_cost

# Import a structured bundle folder in one command
python main.py batch-import --bundle D:\XQ\twqc_bundle
```

Bundle folder structure:

```
D:\XQ\twqc_bundle\
  profile\
  daily\
  institutional\
  margin\
  monthly_revenue\
  holder\
  trust_cost\
```

#### Required data length per symbol

| Data type | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| daily | 20 rows | ≥ 120 rows | 120 needed for long-term analysis |
| institutional | 5 rows | ≥ 40 rows | 5 needed for short/mid-term |
| margin | 5 rows | ≥ 40 rows | 5 needed for short/mid-term |
| monthly_revenue | 6 months | ≥ 12 months | 12 needed for long-term |
| holder | 2 periods | ≥ 4 periods | 2 needed for mid/long-term |
| trust_cost | 3 rows | ≥ 20–40 rows | supplementary |

#### universe-check output

```bash
python main.py universe-check
```

Shows: symbol count, validation stage, data coverage per threshold, missing gaps, and next-step recommendations.

Validation stages:

| Stage | Symbol count |
|-------|-------------|
| FUNCTIONAL_TEST | < 10 |
| SMALL_SAMPLE | 10–49 |
| BASIC_VALIDATION | 50–99 |
| GOOD_VALIDATION | 100–199 |
| PRACTICAL_SAMPLE | 200+ |

#### data-check --all output

```bash
python main.py data-check --all
```

Shows per-symbol row counts, Short/Mid/Long readiness flags, missing data count. Bottom summary shows Total/Short-ready/Mid-ready/Long-ready counts and current validation stage.

#### New Source Files (v0.3.2)

| File | Description |
|------|-------------|
| `data/universe_builder.py` | Build/merge universe from template or custom CSV |
| `data/batch_importer.py` | Batch import multiple CSV files by type or bundle |
| `data/sample_universe_generator.py` | Read sample template metadata |
| `config/universe/top50_sample.csv` | 50-stock sample universe |
| `config/universe/top100_sample.csv` | 100-stock sample universe |
| `config/universe/top200_sample.csv` | 200-stock sample universe template |
| `docs/data_expansion_guide.md` | Data expansion workflow guide |

> **[!] 不構成投資建議。仍禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。**

### v0.3.3 — 大樣本資料實際匯入與資料清洗 (implemented)

#### 為什麼需要資料清洗？

XQ Global、Excel 匯出的 CSV 常見以下問題：

- 股票代號被 Excel 轉成整數（0050 → 50）
- 日期為民國年格式（113/01/02）或緊湊格式（1130102）
- 數字有千分位（1,234,567）
- 百分比欄位帶有 % 符號
- 編碼為 Big5 / CP950（非 UTF-8）
- N/A / -- / 空白 / null 混用
- 重複的 symbol+date 資料列
- 欄位名稱為中文（日期、股票代號、收盤價等）

v0.3.3 新增 CSVCleaner 自動處理以上所有問題。

#### clean-csv — 清理 CSV（不匯入標準路徑）

```bash
# 預覽清理結果，不寫出任何檔案
python main.py clean-csv --type daily --file D:\XQ\daily.csv --dry-run

# 清理並儲存到指定路徑
python main.py clean-csv --type daily --file D:\XQ\daily.csv --output D:\XQ\daily_clean.csv

python main.py clean-csv --type institutional --file D:\XQ\institutional.csv --dry-run
python main.py clean-csv --type margin       --file D:\XQ\margin.csv --dry-run
python main.py clean-csv --type monthly_revenue --file D:\XQ\revenue.csv --dry-run
python main.py clean-csv --type holder       --file D:\XQ\holder.csv --dry-run
python main.py clean-csv --type trust_cost   --file D:\XQ\trust_cost.csv --dry-run
python main.py clean-csv --type profile      --file D:\XQ\profile.csv --dry-run
```

`clean-csv` 只做清理預覽，**不寫入** `data/import/` 標準路徑。要正式匯入請用 `import-csv`。

輸出範例：

```
TW Quant Cockpit CSV Clean

Type    : daily
Input   : D:\XQ\daily.csv
Mode    : dry-run (no output written)
Input rows : 5000
Output rows        : 4980
Duplicates removed : 20
Warnings           : 2
Errors             : 0
```

#### import-csv 與 clean-csv 差異

| 指令 | 清理 | 寫入標準 CSV | 說明 |
|------|------|-------------|------|
| `clean-csv --dry-run` | 是 | 否 | 預覽清理結果 |
| `clean-csv --output FILE` | 是 | 否（寫到指定路徑） | 輸出到自訂路徑 |
| `import-csv` | 是（整合 CSVCleaner） | 是 | 正式匯入，含清理 |
| `batch-import` | 是 | 是 | 批次正式匯入，含清理 |

#### batch-import --dry-run

```bash
# 模擬匯入，不寫入標準 CSV
python main.py batch-import --bundle D:\XQ\twqc_bundle --dry-run

# 正式匯入並輸出批次報告
python main.py batch-import --bundle D:\XQ\twqc_bundle --export-report
```

#### data-audit — 資料品質稽核

```bash
python main.py data-audit
python main.py data-audit --stock 2383
python main.py data-audit --export
```

`data-audit` 讀取目前所有已匯入的 CSV，輸出：

- Universe 總覽（檔數、驗證階段、統計信心）
- 各資料類型的覆蓋度（達到門檻的股票數）
- 資料品質問題（無效 OHLC、重複列、負值量）
- Short / Mid / Long 就緒數量

`--export` 輸出 Markdown 與 CSV 到 `data/import_reports/`（列為 .gitignore，不 commit）。

輸出範例：

```
TW Quant Cockpit Data Audit

  Universe:
    symbols          : 50
    validation stage : BASIC_VALIDATION
    confidence       : OBSERVATIONAL

  Coverage:
    daily >= 120     : 47 symbols
    institutional >= 40 : 45 symbols
    margin >= 40     : 45 symbols
    revenue >= 12    : 30 symbols
    holder >= 4      : 40 symbols
    trust_cost >= 20 : 38 symbols

  Problems:
    missing data types : none
    invalid OHLC       : 0
    duplicate rows     : 0
    negative volume    : 0

  Readiness:
    short-ready      : 45 symbols
    mid-ready        : 28 symbols
    long-ready       : 28 symbols
```

#### import-plan — 匯入優先計畫

```bash
python main.py import-plan
python main.py import-plan --export
```

依目前 data-audit 結果，產生下一步匯入建議：

```
TW Quant Cockpit Import Plan

Current:
  symbols           : 5
  stage             : FUNCTIONAL_TEST

Priority 1 (short-term analysis requirements):
  - Profile: need 45 more symbols (current: 5, min: 50)
  - Daily K: 2 symbol(s) need >= 120 trading days

Priority 2 (for mid-term analysis):
  - Institutional: 2 symbol(s) need >= 40 days
  ...

Commands:
  python main.py build-universe --template top50 --replace
  python main.py batch-import --bundle D:\XQ\twqc_bundle
  ...
```

#### 大樣本匯入建議流程（50～200 檔）

```bash
# Step 1: 建立 universe（50 檔起步）
python main.py build-universe --template top50 --replace

# Step 2: 批次 dry-run 預覽（確認 CSV 格式正確）
python main.py batch-import --bundle D:\XQ\twqc_bundle --dry-run

# Step 3: 正式批次匯入
python main.py batch-import --bundle D:\XQ\twqc_bundle

# Step 4: 稽核資料品質
python main.py data-audit --export

# Step 5: 查看匯入優先建議
python main.py import-plan

# Step 6: 執行回測驗證
python main.py validate-score --mode real
```

#### 50～200 檔資料需求

| 資料類型 | 最少列數 | 建議列數 | 說明 |
|---------|---------|---------|------|
| 日K | 120 日 / 股 | 250+ 日 | 長線正式判斷需要 |
| 法人 | 40 日 / 股 | 120+ 日 | 短/中線分析 |
| 融資 | 40 日 / 股 | 120+ 日 | 短/中線分析 |
| 月營收 | 12 月 / 股 | 24+ 月 | 中/長線分析 |
| 大戶散戶 | 4 期 / 股 | 8+ 期 | 中/長線分析 |
| 投信成本 | 20 日 / 股 | 40+ 日 | 補充指標 |

50 檔 x 120 日 = 6,000 列日K 為最小可行規模。

#### 資料品質規則

詳細規則請見 `docs/data_quality_rules.md`。

XQ / Excel 欄位對應請見 `docs/xq_csv_mapping_guide.md`。

#### New Source Files (v0.3.3)

| 檔案 | 說明 |
|------|------|
| `data/csv_cleaner.py` | XQ / Excel CSV 清洗、正規化、異常偵測 |
| `data/data_auditor.py` | 資料品質稽核，輸出 summary + export |
| `data/import_plan.py` | 依稽核結果產生匯入優先計畫 |
| `data/import_reporter.py` | 輸出 Markdown / CSV 報告 |
| `docs/xq_csv_mapping_guide.md` | XQ / Excel 欄位對應說明 |
| `docs/data_quality_rules.md` | 資料品質規則與門檻說明 |

> **[!] 不構成投資建議。仍禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。**
> 回測結果不得作為正式投資結論。樣本不足時，系統仍會顯示 INSUFFICIENT 警告。

### v0.3.3-hotfix — XQ 技術分析匯出檔一鍵匯入 (implemented)

#### 為什麼不需要手動拆欄？

XQ Global 技術分析圖表匯出的 Excel/CSV 是「寬欄格式」：一個檔案包含所有指標，欄位名稱為中文（時間、開盤價、融資(張)、投信成本線、大戶持股比例 ...）。過去需要手動拆欄、重命名欄位才能匯入 TWQC 標準路徑。

`import-xq-export` 指令自動完成：
1. 辨識日期欄（時間 / 日期 / date）
2. 對應中文 XQ 欄位名稱到 TWQC 標準名稱
3. 拆分成 5 個子集：daily / margin / institutional / trust_cost / holder
4. 各自寫入標準 `data/import/` 路徑
5. 自動填寫 stock_profile.csv（不覆蓋既有資料）

#### import-xq-export

```bash
# Step 1: 預覽（不寫入任何檔案）
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科 --dry-run

# Step 2: 正式匯入
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科

# Step 3: 驗證
python main.py data-check --stock 2454
python main.py stock-report --stock 2454 --mode real
```

**參數：**
- `--file`：必填。XQ 匯出的 .xlsx / .xls / .csv 路徑
- `--symbol`：必填。台股代號（例：2454）
- `--name`：選填。股票名稱（例：聯發科）
- `--dry-run`：選填。預覽偵測欄位與列數，不寫入任何檔案
- `--replace`：選填。覆蓋已有標準 CSV（預設：append 並去重）
- `--export-split`：選填。同時輸出各分割 CSV 供人工檢查
- `--output-dir`：選填（需搭配 --export-split）。分割 CSV 輸出資料夾
- `--sheet`：選填。Excel 工作表名稱（預設：第一個工作表）

#### 支援輸入格式

| 副檔名 | 支援 |
|--------|------|
| .xlsx | 是（需 openpyxl：`pip install openpyxl`） |
| .xls  | 是 |
| .csv  | 是 — UTF-8-SIG / UTF-8 / Big5 / CP950 自動偵測 |

#### 自動對應的欄位

| XQ 欄位 | TWQC 標準欄位 | 資料集 |
|---------|-------------|--------|
| 時間 | date | 所有 |
| 開盤價 / 收盤價 / 最高價 / 最低價 | open/close/high/low | daily |
| 成交量(張) | volume | daily |
| 融資(張) / 融資餘額 | margin_balance | margin |
| 差額(張) / 融資增減 | margin_change | margin |
| 融券(張) / 融券餘額 | short_balance | margin |
| 投信買賣超(張) | trust_net_buy | institutional |
| 外資買賣超(張) | foreign_net_buy | institutional |
| 買賣超(張)（模糊欄） | trust_net_buy 或 foreign_net_buy（依其他欄判斷） | institutional |
| 投信成本線 / 投信平均成本 | trust_avg_cost | trust_cost |
| 投信買超張數 | trust_buy_shares | trust_cost |
| 大戶持股比例 | major_holder_ratio | holder |
| 大戶買賣力 | major_change | holder |
| 散戶持股比例 | retail_holder_ratio | holder |
| 散戶買賣力 | retail_change | holder |

trust_cost 自動計算：`price_vs_trust_cost_pct = (close - trust_avg_cost) / trust_avg_cost * 100`

#### 部分匯入行為

XQ 匯出不一定包含所有欄位。系統不會因為缺少欄位而中止：

- 未偵測到 `short_balance`（融券）→ margin 只匯入融資部分，顯示警告
- 法人只有一個買賣超欄 → 只匯入偵測到的欄位，顯示警告
- 大戶比例欄未匯出 → holder 部分匯入，顯示警告
- 日期欄為 Excel 序號（如 45798）→ 自動轉換為 YYYY-MM-DD

#### 批次匯入多檔

```bash
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科
python main.py import-xq-export --file D:\XQ\2330.xlsx --symbol 2330 --name 台積電
python main.py import-xq-export --file D:\XQ\6669.xlsx --symbol 6669 --name 緯穎

# 全部匯入後稽核
python main.py data-audit --export
python main.py import-plan
```

#### 匯出分割選項

```bash
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科 \
  --export-split --output-dir D:\XQ\twqc_bundle
```

輸出：
```
D:\XQ\twqc_bundle\
  2454_daily.csv
  2454_margin.csv
  2454_institutional.csv
  2454_trust_cost.csv
  2454_holder.csv
```

這些分割 CSV 可再用 `batch-import` 匯入。

#### New Source Files (v0.3.3-hotfix)

| 檔案 | 說明 |
|------|------|
| `data/xq_export_importer.py` | XQ 寬欄格式自動拆分匯入器 |
| `docs/xq_export_import_guide.md` | XQ 匯出一鍵匯入完整說明文件 |
| `data/import/daily/xq_export_sample.csv` | XQ 格式測試用範例 CSV |

> **[!] 不構成投資建議。仍禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。**

### v0.3.4 — 資料源抽象層 + 台股時光機核心特徵 (implemented)

**目標：** 解除系統對 XQ 的長期依賴，建立可插拔資料源介面，整合 Volume Profile 與 Opening Microstructure 特徵。

#### 資料源不再長期依賴 XQ

- 新增 `data/providers/` 抽象層，所有資料請求透過 `BaseMarketDataProvider` 介面。
- `CSVProvider`：主要 provider，讀取 `data/import/` 標準 CSV。
- `XQExportProvider`：過渡 provider，包裝已匯入的 XQ 資料。
- `TWSEOpenAPIProvider`：預留介面，v0.4 接 TWSE / TPEx / MOPS 公開 API。
- `MegaProvider`：預留介面，v0.4+ 接兆豐證券只讀行情 API（下單永久禁止）。
- XQ 僅作為過渡期匯入工具，不再是核心資料源。

#### Volume Profile (分價量)

Volume Profile 以滾動 lookback（預設 60 日）計算分價量分布，找出 POC（最大成交量價位）與 Value Area（70% 成交量區間）。

| Feature | 說明 |
|---|---|
| `vp_peak_price` | POC — 最大分價量價位 |
| `vp_cluster_strength` | POC 量 / 窗口總量（集中度）|
| `vp_distance_to_peak` | 現價距 POC 百分比 |
| `support_pressure_score` | 淨分 = 支撐分 − 壓力分 |
| `vp_value_area_high/low` | Value Area 上下界（70% 成交量） |

嚴格禁止：用全期間資料一次計算 POC 後回填歷史（data leakage）。

#### Opening Microstructure (開盤 15 分鐘微觀特徵)

| Feature | 說明 |
|---|---|
| `microstructure_score` | 綜合買方壓力分數 [0,1] |
| `opening_return_15m` | 開盤 15 分鐘報酬（有 intraday 時精確，否則日線代理） |
| `buy_sell_pressure` | (收盤 − 最低) / (最高 − 最低) |
| `ms_fake_breakout_risk` | 跳空開高但收盤近開盤且量不足時標記 |
| `ms_no_chase_flag` | 漲幅 >2% 但 microstructure_score < 0.4 時標記 |

缺少 intraday / tick / bidask 時，系統使用日線代理值，不 crash。

#### 新增 CLI 指令

```bash
python main.py provider-status                          # 查看資料源狀態
python main.py time-machine-preview --stock 2454        # 時光機特徵摘要
python main.py feature-preview --stock 2454             # 最新全特徵預覽
```

#### 安全限制（同前）

- `TWQC_ENABLE_REAL_ORDER = False` — 實盤下單永久禁止。
- 不接 Shioaji，不接兆豐 API 下單，不接任何券商下單介面。
- Mock mode 仍然可跑。Real mode 只吃真實 CSV / DB，不 fallback 到 mock。

#### New Source Files (v0.3.4)

| 檔案 | 說明 |
|---|---|
| `data/providers/base_provider.py` | 所有資料源共同抽象介面 |
| `data/providers/csv_provider.py` | CSV 標準資料源 provider |
| `data/providers/xq_export_provider.py` | XQ 匯出過渡 provider |
| `data/providers/twse_openapi_provider.py` | TWSE / TPEx 公開 API 預留介面 |
| `data/providers/mega_provider.py` | 兆豐 API 預留介面（下單禁止） |
| `docs/data_provider_roadmap.md` | 資料源架構藍圖 |
| `docs/time_machine_features.md` | Volume Profile / Microstructure 說明 |

> **[!] 不構成投資建議。仍禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。**

### v0.3.6 — Strategy Knowledge Engine Phase 2 (implemented)

Extends the v0.3.6 core Strategy Knowledge Engine with five new sub-engines, integrated across the full analysis pipeline.

#### New Phase 2 Sub-Engines

| 模組 | 檔案 | 說明 |
|------|------|------|
| KD Advanced | `features/kd_advanced.py` | 低檔黃金交叉 / 高檔死亡交叉 / KD 鈍化 / KD 背離 |
| Short Interest | `features/short_interest_features.py` | 融券軋空燃料評分 / 弱勢股融券警示 / 融券回補警示 |
| Bottom Reversal | `analysis/bottom_reversal_analyzer.py` | 破底翻反彈策略（REBOUND / SPECULATIVE_REBOUND，非 A/B/C） |
| Sector Rotation | `analysis/sector_rotation_analyzer.py` | 族群聯動 / 指標股落後補漲 / 60日滾動相關係數 |
| Fundamental Quality | `analysis/fundamental_quality_analyzer.py` | 財報品質評分 / EPS 防呆 / 毛利率 / 營益率 / 財報前警示 |

#### Phase 2.1 — Integration Gaps Closed

Phase 2 signals are now integrated into all major pipeline components:

| 整合點 | Phase 2 訊號 |
|--------|-------------|
| `analysis/buy_point_analyzer.py` | KD 低/高檔訊號加入 no_entry；底部反轉獨立 REBOUND 輸出（不混入 A/B/C） |
| `analysis/short_term_analyzer.py` | KD / 融券 / 破底翻 / 族群 / 財報風險 → no_entry + reasoning |
| `analysis/mid_term_analyzer.py` | 族群輪動 / 基本面品質 / 估值 / formal_allowed 防呆門檻 |
| `analysis/long_term_analyzer.py` | 基本面品質 / 估值河流 / 缺 EPS / 毛利率時 formal_allowed=False |
| `screener/real_score_builder.py` | Phase 2 加分：KD 低檔 / 軋空燃料 / 基本面品質；扣分：KD 高檔 / 弱勢融券 / 財報風險 |
| `strategies/selector.py` | 每個訊號輸出 phase2_strategy_reason / rebound_warning / squeeze_signal / sector_linkage_reason / fundamental_warning |
| `reports/generator.py` | 日報新增 STRATEGY KNOWLEDGE ENGINE PHASE 2 SIGNALS 區塊 |
| `gui/dashboard.py` | ScorePanel 新增 KD / 融券 / 破底翻 / 族群 / 基本面品質訊號顯示，缺資料顯示 unavailable |

#### Phase 2 Rules

1. `bottom_reversal_signal` 只輸出 REBOUND / SPECULATIVE_REBOUND，不可輸出 A/B/C 強勢買點，不可輸出正式長線價位
2. KD 背離為警示訊號，不可單獨作為買進/賣出依據
3. 族群 correlation 只用 rolling 60d 過去資料，不使用未來資料
4. 財報資料須用 announcement_date（本階段標 TODO，防止資料穿越）
5. 缺 EPS / 毛利率 / 月營收時，中長線 `formal_allowed=False`
6. 規則不可凌駕資料完整度

#### Phase 2 Stock Report Section 9

`stock-report` 的 `## 九、策略知識引擎判斷（v0.3.6）` 現在包含：

- Position Plan / Holding Period / Volume Behavior / MACD Strategy / Valuation River
- KD Advanced / Short Interest / Bottom Reversal / Sector Rotation / Fundamental Quality
- No Chase Reasons / No Panic Sell Reasons / Do Not Rebuy Yet Reasons
- Final Strategy Decision

缺資料時顯示 `partial` / `unavailable`，不整節空白，不 crash。

#### New Source Files (v0.3.6)

| 檔案 | 說明 |
|------|------|
| `features/kd_advanced.py` | KD 進階訊號計算 |
| `features/short_interest_features.py` | 融券軋空特徵 |
| `analysis/bottom_reversal_analyzer.py` | 破底翻反彈策略分析器 |
| `analysis/sector_rotation_analyzer.py` | 族群輪動分析器 |
| `analysis/fundamental_quality_analyzer.py` | 基本面品質分析器 |
| `docs/strategy_knowledge_engine.md` | 策略知識引擎完整說明 |

> **[!] 不構成投資建議。仍禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。**

### v0.3.7 — Strategy Knowledge Backtest (implemented)

建立 Strategy Knowledge Engine 的專用回測驗證框架，驗證 Phase 2 各模組的規則是否有效。

#### 新功能

```bash
python main.py backtest-strategy-knowledge --mode real
python main.py backtest-strategy-knowledge --mode real --stock 2454
python main.py backtest-strategy-knowledge --mode real --start 2023-01-01 --end 2024-12-31
python main.py backtest-strategy-knowledge --mode real --holding-days 20
python main.py backtest-strategy-knowledge --mode mock
```

#### 驗證模組

| 模組 | 訊號 | 資料需求 |
|------|------|---------|
| KD Advanced | kd_low_golden_cross, kd_high_death_cross, kd_mid_noise_cross, kd_high_sticky_trend | daily K 線 |
| Short Interest | squeeze_fuel_score, price_up_short_balance_up, weak_stock_short_increase | daily K 線（proxy），或 margin.csv |
| Bottom Reversal | bottom_reversal_detected, is_speculative_rebound | daily K 線 |
| Sector Rotation | linkage_score, laggard_follow_signal | 需要 peer data（v0.3.8+） |
| Fundamental Quality | fundamental_quality_score, earnings_risk_warning | 需要季度財報時序（匯入後） |
| No Chase | kd_high_death_cross 代理 | daily K 線 |

#### 輸出 CSV

```
data/backtest_results/strategy_knowledge_signals.csv
data/backtest_results/strategy_knowledge_module_performance.csv
data/backtest_results/strategy_knowledge_factor_performance.csv
data/backtest_results/strategy_knowledge_no_chase_validation.csv
data/backtest_results/strategy_knowledge_no_panic_sell_validation.csv
data/backtest_results/strategy_knowledge_rebound_validation.csv
data/backtest_results/strategy_knowledge_sector_validation.csv
data/backtest_results/strategy_knowledge_fundamental_guard_validation.csv
```

#### 統計信心等級

| 等級 | 條件 | 含義 |
|------|------|------|
| `INSUFFICIENT` | 標的 < 10 或訊號 < 30 | 功能驗證，不可宣稱策略有效 |
| `OBSERVATIONAL` | 訊號 30–199 | 初步規律，需更多資料 |
| `RELIABLE` | 標的 ≥ 30, 訊號 ≥ 200, 交易日 ≥ 120 | 可作參考（仍非投資建議） |

#### 注意事項

- 目前樣本（3 檔）預期輸出 `INSUFFICIENT`，此為正常行為。
- mock mode 輸出 `MOCK DEMO ONLY`，不可作策略結論。
- 不接 API、不自動下單。
- 詳細說明：[docs/strategy_knowledge_backtest.md](docs/strategy_knowledge_backtest.md)

#### 新增檔案 (v0.3.7)

| 檔案 | 說明 |
|------|------|
| `backtest/strategy_knowledge_backtester.py` | 主控回測器 |
| `backtest/strategy_signal_evaluator.py` | 共用訊號評估工具 |
| `reports/strategy_knowledge_validation_report.py` | Markdown 報告產生器 |
| `docs/strategy_knowledge_backtest.md` | 回測說明文件 |

#### 修改檔案 (v0.3.7)

| 檔案 | 修改內容 |
|------|---------|
| `backtest/stat_confidence.py` | 新增 `for_strategy_module()` 靜態方法 |
| `main.py` | 新增 `backtest-strategy-knowledge` CLI |

> **[!] 不構成投資建議。仍禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。**

### v0.3.5 (planned)
- GUI 顯示回測驗證報告與 Watchlist 追蹤

### v0.4 (planned)
- TWSE / TPEx / MOPS / data.gov.tw 自動補月營收與基本面
- 兆豐 API 只讀即時行情 / 五檔 / 逐筆
- 不再依賴 XQ 作為核心資料源
- 不做實盤自動下單

---

*TW Quant Cockpit v1 — For research and simulation only. Not investment advice.*
