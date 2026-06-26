"""
paper_trading/analytics/signal_quality_v164.py — Signal Quality Analysis v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
Post-event analysis only. No forward data used in real-time decisions.
No auto strategy changes.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
NO_BROKER = True
PAPER_ONLY = True
AUTO_STRATEGY_CHANGE_ENABLED = False

# Post-event forward analysis is labelled explicitly
POST_EVENT_ANALYSIS_ONLY = True


@dataclass
class SignalQualityMetrics:
    """
    Signal quality metrics.
    Forward return windows are POST_EVENT_ONLY — labelled explicitly.
    No auto strategy changes from this analysis.
    """
    session_id: str
    signal_count: Optional[int] = None
    accepted_count: Optional[int] = None
    rejected_count: Optional[int] = None
    duplicate_count: Optional[int] = None
    conflicting_count: Optional[int] = None
    stale_count: Optional[int] = None
    acceptance_rate: Optional[Decimal] = None
    rejection_rate: Optional[Decimal] = None
    signal_decay_detected: Optional[bool] = None
    regime_compatible_count: Optional[int] = None
    false_positive_proxy: Optional[Decimal] = None
    # Forward return windows — POST_EVENT_ONLY, never used in real-time
    forward_return_1d_post_event: Optional[Decimal] = None
    forward_return_5d_post_event: Optional[Decimal] = None
    max_favorable_excursion: Optional[Decimal] = None
    max_adverse_excursion: Optional[Decimal] = None
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    post_event_label: str = "POST_EVENT_ONLY"
    paper_only: bool = True
    auto_strategy_change: bool = False

    def validate_no_auto_change(self) -> None:
        if self.auto_strategy_change:
            raise ValueError(
                "auto_strategy_change is forbidden. "
                "Signal quality analysis must not auto-modify strategy."
            )


class SignalQualityAnalyzer:
    """Analyzes signal quality from session data."""

    def analyze(self, session_id: str, raw: Dict[str, Any]) -> SignalQualityMetrics:
        def _dec(key: str) -> Optional[Decimal]:
            v = raw.get(key)
            return Decimal(str(v)) if v is not None else None

        def _int(key: str) -> Optional[int]:
            v = raw.get(key)
            return int(v) if v is not None else None

        total = _int("signal_count")
        accepted = _int("accepted_count")
        rejected = _int("rejected_count")

        acceptance_rate: Optional[Decimal] = None
        rejection_rate: Optional[Decimal] = None
        if total and total > 0:
            if accepted is not None:
                acceptance_rate = Decimal(str(accepted)) / Decimal(str(total))
            if rejected is not None:
                rejection_rate = Decimal(str(rejected)) / Decimal(str(total))

        metrics = SignalQualityMetrics(
            session_id=session_id,
            signal_count=total,
            accepted_count=accepted,
            rejected_count=rejected,
            duplicate_count=_int("duplicate_count"),
            conflicting_count=_int("conflicting_count"),
            stale_count=_int("stale_count"),
            acceptance_rate=_dec("acceptance_rate") or acceptance_rate,
            rejection_rate=_dec("rejection_rate") or rejection_rate,
            signal_decay_detected=raw.get("signal_decay_detected"),
            regime_compatible_count=_int("regime_compatible_count"),
            false_positive_proxy=_dec("false_positive_proxy"),
            forward_return_1d_post_event=_dec("forward_return_1d"),
            forward_return_5d_post_event=_dec("forward_return_5d"),
            max_favorable_excursion=_dec("max_favorable_excursion"),
            max_adverse_excursion=_dec("max_adverse_excursion"),
            auto_strategy_change=False,
        )

        available = sum(1 for v in [metrics.signal_count, metrics.acceptance_rate] if v is not None)
        metrics.quality = MetricQuality.VALID if available == 2 else (
            MetricQuality.PARTIAL if available > 0 else MetricQuality.INSUFFICIENT_DATA
        )
        metrics.validate_no_auto_change()
        return metrics


__all__ = ["SignalQualityMetrics", "SignalQualityAnalyzer", "POST_EVENT_ANALYSIS_ONLY"]
