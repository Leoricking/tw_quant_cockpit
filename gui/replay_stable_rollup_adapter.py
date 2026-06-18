"""
gui/replay_stable_rollup_adapter.py — ReplayStableRollupAdapter v1.2.9

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStableRollupAdapter:
    """
    GUI adapter for Replay Training Stable Rollup panel.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._summary_cache: Optional[dict] = None

    def summary(self) -> dict:
        """Return stable rollup summary dict."""
        if self._summary_cache is not None:
            return self._summary_cache
        try:
            from replay.stable_summary import ReplayStableSummary
            s = ReplayStableSummary().build()
            self._summary_cache = s
            return s
        except Exception as exc:
            logger.warning("stable_summary unavailable: %s", exc)
            return {
                "release_version": "1.2.9",
                "release_name": "Replay Training Stable Rollup",
                "module_count": 12,
                "stable_capability_count": 16,
                "store_count": 10,
                "no_real_orders": True,
                "broker_disabled": True,
                "research_only": True,
                "stable_rollup": True,
                "replay_training_line_complete": True,
                "status": "UNAVAILABLE",
            }

    def manifest(self) -> dict:
        """Return stable manifest dict."""
        try:
            from replay.stable_manifest import ReplayStableManifest
            return ReplayStableManifest().build()
        except Exception as exc:
            logger.warning("stable_manifest unavailable: %s", exc)
            return {"status": "UNAVAILABLE", "research_only": True, "no_real_orders": True}

    def capabilities(self) -> list:
        """Return capability matrix list."""
        try:
            from replay.stable_capability_matrix import ReplayStableCapabilityMatrix
            return ReplayStableCapabilityMatrix().build()
        except Exception as exc:
            logger.warning("capability_matrix unavailable: %s", exc)
            return []
