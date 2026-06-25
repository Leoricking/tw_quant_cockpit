"""paper_trading/latency_model_v160.py — Latency Model v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
All latency assumptions disclosed. Zero latency != real market equivalence.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Optional

from .enums_v160 import LatencyModel


@dataclass
class LatencyAssumption:
    model: LatencyModel
    fixed_ms: Optional[int] = None
    event_count_delay: Optional[int] = None
    disclosed: bool = True
    note: str = ""

    def describe(self) -> str:
        if self.model == LatencyModel.ZERO_DISCLOSED:
            return "ZERO_LATENCY_DISCLOSED: assumes instant fill, not real-market equivalent"
        if self.model == LatencyModel.FIXED_MS:
            return f"FIXED_LATENCY_{self.fixed_ms}ms_DISCLOSED"
        if self.model == LatencyModel.EVENT_COUNT_DELAY:
            return f"EVENT_COUNT_DELAY_{self.event_count_delay}_EVENTS_DISCLOSED"
        return "UNKNOWN_LATENCY_DISCLOSED"


def build_latency_assumption(model_id: str, params: Optional[Dict[str, Any]] = None) -> LatencyAssumption:
    params = params or {}
    if model_id in ("ZERO_DISCLOSED", "zero"):
        return LatencyAssumption(
            model=LatencyModel.ZERO_DISCLOSED,
            note="ZERO_DISCLOSED: instant fill assumption, not real-market equivalent",
        )
    if model_id in ("FIXED_MS", "fixed"):
        ms = int(params.get("fixed_ms", 100))
        return LatencyAssumption(
            model=LatencyModel.FIXED_MS,
            fixed_ms=ms,
            note=f"FIXED_{ms}ms latency assumption",
        )
    if model_id in ("EVENT_COUNT_DELAY", "event_count"):
        count = int(params.get("event_count_delay", 1))
        return LatencyAssumption(
            model=LatencyModel.EVENT_COUNT_DELAY,
            event_count_delay=count,
            note=f"EVENT_COUNT_{count} delay assumption",
        )
    return LatencyAssumption(
        model=LatencyModel.ZERO_DISCLOSED,
        note="default: ZERO_DISCLOSED",
    )
