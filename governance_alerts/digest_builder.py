"""
governance_alerts.digest_builder — GovernanceDigestBuilder v1.1.7

Builds morning, end-of-day, daily, weekly, and manual governance digests.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No external notification send. No auto repair/import/gate override/trade.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
EXTERNAL_NOTIFICATION_SEND_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _new_uuid() -> str:
    return str(uuid.uuid4())


class GovernanceDigestBuilder:
    """Builds governance digests from alert collections.

    [!] No external send. Produces local preview only.
    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def build_morning_digest(self, alerts: List, governance_summary=None):
        """Morning digest: overnight changes, P0, P1, stale/missing, source interruptions."""
        from governance_alerts.alert_schema import GovernanceDigest
        now = _now_utc()
        today = _today_str()

        p0 = [a for a in alerts if a.priority == "P0"]
        p1 = [a for a in alerts if a.priority == "P1"]
        escalated = [a for a in alerts if a.status == "ESCALATED"]
        stale = sum(1 for a in alerts if a.alert_type == "STALE_SYMBOL_INCREASE")
        missing = sum(1 for a in alerts if a.alert_type == "MISSING_SYMBOL_INCREASE")
        interruptions = sum(1 for a in alerts if a.alert_type == "SOURCE_INTERRUPTION")
        audit_fails = sum(1 for a in alerts if a.alert_type == "AUDIT_CHAIN_FAILURE")

        formal_change = 0
        if governance_summary:
            try:
                gs = governance_summary if isinstance(governance_summary, dict) else governance_summary.to_dict()
                formal_change = int(gs.get("formal_eligible", 0))
            except Exception:
                pass

        overall = self._overall_status(alerts)

        return GovernanceDigest(
            digest_id=_new_uuid(),
            digest_type="MORNING",
            generated_at=now,
            period_start=today + "T00:00:00+00:00",
            period_end=now,
            overall_status=overall,
            p0_count=len(p0),
            p1_count=len(p1),
            new_alerts=len([a for a in alerts if a.status == "OPEN"]),
            escalated_alerts=len(escalated),
            resolved_alerts=len([a for a in alerts if a.status == "RESOLVED"]),
            reopened_alerts=len([a for a in alerts if a.status == "REOPENED"]),
            stale_symbols=stale,
            missing_symbols=missing,
            source_interruptions=interruptions,
            audit_failures=audit_fails,
            formal_eligible_change=formal_change,
            top_actions=self.top_actions(limit=5),
            module_health=self._module_health_summary(alerts),
            safe_next_steps=self.safe_next_steps(alerts),
            research_only=True,
            no_real_orders=True,
        )

    def build_end_of_day_digest(self, alerts: List, governance_summary=None):
        """End-of-day digest: new, resolved, reopened, unresolved P0/P1, carryover."""
        from governance_alerts.alert_schema import GovernanceDigest
        now = _now_utc()
        today = _today_str()

        overall = self._overall_status(alerts)

        return GovernanceDigest(
            digest_id=_new_uuid(),
            digest_type="END_OF_DAY",
            generated_at=now,
            period_start=today + "T00:00:00+00:00",
            period_end=now,
            overall_status=overall,
            p0_count=sum(1 for a in alerts if a.priority == "P0" and a.status not in ("RESOLVED", "SUPPRESSED")),
            p1_count=sum(1 for a in alerts if a.priority == "P1" and a.status not in ("RESOLVED", "SUPPRESSED")),
            new_alerts=len([a for a in alerts if a.status == "OPEN"]),
            escalated_alerts=len([a for a in alerts if a.status == "ESCALATED"]),
            resolved_alerts=len([a for a in alerts if a.status == "RESOLVED"]),
            reopened_alerts=len([a for a in alerts if a.status == "REOPENED"]),
            stale_symbols=sum(1 for a in alerts if a.alert_type == "STALE_SYMBOL_INCREASE"),
            missing_symbols=sum(1 for a in alerts if a.alert_type == "MISSING_SYMBOL_INCREASE"),
            source_interruptions=sum(1 for a in alerts if a.alert_type == "SOURCE_INTERRUPTION"),
            audit_failures=sum(1 for a in alerts if a.alert_type == "AUDIT_CHAIN_FAILURE"),
            top_actions=self.top_actions(limit=10),
            module_health=self._module_health_summary(alerts),
            safe_next_steps=self.safe_next_steps(alerts),
            research_only=True,
            no_real_orders=True,
        )

    def build_daily_digest(self, alerts: List, governance_summary=None):
        """Combined daily digest."""
        from governance_alerts.alert_schema import GovernanceDigest
        now = _now_utc()
        today = _today_str()
        overall = self._overall_status(alerts)

        return GovernanceDigest(
            digest_id=_new_uuid(),
            digest_type="DAILY",
            generated_at=now,
            period_start=today + "T00:00:00+00:00",
            period_end=now,
            overall_status=overall,
            p0_count=sum(1 for a in alerts if a.priority == "P0"),
            p1_count=sum(1 for a in alerts if a.priority == "P1"),
            new_alerts=len([a for a in alerts if a.status in ("OPEN", "REOPENED")]),
            escalated_alerts=len([a for a in alerts if a.status == "ESCALATED"]),
            resolved_alerts=len([a for a in alerts if a.status == "RESOLVED"]),
            reopened_alerts=len([a for a in alerts if a.status == "REOPENED"]),
            stale_symbols=sum(1 for a in alerts if a.alert_type == "STALE_SYMBOL_INCREASE"),
            missing_symbols=sum(1 for a in alerts if a.alert_type == "MISSING_SYMBOL_INCREASE"),
            source_interruptions=sum(1 for a in alerts if a.alert_type == "SOURCE_INTERRUPTION"),
            audit_failures=sum(1 for a in alerts if a.alert_type == "AUDIT_CHAIN_FAILURE"),
            top_actions=self.top_actions(limit=10),
            module_health=self._module_health_summary(alerts),
            safe_next_steps=self.safe_next_steps(alerts),
            research_only=True,
            no_real_orders=True,
        )

    def build_weekly_digest(self, alerts: List, governance_summary=None):
        """Weekly trend digest."""
        from governance_alerts.alert_schema import GovernanceDigest
        now = _now_utc()
        today = _today_str()
        week_start = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
        overall = self._overall_status(alerts)

        return GovernanceDigest(
            digest_id=_new_uuid(),
            digest_type="WEEKLY",
            generated_at=now,
            period_start=week_start + "T00:00:00+00:00",
            period_end=now,
            overall_status=overall,
            p0_count=sum(1 for a in alerts if a.priority == "P0"),
            p1_count=sum(1 for a in alerts if a.priority == "P1"),
            new_alerts=len(alerts),
            escalated_alerts=len([a for a in alerts if a.status == "ESCALATED"]),
            resolved_alerts=len([a for a in alerts if a.status == "RESOLVED"]),
            reopened_alerts=len([a for a in alerts if a.status == "REOPENED"]),
            stale_symbols=sum(1 for a in alerts if a.alert_type == "STALE_SYMBOL_INCREASE"),
            missing_symbols=sum(1 for a in alerts if a.alert_type == "MISSING_SYMBOL_INCREASE"),
            source_interruptions=sum(1 for a in alerts if a.alert_type == "SOURCE_INTERRUPTION"),
            audit_failures=sum(1 for a in alerts if a.alert_type == "AUDIT_CHAIN_FAILURE"),
            top_actions=self.top_actions(limit=10),
            module_health=self._module_health_summary(alerts),
            safe_next_steps=self.safe_next_steps(alerts),
            research_only=True,
            no_real_orders=True,
        )

    def build_manual_digest(self, alerts: List, governance_summary=None):
        """Manually triggered digest."""
        from governance_alerts.alert_schema import GovernanceDigest
        now = _now_utc()
        today = _today_str()
        overall = self._overall_status(alerts)

        return GovernanceDigest(
            digest_id=_new_uuid(),
            digest_type="MANUAL",
            generated_at=now,
            period_start=today + "T00:00:00+00:00",
            period_end=now,
            overall_status=overall,
            p0_count=sum(1 for a in alerts if a.priority == "P0"),
            p1_count=sum(1 for a in alerts if a.priority == "P1"),
            new_alerts=len([a for a in alerts if a.status == "OPEN"]),
            escalated_alerts=len([a for a in alerts if a.status == "ESCALATED"]),
            resolved_alerts=len([a for a in alerts if a.status == "RESOLVED"]),
            reopened_alerts=len([a for a in alerts if a.status == "REOPENED"]),
            stale_symbols=sum(1 for a in alerts if a.alert_type == "STALE_SYMBOL_INCREASE"),
            missing_symbols=sum(1 for a in alerts if a.alert_type == "MISSING_SYMBOL_INCREASE"),
            source_interruptions=sum(1 for a in alerts if a.alert_type == "SOURCE_INTERRUPTION"),
            audit_failures=sum(1 for a in alerts if a.alert_type == "AUDIT_CHAIN_FAILURE"),
            top_actions=self.top_actions(limit=10),
            module_health=self._module_health_summary(alerts),
            safe_next_steps=self.safe_next_steps(alerts),
            research_only=True,
            no_real_orders=True,
        )

    def compare_with_previous(self, current, previous) -> dict:
        """Compare current digest with a previous one."""
        if previous is None:
            return {"no_previous": True}
        return {
            "p0_change": current.p0_count - previous.p0_count,
            "p1_change": current.p1_count - previous.p1_count,
            "escalated_change": current.escalated_alerts - previous.escalated_alerts,
            "stale_change": current.stale_symbols - previous.stale_symbols,
            "missing_change": current.missing_symbols - previous.missing_symbols,
            "audit_change": current.audit_failures - previous.audit_failures,
        }

    def top_alerts(self, alerts: List, limit: int = 10) -> List:
        """Return top alerts by priority/severity."""
        priority_rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        sorted_alerts = sorted(
            [a for a in alerts if a.status not in ("RESOLVED", "SUPPRESSED")],
            key=lambda a: (
                priority_rank.get(a.priority, 9),
                severity_rank.get(a.severity, 9),
                -(a.occurrence_count or 1),
            )
        )
        return sorted_alerts[:limit]

    def top_actions(self, limit: int = 10) -> List[str]:
        """Return top suggested actions (safe commands only)."""
        return [
            "governance-alerts --priority P0",
            "governance-alerts-health",
            "governance-health",
            "freshness-summary",
            "quality-gate-summary",
            "gate-enforcement-verify",
            "governance-alert-audit-verify",
            "governance-checklist",
        ][:limit]

    def safe_next_steps(self, alerts: List) -> List[str]:
        """Return safe next steps based on alert state."""
        steps = []
        if any(a.priority == "P0" for a in alerts if a.status not in ("RESOLVED", "SUPPRESSED")):
            steps.append("REVIEW: Run governance-alerts --priority P0 to review critical alerts")
        if any(a.alert_type == "AUDIT_CHAIN_FAILURE" for a in alerts):
            steps.append("VERIFY_AUDIT: Run gate-enforcement-verify to check audit chain")
        if any(a.alert_type == "FRESHNESS_SLA_BREACH" for a in alerts):
            steps.append("REVIEW: Run freshness-summary to check data freshness")
        if any(a.alert_type == "SOURCE_INTERRUPTION" for a in alerts):
            steps.append("PROVIDE_SOURCE_DATA: Source interruption detected — provide updated data")
        if not steps:
            steps.append("KEEP_OBSERVING: No critical alerts — continue routine monitoring")
        steps.append("READ_REPORT: Run governance-alerts-report for full details")
        return steps

    def _overall_status(self, alerts: List) -> str:
        open_alerts = [a for a in alerts if a.status not in ("RESOLVED", "SUPPRESSED")]
        if any(a.priority == "P0" for a in open_alerts):
            return "CRITICAL"
        if any(a.priority == "P1" for a in open_alerts):
            return "ATTENTION_REQUIRED"
        if any(a.priority == "P2" for a in open_alerts):
            return "DEGRADED"
        if open_alerts:
            return "MONITORING"
        return "HEALTHY"

    def _module_health_summary(self, alerts: List) -> dict:
        module_alerts = [a for a in alerts if a.module and a.alert_type in ("MODULE_HEALTH_FAIL", "MODULE_HEALTH_DEGRADED")]
        result = {}
        for a in module_alerts:
            if a.module not in result or a.severity > result[a.module]:
                result[a.module] = a.severity
        return result

    def render_markdown(self, digest) -> str:
        """Render a digest as markdown text."""
        lines = [
            f"## Governance Digest — {digest.digest_type} ({digest.generated_at[:10]})",
            f"",
            f"**Overall Status:** {digest.overall_status}",
            f"**P0 Alerts:** {digest.p0_count} | **P1 Alerts:** {digest.p1_count}",
            f"**New:** {digest.new_alerts} | **Escalated:** {digest.escalated_alerts} | **Resolved:** {digest.resolved_alerts} | **Reopened:** {digest.reopened_alerts}",
            f"**Stale Symbols:** {digest.stale_symbols} | **Missing:** {digest.missing_symbols}",
            f"**Source Interruptions:** {digest.source_interruptions} | **Audit Failures:** {digest.audit_failures}",
            f"",
            f"### Safe Next Steps",
        ]
        for step in (digest.safe_next_steps or []):
            lines.append(f"- {step}")
        lines.append(f"")
        lines.append(f"> [!] Research Only. No Real Orders. Not Investment Advice.")
        return "\n".join(lines)

    def render_text(self, digest) -> str:
        """Render a digest as plain text."""
        lines = [
            f"Governance Digest [{digest.digest_type}] — {digest.generated_at[:10]}",
            f"Status: {digest.overall_status}",
            f"P0: {digest.p0_count} | P1: {digest.p1_count} | New: {digest.new_alerts} | Escalated: {digest.escalated_alerts}",
            f"Resolved: {digest.resolved_alerts} | Reopened: {digest.reopened_alerts}",
            f"Stale: {digest.stale_symbols} | Missing: {digest.missing_symbols} | Interruptions: {digest.source_interruptions}",
            f"[!] Research Only. No Real Orders.",
        ]
        return "\n".join(lines)
