"""
scripts/update_panel_version_197.py
Adds "1.9.7" to all PANEL_VERSION backward-compat checks for v1.9.6.
Safe, targeted string replacements only.
"""
import os

REPO = os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit")

# Each entry: (file_path_relative, old_str, new_str)
CHANGES = [
    # ── Release gate files ────────────────────────────────────────────────────
    ("release/abc_buy_point_execution_plan_release_gate_v172.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/theme_rotation_scanner_release_gate_v177.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/small_capital_strategy_integration_release_gate_v178.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/stable_rollup_release_gate_v179.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/stable_rollup_release_gate_v179.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("release/decision_cockpit_release_gate_v186.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/decision_report_release_gate_v187.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/decision_workflow_release_gate_v188.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/decision_performance_release_gate_v190.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/strategy_tuning_release_gate_v191.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    ("release/strategy_sandbox_release_gate_v192.py",
     '"1.9.4", "1.9.5", "1.9.6"))',
     '"1.9.4", "1.9.5", "1.9.6", "1.9.7"))'),

    ("release/strategy_promotion_release_gate_v193.py",
     '"1.9.4", "1.9.5", "1.9.6"))',
     '"1.9.4", "1.9.5", "1.9.6", "1.9.7"))'),

    ("release/strategy_monitoring_release_gate_v194.py",
     '"1.9.4", "1.9.5", "1.9.6"))',
     '"1.9.4", "1.9.5", "1.9.6", "1.9.7"))'),

    ("release/strategy_review_release_gate_v195.py",
     '"1.9.5", "1.9.6"))',
     '"1.9.5", "1.9.6", "1.9.7"))'),

    # v196 gate uses ("1.9.6",) - two occurrences
    ("release/strategy_registry_release_gate_v196.py",
     'lambda: PANEL_VERSION in ("1.9.6",))',
     'lambda: PANEL_VERSION in ("1.9.6", "1.9.7"))'),

    # ── Health files ──────────────────────────────────────────────────────────
    ("paper_trading/small_capital_strategy/theme_rotation_health_v177.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("paper_trading/small_capital_strategy/decision_cockpit_health_v186.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("paper_trading/small_capital_strategy/strategy_tuning_health_v191.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("paper_trading/small_capital_strategy/strategy_sandbox_health_v192.py",
     '"1.9.4", "1.9.5", "1.9.6")',
     '"1.9.4", "1.9.5", "1.9.6", "1.9.7")'),

    ("paper_trading/small_capital_strategy/strategy_review_health_v195.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),
]

# Test file changes
TEST_CHANGES = [
    # ── PANEL_VERSION in (...) assertions ──────────────────────────────────────
    ("tests/test_decision_cockpit_gui_v186.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_decision_cockpit_gui_v186.py",
     'or "1.9.6" in PANEL_TITLE',
     'or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE'),

    ("tests/test_decision_cockpit_gui_v186.py",
     'or "Review" in PANEL_TITLE',
     'or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE'),

    ("tests/test_decision_report_gui_v187.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_decision_report_gui_v187.py",
     'or "1.9.6" in PANEL_TITLE',
     'or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE'),

    ("tests/test_decision_report_gui_v187.py",
     'or "Review" in PANEL_TITLE',
     'or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE'),

    ("tests/test_decision_workflow_gui_v188.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_decision_workflow_gui_v188.py",
     'or "1.9.6" in PANEL_TITLE',
     'or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE'),

    ("tests/test_decision_workflow_gui_v188.py",
     'or "Review" in PANEL_TITLE',
     'or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE'),

    ("tests/test_decision_journal_gui_v189.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_decision_journal_gui_v189.py",
     'or "1.9.6" in PANEL_TITLE',
     'or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE'),

    ("tests/test_decision_journal_gui_v189.py",
     'or "Review" in PANEL_TITLE',
     'or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE'),

    ("tests/test_decision_performance_gui_v190.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_decision_performance_gui_v190.py",
     'or "1.9.6" in PANEL_TITLE',
     'or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE'),

    ("tests/test_decision_performance_gui_v190.py",
     'or "Drift" in PANEL_TITLE',
     'or "Drift" in PANEL_TITLE or "Governance" in PANEL_TITLE'),

    ("tests/test_strategy_tuning_gui_v191.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_strategy_sandbox_gui_v192.py",
     '"1.9.4", "1.9.5", "1.9.6")',
     '"1.9.4", "1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_strategy_promotion_gui_v193.py",
     '"1.9.4", "1.9.5", "1.9.6")',
     '"1.9.4", "1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_strategy_promotion_gui_v193.py",
     'or "Review" in PANEL_TITLE',
     'or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE'),

    ("tests/test_strategy_monitoring_gui_v194.py",
     '"1.9.4", "1.9.5", "1.9.6")',
     '"1.9.4", "1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_strategy_monitoring_gui_v194.py",
     'or "Review" in PANEL_TITLE',
     'or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE'),

    ("tests/test_strategy_review_gui_v195.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_stable_rollup_integration_v179.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),

    ("tests/test_decision_performance_gui_v190.py",
     '"1.9.5", "1.9.6")',
     '"1.9.5", "1.9.6", "1.9.7")'),
]

ALL_CHANGES = CHANGES + TEST_CHANGES

updated = 0
skipped = 0
for rel_path, old_str, new_str in ALL_CHANGES:
    full_path = os.path.join(REPO, rel_path.replace("/", os.sep))
    if not os.path.exists(full_path):
        print(f"  SKIP (not found): {rel_path}")
        skipped += 1
        continue
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    if old_str not in content:
        print(f"  SKIP (pattern not found): {rel_path!r}  pattern={old_str!r}")
        skipped += 1
        continue
    new_content = content.replace(old_str, new_str)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  OK: {rel_path}")
    updated += 1

print(f"\nDone: {updated} files updated, {skipped} skipped.")
