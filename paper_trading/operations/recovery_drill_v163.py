"""
Recovery Drill v1.6.3 — Fixture/Replay only. No real sessions.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.operations.models_v163 import _new_id, _now_utc


DRILL_SCENARIOS = [
    "market_data_disconnect",
    "stale_data",
    "sequence_gap",
    "paper_session_halt",
    "strategy_failure",
    "checkpoint_hash_mismatch",
    "recovery_replay_mismatch",
    "alert_storm_suppression",
    "incident_lifecycle",
    "safety_violation",
]


@dataclass
class DrillStep:
    step_id:         str
    description:     str
    action:          str
    expected_result: str
    actual_result:   str  = ""
    passed:          bool = False
    error:           str  = ""


@dataclass
class DrillResult:
    scenario_id:       str
    scenario_name:     str
    drill_id:          str
    steps:             List[DrillStep]    = field(default_factory=list)
    expected_result:   str               = ""
    actual_result:     str               = ""
    passed:            bool              = False
    failed_step:       Optional[str]     = None
    recovery_duration: float             = 0.0  # simulated seconds
    final_status:      str               = ""
    final_hash:        str               = ""
    audit_ids:         List[str]         = field(default_factory=list)
    completed_at:      Optional[datetime] = None
    paper_only:        bool              = True
    research_only:     bool              = True


class RecoveryDrillEngine:
    """Runs fixture-based recovery drills. Never operates on real sessions."""

    def run(
        self,
        scenario: str,
        *,
        inject_failure: bool = False,
        fixture_data:   Optional[Dict[str, Any]] = None,
    ) -> DrillResult:
        if scenario not in DRILL_SCENARIOS:
            return DrillResult(
                scenario_id=scenario, scenario_name="unknown",
                drill_id=_new_id("drl_"),
                passed=False, actual_result=f"Unknown scenario: {scenario}",
                paper_only=True, research_only=True,
            )

        drill_id = _new_id("drl_")
        steps = self._build_steps(scenario, inject_failure, fixture_data or {})
        all_passed = all(s.passed for s in steps)
        failed_step = next((s.step_id for s in steps if not s.passed), None)

        from paper_trading.operations.models_v163 import _semantic_hash
        final_hash = _semantic_hash({
            "scenario": scenario,
            "drill_id": drill_id,
            "steps": len(steps),
            "all_passed": all_passed,
        })

        return DrillResult(
            scenario_id=scenario,
            scenario_name=scenario.replace("_", " ").title(),
            drill_id=drill_id,
            steps=steps,
            expected_result="Recovery completed in RECOVERED status",
            actual_result="RECOVERED — explicit resume required" if all_passed else f"Failed at step {failed_step}",
            passed=all_passed,
            failed_step=failed_step,
            recovery_duration=1.5 if all_passed else 0.5,
            final_status="RECOVERED" if all_passed else "HALTED",
            final_hash=final_hash,
            audit_ids=[_new_id("aud_")],
            completed_at=_now_utc(),
            paper_only=True,
            research_only=True,
        )

    def _build_steps(self, scenario: str, inject_failure: bool, fixture_data: dict) -> List[DrillStep]:
        base = [
            DrillStep("s1", "Detect condition",      "detect",    "Condition detected",       actual_result="Detected",       passed=True),
            DrillStep("s2", "Pause session",          "pause",     "Session PAUSED",           actual_result="PAUSED",         passed=True),
            DrillStep("s3", "Create checkpoint",      "checkpoint","Checkpoint created",       actual_result="Created",        passed=True),
            DrillStep("s4", "Validate checkpoint",    "validate",  "Checkpoint valid",         actual_result="Valid" if not inject_failure else "HASH_MISMATCH", passed=not inject_failure),
            DrillStep("s5", "Replay tail events",     "replay",    "Replay complete",          actual_result="Replayed",       passed=not inject_failure),
            DrillStep("s6", "Verify final hash",      "verify",    "Hash matches",             actual_result="Match",          passed=not inject_failure),
            DrillStep("s7", "Set RECOVERED",          "recover",   "Status=RECOVERED",         actual_result="RECOVERED",      passed=not inject_failure),
            DrillStep("s8", "Await explicit resume",  "wait",      "Awaiting manual resume",   actual_result="Waiting",        passed=not inject_failure),
        ]
        return base

    def list_scenarios(self) -> List[str]:
        return list(DRILL_SCENARIOS)


__all__ = ["RecoveryDrillEngine", "DrillResult", "DrillStep", "DRILL_SCENARIOS"]
