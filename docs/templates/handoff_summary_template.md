# Handoff Summary Template

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Handoff Date: [YYYY-MM-DD]

## Current Version: v[VERSION] — [RELEASE_NAME]

## 一、System State

| Component | Status | Notes |
|-----------|--------|-------|
| Current Version | v[VERSION] | |
| Git Branch | main | |
| Last Commit | [HASH] | |
| Last Tag | v[VERSION] | |
| Regression Status | [PASS/WARN/FAIL] | |
| Safety Scan | [0 BLOCKED] | |

## 二、Known WARNs (Acceptable)

| Warning | Classification | Action Required |
|---------|---------------|----------------|
| CP950 encoding warning | KNOWN_CP950_WARNING | None |
| paper_state.json missing | KNOWN_PAPER_SMOKE_WARNING | None |
| ENV_LIMITED report status | KNOWN_REPORT_PACK_OPTIONAL | None |
| | | |

## 三、Research State

Current strategy validation grades:

| Strategy | Grade | Next Action |
|----------|-------|-------------|
| | | |

## 四、Critical Rules (Must Preserve)

1. **No Real Orders** — Never add broker API or real order execution
2. **No auto-trading** — Never add automatic trading logic
3. **No git add .** — Always add files individually by name
4. **No chain commands** — Never use `&&`, `;`, `||`, or `|` in commands
5. **No heredoc in commits** — Always use multiple `-m` flags
6. **Always use git -C** — Never use `cd path && git command`
7. **No commit runtime outputs** — .csv, .json, .md reports, .db stay gitignored
8. **Safety scan must pass** — 0 BLOCKED before any commit

## 五、Release Process

1. Run `python main.py safety-scan --target all` (must be 0 BLOCKED)
2. Update `release/version_info.py` with new VERSION
3. Add files individually with `git -C "path" add [file]`
4. Commit with multiple `-m` flags (no heredoc, no chain)
5. Run `python main.py regression-run --suite release_gate --mode real`
6. Tag with `git -C "path" tag -a vX.Y.Z -m "message"`
7. Push main and tag as separate commands

## 六、Documentation

Key documents:
- `docs/user_guide_v1.0.md` — User Guide
- `docs/handoff_guide_v1.0.md` — Handoff Guide
- `docs/safety_guide_v1.0.md` — Safety Guide
- `docs/index.md` — Documentation Index
- `docs/roadmap.md` — Roadmap
- `docs/release_notes_v1.0.md` — Release Notes

## 七、Next Planned Versions

| Version | Plan | Priority |
|---------|------|---------|
| v1.0.7 | Knowledge Base Search Polish | P2 |
| v1.1.0 | Data Universe Expansion | P1 |
| v1.2.0 | Replay Training UX | P2 |

## 八、Safety Confirmation

- [ ] No real trading actions in any module
- [ ] All safety flags confirmed: production_blocked=True, no_real_orders=True
- [ ] Handoff recipient understands: VALIDATED does not enable trading
- [ ] Handoff recipient understands: No broker API will be added without explicit request

---

## Safety Declaration

This template is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Templates do not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
