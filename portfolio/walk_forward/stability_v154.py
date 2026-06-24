"""
portfolio/walk_forward/stability_v154.py — Walk-forward Stability Analyzer v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
Score formula versioned: version="1.5.4"
"""
from __future__ import annotations
import math
from typing import Any, Dict, List, Optional

from portfolio.walk_forward.models_v154 import StabilityResult

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
STABILITY_VERSION = "1.5.4"

# Score formula:
# score = positive_ratio×40 + (1 - dispersion_normalized)×30 + (1 - worst_drawdown_normalized)×30
SCORE_FORMULA_VERSION = "1.5.4"
POSITIVE_RATIO_WEIGHT = 40
DISPERSION_WEIGHT = 30
WORST_DRAWDOWN_WEIGHT = 30


class WalkForwardStabilityAnalyzer:
    """Analyze stability of walk-forward window returns."""

    def __init__(self):
        self.version = STABILITY_VERSION

    def analyze(self, window_returns: List[float]) -> "StabilityResult":
        """
        Analyze stability of window return series.
        Score 0-100: positive_ratio×40 + (1-dispersion_norm)×30 + (1-worst_dd_norm)×30
        Missing component: mark None, not 0.
        """
        if not window_returns:
            return StabilityResult(
                window_metric_name="period_return",
                window_values=[],
                mean=0.0,
                median=0.0,
                standard_deviation=0.0,
                positive_window_ratio=0.0,
                worst_window=0.0,
                best_window=0.0,
                dispersion=0.0,
                trend=None,
                status="INSUFFICIENT_DATA",
                metadata={"formula_version": SCORE_FORMULA_VERSION, "research_only": True},
            )

        n = len(window_returns)
        mean = sum(window_returns) / n

        sorted_r = sorted(window_returns)
        if n % 2 == 1:
            median = sorted_r[n // 2]
        else:
            median = (sorted_r[n // 2 - 1] + sorted_r[n // 2]) / 2

        if n >= 2:
            variance = sum((r - mean) ** 2 for r in window_returns) / (n - 1)
            std = math.sqrt(variance)
        else:
            std = None

        positive_ratio = sum(1 for r in window_returns if r > 0) / n
        worst = min(window_returns)
        best = max(window_returns)
        dispersion = (best - worst) if n >= 2 else None

        # Score components (None if missing)
        score_pos = positive_ratio * POSITIVE_RATIO_WEIGHT

        if dispersion is not None and abs(mean) > 0:
            dispersion_normalized = min(abs(dispersion) / (abs(mean) + 1e-9), 1.0)
            score_disp = (1 - dispersion_normalized) * DISPERSION_WEIGHT
        else:
            score_disp = None

        worst_dd_normalized = min(abs(worst) / 0.5, 1.0) if worst < 0 else 0.0
        score_dd = (1 - worst_dd_normalized) * WORST_DRAWDOWN_WEIGHT

        if score_disp is not None:
            stability_score = score_pos + score_disp + score_dd
        else:
            stability_score = None

        # Trend: simple slope sign
        if n >= 3:
            first_half = window_returns[:n // 2]
            second_half = window_returns[n // 2:]
            trend = "IMPROVING" if sum(second_half) / len(second_half) > sum(first_half) / len(first_half) else "DECLINING"
        else:
            trend = None

        return StabilityResult(
            window_metric_name="period_return",
            window_values=window_returns,
            mean=mean,
            median=median,
            standard_deviation=std if std is not None else 0.0,
            positive_window_ratio=positive_ratio,
            worst_window=worst,
            best_window=best,
            dispersion=dispersion if dispersion is not None else 0.0,
            trend=trend,
            status="STABLE" if (stability_score is not None and stability_score >= 60) else "UNSTABLE",
            metadata={
                "formula_version": SCORE_FORMULA_VERSION,
                "stability_score": stability_score,
                "score_positive_ratio": score_pos,
                "score_dispersion": score_disp,
                "score_drawdown": score_dd,
                "research_only": True,
                "no_future_guarantee": True,
            },
        )
