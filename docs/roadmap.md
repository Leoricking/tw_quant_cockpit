# TW Quant Cockpit — Roadmap

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## Completed Milestones

| Version | Feature | Status |
|---------|---------|--------|
| v0.3.1–v0.3.8 | Core infrastructure, data pipeline, signal engine | Done |
| v0.3.9 | Public data API layer (TWSE public endpoints) | Done |
| v0.3.10 | Intraday OHLC fix, microstructure display fix | Done |
| v0.3.11 | Long-term strategy validation (multi-year backtest) | Done |
| v0.3.12 | Portfolio & risk simulation | Done |
| v0.3.13 | GUI Portfolio Cockpit tab | Done |
| v0.3.14 | Signal Quality Dashboard | Done |
| v0.3.15 | Rule Weight Tuning Lab | Done |
| v0.3.16 | Auto Report Center | Done |
| v0.3.17 | Automation Scheduler | Done |
| v0.3.18 | API Provider Hardening | Done |
| v0.3.19 | Data Provider Auto Fetch | Done |
| v0.3.20 | Data Quality Gate | Done |
| v0.3.21 | Daily Workflow Engine | Done |
| v0.3.22 | Usability QA & Error Message Polish | Done |
| v0.3.23 | Documentation & Release Notes Pack | Done |

---

## Planned: v0.3.24

**Target:** Data coverage expansion

- Additional XQ export column mappings
- Support for more ticker ranges in universe expansion
- Data freshness alerting (configurable staleness thresholds)
- Provider fallback chain (FinMind → TWSE public → cached)

---

## Planned: v0.3.25

**Target:** Report quality improvements

- HTML report option (alongside Markdown)
- Report diff: highlight changes from previous day
- Candidate stock detail section in daily summary
- Email/notification export (local only; no external services)

---

## Planned: v0.3.26

**Target:** Signal quality improvements

- Multi-period signal quality scoring (not just latest day)
- Signal stability metric (how consistent is the recommendation over N days)
- Rule dependency analysis (correlated rules detection)

---

## Planned: v0.4.0

**Target:** Architecture consolidation

- Unified data model (replace ad-hoc dict structures with dataclasses)
- Plugin architecture for custom rules
- Config file support (`config.yaml`) for provider tokens and thresholds
- Full test suite (pytest) with real data fixtures

**Safety constraints remain unchanged in v0.4.x:**
- PRODUCTION_BLOCKED=True
- REAL_ORDER_READY=False
- No broker connections

---

## Non-Goals (Permanent)

The following are explicitly out of scope for all future versions:

| Non-Goal | Reason |
|----------|--------|
| Real order execution | Research platform only |
| Broker API integration (Shioaji, Mega, etc.) | Out of scope |
| Investment advice generation | Not a registered advisor; legal constraint |
| Auto weight application | Manual review required; safety constraint |
| Cloud deployment | Local research tool |
| Multi-user access | Single-user research tool |

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
