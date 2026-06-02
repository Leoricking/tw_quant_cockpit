# Research Assistant / Coach — v0.4.8

## v0.4.8 目標

建立 Research Assistant / Coach，根據 Research Review Dashboard、Portfolio Journal、
Notification Center、Rule Governance、Model Monitoring、Intraday Replay、Data Quality Gate
的結果，自動產生每日 / 每週研究教練建議。

---

## Research Assistant / Coach 是什麼

Research Assistant / Coach 是一個純研究輔助系統，功能如下：

- 讀取所有子系統的輸出（Research Review Dashboard, Journal, Rule Governance 等）
- 自動產生每日 / 每週研究檢查清單
- 產生 Replay 訓練菜單（根據 Journal 常犯錯誤自動匹配情境）
- 產生 Rule Review Queue（低信心 / 樣本不足 / transcript 候選）
- 產生資料修復優先順序（Data Quality Gate + Provider Reliability）
- 產生 Journal / Process Coaching 提醒
- 產生 Model / ML Coaching 提醒

**不會做的事：**
- 不接實盤下單
- 不自動買賣
- 不自動改 Rule 權重
- 不自動啟用 ML feature
- 不顯示 token / 密碼
- 不連接 broker

---

## 與 Research Review Dashboard 的關係

| 系統 | 功能 |
|------|------|
| Research Review Dashboard (v0.4.7) | 彙整所有子系統輸出，產生 ReviewItem, Scorecard, Action Plan |
| Research Assistant / Coach (v0.4.8) | 讀取 Research Review 輸出，產生研究教練建議 |

Research Assistant 是 Research Review 的下游消費者，
讀取其 persisted CSV 輸出進行分析。

---

## Daily Checklist

每日研究前必須執行的檢查清單：

1. Check Data Quality Gate — `python main.py data-quality-gate --mode real`
2. Check Provider Reliability — `python main.py provider-reliability --mode real`
3. Check Notification Center — `python main.py notification-list`
4. Check Research Review Dashboard — `python main.py research-review-summary`
5. Check Journal Review Queue — `python main.py journal-summary`
6. Check Rule Governance Needs Review — `python main.py rule-governance --mode real`
7. Check Replay Training Focus — `python main.py intraday-replay --mode real`
8. Check ML Knowledge Leakage — `python main.py ml-knowledge-feature-summary`
9. Read Auto Report Daily Summary — `python main.py auto-report --mode real --profile daily`

---

## Weekly Checklist

每週應執行的回顧清單：

1. Review top mistakes this week
2. Review weak rules this week
3. Review replay training progress
4. Review model monitoring warnings
5. Review portfolio journal outcomes
6. Review data blockers
7. Update research notes

---

## Replay Training Plan

根據 Journal 常犯錯誤自動匹配訓練情境：

| 常犯錯誤 | 建議情境 |
|----------|----------|
| chase_high | fake_breakout, chase_high_correction |
| fake_breakout | fake_breakout scenario |
| vwap_loss | vwap_loss, vwap_reclaim |
| no_plan | opening_range_break, stop_loss_discipline |
| weak_stock | weak_stock_filter |

訓練情境列表：
- fake_breakout
- vwap_loss
- vwap_reclaim
- opening_range_break
- opening_range_fail
- volume_profile_poc
- chase_high_correction
- stop_loss_discipline
- weak_stock_filter

---

## Rule Review Queue

以下條件的 Rule 會進入 Review Queue：
- Low confidence
- Insufficient sample count
- Repeated false signal
- High mistake linkage
- Signal disabled / reduce candidate
- Transcript-derived candidate needs backtest
- ML knowledge feature needs mapping

**注意：** Coach 不自動 enable / disable rule，也不自動改權重。

---

## Data Repair Priority

以下情況會產生資料修復建議：
- 資料過時 (stale)
- 資料缺失 (missing dataset)
- Provider 失敗 (provider failed)
- API token 未設定（不顯示 token 內容）
- 日內資料缺失 (intraday missing)
- Lineage 缺失

**注意：** Coach 不修改 .env，不顯示 token 值，不自動抓取實盤資料。

---

## Journal / Process Coaching

- 回顧常犯錯誤
- 清除 review backlog
- 提示本週 process focus
- 識別 good process bad outcome / bad process good outcome patterns

---

## Model / ML Coaching

- 偵測 drift warnings
- 偵測 signal degradation
- 偵測 ML knowledge leakage
- 識別 metadata-only features
- 標記 needs_mapping / needs_backtest features

---

## CLI 使用方式

```bash
# 執行每日 coach
python main.py research-coach --mode real --period daily

# 執行每週 coach
python main.py research-coach --mode real --period weekly

# 產生 coach report
python main.py research-coach-report --mode real --period daily

# 查看 coach summary
python main.py research-coach-summary

# 查看每日 checklist
python main.py research-coach-checklist

# 查看 replay training plan
python main.py research-coach-replay-plan

# 查看 rule review queue
python main.py research-coach-rule-queue

# 查看 data repair plan
python main.py research-coach-data-repair
```

---

## GUI 使用方式

1. 啟動 GUI：`python main.py gui`
2. 在 tab bar 選擇 **Research Coach**
3. 點選 **Run Daily Coach** 或 **Run Weekly Coach** 執行分析
4. 在各 tab 查看 Daily Checklist / Weekly Checklist / Replay Training / Rule Review Queue / Data Repair
5. 點選 **Generate Report** 產生 Markdown 報告
6. 點選 **Open Latest Report** 開啟報告
7. 點選 **Refresh** 重新讀取最新儲存的分析結果

---

## 不下單 / 不接實盤交易

- Coaching Only — 純研究教練，不提供交易指令
- Research Only — 所有建議均為研究流程改善，非交易建議
- No Real Orders — 不連接 broker，不接 submit_order，不自動下單
- Not Investment Advice — 非投資建議，非買賣建議
- Production Trading BLOCKED — REAL_ORDER_READY=False

---

## 不提供投資建議

本系統所有輸出均為：
- 研究流程改善建議
- 回放訓練計畫
- Rule 審查優先序
- 資料修復優先序
- 學習筆記提示

所有輸出不構成任何投資建議、交易建議、買賣建議。
