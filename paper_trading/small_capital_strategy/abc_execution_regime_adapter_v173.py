"""
paper_trading/small_capital_strategy/abc_execution_regime_adapter_v173.py
Adapter linking ABC execution plan to market regime v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, Any

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimePermissionStatus, RegimeBlockReason,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeDetectionResult, ABCRegimePermission,
)
from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
    get_abc_regime_permission,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.abc_execution_regime_adapter_v173"


def adapt_regime_to_abc(
    detection: MarketRegimeDetectionResult,
    tier: str = "MAIN_THEME_SWING",
) -> Dict[str, Any]:
    """
    Adapt regime detection result to ABC execution plan constraints.
    Returns dict with abc_permission, tier, regime, blocked, block_reasons, note.
    Paper only.
    """
    regime = detection.regime
    abc_perm = get_abc_regime_permission(regime)

    blocked = abc_perm.permission == RegimePermissionStatus.BLOCKED
    block_reasons = list(abc_perm.block_reasons)

    # Propagate detection-level blocks
    for br in detection.block_reasons:
        if br not in block_reasons:
            block_reasons.append(br)

    note = (
        f"regime={regime.value} "
        f"a={abc_perm.a_allowed} b={abc_perm.b_allowed} c={abc_perm.c_allowed} "
        f"blocked={blocked}"
    )

    return {
        "regime": regime,
        "abc_permission": abc_perm,
        "tier": tier,
        "blocked": blocked,
        "block_reasons": block_reasons,
        "a_allowed": abc_perm.a_allowed,
        "b_allowed": abc_perm.b_allowed,
        "c_allowed": abc_perm.c_allowed,
        "note": note,
        "paper_only": True,
        "no_real_orders": True,
    }


def is_abc_execution_allowed(
    detection: MarketRegimeDetectionResult,
    buy_point_type: str,
) -> bool:
    """
    Return True if the given buy point type (A/B/C) is allowed under current regime.
    Paper only.
    """
    result = adapt_regime_to_abc(detection)
    if buy_point_type == "A":
        return result["a_allowed"]
    if buy_point_type == "B":
        return result["b_allowed"]
    if buy_point_type == "C":
        return result["c_allowed"]
    return False


def get_regime_abc_summary(regime: MarketRegime) -> Dict[str, Any]:
    """
    Get ABC permission summary for a regime without a full detection result.
    Paper only.
    """
    perm = get_abc_regime_permission(regime)
    return {
        "regime": regime.value,
        "a_allowed": perm.a_allowed,
        "b_allowed": perm.b_allowed,
        "c_allowed": perm.c_allowed,
        "permission": perm.permission.value,
        "block_reasons": [br.value for br in perm.block_reasons],
        "paper_only": True,
        "no_real_orders": True,
    }
