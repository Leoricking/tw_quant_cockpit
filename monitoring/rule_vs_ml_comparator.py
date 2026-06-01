"""
monitoring/rule_vs_ml_comparator.py — Rule vs ML Comparator for v0.4.3 Model Monitoring.

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class RuleVsMLComparator:
    """
    Compare rule-based signals against ML predictions.

    If ML predictions are not available, returns ML_NOT_AVAILABLE in all fields.
    [!] Monitoring Only. Read Only. No Real Orders.
    """

    read_only      = True
    no_real_orders = True

    _SAFETY = {
        "research_only":      True,
        "no_real_orders":     True,
        "monitoring_only":    True,
        "production_blocked": True,
        "real_order_ready":   False,
    }

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def compare(
        self,
        rule_signals:   Optional[list] = None,
        ml_predictions: Optional[list] = None,
        actuals:        Optional[dict] = None,
    ) -> dict:
        """
        Main comparison entry.

        rule_signals:   list of dicts with symbol, date, signal (BUY/SELL/HOLD), hit
        ml_predictions: list of dicts with symbol, date, predicted_label, hit
        actuals:        dict of {symbol: {date: actual_return}}
        """
        warnings: list = []

        # Detect ML availability
        ml_available = bool(ml_predictions)

        if not ml_available:
            rule_hr = self._group_hit_rate(rule_signals or [])
            return {
                "agreement_rate":        None,
                "rule_only_hits":        rule_hr.get("hits"),
                "ml_only_hits":          None,
                "both_hits":             None,
                "both_misses":           None,
                "disagreement_symbols":  [],
                "recommendation":        "ML_NOT_AVAILABLE",
                "ml_available":          False,
                "rule_hit_rate":         rule_hr.get("hit_rate"),
                "ml_hit_rate":           None,
                "rule_return":           None,
                "ml_return":             None,
                "warnings":              ["ML predictions not available — rule-only analysis."],
                **self._SAFETY,
            }

        if not rule_signals:
            return {
                "agreement_rate":        None,
                "rule_only_hits":        None,
                "ml_only_hits":          None,
                "both_hits":             None,
                "both_misses":           None,
                "disagreement_symbols":  [],
                "recommendation":        "RULE_SIGNALS_NOT_AVAILABLE",
                "ml_available":          True,
                "rule_hit_rate":         None,
                "ml_hit_rate":           None,
                "rule_return":           None,
                "ml_return":             None,
                "warnings":              ["Rule signals not available."],
                **self._SAFETY,
            }

        # Core comparisons
        agr_rate     = self.agreement_rate(rule_signals, ml_predictions)
        disagreements = self.disagreement_cases(rule_signals, ml_predictions)
        hit_comp     = self.compare_hit_rate(rule_signals, ml_predictions, actuals or {})
        ret_comp     = self.compare_return(rule_signals, ml_predictions, actuals or {})

        # Recommendation logic
        if agr_rate is None:
            recommendation = "INSUFFICIENT_DATA"
        elif agr_rate >= 0.70:
            recommendation = "AGREEMENT_HIGH"
        elif agr_rate >= 0.40:
            recommendation = "AGREEMENT_MODERATE_REVIEW"
        else:
            recommendation = "AGREEMENT_LOW_REVIEW"

        return {
            "agreement_rate":        agr_rate,
            "rule_only_hits":        hit_comp.get("rule_only_hits"),
            "ml_only_hits":          hit_comp.get("ml_only_hits"),
            "both_hits":             hit_comp.get("both_hits"),
            "both_misses":           hit_comp.get("both_misses"),
            "disagreement_symbols":  [d.get("symbol") for d in disagreements[:20]],
            "disagreement_cases":    disagreements[:20],
            "recommendation":        recommendation,
            "ml_available":          True,
            "rule_hit_rate":         hit_comp.get("rule_hit_rate"),
            "ml_hit_rate":           hit_comp.get("ml_hit_rate"),
            "rule_return":           ret_comp.get("rule_avg_return"),
            "ml_return":             ret_comp.get("ml_avg_return"),
            "warnings":              warnings,
            **self._SAFETY,
        }

    # ------------------------------------------------------------------
    # Core calculations
    # ------------------------------------------------------------------

    def agreement_rate(self, rule_signals: list, ml_predictions: list) -> Optional[float]:
        """Fraction of (symbol, date) pairs where rule and ML agree."""
        if not rule_signals or not ml_predictions:
            return None

        # Build lookup: (symbol, date) → signal
        rule_map = {}
        for r in rule_signals:
            key = (r.get("symbol", ""), r.get("date", ""))
            rule_map[key] = str(r.get("signal", r.get("predicted_label", ""))).upper()

        ml_map = {}
        for r in ml_predictions:
            key = (r.get("symbol", ""), r.get("date", ""))
            ml_map[key] = str(r.get("predicted_label", r.get("signal", ""))).upper()

        common_keys = set(rule_map.keys()) & set(ml_map.keys())
        if not common_keys:
            return None

        agree = sum(1 for k in common_keys if rule_map[k] == ml_map[k])
        return agree / len(common_keys)

    def disagreement_cases(self, rule_signals: list, ml_predictions: list) -> list:
        """Return list of cases where rule and ML disagree."""
        if not rule_signals or not ml_predictions:
            return []

        rule_map = {}
        for r in rule_signals:
            key = (r.get("symbol", ""), r.get("date", ""))
            rule_map[key] = r

        ml_map = {}
        for r in ml_predictions:
            key = (r.get("symbol", ""), r.get("date", ""))
            ml_map[key] = r

        cases = []
        for key in set(rule_map.keys()) & set(ml_map.keys()):
            r_sig = str(rule_map[key].get("signal", rule_map[key].get("predicted_label", ""))).upper()
            m_sig = str(ml_map[key].get("predicted_label", ml_map[key].get("signal", ""))).upper()
            if r_sig != m_sig:
                cases.append({
                    "symbol":       key[0],
                    "date":         key[1],
                    "rule_signal":  r_sig,
                    "ml_signal":    m_sig,
                })
        return cases

    def compare_hit_rate(
        self,
        rule_signals:   list,
        ml_predictions: list,
        actuals:        dict,
    ) -> dict:
        """Compare hit rates across rule vs ML signals."""
        def hr(records):
            hits   = sum(1 for r in records if r.get("hit") is True)
            misses = sum(1 for r in records if r.get("hit") is False)
            total  = hits + misses
            return hits / total if total > 0 else None, hits, misses

        r_rate, r_hits, r_misses = hr(rule_signals)
        m_rate, m_hits, m_misses = hr(ml_predictions)

        # both_hits / both_misses for common (symbol, date)
        rule_map = {(r.get("symbol"), r.get("date")): r.get("hit") for r in rule_signals}
        ml_map   = {(r.get("symbol"), r.get("date")): r.get("hit") for r in ml_predictions}
        common   = set(rule_map.keys()) & set(ml_map.keys())

        both_hits   = sum(1 for k in common if rule_map[k] is True  and ml_map[k] is True)
        both_misses = sum(1 for k in common if rule_map[k] is False and ml_map[k] is False)
        rule_only   = sum(1 for k in common if rule_map[k] is True  and ml_map[k] is not True)
        ml_only     = sum(1 for k in common if ml_map[k]   is True  and rule_map[k] is not True)

        return {
            "rule_hit_rate":  r_rate,
            "ml_hit_rate":    m_rate,
            "rule_only_hits": rule_only,
            "ml_only_hits":   ml_only,
            "both_hits":      both_hits,
            "both_misses":    both_misses,
        }

    def compare_return(
        self,
        rule_signals:   list,
        ml_predictions: list,
        actuals:        dict,
    ) -> dict:
        """Compare average actual returns for rule vs ML signals."""
        def avg_ret(records):
            vals = [r.get("actual_return") for r in records if r.get("actual_return") is not None]
            return sum(vals) / len(vals) if vals else None

        return {
            "rule_avg_return": avg_ret(rule_signals),
            "ml_avg_return":   avg_ret(ml_predictions),
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _group_hit_rate(self, records: list) -> dict:
        if not records:
            return {"hit_rate": None, "hits": 0, "total": 0}
        hits  = sum(1 for r in records if r.get("hit") is True)
        total = sum(1 for r in records if r.get("hit") is not None)
        return {"hit_rate": hits / total if total > 0 else None, "hits": hits, "total": total}
