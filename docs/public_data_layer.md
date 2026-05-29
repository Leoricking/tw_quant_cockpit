# Public Data Layer — v0.3.9

## 概覽

v0.3.9 建立公開資料 API / 爬蟲資料層，用來自動補足：

1. 月營收 12 個月以上
2. EPS / 毛利率 / 營業利益率
3. 財報公告日 (announcement_date)
4. 完整三大法人細分
5. 完整融資融券資料
6. Intraday 1 分 K / 5 分 K 匯入與標準化
7. 未來 tick / 五檔資料 provider 介面 (PLANNED)

## 支援資料來源

| 優先序 | 來源 | 資料類型 | 需要 Token |
|--------|------|---------|-----------|
| 1 | FinMind API | 月營收、財報、法人、融資券 | 選填 (FINMIND_TOKEN) |
| 2 | TWSE OpenAPI | 上市月營收、法人、融資券 | 不需要 |
| 3 | TPEx OpenAPI | 上櫃月營收、法人、融資券 | 不需要 |
| 4 | MOPS 爬蟲 | 月營收歷史、財報公告日、EPS | 不需要 |

Fallback 順序：FinMind → TWSE/TPEx → MOPS crawler → existing CSV

## 欄位 Schema

### monthly_revenue.csv
```
month,symbol,name,revenue,revenue_mom,revenue_yoy,accumulated_revenue,accumulated_yoy,source,fetched_at
```

### fundamental.csv
```
year,quarter,symbol,eps,gross_margin,operating_margin,operating_income,net_income,announcement_date,source,fetched_at
```

### institutional.csv
```
date,symbol,foreign_net_buy,trust_net_buy,dealer_net_buy,foreign_buy,foreign_sell,trust_buy,trust_sell,dealer_buy,dealer_sell,source,fetched_at
```

### margin.csv
```
date,symbol,margin_balance,margin_change,short_balance,short_change,sbl_short_balance,source,fetched_at
```

### intraday (1min / 5min)
```
symbol,date,time,datetime,open,high,low,close,volume,source
```
Optional: vwap,big_buy_sell_power,retail_buy_sell_power,bid_volume,ask_volume,buy_sell_pressure

## CLI 使用方式

### 抓取公開資料
```bash
# 抓單股
python main.py fetch-public-data --stock 2454
python main.py fetch-public-data --stock 2454 --months 24

# 抓 universe（需先 build-universe-manifest）
python main.py fetch-public-data --universe 10
python main.py fetch-public-data --manifest data/universe/universe_manifest.csv

# 指定來源
python main.py fetch-public-data --stock 2454 --source finmind
python main.py fetch-public-data --stock 2454 --source twse
python main.py fetch-public-data --stock 2454 --source mops

# Dry-run（不寫檔）
python main.py fetch-public-data --stock 2454 --dry-run

# 覆蓋模式
python main.py fetch-public-data --stock 2454 --replace
```

### 匯入 Intraday 資料
```bash
# 資料夾批次匯入
python main.py import-intraday --folder D:\XQ\twqc_bundle\intraday --freq 1min
python main.py import-intraday --folder D:\XQ\twqc_bundle\intraday --freq 5min

# 單檔匯入
python main.py import-intraday --file D:\XQ\twqc_bundle\intraday\2454_1min.csv --symbol 2454 --freq 1min

# Dry-run
python main.py import-intraday --folder D:\XQ\twqc_bundle\intraday --freq 1min --dry-run
```

### 查看資料來源狀態
```bash
python main.py data-source-status
```

### 批次補充 Universe 資料
```bash
python main.py enrich-universe-data --universe 10
python main.py enrich-universe-data --manifest data/universe/universe_manifest.csv --months 24
python main.py enrich-universe-data --universe 10 --dry-run
```

## Cache / Rate Limit

- API 回應快取於 `data_cache/api/`（TTL 預設 1 小時）
- MOPS 爬蟲最小間隔 2 秒，最大重試 2 次
- TWSE / TPEx 最小間隔 1.5 秒
- FinMind 最小間隔 1 秒

## Data Lineage

所有資料均保留：
- `source`：資料來源（finmind / twse_openapi / tpex_openapi / mops_crawler / xq_intraday_1min）
- `fetched_at`：抓取時間（UTC ISO 格式）

## 缺資料 Fallback

| 情況 | 行為 |
|------|------|
| 單一 source 失敗 | 記錄 warning，繼續試下一個 source |
| 所有 source 失敗 | 回傳 None，不 crash |
| 網路斷線 | 記錄 warning，顯示 source failed |
| MOPS 格式改變 | 記錄 warning，回 None |

## Tick / BidAsk — 未來介面

目前 tick / 五檔資料為 PLANNED / NOT CONFIGURED。

- `data/tick_bidask_interface.py`：定義標準欄位，不抓真實資料
- `provider-status` / `data-source-status` 顯示 PLANNED / NOT CONFIGURED
- 不假造 tick / bidask 資料

## 注意事項

1. 不接兆豐 API。
2. 不接 Shioaji。
3. 不自動下單。
4. FinMind token 只能透過環境變數 `FINMIND_TOKEN` 設定，不寫入程式。
5. `announcement_date` 缺失時，財報資料只能作 PARTIAL / 指示性判斷。
6. 回測不可使用 mock 資料作正式結論。
7. 樣本不足時必須顯示 INSUFFICIENT。
8. 所有公開資料僅供研究、回測、選股參考，不構成投資建議。
