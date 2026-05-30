# Long-Term Strategy Validation — v0.3.11

## Overview

本文件說明 v0.3.11 長線策略驗證框架的設計、使用方式與解讀限制。

**目標**：驗證 v0.3.10 補齊長線資料後（`long_term_ready=14/14`），長線策略規則
（EPS 品質、毛利率趨勢、PE 估值區間、BUY_BREAKOUT 信號）是否對 60/120 日前向報酬
有統計上可識別的正面影響。

---

## 使用方式

```bash
# 全 universe 回測（預設 holding_days=60）
python main.py backtest-long-term-strategy --mode real

# 單一個股
python main.py backtest-long-term-strategy --mode real --stock 2454

# 120 日持有
python main.py backtest-long-term-strategy --mode real --holding-days 120

# Mock 模式（不需要真實資料）
python main.py backtest-long-term-strategy --mode mock

# 指定輸出目錄
python main.py backtest-long-term-strategy --mode real \
    --output-dir data/backtest_results/ \
    --report-dir reports/
```

---

## 架構

### 核心元件

| 元件 | 路徑 | 說明 |
|------|------|------|
| 回測主引擎 | `backtest/long_term_strategy_backtester.py` | 逐 symbol 逐 date 評估長線信號 + 前向報酬 |
| 因子分析工具 | `backtest/long_term_factor_evaluator.py` | bucket/boolean/zone/filter 共用函式 |
| 報告產生器 | `reports/long_term_validation_report.py` | 8 節 Markdown 報告 |
| 置信度評估 | `backtest/stat_confidence.py` | `for_long_term_strategy()` 方法 |

### 資料流

```
universe_profile.csv
      │
      ▼
LongTermStrategyBacktester.run()
      │
      ├─ _load_daily_df(symbol)          ← 全部日線（不截斷）
      ├─ _load_fundamental_snapshot()    ← EPS, gross_margin, announcement_date
      └─ _load_monthly_revenue_rows()    ← 月營收列表
            │
            ▼
      每 20 個交易日取樣點 (bar 240 ~ bar n-holding_days)
            │
            ▼
      LongTermAnalyzer.analyze()
            │ 輸出穩定回測欄位:
            │   long_term_score, long_term_signal,
            │   eps_positive, eps_growth_bucket,
            │   gross_margin_bucket, valuation_zone,
            │   pe_bucket, timing_quality, timing_estimated
            │
            ▼
      計算 fwd_{holding_days}d 前向報酬
            │
            ▼
      LongTermFactorEvaluator 因子分析
            │
            ▼
      LongTermValidationReport（Markdown）
```

---

## 穩定回測欄位（v0.3.11 新增）

`LongTermAnalyzer.analyze()` 回傳 dict 新增以下欄位：

| 欄位 | 型別 | 說明 |
|------|------|------|
| `long_term_score` | float | 長線評分原始值（正分看多，負分看空） |
| `long_term_signal` | str | 同 decision：BUY_BREAKOUT / WATCH / HOLD / AVOID |
| `long_term_buy_allowed` | bool | signal==BUY_BREAKOUT AND formal_allowed |
| `long_term_watch_only` | bool | signal in (WATCH, HOLD) |
| `long_term_exit_warning` | bool | signal==AVOID OR score<0 |
| `eps_positive` | bool\|None | EPS TTM > 0 |
| `eps_growth_bucket` | str | EPS_NEGATIVE / EPS_LOW / EPS_MED / EPS_HIGH / EPS_UNKNOWN |
| `gross_margin_bucket` | str | GM_LOW / GM_MED / GM_HIGH / GM_VERY_HIGH / GM_UNKNOWN |
| `operating_margin_bucket` | str | OM_NEG / OM_LOW / OM_MED / OM_HIGH / OM_UNKNOWN |
| `valuation_zone` | str | BELOW_HISTORICAL_LOW / LOW_VALUE_ZONE / FAIR_VALUE_ZONE / HIGH_VALUE_ZONE / OVERVALUED_ZONE / UNAVAILABLE |
| `pe_bucket` | str | PE<8 / PE_8-12 / PE_12-18 / PE_18-25 / PE>=25 / NO_EPS |
| `timing_quality` | str | MOPS / ESTIMATED / UNKNOWN |
| `timing_estimated` | bool | announcement_date 為估計值（法定申報期限推算） |

