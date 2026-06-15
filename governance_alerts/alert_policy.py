"""
governance_alerts.alert_policy — GovernanceAlertPolicy v1.1.7

Defines severity, priority, suppression windows, escalation rules,
safe actions, and allowed suggested commands for each alert type.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Suggested commands allowlist only. Broker/order/trading commands FORBIDDEN.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# ---------------------------------------------------------------------------
# Allowlist for suggested commands — ONLY these are permitted
# ---------------------------------------------------------------------------
ALLOWED_COMMAND_PREFIXES = [
    "governance-summary",
    "governance-actions",
    "governance-health",
    "governance-dashboard",
    "governance-module-health",
    "governance-symbols",
    "governance-audit-summary",
    "freshness-summary",
    "freshness-stale",
    "freshness-health",
    "coverage-repair-plan",
    "coverage-repair-run --dry-run",
    "import-preview",
    "import-validate",
    "import-batch --dry-run",
    "quality-gate-summary",
    "quality-gate-health",
    "gate-enforcement-verify",
    "gate-enforcement-health",
    "gate-enforcement-audit",
    "safety-scan",
    "governance-alerts-health",
    "governance-alerts-scan",
    "governance-alerts",
    "governance-alert-history",
    "governance-alert-escalations",
    "governance-digest",
    "governance-checklist",
    "governance-alert-trend",
    "governance-alert-compare",
    "governance-daily-operations",
    "governance-alerts-report",
    "governance-alert-audit",
    "governance-alert-audit-verify",
    "research-cockpit-stable",
    "stable-v060-check",
]

# ---------------------------------------------------------------------------
# Forbidden command fragments — never allowed in suggested commands
# ---------------------------------------------------------------------------
FORBIDDEN_COMMAND_FRAGMENTS = [
    "broker", "order", "shioaji", "real_trade", "live_trade",
    "auto_trade", "execute_order", "submit_order",
    "repair-run --allow", "repair execute",
    "import-batch --allow-write", "import-batch --allow-replace",
    "import execute",
    "gate override",
    "兆豐", "買", "賣",
]

# ---------------------------------------------------------------------------
# Policy table
# ---------------------------------------------------------------------------
_POLICIES: Dict[str, dict] = {
    "AUDIT_CHAIN_FAILURE": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,  # never suppress
        "snooze_limit": None,      # no snooze for CRITICAL
        "safe_actions": ["VERIFY_AUDIT", "READ_REPORT"],
        "suggested_commands": ["gate-enforcement-verify", "gate-enforcement-audit", "governance-alerts-health"],
        "permanent_suppress_allowed": False,
    },
    "FUTURE_DATE": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["FIX_DATA", "REVIEW"],
        "suggested_commands": ["coverage-repair-plan", "governance-summary"],
        "permanent_suppress_allowed": False,
    },
    "DATE_REGRESSION": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["FIX_DATA", "REVIEW"],
        "suggested_commands": ["coverage-repair-plan", "governance-summary"],
        "permanent_suppress_allowed": False,
    },
    "REPRODUCIBILITY_FAILURE": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "READ_REPORT"],
        "suggested_commands": ["gate-enforcement-verify", "governance-alerts-health"],
        "permanent_suppress_allowed": False,
    },
    "SOURCE_INTERRUPTION": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 1800,  # 30 min
        "snooze_limit": 86400,       # max 24h snooze
        "safe_actions": ["PROVIDE_SOURCE_DATA", "REVIEW"],
        "suggested_commands": ["freshness-summary", "freshness-stale", "governance-summary"],
        "permanent_suppress_allowed": False,
    },
    "IMPORT_CONFLICT": {
        "severity": "HIGH", "priority": "P0",
        "suppression_window": 3600,
        "snooze_limit": 86400,
        "safe_actions": ["FIX_DATA", "REVIEW"],
        "suggested_commands": ["import-preview", "import-validate", "coverage-repair-plan"],
        "permanent_suppress_allowed": False,
    },
    "INVALID_OHLC": {
        "severity": "HIGH", "priority": "P0",
        "suppression_window": 3600,
        "snooze_limit": 86400,
        "safe_actions": ["FIX_DATA", "REVIEW"],
        "suggested_commands": ["coverage-repair-plan", "import-validate"],
        "permanent_suppress_allowed": False,
    },
    "NEW_P0_ACTION": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-actions", "governance-dashboard"],
        "permanent_suppress_allowed": False,
    },
    "FORMAL_ELIGIBILITY_DROP": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["quality-gate-summary", "governance-symbols"],
        "permanent_suppress_allowed": False,
    },
    "READY_SYMBOL_DROP": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-symbols", "quality-gate-summary"],
        "permanent_suppress_allowed": False,
    },
    "MODULE_HEALTH_FAIL": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-health", "governance-module-health"],
        "permanent_suppress_allowed": False,
    },
    "IMPORT_FAILURE": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["RETRY_IMPORT", "REVIEW"],
        "suggested_commands": ["import-preview", "import-validate"],
        "permanent_suppress_allowed": False,
    },
    "FRESHNESS_SLA_BREACH": {
        "severity": "MEDIUM", "priority": "P1",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["REVIEW", "PROVIDE_SOURCE_DATA"],
        "suggested_commands": ["freshness-summary", "freshness-stale"],
        "permanent_suppress_allowed": False,
    },
    "NEW_P1_ACTION": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-actions", "governance-summary"],
        "permanent_suppress_allowed": True,
    },
    "SOURCE_DEGRADED": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["REVIEW", "PROVIDE_SOURCE_DATA"],
        "suggested_commands": ["freshness-health", "governance-summary"],
        "permanent_suppress_allowed": True,
    },
    "STALE_SYMBOL_INCREASE": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["REVIEW", "PROVIDE_SOURCE_DATA"],
        "suggested_commands": ["freshness-stale", "coverage-repair-plan"],
        "permanent_suppress_allowed": True,
    },
    "MISSING_SYMBOL_INCREASE": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["PROVIDE_SOURCE_DATA", "REVIEW"],
        "suggested_commands": ["freshness-stale", "coverage-repair-plan"],
        "permanent_suppress_allowed": True,
    },
    "BLOCKED_SYMBOL_INCREASE": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "FIX_DATA"],
        "suggested_commands": ["quality-gate-summary", "governance-symbols"],
        "permanent_suppress_allowed": True,
    },
    "NON_QUALIFIED_RUN": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["gate-enforcement-health", "governance-summary"],
        "permanent_suppress_allowed": True,
    },
    "REPORT_QUALIFICATION_WARNING": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-alerts-report", "governance-digest"],
        "permanent_suppress_allowed": True,
    },
    "MODULE_HEALTH_DEGRADED": {
        "severity": "LOW", "priority": "P3",
        "suppression_window": 7200,
        "snooze_limit": 86400 * 14,
        "safe_actions": ["REVIEW", "KEEP_OBSERVING"],
        "suggested_commands": ["governance-module-health", "governance-health"],
        "permanent_suppress_allowed": True,
    },
    "OVERRIDE_USED": {
        "severity": "LOW", "priority": "P3",
        "suppression_window": 7200,
        "snooze_limit": 86400 * 14,
        "safe_actions": ["REVIEW", "VERIFY_AUDIT"],
        "suggested_commands": ["gate-enforcement-audit"],
        "permanent_suppress_allowed": True,
    },
    "DAILY_DIGEST_INFO": {
        "severity": "INFO", "priority": "P3",
        "suppression_window": 3600,
        "snooze_limit": 86400,
        "safe_actions": ["READ_REPORT"],
        "suggested_commands": ["governance-digest", "governance-checklist"],
        "permanent_suppress_allowed": True,
    },
    "ACTION_REOPENED": {
        "severity": "LOW", "priority": "P3",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW"],
        "suggested_commands": ["governance-actions"],
        "permanent_suppress_allowed": True,
    },
}

# Default fallback
_DEFAULT_POLICY = {
    "severity": "INFO", "priority": "P3",
    "suppression_window": 3600,
    "snooze_limit": 86400 * 7,
    "safe_actions": ["REVIEW"],
    "suggested_commands": ["governance-summary"],
    "permanent_suppress_allowed": True,
}


class GovernanceAlertPolicy:
    """Policy engine for governance alert severity, priority, and lifecycle rules.

    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def policy_for(self, alert_type: str) -> dict:
        return _POLICIES.get(alert_type, _DEFAULT_POLICY)

    def severity_for(self, alert_type: str, context: Optional[dict] = None) -> str:
        return self.policy_for(alert_type)["severity"]

    def priority_for(self, alert_type: str, context: Optional[dict] = None) -> str:
        return self.policy_for(alert_type)["priority"]

    def should_alert(self, previous: Optional[dict], current: dict) -> bool:
        """Return True if this represents a new or worsened alert state."""
        if previous is None:
            return True
        prev_status = previous.get("status", "RESOLVED")
        curr_severity = current.get("severity", "INFO")
        prev_severity = previous.get("severity", "INFO")
        severity_order = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        if prev_status == "RESOLVED":
            return True
        curr_sev_rank = severity_order.get(curr_severity, 0)
        prev_sev_rank = severity_order.get(prev_severity, 0)
        return curr_sev_rank > prev_sev_rank

    def should_escalate(self, alert) -> bool:
        """Return True if the alert should be escalated."""
        from governance_alerts.escalation_engine import GovernanceAlertEscalationEngine
        eng = GovernanceAlertEscalationEngine()
        return eng.should_escalate(alert)

    def suppression_window(self, alert_type: str) -> int:
        """Return suppression window in seconds."""
        return self.policy_for(alert_type)["suppression_window"]

    def snooze_limit(self, alert_type: str) -> Optional[int]:
        """Return max snooze duration in seconds, or None (unlimited) for non-P0."""
        return self.policy_for(alert_type)["snooze_limit"]

    def safe_actions(self, alert_type: str) -> List[str]:
        return self.policy_for(alert_type)["safe_actions"]

    def suggested_commands(self, alert_type: str) -> List[str]:
        cmds = self.policy_for(alert_type)["suggested_commands"]
        return [c for c in cmds if self._is_allowed_command(c)]

    def permanent_suppress_allowed(self, alert_type: str) -> bool:
        """P0 alerts cannot be permanently suppressed."""
        policy = self.policy_for(alert_type)
        if policy["priority"] == "P0":
            return False
        return policy.get("permanent_suppress_allowed", True)

    def _is_allowed_command(self, cmd: str) -> bool:
        """Validate command against allowlist and denylist."""
        cmd_lower = cmd.lower().strip()
        for fragment in FORBIDDEN_COMMAND_FRAGMENTS:
            if fragment.lower() in cmd_lower:
                logger.warning("Blocked forbidden command fragment '%s' in: %s", fragment, cmd)
                return False
        for prefix in ALLOWED_COMMAND_PREFIXES:
            if cmd_lower.startswith(prefix.lower()) or cmd_lower == prefix.lower():
                return True
        return False

    def validate_suggested_commands(self, commands: List[str]) -> List[str]:
        """Return only allowed commands from a list."""
        return [c for c in commands if self._is_allowed_command(c)]
