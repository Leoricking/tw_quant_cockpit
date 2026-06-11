# TW Quant Cockpit Handoff Guide v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Project Location

```
C:/Users/Rossi/Documents/Claude/trading_master
```

Current version: **v1.0.5 — Documentation & User Guide Polish**
Base version: **v1.0.0 — Research Trading Cockpit Stable**
Git user: Leoricking
Main branch: main

---

## Safety Constraints

| Constraint | Rule |
|------------|------|
| No real trading | This system is research-only. No broker API. No live orders. |
| No broker execution | BROKER_EXECUTION_ENABLED = False always |
| No auto trading | Production trading is explicitly blocked |
| VALIDATED grade | Research only — does not enable trading |
| Paper trading | Simulation only — not real orders |
| Mock realtime | Simulation only — not live data |

---

## Critical Development Rules

### 1. git -C Rule

Always use `git -C "path" command` format. Never use `cd path` then git.

Correct:
```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" status
git -C "C:/Users/Rossi/Documents/Claude/trading_master" log --oneline -5
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add release/version_info.py
```

Incorrect (do not use):
```
cd C:/Users/Rossi/Documents/Claude/trading_master
git status
```

### 2. No git add .

Always add files individually by name:

Correct:
```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add release/version_info.py
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add documentation/__init__.py
```

Incorrect (do not use):
```
git -C "..." add .
```

### 3. No Runtime Output Commits

Do NOT commit:
- `.csv` files (backtest results, manifests)
- `.json` files (state files, experiment outputs)
- `.md` report files (generated reports in reports/)
- `.db` files (SQLite databases)

These are all gitignored. Only commit source code, documentation, and configuration.

### 4. No Chain Commands

Do NOT use `&&`, `;`, `||`, or `|` to chain commands. Run each command separately.

Correct:
```
python main.py version-info
python main.py research-cockpit-stable --mode real
```

Incorrect (do not use — chain command operators are forbidden):
Run commands one at a time. Never join two commands with chain operators.

### 5. No Heredoc in Git Commit

Do NOT use heredoc (`<<EOF`) in git commit messages. Use multiple `-m` flags instead:

Correct:
```
git -C "..." commit -m "docs: update user guide v1.0.5" -m "Add user guide and safety guide."
```

Incorrect (do not use):
```
git -C "..." commit -m "$(cat <<EOF
message
EOF
)"
```

---

## Key CLI Smoke Tests

Run these before any release to verify the system is working:

```
python main.py version-info
python main.py research-cockpit-stable --mode real
python main.py stable-v060-check --mode real
python main.py safety-scan --target all
python main.py release-gate-health --mode real
python main.py regression-run --suite release_gate --mode real
python main.py mock-realtime --duration 10
python main.py paper
```

---

## Release Process Steps

1. Read the current `release/version_info.py`
2. Update VERSION and RELEASE_NAME
3. Add any new feature flags (e.g., DOCUMENTATION_POLISH_RELEASE = True)
4. Create new modules/files as needed
5. Update checklists (research_cockpit_stable_checklist, stable_release_checklist_v060, intelligence_stable_checklist)
6. Update regression suite (suite_registry.py)
7. Update report pack (report_registry.py, report_collector.py)
8. Update GUI navigation (tab_registry.py) with new keywords
9. Update .gitignore for new runtime outputs
10. Update docs/index.md, docs/roadmap.md, docs/release_notes_v1.0.md
11. Update README.md
12. Validate imports: `python -c "from release.version_info import VERSION; print(VERSION)"`
13. Run all smoke tests
14. Run regression suite
15. Run safety scan
16. Commit with individual file adds and multiple -m flags
17. Tag with `git -C "..." tag -a vX.X.X -m "vX.X.X: Release Name"`
18. Push: `git -C "..." push origin main`
19. Push tag: `git -C "..." push origin vX.X.X`
20. Verify: `git -C "..." log --oneline --decorate -5`

---

## How to Create Next Version Prompt

For each new version:
1. State the current state (VERSION, commit hash, test results)
2. List all files to create/modify with their full content or change description
3. List all validation commands to run
4. List the exact git commands for commit and tag
5. Specify safety constraints that must be maintained
6. List known WARNs that are acceptable

---

## Known Warnings (Acceptable)

| Warning | Classification |
|---------|---------------|
| cp950 encoding warning | KNOWN_CP950_WARNING — non-critical |
| paper_state.json missing | KNOWN_PAPER_SMOKE_WARNING — non-critical |
| ENV_LIMITED report status | KNOWN_REPORT_PACK_OPTIONAL — non-critical |
| no_real_orders flag check WARN | KNOWN_NO_REAL_ORDERS_FLAG_CHECK — known |

---

## What NOT To Do

- Do NOT add broker API integration
- Do NOT enable real order execution
- Do NOT add auto-trading logic
- Do NOT skip safety checks in releases
- Do NOT commit runtime outputs
- Do NOT use `git add .`
- Do NOT chain commands with `&&`
- Do NOT ignore BLOCKED status from safety scanner

---

*TW Quant Cockpit v1.0.5 — Documentation & User Guide Polish — Research Only — Not Investment Advice*
