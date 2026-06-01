# Intraday Replay Cockpit — Documentation

**Version**: v0.4.4
**Status**: Stable
**Mode**: Replay Training Only | Read Only | No Real Orders | Production Trading: BLOCKED

---

> **[!] SAFETY NOTICE**
> This module is for research and training purposes only.
> It does NOT generate real orders, live predictions, or trading signals.
> Production trading is permanently blocked in all components.
> Not investment advice.

---

## v0.4.4 目標 (Goals)

v0.4.4 的核心目標是提供一個完整的 Intraday Replay Cockpit，用於研究和訓練：

1. 以 1min / 5min 頻率回放歷史 Intraday 數據，bar-by-bar
2. 偵測 Opening Range / VWAP / Fake Breakout / Volume Profile 等關鍵 overlay
3. 結合 Strategy 規則 overlay，作為訓練參考（僅標記，不下單）
4. Training Mode：根據事件生成練習題目，評估學習成效
5. 產生 Replay Session 報告，記錄訓練指標
6. 絕對安全：read_only = True，no_real_orders = True，production_blocked = True

---

## Intraday Replay Cockpit 是什麼

Intraday Replay Cockpit 是一個 11 個模組組成的訓練系統：

| # | 模組 | 說明 |
|---|------|------|
| 1 | `replay/__init__.py` | 套件入口，版本定義 |
| 2 | `replay/replay_session.py` | Session 管理、JSON 持久化 |
| 3 | `replay/replay_engine.py` | Bar-by-bar 回放引擎、CSV 載入 |
| 4 | `replay/replay_events.py` | 事件偵測（OR / VWAP / Fake / Volume） |
| 5 | `replay/opening_range_replay.py` | Opening Range overlay 計算 |
| 6 | `replay/vwap_replay.py` | 累計 VWAP overlay 計算 |
| 7 | `replay/fake_breakout_replay.py` | Fake Breakout 偵測 overlay |
| 8 | `replay/volume_profile_replay.py` | Volume Profile / POC / Value Area |
| 9 | `replay/strategy_replay.py` | Strategy 規則 overlay（唯讀，標記用） |
| 10 | `replay/training_mode.py` | 練習題目生成、答題、評分 |
| 11 | `replay/replay_metrics.py` | Session 指標計算 |

支援模組：

| # | 模組 | 說明 |
|---|------|------|
| 12 | `reports/intraday_replay_report.py` | Markdown 報告生成 |
| 13 | `gui/intraday_replay_adapter.py` | GUI ↔ Replay 橋接層 |
| 14 | `gui/intraday_replay_panel.py` | PySide6 GUI 面板 |
| 15 | `docs/intraday_replay_cockpit.md` | 本文件 |

---

## 1min / 5min Replay

回放引擎從以下路徑讀取資料：

```
data/import/intraday_standard/{freq}/{symbol}.csv
data/import/intraday_standard/{freq}/{symbol}_*.csv
```

- **freq**: `1min` 或 `5min`（可擴充）
- 載入後按 date 過濾（選填）
- Bar-by-bar 回放，`step_forward()` / `step_backward()` / `jump_to_time()`
- 完全不暴露未來 bar（除非 `reveal_future=True`）
- 缺少資料時返回 `INSUFFICIENT_INTRADAY_DATA`，不崩潰

---

## Opening Range Replay

從當日前 N 根 bar（預設 N=15 for 1min）計算 Opening Range。

### 六種狀態

| 狀態 | 說明 |
|------|------|
| `BUILDING_RANGE` | 開盤 N 根 bar 尚未完成，仍在建立 OR |
| `INSIDE_RANGE` | 當前價格在 OR High / Low 之間 |
| `BREAK_HIGH` | 價格突破 OR High |
| `BREAK_LOW` | 價格跌破 OR Low |
| `FAILED_BREAK_HIGH` | 曾突破 OR High 但已回到 OR 內 |
| `FAILED_BREAK_LOW` | 曾跌破 OR Low 但已回到 OR 內 |

Overlay 輸出：
- `opening_high` / `opening_low` / `opening_range_pct`
- `current_position_in_range` (0-1)
- `opening_strength_so_far` (0-100)
- `bars_in_range` / `opening_bars_count`

---

## VWAP Replay

以累計方式計算 VWAP，使用可見 bar 的 close × volume。

### 狀態

| 狀態 | 說明 |
|------|------|
| `ABOVE_VWAP` | 當前價格高於 VWAP |
| `BELOW_VWAP` | 當前價格低於 VWAP |
| `AT_VWAP` | 當前價格距 VWAP ≤ 0.1% |
| `UNKNOWN` | 資料不足 |

