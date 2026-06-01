# Model Monitoring

**Version:** v0.4.3 | **Status:** Stable | **Type:** ML Research Only | **Mode:** Read Only | **No Real Orders** | **Production Trading: BLOCKED**

> [!] 本模組為研究監控工具，不做 live prediction、不下真實訂單、不連結 broker。
> [!] All outputs labeled: Monitoring Only / No Real Orders / Production Trading BLOCKED.

---

## v0.4.3 目標

v0.4.3 新增完整的 Model Monitoring 子系統，讓研究者能夠：

- 追蹤已訓練模型的元數據（ModelRegistry）
- 記錄每次預測/信號輸出（PredictionLog）
- 追蹤命中/未命中率（HitMissReviewer）
- 偵測特徵與標籤分佈的漂移（DriftDetector）
- 監控信號品質退化（SignalDegradationMonitor）
- 比較規則信號與 ML 預測的一致性（RuleVsMLComparator）
- 彙整所有監控結果（ModelMonitoringSummary）
- 產生完整報告（ModelMonitoringReportBuilder）
- 透過 GUI 面板整合操作（ModelMonitoringPanel）

---

## Model Monitoring 是什麼

Model Monitoring 由以下 8 個核心元件組成：

1. **ModelRegistry** — 記錄每個研究模型的元數據、特徵快照 ID、資料路徑、訓練區間、洩漏狀態
2. **PredictionLog** — 以 JSONL 格式記錄每次預測或信號輸出；支援按 model/symbol/date 過濾
3. **HitMissReviewer** — 計算命中率、精確率、召回率；按 symbol/rule/model/source 分組
4. **DriftDetector** — 比較 baseline 與當前特徵分佈、缺失率、標籤分佈、預測分數
5. **SignalDegradationMonitor** — 讀取 backtest/rule/portfolio 資料，偵測性能退化趨勢
6. **RuleVsMLComparator** — 比較規則信號與 ML 預測的一致性；ML 不可用時返回 ML_NOT_AVAILABLE
7. **ModelMonitoringSummary** — 彙整所有子模組結果，產生統一摘要與 next_actions
8. **ModelMonitoringReportBuilder** — 產生 Markdown 報告（8 個章節，含安全聲明）

---

## Prediction Tracking

`PredictionLog` 以每日 JSONL 檔案格式記錄預測：

```
model_monitoring/predictions/predictions_YYYYMMDD.jsonl
```

每筆記錄包含：
- 預測 ID、model_id、signal_id、rule_id、symbol、date
- prediction_type：`classification` / `regression` / `rule_signal` / `signal_quality` / `portfolio_candidate`
- source：`ml_prediction` / `rule_signal` / `signal_quality` / `portfolio_candidate` / `backtest_signal`
- predicted_label、predicted_score、predicted_return、confidence、horizon
- feature_snapshot_id、experiment_id（資料溯源）
- actual_return、actual_label、hit、reviewed（事後更新）

**填寫 actuals：**

```python
from monitoring.prediction_log import PredictionLog

pl = PredictionLog()
pl.update_actuals({
    "2330": {"2026-05-20": 0.023, "2026-05-21": -0.008},
    "2317": {"2026-05-20": 0.011},
})
```

---

## Hit / Miss Review

`HitMissReviewer` 對已有 actuals 的記錄進行分析：

```python
from monitoring.hit_miss_review import HitMissReviewer

result = HitMissReviewer().run(horizon=5)
print(result["hit_rate"])     # e.g. 0.62
print(result["by_symbol"])    # hit rate breakdown per symbol
print(result["by_rule"])      # hit rate breakdown per rule
print(result["status"])       # CLEAN / PARTIAL / INSUFFICIENT_DATA
```

**Status 說明：**

| Status | 說明 |
|---|---|
| CLEAN | 有足夠資料，分析完整 |
| PARTIAL | 資料不足 10 筆，結果僅供參考 |
| INSUFFICIENT_DATA | 無已審查記錄 |

---

## Drift Detection

`DriftDetector` 比較 baseline 與 current 資料集之間的特徵分佈變化：

```python
from monitoring.drift_detector import DriftDetector
import pandas as pd

baseline_df = pd.read_csv("data/ml_features/snapshot_20260101.csv")
current_df  = pd.read_csv("data/ml_features/snapshot_20260501.csv")

result = DriftDetector().run(baseline_df=baseline_df, current_df=current_df)
print(result["status"])          # STABLE / WATCH / DRIFT_WARNING / DRIFT_CRITICAL
print(result["feature_drift"])   # per-feature mean/std changes
print(result["label_drift"])     # label distribution shift
```

**Drift 狀態閾值：**

