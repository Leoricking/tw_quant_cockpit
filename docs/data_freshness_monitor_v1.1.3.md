# Data Freshness Monitor — v1.1.3

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] Auto External Refresh: DISABLED. Stale Auto Repair: DISABLED.
> [!] Future Date does not count as Fresh.
> [!] Not Investment Advice.

---

## v1.1.3 目標

v1.1.3 Data Freshness Monitor 的目標是持續監控 TW Quant Cockpit 的資料新鮮度，確保研究流程使用的歷史資料是最新、可信賴、且沒有異常的。

**核心能力：**
- 可識別的資料新鮮度狀態（8 種 status）
- 可計算的 Trading-day lag（工作日滯後，非日曆天）
- 可追蹤的 Source 健康度（HEALTHY / DEGRADED / INTERRUPTED / UNKNOWN）
- 可偵測的異常：Future Date、Date Regression、Partial Update、Source Interruption
- 可輸出的 Repair Handoff task list（僅建立任務，不執行修復）
- 可匯出的 Markdown 報告
- 可整合 GUI Panel（PySide6，read-only）

**安全原則（不可更改）：**
- `research_only = True`
- `no_real_orders = True`
- `auto_download_disabled = True`
- `auto_repair_disabled = True`
- Mock 資料不得用於正式 freshness 結論

---

## 一、Freshness Status 定義

| Status | 說明 | 嚴重度 |
|--------|------|--------|
| `FRESH` | 資料日期 = 預期最新交易日，無異常 | INFO |
| `ACCEPTABLE` | 資料日期在 SLA 內（1–2 個交易日滯後），可接受 | LOW |
| `DELAYED` | 資料日期超過 SLA 下限但未達 STALE 門檻（通常 2–5 個交易日） | MEDIUM |
| `STALE` | 資料日期遠超 SLA（通常 >5 個交易日滯後），資料已明顯過時 | HIGH |
| `INTERRUPTED` | 來源中斷：多個 symbol 同源、同時段全部 STALE，視為 source interruption | CRITICAL |
| `MISSING` | 完全沒有任何資料行，資料缺失 | CRITICAL |
| `FUTURE_DATE` | 資料日期超過當前日期，不可能是真實已發生的資料 | CRITICAL |
| `DATE_REGRESSION` | 最新資料日期比上一次已知日期更舊，資料發生倒退 | CRITICAL |

> [!] `FUTURE_DATE` 不計為 FRESH。Future date 一律為 P0 異常，需人工審查。
> [!] `DATE_REGRESSION` 為 P0 異常，表示資料被錯誤覆寫或資料管道出錯。

---

## 二、Trading-day Lag 說明

**Trading-day lag ≠ 日曆天數差異**

Trading-day lag 是指「資料最新日期距離預期最新交易日的交易日天數差」，排除週末與公眾假期。

**計算方式：**
```
lag = count_trading_days(actual_latest_date + 1 day → expected_latest_date)
```

**範例：**
- 預期最新日期：2024-03-15（週五）
- 資料最新日期：2024-03-12（週二）
- 日曆天差：3 天
- Trading-day lag：**2 個交易日**（週三 2024-03-13、週四 2024-03-14 為交易日，2024-03-12 之後到 2024-03-15 之間有 2 個交易日未更新）

**為何使用 trading-day lag：**
- 週末本來就沒有交易，不應計入滯後
- 假日亦同（但目前為近似值，見第三節）
- 讓 SLA 門檻有意義：「延遲 2 個交易日」比「延遲 3 個日曆天」更精確

---

## 三、Trading Calendar 說明

### 使用方式

`TradingCalendar`（`data_freshness/trading_calendar.py`）負責判斷某日是否為交易日，並計算 trading-day lag。

### 近似值（Approximate）模式

**目前版本使用週一至週五的工作日啟發式規則**，沒有載入官方 TWSE 假期清單。

- `is_approximate()` 回傳 `True`
- `calendar_source()` 回傳 `"weekday_heuristic"`

