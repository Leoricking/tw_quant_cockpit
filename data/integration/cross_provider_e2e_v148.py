"""
data/integration/cross_provider_e2e_v148.py — Cross-Provider E2E Scenarios v1.4.8.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Offline E2E validation only. No live fetch. No mock fallback.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from .models_v148 import E2EScenarioResult, IntegrationStatus

logger = logging.getLogger(__name__)

SCENARIOS = [
    {"id": "A", "name": "Listed stock full research chain",
     "providers": ["twse_official", "mops_official", "data_gov_tw_official", "finmind", "ptt_stock_public"]},
    {"id": "B", "name": "OTC stock full research chain",
     "providers": ["tpex_official", "mops_official", "data_gov_tw_official", "finmind", "ptt_stock_public"]},
    {"id": "C", "name": "FinMind vs official conflict",
     "providers": ["twse_official", "finmind"]},
    {"id": "D", "name": "Forum sentiment vs official contradiction",
     "providers": ["twse_official", "ptt_stock_public"]},
    {"id": "E", "name": "MOPS revision",
     "providers": ["mops_official"]},
    {"id": "F", "name": "Partial provider outage",
     "providers": ["twse_official", "data_gov_tw_official", "finmind", "ptt_stock_public"]},
    {"id": "G", "name": "Storage migration upgrade",
     "providers": ["twse_official", "tpex_official", "mops_official"]},
    {"id": "H", "name": "Runtime DB corrupt",
     "providers": ["twse_official"]},
]


class CrossProviderE2EValidator:
    """Runs offline E2E scenario checks across providers."""

    VERSION = "1.4.8"
    AUTO_FALLBACK_ENABLED   = False
    MOCK_FALLBACK_ENABLED   = False
    AUTO_REPAIR_ENABLED     = False

    def run_all(self) -> List[E2EScenarioResult]:
        return [self._run_scenario(s) for s in SCENARIOS]

    def run_scenario(self, scenario_id: str) -> E2EScenarioResult:
        for s in SCENARIOS:
            if s["id"] == scenario_id:
                return self._run_scenario(s)
        return E2EScenarioResult(
            scenario_id=scenario_id, name="Unknown",
            status=IntegrationStatus.FAIL, detail="Scenario not found"
        )

    def _run_scenario(self, scenario: Dict[str, Any]) -> E2EScenarioResult:
        sid = scenario["id"]
        name = scenario["name"]
        providers = scenario["providers"]

        pit_valid     = self._check_pit(sid)
        lineage_valid = self._check_lineage(sid)
        conflict_valid = self._check_conflict(sid)

        all_ok = pit_valid and lineage_valid and conflict_valid
        status = IntegrationStatus.PASS if all_ok else IntegrationStatus.FAIL
        detail = (
            f"pit={pit_valid} lineage={lineage_valid} conflict={conflict_valid}"
        )
        return E2EScenarioResult(
            scenario_id=sid, name=name, providers=list(providers),
            pit_valid=pit_valid, lineage_valid=lineage_valid,
            conflict_valid=conflict_valid, status=status, detail=detail,
        )

    # ------------------------------------------------------------------
    # Per-scenario offline checks
    # ------------------------------------------------------------------

    def _check_pit(self, scenario_id: str) -> bool:
        from .cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        return v.check_scenario(scenario_id)

    def _check_lineage(self, scenario_id: str) -> bool:
        from .cross_provider_lineage_v148 import CrossProviderLineageValidator
        v = CrossProviderLineageValidator()
        return v.check_scenario(scenario_id)

    def _check_conflict(self, scenario_id: str) -> bool:
        from .cross_provider_conflict_v148 import CrossProviderConflictValidator
        v = CrossProviderConflictValidator()
        return v.check_scenario(scenario_id)

    def get_summary(self, results: List[E2EScenarioResult] = None) -> Dict[str, Any]:
        if results is None:
            results = self.run_all()
        passed = sum(1 for r in results if r.status == IntegrationStatus.PASS)
        return {
            "version": self.VERSION,
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "scenarios": [
                {"id": r.scenario_id, "name": r.name,
                 "status": r.status, "detail": r.detail}
                for r in results
            ],
        }
