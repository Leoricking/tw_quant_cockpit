# TW Quant Cockpit — Strategy Validation Score v0.9.2

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] VALIDATED = research validated only. NOT trading enabled. Not Investment Advice.**

---

## v0.9.2 目標

Strategy Validation Score (v0.9.2) 為每條策略規則建立一個系統化的研究驗證評分，根據多個證據來源（Evidence Graph、Backtest、Replay、Journal 等）計算出一個 0–100 的綜合分數，並給予以下驗證等級之一：INSUFFICIENT、OBSERVATIONAL、VALIDATING、VALIDATED、CONFLICTED、REJECTED。

**核心原則：**
- 所有輸出僅供研究參考
- 不發出任何真實交易指令
- VALIDATED 等級代表研究結論，不代表啟用策略或下單
- Production trading 始終 BLOCKED

---

## Validation Grade 定義

| Grade | 說明 | 條件 |
|-------|------|------|
| **INSUFFICIENT** | 證據不足，無法評分 | 樣本數 < 10，或缺乏 Evidence Graph 資料 |
| **OBSERVATIONAL** | 觀察性規則，僅有初步觀察 | 有基礎觀察紀錄但無回測；或樣本 10–29 |
| **VALIDATING** | 正在驗證中，有部分證據 | 有回測或 Replay 紀錄，但尚未達到 VALIDATED 門檻 |
| **VALIDATED** | 研究驗證通過 | 分數 ≥ 70，有 Evidence Graph 支撐，有回測，無嚴重矛盾 |
| **CONFLICTED** | 矛盾規則，有相互衝突的證據 | 矛盾計數 ≥ 2，或正負證據勢均力敵 |
| **REJECTED** | 規則被拒絕，有明確反向證據 | 有強烈反向證據，或回測表現持續負面 |

### INSUFFICIENT 詳細條件
- Evidence Graph 樣本數 < 10
- 無任何回測記錄
- 無 Journal 記錄
- 資料覆蓋率 < 20%

### OBSERVATIONAL 詳細條件
- 有 Journal 或 Replay 記錄，但無正式回測
- 樣本數 10–29
- Evidence Graph score 存在但 < 40

### VALIDATING 詳細條件
- 有回測記錄，但樣本數 < 30 或回測期 < 6 個月
- Evidence Graph score 40–69
- 缺乏 Replay 或 Training Metrics 佐證

### VALIDATED 詳細條件
- Final score ≥ 70
- Evidence Graph score ≥ 60
- 有回測記錄，樣本數 ≥ 30
- 矛盾計數 = 0 或 1（輕微）
- 無 REJECTED 等級的子組件

### CONFLICTED 詳細條件
- 矛盾計數 ≥ 2
- 正負面證據差距 < 15 分
- 不同資料集或時間段有相互矛盾的回測結果

### REJECTED 詳細條件
- 有明確反向 Evidence Graph 節點（weight > 0.3）
- 回測勝率持續 < 40%（樣本 ≥ 30）
- Journal 記錄顯示系統性執行失敗

---

## 分數來源

Strategy Validation Score 的 final_score 由以下 7 個子分數加權計算而成：

| 來源 | 說明 | 基本權重 |
|------|------|----------|
| Evidence Graph | Research Intelligence 節點強度與連結密度 | 25% |
| Backtest | 歷史回測勝率、報酬率、樣本數 | 25% |
| Replay | 盤中重播驗證結果 | 15% |
| Journal | 交易日誌中的相關觀察記錄 | 10% |
| Training Metrics | 模型/規則訓練評估指標 | 10% |
| Data Coverage | 資料覆蓋期間與完整性 | 10% |
| Risk/Contradiction penalty | 矛盾扣分、風險因子扣分 | 最高 −25 |

---

## 權重表

```
final_score = (
    evidence_graph_score  × 0.25 +
    backtest_score        × 0.25 +
    replay_score          × 0.15 +
    journal_score         × 0.10 +
    training_score        × 0.10 +
    data_coverage_score   × 0.10 +
    validation_score      × 0.05
) - contradiction_penalty - risk_penalty

Max base score:     100.0
Max penalty:        -25.0
Effective range:    0 – 100 (clamped)
```

---

## 特殊覆蓋規則

以下規則會覆蓋標準分數計算，強制指定等級：

| 條件 | 覆蓋結果 |
|------|----------|
| sample_count < 10 | 強制 max grade = OBSERVATIONAL（即使分數高） |
| contradiction_count ≥ 2 | 強制 grade = CONFLICTED |
| 有明確 REJECTED Evidence Graph 節點 | 強制 grade = REJECTED（不論分數） |
| 無任何 Evidence Graph 資料 | 強制 grade = INSUFFICIENT |
| 回測勝率 < 40%（樣本 ≥ 30） | 最高 grade = VALIDATING |
| data_coverage < 20% | 最高 grade = OBSERVATIONAL |

---

# VALIDATED 不等於啟用策略

## ⚠ 重要聲明 ⚠

**VALIDATED 等級僅代表「研究驗證通過」。**

VALIDATED **不代表**：
- 啟用自動交易
- 生成買賣訊號
- 發出真實委託單
- 建議任何實際交易行為

VALIDATED **代表**：
- 研究證據支持此策略規則的有效性
- 可進行進一步的深度研究與回測
- 研究結論記錄在案，供未來決策參考

