"""scripts/check_perf_gui.py - Check test_decision_performance_gui_v190."""
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
from gui.small_capital_strategy_panel import PANEL_VERSION, PANEL_TITLE

# Check the version assertion
ok = PANEL_VERSION in ("1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7")
print(f"PANEL_VERSION={PANEL_VERSION!r} in tuple: {ok}")

# Check the title assertion
title_ok = ("1.9.0" in PANEL_TITLE or "1.9.1" in PANEL_TITLE or "1.9.2" in PANEL_TITLE
            or "1.9.3" in PANEL_TITLE or "1.9.4" in PANEL_TITLE or "1.9.5" in PANEL_TITLE
            or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE)
print(f"title contains version: {title_ok}, PANEL_TITLE={PANEL_TITLE!r}")

# Check keyword
kw_ok = ("Performance" in PANEL_TITLE or "Review" in PANEL_TITLE or "Tuning" in PANEL_TITLE
         or "Sandbox" in PANEL_TITLE or "Promotion" in PANEL_TITLE or "Rollback" in PANEL_TITLE
         or "Monitoring" in PANEL_TITLE or "Drift" in PANEL_TITLE or "Governance" in PANEL_TITLE)
print(f"keyword ok: {kw_ok}")
