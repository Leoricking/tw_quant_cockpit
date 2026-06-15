"""report_pack/report_registry.py — ReportRegistry for TW Quant Cockpit v0.5.4.

Defines which report types are included in each pack type (daily/weekly/full).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List

from report_pack.report_pack_schema import (
    PACK_DAILY, PACK_WEEKLY, PACK_FULL, PACK_CUSTOM,
    REPORT_DAILY_MARKET, REPORT_AUTO_REPORT, REPORT_DATA_QUALITY,
    REPORT_PROVIDER, REPORT_STRATEGY_FILTER, REPORT_SIGNAL_QUALITY,
    REPORT_RULE_GOVERNANCE, REPORT_PORTFOLIO_JOURNAL, REPORT_RESEARCH_REVIEW,
    REPORT_RESEARCH_COACH, REPORT_RESEARCH_WORKFLOW, REPORT_RESEARCH_OS,
    REPORT_REGRESSION, REPORT_CLI_UX, REPORT_GUI_NAVIGATION,
    REPORT_NOTIFICATION, REPORT_INTRADAY_REPLAY, REPORT_EXPERIMENT,
    REPORT_RELEASE, REPORT_SAFETY, REPORT_DATA_STABILIZATION,
    REPORT_REPLAY_TRAINING, REPORT_STABLE_RELEASE_V060, REPORT_RELEASE_MANIFEST,
    REPORT_DATA_COVERAGE, REPORT_RESEARCH_INTELLIGENCE,
    REPORT_STRATEGY_MEMORY,
    REPORT_BACKTEST_COACH,
    REPORT_INTELLIGENCE_STABLE,
    REPORT_TRAINING_METRICS,
    REPORT_EVIDENCE_GRAPH,
)

# v0.9.0.1 crash reversal
REPORT_CRASH_REVERSAL = "crash_reversal_strategy_report"

# v0.9.2 strategy validation
REPORT_STRATEGY_VALIDATION = "strategy_validation_report"

# v0.9.3 strategy lab dashboard
REPORT_STRATEGY_LAB_DASHBOARD = "strategy_lab_dashboard_report"

# v1.0.0 Research Trading Cockpit Stable
REPORT_RESEARCH_COCKPIT_STABLE = "research_trading_cockpit_stable_report"

# v1.0.2 Data & Report Hygiene
REPORT_DATA_REPORT_HYGIENE = "data_report_hygiene_report"

# v1.0.3 GUI Stability & Usability Polish
REPORT_GUI_USABILITY = "gui_usability_report"

# v1.0.4 Regression & Release Gate Hardening
REPORT_REGRESSION_HARDENING = "regression_hardening_report"

# v1.0.5 Documentation & User Guide Polish
REPORT_DOCUMENTATION_HEALTH = "documentation_health_report"

# v1.0.6 Example Workflows & Templates
REPORT_WORKFLOW_TEMPLATES = "workflow_templates_report"

# v1.0.7 Knowledge Base Search Polish
REPORT_KNOWLEDGE_BASE_SEARCH = "knowledge_base_search_report"

# v1.0.8 Local Research Assistant Polish
REPORT_LOCAL_RESEARCH_ASSISTANT = "local_research_assistant_report"

# v1.0.9 Final Maintenance Rollup
REPORT_FINAL_MAINTENANCE_ROLLUP = "final_maintenance_rollup_report"

# v1.1.0 Data Universe Expansion
REPORT_DATA_UNIVERSE_EXPANSION = "data_universe_expansion_report"

# v1.1.1 Data Import UX & Batch Onboarding
REPORT_DATA_IMPORT_ONBOARDING = "data_import_onboarding_report"

# v1.1.2 Coverage Repair Workflow
REPORT_COVERAGE_REPAIR = "coverage_repair_report"

# v1.1.3 Data Freshness Monitor
REPORT_DATA_FRESHNESS = "data_freshness_report"

# v1.1.4 Coverage Quality Gates
REPORT_COVERAGE_QUALITY_GATE = "coverage_quality_gate_report"

# v1.1.5 Quality Gate Enforcement & Audit
REPORT_GATE_ENFORCEMENT_AUDIT    = "quality_gate_enforcement_audit_report"
REPORT_GATE_RUN_SUMMARY          = "gate_run_summary_report"
REPORT_GATE_EXCLUSION_SUMMARY    = "gate_exclusion_summary_report"
REPORT_GATE_REPRODUCIBILITY      = "gate_reproducibility_summary_report"

# v1.1.6 Data Governance Operations Dashboard
REPORT_DATA_GOVERNANCE_OPERATIONS = "data_governance_operations_report"
REPORT_GOVERNANCE_ACTION_QUEUE    = "governance_action_queue_report"
REPORT_GOVERNANCE_MODULE_HEALTH   = "governance_module_health_report"
REPORT_GOVERNANCE_AUDIT_SUMMARY   = "governance_audit_summary_report"

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pack definitions: which report types are included per pack type
# ---------------------------------------------------------------------------

_PACK_DEFINITIONS: Dict[str, List[str]] = {
    PACK_DAILY: [
        REPORT_DAILY_MARKET,
        REPORT_AUTO_REPORT,
        REPORT_DATA_QUALITY,
        REPORT_PROVIDER,
        REPORT_SIGNAL_QUALITY,
        REPORT_PORTFOLIO_JOURNAL,
        REPORT_NOTIFICATION,
        REPORT_RESEARCH_COACH,
        REPORT_STRATEGY_FILTER,
        REPORT_DATA_STABILIZATION,
        REPORT_REPLAY_TRAINING,
        # v0.7.2 Strategy Research Memory (optional in daily pack)
        REPORT_STRATEGY_MEMORY,
        # v0.7.3 Backtest-to-Coach Loop (optional in daily pack)
        REPORT_BACKTEST_COACH,
        # v0.8.0 Research Intelligence Stable (optional in daily pack)
        REPORT_INTELLIGENCE_STABLE,
        # v0.8.2 Backtest Training Metrics (optional in daily pack)
        REPORT_TRAINING_METRICS,
        # v0.8.3 Research Intelligence Evidence Graph (optional in daily pack)
        REPORT_EVIDENCE_GRAPH,
        # v0.9.0.1 Crash Reversal & Risk Discipline Strategy Pack (optional in daily pack)
        REPORT_CRASH_REVERSAL,
        # v0.9.2 Strategy Validation Score (optional in daily pack)
        REPORT_STRATEGY_VALIDATION,
        # v0.9.3 Strategy Lab Dashboard (optional in daily pack)
        REPORT_STRATEGY_LAB_DASHBOARD,
        # v1.0.3 GUI Stability & Usability Polish (optional in daily pack)
        REPORT_GUI_USABILITY,
        # v1.0.4 Regression & Release Gate Hardening (optional in daily pack)
        REPORT_REGRESSION_HARDENING,
        # v1.0.5 Documentation & User Guide Polish (optional in daily pack)
        REPORT_DOCUMENTATION_HEALTH,
        # v1.0.6 Example Workflows & Templates (optional in daily pack)
        REPORT_WORKFLOW_TEMPLATES,
        # v1.0.7 Knowledge Base Search Polish (optional in daily pack)
        REPORT_KNOWLEDGE_BASE_SEARCH,
        # v1.0.8 Local Research Assistant Polish (optional in daily pack)
        REPORT_LOCAL_RESEARCH_ASSISTANT,
        # v1.0.9 Final Maintenance Rollup (optional in daily pack)
        REPORT_FINAL_MAINTENANCE_ROLLUP,
        # v1.1.6 Data Governance Operations Dashboard (optional in daily pack)
        REPORT_DATA_GOVERNANCE_OPERATIONS,
        REPORT_GOVERNANCE_ACTION_QUEUE,
    ],
    PACK_WEEKLY: [
        REPORT_DAILY_MARKET,
        REPORT_AUTO_REPORT,
        REPORT_DATA_QUALITY,
        REPORT_PROVIDER,
        REPORT_SIGNAL_QUALITY,
        REPORT_PORTFOLIO_JOURNAL,
        REPORT_NOTIFICATION,
        REPORT_RESEARCH_COACH,
        REPORT_STRATEGY_FILTER,
        REPORT_RULE_GOVERNANCE,
        REPORT_RESEARCH_REVIEW,
        REPORT_RESEARCH_WORKFLOW,
        REPORT_RESEARCH_OS,
        REPORT_CLI_UX,
        REPORT_GUI_NAVIGATION,
        REPORT_EXPERIMENT,
        REPORT_DATA_STABILIZATION,
        # v0.7.2 Strategy Research Memory (optional in weekly pack)
        REPORT_STRATEGY_MEMORY,
        # v0.7.3 Backtest-to-Coach Loop (optional in weekly pack)
        REPORT_BACKTEST_COACH,
        # v0.8.0 Research Intelligence Stable (optional in weekly pack)
        REPORT_INTELLIGENCE_STABLE,
        # v0.8.2 Backtest Training Metrics (optional in weekly pack)
        REPORT_TRAINING_METRICS,
        # v0.8.3 Research Intelligence Evidence Graph (optional in weekly pack)
        REPORT_EVIDENCE_GRAPH,
        # v0.9.0.1 Crash Reversal & Risk Discipline Strategy Pack (optional in weekly pack)
        REPORT_CRASH_REVERSAL,
        # v0.9.2 Strategy Validation Score (optional in weekly pack)
        REPORT_STRATEGY_VALIDATION,
        # v0.9.3 Strategy Lab Dashboard (optional in weekly pack)
        REPORT_STRATEGY_LAB_DASHBOARD,
        # v1.0.3 GUI Stability & Usability Polish (optional in weekly pack)
        REPORT_GUI_USABILITY,
        # v1.0.4 Regression & Release Gate Hardening (optional in weekly pack)
        REPORT_REGRESSION_HARDENING,
        # v1.0.5 Documentation & User Guide Polish (optional in weekly pack)
        REPORT_DOCUMENTATION_HEALTH,
        # v1.0.6 Example Workflows & Templates (optional in weekly pack)
        REPORT_WORKFLOW_TEMPLATES,
        # v1.0.7 Knowledge Base Search Polish (optional in weekly pack)
        REPORT_KNOWLEDGE_BASE_SEARCH,
        # v1.0.8 Local Research Assistant Polish (optional in weekly pack)
        REPORT_LOCAL_RESEARCH_ASSISTANT,
        # v1.0.9 Final Maintenance Rollup (optional in weekly pack)
        REPORT_FINAL_MAINTENANCE_ROLLUP,
        # v1.1.0 Data Universe Expansion (optional in weekly pack)
        REPORT_DATA_UNIVERSE_EXPANSION,
        # v1.1.1 Data Import UX & Batch Onboarding (optional in weekly pack)
        REPORT_DATA_IMPORT_ONBOARDING,
        # v1.1.2 Coverage Repair Workflow (optional in weekly pack)
        REPORT_COVERAGE_REPAIR,
        # v1.1.3 Data Freshness Monitor (optional in weekly pack)
        REPORT_DATA_FRESHNESS,
        # v1.1.4 Coverage Quality Gates (optional in weekly pack)
        REPORT_COVERAGE_QUALITY_GATE,
        # v1.1.5 Quality Gate Enforcement & Audit (optional in weekly pack)
        REPORT_GATE_ENFORCEMENT_AUDIT,
        REPORT_GATE_RUN_SUMMARY,
        REPORT_GATE_EXCLUSION_SUMMARY,
        REPORT_GATE_REPRODUCIBILITY,
        # v1.1.6 Data Governance Operations Dashboard (optional in weekly pack)
        REPORT_DATA_GOVERNANCE_OPERATIONS,
        REPORT_GOVERNANCE_ACTION_QUEUE,
        REPORT_GOVERNANCE_MODULE_HEALTH,
        REPORT_GOVERNANCE_AUDIT_SUMMARY,
    ],
    PACK_FULL: [
        REPORT_DAILY_MARKET,
        REPORT_AUTO_REPORT,
        REPORT_DATA_QUALITY,
        REPORT_PROVIDER,
        REPORT_SIGNAL_QUALITY,
        REPORT_PORTFOLIO_JOURNAL,
        REPORT_NOTIFICATION,
        REPORT_RESEARCH_COACH,
        REPORT_STRATEGY_FILTER,
        REPORT_RULE_GOVERNANCE,
        REPORT_RESEARCH_REVIEW,
        REPORT_RESEARCH_WORKFLOW,
        REPORT_RESEARCH_OS,
        REPORT_CLI_UX,
        REPORT_GUI_NAVIGATION,
        REPORT_EXPERIMENT,
        REPORT_REGRESSION,
        REPORT_INTRADAY_REPLAY,
        REPORT_RELEASE,
        REPORT_SAFETY,
        REPORT_DATA_STABILIZATION,
        REPORT_REPLAY_TRAINING,
        # v0.6.0 Stable Release
        REPORT_STABLE_RELEASE_V060,
        REPORT_RELEASE_MANIFEST,
        # v0.6.2 Data Coverage Expansion (optional in full pack)
        REPORT_DATA_COVERAGE,
        # v0.7.0 Research Intelligence (optional in full pack)
        REPORT_RESEARCH_INTELLIGENCE,
        # v0.7.2 Strategy Research Memory (optional in full pack)
        REPORT_STRATEGY_MEMORY,
        # v0.7.3 Backtest-to-Coach Loop (optional in full pack)
        REPORT_BACKTEST_COACH,
        # v0.8.0 Research Intelligence Stable (optional in full pack)
        REPORT_INTELLIGENCE_STABLE,
        # v0.8.2 Backtest Training Metrics (optional in full pack)
        REPORT_TRAINING_METRICS,
        # v0.8.3 Research Intelligence Evidence Graph (optional in full pack)
        REPORT_EVIDENCE_GRAPH,
        # v0.9.0.1 Crash Reversal & Risk Discipline Strategy Pack (optional in full pack)
        REPORT_CRASH_REVERSAL,
        # v0.9.2 Strategy Validation Score (optional in full pack)
        REPORT_STRATEGY_VALIDATION,
        # v0.9.3 Strategy Lab Dashboard (optional in full pack)
        REPORT_STRATEGY_LAB_DASHBOARD,
        # v1.0.0 Research Trading Cockpit Stable (optional in full pack)
        REPORT_RESEARCH_COCKPIT_STABLE,
        # v1.0.2 Data & Report Hygiene (full pack)
        REPORT_DATA_REPORT_HYGIENE,
        # v1.0.3 GUI Stability & Usability Polish (optional in full pack)
        REPORT_GUI_USABILITY,
        # v1.0.4 Regression & Release Gate Hardening (optional in full pack)
        REPORT_REGRESSION_HARDENING,
        # v1.0.5 Documentation & User Guide Polish (optional in full pack)
        REPORT_DOCUMENTATION_HEALTH,
        # v1.0.6 Example Workflows & Templates (optional in full pack)
        REPORT_WORKFLOW_TEMPLATES,
        # v1.0.7 Knowledge Base Search Polish (optional in full pack)
        REPORT_KNOWLEDGE_BASE_SEARCH,
        # v1.0.8 Local Research Assistant Polish (optional in full pack)
        REPORT_LOCAL_RESEARCH_ASSISTANT,
        # v1.0.9 Final Maintenance Rollup (optional in full pack)
        REPORT_FINAL_MAINTENANCE_ROLLUP,
        # v1.1.0 Data Universe Expansion (optional in full pack)
        REPORT_DATA_UNIVERSE_EXPANSION,
        # v1.1.1 Data Import UX & Batch Onboarding (optional in full pack)
        REPORT_DATA_IMPORT_ONBOARDING,
        # v1.1.2 Coverage Repair Workflow (optional in full pack)
        REPORT_COVERAGE_REPAIR,
        # v1.1.3 Data Freshness Monitor (optional in full pack)
        REPORT_DATA_FRESHNESS,
        # v1.1.4 Coverage Quality Gates (optional in full pack)
        REPORT_COVERAGE_QUALITY_GATE,
        # v1.1.5 Quality Gate Enforcement & Audit (optional in full pack)
        REPORT_GATE_ENFORCEMENT_AUDIT,
        REPORT_GATE_RUN_SUMMARY,
        REPORT_GATE_EXCLUSION_SUMMARY,
        REPORT_GATE_REPRODUCIBILITY,
        # v1.1.6 Data Governance Operations Dashboard (optional in full pack)
        REPORT_DATA_GOVERNANCE_OPERATIONS,
        REPORT_GOVERNANCE_ACTION_QUEUE,
        REPORT_GOVERNANCE_MODULE_HEALTH,
        REPORT_GOVERNANCE_AUDIT_SUMMARY,
    ],
}

# Display metadata per pack type
_PACK_META: Dict[str, dict] = {
    PACK_DAILY: {
        "display_name": "Daily Research Pack",
        "description":  "Core daily research reports: market, signals, data quality, portfolio",
        "report_count": len(_PACK_DEFINITIONS[PACK_DAILY]),
    },
    PACK_WEEKLY: {
        "display_name": "Weekly Research Pack",
        "description":  "Weekly review + daily pack: strategy, governance, workflow, OS, CLI/GUI",
        "report_count": len(_PACK_DEFINITIONS[PACK_WEEKLY]),
    },
    PACK_FULL: {
        "display_name": "Full Research Pack",
        "description":  "All 22 report types: weekly + regression, replay, release, safety, stable_release v0.6.0",
        "report_count": len(_PACK_DEFINITIONS[PACK_FULL]),
    },
}


class ReportRegistry:
    """Registry of report pack definitions.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def get_report_types(self, pack_type: str) -> List[str]:
        """Return ordered list of report types for a pack type."""
        return list(_PACK_DEFINITIONS.get(pack_type, []))

    def get_pack_meta(self, pack_type: str) -> dict:
        """Return display metadata for a pack type."""
        return dict(_PACK_META.get(pack_type, {}))

    def list_pack_types(self) -> List[str]:
        """Return all supported pack types."""
        return [PACK_DAILY, PACK_WEEKLY, PACK_FULL, PACK_CUSTOM]

    def pack_type_display(self, pack_type: str) -> str:
        meta = _PACK_META.get(pack_type, {})
        return meta.get("display_name", pack_type.title())
