# Coverage Repair Workflow — v1.1.2

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] VALIDATED does not enable trading. Broker Execution Disabled.
> [!] dry_run=True default. destructive=False enforced.
> [!] Not Investment Advice.

---

## v1.1.2 目標

v1.1.2 Coverage Repair Workflow 的目標是把既有 Universe Coverage、Data Import Onboarding、
Retry Manifest、Data Hygiene 的異常資料狀態，轉換成可識別、可排序、可追蹤、可驗證的修復工作流程。

**核心能力：**
- 可識別的 coverage issue（18 種 issue type）
- 可排序的 repair task（P0–P3 priority）
- 可執行 dry-run 的修復計畫
- 可追蹤的修復批次
- 可驗證 before / after coverage 差異
- 可輸出的 unresolved / blocked / retry 清單
- 可安全執行的 metadata repair

---

## Coverage Issue 類型（18 種）

| Issue Type | 說明 | 預設處理 |
|---|---|---|
| MISSING_SYMBOL_DATA | 沒有任何 real daily 資料 | SOURCE_REQUIRED |
| INSUFFICIENT_HISTORY | trading_days < 120 | SOURCE_REQUIRED |
| PARTIAL_OHLC | OHLC 欄位不完整 | SOURCE_REQUIRED |
| MISSING_VOLUME | volume 缺漏 | SEMI_AUTO |
| DUPLICATE_DATE | 同 symbol/date 有完全相同 row | AUTO_SAFE |
| CONFLICTING_ROW | 同 symbol/date 有不同 OHLCV | MANUAL |
| INVALID_OHLC | high < low / close <= 0 等 | NOT_REPAIRABLE (BLOCKED) |
| INVALID_VOLUME | 負數 volume / 非數字 volume | MANUAL |
| FUTURE_DATE | 日期超出今日 | MANUAL |
| STALE_DATA | 最後日期超過門檻（30 天） | SOURCE_REQUIRED |
| DATE_GAP | 疑似交易日缺口（heuristic，標 approximation） | SEMI_AUTO |
| MISSING_CHIPS | 缺籌碼資料集 | SOURCE_REQUIRED |
| MISSING_REVENUE | 缺營收資料集 | SOURCE_REQUIRED |
| MISSING_FUNDAMENTALS | 缺基本面資料集 | SOURCE_REQUIRED |
| SCHEMA_MISMATCH | 欄位名稱 / dtype / 日期格式不一致 | AUTO_SAFE |
| SOURCE_UNKNOWN | 資料來源不明 | MANUAL |
| IMPORT_FAILED | 前次匯入失敗 | SEMI_AUTO |
| LOW_MAPPING_CONFIDENCE | 欄位映射信心值低 | NOT_REPAIRABLE (BLOCKED) |

---

## Severity

| Level | 說明 |
|---|---|
| CRITICAL | 嚴重資料損壞，影響所有計算 |
| HIGH | 影響正式回測 / backtest blocker |
| MEDIUM | 部分資料缺失，影響統計信心 |
| LOW | 次要欄位缺漏 |
| INFO | 提示性，不影響計算 |

---

## Repairability

| Level | 說明 |
|---|---|
| AUTO_SAFE | 可安全自動執行（identical duplicate removal, schema normalize） |
| SEMI_AUTO | 需要確認後執行（reimport safe） |
| MANUAL | 需人工審查後處理 |
| SOURCE_REQUIRED | 需補充原始資料才能修復 |
| NOT_REPAIRABLE | 無法自動修復（INVALID OHLC, LOW_MAPPING_CONFIDENCE） |

---

## Priority

| Level | 適用情境 |
|---|---|
| P0 | INVALID OHLC、嚴重 CONFLICT、formal backtest blocker、corrupt schema |
| P1 | CORE_10 缺資料 / 不足歷史 / 過期 / 關鍵欄位 duplicate / partial |
| P2 | RESEARCH_30 partial coverage / missing volume / 缺 chips / revenue |
| P3 | optional fundamentals / low-impact metadata / broad100 待辦 |

