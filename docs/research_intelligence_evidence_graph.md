# Research Intelligence Evidence Graph — v0.9.1 Evidence Graph UX

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not Investment Advice. Does NOT auto-trade or auto-enable strategies.**

---

## v0.8.3 目標

將 Research Intelligence 所有研究結論串成可追溯的 Evidence Graph，讓每個結論可以查到：
- 來源（source module）
- 證據（evidence）
- 支持關係（SUPPORTS）
- 衝突關係（CONTRADICTS）
- 需要更多資料（REQUIRES_DATA）
- 需要回測（REQUIRES_BACKTEST）
- 需要復盤（REQUIRES_REPLAY）

---

## Evidence Graph 是什麼

Evidence Graph 是一個 **研究證據圖譜**，不是交易訊號圖譜。

- **Node**：每個研究結論、記憶、任務、指標、錯誤、資料缺口等
- **Edge**：節點之間的關聯（支持、衝突、需要、驗證等）
- **Thread**：從 anchor node 出發的證據鏈

所有輸出只能是研究指令（REVIEW / VALIDATE / BACKTEST_MORE / FIX_DATA 等），絕不輸出 BUY / SELL / ORDER。

---

## Node Types

| Type | 說明 | 來源 |
|------|------|------|
| `RESEARCH_RECOMMENDATION` | 研究建議 | research_intelligence |
| `STRATEGY_MEMORY` | 策略記憶 | strategy_memory |
| `BACKTEST_COACH_TASK` | 教練任務 | backtest_coach |
| `TRAINING_METRIC` | 訓練指標 | training_metrics |
| `REPLAY_MISTAKE` | 復盤錯誤 | replay_training |
| `JOURNAL_PATTERN` | 日誌模式 | portfolio_journal |
| `DATA_GAP` | 資料缺口 | data_coverage |
| `REPORT_RESULT` | 報告結果 | report_pack |
| `REGRESSION_RESULT` | 回歸測試結果 | regression |
| `RULE_CANDIDATE` | 規則候選 | rule_governance |
| `STRATEGY_HYPOTHESIS` | 策略假說 | strategy_memory |
| `PROVIDER_LIMITATION` | 數據商限制 | data_coverage |
| `STABLE_CHECK` | 穩定性檢查 | stable_release |
| `MANUAL_NOTE` | 手動備注 | manual |

---

## Edge Relation Types

| Relation | 說明 |
|----------|------|
| `SUPPORTS` | A 支持 B |
| `CONTRADICTS` | A 與 B 衝突（保守偵測） |
| `DUPLICATES` | A 與 B 重複 |
| `REFINES` | A 精煉 B |
| `REQUIRES_DATA` | A 需要 B 提供的資料 |
| `REQUIRES_BACKTEST` | A 需要回測驗證 |
| `REQUIRES_REPLAY` | A 需要復盤練習 |
| `REQUIRES_JOURNAL_REVIEW` | A 需要日誌回顧 |
| `GENERATED_FROM` | A 由 B 生成 |
| `VALIDATED_BY` | A 由 B 驗證 |
| `WEAKENED_BY` | A 被 B 削弱 |
| `RELATED_TO` | A 與 B 相關（同 symbol/strategy） |

---

## Evidence Threads

Evidence Thread 是從 anchor node（通常是 RESEARCH_RECOMMENDATION 或 STRATEGY_HYPOTHESIS）出發，
透過 BFS 最多 3 層找到的所有相關 nodes，形成一條證據鏈。

每條 thread 有：
- `anchor_title` — 起點 node 標題
- `key_nodes` — 主要 node IDs
- `evidence_path` — node 類型路徑
- `suggested_next_step` — 建議下一步（安全研究指令）

---

## Orphan Nodes

沒有任何 edge 的 node 稱為 orphan node。Orphan node 代表：
- 來源模組尚未跑過
- 或此 node 與其他節點缺乏明確關聯

建議：先跑更多 Research OS 模組，再執行 `evidence-graph`。

---

## Contradictions

