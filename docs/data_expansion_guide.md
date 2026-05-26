# TW Quant Cockpit v0.3.2 — Data Expansion Guide

> **[!] 本系統僅供研究、模擬交易與決策輔助，不構成投資建議。**

---

## 為什麼需要 50～200 檔？

- 3～5 檔樣本：只能驗證功能是否正常運作（FUNCTIONAL_TEST）
- 10～49 檔：SMALL_SAMPLE，回測結果僅供參考
- 50～99 檔：BASIC_VALIDATION，可初步檢視策略傾向
- 100～199 檔：GOOD_VALIDATION，結果較具參考價值
- 200+ 檔：PRACTICAL_SAMPLE，可進行較系統性策略研究

數量少時，回測結果可能高估績效、受特定產業偏誤影響、具高隨機性。**擴充樣本不改善策略，只讓結論更誠實。**

---

## 回測信心階段

| 階段 | 股票數 | 說明 |
|------|-------|------|
| FUNCTIONAL_TEST | < 10 | 功能驗證，不具統計意義 |
| SMALL_SAMPLE | 10–49 | 小樣本，觀察用 |
| BASIC_VALIDATION | 50–99 | 基本驗證，初步可用 |
| GOOD_VALIDATION | 100–199 | 較好驗證，建議階段 |
| PRACTICAL_SAMPLE | 200+ | 實用樣本，較可信 |

---

## 每檔股票需要的資料長度

| 資料類型 | 最低需求 | 建議長度 | 說明 |
|---------|---------|---------|------|
| daily（日K） | 20 列 | ≥ 120 列 | 短線需20，長線需120+ |
| institutional（法人買賣）| 5 列 | ≥ 40 列 | 短/中線需5+ |
| margin（融資融券） | 5 列 | ≥ 40 列 | 短/中線需5+ |
| monthly_revenue（月營收） | 6 個月 | ≥ 12 個月 | 中線需6，長線需12 |
| holder（大戶散戶比例） | 2 期 | ≥ 4 期 | 中/長線需2+ |
| trust_cost（投信成本） | 3 列 | ≥ 20～40 列 | 輔助參考 |

---

## 匯入順序

建議依下列順序匯入，確保資料完整性：

1. **Profile** — 建立股票基本資料（symbol, name, market, industry, theme_tags）
2. **Daily K** — 日K資料（date, symbol, open, high, low, close, volume）
3. **Institutional** — 法人買賣（date, symbol, foreign_net_buy, trust_net_buy, dealer_net_buy）
4. **Margin** — 融資融券（date, symbol, margin_balance, margin_change, short_balance, short_change）
5. **Monthly Revenue** — 月營收（month, symbol, revenue, mom, yoy, accumulated_yoy）
6. **Holder** — 大戶散戶比例（date, symbol, major_holder_ratio, retail_holder_ratio, ...）
7. **Trust Cost** — 投信成本（date, symbol, trust_buy_shares, trust_avg_cost, ...）

---

## 快速開始：使用 top50 sample

```bash
# 建立 50 檔 universe（台積電、聯發科、鴻海等主要成分股）
python main.py build-universe --template top50 --replace

# 確認 universe
python main.py universe-check

# 確認資料完整度
python main.py data-check --all
```

---

## build-universe 使用方式

### 使用內建 sample template

```bash
# 建立 top50 universe
python main.py build-universe --template top50 --replace

# 建立 top100 universe
python main.py build-universe --template top100 --replace

# 建立 top200 universe（部分 theme_tags 為概略分類）
python main.py build-universe --template top200 --replace
```

### 使用自備 profile CSV

```bash
# 追加匯入（預設，依 symbol 去重，新資料覆蓋舊資料）
python main.py build-universe --file D:\XQ\profile.csv

# 覆蓋匯入（完全取代現有 profile）
python main.py build-universe --file D:\XQ\profile.csv --replace
```

### Profile CSV 格式

```csv
symbol,name,market,industry,theme_tags,is_mainstream_theme,sector
2330,台積電,TWSE,半導體,AI/HPC/先進製程,1,半導體
2454,聯發科,TWSE,IC設計,手機晶片/AI Edge,1,半導體
```

**注意事項：**
- `symbol` 必須保留字串格式（含前置零，如 `0050`）
- `market` 支援 `TWSE` / `TPEx`
- `is_mainstream_theme` 填 `1` 或 `0`
- `theme_tags` 以 `/` 分隔多個題材

---

## batch-import 使用方式

### 匯入單一資料類型

