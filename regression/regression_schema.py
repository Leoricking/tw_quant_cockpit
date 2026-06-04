"""regression/regression_schema.py — RegressionTestCase / RegressionTestResult schema.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_PASS    = "PASS"
STATUS_WARNING = "WARNING"
STATUS_FAIL    = "FAIL"
STATUS_SKIPPED = "SKIPPED"
STATUS_BLOCKED = "BLOCKED"
STATUS_TIMEOUT = "TIMEOUT"

# ---------------------------------------------------------------------------
# Suite constants
# ---------------------------------------------------------------------------
SUITE_QUICK       = "quick"
SUITE_FULL        = "full"
SUITE_GUI         = "gui"
SUITE_REPORT      = "report"
SUITE_SAFETY      = "safety"
SUITE_DATA        = "data"
SUITE_PROVIDER    = "provider"
SUITE_STRATEGY    = "strategy"
SUITE_REPLAY      = "replay"
SUITE_RESEARCH_OS = "research_os"
SUITE_RELEASE_GATE = "release_gate"


@dataclass
class RegressionTestCase:
    """Schema for a single regression test case.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    test_id:          str
    name:             str
    suite:            str
    category:         str
    command:          List[str]
    timeout_seconds:  int  = 60
    expected_status:  str  = STATUS_PASS
    required:         bool = True
    mode:             str  = "real"
    safety_level:     str  = "RESEARCH_ONLY"
    description:      str  = ""
    tags:             List[str] = field(default_factory=list)

    # Safety invariants — always True, never modified
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "test_id":          self.test_id,
            "name":             self.name,
            "suite":            self.suite,
            "category":         self.category,
            "command":          self.command,
            "timeout_seconds":  self.timeout_seconds,
            "expected_status":  self.expected_status,
            "required":         self.required,
            "mode":             self.mode,
            "safety_level":     self.safety_level,
            "description":      self.description,
            "tags":             self.tags,
            "read_only":        self.read_only,
            "no_real_orders":   self.no_real_orders,
            "production_blocked": self.production_blocked,
        }


@dataclass
class RegressionTestResult:
    """Schema for a single regression test result.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    test_id:          str
    name:             str
    suite:            str
    status:           str
    return_code:      int   = 0
    duration_seconds: float = 0.0
    stdout_tail:      str   = ""
    stderr_tail:      str   = ""
    warning:          str   = ""
    error:            str   = ""
    started_at:       str   = ""
    finished_at:      str   = ""

    # Safety invariants — always True, never modified
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "test_id":          self.test_id,
            "name":             self.name,
            "suite":            self.suite,
            "status":           self.status,
            "return_code":      self.return_code,
            "duration_seconds": self.duration_seconds,
            "stdout_tail":      self.stdout_tail,
            "stderr_tail":      self.stderr_tail,
            "warning":          self.warning,
            "error":            self.error,
            "started_at":       self.started_at,
            "finished_at":      self.finished_at,
            "read_only":        self.read_only,
            "no_real_orders":   self.no_real_orders,
            "production_blocked": self.production_blocked,
        }
