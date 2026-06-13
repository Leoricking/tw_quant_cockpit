"""
final_rollup/rollup_schema.py — Schema dataclasses for Final Maintenance Rollup v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Final Maintenance Rollup.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Cadence constants
# ---------------------------------------------------------------------------
CADENCE_DAILY    = "DAILY"
CADENCE_WEEKLY   = "WEEKLY"
CADENCE_MONTHLY  = "MONTHLY"
CADENCE_RELEASE  = "RELEASE"
CADENCE_INCIDENT = "INCIDENT"
CADENCE_ADHOC    = "ADHOC"

# ---------------------------------------------------------------------------
# Safe action constants (forbidden: BUY, SELL, ORDER, EXECUTE, etc.)
# ---------------------------------------------------------------------------
SAFE_REVIEW          = "REVIEW"
SAFE_READ_REPORT     = "READ_REPORT"
SAFE_FIX_DATA        = "FIX_DATA"
SAFE_BACKTEST_MORE   = "BACKTEST_MORE"
SAFE_KEEP_OBSERVING  = "KEEP_OBSERVING"
SAFE_WAIT            = "WAIT"

# Allowed outputs (must match the allowed output list from spec)
ALLOWED_OUTPUTS = [
    "REVIEW", "FIX_DATA", "READ_REPORT", "KEEP_OBSERVING",
    "MARK_RESEARCH_ONLY", "PAPER_ONLY", "MOCK_ONLY", "WAIT",
    "BACKTEST_MORE", "PRACTICE_REPLAY", "REVIEW_JOURNAL",
    "REVIEW_RISK", "REVIEW_EARNINGS", "REVIEW_CHIPS", "DO_NOT_CHASE",
]

# Forbidden outputs
FORBIDDEN_OUTPUTS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]


@dataclass
class ReleaseEntry:
    """Metadata for a single release in the v1.0.x history.

    [!] Research Only. No Real Orders. No broker execution.
    """
    version: str
    title: str
    commit: str
    tag: str
    release_type: str
    summary: str
    key_modules: List[str] = field(default_factory=list)
    key_commands: List[str] = field(default_factory=list)
    safety_status: str = "STABLE"
    validation_summary: str = ""
    known_warnings: List[str] = field(default_factory=list)
    no_real_orders: bool = True
    broker_disabled: bool = True
    validated_does_not_enable_trading: bool = True

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "title": self.title,
            "commit": self.commit,
            "tag": self.tag,
            "release_type": self.release_type,
            "summary": self.summary,
            "key_modules": "|".join(self.key_modules),
            "key_commands": "|".join(self.key_commands),
            "safety_status": self.safety_status,
            "validation_summary": self.validation_summary,
            "known_warnings": "|".join(self.known_warnings),
            "no_real_orders": self.no_real_orders,
            "broker_disabled": self.broker_disabled,
            "validated_does_not_enable_trading": self.validated_does_not_enable_trading,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ReleaseEntry":
        return cls(
            version=d.get("version", ""),
            title=d.get("title", ""),
            commit=d.get("commit", ""),
            tag=d.get("tag", ""),
            release_type=d.get("release_type", ""),
            summary=d.get("summary", ""),
            key_modules=[x for x in d.get("key_modules", "").split("|") if x],
            key_commands=[x for x in d.get("key_commands", "").split("|") if x],
            safety_status=d.get("safety_status", "STABLE"),
            validation_summary=d.get("validation_summary", ""),
            known_warnings=[x for x in d.get("known_warnings", "").split("|") if x],
            no_real_orders=bool(d.get("no_real_orders", True)),
            broker_disabled=bool(d.get("broker_disabled", True)),
            validated_does_not_enable_trading=bool(d.get("validated_does_not_enable_trading", True)),
        )


@dataclass
class FinalMaintenanceStatus:
    """Aggregated final maintenance status for v1.0.9.

    [!] Research Only. No Real Orders. No broker execution.
    """
    version: str
    generated_at: str
    total_releases: int
    stable_checks: str
    regression_status: str
    safety_scan_status: str
    gui_status: str
    docs_status: str
    data_hygiene_status: str
    local_assistant_status: str
    knowledge_base_status: str
    workflow_templates_status: str
    long_term_maintenance_ready: bool = True
    no_real_orders: bool = True
    broker_disabled: bool = True
    external_api_disabled: bool = True

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "total_releases": self.total_releases,
            "stable_checks": self.stable_checks,
            "regression_status": self.regression_status,
            "safety_scan_status": self.safety_scan_status,
            "gui_status": self.gui_status,
            "docs_status": self.docs_status,
            "data_hygiene_status": self.data_hygiene_status,
            "local_assistant_status": self.local_assistant_status,
            "knowledge_base_status": self.knowledge_base_status,
            "workflow_templates_status": self.workflow_templates_status,
            "long_term_maintenance_ready": self.long_term_maintenance_ready,
            "no_real_orders": self.no_real_orders,
            "broker_disabled": self.broker_disabled,
            "external_api_disabled": self.external_api_disabled,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FinalMaintenanceStatus":
        return cls(
            version=d.get("version", ""),
            generated_at=d.get("generated_at", ""),
            total_releases=int(d.get("total_releases", 0)),
            stable_checks=d.get("stable_checks", ""),
            regression_status=d.get("regression_status", ""),
            safety_scan_status=d.get("safety_scan_status", ""),
            gui_status=d.get("gui_status", ""),
            docs_status=d.get("docs_status", ""),
            data_hygiene_status=d.get("data_hygiene_status", ""),
            local_assistant_status=d.get("local_assistant_status", ""),
            knowledge_base_status=d.get("knowledge_base_status", ""),
            workflow_templates_status=d.get("workflow_templates_status", ""),
            long_term_maintenance_ready=bool(d.get("long_term_maintenance_ready", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
            broker_disabled=bool(d.get("broker_disabled", True)),
            external_api_disabled=bool(d.get("external_api_disabled", True)),
        )


@dataclass
class LongTermMaintenanceTask:
    """A single long-term maintenance task.

    [!] Research Only. No Real Orders. safe_action must be in ALLOWED_OUTPUTS.
    """
    task_id: str
    cadence: str          # DAILY / WEEKLY / MONTHLY / RELEASE / INCIDENT / ADHOC
    title: str
    command: str
    expected_result: str
    owner_note: str
    safe_action: str      # REVIEW / READ_REPORT / FIX_DATA / BACKTEST_MORE / KEEP_OBSERVING / WAIT
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "cadence": self.cadence,
            "title": self.title,
            "command": self.command,
            "expected_result": self.expected_result,
            "owner_note": self.owner_note,
            "safe_action": self.safe_action,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "LongTermMaintenanceTask":
        return cls(
            task_id=d.get("task_id", ""),
            cadence=d.get("cadence", ""),
            title=d.get("title", ""),
            command=d.get("command", ""),
            expected_result=d.get("expected_result", ""),
            owner_note=d.get("owner_note", ""),
            safe_action=d.get("safe_action", "REVIEW"),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )
