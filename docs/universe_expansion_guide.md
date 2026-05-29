# Universe Expansion Guide — v0.3.8

## 目標

將真實股票樣本從 1 檔（INSUFFICIENT）擴充到 10 / 30 / 50 檔，
讓策略回測的統計信心從 INSUFFICIENT 提升到 OBSERVATIONAL / RELIABLE。

| 樣本數 | 統計信心 | 含義 |
|--------|---------|------|
| < 10   | INSUFFICIENT  | 功能驗證，不可宣稱策略有效 |
| 10–29  | OBSERVATIONAL | 初步可觀察，不可作正式結論 |
| ≥ 30 (+ ≥120 交易日) | RELIABLE | 可參考，仍非投資建議 |

## 完整 Workflow

### Step 1 — 建立 Universe Manifest

```bash
python main.py build-universe-manifest --size 10
```

輸出：`data/universe/universe_manifest.csv`（10 檔主流股清單）

### Step 2 — 準備 XQ 匯出檔案

1. 開啟 XQ Global / XQ 金融終端
2. 對每檔股票匯出技術分析資料（Excel 或 CSV）
3. 將檔案放到：`D:\XQ\twqc_bundle\raw\`

**檔名規則：**
```
2454.xlsx       ← 以股票代碼命名（推薦）
2454_聯發科.xlsx  ← 股票代碼開頭
2383.csv
```

### Step 3 — Dry-Run 確認

```bash
python main.py batch-import-xq --folder D:\XQ\twqc_bundle\raw --universe 10 --dry-run
```

會列出：
- 找到哪些檔案
- 哪些股票缺少檔案
- 不寫入任何資料

### Step 4 — 正式匯入

```bash
python main.py batch-import-xq --folder D:\XQ\twqc_bundle\raw --universe 10
```

### Step 5 — 檢查資料品質

```bash
python main.py universe-quality --report
```

輸出：
- 每檔股票的資料完整度（日K / 法人 / 融資券 / 大戶 / 月營收 / 保管資料）
- 短線 / 中線 / 長線 / 策略回測可用性
- 統計信心期望
- 報告：`reports/universe_quality_report_YYYY-MM-DD.md`

### Step 6 — 跑驗證套件

```bash
python main.py run-validation-suite --mode real --min-symbols 10
```

依序執行：
1. validate-score
2. backtest-buy-points
3. backtest-screener
4. backtest-strategy-knowledge

## 10 檔主流股清單（預設）

| 代碼 | 名稱 | 類股 |
|------|------|------|
| 2454 | 聯發科 | 半導體 |
| 2383 | 台光電 | 電子零組件 |
| 6669 | 緯穎 | 電腦及周邊 |
| 2345 | 智邦 | 網路通訊 |
| 2330 | 台積電 | 半導體 |
| 2308 | 台達電 | 電子零組件 |
| 2317 | 鴻海 | 電子製造服務 |
| 2382 | 廣達 | 電腦及周邊 |
| 3017 | 奇鋐 | 電子零組件 |
| 3661 | 世芯-KY | 半導體 |

30 檔：`python main.py build-universe-manifest --size 30`  
50 檔：`python main.py build-universe-manifest --size 50`

## 如何解讀統計信心

**INSUFFICIENT** — 樣本太少，程式可跑但不能說策略有效  
**OBSERVATIONAL** — 初步規律可觀察，擴充樣本才能確認  
**RELIABLE** — 樣本足夠作為策略調整參考（仍非投資建議）

> 目前 v0.3.8 預設狀態（1 檔 real data）= **INSUFFICIENT**  
> 這是正常行為，不是 bug。

## 資料完整度門檻

| 分析類型 | 日K | 法人 | 融資券 | 大戶 | 月營收 |
|---------|-----|------|--------|------|--------|
| 短線    | ≥ 60 | ≥ 5 | ≥ 5 | — | — |
| 中線    | ≥ 120 | ≥ 20 | ≥ 20 | ≥ 2 | ≥ 6 |
| 長線    | ≥ 240 | — | — | ≥ 2 | ≥ 12 |
| 策略回測 | ≥ 60 | — | — | — | — |

## 注意事項

- 本系統不接 Shioaji、不接兆豐 API、不自動下單。
- 回測結果不構成投資建議。
- `data/universe/universe_manifest.csv` 不 commit（使用者資料）。
- `data/universe/universe_manifest_sample.csv` 可 commit（範例）。
- mock mode 只做功能展示，不可作策略結論。
