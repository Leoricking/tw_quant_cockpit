"""
data/governance/quality/report_gate_v146.py — Report Eligibility Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] BLOCKED section → no mock fill. Show BLOCKED/MISSING/DEGRADED.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import GateStatus, ReportSectionEligibility

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ReportEligibilityGate:
    """Per-section report eligibility evaluation. BLOCKED sections show BLOCKED/MISSING."""

    POLICY_VERSION = "1.4.6"

    def evaluate_section(self, section_id: str, provider_id: str, dataset_id: str,
                         context: Optional[Dict[str, Any]] = None) -> ReportSectionEligibility:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"

        source_ok = ctx.get("source_valid", False)
        authority_ok = ctx.get("authority_valid", False)
        lineage_ok = ctx.get("lineage_valid", False)
        freshness_ok = ctx.get("freshness_ok", False)
        quality_ok = ctx.get("quality_ok", False)
        pit_ok = ctx.get("pit_ok", False)
        no_conflict = ctx.get("no_conflict", False)

        blocking_failures = []
        warnings = []

        if not source_ok:
            blocking_failures.append("source_not_valid")
        if not authority_ok:
            blocking_failures.append("authority_not_valid")
        if not lineage_ok:
            blocking_failures.append("lineage_not_valid")
        if not quality_ok:
            blocking_failures.append("quality_gate_failed")
        if not pit_ok:
            blocking_failures.append("pit_not_compliant")

        if not freshness_ok:
            warnings.append("data_not_fresh")
        if not no_conflict:
            warnings.append("unresolved_conflicts_present")

        eligible = len(blocking_failures) == 0
        if blocking_failures:
            status = "BLOCKED"
        elif warnings:
            status = "DEGRADED"
        else:
            status = "ALLOWED"

        return ReportSectionEligibility(
            section_id=section_id,
            provider_id=provider_id,
            dataset_id=dataset_id,
            eligible=eligible,
            status=status,
            blocking_failures=blocking_failures,
            warnings=warnings,
            no_mock_fill=True,  # BLOCKED → no mock fill, always True
            evaluated_at=now,
            policy_version=self.POLICY_VERSION,
        )

    def evaluate_report(self, sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate all sections of a report."""
        results = []
        blocked_sections = []
        degraded_sections = []

        for s in sections:
            result = self.evaluate_section(
                section_id=s.get("section_id", "unknown"),
                provider_id=s.get("provider_id", "unknown"),
                dataset_id=s.get("dataset_id", "unknown"),
                context=s.get("context", {}),
            )
            results.append(result.to_dict())
            if result.status == "BLOCKED":
                blocked_sections.append(result.section_id)
            elif result.status == "DEGRADED":
                degraded_sections.append(result.section_id)

        return {
            "total_sections": len(results),
            "blocked_sections": blocked_sections,
            "degraded_sections": degraded_sections,
            "allowed_sections": len(results) - len(blocked_sections) - len(degraded_sections),
            "report_eligible": len(blocked_sections) == 0,
            "sections": results,
            "policy_version": self.POLICY_VERSION,
        }
