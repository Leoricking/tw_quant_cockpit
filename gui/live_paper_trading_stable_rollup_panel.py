"""
gui/live_paper_trading_stable_rollup_panel.py
Headless-safe GUI panel for Live Paper Trading Stable Rollup v1.6.9.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 21 tabs. Headless-safe: no tkinter at module level. Renders to dict or text.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
PRODUCTION_BLOCKED = True
headless_safe = True

PANEL_TITLE = "Live Paper Trading Stable Rollup"
PANEL_VERSION = "1.6.9"

PANEL_TABS = [
    "Overview",
    "Releases",
    "Manifest",
    "Capabilities",
    "Components",
    "Safety Matrix",
    "Compatibility",
    "Health",
    "Gates",
    "CLI",
    "GUI",
    "Fixtures",
    "Scenarios",
    "Lineage",
    "Contracts",
    "Regression",
    "Reconciliation",
    "Scorecard",
    "Migration Readiness",
    "Report",
    "Safety",
]
assert len(PANEL_TABS) == 21, f"Expected 21 tabs, got {len(PANEL_TABS)}"


class LivePaperTradingStableRollupPanel:
    """
    Headless-safe GUI panel for stable rollup v1.6.9.
    tkinter is imported inside methods only (never at module level).
    Renders to dict or text. No real-time data. No broker. No production.
    """

    headless_safe = True
    NO_REAL_ORDERS = True
    PRODUCTION_BLOCKED = True

    def __init__(self, run_data: Optional[Dict[str, Any]] = None) -> None:
        self._run = run_data or {}
        self._selected_tab = 0

    def set_run_data(self, run_data: Dict[str, Any]) -> None:
        """Set the run data to display."""
        self._run = run_data

    def select_tab(self, tab_index: int) -> None:
        """Select a tab by index (0-based)."""
        if 0 <= tab_index < len(PANEL_TABS):
            self._selected_tab = tab_index

    def get_tab_names(self) -> List[str]:
        """Return list of all tab names."""
        return list(PANEL_TABS)

    def render_tab(self, tab_index: int) -> Dict[str, Any]:
        """Render a single tab as a dict."""
        if tab_index < 0 or tab_index >= len(PANEL_TABS):
            return {"error": f"invalid_tab_index: {tab_index}"}
        tab_name = PANEL_TABS[tab_index]
        section_key = tab_name.lower().replace(" ", "_").replace("/", "_")
        data = self._run.get(section_key, {})

        # Load data from stable rollup modules if not provided
        if not data:
            data = self._load_tab_data(tab_name)

        return {
            "tab_index": tab_index,
            "tab_name": tab_name,
            "section_key": section_key,
            "data": data,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    def render_all_tabs(self) -> List[Dict[str, Any]]:
        """Render all tabs."""
        return [self.render_tab(i) for i in range(len(PANEL_TABS))]

    def render_overview(self) -> Dict[str, Any]:
        """Render the Overview tab."""
        return {
            "title": PANEL_TITLE,
            "version": PANEL_VERSION,
            "release_name": "Live Paper Trading Stable Rollup",
            "base_release": "1.6.8 Operational Integration Hardening",
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
            "headless_safe": True,
        }

    def _load_tab_data(self, tab_name: str) -> Dict[str, Any]:
        """Load data for a tab from stable rollup modules (headless-safe, no crash on missing)."""
        try:
            if tab_name == "Overview":
                return self.render_overview()
            elif tab_name == "Releases":
                from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
                return {"releases": get_manifest()}
            elif tab_name == "Manifest":
                from paper_trading.stable_rollup.release_manifest_v169 import validate_manifest
                return validate_manifest()
            elif tab_name == "Capabilities":
                from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
                return {"capabilities": get_matrix()}
            elif tab_name == "Components":
                from paper_trading.stable_rollup.component_matrix_v169 import get_matrix
                return {"components": get_matrix()}
            elif tab_name == "Safety Matrix":
                from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix
                return {"safety_items": get_matrix()}
            elif tab_name == "Compatibility":
                from paper_trading.stable_rollup.compatibility_matrix_v169 import get_edges
                return {"edges": get_edges()}
            elif tab_name == "Health":
                from paper_trading.stable_rollup.health_aggregator_v169 import run
                return run()
            elif tab_name == "Gates":
                from paper_trading.stable_rollup.gate_aggregator_v169 import run
                return run()
            elif tab_name == "CLI":
                from paper_trading.stable_rollup.cli_aggregator_v169 import run
                return run()
            elif tab_name == "GUI":
                from paper_trading.stable_rollup.gui_aggregator_v169 import run
                return run()
            elif tab_name == "Fixtures":
                from paper_trading.stable_rollup.fixture_aggregator_v169 import run
                return run()
            elif tab_name == "Scenarios":
                from paper_trading.stable_rollup.scenario_aggregator_v169 import run
                return run()
            elif tab_name == "Lineage":
                from paper_trading.stable_rollup.lineage_aggregator_v169 import run
                return run()
            elif tab_name == "Contracts":
                from paper_trading.stable_rollup.contract_aggregator_v169 import run
                return run()
            elif tab_name == "Regression":
                from paper_trading.stable_rollup.regression_matrix_v169 import RegressionChecker
                return RegressionChecker().summary()
            elif tab_name == "Reconciliation":
                from paper_trading.stable_rollup.stable_reconciler_v169 import run_reconciliation
                return run_reconciliation()
            elif tab_name == "Scorecard":
                from paper_trading.stable_rollup.stable_scorecard_v169 import compute_scorecard
                score = compute_scorecard()
                return {
                    "total_score": score.total_score,
                    "grade": score.grade,
                    "component_scores": score.component_scores,
                    "migration_ready": score.migration_ready,
                }
            elif tab_name == "Migration Readiness":
                from paper_trading.stable_rollup.migration_readiness_v169 import assess_migration_readiness
                return assess_migration_readiness()
            elif tab_name == "Report":
                from paper_trading.stable_rollup.stable_report_v169 import generate_report, StableReport
                report = generate_report()
                return StableReport().to_dict(report)
            elif tab_name == "Safety":
                from paper_trading.stable_rollup.safety_v169 import validate_safety
                return validate_safety()
            else:
                return {"tab": tab_name, "note": "No data loader for this tab"}
        except Exception as exc:
            return {"tab": tab_name, "error": str(exc)}

    def to_text(self) -> str:
        """Render all tabs to a text summary."""
        lines = [
            f"{'=' * 60}",
            f"  {PANEL_TITLE}",
            f"  Version: {PANEL_VERSION}",
            f"  Paper Only: True | No Real Orders: True",
            f"{'=' * 60}",
        ]
        for i, tab in enumerate(PANEL_TABS):
            lines.append(f"\n[Tab {i}] {tab}")
        return "\n".join(lines)

    def launch_gui(self) -> None:
        """
        Launch the GUI (requires display). Imports tkinter inside method.
        Falls back gracefully if display is unavailable.
        """
        try:
            import tkinter as tk
            from tkinter import ttk

            root = tk.Tk()
            root.title(f"{PANEL_TITLE} v{PANEL_VERSION}")
            root.resizable(True, True)

            notebook = ttk.Notebook(root)
            notebook.pack(fill="both", expand=True)

            for i, tab_name in enumerate(PANEL_TABS):
                frame = ttk.Frame(notebook)
                notebook.add(frame, text=tab_name)
                tab_data = self.render_tab(i)
                label = tk.Label(
                    frame,
                    text=f"[RESEARCH ONLY] {tab_name}\nPaper Only | No Real Orders | Not for Production\n\n{tab_data.get('data', {})}",
                    justify="left",
                    anchor="nw",
                    wraplength=900,
                )
                label.pack(fill="both", expand=True, padx=10, pady=10)

            root.mainloop()
        except Exception:
            # Headless fallback
            pass
