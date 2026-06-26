"""
paper_trading/analytics/lineage_v164.py — Analytics Lineage v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone

from paper_trading.analytics.models_v164 import AnalyticsLineage

NO_REAL_ORDERS = True
PAPER_ONLY = True


class AnalyticsLineageTracker:
    """
    Tracks lineage for analytics results.
    Records source session IDs, event IDs, policy versions, code version, as_of.
    """

    def create_lineage(
        self,
        analytics_id: str,
        source_session_ids: List[str],
        source_event_ids: Optional[List[str]] = None,
        as_of: Optional[datetime] = None,
        metric_policy_version: str = "1.6.4",
        attribution_policy_version: str = "1.6.4",
        review_policy_version: str = "1.6.4",
        code_version: str = "1.6.4",
        release_version: str = "1.6.4",
    ) -> AnalyticsLineage:
        return AnalyticsLineage(
            lineage_id=str(uuid.uuid4()),
            analytics_id=analytics_id,
            source_session_ids=source_session_ids,
            source_event_ids=source_event_ids or [],
            metric_policy_version=metric_policy_version,
            attribution_policy_version=attribution_policy_version,
            review_policy_version=review_policy_version,
            as_of=as_of,
            code_version=code_version,
            release_version=release_version,
        )

    def has_gaps(self, lineage: AnalyticsLineage) -> bool:
        """Check for lineage gaps — no source sessions or missing as_of."""
        return not lineage.source_session_ids or lineage.as_of is None

    def to_dict(self, lineage: AnalyticsLineage) -> Dict[str, Any]:
        return {
            "lineage_id": lineage.lineage_id,
            "analytics_id": lineage.analytics_id,
            "source_session_ids": lineage.source_session_ids,
            "source_event_ids": lineage.source_event_ids,
            "metric_policy_version": lineage.metric_policy_version,
            "as_of": lineage.as_of.isoformat() if lineage.as_of else None,
            "code_version": lineage.code_version,
            "release_version": lineage.release_version,
            "paper_only": True,
        }


__all__ = ["AnalyticsLineageTracker"]
