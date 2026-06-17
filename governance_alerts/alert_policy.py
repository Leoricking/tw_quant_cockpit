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
    "research-registry-health",
    "research-registry-summary",
    "research-runs",
    "research-run",
    "research-run-artifacts",
    "research-run-lineage",
    "research-run-verify",
    "research-run-duplicates",
    "research-run-duplicate-check",
    "research-run-compare",
    "research-run-search",
    "research-run-latest-successful",
    "research-run-latest-formal",
    "research-run-missing-artifacts",
    "research-registry-backfill",
    "research-registry-report",
    "research-registry-audit",
    "research-registry-audit-verify",
    # v1.2.0 Replay Training UX Foundation
    "replay-health",
    "replay-sessions",
    "replay-session",
    "replay-current",
    "replay-summary",
    "replay-report",
    "replay-firewall-check",
    "replay-point-in-time-check",
    # v1.1.9 Data Governance Stable Rollup
    "governance-rollup-health",
    "governance-rollup-run",
    "governance-rollup-summary",
    "governance-rollup-modules",
    "governance-rollup-consistency",
    "governance-rollup-store-inventory",
    "governance-rollup-store-validate",
    "governance-rollup-paths",
    "governance-rollup-indexes",
    "governance-rollup-audits",
    "governance-rollup-recovery-plans",
    "governance-rollup-migration-plans",
    "governance-rollup-health-matrix",
    "governance-rollup-cli-audit",
    "governance-rollup-gui-audit",
    "governance-rollup-docs-audit",
    "governance-rollup-report",
    "governance-rollup-history",
    "governance-rollup-compare",
    "governance-store-recovery-preview",
    "governance-index-rebuild --dry-run",
    "governance-metadata-migrate --dry-run",
    # v1.2.2 Decision Journal commands
    "replay-journal-health",
    "replay-journal-list",
    "replay-journal-entry",
    "replay-journal-search",
    "replay-journal-filter",
    "replay-journal-revisions",
    "replay-journal-compare",
    "replay-journal-summary",
    "replay-journal-session-summary",
    "replay-journal-report",
    "replay-journal-summary-report",
    "replay-journal-checklist",
    "replay-journal-export",
    "replay-journal-import --dry-run",
    "replay-journal-templates",
    # v1.2.3 Replay Scoring & Mistake Taxonomy commands
    "replay-scoring-health",
    "replay-score-session",
    "replay-score-summary",
    "replay-score-report",
    "replay-mistakes-list",
    "replay-mistake-report",
    # v1.2.4 Strategy Knowledge Replay commands
    "replay-strategy-health",
    "replay-strategy-snapshot",
    "replay-strategy-list",
    "replay-strategy-timeline",
    "replay-strategy-agreement",
    "replay-strategy-conflicts",
    "replay-strategy-reviews",
    "replay-strategy-pending-reviews",
    "replay-strategy-summary",
    "replay-strategy-report",
    "replay-strategy-timeline-report",
    "replay-strategy-summary-report",
    "replay-strategy-compare",
    "replay-strategy-search",
    "replay-strategy-batch-preview",
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
    # v1.1.8 Research Run Registry alert types
    "RESEARCH_RUN_FAILED_FORMAL": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["research-registry-health", "research-run-missing-artifacts"],
        "permanent_suppress_allowed": False,
    },
    "RESEARCH_RUN_FAILED_OBSERVATIONAL": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["research-registry-summary", "research-run-missing-artifacts"],
        "permanent_suppress_allowed": True,
    },
    "RESEARCH_RUN_BLOCKED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["research-run-verify", "research-registry-health"],
        "permanent_suppress_allowed": False,
    },
    "RESEARCH_RUN_DUPLICATE": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["research-run-duplicates", "research-run-duplicate-check"],
        "permanent_suppress_allowed": True,
    },
    "RESEARCH_ARTIFACT_MISSING_FORMAL": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["research-run-missing-artifacts", "research-registry-health"],
        "permanent_suppress_allowed": False,
    },
    "RESEARCH_ARTIFACT_MISSING_OPTIONAL": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW"],
        "suggested_commands": ["research-run-missing-artifacts"],
        "permanent_suppress_allowed": True,
    },
    "RESEARCH_HASH_MISMATCH": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "READ_REPORT"],
        "suggested_commands": ["research-run-verify", "research-registry-audit-verify"],
        "permanent_suppress_allowed": False,
    },
    "RESEARCH_REGISTRY_CORRUPTED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "READ_REPORT"],
        "suggested_commands": ["research-registry-audit-verify", "research-registry-health"],
        "permanent_suppress_allowed": False,
    },
    # v1.1.9 Data Governance Stable Rollup alert types
    "ROLLUP_CONSISTENCY_FAILURE": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-rollup-consistency", "governance-rollup-health"],
        "permanent_suppress_allowed": False,
    },
    "ROLLUP_STORE_CORRUPTED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "READ_REPORT"],
        "suggested_commands": ["governance-rollup-store-validate", "governance-rollup-audits"],
        "permanent_suppress_allowed": False,
    },
    "ROLLUP_STORE_VALIDATION_FAILURE": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-rollup-store-validate", "governance-rollup-store-inventory"],
        "permanent_suppress_allowed": False,
    },
    "ROLLUP_PATH_MISMATCH": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-rollup-paths", "governance-rollup-consistency"],
        "permanent_suppress_allowed": True,
    },
    "ROLLUP_INDEX_STALE": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-rollup-indexes", "governance-index-rebuild", "--dry-run"],
        "permanent_suppress_allowed": True,
    },
    "ROLLUP_HEALTH_DEGRADED": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-rollup-health", "governance-rollup-health-matrix"],
        "permanent_suppress_allowed": True,
    },
    "ROLLUP_MIGRATION_NEEDED": {
        "severity": "LOW", "priority": "P3",
        "suppression_window": 7200,
        "snooze_limit": 86400 * 14,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["governance-rollup-migration-plans", "governance-metadata-migrate", "--dry-run"],
        "permanent_suppress_allowed": True,
    },
    # v1.2.0 Replay Training alert types
    "REPLAY_FUTURE_DATA_LEAK_DETECTED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-firewall-check", "replay-point-in-time-check", "replay-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_SESSION_BLOCKED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["replay-health", "replay-sessions", "replay-session"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_DATA_UNAVAILABLE": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 3,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["replay-current", "replay-health"],
        "permanent_suppress_allowed": True,
    },
    "REPLAY_STORE_CORRUPTED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-health", "replay-sessions"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_POINT_IN_TIME_WARNING": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400 * 7,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["replay-point-in-time-check", "replay-firewall-check"],
        "permanent_suppress_allowed": True,
    },
    # v1.2.1 Replay Scenario & Session Manager alert types
    "REPLAY_SCENARIO_ARCHIVED_INSTANTIATION_BLOCKED": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["replay-scenario-restore", "replay-scenario-show", "replay-scenario-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_SCENARIO_VALIDATION_FAILED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 0,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-scenario-validate", "replay-scenario-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_SCENARIO_STORE_CORRUPTED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-scenario-health", "replay-scenarios"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_CHECKPOINT_FUTURE_FIELD_BLOCKED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-scenario-health", "replay-session-checkpoints"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_SESSION_LINEAGE_CYCLE_DETECTED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 0,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-session-lineage", "replay-scenario-health"],
        "permanent_suppress_allowed": False,
    },
    # v1.2.2 Decision Journal alert types
    "REPLAY_JOURNAL_POINT_IN_TIME_FAILED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-journal-health", "replay-point-in-time-check"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_JOURNAL_FUTURE_FIELD_DETECTED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-journal-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_JOURNAL_SECRET_DETECTED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-journal-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_JOURNAL_ORPHANED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["replay-journal-health", "replay-journal-list"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_JOURNAL_INVALID_REVISION": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-journal-health", "replay-journal-revisions"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_JOURNAL_REQUIRED_CHECKLIST_MISSING": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW", "READ_REPORT"],
        "suggested_commands": ["replay-journal-checklist", "replay-journal-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_JOURNAL_IMPORT_BLOCKED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-journal-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_JOURNAL_STORE_CORRUPTED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-journal-health"],
        "permanent_suppress_allowed": False,
    },
    # v1.2.3 Replay Scoring & Mistake Taxonomy alert types
    "REPLAY_SCORING_FUTURE_DATA_DETECTED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-scoring-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_MISTAKE_AUTO_CONFIRMED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-scoring-health", "replay-mistakes-list"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_SCORE_WEIGHTS_SUM_INVALID": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 3600,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW"],
        "suggested_commands": ["replay-scoring-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_SCORING_STORE_CORRUPTED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-scoring-health"],
        "permanent_suppress_allowed": False,
    },
    # v1.2.4 Strategy Knowledge Replay alert types
    "REPLAY_STRATEGY_FUTURE_FIELD_DETECTED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_STRATEGY_AUTO_DECISION_ENABLED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_STRATEGY_AUTO_EXECUTION_ENABLED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_STRATEGY_CONFLICT_AUTO_BLOCKED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health", "replay-strategy-conflicts"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_STRATEGY_RULE_REVIEW_AUTO_CONFIRMED": {
        "severity": "CRITICAL", "priority": "P0",
        "suppression_window": 0,
        "snooze_limit": None,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health", "replay-strategy-reviews"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_STRATEGY_SNAPSHOT_MISSING_PIT": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_STRATEGY_STORE_CORRUPTED": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health"],
        "permanent_suppress_allowed": False,
    },
    "REPLAY_STRATEGY_BATCH_BLOCKED": {
        "severity": "MEDIUM", "priority": "P2",
        "suppression_window": 3600,
        "snooze_limit": 86400,
        "safe_actions": ["REVIEW"],
        "suggested_commands": ["replay-strategy-batch-preview"],
        "permanent_suppress_allowed": True,
    },
    "REPLAY_STRATEGY_UNAVAILABLE_COUNTED_BEARISH": {
        "severity": "HIGH", "priority": "P1",
        "suppression_window": 1800,
        "snooze_limit": 86400,
        "safe_actions": ["VERIFY_AUDIT", "REVIEW"],
        "suggested_commands": ["replay-strategy-health"],
        "permanent_suppress_allowed": False,
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
