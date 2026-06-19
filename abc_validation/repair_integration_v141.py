"""
abc_validation/repair_integration_v141.py — Repair integration for A/B/C validation v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Creates repair candidates for data issues but defaults to create_repair_tasks=False.
No auto repair, no auto refresh, no auto download, no mock fallback.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ABCRepairIntegration:
    """
    Creates repair candidates for data issues found during A/B/C validation.

    Defaults: create_repair_tasks=False, no auto repair, no auto refresh,
    no auto download, no mock fallback.
    Uses CoverageRepairQueue dedup.
    """

    def __init__(self, create_repair_tasks: bool = False):
        self.create_repair_tasks = create_repair_tasks
        # Safety flags
        self.auto_repair_enabled = False
        self.auto_refresh_enabled = False
        self.auto_download_enabled = False
        self.mock_fallback_enabled = False

    def identify_repair_candidates(self, blocked_signals: List[dict]) -> List[dict]:
        """Identify data repair candidates from blocked/insufficient signals."""
        candidates = []
        seen = set()  # dedup

        for sig in blocked_signals:
            symbol = sig.get("symbol", "")
            signal_date = sig.get("signal_date", "")
            issues = sig.get("integrity_issues", [])

            for issue in issues:
                key = f"{symbol}:{signal_date}:{issue}"
                if key in seen:
                    continue
                seen.add(key)

                candidates.append({
                    "symbol": symbol,
                    "signal_date": signal_date,
                    "issue_type": issue,
                    "repair_type": self._classify_repair_type(issue),
                    "priority": self._classify_priority(issue),
                    "auto_repair": False,
                    "auto_refresh": False,
                    "auto_download": False,
                    "mock_fallback": False,
                    "source": "abc_validation_v141",
                })

        return candidates

    def create_candidates(
        self,
        blocked_signals: List[dict],
    ) -> Dict[str, Any]:
        """
        Create repair candidate records.

        If create_repair_tasks=False (default): returns candidates without creating tasks.
        If create_repair_tasks=True: creates tasks in CoverageRepairQueue.
        """
        candidates = self.identify_repair_candidates(blocked_signals)

        if not self.create_repair_tasks:
            return {
                "candidates": candidates,
                "tasks_created": 0,
                "create_repair_tasks": False,
                "note": "create_repair_tasks=False — no tasks created. Use --execute to create.",
                "auto_repair_enabled": False,
                "auto_refresh_enabled": False,
                "auto_download_enabled": False,
                "mock_fallback_enabled": False,
                "no_real_orders": True,
            }

        # Only create tasks if explicitly enabled
        tasks_created = 0
        task_errors = []
        for candidate in candidates:
            try:
                from coverage_repair.repair_queue import CoverageRepairQueue
                queue = CoverageRepairQueue()
                queue.add(candidate)
                tasks_created += 1
            except ImportError:
                task_errors.append("CoverageRepairQueue not available")
                break
            except Exception as e:
                task_errors.append(str(e))

        return {
            "candidates": candidates,
            "tasks_created": tasks_created,
            "create_repair_tasks": True,
            "errors": task_errors,
            "auto_repair_enabled": False,
            "auto_refresh_enabled": False,
            "auto_download_enabled": False,
            "mock_fallback_enabled": False,
            "no_real_orders": True,
        }

    def _classify_repair_type(self, issue: str) -> str:
        if "HISTORY" in issue or "BASELINE" in issue:
            return "FETCH_HISTORICAL_DATA"
        if "VOLUME" in issue:
            return "FETCH_VOLUME_DATA"
        if "TIMESTAMP" in issue:
            return "VERIFY_DATA_TIMESTAMPS"
        if "STALE" in issue:
            return "REFRESH_STALE_DATA"
        if "CORPORATE_ACTION" in issue:
            return "VERIFY_CORPORATE_ACTIONS"
        return "GENERIC_DATA_REPAIR"

    def _classify_priority(self, issue: str) -> str:
        if "LOOKAHEAD" in issue or "TIMESTAMP_ORDER" in issue:
            return "HIGH"
        if "STALE" in issue or "CORPORATE_ACTION" in issue:
            return "MEDIUM"
        return "LOW"
