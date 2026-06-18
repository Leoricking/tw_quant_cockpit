"""
replay/stable_manifest.py — ReplayStableManifest for v1.2.9 Stable Rollup.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
[!] Manifest contains no absolute paths, no secrets, no usernames.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStableManifest:
    """
    Generates the v1.2.9 stable release manifest dict.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] No absolute paths. No secrets. No usernames.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    MODULES = [
        "replay_foundation",
        "scenario_manager",
        "session_manager",
        "decision_journal",
        "scoring_mistake_taxonomy",
        "strategy_knowledge",
        "multi_timeframe",
        "review_dashboard",
        "challenge_mode",
        "dataset_registry",
        "session_registry",
        "stable_rollup",
    ]

    CAPABILITIES = [
        "replay_session_step",
        "scenario_library",
        "session_fork_checkpoint",
        "decision_journal",
        "process_outcome_scoring",
        "mistake_taxonomy",
        "strategy_replay",
        "multi_timeframe_sync",
        "review_queue",
        "challenge_mode",
        "challenge_personal_leaderboard",
        "dataset_registry",
        "session_registry",
        "stable_health_check",
        "stable_manifest",
        "capability_matrix",
    ]

    CLI_COMMANDS = [
        "replay-health",
        "replay-scenario-health",
        "replay-session-manager-health",
        "replay-journal-health",
        "replay-scoring-health",
        "replay-strategy-health",
        "replay-timeframe-health",
        "replay-review-health",
        "replay-challenge-health",
        "replay-registry-health",
        "replay-stable-health",
        "replay-stable-summary",
        "replay-stable-manifest",
        "replay-stable-capabilities",
        "replay-stable-contracts",
        "replay-stable-compatibility",
        "replay-stable-store-audit",
        "replay-stable-runtime-audit",
        "replay-stable-cli-audit",
        "replay-stable-gui-audit",
        "replay-stable-report-audit",
        "replay-stable-safety-audit",
        "replay-stable-regression-audit",
        "replay-stable-report",
    ]

    HEALTH_CHECKS = [
        "replay_foundation",
        "scenario_manager",
        "session_manager",
        "decision_journal",
        "scoring",
        "strategy",
        "timeframe",
        "review",
        "challenge",
        "dataset_registry",
        "session_registry",
        "stable_manifest",
        "capability_matrix",
        "contracts",
        "backward_compatibility",
        "store_audit",
        "runtime_isolation",
        "cli_audit",
        "gui_audit",
        "report_audit",
        "safety_audit",
        "regression_audit",
        "release_gate",
    ]

    STORE_PATHS = [
        "data/replay_sessions/",
        "data/replay_scenarios/",
        "data/replay_journal/",
        "data/replay_scoring/",
        "data/replay_strategy/",
        "data/replay_timeframes/",
        "data/replay_review/",
        "data/replay_challenges/",
        "data/replay_registry/",
        "data/replay_stable/",
    ]

    REPORT_TYPES = [
        "replay_training_stable_rollup",
        "replay_scoring_report",
        "replay_challenge_report",
        "replay_registry_report",
        "replay_review_report",
        "replay_strategy_report",
        "replay_timeframe_report",
        "replay_journal_report",
        "replay_session_report",
        "replay_scenario_report",
    ]

    GUI_TABS = [
        "replay_training",
        "replay_scenario_library",
        "replay_session_manager",
        "replay_decision_journal",
        "replay_scoring",
        "replay_strategy_knowledge",
        "replay_multi_timeframe",
        "replay_review_dashboard",
        "replay_challenge",
        "replay_registry",
        "replay_stable",
    ]

    BACKWARD_COMPATIBILITY_RANGE = [
        "1.2.0", "1.2.1", "1.2.2", "1.2.3",
        "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8",
    ]

    SCHEMA_VERSIONS = {
        "replay_schema": "1.2.0",
        "scenario_schema": "1.2.1",
        "session_schema": "1.2.1",
        "decision_journal_schema": "1.2.2",
        "scoring_schema": "1.2.3",
        "strategy_replay_schema": "1.2.4",
        "timeframe_schema": "1.2.5",
        "review_dashboard_schema": "1.2.6",
        "challenge_schema": "1.2.7",
        "dataset_registry_schema": "1.2.8",
        "session_registry_schema": "1.2.8",
        "stable_schema": "1.2.9",
    }

    KNOWN_WARNINGS = [
        "PySide6 optional — GUI panels degrade gracefully without it",
        "Real data required for FORMAL qualification — mock data gates BLOCKED",
        "Outcome reveal requires explicit user action — AUTO_OUTCOME_REVEAL_ENABLED=False",
        "Mistake confirmation requires explicit user action — AUTO_MISTAKE_CONFIRMATION_ENABLED=False",
        "Public leaderboard disabled — local personal records only",
        "Auto session rebind disabled — manual rebind required",
        "Auto dataset repair disabled — manual repair required",
    ]

    def build(self) -> Dict[str, Any]:
        """Build and return the stable manifest dict.

        [!] No absolute paths. No secrets. No usernames.
        """
        return {
            "release_version": "1.2.9",
            "release_name": "Replay Training Stable Rollup",
            "base_release": "1.2.8 Replay Dataset & Session Registry",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "modules": self.MODULES,
            "module_count": len(self.MODULES),
            "capabilities": self.CAPABILITIES,
            "capability_count": len(self.CAPABILITIES),
            "safety_flags": {
                "no_real_orders": True,
                "broker_disabled": True,
                "research_only": True,
                "production_trading_blocked": True,
                "validated_does_not_enable_trading": True,
                "auto_replay_decision_enabled": False,
                "auto_replay_execution_enabled": False,
                "auto_mistake_confirmation_enabled": False,
                "auto_outcome_reveal_enabled": False,
                "auto_strategy_change_enabled": False,
                "auto_dataset_repair_enabled": False,
                "auto_session_rebind_enabled": False,
                "replay_trade_execution_enabled": False,
            },
            "CLI_commands": self.CLI_COMMANDS,
            "cli_command_count": len(self.CLI_COMMANDS),
            "health_checks": self.HEALTH_CHECKS,
            "schema_versions": self.SCHEMA_VERSIONS,
            "store_paths": self.STORE_PATHS,
            "store_count": len(self.STORE_PATHS),
            "report_types": self.REPORT_TYPES,
            "report_count": len(self.REPORT_TYPES),
            "GUI_tabs": self.GUI_TABS,
            "gui_tab_count": len(self.GUI_TABS),
            "backward_compatibility_range": self.BACKWARD_COMPATIBILITY_RANGE,
            "known_warnings": self.KNOWN_WARNINGS,
            "no_real_orders": True,
            "broker_disabled": True,
            "research_only": True,
            "stable_rollup": True,
            "replay_training_line_complete": True,
            "long_term_maintenance_ready": True,
        }
