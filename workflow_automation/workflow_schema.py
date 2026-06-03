"""
workflow_automation/workflow_schema.py — ResearchWorkflowTask / ResearchWorkflowRun (v0.4.9).

Defines schema for Research Workflow Automation.

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] suggested_command must pass SafeCommandRegistry. No buy/sell/order.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# ---------------------------------------------------------------------------
# workflow_type constants
# ---------------------------------------------------------------------------
WF_DAILY_RESEARCH   = "daily_research"
WF_WEEKLY_REVIEW    = "weekly_review"
WF_COACH_CHECKLIST  = "coach_checklist"
WF_DATA_REPAIR      = "data_repair"
WF_REPLAY_TRAINING  = "replay_training"
WF_RULE_REVIEW      = "rule_review"
WF_SAFETY_CHECK     = "safety_check"

ALL_WORKFLOW_TYPES = [
    WF_DAILY_RESEARCH, WF_WEEKLY_REVIEW, WF_COACH_CHECKLIST,
    WF_DATA_REPAIR, WF_REPLAY_TRAINING, WF_RULE_REVIEW, WF_SAFETY_CHECK,
]

# ---------------------------------------------------------------------------
# task_type constants
# ---------------------------------------------------------------------------
TASK_COMMAND      = "command"
TASK_REPORT       = "report"
TASK_CHECKLIST    = "checklist"
TASK_REVIEW       = "review"
TASK_PACKAGE      = "package"
TASK_NOTIFICATION = "notification"

ALL_TASK_TYPES = [
    TASK_COMMAND, TASK_REPORT, TASK_CHECKLIST,
    TASK_REVIEW, TASK_PACKAGE, TASK_NOTIFICATION,
]

# ---------------------------------------------------------------------------
# status constants
# ---------------------------------------------------------------------------
STATUS_PENDING  = "PENDING"
STATUS_RUNNING  = "RUNNING"
STATUS_PASS     = "PASS"
STATUS_WARNING  = "WARNING"
STATUS_FAILED   = "FAILED"
STATUS_SKIPPED  = "SKIPPED"
STATUS_BLOCKED  = "BLOCKED"

ALL_STATUSES = [
    STATUS_PENDING, STATUS_RUNNING, STATUS_PASS,
    STATUS_WARNING, STATUS_FAILED, STATUS_SKIPPED, STATUS_BLOCKED,
]

# ---------------------------------------------------------------------------
# priority constants
# ---------------------------------------------------------------------------
PRIORITY_P0 = "P0"
PRIORITY_P1 = "P1"
PRIORITY_P2 = "P2"
PRIORITY_P3 = "P3"


@dataclass
class ResearchWorkflowTask:
    """
    A single research workflow task.

    Safety invariants (always True):
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      suggested_command  = research-only (validated by SafeCommandRegistry)
    """

    # Identity
    task_id:    str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    workflow_id: str = ""

    # Classification
    task_type: str = TASK_COMMAND
    task_name: str = ""
    priority:  str = PRIORITY_P3

    # Category (free-form mirror of coach/review category)
    category:  str = "workflow"

    # Action
    suggested_command: str = ""

    # Status
    status: str = STATUS_PENDING

    # References
    source:                   str = ""
    source_recommendation_id: Optional[str] = None
    related_report:           Optional[str] = None
    related_dataset:          Optional[str] = None
    related_rule_id:          Optional[str] = None
    related_journal_id:       Optional[str] = None
    related_experiment_id:    Optional[str] = None

    # Results
    result_summary:   str = ""
    warning:          str = ""
    duration_seconds: float = 0.0

    # Safety flags — always True
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "task_id":                   self.task_id,
            "created_at":                self.created_at,
            "workflow_id":               self.workflow_id,
            "task_type":                 self.task_type,
            "task_name":                 self.task_name,
            "priority":                  self.priority,
            "category":                  self.category,
            "suggested_command":         self.suggested_command,
            "status":                    self.status,
            "source":                    self.source,
            "source_recommendation_id":  self.source_recommendation_id or "",
            "related_report":            self.related_report or "",
            "related_dataset":           self.related_dataset or "",
            "related_rule_id":           self.related_rule_id or "",
            "related_journal_id":        self.related_journal_id or "",
            "related_experiment_id":     self.related_experiment_id or "",
            "result_summary":            self.result_summary,
            "warning":                   self.warning,
            "duration_seconds":          self.duration_seconds,
            "read_only":                 self.read_only,
            "no_real_orders":            self.no_real_orders,
            "production_blocked":        self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ResearchWorkflowTask":
        return cls(
            task_id=d.get("task_id", str(uuid.uuid4())[:12]),
            created_at=d.get("created_at", datetime.now().isoformat(timespec="seconds")),
            workflow_id=d.get("workflow_id", ""),
            task_type=d.get("task_type", TASK_COMMAND),
            task_name=d.get("task_name", ""),
            priority=d.get("priority", PRIORITY_P3),
            category=d.get("category", "workflow"),
            suggested_command=d.get("suggested_command", ""),
            status=d.get("status", STATUS_PENDING),
            source=d.get("source", ""),
            source_recommendation_id=d.get("source_recommendation_id") or None,
            related_report=d.get("related_report") or None,
            related_dataset=d.get("related_dataset") or None,
            related_rule_id=d.get("related_rule_id") or None,
            related_journal_id=d.get("related_journal_id") or None,
            related_experiment_id=d.get("related_experiment_id") or None,
            result_summary=d.get("result_summary", ""),
            warning=d.get("warning", ""),
            duration_seconds=float(d.get("duration_seconds", 0.0) or 0.0),
            read_only=True,
            no_real_orders=True,
            production_blocked=True,
        )


@dataclass
class ResearchWorkflowRun:
    """
    A research workflow run record.

    Safety invariants (always True):
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    workflow_id:   str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    created_at:    str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    mode:          str = "real"
    profile:       str = "daily"
    workflow_type: str = WF_DAILY_RESEARCH
    status:        str = STATUS_PENDING

    tasks_total:   int = 0
    tasks_run:     int = 0
    tasks_passed:  int = 0
    tasks_failed:  int = 0
    tasks_skipped: int = 0
    tasks_blocked: int = 0

    output_package_path: str = ""
    report_path:         str = ""

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "workflow_id":          self.workflow_id,
            "created_at":           self.created_at,
            "mode":                 self.mode,
            "profile":              self.profile,
            "workflow_type":        self.workflow_type,
            "status":               self.status,
            "tasks_total":          self.tasks_total,
            "tasks_run":            self.tasks_run,
            "tasks_passed":         self.tasks_passed,
            "tasks_failed":         self.tasks_failed,
            "tasks_skipped":        self.tasks_skipped,
            "tasks_blocked":        self.tasks_blocked,
            "output_package_path":  self.output_package_path,
            "report_path":          self.report_path,
            "read_only":            self.read_only,
            "no_real_orders":       self.no_real_orders,
            "production_blocked":   self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ResearchWorkflowRun":
        return cls(
            workflow_id=d.get("workflow_id", str(uuid.uuid4())[:12]),
            created_at=d.get("created_at", datetime.now().isoformat(timespec="seconds")),
            mode=d.get("mode", "real"),
            profile=d.get("profile", "daily"),
            workflow_type=d.get("workflow_type", WF_DAILY_RESEARCH),
            status=d.get("status", STATUS_PENDING),
            tasks_total=int(d.get("tasks_total", 0) or 0),
            tasks_run=int(d.get("tasks_run", 0) or 0),
            tasks_passed=int(d.get("tasks_passed", 0) or 0),
            tasks_failed=int(d.get("tasks_failed", 0) or 0),
            tasks_skipped=int(d.get("tasks_skipped", 0) or 0),
            tasks_blocked=int(d.get("tasks_blocked", 0) or 0),
            output_package_path=d.get("output_package_path", ""),
            report_path=d.get("report_path", ""),
            read_only=True,
            no_real_orders=True,
            production_blocked=True,
        )
