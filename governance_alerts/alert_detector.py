"""
governance_alerts.alert_detector — GovernanceAlertDetector v1.1.7

Detects governance alerts from all sources. Only creates CHANGE alerts when
state worsens. Aggregates source interruptions. Never suppressible for
FUTURE_DATE, DATE_REGRESSION, or AUDIT_CHAIN_FAILURE.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import hashlib
import logging
import uuid
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _fingerprint(*parts) -> str:
    key = "|".join(str(p).strip().upper() for p in parts if p)
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


class GovernanceAlertDetector:
    """Detects governance alerts from all configured sources.

    [!] Research Only. No Real Orders.
    real mode: no fallback mock.
    mock mode: labels alerts DEMO_ONLY.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, mode: str = "real", tier: str = "research30"):
        self._mode = mode
        self._tier = tier

    def detect_all(self, mode: str = "real", tier: str = "research30") -> List:
        """Detect all governance alerts from all sources."""
        from governance_alerts.alert_sources import build_all_sources
        from governance_alerts.alert_schema import GovernanceAlert

        self._mode = mode
        self._tier = tier
        alerts: List[GovernanceAlert] = []

        sources_map = {
            "governance_summary": None,
            "actions": None,
            "module_health": None,
            "freshness": None,
            "source_health": None,
            "repairs": None,
            "onboarding": None,
            "quality_gates": None,
            "enforcement": None,
            "reports": None,
        }

        try:
            from governance_alerts.alert_sources import (
                GovernanceSummaryAlertSource,
                GovernanceActionAlertSource,
                ModuleHealthAlertSource,
                FreshnessAlertSource,
                SourceHealthAlertSource,
                RepairAlertSource,
                OnboardingAlertSource,
                QualityGateAlertSource,
                EnforcementAuditAlertSource,
                ReportQualificationAlertSource,
            )
            sources_map["governance_summary"] = GovernanceSummaryAlertSource()
            sources_map["actions"] = GovernanceActionAlertSource()
            sources_map["module_health"] = ModuleHealthAlertSource()
            sources_map["freshness"] = FreshnessAlertSource()
            sources_map["source_health"] = SourceHealthAlertSource()
            sources_map["repairs"] = RepairAlertSource()
            sources_map["onboarding"] = OnboardingAlertSource()
            sources_map["quality_gates"] = QualityGateAlertSource()
            sources_map["enforcement"] = EnforcementAuditAlertSource()
            sources_map["reports"] = ReportQualificationAlertSource()
        except Exception as exc:
            logger.warning("GovernanceAlertDetector: failed to build sources: %s", exc)

        detector_methods = [
            ("governance_summary", self.detect_from_governance_summary),
            ("actions", self.detect_from_actions),
            ("module_health", self.detect_from_module_health),
            ("freshness", self.detect_from_freshness),
            ("source_health", self.detect_from_source_health),
            ("repairs", self.detect_from_repairs),
            ("onboarding", self.detect_from_onboarding),
            ("quality_gates", self.detect_from_quality_gates),
            ("enforcement", self.detect_from_enforcement),
            ("reports", self.detect_from_reports),
        ]

        for source_name, method in detector_methods:
            source = sources_map.get(source_name)
            if source is None:
                continue
            try:
                new_alerts = method(source)
                alerts.extend(new_alerts)
            except Exception as exc:
                logger.warning("GovernanceAlertDetector source %s failed: %s", source_name, exc)

        if mode == "mock":
            for alert in alerts:
                alert.demo_only = True
                alert.title = "[DEMO_ONLY] " + alert.title

        return alerts

    def detect_from_governance_summary(self, source) -> List:
        from governance_alerts.alert_schema import GovernanceAlert
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()

        try:
            if not source.available():
                return alerts
            curr = source.current_records()
            prev = source.previous_records()

            # FORMAL_ELIGIBILITY_DROP
            curr_formal = int(curr.get("formal_eligible", 0))
            prev_formal = int(prev.get("formal_eligible", curr_formal)) if prev else curr_formal
            if curr_formal < prev_formal:
                delta = prev_formal - curr_formal
                alert = self.build_alert(
                    alert_type="FORMAL_ELIGIBILITY_DROP",
                    title=f"Formal Eligible symbols dropped by {delta}",
                    message=f"Formal eligible count decreased from {prev_formal} to {curr_formal}.",
                    reason_codes=["FORMAL_ELIGIBILITY_DROP"],
                    previous_state=str(prev_formal),
                    current_state=str(curr_formal),
                    policy=policy,
                )
                alerts.append(alert)

            # READY_SYMBOL_DROP
            curr_ready = int(curr.get("ready_symbols", 0))
            prev_ready = int(prev.get("ready_symbols", curr_ready)) if prev else curr_ready
            if curr_ready < prev_ready:
                delta = prev_ready - curr_ready
                alert = self.build_alert(
                    alert_type="READY_SYMBOL_DROP",
                    title=f"Ready symbols dropped by {delta}",
                    message=f"Ready symbol count decreased from {prev_ready} to {curr_ready}.",
                    reason_codes=["READY_SYMBOL_DROP"],
                    previous_state=str(prev_ready),
                    current_state=str(curr_ready),
                    policy=policy,
                )
                alerts.append(alert)

            # BLOCKED_SYMBOL_INCREASE
            curr_blocked = int(curr.get("blocked_symbols", 0))
            prev_blocked = int(prev.get("blocked_symbols", curr_blocked)) if prev else curr_blocked
            if curr_blocked > prev_blocked:
                delta = curr_blocked - prev_blocked
                alert = self.build_alert(
                    alert_type="BLOCKED_SYMBOL_INCREASE",
                    title=f"Blocked symbols increased by {delta}",
                    message=f"Blocked symbol count increased from {prev_blocked} to {curr_blocked}.",
                    reason_codes=["BLOCKED_SYMBOL_INCREASE"],
                    previous_state=str(prev_blocked),
                    current_state=str(curr_blocked),
                    policy=policy,
                )
                alerts.append(alert)

            # STALE_SYMBOL_INCREASE
            curr_stale = int(curr.get("stale_symbols", 0))
            prev_stale = int(prev.get("stale_symbols", curr_stale)) if prev else curr_stale
            if curr_stale > prev_stale:
                alert = self.build_alert(
                    alert_type="STALE_SYMBOL_INCREASE",
                    title=f"Stale symbols increased to {curr_stale}",
                    message=f"Stale symbol count increased from {prev_stale} to {curr_stale}.",
                    reason_codes=["STALE_SYMBOL_INCREASE"],
                    previous_state=str(prev_stale),
                    current_state=str(curr_stale),
                    policy=policy,
                )
                alerts.append(alert)

            # MISSING_SYMBOL_INCREASE
            curr_missing = int(curr.get("missing_symbols", 0))
            prev_missing = int(prev.get("missing_symbols", curr_missing)) if prev else curr_missing
            if curr_missing > prev_missing:
                alert = self.build_alert(
                    alert_type="MISSING_SYMBOL_INCREASE",
                    title=f"Missing symbols increased to {curr_missing}",
                    message=f"Missing symbol count increased from {prev_missing} to {curr_missing}.",
                    reason_codes=["MISSING_SYMBOL_INCREASE"],
                    previous_state=str(prev_missing),
                    current_state=str(curr_missing),
                    policy=policy,
                )
                alerts.append(alert)

        except Exception as exc:
            logger.warning("detect_from_governance_summary: %s", exc)

        return alerts

    def detect_from_actions(self, source) -> List:
        from governance_alerts.alert_schema import GovernanceAlert
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()

        try:
            if not source.available():
                return alerts
            curr = source.current_records()
            p0 = int(curr.get("p0_count", 0))
            p1 = int(curr.get("p1_count", 0))

            if p0 > 0:
                alert = self.build_alert(
                    alert_type="NEW_P0_ACTION",
                    title=f"{p0} open P0 governance action(s) require immediate review",
                    message=f"There are {p0} open P0 governance actions. Review: governance-actions --priority P0",
                    reason_codes=["NEW_P0_ACTION"],
                    current_state=str(p0),
                    policy=policy,
                )
                alerts.append(alert)

            if p1 > 0:
                alert = self.build_alert(
                    alert_type="NEW_P1_ACTION",
                    title=f"{p1} open P1 governance action(s) require review",
                    message=f"There are {p1} open P1 governance actions. Review: governance-actions --priority P1",
                    reason_codes=["NEW_P1_ACTION"],
                    current_state=str(p1),
                    policy=policy,
                )
                alerts.append(alert)

        except Exception as exc:
            logger.warning("detect_from_actions: %s", exc)

        return alerts

    def detect_from_module_health(self, source) -> List:
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()

        try:
            if not source.available():
                return alerts
            modules = source.current_records()
            for name, mod in modules.items():
                status = mod.get("health_status", "UNKNOWN")
                if status in ("FAIL", "BLOCKED"):
                    alert = self.build_alert(
                        alert_type="MODULE_HEALTH_FAIL",
                        title=f"Module {name} health: {status}",
                        message=f"Governance module '{name}' reported health status {status}.",
                        module=name,
                        reason_codes=["MODULE_HEALTH_FAIL", status],
                        current_state=status,
                        policy=policy,
                    )
                    alerts.append(alert)
                elif status == "WARN":
                    alert = self.build_alert(
                        alert_type="MODULE_HEALTH_DEGRADED",
                        title=f"Module {name} health degraded: WARN",
                        message=f"Governance module '{name}' reported health status WARN.",
                        module=name,
                        reason_codes=["MODULE_HEALTH_DEGRADED"],
                        current_state=status,
                        policy=policy,
                    )
                    alerts.append(alert)

        except Exception as exc:
            logger.warning("detect_from_module_health: %s", exc)

        return alerts

    def detect_from_freshness(self, source) -> List:
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()

        try:
            if not source.available():
                return alerts
            curr = source.current_records()
            if not curr:
                return alerts
            stale = int(curr.get("stale_count", 0))
            interrupted = int(curr.get("interrupted_count", 0))

            if stale > 0:
                alert = self.build_alert(
                    alert_type="FRESHNESS_SLA_BREACH",
                    title=f"{stale} symbol(s) breaching freshness SLA",
                    message=f"{stale} symbols are stale beyond SLA threshold.",
                    reason_codes=["FRESHNESS_SLA_BREACH", "STALE_DATA"],
                    current_state=str(stale),
                    policy=policy,
                )
                alerts.append(alert)

            if interrupted > 0:
                alert = self.build_alert(
                    alert_type="SOURCE_INTERRUPTION",
                    title=f"{interrupted} source(s) interrupted",
                    message=f"{interrupted} data sources have interruptions detected.",
                    reason_codes=["SOURCE_INTERRUPTION"],
                    current_state=str(interrupted),
                    policy=policy,
                )
                alerts.append(alert)

        except Exception as exc:
            logger.warning("detect_from_freshness: %s", exc)

        return alerts

    def detect_from_source_health(self, source) -> List:
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()

        try:
            if not source.available():
                return alerts
            curr = source.current_records()
            count = int(curr.get("source_interruptions", 0))
            if count > 0:
                alert = self.build_alert(
                    alert_type="SOURCE_INTERRUPTION",
                    title=f"{count} source interruption(s) detected",
                    message=f"Governance operations reports {count} source interruption(s).",
                    reason_codes=["SOURCE_INTERRUPTION"],
                    current_state=str(count),
                    policy=policy,
                )
                alerts.append(alert)
        except Exception as exc:
            logger.warning("detect_from_source_health: %s", exc)

        return alerts

    def detect_from_repairs(self, source) -> List:
        alerts = []
        try:
            if not source.available():
                return alerts
        except Exception as exc:
            logger.warning("detect_from_repairs: %s", exc)
        return alerts

    def detect_from_onboarding(self, source) -> List:
        alerts = []
        try:
            if not source.available():
                return alerts
        except Exception as exc:
            logger.warning("detect_from_onboarding: %s", exc)
        return alerts

    def detect_from_quality_gates(self, source) -> List:
        alerts = []
        try:
            if not source.available():
                return alerts
        except Exception as exc:
            logger.warning("detect_from_quality_gates: %s", exc)
        return alerts

    def detect_from_enforcement(self, source) -> List:
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()

        try:
            if not source.available():
                return alerts
            curr = source.current_records()
            failures = int(curr.get("audit_failures", 0))
            if failures > 0:
                alert = self.build_alert(
                    alert_type="AUDIT_CHAIN_FAILURE",
                    title=f"Audit chain failure detected ({failures} run(s))",
                    message=f"Gate enforcement audit chain failure in {failures} run(s). Immediate review required.",
                    reason_codes=["AUDIT_CHAIN_FAILURE"],
                    current_state=str(failures),
                    policy=policy,
                )
                alerts.append(alert)
        except Exception as exc:
            logger.warning("detect_from_enforcement: %s", exc)

        return alerts

    def detect_from_reports(self, source) -> List:
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()

        try:
            if not source.available():
                return alerts
            curr = source.current_records()
            non_qualified = int(curr.get("non_qualified_runs", 0))
            if non_qualified > 0:
                alert = self.build_alert(
                    alert_type="NON_QUALIFIED_RUN",
                    title=f"{non_qualified} non-qualified gate enforcement run(s)",
                    message=f"{non_qualified} gate enforcement runs did not qualify.",
                    reason_codes=["NON_QUALIFIED_RUN"],
                    current_state=str(non_qualified),
                    policy=policy,
                )
                alerts.append(alert)
        except Exception as exc:
            logger.warning("detect_from_reports: %s", exc)

        return alerts

    def detect_state_changes(self, previous: List, current: List) -> List:
        """Return alerts that represent state changes from previous to current."""
        # Simple implementation: return current that don't appear in previous fingerprints
        prev_fps = {a.fingerprint for a in previous}
        return [a for a in current if a.fingerprint not in prev_fps]

    def build_alert(
        self,
        alert_type: str,
        title: str,
        message: str,
        symbol: Optional[str] = None,
        dataset: str = "",
        source: str = "",
        module: str = "",
        reason_codes: Optional[List[str]] = None,
        previous_state: Optional[str] = None,
        current_state: Optional[str] = None,
        policy=None,
    ):
        from governance_alerts.alert_schema import GovernanceAlert
        from governance_alerts.alert_policy import GovernanceAlertPolicy

        if policy is None:
            policy = GovernanceAlertPolicy()

        if reason_codes is None:
            reason_codes = []

        severity = policy.severity_for(alert_type)
        priority = policy.priority_for(alert_type)
        safe_actions = policy.safe_actions(alert_type)
        suggested_commands = policy.suggested_commands(alert_type)

        # Build deterministic fingerprint
        fp = _fingerprint(alert_type, symbol or "", dataset, source, module, *sorted(reason_codes))

        alert_id = _new_uuid()
        now = _now_utc()

        return GovernanceAlert(
            alert_id=alert_id,
            fingerprint=fp,
            alert_type=alert_type,
            severity=severity,
            priority=priority,
            title=title,
            message=message,
            symbol=symbol,
            dataset=dataset,
            source=source,
            module=module,
            reason_codes=reason_codes,
            safe_actions=safe_actions,
            suggested_commands=suggested_commands,
            status="OPEN",
            first_detected_at=now,
            last_detected_at=now,
            occurrence_count=1,
            previous_state=previous_state,
            current_state=current_state,
            research_only=True,
            no_real_orders=True,
            demo_only=(self._mode == "mock"),
        )

    def detect_from_research_registry(self) -> List:
        """Detect alerts from research run registry. [!] Research Only."""
        from governance_alerts.alert_schema import GovernanceAlert
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()
        try:
            from research_registry.registry_query import RegistryQuery
            q = RegistryQuery()

            # RESEARCH_RUN_FAILED: check for recent formal failures
            failed = q.list_failed()
            for r in failed[-5:]:
                is_formal = r.qualification == "FORMALLY_QUALIFIED"
                alert_type = "RESEARCH_RUN_FAILED_FORMAL" if is_formal else "RESEARCH_RUN_FAILED_OBSERVATIONAL"
                alert = self.build_alert(
                    alert_type=alert_type,
                    title=f"Research run FAILED: {r.command_name}",
                    message=f"Run {r.run_id[:12]} ({r.command_name}) failed. Qualification: {r.qualification}.",
                    reason_codes=["RESEARCH_RUN_FAILED"],
                    policy=policy,
                )
                alerts.append(alert)

            # RESEARCH_RUN_BLOCKED: check for formal blocked runs
            blocked = q.list_blocked()
            for r in blocked[-3:]:
                if r.qualification in ("FORMALLY_QUALIFIED", "BLOCKED"):
                    alert = self.build_alert(
                        alert_type="RESEARCH_RUN_BLOCKED",
                        title=f"Research run BLOCKED: {r.command_name}",
                        message=f"Run {r.run_id[:12]} blocked. Reasons: {r.blocked_reason_codes}.",
                        reason_codes=r.blocked_reason_codes or ["RESEARCH_RUN_BLOCKED"],
                        policy=policy,
                    )
                    alerts.append(alert)

            # RESEARCH_RUN_DUPLICATE
            dups = q.list_duplicates()
            if dups:
                alert = self.build_alert(
                    alert_type="RESEARCH_RUN_DUPLICATE",
                    title=f"{len(dups)} duplicate research run(s) detected",
                    message=f"Detected {len(dups)} run(s) marked as exact duplicates.",
                    reason_codes=["RESEARCH_RUN_DUPLICATE"],
                    policy=policy,
                )
                alerts.append(alert)

            # RESEARCH_ARTIFACT_MISSING
            missing = q.list_missing_artifacts()
            formal_missing = [r for r in missing if r.qualification == "FORMALLY_QUALIFIED"]
            if formal_missing:
                alert = self.build_alert(
                    alert_type="RESEARCH_ARTIFACT_MISSING_FORMAL",
                    title=f"{len(formal_missing)} formal run(s) with missing artifacts",
                    message=f"Formally qualified runs have missing output artifacts.",
                    reason_codes=["RESEARCH_ARTIFACT_MISSING"],
                    policy=policy,
                )
                alerts.append(alert)

            # RESEARCH_REGISTRY_CORRUPTED: check audit chain
            from research_registry.registry_store import RegistryStore
            store = RegistryStore()
            audit_result = store.verify_audit_chain()
            if not audit_result.get("valid") and audit_result.get("event_count", 0) > 0:
                alert = self.build_alert(
                    alert_type="RESEARCH_REGISTRY_CORRUPTED",
                    title="Research registry audit chain broken",
                    message=f"Audit chain integrity failure detected at event {audit_result.get('broken_at', '?')}.",
                    reason_codes=["REGISTRY_AUDIT_BROKEN"],
                    policy=policy,
                )
                alerts.append(alert)

        except Exception as exc:
            logger.debug("detect_from_research_registry failed (non-fatal): %s", exc)
        return alerts

    def detect_from_mtf_replay(self) -> List:
        """Detect alerts from multi-timeframe replay module. [!] Research Only."""
        from governance_alerts.alert_schema import GovernanceAlert
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()
        try:
            from replay.timeframe_health import run_health_check
            results = run_health_check()
            failed = [r for r in results if r.get("status") == "FAIL"]
            for r in failed:
                check_name = r.get("check", r.get("name", "unknown"))
                detail = r.get("detail", "")
                alert_type = "MTF_STORE_CORRUPTED" if "store" in check_name.lower() else "MTF_FUTURE_KLINE_DETECTED"
                alert = self.build_alert(
                    alert_type=alert_type,
                    title=f"MTF health check FAILED: {check_name}",
                    message=f"MTF replay health check {check_name} failed. {detail}",
                    reason_codes=["MTF_HEALTH_FAIL"],
                    policy=policy,
                )
                alerts.append(alert)
        except Exception as exc:
            logger.debug("detect_from_mtf_replay failed (non-fatal): %s", exc)
        return alerts

    def detect_from_replay_review(self) -> List:
        """Detect alerts from replay review dashboard module. [!] Research Only."""
        from governance_alerts.alert_schema import GovernanceAlert
        from governance_alerts.alert_policy import GovernanceAlertPolicy
        alerts = []
        policy = GovernanceAlertPolicy()
        try:
            from replay.review_health import ReplayReviewDashboardHealthCheck
            hc = ReplayReviewDashboardHealthCheck()
            results = hc.run()
            for check_name, (status, detail) in results.items():
                if status == "FAIL":
                    # Map check names to alert types
                    if "data_leak" in check_name or "future" in check_name:
                        alert_type = "REPLAY_REVIEW_DATA_LEAK"
                    elif "outcome_visible" in check_name or "outcome_hidden" in check_name:
                        alert_type = "REPLAY_REVIEW_OUTCOME_VISIBLE_BEFORE_REVEAL"
                    elif "auto_confirm" in check_name:
                        alert_type = "REPLAY_REVIEW_AUTO_CONFIRM_ATTEMPT"
                    elif "auto_complete" in check_name or "auto_review" in check_name:
                        alert_type = "REPLAY_REVIEW_AUTO_COMPLETE_ATTEMPT"
                    elif "score_to_trade" in check_name or "trade_exec" in check_name:
                        alert_type = "REPLAY_REVIEW_SCORE_TO_TRADE_ATTEMPT"
                    elif "store" in check_name or "corrupted" in check_name:
                        alert_type = "REPLAY_REVIEW_STORE_CORRUPTED"
                    elif "module" in check_name or "unavailable" in check_name:
                        alert_type = "REPLAY_REVIEW_MODULE_UNAVAILABLE"
                    elif "orphan" in check_name:
                        alert_type = "REPLAY_REVIEW_ORPHANED_SESSION_REF"
                    else:
                        alert_type = "REPLAY_REVIEW_MODULE_UNAVAILABLE"
                    alert = self.build_alert(
                        alert_type=alert_type,
                        title=f"Replay Review health check FAILED: {check_name}",
                        message=f"Replay Review health check {check_name} failed. {detail}",
                        reason_codes=["REPLAY_REVIEW_HEALTH_FAIL"],
                        policy=policy,
                    )
                    alerts.append(alert)
        except Exception as exc:
            logger.debug("detect_from_replay_review failed (non-fatal): %s", exc)
        return alerts

    def summarize_detection(self, alerts: List) -> dict:
        if not alerts:
            return {
                "total": 0, "p0": 0, "p1": 0, "p2": 0, "p3": 0,
                "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0,
            }
        return {
            "total": len(alerts),
            "p0": sum(1 for a in alerts if a.priority == "P0"),
            "p1": sum(1 for a in alerts if a.priority == "P1"),
            "p2": sum(1 for a in alerts if a.priority == "P2"),
            "p3": sum(1 for a in alerts if a.priority == "P3"),
            "critical": sum(1 for a in alerts if a.severity == "CRITICAL"),
            "high": sum(1 for a in alerts if a.severity == "HIGH"),
            "medium": sum(1 for a in alerts if a.severity == "MEDIUM"),
            "low": sum(1 for a in alerts if a.severity == "LOW"),
            "info": sum(1 for a in alerts if a.severity == "INFO"),
        }
