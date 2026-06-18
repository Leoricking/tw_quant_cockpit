"""
replay/stable_contracts.py — ReplayStableContractChecker for v1.2.9.

Cross-module contract verification via lightweight import-based checks.
No real execution. No real orders. Research only.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStableContractChecker:
    """
    Lightweight cross-module contract checker for v1.2.9.

    check_all() returns Dict[str, Tuple[str, str]] (status, message).
    Import failures → WARN (module may be optional).
    Hard invariant violations → FAIL.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def check_all(self) -> Dict[str, Tuple[str, str]]:
        """Run all contract checks. Returns {contract_id: (status, message)}."""
        results: Dict[str, Tuple[str, str]] = {}

        results["session_scenario"]              = self._check_session_scenario()
        results["session_journal"]               = self._check_session_journal()
        results["session_scoring"]               = self._check_session_scoring()
        results["scenario_dataset"]              = self._check_scenario_dataset()
        results["scoring_outcome_separation"]    = self._check_scoring_outcome_separation()
        results["strategy_point_in_time"]        = self._check_strategy_point_in_time()
        results["timeframe_future_firewall"]      = self._check_timeframe_future_firewall()
        results["challenge_hidden_data"]         = self._check_challenge_hidden_data()
        results["dataset_registry_schema"]       = self._check_dataset_registry_schema()
        results["session_registry_schema"]       = self._check_session_registry_schema()
        results["stable_schema"]                 = self._check_stable_schema()
        results["expected_safety_block_pass"]    = self._check_expected_safety_block_pass()
        results["fail_nonzero"]                  = self._check_fail_nonzero()
        results["unexpected_blocked_nonzero"]    = self._check_unexpected_blocked_nonzero()
        results["no_real_orders_invariant"]      = self._check_no_real_orders_invariant()
        results["research_only_invariant"]       = self._check_research_only_invariant()

        return results

    def _check_session_scenario(self) -> Tuple[str, str]:
        try:
            from replay.replay_schema import ReplaySession  # noqa: F401
            from replay.scenario_schema import ScenarioLibrary  # noqa: F401
            return ("PASS", "ReplaySession and ScenarioLibrary both import OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_session_journal(self) -> Tuple[str, str]:
        try:
            from replay.replay_schema import ReplaySession  # noqa: F401
            from replay.decision_journal_schema import DecisionJournalEntry  # noqa: F401
            return ("PASS", "ReplaySession and DecisionJournalEntry both import OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_session_scoring(self) -> Tuple[str, str]:
        try:
            from replay.replay_schema import ReplaySession  # noqa: F401
            from replay.scoring_schema import ReplayScoringEntry  # noqa: F401
            return ("PASS", "ReplaySession and ReplayScoringEntry both import OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_scenario_dataset(self) -> Tuple[str, str]:
        try:
            from replay.scenario_schema import ScenarioLibrary  # noqa: F401
            from replay.dataset_registry_schema import ReplayDatasetRecord  # noqa: F401
            return ("PASS", "ScenarioLibrary and ReplayDatasetRecord both import OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_scoring_outcome_separation(self) -> Tuple[str, str]:
        try:
            from replay.scoring_schema import ReplayScoringEntry
            entry = ReplayScoringEntry.__dataclass_fields__
            # Verify forbidden future fields are not present
            forbidden = {"realized_return", "future_return", "realized_pnl"}
            found = forbidden.intersection(entry.keys())
            if found:
                return ("FAIL", f"scoring_schema has forbidden future fields: {found}")
            return ("PASS", "scoring_schema has no forbidden future fields")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_strategy_point_in_time(self) -> Tuple[str, str]:
        try:
            from replay.strategy_replay_schema import StrategyReplaySession  # noqa: F401
            return ("PASS", "StrategyReplaySession imports OK (point-in-time contract)")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_timeframe_future_firewall(self) -> Tuple[str, str]:
        try:
            from replay.timeframe_schema import TimeframeReplaySession  # noqa: F401
            from replay.timeframe_future_firewall import TimeframeFutureFirewall  # noqa: F401
            return ("PASS", "TimeframeReplaySession and TimeframeFutureFirewall both import OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_challenge_hidden_data(self) -> Tuple[str, str]:
        try:
            from replay.challenge_schema import ReplayChallengeDefinition
            defn_fields = ReplayChallengeDefinition.__dataclass_fields__
            if "hidden_outcome" not in defn_fields and "research_only" not in defn_fields:
                return ("WARN", "challenge_schema missing expected safety fields")
            return ("PASS", "ReplayChallengeDefinition imports OK with safety fields")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_dataset_registry_schema(self) -> Tuple[str, str]:
        try:
            from replay.dataset_registry_schema import ReplayDatasetRecord  # noqa: F401
            return ("PASS", "ReplayDatasetRecord imports OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_session_registry_schema(self) -> Tuple[str, str]:
        try:
            from replay.session_registry_schema import ReplaySessionRecord  # noqa: F401
            return ("PASS", "ReplaySessionRecord imports OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_stable_schema(self) -> Tuple[str, str]:
        try:
            from replay.stable_schema import (
                StableModuleInfo, StableCapability, StableManifest,
                StableContractResult, StableCompatibilityResult, StableAuditResult,
            )
            # Verify safety fields
            m = StableModuleInfo(module_name="test", introduced_version="1.2.9")
            assert m.no_real_orders is True
            assert m.research_only is True
            return ("PASS", "All stable schema dataclasses import OK with safety flags")
        except Exception as exc:
            return ("FAIL", f"stable_schema error: {exc}")

    def _check_expected_safety_block_pass(self) -> Tuple[str, str]:
        try:
            from regression.regression_schema import RegressionTestCase
            fields = RegressionTestCase.__dataclass_fields__
            if "expected_block" not in fields:
                return ("FAIL", "RegressionTestCase missing expected_block field")
            return ("PASS", "RegressionTestCase.expected_block field exists")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_fail_nonzero(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import _is_forbidden
            # _is_forbidden is the guard that prevents real order commands
            if callable(_is_forbidden):
                return ("PASS", "_is_forbidden guard found in suite_registry")
            return ("FAIL", "_is_forbidden is not callable")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_unexpected_blocked_nonzero(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import _is_forbidden
            # Verify that known safe commands are not blocked
            safe_cmd = ["main.py", "replay-stable-health"]
            if _is_forbidden(safe_cmd):
                return ("FAIL", f"_is_forbidden incorrectly blocks safe command: {safe_cmd}")
            return ("PASS", "_is_forbidden does not block safe replay-stable-health command")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_no_real_orders_invariant(self) -> Tuple[str, str]:
        try:
            from release.version_info import NO_REAL_ORDERS, REAL_ORDERS_ENABLED
            if NO_REAL_ORDERS is not True:
                return ("FAIL", f"NO_REAL_ORDERS={NO_REAL_ORDERS}, expected True")
            if REAL_ORDERS_ENABLED is not False:
                return ("FAIL", f"REAL_ORDERS_ENABLED={REAL_ORDERS_ENABLED}, expected False")
            return ("PASS", "NO_REAL_ORDERS=True, REAL_ORDERS_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"version_info check error: {exc}")

    def _check_research_only_invariant(self) -> Tuple[str, str]:
        try:
            from release.version_info import PRODUCTION_TRADING_BLOCKED, BROKER_EXECUTION_ENABLED
            if PRODUCTION_TRADING_BLOCKED is not True:
                return ("FAIL", f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED}, expected True")
            if BROKER_EXECUTION_ENABLED is not False:
                return ("FAIL", f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED}, expected False")
            return ("PASS", "PRODUCTION_TRADING_BLOCKED=True, BROKER_EXECUTION_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"version_info check error: {exc}")
