"""
gui/paper_performance_attribution_panel.py
Headless-safe GUI panel for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 31 tabs. Headless-safe: no tkinter/Qt at module level. Renders to dict or text.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

PANEL_TABS = [
    "Attribution Summary",
    "Gross vs Net Return",
    "Realized vs Unrealized",
    "Active Return Decomposition",
    "Selection Attribution",
    "Allocation Attribution",
    "Timing Attribution",
    "Execution Attribution",
    "Cost Attribution",
    "Slippage Attribution",
    "Turnover Attribution",
    "Exposure Attribution",
    "Risk Attribution",
    "Drawdown Attribution",
    "Regime Attribution",
    "Benchmark Attribution",
    "Factor Attribution",
    "Strategy Attribution",
    "Session Attribution",
    "Symbol Attribution",
    "Sector Attribution",
    "Industry Attribution",
    "Position Attribution",
    "Trade Attribution",
    "Portfolio Attribution",
    "Reconciliation Status",
    "Quality Scorecard",
    "Top / Bottom Contributors",
    "Data Quality Summary",
    "Disclaimer",
    "Not for Real Trading",
]
assert len(PANEL_TABS) == 31


class PaperAttributionPanel:
    """
    Headless-safe GUI panel for paper performance attribution.
    Renders to dict (GUI model) or text (console). No real-time data. No broker.
    """

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
        return {
            "tab_index":   tab_index,
            "tab_name":    tab_name,
            "section_key": section_key,
            "data":        self._run.get(section_key, {"status": "EMPTY"}),
            "run_id":      self._run.get("run_id", ""),
            "period_start": self._run.get("period_start", ""),
            "period_end":  self._run.get("period_end", ""),
            "paper_only":  True,
            "research_only": True,
            "no_real_orders": True,
        }

    def render(self) -> Dict[str, Any]:
        """
        Render the full panel as a GUI model dict.
        Returns all 31 tabs with their content.
        """
        tabs = []
        for i, tab_name in enumerate(PANEL_TABS):
            tabs.append(self.render_tab(i))

        return {
            "panel_type":    "paper_performance_attribution",
            "version":       "1.6.7",
            "title":         "Paper Performance Attribution",
            "subtitle":      "[Research Only] [Paper Only] [No Real Orders]",
            "run_id":        self._run.get("run_id", ""),
            "portfolio_id":  self._run.get("portfolio_id", ""),
            "period_start":  self._run.get("period_start", ""),
            "period_end":    self._run.get("period_end", ""),
            "status":        self._run.get("status", "EMPTY"),
            "tabs":          tabs,
            "tab_count":     len(tabs),
            "selected_tab":  self._selected_tab,
            "paper_only":    True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
            "not_for_real_trading": True,
        }

    def render_text(self) -> str:
        """Render panel summary as plain text (console/headless)."""
        lines = [
            "=" * 70,
            "  PAPER PERFORMANCE ATTRIBUTION PANEL  (Research Only)",
            "=" * 70,
            f"  Run ID    : {self._run.get('run_id', 'N/A')}",
            f"  Portfolio : {self._run.get('portfolio_id', 'N/A')}",
            f"  Period    : {self._run.get('period_start', '')} → {self._run.get('period_end', '')}",
            f"  Status    : {self._run.get('status', 'EMPTY')}",
            "-" * 70,
            f"  Tabs ({len(PANEL_TABS)}):",
        ]
        for i, tab in enumerate(PANEL_TABS):
            marker = "►" if i == self._selected_tab else " "
            lines.append(f"  {marker} [{i:02d}] {tab}")
        lines += [
            "=" * 70,
            "  NOT FOR REAL TRADING. PAPER RESEARCH ONLY.",
            "=" * 70,
        ]
        return "\n".join(lines)

    def get_summary_kpis(self) -> Dict[str, Any]:
        """Return key performance indicators for the panel header."""
        pa = self._run.get("portfolio_attribution", {}) or {}
        qs = self._run.get("quality_score", {}) or {}
        return {
            "active_return":  pa.get("active_return"),
            "gross_return":   pa.get("gross_return"),
            "net_return":     pa.get("net_return"),
            "reconciled":     pa.get("reconciled"),
            "confidence":     pa.get("confidence", "UNKNOWN"),
            "quality_score":  qs.get("total_score"),
            "grade":          qs.get("grade"),
            "paper_only":     True,
        }
