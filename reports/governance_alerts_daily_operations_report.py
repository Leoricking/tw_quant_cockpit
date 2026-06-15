"""
reports/governance_alerts_daily_operations_report.py — GovernanceAlertsDailyOperationsReportBuilder v1.1.7

Generates governance_alerts_daily_operations_report_YYYY-MM-DD.md

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Alerts do NOT repair, import, override gates, or enable trading.
[!] External notifications DISABLED. Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class GovernanceAlertsDailyOperationsReportBuilder:
    """Builds the Governance Alerts & Daily Operations report.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    no_real_orders = True
    research_only = True

    def build(self, tier: str = "research30", mode: str = "real", output_dir: str = "reports") -> str:
        """Generate the report and return the output path."""
        today = _today_str()
        generated_at = _now_utc()

        # Load data defensively
        alerts = []
        digest = None
        checklist = None
        escalation_summary = {}
        governance_summary = {}

        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            store = GovernanceAlertStore()
            alerts = store.list_all_alerts()
        except Exception as exc:
            logger.warning("Report: failed to load alerts: %s", exc)

        try:
            from governance_alerts.digest_builder import GovernanceDigestBuilder
            builder = GovernanceDigestBuilder()
            digest = builder.build_daily_digest(alerts)
        except Exception as exc:
            logger.warning("Report: failed to build digest: %s", exc)

        try:
            from governance_alerts.daily_checklist import GovernanceDailyChecklistBuilder
            cl_builder = GovernanceDailyChecklistBuilder()
            checklist = cl_builder.build()
        except Exception as exc:
            logger.warning("Report: failed to build checklist: %s", exc)

        try:
            from governance_alerts.escalation_engine import GovernanceAlertEscalationEngine
            eng = GovernanceAlertEscalationEngine()
            escalation_summary = eng.build_escalation_summary(alerts)
        except Exception as exc:
            logger.warning("Report: failed to build escalation summary: %s", exc)

        try:
            from governance_ops.operations_query import OperationsQuery
            q = OperationsQuery()
            s = q.latest_summary()
            if s:
                governance_summary = s.to_dict()
        except Exception as exc:
            logger.warning("Report: failed to load governance summary: %s", exc)

        # Build report markdown
        lines = self._build_report(
            today=today,
            generated_at=generated_at,
            tier=tier,
            mode=mode,
            alerts=alerts,
            digest=digest,
            checklist=checklist,
            escalation_summary=escalation_summary,
            governance_summary=governance_summary,
        )

        # Write to file
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(output_dir, exist_ok=True)
        filename = f"governance_alerts_daily_operations_report_{today}.md"
        filepath = os.path.join(output_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            logger.info("GovernanceAlertsDailyOperationsReportBuilder: wrote %s", filepath)
        except Exception as exc:
            logger.error("Report write failed: %s", exc)
            return ""

        return filepath

    def _build_report(
        self,
        today: str,
        generated_at: str,
        tier: str,
        mode: str,
        alerts: List,
        digest,
        checklist,
        escalation_summary: dict,
        governance_summary: dict,
    ) -> List[str]:
        open_alerts = [a for a in alerts if a.status not in ("RESOLVED", "SUPPRESSED")]
        acked = [a for a in alerts if a.status == "ACKNOWLEDGED"]
        snoozed = [a for a in alerts if a.status == "SNOOZED"]
        escalated = [a for a in alerts if a.status == "ESCALATED"]
        resolved = [a for a in alerts if a.status == "RESOLVED"]
        reopened = [a for a in alerts if a.status == "REOPENED"]
        suppressed = [a for a in alerts if a.status == "SUPPRESSED"]
        p0 = [a for a in open_alerts if a.priority == "P0"]
        p1 = [a for a in open_alerts if a.priority == "P1"]
        p2 = [a for a in open_alerts if a.priority == "P2"]
        p3 = [a for a in open_alerts if a.priority == "P3"]

        overall_status = "HEALTHY"
        if p0:
            overall_status = "CRITICAL"
        elif p1:
            overall_status = "ATTENTION_REQUIRED"
        elif p2:
            overall_status = "DEGRADED"
        elif open_alerts:
            overall_status = "MONITORING"

        # Checklist info
        cl_total = cl_completed = cl_pending = 0
        cl_rate = 0.0
        if checklist:
            cl_total = len(checklist.items)
            cl_completed = sum(1 for i in checklist.items if i.status == "COMPLETE")
            cl_pending = sum(1 for i in checklist.items if i.status == "PENDING")
            cl_rate = checklist.completion_rate * 100

        lines = [
            f"# Governance Alerts & Daily Operations Report v1.1.7",
            f"",
            f"---",
            f"",
            f"## 1. Executive Summary",
            f"",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Version | 1.1.7 |",
            f"| Release | Governance Alerts & Daily Operations |",
            f"| Research Only | True |",
            f"| No Real Orders | True |",
            f"| Mode | {mode} |",
            f"| Tier | {tier} |",
            f"| Overall Status | **{overall_status}** |",
            f"| Digest Type | DAILY |",
            f"| Generated At | {generated_at} |",
            f"| Report Date | {today} |",
            f"",
            f"---",
            f"",
            f"## 2. Alert Overview",
            f"",
            f"| Status | Count |",
            f"|--------|-------|",
            f"| Open | {len(open_alerts)} |",
            f"| Acknowledged | {len(acked)} |",
            f"| Snoozed | {len(snoozed)} |",
            f"| Escalated | {len(escalated)} |",
            f"| Resolved | {len(resolved)} |",
            f"| Reopened | {len(reopened)} |",
            f"| Suppressed | {len(suppressed)} |",
            f"| **Total** | **{len(alerts)}** |",
            f"",
            f"---",
            f"",
            f"## 3. Priority Alerts",
            f"",
        ]

        # P0/P1/P2/P3 tables
        for priority_group, label in [(p0, "P0 — Critical"), (p1, "P1 — High"), (p2, "P2 — Medium"), (p3, "P3 — Low/Info")]:
            lines.append(f"### {label} ({len(priority_group)} alerts)")
            if priority_group:
                lines.append(f"")
                lines.append(f"| Type | Symbol/Source | Title | Status | First Detected | Occurrences | Escalation | Safe Action |")
                lines.append(f"|------|--------------|-------|--------|----------------|-------------|------------|-------------|")
                for a in priority_group[:10]:
                    sym = a.symbol or a.source or "(system)"
                    title = a.title[:50]
                    lines.append(f"| {a.alert_type} | {sym} | {title} | {a.status} | {(a.first_detected_at or '')[:10]} | {a.occurrence_count} | {a.escalation_level} | {', '.join(a.safe_actions[:2]) if a.safe_actions else 'REVIEW'} |")
                if len(priority_group) > 10:
                    lines.append(f"| ... | ... | *{len(priority_group) - 10} more* | | | | | |")
            else:
                lines.append(f"_No {label} alerts._")
            lines.append(f"")

        lines.extend([
            f"---",
            f"",
            f"## 4. State Changes",
            f"",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| New Alerts | {len([a for a in alerts if a.occurrence_count == 1])} |",
            f"| Resolved Today | {len(resolved)} |",
            f"| Reopened | {len(reopened)} |",
            f"| Escalated | {len(escalated)} |",
            f"",
            f"---",
            f"",
            f"## 5. Freshness & Sources",
            f"",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| SLA Breaches | {sum(1 for a in open_alerts if a.alert_type == 'FRESHNESS_SLA_BREACH')} |",
            f"| Stale Symbol Alerts | {sum(1 for a in open_alerts if a.alert_type == 'STALE_SYMBOL_INCREASE')} |",
            f"| Missing Symbol Alerts | {sum(1 for a in open_alerts if a.alert_type == 'MISSING_SYMBOL_INCREASE')} |",
            f"| Source Interruptions | {sum(1 for a in open_alerts if a.alert_type == 'SOURCE_INTERRUPTION')} |",
            f"| Source Degraded | {sum(1 for a in open_alerts if a.alert_type == 'SOURCE_DEGRADED')} |",
            f"",
            f"---",
            f"",
            f"## 6. Data Integrity",
            f"",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Import Conflicts | {sum(1 for a in open_alerts if a.alert_type == 'IMPORT_CONFLICT')} |",
            f"| Invalid OHLC | {sum(1 for a in open_alerts if a.alert_type == 'INVALID_OHLC')} |",
            f"| Future Date | {sum(1 for a in open_alerts if a.alert_type == 'FUTURE_DATE')} |",
            f"| Date Regression | {sum(1 for a in open_alerts if a.alert_type == 'DATE_REGRESSION')} |",
            f"| Import Failures | {sum(1 for a in open_alerts if a.alert_type == 'IMPORT_FAILURE')} |",
            f"",
            f"---",
            f"",
            f"## 7. Quality & Audit",
            f"",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Formal Eligibility Drop | {sum(1 for a in open_alerts if a.alert_type == 'FORMAL_ELIGIBILITY_DROP')} |",
            f"| Blocked Symbol Increase | {sum(1 for a in open_alerts if a.alert_type == 'BLOCKED_SYMBOL_INCREASE')} |",
            f"| Non-qualified Runs | {sum(1 for a in open_alerts if a.alert_type == 'NON_QUALIFIED_RUN')} |",
            f"| Override Used | {sum(1 for a in open_alerts if a.alert_type == 'OVERRIDE_USED')} |",
            f"| Audit Chain Failures | {sum(1 for a in open_alerts if a.alert_type == 'AUDIT_CHAIN_FAILURE')} |",
            f"| Reproducibility Failures | {sum(1 for a in open_alerts if a.alert_type == 'REPRODUCIBILITY_FAILURE')} |",
            f"",
            f"---",
            f"",
            f"## 8. Daily Checklist",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Items | {cl_total} |",
            f"| Required | {sum(1 for i in checklist.items if i.required) if checklist else 0} |",
            f"| Completed | {cl_completed} |",
            f"| Pending | {cl_pending} |",
            f"| Completion Rate | {cl_rate:.0f}% |",
            f"",
        ])

        if checklist and checklist.items:
            lines.append(f"| Category | Item | Required | Status | Safe Action |")
            lines.append(f"|----------|------|----------|--------|-------------|")
            for item in checklist.items[:15]:
                lines.append(f"| {item.category} | {item.title[:50]} | {'Yes' if item.required else 'No'} | {item.status} | {item.safe_action} |")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 9. Escalations",
            f"",
            f"| Level | Count |",
            f"|-------|-------|",
            f"| L1 | {escalation_summary.get('l1_count', 0)} |",
            f"| L2 | {escalation_summary.get('l2_count', 0)} |",
            f"| L3 | {escalation_summary.get('l3_count', 0)} |",
            f"| Total Escalated | {escalation_summary.get('total_escalated', len(escalated))} |",
            f"",
            f"---",
            f"",
            f"## 10. Safe Next Steps",
            f"",
            f"Allowed actions (read-only research use only):",
            f"",
            f"- REVIEW: Run `governance-alerts --priority P0` to review critical alerts",
            f"- VERIFY_AUDIT: Run `gate-enforcement-verify` to check audit chain",
            f"- READ_REPORT: Review this report and governance-digest for full details",
            f"- PROVIDE_SOURCE_DATA: Supply updated data files if source interruption detected",
            f"- REFRESH_COVERAGE: Run `coverage-repair-plan` (dry-run only)",
            f"- RETRY_IMPORT: Run `import-validate` before any import attempt",
            f"- KEEP_OBSERVING: Monitor trend with `governance-alert-trend --days 7`",
            f"- WAIT: Allow time for data providers to update",
            f"",
            f"---",
            f"",
            f"## 11. Notification Preview",
            f"",
            f"> **[!] LOCAL PREVIEW ONLY — External Notification Send: DISABLED**",
            f">",
            f"> No LINE, Telegram, Slack, email, webhook, or any external notification is sent.",
            f"> These previews are for local review only.",
            f"",
        ])

        if digest:
            lines.extend([
                f"### Morning Digest Preview",
                f"",
                f"```",
                f"Status: {digest.overall_status}",
                f"P0: {digest.p0_count} | P1: {digest.p1_count} | Escalated: {digest.escalated_alerts}",
                f"Source Interruptions: {digest.source_interruptions} | Audit Failures: {digest.audit_failures}",
                f"[!] Research Only. No Real Orders.",
                f"```",
                f"",
                f"### End-of-Day Digest Preview",
                f"",
                f"```",
                f"Resolved Today: {digest.resolved_alerts} | Reopened: {digest.reopened_alerts}",
                f"New Alerts: {digest.new_alerts} | Carryover P0: {digest.p0_count}",
                f"[!] Research Only. No Real Orders.",
                f"```",
                f"",
            ])

        lines.extend([
            f"---",
            f"",
            f"## 12. 安全聲明 (Safety Declaration)",
            f"",
            f"| Safety Flag | Value |",
            f"|-------------|-------|",
            f"| No Real Orders | **True** |",
            f"| Broker Execution Disabled | **True** |",
            f"| Alerts do NOT repair/import/override/enable trading | **True** |",
            f"| External Notifications Disabled | **True** |",
            f"| Not Investment Advice | **True** |",
            f"| Production Trading Blocked | **True** |",
            f"| GOVERNANCE_AUTO_REPAIR_ENABLED | **False** |",
            f"| GOVERNANCE_AUTO_DOWNLOAD_ENABLED | **False** |",
            f"| GOVERNANCE_AUTO_IMPORT_ENABLED | **False** |",
            f"| GOVERNANCE_GATE_OVERRIDE_ENABLED | **False** |",
            f"| GOVERNANCE_TRADE_EXECUTION_ENABLED | **False** |",
            f"| EXTERNAL_NOTIFICATION_SEND_ENABLED | **False** |",
            f"",
            f"---",
            f"",
            f"*Generated by TW Quant Cockpit v1.1.7 — Governance Alerts & Daily Operations*",
            f"",
            f"*[!] Research Only. No Real Orders. Production Trading: BLOCKED.*",
            f"*[!] Governance Alerts do NOT repair, import, override gates, or enable trading.*",
            f"*[!] External notifications DISABLED. Not Investment Advice.*",
            f"*[!] This report is for research purposes only.*",
        ])

        return lines
