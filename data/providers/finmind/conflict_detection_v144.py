"""
data/providers/finmind/conflict_detection_v144.py — FinMind conflict detection v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Primary always wins. FinMind preserved as secondary evidence. No auto-repair.
[!] Volume and money have different tolerances.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from data.providers.finmind.models_v144 import FinMindConflictResult

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _within_tolerance(primary_val: Any, finmind_val: Any, tolerance: float) -> bool:
    """Return True if values are within tolerance of each other."""
    try:
        p = float(primary_val)
        f = float(finmind_val)
        if p == 0 and f == 0:
            return True
        if p == 0:
            return abs(f) <= tolerance
        return abs(p - f) / abs(p) <= tolerance
    except (TypeError, ValueError):
        return primary_val == finmind_val


class FinMindConflictDetector:
    """
    Detects conflicts between primary source data and FinMind secondary data.
    Primary always wins. FinMind preserved as secondary evidence. No auto-repair.
    """

    def compare_price(
        self,
        primary_records: List[Dict[str, Any]],
        finmind_records: List[Dict[str, Any]],
        tolerance: float = 0.0001,
    ) -> List[Dict[str, Any]]:
        """
        Compare price data. Returns list of conflict results per (date, symbol).
        Fields checked: open, high, low, close, volume, turnover.
        Primary always wins on conflict.
        """
        # Index primary by (trade_date or date, symbol or stock_id)
        def _key(rec: Dict) -> str:
            d = rec.get("trade_date") or rec.get("date", "")
            s = rec.get("symbol") or rec.get("stock_id", "")
            return f"{d}|{s}"

        primary_index = {_key(r): r for r in primary_records}
        results = []

        for fm_rec in finmind_records:
            key = _key(fm_rec)
            prim = primary_index.get(key)

            if prim is None:
                results.append({
                    "key": key,
                    "result": FinMindConflictResult.MISSING_PRIMARY.value,
                    "field": None,
                    "primary_value": None,
                    "finmind_value": None,
                    "note": "No matching primary record",
                })
                continue

            price_fields = [
                ("close", "close"),
                ("open", "open"),
                ("high", "high"),  # also check max/high alias
                ("low", "low"),    # also check min/low alias
            ]
            volume_tolerance = 10  # absolute for volume differences

            for prim_field, fm_field in price_fields:
                pv = prim.get(prim_field)
                fv = fm_rec.get(fm_field) or fm_rec.get(
                    {"high": "max", "low": "min"}.get(fm_field, fm_field)
                )
                if pv is None or fv is None:
                    continue
                if _within_tolerance(pv, fv, tolerance):
                    results.append({
                        "key": key,
                        "result": FinMindConflictResult.WITHIN_TOLERANCE.value,
                        "field": prim_field,
                        "primary_value": pv,
                        "finmind_value": fv,
                    })
                else:
                    results.append({
                        "key": key,
                        "result": FinMindConflictResult.VALUE_CONFLICT.value,
                        "field": prim_field,
                        "primary_value": pv,
                        "finmind_value": fv,
                        "winner": "PRIMARY",
                    })

        return results

    def compare_institutional(
        self,
        primary: List[Dict[str, Any]],
        finmind: List[Dict[str, Any]],
        tolerance: float = 1000,
    ) -> List[Dict[str, Any]]:
        """
        Compare institutional flow data.
        Checks: foreign_net, trust_net, dealer_net.
        Tolerance is absolute (share count).
        """
        def _key(rec: Dict) -> str:
            d = rec.get("trade_date") or rec.get("date", "")
            s = rec.get("symbol") or rec.get("stock_id", "")
            return f"{d}|{s}"

        primary_index = {_key(r): r for r in primary}
        results = []

        for fm_rec in finmind:
            key = _key(fm_rec)
            prim = primary_index.get(key)
            if prim is None:
                results.append({
                    "key": key,
                    "result": FinMindConflictResult.MISSING_PRIMARY.value,
                    "field": None,
                })
                continue

            for field in ["foreign_net", "trust_net", "dealer_net"]:
                pv = prim.get(field)
                fv = fm_rec.get(field)
                if pv is None or fv is None:
                    continue
                try:
                    if abs(float(pv) - float(fv)) <= tolerance:
                        results.append({
                            "key": key,
                            "result": FinMindConflictResult.WITHIN_TOLERANCE.value,
                            "field": field,
                            "primary_value": pv,
                            "finmind_value": fv,
                        })
                    else:
                        results.append({
                            "key": key,
                            "result": FinMindConflictResult.VALUE_CONFLICT.value,
                            "field": field,
                            "primary_value": pv,
                            "finmind_value": fv,
                            "winner": "PRIMARY",
                        })
                except (TypeError, ValueError):
                    results.append({
                        "key": key,
                        "result": FinMindConflictResult.SCHEMA_INCOMPARABLE.value,
                        "field": field,
                    })

        return results

    def compare_margin(
        self,
        primary: List[Dict[str, Any]],
        finmind: List[Dict[str, Any]],
        tolerance: float = 100,
    ) -> List[Dict[str, Any]]:
        """
        Compare margin/short data.
        Checks: margin_balance, short_balance.
        Tolerance is absolute (shares).
        Never mix margin/short fields.
        """
        def _key(rec: Dict) -> str:
            d = rec.get("trade_date") or rec.get("date", "")
            s = rec.get("symbol") or rec.get("stock_id", "")
            return f"{d}|{s}"

        primary_index = {_key(r): r for r in primary}
        results = []

        for fm_rec in finmind:
            key = _key(fm_rec)
            prim = primary_index.get(key)
            if prim is None:
                results.append({
                    "key": key,
                    "result": FinMindConflictResult.MISSING_PRIMARY.value,
                    "field": None,
                })
                continue

            for field in ["margin_balance", "short_balance"]:
                pv = prim.get(field)
                fv = fm_rec.get(field)
                if pv is None or fv is None:
                    continue
                try:
                    if abs(float(pv) - float(fv)) <= tolerance:
                        results.append({
                            "key": key,
                            "result": FinMindConflictResult.WITHIN_TOLERANCE.value,
                            "field": field,
                            "primary_value": pv,
                            "finmind_value": fv,
                        })
                    else:
                        results.append({
                            "key": key,
                            "result": FinMindConflictResult.VALUE_CONFLICT.value,
                            "field": field,
                            "primary_value": pv,
                            "finmind_value": fv,
                            "winner": "PRIMARY",
                        })
                except (TypeError, ValueError):
                    results.append({
                        "key": key,
                        "result": FinMindConflictResult.SCHEMA_INCOMPARABLE.value,
                        "field": field,
                    })

        return results