這代表：
- 週末（週六、週日）正確排除
- 台灣國定假日**無法排除**（例如：228 和平紀念日、清明節、端午節、中秋節、國慶日等）
- 假期當週的 trading-day lag 可能被低估

### 載入假期清單

可以用 `cal.load_holidays(list_of_dates)` 載入已知假期：

```python
from datetime import date
from data_freshness.trading_calendar import TradingCalendar

cal = TradingCalendar()
cal.load_holidays([
    date(2024, 2, 28),  # 228 和平紀念日
    date(2024, 4, 4),   # 兒童節
    # ...
])
```

載入後 `is_approximate()` 回傳 `False`，`calendar_source()` 回傳 `"provided_holiday_list"`。

---

## 四、近似假期日曆限制

由於沒有官方 TWSE 假期清單，本系統有以下限制：

1. **假期 lag 低估**：如果資料在假期前後正常更新，但假期造成的 1–2 天空缺可能被誤算為 DELAYED。
2. **不可主張精確 SLA 達標**：在 `is_approximate=True` 時，「完全符合 SLA」的聲明不可靠。
3. **報告中會標明**：所有報告在「總覽」區塊都會顯示 `Calendar Approximate: True`，提醒使用者。

---

## 五、Dataset SLA 表

| Dataset | 頻率 | SLA 門檻 | FRESH | ACCEPTABLE | DELAYED | STALE |
|---------|------|---------|-------|------------|---------|-------|
| `DAILY_PRICE` | 日頻 | 1 交易日 | 0 lag | 1 lag | 2–5 lag | >5 lag |
| `VOLUME` | 日頻 | 1 交易日 | 0 lag | 1 lag | 2–5 lag | >5 lag |
| `CHIPS` | 日頻 | 2 交易日 | 0–1 lag | 2 lag | 3–7 lag | >7 lag |
| `MARGIN` | 日頻 | 2 交易日 | 0–1 lag | 2 lag | 3–7 lag | >7 lag |
| `SHORT_INTEREST` | 日頻 | 2 交易日 | 0–1 lag | 2 lag | 3–7 lag | >7 lag |
| `REVENUE` | 月頻 | 10 日（月底後） | ≤10 calendar days after month-end | 11–20 days | 21–40 days | >40 days |
| `FUNDAMENTALS` | 季頻 | 45 日（季末後） | ≤45 calendar days after quarter-end | 46–60 days | 61–90 days | >90 days |

> [!] SLA 門檻為近似值。官方公告時程可能因公司、主管機關要求而有所不同。

---

## 六、日頻 / 月頻 / 季頻差異說明

### 日頻資料（DAILY_PRICE, VOLUME, CHIPS, MARGIN, SHORT_INTEREST）

- 每個交易日更新一次
- 使用 trading-day lag 計算（工作日，非日曆天）
- 預期最新日期 = 最近一個交易日

### 月頻資料（REVENUE）

- 每個月底後約 10 個日曆天內發布
- 使用日曆天計算，不使用 trading-day lag
- 預期最新資料 = 上個月份（例如：現在是 2024-03-15，預期最新月份為 2024-02）
- SLA：月底後 10 天內 = FRESH，11–20 天 = ACCEPTABLE，21–40 天 = DELAYED，>40 天 = STALE

### 季頻資料（FUNDAMENTALS）

- 每季末後約 45 個日曆天內發布
- 使用日曆天計算
- 預期最新資料 = 上季（例如：現在是 2024-03-15，預期最新季度為 2023Q4）
- SLA：季末後 45 天內 = FRESH，46–60 天 = ACCEPTABLE，61–90 天 = DELAYED，>90 天 = STALE

---

## 七、Stale 偵測流程

1. **取得預期最新交易日**：呼叫 `TradingCalendar.expected_latest_trading_date()`
2. **比較實際最新資料日期**：從 CSV 取得最後一筆資料的日期
3. **計算 trading-day lag**：`TradingCalendar.count_trading_days(actual+1, expected)`
4. **套用 SLA 門檻**：根據 dataset 的 SLA 設定，判斷 status
5. **偵測特殊異常**：
   - `actual_date > today` → `FUTURE_DATE`
   - `actual_date < previous_known_date` → `DATE_REGRESSION`
   - `row_count == 0` → `MISSING`