| Status | 閾值 | 說明 |
|---|---|---|
| STABLE | 所有變化 < 10% | 無顯著漂移 |
| WATCH | 任何變化 ≥ 10% | 輕微漂移，持續觀察 |
| DRIFT_WARNING | 任何變化 ≥ 25% | 需要注意，考慮重新訓練 |
| DRIFT_CRITICAL | 任何變化 ≥ 50% | 嚴重漂移，建議重新訓練 |
| INSUFFICIENT_DATA | 資料為空或 None | 無法分析 |

---

## Signal Degradation Warning

`SignalDegradationMonitor` 讀取可用的 backtest/signal/rule 資料：

```python
from monitoring.signal_degradation import SignalDegradationMonitor

result = SignalDegradationMonitor().run()
print(result["status"])                    # STABLE / WATCH / DEGRADED / SEVERE
print(result["rule_degradation"])          # 規則信心度退化
print(result["signal_quality_degradation"])# 信號品質退化
print(result["portfolio_degradation"])     # 組合績效退化
```

**Degradation 狀態：**

| Status | 說明 |
|---|---|
| STABLE | 無退化跡象 |
| WATCH | 輕微退化，觀察中 |
| DEGRADED | 顯著退化，建議審查 |
| SEVERE | 嚴重退化，需立即處理 |
| INSUFFICIENT_DATA | 無可用資料 |

---

## Rule vs ML Comparison

`RuleVsMLComparator` 比較規則信號與 ML 預測：

```python
from monitoring.rule_vs_ml_comparator import RuleVsMLComparator

result = RuleVsMLComparator().compare(
    rule_signals   = rule_signal_list,    # list of dicts
    ml_predictions = ml_prediction_list,  # list of dicts (can be None)
    actuals        = actuals_dict,
)

print(result["agreement_rate"])    # float 0-1 or None
print(result["recommendation"])    # ML_NOT_AVAILABLE / AGREEMENT_HIGH / AGREEMENT_LOW_REVIEW
print(result["ml_available"])      # bool
```

**Recommendation 說明：**

| Recommendation | 說明 |
|---|---|
| ML_NOT_AVAILABLE | 無 ML 預測可供比較 |
| AGREEMENT_HIGH | 一致率 ≥ 70%，兩者高度一致 |
| AGREEMENT_MODERATE_REVIEW | 一致率 40%-70%，建議審查差異 |
| AGREEMENT_LOW_REVIEW | 一致率 < 40%，顯著差異需要審查 |
| INSUFFICIENT_DATA | 資料不足 |

---

## 為什麼不做 live prediction

本平台為**研究工具**，設計原則如下：

1. **研究優先**：目標是找到統計有效的模式，而非即時預測
2. **避免過度擬合**：live prediction 容易導致在真實資料上的偏差
3. **安全隔離**：研究環境與交易環境完全隔離，防止誤操作
4. **資料洩漏防護**：live prediction 會引入前瞻偏差風險
5. **合規考量**：未經驗證的模型不應直接驅動真實交易決策

所有 `read_only = True`、`no_real_orders = True`、`production_blocked = True` 的設計均為強制性安全措施。

---

## CLI 使用方式

### 基本監控操作