CONTRADICTS edge 採保守偵測：只有 title 字詞高度重疊 AND 情緒關鍵字相反時才建立。
不要把 Evidence Graph contradiction 當成交易訊號。

---

## Requires Data / Backtest / Replay

| 狀態 | 說明 | 建議指令 |
|------|------|---------|
| `REQUIRES_DATA` | 需要補充資料 | `FIX_DATA` |
| `REQUIRES_BACKTEST` | 需要回測驗證 | `BACKTEST_MORE` |
| `REQUIRES_REPLAY` | 需要復盤練習 | `PRACTICE_REPLAY` |

---

## CLI Usage

```bash
# 完整跑 evidence graph pipeline
python main.py evidence-graph --mode real

# 看 summary
python main.py evidence-graph-summary

# 看 nodes
python main.py evidence-graph-nodes
python main.py evidence-graph-nodes --node-type RESEARCH_RECOMMENDATION
python main.py evidence-graph-nodes --source-module strategy_memory
python main.py evidence-graph-nodes --keyword "momentum"

# 看 edges
python main.py evidence-graph-edges

# 看 evidence threads
python main.py evidence-graph-threads

# 看 orphan nodes
python main.py evidence-graph-orphans

# 看 requires backtest
python main.py evidence-graph-requires-backtest

# 看 requires data
python main.py evidence-graph-requires-data

# 產生 Markdown 報告
python main.py evidence-graph-report --mode real
```

---

## GUI Usage

1. 啟動 GUI：`python main.py cockpit`
2. 找到 **Evidence Graph** tab
3. 點 **Build Graph** 執行 pipeline
4. 查看 Summary Cards、Node Table、Edge Table、Evidence Thread Table
5. 使用 Filters 篩選 node_type / source_module / keyword
6. 點選 node 查看 Detail Panel（neighbors、evidence text）
7. 點 **Copy Suggested Next Step** 複製安全研究指令

---

## Report Usage

報告儲存於 `reports/evidence_graph_report_YYYY-MM-DD.md`

章節包含：
1. 總覽（nodes/edges/orphans/contradictions/overall status）
2. Top Evidence Threads
3. Research Recommendation Evidence
4. Strategy Memory Evidence
5. Backtest Coach Evidence
6. Training Metrics Evidence
7. Data / Report / Regression Evidence
8. Graph Gaps（orphans / requires data/backtest/replay）
9. Safety Declaration

---

## Safety / No Real Orders

- **Production Trading BLOCKED** — 絕不下單
- **No Real Orders** — 不接 broker
- **No Auto Trading** — 不自動交易
- **Research Only** — 僅供研究
- **Not Investment Advice** — 不構成投資建議
- 所有 node/edge action 欄位禁止 BUY / SELL / ORDER / EXECUTE / SUBMIT_ORDER / AUTO_TRADE / REAL_TRADE
- 不自動修改 memory status、coach task status、rule weight、strategy enabled

---

## 不會自動下單

Evidence Graph 是純研究工具。
無論 Evidence Graph 的結論是什麼，都不會觸發任何交易行為。
所有輸出的 suggested_next_step 都只是研究建議（REVIEW / VALIDATE / BACKTEST_MORE 等）。

## 不會自動啟用策略

Evidence Graph 的結論不會自動修改任何模組狀態：
- 不修改 strategy_memory status
- 不修改 backtest_coach task status
- 不修改 rule_governance weight
- 不修改任何 enabled 旗標

---

## v0.9.1 Evidence Graph UX Overview

v0.9.1 adds a full UX layer on top of the Evidence Graph engine:

- **Evidence Thread Quality Board** — score each thread as STRONG / PARTIAL / NEEDS_DATA / NEEDS_BACKTEST / CONFLICTED / ORPHANED
- **Crash Reversal Evidence Chain** — 6-stage visual chain view
- **Graph Gap View** — detect and classify orphans, missing data, contradictions
- **Evidence Path Explanations** — explain any node or thread in plain language
- **7 new CLI commands** for interactive research use

---

## Evidence Thread Quality Board

Each evidence thread receives a quality label based on its nodes and edges:

