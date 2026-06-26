"""
paper_trading/analytics/recovery_impact_v164.py — Recovery Impact Analysis v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True
AUTO_RESUME_RUNNING = False


@dataclass
class RecoveryImpactAnalysis:
    session_id: str
    recovery_count: int = 0
    successful_recoveries: int = 0
    failed_recoveries: int = 0
    recovery_success_rate: Optional[Decimal] = None
    mean_recovery_duration_seconds: Optional[Decimal] = None
    checkpoint_restore_count: int = 0
    checkpoint_effectiveness: Optional[Decimal] = None
    repeated_incident_patterns: List[str] = field(default_factory=list)
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True
    auto_resume: bool = False

    def validate_no_auto_resume(self) -> None:
        if self.auto_resume:
            raise ValueError("auto_resume is forbidden. All recovery is manual / research-only.")


class RecoveryImpactAnalyzer:

    def analyze(
        self,
        session_id: str,
        recovery_records: List[Dict[str, Any]],
        checkpoint_restore_count: int = 0,
    ) -> RecoveryImpactAnalysis:
        total = len(recovery_records)
        successful = sum(1 for r in recovery_records if r.get("success") is True)
        failed = total - successful

        success_rate: Optional[Decimal] = None
        if total > 0:
            success_rate = Decimal(str(successful)) / Decimal(str(total))

        durations = [Decimal(str(r["duration_seconds"])) for r in recovery_records
                     if r.get("duration_seconds") is not None]
        mean_dur = (sum(durations) / Decimal(str(len(durations)))) if durations else None

        checkpoint_eff: Optional[Decimal] = None
        if total > 0 and checkpoint_restore_count > 0:
            checkpoint_eff = Decimal(str(checkpoint_restore_count)) / Decimal(str(total))

        result = RecoveryImpactAnalysis(
            session_id=session_id,
            recovery_count=total,
            successful_recoveries=successful,
            failed_recoveries=failed,
            recovery_success_rate=success_rate,
            mean_recovery_duration_seconds=mean_dur,
            checkpoint_restore_count=checkpoint_restore_count,
            checkpoint_effectiveness=checkpoint_eff,
            quality=MetricQuality.VALID if total > 0 else MetricQuality.INSUFFICIENT_DATA,
            auto_resume=False,
        )
        result.validate_no_auto_resume()
        return result


__all__ = ["RecoveryImpactAnalysis", "RecoveryImpactAnalyzer"]
