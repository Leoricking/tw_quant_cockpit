# Governance Alerts & Daily Operations v1.1.7

**[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
**[!] External Notification Send DISABLED. No broker. No trading.**
**[!] Alert detection does NOT repair, import, override gates, or enable trading.**

---

## Overview

v1.1.7 introduces the Governance Alerts & Daily Operations subsystem. It provides deterministic alert detection, deduplication, lifecycle management, snooze and escalation, morning and end-of-day digests, daily checklists, safe notification previews, and a full GUI panel and CLI for governance alert operations.

---

## Modules

| Module | Class | Description |
|--------|-------|-------------|
| `governance_alerts/alert_schema.py` | GovernanceAlert, AlertStateTransition, GovernanceDigest, DailyChecklistItem, DailyOperationsChecklist | Core dataclasses |
| `governance_alerts/alert_policy.py` | GovernanceAlertPolicy | Priority, severity, suppression, snooze limits, command allowlist |
| `governance_alerts/alert_sources.py` | 10 source classes | Read-only data sources for alert detection |
| `governance_alerts/alert_detector.py` | GovernanceAlertDetector | Detects alerts from all sources |
| `governance_alerts/alert_deduplicator.py` | GovernanceAlertDeduplicator | SHA-256 fingerprint, deterministic, P0 never lost |
| `governance_alerts/alert_lifecycle.py` | GovernanceAlertLifecycle | OPEN→ACK→SNOOZE→ESCALATE→RESOLVE→REOPEN transitions |
| `governance_alerts/escalation_engine.py` | GovernanceAlertEscalationEngine | L0→L1→L2→L3 escalation |
| `governance_alerts/digest_builder.py` | GovernanceDigestBuilder | MORNING/END_OF_DAY/DAILY/WEEKLY/MANUAL digests |
| `governance_alerts/daily_checklist.py` | GovernanceDailyChecklistBuilder | Daily operations checklist |
| `governance_alerts/notification_preview.py` | GovernanceNotificationPreview | Local-only preview, EXTERNAL_NOTIFICATION_SEND_ENABLED=False |
| `governance_alerts/alert_store.py` | GovernanceAlertStore | Append-only JSONL/CSV runtime outputs |
| `governance_alerts/alert_query.py` | Query functions | latest_alerts, alerts_by_priority, alert_history |
| `governance_alerts/alert_health.py` | GovernanceAlertsHealthCheck | 25 health checks (PASS/WARN/FAIL/BLOCKED) |
| `governance_alerts/daily_operations_engine.py` | GovernanceDailyOperationsEngine | Full daily operations flow |

---

## Alert Types

| Type | Priority | Severity |
|------|----------|----------|
| AUDIT_CHAIN_FAILURE | P0 | CRITICAL |
| FUTURE_DATE | P0 | CRITICAL |
| DATE_REGRESSION | P0 | CRITICAL |
| REPRODUCIBILITY_FAILURE | P0 | CRITICAL |
| SOURCE_INTERRUPTION | P0 | CRITICAL |
| IMPORT_CONFLICT | P0 | HIGH |
| INVALID_OHLC | P0 | HIGH |
| NEW_P0_ACTION | P1 | HIGH |
| FORMAL_ELIGIBILITY_DROP | P1 | HIGH |
| READY_SYMBOL_DROP | P1 | HIGH |
| MODULE_HEALTH_FAIL | P1 | HIGH |
| IMPORT_FAILURE | P1 | HIGH |
| FRESHNESS_SLA_BREACH | P1 | MEDIUM |
| NEW_P1_ACTION | P2 | MEDIUM |
| SOURCE_DEGRADED | P2 | MEDIUM |
| STALE_SYMBOL_INCREASE | P2 | MEDIUM |
| MISSING_SYMBOL_INCREASE | P2 | MEDIUM |
| BLOCKED_SYMBOL_INCREASE | P2 | MEDIUM |
| NON_QUALIFIED_RUN | P2 | MEDIUM |
| REPORT_QUALIFICATION_WARNING | P2 | MEDIUM |
| MODULE_HEALTH_DEGRADED | P3 | LOW |
| OVERRIDE_USED | P3 | LOW |
| ACTION_REOPENED | P3 | LOW |
| DAILY_DIGEST_INFO | P3 | INFO |

---

## CLI Commands

```
python main.py governance-alerts-health
python main.py governance-alerts-scan --tier research30
python main.py governance-alerts
python main.py governance-alert --alert-id <id>
python main.py governance-alert-history --alert-id <id>
python main.py governance-alert-ack --alert-id <id>
python main.py governance-alert-snooze --alert-id <id> --hours 24
python main.py governance-alert-resolve --alert-id <id> --note "resolved"
python main.py governance-alert-reopen --alert-id <id> --reason "recurred"
python main.py governance-alert-escalations
python main.py governance-digest --type morning
python main.py governance-digest --type daily
python main.py governance-checklist
python main.py governance-checklist-complete --item-id <id> --note "done"
python main.py governance-notification-preview --type daily --format markdown
python main.py governance-alert-trend
python main.py governance-alert-compare
python main.py governance-daily-operations --tier research30 --digest-type daily
python main.py governance-alerts-report --tier research30 --mode real
python main.py governance-alert-audit
python main.py governance-alert-audit-verify
```

---

## Safety Constraints

- `EXTERNAL_NOTIFICATION_SEND_ENABLED = False` — no LINE/Telegram/Slack/email/webhook
- `GOVERNANCE_AUTO_REPAIR_ENABLED = False` — alerts never trigger repair
- `GOVERNANCE_AUTO_DOWNLOAD_ENABLED = False` — no external data fetch
- `GOVERNANCE_AUTO_IMPORT_ENABLED = False` — no import execution
- `GOVERNANCE_GATE_OVERRIDE_ENABLED = False` — no gate override
- `GOVERNANCE_TRADE_EXECUTION_ENABLED = False` — no trading
- P0 alerts cannot be permanently suppressed
- FUTURE_DATE and AUDIT_CHAIN_FAILURE cannot be permanently suppressed
- Suggested commands: allowlist only (no broker, order, trade execution commands)
- Alert audit log: append-only, immutable_hash chain

---

## Runtime Outputs (not committed)

```
data/governance_alerts/alerts.jsonl
data/governance_alerts/alert_transitions.jsonl
data/governance_alerts/alert_index.csv
data/governance_alerts/open_alerts.csv
data/governance_alerts/escalations.csv
data/governance_alerts/digests.jsonl
data/governance_alerts/daily_checklists.jsonl
data/governance_alerts/daily_metrics.csv
data/governance_alerts/notification_previews/
data/governance_alerts/alert_state.json
reports/governance_alerts_daily_operations_report_YYYY-MM-DD.md
```

---

## Test Fixtures

`tests/fixtures/governance_alerts/` contains 16 fixture files for testing alert detection, dedup, lifecycle, snooze, escalation, audit chain validation, notification redaction, and command allowlist checks.

---

*[!] Not Investment Advice. Research Only.*
