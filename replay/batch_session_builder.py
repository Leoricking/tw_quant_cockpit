"""
replay/batch_session_builder.py — ReplayBatchSessionBuilder v1.2.1

Builds multiple sessions from a scenario.
Default: preview/dry-run.
Requires explicit allow_write=True to create sessions.
Max sessions default 50, hard limit 500.
Does NOT auto-play, auto-decide, auto-score, auto-execute, auto-download.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Batch execution BLOCKED without allow_write=True.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayBatchSessionBuilder:
    """
    Builds multiple sessions from a scenario.
    Default: preview/dry-run.
    Requires explicit allow_write=True to create sessions.
    Max sessions default 50, hard limit 500.
    Does NOT auto-play, auto-decide, auto-score, auto-execute, auto-download.
    """

    DEFAULT_MAX_SESSIONS = 50
    HARD_MAX_SESSIONS = 500
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, session_manager=None, scenario_lib=None, repo_root=None):
        self._session_manager = session_manager
        self._scenario_lib = scenario_lib
        self._repo_root = repo_root or "."

    def preview_batch(
        self, scenario_id: str, symbols: List[str],
        date_ranges: Optional[List[Tuple[str, str]]] = None,
        max_sessions: int = DEFAULT_MAX_SESSIONS,
    ) -> Dict[str, Any]:
        """Preview batch without writing any sessions."""
        count = self.estimate_count(scenario_id, symbols, date_ranges)
        if count > self.HARD_MAX_SESSIONS:
            return {
                "ok": False,
                "blocked": True,
                "reason": f"Requested {count} sessions exceeds hard limit {self.HARD_MAX_SESSIONS}",
                "estimated_count": count,
                "dry_run": True,
            }
        if count > max_sessions:
            return {
                "ok": False,
                "blocked": True,
                "reason": f"Requested {count} sessions exceeds max_sessions={max_sessions}",
                "estimated_count": count,
                "dry_run": True,
            }
        sessions_plan = self._build_plan(scenario_id, symbols, date_ranges, max_sessions)
        return {
            "ok": True,
            "dry_run": True,
            "scenario_id": scenario_id,
            "symbols": symbols,
            "estimated_count": count,
            "sessions_plan": sessions_plan,
            "allow_write": False,
            "note": "Preview only. Use allow_write=True to create sessions.",
            "research_only": True,
            "no_real_orders": True,
        }

    def build_from_scenario(
        self, scenario_id: str, symbols: Optional[List[str]] = None,
        date_ranges: Optional[List[Tuple[str, str]]] = None,
        allow_write: bool = False,
        max_sessions: int = DEFAULT_MAX_SESSIONS,
    ) -> Dict[str, Any]:
        """Build sessions from scenario. BLOCKED without allow_write=True."""
        if not allow_write:
            preview = self.preview_batch(scenario_id, symbols or [], date_ranges, max_sessions)
            preview["blocked_reason"] = "allow_write=False. Use --allow-write to create sessions."
            preview["blocked"] = True
            return preview

        count = self.estimate_count(scenario_id, symbols or [], date_ranges)
        if count > self.HARD_MAX_SESSIONS:
            return {"ok": False, "blocked": True, "reason": f"Count {count} exceeds hard limit {self.HARD_MAX_SESSIONS}"}
        if count > max_sessions:
            return {"ok": False, "blocked": True, "reason": f"Count {count} exceeds max_sessions={max_sessions}"}

        plan = self._build_plan(scenario_id, symbols or [], date_ranges, max_sessions)
        return self.execute_batch(plan, allow_write=allow_write)

    def build_free_practice_batch(
        self, symbols: List[str], start_date: str, end_date: str,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Build free practice sessions. BLOCKED without allow_write=True."""
        if not allow_write:
            return {
                "ok": False,
                "blocked": True,
                "reason": "allow_write=False. Use --allow-write to create sessions.",
                "dry_run": True,
            }
        if len(symbols) > self.DEFAULT_MAX_SESSIONS:
            return {"ok": False, "blocked": True, "reason": f"Symbols count {len(symbols)} exceeds default max {self.DEFAULT_MAX_SESSIONS}"}

        results = []
        for sym in symbols:
            if self._session_manager:
                try:
                    result = self._session_manager.create_free_practice(sym, start_date, end_date)
                    results.append({"symbol": sym, "ok": True, "session_id": getattr(result, "session_id", None)})
                except Exception as exc:
                    results.append({"symbol": sym, "ok": False, "error": str(exc)})
            else:
                results.append({"symbol": sym, "ok": False, "error": "session_manager not available"})

        return {"ok": True, "results": results, "allow_write": True, "research_only": True}

    def validate_batch(
        self, scenario_id: str, symbols: List[str],
        date_ranges: Optional[List[Tuple[str, str]]] = None,
    ) -> Dict[str, Any]:
        errors = []
        if not scenario_id:
            errors.append("scenario_id required")
        if not symbols:
            errors.append("symbols list is empty")
        count = self.estimate_count(scenario_id, symbols, date_ranges)
        if count > self.HARD_MAX_SESSIONS:
            errors.append(f"Estimated count {count} exceeds hard limit {self.HARD_MAX_SESSIONS}")
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "estimated_count": count,
        }

    def estimate_count(
        self, scenario_id: str, symbols: List[str],
        date_ranges: Optional[List[Tuple[str, str]]] = None,
    ) -> int:
        if not date_ranges:
            return len(symbols)
        return len(symbols) * len(date_ranges)

    def _build_plan(
        self, scenario_id: str, symbols: List[str],
        date_ranges: Optional[List[Tuple[str, str]]] = None,
        max_sessions: int = DEFAULT_MAX_SESSIONS,
    ) -> List[Dict[str, Any]]:
        plan = []
        if not date_ranges:
            for sym in symbols:
                if len(plan) >= max_sessions:
                    break
                plan.append({"scenario_id": scenario_id, "symbol": sym, "start_date": None, "end_date": None})
        else:
            for sym in symbols:
                for (start, end) in date_ranges:
                    if len(plan) >= max_sessions:
                        break
                    plan.append({"scenario_id": scenario_id, "symbol": sym, "start_date": start, "end_date": end})
        return plan

    def execute_batch(self, plan: List[Dict[str, Any]], allow_write: bool = False) -> Dict[str, Any]:
        """Execute batch plan. BLOCKED if not allow_write."""
        if not allow_write:
            return {
                "ok": False,
                "blocked": True,
                "reason": "execute_batch requires allow_write=True",
                "plan_count": len(plan),
            }
        results = []
        for item in plan:
            if self._session_manager:
                try:
                    session = self._session_manager.create_from_scenario(
                        item["scenario_id"], item["symbol"],
                        start_date=item.get("start_date"),
                        end_date=item.get("end_date"),
                    )
                    sid = getattr(session, "session_id", None)
                    results.append({"ok": True, "session_id": sid, **item})
                except Exception as exc:
                    results.append({"ok": False, "error": str(exc), **item})
            else:
                results.append({"ok": False, "error": "session_manager not available", **item})

        return {
            "ok": True,
            "allow_write": True,
            "executed": len([r for r in results if r.get("ok")]),
            "failed": len([r for r in results if not r.get("ok")]),
            "results": results,
            "research_only": True,
            "no_real_orders": True,
        }

    def batch_summary(self, results: Dict[str, Any]) -> str:
        if not results.get("ok"):
            return f"Batch BLOCKED: {results.get('reason', results.get('blocked_reason', 'unknown'))}"
        lines = [
            f"Batch Summary: {results.get('executed', 0)} created, {results.get('failed', 0)} failed",
            f"  allow_write: {results.get('allow_write', False)}",
            f"  [!] Research Only | No Real Orders",
        ]
        return "\n".join(lines)
