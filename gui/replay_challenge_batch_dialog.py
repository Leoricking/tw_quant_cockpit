"""
gui/replay_challenge_batch_dialog.py — Challenge batch dialog v1.2.7

Shows: Total Elapsed, Current Item Elapsed, Average Per Item, ETA,
Completed/Total, Success/Failed/Skipped/Cancelled.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeBatchDialog:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_START_CHALLENGE = False
    AUTO_SUBMIT_DECISION = False
    AUTO_REVEAL = False
    def get_progress_display(self, batch_result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "total_elapsed": batch_result.get("total_elapsed", 0.0),
            "current_item_elapsed": 0.0,
            "average_per_item": batch_result.get("average_per_item", 0.0),
            "eta": 0.0,
            "completed": batch_result.get("completed", 0),
            "total": batch_result.get("total", 0),
            "success": batch_result.get("completed", 0),
            "failed": batch_result.get("failed", 0),
            "skipped": batch_result.get("skipped", 0),
            "cancelled": batch_result.get("cancelled", 0),
            "auto_start_challenge": False,
            "auto_submit_decision": False,
            "auto_reveal": False,
            "research_only": True,
        }
