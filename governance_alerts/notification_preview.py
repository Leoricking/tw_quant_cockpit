"""
governance_alerts.notification_preview — GovernanceNotificationPreview v1.1.7

Generates local notification previews only. NEVER sends to any external system.

[!] EXTERNAL_NOTIFICATION_SEND_ENABLED = False (permanently)
[!] No LINE, Telegram, Slack, email, webhook, or any external notification.
[!] No broker commands. No trading instructions. No BUY/SELL/ORDER.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
EXTERNAL_NOTIFICATION_SEND_ENABLED = False  # PERMANENTLY FALSE

# Patterns to redact from any preview content
_REDACT_PATTERNS = [
    (re.compile(r'[A-Za-z0-9_\-]{20,}', re.ASCII), "[REDACTED_TOKEN]"),
    (re.compile(r'api[_\-]?key\s*[:=]\s*\S+', re.IGNORECASE), "API_KEY=[REDACTED]"),
    (re.compile(r'token\s*[:=]\s*\S+', re.IGNORECASE), "TOKEN=[REDACTED]"),
    (re.compile(r'password\s*[:=]\s*\S+', re.IGNORECASE), "PASSWORD=[REDACTED]"),
    (re.compile(r'secret\s*[:=]\s*\S+', re.IGNORECASE), "SECRET=[REDACTED]"),
]

_FORBIDDEN_ACTION_VERBS = ["BUY", "SELL", "ORDER", "EXECUTE_ORDER", "SUBMIT_ORDER", "AUTO_TRADE"]


class GovernanceNotificationPreview:
    """Generates local-only notification previews for governance alerts and digests.

    [!] NEVER sends to external systems.
    [!] Research Only. No Real Orders. No trading instructions.
    """

    EXTERNAL_NOTIFICATION_SEND_ENABLED = False

    def preview_alert(self, alert, format: str = "markdown") -> str:
        """Generate a local preview of an alert notification."""
        if format.lower() == "markdown":
            return self._alert_to_markdown(alert)
        elif format.lower() in ("email_preview", "chat_preview"):
            return self._alert_to_text(alert)
        else:
            return self._alert_to_text(alert)

    def preview_digest(self, digest, format: str = "markdown") -> str:
        """Generate a local preview of a digest notification."""
        if format.lower() == "markdown":
            return self._digest_to_markdown(digest)
        else:
            return self._digest_to_text(digest)

    def preview_escalation(self, alert, format: str = "markdown") -> str:
        """Generate a local preview of an escalation notification."""
        lines = [
            f"[ESCALATION PREVIEW — LOCAL ONLY]",
            f"Alert: {alert.title}",
            f"Priority: {alert.priority} | Severity: {alert.severity}",
            f"Escalation Level: {alert.escalation_level}",
            f"Alert ID: {alert.alert_id}",
            f"",
            f"[!] Research Only. No Real Orders.",
            f"[!] This is a LOCAL PREVIEW ONLY. No external notification sent.",
            f"[!] External Notification Send: DISABLED",
        ]
        return "\n".join(lines)

    def redact_sensitive_content(self, text: str) -> str:
        """Redact API keys, tokens, passwords, and other secrets from text."""
        result = text
        # Only redact clearly secret-looking patterns (not all long strings)
        result = re.sub(r'(api[_\-]?key\s*[:=]\s*)\S+', r'\1[REDACTED]', result, flags=re.IGNORECASE)
        result = re.sub(r'(token\s*[:=]\s*)\S+', r'\1[REDACTED]', result, flags=re.IGNORECASE)
        result = re.sub(r'(password\s*[:=]\s*)\S+', r'\1[REDACTED]', result, flags=re.IGNORECASE)
        result = re.sub(r'(secret\s*[:=]\s*)\S+', r'\1[REDACTED]', result, flags=re.IGNORECASE)
        result = re.sub(r'(bearer\s+)\S+', r'\1[REDACTED]', result, flags=re.IGNORECASE)
        return result

    def validate_safe_content(self, text: str) -> bool:
        """Return True if text contains no forbidden action verbs or sensitive patterns."""
        text_upper = text.upper()
        for verb in _FORBIDDEN_ACTION_VERBS:
            if verb in text_upper:
                return False
        if re.search(r'(api[_\-]?key|password|secret|bearer)\s*[:=]\s*\S{8,}', text, re.IGNORECASE):
            return False
        return True

    def _alert_to_markdown(self, alert) -> str:
        lines = [
            f"## [{alert.priority}] {alert.title}",
            f"",
            f"**Alert Type:** {alert.alert_type}",
            f"**Severity:** {alert.severity} | **Priority:** {alert.priority}",
            f"**Status:** {alert.status} | **Occurrences:** {alert.occurrence_count}",
        ]
        if alert.symbol:
            lines.append(f"**Symbol:** {alert.symbol}")
        if alert.source:
            lines.append(f"**Source:** {alert.source}")
        if alert.module:
            lines.append(f"**Module:** {alert.module}")
        lines.extend([
            f"",
            f"**Message:** {alert.message}",
        ])
        if alert.reason_codes:
            lines.append(f"**Reason Codes:** {', '.join(alert.reason_codes)}")
        if alert.safe_actions:
            lines.append(f"**Safe Actions:** {', '.join(alert.safe_actions)}")
        if alert.suggested_commands:
            lines.append(f"**Suggested Commands:**")
            for cmd in alert.suggested_commands:
                lines.append(f"  - `python main.py {cmd}`")
        lines.extend([
            f"",
            f"**First Detected:** {alert.first_detected_at}",
            f"**Escalation Level:** {alert.escalation_level}",
            f"",
            f"> [!] Research Only. No Real Orders. Not Investment Advice.",
            f"> [!] LOCAL PREVIEW ONLY — External Notification Send: DISABLED",
        ])
        return self.redact_sensitive_content("\n".join(lines))

    def _alert_to_text(self, alert) -> str:
        lines = [
            f"[{alert.priority}] {alert.title}",
            f"Type: {alert.alert_type} | Severity: {alert.severity}",
            f"Status: {alert.status} | Occurrences: {alert.occurrence_count}",
            f"Message: {alert.message}",
            f"[!] Research Only. No Real Orders.",
            f"[!] LOCAL PREVIEW ONLY — No external notification sent.",
        ]
        return self.redact_sensitive_content("\n".join(lines))

    def _digest_to_markdown(self, digest) -> str:
        lines = [
            f"## Governance Digest Preview — {digest.digest_type}",
            f"",
            f"**Generated:** {digest.generated_at}",
            f"**Period:** {digest.period_start} → {digest.period_end}",
            f"**Overall Status:** {digest.overall_status}",
            f"",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| P0 Alerts | {digest.p0_count} |",
            f"| P1 Alerts | {digest.p1_count} |",
            f"| New Alerts | {digest.new_alerts} |",
            f"| Escalated | {digest.escalated_alerts} |",
            f"| Resolved | {digest.resolved_alerts} |",
            f"| Reopened | {digest.reopened_alerts} |",
            f"| Stale Symbols | {digest.stale_symbols} |",
            f"| Missing Symbols | {digest.missing_symbols} |",
            f"| Source Interruptions | {digest.source_interruptions} |",
            f"| Audit Failures | {digest.audit_failures} |",
            f"",
            f"### Safe Next Steps",
        ]
        for step in (digest.safe_next_steps or []):
            lines.append(f"- {step}")
        lines.extend([
            f"",
            f"> [!] Research Only. No Real Orders. Not Investment Advice.",
            f"> [!] LOCAL PREVIEW ONLY — External Notification Send: DISABLED",
            f"> [!] This preview does NOT represent actual notification delivery.",
        ])
        return self.redact_sensitive_content("\n".join(lines))

    def _digest_to_text(self, digest) -> str:
        lines = [
            f"Governance Digest [{digest.digest_type}]",
            f"Status: {digest.overall_status}",
            f"P0: {digest.p0_count} | P1: {digest.p1_count} | Escalated: {digest.escalated_alerts}",
            f"[!] Research Only. No Real Orders.",
            f"[!] LOCAL PREVIEW ONLY. No external notification sent.",
        ]
        return "\n".join(lines)
