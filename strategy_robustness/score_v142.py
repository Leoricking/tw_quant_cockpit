"""
strategy_robustness/score_v142.py — Robustness scoring engine for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class StrategyRobustnessScoreEngine:
    """
    Scores strategy robustness across 14 dimensions (0-100).
    ROBUST 80-100, ACCEPTABLE 65-79, FRAGILE 45-64, HIGH_RISK 25-44, BLOCKED 0-24.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    DIMENSION_WEIGHTS = {
        "time": 10,
        "cross_sectional": 8,
        "industry": 6,
        "regime": 10,
        "parameter": 8,
        "cost": 8,
        "slippage": 6,
        "concentration": 8,
        "bootstrap": 8,
        "monte_carlo": 6,
        "rolling": 6,
        "decay": 8,
        "data_quality": 8,
        "sample_size": 10,
    }

    def score(self, robustness_result: dict) -> dict:
        """
        Compute overall robustness score.

        Parameters
        ----------
        robustness_result : dict (from StrategyRobustnessResult.to_dict())

        Returns
        -------
        dict with overall_score, dimension_scores, penalties, bonuses, reasons, status
        """
        dimension_scores: Dict[str, float] = {}
        reasons = []
        penalties = []
        bonuses = []

        # Time dimension
        time_rob = robustness_result.get("time_robustness", {})
        time_checks = time_rob.get("checks", {})
        time_pass = sum(1 for c in time_checks.values() if c.get("pass", True))
        time_total = max(1, len(time_checks))
        dimension_scores["time"] = 100.0 * time_pass / time_total
        if time_rob.get("status") == "FRAGILE":
            reasons.append("TIME: fragile time-series performance")

        # Cross-sectional dimension
        cross = robustness_result.get("cross_sectional", {})
        cross_pass = cross.get("profitable_symbol_ratio", 0.5) >= 0.5
        cross_conc = cross.get("top_contributor_share", 1.0) <= 0.5
        dimension_scores["cross_sectional"] = 100.0 * (int(cross_pass) + int(cross_conc)) / 2
        if not cross_pass:
            reasons.append("SYMBOL: less than 50% profitable symbols")

        # Industry dimension
        industry = robustness_result.get("industry_robustness", {})
        ind_checks = industry.get("checks", {})
        ind_pass = sum(1 for c in ind_checks.values() if c.get("pass", True))
        ind_total = max(1, len(ind_checks))
        dimension_scores["industry"] = 100.0 * ind_pass / ind_total

        # Regime dimension
        regime = robustness_result.get("regime_robustness", {})
        regime_dep = regime.get("regime_dependency_score", 0.5)
        dimension_scores["regime"] = max(0.0, 100.0 * (1.0 - regime_dep))
        if regime_dep >= 0.6:
            penalties.append(f"REGIME_DEPENDENT: score={regime_dep:.2f}")

        # Parameter dimension
        param = robustness_result.get("parameter_sensitivity", {})
        param_checks = param.get("checks", {})
        param_pass = sum(1 for c in param_checks.values() if c.get("pass", True))
        param_total = max(1, len(param_checks))
        dimension_scores["parameter"] = 100.0 * param_pass / param_total if param_checks else 50.0

        # Cost dimension
        cost = robustness_result.get("cost_stress", {})
        cost_checks = cost.get("checks", {})
        cost_pass = sum(1 for c in cost_checks.values() if c.get("pass", True))
        cost_total = max(1, len(cost_checks))
        dimension_scores["cost"] = 100.0 * cost_pass / cost_total if cost_checks else 50.0
        if cost.get("status") == "COST_SENSITIVE":
            penalties.append("COST_SENSITIVE")

        # Slippage (approximate from cost)
        dimension_scores["slippage"] = dimension_scores["cost"]  # Use cost proxy

        # Concentration dimension
        conc = robustness_result.get("trade_concentration", {})
        conc_checks = conc.get("checks", {})
        conc_pass = sum(1 for c in conc_checks.values() if c.get("pass", True))
        conc_total = max(1, len(conc_checks))
        dimension_scores["concentration"] = 100.0 * conc_pass / conc_total if conc_checks else 50.0
        if conc.get("status") == "CONCENTRATED":
            penalties.append("CONCENTRATED: strategy depends on few trades")

        # Bootstrap dimension
        bootstrap = robustness_result.get("bootstrap", {})
        bootstrap_metrics = bootstrap.get("metrics", {})
        if bootstrap_metrics:
            pass_count = sum(1 for m in bootstrap_metrics.values() if m.get("status") == "PASS")
            dimension_scores["bootstrap"] = 100.0 * pass_count / len(bootstrap_metrics)
        else:
            dimension_scores["bootstrap"] = 30.0  # Low score if not run

        # Monte Carlo dimension
        mc = robustness_result.get("monte_carlo", {})
        if mc.get("status") == "PASS":
            dimension_scores["monte_carlo"] = 80.0
        elif mc.get("status") == "MARGINAL":
            dimension_scores["monte_carlo"] = 50.0
        elif mc.get("status") == "FAIL":
            dimension_scores["monte_carlo"] = 20.0
        else:
            dimension_scores["monte_carlo"] = 30.0

        # Rolling stability dimension
        rolling = robustness_result.get("rolling_stability", {})
        roll_summary = rolling.get("summary", {})
        pos_ratio = roll_summary.get("positive_window_ratio", 0.5)
        dimension_scores["rolling"] = 100.0 * pos_ratio

        # Decay dimension
        decay = robustness_result.get("decay", {})
        from strategy_robustness.models_v142 import DecayStatus
        decay_status = decay.get("decay_status", DecayStatus.UNKNOWN)
        if decay_status == DecayStatus.NO_DECAY:
            dimension_scores["decay"] = 90.0
        elif decay_status == DecayStatus.POSSIBLE_DECAY:
            dimension_scores["decay"] = 50.0
            penalties.append("POSSIBLE_DECAY")
        elif decay_status == DecayStatus.SIGNIFICANT_DECAY:
            dimension_scores["decay"] = 10.0
            penalties.append("SIGNIFICANT_DECAY")
        elif decay_status == DecayStatus.INSUFFICIENT_DATA:
            dimension_scores["decay"] = 40.0
        else:
            dimension_scores["decay"] = 40.0

        # Data quality dimension
        dimension_scores["data_quality"] = 70.0  # Default moderate; real data improves this

        # Sample size dimension
        trade_count = robustness_result.get("trade_count", 0)
        if trade_count >= 100:
            dimension_scores["sample_size"] = 100.0
            bonuses.append("LARGE_SAMPLE")
        elif trade_count >= 50:
            dimension_scores["sample_size"] = 80.0
        elif trade_count >= 30:
            dimension_scores["sample_size"] = 60.0
        elif trade_count >= 15:
            dimension_scores["sample_size"] = 30.0
        else:
            dimension_scores["sample_size"] = 10.0
            reasons.append("SAMPLE_SIZE: insufficient trades for robust scoring")

        # Compute weighted average
        total_weight = sum(self.DIMENSION_WEIGHTS.values())
        weighted_sum = sum(
            self.DIMENSION_WEIGHTS.get(dim, 5) * score
            for dim, score in dimension_scores.items()
        )
        overall_score = round(weighted_sum / total_weight, 2)

        # Apply penalties
        penalty_total = len(penalties) * 3.0  # 3 points per penalty
        overall_score = max(0.0, overall_score - penalty_total)

        # Determine status
        if overall_score >= 80:
            robustness_status = "ROBUST"
        elif overall_score >= 65:
            robustness_status = "ACCEPTABLE"
        elif overall_score >= 45:
            robustness_status = "FRAGILE"
        elif overall_score >= 25:
            robustness_status = "HIGH_RISK"
        else:
            robustness_status = "BLOCKED"

        # Formal conclusion gates
        formal_conclusion_allowed = (
            robustness_result.get("data_mode", "REAL") == "REAL"
            and trade_count >= 30
            and not any(f.get("blocks_formal_conclusion", False) for f in robustness_result.get("failure_modes", []))
            and overall_score >= 65
        )

        return {
            "overall_score": overall_score,
            "dimension_scores": {k: round(v, 2) for k, v in dimension_scores.items()},
            "penalties": penalties,
            "bonuses": bonuses,
            "reasons": reasons,
            "robustness_status": robustness_status,
            "confidence": "HIGH" if trade_count >= 50 else ("MEDIUM" if trade_count >= 20 else "LOW"),
            "formal_conclusion_allowed": formal_conclusion_allowed,
        }
