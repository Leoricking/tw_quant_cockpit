# Research Notebook / Experiment Registry — v0.3.29

> [!] Research Only. Backtest Only. No Real Orders. Production Trading: BLOCKED.

## 目標

v0.3.29 為每次研究、回測與報告產出建立可追蹤的 experiment_id，支援 config snapshot、universe snapshot、data quality snapshot、rule snapshot、backtest result snapshot，以及 experiment 之間的比較。

## Experiment Registry 是什麼

Experiment Registry 是一個本地的研究記錄系統，儲存在 `experiments/` 目錄（不 commit 到 git）。每個 experiment 包含：

- metadata.json：基本資訊
- snapshots/：各類 snapshot JSON
- reports/：report 路徑記錄
- notebook.md：研究筆記
- notes.md：追加筆記

## experiment_id 規則

格式：`EXP-YYYYMMDD-HHMMSS-shortuuid`

範例：`EXP-20260601-143022-a1b2c3d4`

## snapshot 類型

| Type | 內容 |
|------|------|
| config | mode, git_commit, git_tag, python_version |
| universe | universe_name, size, sectors |
| data_quality | production_readiness_score, backtest_readiness_score |
| provider_reliability | reliability_score, weak_datasets |
| rule_governance | total rules, active, experimental |
| backtest | hardened backtest metrics, portfolio metrics |
| signal_quality | boost/keep/reduce/disable counts |
| portfolio | sharpe, max_drawdown, profit_factor |
| intraday | quality_score, tick_bidask_ready |
| reports | report paths and counts |

## notebook.md 怎麼看

notebook.md 包含十個章節：基本資訊、研究目的、各類 snapshot 摘要、observation、next action、安全聲明。

## 如何比較 experiments

```
python main.py experiment-compare --ids EXP-aaa,EXP-bbb
```

比較欄位包括：data quality score、backtest readiness、provider reliability、universe size、rule count、hardened backtest metrics、portfolio sharpe。

**IMPROVED 不代表可以下單。No real orders.**

## CLI 使用方式

```bash
python main.py experiment-create --name "daily research" --type daily_research --mode real --profile standard
python main.py experiment-register-latest --mode real
python main.py experiment-list
python main.py experiment-show --id EXP-xxxx
python main.py experiment-notebook --id EXP-xxxx
python main.py experiment-compare --ids EXP-aaa,EXP-bbb
python main.py experiment-report
python main.py experiment-snapshot --id EXP-xxxx
```

## GUI 使用方式

Open Cockpit → Experiment Registry tab。

功能：Create Experiment、Register Latest Run、Build Snapshots、Build Notebook、Generate Report、Compare Selected、Refresh。

## 安全聲明

- 不下單
- 不接 Shioaji / 兆豐實盤
- 不自動改權重
- 不自動套用 Rule Weight Tuning
- `production_blocked = True`
- `real_order_ready = False`

## 如何避免 commit runtime experiments

`.gitignore` 排除 `experiments/EXP-*` 和 `experiments/registry.json`。`experiments/.gitkeep` 和 `experiments/README.md` 可 commit。
