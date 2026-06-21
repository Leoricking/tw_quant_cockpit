"""
data/governance/provenance_v145.py — Provenance Completeness Gate v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] PASS requires all mandatory fields. BLOCKED for mock in real mode.
[!] FAIL if source_hash missing, parser_version missing, or cache hit without source lineage.
"""
from __future__ import annotations

from typing import Any, Dict, List

from data.governance.models_v145 import ProvenanceGateResult, SourceLineageRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_PASS_REQUIRED_FIELDS = [
    "provider_id", "source_id", "authority_level", "dataset",
    "request_fingerprint", "fetched_at", "source_content_hash",
    "normalized_content_hash", "schema_version", "parser_version",
]

_BLOCKED_AUTHORITIES = {"MOCK", "TEST_FIXTURE"}


class ProvenanceCompletenessGate:
    """
    Gate for provenance completeness.
    PASS: all mandatory fields present, real mode, no mock fallback.
    BLOCKED: mock in real mode, fixture in formal conclusion, PIT required + unknown.
    FAIL: source_hash missing, parser_version missing, cache hit without source lineage.
    """

    def check(
        self,
        lineage: SourceLineageRecord,
        mode: str = "real",
        pit_required: bool = False,
    ) -> Dict[str, Any]:
        missing_fields: List[str] = []
        blocking_reasons: List[str] = []

        # Check required fields
        for f in _PASS_REQUIRED_FIELDS:
            val = getattr(lineage, f, None)
            if not val:
                missing_fields.append(f)

        # Observation date or reporting period required
        if not lineage.observation_date and not lineage.reporting_period:
            missing_fields.append("observation_date_or_reporting_period")

        # Check quality and freshness status
        if not lineage.quality_status:
            missing_fields.append("quality_status")
        if not lineage.freshness_status:
            missing_fields.append("freshness_status")

        # BLOCKED conditions
        if lineage.authority_level in _BLOCKED_AUTHORITIES and mode == "real":
            blocking_reasons.append(f"mock/fixture lineage ({lineage.authority_level}) in real mode")
        if lineage.authority_level == "MOCK":
            blocking_reasons.append("mock lineage cannot be used for formal conclusion")
        if lineage.authority_level == "TEST_FIXTURE":
            blocking_reasons.append("test fixture cannot be used for formal conclusion")
        if pit_required and not lineage.available_from:
            blocking_reasons.append("PIT required but available_from unknown")
        if lineage.authority_level == "PRIMARY_OFFICIAL" and not lineage.source_content_hash:
            blocking_reasons.append("PRIMARY_OFFICIAL missing source_content_hash lineage")

        # FAIL conditions
        fail_reasons: List[str] = []
        if not lineage.source_content_hash:
            fail_reasons.append("source_content_hash missing")
        if not lineage.parser_version:
            fail_reasons.append("parser_version missing")
        cache_hit = lineage.cache_entry_id and not lineage.source_id
        if cache_hit:
            fail_reasons.append("cache hit without source lineage")

        # Determine gate result
        if blocking_reasons:
            gate_result = ProvenanceGateResult.BLOCKED
        elif fail_reasons or missing_fields:
            gate_result = ProvenanceGateResult.FAIL
        else:
            gate_result = ProvenanceGateResult.PASS

        return {
            "gate_result": gate_result.value,
            "missing_fields": missing_fields,
            "blocking_reasons": blocking_reasons,
            "fail_reasons": fail_reasons,
            "passed": gate_result == ProvenanceGateResult.PASS,
        }
