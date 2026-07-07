"""
paper_trading/small_capital_strategy/buy_point_rules_v170.py
Buy point rules for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.enums_v170 import (
    BuyPointType, ThemeStrength, ForbiddenTradeReason, EntryPlanStatus,
)

# ── A: 10MA Pullback Required Conditions ────────────────────────────────────
A_REQUIRED_CONDITIONS = [
    "theme_strength >= STRONG",
    "close > MA20",
    "close > MA60",
    "low <= MA10",
    "close >= MA10",
    "volume_contracting == True",
    "KD not dead cross",
    "institutional_not_net_selling == True",
    "financing_not_overheated == True",
]

# ── B: Platform Breakout Required Conditions ─────────────────────────────────
B_REQUIRED_CONDITIONS = [
    "consolidation_weeks in [2, 6]",
    "close > prior_platform_high",
    "volume_ratio >= 1.5",
    "not third_extended_red_candle",
    "financing_not_overheated == True",
    "market_regime != BEAR",
]

# ── C: 20MA Reclaim Second Wave Required Conditions ──────────────────────────
C_REQUIRED_CONDITIONS = [
    "had_first_wave == True",
    "pullback_completed == True",
    "close reclaims MA20",
    "volume_dry_up_before_reclaim == True",
    "KD golden cross or improving",
    "institutional_reaccumulation == True",
]


def check_a_buy_point(signal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate A buy point (10MA pullback). Returns evaluation dict.
    All conditions checked; missing conditions listed.
    """
    missing = []
    required = list(A_REQUIRED_CONDITIONS)
    forbidden = []

    theme_strength = signal.get("theme_strength", "NONE")
    if theme_strength not in ("STRONG",):
        missing.append("theme_strength >= STRONG")
        forbidden.append(ForbiddenTradeReason.WEAK_THEME)

    if not signal.get("close_gt_ma20", False):
        missing.append("close > MA20")
        forbidden.append(ForbiddenTradeReason.BELOW_20MA)

    if not signal.get("close_gt_ma60", False):
        missing.append("close > MA60")
        forbidden.append(ForbiddenTradeReason.BELOW_60MA)

    if not signal.get("low_lte_ma10", False):
        missing.append("low <= MA10")

    if not signal.get("close_gte_ma10", False):
        missing.append("close >= MA10")

    if not signal.get("volume_contracting", False):
        missing.append("volume_contracting == True")

    if signal.get("kd_dead_cross", False):
        missing.append("KD not dead cross")

    if not signal.get("institutional_not_net_selling", False):
        missing.append("institutional_not_net_selling == True")

    if signal.get("financing_overheated", False):
        missing.append("financing_not_overheated == True")
        forbidden.append(ForbiddenTradeReason.FINANCING_OVERHEATED)

    passed = len(missing) == 0
    status = EntryPlanStatus.VALID if passed else EntryPlanStatus.BLOCKED

    return {
        "buy_point_type": BuyPointType.A_10MA_PULLBACK.value,
        "passed": passed,
        "status": status.value,
        "required_conditions": required,
        "missing_conditions": missing,
        "forbidden_reasons": [r.value for r in forbidden],
        "entry": "near MA10 reclaim",
        "stop": "below MA10 or recent swing low",
        "add": "reclaim MA5 or break prior high",
    }


def check_b_buy_point(signal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate B buy point (platform breakout). Returns evaluation dict.
    """
    missing = []
    required = list(B_REQUIRED_CONDITIONS)
    forbidden = []

    weeks = signal.get("consolidation_weeks", 0)
    if not (2 <= weeks <= 6):
        missing.append(f"consolidation_weeks in [2, 6] (got {weeks})")

    if not signal.get("close_gt_platform_high", False):
        missing.append("close > prior_platform_high")

    volume_ratio = signal.get("volume_ratio", 0.0)
    if volume_ratio < 1.5:
        missing.append(f"volume_ratio >= 1.5 (got {volume_ratio})")

    if signal.get("third_extended_red_candle", False):
        missing.append("not third_extended_red_candle")
        forbidden.append(ForbiddenTradeReason.LEGAL_OR_SAFETY_BLOCKED)

    if signal.get("financing_overheated", False):
        missing.append("financing_not_overheated == True")
        forbidden.append(ForbiddenTradeReason.FINANCING_OVERHEATED)

    regime = signal.get("market_regime", "UNKNOWN")
    if regime == "BEAR":
        missing.append("market_regime != BEAR")
        forbidden.append(ForbiddenTradeReason.MARKET_BEAR_NON_CORE)

    passed = len(missing) == 0
    status = EntryPlanStatus.VALID if passed else EntryPlanStatus.BLOCKED

    return {
        "buy_point_type": BuyPointType.B_PLATFORM_BREAKOUT.value,
        "passed": passed,
        "status": status.value,
        "required_conditions": required,
        "missing_conditions": missing,
        "forbidden_reasons": [r.value for r in forbidden],
        "entry": "breakout confirmation",
        "stop": "platform upper bound or breakout day low",
        "add": "second-day hold / retest hold",
    }


def check_c_buy_point(signal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate C buy point (20MA second wave). Returns evaluation dict.
    """
    missing = []
    required = list(C_REQUIRED_CONDITIONS)
    forbidden = []

    if not signal.get("had_first_wave", False):
        missing.append("had_first_wave == True")

    if not signal.get("pullback_completed", False):
        missing.append("pullback_completed == True")

    if not signal.get("close_reclaims_ma20", False):
        missing.append("close reclaims MA20")
        forbidden.append(ForbiddenTradeReason.BELOW_20MA)

    if not signal.get("volume_dry_up_before_reclaim", False):
        missing.append("volume_dry_up_before_reclaim == True")

    if not signal.get("kd_golden_cross_or_improving", False):
        missing.append("KD golden cross or improving")

    if not signal.get("institutional_reaccumulation", False):
        missing.append("institutional_reaccumulation == True")

    passed = len(missing) == 0
    status = EntryPlanStatus.VALID if passed else EntryPlanStatus.BLOCKED

    return {
        "buy_point_type": BuyPointType.C_20MA_RECLAIM.value,
        "passed": passed,
        "status": status.value,
        "required_conditions": required,
        "missing_conditions": missing,
        "forbidden_reasons": [r.value for r in forbidden],
        "entry": "MA20 reclaim",
        "stop": "below MA20",
        "add": "break reaction high",
    }


def evaluate_buy_point(buy_point_type: BuyPointType, signal: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch to the appropriate buy point checker."""
    if buy_point_type == BuyPointType.A_10MA_PULLBACK:
        return check_a_buy_point(signal)
    if buy_point_type == BuyPointType.B_PLATFORM_BREAKOUT:
        return check_b_buy_point(signal)
    if buy_point_type == BuyPointType.C_20MA_RECLAIM:
        return check_c_buy_point(signal)
    return {
        "buy_point_type": BuyPointType.UNSUPPORTED.value,
        "passed": False,
        "status": EntryPlanStatus.BLOCKED.value,
        "required_conditions": [],
        "missing_conditions": ["unsupported buy point type"],
        "forbidden_reasons": [],
    }
