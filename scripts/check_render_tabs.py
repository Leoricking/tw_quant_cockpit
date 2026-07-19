"""scripts/check_render_tabs.py - Verify render_all_tabs has no errors."""
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
from gui.small_capital_strategy_panel import render_all_tabs

rendered = render_all_tabs()
error_tabs = [k for k, v in rendered.items() if isinstance(v, dict) and v.get("error") is not None]
if error_tabs:
    print(f"FAIL: error_tabs = {error_tabs}")
    sys.exit(1)
else:
    print(f"OK: {len(rendered)} tabs rendered, no errors")
    print(f"  governance_dashboard in rendered: {'governance_dashboard' in rendered}")
    print(f"  decision_quality in rendered: {'decision_quality' in rendered}")
    print(f"  governance_analytics in rendered: {'governance_analytics' in rendered}")
