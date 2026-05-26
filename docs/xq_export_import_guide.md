# XQ Export One-Command Import Guide

This guide explains how to import XQ Global technical-analysis export files
directly into TW Quant Cockpit without manually splitting columns.

---

## Why You Do Not Need to Split Columns Manually

XQ Global exports a single file that contains all data in a wide-column format:

```
時間, 開盤價, 最高價, 最低價, 收盤價, 成交量(張),
融資(張), 差額(張), 融券(張), 融券差額,
買賣超(張), 投信持股(張), 投信成本線,
大戶持股比例, 散戶持股比例, 大戶買賣力, 散戶買賣力,
...
```

The `import-xq-export` command reads this file and automatically:

1. Identifies the date/time column
2. Maps Chinese XQ column names to TWQC standard names
3. Splits into separate datasets: daily, margin, institutional, trust_cost, holder
4. Imports each to the standard `data/import/` path
5. Auto-fills the stock profile

---

## How to Export from XQ Global

1. Open the XQ Global technical analysis chart for the stock.
2. Right-click on the chart area.
3. Select "輸出到 Excel" (Export to Excel) or "匯出資料".
4. Save the file as `.xlsx` or `.csv`.

The exported file will contain all the indicator columns that are visible in the chart panel.

---

## Usage

### Step 1: Dry-run (preview, no files written)

```bash
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科 --dry-run
```

This shows:
- Which columns were detected
- How many rows each data type would contain
- Any warnings about partial or missing data

### Step 2: Import (write to standard paths)

```bash
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科
```

### Step 3: Verify

```bash
python main.py data-check --stock 2454
python main.py stock-report --stock 2454 --mode real
```

---

## Supported Input Formats

| Extension | Support |
|-----------|---------|
| .xlsx | Yes (requires openpyxl: `pip install openpyxl`) |
| .xls | Yes (requires openpyxl or xlrd) |
| .csv | Yes — UTF-8-SIG, UTF-8, Big5, CP950 auto-detected |

---

## Column Mapping

### Daily OHLCV

| XQ Column | TWQC Column |
|-----------|-------------|
| 時間 | date |
| 開盤價 | open |
| 最高價 | high |
| 最低價 | low |
| 收盤價 | close |
| 成交量 / 成交量(張) / 成交股數 | volume |

### Margin / Short

| XQ Column | TWQC Column |
|-----------|-------------|
| 融資(張) / 融資餘額 | margin_balance |
| 差額(張) / 融資增減 | margin_change |
| 融券(張) / 融券餘額 | short_balance |
| 融券差額 / 融券增減 | short_change |

### Institutional Net Buy

| XQ Column | TWQC Column |
|-----------|-------------|
| 投信買賣超(張) / 投信買賣超 | trust_net_buy |
| 外資買賣超(張) / 外資買賣超 | foreign_net_buy |
| 自營商買賣超(張) / 自營商買賣超 | dealer_net_buy |
| 買賣超(張) (ambiguous) | trust_net_buy if trust holding columns exist |

### Trust Cost

| XQ Column | TWQC Column |
|-----------|-------------|
| 投信成本線 / 投信平均成本 | trust_avg_cost |
| 投信買超張數 / 投信買超 | trust_buy_shares |
| 投信買進金額 / 投信金額 | trust_buy_amount |
| 收盤價 | close |
| (computed) | price_vs_trust_cost_pct |

`price_vs_trust_cost_pct = (close - trust_avg_cost) / trust_avg_cost * 100`

### Holder Structure

| XQ Column | TWQC Column |
|-----------|-------------|
| 大戶持股比例 / 大戶比例 | major_holder_ratio |
| 大戶買賣力 | major_change |
| 散戶持股比例 / 散戶比例 | retail_holder_ratio |
| 散戶買賣力 | retail_change |

---

## Common Warnings

### short_balance not found

The XQ export does not include short-selling (融券) columns.
`margin` will still be imported with financing (融資) fields only.

### institutional contains trust only

The export has only one net-buy column and it was mapped to `trust_net_buy`.
`foreign_net_buy` and `dealer_net_buy` will be empty.

### holder import is partial

`major_holder_ratio` was not found in the export.
Holder data is imported with available fields only.

### Excel serial date converted

The date column contained numeric values like `45798`.
These are Excel serial dates (days since 1899-12-30) and have been automatically converted:
`45798 -> 2025-05-xx`

---

## Date Formats Supported

| Input | Output |
|-------|--------|
| 2024-01-02 | 2024-01-02 |
| 2024/01/02 | 2024-01-02 |
| 20240102 | 2024-01-02 |
| 113/01/02 (ROC year) | 2024-01-02 |
| 1130102 (ROC compact) | 2024-01-02 |
| 45798 (Excel serial) | 2025-05-xx |

---

## Batch Processing Multiple Stocks

Process each stock one at a time:

```bash
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科
python main.py import-xq-export --file D:\XQ\2330.xlsx --symbol 2330 --name 台積電
python main.py import-xq-export --file D:\XQ\6669.xlsx --symbol 6669 --name 緯穎
```

After importing all stocks, run audit and plan:

```bash
python main.py data-audit --export
python main.py import-plan
```

---

## Export Split Option

To save each split DataFrame to separate CSV files (for inspection or re-use):

```bash
python main.py import-xq-export --file D:\XQ\2454.xlsx --symbol 2454 --name 聯發科 --export-split --output-dir D:\XQ\twqc_bundle
```

This creates:

```
D:\XQ\twqc_bundle\
  2454_daily.csv
  2454_margin.csv
  2454_institutional.csv
  2454_trust_cost.csv
  2454_holder.csv
```

These split CSVs can later be imported via `batch-import` if needed.

---

## Disclaimer

All data, analysis, and reports are for research and simulation only.
They do not constitute investment advice.
Automated order execution is strictly prohibited in v1.
