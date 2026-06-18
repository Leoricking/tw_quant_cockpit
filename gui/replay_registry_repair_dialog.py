"""
gui/replay_registry_repair_dialog.py — Registry Repair dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Preview by default. Execute requires allow-write via CLI.
[!] AUTO_REGISTRY_REPAIR_ENABLED = False
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_REGISTRY_REPAIR_ENABLED = False


class ReplayRegistryRepairDialog:
    """
    Preview and display registry repair plan.
    Execute always blocked from GUI — must use CLI with --execute --allow-write.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Auto repair is disabled.
    [!] Does NOT modify raw datasets.
    [!] Does NOT auto-download or create fake files.
    """

    RESEARCH_ONLY               = True
    NO_REAL_ORDERS              = True
    AUTO_REGISTRY_REPAIR_ENABLED = False

    PLAN_COLUMNS = ["issue_type", "target", "severity", "repairability",
                    "proposed_action", "blocked"]

    def __init__(self) -> None:
        self._last_preview: Optional[Dict[str, Any]] = None

    def run_preview(self) -> Dict[str, Any]:
        try:
            from replay.registry_repair import ReplayRegistryRepairPlanner
            from replay.dataset_registry import ReplayDatasetRegistry
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            planner  = ReplayRegistryRepairPlanner()
            ds_reg   = ReplayDatasetRegistry()
            sess_reg = ReplaySessionRegistryV128()
            result = planner.preview(
                dataset_registry=ds_reg,
                session_registry=sess_reg,
            )
            self._last_preview = result
            return result
        except Exception as exc:
            logger.warning("repair preview failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}

    def execute(self) -> Dict[str, Any]:
        """GUI always blocks — must use CLI with --execute --allow-write."""
        return {
            "blocked":       True,
            "reason":        "Repair must be executed via CLI with --execute --allow-write",
            "research_only": True,
        }

    def verify(self) -> Dict[str, Any]:
        try:
            from replay.registry_repair import ReplayRegistryRepairPlanner
            from replay.dataset_registry import ReplayDatasetRegistry
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            planner  = ReplayRegistryRepairPlanner()
            ds_reg   = ReplayDatasetRegistry()
            sess_reg = ReplaySessionRegistryV128()
            return planner.verify(
                dataset_registry=ds_reg,
                session_registry=sess_reg,
            )
        except Exception as exc:
            logger.warning("verify failed: %s", exc)
            return {"ok": False, "reason": str(exc)}

    def get_last_preview(self) -> Optional[Dict[str, Any]]:
        return self._last_preview

    def get_plan_rows(self) -> List[Dict[str, Any]]:
        preview = self._last_preview or {}
        return preview.get("plan", [])
