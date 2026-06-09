# Crash Reversal & Risk Discipline Strategy Pack
# 大跌反轉與風險紀律策略包

**Version:** v0.9.0.1  
**Status:** Research Only — No Real Orders — Production Trading BLOCKED  
**Not Investment Advice**

---

## v0.9.0.1 目標 / Goals

This release introduces the **Crash Reversal & Risk Discipline Strategy Pack**, a structured
research framework for analyzing market crashes, classifying their cause, evaluating stabilization
conditions, and applying disciplined risk filters before any entry consideration is permitted.

**Core principle:** A large market drop does **not** automatically imply a research entry signal.
Every component in this pack is designed to prevent impulsive decisions and enforce evidence-based
discipline.

All outputs are **research-only**. No component generates BUY, SELL, ORDER, EXECUTE, or any
real-trading instruction. Production trading is permanently blocked in this pack.

---

## 大跌不是直接買 / Crash ≠ Auto Buy

> "大跌不是直接買的信號，是需要更多確認的信號。"
> "A large crash is not a direct entry signal — it is a signal that *more confirmation is required*."

A crash may represent:
- A temporary technical flush (訊號：市場修正，短期恐慌)
- A structural regime change (訊號：多頭轉空頭)
- A liquidity crisis (訊號：流動性危機，需等穩定)
- A macro/policy shock (訊號：政策/總經衝擊)

Each cause type has different implications, different recovery timelines, and different risk
discipline requirements. The pack classifies the crash first, then filters entry eligibility.

---

## 送分題 vs 轉空頭 / Gift Opportunity vs Bear Market Turn

| Scenario | 中文 | Characteristics | Research Action |
|---|---|---|---|
| Gift Opportunity | 送分題 | Short-term panic, strong fundamentals intact, MA structure holding, volume capitulation | Eligible for dip filter analysis |
| Bear Market Turn | 轉空頭 | Macro deterioration, MA structure broken, earnings estimates declining, sector rotation defensive | Ineligible — avoid dip analysis |

The **Crash Cause Classifier** and **Post-Crash Stabilization Checklist** together determine
which scenario applies. Only "gift opportunity" scenarios pass through to the downstream filters.

---

## Crash Cause Classifier / 大跌原因分類器

Classifies each crash event into one of four cause types, each with specific conditions and
research conclusions.

### Cause Types

| Cause Type | 中文 | Trigger Conditions | Research Conclusion |
|---|---|---|---|
| `TECH_FLUSH` | 技術性洗盤 | Price -5% to -15%, volume spike 2x+, MA structure intact, no fundamental change | Short-term flush; stabilization checklist required before analysis |
| `MACRO_SHOCK` | 總經衝擊 | Rate decision, CPI/PPI surprise, Fed policy shift, geopolitical event | Macro-driven; wait for policy clarity; high uncertainty |
| `LIQUIDITY_CRISIS` | 流動性危機 | Broad margin calls, correlation spike >0.85, credit spread widening, VIX >35 | Avoid until liquidity normalizes; funding risk elevated |
| `BEAR_TURN` | 空頭轉折 | MA60 breakdown, earnings estimate cuts, defensive rotation, breadth deterioration | Do not consider dip analysis; bear regime active |

### Scoring

- **Score 0–40:** Insufficient evidence, no analysis permitted
- **Score 41–60:** Partial evidence, high caution
- **Score 61–80:** Moderate evidence, stabilization checklist required
- **Score 81–100:** Strong evidence, proceed to full filter stack

### Risk Levels

| Risk Level | Score Range | Meaning |
|---|---|---|
| `LOW` | 81–100 | Evidence strong; lower regime risk |
| `MEDIUM` | 61–80 | Moderate evidence; caution required |
| `HIGH` | 41–60 | Partial evidence; high uncertainty |
| `EXTREME` | 0–40 | Insufficient evidence; analysis blocked |

---

## Post-Crash Stabilization Checklist / 大跌後穩定核查清單

Eight weighted checklist items that must be evaluated before any downstream analysis is
considered valid.

| # | Item | 中文 | Weight | Passing Condition |
|---|---|---|---|---|
| 1 | Volume Dry-Up | 成交量萎縮 | 15% | Daily volume < 50% of crash-day volume |
| 2 | Price Stabilization | 價格穩定 | 15% | 3+ consecutive days without new lows |
| 3 | MA5 Recapture | MA5 回收 | 10% | Price closes above 5-day moving average |
| 4 | Sector Leaders Holding | 龍頭股守住 | 15% | Top 3 sector leaders not making new lows |
| 5 | Breadth Recovery | 市場廣度回升 | 10% | Advance/Decline ratio > 1.2 for 2+ days |
| 6 | VIX Declining | VIX 下降 | 10% | VIX trending down from crash-day high |
| 7 | Index Support Hold | 指數支撐守住 | 15% | Key index (e.g., MA20 or prior pivot) holding |
| 8 | No New Macro Shock | 無新總經衝擊 | 10% | No new policy/macro event in prior 5 sessions |

