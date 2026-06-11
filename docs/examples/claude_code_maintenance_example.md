# Claude Code Maintenance Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows how to perform maintenance tasks using Claude Code for TW Quant Cockpit v1.0.6.
All git commands must use `git -C "path"` format. No chain commands. No heredoc in commits.

---

## Critical Rules for Claude Code Maintenance

1. **Always use `git -C "C:/Users/Rossi/Documents/Claude/trading_master" command`** — never `cd path` then git
2. **Do NOT use `git add .`** — add files individually by name
3. **Do NOT chain commands** with `&&`, `;`, `||`, or `|`
4. **Do NOT use heredoc in git commit** — use multiple `-m` flags instead
5. **Do NOT commit runtime outputs** (.csv, .json, .md reports, .db)

---

## Step 1 — Check Git Status

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" status
```

REVIEW: confirm working tree is clean before making changes.

## Step 2 — Check Recent Commits

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" log --oneline -5
```

REVIEW: understand recent commit history.

## Step 3 — Run Safety Scan Before Commit

```
python main.py safety-scan --target all
```

Expected: 0 BLOCKED files. Do not commit if any BLOCKED files exist.

## Step 4 — Add Files Individually (Never git add .)

Add each modified file individually:

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add release/version_info.py
```

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add main.py
```

**Do NOT use `git add .`**

## Step 5 — Commit with Multiple -m Flags (Never Heredoc)

Use multiple `-m` flags for multi-line commit messages.
Do not use heredoc for commit messages.

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" commit -m "feat: example change v1.0.6" -m "Description of change. Research Only. No Real Orders."
```

## Step 6 — Run Regression After Changes

```
python main.py regression-run --suite release_gate --mode real
```

REVIEW: confirm all tests pass. WAIT if new failures appear.

## Step 7 — Tag a Release (If Applicable)

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" tag -a v1.0.6 -m "v1.0.6: Example Workflows & Templates"
```

## Step 8 — Push to Remote

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" push origin main
```

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" push origin v1.0.6
```

---

## Forbidden Patterns (Never Use)

- `cd "C:/Users/Rossi/Documents/Claude/trading_master" && git status` — chain command FORBIDDEN
- `git add .` — adds all files, may include runtime outputs FORBIDDEN
- `git commit -m "$(cat <<'EOF' ... EOF)"` — heredoc in commit FORBIDDEN
- Multiple commands on one line with `;` FORBIDDEN

---

## Allowed Actions (REVIEW mode)

- REVIEW git status and log
- READ_REPORT regression results
- WAIT if safety scan shows BLOCKED files

## What NOT To Do

- Do NOT commit runtime outputs
- Do NOT skip safety scan before commit
- Do NOT use chain commands or heredoc

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Maintenance does not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