---

## 因子分析類型

### 1. Boolean Factor（布林因子）
比較 True / False 兩群的前向報酬。

例：`eps_positive=True` vs `eps_positive=False`

### 2. Zone Factor（類別因子）
按標籤分組，計算各組平均報酬、勝率、Profit Factor。

例：`valuation_zone`、`pe_bucket`、`eps_growth_bucket`

### 3. Filter Effect（篩選效果）
比較「通過篩選」vs「未通過篩選」的報酬差異。

例：`long_term_signal==BUY_BREAKOUT` vs 其他

### 4. Numeric Bucket（數值分桶）
將連續數值切分成桶，計算各桶統計。

例：`long_term_score` 切分為 <0 / 0-4 / 4-7 / ≥7

---

## 輸出檔案

| 檔案 | 說明 |
|------|------|
| `data/backtest_results/long_term_signals_<ts>.csv` | 逐 symbol 逐 date 信號與前向報酬 |
| `data/backtest_results/long_term_eps_factor_<ts>.csv` | EPS bucket 分析 |
| `data/backtest_results/long_term_gm_factor_<ts>.csv` | 毛利率 bucket 分析 |
| `data/backtest_results/long_term_val_factor_<ts>.csv` | 估值區間分析 |
| `data/backtest_results/long_term_score_factor_<ts>.csv` | 長線評分 bucket 分析 |
| `reports/long_term_validation_report_<ts>.md` | 完整 Markdown 報告 |

以上輸出檔案均已加入 `.gitignore`，不提交至 repo。

---

## 統計置信度

`StatConfidence.for_long_term_strategy()` 評估規則（v0.3.11）：

| 條件 | 判定 |
|------|------|
| symbol_count < 10 | INSUFFICIENT |
| signal_count < 30 | INSUFFICIENT |
| signal_count 30–199 | OBSERVATIONAL |
| trading_days < 120 | not RELIABLE |
| fundamental_rows/symbol < 4 | OBSERVATIONAL（降級） |
| timing_estimated_ratio > 80% | 新增 timing_warning |

**14 個股的預期結果**：INSUFFICIENT（樣本量不足，僅確認框架功能正常）。

擴大 universe 路徑：
1. `python main.py build-universe-manifest --size 30`
2. 匯入 30 個股的 XQ 日線資料
3. `python main.py fetch-daily-history --universe 30 --years 3`
4. `python main.py backtest-long-term-strategy --mode real`

---

## 資料穿越說明（Data Leakage）

**目前限制**：基本面資料（EPS、毛利率）為靜態快照，非 per-date 過濾。
每個評估點使用的是「現在能看到的最新財報」，而非「那個日期能看到的財報」。

**已有的防護機制**：
- `timing_estimated` 欄位標示估計公告日（法定申報期限）
- `formal_allowed=False` 阻擋正式長線下單判斷
- 報告在置信度說明中明確標示 PARTIAL / OBSERVATIONAL 等級

**未來改進**：
- 按 `announcement_date` 過濾：只使用公告日之前的財報資料
- 建立季度財報時間序列（多個 quarter 的歷史記錄）

---

## 注意事項

> **[!] 本框架僅供研究與模擬，不構成投資建議。**
> 統計樣本量不足時，所有因子分析結果不可用於實際交易決策。
> 所有前向報酬為歷史數據，不保證未來表現。

---

*TW Quant Cockpit v0.3.11 — 2026*