**Passing threshold:** Weighted score ≥ 65% required to proceed to relative strength and dip filters.

---

## Relative Strength After Crash Score / 大跌後相對強度評分

Evaluates each symbol's strength relative to the market during and after the crash.

### Scoring Table

| Condition | 中文 | Points |
|---|---|---|
| Price decline < market decline | 跌幅小於大盤 | +25 |
| Recovery started before index | 早於指數開始反彈 | +20 |
| MA5 > MA10 (short-term uptrend intact) | 短期均線排列向上 | +15 |
| Volume confirming recovery | 量能配合回升 | +20 |
| Sector leadership (top quartile) | 板塊龍頭地位 | +10 |
| EPS estimate not cut | 獲利預估未下修 | +10 |

**Rating Scale:**
- 76–100 → `STRONG` — Eligible for further filters
- 51–75  → `MODERATE` — Caution; additional confirmation required
- 26–50  → `WEAK` — Not eligible
- 0–25   → `VERY_WEAK` — Actively avoid

### Forbidden Traps / 禁止陷阱

The following patterns disqualify a symbol from analysis regardless of score:

| Trap | 中文 | Description |
|---|---|---|
| Dead Cat Bounce | 死貓彈 | Price recovery without volume; new low likely |
| Falling Knife | 下落刀鋒 | No stabilization signs; downtrend accelerating |
| Sector Contagion | 板塊傳染 | Whole sector in breakdown; no relative safety |
| Earnings Deterioration | 獲利惡化 | Forward EPS estimates declining |

---

## Sakata EPS-backed Dip Buy Filter / 酒田法則EPS支撐低點買進過濾器

Filters symbols for EPS-backed dip consideration using Sakata method principles combined
with fundamental anchors.

### Allowed Conditions / 允許條件

| Condition | 中文 |
|---|---|
| Positive EPS (trailing 12m) | 過去12個月EPS為正 |
| EPS growth ≥ 0% YoY | EPS年增率 ≥ 0% |
| P/E below 5-year median | 本益比低於5年中位數 |
| No dividend cut in past 12m | 過去12個月未減息 |
| Price within 20% of 52-week MA | 股價在52週均線20%以內 |

### Forbidden Conditions / 禁止條件 (any one disqualifies)

| Condition | 中文 |
|---|---|
| Negative EPS | EPS為負值 |
| EPS estimate cut ≥ 10% | 獲利預估下修 ≥ 10% |
| Debt/Equity > 3.0 | 負債股本比 > 3.0 |
| Revenue decline > 15% YoY | 營收年衰退 > 15% |
| Sector in confirmed bear trend | 所屬板塊確認空頭趨勢 |

### Scoring

- Each allowed condition met: +20 points (max 100)
- Any forbidden condition present: score = 0, `eligible = False`
- Threshold for `eligible = True`: score ≥ 60

---

## Moving Average Profit Discipline / 移動平均線獲利紀律

Enforces structured exit discipline based on MA alignment. Prevents holding through
full trend reversals.

### MA Rules Table

| MA Level | 中文 | Rule | Action Hint |
|---|---|---|---|
| MA5 | 5日均線 | Short-term momentum; price must be above for continuation | Monitor daily |
| MA10 | 10日均線 | 2-week trend; first line of support discipline | Re-evaluate if broken |
| MA20 | 20日均線 | Monthly trend; critical support level | Reduce risk on sustained break |
| MA60 | 60日均線 | Quarterly trend; major regime indicator | Significant risk reduction required if broken |

### Trend Status Definitions

| Status | Condition | Meaning |
|---|---|---|
| `ALIGNED_BULL` | MA5 > MA10 > MA20 > MA60 | Full bullish alignment |
| `PARTIAL_BULL` | MA5 > MA20, MA60 intact | Partial alignment; proceed cautiously |
| `MIXED` | Mixed MA ordering | No clear trend; reduce exposure |
| `PARTIAL_BEAR` | MA5 < MA20, MA60 beginning to fall | Bearish developing; high caution |
| `ALIGNED_BEAR` | MA5 < MA10 < MA20 < MA60 | Full bearish alignment; avoid |

**Discipline rule:** When `ALIGNED_BEAR` is detected, all analysis for that symbol is suspended
until MA structure improves to at least `MIXED`.

---

## High-Risk Industry Exposure Guard / 高風險產業曝險防護

Applies additional restrictions to symbols in structurally high-risk industries.

### Covered Industries / 涵蓋產業

| Industry | 中文 | Risk Multiplier | Max Position | Financing | Hard Stop |
|---|---|---|---|---|---|
| Semiconductor | 半導體 | 1.5x | 15% of portfolio | Restricted | MA60 break |
| Biotech / Pharma | 生技製藥 | 2.0x | 10% of portfolio | Blocked | MA20 break |
| Leveraged Finance | 槓桿金融 | 2.5x | 5% of portfolio | Blocked | Any new low |
| Crypto-exposed | 加密貨幣曝險 | 3.0x | 5% of portfolio | Blocked | Any new low |
| High-debt cyclical | 高負債景氣循環 | 2.0x | 10% of portfolio | Restricted | MA60 break |
| Emerging market | 新興市場 | 1.5x | 15% of portfolio | Restricted | MA60 break |

