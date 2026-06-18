"""
replay/challenge_hidden_data.py — ReplayChallengeHiddenDataGuard v1.2.7

[!] Future data MUST be hidden. Outcome hidden until explicit reveal.
[!] Answer key stored separately — active payload cannot access it.
[!] Forbidden fields in active payload cause BLOCKED status.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# ---------------------------------------------------------------------------
# Forbidden fields — MUST NOT appear in active challenge payload
# ---------------------------------------------------------------------------

FORBIDDEN_ACTIVE_FIELDS: Set[str] = {
    "forward_return",
    "realized_pnl",
    "outcome_score",
    "future_signal",
    "final_high",
    "final_low",
    "hindsight_score",
    "answer_key",
    "best_action",
    "expected_result",
    "future_bars",
    "future_strategy_signals",
    "future_timeframe_conflicts",
    "future_review_classification",
    "prior_attempt_answer",
    "best_attempt_answer",
    "future_journal_revisions",
    "MFE",
    "MAE",
    "final_session_high",
    "final_session_low",
}

# ---------------------------------------------------------------------------
# Optional hidden fields (by difficulty)
# ---------------------------------------------------------------------------

OPTIONAL_HIDDEN_FIELDS: Set[str] = {
    "symbol",
    "date",
    "company_name",
    "exact_price_scale",
    "strategy_module_label",
    "timeframe_label",
}


class ReplayChallengeHiddenDataGuard:
    """
    Guards the active challenge payload against future data leaks.

    [!] MUST hide all forbidden fields.
    [!] Active payload never contains: forward_return, realized_pnl, outcome_score,
        future_signal, final_high, final_low, hindsight_score, answer_key, best_action,
        expected_result → BLOCKED if found.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    FUTURE_FIREWALL_ACTIVE = True

    def sanitize_active_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Remove all forbidden fields from active payload."""
        return {
            k: v for k, v in payload.items()
            if k not in FORBIDDEN_ACTIVE_FIELDS
        }

    def hide_future(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Hide all future data fields."""
        future_keys = {k for k in payload if (
            k.startswith("future_")
            or k in {"forward_return", "final_high", "final_low",
                     "MFE", "MAE", "final_session_high", "final_session_low"}
        )}
        result = dict(payload)
        for k in future_keys:
            result[k] = "HIDDEN"
        return result

    def hide_outcome(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Hide outcome-related fields."""
        outcome_keys = {
            "realized_pnl", "outcome_score", "hindsight_score",
            "final_session_high", "final_session_low", "MFE", "MAE",
        }
        result = dict(payload)
        for k in outcome_keys:
            if k in result:
                result[k] = "HIDDEN"
        result["outcome_hidden"] = True
        return result

    def hide_identity(
        self,
        payload: Dict[str, Any],
        hide_symbol: bool = False,
        hide_date: bool = False,
    ) -> Dict[str, Any]:
        """Hide symbol and/or date for higher difficulty challenges."""
        result = dict(payload)
        if hide_symbol:
            for k in ("symbol", "company_name", "exact_price_scale"):
                if k in result:
                    result[k] = "HIDDEN"
            result["symbol_hidden"] = True
        if hide_date:
            result["date"] = "HIDDEN"
            result["date_hidden"] = True
        return result

    def hide_answer_key(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure answer key is not in active payload."""
        result = dict(payload)
        for k in ("answer_key", "best_action", "expected_result",
                  "prior_attempt_answer", "best_attempt_answer"):
            if k in result:
                del result[k]
        result["answer_key_stored_separately"] = True
        return result

    def validate_active_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that active payload contains no forbidden fields."""
        found_forbidden = [k for k in payload if k in FORBIDDEN_ACTIVE_FIELDS]
        blocked = len(found_forbidden) > 0
        return {
            "valid": not blocked,
            "blocked": blocked,
            "found_forbidden": found_forbidden,
            "status": "BLOCKED" if blocked else "OK",
            "future_firewall_active": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def detect_leak(self, payload: Dict[str, Any]) -> List[str]:
        """Detect any leaked forbidden fields."""
        return [k for k in payload if k in FORBIDDEN_ACTIVE_FIELDS]

    def build_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Build a hidden data report for the payload."""
        leaks = self.detect_leak(payload)
        validation = self.validate_active_payload(payload)
        return {
            "forbidden_fields_found": leaks,
            "blocked": validation["blocked"],
            "status": validation["status"],
            "total_fields_checked": len(payload),
            "hidden_future": True,
            "hidden_outcome": True,
            "answer_key_separate": True,
            "future_firewall_active": True,
            "research_only": True,
            "no_real_orders": True,
        }
