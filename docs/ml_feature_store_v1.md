# ML Feature Store v1

**Version:** v0.4.2  
**Status:** Stable  
**ML Research Only | Read Only | No Real Orders | Production Trading: BLOCKED**

---

## v0.4.2 目標

建立 ML Feature Store v1，讓現有研究資料可以整理成可訓練機器學習模型的標準資料集。
提供 Feature Snapshot、Label Generation、Train/Validation/Test Split、No Leakage Check、Model-Ready Dataset Export、Feature Quality、Feature Importance Shell。

**不訓練正式交易模型。不做 live prediction。不接實盤下單。**

---

## Feature Store 是什麼

ML Feature Store 是一個 ML 資料準備層，負責：

1. **Feature Catalog** — 管理所有 feature 定義，包含 leakage risk、experimental flag、timeframe
2. **Feature Snapshot** — 從現有資料來源擷取 feature matrix
3. **Label Generation** — 產生 forward return / classification / triple barrier labels（使用未來報酬，但嚴格分離為 label columns）
4. **Train/Validation/Test Split** — 時間序列 split，避免 data leakage
5. **No Leakage Check** — 自動檢查潛在 data leakage
6. **Model-Ready Dataset Export** — 輸出完整 dataset CSV（不 commit）
7. **Feature Quality Check** — missing ratio、constant features、label balance
8. **Feature Importance Shell** — correlation / mutual info 初步重要性分析

---

## Feature Catalog

`ml/feature_catalog.py` — `FeatureCatalog` + `FeatureDefinition`

| Category | Features |
|---|---|
| price | close_return_1/5/20d, volatility_20d, high_low_range_pct |
| technical | ma5/10/20/60_gap, macd, rsi6/12, kd_k/d |
| volume | volume_ratio_5/20d, turnover_value, volume_breakout_flag |
| chip | foreign/trust/dealer/institutional net buy |
| margin | margin_balance/change, short_balance/change |
| revenue | revenue_mom/yoy, cumulative_yoy |
| fundamental | eps, gross_margin, operating_margin, pe_bucket, timing_quality |
| intraday | opening_return_15m, price_vs_vwap_pct, fake_breakout_score, intraday_poc |
| data_quality | freshness/reliability/confidence/mock_contamination scores |
| rule_governance | active/experimental rule count, rule_confidence_score |
| signal_quality | signal boost/reduce/disable count |

每個 feature 標示：
- `leakage_risk` : LOW / MEDIUM / HIGH
- `experimental` : True / False
- `lookback_window` : 最少需要的歷史資料天數

---

## Label Generation

`ml/label_generator.py` — `LabelGenerator`

### Forward Return Labels

```
fwd_return_1d  = close[t+1] / close[t] - 1
fwd_return_5d
fwd_return_10d
fwd_return_20d
```

### Classification Labels

```
label_direction_5d    : 1 if fwd_return_5d > 0, else 0
label_up_5d_3pct      : 1 if fwd_return_5d >= 0.03
label_down_5d_3pct    : 1 if fwd_return_5d <= -0.03
```

### Triple Barrier Labels

```
label_triple_barrier_10d:
    +1 = upper barrier (+5%) hit first within 10 days
    -1 = lower barrier (-3%) hit first within 10 days
     0 = neither

label_max_drawdown_10d
label_max_runup_10d
```

**[!] Label columns 使用未來報酬 — 嚴格前綴 label_ 或 fwd_，永遠不混入 feature columns。**

---

## Train / Validation / Test Split

`ml/split_manager.py` — `MLSplitManager`

預設：`time_series` split（按日期排序，不使用 random split）

```
train      : 60% (最早)
validation : 20%
test       : 20% (最新)
```

其他方法：
- `symbol_grouped` : 每個 symbol 獨立按時間 split
- `walk_forward` : N-fold walk-forward split
- `random` : 有 data leakage warning（不建議用於時間序列）

---

## No Data Leakage Check

`ml/leakage_checker.py` — `DataLeakageChecker`

