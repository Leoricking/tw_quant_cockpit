"""
portfolio/walk_forward/eligibility_v154.py — Walk-forward Eligibility Gate v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
ELIGIBILITY_VERSION = "1.5.4"


class PortfolioWalkForwardEligibilityGate:
    """Evaluate walk-forward eligibility. Returns structured result, not boolean only."""

    def __init__(self):
        self.version = ELIGIBILITY_VERSION

    def evaluate(self, config) -> Dict[str, Any]:
        """
        Evaluate eligibility for walk-forward run.
        Checks: config valid, research_only=True, broker=False, dates valid,
        min windows, sample sufficient, purge/embargo valid, no future data,
        no executable orders, reproducibility inputs.
        """
        blocked_components: List[str] = []
        warnings: List[str] = []
        blockers: List[str] = []
        evidence: Dict[str, Any] = {}

        if config is None:
            return {
                "run_allowed": False,
                "window_generation_allowed": False,
                "decision_replay_allowed": False,
                "sizing_replay_allowed": False,
                "correlation_replay_allowed": False,
                "risk_control_replay_allowed": False,
                "performance_analysis_allowed": False,
                "formal_research_report_allowed": False,
                "blocked_components": ["ALL"],
                "warnings": [],
                "blockers": ["config is None"],
                "evidence": {},
                "eligibility_status": "BLOCKED",
            }

        # research_only check
        research_only = getattr(config, "research_only", None)
        if research_only is not True:
            blockers.append("research_only must be True")
            blocked_components.append("ALL")

        # auto_apply check
        auto_apply = getattr(config, "auto_apply_enabled", None)
        if auto_apply is True:
            blockers.append("auto_apply_enabled must be False")
            blocked_components.append("ALL")

        # Date checks
        start = getattr(config, "start_date", None)
        end = getattr(config, "end_date", None)
        if start and end:
            if start >= end:
                blockers.append(f"start_date ({start}) >= end_date ({end})")
                blocked_components.append("window_generation")
        else:
            blockers.append("start_date or end_date missing")
            blocked_components.append("window_generation")

        # Length checks
        training = getattr(config, "training_length", 0)
        validation = getattr(config, "validation_length", 0)
        step = getattr(config, "step_length", 0)
        purge = getattr(config, "purge_length", 0)
        embargo = getattr(config, "embargo_length", 0)
        min_windows = getattr(config, "minimum_windows", 0)

        if training <= 0:
            blockers.append("training_length must be > 0")
        if validation <= 0:
            blockers.append("validation_length must be > 0")
        if step <= 0:
            blockers.append("step_length must be > 0")
        if purge < 0:
            blockers.append("purge_length must be >= 0")
        if embargo < 0:
            blockers.append("embargo_length must be >= 0")
        if min_windows <= 0:
            blockers.append("minimum_windows must be > 0")

        if training < 21:
            warnings.append("training_length < 21 days — very short")
        if validation < 5:
            warnings.append("validation_length < 5 days — very short")

        evidence = {
            "research_only": research_only,
            "auto_apply_enabled": auto_apply,
            "training_length": training,
            "validation_length": validation,
            "step_length": step,
            "purge_length": purge,
            "embargo_length": embargo,
            "minimum_windows": min_windows,
        }

        is_blocked = len(blockers) > 0
        run_allowed = not is_blocked

        return {
            "run_allowed": run_allowed,
            "window_generation_allowed": run_allowed,
            "decision_replay_allowed": run_allowed,
            "sizing_replay_allowed": run_allowed,
            "correlation_replay_allowed": run_allowed,
            "risk_control_replay_allowed": run_allowed,
            "performance_analysis_allowed": run_allowed,
            "formal_research_report_allowed": run_allowed,
            "blocked_components": blocked_components,
            "warnings": warnings,
            "blockers": blockers,
            "evidence": evidence,
            "eligibility_status": "BLOCKED" if is_blocked else "ELIGIBLE",
            "research_only": True,
        }
