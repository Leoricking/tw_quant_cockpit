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

### v0.2 (remaining planned)
- Connect real FinMind data for screener fundamental filter
- Integrate real chip data (foreign/trust/dealer net buy) via API
- Persist paper trading state across sessions
- Cockpit GUI stock selection (click to view detail)
- Alert system for breakout candidates

### v0.3 (planned)
- Shioaji real-time quote subscription (read-only)
- Real 5-level order book display
- Intraday minute K chart
- Paper order execution from GUI
- AI training dataset export
- Walk-forward screener validation

---

*TW Quant Cockpit v1 — For research and simulation only. Not investment advice.*
