"""
abc_validation/second_wave_analyzer_v141.py — Second wave analysis for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Second-wave conditions: prior impulse, intact trend, pullback volume contraction,
valid support, re-strengthening, no institutional retreat, no excessive margin,
reasonable distance from high, not overextended.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ABCSecondWaveAnalyzer:
    """
    Compares A/B/C buy point performance with and without second-wave filter.

    Second-wave conditions:
    1. Prior impulse detected (strong upward move)
    2. Trend intact (price above MA20 or MA60)
    3. Pullback volume contraction
    4. Valid support level (MA5/MA10/MA20 holding)
    5. Re-strengthening signal (price recovery + volume)
    6. No institutional retreat (foreign/trust not exiting)
    7. No excessive margin buildup
    8. Reasonable distance from prior high (< 30%)
    9. Not overextended (not too far above MA)
    """

    def check_second_wave_conditions(self, signal: dict, bars: Optional[list] = None) -> Dict[str, Any]:
        """Check all second-wave conditions for a signal. Returns dict of condition → bool/None."""
        conditions = {}

        # 1. Prior impulse
        prior_impulse = signal.get("prior_impulse")
        conditions["prior_impulse"] = prior_impulse if prior_impulse is not None else None

        # 2. Intact trend
        intact_trend = signal.get("intact_trend")
        conditions["intact_trend"] = intact_trend if intact_trend is not None else None

        # 3. Pullback volume contraction
        vol_contraction = signal.get("vol_contraction")
        conditions["pullback_vol_contraction"] = vol_contraction if vol_contraction is not None else None

        # 4. Valid support
        valid_support = signal.get("valid_support")
        conditions["valid_support"] = valid_support if valid_support is not None else None

        # 5. Re-strengthening
        re_strengthen = signal.get("re_strengthening")
        conditions["re_strengthening"] = re_strengthen if re_strengthen is not None else None

        # 6. No institutional retreat
        foreign_net = signal.get("foreign_net", 0)
        trust_net = signal.get("trust_net", 0)
        no_inst_retreat = (foreign_net >= -500) and (trust_net >= -200)
        conditions["no_institutional_retreat"] = no_inst_retreat

        # 7. No excessive margin
        margin_excessive = signal.get("margin_excessive", False)
        conditions["no_excessive_margin"] = not margin_excessive

        # 8. Reasonable distance from high
        entry_price = signal.get("entry_price")
        prior_high = signal.get("prior_high")
        if entry_price and prior_high and prior_high > 0:
            dist_from_high = (prior_high - entry_price) / prior_high
            conditions["reasonable_distance_from_high"] = dist_from_high <= 0.30
        else:
            conditions["reasonable_distance_from_high"] = None

        # 9. Not overextended
        overextended = signal.get("overextended", False)
        conditions["not_overextended"] = not overextended

        # Overall: all non-None conditions must be True
        non_none = [v for v in conditions.values() if v is not None]
        if not non_none:
            qualifies = None
        else:
            qualifies = all(non_none)

        return {
            "conditions": conditions,
            "qualifies_as_second_wave": qualifies,
            "conditions_checked": len(non_none),
            "conditions_passed": sum(1 for v in non_none if v),
        }

    def analyze(
        self,
        signals: List[dict],
        bars_by_symbol: Optional[Dict[str, list]] = None,
        trade_results: Optional[List[dict]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Compare performance with and without second-wave filter."""
        bars_by_symbol = bars_by_symbol or {}
        trade_results = trade_results or []

        second_wave_signals = []
        non_second_wave_signals = []

        for sig in signals:
            symbol = sig.get("symbol", "")
            bars = bars_by_symbol.get(symbol, [])
            signal_date = sig.get("signal_date", "")
            bars_before = [b for b in bars if b.get("date", "") < signal_date]
            check = self.check_second_wave_conditions(sig, bars_before)
            if check["qualifies_as_second_wave"] is True:
                second_wave_signals.append(sig)
            elif check["qualifies_as_second_wave"] is False:
                non_second_wave_signals.append(sig)
            # None = insufficient data, excluded from both groups

        def metrics(sigs, trades) -> dict:
            sig_ids = {s.get("signal_id") for s in sigs}
            rel = [t for t in trades if t.get("signal_id") in sig_ids]
            if not rel:
                return {"signal_count": len(sigs), "trade_count": 0,
                        "win_rate": None, "expectancy": None}
            net_rets = [t.get("net_return", 0) for t in rel]
            wins = [r for r in net_rets if r > 0]
            losses = [r for r in net_rets if r <= 0]
            wr = len(wins) / len(net_rets)
            aw = sum(wins) / len(wins) if wins else 0.0
            al = abs(sum(losses) / len(losses)) if losses else 0.0
            exp = wr * aw - (1 - wr) * al
            return {"signal_count": len(sigs), "trade_count": len(rel),
                    "win_rate": wr, "expectancy": exp}

        return {
            "buy_point_type": buy_point_type,
            "all_signals_count": len(signals),
            "second_wave_signals_count": len(second_wave_signals),
            "non_second_wave_signals_count": len(non_second_wave_signals),
            "second_wave_metrics": metrics(second_wave_signals, trade_results),
            "non_second_wave_metrics": metrics(non_second_wave_signals, trade_results),
            "insufficient_data_count": len(signals) - len(second_wave_signals) - len(non_second_wave_signals),
            "no_real_orders": True,
        }
