# Strategy Knowledge Ingestion — v0.4.1.1

> [!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] auto_activated=False. Transcript-only confidence ≤ PARTIAL.
> [!] Not investment advice. Long-cycle risk is NOT a short-term trading signal.

---

## 目標

v0.4.1.1 的目標是建立 **Strategy Knowledge Ingestion from Transcripts** 系統：

把使用者匯入的投資影片逐字稿、直播筆記、YouTube transcript、手動文字筆記，
轉成系統可讀的結構化策略知識（`rule_candidates`、`factor_candidates`、`entry_conditions`、`avoid_conditions`、`risk_conditions`），
以供後續 Rule Governance、ML Feature Store、Model Monitoring 參考。

---

## 為什麼要在 ML Feature Store 之前做 Transcript Ingestion

1. ML Feature Store (v0.4.2) 需要知道哪些 factor 有策略依據。
2. Rule Governance (v0.3.28) 的 candidate rules 需要一個明確的來源追蹤。
3. 先把「知識」結構化，才能做有意義的 feature engineering。
4. 避免 ML 模型學到沒有基本面依據的 noise factor。

---

## 支援的逐字稿格式

系統支援以下格式（`.txt` / `.md`）：

```
[title]          影片標題或筆記標題
[video_id]       YouTube video ID 或 N/A
[media_source]   youtube / manual_note / article / imported_text
[media_ref]      URL 或 N/A
[Transcript]     逐字稿內文（多行）
[Summary]        摘要（多行，可選）
```

如果沒有這些 section header，系統會把整個檔案當成 `Transcript` 處理。

---

## 阪田戰法萃取範例

輸入（逐字稿片段）：

```
財報底部翻多，提前卡位提前佈局，EPS 優於去年同期，
第一季乘以四估全年，股價尚在低位階，技術面剛翻多。
```

萃取輸出：

| category | statement | suggested_rule_id |
|----------|-----------|-------------------|
| entry_condition | 財報底部翻多 | BUY.SHORT.SECOND_WAVE.V1 |
| factor_candidate | EPS 優於去年同期 | LONG.FUNDAMENTAL.EPS_POSITIVE.V1 |
| entry_condition | 提前卡位提前佈局 | BUY.SHORT.SECOND_WAVE.V1 |
| factor_candidate | 第一季乘以四估全年 EPS | LONG.FUNDAMENTAL.EPS_POSITIVE.V1 |

---

## 獅公長週期風險萃取範例

輸入（逐字稿片段）：

```
2028 到 2031 可能發生 50% 股災，這是長週期風險，不要恐慌，
不是現在立刻賣出的訊號。
```

萃取輸出：

| category | statement | suggested_rule_id | confidence |
|----------|-----------|-------------------|------------|
| long_cycle_risk | 2028～2031 長週期股災 watch | RISK.CYCLE.CRASH_WATCH.V1 | PLANNED |
| risk_condition | 50% crash definition | RISK.CYCLE.CRASH_WATCH.V1 | PLANNED |

> **重要**：長週期 crash watch 的 confidence 永遠為 `PLANNED`，不可為 `HIGH`。
> 不是短線賣出訊號，不是投資建議。

---

## rule_candidates / factor_candidates / avoid_conditions 差異

| 類型 | 說明 | 輸出檔案 |
|------|------|---------|
| rule_candidate | 可對應到 Rule Governance rule_id 的規則候選 | rule_candidates.csv |
| factor_candidate | 可對應到 ML Feature 的 factor 候選（EPS、revenue 等） | factor_candidates.csv |
| avoid_condition | 明確避開的條件（M頭、頭肩頂、財報衰退等） | avoid_conditions.csv |
| risk_condition | 風險監控條件（外資期貨空單、長週期 crash） | risk_conditions.csv |
| entry_condition | 進場條件 | knowledge_items.csv（category=entry_condition） |
| exit_condition | 出場條件 | knowledge_items.csv（category=exit_condition） |

---

## Rule Governance 整合方式

1. 從逐字稿萃取的 rule candidate 會寫入 `rule_candidates.csv`，
   欄位包含 `suggested_rule_id`、`existing_rule_match`、`governance_status`。
2. `auto_activated` 永遠為 `False`，不自動加入正式 ACTIVE rule。
3. 如 `suggested_rule_id` 在 Rule Registry 中已存在，`existing_rule_match = True`。
4. 如不存在，`governance_status = CANDIDATE`，需人工審查後才能升級為 ACTIVE。
5. Confidence 來自 transcript 的 rule candidates 最高只能到 `PARTIAL`，
   長週期 crash watch 規則固定為 `PLANNED`。

---

## CLI 使用方式

```bash
# 測試執行（不寫出 CSV）
python main.py strategy-knowledge-ingest --mode real --dry-run

# 正式執行（寫出 CSV）
python main.py strategy-knowledge-ingest --mode real

# 指定輸入目錄
python main.py strategy-knowledge-ingest --mode real --input-dir "data/import/transcripts"

# 執行後產生報告
python main.py strategy-knowledge-ingest --mode real --report

# 查看最新 summary
python main.py strategy-knowledge-summary
```

---

## GUI 使用方式

1. 開啟 Cockpit：`python main.py cockpit`
2. 點選 **Strategy Knowledge** tab
3. 確認 input 資料夾路徑（預設：`knowledge/transcripts`）
4. 點選 **Run Dry Run** 先確認發現哪些檔案
5. 確認無誤後點選 **Run Ingestion** 執行正式 ingestion
6. 點選 **Generate Report** 產生 Markdown 報告

---

## 輸出目錄

| 檔案 | 說明 |
|------|------|
| `data/backtest_results/strategy_knowledge/sources.csv` | Transcript source 清單 |
| `data/backtest_results/strategy_knowledge/knowledge_items.csv` | 所有萃取出的知識項目 |
| `data/backtest_results/strategy_knowledge/rule_candidates.csv` | 規則候選（不自動啟用） |
| `data/backtest_results/strategy_knowledge/factor_candidates.csv` | Feature 候選 |
| `data/backtest_results/strategy_knowledge/avoid_conditions.csv` | 避開條件 |
| `data/backtest_results/strategy_knowledge/risk_conditions.csv` | 風險條件 |
| `reports/strategy_knowledge_ingestion_report_YYYY-MM-DD.md` | Markdown 報告 |

> 所有輸出均不 commit（已加入 `.gitignore`）。

---

## 安全聲明

| 項目 | 狀態 |
|------|------|
| Knowledge Only | True |
| Research Only | True |
| No Real Orders | True |
| Production Trading | BLOCKED |
| auto_activated | False |
| Transcript confidence cap | PARTIAL |
| Long-cycle crash watch | PLANNED only |
| 是否投資建議 | 否 |

---

*TW Quant Cockpit v0.4.1.1 — Strategy Knowledge Ingestion — Research Only — Not Investment Advice*
