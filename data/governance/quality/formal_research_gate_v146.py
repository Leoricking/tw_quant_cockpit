"""
data/governance/quality/formal_research_gate_v146.py — Formal Research Eligibility Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Returns FormalResearchEligibility (not just bool).
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import FormalResearchEligibility, GateStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_FORMAL_ALLOWED_AUTHORITIES = {
    "PRIMARY_OFFICIAL", "PRIMARY_DOMAIN_OFFICIAL", "SECONDARY_OFFICIAL",
}


class FormalResearchEligibilityGate:
    """
    All conditions for formal research use must be satisfied.
    MOCK/TEST_FIXTURE/UNKNOWN → BLOCKED for formal research.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, provider_id: str, dataset_id: str,
                 context: Optional[Dict[str, Any]] = None) -> FormalResearchEligibility:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        authority_level = ctx.get("authority_level", "UNKNOWN")
        provenance_complete = ctx.get("provenance_complete", False)
        pit_compliant = ctx.get("pit_compliant", False)
        schema_valid = ctx.get("schema_valid", False)
        no_conflicts = ctx.get("no_unresolved_conflicts", False)
        dataset_admitted = ctx.get("dataset_admitted", False)
        real_data = ctx.get("real_data", False)

        blocking_failures = []
        warnings = []

        # Authority check
        authority_sufficient = authority_level in _FORMAL_ALLOWED_AUTHORITIES
        if not authority_sufficient:
            blocking_failures.append(
                f"authority_insufficient: {authority_level} not allowed for formal research"
            )

        # Dataset admission
        if not dataset_admitted:
            blocking_failures.append("dataset_not_admitted")

        # Provenance
        if not provenance_complete:
            blocking_failures.append("provenance_incomplete")

        # PIT compliance
        if not pit_compliant:
            blocking_failures.append("pit_not_compliant")

        # Schema
        if not schema_valid:
            blocking_failures.append("schema_invalid")

        # Conflict check
        if not no_conflicts:
            blocking_failures.append("unresolved_conflicts_exist")

        # Real data required
        if not real_data:
            blocking_failures.append("real_data_not_confirmed")

        eligible = len(blocking_failures) == 0

        return FormalResearchEligibility(
            provider_id=provider_id,
            dataset_id=dataset_id,
            eligible=eligible,
            blocking_failures=blocking_failures,
            warnings=warnings,
            authority_sufficient=authority_sufficient,
            provenance_complete=provenance_complete,
            pit_compliant=pit_compliant,
            schema_valid=schema_valid,
            no_unresolved_conflicts=no_conflicts,
            evaluated_at=now,
            policy_version=self.POLICY_VERSION,
        )