Production trading 始終 **BLOCKED**。`production_blocked = True` 在所有模組中強制執行，無法關閉。

---

## CLI Usage

以下 CLI 指令全部為研究模式。不發出任何真實交易指令。

| 指令 | 說明 |
|------|------|
| `python main.py strategy-validation` | 執行完整驗證評分（預設 real mode） |
| `python main.py strategy-validation --mode real` | 使用真實資料執行評分 |
| `python main.py strategy-validation --mode dry_run` | 使用模擬資料執行評分 |
| `python main.py strategy-validation-summary` | 顯示驗證摘要（總覽） |
| `python main.py strategy-validation-list` | 列出所有策略的驗證等級 |
| `python main.py strategy-validation-top` | 顯示 Top 10 VALIDATED 策略 |
| `python main.py strategy-validation-needs-backtest` | 列出需要回測的策略 |
| `python main.py strategy-validation-conflicted` | 列出 CONFLICTED 策略 |
| `python main.py strategy-validation-explain <strategy_id>` | 顯示指定策略的評分說明 |
| `python main.py strategy-validation-report` | 生成完整 Markdown 報告 |

---

## GUI Usage

### Strategy Validation Tab

在 TW Quant Cockpit 主視窗中點選 **Strategy Validation** 標籤。

**安全提示條（橘色）：**
頁面頂部顯示安全提示，提醒所有操作為研究用途，不涉及任何真實訂單。

**摘要卡片（Summary Cards）：**
共 9 個統計卡片：Total、Validated、Validating、Observational、Insufficient、Conflicted、Rejected、Avg Score、Forbidden Actions

### 5 個子標籤說明

**Tab 1: Validation Scores**
- 顯示所有策略的驗證等級與分數
- 按 final_score 降序排列
- 顏色標示：VALIDATED=綠、VALIDATING=黃、OBSERVATIONAL=藍、INSUFFICIENT=灰、CONFLICTED=橘、REJECTED=紅
- VALIDATED 等級顯示為「VALIDATED (research only)」
- 點選任意列可在 Tab 5 查看詳細說明

**Tab 2: Evidence Components**
- 顯示各策略的子分數明細
- 欄位：Component、Score、Weight、Weighted Score、Evidence、Limitation
- 按 weighted_score 降序排列

**Tab 3: Crash Reversal Validation**
- 專門顯示 6 條 Crash Reversal 策略規則的驗證狀態
- 若尚未執行驗證，顯示提示訊息

**Tab 4: Needs More Evidence**
- 顯示 INSUFFICIENT、OBSERVATIONAL、VALIDATING 等級的策略
- 說明缺少的證據類型與建議的下一步行動

**Tab 5: Explanation**
- 顯示選中策略的完整評分說明
- 包含：評分原因、支撐證據、矛盾點、限制、安全的下一步行動
- 所有輸出已過濾 BUY/SELL/ORDER 等禁用詞

### 操作按鈕

| 按鈕 | 功能 |
|------|------|
| Run Validation | 在背景執行 StrategyValidationEngine（不阻塞 UI） |
| Generate Report | 生成完整 Markdown 報告並顯示路徑 |
| Refresh | 重新載入最新已儲存的驗證結果 |
| Copy Explanation | 複製選中策略的說明至剪貼簿（已過濾禁用詞） |
| Copy Safe Next Step | 複製安全的下一步行動至剪貼簿 |

---

## Report Usage

報告以 Markdown 格式輸出至 `reports/` 目錄。

**生成方式：**
```bash
python main.py strategy-validation-report
# 或在 GUI 中點選 "Generate Report" 按鈕
# 或在 Python 中：
from reports.strategy_validation_report import StrategyValidationReportBuilder
builder = StrategyValidationReportBuilder()
path = builder.build(mode="real", output_dir="reports")
```

**報告輸出路徑：**
```
reports/strategy_validation_report_YYYY-MM-DD.md
```

**報告包含 9 個章節：**
1. 總覽（Overview）
2. Validation Grade Board（Top 20）
3. Validated Research Rules
4. Observational / Validating Rules
5. Conflicted / Rejected Rules
6. Crash Reversal Strategy Validation（6 條規則）
7. Evidence Components（Top 10）
8. Suggested Safe Next Steps
9. 安全聲明

---

## No Real Orders

本模組的所有功能均嚴格遵循以下安全原則：

- **`no_real_orders = True`** — 所有類別均設定此屬性，不可覆蓋
- **`production_blocked = True`** — Production 交易永遠封鎖
- **`validated_does_not_enable_trading = True`** — VALIDATED 等級不啟用交易
- **禁用詞過濾** — BUY、SELL、ORDER、EXECUTE、SUBMIT_ORDER、AUTO_TRADE、REAL_TRADE 在所有輸出中被替換為 REVIEW
- **無 Broker 連線** — 本模組不連接任何 Broker API
- **無自動執行** — 沒有任何排程或觸發機制會執行真實交易

---

## Not Investment Advice

本文件及所有相關程式碼輸出僅供研究與教育目的使用。

- 不構成任何形式的投資建議
- 不保證任何策略的未來績效
- 研究結論僅反映歷史資料分析，不預測未來市場走向
- 任何投資決策均應諮詢合格的財務顧問

**TW Quant Cockpit v0.9.2 — Strategy Validation Score**
*Research Only | No Real Orders | Production Trading BLOCKED*
