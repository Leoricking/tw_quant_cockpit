"""
governance_alerts.alert_sources — Alert data sources for Governance Alerts v1.1.7

Each source imports defensively, is read-only, and returns empty + logs warning
on missing/corrupt store. No mock fallback in real mode.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class _BaseAlertSource:
    """Base class for all governance alert sources."""
    no_real_orders = True
    research_only = True

    def available(self) -> bool:
        return False

    def current_records(self) -> dict:
        return {}

    def previous_records(self) -> dict:
        return {}

    def detect_changes(self) -> List[dict]:
        return []

    def limitations(self) -> List[str]:
        return []

    def last_updated(self) -> Optional[str]:
        return None


class GovernanceSummaryAlertSource(_BaseAlertSource):
    """Alert source from governance operations summary."""

    def available(self) -> bool:
        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            s = q.latest_summary()
            return s is not None
        except Exception as exc:
            logger.warning("GovernanceSummaryAlertSource: %s", exc)
            return False

    def current_records(self) -> dict:
        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            s = q.latest_summary()
            if s:
                return s.to_dict()
            return {}
        except Exception as exc:
            logger.warning("GovernanceSummaryAlertSource.current_records: %s", exc)
            return {}

    def previous_records(self) -> dict:
        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            history = q.summary_history(limit=2)
            if len(history) >= 2:
                return history[-1].to_dict()
            return {}
        except Exception as exc:
            logger.warning("GovernanceSummaryAlertSource.previous_records: %s", exc)
            return {}

    def detect_changes(self) -> List[dict]:
        curr = self.current_records()
        prev = self.previous_records()
        if not curr:
            return []
        changes = []
        try:
            for key in ["formal_eligible", "ready_symbols", "blocked_symbols", "stale_symbols", "missing_symbols"]:
                cv = int(curr.get(key, 0))
                pv = int(prev.get(key, 0)) if prev else cv
                if cv != pv:
                    changes.append({"field": key, "previous": pv, "current": cv, "delta": cv - pv})
        except Exception as exc:
            logger.warning("GovernanceSummaryAlertSource.detect_changes: %s", exc)
        return changes

    def limitations(self) -> List[str]:
        return ["requires governance-dashboard to have run", "stale if not refreshed today"]

    def last_updated(self) -> Optional[str]:
        curr = self.current_records()
        return curr.get("generated_at") or None


class GovernanceActionAlertSource(_BaseAlertSource):
    """Alert source from governance action queue."""

    def available(self) -> bool:
        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            return q.latest_summary() is not None
        except Exception as exc:
            logger.warning("GovernanceActionAlertSource.available: %s", exc)
            return False

    def current_records(self) -> dict:
        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            actions = q.action_queue()
            return {
                "p0_count": sum(1 for a in actions if a.priority == "P0"),
                "p1_count": sum(1 for a in actions if a.priority == "P1"),
                "open_count": sum(1 for a in actions if a.status == "OPEN"),
                "actions": [a.to_dict() for a in actions[:50]],
            }
        except Exception as exc:
            logger.warning("GovernanceActionAlertSource.current_records: %s", exc)
            return {}

    def detect_changes(self) -> List[dict]:
        curr = self.current_records()
        if not curr:
            return []
        changes = []
        if curr.get("p0_count", 0) > 0:
            changes.append({"field": "p0_actions", "current": curr["p0_count"]})
        if curr.get("p1_count", 0) > 0:
            changes.append({"field": "p1_actions", "current": curr["p1_count"]})
        return changes


class ModuleHealthAlertSource(_BaseAlertSource):
    """Alert source from governance module health."""

    def available(self) -> bool:
        try:
            from governance_ops.operations_engine import DataGovernanceOperationsEngine
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from governance_ops.operations_engine import DataGovernanceOperationsEngine
            engine = DataGovernanceOperationsEngine()
            modules = engine.build_module_health()
            return {k: v.to_dict() for k, v in modules.items()}
        except Exception as exc:
            logger.warning("ModuleHealthAlertSource.current_records: %s", exc)
            return {}

    def detect_changes(self) -> List[dict]:
        curr = self.current_records()
        if not curr:
            return []
        changes = []
        for name, mod in curr.items():
            status = mod.get("health_status", "UNKNOWN")
            if status in ("FAIL", "BLOCKED"):
                changes.append({"module": name, "status": status})
            elif status == "WARN":
                changes.append({"module": name, "status": status})
        return changes


class FreshnessAlertSource(_BaseAlertSource):
    """Alert source from data freshness monitor."""

    def available(self) -> bool:
        try:
            import data_freshness
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from data_freshness.freshness_query import FreshnessQuery
            q = FreshnessQuery()
            summary = q.latest_summary()
            if summary:
                return summary.to_dict() if hasattr(summary, "to_dict") else dict(summary)
            return {}
        except Exception as exc:
            logger.warning("FreshnessAlertSource.current_records: %s", exc)
            return {}

    def detect_changes(self) -> List[dict]:
        curr = self.current_records()
        if not curr:
            return []
        changes = []
        stale = int(curr.get("stale_count", 0))
        missing = int(curr.get("missing_count", 0))
        interrupted = int(curr.get("interrupted_count", 0))
        if stale > 0:
            changes.append({"field": "stale_count", "current": stale})
        if missing > 0:
            changes.append({"field": "missing_count", "current": missing})
        if interrupted > 0:
            changes.append({"field": "interrupted_count", "current": interrupted})
        return changes

    def limitations(self) -> List[str]:
        return ["requires data_freshness module", "data_freshness may not be present"]


class SourceHealthAlertSource(_BaseAlertSource):
    """Alert source from source/provider health."""

    def available(self) -> bool:
        try:
            from governance_ops.operations_query import OperationsQuery
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            summary = q.latest_summary()
            if summary:
                return {"source_interruptions": summary.source_interruptions}
            return {}
        except Exception as exc:
            logger.warning("SourceHealthAlertSource.current_records: %s", exc)
            return {}

    def detect_changes(self) -> List[dict]:
        curr = self.current_records()
        if not curr:
            return []
        count = int(curr.get("source_interruptions", 0))
        if count > 0:
            return [{"field": "source_interruptions", "current": count}]
        return []


class RepairAlertSource(_BaseAlertSource):
    """Alert source from coverage repair module."""

    def available(self) -> bool:
        try:
            import coverage_repair
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from coverage_repair.repair_query import RepairQuery
            q = RepairQuery()
            summary = q.latest_summary()
            if summary:
                return summary.to_dict() if hasattr(summary, "to_dict") else {}
            return {}
        except Exception as exc:
            logger.warning("RepairAlertSource.current_records: %s", exc)
            return {}

    def limitations(self) -> List[str]:
        return ["requires coverage_repair module"]


class OnboardingAlertSource(_BaseAlertSource):
    """Alert source from import/onboarding module."""

    def available(self) -> bool:
        try:
            import import_onboarding
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from import_onboarding.onboarding_query import OnboardingQuery
            q = OnboardingQuery()
            summary = q.latest_summary()
            if summary:
                return summary.to_dict() if hasattr(summary, "to_dict") else {}
            return {}
        except Exception as exc:
            logger.warning("OnboardingAlertSource.current_records: %s", exc)
            return {}

    def limitations(self) -> List[str]:
        return ["requires import_onboarding module"]


class QualityGateAlertSource(_BaseAlertSource):
    """Alert source from coverage quality gates."""

    def available(self) -> bool:
        try:
            from coverage_quality_gates.gate_query import GateQuery
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from coverage_quality_gates.gate_query import GateQuery
            q = GateQuery()
            summary = q.latest_summary()
            if summary:
                return summary.to_dict() if hasattr(summary, "to_dict") else {}
            return {}
        except Exception as exc:
            logger.warning("QualityGateAlertSource.current_records: %s", exc)
            return {}

    def limitations(self) -> List[str]:
        return ["requires coverage_quality_gates module"]


class EnforcementAuditAlertSource(_BaseAlertSource):
    """Alert source from gate enforcement audit."""

    def available(self) -> bool:
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            q = EnforcementQuery()
            runs = q.list_runs(limit=5)
            audit_failures = sum(1 for r in runs if not r.get("audit_chain_valid", True))
            return {"audit_failures": audit_failures, "total_runs": len(runs)}
        except Exception as exc:
            logger.warning("EnforcementAuditAlertSource.current_records: %s", exc)
            return {}

    def detect_changes(self) -> List[dict]:
        curr = self.current_records()
        if not curr:
            return []
        failures = int(curr.get("audit_failures", 0))
        if failures > 0:
            return [{"field": "audit_chain_failures", "current": failures}]
        return []


class ReportQualificationAlertSource(_BaseAlertSource):
    """Alert source from report qualification/gate enforcement runs."""

    def available(self) -> bool:
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            return True
        except Exception:
            return False

    def current_records(self) -> dict:
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            q = EnforcementQuery()
            runs = q.list_runs(limit=10)
            non_qualified = sum(1 for r in runs if r.get("qualification", "QUALIFIED") != "QUALIFIED")
            return {"non_qualified_runs": non_qualified}
        except Exception as exc:
            logger.warning("ReportQualificationAlertSource.current_records: %s", exc)
            return {}

    def limitations(self) -> List[str]:
        return ["requires gate_enforcement module"]


def build_all_sources() -> List[_BaseAlertSource]:
    """Return all configured alert sources."""
    return [
        GovernanceSummaryAlertSource(),
        GovernanceActionAlertSource(),
        ModuleHealthAlertSource(),
        FreshnessAlertSource(),
        SourceHealthAlertSource(),
        RepairAlertSource(),
        OnboardingAlertSource(),
        QualityGateAlertSource(),
        EnforcementAuditAlertSource(),
        ReportQualificationAlertSource(),
    ]