6. **建立 DatasetFreshnessRecord**：記錄所有欄位，包括 `reason` 說明

---

## 八、Source Interruption 偵測

Source Interruption 表示來源系統（例如資料供應商 API）可能發生中斷，導致多個 symbol 同時停止更新。

### 偵測條件（DataSourceFreshnessMonitor）

滿足以下**全部條件**時，判定為 `SOURCE_INTERRUPTION`：

1. **最小樣本保護**：同一來源至少有 **5 個 symbol**（避免小樣本誤判）
2. **多數 STALE**：該來源超過 **50%** 的 symbol 為 STALE 或 MISSING
3. **同時發生**：所有 STALE symbol 的最新日期在同一個時間窗口內（集中性）

### 影響

- 來源的 `SourceFreshnessStatus.status` 設為 `SOURCE_INTERRUPTED`
- 所有受影響的 symbol 狀態升級為 `INTERRUPTED`（severity: CRITICAL）
- 產生 `SOURCE_INTERRUPTION` alert
- Repair Handoff 中建立 source-level 任務（非 per-symbol）

### 最小樣本保護說明

如果某來源只有 1–4 個 symbol，即使全部 STALE，也**不判定為 SOURCE_INTERRUPTION**，改為個別 STALE。這避免因為偶然的小型資料集被誤判為來源中斷。

---

## 九、Future Date 說明

### 定義

`FUTURE_DATE`：資料集中有日期**晚於當前日期**（`as_of` 時間）的資料行。

### 為何不算 FRESH

Future date 代表資料中混入了不可能存在的「未來資料」。可能原因：
- 測試資料混入生產路徑
- 資料管道日期解析錯誤
- 系統時鐘異常

因此 v1.1.3 明確規定：**Future date 不計為 FRESH，一律為 P0 異常。**

### 處理方式

- status = `FUTURE_DATE`
- severity = `CRITICAL`
- priority = `P0`
- Repair action = `REVIEW`（人工審查，不自動刪除）

> [!] Future date 資料**不會被自動刪除**。系統僅標記並建立 handoff task，需人工處理。

---

## 十、Date Regression 說明

### 定義

`DATE_REGRESSION`：資料的最新日期比上一次已知的最新日期**更舊**。

例如：
- 前次掃描時，TST1 的最新日期為 2024-03-15
- 本次掃描時，TST1 的最新日期為 2024-03-10
- → 發生 DATE_REGRESSION

### 可能原因

- 資料管道錯誤覆寫（truncation + partial reload）
- 資料版本錯誤
- CSV 檔被舊版本覆蓋
- 來源 API 回傳舊資料

### 處理方式

- status = `DATE_REGRESSION`
- severity = `CRITICAL`
- priority = `P0`
- Repair action = `REVIEW`（人工審查）

> [!] Date Regression 為 P0 異常，不自動修復。必須人工確認原因後才能清除。

---

## 十一、Partial Update 偵測

Partial Update 指的是部分資料已更新，但相關配對資料尚未更新，造成資料不一致。

### 主要模式

1. **DAILY_PRICE fresh，VOLUME missing / stale**：
   - 價格已更新但成交量資料缺失
   - 影響：部分依賴 price-volume 聯合分析的指標可能失效

2. **Source partial failure**：
   - 同一來源的部分 symbol 更新、部分未更新
   - 但尚未達到 SOURCE_INTERRUPTION 門檻

3. **Coverage not refreshed**：
   - 新 symbol 已加入 Universe，但 freshness coverage 掃描尚未納入
   - alert_type = `COVERAGE_NOT_REFRESHED`

### 偵測方式

`DataFreshnessReportBuilder` 在「七、Partial Updates」章節會：
1. 逐一比對每個 symbol 的 DAILY_PRICE 狀態 vs VOLUME 狀態
2. 如果 DAILY_PRICE 為 FRESH/ACCEPTABLE 但 VOLUME 為 STALE/MISSING，標記為 partial
3. 列出所有 `PARTIAL_UPDATE` 和 `COVERAGE_NOT_REFRESHED` alert

