# TW Quant Cockpit — Maintenance v1.0.1

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] VALIDATED does not enable trading. Broker Execution Disabled.**
> **[!] Not Investment Advice.**

---

## v1.0.1 — Maintenance & Polish

**Base Release:** v1.0.0 Research Trading Cockpit Stable

**Stage:** STABLE

**Type:** Maintenance / Polish release — no new features, no broker API, no live trading.

---

## Overview

v1.0.1 is a maintenance and polish release based on v1.0.0 Research Trading Cockpit Stable.

| Safety Flag | Value |
|-------------|-------|
| Research Only | True |
| No Real Orders | True |
| Production Trading BLOCKED | True |
| Broker Execution | Disabled |
| VALIDATED does not enable trading | True |
| Paper Trading | Simulation Only |
| Mock Realtime | Simulation Only |
| Broker API | Not connected |
| Auto Trading | Not enabled |
| Auto Placement | Not enabled |

---

## What Changed in v1.0.1

- Version info updated: VERSION = "1.0.1", BASE_RELEASE = "1.0.0"
- CLI `version-info` now shows Base Release line
- Stable checklist accepts v1.0.x maintenance releases
- Added v1.0.1 checks to stable_release_checklist_v060 and intelligence_stable_checklist
- GUI navigation keywords updated: maintenance, polish, v1.0.1, 維護版
- Regression suite: added gui-nav-search keyword tests
- Docs: maintenance_v1.0.1.md (this file), release_notes_v1.0.md updated

## What Did NOT Change

- No broker API connected
- No live trading enabled
- No real order execution
- No strategy auto-enable
- No auto weight modification
- All v1.0.0 modules preserved
- All v0.9.x modules preserved
- paper trading remains simulation only
- mock realtime remains simulation only

---

## Known Warnings (Inherited from v1.0.0)

| Warning | Severity | Notes |
|---------|----------|-------|
| cp950 subprocess encoding (Windows) | Low | Non-critical, cosmetic |
| paper smoke test WARN if no state file | Low | Non-critical |
| no_real_orders flag pre-existing check BLOCKED | Low | Advisory only — whitelist check |
| Optional report_pack ENV_LIMITED | Low | Non-critical |

---

## CLI Smoke Test

```bash
python main.py version-info
python main.py research-cockpit-stable --mode real
python main.py research-cockpit-stable-checks
python main.py strategy-lab-dashboard --mode real
python main.py strategy-validation-summary
python main.py evidence-graph-ux --mode real
python main.py crash-reversal-summary
python main.py mock-realtime --duration 10
python main.py paper
python main.py stable-v060-check --mode real
python main.py regression-run --suite release_gate --mode real
```

Expected:
- version-info: VERSION=1.0.1, Base Release: 1.0.0
- research-cockpit-stable: 25/25 PASS
- All modules functional
- No forbidden trading action outputs (research-only actions only)
- mock-realtime: simulation only
- paper: simulation only

---

## GUI Smoke Test

```bash
python main.py cockpit
```

Expected visible:
- Version Info card: v1.0.1 Maintenance & Polish / Base Release v1.0.0
- Safety banner: Research Only / No Real Orders / Production Trading BLOCKED / Broker Execution Disabled
- Strategy Lab Dashboard tab
- Strategy Validation tab
- Evidence Graph tab
- Crash Reversal tab
- Strategy Memory tab
- Backtest Coach tab
- Training Metrics tab
- Research Intelligence tab

Not visible:
- No trading action buttons (research-only UI)
- No broker connect button
- No live trading button
- No real order execution button

---

## Release Checklist

| Check | Expected |
|-------|----------|
| version-info displays 1.0.1 | PASS |
| research-cockpit-stable 25/25 PASS | PASS |
| stable-v060-check no FAIL | PASS |
| release_gate regression no FAIL | PASS |
| No forbidden actions | PASS |
| No Real Orders intact | PASS |
| Broker Execution Disabled | PASS |
| VALIDATED does not enable trading | PASS |
| mock-realtime simulation | PASS |
| paper simulation | PASS |

---

## Safety Declaration

- **Research Only** — All outputs are for research and learning purposes only.
- **No Real Orders** — This system does not and cannot place real trading orders.
- **Production Trading BLOCKED** — Production trading is permanently blocked.
- **Broker Execution Disabled** — There is no connection to any broker API.
- **VALIDATED does not enable trading** — VALIDATED grade is research-validated only.
- **Paper trading is simulation only** — Paper trades are simulated, not real.
- **Mock realtime is simulation only** — Mock realtime is not live market data.
- **Not Investment Advice** — Nothing in this system constitutes investment advice.

---

*TW Quant Cockpit v1.0.1 — Maintenance & Polish — Research Only — Not Investment Advice*
