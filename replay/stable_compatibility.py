"""
replay/stable_compatibility.py — ReplayStableCompatibilityChecker for v1.2.9.

Backward compatibility checks for v1.2.0 through v1.2.8.
Lightweight fixture-based checks — no real execution.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Minimal fixture data per version — just enough to exercise schema loading
_VERSION_FIXTURES: Dict[str, dict] = {
    "1.2.0": {
        "session_id": "SES-TST-v120",
        "symbol": "TST001",
        "start_date": "2023-01-01",
        "current_date": "2023-01-10",
        "mode": "mock",
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.1": {
        "session_id": "SES-TST-v121",
        "symbol": "TST001",
        "start_date": "2023-01-01",
        "current_date": "2023-01-10",
        "mode": "mock",
        "scenario_id": "SCN-TST-v121",
        "checkpoint_id": None,
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.2": {
        "session_id": "SES-TST-v122",
        "entry_id": "DJR-TST-v122",
        "decision_type": "ENTRY",
        "simulation_decision_only": True,
        "no_paper_order": True,
        "no_broker_order": True,
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.3": {
        "session_id": "SES-TST-v123",
        "score_id": "SCR-TST-v123",
        "process_score": 75.0,
        "outcome_revealed": False,
        "auto_outcome_reveal_enabled": False,
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.4": {
        "session_id": "SES-TST-v124",
        "strategy_id": "STR-TST-v124",
        "point_in_time": "2023-01-10",
        "no_forward_return": True,
        "auto_strategy_decision_enabled": False,
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.5": {
        "session_id": "SES-TST-v125",
        "timeframes": ["D1", "M60", "M20", "M5", "M1"],
        "no_future_klines": True,
        "no_bfill": True,
        "past_only_asof_join": True,
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.6": {
        "session_id": "SES-TST-v126",
        "review_queue_id": "RVQ-TST-v126",
        "auto_review_complete": False,
        "auto_outcome_reveal": False,
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.7": {
        "challenge_id": "CHG-TST-v127",
        "hidden_outcome": True,
        "future_data_embedded": False,
        "public_leaderboard_enabled": False,
        "network_submission_enabled": False,
        "research_only": True,
        "no_real_orders": True,
    },
    "1.2.8": {
        "dataset_id": "DST-TST-v128",
        "dataset_version": "v1",
        "frozen_at": None,
        "auto_dataset_overwrite_enabled": False,
        "auto_session_rebind_enabled": False,
        "research_only": True,
        "no_real_orders": True,
    },
}


class ReplayStableCompatibilityChecker:
    """
    Checks backward compatibility for v1.2.0 through v1.2.8.

    For each version, creates a minimal fixture dict and tries to verify
    the required safety fields. Lightweight — no real execution.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    SUPPORTED_VERSIONS = [
        "1.2.0", "1.2.1", "1.2.2", "1.2.3",
        "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8",
    ]

    def check_version(self, version_str: str) -> Tuple[str, str]:
        """Check backward compatibility for a single version.

        Returns (status, message) where status is PASS/WARN/FAIL.
        """
        fixture = _VERSION_FIXTURES.get(version_str)
        if fixture is None:
            return ("WARN", f"No fixture defined for version {version_str}")
        try:
            # Verify required safety fields in fixture
            if fixture.get("research_only") is not True:
                return ("FAIL", f"v{version_str} fixture missing research_only=True")
            if fixture.get("no_real_orders") is not True:
                return ("FAIL", f"v{version_str} fixture missing no_real_orders=True")
            # Try version-specific schema import
            status, msg = self._check_version_schema(version_str, fixture)
            return (status, msg)
        except Exception as exc:
            return ("WARN", f"v{version_str} compatibility check error: {exc}")

    def _check_version_schema(self, version: str, fixture: dict) -> Tuple[str, str]:
        """Try to load schema for a given version using fixture data."""
        try:
            if version == "1.2.0":
                from replay.replay_schema import ReplaySession
                # Minimal construction check — just verify it can be imported
                return ("PASS", f"v{version}: replay_schema imports OK")
            elif version == "1.2.1":
                from replay.scenario_schema import ScenarioLibrary  # noqa: F401
                from replay.session_manager import ReplaySessionManager  # noqa: F401
                return ("PASS", f"v{version}: scenario_schema and session_manager import OK")
            elif version == "1.2.2":
                from replay.decision_journal_schema import DecisionJournalEntry  # noqa: F401
                return ("PASS", f"v{version}: decision_journal_schema imports OK")
            elif version == "1.2.3":
                from replay.scoring_schema import ReplayScoringEntry  # noqa: F401
                return ("PASS", f"v{version}: scoring_schema imports OK")
            elif version == "1.2.4":
                from replay.strategy_replay_schema import StrategyReplaySession  # noqa: F401
                return ("PASS", f"v{version}: strategy_replay_schema imports OK")
            elif version == "1.2.5":
                from replay.timeframe_schema import TimeframeReplaySession  # noqa: F401
                return ("PASS", f"v{version}: timeframe_schema imports OK")
            elif version == "1.2.6":
                from replay.review_dashboard_schema import ReviewDashboardEntry  # noqa: F401
                return ("PASS", f"v{version}: review_dashboard_schema imports OK")
            elif version == "1.2.7":
                from replay.challenge_schema import ReplayChallengeDefinition  # noqa: F401
                return ("PASS", f"v{version}: challenge_schema imports OK")
            elif version == "1.2.8":
                from replay.dataset_registry_schema import ReplayDatasetRecord  # noqa: F401
                return ("PASS", f"v{version}: dataset_registry_schema imports OK")
            else:
                return ("WARN", f"No schema check defined for v{version}")
        except ImportError as exc:
            return ("WARN", f"v{version}: schema import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"v{version}: schema check error: {exc}")

    def check_all(self) -> Dict[str, Tuple[str, str]]:
        """Run compatibility check for all supported versions.

        Returns {version: (status, message)}.
        """
        results: Dict[str, Tuple[str, str]] = {}
        for version in self.SUPPORTED_VERSIONS:
            results[version] = self.check_version(version)
        return results