Overlay 輸出：
- `current_vwap` / `price_vs_vwap_pct`
- `above_vwap_ratio_so_far` — 已可見 bar 中在 VWAP 上方的比例
- `vwap_reclaim` / `vwap_lost` — 最近 3 bar 是否有交叉

缺少 volume 欄位時自動 fallback 為等權 VWAP（close 平均）。

---

## Fake Breakout Replay

偵測假突破模式，評估追高風險。

### 偵測邏輯

1. **突破嘗試 (Breakout Attempt)**: 前一根 bar 收在近 10 bar High 之上
2. **突破確認 (Breakout Confirmed)**: 目前 bar 仍維持在突破水位之上
3. **假突破失敗 (Breakout Failed)**: 前一根突破，目前 bar 收回水位之下

### 風險等級

| 等級 | 說明 |
|------|------|
| `LOW` | 無明顯突破嘗試 |
| `MEDIUM` | 有突破嘗試，尚未確認 |
| `HIGH` | 突破已失敗，確認為假突破 |
| `CRITICAL` | 低量假突破，追高風險極高 |

---

## Volume Profile Replay

以可見 bar 的成交量分佈建立 Volume Profile。

### 輸出

- `poc_price_so_far` — 成交量最大價位 (Point of Control)
- `value_area_high_so_far` / `value_area_low_so_far` — 含 70% 成交量的價格區間
- `price_vs_poc_pct` — 當前價格相對 POC 的偏移百分比
- `volume_cluster_strength` (0-100) — POC 集中度
- `support_pressure_state` — AT_POC / ABOVE_POC / BELOW_POC / IN_VALUE_AREA / OUTSIDE_VALUE_AREA

---

## Strategy Overlay

`StrategyReplayOverlay` 從已有的 rule governance snapshot 讀取規則，作為訓練標記顯示。

**重要安全原則**：
- 所有信號標記為 `training_annotation: True`
- `research_only: True` / `no_real_orders: True`
- 永遠不調用 `submit_order` 或任何下單函式
- 僅讀取現有研究資料，不做任何預測

---

## Training Mode

### 六種題目類型

| 類型 | 觸發事件 |
|------|----------|
| `OPENING_RANGE_DECISION` | OR Break 事件 |
| `VWAP_DECISION` | VWAP Reclaim / Lost 事件 |
| `FAKE_BREAKOUT_RISK` | Fake Breakout Warning 事件 |
| `CHASE_OR_WAIT` | Volume Spike 事件 |
| `SUPPORT_PRESSURE` | POC Touch 事件 |
| `EXIT_OR_HOLD` | 預留（未來擴充） |

### 評分

- 每題 10 分
- 總分 0-100，等第 A/B/C/D/F
- 訓練分數僅供自我評估，不代表實際交易績效

---

## 為什麼不做 Live Prediction

Intraday Replay Cockpit 故意不做 live prediction，原因如下：

1. **資料品質**: 即時 tick 資料尚未通過完整的品質驗證
2. **過擬合風險**: 回測中看起來好的 pattern，live 環境不保證有效
3. **執行風險**: 無 slippage / 手續費 / 流動性模型，live prediction 毫無意義
4. **監管合規**: 此系統為研究工具，任何 live prediction 可能違反適用法規
5. **訓練優先**: Replay 的目的是訓練研究者的判斷力，而非自動化
6. **安全設計**: `production_blocked = True` 是架構層面的硬限制，不是選項

---

## CLI 使用方式

所有 CLI 命令均為研究/訓練用，不產生真實交易。

### 1. 準備 Intraday 數據

```bash
python -m scripts.intraday_pipeline --symbol AAPL --freq 1min
```

確認數據位於 `data/import/intraday_standard/1min/AAPL.csv`。

### 2. 啟動 Replay Session

```python
from replay.replay_session import ReplaySessionManager
mgr = ReplaySessionManager()
session = mgr.create_session(symbol="AAPL", date="2025-01-15", freq="1min")
print(session.session_id)
```

### 3. 載入並回放

```python
from replay.replay_engine import IntradayReplayEngine
engine = IntradayReplayEngine()
result = engine.prepare_replay(symbol="AAPL", date="2025-01-15", freq="1min")
print(result["total_bars"])
```

### 4. 逐 Bar 步進

```python
bar = engine.step_forward()
print(bar)  # {"bar_index": 1, "close": 225.30, ...}

bar = engine.step_backward()
bar = engine.jump_to_time("10:30")
```

