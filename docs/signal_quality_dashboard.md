# Signal Quality Dashboard — v0.3.14

## v0.3.14 目標

在 v0.3.13 完成 GUI Portfolio Cockpit 後，v0.3.14 把所有已有的回測與驗證輸出整合成
「Signal Quality Dashboard」，讓使用者清楚知道目前哪些訊號規則：

- 應該**加權**（BOOST）
- 應該**維持**（KEEP）
- 應該**降權**（REDUCE）
- 應該**停用**（DISABLE）
- **樣本不足，暫不判斷**（INSUFFICIENT_SAMPLE）

---

## 為什麼需要 Signal Quality Dashboard

策略系統有多種訊號來源，但不知道哪些真的有效：

| 訊號來源 | 對應回測 |
|---------|---------|
| A/B/C 買點 | backtest-buy-points |
| Screener bull_stock_score | validate-score |
| Strategy Knowledge 規則 | backtest-strategy-knowledge |
| Long-Term 因子 | backtest-long-term-strategy |
| Portfolio Scenario | simulate-portfolio |
| Intraday Microstructure | （尚無獨立回測，報告 coverage 狀態） |

Signal Quality Dashboard 統一讀取以上輸出，計算標準化 KPI，並給出可解讀的建議。

---

## 如何解讀 BOOST / KEEP / REDUCE / DISABLE / INSUFFICIENT_SAMPLE

| 推薦 | 條件 | 說明 |
|------|------|------|
| **BOOST** | PF >= 1.5, avg_return > 0, confidence != INSUFFICIENT | 建議增加此訊號權重 |
| **KEEP** | PF >= 1.1, avg_return >= 0, sample >= 30 | 維持現有權重 |
| **REDUCE** | PF < 1.1 或 avg_return < 0 | 建議降低此訊號權重 |
| **DISABLE** | PF < 1.0 且 avg_return < 0 | 建議停用此訊號 |
| **INSUFFICIENT_SAMPLE** | sample < 30 或 confidence = INSUFFICIENT | 樣本不足，無法判斷 |

**重要：** 推薦為建議，不自動調整策略權重。需人工確認。

---

## 如何解讀 confidence

| 等級 | 條件 | 說明 |
|------|------|------|
| RELIABLE | symbol >= 30, trade >= 200, days >= 240 | 可信賴 |
| OBSERVATIONAL | symbol 10~29 | 觀察性，不可宣稱策略有效 |
| INSUFFICIENT | symbol < 10 或 sample < 30 | 樣本不足 |

目前 14-symbol universe → 所有來源均為 **OBSERVATIONAL**。

---

## 如何啟動 CLI

```bash
# 基本使用（不產生報告）
python main.py signal-quality --mode real

# 產生 Markdown 報告
python main.py signal-quality --mode real --report

# 重新整合所有來源並產生報告
python main.py signal-quality --mode real --refresh

# Mock mode（demo 用）
python main.py signal-quality --mode mock --report
```

Console 輸出範例：

```
TW Quant Cockpit — Signal Quality Dashboard (v0.3.14)

Mode: real
Available backtests  : buy_point, screener, strategy_knowledge, long_term, portfolio
Total signals        : 42
Confidence           : OBSERVATIONAL

BOOST            : 3
KEEP             : 12
REDUCE           : 8
DISABLE          : 1
INSUFFICIENT     : 18

Top BOOST signals:
  [buy_point] buy_point/Grade_A — PF 2.10 and avg return positive
  ...

Output CSV   : data/backtest_results/signal_quality_summary.csv
Report       : reports/signal_quality_report_2026-05-30.md
```

---

## 如何在 GUI 查看

1. 啟動 `python main.py cockpit --mode real`
2. 點選 **Signal Quality** 標籤頁
3. 若尚未有資料，顯示 Empty State，按 **Refresh Signal Quality**
4. Summary Cards 顯示 BOOST/KEEP/REDUCE/DISABLE/INSUFFICIENT 數量
5. Recommendations 標籤頁顯示所有訊號詳細推薦
6. Groups 標籤頁顯示各訊號群組的匯總統計
7. Action List 標籤頁顯示純文字版本的行動清單

---

## 為什麼目前仍是 OBSERVATIONAL

目前 universe 有 14 個股票：

```
symbol_count = 14 < 30 → OBSERVATIONAL
```

要達到 RELIABLE：
- symbol_count >= 30
- trade_count >= 200
- trading_days >= 240

在此之前，所有結論不可宣稱策略有效。Signal Quality Dashboard 的用途是：
1. 確認框架功能正確運作
2. 在擴大 universe 後提供更可信賴的方向性參考

---

## 注意事項

> **[!] Simulation Only. No Real Orders.**
> **Recommendations do not automatically change strategy weights.**
> 本框架僅供研究與模擬，不構成投資建議。
> 系統不接兆豐 API，不接 Shioaji，不自動下單。
> 不接 API、不修改帳戶、不修改 API Key。

---

*TW Quant Cockpit v0.3.14 — 2026*
