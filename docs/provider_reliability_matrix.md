# Provider Reliability & Fallback Matrix (v0.3.24)

> **[!] Read Only | No Real Orders | Production Trading: BLOCKED**
> Research / Backtesting Only. No live order placement. No broker API write.

---

## 目錄

1. [v0.3.24 目標](#v0324-目標)
2. [Provider Reliability 是什麼](#provider-reliability-是什麼)
3. [Fallback Matrix 是什麼](#fallback-matrix-是什麼)
4. [Dataset Confidence Score 算法](#dataset-confidence-score-算法)
5. [各 Provider 差異比較](#各-provider-差異比較)
6. [No Mock Fallback Policy](#no-mock-fallback-policy)
7. [GUI 使用方式](#gui-使用方式)
8. [CLI 使用方式](#cli-使用方式)
9. [安全聲明：不下單、不接實盤交易](#安全聲明)

---

## v0.3.24 目標

v0.3.24 引入 **Provider Reliability & Fallback Matrix**，核心目標如下：

| 目標 | 說明 |
|---|---|
| 可見性 | 讓研究者能一眼看到各 Provider 的健康狀態、成功率、延遲分數 |
| 可靠性 | 為每個 Dataset 建立明確的 Fallback Chain，確保資料不中斷 |
| 信心分數 | 量化每個 Dataset 的資料品質，提供 0–100 Confidence Score |
| No Mock Fallback | Real mode 下嚴格禁止 Mock Fallback，確保研究資料真實性 |
| 安全不變量 | `read_only=True`, `no_real_orders=True`, `production_blocked=True` 寫入每個模組 |

---

## Provider Reliability 是什麼

**Provider Reliability** 是對每個資料提供者（Provider）的綜合可靠性評估，包含以下指標：

### 指標定義

| 指標 | 說明 | 來源 |
|---|---|---|
| `success_rate` | 成功取得資料的次數比例 (0–1) | logs、fetch reports |
| `failure_rate` | 失敗比例 = 1 - success_rate | 計算 |
| `latency_score` | 資料回應速度分數 (0–1，1=最快) | 估算，本機 CSV/XQ 較高 |
| `row_coverage_score` | 回傳資料列數完整度 (0–1) | 估算 |
| `freshness_score` | 資料時效性分數 (0–1) | DataFreshnessChecker |
| `reliability_score` | 綜合分數 (0–100) | 加權計算 |

### Reliability Score 計算公式

```
reliability_score = (
    success_rate      * 0.40 +
    latency_score     * 0.20 +
    row_coverage      * 0.20 +
    freshness_score   * 0.20
) * 100
```

### Provider 狀態定義

| 狀態 | 說明 |
|---|---|
| `OK` | Provider 正常運作，token 已設定 |
| `PARTIAL` | 部分功能可用（如 token 未設定但可使用公開 API） |
| `NOT_CONFIGURED` | token 未設定，功能受限 |
| `PLANNED` | 尚未實作，v0.4+ 規劃中 |
| `FAILED` | 最近一次呼叫失敗 |
| `UNKNOWN` | 無足夠歷史資料判斷 |

---

## Fallback Matrix 是什麼

**Fallback Matrix** 為每個 Dataset 定義一條 **Provider 優先順序鏈**。

當優先 Provider 失敗或不可用時，系統自動依序嘗試下一個 Provider，最終保底為本機 CSV 或 XQ Export。

### Dataset Fallback Chains

| Dataset | Provider 順序 |
|---|---|
| `daily_price` | finmind → twse → tpex → csv → xq_export |
| `monthly_revenue` | finmind → twse → mops → csv → xq_export |
| `institutional` | finmind → twse → tpex → csv → xq_export |
| `margin` | finmind → twse → tpex → csv → xq_export |
| `fundamental` | finmind → mops → csv → xq_export |
| `intraday` | csv → xq_export → planned_tick_provider |
| `tick` | planned_tick_provider (v0.4+) |
| `bidask` | planned_bidask_provider (v0.4+) |

### Fallback 觸發條件

| 觸發原因 | 代碼 | 說明 |
|---|---|---|
| token_missing | `API_FALLBACK` | API token 未設定，跳到下一個 |
| network_failure | `API_FALLBACK` | 網路連線失敗 |
| provider_unsupported | `PLANNED_NOT_AVAILABLE` | Provider 尚未實作 |
| schema_partial | `API_FALLBACK` | 回傳欄位不完整 |
| stale_data | `API_FALLBACK` | 資料過舊 |
| local_csv_fallback | `LOCAL_FALLBACK` | 使用本機 CSV |
| xq_fallback | `LOCAL_FALLBACK` | 使用 XQ Export |

---

## Dataset Confidence Score 算法

**Dataset Confidence Score** 是對每個 Dataset 資料品質的綜合評估，範圍 0–100。

### 評分公式

```
raw_score = (
    provider_reliability  * 0.30 +
    freshness_score       * 0.25 +
    coverage_score        * 0.20 +
    schema_completeness   * 0.10 +
    source_priority       * 0.10 +
    mock_clean_score      * 0.05
) * 100
```

### 各分項說明

| 分項 | 權重 | 說明 |
|---|---|---|
| `provider_reliability` | 30% | Fallback chain 前 3 個 Provider 的平均 success_rate |
| `freshness_score` | 25% | 資料時效性（FRESH=1.0, STALE=0.6, OLD=0.3, MISSING=0.0） |
| `coverage_score` | 20% | 資料覆蓋率（有資料的股票數 / 預期總數） |
| `schema_completeness` | 10% | 必要欄位完整度（0.85 如有資料列，0.0 如無） |
| `source_priority` | 10% | 主 Provider 品質（finmind=1.0, csv=0.7, xq_export=0.65） |
| `mock_clean_score` | 5% | Mock 資料污染檢查（1.0=乾淨, 0.0=污染） |

### 信心等級

| 分數範圍 | 等級 | 說明 |
|---|---|---|
| 90–100 | HIGH | 資料品質優良，可信賴 |
| 75–89 | GOOD | 資料品質良好 |
| 60–74 | PARTIAL | 部分資料可用，建議補充 |
| 40–59 | WEAK | 資料品質不足，謹慎使用 |
| 0–39 | LOW | 資料嚴重不足或缺失 |

### 特殊上限規則

| 條件 | 最高分 |
|---|---|
| freshness_status == MISSING | 30 |
| freshness_status == OLD | 75 |
| freshness_status == STALE | 80 |
| schema_sc < 0.5 | 60 |
| dataset == fundamental | 80 |
| tick / bidask (planned only) | 30 |
| token 未設定但有本機 fallback | 80 |
| Mock 污染（real mode） | 40 |

---

## 各 Provider 差異比較

### FinMind

| 項目 | 說明 |
|---|---|
| 類型 | 第三方 API（需 token） |
| 支援 Dataset | daily_price, monthly_revenue, institutional, margin, fundamental |
| Token 設定 | `FINMIND_TOKEN` in `.env` |
| 免費限制 | 有 rate limit，付費方案可提升 |
| 狀態 | 主要 Provider，優先使用 |
| 備註 | Token 未設定時 success_rate 受限，系統自動 fallback 到 TWSE/CSV |

### TWSE (台灣證交所)

| 項目 | 說明 |
|---|---|
| 類型 | 公開 API（無需 token） |
| 支援 Dataset | daily_price, monthly_revenue, institutional, margin |
| Token 設定 | 不需要 |
| 狀態 | v0.3.x PLANNED（尚未完整實作），列為 Fallback 2 |
| 備註 | 規劃在 v0.4 完整接入 TWSE OpenAPI |

### TPEx (櫃買中心)

| 項目 | 說明 |
|---|---|
| 類型 | 公開 API（無需 token） |
| 支援 Dataset | daily_price, institutional, margin |
| Token 設定 | 不需要 |
| 狀態 | v0.3.x PLANNED |
| 備註 | 規劃 v0.4 完整接入 |

### MOPS (公開資訊觀測站)

| 項目 | 說明 |
|---|---|
| 類型 | 爬蟲 / 公開資料 |
| 支援 Dataset | monthly_revenue, fundamental |
| Token 設定 | 不需要 |
| 狀態 | v0.3.x PLANNED |
| 備註 | 爬蟲有頻率限制，規劃 v0.4 實作 |

### CSV (本機 CSV Import)

| 項目 | 說明 |
|---|---|
| 類型 | 本機檔案 |
| 支援 Dataset | daily_price, monthly_revenue, institutional, margin, fundamental, intraday |
| Token 設定 | 不需要 |
| 狀態 | 可用，作為 Local Fallback |
| 備註 | 放置於 `data/import/daily/daily_k.csv` 等路徑；無網路時最可靠 |

### XQ Export (XQ 全球贏家匯出)

| 項目 | 說明 |
|---|---|
| 類型 | 本機 XQ 匯出檔案 |
| 支援 Dataset | daily_price, intraday |
| Token 設定 | 不需要（需安裝 XQ 並手動匯出） |
| 狀態 | 可用，作為 Local Fallback |
| 備註 | 適合有 XQ 訂閱的用戶；分鐘線 / 日線均可 |

---

## No Mock Fallback Policy

**核心原則：Real mode 下嚴格禁止 Mock Fallback。**

### 規則

- **Real mode (`mode="real"`)**: 所有 Provider 失敗時，只能 fallback 到真實資料來源（CSV/XQ Export）。絕不使用 Mock 資料。
- **Mock mode (`mode="mock"`)**: 僅用於 Demo / 測試 / CI，不得用於真實研究或回測。
- `mock_fallback_count` 在 real mode 報告中永遠為 **0**。
- Mock 資料污染偵測：如偵測到 real mode 中有 Mock 資料，Confidence Score 上限為 40。

### 為什麼重要

使用 Mock 資料進行回測或研究，會導致：

1. 回測結果過度樂觀（資料完美、無缺漏）
2. 策略在真實資料上表現大幅低於回測
3. 研究結論失效

---

## GUI 使用方式

### 開啟 Provider Reliability Panel

在主 Dashboard 中，點選側邊欄的 **「Provider Reliability」** 標籤頁。

### 面板說明

```
[Safety Banner]  Provider Reliability | Research Only | Read Only | No Real Orders | Production: BLOCKED | Mock Fallback: DISABLED

[Summary Cards]
  Overall Reliability | High Confidence | Weak Datasets | Failed Providers | Local Fallback Used | Mock Fallback Count

[C. Provider Reliability Table]
  Provider | Status | Success Rate | Latency | Row Coverage | Freshness | Reliability Score | Recommended Usage

[D. Dataset Fallback Matrix Table]
  Dataset | Primary | Fallback 1 | Fallback 2 | Local Fallback | Last Used | Confidence | Recommendation

[E. Dataset Confidence Table]
  Dataset | Score | Level | Freshness | Coverage | Missing Symbols | Warning

[F. Actions]
  [Refresh Reliability]  [Generate Report]  [Open Latest Report]  [Check Provider Health]  [Run Auto Fetch Dry Run]
```

### 操作步驟

1. 點選 **Refresh Reliability** 執行完整可靠性矩陣分析
2. 查看 Provider Reliability Table，確認各 Provider 狀態
3. 查看 Dataset Confidence Table，確認資料集信心等級
4. 如有 WEAK / LOW 資料集，查看 Recommendation 欄位
5. 點選 **Generate Report** 產生 Markdown 報告
6. 點選 **Open Latest Report** 用記事本開啟報告
7. 點選 **Check Provider Health** 快速確認 Provider 健康狀態

### 顏色說明

| 顏色 | 意義 |
|---|---|
| 綠色 (#33CC66) | OK / HIGH / GOOD |
| 橘色 (#FFAA00) | PARTIAL / 警告 |
| 紅色 (#FF4444) | FAILED / ERROR / LOW / WEAK |

---

## CLI 使用方式

### 執行可靠性矩陣分析

```bash
# 執行完整可靠性矩陣（real mode）
python main.py provider-reliability-matrix

# 指定 mode
python main.py provider-reliability-matrix --mode real
python main.py provider-reliability-matrix --mode mock

# 產生報告
python main.py provider-reliability-matrix --report

# 查看特定 Dataset 的 fallback chain
python main.py provider-reliability-matrix --dataset daily_price
```

### 相關指令

```bash
# Provider 健康檢查
python main.py provider-health-check

# 自動補抓資料（dry-run 模式，不實際寫入）
python main.py provider-auto-fetch --dry-run

# 自動補抓特定 Dataset
python main.py provider-auto-fetch --dataset daily_price

# 查看資料新鮮度
python main.py data-freshness-check
```

### Python API 使用

```python
from data.providers.reliability_matrix import ProviderReliabilityMatrix

# 執行可靠性矩陣
matrix = ProviderReliabilityMatrix(mode="real")
result = matrix.run()

# 查看 Provider 總覽
for p in result["provider_summary"]:
    print(p["provider_name"], p["status"], p["reliability_score"])

# 查看 Dataset Confidence
for ds, conf in result["dataset_confidence_scores"].items():
    print(ds, conf["score"], conf["level"])

# 查詢特定 Dataset 的最佳 Provider
best = matrix.determine_best_provider_for_dataset("daily_price")
print("Best provider:", best)

# 查詢 fallback chain
chain = matrix.determine_fallback_chain("monthly_revenue")
print("Fallback chain:", chain)
```

```python
# 產生報告（GUI adapter）
from gui.provider_reliability_adapter import ProviderReliabilityAdapter

adapter = ProviderReliabilityAdapter()
report_path = adapter.generate_report(mode="real")
print("Report written to:", report_path)

# 載入最新摘要
summary = adapter.load_latest_summary()
print("Overall reliability:", summary.get("overall_reliability_score"))
```

---

## 安全聲明

### 不下單、不接實盤交易

本模組及相關所有程式碼嚴格遵守以下安全不變量：

| 不變量 | 值 | 說明 |
|---|---|---|
| `read_only` | `True` | 不寫入 Broker API；不修改任何帳戶設定 |
| `no_real_orders` | `True` | 不下任何實際委託單 |
| `production_blocked` | `True` | 生產交易永久封鎖，直至 `REAL_ORDER_READY=True` 由人工確認 |
| `mock_fallback_disabled` | `True` | Real mode 不使用 Mock 資料 |
| Token 安全 | 無 | 不在程式碼中寫入任何 API Token；不在 log 中輸出完整 Token |

### 使用場景限制

| 允許 | 不允許 |
|---|---|
| 歷史資料回測 | 實盤下單 |
| 資料品質研究 | 修改 Broker 帳戶設定 |
| Provider 健康監控 | 接收即時 tick 並自動交易 |
| 產生分析報告 | 將報告視為投資建議 |

### 關於 Token

- FinMind Token（`FINMIND_TOKEN`）設定於 `.env` 檔案，**不寫入程式碼**
- Log 輸出中只顯示 Token 是否存在（`token_configured: True/False`），**不輸出 Token 值**
- 其他 Provider 目前不需要 Token

---

## 版本資訊

| 版本 | 異動 |
|---|---|
| v0.3.24 | 新增 Provider Reliability Matrix、Dataset Confidence Score、Fallback Matrix、GUI Panel、Report Builder |
| v0.3.23 | Provider Auto Fetch、Data Freshness Checker |
| v0.3.22 | Usability QA、Error Message Polish |

---

*Provider Reliability & Fallback Matrix — TW Quant Cockpit v0.3.24*
*Research Only. No Real Orders. Production Trading: BLOCKED.*
