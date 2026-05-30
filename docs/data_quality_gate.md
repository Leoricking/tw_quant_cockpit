# Data Quality Gate & Production Readiness Score (v0.3.20)

## v0.3.20 目標

對現有資料、Provider 健康狀態、Mock 汙染情況進行綜合評分，
產出 Production Readiness Score 與 Backtest Readiness Score，
並決定 8 個 Gate 開關。

**只做 read-only 評分。不下單。不接實盤交易。不自動改權重。**

---

## DataQualityGate 是什麼

`DataQualityGate` 是資料品質評分引擎：

1. 計算 8 個 Sub-Score（0-100）
2. 加權合成 `production_readiness_score`（0-100）
3. 加權合成 `backtest_readiness_score`（0-100，有 cap 規則）
4. 評估 8 個 Gate 開關（RESEARCH_ONLY / BACKTEST_READY / ...）
5. 輸出 9-Section Markdown 報告

---

## Sub-Scores

| Sub-Score | 說明 | 新鮮度判斷依據 |
|-----------|------|---------------|
| freshness_score | 各 dataset 新鮮度加總 | DataFreshnessChecker |
| coverage_score | 標準 CSV 存在且非空 | data/import/ 下各檔案 |
| source_confidence_score | Provider OK 比例 | ProviderHealthChecker |
| timing_quality_score | 關鍵資料時效性 | latest_date vs today |
| sample_size_score | 資料列數 | CSV row count |
| intraday_coverage_score | intraday CSV 是否存在 | data/import/intraday/ |
| provider_health_score | Provider 健康比例 | ProviderHealthChecker |
| mock_contamination_score | Mock 汙染偵測 | MockContaminationChecker |

---

## Score 公式

```
production_readiness_score =
  0.20 * freshness_score
  0.20 * coverage_score
  0.15 * source_confidence_score
  0.15 * timing_quality_score
  0.10 * sample_size_score
  0.10 * intraday_coverage_score
  0.05 * provider_health_score
  0.05 * mock_contamination_score

backtest_readiness_score =
  0.25 * coverage_score
  0.20 * sample_size_score
  0.20 * mock_contamination_score
  0.15 * freshness_score
  0.10 * timing_quality_score
  0.10 * source_confidence_score
```

### Cap 規則

- 若 `mock_contamination_score < 90` → `backtest_readiness` 上限 60
- 若 `coverage_score < 70` → `backtest_readiness` 上限 70

---

## 分類等級

| 分數 | 等級 |
|------|------|
| 90-100 | STRONG |
| 75-89  | READY_FOR_RESEARCH |
| 60-74  | PARTIAL |
| 40-59  | WEAK |
| 0-39   | BLOCKED |

---

## Gate 決策

| Gate | 條件 |
|------|------|
| RESEARCH_ONLY | 永遠 True |
| BACKTEST_READY | production>=70 AND coverage>=70 AND mock_contamination>=90 |
| PAPER_TRADING_READY | production>=80 AND backtest>=75 |
| PRODUCTION_BLOCKED | **永遠 True**（v1） |
| API_READY_READONLY | provider_health>=60 |
| INTRADAY_READY | intraday_coverage>=70 |
| LONG_TERM_READY | long-term coverage>=70 |
| PORTFOLIO_READY | portfolio sim 存在 AND production>=70 |
| REAL_ORDER_READY | **永遠 False**（不允許） |

---

## Mock Contamination 偵測

`MockContaminationChecker` 掃描：

1. CSV 欄位值（source / mode / data_mode 欄）
2. Backtest result CSV 的 mode 欄
3. Report Markdown 檔案文字內容

**預期 Mock 標記**（不算汙染）：
- `mock-realtime`（GUI 模擬模式）
- `paper_trading`（紙上交易）
- `no_real_orders`、`read_only`（安全欄位名稱）
- `mock_contamination`（本模組自身欄位名稱）

---

## CLI 使用方式

```bash
# 執行品質門檻評估
python main.py data-quality-gate --mode real

# 同時產生 Markdown 報告
python main.py data-quality-gate --mode real --report

# 只跑 mock contamination 掃描
python main.py data-quality-gate --check-mock

# 指定自訂路徑
python main.py data-quality-gate --import-root data/import --results-dir data/backtest_results
```

---

## GUI 使用方式

1. 開啟 `python main.py cockpit`
2. 點選 **Data Quality Gate** tab
3. 點 **Run Quality Gate** 執行評分
4. 查看 **Scores** / **Gates** / **Mock Contamination** / **Blockers** tab
5. 點 **Generate Report** 產生 Markdown 報告

---

## Scheduler 整合

`daily_validation` 執行順序新增：

5. **Data Quality Gate（v0.3.20）**

`latest_status.json` 記錄 `quality_gate_summary`：
- `production_readiness_score`
- `backtest_readiness_score`
- `production_classification`
- `gates`

---

## 不下單、不接實盤交易

- `DataQualityGate.read_only = True`
- `DataQualityGate.no_real_orders = True`
- `DataQualityGate.PRODUCTION_BLOCKED = True`（永遠）
- `DataQualityGate.REAL_ORDER_READY = False`（永遠）
