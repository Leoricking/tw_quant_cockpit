# Rule Weight Tuning Lab — v0.3.15

## v0.3.15 目標

在 v0.3.14 完成 Signal Quality Dashboard 後，v0.3.15 建立
「Rule Weight Tuning Lab」，讓使用者可以回測比較不同 scoring weight 配置，
找出在現有 universe 下更穩定的權重組合。

---

## 為什麼需要 Rule Weight Tuning Lab

`portfolio_rank_score` 目前使用固定權重：

```
0.30 * bull_stock_score
0.20 * buy_point_score
0.20 * strategy_knowledge_score
0.15 * fundamental_quality_score
0.10 * microstructure_score
0.05 * sector_strength_score
− warnings_penalty
```

但 Signal Quality Dashboard 顯示各訊號的實際歷史效果不同。
Rule Weight Tuning Lab 讓我們系統性地比較 7 種配置，了解哪種權重組合
在同樣 universe 上產生更好的模擬結果。

---

## 7 種預設配置

| 配置 | 說明 |
|------|------|
| **baseline_current** | 現有 production 權重（0.30/0.20/0.20/0.15/0.10/0.05） |
| **technical_heavy** | 技術面加重（bull_stock 0.35, buy_point 0.25） |
| **fundamental_heavy** | 基本面加重（fundamental 0.30） |
| **intraday_heavy** | 微結構/盤中加重（intraday 0.25） |
| **risk_control_heavy** | 懲罰加重，保守風控（all penalties ×1.5） |
| **signal_quality_boosted** | 從 signal_quality_summary.csv 動態計算 |
| **balanced_v2** | 六個元件等權重（各 1/6 ≈ 0.167） |

### signal_quality_boosted 計算方式

讀取 `data/backtest_results/signal_quality_summary.csv`，
對每個 signal_group 取主流推薦，套用乘數：

| 推薦 | 乘數 |
|------|------|
| BOOST | ×1.15 |
| KEEP | ×1.00 |
| REDUCE | ×0.85 |
| DISABLE | ×0.60 |
| INSUFFICIENT_SAMPLE | ×1.00 |

計算完成後重新正規化，使各權重和 = 1.0。
若 CSV 不存在，退回 balanced_v2。

---

## balanced_score 公式

```
balanced_score = 0.35 * norm_sharpe
               + 0.25 * norm_pf
               + 0.20 * norm_return
               + 0.20 * norm_drawdown_score
```

其中 `norm_*` = min-max 正規化（同批 7 個配置相互比較）。
`norm_drawdown_score` = 1 − norm(|max_drawdown|)（drawdown 越小越好）。

---

## 淘汰條件（Disqualification）

下列任一條件成立，該配置即被排除在 `best_config` 選擇之外：

| 條件 | 說明 |
|------|------|
| max_drawdown < −25% | 最大回撤超過 25% |
| profit_factor < 1.20 | 獲利因子低於 1.20 |
| trade_count < 30 | 交易次數少於 30 |

被淘汰的配置仍出現在比較表中，標記 DQ=YES。

---

## 如何啟動 CLI

```bash
# 比較全部 7 種配置
python main.py tune-rule-weights --mode real

# 比較並輸出 Markdown 報告
python main.py tune-rule-weights --mode real --report

# 僅評估單一配置
python main.py tune-rule-weights --mode real --config technical_heavy

# 自訂資本與日期範圍
python main.py tune-rule-weights --mode real --initial-capital 500000 --start 2023-01-01 --report
```

Console 輸出範例：

```
TW Quant Cockpit — Rule Weight Tuning Lab (v0.3.15)

Mode             : real
Config(s)        : all
Initial capital  : NTD 1,000,000

[!] Advisory Only. Does NOT auto-apply weights to production strategy.

  Rank  Config                         Return   Sharpe    MaxDD     PF  B.Score   DQ?
  -------------------------------------------------------------------------
  1     technical_heavy               +8.50%    1.32   -15.20%   1.45   0.7823    no
  2     baseline_current              +7.20%    1.18   -17.80%   1.38   0.6541    no
  3     signal_quality_boosted        +6.90%    1.15   -16.50%   1.35   0.6302    no
  4     balanced_v2                   +5.40%    0.98   -19.20%   1.22   0.5011    no
  5     fundamental_heavy             +4.80%    0.87   -21.50%   1.19   0.4202   YES
  6     risk_control_heavy            +3.20%    0.72   -13.80%   1.10   0.3891   YES
  7     intraday_heavy                +2.50%    0.61   -22.10%   1.08   0.3201   YES

Best config (balanced score) : technical_heavy
Best by Sharpe               : technical_heavy
Best by drawdown             : risk_control_heavy
Best by PF                   : technical_heavy

Comparison CSV : data/backtest_results/rule_weight_config_comparison.csv
```

---

## 如何在 GUI 查看

1. 啟動 `python main.py cockpit --mode real`
2. 點選 **Rule Weight Tuning** 標籤頁
3. 若無資料，顯示 Empty State，按 **Run Tuning**
4. Summary Cards：configs 總數、qualified 數、best config、balanced_score
5. Comparison 標籤頁：可排序的完整比較表
6. Weights 標籤頁：7 種配置的權重矩陣
7. Best Config 標籤頁：最佳配置詳細資訊
8. Signal Quality Integration 標籤頁：signal_quality_boosted 調整細節
9. Action List 標籤頁：純文字的行動建議清單

---

## 重要提醒

> **[!] Advisory Only. Does NOT auto-apply weights to production strategy.**
> **[!] Simulation Only. No Real Orders.**
>
> 本框架僅供研究與模擬，不構成投資建議。
> 所有配置比較結果僅為歷史回測，不保證未來績效。
> 建議配置需人工審閱後，手動更新 `backtest/portfolio_rules.py`。
> 系統不接兆豐 API，不接 Shioaji，不自動下單。

---

*TW Quant Cockpit v0.3.15 — 2026*
