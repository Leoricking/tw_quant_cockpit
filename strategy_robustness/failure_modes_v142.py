"""
strategy_robustness/failure_modes_v142.py — Failure mode classification for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Output NEVER contains: BUY, SELL, TRADE, ORDER, AUTO_OPTIMIZE.
[!] recommended_research_action is research guidance only.
"""
from __future__ import annotations

from typing import List, Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

FAILURE_MODES = [
    "OVERFIT",
    "REGIME_DEPENDENT",
    "PARAMETER_CLIFF",
    "COST_EROSION",
    "SLIPPAGE_EROSION",
    "TRADE_CONCENTRATION",
    "SYMBOL_CONCENTRATION",
    "INDUSTRY_CONCENTRATION",
    "TIME_CONCENTRATION",
    "SAMPLE_TOO_SMALL",
    "DATA_QUALITY_WEAK",
    "FRESHNESS_WEAK",
    "SURVIVORSHIP_RISK",
    "CORPORATE_ACTION_RISK",
    "RECENT_DECAY",
    "NO_OOS_SUPPORT",
    "WALK_FORWARD_INSTABILITY",
    "UNKNOWN",
]

VALID_RESEARCH_ACTIONS = [
    "COLLECT_MORE_DATA",
    "EXPAND_UNIVERSE",
    "REVIEW_PARAMETERS",
    "REVIEW_COST_ASSUMPTIONS",
    "REVIEW_REGIME_FILTER",
    "REVIEW_DATA_QUALITY",
    "RUN_MORE_OOS",
    "RUN_MORE_WALK_FORWARD",
    "KEEP_OBSERVING",
    "BLOCK_FORMAL_CONCLUSION",
]


