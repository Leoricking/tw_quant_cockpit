"""
paper_trading/stable_rollup/stable_query_v169.py
Query module for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
import uuid
from typing import Dict, Any, Optional

from paper_trading.stable_rollup.models_v169 import StableRollupQuery

VERSION = "1.6.9"


class StableQuery:
    """Query interface for stable rollup data."""

    def _make_query(self, query_type: str, filters: Optional[Dict] = None, results=None) -> StableRollupQuery:
        if results is None:
            results = []
        filt = filters or {}
        return StableRollupQuery(
            query_id=f"srq-{uuid.uuid4().hex[:8]}",
            query_type=query_type,
            filters=filt,
            result_count=len(results),
            results=results,
        )

    def query_releases(self, filters: Optional[Dict] = None) -> StableRollupQuery:
        """Query the release manifest."""
        try:
            from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
            releases = get_manifest()
            filt = filters or {}
            if filt.get("version"):
                releases = [r for r in releases if r["version"] == filt["version"]]
            if filt.get("category"):
                releases = [r for r in releases if r.get("release_category") == filt["category"]]
            if filt.get("sealed_status"):
                releases = [r for r in releases if r.get("sealed_status") == filt["sealed_status"]]
            return self._make_query("releases", filters, releases)
        except Exception as exc:
            return self._make_query("releases", filters, [{"error": str(exc)}])

    def query_capabilities(self, filters: Optional[Dict] = None) -> StableRollupQuery:
        """Query the capability matrix."""
        try:
            from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
            caps = get_matrix()
            filt = filters or {}
            if filt.get("capability"):
                caps = [c for c in caps if c["capability"] == filt["capability"]]
            if filt.get("introduced_in"):
                caps = [c for c in caps if c["introduced_in"] == filt["introduced_in"]]
            if filt.get("production_ready") is not None:
                caps = [c for c in caps if c.get("production_ready") == filt["production_ready"]]
            return self._make_query("capabilities", filters, caps)
        except Exception as exc:
            return self._make_query("capabilities", filters, [{"error": str(exc)}])

    def query_safety(self, filters: Optional[Dict] = None) -> StableRollupQuery:
        """Query the safety matrix."""
        try:
            from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix
            items = get_matrix()
            filt = filters or {}
            if filt.get("capability"):
                items = [i for i in items if i["capability"] == filt["capability"]]
            if filt.get("status"):
                items = [i for i in items if i["status"] == filt["status"]]
            return self._make_query("safety", filters, items)
        except Exception as exc:
            return self._make_query("safety", filters, [{"error": str(exc)}])

    def query_health(self, filters: Optional[Dict] = None) -> StableRollupQuery:
        """Query health aggregation results."""
        try:
            from paper_trading.stable_rollup.health_aggregator_v169 import run
            result = run()
            summaries = result.get("summaries", [])
            filt = filters or {}
            if filt.get("status"):
                summaries = [s for s in summaries if s.get("status") == filt["status"]]
            return self._make_query("health", filters, summaries)
        except Exception as exc:
            return self._make_query("health", filters, [{"error": str(exc)}])
