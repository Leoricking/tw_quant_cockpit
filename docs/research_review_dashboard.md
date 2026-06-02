# Research Review Dashboard (v0.4.7)

> **[!] Review Only | Research Only | No Real Orders | Production Trading: BLOCKED**

## 目標

Research Review Dashboard 把所有研究子系統的結果，彙整成每日 / 每週研究檢討總控台。

- 聚合 Notification Center、Portfolio Journal、Experiment Registry、Rule Governance、Model Monitoring、Intraday Replay、Data Quality Gate、Provider Reliability、Signal Quality、ML Knowledge Integration
- 產生 Research Scorecard
- 產生 Action Plan（只包含研究指令，不含交易指令）
- 產生 Markdown 報告

---

## 定位

1. 這是研究檢討總控台，不是交易中心。
2. 只彙整研究結果、錯誤標籤、弱規則、資料阻塞、模型監控、Replay 訓練焦點。
3. 不接實盤下單。
4. 不自動下單。
5. 不自動改權重。
6. 不讀取真實券商成交回報。
7. 所有輸出標示 Review Only / Research Only / No Real Orders / Production Trading BLOCKED。

---

## Daily Review vs Weekly Review

| 項目 | Daily Review | Weekly Review |
|------|-------------|---------------|
| period | daily | weekly |
| 聚合範圍 | 當日資料 | 最近 7 天 |
| Scorecard | 每日分數 | 每週累計 |
| Action Plan | 當日 P0/P1 優先 | 全周 P0-P3 |

---

## Scorecard 計分

| 維度 | 滿分 | 說明 |
|------|------|------|
| Process Quality | 90 | top mistakes 越多越低 |
| Data Health | 90 | data blockers 越多越低 |
| Signal Health | 85 | weak/disable signals 越多越低 |
| Rule Health | 85 | weak/low confidence rules 越多越低 |
| Model Health | 80 | drift/degradation warnings 越多越低 |
| Replay Training | 85 | training overdue → 40 |
| Journal Completion | 90 | review_required 越多越低 |
| Safety | 100 | production_blocked=True 且 real_order_ready=False |

Grade：STRONG(≥85) / GOOD(≥70) / PARTIAL(≥50) / WEAK(≥30) / BLOCKED(<30)

**Critical safety issue → overall max BLOCKED**

---

## Top Mistakes

- 從 Portfolio Journal 彙整 mistake_tag
- 最常見的 mistake_tag 顯示為 Top Mistake
- 建議練習 Intraday Replay

---

## Weak Rules

- 從 Rule Governance 抓出 low / weak / unknown confidence 的規則
- **不自動改 rule status**
- 建議人工檢視

---

## Data Blockers

- 從 Data Quality Gate 抓出失敗的 gates
- 從 Provider Reliability 抓出失敗的 provider
- **不自動修復**

---

## Replay Training Focus

- 檢查最近 replay session 是否有
  - Fake breakout 練習
  - VWAP loss/reclaim 練習
  - Opening range 練習
- 若 training_overdue=True → 降低 replay training score

---

## Journal Review

- 從 Portfolio Journal 抓出 review_required 的 entries
- 顯示 open simulated trades
- 建議人工 review

---

## Action Plan 優先級

| Priority | 條件 | 動作 |
|----------|------|------|
| P0 | Safety issue / production_blocked=False / token leak | safety_check |
| P1 | Data blocker / provider failure / critical mistake | fix_data / check_provider |
| P2 | Weak rule / model drift / replay overdue / journal backlog | review_rule / practice_replay |
| P3 | Docs / notes / optional review | read_report / update_notes |

所有 suggested commands 只能是研究指令。

---

## CLI 使用方式

```bash
# 每日 review
python main.py research-review --mode real --period daily

# 每週 review
python main.py research-review --mode real --period weekly

# 產生報告
python main.py research-review-report --mode real --period daily

# 查看最新 summary
python main.py research-review-summary

# 查看 action plan
python main.py research-review-actions
```

---

## GUI 使用方式

1. `python main.py cockpit --mode real`
2. 選擇 **Research Review** tab
3. 點選 **Run Daily Review** 或 **Run Weekly Review**
4. 查看 Scorecard / Review Items / Top Mistakes / Weak Rules / Data Blockers / Action Plan
5. 點選 **Generate Report** 產生 Markdown 報告
6. 點選 **Open Latest Report** 開啟報告

---

## 不下單 / 不接實盤交易

- 不連 Shioaji
- 不連兆豐
- 不呼叫 submit_order / place_order / broker
- 不自動改 rule status
- 不自動改權重
- 不自動啟用 ML feature
- 不讀取真實成交回報
- REAL_ORDER_READY = False（永遠）
- Production Trading = BLOCKED（永遠）

---

## 輸出位置（gitignored）

```
data/backtest_results/research_review/
  review_summary.csv
  review_items.csv
  review_scorecard.csv
  review_action_plan.csv

reports/
  research_review_dashboard_report_YYYY-MM-DD.md
```
