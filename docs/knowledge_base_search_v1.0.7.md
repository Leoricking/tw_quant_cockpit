# Knowledge Base Search v1.0.7

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Search does not enable trading. Broker Execution Disabled.

## v1.0.7 目標

v1.0.7 Knowledge Base Search Polish 把累積的文件、範例、模板、報告、Strategy Memory、Evidence Graph 變成可搜尋、可導覽、可複用的研究知識庫入口。

## Knowledge Base Index

掃描範圍：
- README.md
- docs/ (所有 .md 文件)
- docs/examples/ (範例文件)
- docs/templates/ (模板文件)
- reports/ (報告建構器)
- gui/navigation/tab_registry.py (GUI 分頁註冊表)
- Strategy Memory metadata (若存在)
- Evidence Graph metadata (若存在)

## Search scope

- DOC：文件
- EXAMPLE：範例
- TEMPLATE：模板
- REPORT：報告
- STRATEGY_MEMORY：策略記憶
- EVIDENCE_GRAPH：證據圖
- REGRESSION：回歸測試
- GUI：GUI 分頁
- DATA_HYGIENE：資料清理
- WORKFLOW：工作流程
- SAFETY：安全文件
- RELEASE：發布文件

## Search CLI

```
python main.py kb-index
python main.py kb-summary
python main.py kb-health-check
python main.py kb-search --query "strategy validation"
python main.py kb-search --query "crash reversal" --limit 10
python main.py kb-search --query "release gate" --category DOC
python main.py kb-search --query "data hygiene" --module maintenance
python main.py kb-explain --item-id <item_id>
python main.py kb-report --mode real
```

## Search GUI

Knowledge Base Search Panel (gui/knowledge_base_search_panel.py) 提供：
- Safety Banner
- 搜尋欄位（query / category filter / module filter / limit）
- 結果表格（Title / Category / Module / Score / Path / Safe Next Step）
- 詳細資訊面板（excerpt / reason / safe next step / no real orders note）
- 操作按鈕（Build Index / Search / Refresh / Copy Safe Summary / Copy File Path）

## How scoring works

| Match Type | Score |
|------------|-------|
| Title exact | 100 |
| Title partial | 60 |
| Tag match | 40 |
| Keyword match | 30 |
| Module match | 25 |
| Path match | 20 |
| Content match | 15 |

Simple local lightweight scoring. No external vector DB. No embedding API. No network.

## Safe summary

Safe next steps (allowed):
- REVIEW
- READ_REPORT
- KEEP_OBSERVING
- MARK_RESEARCH_ONLY
- PAPER_ONLY
- MOCK_ONLY
- WAIT
- BACKTEST_MORE
- PRACTICE_REPLAY
- REVIEW_JOURNAL
- REVIEW_RISK
- REVIEW_EARNINGS
- REVIEW_CHIPS
- DO_NOT_CHASE
- FIX_DATA
- REVIEW_JOURNAL

Forbidden (never output): BUY / SELL / ORDER / EXECUTE / SUBMIT_ORDER / AUTO_TRADE / REAL_TRADE / LIVE_TRADE / BROKER_ORDER

## No external API

- No OpenAI API
- No embedding API
- No external services
- No network connection
- No FAISS
- No Chroma
- Local lightweight search only

## No Real Orders

- Search does not enable trading
- Broker Execution Disabled
- VALIDATED does not enable trading
- Production Trading BLOCKED
- Not Investment Advice

## Examples

```bash
# 搜尋策略驗證相關文件
python main.py kb-search --query "strategy validation"

# 搜尋崩盤反彈相關文件
python main.py kb-search --query "crash reversal"

# 搜尋資料清理相關文件
python main.py kb-search --query "data hygiene"

# 搜尋交接相關文件
python main.py kb-search --query "handoff"

# 搜尋發布閘門相關文件
python main.py kb-search --query "release gate"

# 建立索引
python main.py kb-index

# 查看知識庫健康狀態
python main.py kb-health-check

# 產生知識庫搜尋報告
python main.py kb-report --mode real
```

---

**Note (v1.0.9):** v1.0.7 is included in the v1.0.9 Final Maintenance Rollup. See `docs/final_maintenance_rollup_v1.0.9.md`.

*TW Quant Cockpit v1.0.7 — Knowledge Base Search Polish — Research Only — Not Investment Advice*