> [!] Priority 不以股票熱門程度或預期報酬為依據。

---

## Dry-Run 行為

- 所有操作預設 `dry_run=True`。
- `dry_run=True` 時只輸出計畫，不修改任何資料。
- 必須明確加 `--execute --allow-write` 才能寫入。
- `--execute` 未加 `--allow-write` → **BLOCKED**。
- `--dry-run` 與 `--execute` 不可同時使用。

---

## Auto-Safe Repair（允許的安全操作）

以下操作可在 `allow_write=True` 時執行：

1. **DEDUPLICATE_IDENTICAL** — 僅移除 symbol/date/OHLCV 完全相同的 row，保留一筆。
2. **NORMALIZE_SCHEMA** — 僅欄位名稱 / dtype / 日期格式正規化，不改 OHLCV 數值。
3. **NORMALIZE_DATE** — 僅可明確解析的格式，不猜日期，不移動 future date。
4. **REIMPORT_SAFE** — 呼叫既有 onboarding / importer，使用 MERGE_SAFE。
5. **REFRESH_COVERAGE** — 呼叫 UniverseCoverageAnalyzer，更新 UniverseStore。

---

## Manual Review（不可自動執行）

以下 issue 必須人工審查：

- **CONFLICTING_ROW** — 同 symbol/date 有不同 OHLCV，不可自動覆蓋。
- **INVALID_OHLC** — high < low / close <= 0，不可自動改值（BLOCKED）。
- **INVALID_VOLUME** — 負數 / 非數字 volume，不可自動修正。
- **LOW_MAPPING_CONFIDENCE** — 欄位映射信心值低，禁止自動執行（BLOCKED）。
- **FUTURE_DATE** — 日期超出今日，需確認是否為格式錯誤再處理。

---

## Source Data Required（不下載、不捏造）

以下 issue 需補充原始資料才能修復：

- MISSING_SYMBOL_DATA
- INSUFFICIENT_HISTORY
- PARTIAL_OHLC
- STALE_DATA
- MISSING_CHIPS / MISSING_REVENUE / MISSING_FUNDAMENTALS

> [!] 不自動下載外部資料。不使用 mock data 補正式 K 線。不線性插值捏造 OHLC。
> [!] 不以前值填補正式價格。不以未來資料補 K 線。

---

## Conflict Policy

- CONFLICTING_ROW 永遠進入 MANUAL_REVIEW。
- CLI / GUI 不提供 auto overwrite 選項。
- `CONFLICT_AUTO_OVERWRITE_ENABLED = False` 永遠不可設為 True。

---

## Synthetic Data Prohibition

- `SYNTHETIC_PRICE_REPAIR_ENABLED = False` — 不捏造任何 OHLCV。
- `EXTERNAL_DATA_DOWNLOAD_ENABLED = False` — 不自動下載外部資料。
- `MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False` — mock data 不可用於正式結論。

---

## Before / After Validation

修復完成後執行以下驗證：

1. rows 不應意外大幅減少（超過 deduplicated 數量）。
2. dedupe 只能移除完全相同 duplicate。
3. 不能新增 invalid OHLC。
4. 不能新增 future date。
5. 不能新增 conflicting row。
6. real dataset 不能混入 mock source。
7. coverage quality 若未改善，狀態不可寫 REPAIRED。
8. 若只完成部分，標 PARTIAL。
9. 若仍缺 source，維持 NEEDS_SOURCE_DATA。

---

## Universe Integration

- repair scan 依 CORE_10 / RESEARCH_30 / EXPANDED_50 / BROAD_100 / custom / single stock。
- 修復後呼叫 UniverseCoverageAnalyzer，更新 UniverseStore。
- 顯示 ready_before / ready_after / partial_before / partial_after 等差異。
- 不自動重跑全部 backtest。

---

## Onboarding Integration

