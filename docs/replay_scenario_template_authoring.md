# Replay Scenario Template Authoring Guide — v1.2.1

> [!] Research Only. No Real Orders. Templates NEVER contain future answers. Not Investment Advice.

## Overview

Scenario templates define structured training scenarios for replay sessions. They specify what type of market situation to look for, what the learner's objectives are, and what constraints apply.

Templates are stored in `data/replay_scenarios/` and loaded via `ReplayScenarioLibrary`. Builtin templates live in `replay/templates/*.json`.

## Template Schema

```json
{
  "scenario_id": "RSC-XXXXXXXX",
  "scenario_name": "Descriptive Name",
  "description": "What this scenario teaches",
  "category": "PULLBACK",
  "difficulty": "INTERMEDIATE",
  "objectives": ["Identify the pullback entry", "Record reason before entry"],
  "instructions": "Step-by-step instructions for the trainee",
  "rules": ["No chasing entries above previous close", "Set stop before entry"],
  "symbol_selector": "FREE",
  "symbols": [],
  "date_selector": "FREE",
  "start_date": null,
  "end_date": null,
  "duration_days": null,
  "initial_visible_history_days": 120,
  "required_datasets": ["price"],
  "optional_datasets": ["volume_profile", "chips"],
  "strict_future_firewall": true,
  "include_quality_gate": true,
  "include_strategy_knowledge": true,
  "include_chips": false,
  "include_fundamental": false,
  "default_playback_speed": 1,
  "allowed_actions": ["WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"],
  "tags": ["pullback", "trend"],
  "source": "user",
  "version": "1",
  "archived": false
}
```

## Field Reference

### Required Fields

| Field | Type | Notes |
|-------|------|-------|
| `scenario_id` | string | RSC- prefix; auto-generated if omitted |
| `scenario_name` | string | Human-readable name |
| `category` | string | See valid categories below |
| `difficulty` | string | BEGINNER / INTERMEDIATE / ADVANCED / EXPERT |
| `strict_future_firewall` | bool | Must be `true` — validation error if false |

### Categories

```
TREND_FOLLOWING, BREAKOUT, PULLBACK, BOTTOM_REVERSAL,
MOMENTUM, SECTOR_ROTATION, FUNDAMENTAL_TURNAROUND,
RISK_CONTROL, NO_CHASE, NO_PANIC_SELL, FREE_PRACTICE, CUSTOM
```

### Symbol Selectors

| Value | Meaning |
|-------|---------|
| `FREE` | Researcher picks any symbol at session creation |
| `FIXED` | Symbol is determined by the template (list in `symbols`) |
| `CATEGORY` | Symbol chosen from a predefined category |

### Date Selectors

| Value | Meaning |
|-------|---------|
| `FREE` | Researcher picks start/end at session creation |
| `FIXED` | Template specifies exact start_date / end_date |
| `RELATIVE` | duration_days sets a fixed window length |

## FORBIDDEN Fields

These fields MUST NOT appear in any template payload:

```
future_return, outcome, final_label, answer,
realized_pnl, broker, order_token, api_key, secret
```

The validator will reject any template containing these fields.

## Creating a Template

### CLI

```bash
python main.py replay-scenario-create \
  --name "My Pullback Study" \
  --category PULLBACK \
  --difficulty INTERMEDIATE \
  --description "Study pullback entries in trending stocks"
```

### JSON File (for builtin or import)

Create `replay/templates/my_scenario.json` with the schema above, then run:

```bash
python main.py replay-scenario-health
# Builtins are auto-loaded from replay/templates/
```

### Programmatic

```python
from replay.scenario_library import ReplayScenarioLibrary

lib = ReplayScenarioLibrary(repo_root=".")
template = lib.create_template(
    name="My Pullback Study",
    category="PULLBACK",
    difficulty="INTERMEDIATE",
    description="Study pullback entries",
    objectives=["Identify entry level", "Record reason"],
    strict_future_firewall=True,
)
print(template.scenario_id)
```

## Validating a Template

```bash
python main.py replay-scenario-validate --scenario-id RSC-XXXXXXXX
```

Validation checks:
- scenario_id present and RSC- prefix
- scenario_name present
- category in valid list
- difficulty in valid list
- strict_future_firewall = True (required)
- No forbidden fields in payload
- Date consistency (start_date < end_date when both specified)
- symbols list required when symbol_selector = FIXED
- allowed_actions must be subset of valid actions

## Archiving and Restoring

```bash
# Archive (blocks instantiation)
python main.py replay-scenario-archive --scenario-id RSC-XXXXXXXX

# Restore (allows instantiation again)
python main.py replay-scenario-restore --scenario-id RSC-XXXXXXXX
```

Archived templates are NOT deleted. They remain in the store and audit log.

## Exporting and Importing

```python
# Export
lib.export_template("RSC-XXXXXXXX", output_path="/tmp/my_scenario.json")

# Import (dry-run first)
result = lib.import_template("/tmp/my_scenario.json", dry_run=True)
print(result)

# Import for real
result = lib.import_template("/tmp/my_scenario.json", dry_run=False)
```

Imported templates are automatically validated before saving. Forbidden fields are stripped.

## Builtin Template IDs

| File | Scenario ID |
|------|-------------|
| `free_practice.json` | RSC-BUILTIN-FREE-PRACTICE-001 |
| `pullback_training.json` | RSC-BUILTIN-PULLBACK-001 |
| `breakout_training.json` | RSC-BUILTIN-BREAKOUT-001 |
| `bottom_reversal_training.json` | RSC-BUILTIN-BOTTOM-REVERSAL-001 |
| `no_chase_training.json` | RSC-BUILTIN-NO-CHASE-001 |
| `risk_control_training.json` | RSC-BUILTIN-RISK-CONTROL-001 |

## Safety Notes

- Templates are training aids only — NOT trading signals
- `research_only=True` and `no_real_orders=True` are enforced at runtime
- `strict_future_firewall=True` is required for all templates
- Scenarios do NOT contain realized outcomes, future prices, or trading recommendations
