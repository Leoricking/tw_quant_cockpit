"""
paper_trading/analytics/replay_v164.py — Analytics Replay v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Same input + policies + code = same output hash. Mismatch raises REPRODUCIBILITY_MISMATCH.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional

from paper_trading.analytics.enums_v164 import ReproducibilityStatus
from paper_trading.analytics.snapshot_v164 import _hash_dict

NO_REAL_ORDERS = True
PAPER_ONLY = True
SILENT_ACCEPT_MISMATCH = False  # Always explicit on mismatch


@dataclass
class ReplayResult:
    original_hash: str
    replay_hash: str
    status: ReproducibilityStatus
    details: str = ""
    paper_only: bool = True


class AnalyticsReplayer:
    """
    Replays analytics computation and verifies reproducibility hash.
    Mismatch → explicit REPRODUCIBILITY_MISMATCH. Never silently accepted.
    """

    def replay(
        self,
        original_snapshot: Any,
        replay_input: Dict[str, Any],
        replay_output: Dict[str, Any],
        code_version: str = "1.6.4",
        metric_policy_version: str = "1.6.4",
        attribution_policy_version: str = "1.6.4",
    ) -> ReplayResult:
        replay_hash = _hash_dict({
            "input": _hash_dict(replay_input),
            "output": _hash_dict(replay_output),
            "code_version": code_version,
            "metric_policy_version": metric_policy_version,
            "attribution_policy_version": attribution_policy_version,
        })
        original_hash = getattr(original_snapshot, "reproducibility_hash", "")

        if not original_hash:
            return ReplayResult(
                original_hash=original_hash,
                replay_hash=replay_hash,
                status=ReproducibilityStatus.INCOMPLETE,
                details="Original snapshot has no reproducibility_hash",
            )

        if replay_hash == original_hash:
            status = ReproducibilityStatus.MATCH
            details = "Hashes match — result is reproducible"
        else:
            status = ReproducibilityStatus.MISMATCH
            details = (
                f"REPRODUCIBILITY_MISMATCH: "
                f"original={original_hash[:16]}... "
                f"replay={replay_hash[:16]}..."
            )

        return ReplayResult(
            original_hash=original_hash,
            replay_hash=replay_hash,
            status=status,
            details=details,
        )


__all__ = ["AnalyticsReplayer", "ReplayResult"]
