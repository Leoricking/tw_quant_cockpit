# Data Universe Expansion v1.1.0

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] Not Investment Advice.
> [!] Real Data Coverage Required. Mock Data Formal Conclusion: DISABLED.

---

## v1.1.0 目標

Data Universe Expansion 擴充真實股票樣本與 universe coverage，讓既有 Strategy Validation、Backtest、Screener、Knowledge Base 與 Research Cockpit 的統計基礎更可信。

**核心目標：**

- 建立可管理的股票 universe 定義（集中管理，不散落 hardcode）
- 支援 CORE_10 / RESEARCH_30 / EXPANDED_50 / BROAD_100 tier
- 驗證日 K、成交量、籌碼、營收、財報等欄位覆蓋率
- 建立 data coverage matrix per symbol
- 建立 universe health check
- 建立 universe expansion report
- 將統計信心從 INSUFFICIENT 推進到 OBSERVATIONAL / RELIABLE

---

## Universe Tiers

| Tier          | 說明 | 目標 |
|---------------|------|------|
| CORE_10       | 核心 10 檔 | 2330, 2308, 2345, 2383, 2454, 3017, 5274, 6669, 2317, 2327 |
| RESEARCH_30   | CORE_10 + 20 檔擴充 | AI server, semicon, networking, PCB, cooling |
| EXPANDED_50   | RESEARCH_30 + 20 檔擴充 | 更廣泛的台股 large-cap |
| BROAD_100     | Schema 支援，未來擴充至 100 檔 | 長期目標 |

Tiers 是累計的：RESEARCH_30 包含 CORE_10 的所有 symbol。

---

## Real Data Readiness

### Quality Status

| Status       | 條件 |
|--------------|------|
| READY        | daily rows >= 240, OHLC completeness >= 98%, invalid price = 0 |
| PARTIAL      | daily rows >= 120, OHLC completeness >= 90% |
| INSUFFICIENT | daily rows < 120 |
| MISSING      | 無真實日 K 資料 |
| INVALID      | 重複日期 / 負價格 / schema 破損嚴重 |

### 重要原則

- **Real mode 不可 fallback 到 mock。**
- **Mock data 不可用於正式結論。**
- 缺資料不 crash：顯示 MISSING / INSUFFICIENT，提示 FIX_DATA。
- registered 多但 ready 少 → confidence 不可 RELIABLE。

---

## 如何匯入更多股票

1. 取得真實 TWSE 日 K 資料（authorized data provider，例如 FinMind、XQ）
2. 將資料存放至 `data/import/daily/daily_k.csv`
3. 格式：symbol, date, open, high, low, close, volume
4. 執行 `python main.py universe-coverage --tier research30`
5. 查看哪些 symbol 仍為 MISSING，針對性補充

**注意：不自動下載未授權資料。不連 broker API。不下單。**

---

## 如何執行 Coverage

```bash
# 建立 CORE_10 tier
python main.py universe-build --tier core10

# 建立 RESEARCH_30 tier
python main.py universe-build --tier research30

# 分析 RESEARCH_30 coverage
python main.py universe-coverage --tier research30

# 查看缺失 symbol
python main.py universe-missing --tier research30

# 查看單一 symbol
python main.py universe-symbol --stock 2454

# 產生 report
python main.py universe-report --tier research30 --mode real
```

---

## 如何重跑 Validation

Coverage 完成後，既有指令支援 optional `--universe` / `--symbols` 參數：

```bash
# 原有行為不變（無參數）
python main.py validate-score --mode real

# 指定 universe tier（可選）
python main.py validate-score --mode real --universe research30

# 指定 symbols（可選）
python main.py validate-score --mode real --symbols 2330,2454,6669
```

---

## 統計信心解讀

| 信心等級      | 條件 |
|--------------|------|
| INSUFFICIENT | evaluated_symbols < 10 |
| OBSERVATIONAL | evaluated_symbols 10–29 |
| RELIABLE     | evaluated_symbols >= 30 AND signal_count >= 200 AND trading_days >= 120 |

**為什麼 3～5 檔不能宣稱可靠？**

3～5 檔的樣本太小，無法排除個別股票特性造成的偏差。策略結論需要足夠的橫截面樣本（symbol diversity）和時間序列深度（trading_days），才能超越個案觀察進入 OBSERVATIONAL，再到 RELIABLE。

用 3 檔聲稱策略有效，等同於從 3 人的問卷宣稱全民偏好。

---

## Mock Data 不可作正式結論

- Mock data 用於 demo / CI 功能測試。
- Mock data 不可用於 strategy validation 正式結論。
- `MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False`
- Real mode 不可 fallback 到 mock rows 判 READY。

---

## No Real Orders — Not Investment Advice

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] Broker Execution Disabled. VALIDATED does not enable trading.
> [!] Not Investment Advice. Do not make financial decisions based on these outputs.
> [!] Data Universe Expansion does not enable trading.

---

*TW Quant Cockpit v1.1.0 — Data Universe Expansion — Research Only — Not Investment Advice*
