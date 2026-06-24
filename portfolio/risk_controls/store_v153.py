"""
portfolio/risk_controls/store_v153.py — Immutable Risk Controls Store v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownRiskControlsStore:
    """
    Immutable in-memory store for risk controls evaluations.
    Research-only. No order table. No ledger write.
    """

    RESEARCH_ONLY = True

    def __init__(self, storage_path: str = ":memory:") -> None:
        self._storage_path = storage_path
        self._evaluations: Dict[str, Any] = {}  # evaluation_id -> evaluation
        self._drawdown_summaries: Dict[str, Any] = {}  # key -> summary

    def save_evaluation(self, evaluation) -> str:
        """Save a risk controls evaluation. Returns evaluation_id."""
        eid = getattr(evaluation, "evaluation_id", "")
        if not eid:
            raise ValueError("evaluation must have evaluation_id")
        if eid not in self._evaluations:
            self._evaluations[eid] = evaluation
        return eid

    def get_evaluation(self, evaluation_id: str):
        """Retrieve an evaluation by ID."""
        return self._evaluations.get(evaluation_id)

    def list_evaluations(self, portfolio_id: Optional[str] = None) -> List[Any]:
        """List all evaluations, optionally filtered by portfolio."""
        evals = list(self._evaluations.values())
        if portfolio_id:
            evals = [e for e in evals if getattr(e, "portfolio_id", "") == portfolio_id]
        return evals

    def save_drawdown_summary(self, summary, key: str = "") -> str:
        """Save a drawdown summary."""
        k = key or f"{getattr(summary, 'portfolio_id', '')}_{getattr(summary, 'as_of', '')}"
        if k not in self._drawdown_summaries:
            self._drawdown_summaries[k] = summary
        return k

    def get_drawdown_summary(self, key: str):
        """Retrieve a drawdown summary by key."""
        return self._drawdown_summaries.get(key)
