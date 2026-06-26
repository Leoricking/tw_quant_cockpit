"""
paper_trading/analytics/snapshot_v164.py — Analytics Snapshot v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Immutable snapshots. All hashes deterministic.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid

from paper_trading.analytics.models_v164 import AnalyticsSnapshot

NO_REAL_ORDERS = True
PAPER_ONLY = True


def _hash_dict(d: Dict[str, Any]) -> str:
    """Deterministic JSON hash of dict."""
    serialized = json.dumps(d, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()


class AnalyticsSnapshotManager:
    """Creates immutable analytics snapshots for reproducibility."""

    def create_snapshot(
        self,
        analytics_id: str,
        session_id: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        as_of: datetime,
        code_version: str = "1.6.4",
        release_version: str = "1.6.4",
        metric_policy_version: str = "1.6.4",
        attribution_policy_version: str = "1.6.4",
    ) -> AnalyticsSnapshot:
        input_hash = _hash_dict(input_data)
        output_hash = _hash_dict(output_data)
        repro_hash = _hash_dict({
            "input": input_hash,
            "output": output_hash,
            "code_version": code_version,
            "metric_policy_version": metric_policy_version,
            "attribution_policy_version": attribution_policy_version,
        })
        now = datetime.now(tz=timezone.utc)
        return AnalyticsSnapshot(
            snapshot_id=str(uuid.uuid4()),
            analytics_id=analytics_id,
            session_id=session_id,
            input_hash=input_hash,
            output_hash=output_hash,
            reproducibility_hash=repro_hash,
            code_version=code_version,
            release_version=release_version,
            metric_policy_version=metric_policy_version,
            attribution_policy_version=attribution_policy_version,
            as_of=as_of,
            created_at=now,
        )


__all__ = ["AnalyticsSnapshotManager", "_hash_dict"]
