"""
portfolio/correlation/validation_v152.py — Request Validation v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY       = True
VALIDATION_VERSION  = "1.5.2"


def validate_correlation_request(req) -> Dict[str, Any]:
    """
    Validate a CorrelationAnalysisRequest.

    Returns:
        {"valid": bool, "errors": list[str]}
    """
    errors: List[str] = []

    # research_only must be True
    if getattr(req, "research_only", None) is not True:
        errors.append("research_only must be True")

    # minimum_observations >= 1
    min_obs = getattr(req, "minimum_observations", 0)
    if not isinstance(min_obs, int) or min_obs < 1:
        errors.append(f"minimum_observations must be >= 1, got {min_obs}")

    # lookback_days >= minimum_observations
    lookback = getattr(req, "lookback_days", 0)
    if not isinstance(lookback, int) or lookback < min_obs:
        errors.append(
            f"lookback_days ({lookback}) must be >= minimum_observations ({min_obs})"
        )

    # symbols: at least 2
    symbols = getattr(req, "symbols", [])
    if not isinstance(symbols, list) or len(symbols) < 2:
        errors.append(f"symbols must contain at least 2 entries, got {len(symbols) if isinstance(symbols, list) else type(symbols)}")

    # weights sum ≈ 1.0 (within 0.01)
    weights = getattr(req, "weights", {})
    if isinstance(weights, dict) and len(weights) > 0:
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            errors.append(
                f"weights must sum to ~1.0 (within 0.01), got {total:.6f}"
            )
    else:
        errors.append("weights must be a non-empty dict")

    # source_lineage_ids recommended
    lineage = getattr(req, "source_lineage_ids", [])
    if not lineage:
        errors.append("LINEAGE_MISSING: source_lineage_ids is empty")

    return {"valid": len(errors) == 0, "errors": errors}
