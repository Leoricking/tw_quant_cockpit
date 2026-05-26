# XQ / Excel CSV Mapping Guide

This document explains how XQ Global, Excel, and manually-exported CSV columns
map to TWQC standard column names.

---

## General Notes

### Encoding

- XQ exports are often Big5 or CP950 encoded.
- Excel "Save As CSV" on Traditional Chinese Windows uses CP950.
- The TWQC importer auto-detects: UTF-8-SIG, UTF-8, Big5, CP950.
- If auto-detection fails, re-save as UTF-8 in Excel: File > Save As > CSV UTF-8 (BOM).

### Excel: Prevent Symbol Conversion to Number

- Stock codes like 0050, 2330 may be converted to integers (50, 2330) by Excel.
- To prevent this: format the symbol column as Text before pasting, or add a leading apostrophe.
- The TWQC cleaner handles 2330.0 -> 2330 but cannot recover a truncated 0050 -> 50.

### Date Formats

TWQC accepts all of the following and normalizes to YYYY-MM-DD:

| Input | Output |
|-------|--------|
| 2024/01/02 | 2024-01-02 |
| 20240102 | 2024-01-02 |
| 113/01/02 (ROC year) | 2024-01-02 |
| 1130102 (ROC compact) | 2024-01-02 |

### Month Formats

TWQC accepts all of the following and normalizes to YYYY-MM:

| Input | Output |
|-------|--------|
| 2024/01 | 2024-01 |
| 202401 | 2024-01 |
| 113/01 (ROC year) | 2024-01 |
| 11301 (ROC compact) | 2024-01 |

### Numeric Values

- Thousand separators are removed: 1,234,567 -> 1234567
- N/A, -, --, blank, null, None are converted to NaN (missing)
- Percentage columns: 12.3% -> 12.3 (stored as percentage, not fraction)

---

## 1. Daily K (daily)

Standard output: `data/import/daily/daily_k.csv`

| TWQC Column | XQ / Excel Chinese | Alternative Names |
|-------------|-------------------|-------------------|
| date | 日期 | Date, trading_date |
| symbol | 股票代號 | 代號, symbol, code, ticker |
| open | 開盤價 | 開盤, open_price |
| high | 最高價 | 最高, high_price |
| low | 最低價 | 最低, low_price |
| close | 收盤價 | 收盤, close_price |
| volume | 成交量 | 成交量(股), volume_shares |

Minimum required rows: 20 (short-term), 60 (mid-term), 120 (long-term)

---

## 2. Institutional (institutional)

Standard output: `data/import/institutional/institutional.csv`

| TWQC Column | XQ / Excel Chinese | Alternative Names |
|-------------|-------------------|-------------------|
| date | 日期 | Date |
| symbol | 股票代號 | 代號 |
| foreign_net_buy | 外資買賣超 | 外資淨買, foreign_net |
| trust_net_buy | 投信買賣超 | 投信淨買, trust_net |
| dealer_net_buy | 自營商買賣超 | 自營淨買, dealer_net |

Positive values = net buy. Negative values = net sell.
Minimum required rows: 5 (short/mid-term), 40 (full analysis)

---

## 3. Margin (margin)

Standard output: `data/import/margin/margin.csv`

| TWQC Column | XQ / Excel Chinese | Alternative Names |
|-------------|-------------------|-------------------|
| date | 日期 | Date |
| symbol | 股票代號 | 代號 |
| margin_balance | 融資餘額 | 融資, margin_bal |
| margin_change | 融資增減 | 融資變動, margin_chg |
| short_balance | 融券餘額 | 融券, short_bal |
| short_change | 融券增減 | 融券變動, short_chg |

Minimum required rows: 5 (short/mid-term), 40 (full analysis)

---

## 4. Monthly Revenue (monthly_revenue)

Standard output: `data/import/monthly_revenue/monthly_revenue.csv`

| TWQC Column | XQ / Excel Chinese | Alternative Names |
|-------------|-------------------|-------------------|
| month | 月份 | 年月, ym, period |
| symbol | 股票代號 | 代號 |
| revenue | 月營收 | 當月營收, monthly_rev |
| mom | 月增率 | 月成長率, mom_pct |
| yoy | 年增率 | 年成長率, yoy_pct |
| accumulated_yoy | 累計年增率 | 累計成長, accum_yoy |

Revenue values in thousands NTD (TWD). Percentage columns stored as e.g. 12.3 not 0.123.
Minimum required rows: 6 (mid-term), 12 (long-term)

---

## 5. Holder (holder)

Standard output: `data/import/holder/holder.csv`

| TWQC Column | XQ / Excel Chinese | Alternative Names |
|-------------|-------------------|-------------------|
| date | 日期 | Date, snapshot_date |
| symbol | 股票代號 | 代號 |
| major_holder_ratio | 大戶持股比例 | 大戶比, major_pct |
| retail_holder_ratio | 散戶持股比例 | 散戶比, retail_pct |
| major_change | 大戶持股增減 | 大戶變動, major_chg |
| retail_change | 散戶持股增減 | 散戶變動, retail_chg |

Values are percentages (0-100). Snapshots are typically weekly or monthly.
Minimum required rows: 2 (mid-term), 4 (long-term)

---

## 6. Trust Cost (trust_cost)

Standard output: `data/import/trust_cost/trust_cost.csv`

| TWQC Column | XQ / Excel Chinese | Alternative Names |
|-------------|-------------------|-------------------|
| date | 日期 | Date |
| symbol | 股票代號 | 代號 |
| trust_buy_shares | 投信買進股數 | 投信買, trust_buy |
| trust_buy_amount | 投信買進金額 | 投信買金額, trust_amt |
| trust_avg_cost | 投信平均成本 | 均成本, avg_cost |
| close | 收盤價 | 收盤 |
| price_vs_trust_cost_pct | 股價對比投信成本% | 溢折價%, price_vs_cost |

Minimum required rows: 3 (basic), 20 (standard), 40 (full analysis)

---

## 7. Profile (profile)

Standard output: `data/import/profile/stock_profile.csv`

| TWQC Column | XQ / Excel Chinese | Alternative Names |
|-------------|-------------------|-------------------|
| symbol | 股票代號 | 代號, code |
| name | 股票名稱 | 公司名, stock_name |
| market | 市場 | 交易所, exchange |
| industry | 產業 | 行業, sector_code |
| theme_tags | 主題標籤 | 主題, themes |
| is_mainstream_theme | 主流主題 | 主流, mainstream |
| sector | 類股 | 族群, group |

One row per stock. Profile does not have a date column.

---

## Common Issues

1. Symbol column recognized as integer by Excel
   - Re-format as Text in Excel before export.
   - Use clean-csv to verify: python main.py clean-csv --type profile --file profile.csv --dry-run

2. Date in ROC year format (民國年)
   - The cleaner handles both 113/01/02 and 1130102 formats automatically.

3. Thousand separators in revenue or volume
   - The cleaner removes commas automatically: 1,234,567 -> 1234567

4. Big5 / CP950 encoding error
   - The importer tries UTF-8-SIG, UTF-8, Big5, CP950 in order.
   - If all fail, re-save as UTF-8 CSV from Excel.

5. Percentage columns with % sign
   - 12.3% is stored as 12.3 (percentage number, not fraction).
   - Do not multiply by 100 before import.

6. Blank rows or header rows in the middle of the file
   - Remove these manually before import.
   - The cleaner will drop rows with empty symbol.
