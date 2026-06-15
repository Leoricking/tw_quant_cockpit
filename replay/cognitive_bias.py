"""
replay/cognitive_bias.py — CognitiveBiasRegistry for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Bias flags are SELF-REPORTED or explicit rule-triggered only.
[!] No psychological diagnosis. No performance inference.
[!] No auto-scoring based on future results.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class CognitiveBiasRegistry:
    """
    Registry of known cognitive bias flags for replay training.

    [!] Flags are self-reported or explicit rule-triggered only.
    [!] NOT inferred from performance. NOT a psychological diagnosis.
    [!] Only known bias names accepted.
    """

    no_real_orders = True
    research_only = True

    KNOWN_BIASES = [
        "CONFIRMATION_BIAS",
        "RECENCY_BIAS",
        "ANCHORING_BIAS",
        "LOSS_AVERSION",
        "OVERCONFIDENCE",
        "FOMO",
        "PANIC_SELL",
        "CHASING_PERFORMANCE",
        "SUNK_COST",
        "HINDSIGHT_BIAS",
        "DISPOSITION_EFFECT",
        "GAMBLER_FALLACY",
        "REVENGE_TRADING",
        "ANCHORING",
        "HERDING",
        "ACTION_BIAS",
        "UNKNOWN",
    ]

    BIAS_DESCRIPTIONS = {
        "CONFIRMATION_BIAS": "Tendency to search for information confirming pre-existing beliefs",
        "RECENCY_BIAS": "Overweighting recent events compared to historical patterns",
        "ANCHORING_BIAS": "Over-relying on first piece of information encountered",
        "LOSS_AVERSION": "Tendency to prefer avoiding losses over acquiring equivalent gains",
        "OVERCONFIDENCE": "Excessive confidence in one's own accuracy of assessment",
        "FOMO": "Fear of missing out — acting out of anxiety about missing an opportunity",
        "PANIC_SELL": "Selling driven by fear rather than analysis",
        "CHASING_PERFORMANCE": "Buying after strong recent performance expecting it to continue",
        "SUNK_COST": "Continuing a behavior due to previously invested resources",
        "HINDSIGHT_BIAS": "Tendency to see past events as predictable after the fact",
        "DISPOSITION_EFFECT": "Tendency to sell winners too early and hold losers too long",
        "GAMBLER_FALLACY": "Believing past random events influence future probability",
        "REVENGE_TRADING": "Making impulsive trades to recover recent losses",
        "ANCHORING": "Over-relying on initial price or value as reference",
        "HERDING": "Following the crowd without independent analysis",
        "ACTION_BIAS": "Tendency to act even when inaction is better",
        "UNKNOWN": "Unspecified cognitive bias",
    }

    def flag_bias(
        self, bias_name: str, triggered_by: str = "user_self_reported"
    ) -> Dict[str, Any]:
        """
        Create a bias flag.
        [!] Only known bias names accepted.
        [!] triggered_by must be 'user_self_reported' or explicit rule name.
        """
        if bias_name not in self.KNOWN_BIASES:
            raise ValueError(
                f"Unknown bias name: '{bias_name}'. "
                f"Known biases: {self.KNOWN_BIASES}"
            )
        return {
            "bias_name": bias_name,
            "triggered_by": triggered_by,
            "description": self.BIAS_DESCRIPTIONS.get(bias_name, ""),
            "self_reported": triggered_by == "user_self_reported",
            "simulation_only": True,
        }

    def create_flags(
        self, bias_names: List[str], triggered_by: str = "user_self_reported"
    ) -> List[Dict[str, Any]]:
        """Create multiple bias flags."""
        return [self.flag_bias(name, triggered_by) for name in bias_names]

    def validate_flags(self, flags: List[str]) -> Dict[str, Any]:
        """Validate a list of bias flag names."""
        invalid = [f for f in flags if f not in self.KNOWN_BIASES]
        return {
            "valid": len(invalid) == 0,
            "invalid_flags": invalid,
            "known_biases": self.KNOWN_BIASES,
        }

    def explain_flag(self, bias_name: str) -> str:
        """Explain a bias flag."""
        if bias_name not in self.KNOWN_BIASES:
            return f"Unknown bias: {bias_name}"
        return self.BIAS_DESCRIPTIONS.get(bias_name, "No description available")

    def list_for_entry(self, entry_dict: Dict[str, Any]) -> List[str]:
        """Get bias flags from a journal entry."""
        return entry_dict.get("cognitive_bias_flags", [])

    def summary(self, flag_lists: List[List[str]]) -> Dict[str, int]:
        """Count occurrences of each bias across multiple entries."""
        counts: Dict[str, int] = {}
        for flags in flag_lists:
            for f in flags:
                counts[f] = counts.get(f, 0) + 1
        return counts


# Backward-compat alias
CognitiveBiasFlagManager = CognitiveBiasRegistry
