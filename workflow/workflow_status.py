"""
workflow/workflow_status.py - Workflow Step Result & Status (v0.3.21).

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Step result
# ---------------------------------------------------------------------------

class WorkflowStepResult:
    """
    Holds the result of a single workflow step.

    Parameters
    ----------
    step_name : identifier string, e.g. 'provider_health'
    """

    # Status constants
    OK      = "OK"
    PARTIAL = "PARTIAL"
    FAILED  = "FAILED"
    SKIPPED = "SKIPPED"
    BLOCKED = "BLOCKED"

    # Safety invariants
    read_only      = True
    no_real_orders = True
    production_blocked = True

    __slots__ = (
        "step_name",
        "status",
        "started_at",
        "finished_at",
        "duration_seconds",
        "outputs",
        "warnings",
        "errors",
        "safety_flags",
        "next_action",
        "extra",
        "_start_dt",
    )

    def __init__(self, step_name: str):
        self.step_name:        str   = step_name
        self.status:           str   = self.SKIPPED
        self.started_at:       Optional[str] = None
        self.finished_at:      Optional[str] = None
        self.duration_seconds: float = 0.0
        self.outputs:          List[str] = []
        self.warnings:         List[str] = []
        self.errors:           List[str] = []
        self.safety_flags:     dict = {
            "read_only":           True,
            "no_real_orders":      True,
            "production_blocked":  True,
        }
        self.next_action:      str  = ""
        self.extra:            dict = {}
        self._start_dt               = None

    # ------------------------------------------------------------------
    # Context manager for timing
    # ------------------------------------------------------------------

    def __enter__(self):
        self.started_at = datetime.now().isoformat()
        self._start_dt  = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = datetime.now()
        self.finished_at      = end.isoformat()
        self.duration_seconds = round((end - self._start_dt).total_seconds(), 2)
        if exc_type is not None:
            self.status = self.FAILED
            self.errors.append(str(exc_val))
        return False   # do not suppress exceptions

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def mark_ok(self, outputs: Optional[List[str]] = None):
        self.status = self.OK
        if outputs:
            self.outputs.extend(outputs)

    def mark_partial(self, warnings: Optional[List[str]] = None):
        self.status = self.PARTIAL
        if warnings:
            self.warnings.extend(warnings)

    def mark_failed(self, error: str):
        self.status = self.FAILED
        self.errors.append(error)

    def mark_skipped(self, reason: str = ""):
        self.status = self.SKIPPED
        if reason:
            self.outputs.append(f"Skipped: {reason}")

    def to_dict(self) -> dict:
        return {
            "step_name":        self.step_name,
            "status":           self.status,
            "started_at":       self.started_at,
            "finished_at":      self.finished_at,
            "duration_seconds": self.duration_seconds,
            "outputs":          self.outputs,
            "warnings":         self.warnings,
            "errors":           self.errors,
            "safety_flags":     self.safety_flags,
            "next_action":      self.next_action,
            **self.extra,
        }


# ---------------------------------------------------------------------------
# Overall workflow status
# ---------------------------------------------------------------------------

class WorkflowStatus:
    """
    Tracks overall workflow execution status across all steps.

    Parameters
    ----------
    workflow_name : e.g. 'daily_workflow'
    mode          : 'real' or 'mock'
    profile       : 'quick' / 'standard' / 'full' / 'gui_only'
    """

    # Safety invariants
    read_only       = True
    no_real_orders  = True
    production_blocked = True

    def __init__(
        self,
        workflow_name: str = "daily_workflow",
        mode:    str = "real",
        profile: str = "standard",
    ):
        self.workflow_name = workflow_name
        self.mode          = mode
        self.profile       = profile
        self.started_at:  Optional[str] = None
        self.finished_at: Optional[str] = None
        self.steps: List[WorkflowStepResult] = []
        self._start_dt: Optional[datetime] = None

    def start(self):
        self._start_dt  = datetime.now()
        self.started_at = self._start_dt.isoformat()

    def finish(self):
        end = datetime.now()
        self.finished_at     = end.isoformat()
        self.duration_seconds = round(
            (end - self._start_dt).total_seconds(), 2
        ) if self._start_dt else 0.0

    def add_step(self, step: WorkflowStepResult):
        self.steps.append(step)

    # ------------------------------------------------------------------
    # Aggregate status
    # ------------------------------------------------------------------

    @property
    def overall_status(self) -> str:
        if any(s.status == WorkflowStepResult.FAILED for s in self.steps):
            return "PARTIAL"   # partial = some steps failed but others succeeded
        if all(s.status in (WorkflowStepResult.OK, WorkflowStepResult.SKIPPED) for s in self.steps):
            return "OK"
        if any(s.status == WorkflowStepResult.PARTIAL for s in self.steps):
            return "PARTIAL"
        return "OK"

    @property
    def failed_steps(self) -> List[str]:
        return [s.step_name for s in self.steps if s.status == WorkflowStepResult.FAILED]

    @property
    def ok_steps(self) -> List[str]:
        return [s.step_name for s in self.steps if s.status == WorkflowStepResult.OK]

    @property
    def warning_count(self) -> int:
        return sum(len(s.warnings) for s in self.steps)

    def to_dict(self) -> dict:
        return {
            "workflow_name":    self.workflow_name,
            "mode":             self.mode,
            "profile":          self.profile,
            "started_at":       self.started_at,
            "finished_at":      self.finished_at,
            "duration_seconds": getattr(self, "duration_seconds", 0.0),
            "overall_status":   self.overall_status,
            "ok_steps":         self.ok_steps,
            "failed_steps":     self.failed_steps,
            "warning_count":    self.warning_count,
            "steps":            [s.to_dict() for s in self.steps],
            "safety_flags": {
                "read_only":          self.read_only,
                "no_real_orders":     self.no_real_orders,
                "production_blocked": self.production_blocked,
            },
        }
