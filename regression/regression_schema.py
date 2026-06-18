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

    expected_block: set True when the test intentionally verifies that the system
    *correctly* blocks a dangerous operation (e.g. real orders, broker execution).
    When True and the test result is BLOCKED, the runner classifies the outcome as
    PASS ("expected safety block confirmed") rather than a blocking failure.
    This MUST NOT be used to hide genuine execution failures.
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

    # expected_block: True means the test verifies that a dangerous operation is
    # correctly blocked.  BLOCKED result => PASS ("safety guard confirmed").
    expected_block:   bool = False

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
            "expected_block":   self.expected_block,
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

    expected_block: carried from the test case — True when the test intentionally
    verifies that the system blocks a dangerous operation.
    counts_as_pass: True when an expected_block test produced the expected BLOCKED
    result and is therefore counted as a passing check.
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

    # expected-block fields
    expected_block:  bool = False
    counts_as_pass:  bool = False

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
            "expected_block":   self.expected_block,
            "counts_as_pass":   self.counts_as_pass,
            "read_only":        self.read_only,
            "no_real_orders":   self.no_real_orders,
            "production_blocked": self.production_blocked,
        }
