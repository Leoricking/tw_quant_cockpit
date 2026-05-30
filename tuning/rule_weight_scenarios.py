"""
tuning/rule_weight_scenarios.py - Preset weight configurations (v0.3.15).

Defines 7 standard scoring weight configurations for comparison:

  1. baseline_current          — current hardcoded production weights
  2. technical_heavy           — emphasise bull_stock + buy_point
  3. fundamental_heavy         — emphasise fundamental quality
  4. intraday_heavy            — emphasise microstructure / intraday
  5. risk_control_heavy        — higher penalties, conservative stance
  6. signal_quality_boosted    — dynamically derived from signal_quality_summary.csv
  7. balanced_v2               — equal-weight across all 6 components

[!] Advisory only. Never auto-applied to production strategy.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, Optional

from tuning.rule_weight_config import RuleWeightConfig

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_RESULTS_DIR = os.path.join(_BASE_DIR, "data", "backtest_results")

# ---------------------------------------------------------------------------
# Static preset configs
# ---------------------------------------------------------------------------

BASELINE_CURRENT = RuleWeightConfig(
    name="baseline_current",
    description="Current hardcoded production weights (0.30/0.20/0.20/0.15/0.10/0.05)",
    bull_stock_weight=0.30,
    buy_point_weight=0.20,
    strategy_knowledge_weight=0.20,
    fundamental_weight=0.15,
    intraday_weight=0.10,
    sector_strength_weight=0.05,
    source="preset",
)

TECHNICAL_HEAVY = RuleWeightConfig(
    name="technical_heavy",
    description="Emphasise technical signals: bull_stock + buy_point boosted",
    bull_stock_weight=0.35,
    buy_point_weight=0.25,
    strategy_knowledge_weight=0.20,
    fundamental_weight=0.10,
    intraday_weight=0.07,
    sector_strength_weight=0.03,
    source="preset",
)

FUNDAMENTAL_HEAVY = RuleWeightConfig(
    name="fundamental_heavy",
    description="Emphasise fundamental quality: eps, gross_margin, PE signals",
    bull_stock_weight=0.25,
    buy_point_weight=0.15,
    strategy_knowledge_weight=0.15,
    fundamental_weight=0.30,
    intraday_weight=0.10,
    sector_strength_weight=0.05,
    source="preset",
)

INTRADAY_HEAVY = RuleWeightConfig(
    name="intraday_heavy",
    description="Emphasise intraday microstructure: volume expansion, opening patterns",
    bull_stock_weight=0.25,
    buy_point_weight=0.20,
    strategy_knowledge_weight=0.15,
    fundamental_weight=0.10,
    intraday_weight=0.25,
    sector_strength_weight=0.05,
    source="preset",
)

RISK_CONTROL_HEAVY = RuleWeightConfig(
    name="risk_control_heavy",
    description="Stricter penalties; conservative score compression",
    bull_stock_weight=0.28,
    buy_point_weight=0.20,
    strategy_knowledge_weight=0.20,
    fundamental_weight=0.15,
    intraday_weight=0.10,
    sector_strength_weight=0.07,
    # Elevated penalties
    penalty_no_chase=12.0,
    penalty_fake_breakout=12.0,
    penalty_fundamental_warn=9.0,
    penalty_overvalued=9.0,
    penalty_timing_estimated=5.0,
    penalty_sector_conc=6.0,
    source="preset",
)

BALANCED_V2 = RuleWeightConfig(
    name="balanced_v2",
    description="Equal weight across all 6 components (1/6 each ≈ 0.167)",
    bull_stock_weight=round(1 / 6, 4),
    buy_point_weight=round(1 / 6, 4),
    strategy_knowledge_weight=round(1 / 6, 4),
    fundamental_weight=round(1 / 6, 4),
    intraday_weight=round(1 / 6, 4),
    sector_strength_weight=round(1 / 6, 4),
    source="preset",
)

# Ordered dict of all static presets (signal_quality_boosted is built at runtime)
STATIC_SCENARIOS: Dict[str, RuleWeightConfig] = {
    "baseline_current":      BASELINE_CURRENT,
    "technical_heavy":       TECHNICAL_HEAVY,
    "fundamental_heavy":     FUNDAMENTAL_HEAVY,
    "intraday_heavy":        INTRADAY_HEAVY,
    "risk_control_heavy":    RISK_CONTROL_HEAVY,
    "balanced_v2":           BALANCED_V2,
}


# ---------------------------------------------------------------------------
# signal_quality_boosted — built dynamically from signal_quality_summary.csv
# ---------------------------------------------------------------------------

# Maps CSV signal_group values to RuleWeightConfig field names
_GROUP_TO_FIELD = {
    "buy_point":         "buy_point_weight",
    "screener":          "bull_stock_weight",
    "strategy_knowledge":"strategy_knowledge_weight",
    "long_term":         "fundamental_weight",
    "microstructure":    "intraday_weight",
}

# Adjustment multipliers per recommendation
_REC_MULTIPLIER = {
    "BOOST":              1.15,
    "KEEP":               1.00,
    "REDUCE":             0.85,
    "DISABLE":            0.60,
    "INSUFFICIENT_SAMPLE": 1.00,
}


def build_signal_quality_boosted(
    results_dir: Optional[str] = None,
) -> RuleWeightConfig:
    """
    Derive signal_quality_boosted config from signal_quality_summary.csv.

    For each signal group (buy_point / screener / strategy_knowledge /
    long_term / microstructure), the dominant recommendation across all
    signals in that group is used to adjust the corresponding weight:

        BOOST  → ×1.15
        KEEP   → unchanged
        REDUCE → ×0.85
        DISABLE → ×0.60
        INSUFFICIENT_SAMPLE → unchanged

    Weights are then renormalized to sum to 1.0.
    Falls back to BALANCED_V2 if CSV is missing or unreadable.
    """
    dir_ = results_dir or _DEFAULT_RESULTS_DIR
    csv_path = os.path.join(dir_, "signal_quality_summary.csv")

    if not os.path.exists(csv_path):
        logger.info(
            "signal_quality_summary.csv not found at %s; "
            "using balanced_v2 fallback for signal_quality_boosted",
            csv_path,
        )
        fb = RuleWeightConfig(**{**BALANCED_V2.to_dict(),
                                  "name": "signal_quality_boosted",
                                  "description": "Fallback to balanced_v2 (signal_quality_summary.csv missing)",
                                  "source": "signal_quality_csv_fallback"})
        return fb

    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
    except Exception as exc:
        logger.warning("Cannot read %s: %s; falling back to balanced_v2", csv_path, exc)
        fb = RuleWeightConfig(**{**BALANCED_V2.to_dict(),
                                  "name": "signal_quality_boosted",
                                  "description": "Fallback to balanced_v2 (CSV read error)",
                                  "source": "signal_quality_csv_fallback"})
        return fb

    if "signal_group" not in df.columns or "recommendation" not in df.columns:
        logger.warning(
            "signal_quality_summary.csv missing required columns; using balanced_v2"
        )
        fb = RuleWeightConfig(**{**BALANCED_V2.to_dict(),
                                  "name": "signal_quality_boosted",
                                  "description": "Fallback to balanced_v2 (missing columns)",
                                  "source": "signal_quality_csv_fallback"})
        return fb

    # Collect recommendations per group
    from collections import Counter

    group_recs: Dict[str, list] = {}
    for _, row in df.iterrows():
        grp = str(row.get("signal_group", "")).lower().strip()
        rec = str(row.get("recommendation", "")).strip()
        if grp and rec:
            group_recs.setdefault(grp, []).append(rec)

    def _dominant(recs: list) -> str:
        if not recs:
            return "KEEP"
        return Counter(recs).most_common(1)[0][0]

    # Start from baseline weights
    weights = {
        "bull_stock_weight":           BASELINE_CURRENT.bull_stock_weight,
        "buy_point_weight":            BASELINE_CURRENT.buy_point_weight,
        "strategy_knowledge_weight":   BASELINE_CURRENT.strategy_knowledge_weight,
        "fundamental_weight":          BASELINE_CURRENT.fundamental_weight,
        "intraday_weight":             BASELINE_CURRENT.intraday_weight,
        "sector_strength_weight":      BASELINE_CURRENT.sector_strength_weight,
    }

    adjustments: list = []
    for grp, field in _GROUP_TO_FIELD.items():
        recs = group_recs.get(grp, [])
        rec = _dominant(recs)
        mult = _REC_MULTIPLIER.get(rec, 1.0)
        old = weights[field]
        weights[field] = round(old * mult, 6)
        adjustments.append(f"{grp}:{rec}(×{mult})")

    # Renormalize
    total = sum(weights.values())
    if total > 0:
        for k in weights:
            weights[k] = round(weights[k] / total, 4)

    desc = (
        "Adjusted from baseline using signal_quality_summary.csv. "
        + " | ".join(adjustments)
    )

    return RuleWeightConfig(
        name="signal_quality_boosted",
        description=desc,
        source="signal_quality_csv",
        **weights,
    )


def get_all_scenarios(results_dir: Optional[str] = None) -> Dict[str, RuleWeightConfig]:
    """Return all 7 configs including signal_quality_boosted."""
    scenarios = dict(STATIC_SCENARIOS)
    scenarios["signal_quality_boosted"] = build_signal_quality_boosted(results_dir)
    return scenarios
