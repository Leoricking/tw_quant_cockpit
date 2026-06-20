"""
strategy_robustness/replay_integration_v142.py — Replay integration for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Read-only evidence for Replay v1.2.9. NEVER modifies Replay session scores,
    challenge questions, or rule parameters.
"""
from __future__ import annotations

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Hard safety flags — never modify these
REPLAY_SCORE_MODIFICATION_ENABLED = False
REPLAY_CHALLENGE_MODIFICATION_ENABLED = False
RULE_PARAMETER_MODIFICATION_ENABLED = False


class RobustnessReplayIntegration:
    """
    Provides read-only robustness evidence for Replay sessions.
    NEVER modifies Replay session scores, challenge questions, or rule parameters.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir
        self._store = None

    def _get_store(self):
        if self._store is None:
            from strategy_robustness.store_v142 import StrategyRobustnessStore
            self._store = StrategyRobustnessStore(base_dir=self.base_dir)
        return self._store

    def get_evidence_for_rule(self, rule_id: str) -> dict:
        """
        Return read-only robustness evidence for a rule.
        Safe to pass to Replay session as context — does not modify anything.

        Parameters
        ----------
        rule_id : str

        Returns
        -------
        dict with robustness_score, regime_dependency, parameter_sensitivity,
               cost_sensitivity, decay_status, formal_conclusion_status
        """
        results = self._get_store().list_by_rule(rule_id)
        if not results:
            return {
                "rule_id": rule_id,
                "robustness_score": None,
                "regime_dependency": None,
                "parameter_sensitivity": None,
                "cost_sensitivity": None,
                "decay_status": None,
                "formal_conclusion_status": "NO_ROBUSTNESS_DATA",
                "read_only": True,
                "modifies_replay": False,
                "modifies_session_score": False,
                "modifies_challenge_questions": False,
                "modifies_rule_parameters": False,
            }

        # Use most recent result
        latest = sorted(results, key=lambda r: r.get("created_at", ""), reverse=True)[0]
        from strategy_robustness.models_v142 import DecayStatus

        return {
            "rule_id": rule_id,
            "robustness_score": latest.get("overall_score"),
            "regime_dependency": latest.get("regime_robustness", {}).get("regime_dependency_score"),
            "parameter_sensitivity": latest.get("parameter_sensitivity", {}).get("status"),
            "cost_sensitivity": latest.get("cost_stress", {}).get("status"),
            "decay_status": latest.get("decay", {}).get("decay_status", DecayStatus.UNKNOWN),
            "formal_conclusion_status": "ALLOWED" if latest.get("formal_conclusion_allowed") else "BLOCKED",
            "robustness_status": latest.get("robustness_status"),
            "read_only": True,
            "modifies_replay": False,
            "modifies_session_score": False,
            "modifies_challenge_questions": False,
            "modifies_rule_parameters": False,
        }
