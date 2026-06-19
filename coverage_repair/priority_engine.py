"""coverage_repair/priority_engine.py — CoverageRepairPriorityEngine for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Deterministic scoring. No randomness. Score bounded 0-100.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

from coverage_repair.models_v133 import (
    CoverageRepairTask,
    RepairIssueType,
    RepairPriority,
    RepairTaskStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CoverageRepairPriorityEngine:
    """Deterministic priority scoring for coverage repair tasks.

    Returns (priority_label, score_0_100, reasons_dict) tuples.
    Score is always bounded to [0, 100].
    No randomness — same inputs always produce same output.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    no_real_orders = True
    production_trading_blocked = True

    # Base score by issue type
    _BASE_SCORES: Dict[str, float] = {
        RepairIssueType.SOURCE_CONFLICT:         70.0,
        RepairIssueType.MARKET_CONFLICT:         70.0,
        RepairIssueType.BLOCKED_DATA:            65.0,
        RepairIssueType.DUPLICATE_BAR:           65.0,
        RepairIssueType.DEMO_ONLY_DATA:          60.0,
        RepairIssueType.MALFORMED_RESPONSE:      60.0,
        RepairIssueType.MISSING_DATA:            50.0,
        RepairIssueType.PARTIAL_DATA:            45.0,
        RepairIssueType.STALE_DATA:              40.0,
        RepairIssueType.INSUFFICIENT_HISTORY:    45.0,
        RepairIssueType.PROVIDER_AUTH_REQUIRED:  45.0,
        RepairIssueType.PROVIDER_RATE_LIMITED:   35.0,
        RepairIssueType.PROVIDER_DISABLED:       40.0,
        RepairIssueType.UNAVAILABLE_SOURCE:      35.0,
        RepairIssueType.MISSING_INSTITUTIONAL:   40.0,
        RepairIssueType.MISSING_REVENUE:         35.0,
        RepairIssueType.MISSING_MARGIN:          35.0,
        RepairIssueType.MISSING_FINANCIAL:       35.0,
        RepairIssueType.MISSING_SHAREHOLDER:     30.0,
        RepairIssueType.MISSING_ETF_OVERLAP:     25.0,
        RepairIssueType.MISSING_TECHNICAL_INDICATOR: 30.0,
        RepairIssueType.CACHE_STALE:             30.0,
        RepairIssueType.CACHE_CORRUPTION:        35.0,
        RepairIssueType.INVALID_SCHEMA:          40.0,
        RepairIssueType.MISSING_BAR:             35.0,
        RepairIssueType.CORPORATE_ACTION_UNKNOWN: 40.0,
        RepairIssueType.MISSING_CAPABILITY:      25.0,
        RepairIssueType.UNKNOWN:                 20.0,
    }

    # Tier adjustments
    _TIER_ADJUSTMENTS: Dict[str, float] = {
        "CORE":     15.0,
        "core":     15.0,
        "RESEARCH": 5.0,
        "research": 5.0,
        "EXTENDED": -5.0,
        "extended": -5.0,
        "EXCLUDED": -10.0,
        "excluded": -10.0,
    }

    # Profile adjustments
    _PROFILE_ADJUSTMENTS: Dict[str, float] = {
        "precise_price": 15.0,
        "backtest":      12.0,
        "fundamental":   8.0,
        "research":      5.0,
        "overview":      2.0,
    }

    def score(self, task: CoverageRepairTask) -> Tuple[str, float, Dict[str, Any]]:
        """Compute priority label, score [0,100], and reason dict for a task.

        Returns: (priority_label, final_score, reasons)
        """
        reasons: Dict[str, Any] = {}

        # --- Base score ---
        base = self._BASE_SCORES.get(task.issue_type, 20.0)
        reasons["base_score"] = base

        # --- Tier adjustment ---
        tier_adj = self._TIER_ADJUSTMENTS.get(task.universe_tier, 0.0)
        reasons["tier_adjustment"] = tier_adj

        # --- Profile adjustment ---
        profile_adj = self._PROFILE_ADJUSTMENTS.get(task.profile, 0.0)
        reasons["profile_adjustment"] = profile_adj

        # --- Severity adjustment ---
        severity_adj = self._severity_adjustment(task, reasons)

        # --- Retryability adjustment ---
        retry_adj = 3.0 if task.retryable else 0.0
        reasons["retryability_adjustment"] = retry_adj

        # --- Age adjustment (attempt_count as proxy) ---
        age_adj = min(task.attempt_count * 2.0, 10.0)
        reasons["age_adjustment"] = age_adj

        # --- Final score ---
        raw = base + tier_adj + profile_adj + severity_adj + retry_adj + age_adj
        final = max(0.0, min(100.0, raw))
        reasons["final_score"] = final

        # --- Priority label ---
        priority = self._label(final)
        reasons["priority"] = priority

        return priority, final, reasons

    def _severity_adjustment(self, task: CoverageRepairTask, reasons: Dict[str, Any]) -> float:
        adj = 0.0
        issue = task.issue_type
        tier = (task.universe_tier or "").upper()
        profile = (task.profile or "").lower()

        # CRITICAL triggers (+25 to +30)
        if issue == RepairIssueType.SOURCE_CONFLICT:
            adj += 30.0
            reasons["severity_note"] = "SOURCE_CONFLICT blocks precise_price"
        elif issue == RepairIssueType.BLOCKED_DATA and profile in ("backtest", "precise_price", "fundamental"):
            adj += 30.0
            reasons["severity_note"] = f"BLOCKED_DATA blocks {profile}"
        elif issue == RepairIssueType.MARKET_CONFLICT:
            adj += 25.0
            reasons["severity_note"] = "MARKET_CONFLICT critical"
        elif issue == RepairIssueType.DUPLICATE_BAR:
            adj += 25.0
            reasons["severity_note"] = "DUPLICATE_BAR affects backtest"
        elif issue == RepairIssueType.DEMO_ONLY_DATA and profile in ("precise_price", "backtest"):
            adj += 30.0
            reasons["severity_note"] = f"DEMO_ONLY_DATA in {profile} profile"
        elif issue == RepairIssueType.MALFORMED_RESPONSE and profile in ("precise_price", "backtest"):
            adj += 30.0
            reasons["severity_note"] = "MALFORMED_RESPONSE in core price profile"
        elif tier == "CORE" and issue == RepairIssueType.MISSING_DATA:
            adj += 25.0
            reasons["severity_note"] = "CORE tier MISSING_DATA"

        # HIGH triggers (+10 to +20)
        elif tier == "CORE" and issue == RepairIssueType.STALE_DATA:
            adj += 20.0
            reasons["severity_note"] = "CORE tier STALE_DATA"
        elif tier == "CORE" and issue == RepairIssueType.PARTIAL_DATA:
            adj += 20.0
            reasons["severity_note"] = "CORE tier PARTIAL_DATA"
        elif profile in ("precise_price", "backtest") and issue == RepairIssueType.BLOCKED_DATA:
            adj += 20.0
            reasons["severity_note"] = f"{profile} profile blocked"
        elif issue == RepairIssueType.INSUFFICIENT_HISTORY:
            adj += 15.0
            reasons["severity_note"] = "INSUFFICIENT_HISTORY"
        elif issue == RepairIssueType.MISSING_INSTITUTIONAL and tier == "CORE":
            adj += 15.0
            reasons["severity_note"] = "MISSING_INSTITUTIONAL in CORE"
        elif issue == RepairIssueType.PROVIDER_AUTH_REQUIRED:
            adj += 10.0
            reasons["severity_note"] = "PROVIDER_AUTH_REQUIRED retryable path"

        # MEDIUM triggers (+5 to +10)
        elif tier == "RESEARCH" and issue == RepairIssueType.MISSING_DATA:
            adj += 10.0
            reasons["severity_note"] = "RESEARCH tier missing"
        elif tier == "RESEARCH" and issue == RepairIssueType.PARTIAL_DATA:
            adj += 10.0
            reasons["severity_note"] = "PARTIAL_DATA in RESEARCH"
        elif issue == RepairIssueType.MISSING_REVENUE and task.stale_fields:
            adj += 8.0
            reasons["severity_note"] = "MISSING_REVENUE stale fields"
        elif issue == RepairIssueType.CACHE_STALE:
            adj += 8.0
            reasons["severity_note"] = "CACHE_STALE with available source"
        elif issue == RepairIssueType.MISSING_TECHNICAL_INDICATOR and tier != "CORE":
            adj += 5.0
            reasons["severity_note"] = "non-core technical indicator missing"

        # LOW triggers (negative)
        elif tier in ("EXCLUDED", "excluded"):
            adj -= 10.0
            reasons["severity_note"] = "EXCLUDED tier"
        elif tier in ("EXTENDED", "extended"):
            adj -= 5.0
            reasons["severity_note"] = "EXTENDED tier optional"

        reasons["severity_adjustment"] = adj
        return adj

    def _label(self, score: float) -> str:
        if score >= 80.0:
            return RepairPriority.CRITICAL
        if score >= 60.0:
            return RepairPriority.HIGH
        if score >= 40.0:
            return RepairPriority.MEDIUM
        return RepairPriority.LOW
