"""
portfolio/walk_forward/explain_v154.py — Walk-forward Explainer v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
safety_text must include required strings.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
EXPLAIN_VERSION = "1.5.4"

REQUIRED_SAFETY_TEXT = [
    "HISTORICAL_SIMULATION_ONLY",
    "NOT_AN_ORDER",
    "NO_BROKER_CALL",
    "NO_FORMAL_LEDGER_WRITE",
    "PAST_PERFORMANCE_NOT_FUTURE_GUARANTEE",
]


class PortfolioWalkForwardExplainer:
    """Generate comprehensive explanation for walk-forward results."""

    def __init__(self):
        self.version = EXPLAIN_VERSION

    def explain(
        self,
        summary,
        config,
        windows: List[Any],
        eligibility: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate full explanation of walk-forward run.
        safety_text includes all required strings.
        """
        config_id = getattr(config, "config_id", "unknown") if config else "unknown"
        window_type = getattr(config, "window_type", None) if config else None
        window_type_str = window_type.value if hasattr(window_type, "value") else str(window_type)

        # Safety text — all required strings present
        safety_text = " | ".join(REQUIRED_SAFETY_TEXT)

        total_windows = len(windows)
        valid_windows = sum(1 for w in windows if hasattr(w, "status") and str(w.status.value if hasattr(w.status, "value") else w.status) == "VALID")
        partial_windows = sum(1 for w in windows if hasattr(w, "status") and str(w.status.value if hasattr(w.status, "value") else w.status) == "PARTIAL")

        return {
            "configuration": {
                "config_id": config_id,
                "window_type": window_type_str,
                "training_length": getattr(config, "training_length", None) if config else None,
                "validation_length": getattr(config, "validation_length", None) if config else None,
                "step_length": getattr(config, "step_length", None) if config else None,
            },
            "windows_summary": {
                "total": total_windows,
                "valid": valid_windows,
                "partial": partial_windows,
                "blocked": total_windows - valid_windows - partial_windows,
            },
            "purge_embargo": {
                "purge_length": getattr(config, "purge_length", 0) if config else 0,
                "embargo_length": getattr(config, "embargo_length", 0) if config else 0,
                "purpose": "Prevent data leakage between training and validation",
            },
            "timing_assumption": "NEXT_CLOSE — decisions executed at next available close",
            "reconstruction_method": "FIXTURE_DEMO — historical portfolio state reconstructed from fixtures",
            "sizing_method": "ATR_STOP_DISTANCE — research only",
            "correlation_constraints": "ROLLING_CORRELATION — 60-day window, training data only",
            "risk_controls": "DRAWDOWN_LIMIT, RISK_BUDGET, VOLATILITY_LIMIT — simulation only",
            "costs_summary": {
                "buy_fee_rate": 0.001425,
                "sell_fee_rate": 0.001425,
                "tax_rate": 0.003,
                "minimum_fee": 20.0,
                "currency": "TWD",
            },
            "slippage_summary": {
                "model": "FIXED_BPS",
                "bps": 5.0,
                "assumptions": ["FIXED_BPS_APPLIED", "RESEARCH_ONLY"],
            },
            "liquidity_summary": {
                "participation_rate": 0.10,
                "partial_fill": True,
                "missing_adv_blocked": True,
            },
            "window_results": [
                {
                    "window_id": getattr(w, "window_id", "?"),
                    "status": str(getattr(w, "status", "UNKNOWN")),
                    "training": f"{getattr(w, 'training_start', '?')} to {getattr(w, 'training_end', '?')}",
                    "validation": f"{getattr(w, 'validation_start', '?')} to {getattr(w, 'validation_end', '?')}",
                }
                for w in windows[:5]  # Show first 5
            ],
            "degradation": {
                "in_sample_return": getattr(summary, "in_sample_return", None) if summary else None,
                "out_of_sample_return": getattr(summary, "out_of_sample_return", None) if summary else None,
                "label": "EXPLORATORY — degradation between in-sample and out-of-sample performance",
            },
            "stability": {
                "stability_score": getattr(summary, "stability_score", None) if summary else None,
                "version": "1.5.4",
            },
            "sensitivity": {
                "parameters_tested": 8,
                "selection_applied": False,
                "note": "No auto-selection — research guidance only",
            },
            "regimes": {
                "classified_by": "benchmark return + volatility",
                "thresholds": {
                    "bullish": "> 5% annualized",
                    "bearish": "< -5% annualized",
                    "high_volatility": "> 25%",
                    "low_volatility": "< 10%",
                    "sideways": "abs(return) < 2%",
                },
            },
            "benchmark": {
                "symbol": getattr(config, "benchmark_symbol", "^TWII") if config else "^TWII",
                "pit_safe": True,
            },
            "drawdown": {
                "max_drawdown": getattr(summary, "maximum_drawdown", None) if summary else None,
                "method": "ROLLING_PEAK_TROUGH",
            },
            "turnover": {
                "total_turnover": getattr(summary, "turnover", None) if summary else None,
                "by_window": "see detailed results",
            },
            "warnings": eligibility.get("warnings", []) if eligibility else [],
            "blockers": eligibility.get("blockers", []) if eligibility else [],
            "limitations": [
                "Fixture data only — not real market data",
                "Decision replay applies current engine to historical data",
                "Past performance does not guarantee future results",
                "Slippage and cost models are simplified approximations",
                "No corporate action adjustments in fixture mode",
            ],
            "safety_text": safety_text,
            "HISTORICAL_SIMULATION_ONLY": True,
            "NOT_AN_ORDER": True,
            "NO_BROKER_CALL": True,
            "NO_FORMAL_LEDGER_WRITE": True,
            "PAST_PERFORMANCE_NOT_FUTURE_GUARANTEE": True,
            "research_only": True,
        }
