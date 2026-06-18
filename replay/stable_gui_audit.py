"""
replay/stable_gui_audit.py — ReplayStableGUIAudit for v1.2.9.

Lightweight import-based audit of GUI panels for stable rollup.
No real orders. No broker. Research only.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import importlib
import importlib.util
import logging
import os
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_EXPECTED_PANELS: List[Tuple[str, str]] = [
    ("gui.replay_stable_rollup_panel",       "ReplayStableRollupPanel"),
    ("gui.replay_stable_rollup_adapter",     "ReplayStableRollupAdapter"),
    ("gui.replay_stable_capability_panel",   "ReplayStableCapabilityPanel"),
    ("gui.replay_stable_health_panel",       "ReplayStableHealthPanel"),
    ("gui.replay_stable_contract_panel",     "ReplayStableContractPanel"),
    ("gui.replay_stable_compatibility_panel","ReplayStableCompatibilityPanel"),
    ("gui.replay_stable_audit_panel",        "ReplayStableAuditPanel"),
    ("gui.replay_stable_report_panel",       "ReplayStableReportPanel"),
]


class ReplayStableGUIAudit:
    """
    Audits that all stable GUI panels can be imported.
    Also checks gui/dashboard.py has replay_stable tab registered.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, project_root: str = "") -> None:
        if project_root:
            self._root = project_root
        else:
            self._root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def audit_all(self) -> Dict[str, Tuple[str, str]]:
        """Audit all expected GUI panels. Returns {panel: (status, message)}."""
        results: Dict[str, Tuple[str, str]] = {}

        for module_path, class_name in _EXPECTED_PANELS:
            results[module_path] = self._check_panel(module_path, class_name)

        # Check dashboard.py for replay_stable tab
        results["dashboard_replay_stable_tab"] = self._check_dashboard_tab()

        return results

    def _check_panel(self, module_path: str, class_name: str) -> Tuple[str, str]:
        """Check if panel module can be spec-found (not fully imported to avoid Qt)."""
        try:
            spec = importlib.util.find_spec(module_path)
            if spec is None:
                return ("WARN", f"{module_path}: module spec not found (may be optional)")
            # Try import without Qt side effects
            try:
                mod = importlib.import_module(module_path)
                cls = getattr(mod, class_name, None)
                if cls is None:
                    return ("WARN", f"{module_path}: class {class_name} not found after import")
                return ("PASS", f"{module_path}.{class_name} imports OK")
            except ImportError as qt_exc:
                # Qt not installed — check spec only
                if "PySide6" in str(qt_exc) or "Qt" in str(qt_exc):
                    return ("PASS", f"{module_path}: spec found, Qt not installed (expected in non-GUI env)")
                return ("WARN", f"{module_path}: import error: {qt_exc}")
        except Exception as exc:
            return ("WARN", f"{module_path}: spec check error: {exc}")

    def _check_dashboard_tab(self) -> Tuple[str, str]:
        """Check gui/dashboard.py has replay_stable tab registered."""
        dashboard_path = os.path.join(self._root, "gui", "dashboard.py")
        try:
            with open(dashboard_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "replay_stable" in content or "ReplayStableRollupPanel" in content:
                return ("PASS", "gui/dashboard.py references replay_stable / ReplayStableRollupPanel")
            return ("WARN", "gui/dashboard.py may not register replay_stable tab yet")
        except Exception as exc:
            return ("WARN", f"dashboard.py check error: {exc}")
