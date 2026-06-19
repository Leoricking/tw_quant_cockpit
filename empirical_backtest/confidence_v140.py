"""
empirical_backtest/confidence_v140.py — Backtest Confidence Evaluator for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from .models_v140 import BacktestResult, BacktestConfiguration, BacktestStatus, ConfidenceLevel, CorporateActionStatus


class BacktestConfidenceEvaluator:
    """Evaluates the confidence level of a backtest result."""

    def evaluate(self, result: BacktestResult, config: BacktestConfiguration = None) -> dict:
        reasons = []
        limitations = []

        # Blocked immediately
        if result.status == BacktestStatus.BLOCKED:
            return {
                "confidence": ConfidenceLevel.BLOCKED,
                "score": 0,
                "reasons": ["Status is BLOCKED"],
                "limitations": [],
                "blocks_formal_conclusion": True,
            }

        # Mock/demo/fixture data → immediately blocked
        data_mode = result.quality_summary.get("data_mode", "unknown")
        if data_mode in ("mock", "demo", "fixture"):
            return {
                "confidence": ConfidenceLevel.BLOCKED,
                "score": 0,
                "reasons": ["Mock/demo/fixture data cannot produce formal conclusions"],
                "limitations": [],
                "blocks_formal_conclusion": True,
            }

        score = 50
        trade_count = result.trade_count

        # Trade count adjustments
        if trade_count < 10:
            score -= 30
            reasons.append("Fewer than 10 trades — insufficient statistical sample")
        if trade_count >= 30:
            score += 10
        if trade_count >= 100:
            score += 10

        # Sharpe ratio
        if result.metrics.get("sharpe_ratio", "unavailable") == "unavailable":
            score -= 10

        # Survivorship risk
        if result.quality_summary.get("has_survivorship_risk"):
            score -= 15
            limitations.append("Survivorship bias risk not eliminated")

        # Corporate action status
        ca_status = result.quality_summary.get("corporate_action_status", "UNKNOWN")
        if ca_status not in (CorporateActionStatus.ADJUSTED, CorporateActionStatus.NOT_APPLICABLE, "UNKNOWN"):
            score -= 10

        # OOS validation bonus
        if (
            result.validation_metrics.get("oos_tested") is True
            and result.validation_metrics.get("oos_degraded") is False
        ):
            score += 15

        # Cap score
        score = max(0, min(100, score))

        # Determine confidence level
        if score >= 70 and trade_count >= 30:
            confidence = ConfidenceLevel.HIGH
        elif score >= 50:
            confidence = ConfidenceLevel.MEDIUM
        elif trade_count < 10:
            confidence = ConfidenceLevel.INSUFFICIENT
        else:
            confidence = ConfidenceLevel.LOW

        blocks_formal_conclusion = (
            confidence in (ConfidenceLevel.BLOCKED, ConfidenceLevel.INSUFFICIENT)
            or result.status in (BacktestStatus.BLOCKED, BacktestStatus.DEMO_ONLY, BacktestStatus.FAILED)
        )

        return {
            "confidence": confidence,
            "score": score,
            "reasons": reasons,
            "limitations": limitations,
            "blocks_formal_conclusion": blocks_formal_conclusion,
        }
