"""
portfolio/risk_controls/point_in_time_v153.py — Drawdown Risk Controls PIT Validator v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownRiskControlsPITValidator:
    """Point-in-time validator for drawdown & risk controls."""

    RESEARCH_ONLY = True

    def validate_equity_curve(
        self,
        equity_curve: List[Any],
        as_of: str,
    ) -> Dict[str, Any]:
        """Ensure no equity curve point is dated beyond as_of."""
        future_dates: List[str] = []
        for pt in equity_curve:
            date = getattr(pt, "date", "")
            if date and date > as_of:
                future_dates.append(date)

        valid = len(future_dates) == 0
        return {
            "valid": valid,
            "as_of": as_of,
            "future_dates_found": future_dates,
            "errors": [f"Future date in equity curve: {d}" for d in future_dates],
        }

    def validate_as_of(self, as_of: str) -> Dict[str, Any]:
        """Validate the as_of date format."""
        import datetime
        errors: List[str] = []
        try:
            datetime.date.fromisoformat(as_of)
        except (ValueError, TypeError):
            errors.append(f"Invalid as_of date: {as_of!r}")

        return {"valid": len(errors) == 0, "errors": errors}
