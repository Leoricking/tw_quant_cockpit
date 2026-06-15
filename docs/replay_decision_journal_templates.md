# Replay Decision Journal Templates v1.2.2

> **[!] Research Only. No Real Orders. Simulation Decision Only.**

## Overview

Journal templates provide pre-filled starting points for common decision scenarios.
Templates are stored in `replay/journal_templates/*.json`.

All templates have `simulation_only: true`.

## Available Templates

| Template Name | Setup Type | Description |
|---------------|------------|-------------|
| `free_form` | FREE_FORM | Open-ended journal with no pre-set structure |
| `breakout` | BREAKOUT | Price breakout above resistance with volume |
| `pullback` | PULLBACK | Pullback to moving average or support in uptrend |
| `bottom_reversal` | BOTTOM_REVERSAL | Potential trend reversal from oversold conditions |
| `no_chase` | NO_CHASE | Decision to wait rather than chase a move |
| `risk_reduction` | RISK_REDUCTION | Reducing position size or tightening stop |
| `exit_review` | EXIT_REVIEW | Reviewing exit decision in hindsight (process only, no PnL) |
| `wait_confirmation` | WAIT_CONFIRMATION | Waiting for additional confirmation before acting |

## Template File Format

```json
{
  "template_name": "breakout",
  "setup_type": "BREAKOUT",
  "simulation_only": true,
  "checklist_items": [
    {"item_id": "BKO-001", "category": "SETUP", "label": "Price above resistance", "required": true},
    {"item_id": "BKO-002", "category": "SETUP", "label": "Volume confirming breakout", "required": true}
  ],
  "default_fields": {
    "time_horizon": "INTRADAY",
    "action": "BUY"
  }
}
```

## Using Templates

```python
from replay.decision_templates import DecisionTemplateLibrary

lib = DecisionTemplateLibrary(repo_root="/path/to/repo")
templates = lib.list_templates()
t = lib.load_template("breakout")
applied = lib.apply_template(t, symbol="AAPL", replay_date="2026-06-10")
```

## Adding Custom Templates

Place a JSON file in `replay/journal_templates/` following the format above.
Required fields: `template_name`, `setup_type`, `simulation_only: true`.

Custom templates are loaded automatically by `DecisionTemplateLibrary`.
