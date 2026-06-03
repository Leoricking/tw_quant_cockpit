# Research Workflow Automation (v0.4.9)

> **[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. No broker connection. No auto-weight changes.**

---

## v0.4.9 目標

將 Research Assistant / Coach 產出的 daily checklist、weekly checklist、replay training plan、rule review queue、data repair plan 串成可執行的「研究型工作流」。

---

## Research Workflow Automation 是什麼

Research Workflow Automation 是一套 read-only / research-only 的工作流執行引擎。

它負責：
1. 從 Research Coach 與 Research Review Dashboard 讀取建議
2. 將建議轉換為可執行的 ResearchWorkflowTask
3. 透過 SafeCommandRegistry 驗證每個 task 的指令安全性
4. 執行通過安全檢查的 tasks（使用 subprocess，不使用 shell=True）
5. 產生 daily / weekly research package
6. 產生 workflow summary 與 Markdown report

---

## 與 Research Coach 的關係

Research Coach（v0.4.8）產生：
- Daily checklist
- Weekly checklist
- Replay training plan
- Rule review queue
- Data repair plan

Research Workflow Automation（v0.4.9）讀取這些輸出，並將其轉換為可執行的 workflow tasks。

如果沒有 coach output，workflow builder 會產生 basic workflow（使用預設的 safe command 清單）。

---

## Daily Research Workflow

Daily research workflow 包含：

1. Data quality gate check
2. Provider reliability check
3. Provider health check
4. Data freshness check
5. Notification scan
6. Research review (daily)
7. Research coach (daily)
8. Journal summary
9. Rule governance check
10. Signal quality report
11. ML knowledge feature summary
12. ML knowledge leakage check
13. Auto report (daily profile)

每個 task 都會通過 SafeCommandRegistry 驗證。不通過者 status=BLOCKED，不執行。

---

## Weekly Review Workflow

Weekly review workflow 包含：

1. Research review (weekly)
2. Research coach (weekly)
3. Signal quality report
4. Rule governance check
5. Journal summary
6. Experiment list
7. Intraday replay
8. ML knowledge leakage check
9. Model monitoring (if available)

---

## Safe Command Registry

SafeCommandRegistry 定義允許執行的 research-only commands。

### 允許的指令（白名單）

```
python main.py data-quality-gate --mode real
python main.py provider-reliability --mode real
python main.py provider-health
python main.py api-fetch-diagnostics --mode real
python main.py data-freshness
python main.py notification-list
python main.py notification-scan --mode real
python main.py research-review --mode real --period daily
python main.py research-review-summary
python main.py research-coach --mode real --period daily
python main.py research-coach-summary
python main.py journal-summary
python main.py rule-governance --mode real
python main.py signal-quality --mode real --report
python main.py ml-knowledge-feature-summary
python main.py ml-knowledge-leakage-check --mode real
python main.py experiment-list
python main.py auto-report --mode real --profile daily
python main.py intraday-replay --mode real
python main.py stable-release-check --mode real
```

### Blocked Command Rules

任何包含以下關鍵字的指令都會被 BLOCKED：

**Trading words:** buy, sell, order, submit_order, place_order, broker, shioaji, live trade, auto trade, execute trade

**Shell compound:** &&, ;, ||, |, >, <, `` ` ``

**Shell control:** cd, powershell, cmd, bash, sh

**Git commands:** git

**Secrets:** .env, token, password, api_key

---

## Daily Research Package

Daily package 存於 `data/backtest_results/research_workflow/daily_package_YYYY-MM-DD/`

包含：
- `index.md` — Package 索引
- Workflow summary
- Coach checklist summary
- Research review summary
- Notification summary
- Journal summary
- Data quality summary
- Provider reliability summary
- Rule governance summary
- ML knowledge summary
- Report links
- Next action list
- Safety statement

---

## Weekly Review Package

Weekly package 存於 `data/backtest_results/research_workflow/weekly_package_YYYY-MM-DD/`

包含：
- `index.md` — Package 索引
- Weekly scorecard
- Top mistakes
- Weak rules
- Data blockers
- Replay training progress
- Journal review backlog
- Experiment summary
- Model monitoring summary
- Next week action plan
- Safety statement

---

## CLI 使用方式

```bash
# Dry run（只列出 tasks，不執行）
python main.py research-workflow --mode real --type daily_research --dry-run

# Run daily research workflow
python main.py research-workflow --mode real --type daily_research

# Run weekly review workflow
python main.py research-workflow --mode real --type weekly_review --dry-run
python main.py research-workflow --mode real --type weekly_review

# 產生 Markdown report
python main.py research-workflow-report --mode real

# 顯示 latest summary
python main.py research-workflow-summary

# 列出 latest tasks
python main.py research-workflow-tasks

# 產生 / 顯示 package
python main.py research-workflow-package --type daily_research
python main.py research-workflow-package --type weekly_review
```

---

## GUI 使用方式

1. `python main.py cockpit --mode real`
2. 選擇 **Research Workflow** 標籤頁
3. 點擊 **Run Daily Workflow Dry Run** 預覽 tasks
4. 點擊 **Run Daily Workflow** 執行
5. Task Table 顯示 priority、status、duration、warning
6. Blocked Command Table 顯示所有 blocked commands 與原因
7. Package Panel 顯示 package path 或 empty state

---

## 不下單 / 不接實盤交易

- 不接 Shioaji 實盤下單
- 不接兆豐實盤下單
- 不接 broker submit_order
- 不自動下單
- 不自動買賣
- 不自動改權重
- 不自動套用最佳權重
- 不自動啟用 ML feature
- 不讀取真實券商成交回報

---

## 不提供投資建議

本系統所有輸出（workflow summary、daily package、weekly package、report）僅供研究參考，不構成投資建議。

`REAL_ORDER_READY=False` 永遠不得改為 True。

---

*TW Quant Cockpit v0.4.9 — Research Workflow Automation — Research Only — Not Investment Advice*
