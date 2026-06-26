"""
paper_trading/analytics/regime_context_v164.py — Regime Context v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


@dataclass
class RegimeContextRecord:
    """Regime context for a session window."""
    session_id: str
    regime_id: Optional[str] = None
    regime_label: Optional[str] = None
    regime_duration_ratio: Optional[Decimal] = None
    regime_transitions: int = 0
    regime_distribution: Dict[str, Decimal] = field(default_factory=dict)
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True


class RegimeContextComputer:

    def compute(
        self,
        session_id: str,
        regime_events: List[Dict[str, Any]],
        total_seconds: Optional[Decimal] = None,
    ) -> RegimeContextRecord:
        distribution: Dict[str, Decimal] = {}
        transitions = max(0, len(regime_events) - 1)

        for ev in regime_events:
            label = ev.get("regime_label", "UNKNOWN")
            secs = Decimal(str(ev.get("duration_seconds", 0)))
            distribution[label] = distribution.get(label, Decimal("0")) + secs

        # Normalize
        total_dur = sum(distribution.values(), Decimal("0"))
        if total_dur > Decimal("0"):
            distribution = {k: v / total_dur for k, v in distribution.items()}

        dominant = max(distribution, key=lambda k: distribution[k]) if distribution else None

        return RegimeContextRecord(
            session_id=session_id,
            regime_label=dominant,
            regime_transitions=transitions,
            regime_distribution=distribution,
            quality=MetricQuality.VALID if regime_events else MetricQuality.INSUFFICIENT_DATA,
        )


__all__ = ["RegimeContextRecord", "RegimeContextComputer"]
