"""
workflow/workflow_profiles.py - Workflow Profile Registry (v0.3.21).

Defines which steps to run for each profile:
  quick     : pre-market / fast check
  standard  : daily after close
  full      : weekend comprehensive research
  gui_only  : just open cockpit

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

from typing import Dict, List


# ---------------------------------------------------------------------------
# Step names (canonical identifiers)
# ---------------------------------------------------------------------------

STEP_PROVIDER_HEALTH    = "provider_health"
STEP_PROVIDER_FETCH     = "provider_auto_fetch"
STEP_DATA_FRESHNESS     = "data_freshness"
STEP_QUALITY_GATE       = "data_quality_gate"
STEP_DATA_SOURCE_STATUS = "data_source_status"
STEP_UNIVERSE_QUALITY   = "universe_quality"
STEP_SIGNAL_QUALITY     = "signal_quality"
STEP_PORTFOLIO_SIM      = "portfolio_simulation"
STEP_RULE_WEIGHT        = "rule_weight_tuning"
STEP_AUTO_REPORT        = "auto_report"
STEP_LONG_TERM          = "backtest_long_term"
STEP_STRATEGY_KNOWLEDGE = "backtest_strategy_knowledge"
STEP_VALIDATION_SUITE   = "run_validation_suite"


# ---------------------------------------------------------------------------
# Profile definitions
# ---------------------------------------------------------------------------

class WorkflowProfile:
    """
    Describes which steps to run for a named profile.

    Parameters
    ----------
    name        : profile name
    description : human-readable description
    update_data_steps  : steps for update-data phase
    research_steps     : steps for run-research phase
    auto_report_profile: 'daily' or 'full' for AutoReportCenter
    """

    def __init__(
        self,
        name: str,
        description: str,
        update_data_steps: List[str],
        research_steps: List[str],
        auto_report_profile: str = "daily",
    ):
        self.name                = name
        self.description         = description
        self.update_data_steps   = list(update_data_steps)
        self.research_steps      = list(research_steps)
        self.auto_report_profile = auto_report_profile

    def all_steps(self) -> List[str]:
        seen = set()
        result = []
        for s in self.update_data_steps + self.research_steps:
            if s not in seen:
                seen.add(s)
                result.append(s)
        return result

    def to_dict(self) -> dict:
        return {
            "name":                self.name,
            "description":         self.description,
            "update_data_steps":   self.update_data_steps,
            "research_steps":      self.research_steps,
            "auto_report_profile": self.auto_report_profile,
        }


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_PROFILES: Dict[str, WorkflowProfile] = {
    "quick": WorkflowProfile(
        name="quick",
        description="Pre-market / fast check: health + freshness + quality gate + auto-report",
        update_data_steps=[
            STEP_PROVIDER_HEALTH,
            STEP_DATA_FRESHNESS,
            STEP_QUALITY_GATE,
        ],
        research_steps=[
            STEP_QUALITY_GATE,
            STEP_AUTO_REPORT,
        ],
        auto_report_profile="daily",
    ),
    "standard": WorkflowProfile(
        name="standard",
        description="Daily after close: full data update + research reports",
        update_data_steps=[
            STEP_PROVIDER_HEALTH,
            STEP_PROVIDER_FETCH,
            STEP_DATA_FRESHNESS,
            STEP_QUALITY_GATE,
            STEP_DATA_SOURCE_STATUS,
            STEP_UNIVERSE_QUALITY,
        ],
        research_steps=[
            STEP_QUALITY_GATE,
            STEP_SIGNAL_QUALITY,
            STEP_PORTFOLIO_SIM,
            STEP_AUTO_REPORT,
        ],
        auto_report_profile="daily",
    ),
    "full": WorkflowProfile(
        name="full",
        description="Weekend comprehensive research: all steps + validation suites",
        update_data_steps=[
            STEP_PROVIDER_HEALTH,
            STEP_PROVIDER_FETCH,
            STEP_DATA_FRESHNESS,
            STEP_QUALITY_GATE,
            STEP_DATA_SOURCE_STATUS,
            STEP_UNIVERSE_QUALITY,
        ],
        research_steps=[
            STEP_QUALITY_GATE,
            STEP_SIGNAL_QUALITY,
            STEP_PORTFOLIO_SIM,
            STEP_RULE_WEIGHT,
            STEP_LONG_TERM,
            STEP_STRATEGY_KNOWLEDGE,
            STEP_VALIDATION_SUITE,
            STEP_AUTO_REPORT,
        ],
        auto_report_profile="full",
    ),
    "gui_only": WorkflowProfile(
        name="gui_only",
        description="Open cockpit GUI only, no data update or research",
        update_data_steps=[],
        research_steps=[],
        auto_report_profile="daily",
    ),
}


class WorkflowProfileRegistry:
    """Registry of available workflow profiles."""

    @staticmethod
    def get(name: str) -> WorkflowProfile:
        if name not in _PROFILES:
            raise ValueError(
                f"Unknown profile '{name}'. Available: {list(_PROFILES.keys())}"
            )
        return _PROFILES[name]

    @staticmethod
    def names() -> List[str]:
        return list(_PROFILES.keys())

    @staticmethod
    def all_profiles() -> Dict[str, WorkflowProfile]:
        return dict(_PROFILES)