```bash
# 1. 查看監控摘要
python -c "
from monitoring.monitoring_summary import ModelMonitoringSummary
import json
result = ModelMonitoringSummary().run()
print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
"

# 2. 列出所有已登錄模型
python -c "
from monitoring.model_registry import ModelRegistry
reg = ModelRegistry()
for m in reg.list_models():
    print(m['model_id'], m['model_type'], m['monitoring_status'])
"

# 3. 登錄新模型元數據
python -c "
from monitoring.model_registry import ModelRegistry, ModelMetadata
from datetime import date
meta = ModelMetadata(
    model_id='rf_5d_v1',
    model_name='RandomForest 5-day Return',
    model_type='RandomForestClassifier',
    version='v1.0',
    created_at=date.today().isoformat(),
    feature_snapshot_id='snap_20260101',
    dataset_path='data/ml_features/dataset_20260101.csv',
    target_label='return_5d_up',
    train_start='2020-01-01',
    train_end='2025-06-30',
    validation_start='2025-07-01',
    validation_end='2026-01-01',
    feature_count=42,
    row_count=15000,
    leakage_status='CLEAN',
)
ModelRegistry().register_model(meta)
print('Model registered.')
"

# 4. 記錄預測
python -c "
from monitoring.prediction_log import PredictionLog, PredictionRecord
import uuid
from datetime import datetime
rec = PredictionRecord(
    prediction_id=str(uuid.uuid4())[:8],
    model_id='rf_5d_v1',
    signal_id='sig_001',
    rule_id='rule_momentum',
    symbol='2330',
    date='2026-06-01',
    prediction_time=datetime.now().isoformat(),
    prediction_type='classification',
    predicted_label='BUY',
    predicted_score=0.72,
    predicted_return=0.025,
    confidence=0.68,
    horizon=5,
    source='ml_prediction',
    feature_snapshot_id='snap_20260101',
    experiment_id='exp_001',
)
PredictionLog().append(rec)
print('Prediction logged.')
"

# 5. 更新 actuals
python -c "
from monitoring.prediction_log import PredictionLog
pl = PredictionLog()
result = pl.update_actuals({
    '2330': {'2026-06-01': 0.023},
    '2317': {'2026-06-01': -0.005},
})
print(result)
"

# 6. Hit/Miss 分析
python -c "
from monitoring.hit_miss_review import HitMissReviewer
import json
result = HitMissReviewer().run(horizon=5)
print(f'Hit Rate: {result[\"hit_rate\"]}')
print(f'Status: {result[\"status\"]}')
print(json.dumps(result['by_symbol'], indent=2, default=str))
"

# 7. 漂移偵測
python -c "
from monitoring.drift_detector import DriftDetector
result = DriftDetector().run()
print(f'Drift Status: {result[\"status\"]}')
"

# 8. 信號退化監控
python -c "
from monitoring.signal_degradation import SignalDegradationMonitor
result = SignalDegradationMonitor().run()
print(f'Degradation Status: {result[\"status\"]}')
print(f'Rule Degradation: {result[\"rule_degradation\"][\"status\"]}')
"

# 9. 產生報告
python -c "
from gui.model_monitoring_adapter import ModelMonitoringAdapter
result = ModelMonitoringAdapter().generate_report(mode='real')
print(f'Report saved: {result[\"report_path\"]}')
"
```

---

## GUI 使用方式

在 TW Quant Cockpit 主視窗中，點選 **Model Monitoring** 頁籤即可開啟 `ModelMonitoringPanel`。

**主要功能區塊：**

- **Summary Cards** — 即時顯示 Model Count、Prediction Count、Reviewed Count、Hit Rate、Drift Status、Degradation Status
- **Model Registry Table** — 所有已登錄模型的列表（Model ID、Name、Type、Target、Feature Snapshot、Leakage Status、Monitoring Status）
- **Prediction Log Table** — 最近的預測記錄（Prediction ID、Symbol、Date、Source、Horizon、Predicted、Actual、Hit、Reviewed）
- **Drift Table** — 特徵/標籤漂移結果（Feature/Label、Baseline、Current、Drift Score、Status、Warning）
- **Degradation Table** — 信號退化結果（Signal/Rule、Baseline、Recent、Change、Status、Next Step）
- **Rule vs ML Table** — 規則與 ML 比較（Symbol、Rule Signal、ML Signal、Actual、Agreement、Result）

**動作按鈕：**

| 按鈕 | 功能 |
|---|---|
| Refresh Monitoring | 重新執行所有監控模組，更新摘要卡片 |
| Register Model Metadata | 開啟對話框登錄新模型元數據 |
| Update Actuals | 提示使用者透過 CLI 更新 actuals |
| Run Drift Check | 執行漂移偵測，更新 Drift Table |
| Generate Report | 產生完整 Markdown 報告到 reports/ |
| Open Latest Report | 開啟最新的監控報告檔案 |

---

## 安全原則

1. **read_only = True** — 所有類別屬性設定，不寫入交易系統
2. **no_real_orders = True** — 所有類別屬性設定，禁止真實訂單
3. **production_blocked = True** — 正式交易環境完全封鎖
4. **real_order_ready = False** — 明確標示未達到真實交易標準
5. **monitoring_only = True** — 僅為監控目的，不做預測推斷
6. **Runtime 輸出隔離** — 所有運行時輸出存放在 `model_monitoring/`（不納入版本控制）
7. **sklearn 選用** — 若 sklearn 未安裝，所有功能優雅降級
8. **pandas 選用** — 若 pandas 未安裝，使用純 Python 替代
9. **No crash on missing data** — 所有模組在資料缺失時返回 INSUFFICIENT_DATA 而非崩潰
10. **try/except 隔離** — ModelMonitoringSummary 對每個子模組使用獨立的 try/except

---

## 安全聲明

```
[!] Monitoring Only / No Real Orders / Production Trading BLOCKED
[!] No live prediction. No auto-trading. No broker connections.
[!] All outputs are research-only monitoring data.

read_only            = True
no_real_orders       = True
production_blocked   = True
real_order_ready     = False
monitoring_only      = True
research_only        = True
live_prediction      = False
auto_trading         = False
```

> 本文件涵蓋 TW Quant Cockpit v0.4.3 Model Monitoring 子系統。
> 所有功能僅供量化研究使用。未經充分驗證，不應用於真實交易決策。
