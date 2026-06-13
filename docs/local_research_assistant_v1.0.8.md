# Local Research Assistant v1.0.8 User Guide

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] Not Investment Advice.
> [!] No external API. No broker execution.
> [!] Local assistant does not enable trading.

---

## v1.0.8 目標

Local Research Assistant Polish — synthesizes Knowledge Base Search results into safe, structured research answers with:

- Safe research summaries
- Module routing (which cockpit module to use next)
- Safe next steps (ALLOWED_ACTIONS only)
- Unsafe query blocking (BLOCKED_UNSAFE_QUERY for trading queries)

---

## What is the Local Research Assistant?

The Local Research Assistant is a **local-only**, **no-external-API** synthesis layer that:

1. Takes your research question
2. Searches the local Knowledge Base index
3. Routes you to the correct cockpit module
4. Suggests safe next steps (no trading actions)
5. Blocks unsafe queries (buy/sell/order etc.)

**It does not:**
- Place any orders
- Connect to any broker
- Call any external API (no OpenAI, no Anthropic, no embeddings)
- Use any network
- Enable real trading in any way

---

## Local Only / No External API

All processing is local:

```
Your Question
    → KnowledgeBaseSearchEngine (local index)
    → ResearchRouter (keyword matching)
    → SafeAnswerBuilder (rule-based)
    → ResearchAssistantAnswer (returned to you)
```

No LLM. No embedding API. No network. No broker.

---

## CLI Usage

### Ask a research question

```
python main.py local-assistant --ask "strategy validation"
python main.py local-assistant --ask "crash reversal"
python main.py local-assistant --ask "data hygiene"
python main.py local-assistant --ask "release gate warning"
python main.py local-assistant --ask "handoff guide"
```

### Filters

```
python main.py local-assistant --ask "validation" --category strategy_validation
python main.py local-assistant --ask "data" --module data_hygiene --limit 5
```

### Summary (sample questions batch)

```
python main.py local-assistant-summary
```

### Health check

```
python main.py local-assistant-health
```

### Generate report

```
python main.py local-assistant-report --mode real
```

### Explain an answer

```
python main.py local-assistant-explain --answer-id "strategy validation"
```

---

## How to Read Sources

Each answer includes sources from the local KB index:

| Field    | Meaning                              |
|----------|--------------------------------------|
| title    | Document title                       |
| path     | Local file path                      |
| category | Document category (e.g. strategy_validation) |
| module   | Cockpit module name                  |
| score    | Keyword match score (local, no embeddings) |

---

## How to Read Module Routes

Module routes tell you which cockpit module is most relevant:

| Field            | Meaning                              |
|------------------|--------------------------------------|
| module           | Module name (e.g. Strategy Validation) |
| reason           | Why this module was matched          |
| suggested_cli    | Safe CLI commands to run next        |
| suggested_gui_tab| GUI tab to open in the cockpit       |
| safe_action      | What to do (always from ALLOWED_ACTIONS) |

---

## How to Read Safe Next Steps

Safe next steps use only ALLOWED_ACTIONS:

| Action          | Meaning                              |
|-----------------|--------------------------------------|
| REVIEW          | Review the module or report          |
| READ_REPORT     | Read an existing research report     |
| BACKTEST_MORE   | Run more backtests                   |
| PRACTICE_REPLAY | Practice with replay sessions        |
| REVIEW_JOURNAL  | Review journal entries               |
| REVIEW_RISK     | Review risk parameters               |
| REVIEW_EARNINGS | Review earnings context              |
| REVIEW_CHIPS    | Review chip distribution             |
| DO_NOT_CHASE    | Do not chase a move                  |
| KEEP_OBSERVING  | Continue observing                   |
| FIX_DATA        | Fix or clean data                    |
| WAIT            | Wait for clearer signals             |

**None of these actions enable real trading.**

---

## How Unsafe Queries are Blocked

Queries containing these patterns are blocked with `BLOCKED_UNSAFE_QUERY`:

- buy, sell, order, purchase, place an order, submit order
- execute, trade now, should i buy, should i sell
- enter position, open position, auto trade, live trade, real trade
- broker order
- 下單, 買進, 賣出, 買入, 進場, 出場

Example blocked response:
```
[BLOCKED] This query contains patterns that suggest a trading action.
[!] Local Research Assistant is for RESEARCH ONLY.
[!] No Real Orders. Broker Execution Disabled.
Safe alternatives are listed below.
```

---

## Limitations

- Local KB search only — results depend on indexed local files
- No external LLM — answers are rule-based, not AI-generated
- No investment advice — never interpret answers as trading recommendations
- No real orders — this system cannot and does not place orders
- Answers reflect locally indexed documents, not live market data
- Confidence is based on document count, not semantic quality

---

## No Real Orders — Not Investment Advice

> [!] This system is for RESEARCH ONLY.
> [!] No Real Orders. Broker Execution Disabled.
> [!] VALIDATED does not enable trading.
> [!] Not Investment Advice. Do not make financial decisions based on these outputs.
> [!] Local assistant does not enable trading.

---

*TW Quant Cockpit v1.0.8 — Local Research Assistant Polish — superseded by v1.0.9 Final Maintenance Rollup*

**Note (v1.0.9):** v1.0.8 is included in the v1.0.9 Final Maintenance Rollup. See `docs/final_maintenance_rollup_v1.0.9.md` for the complete v1.0.x maintenance history and long-term SOP.
