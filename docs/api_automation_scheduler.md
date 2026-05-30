# API Automation Scheduler — v0.3.17

## v0.3.17 目標

在 v0.3.16.1 完成 Auto Report Center Hotfix 後，v0.3.17 建立
「API Automation Scheduler」，用於 read-only 自動化每日資料更新
與研究報告產出。

---

## Scheduler 是什麼

一個本機 CLI + GUI 工具，允許使用者手動觸發或排程以下 read-only 任務：

| 任務 | 說明 |
|------|------|
| `daily_data_update` | 抓公開資料、檢查資料來源 |
| `daily_validation` | 執行驗證套件 + 訊號品質 + 投組模擬 |
| `daily_auto_report` | Auto Report Center（daily profile） |
| `weekly_signal_quality` | 每週訊號品質報告 |
| `weekly_rule_weight_tuning` | 每週規則權重調優（不自動套用） |
| `monthly_universe_quality` | 每月 universe 品質檢查 |

---

## 為什麼第一版只做 Read-Only

1. 投資決策不可自動化 — 需要人工審閱才能下單。
2. Rule Weight Tuning 結果僅供參考，不自動套用到正式策略。
3. 本系統不接券商 API，不接 Shioaji，不接兆豐實盤。
4. 第一版以研究與模擬為主，等資料量足夠、策略驗證充分後才考慮進一步自動化。

---

## 支援哪些任務

所有任務均為 `read_only=True` + `no_real_orders=True`：

| 任務名稱 | 排程 | 執行時間 |
|---------|------|---------|
| `daily_data_update` | 每日 | 18:00 |
| `daily_validation` | 每日 | 18:20 |
| `daily_auto_report` | 每日 | 18:40 |
| `weekly_signal_quality` | 每週五 | 19:00 |
| `weekly_rule_weight_tuning` | 每週五 | 19:30 |
| `monthly_universe_quality` | 每月 1 日 | 20:00 |

---

## CLI 使用方式

```bash
# 初始化安全 config（全部 disabled）
python main.py scheduler-init-config

# 查看 scheduler 狀態
python main.py scheduler-status

# 列出所有任務
python main.py scheduler-list

# 查看下次執行時間
python main.py scheduler-next-runs

# 手動觸發任務
python main.py scheduler-run --task daily_auto_report --mode real
python main.py scheduler-run --task daily_validation --mode real
python main.py scheduler-run --task weekly_signal_quality --mode real
python main.py scheduler-run --task weekly_rule_weight_tuning --mode real
python main.py scheduler-run --task monthly_universe_quality --mode real

# 指定 config 與 log 路徑
python main.py scheduler-run --task daily_auto_report --mode real \
    --config config/scheduler_config.yaml \
    --log-dir logs/automation
```

---

## GUI 使用方式

```bash
python main.py cockpit --mode real
```

進入 **Automation Scheduler** 標籤頁：

1. **Initialize Safe Config** — 建立安全預設 config（全部 disabled）
2. **Run Once buttons** — 手動觸發各任務，使用 QThread 背景執行
3. **Task Schedule** 標籤頁 — 顯示所有任務的排程與狀態
4. **Recent Runs** 標籤頁 — 顯示最近執行記錄
5. **Safety** 標籤頁 — 顯示所有安全防線

---

## config/scheduler_config.yaml 說明

複製 `config/scheduler_config.example.yaml` 並重命名：

```yaml
enabled: false       # false = 不自動啟動排程
mode: real           # real | mock
timezone: Asia/Taipei
read_only: true
no_real_orders: true

tasks:
  daily_auto_report:
    enabled: false   # 改為 true 以啟用
    schedule_type: daily
    run_time: "18:40"
    read_only: true
    no_real_orders: true
```

**注意：**
- `config/scheduler_config.yaml` 已加入 `.gitignore`，不會 commit 到 repo
- 不要在 config 檔案中寫入任何 token 或 API key
- 所有 token 請設定在 `.env` 檔案中

---

## task_runs.jsonl 說明

路徑：`logs/automation/task_runs.jsonl`

每行一個 JSON 物件，記錄一次任務執行：

```json
{
  "task_id": "a1b2c3d4",
  "task_name": "daily_auto_report",
  "mode": "real",
  "started_at": "2026-05-30T18:40:01.123456",
  "finished_at": "2026-05-30T18:41:15.654321",
  "duration_seconds": 74.5,
  "status": "ok",
  "generated_outputs": ["auto_report [daily]: 5 generated → ..."],
  "warnings": [],
  "errors": [],
  "read_only": true,
  "no_real_orders": true
}
```

---

## latest_status.json 說明

路徑：`logs/automation/latest_status.json`

記錄最近一次任務執行摘要與各任務狀態：

```json
{
  "last_task": "daily_auto_report",
  "last_status": "ok",
  "last_run_at": "2026-05-30T18:41:15.654321",
  "read_only": true,
  "no_real_orders": true,
  "tasks": {
    "daily_auto_report": {
      "last_status": "ok",
      "last_run_at": "2026-05-30T18:41:15.654321",
      "last_duration": 74.5
    }
  }
}
```

---

## 為什麼不自動下單

1. 本系統不接任何券商 API（Shioaji、兆豐、Interactive Brokers 等）。
2. `AutomationTaskRunner` 的 `no_real_orders=True` 為 hard-coded，無法由 config 覆蓋。
3. 所有包含 `order / trade / submit / buy / sell / broker / live / execute` 等關鍵字的任務名稱會被 Safety Guard 攔截。
4. 實盤下單需要人工確認，不可自動化。

---

## 為什麼不自動改權重

1. `weekly_rule_weight_tuning` 僅執行分析，輸出 `best_config` 建議。
2. 系統不自動修改 `backtest/portfolio_rules.py` 中的正式策略權重。
3. 需要人工審閱回測結果後，手動更新策略。
4. 建議流程：週五執行 → 週末審閱報告 → 決定是否手動調整。

---

## 重要提醒

> **[!] Read Only. Research Only. No Real Orders.**
> **[!] Scheduler Does Not Trade. Does Not Modify Weights.**
> **[!] Does Not Connect Broker API. Does Not Place Orders.**
> **[!] Does Not Write API Keys. Does Not Send Emails.**
> **[!] Does Not Upload Reports to External Services.**
>
> 本框架僅供研究與模擬，不構成投資建議。
> 所有任務執行結果僅為歷史回測與觀察性分析，不保證未來績效。
> 建議配置需人工審閱後，手動更新策略參數。

---

*TW Quant Cockpit v0.3.17 — 2026*
