# TW Quant Cockpit — Stable UX Polish v0.6.1

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

---

## Overview

v0.6.1 is a targeted UX polish release. No new trading features. No trading functionality changes.
All outputs remain research-only.

**Goals:**
- Add `--type` CLI alias for `--pack-type` in `report-pack` / `report-pack-items`
- Add `--mode` parameter (no-op) to `report-pack` with friendly message
- Introduce smarter report status classification: `ENV_LIMITED` / `NOT_GENERATED`
- Ensure optional missing and provider-limited reports do not count as release failures
- Align GUI display, docs, and stable release checklist

---

## CLI Alias Policy

### `--type` / `--pack-type` Alias

Both `--type` and `--pack-type` are accepted interchangeably:

```bash
# These are equivalent:
python main.py report-pack --pack-type full
python main.py report-pack --type full

python main.py report-pack-items --pack-type full
python main.py report-pack-items --type full
```

### `--mode` Parameter (no-op)

`report-pack` accepts `--mode` but treats it as a no-op (the pack is always read-only):

```bash
python main.py report-pack --type full --mode real
# Prints: "Read-only report pack mode accepted: real"
```

---

## Status Interpretation Guide

| Status | Meaning | Release Impact |
|--------|---------|---------------|
| `READY` | Report file found and non-empty | Good |
| `MISSING` | Required report not found | Failure — run auto-report |
| `ENV_LIMITED` | Report requires provider API token | Warning only — not a release failure |
| `NOT_GENERATED` | Optional report not yet generated | Info only — not a release failure |
| `MISSING_OPTIONAL` | Optional report missing | Info only — not a release failure |
| `MISSING_REQUIRED` | Required report missing | Failure |
| `FAILED` | Report generation error | Failure — investigate |
| `PARTIAL` | Pack has mix of READY + non-READY | See stable release pass criteria |

---

## Optional Missing Behavior

Optional report types do NOT cause release failure when missing:

```python
OPTIONAL_REPORT_TYPES = {
    "experiment",
    "intraday_replay",
    "rule_governance",
    "replay_training",
    "stable_release_v060_report",
    "release_manifest",
}
```

When a report in this set has no output files, its status is set to `NOT_GENERATED`
(not `MISSING`). This is purely informational.

---

## ENV_LIMITED Explanation

The `provider` report type requires a provider API token set via environment variable.
When the token is absent, the collector sets the status to `ENV_LIMITED`:

```python
ENV_LIMITED_REPORT_TYPES = {
    "provider",
}
```

`ENV_LIMITED` is a warning — it does NOT count as a required missing or a release failure.

To enable the provider report, set the appropriate API token environment variable:
```bash
set TWSE_API_TOKEN=your_token_here   # Windows
export TWSE_API_TOKEN=your_token_here  # Linux/macOS
```

---

## Stable Release Pass Criteria

A stable release **passes** report pack checks when **all** of the following are true:

1. `failed_count == 0` — no report generation errors
2. `required_missing_count == 0` — no `STATUS_MISSING` on required report types

**Required report types** (absence = failure):
- `daily_market`
- `auto_report`
- `data_quality`
- `signal_quality`

**Non-failure statuses** (PARTIAL pack is acceptable):
- All items are `ENV_LIMITED` or `NOT_GENERATED`
- Pack status may be `PARTIAL` — this is OK if criteria above are met

---

## Health Checker Behavior

The `ReportHealthChecker` uses the following logic:

```
if failed == 0 and required_missing == 0:
    health_label = "HEALTHY"
else:
    health_label = score-based (HEALTHY / DEGRADED / CRITICAL)
```

Score thresholds:
- `>= 80%` → HEALTHY
- `50–79%` → DEGRADED
- `< 50%` → CRITICAL

The score is `ready_count / total * 100`. ENV_LIMITED and NOT_GENERATED items are NOT
counted as ready — but they do NOT trigger CRITICAL if required_missing == 0.

---

## Windows Terminal Notes

- Commands are run from `D:/code/Claude/tw_quant_cockpit` as the working directory
- No compound shell operators (`&&`, `;`, `||`, `|`) — run each command separately
- Use forward slashes in Python paths; use `"D:/..."` format
- Git commands: `git -C "D:/code/Claude/tw_quant_cockpit" <subcommand>`
- UTF-8 Chinese characters in GUI labels (`環境限制`, `尚未產生`) render correctly in PySide6

---

## GUI Status Display

In `gui/report_pack_panel.py`:

| Raw Status | Display Label | Color |
|------------|--------------|-------|
| `READY` | `READY` | Dark green |
| `MISSING` / `FAILED` / `MISSING_REQUIRED` | status text | Red |
| `ENV_LIMITED` | `環境限制 (需設定 token)` | Dark yellow |
| `NOT_GENERATED` / `MISSING_OPTIONAL` | `尚未產生 (optional)` | Dark yellow |

Empty state hint:
```
執行: python main.py auto-report --mode real --profile daily
```

---

## Safety

All outputs: Research Only / No Real Orders / Production BLOCKED

| Flag | Value |
|------|-------|
| `research_only` | True |
| `no_real_orders` | True |
| `production_blocked` | True |
| `real_order_ready` | False |
| `broker_api` | NOT CONNECTED |

---

*TW Quant Cockpit v0.6.1 — Research Only / No Real Orders / Production Trading BLOCKED*
