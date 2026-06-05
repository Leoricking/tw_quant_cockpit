"""research_intelligence/priority_planner.py — ResearchPriorityPlanner v0.7.0.

Builds P0/P1/P2/P3 priority board from signals and recommendations.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
"""
from __future__ import annotations

import logging
from typing import Dict, List

from research_intelligence.research_intelligence_schema import (
    ResearchSignal, ResearchRecommendation,
    PRI_P0, PRI_P1, PRI_P2, PRI_P3,
    ACT_RUN_REGRESSION, ACT_FIX_DATA, ACT_GENERATE_REPORT,
    ACT_PRACTICE_REPLAY, ACT_REVIEW_JOURNAL, ACT_REVIEW_RULE,
    ACT_RUN_BACKTEST, ACT_READ_REPORT,
)

logger = logging.getLogger(__name__)

_P0_DESC = "必修：不處理會影響系統可信度"
_P1_DESC = "高優先：影響策略/復盤品質"
_P2_DESC = "中優先：研究效率改善"
_P3_DESC = "低優先：optional polish"


class ResearchPriorityPlanner:
    """Builds a prioritised research board from signals and recommendations.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def build_priority_board(
        self,
        signals: List[ResearchSignal],
        recommendations: List[ResearchRecommendation],
    ) -> Dict[str, list]:
        """Return board dict keyed P0/P1/P2/P3 with priority items."""
        board: Dict[str, list] = {PRI_P0: [], PRI_P1: [], PRI_P2: [], PRI_P3: []}

        # Build from recommendations (already ranked)
        for rec in recommendations:
            item = self._rec_to_board_item(rec, signals)
            pri = rec.priority if rec.priority in board else PRI_P3
            board[pri].append(item)

        # Ensure P0 signals without recommendations are included
        for sig in signals:
            if sig.priority == PRI_P0:
                # Check if already covered
                covered = any(
                    sig.signal_id in " ".join(str(v) for v in item.values())
                    for item in board[PRI_P0]
                )
                if not covered:
                    board[PRI_P0].append({
                        "title":    sig.title,
                        "why":      sig.description or sig.evidence,
                        "evidence": sig.evidence,
                        "action":   sig.suggested_action,
                        "command":  sig.suggested_command,
                        "module":   sig.source_module,
                        "due_hint": "Immediately",
                        "priority": PRI_P0,
                    })

        return board

    def summarize_priority(self, board: Dict[str, list]) -> dict:
        """Return a summary dict of priority board counts and top item."""
        p0 = board.get(PRI_P0, [])
        p1 = board.get(PRI_P1, [])
        p2 = board.get(PRI_P2, [])
        p3 = board.get(PRI_P3, [])

        top = ""
        for items in (p0, p1, p2, p3):
            if items:
                top = items[0].get("title", "")
                break

        return {
            "p0_count":    len(p0),
            "p1_count":    len(p1),
            "p2_count":    len(p2),
            "p3_count":    len(p3),
            "total":       len(p0) + len(p1) + len(p2) + len(p3),
            "top_priority": top,
            "p0_desc":     _P0_DESC,
            "p1_desc":     _P1_DESC,
            "p2_desc":     _P2_DESC,
            "p3_desc":     _P3_DESC,
            "no_real_orders":    True,
            "production_blocked": True,
        }

    def board_to_rows(self, board: Dict[str, list]) -> List[dict]:
        """Flatten board to list of dicts for CSV serialisation."""
        rows = []
        for pri in (PRI_P0, PRI_P1, PRI_P2, PRI_P3):
            for item in board.get(pri, []):
                rows.append({**item, "priority": pri})
        return rows

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _rec_to_board_item(
        self,
        rec: ResearchRecommendation,
        signals: List[ResearchSignal],
    ) -> dict:
        cmd = rec.suggested_commands[0] if rec.suggested_commands else ""
        evidence = ""
        for sig in signals:
            if sig.signal_id in rec.related_signals:
                evidence = sig.evidence
                break
        return {
            "title":    rec.title,
            "why":      rec.rationale,
            "evidence": evidence,
            "action":   rec.action_type,
            "command":  cmd,
            "module":   rec.related_modules[0] if rec.related_modules else "",
            "due_hint": rec.due_hint,
            "priority": rec.priority,
        }
