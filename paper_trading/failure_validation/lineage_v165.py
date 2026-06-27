"""
paper_trading/failure_validation/lineage_v165.py — Failure injection lineage tracking v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

PAPER_ONLY = True
RESEARCH_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class LineageEntry:
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario_id: str = ""
    result_id: str = ""
    validation_id: str = ""
    scorecard_id: str = ""
    phase: str = ""
    detail: str = ""
    ts: datetime = field(default_factory=_utcnow)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "scenario_id": self.scenario_id,
            "result_id": self.result_id,
            "phase": self.phase,
            "detail": self.detail,
            "ts": self.ts.isoformat(),
        }


class LineageTracker:
    """Tracks lineage of failure injection → validation → scorecard chain."""

    def __init__(self) -> None:
        self._entries: List[LineageEntry] = []

    def record(self, scenario_id: str, result_id: str, phase: str, detail: str = "",
               validation_id: str = "", scorecard_id: str = "") -> LineageEntry:
        entry = LineageEntry(
            scenario_id=scenario_id,
            result_id=result_id,
            validation_id=validation_id,
            scorecard_id=scorecard_id,
            phase=phase,
            detail=detail,
        )
        self._entries.append(entry)
        return entry

    def chain_for(self, scenario_id: str) -> List[LineageEntry]:
        return [e for e in self._entries if e.scenario_id == scenario_id]

    def all_entries(self) -> List[LineageEntry]:
        return list(self._entries)

    def count(self) -> int:
        return len(self._entries)
