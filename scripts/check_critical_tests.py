"""scripts/check_critical_tests.py - Quick sanity check of critical previously-failing tests."""
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

errors = []

# 1. v196 gate
from release.strategy_registry_release_gate_v196 import run_release_gate
r = run_release_gate()
if not r["gate_passed"]:
    errors.append(f"v196 gate FAIL: {[c['name'] for c in r['checks'] if not c['passed']]}")
else:
    print(f"OK: v196 gate {r['passed_count']}/{r['total']}")

# 2. stable rollup gui audit
from paper_trading.small_capital_strategy.stable_rollup_gui_audit_v179 import run_gui_audit
audit = run_gui_audit()
if not audit["render_clean"] or audit["error_tabs"]:
    errors.append(f"stable_rollup gui audit FAIL: error_tabs={audit['error_tabs']}")
else:
    print(f"OK: stable_rollup gui_audit render_clean={audit['render_clean']}")

# 3. stable_rollup health
from paper_trading.small_capital_strategy.stable_rollup_health_v179 import run_health_check
h = run_health_check()
if not h.all_passed:
    failed = [c for c in h.checks if not c["passed"]]
    errors.append(f"stable_rollup health FAIL: {[c['name'] for c in failed]}")
else:
    print(f"OK: stable_rollup health {h.passed}/{h.total}")

# 4. v196 registry health
from paper_trading.small_capital_strategy.strategy_registry_health_v196 import run_health_check as v196_health
rh = v196_health()
if not rh["all_passed"]:
    errors.append(f"v196 registry health FAIL: failed={rh['failed']}")
else:
    print(f"OK: v196 registry health {rh['passed']}/{rh['total']}")

# 5. render_all_tabs
from gui.small_capital_strategy_panel import render_all_tabs
rendered = render_all_tabs()
error_tabs = [k for k, v in rendered.items() if isinstance(v, dict) and v.get("error") is not None]
if error_tabs:
    errors.append(f"render_all_tabs FAIL: error_tabs={error_tabs}")
else:
    print(f"OK: render_all_tabs {len(rendered)} tabs, no errors")

if errors:
    print("\nFAILURES:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print("\nAll critical checks PASSED")
