"""
Metrics Collector v1.6.3 — In-process, no external service.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional

from paper_trading.operations.enums_v163 import ManagedSessionType
from paper_trading.operations.models_v163 import SessionMetric, _new_id


class CollectionError(Exception):
    pass


class MetricsCollector:
    """
    In-process, append-only, idempotent metrics collector.

    Requirements:
    - injectable clock (default: UTC now)
    - no external service / no network
    - no real sleep
    - deterministic windows
    - duplicate observation (same metric_id) blocked
    - future timestamp blocked
    - timezone-naive timestamp blocked
    """

    def __init__(self, clock: Optional[Callable[[], datetime]] = None):
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._observations: List[SessionMetric] = []
        self._seen_ids: set = set()

    # ------------------------------------------------------------------
    def observe(
        self,
        metric_name:  str,
        session_id:   str,
        session_type: ManagedSessionType,
        value:        float,
        unit:         str = "",
        observed_at:  Optional[datetime] = None,
        metric_id:    Optional[str] = None,
        **kwargs,
    ) -> SessionMetric:
        ts = observed_at or self._clock()

        # Timezone-naive blocked
        if ts.tzinfo is None:
            raise CollectionError(f"Timezone-naive timestamp blocked for {metric_name}")

        # Future timestamp blocked
        now = self._clock()
        if ts > now:
            raise CollectionError(f"Future timestamp blocked for {metric_name}: {ts} > {now}")

        mid = metric_id or _new_id("m_")

        # Duplicate ID blocked
        if mid in self._seen_ids:
            raise CollectionError(f"Duplicate observation ID blocked: {mid}")

        obs = SessionMetric(
            metric_id=mid,
            metric_name=metric_name,
            session_id=session_id,
            session_type=session_type,
            value=value,
            unit=unit,
            observed_at=ts,
            metadata=kwargs,
        )
        self._observations.append(obs)
        self._seen_ids.add(mid)
        return obs

    def all_observations(self) -> List[SessionMetric]:
        return list(self._observations)

    def observations_for(self, session_id: str) -> List[SessionMetric]:
        return [o for o in self._observations if o.session_id == session_id]

    def observations_by_metric(self, metric_name: str) -> List[SessionMetric]:
        return [o for o in self._observations if o.metric_name == metric_name]

    def count(self) -> int:
        return len(self._observations)

    def reset(self):
        self._observations.clear()
        self._seen_ids.clear()


__all__ = ["MetricsCollector", "CollectionError"]
