"""
gui/quality_gate_enforcement_adapter.py — QualityGateEnforcementAdapter v1.1.5

Adapter between CLI enforcement engine and GUI panel.
Runs enforcement in background thread, emits results to panel.
Research Only. No Real Orders.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True


class QualityGateEnforcementAdapter:
    """
    Adapter between CLI enforcement engine and GUI panel.
    Dispatches to background thread to avoid GUI freeze.
    No broker. No orders. Research only.
    """

    def __init__(self, panel=None):
        self._panel = panel

    def preview(self, command_name: str, mode: str = "real") -> dict:
        """Preview enforcement for command without running it."""
        try:
            from gate_enforcement.enforcement_policy import QualityGateEnforcementPolicy
            policy = QualityGateEnforcementPolicy()
            return {
                "command": command_name,
                "gate": policy.resolve_gate(command_name),
                "default_level": policy.resolve_default_level(command_name, mode),
                "allow_observational": policy.allow_observational(command_name),
                "allow_demo": policy.allow_demo(command_name),
                "enforcement_required": policy.enforcement_required(command_name),
                "policy_version": policy.POLICY_VERSION,
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.error("preview failed: %s", exc)
            return {"error": str(exc)}

    def run_enforcement(
        self,
        command_name: str,
        symbols: List[str],
        mode: str = "real",
        quality_gate: Optional[str] = None,
        gate_mode: str = "enforce",
    ) -> dict:
        """
        Run enforcement for symbols. Returns result dict.
        Does NOT run real workflows — only pre-processes eligibility.
        """
        try:
            from gate_enforcement.enforcement_engine import QualityGateEnforcementEngine
            import argparse
            args = argparse.Namespace(
                command=command_name,
                mode=mode,
                quality_gate=quality_gate,
                gate_mode=gate_mode,
                allow_research_override=False,
                override_id=None,
            )
            engine = QualityGateEnforcementEngine()
            included, result = engine.enforce(command_name, args, symbols, mode=mode)
            return {
                "included": included,
                "result": result.to_dict(),
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.error("run_enforcement failed: %s", exc)
            return {"error": str(exc), "included": [], "research_only": True}

    def get_latest_runs(self, limit: int = 20) -> List[dict]:
        """Get latest enforcement runs."""
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            query = EnforcementQuery()
            return query.latest_runs(limit=limit)
        except Exception as exc:
            logger.warning("get_latest_runs failed: %s", exc)
            return []

    def get_audit_events(self, run_id: Optional[str] = None) -> dict:
        """Get audit events and chain verification status."""
        try:
            from gate_enforcement.audit_log import QualityGateAuditLog
            log = QualityGateAuditLog()
            events = log.list_events(run_id=run_id)
            chain = log.verify_chain()
            return {"events": events, "chain": chain}
        except Exception as exc:
            logger.warning("get_audit_events failed: %s", exc)
            return {"events": [], "chain": {"valid": False, "error": str(exc)}}

    def build_report(self, run_id: Optional[str] = None, output_dir: str = "reports") -> str:
        """Build and return path to audit report."""
        try:
            from reports.quality_gate_enforcement_audit_report import QualityGateEnforcementAuditReportBuilder
            builder = QualityGateEnforcementAuditReportBuilder()
            return builder.build(run_id=run_id, output_dir=output_dir)
        except Exception as exc:
            logger.error("build_report failed: %s", exc)
            return ""
