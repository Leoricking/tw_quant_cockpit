# Notification Center — v0.4.5

> **[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] external_enabled = False. LINE / Telegram disabled (placeholder only).**

## Overview

The Notification Center records important research platform events as local, read-only
notifications. It does **not** send any external messages (LINE, Telegram, email) in v0.4.5.
All notifications are stored locally in `logs/notifications/notification_history.jsonl`
(gitignored) and can be reviewed via CLI or GUI.

## Architecture

```
notifications/
  __init__.py                       # package init
  notification_schema.py            # NotificationEvent dataclass, constants
  notification_center.py            # Main engine: JSONL persistence, list, mark-read
  notification_rules.py             # NotificationRuleEngine: 9 evaluate_* methods
  local_notifier.py                 # Console + optional win10toast
  external_notifier_placeholder.py  # Permanently disabled (LINE/Telegram placeholder)
  notification_preferences.py       # User preferences (local only)

gui/
  notification_center_adapter.py    # GUI bridge: all methods return dicts, never raise
  notification_center_panel.py      # PySide6 panel for Cockpit

reports/
  notification_center_report.py     # 8-section Markdown report generator

config/
  notification_preferences.example.json  # Safe example (committable)
  notification_preferences.json          # Runtime config (gitignored)
```

## Event Schema

Each `NotificationEvent` has:

| Field | Description |
|-------|-------------|
| `notification_id` | UUID-based ID: `NOTIF-<12 hex chars>` |
| `created_at` | ISO timestamp |
| `event_type` | One of 13 event types (see below) |
| `severity` | INFO / NOTICE / WARNING / ERROR / CRITICAL / BLOCKED |
| `category` | One of 11 categories (see below) |
| `title` | Short title |
| `message` | Full description |
| `status` | `unread` / `read` / `ignored` |
| `action_required` | Boolean |
| `next_steps` | List of suggested actions |
| `source` | Source module or command |
| `no_real_orders` | Always `True` |
| `production_blocked` | Always `True` |

### Event Types

| Type | Trigger |
|------|---------|
| `daily_report_ready` | Auto-report run completed |
| `data_quality_alert` | Data quality gate blockers/warnings |
| `provider_failure` | Provider fetch failure |
| `provider_recovery` | Provider recovered after failure |
| `signal_quality_alert` | Signal quality DISABLE/REDUCE |
| `ml_knowledge_leakage_alert` | ML leakage risk detected |
| `model_monitoring_alert` | Model drift / monitoring alert |
| `intraday_replay_reminder` | Intraday replay session overdue |
| `experiment_created` | New experiment registered |
| `rule_governance_review` | Rule governance review needed |
| `scheduler_task_result` | Scheduled task failure/warning |
| `system_health` | General system health |
| `safety_warning` | Safety invariant violated |

### Categories

`report` / `data` / `provider` / `signal` / `ml` / `replay` / `experiment` / `governance` / `scheduler` / `safety` / `system`

## Severity Levels

| Level | Meaning |
|-------|---------|
| INFO | Routine informational |
| NOTICE | Notable, elevated priority |
| WARNING | Review suggested |
| ERROR | Action recommended |
| CRITICAL | Immediate attention — safety or failure |
| BLOCKED | Production blocked (expected safe state) |

> **production_blocked = True is the expected SAFE state. It triggers INFO, not ERROR.**

## CLI Commands

```bash
# Evaluate notification rules (empty context — adds system health check)
python main.py notification-scan --mode real

# List recent notifications
python main.py notification-list
python main.py notification-list --limit 20 --severity WARNING
python main.py notification-list --category data --unread-only

# Add a test notification
python main.py notification-test --severity WARNING

# Generate Markdown report
python main.py notification-report --mode real
python main.py notification-report --dry-run

# Clear all read notifications
python main.py notification-clear-read
```

## Preferences

Copy `config/notification_preferences.example.json` to `config/notification_preferences.json`
and edit as needed. Do **not** commit `notification_preferences.json` (gitignored).

| Setting | Default | Description |
|---------|---------|-------------|
| `local_enabled` | `true` | Enable local console notifications |
| `external_enabled` | `false` | Always false in v0.4.5 |
| `min_severity` | `"INFO"` | Minimum severity to record |
| `categories_enabled` | all | Categories to record |
| `quiet_hours_enabled` | `false` | Suppress display during quiet hours |
| `quiet_hours_start` | `"22:00"` | Quiet hours start time |
| `quiet_hours_end` | `"08:00"` | Quiet hours end time |
| `daily_summary_enabled` | `true` | Enable daily summary event |
| `replay_reminder_enabled` | `true` | Enable intraday replay reminders |

## NotificationRuleEngine

The rule engine evaluates summaries from other platform components and generates events:

| Method | Input | Example Triggers |
|--------|-------|-----------------|
| `evaluate_safety(context)` | `real_order_ready`, `production_blocked`, etc. | CRITICAL if `real_order_ready=True` |
| `evaluate_data_quality(dq_summary)` | Data quality gate summary | WARNING/ERROR for blockers |
| `evaluate_provider_health(provider_summary)` | Provider health summary | ERROR on failure |
| `evaluate_signal_quality(signal_summary)` | Signal quality report | WARNING for DISABLE/REDUCE signals |
| `evaluate_ml_knowledge(ml_summary)` | ML knowledge integration summary | WARNING for leakage risk |
| `evaluate_model_monitoring(monitoring_summary)` | Model drift summary | WARNING for drift detected |
| `evaluate_intraday_replay(replay_summary)` | Replay session summary | NOTICE for overdue sessions |
| `evaluate_experiment_registry(experiment_summary)` | Experiment registry summary | INFO for new experiments |
| `evaluate_scheduler_result(task_result)` | Scheduler task result | WARNING for task failures |

## Output Files

All output files are gitignored:

| File | Description |
|------|-------------|
| `logs/notifications/notification_history.jsonl` | Full event log (JSONL, append-only) |
| `data/backtest_results/notification_summary.csv` | CSV export via `export_history()` |
| `reports/notification_center_report_YYYYMMDD_HHMMSS.md` | Markdown reports |

## Safety Notes

- `no_real_orders = True` — all classes enforce this invariant
- `production_blocked = True` — expected safe state; triggers INFO not ERROR
- `external_enabled = False` — LINE/Telegram placeholder only, never sends messages
- Notification creation never raises — failures are logged as warnings
- Notification metadata never contains tokens, passwords, or API keys
- `config/notification_preferences.json` is gitignored (never committed)

---

_Notification Center v0.4.5 — Research Only. No Real Orders._
