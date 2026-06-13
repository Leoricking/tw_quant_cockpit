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

*TW Quant Cockpit v1.1.0 — Data Universe Expansion — Research Only — Not Investment Advice*

---

## v1.0.9 Final Maintenance Rollup Commands

```bash
python main.py final-rollup
python main.py final-rollup-history
python main.py final-rollup-health
python main.py final-rollup-maintenance-plan
python main.py final-rollup-smoke
python main.py final-rollup-report --mode real
```

**[!] Research Only. No Real Orders. v1.0 Maintenance Line Complete.**

---

## v1.1.0 Data Universe Expansion Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `python main.py universe-build --tier core10` | Build CORE_10 universe | `--tier core10\|research30\|expanded50\|broad100` |
| `python main.py universe-summary --tier research30` | Show tier summary | `--tier <alias>` |
| `python main.py universe-health` | Universe health check (16 items) | — |
| `python main.py universe-coverage --tier research30` | Analyze data coverage per symbol | `--tier`, `--mode real\|mock` |
| `python main.py universe-symbol --stock 2454` | Per-symbol coverage detail | `--stock <ticker>` |
| `python main.py universe-missing --tier expanded50` | List symbols missing real data | `--tier <alias>` |
| `python main.py universe-report --tier research30` | Build coverage expansion report | `--tier <alias>` |

### Tier Reference

| Alias | Canonical | Symbol Count | Description |
|-------|-----------|--------------|-------------|
| `core10` | `CORE_10` | 10 | High-liquidity core (台積電, 聯發科…) |
| `research30` | `RESEARCH_30` | 30 (cumulative) | Core + 20 research names |
| `expanded50` | `EXPANDED_50` | 50 (cumulative) | Research + 20 expanded names |
| `broad100` | `BROAD_100` | up to 100 | Schema support; add symbols as needed |

### Quality Statuses

| Status | Meaning |
|--------|---------|
| `READY` | ≥240 rows, ≥98% OHLC, 0 invalid prices |
| `PARTIAL` | ≥120 rows, ≥90% OHLC |
| `INSUFFICIENT` | <120 rows of real data |
| `MISSING` | No real data file found |
| `INVALID` | Duplicate dates or broken schema |

**[!] Real Data Required. Mock Data Formal Conclusion BLOCKED. Research Only.**

---

## v1.1.1 Data Import UX & Batch Onboarding Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `python main.py import-discover --path <dir>` | Discover importable files | `--path <dir>` |
| `python main.py import-preview --file <file>` | Preview columns and schema for one file | `--file <path>` |
| `python main.py import-validate --path <dir>` | Validate all files (OHLC, columns, dates) | `--path <dir>` |
| `python main.py import-plan --path <dir>` | Build import plan (MERGE_SAFE / BLOCKED / REVIEW) | `--path <dir>` |
| `python main.py import-batch --path <dir> --dry-run` | Dry-run batch import (no writes) | `--dry-run` |
| `python main.py import-batch --path <dir> --execute --allow-write` | Execute safe items | `--execute --allow-write` |
| `python main.py import-retry-manifest` | Show / save retry manifest for failed files | `--output-dir <dir>` |
| `python main.py import-onboarding-health` | Onboarding health check (19 items) | — |
| `python main.py import-onboarding-report` | Build import onboarding report | `--mode real\|mock` |

### Import Plan Actions

| Action | Meaning |
|--------|---------|
| `MERGE_SAFE` | New rows only; safe to execute |
| `APPEND_SAFE` | Append; fails if any date overlap |
| `REVIEW` | Conflicting rows detected; manual review required |
| `BLOCKED` | Validation FAIL or REPLACE_EXPLICIT attempt; cannot execute |
| `DRY_RUN` | Simulated only; no actual write |

### Recommended Import SOP

```
1. python main.py import-discover --path <dir>
2. python main.py import-validate --path <dir>
3. python main.py import-plan --path <dir>
4. python main.py import-batch --path <dir> --dry-run
5. (resolve BLOCKED / REVIEW items manually)
6. python main.py import-batch --path <dir> --execute --allow-write
7. python main.py universe-coverage --tier research30 --mode real
```

**[!] dry_run=True by default. REPLACE_EXPLICIT BLOCKED. Conflicts → REVIEW. No Real Orders.**
