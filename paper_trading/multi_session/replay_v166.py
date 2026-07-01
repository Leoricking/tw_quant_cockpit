"""
paper_trading/multi_session/replay_v166.py — Coordination Replay v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Same input → same output hash. Silent mismatch forbidden.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.coordination_context_v166 import CoordinationContext
from paper_trading.multi_session.models_v166 import CoordinationResult

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_SILENT_MISMATCH = True


class CoordinationReplay:
    """Replays coordination decisions for reproducibility validation."""

    def __init__(self) -> None:
        self._log: List[Dict[str, Any]] = []

    def record(self, ctx: CoordinationContext, result: CoordinationResult) -> None:
        self._log.append({
            "input_hash": ctx.to_input_hash(),
            "output_hash": result.reproducibility_hash,
            "sessions_admitted": sorted(result.sessions_admitted),
            "sessions_blocked": sorted(result.sessions_blocked),
            "conflicts_detected": result.conflicts_detected,
        })

    def validate_reproducibility(
        self,
        ctx: CoordinationContext,
        result: CoordinationResult,
        expected_hash: str,
    ) -> Dict[str, Any]:
        actual = result.reproducibility_hash
        match = actual == expected_hash
        if not match:
            return {
                "reproducible": False,
                "input_hash": ctx.to_input_hash(),
                "expected_hash": expected_hash,
                "actual_hash": actual,
                "mismatch": True,
            }
        return {
            "reproducible": True,
            "input_hash": ctx.to_input_hash(),
            "hash": actual,
            "mismatch": False,
        }

    def get_log(self) -> List[Dict[str, Any]]:
        return list(self._log)
