"""
portfolio/risk_controls/validation_v153.py — Drawdown & Risk Controls Validation v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
VALIDATION_VERSION = "1.5.3"


def validate_drawdown_request(request) -> Dict[str, Any]:
    """Validate a DrawdownAnalysisRequest. Returns {valid, errors, warnings}."""
    errors: List[str] = []
    warnings: List[str] = []

    if not getattr(request, "research_only", False):
        errors.append("research_only must be True")

    if not getattr(request, "portfolio_id", ""):
        errors.append("portfolio_id is required")

    if not getattr(request, "as_of", ""):
        errors.append("as_of is required")

    lookback = getattr(request, "lookback_days", 0)
    if lookback < 20:
        errors.append(f"lookback_days must be >= 20, got {lookback}")
    elif lookback < 60:
        warnings.append("lookback_days < 60 may produce unreliable statistics")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate_equity_curve(curve_points: List) -> Dict[str, Any]:
    """Validate an equity curve point list."""
    errors: List[str] = []
    if not curve_points:
        errors.append("equity_curve is empty")
    return {"valid": len(errors) == 0, "errors": errors}


def validate_risk_policy(policy) -> Dict[str, Any]:
    """Validate a RiskControlPolicy."""
    errors: List[str] = []
    if not getattr(policy, "research_only", False):
        errors.append("research_only must be True")
    if getattr(policy, "executable", True):
        errors.append("executable must be False")
    if getattr(policy, "order_created", True):
        errors.append("order_created must be False")
    if getattr(policy, "auto_applied", True):
        errors.append("auto_applied must be False")
    return {"valid": len(errors) == 0, "errors": errors}