---

## 十二、Repair Handoff 映射表

Repair Handoff 將 alert 轉換為可追蹤的任務清單，**不執行任何修復動作**。

| Alert Type | Issue Type | Action | Auto-Safe | Priority |
|-----------|-----------|--------|-----------|----------|
| `DATA_STALE` | `STALE_DATA` | `REVIEW` | No — manual required | P1 |
| `DATA_MISSING` | `MISSING_SYMBOL_DATA` | `INVESTIGATE` | No — manual required | P1 |
| `SOURCE_INTERRUPTION` | `SOURCE_INTERRUPTION` | `SOURCE_REQUIRED` | No — manual required | P0 |
| `FUTURE_DATE` | `FUTURE_DATE_ANOMALY` | `REVIEW` | No — manual required | P0 |
| `DATE_REGRESSION` | `DATE_REGRESSION_ANOMALY` | `REVIEW` | No — manual required | P0 |
| `COVERAGE_NOT_REFRESHED` | `COVERAGE_STALE` | `REFRESH_COVERAGE` | Yes (metadata only) | P2 |

> [!] `SOURCE_INTERRUPTION` 建立 **一個** source-level 任務，而非每個受影響 symbol 各一個任務。
> [!] `FUTURE_DATE` 和 `DATE_REGRESSION` 必須人工審查，系統不自動刪除或修改資料。

---

## 十三、CLI SOP（13 個 Freshness 指令）

所有 CLI 指令均為**唯讀**，不修改資料、不下載資料、不執行修復。

```bash
# 1. 整體健康狀態
python main.py freshness-health

# 2. 指定 tier 的 freshness summary
python main.py freshness-summary --tier core10
python main.py freshness-summary --tier research30
python main.py freshness-summary --tier expanded50

# 3. 列出 stale symbols
python main.py freshness-stale
python main.py freshness-stale --tier core10

# 4. Source 健康度
python main.py freshness-source-health

# 5. 指定 symbol 的 freshness 詳情
python main.py freshness-symbol --symbol 2330

# 6. 列出所有 open alerts
python main.py freshness-alerts
python main.py freshness-alerts --severity CRITICAL

# 7. 偵測 future date 異常
python main.py freshness-future-date

# 8. 偵測 date regression 異常
python main.py freshness-date-regression

# 9. Coverage repair source required 清單
python main.py coverage-repair-source-required

# 10. 建立 Repair Handoff task list（不執行修復）
python main.py freshness-repair-handoff

# 11. 輸出 Markdown 報告
python main.py freshness-report
python main.py freshness-report --tier research30 --output reports/

# 12. Source interruption 偵測
python main.py freshness-source-interruption

# 13. 完整掃描（all tiers, all datasets）
python main.py freshness-scan-all
```

**指令安全性：**
- 所有指令皆 read-only
- 不連接 broker
- 不下載外部資料
- 不執行 repair
- `freshness-repair-handoff` 僅建立 task list，不執行修復

---

## 十四、GUI SOP

### 開啟 Data Freshness Panel

1. 從主選單 → Research Tools → Data Freshness Monitor
2. 或從 Coverage Repair Panel 的「Freshness Status」連結

### 使用流程

1. **設定 Scope**：選擇 Tier（core10 / research30 / expanded50 / all）、輸入個股代號（可選）、選擇 Mode（real / mock）
2. **執行掃描**：點「Run Scan」→ 背景執行，GUI 不凍結（QThread）
3. **查看 Summary Cards**：Fresh / Delayed / Stale / Missing / Critical / Interrupted 計數
4. **查看 Symbol Freshness Table**：依 Priority 排序，顯示所有 symbol 的詳細狀態
5. **查看 Source Health Table**：來源健康度匯總
6. **查看 Alerts Table**：所有 OPEN alerts
7. **匯出操作（read-only）**：
   - Export Stale List：匯出 STALE / INTERRUPTED symbol 清單
   - Export Source Issues：匯出 INTERRUPTED source 清單
