"""
gui/multi_session_coordination_panel.py — Multi-Session Coordination Panel v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
Headless-safe: no tkinter/Qt import at module level. 26 tabs (logical sections).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
HEADLESS_SAFE = True

PANEL_VERSION = "1.6.6"

# 26 logical tab sections
PANEL_TABS = [
    "overview",
    "sessions",
    "lifecycle",
    "capabilities",
    "coordination_policy",
    "resources",
    "locks_leases",
    "priority",
    "fairness",
    "schedule",
    "conflicts",
    "conflict_resolution",
    "event_ordering",
    "barriers",
    "market_data",
    "data_isolation",
    "capital",
    "risk",
    "symbol_exposure",
    "strategy_conflicts",
    "leader_election",
    "heartbeat",
    "checkpoints",
    "recovery",
    "scorecard",
    "report",
]

assert len(PANEL_TABS) == 26, f"Expected 26 tabs, got {len(PANEL_TABS)}"


class MultiSessionCoordinationPanel:
    """
    Headless-safe panel for multi-session coordination v1.6.6.
    Renders to dict/text; no GUI toolkit required at module level.
    """

    def __init__(self) -> None:
        self._tab_data: Dict[str, Any] = {tab: {} for tab in PANEL_TABS}
        self._active_tab: str = PANEL_TABS[0]
        self._warnings: List[str] = []

    # ── Data loading ─────────────────────────────────────────────────────────

    def load_overview(self, data: Dict[str, Any]) -> None:
        self._tab_data["overview"] = data

    def load_sessions(self, sessions: List[Dict[str, Any]]) -> None:
        self._tab_data["sessions"] = sessions

    def load_lifecycle(self, lifecycle: Dict[str, Any]) -> None:
        self._tab_data["lifecycle"] = lifecycle

    def load_capabilities(self, caps: Dict[str, Any]) -> None:
        self._tab_data["capabilities"] = caps

    def load_coordination_policy(self, policy: Dict[str, Any]) -> None:
        self._tab_data["coordination_policy"] = policy

    def load_resources(self, resources: Dict[str, Any]) -> None:
        self._tab_data["resources"] = resources

    def load_locks_leases(self, data: Dict[str, Any]) -> None:
        self._tab_data["locks_leases"] = data

    def load_priority(self, data: Dict[str, Any]) -> None:
        self._tab_data["priority"] = data

    def load_fairness(self, data: Dict[str, Any]) -> None:
        self._tab_data["fairness"] = data

    def load_schedule(self, schedule: List[Dict[str, Any]]) -> None:
        self._tab_data["schedule"] = schedule

    def load_conflicts(self, conflicts: List[Dict[str, Any]]) -> None:
        self._tab_data["conflicts"] = conflicts

    def load_conflict_resolution(self, data: Dict[str, Any]) -> None:
        self._tab_data["conflict_resolution"] = data

    def load_event_ordering(self, data: Dict[str, Any]) -> None:
        self._tab_data["event_ordering"] = data

    def load_barriers(self, data: Dict[str, Any]) -> None:
        self._tab_data["barriers"] = data

    def load_market_data(self, data: Dict[str, Any]) -> None:
        self._tab_data["market_data"] = data

    def load_data_isolation(self, data: Dict[str, Any]) -> None:
        self._tab_data["data_isolation"] = data

    def load_capital(self, data: Dict[str, Any]) -> None:
        self._tab_data["capital"] = data

    def load_risk(self, data: Dict[str, Any]) -> None:
        self._tab_data["risk"] = data

    def load_symbol_exposure(self, data: Dict[str, Any]) -> None:
        self._tab_data["symbol_exposure"] = data

    def load_strategy_conflicts(self, data: Dict[str, Any]) -> None:
        self._tab_data["strategy_conflicts"] = data

    def load_leader_election(self, data: Dict[str, Any]) -> None:
        self._tab_data["leader_election"] = data

    def load_heartbeat(self, data: Dict[str, Any]) -> None:
        self._tab_data["heartbeat"] = data

    def load_checkpoints(self, data: Dict[str, Any]) -> None:
        self._tab_data["checkpoints"] = data

    def load_recovery(self, data: Dict[str, Any]) -> None:
        self._tab_data["recovery"] = data

    def load_scorecard(self, data: Dict[str, Any]) -> None:
        self._tab_data["scorecard"] = data

    def load_report(self, data: Dict[str, Any]) -> None:
        self._tab_data["report"] = data

    # ── Navigation ───────────────────────────────────────────────────────────

    def select_tab(self, tab: str) -> None:
        if tab not in PANEL_TABS:
            raise ValueError(f"Unknown tab: {tab}. Valid: {PANEL_TABS}")
        self._active_tab = tab

    def get_active_tab(self) -> str:
        return self._active_tab

    def list_tabs(self) -> List[str]:
        return list(PANEL_TABS)

    def tab_count(self) -> int:
        return len(PANEL_TABS)

    # ── Render ───────────────────────────────────────────────────────────────

    def render_tab(self, tab: Optional[str] = None) -> Dict[str, Any]:
        """Render a single tab to a dict (headless-safe)."""
        t = tab or self._active_tab
        if t not in PANEL_TABS:
            raise ValueError(f"Unknown tab: {t}")
        return {
            "tab": t,
            "panel_version": PANEL_VERSION,
            "paper_only": PAPER_ONLY,
            "research_only": RESEARCH_ONLY,
            "data": self._tab_data.get(t, {}),
            "warnings": self._warnings,
        }

    def render_all(self) -> Dict[str, Any]:
        """Render all 26 tabs to a dict (headless-safe)."""
        return {
            "panel_version": PANEL_VERSION,
            "paper_only": PAPER_ONLY,
            "research_only": RESEARCH_ONLY,
            "tabs": {tab: self._tab_data.get(tab, {}) for tab in PANEL_TABS},
            "active_tab": self._active_tab,
            "warnings": self._warnings,
        }

    def render_text_summary(self) -> str:
        """Plain-text summary of all tabs (headless-safe)."""
        lines = [
            f"Multi-Session Coordination Panel v{PANEL_VERSION}",
            "[!] Research Only. Paper Only. No Real Orders. No Broker.",
            f"Active tab: {self._active_tab}",
            "",
        ]
        for tab in PANEL_TABS:
            data = self._tab_data.get(tab, {})
            status = "loaded" if data else "empty"
            lines.append(f"  [{tab}]: {status}")
        if self._warnings:
            lines.append("")
            lines.append("Warnings:")
            for w in self._warnings:
                lines.append(f"  - {w}")
        return "\n".join(lines)

    # ── Warning management ───────────────────────────────────────────────────

    def add_warning(self, msg: str) -> None:
        self._warnings.append(msg)

    def clear_warnings(self) -> None:
        self._warnings.clear()

    def get_warnings(self) -> List[str]:
        return list(self._warnings)

    # ── Introspection ────────────────────────────────────────────────────────

    def loaded_tab_count(self) -> int:
        return sum(1 for tab in PANEL_TABS if self._tab_data.get(tab))

    def to_dict(self) -> Dict[str, Any]:
        return self.render_all()
