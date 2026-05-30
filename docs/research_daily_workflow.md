# Research Daily Workflow (v0.3.21)

## v0.3.21 目標

把每日研究流程打磨成 3 個高階指令，讓使用者每天只需執行：

```bash
python main.py update-data --mode real
python main.py run-research --mode real
python main.py open-cockpit --mode real
```

或一鍵：

```bash
python main.py daily-workflow --mode real
```

**不接實盤下單。不自動交易。不自動改權重。Read Only。**

---

## 每日推薦使用流程

### 每日收盤後

**Step 1: 更新資料**
```bash
python main.py update-data --mode real
```
執行：provider-health → provider-auto-fetch → data-freshness → data-quality-gate → data-source-status → universe-quality

**Step 2: 跑研究報告**
```bash
python main.py run-research --mode real --profile standard
```
執行：data-quality-gate → signal-quality → simulate-portfolio → auto-report

**Step 3: 開 GUI 查看**
```bash
python main.py open-cockpit --mode real
```

---

### 週末完整研究

```bash
python main.py daily-workflow --mode real --profile full
```

包含：standard 所有步驟 + rule-weight-tuning + backtest-long-term + backtest-strategy-knowledge + run-validation-suite + auto-report full

---

### 快速檢查（盤前）

```bash
python main.py run-research --mode real --profile quick
```

包含：provider-health → data-freshness → data-quality-gate → auto-report daily

---

## Workflow Profiles

| Profile | 說明 | 適合時機 |
|---------|------|---------|
| quick | 快速健康檢查 | 盤前 / 快速確認 |
| standard | 每日收盤後完整流程 | 每日常規使用 |
| full | 完整研究（含 backtest / tuning） | 週末 / 週期性深度研究 |
| gui_only | 只開 GUI | 查看已有結果 |

---

## Windows 雙擊腳本

| 腳本 | 功能 |
|------|------|
| `scripts/update_data.bat` | 更新資料 |
| `scripts/run_research.bat` | 跑研究報告 |
| `scripts/open_cockpit.bat` | 開啟 GUI |

---

## CLI 完整指令

```bash
# 更新資料
python main.py update-data --mode real
python main.py update-data --mode real --dry-run

# 研究報告
python main.py run-research --mode real
python main.py run-research --mode real --profile quick
python main.py run-research --mode real --profile standard
python main.py run-research --mode real --profile full

# 完整每日流程
python main.py daily-workflow --mode real
python main.py daily-workflow --mode real --profile standard
python main.py daily-workflow --mode real --profile full
python main.py daily-workflow --mode real --open-gui

# 開啟 GUI
python main.py open-cockpit --mode real
```

---

## 輸出產物

| 輸出 | 路徑 |
|------|------|
| Workflow Summary | `reports/daily_workflow/YYYY-MM-DD/workflow_summary.md` |
| Workflow Run Log | `logs/workflow/daily_workflow_runs.jsonl` |
| Auto Report Center | `reports/auto_report_center/YYYY-MM-DD/` |
| Data Quality Gate Report | `reports/data_quality_gate_report_YYYY-MM-DD.md` |

---

## GUI Daily Workflow Tab

1. 開啟 `python main.py cockpit`
2. 點選 **Daily Workflow** tab
3. 選擇 Mode (real/mock) 與 Profile (quick/standard/full)
4. 點 **Update Data** 更新資料
5. 點 **Run Research** 執行研究分析
6. 點 **Open Latest Report** 查看 workflow summary
7. 點 **Open Cockpit** 會提示 GUI 已開啟

---

## Safety 說明

| 安全項目 | 狀態 |
|---------|------|
| Read Only | True |
| No Real Orders | True |
| Production Trading | **BLOCKED（永遠）** |
| REAL_ORDER_READY | False（永遠不允許） |
| Does NOT auto-apply weights | True |
| Does NOT call broker.submit_order | True |

### PRODUCTION_BLOCKED 說明

`PRODUCTION_BLOCKED=True` 在 v0.3.x (v1) 永遠為 True。
這意味著系統只做研究分析，永遠不允許實盤下單或自動交易。

---

## Troubleshooting

### update-data 失敗
- 檢查 `.env` 是否設定 `FINMIND_TOKEN`
- 執行 `python main.py provider-health` 查看 provider 狀態
- 若 provider 全部失敗，執行 `python main.py data-freshness` 查看現有資料

### run-research 失敗
- 先執行 `update-data` 確保資料已更新
- 執行 `python main.py data-quality-gate --mode real` 查看資料品質分數
- 若 coverage_score < 70，需先 import 更多資料

### GUI 無法開啟
- 確認已安裝 PySide6：`pip install PySide6`
- 直接執行：`python main.py cockpit`

### report 未產生
- 確認 `reports/` 目錄存在
- 執行 `python main.py auto-report --mode real --profile daily`
