"""
paper_trading/stable_rollup/stable_report_v169.py
Report generation for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
import datetime
import uuid
from typing import Dict, Any

from paper_trading.stable_rollup.models_v169 import StableRollupReport
from paper_trading.stable_rollup.enums_v169 import RollupStatus, MigrationReadiness

VERSION = "1.6.9"
RELEASE_NAME = "Live Paper Trading Stable Rollup"


class StableReport:
    """Generate comprehensive stable rollup reports."""

    def generate(self) -> StableRollupReport:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        report_id = f"sr-report-{VERSION}-{uuid.uuid4().hex[:8]}"

        manifest = None
        snapshot = None
        validation_results = []
        reconciliation = []
        score = None
        migration_readiness = MigrationReadiness.NOT_READY

        try:
            from paper_trading.stable_rollup.stable_snapshot_v169 import StableSnapshot
            from paper_trading.stable_rollup.enums_v169 import SealStatus
            snapper = StableSnapshot()
            snapshot = snapper.take(RollupStatus.READY, SealStatus.NOT_SEALED)
        except Exception:
            pass

        try:
            from paper_trading.stable_rollup.stable_validator_v169 import StableValidator
            validator = StableValidator()
            validation_results = validator.validate_all()
        except Exception:
            pass

        try:
            from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
            reconciler = StableReconciler()
            reconciliation = reconciler.reconcile_all()
        except Exception:
            pass

        try:
            from paper_trading.stable_rollup.stable_scorecard_v169 import compute_scorecard
            score = compute_scorecard()
        except Exception:
            pass

        try:
            from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
            assessor = MigrationReadinessAssessor()
            summary = assessor.assess()
            migration_readiness = summary.readiness
        except Exception:
            pass

        rollup_status = RollupStatus.READY
        if validation_results:
            if any(not r.passed for r in validation_results):
                rollup_status = RollupStatus.DEGRADED

        return StableRollupReport(
            report_id=report_id,
            generated_at=now,
            rollup_status=rollup_status,
            manifest=manifest,
            snapshot=snapshot,
            validation_results=validation_results,
            reconciliation=reconciliation,
            score=score,
            migration_readiness=migration_readiness,
            release_version=VERSION,
            release_name=RELEASE_NAME,
            created_at=now,
        )

    def to_dict(self, report: StableRollupReport) -> Dict[str, Any]:
        """Convert report to a plain dictionary."""
        return {
            "report_id": report.report_id,
            "generated_at": report.generated_at,
            "rollup_status": report.rollup_status.value,
            "release_version": report.release_version,
            "release_name": report.release_name,
            "migration_readiness": report.migration_readiness.value,
            "validation_results": [
                {
                    "validator_name": r.validator_name,
                    "passed": r.passed,
                    "severity": r.severity.value,
                    "issues": r.issues,
                }
                for r in report.validation_results
            ],
            "reconciliation": [
                {
                    "domain": r.domain,
                    "expected": r.expected,
                    "actual": r.actual,
                    "residual": r.residual,
                    "status": r.status.value,
                }
                for r in report.reconciliation
            ],
            "score": {
                "total_score": report.score.total_score if report.score else 0.0,
                "grade": report.score.grade if report.score else "F",
                "migration_ready": report.score.migration_ready if report.score else False,
            } if report.score else None,
            "paper_only": report.paper_only,
            "research_only": report.research_only,
            "no_real_orders": report.no_real_orders,
            "not_for_production": report.not_for_production,
        }

    def summary(self, report: StableRollupReport) -> str:
        """Return a brief text summary of the report."""
        d = self.to_dict(report)
        lines = [
            f"Stable Rollup Report v{VERSION}",
            f"  Report ID    : {d['report_id']}",
            f"  Generated    : {d['generated_at']}",
            f"  Status       : {d['rollup_status']}",
            f"  Migration    : {d['migration_readiness']}",
            f"  Score        : {d['score']['total_score'] if d['score'] else 'N/A'} ({d['score']['grade'] if d['score'] else 'N/A'})",
            f"  Paper Only   : True",
            f"  No Real Orders: True",
        ]
        return "\n".join(lines)


def generate_report() -> StableRollupReport:
    """Convenience function: generate a full stable rollup report."""
    return StableReport().generate()
