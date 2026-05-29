# Strategy Knowledge Backtest — v0.3.7

## 目標

驗證 Strategy Knowledge Engine Phase 2 各模組的規則是否真的有效，
而不只是教學邏輯。使用歷史真實 K 線資料計算每個訊號的勝率、
平均報酬、最大回撤、Profit Factor。

## 驗證模組

| 模組 | 驗證訊號 |
|------|---------|
| KD Advanced | kd_low_golden_cross, kd_high_death_cross, kd_mid_noise_cross, kd_high_sticky_trend |
| Short Interest | short_squeeze_fuel_score, price_up_short_balance_up, limit_up_short_balance_up, weak_stock_short_increase |
| Bottom Reversal | bottom_reversal_detected, is_speculative_rebound |
| Sector Rotation | 需要 leader_df + sector_peers（v0.3.8+ 啟用） |
| Fundamental Quality | 需要季度 EPS/毛利率時序資料（匯入後啟用） |
| No Chase | kd_high_death_cross 代理、weak_stock_short_increase 代理 |

## 如何執行 CLI

```bash
# 全部標的，real mode
python main.py backtest-strategy-knowledge --mode real

# 單一標的
python main.py backtest-strategy-knowledge --mode real --stock 2454

# 指定日期範圍
python main.py backtest-strategy-knowledge --mode real --start 2023-01-01 --end 2024-12-31

# 指定持有天數
python main.py backtest-strategy-knowledge --mode real --holding-days 20

# mock demo（不可作策略結論）
python main.py backtest-strategy-knowledge --mode mock
```

### 完整參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `--mode` | real | real / mock |
| `--stock` | 全部 | 單一標的（可選） |
| `--start` | 全部歷史 | 起始日期 YYYY-MM-DD |
| `--end` | 全部歷史 | 結束日期 YYYY-MM-DD |
| `--holding-days` | 20 | 前向報酬計算天數 |
| `--min-samples` | 30 | 最小訊號數量門檻 |
| `--output-dir` | data/backtest_results/ | CSV 輸出目錄 |
| `--report-dir` | reports/ | Markdown 報告輸出目錄 |

## 輸出 CSV

| 檔案 | 內容 |
|------|------|
| `strategy_knowledge_signals.csv` | 每個交易日 × 訊號的原始資料 |
| `strategy_knowledge_module_performance.csv` | 各模組訊號的勝率、平均報酬、PF |
| `strategy_knowledge_factor_performance.csv` | 各 filter 前後比較 |
| `strategy_knowledge_no_chase_validation.csv` | 不追價規則驗證 |
| `strategy_knowledge_no_panic_sell_validation.csv` | 不亂砍規則驗證 |
| `strategy_knowledge_rebound_validation.csv` | 破底翻反彈驗證 |
| `strategy_knowledge_sector_validation.csv` | 族群聯動（暫空） |
| `strategy_knowledge_fundamental_guard_validation.csv` | 財報防呆（暫空） |

## 輸出 Markdown 報告

```
reports/strategy_knowledge_validation_report_YYYY-MM-DD.md
```

## 如何解讀統計信心

| 等級 | 條件 | 含義 |
|------|------|------|
| `INSUFFICIENT` | 標的數 < 10 或訊號數 < 30 | 只能確認程式可跑，不能作策略結論 |
| `OBSERVATIONAL` | 訊號數 30–199 | 初步規律，需要更多資料 |
| `RELIABLE` | 標的數 ≥ 30 且訊號數 ≥ 200 且交易日 ≥ 120 | 可作參考依據（仍非投資建議） |

## 為什麼不能用 1～3 檔樣本下結論

- 3 檔樣本的訊號數通常遠低於 30（INSUFFICIENT）
- 個股特殊性強，3 檔不代表市場整體
- KD 黃金交叉一年可能只出現 2–5 次/檔 → 3 檔合計 6–15 次，無統計意義
- 需至少 30 檔、200 個訊號才能初步觀察
- 目前版本（v0.3.7）定位：功能驗證 + 框架建立，等待 v0.3.8 擴大樣本

## 如何避免 Data Leakage

1. **訊號只使用當日與過去資料**  
   所有 KD、短線分析、破底翻偵測均使用嚴格 backward-looking 計算。

2. **前向報酬只用於 label（不寫回 feature）**  
   `forward_return_Nd` 欄位僅用於評估，不作為訊號輸入。

3. **KD 計算使用 EMA（指數移動平均）**  
   EMA 在每個時間點只依賴過去資料，不引入未來值。

4. **破底翻訊號日 = 確認日（次日）**  
   偵測邏輯使用 `shift(1)` 確保前一天的反彈模式，而非當天的未來資訊。

5. **族群 correlation 僅用 rolling 60d 過去資料**  
   （v0.3.8 啟用時實作）

6. **財報資料若無 announcement_date，報告標示 [WARN]**

7. **mock mode 標示 MOCK DEMO ONLY**  
   不可作正式策略結論。

## 各模組驗證邏輯

### KD Advanced
- 使用 9 日 Stochastic，K/D 各做 3 期 EMA 平滑
- Golden cross: K 由下向上穿越 D，且兩者均 < 25（低檔黃金交叉）
- Death cross: K 由上向下穿越 D，且兩者均 > 75（高檔死亡交叉）
- Mid-range cross (25–75): 噪音，預期效果低
- Sticky high (K ≥ 80 持續 3 天+): 強勢趨勢

### Short Interest（proxy）
- 目前缺乏 margin_df，改用 price/volume 代理：
  - `price_up_short_balance_up`: 3 日漲 > 3% + 量能高於均值
  - `limit_up_short_balance_up`: 單日漲幅 ≥ 6.9%（台灣漲停代理）
  - `weak_stock_short_increase`: 收盤在 SMA20 以下 + 量能萎縮
- 匯入 margin.csv 後可使用真實融券資料

### Bottom Reversal
- 必要條件：前一日收盤在近 60 日高點下方 20%+（深跌）
- 確認條件：當日收盤 > 前日收盤（反彈收紅）+ 更高低點 + 量能不低
- 推測性反彈：滿足深跌條件但確認不完整
- 不計入 A/B/C 買點等級

## 注意事項

- 本系統不接 Shioaji、不接兆豐 API、不自動下單。
- 此回測結果不構成投資建議。
- mock mode 為功能展示，不代表真實市場績效。
- 未達 RELIABLE 等級時，不應宣稱「策略有效」。
