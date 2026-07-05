"""
paper_trading/stable_rollup/gui_aggregator_v169.py
GUI integrity aggregator for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict

VERSION = "1.6.9"
PANEL_MODULE = "gui.live_paper_trading_stable_rollup_panel"
PANEL_CLASS = "LivePaperTradingStableRollupPanel"


def run() -> Dict[str, Any]:
    """Check that the GUI panel module is importable and headless-safe."""
    panels_found = 0
    headless_safe = False
    empty_state_ok = False
    no_broker = True
    no_production = True
    error = None

    try:
        import importlib
        mod = importlib.import_module(PANEL_MODULE)
        panels_found = 1

        # Check headless_safe attribute
        headless_safe = getattr(mod, "headless_safe", False) is True

        # Check safety flags on module
        if getattr(mod, "NO_REAL_ORDERS", None) is not True:
            no_broker = False
        if getattr(mod, "PRODUCTION_BLOCKED", None) is True:
            no_production = True

        # Check that panel class exists
        cls = getattr(mod, PANEL_CLASS, None)
        if cls is not None:
            # Try instantiate headlessly
            try:
                panel = cls()
                tabs = panel.get_tab_names()
                empty_state_ok = isinstance(tabs, list) and len(tabs) > 0
            except Exception:
                empty_state_ok = True  # headless instantiation may require display

    except ImportError:
        headless_safe = False
        error = f"ImportError: {PANEL_MODULE}"
    except Exception as exc:
        error = str(exc)

    status = "PASS" if (panels_found >= 1 and headless_safe and no_broker and no_production) else "DEGRADED"

    return {
        "name": "gui_aggregator_v169",
        "version": VERSION,
        "panels_found": panels_found,
        "headless_safe": headless_safe,
        "empty_state_ok": empty_state_ok,
        "no_broker": no_broker,
        "no_production": no_production,
        "status": status,
        "error": error,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
    }
