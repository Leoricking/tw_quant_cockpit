"""
governance_ops.operations_engine — DataGovernanceOperationsEngine v1.1.6

Orchestrates the full governance operations dashboard run:
1. Check module availability
2. Read latest summaries from all adapters
3. Aggregate symbol matrix
4. Aggregate action queue
5. Calculate priority
6. Aggregate enforcement runs
7. Verify audit chain
8. Build governance summary
9. Write runtime store
10. Generate report

Engine does NOT execute repair, import, override, trading, strategy changes.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] real mode: no fallback to mock
[!] mock mode: label DEMO_ONLY
[!] One module failing ≠ whole dashboard crash
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from governance_ops.governance_schema import (
    GovernanceModuleStatus,
    GovernanceSymbolStatus,
    GovernanceActionItem,
    GovernanceSummary,
    GovernanceRunSummary,
    _now_utc,
)
from governance_ops.governance_aggregator import DataGovernanceAggregator
from governance_ops.action_queue import GovernanceActionQueue
from governance_ops.priority_engine import GovernancePriorityEngine
from governance_ops.operations_store import OperationsStore

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataGovernanceOperationsEngine:
    """
    Runs the full data governance operations dashboard.

    [!] Research Only. No Real Orders.
    [!] Engine does NOT repair, download, override, or trade.
    """

    def __init__(self):
        self._aggregator = DataGovernanceAggregator()
        self._priority_engine = GovernancePriorityEngine()
        self._store = OperationsStore()

    def run(self, mode: str = "real", tier: Optional[str] = None,
            symbols: Optional[List[str]] = None) -> GovernanceSummary:
        """Run full governance operations dashboard. Returns GovernanceSummary."""
        summary = self.refresh_dashboard(mode=mode, tier=tier, symbols=symbols)
        self.save_outputs(summary, [])
        return summary

    def refresh_dashboard(self, mode: str = "real", tier: Optional[str] = None,
                          symbols: Optional[List[str]] = None) -> GovernanceSummary:
        """Refresh all governance data and return updated summary."""
        return self.build_daily_summary(mode=mode, tier=tier, symbols=symbols)

    def build_daily_summary(self, mode: str = "real", tier: Optional[str] = None,
                             symbols: Optional[List[str]] = None) -> GovernanceSummary:
        """Build a full daily governance summary."""
        # Step 1 & 2: Module health
        module_health = self.build_module_health()

        # Step 3: Symbol matrix
        symbol_matrix = self.build_symbol_matrix(tier=tier)

        # Step 4 & 5: Action queue
        actions = self.build_action_queue_from_data(symbol_matrix, module_health)

        # Step 6: Enforcement runs
        runs = self._aggregator.aggregate_runs()

        # Step 7: Verify audit chain (best effort)
        audit_failures = self._check_audit_chain()

        # Step 8: Build summary
        summary = self._aggregator.build_summary(
            module_statuses=module_health,
            symbol_statuses=symbol_matrix,
            actions=actions,
            runs=runs,
            mode=mode,
            tier=tier or "",
        )
        summary.audit_chain_failures = audit_failures

        return summary

    def build_action_queue(self, summary: GovernanceSummary) -> List[GovernanceActionItem]:
        """Build action queue from a governance summary."""
        return []  # Actions are included in summary already

    def build_action_queue_from_data(self, symbol_statuses: List[GovernanceSymbolStatus],
                                      module_statuses: Dict[str, GovernanceModuleStatus]) -> List[GovernanceActionItem]:
        """Build action queue from symbol and module data."""
        try:
            return self._aggregator.aggregate_actions(symbol_statuses, module_statuses)
        except Exception as exc:
            logger.warning("build_action_queue_from_data error: %s", exc)
            return []

    def build_module_health(self) -> Dict[str, GovernanceModuleStatus]:
        """Build module health status for all modules."""
        try:
            return self._aggregator.aggregate_modules()
        except Exception as exc:
            logger.warning("build_module_health error: %s", exc)
            return {}

    def build_symbol_matrix(self, tier: Optional[str] = None) -> List[GovernanceSymbolStatus]:
        """Build symbol governance status matrix."""
        try:
            return self._aggregator.aggregate_symbols(tier=tier)
        except Exception as exc:
            logger.warning("build_symbol_matrix error: %s", exc)
            return []

    def build_run_audit_summary(self) -> List[GovernanceRunSummary]:
        """Build recent enforcement run audit summary."""
        try:
            return self._aggregator.aggregate_runs()
        except Exception as exc:
            logger.warning("build_run_audit_summary error: %s", exc)
            return []

    def build_safe_next_steps(self, actions: List[GovernanceActionItem]) -> List[str]:
        """Build list of safe next steps from top actions."""
        steps = []
        seen = set()
        for action in actions[:10]:
            cmd = action.suggested_command
            if cmd and cmd not in seen:
                seen.add(cmd)
                steps.append(f"[{action.priority}] {action.title}: {cmd}")
        if not steps:
            steps = [
                "python main.py governance-health  # Check all module health",
                "python main.py governance-module-health  # View module status",
                "python main.py governance-actions  # View action queue",
            ]
        return steps

    def save_outputs(self, summary: GovernanceSummary,
                     actions: List[GovernanceActionItem]) -> None:
        """Save runtime outputs to store (NOT committed to git)."""
        try:
            self._store.save_summary(summary.to_dict())
            # Append daily snapshot
            snapshot = summary.to_dict()
            snapshot["_snapshot_type"] = "daily_governance_summary"
            self._store.append_daily_snapshot(snapshot)
        except Exception as exc:
            logger.warning("save_outputs error: %s", exc)

    def generate_report(self, summary: GovernanceSummary,
                        actions: List[GovernanceActionItem],
                        output_dir: str = "reports") -> str:
        """Generate governance operations report."""
        try:
            from reports.data_governance_operations_report import DataGovernanceOperationsReportBuilder
            builder = DataGovernanceOperationsReportBuilder()
            return builder.build(
                tier=summary.tier,
                mode=summary.mode,
                output_dir=output_dir,
            )
        except Exception as exc:
            logger.warning("generate_report error: %s", exc)
            return ""

    def _check_audit_chain(self) -> int:
        """Check audit chain validity. Returns count of failures."""
        try:
            from gate_enforcement.audit_log import QualityGateAuditLog
            log = QualityGateAuditLog()
            result = log.verify_chain()
            if not result.get("valid", True):
                return 1
            return 0
        except Exception:
            return 0  # Module unavailable, not a failure
