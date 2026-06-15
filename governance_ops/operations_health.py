"""
governance_ops.operations_health — DataGovernanceOperationsHealthCheck v1.1.6

Health checks for the governance operations dashboard subsystem.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataGovernanceOperationsHealthCheck:
    """
    Runs health checks on the governance operations dashboard subsystem.
    Returns list of (check_name, status, message) tuples.
    Statuses: PASS / WARN / FAIL / BLOCKED
    """

    def run(self) -> List[Tuple[str, str, str]]:
        results = []
        checks = [
            self._check_package_import,
            self._check_schema_available,
            self._check_adapters_available,
            self._check_universe_integration,
            self._check_onboarding_integration,
            self._check_repair_integration,
            self._check_freshness_integration,
            self._check_quality_gates_integration,
            self._check_enforcement_integration,
            self._check_report_pack_integration,
            self._check_action_queue_available,
            self._check_deduplication_works,
            self._check_priority_engine_works,
            self._check_module_failure_graceful,
            self._check_runtime_output_ignored,
            self._check_no_auto_repair,
            self._check_no_auto_download,
            self._check_no_gate_override,
            self._check_no_trade_execution,
            self._check_no_broker_execution,
            self._check_no_forbidden_actions,
        ]
        for fn in checks:
            try:
                name, status, msg = fn()
            except Exception as exc:
                name = fn.__name__
                status = "FAIL"
                msg = f"Exception: {exc}"
            results.append((name, status, msg))
        return results

    def _check_package_import(self):
        name = "governance_ops_package_import"
        try:
            import governance_ops
            ok = getattr(governance_ops, "NO_REAL_ORDERS", False) is True
            return name, ("PASS" if ok else "FAIL"), "NO_REAL_ORDERS=True" if ok else "NO_REAL_ORDERS missing"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_schema_available(self):
        name = "governance_schema_available"
        try:
            from governance_ops.governance_schema import (
                GovernanceSummary, GovernanceActionItem, GovernanceModuleStatus, GovernanceSymbolStatus
            )
            return name, "PASS", "All schema classes importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_adapters_available(self):
        name = "governance_adapters_available"
        try:
            from governance_ops.governance_adapters import (
                UniverseGovernanceAdapter,
                OnboardingGovernanceAdapter,
                RepairGovernanceAdapter,
                FreshnessGovernanceAdapter,
                QualityGateGovernanceAdapter,
                EnforcementGovernanceAdapter,
                ReportPackGovernanceAdapter,
                SystemHealthGovernanceAdapter,
            )
            return name, "PASS", "All adapters importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_universe_integration(self):
        name = "universe_integration"
        try:
            from governance_ops.governance_adapters import UniverseGovernanceAdapter
            adapter = UniverseGovernanceAdapter()
            status = adapter.health()
            avail = adapter.available()
            return name, ("PASS" if avail else "WARN"), f"available={avail}, health={status.health_status}"
        except Exception as exc:
            return name, "WARN", f"universe adapter error: {exc}"

    def _check_onboarding_integration(self):
        name = "onboarding_integration"
        try:
            from governance_ops.governance_adapters import OnboardingGovernanceAdapter
            adapter = OnboardingGovernanceAdapter()
            avail = adapter.available()
            return name, ("PASS" if avail else "WARN"), f"available={avail}"
        except Exception as exc:
            return name, "WARN", f"onboarding adapter error: {exc}"

    def _check_repair_integration(self):
        name = "repair_integration"
        try:
            from governance_ops.governance_adapters import RepairGovernanceAdapter
            adapter = RepairGovernanceAdapter()
            avail = adapter.available()
            return name, ("PASS" if avail else "WARN"), f"available={avail}"
        except Exception as exc:
            return name, "WARN", f"repair adapter error: {exc}"

    def _check_freshness_integration(self):
        name = "freshness_integration"
        try:
            from governance_ops.governance_adapters import FreshnessGovernanceAdapter
            adapter = FreshnessGovernanceAdapter()
            avail = adapter.available()
            return name, ("PASS" if avail else "WARN"), f"available={avail}"
        except Exception as exc:
            return name, "WARN", f"freshness adapter error: {exc}"

    def _check_quality_gates_integration(self):
        name = "quality_gates_integration"
        try:
            from governance_ops.governance_adapters import QualityGateGovernanceAdapter
            adapter = QualityGateGovernanceAdapter()
            avail = adapter.available()
            return name, ("PASS" if avail else "WARN"), f"available={avail}"
        except Exception as exc:
            return name, "WARN", f"quality gates adapter error: {exc}"

    def _check_enforcement_integration(self):
        name = "enforcement_integration"
        try:
            from governance_ops.governance_adapters import EnforcementGovernanceAdapter
            adapter = EnforcementGovernanceAdapter()
            avail = adapter.available()
            return name, ("PASS" if avail else "WARN"), f"available={avail}"
        except Exception as exc:
            return name, "WARN", f"enforcement adapter error: {exc}"

    def _check_report_pack_integration(self):
        name = "report_pack_integration"
        try:
            from governance_ops.governance_adapters import ReportPackGovernanceAdapter
            adapter = ReportPackGovernanceAdapter()
            avail = adapter.available()
            return name, ("PASS" if avail else "WARN"), f"available={avail}"
        except Exception as exc:
            return name, "WARN", f"report pack adapter error: {exc}"

    def _check_action_queue_available(self):
        name = "action_queue_available"
        try:
            from governance_ops.action_queue import GovernanceActionQueue
            q = GovernanceActionQueue()
            ok = hasattr(q, "deduplicate") and hasattr(q, "prioritize") and hasattr(q, "acknowledge")
            return name, ("PASS" if ok else "FAIL"), "GovernanceActionQueue importable with required methods"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_deduplication_works(self):
        name = "deduplication_works"
        try:
            from governance_ops.action_queue import GovernanceActionQueue
            from governance_ops.governance_schema import GovernanceActionItem
            q = GovernanceActionQueue()
            item1 = GovernanceActionItem(
                action_id="test-1",
                priority="P1",
                action_type="REVIEW_CONFLICT",
                symbol="TST001",
                reason_codes=["CONFLICT"],
            )
            item2 = GovernanceActionItem(
                action_id="test-2",
                priority="P1",
                action_type="REVIEW_CONFLICT",
                symbol="TST001",
                reason_codes=["CONFLICT"],
            )
            deduped = q.deduplicate([item1, item2])
            ok = len(deduped) == 1
            return name, ("PASS" if ok else "FAIL"), f"deduplicated 2 → {len(deduped)}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_priority_engine_works(self):
        name = "priority_engine_works"
        try:
            from governance_ops.priority_engine import GovernancePriorityEngine
            from governance_ops.governance_schema import GovernanceActionItem
            engine = GovernancePriorityEngine()
            item = GovernanceActionItem(
                action_id="test-p0",
                priority="P3",
                action_type="REVIEW_CONFLICT",
                symbol="TST001",
                reason_codes=["AUDIT_CHAIN_INVALID"],
            )
            p = engine.assign_priority(item)
            ok = p == "P0"
            return name, ("PASS" if ok else "FAIL"), f"AUDIT_CHAIN_INVALID → priority={p}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_module_failure_graceful(self):
        name = "module_failure_graceful"
        try:
            from governance_ops.governance_aggregator import DataGovernanceAggregator
            agg = DataGovernanceAggregator()
            modules = agg.aggregate_modules()
            # Should return dict without crash even if modules unavailable
            ok = isinstance(modules, dict)
            return name, ("PASS" if ok else "FAIL"), f"aggregate_modules returned dict: {ok}"
        except Exception as exc:
            return name, "FAIL", f"Module failure not graceful: {exc}"

    def _check_runtime_output_ignored(self):
        name = "runtime_output_not_committed"
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        if not os.path.isfile(gitignore_path):
            return name, "WARN", ".gitignore not found"
        try:
            with open(gitignore_path, encoding="utf-8") as f:
                content = f.read()
            ok = "governance_ops" in content or "data/governance_ops" in content
            return name, ("PASS" if ok else "WARN"), "governance_ops dirs in .gitignore" if ok else "governance_ops not in .gitignore"
        except Exception as exc:
            return name, "WARN", str(exc)

    def _check_no_auto_repair(self):
        name = "no_auto_repair"
        try:
            import governance_ops
            ok = getattr(governance_ops, "GOVERNANCE_AUTO_REPAIR_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_AUTO_REPAIR_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_auto_download(self):
        name = "no_auto_download"
        try:
            import governance_ops
            ok = getattr(governance_ops, "GOVERNANCE_AUTO_DOWNLOAD_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_AUTO_DOWNLOAD_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_gate_override(self):
        name = "no_gate_override"
        try:
            import governance_ops
            ok = getattr(governance_ops, "GOVERNANCE_GATE_OVERRIDE_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_GATE_OVERRIDE_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_trade_execution(self):
        name = "no_trade_execution"
        try:
            import governance_ops
            ok = getattr(governance_ops, "GOVERNANCE_TRADE_EXECUTION_ENABLED", True) is False
            return name, ("PASS" if ok else "FAIL"), f"GOVERNANCE_TRADE_EXECUTION_ENABLED={not ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_broker_execution(self):
        name = "no_broker_execution"
        try:
            import governance_ops
            ok = getattr(governance_ops, "BROKER_DISABLED", False) is True
            return name, ("PASS" if ok else "FAIL"), f"BROKER_DISABLED={ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_forbidden_actions(self):
        name = "no_forbidden_actions"
        engine_path = os.path.join(BASE_DIR, "governance_ops", "operations_engine.py")
        if not os.path.isfile(engine_path):
            return name, "WARN", "operations_engine.py not found"
        try:
            with open(engine_path, encoding="utf-8") as f:
                lines = f.readlines()
            forbidden_import_patterns = [
                "import shioaji", "import broker", "from broker",
                "submit_order", "place_order", "buy(", "sell(",
            ]
            found = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                line_lower = stripped.lower()
                for kw in forbidden_import_patterns:
                    if kw in line_lower and kw not in found:
                        found.append(kw)
            if found:
                return name, "FAIL", f"Forbidden keywords found: {found}"
            return name, "PASS", "No forbidden actions in operations engine"
        except Exception as exc:
            return name, "WARN", str(exc)
