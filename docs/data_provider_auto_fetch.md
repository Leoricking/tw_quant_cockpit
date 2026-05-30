# Data Provider Auto Fetch Integration (v0.3.19)

## v0.3.19 目標

讓 Data Provider Layer 真正整合到 `daily_data_update`，自動依 provider 狀態抓取並更新資料。

**只做 read-only data fetch。不下單。不接實盤交易。不自動改權重。**

---

## Auto Fetch 是什麼

`DataProviderAutoFetcher` 是資料自動抓取引擎：

1. 檢查 provider health（FinMind / TWSE / CSV / XQ）
2. 依 provider priority 選擇最佳可用 provider
3. 逐個 dataset 抓取資料
4. 寫入標準 CSV 路徑（merge / dedup）
5. 回報抓取結果與新鮮度

---

## Provider 優先順序

| Dataset | Priority 1 | Priority 2 | Priority 3 | Priority 4 |
|---------|-----------|-----------|-----------|-----------|
| daily_price | FinMind | TWSE/TPEx | CSV existing | XQ existing |
| monthly_revenue | FinMind | TWSE/MOPS | CSV existing | XQ existing |
| institutional | FinMind | TWSE | CSV existing | XQ existing |
| margin | FinMind | TWSE | CSV existing | XQ existing |
| fundamental | FinMind | MOPS | CSV existing | XQ existing |
| intraday | — (PLANNED v0.4+) | | | |

**Real mode 不使用 mock fallback。若所有 provider 失敗，status=FAILED，不假裝成功。**

---

## 支援 Dataset

| Dataset | 標準路徑 | 新鮮度判斷 |
|---------|---------|----------|
| daily_price | `data/import/daily/daily_k.csv` | 3 日內 FRESH |
| monthly_revenue | `data/import/monthly_revenue/monthly_revenue.csv` | 45 日內 FRESH |
| institutional | `data/import/institutional/institutional.csv` | 3 日內 FRESH |
| margin | `data/import/margin/margin.csv` | 3 日內 FRESH |
| fundamental | `data/import/fundamental/fundamental.csv` | 100 日（~1Q）FRESH |
| intraday | `data/import/intraday/` | HISTORICAL_INTRADAY |

---

## CSV 標準路徑

```
data/import/daily/daily_k.csv
data/import/monthly_revenue/monthly_revenue.csv
data/import/institutional/institutional.csv
data/import/margin/margin.csv
data/import/fundamental/fundamental.csv
```

Intraday 不在 auto fetch 範圍，仍由 `import-intraday` 匯入。

---

## Freshness 判斷

| 狀態 | 說明 |
|------|------|
| FRESH | 最新資料在新鮮期內 |
| STALE | 超過新鮮期，但未超過 stale 期 |
| OLD | 超過 stale 期 |
| MISSING | 檔案不存在或為空 |
| PARTIAL | 部分資料有問題（如 timing_estimated） |
| UNKNOWN | 無法判斷 |
| HISTORICAL_INTRADAY | intraday 有資料但非今日 |

---

## Fallback 邏輯

1. 若 FinMind token 未設定 → 嘗試 TWSE/TPEx public API → 若也無資料 → 保留現有 CSV
2. 若 provider API 失敗 → 嘗試下一個 provider
3. 若所有 provider 失敗 → 該 dataset status=FAILED，不中斷整體 run
4. 任何失敗只記錄 warning，不 crash

---

## Dry-Run

```bash
python main.py provider-auto-fetch --mode real --dry-run
```

- Dry-run 模式只抓取，不寫檔
- 可用於確認 provider 狀態和資料量
- 適合在正式 fetch 前先確認

---

## Scheduler daily_data_update 整合方式

`scheduler-run daily_data_update` 執行順序：

1. Provider health check
2. data-source-status
3. **Provider auto fetch（v0.3.19）**
4. **Data freshness check（v0.3.19）**

`latest_status.json` 記錄：
- `provider_health_summary`
- `auto_fetch_summary`
- `freshness_summary`

---

## GUI 使用方式

1. 開啟 `python main.py cockpit`
2. 點選 **Data Provider Fetch** tab
3. 點 **Run Dry Run** 預覽（不寫檔）
4. 點 **Run Auto Fetch** 正式抓取
5. 點 **Check Freshness** 查看新鮮度
6. 點 **Generate Fetch Report** 產生 Markdown 報告

---

## Token-Safe 注意事項

- Token 只從 `.env` 讀取
- Log / Report 中不顯示完整 token（只顯示 `abc****xyz`）
- `.env` 不 commit（在 `.gitignore`）
- 若 token 未設定，只 warning，不 crash

---

## 不下單、不接實盤交易

- `DataProviderAutoFetcher.read_only = True`
- `DataProviderAutoFetcher.no_real_orders = True`
- 執行前會呼叫 `assert_no_real_orders()` 確認所有 provider 均安全
- 任何 provider 若 `real_order_execution=True`，auto fetch 會 raise RuntimeError
