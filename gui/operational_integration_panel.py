"""
gui/operational_integration_panel.py
Headless-safe GUI panel for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 22 tabs. Headless-safe: no tkinter/Qt at module level. Renders to dict or text.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

PANEL_TABS = [
    "Overview",
    "Components",
    "Contracts",
    "Pipeline",
    "Data Flow",
    "Lineage",
    "Timestamps",
    "Identities",
    "Compatibility",
    "Consistency",
    "Reconciliation",
    "Degraded",
    "Failures",
    "Recovery",
    "Determinism",
    "Scorecard",
    "Snapshots",
    "Report",
    "Scenarios",
    "Fixtures",
    "Health",
    "Safety",
]
assert len(PANEL_TABS) == 22


class OperationalIntegrationPanel:
    """
    Headless-safe GUI panel for operational integration hardening.
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
            "data":        self._run.get(section_key, {}),
            "paper_only":  True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    def render_all_tabs(self) -> List[Dict[str, Any]]:
        """Render all tabs as a list of dicts."""
        return [self.render_tab(i) for i in range(len(PANEL_TABS))]

    def render_text(self) -> str:
        """Render panel summary as plain text. Headless-safe."""
        lines = [
            "=" * 70,
            "Operational Integration Hardening v1.6.8",
            "[!] Research Only. Paper Only. No Real Orders. No Broker.",
            "=" * 70,
        ]
        run_id = self._run.get("run_id", "N/A")
        status = self._run.get("status", "NO_DATA")
        session = self._run.get("session_id", "N/A")
        score_val = self._run.get("total_score", None)
        lines.append(f"Run ID:   {run_id}")
        lines.append(f"Session:  {session}")
        lines.append(f"Status:   {status}")
        if score_val is not None:
            lines.append(f"Score:    {score_val}")
        lines.append("")
        lines.append("Tabs:")
        for i, tab in enumerate(PANEL_TABS):
            prefix = "  >> " if i == self._selected_tab else "     "
            lines.append(f"{prefix}[{i:02d}] {tab}")
        lines.append("=" * 70)
        lines.append("[!] Not for production trading. Not investment advice.")
        return "\n".join(lines)

    def render_gui_model(self) -> Dict[str, Any]:
        """Render the full GUI model as a dict."""
        return {
            "panel_title": "Operational Integration Hardening v1.6.8",
            "version": "1.6.8",
            "release_name": "Operational Integration Hardening",
            "tabs": self.get_tab_names(),
            "tab_count": len(PANEL_TABS),
            "selected_tab": self._selected_tab,
            "selected_tab_name": PANEL_TABS[self._selected_tab],
            "run_id": self._run.get("run_id", ""),
            "session_id": self._run.get("session_id", ""),
            "status": self._run.get("status", "NO_DATA"),
            "total_score": self._run.get("total_score", None),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    def render_overview(self) -> Dict[str, Any]:
        """Render the Overview tab content."""
        return {
            "tab": "Overview",
            "run_id": self._run.get("run_id", ""),
            "session_id": self._run.get("session_id", ""),
            "status": self._run.get("status", "NO_DATA"),
            "total_score": self._run.get("total_score", None),
            "component_count": self._run.get("component_count", 0),
            "contract_count": self._run.get("contract_count", 0),
            "stage_count": self._run.get("stage_count", 0),
            "paper_only": True,
            "research_only": True,
        }

    def render_safety(self) -> Dict[str, Any]:
        """Render the Safety tab content."""
        return {
            "tab": "Safety",
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
            "broker_integration_enabled": False,
            "real_account_integration_enabled": False,
            "production_ledger_integration_enabled": False,
            "live_execution_integration_enabled": False,
            "network_integration_enabled": False,
            "auto_session_control_enabled": False,
            "auto_capital_reallocation_enabled": False,
            "auto_risk_override_enabled": False,
            "safety_note": "All safety capabilities = 0. Paper/research only.",
        }

    def handle_malformed_input(self, data: Any) -> Dict[str, Any]:
        """Handle malformed input gracefully without crashing."""
        if not isinstance(data, dict):
            return {
                "error": "malformed_input",
                "type": type(data).__name__,
                "paper_only": True,
            }
        return {"ok": True, "paper_only": True}
