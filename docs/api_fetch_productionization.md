# API Fetch Productionization

**Version:** v0.4.1  
**Status:** Stable  
**Research Only | Read Only | No Real Orders | Production Trading: BLOCKED**

---

## v0.4.1 目標

建立 API Fetch Productionization layer，把現有 public API / FinMind / TWSE / TPEx / MOPS 資料抓取流程強化成穩定、可追蹤、可重試、可快取、可檢查 lineage 的 read-only data fetch layer。

**不接實盤下單。不接 Shioaji。不自動交易。**

---

## 元件總覽

| 元件 | 位置 | 功能 |
|------|------|------|
| TokenSetupAssistant | `data/providers/token_setup_assistant.py` | FinMind token 配置助理 |
| RetryPolicy | `data/providers/retry_policy.py` | Retry / timeout / backoff 策略 |
| APICache | `data/providers/api_cache.py` | Provider-level response cache |
| DataLineageTracker | `data/providers/data_lineage.py` | 資料來源 lineage 追蹤 |
| APIFetchDiagnostics | `data/providers/api_diagnostics.py` | 統一 fetch diagnostics |
| TWSETPEXParser | `data/providers/twse_tpex_parser.py` | TWSE/TPEx schema hardening |
| MOPSFinancialParser | `data/providers/mops_financial_parser.py` | MOPS 財報 / 公告日 hardening |
| APIFetchProductionReportBuilder | `reports/api_fetch_production_report.py` | 報告產生器 |
| APIFetchStatusPanel | `gui/api_fetch_status_panel.py` | GUI 面板 |
| APIFetchStatusAdapter | `gui/api_fetch_status_adapter.py` | GUI bridge |

---

## FinMind Token Setup

### 取得 Token

1. 前往 [https://finmindtrade.com/](https://finmindtrade.com/) 註冊帳號
2. 在 Dashboard 取得 API Token
3. 在 `.env` 檔案中加入：
   ```
   FINMIND_TOKEN=your_token_here
   ```
4. **不要 commit `.env` 到 git**
5. **不要把 token 貼入程式碼**

### 驗證

```bash
python main.py api-token-check
```

### .env / .env.example 使用方式

- `.env` — 真實 token，**不得 commit**，已在 `.gitignore` 中排除
- `.env.example` — 只含 placeholder，可以 commit

---

## Retry / Timeout / Backoff

`RetryPolicy` 只用於 read-only GET / safe fetch，**不用於下單**。

| 參數 | 預設 | 說明 |
|------|------|------|
| max_retries | 3 | 最多重試次數 |
| timeout_seconds | 15 | 請求 timeout |
| backoff_seconds | 1.5 | 基本 backoff (指數成長) |
| retry_on_status | 429, 500, 502, 503 | 觸發重試的 HTTP status |

可重試錯誤：TIMEOUT, NETWORK, RATE_LIMIT, SERVER_ERROR  
不重試：SCHEMA_CHANGED, AUTH_ERROR, CLIENT_ERROR

---

## API Cache

`data/providers/api_cache.py` 提供 provider-level response cache。

- Cache 存放在 `data_cache/api/`（已 gitignore）
- Cache key 不含完整 token
- Cache metadata 不含完整 token
- TTL 預設 86400 秒（24 小時）
- 可關閉：`APICache(enabled=False)`

---

## Data Lineage

`DataLineageTracker` 記錄每次 fetch/write 操作：

| 欄位 | 說明 |
|------|------|
| lineage_id | 唯一 ID（LIN-XXXXXXXXXX） |
| dataset | 資料集名稱 |
| provider | 資料來源 |
| source_url_or_endpoint_masked | URL（token 已遮蔽）|
| params_hash | 參數 hash（不含 token）|
| fetched_at / written_at | 時間戳 |
| rows_fetched / rows_written | 筆數 |
| schema_status | OK / PARTIAL / SCHEMA_CHANGED |
| cache_status | HIT / MISS |
| retry_attempts | 重試次數 |

Lineage 輸出在 `data/backtest_results/`，不 commit。

---

## TWSE / TPEx Parser Hardening

`TWSETPEXParser` 功能：

- 欄位名稱變動不 crash（使用 alias mapping）
- 數字含逗號可轉數值（`"1,234,567"` → `1234567.0`）
- 民國年（`112/05/01`）→ 西元年（`2023-05-01`）
- Schema 不符時回 `PARTIAL` / `SCHEMA_CHANGED`
- 不假裝成功

---

## MOPS 財報公告日 / Timing Quality

`MOPSFinancialParser` 功能：

- 若實際公告日抓不到，沿用 estimated deadline，但標示 `announcement_date_is_estimated=True`
- `timing_quality` 輸出：`ACTUAL` / `ESTIMATED` / `DEADLINE` / `UNKNOWN`
- 不 crash

**公告截止日估計（法定）：**  
Q1/Q2/Q3 = 季末 +45 天，Q4 = 年末 +90 天

---

## CLI 使用方式

```bash
# 檢查 token 配置
python main.py api-token-check

# 查看 cache 狀態
python main.py api-cache-status

# 執行 fetch diagnostics
python main.py api-fetch-diagnostics --mode real

# 清除過期 cache
python main.py api-cache-cleanup

# 產生 API Fetch Production Report
python main.py api-fetch-production-report --mode real
```

---

## GUI 使用方式

1. 啟動 GUI：`python main.py cockpit`
2. 點選 **API Fetch Status** tab
3. 點選 **Check Token Setup** — 驗證 FINMIND_TOKEN（只顯示 masked 值）
4. 點選 **Run API Diagnostics** — 查看 provider health 和 cache 狀態
5. 點選 **Generate API Fetch Report** — 產生完整報告
6. 點選 **Clear Expired Cache** — 清除過期 cache 條目
7. 點選 **Open Latest Report** — 開啟最新報告

**GUI 保證：**
- 不顯示完整 token
- 不修改 .env
- 不下單
- 操作在 QThread 執行，不 freeze GUI

---

## 安全原則

1. 不接實盤下單
2. 不接 Shioaji / 兆豐下單
3. 不自動交易
4. 不自動改權重
5. 不修改使用者真實 .env
6. 不顯示完整 token
7. 不把 token、cache、reports、data/import 產物 commit
8. 所有報告標示 Research Only / Read Only / No Real Orders / Production Trading BLOCKED
9. Real mode 不 fallback 到 mock
10. Mock mode 仍可跑

---

## 安全聲明

> 本系統僅供量化研究、策略模擬，不提供投資建議。
> Production Trading 永遠 BLOCKED。
> REAL_ORDER_READY = False。
