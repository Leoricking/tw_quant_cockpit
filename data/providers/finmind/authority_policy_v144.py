"""
data/providers/finmind/authority_policy_v144.py — FinMind authority policy v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SECONDARY_AGGREGATOR → formal conclusion blocked by default.
[!] Primary source always wins conflict.
[!] can_override_primary_provider = False.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False
FINMIND_REALTIME_FORMAL_USE_ALLOWED = False
FINMIND_SECONDARY_AGGREGATOR = True


class FinMindAuthorityPolicy:
    """
    Enforces authority policy for FinMind as a SECONDARY_AGGREGATOR.
    Formal use is blocked by default. Primary source always wins.
    """

    AUTHORITATIVE_LEVEL = "SECONDARY_AGGREGATOR"
    FORMAL_USE_ALLOWED_DEFAULT = False
    CAN_OVERRIDE_PRIMARY = False

    def check_formal_use_allowed(
        self,
        dataset: str,
        pit_class: str,
        has_primary_data: bool,
        primary_conflict: bool,
    ) -> Dict[str, Any]:
        """
        Determine if formal use is allowed for this dataset/context.

        Rules:
        - SECONDARY_AGGREGATOR → formal conclusion blocked by default
        - Primary source always wins conflict
        - UNKNOWN PIT class → blocked
        - primary_conflict → blocked (primary source wins)

        Returns dict with: allowed (bool), reason, authoritative_level, dataset
        """
        if primary_conflict:
            return {
                "allowed": False,
                "reason": "Primary source conflict — primary source wins. FinMind data preserved as secondary evidence only.",
                "authoritative_level": self.AUTHORITATIVE_LEVEL,
                "dataset": dataset,
                "pit_class": pit_class,
                "has_primary_data": has_primary_data,
            }

        if pit_class == "UNKNOWN":
            return {
                "allowed": False,
                "reason": "PIT class UNKNOWN — formal historical conclusion blocked.",
                "authoritative_level": self.AUTHORITATIVE_LEVEL,
                "dataset": dataset,
                "pit_class": pit_class,
                "has_primary_data": has_primary_data,
            }

        if has_primary_data:
            return {
                "allowed": False,
                "reason": "Primary source data available — FinMind is secondary supplement only.",
                "authoritative_level": self.AUTHORITATIVE_LEVEL,
                "dataset": dataset,
                "pit_class": pit_class,
                "has_primary_data": has_primary_data,
            }

        # No primary data, no conflict, known PIT class — still SECONDARY_AGGREGATOR
        return {
            "allowed": False,
            "reason": "SECONDARY_AGGREGATOR — formal conclusion blocked by default even without primary data.",
            "authoritative_level": self.AUTHORITATIVE_LEVEL,
            "dataset": dataset,
            "pit_class": pit_class,
            "has_primary_data": has_primary_data,
        }

    def get_policy_summary(self) -> Dict[str, Any]:
        return {
            "authoritative_level": self.AUTHORITATIVE_LEVEL,
            "formal_use_allowed_default": self.FORMAL_USE_ALLOWED_DEFAULT,
            "can_override_primary": self.CAN_OVERRIDE_PRIMARY,
            "realtime_formal_use_allowed": FINMIND_REALTIME_FORMAL_USE_ALLOWED,
            "no_real_orders": True,
            "broker_execution_enabled": False,
        }
