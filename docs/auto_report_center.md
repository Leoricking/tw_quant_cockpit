# Auto Report Center — v0.3.16

## v0.3.16 目標

在 v0.3.15 完成 Rule Weight Tuning Lab 後，v0.3.16 建立
「Auto Report Center」，讓使用者一鍵產生每日研究報告包，
整合所有既有回測、驗證、投資組合、訊號品質與規則權重結果
進入單一帶日期的輸出資料夾。

---

## 為什麼需要 Auto Report Center

每次分析需要手動執行多個 CLI 指令並分散查看結果。
Auto Report Center 統一入口，一次執行所有已啟用的子報告，
並在輸出資料夾中產生：

- `index.md` — 4 段報告索引
- `executive_summary.md` — 跨報告關鍵結論彙整
- `daily_market_summary.md` — 6 段每日市場摘要
- `manifest.json` — 機器可讀元資料與 safety flags

---

## 6 種 Profile

| Profile | 說明 |
|---------|------|
| **full** | 執行所有子報告（預設） |
| **daily** | 每日快速包：universe_quality / signal_quality / portfolio / daily_summary |
| **portfolio** | 僅投資組合模擬 |
| **signal** | 僅 signal_quality + strategy_knowledge |
| **stock** | 僅個股報告 |
| **universe** | 僅 universe_quality |

---

## 子報告列表

| 子報告 | 對應模組 | 輸出子資料夾 |
|--------|----------|--------------|
| Stock Reports | `analysis.stock_report_builder` | `stock_reports/` |
| Universe Quality | `backtest.universe_quality` | `universe_quality/` |
| Signal Quality | `backtest.signal_quality_engine` | `signal_quality/` |
| Portfolio Simulation | `backtest.portfolio_scenarios` | `portfolio/` |
| Rule Weight Tuning | `tuning.rule_weight_tuner` | `rule_weight/` |
| Long-Term Strategy | `backtest.long_term_strategy_backtest` | `long_term/` |
| Strategy Knowledge | `strategy.strategy_knowledge_backtest` | `strategy_knowledge/` |
| Daily Market Summary | `reports.daily_market_summary` | *(root)* |

每個子報告包裝在獨立的 try/except 中。失敗的子報告記錄在
`_failed` 清單中，不中止整體執行。

---

## 輸出結構

```
reports/auto_report_center/
└── YYYY-MM-DD/
    ├── index.md
    ├── executive_summary.md
    ├── daily_market_summary.md
    ├── manifest.json
    ├── stock_reports/
    ├── universe_quality/
    ├── signal_quality/
    ├── portfolio/
    ├── rule_weight/
    ├── long_term/
    └── strategy_knowledge/
```

---

## manifest.json 欄位

```json
{
  "version": "v0.3.16",
  "report_date": "YYYY-MM-DD",
  "generated_at": "ISO8601",
  "mode": "real",
  "safety_flags": {
    "research_only": true,
    "simulation_only": true,
    "no_real_orders": true,
    "does_not_auto_apply_weights": true,
    "does_not_connect_broker_api": true
  },
  "data_readiness": "PARTIAL | READY | UNKNOWN",
  "confidence": "OBSERVATIONAL",
  "universe_size": 14,
  "generated_count": 6,
  "failed_count": 1,
  "generated": [{"name": "...", "path": "..."}],
  "failed":    [{"name": "...", "error": "..."}],
  "key_metrics": {
    "portfolio_best_scenario": "...",
    "portfolio_best_return": 0.085,
    "portfolio_best_sharpe": 1.25,
    "signal_quality_boost_count": 3,
    "signal_quality_reduce_count": 1,
    "rule_weight_best_config": "technical_heavy",
    "rule_weight_best_balanced_score": 0.7823
  }
}
```

---

## CLI 用法

```bash
# 完整報告包（full profile）
python main.py auto-report --mode real

# 每日快速報告
python main.py auto-report --mode real --profile daily

# 投資組合報告
python main.py auto-report --mode real --profile portfolio

# 個股報告（指定股票）
python main.py auto-report --mode real --profile stock --stocks 2330 2454 2382

# 指定輸出日期
python main.py auto-report --mode real --report-date 2026-05-30

# 指定輸出資料夾
python main.py auto-report --mode real --output-dir /tmp/my_reports

# mock 模式（測試用）
python main.py auto-report --mode mock --profile daily
```

Console 輸出範例：

```
TW Quant Cockpit — Auto Report Center (v0.3.16)

Mode    : real
Profile : full
Date    : 2026-05-30

[!] Research Only. Simulation Only. No Real Orders.

Status            : ok
Output folder     : reports/auto_report_center/2026-05-30
Generated reports : 7
Failed reports    : 1

Generated:
  ✓  stock_reports
  ✓  universe_quality
  ✓  signal_quality
  ✓  portfolio
  ✓  rule_weight
  ✓  long_term
  ✓  daily_market_summary

Failed:
  ✗  strategy_knowledge  — No strategy knowledge data found

Index     : reports/auto_report_center/2026-05-30/index.md
Manifest  : reports/auto_report_center/2026-05-30/manifest.json

[!] All outputs are research-only simulation artifacts.
[!] Does NOT auto-apply weights. Does NOT place real orders.
```

---

## GUI 查看

1. 啟動 `python main.py cockpit --mode real`
2. 點選 **Auto Report Center** 標籤頁
3. 選擇 Profile，點選 **Run Auto Report**
4. 執行完成後自動刷新所有標籤頁
5. **Executive Summary** 標籤頁：跨報告結論摘要
6. **Daily Summary** 標籤頁：每日市場摘要
7. **Report Links** 標籤頁：所有已生成報告，雙擊開啟
8. **Failed Reports** 標籤頁：失敗原因清單
9. 按 **Load Latest** 載入最近一次的報告
10. 按 **Open Report Folder** 在檔案總管中開啟輸出資料夾

---

## 重要提醒

> **[!] Research Only. Simulation Only. No Real Orders.**
> **[!] Does NOT auto-apply weights. Does NOT connect broker API.**
>
> 本框架僅供研究與模擬，不構成投資建議。
> 所有報告結果僅為歷史回測，不保證未來績效。
> 系統不接券商 API，不接 Shioaji，不自動下單。
> 建議人工審閱後再決定是否手動調整策略參數。

---

*TW Quant Cockpit v0.3.16 — 2026*
