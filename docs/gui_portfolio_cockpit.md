# GUI Portfolio Cockpit — v0.3.13

## v0.3.13 目標

在 v0.3.12 完成 Portfolio & Risk Simulation CLI 後，v0.3.13 把模擬結果整合進 GUI Cockpit，
形成「投資組合控盤視覺化面板」。

**Portfolio Cockpit 讓你可以直接在 GUI 中：**

1. 查看最新 Scenario 的完整 KPI（Sharpe、Max Drawdown、Profit Factor 等）
2. 比較 4 個 scenario 的結果
3. 查看近期模擬交易記錄
4. 查看候選股排名與建議持倉比例
5. 查看族群集中度
6. 一鍵重新跑模擬（不下單）
7. 開啟最新 Markdown 報告

---

## 如何啟動

```bash
# 預設 mock mode
python main.py cockpit

# real mode（使用真實 CSV 資料）
python main.py cockpit --mode real
```

啟動後在主視窗中點選 **Portfolio Cockpit** 標籤頁。

---

## 如何先跑 simulate-portfolio

Portfolio Cockpit 讀取的是 `data/backtest_results/portfolio_*.csv` 的輸出。

**方法 A：CLI 先跑（建議）**

```bash
python main.py simulate-portfolio --mode real --scenario balanced
python main.py simulate-portfolio --mode real --scenario all
```

跑完後開啟 GUI，Portfolio Cockpit 會自動讀取結果。

**方法 B：GUI 內直接跑**

1. 開啟 `python main.py cockpit --mode real`
2. 點選 **Portfolio Cockpit** 標籤頁
3. 若無資料，顯示 Empty State 提示
4. 按 **Refresh Portfolio Simulation** 或 **Run Balanced Scenario** 觸發模擬
5. 等待背景執行完成（不阻塞 GUI）
6. 結果自動更新到各表格

---

## 如何讀 Scenario Comparison

**Scenarios 標籤頁** 顯示 4 個 scenario 的比較表。

| 欄位 | 說明 |
|------|------|
| Scenario | conservative / balanced / aggressive / no_risk_control_baseline |
| Total Return | 總報酬（相對初始資金） |
| Ann. Return | 年化報酬 |
| Sharpe | Sharpe Ratio（目標 > 1.5） |
| Max Drawdown | 最大回撤（目標 < -20%） |
| Profit Factor | 獲利因子（目標 > 1.5） |
| Win Rate | 勝率 |
| Trades | 交易次數 |
| Avg Exposure | 平均資金曝險比例 |

**顏色說明：**
- Sharpe >= 1.5：綠色
- Sharpe 1.0~1.5：橘色
- Sharpe < 1.0：紅色
- Max Drawdown < -20%：紅色
- Profit Factor >= 1.5：綠色

---

## 如何看 Candidate Ranking

**Candidates 標籤頁** 從交易記錄中統計各標的的表現。

| 欄位 | 說明 |
|------|------|
| Symbol | 股票代號 |
| Name | 股票名稱 |
| Sector | 產業族群 |
| Trades | 此標的交易次數 |
| Total PnL | 此標的總損益 |
| Avg PnL | 此標的平均損益 |
| Win Rate | 此標的勝率 |

注意：此為模擬回測統計，非實際交易記錄。

---

## 如何看 Suggested Positions

**Positions 標籤頁** 顯示依模擬進場訊號的建議配置：

| 欄位 | 說明 |
|------|------|
| Symbol | 股票代號 |
| Name | 股票名稱 |
| Entry Date | 模擬進場日期 |
| Entry Price | 模擬進場價（signal-date close） |
| Suggested Weight | 建議倉位比例（依 scenario 參數） |
| Entry Reason | 進場原因 |
| Stop Loss | 固定停損價 |
| Take Profit Half | 停利一半觸發價 |
| Trailing Stop | 移動停損追蹤價 |
| Risk Warning | 風險警示 |

---

## 如何看 Sector Exposure

**Sector 標籤頁** 顯示目前族群集中度：

| 欄位 | 說明 |
|------|------|
| Sector | 產業族群 |
| Exposure % | 目前族群曝險比例 |
| Limit % | 族群上限（balanced = 50%） |
| Status | OK / OVER_LIMIT |

若超出限制，Risk Warnings 面板會顯示警示。

---

## Simulation Only / No Real Orders

Portfolio Cockpit **固定顯示以下警示**：

```
[ Simulation Only ]
Real Order Execution: DISABLED
No real orders will be sent
```

Portfolio Cockpit **不做以下任何事**：

- 不連接 Shioaji / 兆豐 API
- 不呼叫任何 broker 下單介面
- 不讀取真實帳戶資訊
- 不寫入任何券商系統
- 不修改 API Key / .env

所有計算均為本地歷史資料模擬。

---

## Risk Warnings 說明

### OBSERVATIONAL confidence

目前 14-symbol universe 樣本量不足：

```
OBSERVATIONAL（觀察性）：
  symbol_count = 14（< 30）
  結論不可宣稱策略有效
  僅用於框架功能驗證
```

### TIMING_ESTIMATED

部分財報公告日為法定期限估算（非 MOPS 實際公告日）：

```
timing_estimated=True 時：
  EPS / 毛利率 / PE 等基本面資料
  使用靜態快照，非按 announcement_date 過濾
```

### MAX DRAWDOWN WARNING

若最大回撤超過 -20%，顯示警示提醒。

---

## 注意事項

> **[!] 本框架僅供研究與模擬，不構成投資建議。**
> 統計樣本量不足時，所有數字不可用於實際交易決策。
> 系統不接兆豐 API，不接 Shioaji，不自動下單。
> 第一版仍然禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。

---

*TW Quant Cockpit v0.3.13 — 2026*
