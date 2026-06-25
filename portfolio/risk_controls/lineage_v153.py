"""
portfolio/risk_controls/lineage_v153.py — Drawdown Risk Controls Lineage Tracking v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownRiskControlsLineageTracker:
    """Tracks lineage for drawdown & risk controls evaluations."""

    RESEARCH_ONLY = True

    def build_lineage(
        self,
        evaluation,
        equity_curve_hash: str = "",
        source_lineage: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Build lineage record for a risk controls evaluation."""
        source_lineage = source_lineage or {}
        evaluation_id = getattr(evaluation, "evaluation_id", "")
        portfolio_id  = getattr(evaluation, "portfolio_id", "")
        as_of         = getattr(evaluation, "as_of", "")

        return {
            "lineage_valid":      True,
            "evaluation_id":      evaluation_id,
            "portfolio_id":       portfolio_id,
            "as_of":              as_of,
            "equity_curve_hash":  equity_curve_hash,
            "source_lineage":     source_lineage,
            "generated_at":       datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "research_only":      True,
            "module_version":     MODULE_VERSION,
        }
