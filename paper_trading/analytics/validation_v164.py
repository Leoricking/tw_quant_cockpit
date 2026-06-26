"""
paper_trading/analytics/validation_v164.py — Analytics Validation v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional


NO_REAL_ORDERS = True
NO_BROKER = True
PAPER_ONLY = True


class PITViolation(Exception):
    """Raised when a value references data after as_of (point-in-time violation)."""


class MissingDataError(Exception):
    """Raised when required data is absent — never converted to 0 or healthy."""


class NaiveTimestampError(Exception):
    """Raised when a timestamp lacks timezone info."""


def require_aware(ts: datetime, field_name: str = "timestamp") -> None:
    """Ensure timestamp is timezone-aware."""
    if ts.tzinfo is None:
        raise NaiveTimestampError(f"{field_name} is naive (no tzinfo). Use UTC-aware timestamps.")


def require_pit(value_ts: datetime, as_of: datetime, field_name: str = "event") -> None:
    """Ensure value_ts is not after as_of (PIT safety)."""
    require_aware(value_ts, field_name)
    require_aware(as_of, "as_of")
    if value_ts > as_of:
        raise PITViolation(
            f"{field_name} ({value_ts.isoformat()}) is after as_of ({as_of.isoformat()}). "
            f"Future data is not allowed."
        )


def require_not_missing(value: Any, field_name: str) -> None:
    """Raise MissingDataError if value is None — never default to 0."""
    if value is None:
        raise MissingDataError(
            f"{field_name} is missing. Missing data must not be treated as 0 or healthy."
        )


def validate_score(score: Any, field_name: str) -> Decimal:
    """Validate score is 0-100 Decimal."""
    d = Decimal(str(score))
    if d < Decimal("0") or d > Decimal("100"):
        raise ValueError(f"{field_name}={d} out of range [0, 100]")
    return d


def validate_attribution_reconciliation(
    gross: Decimal,
    components: List[Decimal],
    residual_threshold: Decimal = Decimal("0.01"),
    label: str = "attribution",
) -> Dict[str, Any]:
    """
    Validate attribution components sum to gross within threshold.
    Returns dict with residual, valid, quality.
    """
    total = sum(components, Decimal("0"))
    residual = abs(gross - total)
    valid = residual <= residual_threshold
    from paper_trading.analytics.enums_v164 import MetricQuality
    if valid:
        quality = MetricQuality.VALID
    elif residual <= residual_threshold * Decimal("10"):
        quality = MetricQuality.PARTIAL
    else:
        quality = MetricQuality.INVALID
    return {
        "gross": gross,
        "total_components": total,
        "residual": residual,
        "residual_threshold": residual_threshold,
        "valid": valid,
        "quality": quality,
        "label": label,
    }


def validate_no_duplicate_events(event_ids: List[str]) -> List[str]:
    """Return list of duplicate event IDs."""
    seen: set = set()
    dups: List[str] = []
    for eid in event_ids:
        if eid in seen:
            dups.append(eid)
        seen.add(eid)
    return dups


def validate_ordering(timestamps: List[datetime]) -> List[int]:
    """Return indices where ordering is violated (out-of-order)."""
    violations: List[int] = []
    for i in range(1, len(timestamps)):
        if timestamps[i] < timestamps[i - 1]:
            violations.append(i)
    return violations


__all__ = [
    "PITViolation", "MissingDataError", "NaiveTimestampError",
    "require_aware", "require_pit", "require_not_missing",
    "validate_score", "validate_attribution_reconciliation",
    "validate_no_duplicate_events", "validate_ordering",
]
