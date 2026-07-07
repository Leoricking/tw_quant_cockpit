"""
paper_trading/small_capital_strategy/institutional_filter_v171.py
Institutional support filter for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.watchlist_enums_v171 import InstitutionalGrade
from paper_trading.small_capital_strategy.watchlist_models_v171 import InstitutionalFilterResult

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# Net buy days out of last 20 trading days
INST_ACCUMULATING_THRESHOLD = 10   # >= 10 net buy days: ACCUMULATING
INST_NEUTRAL_THRESHOLD      = 4    # >= 4: NEUTRAL
# < 4: DISTRIBUTING
# < 0 (net sell days > net buy days): BLOCKED


def grade_institutional(net_buy_days: int) -> InstitutionalGrade:
    """Grade institutional support from net buy days (last 20 trading days)."""
    if net_buy_days >= INST_ACCUMULATING_THRESHOLD:
        return InstitutionalGrade.ACCUMULATING
    if net_buy_days >= INST_NEUTRAL_THRESHOLD:
        return InstitutionalGrade.NEUTRAL
    if net_buy_days >= 0:
        return InstitutionalGrade.DISTRIBUTING
    return InstitutionalGrade.BLOCKED


def score_institutional_grade(grade: InstitutionalGrade) -> float:
    """Return 0-100 score from grade."""
    mapping = {
        InstitutionalGrade.ACCUMULATING: 90.0,
        InstitutionalGrade.NEUTRAL:      60.0,
        InstitutionalGrade.DISTRIBUTING: 35.0,
        InstitutionalGrade.BLOCKED:       0.0,
    }
    return mapping[grade]


def apply_institutional_filter(symbol: str, net_buy_days: int) -> InstitutionalFilterResult:
    """Apply institutional filter. Blocked if heavy selling (net_buy_days < 0)."""
    grade = grade_institutional(net_buy_days)
    score = score_institutional_grade(grade)
    passed = grade != InstitutionalGrade.BLOCKED
    reason = "" if passed else f"institutional heavy selling: net_buy_days={net_buy_days}"
    return InstitutionalFilterResult(
        symbol=symbol,
        net_buy_days=net_buy_days,
        grade=grade,
        score=score,
        passed=passed,
        reason=reason,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def get_institutional_thresholds() -> Dict[str, Any]:
    """Return institutional thresholds. Deterministic."""
    return {
        "accumulating": INST_ACCUMULATING_THRESHOLD,
        "neutral": INST_NEUTRAL_THRESHOLD,
        "blocked_below": 0,
    }
