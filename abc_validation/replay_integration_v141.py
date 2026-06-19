"""
abc_validation/replay_integration_v141.py — Replay integration for A/B/C validation v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Read-only evidence provider for Replay v1.2.9.
NEVER modifies Replay session scores, challenge questions, rule parameters, or old registry.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ABCReplayIntegration:
    """
    Read-only evidence provider for Replay v1.2.9.

    Can provide: empirical validation summary, signal outcome taxonomy,
    historical false-signal examples, regime-specific evidence,
    confidence, formal conclusion status.

    NEVER modifies: Replay session scores, challenge questions,
    rule parameters, old registry.
    """

    # Safety flags
    MODIFIES_REPLAY_SESSIONS = False
    MODIFIES_CHALLENGE_QUESTIONS = False
    MODIFIES_RULE_PARAMETERS = False
    MODIFIES_REGISTRY = False
    READ_ONLY = True

    def get_evidence_summary(
        self,
        buy_point_type: str,
        validation_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Get empirical validation summary for Replay evidence display."""
        if validation_result is None:
            return {
                "buy_point_type": buy_point_type,
                "evidence_available": False,
                "note": "No validation result provided.",
                "read_only": True,
                "modifies_replay": False,
            }

        return {
            "buy_point_type": buy_point_type,
            "evidence_available": True,
            "validation_id": validation_result.get("validation_id"),
            "signal_count": validation_result.get("signal_count", 0),
            "trade_count": validation_result.get("trade_count", 0),
            "confidence": validation_result.get("confidence", "INSUFFICIENT"),
            "formal_conclusion_allowed": validation_result.get("formal_conclusion_allowed", False),
            "outcome_distribution": validation_result.get("outcome_distribution", {}),
            "read_only": True,
            "modifies_replay": False,
        }

    def get_false_signal_examples(
        self,
        buy_point_type: str,
        signals: Optional[List[dict]] = None,
        n_examples: int = 5,
    ) -> List[dict]:
        """Get historical false-signal examples for training reference."""
        signals = signals or []
        false_signals = [
            s for s in signals
            if s.get("classification", "").endswith("FAILED_SUPPORT")
            or s.get("outcome", "").startswith("FALSE_")
        ]
        return false_signals[:n_examples]

    def get_regime_evidence(
        self,
        buy_point_type: str,
        regime: str,
        validation_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Get regime-specific evidence for a buy point type."""
        if validation_result is None:
            return {
                "buy_point_type": buy_point_type,
                "regime": regime,
                "evidence_available": False,
                "read_only": True,
            }

        regime_results = validation_result.get("regime_results", {})
        regime_data = regime_results.get(regime, {})

        return {
            "buy_point_type": buy_point_type,
            "regime": regime,
            "evidence_available": bool(regime_data),
            "win_rate": regime_data.get("win_rate"),
            "expectancy": regime_data.get("expectancy"),
            "trade_count": regime_data.get("trade_count", 0),
            "confidence": regime_data.get("confidence", "INSUFFICIENT"),
            "read_only": True,
            "modifies_replay": False,
        }
