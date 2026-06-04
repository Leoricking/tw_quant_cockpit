# Strategy Filter Pack — Financial Turnaround & Trend Discipline

> **[!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.**

Version: v0.5.1.1

---

## 概述

**策略名稱:** 財報翻多 + 趨勢紀律策略篩選  
**English:** Financial Turnaround & Trend Discipline

這是**策略篩選與研究框架**，不是自動交易系統。

- 不下單
- 不自動買賣
- 不自動改權重
- 不自動啟用 ML feature
- 不接券商 API 下單
- 所有輸出標示 Research Only / Strategy Filter Only / No Real Orders / Production Trading BLOCKED

---

## 核心邏輯

### 1. 財報決定是否有上漲理由

- EPS 明顯成長
- Q1 EPS × 4 粗估全年 EPS
- 月營收續強
- 毛利率 / 營益率未惡化
- 股價相對推估 EPS 尚未過度昂貴
- **財報好不等於明天一定漲，只代表值得追蹤**

### 2. 技術面決定買點

- 低位階
- 底部翻多
- 突破下降壓力
- 站上 5 / 10 / 20 日線
- 回測 5 日線 / 10 日線 / 頸線不破
- **不追高，只找回測不破或站回關鍵線**

### 3. 籌碼決定是否有人抬轎

- 外資 / 投信 / 自營商未連續大賣
- 投信續買或投信成本附近有支撐
- 大戶增加、散戶下降加分
- 融資未暴增
- 散戶追高過多扣分

### 4. 均線決定抱不抱

- 20 日線 / 月線為第一道防線
- 跌破 20 日線且 3 天站不回，減碼 1/3～1/2
- 60 日線 / 季線為第二道防線
- 跌破 60 日線且無法快速站回，趨勢轉弱
- 重新站回月線 / 季線，可重新評估回補

### 5. 風控避免一次出局

- 不融資
- 不單押
- 控制持股數
- 不追新聞熱點
- 不猜頂底

---

## 三大劇本

### 劇本 A：財報好 + 低位階 + 技術翻多

**條件：**
- Q1 EPS 明顯成長
- 月營收續強
- 股價低位階
- 突破下降壓力
- 站上 5 / 10 / 20 日線
- 法人沒有連續大賣
- 融資沒有暴增

**判斷：**
- 偏多
- 等回測 5 日線 / 10 日線 / 頸線不破再觀察
- 屬於第二波買點候選

**系統標籤：**
`FINANCIAL_TURNAROUND` | `LOW_BASE_BREAKOUT` | `SECOND_WAVE_CANDIDATE` | `PULLBACK_ENTRY_ONLY`

---

### 劇本 B：財報好，但已經大漲

**條件：**
- 財報很好
- 股價已連漲一大段
- 爆大量 + 長上影
- KD / RSI 過熱
- 散戶大量追進
- 法人開始調節
- 跌破 5 日線且放量

**判斷：**
- 不追高
- 等回測
- 若跌破 5 日線且放量，先減碼

**系統標籤：**
`GOOD_FUNDAMENTAL_BUT_EXTENDED` | `DO_NOT_CHASE` | `TAKE_PROFIT_OR_REDUCE` | `WAIT_PULLBACK`

---

### 劇本 C：財報差 + 大盤創高但個股不過高

**條件：**
- 大盤創高
- 個股兩個高點沒過
- EPS 沒成長
- 營收衰退
- 純題材但營收跟不上
- 跌破 20 日線 / 60 日線

**判斷：**
- 汰弱換強
- 不硬抱
- 降低評分
- 避開或換股

**系統標籤：**
`RELATIVE_WEAKNESS` | `FUNDAMENTAL_DETERIORATION` | `TOP_PATTERN_RISK` | `AVOID_OR_ROTATE`

---

## 分數權重

**Financial Turnaround Trend Score — 0～100 分**

| 維度 | 滿分 |
|------|------|
| 財報 / EPS 成長 | 25 |
| 月營收 / 毛利率 / 營益率續強 | 15 |
| 低位階 / 底部翻多 | 15 |
| 技術轉強 / 站回均線 | 15 |
| 法人 / 籌碼支持 | 15 |
| 風控健康度 / 融資未失控 | 10 |
| **小計** | **95** |
| 避雷扣分（最多 -30） | -30 |

---

## 加分條件

| 條件 | 加分 |
|------|------|
| EPS 年增明顯 | +10 |
| Q1 EPS × 4 後本益比仍合理 | +8 |
| 月營收續強 | +8 |
| 站上 5 / 10 / 20 日線 | +8 |
| 回測 10 日線不破 | +8 |
| 突破下降壓力 | +8 |
| 法人未連續大賣 | +8 |
| 大戶增加、散戶下降 | +6 |
| 融資未暴增 | +5 |

---

## 扣分條件

| 條件 | 扣分 |
|------|------|
| 高檔爆量長上影 | -10 |
| KD / RSI 過熱且放量轉弱 | -8 |
| 法人轉賣 | -8 |
| 融資暴增 | -8 |
| 大盤創高但個股不過前高 | -10 |
| EPS 衰退 | -12 |
| 營收衰退 | -10 |
| 跌破 20 日線且 3 天站不回 | -12 |
| 跌破 60 日線 | -15 |
| M 頭 / 多重頂 / 頭肩頂 / 弧形頂 | -15 |

---

## 評分判讀

| 分數 | 判讀 |
|------|------|
| 80～100 | 財報翻多強勢候選，可等回測買點 |
| 65～79 | 觀察股，等技術確認 |
| 50～64 | 僅觀察，不追 |
| < 50 | 避開或汰弱換強 |

---

## 使用方式

```bash
# 單股篩選
python main.py strategy-filter --stock 2454 --mode real
python main.py strategy-filter --stock 2383 --mode real --report

# 全包篩選
python main.py strategy-filter-pack --mode real
```

### 輸出欄位

| 欄位 | 說明 |
|------|------|
| Score | 0～100 分 |
| Scenario | 劇本 A / B / C |
| Labels | 系統標籤 |
| Suggested Action | WATCH / WAIT_PULLBACK / SECOND_WAVE_CANDIDATE / REDUCE_RISK / AVOID / ROTATE_TO_STRONGER |
| Entry Conditions | 進場條件清單 |
| Risk Conditions | 風險條件清單 |
| Avoid Conditions | 避開條件清單 |

> **Suggested Action 僅供研究參考，不可輸出 BUY / SELL / ORDER。**

---

## 不下單 / 不接實盤

本系統是策略篩選與研究框架：

- 所有輸出僅供研究使用
- 不自動下單
- 不接券商 API
- 不自動改權重
- 不自動啟用 ML feature
- Production Trading: BLOCKED

---

*docs/strategy_filter_pack.md — v0.5.1.1*
