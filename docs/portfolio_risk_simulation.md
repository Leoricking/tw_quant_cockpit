# Portfolio & Risk Simulation — v0.3.12

## v0.3.12 目標

在 v0.3.11 完成長線策略驗證後，v0.3.12 把「單股訊號」升級成「投資組合風險模擬」，
驗證實戰資金配置與風控規則是否對組合 KPI 有幫助。

**要驗證的核心問題：**
1. 最多同時持有幾檔最穩
2. 每檔資金比例多少最合理
3. 停利一半是否改善 Profit Factor
4. 移動停損是否降低 Max Drawdown
5. 族群集中度限制是否降低風險
6. Portfolio KPI 是否符合 Sharpe > 1.5, Max Drawdown < 20%, Profit Factor > 1.5

---

## 為什麼從單股回測進入 Portfolio Simulation

單股回測的限制：
- 無法反映資金分配的影響
- 無法反映持倉分散的效果
- 無法驗證風控規則（停損/停利）在組合層面的實際效益
- 無法計算 Sharpe Ratio（需要組合層面的資金曲線）

Portfolio Simulation 補充：
- 計算實際資金曲線（equity curve）
- 驗證最大持倉數、單檔資金比例的組合影響
- 比較不同風控規則對 Max Drawdown 和 Profit Factor 的效益
- 輸出可解讀的統計報告

---

## CLI 使用方式

```bash
# 預設 balanced scenario
python main.py simulate-portfolio --mode real

# 指定 scenario
python main.py simulate-portfolio --mode real --scenario balanced
python main.py simulate-portfolio --mode real --scenario conservative
python main.py simulate-portfolio --mode real --scenario aggressive

# 比較所有 4 個 scenarios
python main.py simulate-portfolio --mode real --scenario all

# 自訂參數
python main.py simulate-portfolio --mode real \
    --initial-capital 1000000 \
    --max-positions 5 \
    --position-size-pct 0.2 \
    --stop-loss-pct 0.08 \
    --take-profit-pct 0.20 \
    --trailing-stop-pct 0.10

# Mock 模式（使用真實 CSV 資料但在 mock mode 下執行）
python main.py simulate-portfolio --mode mock
```

---

## Scenarios

### A. conservative（保守型）

```
max_positions=3, position_size_pct=0.20
stop_loss_pct=0.06, take_profit_pct=0.15, trailing_stop_pct=0.08
sector_exposure=0.40
```
適合：低風險偏好，優先控制回撤。

### B. balanced（平衡型，預設）

```
max_positions=5, position_size_pct=0.20
stop_loss_pct=0.08, take_profit_pct=0.20, trailing_stop_pct=0.10
sector_exposure=0.50
```
適合：平衡報酬與風險。

### C. aggressive（積極型）

```
max_positions=8, position_size_pct=0.15
stop_loss_pct=0.10, take_profit_pct=0.25, trailing_stop_pct=0.12
sector_exposure=0.60
```
適合：追求高報酬，可接受較高回撤。

### D. no_risk_control_baseline（無風控基準）

```
max_positions=10, position_size_pct=0.15
stop_loss_pct=0.15 (only fixed)
use_half_take_profit=False, no trailing stop
no sector limit
```
用途：基準比較，驗證風控規則是否真的有幫助。

---

## 資金配置規則

### 單檔部位

```
position_value = portfolio_equity * position_size_pct
```

若 max_positions=5, position_size_pct=0.20，滿倉 5 檔時：
全部資金投入（100% exposure）。

若現金不足 position_size_pct * equity：使用可用現金的 95%。

**現金管理規則：**
- 不使用槓桿
- 不融資
- 不做空
- 現金不足時不買入

### 族群集中度

```
sector_exposure = sum(position_value in sector) / portfolio_equity
```

若 sector_exposure + new_position_value > max_sector_exposure_pct：
不允許新增同族群部位。

### 候選排名

```
portfolio_rank_score =
  0.30 * bull_stock_score
  + 0.20 * buy_point_score
  + 0.20 * strategy_knowledge_score
  + 0.15 * fundamental_quality_score
  + 0.10 * microstructure_score
  + 0.05 * sector_strength_score
  - warnings_penalty
```

**Warnings penalty（各項）：**

| Warning | Penalty |
|---------|---------|
| no_chase_warning | -8 |
| fake_breakout_risk | -8 |
| fundamental_warning | -6 |
| overvalued_warning | -6 |
| timing_estimated | -3 |
| sector_concentration_warning | -4 |

---

## 分批進出

**進場分批（v0.3.12 未實作）：**
第一版使用 signal-date close 進場，每 5 個交易日掃描候選。
未來可改為：
- 每 N 日掃描
- 逐步建倉（第一次建半倉，確認後補全倉）