**Notes:**
- "Financing Restricted" = no margin/leverage permitted in research models
- "Financing Blocked" = position must be fully cash-based in any simulation
- "Hard Stop" = automatic disqualification trigger; research analysis suspended
- All position sizes are for **research simulation only** — no real orders

---

## CLI Usage / 命令列使用方式

Five primary CLI commands for the Crash Reversal pack:

```bash
# 1. Run full crash reversal check (market + all universe symbols)
python main.py crash-reversal --mode real

# 2. Run market-level crash cause classification only
python main.py crash-reversal-market --mode real

# 3. Run symbol-level filters for a specific ticker
python main.py crash-reversal-symbol --symbol 2330 --mode real

# 4. Generate crash reversal report
python main.py crash-reversal-report --mode real --output reports/

# 5. Print crash reversal summary (safe command, no forbidden keywords)
python main.py crash-reversal-summary
```

**All commands output research data only. No BUY/SELL/ORDER output. No real trades.**

---

## GUI Usage / 圖形介面使用方式

The **Crash Reversal** tab in TW Quant Cockpit provides:

1. **Safety Banner** — Prominent warning at top: Research Only, No Real Orders, Production Trading BLOCKED
2. **Crash Cause Card** — Shows current crash cause type, score, risk level, action hint, and evidence
3. **Stabilization Checklist** — Table of all 8 checklist items with pass/fail status, scores, weights, evidence
4. **Relative Strength Table** — Per-symbol RS scores, ratings, conditions met, forbidden trap flags
5. **EPS-backed Dip Filter Table** — Per-symbol eligibility, score, allowed/forbidden reason, next safe action hint
6. **MA Profit Discipline Table** — Per-symbol MA5/10/20/60 values, trend status, disciplined action hint
7. **High Risk Industry Guard Table** — Per-symbol industry classification, risk multiplier, position limits, warnings

**Action buttons:**
- **Run Crash Reversal Check** — Runs the full pack in a background thread (non-blocking)
- **Generate Report** — Saves Markdown report to `reports/` directory
- **Refresh** — Resets all tables to empty state
- **Copy Safe Command** — Copies a safe CLI command to clipboard (no forbidden keywords)

---

## Report Usage / 報告使用方式

Reports are generated to `reports/crash_reversal_strategy_report_YYYY-MM-DD.md`.

Each report includes:
- Generation timestamp and version
- Market crash cause classification result
- Stabilization checklist weighted score and status
- Per-symbol relative strength analysis
- Per-symbol EPS-backed dip filter results
- MA discipline status per symbol
- Industry guard warnings per symbol
- Full safety disclaimer

To generate a report:
```bash
python main.py crash-reversal-report --mode real
```

Or via GUI: click **Generate Report** in the Crash Reversal tab.

---

## Strategy Lab Integration / 策略實驗室整合

The Crash Reversal pack integrates with Strategy Lab Stable (v0.9.0):

- **Capability registration:** `crash_reversal_pack` registered as a Strategy Lab capability
- **Check status:** Crash reversal checks feed into the Strategy Lab stable checklist
- **Memory integration:** Analysis results can be stored via Strategy Memory for review
- **Evidence graph:** Crash cause and stabilization evidence fed into Research Intelligence Evidence Graph

To run Strategy Lab validation including crash reversal:
```bash
python main.py strategy-lab --mode real
```

---

## No Real Orders Disclaimer / 無真實訂單聲明

> **This pack does not generate, submit, or execute any real orders.**
>
> All outputs are research data for informational and educational purposes only.
> No component of this pack interfaces with any broker, exchange, trading API,
> or order management system.
>
> The strings BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE, and REAL_TRADE
> are permanently forbidden from all outputs of this pack.
>
> 本套件不產生、提交或執行任何真實訂單。所有輸出均為研究資料，僅供資訊與教育目的。
> 本套件不與任何券商、交易所、交易API或訂單管理系統連接。

---

## Not Investment Advice Disclaimer / 非投資建議聲明

> **This software and all its outputs are NOT investment advice.**
>
> TW Quant Cockpit is a research and analysis tool. Nothing in this system
> constitutes a recommendation to buy, sell, or hold any security. Past
> performance of any analysis framework does not guarantee future results.
> All users are solely responsible for their own investment decisions.
>
> 本軟體及其所有輸出均非投資建議。TW Quant Cockpit 是研究與分析工具。
> 本系統中的任何內容均不構成買入、賣出或持有任何證券的建議。
> 任何分析框架的過往表現不保證未來結果。所有用戶對其自身投資決策負全責。

---

*Generated for TW Quant Cockpit v0.9.0.1 — Crash Reversal & Risk Discipline Strategy Pack*  
*2026-06-09*
