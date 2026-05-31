# Release Checklist — TW Quant Cockpit

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.

## 1. Source Code Check

- [ ] `python -m compileall . -q` — no errors
- [ ] All new modules have module-level safety docstring
- [ ] All classes have `read_only=True`, `no_real_orders=True`, `production_blocked=True`
- [ ] No hardcoded tokens in source
- [ ] No `broker.submit_order` calls in new code
- [ ] No `REAL_ORDER_READY=True` anywhere

## 2. CLI Check

- [ ] `python main.py version-info` — shows v0.4.0
- [ ] `python main.py stable-release-check --mode real` — PASS or PARTIAL
- [ ] `python main.py regression-suite --mode real --quick` — PASS
- [ ] `python main.py regression-suite --mode real --full` — PASS or PARTIAL
- [ ] `python main.py data-quality-gate --mode real` — no crash
- [ ] `python main.py provider-reliability --mode real` — no crash
- [ ] `python main.py rule-governance --mode real` — 53 rules
- [ ] `python main.py experiment-list` — no crash
- [ ] `python main.py hardened-backtest --mode real --entry-model next_open` — no crash
- [ ] `python main.py intraday-pipeline --mode real --freq 1min --dry-run` — no crash
- [ ] `python main.py auto-report --mode real --profile daily` — no crash
- [ ] `python main.py paper` — shows paper trading summary
- [ ] `python main.py mock-realtime --duration 10` — completes

## 3. GUI Check

- [ ] `python main.py cockpit --mode real` — GUI opens
- [ ] Release Status tab visible
- [ ] Run Quick Regression works
- [ ] Generate Stable Release Report works
- [ ] Experiment Registry tab still works
- [ ] Rule Governance tab still works
- [ ] All tabs preserved
- [ ] Close GUI without QThread warning

## 4. Report Check

- [ ] `stable_release_report_*.md` generated in reports/
- [ ] `stable_release_checklist_report_*.md` generated in reports/
- [ ] Reports show "Research Only / No Real Orders / Production BLOCKED"
- [ ] Reports NOT committed to git

## 5. Safety Check

- [ ] `read_only=True` in all new classes
- [ ] `no_real_orders=True` in all new classes
- [ ] `production_blocked=True` in all new classes
- [ ] `real_order_ready=False` confirmed
- [ ] No token in any .py file
- [ ] No `submit_order` in release files
- [ ] .env in .gitignore

## 6. Git Artifact Check

- [ ] `data/backtest_results/` in .gitignore
- [ ] `reports/auto_report_center/` in .gitignore
- [ ] `logs/` in .gitignore
- [ ] `experiments/EXP-*` in .gitignore
- [ ] `reports/stable_release_report_*.md` in .gitignore
- [ ] No runtime artifacts staged

## 7. Tag / Push Check

- [ ] Commit message follows convention
- [ ] `git tag v0.4.0` created
- [ ] `git push origin main` successful
- [ ] `git push origin v0.4.0` successful
- [ ] `git log --oneline -3` shows correct commit

## 8. Post-release Verification

- [ ] `git status` — working tree clean
- [ ] `git tag --list | grep v0.4.0` — tag exists
- [ ] Import tests pass on clean run
- [ ] No leftover debug prints
