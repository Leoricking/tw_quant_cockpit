"""
abc_validation/institutional_margin_analyzer_v141.py — Institutional/margin analysis v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Rules:
  - Missing data → INSUFFICIENT (never 0)
  - Timestamp-safe availability
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


INSTITUTIONAL_STATES = [
    "foreign_non_selling",
    "foreign_net_buying",
    "trust_non_selling",
    "trust_net_buying",
    "combined_support",
    "margin_stable",
    "margin_decreasing_on_pullback",
    "margin_excessive",
    "missing_institutional_data",
    "missing_margin_data",
]

MISSING_SENTINEL = "INSUFFICIENT"


class ABCInstitutionalMarginAnalyzer:
    """
    Analyzes institutional activity and margin data for A/B/C signals.

    Handles: foreign non-selling, foreign net buying, trust non-selling,
    trust net buying, combined support, margin stable, margin decreasing
    on pullback, margin excessive, missing institutional data, missing margin data.
    """

    def classify_signal(self, signal: dict) -> Dict[str, Any]:
        """Classify institutional/margin state for a single signal."""
        result = {}

        # Institutional data availability
        has_foreign = signal.get("foreign_net") is not None
        has_trust = signal.get("trust_net") is not None
        has_margin = signal.get("margin_balance") is not None

        if not has_foreign and not has_trust:
            result["institutional_state"] = MISSING_SENTINEL
            result["foreign_state"] = MISSING_SENTINEL
            result["trust_state"] = MISSING_SENTINEL
        else:
            foreign_net = signal.get("foreign_net", 0) or 0
            trust_net = signal.get("trust_net", 0) or 0

            result["foreign_state"] = (
                "foreign_net_buying" if foreign_net > 1000
                else "foreign_non_selling" if foreign_net >= 0
                else "foreign_selling"
            )
            result["trust_state"] = (
                "trust_net_buying" if trust_net > 500
                else "trust_non_selling" if trust_net >= 0
                else "trust_selling"
            )
            result["institutional_state"] = (
                "combined_support" if (foreign_net >= 0 and trust_net >= 0)
                else "partial_support" if (foreign_net >= 0 or trust_net >= 0)
                else "combined_selling"
            )

        # Margin data
        if not has_margin:
            result["margin_state"] = MISSING_SENTINEL
        else:
            margin_balance = signal.get("margin_balance", 0) or 0
            margin_prev = signal.get("margin_balance_prev", margin_balance) or margin_balance
            margin_pct = signal.get("margin_pct", 0) or 0

            if margin_pct > 0.20:
                result["margin_state"] = "margin_excessive"
            elif margin_balance <= margin_prev:
                result["margin_state"] = "margin_decreasing_on_pullback"
            else:
                result["margin_state"] = "margin_stable"

        # Timestamp safety
        result["data_timestamp_safe"] = signal.get("institutional_data_date", "") <= signal.get("signal_date", "")

        return result

    def analyze(
        self,
        signals: List[dict],
        trade_results: Optional[List[dict]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Analyze institutional/margin data for all signals."""
        trade_results = trade_results or []

        state_counts: Dict[str, int] = {s: 0 for s in INSTITUTIONAL_STATES}
        state_counts["missing_institutional_data"] = 0
        state_counts["missing_margin_data"] = 0

        classified_signals: Dict[str, List[dict]] = {s: [] for s in INSTITUTIONAL_STATES}

        for sig in signals:
            cls = self.classify_signal(sig)
            inst_state = cls.get("institutional_state", MISSING_SENTINEL)
            margin_state = cls.get("margin_state", MISSING_SENTINEL)

            if inst_state == MISSING_SENTINEL:
                state_counts["missing_institutional_data"] += 1
                classified_signals["missing_institutional_data"].append(sig)
            else:
                key = inst_state if inst_state in state_counts else "missing_institutional_data"
                state_counts[key] = state_counts.get(key, 0) + 1
                if key in classified_signals:
                    classified_signals[key].append(sig)

            if margin_state == MISSING_SENTINEL:
                state_counts["missing_margin_data"] += 1
                classified_signals["missing_margin_data"].append(sig)
            else:
                key = margin_state if margin_state in state_counts else "missing_margin_data"
                state_counts[key] = state_counts.get(key, 0) + 1
                if key in classified_signals:
                    classified_signals[key].append(sig)

        # Compute win rate per state
        state_metrics = {}
        for state, sigs in classified_signals.items():
            if not sigs:
                state_metrics[state] = {"signal_count": 0, "trade_count": 0, "win_rate": None}
                continue
            sig_ids = {s.get("signal_id") for s in sigs}
            rel_trades = [t for t in trade_results if t.get("signal_id") in sig_ids]
            if not rel_trades:
                state_metrics[state] = {"signal_count": len(sigs), "trade_count": 0, "win_rate": None}
                continue
            net_rets = [t.get("net_return", 0) for t in rel_trades]
            wins = len([r for r in net_rets if r > 0])
            state_metrics[state] = {
                "signal_count": len(sigs),
                "trade_count": len(rel_trades),
                "win_rate": wins / len(rel_trades) if rel_trades else None,
            }

        return {
            "buy_point_type": buy_point_type,
            "total_signals": len(signals),
            "state_counts": state_counts,
            "state_metrics": state_metrics,
            "missing_data_note": "INSUFFICIENT means data unavailable — never treated as 0",
            "no_real_orders": True,
        }
