"""
research_registry.run_classifier — ResearchRunClassifier v1.1.8

Classifies commands into run types, categories, and default qualifications.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ResearchRunClassifier:
    """
    Classifies research command runs by type, category, and qualification.

    [!] Research Only. No Real Orders.
    mock mode → qualification=DEMO_ONLY
    paper/mock-realtime → qualification=DEMO_ONLY
    health checks: configurable registry eligibility (default off)
    """

    COMMAND_TYPE_MAP = {
        "backtest-buy-points": "BACKTEST",
        "backtest-screener": "BACKTEST",
        "backtest-strategy-knowledge": "BACKTEST",
        "validate-score": "VALIDATION",
        "strategy-validation": "VALIDATION",
        "screener": "SCREENER",
        "selector": "SCREENER",
        "stock-report": "REPORT",
        "report-pack": "REPORT",
        "governance-report": "REPORT",
        "strategy-preview": "PREVIEW",
        "feature-preview": "PREVIEW",
        "paper": "PAPER_SIMULATION",
        "mock-realtime": "MOCK_SIMULATION",
    }

    CATEGORY_MAP = {
        "BACKTEST": "RESEARCH",
        "VALIDATION": "RESEARCH",
        "SCREENER": "RESEARCH",
        "REPORT": "REPORTING",
        "PREVIEW": "PREVIEW",
        "GATE_ENFORCEMENT": "DATA_GOVERNANCE",
        "GOVERNANCE": "DATA_GOVERNANCE",
        "GOVERNANCE_ALERTS": "DATA_GOVERNANCE",
        "DATA_IMPORT": "DATA_GOVERNANCE",
        "DATA_REPAIR": "DATA_GOVERNANCE",
        "DATA_FRESHNESS": "DATA_GOVERNANCE",
        "QUALITY_GATE": "DATA_GOVERNANCE",
        "PAPER_SIMULATION": "SIMULATION",
        "MOCK_SIMULATION": "SIMULATION",
        "SYSTEM_HEALTH": "HEALTH",
        "OTHER": "ADMIN",
    }

    # Health check commands — registry eligibility is off by default
    _HEALTH_PREFIXES = [
        "-health", "health-check", "safety-scan", "docs-health-check",
        "gui-health-check", "research-cockpit-stable", "stable-v060-check",
        "intelligence-stable",
    ]

    _GATE_ENFORCEMENT_PREFIXES = ["gate-enforcement-"]

    _GOVERNANCE_CMDS = [
        "governance-dashboard", "governance-summary", "governance-daily-operations",
        "governance-history", "governance-runs",
    ]

    _GOVERNANCE_ALERTS_PREFIXES = [
        "governance-alerts-", "governance-alert-", "governance-digest",
        "governance-checklist", "governance-notification-preview",
    ]

    _DATA_IMPORT_PREFIXES = ["import-", "data-import-", "import-onboarding"]
    _DATA_REPAIR_PREFIXES = ["coverage-repair-"]
    _DATA_FRESHNESS_PREFIXES = ["freshness-"]
    _QUALITY_GATE_PREFIXES = ["quality-gate-"]

    def classify(self, command_name: str) -> str:
        """Return run_type string for the given command name."""
        if not command_name:
            return "OTHER"

        # Exact match first
        if command_name in self.COMMAND_TYPE_MAP:
            return self.COMMAND_TYPE_MAP[command_name]

        # Pattern matching
        for prefix in self._GATE_ENFORCEMENT_PREFIXES:
            if command_name.startswith(prefix):
                return "GATE_ENFORCEMENT"

        if command_name in self._GOVERNANCE_CMDS:
            return "GOVERNANCE"

        for prefix in self._GOVERNANCE_ALERTS_PREFIXES:
            if command_name.startswith(prefix) or command_name == prefix.rstrip("-"):
                return "GOVERNANCE_ALERTS"

        for prefix in self._DATA_IMPORT_PREFIXES:
            if command_name.startswith(prefix):
                return "DATA_IMPORT"

        for prefix in self._DATA_REPAIR_PREFIXES:
            if command_name.startswith(prefix):
                return "DATA_REPAIR"

        for prefix in self._DATA_FRESHNESS_PREFIXES:
            if command_name.startswith(prefix):
                return "DATA_FRESHNESS"

        for prefix in self._QUALITY_GATE_PREFIXES:
            if command_name.startswith(prefix):
                return "QUALITY_GATE"

        for suffix in self._HEALTH_PREFIXES:
            if command_name.endswith(suffix) or command_name == suffix.lstrip("-"):
                return "SYSTEM_HEALTH"

        return "OTHER"

    def category(self, command_name: str) -> str:
        """Return command_category string for the given command name."""
        run_type = self.classify(command_name)
        return self.CATEGORY_MAP.get(run_type, "ADMIN")

    def default_qualification(self, command_name: str, mode: str) -> str:
        """Return default qualification for a command+mode combination."""
        if mode == "mock":
            return "DEMO_ONLY"

        run_type = self.classify(command_name)

        if run_type == "PAPER_SIMULATION":
            return "DEMO_ONLY"
        if run_type == "MOCK_SIMULATION":
            return "DEMO_ONLY"
        if run_type in ("BACKTEST", "VALIDATION"):
            return "OBSERVATIONAL_ONLY"  # Upgraded to FORMALLY_QUALIFIED after gate enforcement
        if run_type == "SCREENER":
            return "OBSERVATIONAL_ONLY"
        if run_type in ("REPORT", "GOVERNANCE", "GOVERNANCE_ALERTS"):
            return "OBSERVATIONAL_ONLY"
        if run_type == "GATE_ENFORCEMENT":
            return "OBSERVATIONAL_ONLY"  # May become FORMALLY_QUALIFIED
        if run_type == "SYSTEM_HEALTH":
            return "OBSERVATIONAL_ONLY"
        if run_type in ("DATA_IMPORT", "DATA_REPAIR", "DATA_FRESHNESS", "QUALITY_GATE"):
            return "OBSERVATIONAL_ONLY"

        return "UNKNOWN"

    def is_registry_eligible(self, command_name: str) -> bool:
        """Return True if the command is eligible for registry recording by default."""
        run_type = self.classify(command_name)

        # Health checks are off by default
        if run_type == "SYSTEM_HEALTH":
            return False

        # Simulation runs are eligible (for tracking purposes)
        return True

    def is_simulation(self, command_name: str) -> bool:
        """Return True if this is a simulation command."""
        run_type = self.classify(command_name)
        return run_type in ("PAPER_SIMULATION", "MOCK_SIMULATION")

    def is_health_run(self, command_name: str) -> bool:
        """Return True if this is a health check command."""
        return self.classify(command_name) == "SYSTEM_HEALTH"