class StrategyFailureModeClassifier:
    """
    Classifies failure modes from a robustness result dict.
    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] NEVER outputs: BUY, SELL, TRADE, ORDER, AUTO_OPTIMIZE.
    """

    def classify(self, robustness_result: dict) -> list:
        """
        Classify failure modes from a robustness result dict.

        Parameters
        ----------
        robustness_result : dict (from StrategyRobustnessResult.to_dict())

        Returns
        -------
        list of failure mode dicts
        """
        failure_modes = []

        # OVERFIT: insufficient OOS support
        if not robustness_result.get("formal_conclusion_allowed", False):
            if robustness_result.get("trade_count", 0) < 30:
                failure_modes.append({
                    "type": "OVERFIT",
                    "severity": "HIGH",
                    "evidence": ["trade_count < 30 — insufficient OOS validation possible"],
                    "affected_metrics": ["trade_count", "formal_conclusion_allowed"],
                    "recommended_research_action": "COLLECT_MORE_DATA",
                    "blocks_formal_conclusion": True,
                })

        # REGIME_DEPENDENT
        regime = robustness_result.get("regime_robustness", {})
        if regime.get("regime_dependency_score", 0.0) >= 0.6:
            failure_modes.append({
                "type": "REGIME_DEPENDENT",
                "severity": "MEDIUM",
                "evidence": [f"regime_dependency_score={regime.get('regime_dependency_score', 0.0):.2f}"],
                "affected_metrics": ["regime_dependency_score"],
                "recommended_research_action": "REVIEW_REGIME_FILTER",
                "blocks_formal_conclusion": False,
            })

        # PARAMETER_CLIFF
        param_sens = robustness_result.get("parameter_sensitivity", {})
        variants = param_sens.get("variants", [])
        cliff_variants = [v for v in variants if v.get("cliff_risk", False)]
        if cliff_variants:
            failure_modes.append({
                "type": "PARAMETER_CLIFF",
                "severity": "HIGH",
                "evidence": [f"{len(cliff_variants)} parameter variants show cliff risk"],
                "affected_metrics": ["parameter_sensitivity"],
                "recommended_research_action": "REVIEW_PARAMETERS",
                "blocks_formal_conclusion": True,
            })

        # COST_EROSION
        cost_stress = robustness_result.get("cost_stress", {})
        cost_checks = cost_stress.get("checks", {})
        if not cost_checks.get("survives_2x_cost", {}).get("pass", True):
            failure_modes.append({
                "type": "COST_EROSION",
                "severity": "HIGH",
                "evidence": ["Strategy fails at 2x cost multiplier"],
                "affected_metrics": ["cost_stress"],
                "recommended_research_action": "REVIEW_COST_ASSUMPTIONS",
                "blocks_formal_conclusion": False,
            })

        # TRADE_CONCENTRATION
        trade_conc = robustness_result.get("trade_concentration", {})
        if trade_conc.get("status") == "CONCENTRATED":
            failure_modes.append({
                "type": "TRADE_CONCENTRATION",
                "severity": "HIGH",
                "evidence": ["Strategy performance concentrated in few trades"],
                "affected_metrics": ["trade_concentration"],
                "recommended_research_action": "EXPAND_UNIVERSE",
                "blocks_formal_conclusion": False,
            })

        # SYMBOL_CONCENTRATION
        cross = robustness_result.get("cross_sectional", {})
        if cross.get("top_contributor_share", 0.0) > 0.5:
            failure_modes.append({
                "type": "SYMBOL_CONCENTRATION",
                "severity": "MEDIUM",
                "evidence": [f"top_contributor_share={cross.get('top_contributor_share', 0.0):.2f}"],
                "affected_metrics": ["cross_sectional"],
                "recommended_research_action": "EXPAND_UNIVERSE",
                "blocks_formal_conclusion": False,
            })

        # INDUSTRY_CONCENTRATION
        industry = robustness_result.get("industry_robustness", {})
        ind_checks = industry.get("checks", {})
        if not ind_checks.get("single_industry_concentration", {}).get("pass", True):
            failure_modes.append({
                "type": "INDUSTRY_CONCENTRATION",
                "severity": "MEDIUM",
                "evidence": ["Single industry dominates performance"],
                "affected_metrics": ["industry_robustness"],
                "recommended_research_action": "EXPAND_UNIVERSE",
                "blocks_formal_conclusion": False,
            })

        # TIME_CONCENTRATION
        time_rob = robustness_result.get("time_robustness", {})
        time_checks = time_rob.get("checks", {})
        if not time_checks.get("performance_concentration", {}).get("pass", True):
            failure_modes.append({
                "type": "TIME_CONCENTRATION",
                "severity": "MEDIUM",
                "evidence": ["Performance concentrated in a single year"],
                "affected_metrics": ["time_robustness"],
                "recommended_research_action": "COLLECT_MORE_DATA",
                "blocks_formal_conclusion": False,
            })

        # SAMPLE_TOO_SMALL
        if robustness_result.get("trade_count", 0) < 30:
            failure_modes.append({
                "type": "SAMPLE_TOO_SMALL",
                "severity": "HIGH",
                "evidence": [f"trade_count={robustness_result.get('trade_count', 0)} < 30"],
                "affected_metrics": ["trade_count"],
                "recommended_research_action": "COLLECT_MORE_DATA",
                "blocks_formal_conclusion": True,
            })

        # RECENT_DECAY
        decay = robustness_result.get("decay", {})
        from strategy_robustness.models_v142 import DecayStatus
        if decay.get("decay_status") in (DecayStatus.POSSIBLE_DECAY, DecayStatus.SIGNIFICANT_DECAY):
            failure_modes.append({
                "type": "RECENT_DECAY",
                "severity": "HIGH" if decay.get("decay_status") == DecayStatus.SIGNIFICANT_DECAY else "MEDIUM",
                "evidence": decay.get("evidence", ["Decay detected"]),
                "affected_metrics": ["decay"],
                "recommended_research_action": "KEEP_OBSERVING",
                "blocks_formal_conclusion": decay.get("decay_status") == DecayStatus.SIGNIFICANT_DECAY,
            })

        # NO_OOS_SUPPORT
        bootstrap = robustness_result.get("bootstrap", {})
        if bootstrap.get("status") == "FAIL":
            failure_modes.append({
                "type": "NO_OOS_SUPPORT",
                "severity": "HIGH",
                "evidence": ["Bootstrap CI shows no support for positive expectancy"],
                "affected_metrics": ["bootstrap"],
                "recommended_research_action": "RUN_MORE_OOS",
                "blocks_formal_conclusion": True,
            })

        return failure_modes
