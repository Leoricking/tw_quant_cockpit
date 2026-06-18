"""
replay/challenge_batch.py — ReplayChallengeBatchRunner v1.2.7

[!] Preview by default. --execute --allow-write required to write.
[!] Cannot: auto-start challenge, auto-submit decision, auto-reveal,
    auto-confirm mistake, auto-complete review, auto-trade.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeBatchRunner:
    """
    Batch challenge generation, validation, and preview.

    [!] Preview by default.
    [!] --execute --allow-write required to write runtime metadata.
    [!] Cannot auto-start challenge, auto-submit decision, auto-reveal,
        auto-confirm mistake, auto-complete review, or auto-trade.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_START_CHALLENGE = False
    AUTO_SUBMIT_DECISION = False
    AUTO_REVEAL = False
    AUTO_CONFIRM_MISTAKE = False
    AUTO_COMPLETE_REVIEW = False
    AUTO_TRADE = False

    def __init__(self) -> None:
        self._items: List[Dict[str, Any]] = []
        self._start_time: Optional[float] = None
        self._current_idx: int = 0

    def generate_preview(self, session_ids: List[str], difficulty: str = "INTERMEDIATE") -> Dict[str, Any]:
        """Preview batch generation (dry-run)."""
        items = []
        for sid in session_ids:
            items.append({
                "challenge_id": f"PREVIEW-{sid[:8]}",
                "source_session": sid,
                "challenge_type": "FREE_DECISION",
                "difficulty": difficulty,
                "operation": "GENERATE_PREVIEW",
                "status": "PREVIEW",
                "warnings": [],
                "errors": [],
            })
        return {
            "status": "PREVIEW",
            "dry_run": True,
            "items": items,
            "total": len(items),
            "execute_required": True,
            "message": "Use --execute --allow-write to generate challenges",
            "research_only": True,
            "no_real_orders": True,
        }

    def run_batch(
        self,
        session_ids: List[str],
        difficulty: str = "INTERMEDIATE",
        execute: bool = False,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Run batch generation. BLOCKED without execute+allow_write."""
        if execute and not allow_write:
            return {
                "status": "BLOCKED",
                "message": "batch-run requires both --execute AND --allow-write",
                "auto_start_challenge": False,
                "auto_submit_decision": False,
                "auto_reveal": False,
                "research_only": True,
            }
        if not execute:
            return self.generate_preview(session_ids, difficulty)

        # Execute mode
        self._start_time = time.monotonic()
        results = []
        completed = 0
        failed = 0
        for idx, sid in enumerate(session_ids):
            item_start = time.monotonic()
            try:
                from replay.challenge_generator import ReplayChallengeGenerator
                gen = ReplayChallengeGenerator()
                defn = gen.generate_from_session(sid, difficulty=difficulty)
                elapsed = time.monotonic() - item_start
                results.append({
                    "challenge_id": defn.get("challenge_id"),
                    "source_session": sid,
                    "operation": "GENERATED",
                    "started_at": "",
                    "finished_at": "",
                    "elapsed": round(elapsed, 2),
                    "status": "SUCCESS",
                    "warnings": [],
                    "errors": [],
                })
                completed += 1
            except Exception as exc:
                elapsed = time.monotonic() - item_start
                results.append({
                    "source_session": sid,
                    "operation": "GENERATE",
                    "elapsed": round(elapsed, 2),
                    "status": "FAILED",
                    "errors": [str(exc)],
                })
                failed += 1

        total_elapsed = time.monotonic() - (self._start_time or time.monotonic())
        avg_elapsed = total_elapsed / len(session_ids) if session_ids else 0.0

        return {
            "status": "COMPLETED",
            "items": results,
            "total": len(session_ids),
            "completed": completed,
            "failed": failed,
            "skipped": 0,
            "cancelled": 0,
            "total_elapsed": round(total_elapsed, 2),
            "average_per_item": round(avg_elapsed, 2),
            "estimated_remaining": 0.0,
            "auto_start_challenge": False,
            "auto_submit_decision": False,
            "auto_reveal": False,
            "auto_confirm_mistake": False,
            "auto_complete_review": False,
            "auto_trade": False,
            "research_only": True,
            "no_real_orders": True,
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "runner": "ReplayChallengeBatchRunner",
            "preview_by_default": True,
            "auto_start_challenge": False,
            "auto_submit_decision": False,
            "auto_reveal": False,
            "auto_confirm_mistake": False,
            "auto_complete_review": False,
            "auto_trade": False,
            "research_only": True,
            "no_real_orders": True,
        }
