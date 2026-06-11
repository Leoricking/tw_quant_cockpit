# TW Quant Cockpit CLI Cookbook v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

All commands run from the project root directory.
Use `git -C "path" command` for git operations — do not chain commands.

---

## A. System Information

| Command | Purpose | Output |
|---------|---------|--------|
| `python main.py version-info` | Show version and safety flags | Version, release name, safety flags |
| `python main.py research-cockpit-stable --mode real` | Run stable checklist | 44-item checklist results |
| `python main.py stable-v060-check --mode real` | Run v0.6.0 checklist | Multi-category check results |
| `python main.py release-gate-health` | Release gate health | Health check summary |

---

## B. Research & Strategy

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `python main.py strategy-lab-dashboard --mode real` | Strategy Lab Dashboard | Daily — overview of all strategies |
| `python main.py strategy-validation --mode real` | Strategy validation scores | Check strategy confidence grades |
| `python main.py evidence-graph --mode real` | Evidence graph | Trace evidence chains |
| `python main.py crash-reversal --mode real` | Crash reversal analysis | When reviewing post-crash stocks |
| `python main.py research-intelligence --mode real` | Research intelligence priority board | Daily — see what needs attention |

---

## C. Reports

| Command | Purpose | Output Location |
|---------|---------|----------------|
| `python main.py report-pack --type daily --mode real` | Daily report pack | reports/ |
| `python main.py report-pack --type weekly --mode real` | Weekly report pack | reports/ |
| `python main.py report-pack --type full --mode real` | Full report pack | reports/ |
| `python main.py documentation-report --mode real` | Documentation health report | reports/ |
| `python main.py regression-hardening-report --mode real` | Regression hardening report | reports/ |

---

## D. Maintenance

| Command | Purpose | Notes |
|---------|---------|-------|
| `python main.py safety-scan --target all` | Scan for forbidden actions | Must pass (0 BLOCKED) |
| `python main.py safety-scan --target docs` | Scan docs only | Check new docs |
| `python main.py docs-health-check` | Documentation health check | All docs present and safe |
| `python main.py docs-summary` | Documentation summary | Quick overview |
| `python main.py docs-index` | Index all docs | Saves CSV manifest |
| `python main.py data-report-hygiene-summary` | Data hygiene summary | Check stale/large files |
| `python main.py gui-health-check` | GUI health check | Check all GUI panels |

---

## E. Simulation (Research Only)

| Command | Purpose | Notes |
|---------|---------|-------|
| `python main.py mock-realtime --duration 10` | Mock realtime simulation | Simulation only, no real data |
| `python main.py paper` | Paper trading simulation | Simulation only, no real orders |

**Both are simulation only. No real trading. No broker connection.**

---

## Git Operations (Important Rules)

Always use `git -C "path" command` format. Examples:

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" status
git -C "C:/Users/Rossi/Documents/Claude/trading_master" log --oneline -5
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add release/version_info.py
```

Rules:
- Do NOT chain commands with `&&`, `;`, `||`, or `|`
- Do NOT use `git add .` — add files individually by name
- Do NOT commit runtime outputs (.csv, .json, .md reports, .db)
- Do NOT use heredoc in git commit — use multiple `-m` flags

---

*TW Quant Cockpit v1.0.5 — Documentation & User Guide Polish — Research Only — Not Investment Advice*
