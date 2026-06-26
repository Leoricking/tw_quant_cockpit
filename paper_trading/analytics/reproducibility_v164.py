"""
paper_trading/analytics/reproducibility_v164.py — Analytics Reproducibility v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Same seed + same data version = same result. Mismatch always explicit.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional

from paper_trading.analytics.enums_v164 import ReproducibilityStatus
from paper_trading.analytics.snapshot_v164 import _hash_dict

NO_REAL_ORDERS = True
PAPER_ONLY = True
SILENT_MISMATCH_ACCEPTANCE = False


@dataclass
class ReproducibilityRecord:
    analytics_id: str
    input_hash: str
    output_hash: str
    reproducibility_hash: str
    code_version: str
    metric_policy_version: str
    status: ReproducibilityStatus
    paper_only: bool = True


class ReproducibilityChecker:
    """
    Checks that analytics results are reproducible.
    Mismatch → explicit status. Never silently accepted.
    """

    def record(
        self,
        analytics_id: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        code_version: str = "1.6.4",
        metric_policy_version: str = "1.6.4",
    ) -> ReproducibilityRecord:
        input_hash = _hash_dict(input_data)
        output_hash = _hash_dict(output_data)
        repro_hash = _hash_dict({
            "input": input_hash,
            "output": output_hash,
            "code_version": code_version,
            "metric_policy_version": metric_policy_version,
        })
        return ReproducibilityRecord(
            analytics_id=analytics_id,
            input_hash=input_hash,
            output_hash=output_hash,
            reproducibility_hash=repro_hash,
            code_version=code_version,
            metric_policy_version=metric_policy_version,
            status=ReproducibilityStatus.MATCH,
        )

    def verify(
        self,
        original: ReproducibilityRecord,
        replay: ReproducibilityRecord,
    ) -> ReproducibilityStatus:
        if original.reproducibility_hash == replay.reproducibility_hash:
            return ReproducibilityStatus.MATCH
        return ReproducibilityStatus.MISMATCH


__all__ = ["ReproducibilityChecker", "ReproducibilityRecord"]
