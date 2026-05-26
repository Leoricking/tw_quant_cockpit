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

### v0.4 (planned)
- Shioaji real-time quote subscription (read-only)
- Real 5-level order book display
- Intraday minute K chart
- Paper order execution from GUI
- AI training dataset export
- Walk-forward screener validation

---

*TW Quant Cockpit v1 — For research and simulation only. Not investment advice.*
