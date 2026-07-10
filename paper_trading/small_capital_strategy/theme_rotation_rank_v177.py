"""
paper_trading/small_capital_strategy/theme_rotation_rank_v177.py
Theme ranking functions for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def rank_themes(strength_scores: List[object]) -> List[object]:
    """Rank themes by strength_score descending. Returns List[ThemeRotationRank]."""
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRotationRank

    sorted_scores = sorted(strength_scores, key=lambda s: getattr(s, "score", 0.0), reverse=True)
    result = []
    for rank_idx, ss in enumerate(sorted_scores, start=1):
        result.append(ThemeRotationRank(
            theme=getattr(ss, "theme", None),
            rank=rank_idx,
            strength_score=getattr(ss, "score", 0.0),
            grade=getattr(ss, "grade", None),
            momentum_score=0.0,
            breadth_score=0.0,
            continuation_score=0.0,
            risk_score=0.0,
        ))
    return result


def get_top_n_themes(ranks: List[object], n: int) -> List[object]:
    """Return top N themes by rank."""
    sorted_ranks = sorted(ranks, key=lambda r: getattr(r, "rank", 9999))
    return sorted_ranks[:n]


def get_leader_themes(ranks: List[object]) -> List[object]:
    """Return only themes with LEADER grade."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeGrade
    return [r for r in ranks if getattr(r, "grade", None) == ThemeGrade.LEADER]