| Quality Label   | Meaning                                                        |
|-----------------|----------------------------------------------------------------|
| STRONG          | Anchor node has ≥2 supporting nodes, no contradictions         |
| PARTIAL         | Has some support but missing data or backtest                  |
| NEEDS_DATA      | Anchor has REQUIRES_DATA edges with no resolution              |
| NEEDS_BACKTEST  | Anchor has REQUIRES_BACKTEST edges with no backtest result     |
| CONFLICTED      | Thread has active contradiction edges                          |
| ORPHANED        | Anchor node has no edges at all                                |

CLI: `python main.py evidence-graph-thread-quality`

---

## Crash Reversal Evidence Chain

6-stage evidence chain for crash reversal strategies:

1. **Crash Cause** — classify the crash type (macro shock / sector rotation / earnings miss / technical failure)
2. **Stabilization** — post-crash stabilization checklist (volume contraction, range narrowing, support hold)
3. **Relative Strength** — which stocks outperformed during the crash (relative strength score)
4. **EPS Dip Filter** — EPS-backed dip buy filter (Sakata method, 低接 discipline)
5. **MA Discipline** — moving average profit discipline (月線 / 季線 stops)
6. **Risk Guard** — high-risk industry exposure guard (avoid 轉空頭 sectors)

CLI: `python main.py evidence-graph-crash-reversal`

---

## Graph Gap View

Gap types detected by the Evidence Graph UX:

| Gap Type          | Description                                          |
|-------------------|------------------------------------------------------|
| ORPHAN_NODE       | Node has no edges — isolated research conclusion     |
| MISSING_DATA      | REQUIRES_DATA edge with no data node attached        |
| MISSING_BACKTEST  | REQUIRES_BACKTEST edge with no result node           |
| CONTRADICTION     | Two nodes with mutually contradicting evidence       |
| STALE_THREAD      | Thread anchor is >30 days old with no new evidence   |

CLI: `python main.py evidence-graph-gaps`

---

## Evidence Path Explanations

Every node and thread can be explained:

- **explain-node** — show node type, source module, evidence summary, connected edges, suggested next step
- **explain-thread** — show thread title, quality label, evidence path, all nodes, gaps, next step

CLI:
```bash
python main.py evidence-graph-explain-node --node-id <node_id>
python main.py evidence-graph-explain-thread --thread-id <thread_id>
```

---

## New CLI Commands (v0.9.1)

| Command                              | Description                                              |
|--------------------------------------|----------------------------------------------------------|
| `evidence-graph-ux`                  | Full Evidence Graph UX pipeline (threads + gaps)         |
| `evidence-graph-thread-quality`      | Thread quality board (STRONG/PARTIAL/NEEDS_DATA/…)       |
| `evidence-graph-gaps`                | Graph gap view (orphans, missing data, contradictions)   |
| `evidence-graph-crash-reversal`      | Crash reversal evidence chain (6 stages)                 |
| `evidence-graph-explain-node`        | Explain a specific evidence node                         |
| `evidence-graph-explain-thread`      | Explain a specific evidence thread                       |
| `evidence-graph-search`              | Search threads and gaps by keyword/quality/gap type      |

All commands: Research Only | No Real Orders | No BUY/SELL/ORDER output.

---

## GUI UX Tab (v0.9.1)

The Evidence Graph GUI tab provides 6 sub-views:

1. **Graph Overview** — node/edge counts, thread summary, gap summary
2. **Thread Quality Board** — sortable table with quality labels and next steps
3. **Crash Reversal Chain** — 6-stage evidence chain visualization
4. **Gap View** — gap type breakdown with severity and suggested fixes
5. **Node Explorer** — search and explain individual evidence nodes
6. **Thread Explorer** — drill into any thread with full evidence path

---

## Safety Declarations

- `read_only = True` — Evidence Graph UX does not write to any module
- `no_real_orders = True` — No trading commands ever produced
- `production_blocked = True` — Production trading permanently blocked
- No BUY / SELL / ORDER in any output
- Suggested next steps: REVIEW / VALIDATE / BACKTEST_MORE / PRACTICE_REPLAY / FIX_DATA / READ_REPORT / WAIT only
