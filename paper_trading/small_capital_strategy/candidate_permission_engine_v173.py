"""
paper_trading/small_capital_strategy/candidate_permission_engine_v173.py
Candidate permission engine for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimePermissionStatus, RegimeBlockReason, RegimeWarningReason,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    CandidateRegimePermission, ABCRegimePermission,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.candidate_permission_engine_v173"

# Permission table per (regime, tier)
_PERMISSION_TABLE: Dict[tuple, Dict] = {
    # BULL regime
    (MarketRegime.BULL, "CORE"):              {"permission": RegimePermissionStatus.ALLOWED, "max_candidates": 5, "buy_points": ["A", "B", "C"]},
    (MarketRegime.BULL, "MAIN_THEME_SWING"):  {"permission": RegimePermissionStatus.ALLOWED, "max_candidates": 5, "buy_points": ["A", "B", "C"]},
    (MarketRegime.BULL, "SECOND_WAVE_SETUP"): {"permission": RegimePermissionStatus.SELECTIVE, "max_candidates": 3, "buy_points": ["A", "C"]},
    (MarketRegime.BULL, "TRAINING"):          {"permission": RegimePermissionStatus.LIMITED, "max_candidates": 2, "buy_points": ["B"]},
    # RANGE regime
    (MarketRegime.RANGE, "CORE"):              {"permission": RegimePermissionStatus.SELECTIVE, "max_candidates": 4, "buy_points": ["A", "B"]},
    (MarketRegime.RANGE, "MAIN_THEME_SWING"):  {"permission": RegimePermissionStatus.SELECTIVE, "max_candidates": 3, "buy_points": ["A", "B"]},
    (MarketRegime.RANGE, "SECOND_WAVE_SETUP"): {"permission": RegimePermissionStatus.LIMITED, "max_candidates": 2, "buy_points": ["A"]},
    (MarketRegime.RANGE, "TRAINING"):          {"permission": RegimePermissionStatus.LIMITED, "max_candidates": 1, "buy_points": ["B"]},
    # BEAR regime
    (MarketRegime.BEAR, "CORE"):              {"permission": RegimePermissionStatus.LIMITED, "max_candidates": 2, "buy_points": ["A"]},
    (MarketRegime.BEAR, "MAIN_THEME_SWING"):  {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
    (MarketRegime.BEAR, "SECOND_WAVE_SETUP"): {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
    (MarketRegime.BEAR, "TRAINING"):          {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
    # RISK_OFF regime
    (MarketRegime.RISK_OFF, "CORE"):              {"permission": RegimePermissionStatus.LIMITED, "max_candidates": 1, "buy_points": ["A"]},
    (MarketRegime.RISK_OFF, "MAIN_THEME_SWING"):  {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
    (MarketRegime.RISK_OFF, "SECOND_WAVE_SETUP"): {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
    (MarketRegime.RISK_OFF, "TRAINING"):          {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
    # UNKNOWN regime
    (MarketRegime.UNKNOWN, "CORE"):              {"permission": RegimePermissionStatus.DEGRADED, "max_candidates": 2, "buy_points": ["A"]},
    (MarketRegime.UNKNOWN, "MAIN_THEME_SWING"):  {"permission": RegimePermissionStatus.DEGRADED, "max_candidates": 1, "buy_points": ["A"]},
    (MarketRegime.UNKNOWN, "SECOND_WAVE_SETUP"): {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
    (MarketRegime.UNKNOWN, "TRAINING"):          {"permission": RegimePermissionStatus.BLOCKED, "max_candidates": 0, "buy_points": []},
}

_BLOCKED_REGIMES = {MarketRegime.BEAR, MarketRegime.RISK_OFF}


def get_candidate_permission(
    regime: MarketRegime,
    tier: str,
) -> CandidateRegimePermission:
    """Get candidate permission for a tier under a regime. Paper only."""
    key = (regime, tier)
    entry = _PERMISSION_TABLE.get(key)

    if entry is None:
        return CandidateRegimePermission(
            regime=regime,
            tier=tier,
            permission=RegimePermissionStatus.BLOCKED,
            max_candidates=0,
            buy_points_allowed=[],
            block_reasons=[RegimeBlockReason.INSUFFICIENT_DATA],
            note="tier_not_found",
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
        )

    permission = entry["permission"]
    block_reasons: List[RegimeBlockReason] = []
    warnings: List[RegimeWarningReason] = []

    if permission == RegimePermissionStatus.BLOCKED:
        if regime == MarketRegime.BEAR:
            block_reasons.append(RegimeBlockReason.REGIME_BEAR)
        elif regime == MarketRegime.RISK_OFF:
            block_reasons.append(RegimeBlockReason.REGIME_RISK_OFF)
        elif regime == MarketRegime.UNKNOWN:
            block_reasons.append(RegimeBlockReason.REGIME_UNKNOWN)
    if permission == RegimePermissionStatus.DEGRADED:
        warnings.append(RegimeWarningReason.REGIME_DEGRADED)

    note = f"regime={regime.value} tier={tier} perm={permission.value} max={entry['max_candidates']}"

    return CandidateRegimePermission(
        regime=regime,
        tier=tier,
        permission=permission,
        max_candidates=entry["max_candidates"],
        buy_points_allowed=list(entry["buy_points"]),
        block_reasons=block_reasons,
        warnings=warnings,
        note=note,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )


def get_abc_regime_permission(regime: MarketRegime) -> ABCRegimePermission:
    """
    Get A/B/C buy point permission for a regime (based on MAIN_THEME_SWING tier).
    Paper only.
    """
    perm = get_candidate_permission(regime, "MAIN_THEME_SWING")
    a_allowed = "A" in perm.buy_points_allowed
    b_allowed = "B" in perm.buy_points_allowed
    c_allowed = "C" in perm.buy_points_allowed

    block_reasons = list(perm.block_reasons)

    return ABCRegimePermission(
        regime=regime,
        a_allowed=a_allowed,
        b_allowed=b_allowed,
        c_allowed=c_allowed,
        a_note="A_allowed" if a_allowed else "A_blocked",
        b_note="B_allowed" if b_allowed else "B_blocked",
        c_note="C_allowed" if c_allowed else "C_blocked",
        block_reasons=block_reasons,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )


def list_all_tiers() -> List[str]:
    """Return list of all supported tiers."""
    return ["CORE", "MAIN_THEME_SWING", "SECOND_WAVE_SETUP", "TRAINING"]