- IMPORT_FAILED → CoverageIssue (IMPORT_FAILED)
- PARTIAL import → CoverageIssue (PARTIAL_OHLC)
- conflict file → MANUAL task
- missing columns → SOURCE_REQUIRED 或 REVIEW
- retry manifest → 可匯入 CoverageRepairTaskBuilder
- REIMPORT_SAFE → 呼叫既有 onboarding，不重寫 importer

---

## CLI SOP

```
# 1. 掃描 coverage issues
python main.py coverage-repair-scan --tier research30
python main.py coverage-repair-scan --stock 2454

# 2. 查看 issue 清單
python main.py coverage-repair-issues
python main.py coverage-repair-issues --priority P1

# 3. 查看 repair tasks
python main.py coverage-repair-tasks
python main.py coverage-repair-tasks --stock 2454

# 4. 建立 repair plan（dry-run）
python main.py coverage-repair-plan --tier research30
python main.py coverage-repair-plan --symbols 2330,2454,6669

# 5. 執行 dry-run
python main.py coverage-repair-run --tier research30 --dry-run

# 6. 執行（需 --allow-write）
python main.py coverage-repair-run --tier research30 --execute --allow-write

# 7. 查看結果
python main.py coverage-repair-result --plan-id latest

# 8. 查看未解決問題
python main.py coverage-repair-unresolved

# 9. 查看需補資料清單
python main.py coverage-repair-source-required

# 10. 健康檢查
python main.py coverage-repair-health

# 11. 產生報告
python main.py coverage-repair-report --plan-id latest --mode real
```

---

## GUI SOP

1. 開啟 Coverage Repair 分頁。
2. 選擇 Tier / Stock / Custom Symbols。
3. 點 **Scan** — 查看 Issue Summary。
4. 點 **Build Dry Run Plan** — 查看 Task Queue 與 Plan Summary。
5. 點 **Export Source Requirements** — 匯出需補資料清單。
6. 點 **Export Manual Review** — 匯出人工審查清單。
7. 點 **Execute Safe Tasks**（僅在有有效 dry-run plan 後才啟用）。
8. 查看 Before / After 差異。
9. 點 **Build Report** — 產生 Markdown 報告。

> [!] Execute Safe Tasks 必須 require allow-write。Conflict rows 不提供 auto overwrite。

---

## Common Failures

| 症狀 | 可能原因 | 建議處理 |
|---|---|---|
| coverage-repair-health FAIL | coverage_repair 模組未載入 | 確認 `coverage_repair/__init__.py` 存在 |
| execute without allow-write BLOCKED | 安全設計，預期行為 | 加 `--execute --allow-write` |
| INVALID_OHLC 未被修復 | 預期行為，禁止自動修值 | 人工確認原始資料後 reimport |
| CONFLICT 永遠 MANUAL | 安全設計，預期行為 | 人工審查後提供正確資料 |
| SOURCE_REQUIRED 無法修復 | 缺原始資料 | 補充對應 dataset 後重新執行 |
| dry-run 無資料修改 | 預期行為 | 確認不需 `--execute --allow-write` |

---

## Runtime Outputs（不 commit）

```
data/repair_reports/coverage_issue_inventory.csv
data/repair_reports/coverage_repair_tasks.csv
data/repair_reports/coverage_repair_plan.csv
data/repair_reports/coverage_repair_results.csv
data/repair_reports/coverage_repair_validation.csv
data/repair_reports/coverage_source_requirements.csv
data/repair_reports/coverage_manual_review.csv
data/repair_reports/coverage_unresolved.csv
reports/coverage_repair_report_YYYY-MM-DD.md
```

---

## Safety Summary

| 項目 | 狀態 |
|---|---|
| No Real Orders | True |
| Broker Execution | Disabled |
| VALIDATED does not enable trading | True |
| dry_run default | True |
| destructive repair | Disabled by default |
| conflict auto-overwrite | Disabled |
| synthetic OHLC repair | Disabled |
| external data download | Disabled |
| mock formal repair | Disabled |
| Not Investment Advice | True |

---

*v1.1.2 Coverage Repair Workflow — Research Only. No Real Orders. Not Investment Advice.*
