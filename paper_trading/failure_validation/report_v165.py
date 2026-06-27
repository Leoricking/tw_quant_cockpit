"""
paper_trading/failure_validation/report_v165.py — Failure injection report generation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
[!] Reports are local/in-memory only. No external publish.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

PAPER_ONLY = True
RESEARCH_ONLY = True
EXTERNAL_PUBLISH_ENABLED = False


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class FailureInjectionReport:
    """Aggregated report for a failure injection & recovery validation run."""

    def __init__(self, run_id: str = "", scenario_name: str = "") -> None:
        self.run_id = run_id
        self.scenario_name = scenario_name
        self.sections: List[Dict[str, Any]] = []
        self.generated_at = _utcnow()

    def add_section(self, title: str, content: Dict[str, Any]) -> None:
        self.sections.append({"title": title, "content": content})

    def summary(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "scenario_name": self.scenario_name,
            "sections": len(self.sections),
            "generated_at": self.generated_at.isoformat(),
            "paper_only": PAPER_ONLY,
            "research_only": RESEARCH_ONLY,
        }

    def as_dict(self) -> Dict[str, Any]:
        return {
            **self.summary(),
            "sections_detail": self.sections,
        }


class ReportStore:
    """Local in-memory store for failure injection reports."""

    def __init__(self) -> None:
        assert not EXTERNAL_PUBLISH_ENABLED
        self._reports: List[FailureInjectionReport] = []

    def store(self, report: FailureInjectionReport) -> None:
        self._reports.append(report)

    def all(self) -> List[FailureInjectionReport]:
        return list(self._reports)

    def count(self) -> int:
        return len(self._reports)
