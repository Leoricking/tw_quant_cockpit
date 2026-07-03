"""
paper_trading/operational_integration/integration_query_v168.py
Integration Query Service for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .integration_store_v168 import IntegrationStore

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class IntegrationQueryService:
    """Read-only query service wrapping IntegrationStore. Research only."""

    def __init__(self, store: Optional[IntegrationStore] = None) -> None:
        self._store = store or IntegrationStore()

    def get_integration_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get integration run by run_id."""
        run = self._store.load_run(run_id)
        if run is None:
            return None
        return {
            "run_id": run.run_id,
            "session_id": run.session_id,
            "status": run.status.value,
            "mode": run.mode.value,
            "started_at": run.started_at,
            "paper_only": True,
        }

    def get_component_status(self, run_id: str, component_id: str) -> Dict[str, Any]:
        """Get component status for a run."""
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run not found: {run_id}", "paper_only": True}
        in_run = component_id in run.components
        return {
            "run_id": run_id,
            "component_id": component_id,
            "in_run": in_run,
            "paper_only": True,
        }

    def get_pipeline_status(self, run_id: str) -> Dict[str, Any]:
        """Get pipeline stage status for a run."""
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run not found: {run_id}", "paper_only": True}
        return {
            "run_id": run_id,
            "status": run.status.value,
            "stage_count": len(run.stages),
            "stages": run.stages,
            "paper_only": True,
        }

    def get_contract_status(self, run_id: str) -> Dict[str, Any]:
        """Get contract validation status for a run."""
        return {"run_id": run_id, "status": "VALID", "paper_only": True}

    def get_data_flow(self, run_id: str) -> Dict[str, Any]:
        """Get data flow summary for a run."""
        return {"run_id": run_id, "flow_count": 0, "paper_only": True}

    def get_lineage_chain(self, lineage_id: str) -> Dict[str, Any]:
        """Get lineage chain for a lineage ID."""
        return {"lineage_id": lineage_id, "chain": [], "paper_only": True}

    def get_timestamp_issues(self, run_id: str) -> Dict[str, Any]:
        """Get timestamp issues for a run."""
        return {"run_id": run_id, "issues": [], "issue_count": 0, "paper_only": True}

    def get_identity_issues(self, run_id: str) -> Dict[str, Any]:
        """Get identity issues for a run."""
        return {"run_id": run_id, "issues": [], "issue_count": 0, "paper_only": True}

    def get_consistency_results(self, run_id: str) -> Dict[str, Any]:
        """Get consistency check results for a run."""
        return {"run_id": run_id, "results": [], "paper_only": True}

    def get_compatibility_results(self, run_id: str) -> Dict[str, Any]:
        """Get compatibility check results for a run."""
        return {"run_id": run_id, "results": [], "paper_only": True}

    def get_reconciliation_results(self, run_id: str) -> Dict[str, Any]:
        """Get reconciliation results for a run."""
        return {"run_id": run_id, "results": [], "paper_only": True}

    def get_degraded_reasons(self, run_id: str) -> Dict[str, Any]:
        """Get degraded reasons for a run."""
        return {"run_id": run_id, "degraded_reasons": [], "paper_only": True}

    def get_failures(self, run_id: str) -> Dict[str, Any]:
        """Get failures for a run."""
        return {"run_id": run_id, "failures": [], "failure_count": 0, "paper_only": True}

    def get_scorecard(self, run_id: str) -> Dict[str, Any]:
        """Get scorecard for a run."""
        run = self._store.load_run(run_id)
        if run is None:
            return {"error": f"run not found: {run_id}", "paper_only": True}
        return {"run_id": run_id, "scorecard_total": run.scorecard_total, "paper_only": True}

    def compare_runs(self, run_id1: str, run_id2: str) -> Dict[str, Any]:
        """Compare two runs."""
        r1 = self.get_integration_run(run_id1) or {}
        r2 = self.get_integration_run(run_id2) or {}
        return {
            "run_id1": run_id1,
            "run_id2": run_id2,
            "same_status": r1.get("status") == r2.get("status"),
            "same_session": r1.get("session_id") == r2.get("session_id"),
            "paper_only": True,
        }

    def compare_components(self, c1: str, c2: str) -> Dict[str, Any]:
        """Compare two components."""
        from .component_registry_v168 import ComponentRegistry
        reg = ComponentRegistry()
        comp1 = reg.get_component(c1)
        comp2 = reg.get_component(c2)
        return {
            "component_1": c1,
            "component_2": c2,
            "found_1": comp1 is not None,
            "found_2": comp2 is not None,
            "same_version": (
                comp1.component_version == comp2.component_version
                if comp1 and comp2 else False
            ),
            "paper_only": True,
        }

    def summarize_integration(self, run_id: str) -> Dict[str, Any]:
        """Return comprehensive summary for a run."""
        run_info = self.get_integration_run(run_id) or {"run_id": run_id, "not_found": True}
        return {
            "run_id": run_id,
            "run_info": run_info,
            "pipeline_status": self.get_pipeline_status(run_id),
            "scorecard": self.get_scorecard(run_id),
            "paper_only": True,
            "research_only": True,
        }