狀態：
- `CLEAN` — 無 leakage 發現
- `WARNING` — 有輕微風險，需人工確認
- `LEAKAGE_RISK` — 有明確 leakage 風險
- `BLOCKED_FOR_TRAINING` — 有 CRITICAL leakage，不能用於訓練

Findings：
- `FUTURE_COLUMN_IN_FEATURES` — feature column 包含未來資料
- `LABEL_COLUMN_USED_AS_FEATURE` — label column 混入 feature
- `RANDOM_SPLIT_RISK` — 使用 random split
- `TRAIN_DATE_AFTER_TEST_DATE` — split 時間順序錯誤
- `ANNOUNCEMENT_DATE_AFTER_FEATURE_DATE` — 財報公告日 timing risk
- `HIGH_RISK_FEATURE` — HIGH leakage risk feature
- `UNKNOWN_TIMING` — timing_quality = UNKNOWN

**[!] BLOCKED_FOR_TRAINING 時，報告必須說明不能用於訓練。**

---

## Model-Ready Dataset Export

`ml/dataset_builder.py` — `MLFeatureDatasetBuilder`

輸出：
- `data/ml_features/model_ready_dataset_YYYYMMDD_HHMMSS.csv` — 不 commit
- `data/ml_features/model_ready_dataset_summary_YYYYMMDD_HHMMSS.json` — 不 commit

欄位：
- `symbol`, `date`
- feature columns (技術/籌碼/營收/基本面等)
- label columns (fwd_return_* / label_*)
- `split` column (train/validation/test)
- metadata columns (`meta_mode`, `meta_research_only` etc.)

---

## Feature Quality

`ml/feature_quality.py` — `FeatureQualityChecker`

輸出：
- `missing_ratio` per feature
- `constant_feature_count` (zero variance features)
- `high_missing_features` (>50% missing)
- `label_balance` per label column
- `feature_quality_score` (0-100)

---

## Feature Importance Shell

`ml/feature_importance_shell.py` — `FeatureImportanceShell`

方法：
- `correlation_importance()` — Pearson correlation (no sklearn needed)
- `simple_univariate_score()` — mutual info (optional sklearn)

**[!] 第一版不訓練正式模型。Importance scores 僅供探索研究，不構成投資建議。**

---

## CLI 使用方式

```bash
# 列出所有 features
python main.py ml-feature-catalog

# 建立 feature snapshot
python main.py ml-feature-snapshot --mode real

# 產生 labels
python main.py ml-labels --mode real

# 建立 model-ready dataset
python main.py ml-build-dataset --mode real

# 執行 leakage check
python main.py ml-leakage-check --mode real

# Feature quality check
python main.py ml-feature-quality --mode real

# Feature importance
python main.py ml-feature-importance --mode real --target label_direction_5d

# 產生報告
python main.py ml-feature-store-report --mode real
```

---

## GUI 使用方式

1. 啟動：`python main.py cockpit`
2. 點選 **ML Feature Store** tab
3. 點選 **Build Feature Snapshot** — 建立 feature matrix
4. 點選 **Build Model Dataset** — features + labels + split
5. 點選 **Run Leakage Check** — 檢查 data leakage
6. 點選 **Generate Report** — 產生 Markdown 報告
7. 點選 **Open Latest Report** — 開啟最新報告

**GUI 保證：**
- 不下單
- 不做 live prediction
- 不訓練正式交易模型
- 不自動套用模型結果
- 操作在 QThread 執行，不 freeze GUI

---

## 安全原則

1. 不接實盤下單
2. 不接 Shioaji / 兆豐下單
3. 不做 live prediction
4. 不自動交易
5. 不自動改策略權重
6. 不把 model-ready dataset / reports commit 到 git
7. Label columns 永遠前綴 label_ 或 fwd_
8. Features 永遠不使用 label period 未來資料
9. 預設 time_series split，不用 random split
10. 所有報告標示 ML Research Only / No Real Orders / Production Trading BLOCKED

## 安全聲明

> 本系統僅供 ML 量化研究、特徵工程與資料準備，不提供投資建議。
> Production Trading 永遠 BLOCKED。
> REAL_ORDER_READY = False。
> 不做 live prediction。不自動交易。
