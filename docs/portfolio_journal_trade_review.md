# Portfolio Journal & Trade Review — v0.4.6

> **[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. No broker connection. No real execution fills.**

## v0.4.6 目標

建立研究型交易日誌系統，讓平台可以記錄：
- 模擬交易研究 (simulated trade)
- 紙面交易記錄 (paper trade)
- Intraday Replay 訓練筆記 (replay note)
- Signal 有效性檢討 (signal review)
- 投資組合整體回顧 (portfolio review)
- 手動研究筆記 (manual note)

## Portfolio Journal 是什麼

Portfolio Journal 是一個**研究型日誌工具**，不是實盤交易系統。

- 不連接券商
- 不提交訂單
- 不讀取真實成交回報
- 只記錄研究者的思考過程、計劃、結果、錯誤

## 研究型交易日誌 vs 實盤交易日誌

| 項目 | 研究型 (本系統) | 實盤交易日誌 |
|------|---------------|------------|
| 券商連接 | 否 | 是 |
| 真實成交 | 否 | 是 |
| 自動下單 | 否 | 可能 |
| 資料來源 | 研究者手動輸入 | 成交回報 API |
| 目的 | 學習 / 研究 / 回顧 | 帳務紀錄 |

## 如何新增 Journal Entry

### CLI

```bash
# 新增 simulated trade
python main.py journal-add \
  --symbol 2454 \
  --entry-type simulated_trade \
  --reason "MACD golden cross + volume expansion" \
  --thesis "Short-term momentum play, expecting 3-5% in 5 days" \
  --planned-entry 580.0 \
  --planned-stop 565.0 \
  --planned-target 610.0 \
  --timeframe daily

# 新增 replay note
python main.py journal-add \
  --symbol 2330 \
  --entry-type replay_note \
  --reason "Practice opening range detection" \
  --thesis "VWAP reclaim at 09:45, entered after confirmation"
```

### GUI

1. 開啟 Cockpit: `python main.py cockpit`
2. 點選 **Portfolio Journal** tab
3. 填寫 New Entry Form (右側)
4. 點選 **Add Journal Entry**

## Signal vs Actual Outcome 怎麼看

`SignalOutcomeTracker` 追蹤每筆有 `signal_id` 的 journal entry：

- `signal_source` — 訊號來源 (rule_governance / signal_quality / manual)
- `planned_entry` — 計劃入場價
- `actual_entry` / `actual_exit` — 實際入出場 (研究者手動填入)
- `actual_return_pct` — 實際報酬率
- `MFE` / `MAE` — 最大有利/不利偏移
- `outcome_label` — 結果 (WIN / LOSS / FALSE_SIGNAL / …)
- `process_quality` — 過程品質 (GOOD / PARTIAL / POOR)

```bash
python main.py journal-summary  # 查看 win rate / avg return
python main.py journal-report   # 生成完整 Markdown report
```

## Mistake Taxonomy

`MistakeTaxonomy` 提供 13 種錯誤標籤的分類與改善建議：

| Tag | Category | Severity |
|-----|----------|----------|
| `chase_high` | entry_mistake | HIGH |
| `ignored_stop` | exit_mistake | CRITICAL |
| `oversized_position` | sizing_mistake | HIGH |
| `bought_weak_stock` | entry_mistake | MEDIUM |
| `ignored_data_quality` | data_mistake | HIGH |
| `ignored_provider_warning` | data_mistake | MEDIUM |
| `ignored_fake_breakout` | entry_mistake | HIGH |
| `ignored_vwap_loss` | exit_mistake | HIGH |
| `ignored_top_pattern` | entry_mistake | MEDIUM |
| `ignored_fundamental_deterioration` | entry_mistake | MEDIUM |
| `no_plan` | process_mistake | HIGH |
| `emotional_trade` | emotional_mistake | HIGH |
| `overtrading` | process_mistake | MEDIUM |

## Replay Training Notes

`ReplayTrainingNotes` 從 Intraday Replay session 建立 journal entry：

記錄項目：
- Opening range 判斷 (broke up / down / ranging)
- VWAP reclaim / lost
- Fake breakout 觀察
- Volume profile POC level
- Strategy overlay
- 訓練分數 (1–10)
- 下次練習重點

```bash
# 建立 replay note
python main.py journal-add \
  --entry-type replay_note \
  --reason "Opening range breakout — REPLAY-xxxx"
```

## Portfolio Review

`JournalAnalytics` 提供：

```python
analytics.run()  # 全面統計
analytics.summarize_by_symbol()     # 按股票分析
analytics.summarize_by_strategy()   # 按策略分析
analytics.summarize_by_mistake_tag() # 按錯誤標籤分析
analytics.summarize_by_outcome()    # 按結果分析
analytics.summarize_process_quality() # 過程品質
```

## CLI 使用方式

```bash
# 新增 journal entry
python main.py journal-add --symbol 2454 --entry-type simulated_trade --reason "test"

# 列出 entries
python main.py journal-list
python main.py journal-list --limit 10 --symbol 2330 --status CLOSED_SIMULATED

# 顯示單筆 detail
python main.py journal-show --id JOURNAL-xxxxxxxxxxxx

# 更新 review
python main.py journal-review --id JOURNAL-xxxx --outcome WIN --notes "Good process, held stop"

# 統計摘要
python main.py journal-summary

# 生成報告
python main.py journal-report --mode real
python main.py journal-report --dry-run

# 連結 replay session
python main.py journal-link-replay --id JOURNAL-xxxx --replay-session REPLAY-xxxx
```

## GUI 使用方式

1. 開啟 Cockpit: `python main.py cockpit`
2. 點選 **Portfolio Journal** tab
3. 功能：
   - Summary Cards — 總覽統計
   - Journal Entry Table — 所有 entries
   - Entry Detail Panel — 選取後顯示 thesis/reason/planned prices
   - New Entry Form — 新增 entry
   - Review Panel — 更新 outcome / mistake tags
   - Mark Reviewed / Generate Report buttons

## 不下單 / 不接實盤交易

- `no_real_orders = True` — 所有 class 強制
- `production_blocked = True` — 所有 class 強制
- `journal_only = True` — 所有 summary 標注
- 不連 Shioaji、不連兆豐
- 不讀取券商成交回報
- 不修改持倉、不改策略權重
- 不自動啟用 rule / ML feature

## 輸出檔案 (gitignored)

| 檔案 | 說明 |
|------|------|
| `journal_data/journal_entries.jsonl` | 全部 journal entries |
| `data/backtest_results/portfolio_journal_summary.csv` | 摘要 CSV |
| `data/backtest_results/signal_outcome_summary.csv` | Signal outcome 摘要 |
| `reports/portfolio_journal_report_YYYYMMDD_HHMMSS.md` | Markdown 報告 |

---

_Portfolio Journal & Trade Review v0.4.6 — Journal Only. Research Only. No Real Orders._