### 5. 取得 Overlay

```python
from replay.opening_range_replay import OpeningRangeReplay
from replay.vwap_replay import VWAPReplay
import pandas as pd

visible = engine.get_visible_bars()
df = pd.DataFrame(visible)

or_overlay = OpeningRangeReplay().build_overlay(df)
vwap_overlay = VWAPReplay().build_overlay(df)
print(or_overlay["range_break_status"])
print(vwap_overlay["vwap_state"])
```

### 6. 生成事件

```python
from replay.replay_events import ReplayEventBuilder
events = ReplayEventBuilder().build_events(df)
for evt in events:
    print(evt.event_type, evt.title)
```

### 7. 生成報告

```python
from reports.intraday_replay_report import IntradayReplayReportBuilder
builder = IntradayReplayReportBuilder()
path = builder.build(
    session_summary=session.to_dict(),
    opening_range_summary=or_overlay,
    vwap_summary=vwap_overlay,
)
print(f"Report saved: {path}")
```

---

## GUI 使用方式

### 步驟 1：開啟 GUI

```bash
python main.py
```

在主選單選擇 "Intraday Replay Cockpit"。

### 步驟 2：設定參數

- **Symbol**: 輸入股票代號，例如 `AAPL`
- **Date**: 輸入日期 `YYYY-MM-DD`（可留空表示最新）
- **Freq**: 選擇 `1min` 或 `5min`

### 步驟 3：載入數據

點擊 **Load** 按鈕，系統從 `data/import/intraday_standard/` 讀取 CSV。

若找不到資料，顯示 `INSUFFICIENT_INTRADAY_DATA`，不崩潰。

### 步驟 4：逐 Bar 回放

- **Step ▶**: 前進一根 bar
- **◀ Step**: 後退一根 bar
- **Jump to time + Jump**: 跳轉至指定時間（如 `10:30`）

每步後自動更新：Current Price / VWAP State / Opening Range State / Fake Breakout Risk。

### 步驟 5：查看 Overlay

Summary Cards 即時顯示：
- Current Price
- VWAP State (ABOVE/BELOW/AT_VWAP)
- Opening Range State (6 種狀態)
- Fake Breakout Risk (LOW/MEDIUM/HIGH/CRITICAL)
- Bars Replayed / Events Detected

### 步驟 6：查看 Event Timeline

事件表格顯示所有在可見 bar 範圍內偵測到的事件，按嚴重程度著色：
- 綠色: INFO
- 橙色: WARNING
- 紅色: CRITICAL

### 步驟 7：回答練習題目

當重要事件觸發時，Training Panel 顯示練習題目：
1. 閱讀題目描述
2. 選擇答案（Radio Button）
3. 點擊 **Submit Answer**
4. 查看正確答案和說明
5. 追蹤 Training Score

**注意**: 答案僅供學習，不是交易指令。

### 步驟 8：生成報告

點擊 **Generate Report** 生成 Markdown 報告，儲存於 `reports/intraday_replay_report_YYYY-MM-DD.md`。

---

## 安全原則 (Safety Principles)

1. **Read Only**: 所有 replay 模組設定 `read_only = True`，不修改任何市場資料
2. **No Real Orders**: `no_real_orders = True`，絕不產生任何下單指令
3. **Production Blocked**: `production_blocked = True`，架構層面硬性封鎖
4. **No Live Prediction**: 不做 live prediction，不連接任何即時數據源
5. **Training Only**: 所有分析標記為「訓練標注」，不是交易信號
6. **Future Data Protected**: 預設不暴露未來 bar（`reveal_future=False`）
7. **Graceful Degradation**: 缺少資料返回 `INSUFFICIENT_INTRADAY_DATA`，不崩潰
8. **Optional Pandas**: pandas 為選填依賴，無 pandas 時優雅降級
9. **Session Isolation**: Replay sessions 儲存於 `replay_sessions/`，與正式研究數據隔離
10. **Audit Trail**: 所有 session 以 JSON 持久化，每個操作有 timestamp 記錄

---

## 安全聲明 (Safety Declaration)

```
[!] Research Only
[!] Replay Training Only
[!] No Live Prediction
[!] No Real Orders
[!] Production Trading: PERMANENTLY BLOCKED
[!] Not Investment Advice
[!] Past intraday patterns do NOT guarantee future results
[!] This system is for self-education and research purposes only
```

---

*TW Quant Cockpit v0.4.4 — Intraday Replay Cockpit Module*
*Maintained for research and training purposes only.*
