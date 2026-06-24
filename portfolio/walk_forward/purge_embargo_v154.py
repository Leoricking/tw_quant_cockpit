"""
portfolio/walk_forward/purge_embargo_v154.py — Purge & Embargo Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
import datetime
from typing import Dict, Any, Tuple

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
PURGE_EMBARGO_VERSION = "1.5.4"


def _parse(d: str) -> datetime.date:
    return datetime.date.fromisoformat(d)


def _fmt(d: datetime.date) -> str:
    return d.isoformat()


class PurgeEmbargoEngine:
    """Handles purge and embargo period calculations for walk-forward windows."""

    def __init__(self):
        self.version = PURGE_EMBARGO_VERSION

    def apply_purge(self, training_end: str, purge_days: int) -> Dict[str, Any]:
        """
        Apply purge period after training_end.
        Returns dict with purge_start, purge_end, errors.
        """
        errors = []
        if purge_days < 0:
            errors.append(f"purge_days must be >= 0, got {purge_days}")
            return {"purge_start": training_end, "purge_end": training_end, "errors": errors}

        train_end = _parse(training_end)
        purge_start = train_end + datetime.timedelta(days=1)
        purge_end = train_end + datetime.timedelta(days=purge_days) if purge_days > 0 else train_end

        if purge_end < purge_start - datetime.timedelta(days=1):
            errors.append("purge_end before purge_start — reversed dates")

        return {
            "purge_start": _fmt(purge_start),
            "purge_end": _fmt(purge_end),
            "purge_days": purge_days,
            "errors": errors,
        }

    def apply_embargo(self, validation_end: str, embargo_days: int) -> Dict[str, Any]:
        """
        Apply embargo period after validation_end.
        Returns dict with embargo_end, errors.
        """
        errors = []
        if embargo_days < 0:
            errors.append(f"embargo_days must be >= 0, got {embargo_days}")
            return {"embargo_end": validation_end, "errors": errors}

        val_end = _parse(validation_end)
        embargo_end = val_end + datetime.timedelta(days=embargo_days)

        return {
            "embargo_end": _fmt(embargo_end),
            "embargo_days": embargo_days,
            "errors": errors,
        }

    def validate_no_overlap(self, purge_end: str, validation_start: str) -> Dict[str, Any]:
        """Validate that purge period does not overlap with validation."""
        pe = _parse(purge_end)
        vs = _parse(validation_start)
        if pe >= vs:
            return {
                "valid": False,
                "error": f"purge_end ({purge_end}) overlaps with validation_start ({validation_start})"
            }
        return {"valid": True, "error": None}

    def validate_range(self, start: str, end: str, label: str = "period") -> Dict[str, Any]:
        """Validate a date range is not reversed."""
        s = _parse(start)
        e = _parse(end)
        if s > e:
            return {"valid": False, "error": f"{label}: start ({start}) after end ({end})"}
        return {"valid": True, "error": None}