```bash
# 匯入日K資料夾（資料夾內可含多個 CSV）
python main.py batch-import --type daily --folder D:\XQ\daily

# 匯入法人資料
python main.py batch-import --type institutional --folder D:\XQ\institutional

# 匯入融資融券資料
python main.py batch-import --type margin --folder D:\XQ\margin

# 匯入月營收
python main.py batch-import --type monthly_revenue --folder D:\XQ\revenue

# 匯入大戶散戶資料
python main.py batch-import --type holder --folder D:\XQ\holder

# 匯入投信成本
python main.py batch-import --type trust_cost --folder D:\XQ\trust_cost
```

### 一次匯入 Bundle 結構

```bash
python main.py batch-import --bundle D:\XQ\twqc_bundle
```

Bundle 資料夾結構：

```
D:\XQ\twqc_bundle\
  profile\          ← 股票基本資料 CSV
  daily\            ← 日K CSV（可多個）
  institutional\    ← 法人買賣 CSV
  margin\           ← 融資融券 CSV
  monthly_revenue\  ← 月營收 CSV
  holder\           ← 大戶散戶 CSV
  trust_cost\       ← 投信成本 CSV
```

---

## 從 XQ / Excel / 手動 CSV 匯入

### XQ Global 匯出格式

XQ 通常匯出為 Excel 或 CSV，欄位可能為中文名稱。本系統支援自動轉換，例如：

- `股票代號` → `symbol`
- `日期` → `date`
- `開盤價` → `open`
- `最高價` → `high`
- `最低價` → `low`
- `收盤價` → `close`
- `成交量` → `volume`
- `外資買賣超` → `foreign_net_buy`
- `投信買賣超` → `trust_net_buy`

### 手動整理注意事項

1. **日K**：確保 date 格式為 YYYY-MM-DD
2. **月營收**：month 格式為 YYYY-MM（如 `2024-01`）
3. **symbol 格式**：必須是字串，0050 不可寫成 50
4. **缺日K**：除權息日可能缺漏，系統會回報但不會中斷匯入

---

## universe-check 解讀

```bash
python main.py universe-check
```

輸出說明：

| 欄位 | 說明 |
|------|------|
| Current symbols | 目前 profile 中的股票數 |
| Confidence stage | 樣本信心階段 |
| Daily ≥ 120 | 具備長線日K的股票數 |
| Institutional ≥ 40 | 具備充足法人資料的股票數 |
| Revenue ≥ 12 | 具備一年月營收的股票數 |

### 不同階段的建議行動

**目前 < 50 檔：**
1. 執行 `build-universe --template top50 --replace`
2. 匯入每檔至少 120 日 K
3. 匯入法人資料（至少 40 日）
4. 匯入融資融券（至少 40 日）
5. 匯入 12 個月月營收

**50–99 檔：**
1. 執行 `build-universe --template top100` 擴充到 100 檔
2. 補齊 holder / trust_cost 資料

**100 檔以上：**
1. 可執行 `validate-score --mode real` 進行較可信的分數驗證
2. 仍需注意產業分佈偏誤

---

## data-check --all 解讀

```bash
python main.py data-check --all
```

輸出欄位說明：

| 欄位 | 說明 |
|------|------|
| 日K | 日K筆數 |
| 法人 | 法人資料筆數 |
| 融資 | 融資融券筆數 |
| 月收 | 月營收期數 |
| 大戶 | 大戶散戶期數 |
| 投信成 | 投信成本筆數 |
| 短 | 短線正式分析允許（Y/N） |
| 中 | 中線正式分析允許（Y/N） |
| 長 | 長線正式分析允許（Y/N） |

底部匯總：

- **Short-ready**: 可做短線分析的股票數
- **Mid-ready**: 可做中線分析的股票數
- **Long-ready**: 可做長線分析的股票數
- **Validation stage**: 目前信心階段
- **Recommended next import**: 建議下一步匯入項目

---

## 驗證流程

完成資料匯入後，依序執行：

```bash
python main.py data-check --all
python main.py validate-score --mode real
python main.py backtest-buy-points --mode real
python main.py backtest-screener --mode real --top 8
```

**注意：** 資料不足時系統會顯示 `INSUFFICIENT`，不會強行計算或輸出過度自信的結論。

---

## 免責聲明

- 本系統所有回測與驗證結果**僅供研究與學習**，不構成投資建議
- 樣本數不足時，回測結果可能嚴重受到選股偏誤與隨機性影響
- 即使樣本達 200 檔，回測仍有 look-ahead bias 風險，使用者應謹慎解讀
- **禁止實盤自動下單**（`TWQC_ENABLE_REAL_ORDER` 必須為 `false`）
