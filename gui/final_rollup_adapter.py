"""
gui/final_rollup_adapter.py — Final Rollup data adapter for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] GUI UX only. VALIDATED does not enable trading.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


class FinalRollupAdapter:
    """Provides data for the Final Rollup GUI panel.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    No external API. No broker. No auto trading.
    """

    no_real_orders = True
    broker_disabled = True
    external_api_disabled = True

    def __init__(self, project_root: Optional[str] = None) -> None:
        self._root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_release_history(self) -> List[dict]:
        try:
            from final_rollup.release_history import ReleaseHistoryBuilder
            builder = ReleaseHistoryBuilder(project_root=self._root)
            return [e.to_dict() for e in builder.build()]
        except Exception as exc:
            logger.warning("FinalRollupAdapter.get_release_history: %s", exc)
            return []

    def get_health_checks(self) -> List[dict]:
        try:
            from final_rollup.final_health_check import FinalMaintenanceHealthCheck
            checker = FinalMaintenanceHealthCheck(project_root=self._root)
            checks, _ = checker.run()
            return checks
        except Exception as exc:
            logger.warning("FinalRollupAdapter.get_health_checks: %s", exc)
            return []

    def get_maintenance_plan(self) -> List[dict]:
        try:
            from final_rollup.maintenance_plan import LongTermMaintenancePlanBuilder
            builder = LongTermMaintenancePlanBuilder()
            return [t.to_dict() for t in builder.build()]
        except Exception as exc:
            logger.warning("FinalRollupAdapter.get_maintenance_plan: %s", exc)
            return []

    def get_summary(self) -> dict:
        try:
            from final_rollup.final_rollup_engine import FinalRollupEngine
            engine = FinalRollupEngine(project_root=self._root)
            return engine.run()
        except Exception as exc:
            logger.warning("FinalRollupAdapter.get_summary: %s", exc)
            return {
                "version": "1.0.9",
                "error": str(exc),
                "no_real_orders": True,
            }