8. **建立 Repair Handoff**：點「Create Repair Handoff」→ 僅建立 task list，**不執行修復**
9. **輸出報告**：點「Build Report」→ 儲存 Markdown 報告至 `reports/`

> [!] GUI 永遠是 read-only。沒有任何按鈕會修改資料或執行交易。

---

## 十五、每日監控 SOP

建議每個交易日下午 4 點後（台灣時間）執行以下流程：

### 標準流程

```bash
# Step 1: 執行整體健康檢查
python main.py freshness-health

# Step 2: 若有問題，查看 core10 詳情
python main.py freshness-summary --tier core10

# Step 3: 列出所有 STALE 和 MISSING
python main.py freshness-stale

# Step 4: 檢查 source 健康度
python main.py freshness-source-health

# Step 5: 若有 CRITICAL alerts，建立 handoff task list
python main.py freshness-repair-handoff

# Step 6: 輸出每日報告
python main.py freshness-report
```

### 異常處理

| 異常 | 優先度 | 建議動作 |
|------|--------|---------|
| FUTURE_DATE | P0 | 立即人工審查，確認資料來源是否有問題 |
| DATE_REGRESSION | P0 | 立即人工審查，確認資料管道是否發生覆寫 |
| SOURCE_INTERRUPTION | P0 | 確認來源 API 狀態，聯絡資料供應商 |
| DATA_MISSING (core tier) | P1 | 確認資料是否已匯入，手動補充 |
| DATA_STALE (core tier) | P1 | 確認來源資料是否可用，手動更新 |
| DATA_DELAYED (research tier) | P2 | 記錄，等待資料自然更新 |

---

## 十六、常見 Warnings 說明

| Warning 訊息 | 說明 | 處理方式 |
|------------|------|---------|
| `Calendar Approximate: True` | 使用週一至週五啟發式，無官方假期清單 | 了解限制，不以此聲明精確 SLA |
| `DEMO_ONLY: mock mode output` | 使用 mock mode 執行，結果不可用於正式結論 | 切換 mode=real 進行正式掃描 |
| `scan_symbol failed` | 個別 symbol 掃描失敗（可能資料缺失或格式錯誤） | 檢查資料路徑與 CSV 格式 |
| `DataFreshnessAdapter.run_scan error` | Engine 啟動或掃描時發生例外 | 檢查 data_freshness 模組是否正常載入 |
| `FreshnessScanWorker error` | GUI 背景掃描執行緒發生例外 | 查看 status label 的錯誤訊息，確認設定 |
| `Source interruption suspected` | 某來源超過 50% symbol STALE，疑似中斷 | 執行 freshness-source-health，確認來源狀態 |
| `future_date_detected` | 資料中存在未來日期 | 立即人工審查，P0 異常 |
| `date_regression_detected` | 最新資料日期倒退 | 立即人工審查，P0 異常 |

---

## 十七、安全聲明

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.

- **No Real Orders**：本系統不下單、不提交、不路由任何買賣指令。
- **No broker execution**：不連接任何 broker API。不進行即時交易。
- **No automatic data download**：外部資料來源不會被自動下載或刷新。資料必須手動匯入。
- **No automatic repair**：過時資料不會被自動覆寫或修復。Repair Handoff 僅建立 task list。
- **Mock data excluded from formal conclusions**：mock mode 的輸出標記為 DEMO_ONLY，不用於任何正式 freshness 結論或信心計算。
- **Not Investment Advice**：本系統所有輸出僅供研究目的。任何內容均不構成財務投資建議。
- **Future date does not count as Fresh**：含未來日期的資料一律為 P0 異常。
- **Date regression requires manual review**：資料日期倒退必須人工確認，系統不自動處理。

```
research_only = True
no_real_orders = True
auto_download_disabled = True
auto_repair_disabled = True
broker_disabled = True
future_date_counts_as_fresh = False
mock_data_formal_freshness_allowed = False
```

---

## v1.1.4 Integration Note

v1.1.4 Coverage Quality Gates will use DataFreshnessEngine for freshness-gated quality checks.
See docs/coverage_quality_gates_v1.1.4.md (planned).