---

## 停利一半（Half Take-Profit）

當 `price >= entry_price * (1 + take_profit_pct)`：
1. 賣出一半部位，記錄 reason=TAKE_PROFIT_HALF
2. 剩餘部位使用移動停損保護獲利
3. 不允許再次觸發「停利一半」（half_taken=True）

```
peak_price = max(observed prices since entry)
trailing_stop = peak_price * (1 - trailing_stop_pct)
```

---

## 移動停損（Trailing Stop）

僅對「已停利一半」的剩餘部位生效：

```
peak_price = max(current_price, previous_peak_price)
trailing_stop_price = peak_price * (1 - trailing_stop_pct)

if current_price <= trailing_stop_price:
    exit(reason=TRAILING_STOP)
```

---

## 固定停損

對所有持倉（含未停利一半的完整部位）：

```
stop_loss_price = entry_price * (1 - stop_loss_pct)

if current_price <= stop_loss_price:
    exit(reason=STOP_LOSS)
```

---

## 交易成本模型（v0.3.12 簡化版）

| 費用項目 | 費率 |
|---------|------|
| 買進手續費 | 0.1425% |
| 賣出手續費 | 0.1425% |
| 賣出證交稅 | 0.3% |
| 滑價假設   | 5 bps |

```
buy_cost_factor  = 1 + 0.001425 + 0.0005  = 1.001925
sell_rev_factor  = 1 - 0.001425 - 0.003 - 0.0005 = 0.995075
```

---

## KPI 解讀

### Sharpe Ratio（目標 > 1.5）

```
Sharpe = (annualized_excess_return) / annualized_volatility
```

- > 1.5：優秀
- 1.0 ~ 1.5：良好
- < 1.0：需要改進

### Max Drawdown（目標 > -20%）

```
Max Drawdown = min((equity - peak_equity) / peak_equity)
```

- > -10%：良好
- -10% ~ -20%：可接受
- < -20%：風控不足

### Profit Factor（目標 > 1.5）

```
Profit Factor = sum(winning_pnl) / abs(sum(losing_pnl))
```

- > 2.0：優秀
- 1.5 ~ 2.0：良好
- < 1.5：策略邊際效益不足

### 為什麼不追求 90% 勝率

**高勝率≠高獲利。** 若損失遠大於獲利（avg_loss >> avg_win），
90% 勝率也可能虧損。

Expectancy = win_rate × avg_win + (1 - win_rate) × avg_loss

只要 Expectancy > 0 且 Profit Factor > 1，策略就有正期望值。
勝率只是參考，不是優化目標。

---

## Data Leakage 防範

1. **Technical signals**: 僅使用當日與過去資料（backward-looking rolling windows）
2. **Entry price**: 使用 signal-date close price（第一版），報告標示此限制
3. **Fundamental data**: 靜態快照，非 per-date 時間序列過濾
   - timing_estimated=True 的財報公告日為估計值
   - 未來版本應按 announcement_date 過濾
4. **不可用 forward return 排名** candidate selection
5. **不可用未來最高價決定 trailing stop 起始值**

---

## 統計置信度

`StatConfidence.for_portfolio_simulation()` 規則：

| 條件 | 判定 |
|------|------|
| symbol_count < 10 | INSUFFICIENT |
| trade_count < 30 | INSUFFICIENT |
| trading_days < 120 | INSUFFICIENT |
| 10 ≤ symbol_count < 30 | OBSERVATIONAL |
| symbol_count ≥ 30 and trade_count ≥ 200 and trading_days ≥ 240 | RELIABLE |

**14 個股的預期結果**：OBSERVATIONAL。
不可宣稱策略已有效。

---

## 輸出檔案

| 檔案 | 說明 |
|------|------|
| `data/backtest_results/portfolio_equity_curve.csv` | 日期 × 資金曲線 |
| `data/backtest_results/portfolio_trades.csv` | 所有成交記錄 |
| `data/backtest_results/portfolio_daily_positions.csv` | 每日投入資金量 |
| `data/backtest_results/portfolio_metrics.csv` | 核心 KPI |
| `data/backtest_results/portfolio_config_comparison.csv` | Scenario 比較 |
| `reports/portfolio_simulation_report_YYYY-MM-DD.md` | Markdown 報告 |

以上輸出均已加入 `.gitignore`，不提交至 repo。

---

## 注意事項

> **[!] 本框架僅供研究與模擬，不構成投資建議。**
> 統計樣本量不足時，所有數字不可用於實際交易決策。
> 系統不接兆豐 API，不接 Shioaji，不自動下單。
> 第一版仍然禁止實盤自動下單（TWQC_ENABLE_REAL_ORDER=false）。

---

*TW Quant Cockpit v0.3.12 — 2026*
