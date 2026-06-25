"""
data/governance/quality/authority_gate_v146.py — Authority Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Uses v1.4.5 SourceAuthorityLevel. Primary wins, secondary cannot override, mock blocked.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.models_v145 import SourceAuthorityLevel
from data.governance.source_authority_v145 import SourceAuthorityRegistry
from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_registry = SourceAuthorityRegistry()


class AuthorityGate:
    """
    Authority check using v1.4.5 SourceAuthorityLevel.
    Primary wins. Secondary cannot override primary.
    Mock/TEST_FIXTURE/UNKNOWN → blocked from formal real use.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        provider_id = ctx.get("provider_id", subject_id)
        challenger_level = ctx.get("challenger_authority_level")
        incumbent_level = ctx.get("incumbent_authority_level")
        formal_use = ctx.get("formal_use", False)

        authority_level = _registry.get_authority(provider_id)
        is_formal_allowed = _registry.is_formal_allowed(authority_level)

        # Check if challenger can override incumbent
        if challenger_level and incumbent_level:
            try:
                challenger = SourceAuthorityLevel(challenger_level)
                incumbent = SourceAuthorityLevel(incumbent_level)
                can_override = _registry.can_override(challenger, incumbent)
            except ValueError:
                can_override = False

            if not can_override and formal_use:
                return QualityGateResult(
                    gate_id="authority_hierarchy", gate_name="Authority Hierarchy Gate",
                    scope="DATASET", subject_id=subject_id,
                    status=GateStatus.FAIL.value, passed=False, blocking=True,
                    evidence=(
                        f"Authority override rejected: {challenger_level} cannot override "
                        f"{incumbent_level}"
                    ),
                    evaluated_at=now, policy_version=self.POLICY_VERSION,
                )

        # Check formal use allowed for this authority level
        if formal_use and not is_formal_allowed:
            return QualityGateResult(
                gate_id="authority_hierarchy", gate_name="Authority Hierarchy Gate",
                scope="DATASET", subject_id=subject_id,
                status=GateStatus.BLOCKED.value, passed=False, blocking=True,
                evidence=(
                    f"Authority level {authority_level.value} not allowed for formal use "
                    "(MOCK/TEST_FIXTURE/UNKNOWN blocked)"
                ),
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        return QualityGateResult(
            gate_id="authority_hierarchy", gate_name="Authority Hierarchy Gate",
            scope="DATASET", subject_id=subject_id,
            status=GateStatus.PASS.value, passed=True, blocking=False,
            evidence=f"Authority: {authority_level.value}, formal_allowed={is_formal_allowed}",
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
