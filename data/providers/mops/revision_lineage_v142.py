"""
data/providers/mops/revision_lineage_v142.py — MOPS revision lineage service v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Tracks restatement/revision lineage for MOPS financial filings.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.providers.mops.models_v142 import MOPSRevisionRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSRevisionLineageService:
    """
    Tracks revision lineage for MOPS filings.
    Revisions are recorded when a company restates or corrects a prior filing.
    """

    def __init__(self) -> None:
        self._revisions: Dict[str, List[MOPSRevisionRecord]] = {}

    def add_revision(self, record: MOPSRevisionRecord) -> None:
        """Add a revision record."""
        key = f"{record.symbol}:{record.original_filing_id}"
        if key not in self._revisions:
            self._revisions[key] = []
        self._revisions[key].append(record)

    def get_revisions(
        self, symbol: str, original_filing_id: str
    ) -> List[MOPSRevisionRecord]:
        """Get all revisions for a filing."""
        key = f"{symbol}:{original_filing_id}"
        return list(self._revisions.get(key, []))

    def has_revision(self, symbol: str, original_filing_id: str) -> bool:
        """Check if a filing has any revisions."""
        key = f"{symbol}:{original_filing_id}"
        return key in self._revisions and len(self._revisions[key]) > 0

    def get_latest_revision(
        self, symbol: str, original_filing_id: str
    ) -> Optional[MOPSRevisionRecord]:
        """Get the most recent revision for a filing."""
        revs = self.get_revisions(symbol, original_filing_id)
        if not revs:
            return None
        return sorted(revs, key=lambda r: r.revision_sequence)[-1]

    def build_lineage_summary(
        self, symbol: str, original_filing_id: str
    ) -> Dict[str, Any]:
        """Build a revision lineage summary for a filing."""
        revisions = self.get_revisions(symbol, original_filing_id)
        return {
            "symbol": symbol,
            "original_filing_id": original_filing_id,
            "revision_count": len(revisions),
            "has_material_revision": any(r.is_material_revision for r in revisions),
            "latest_revision_date": revisions[-1].revision_date if revisions else None,
            "revision_types": [r.revision_type for r in revisions],
            "available_from": revisions[0].available_from if revisions else None,
        }

    def total_count(self) -> int:
        """Total number of filing keys with revisions."""
        return len(self._revisions)

    def from_fixture(self, fixture_data: Dict[str, Any]) -> MOPSRevisionRecord:
        """Parse a revision record from fixture dict (for offline tests)."""
        now = _now_iso()
        return MOPSRevisionRecord(
            symbol=fixture_data.get("symbol", ""),
            original_filing_id=fixture_data.get("original_filing_id", ""),
            revision_sequence=int(fixture_data.get("revision_sequence", 1)),
            revision_date=fixture_data.get("revision_date"),
            revision_type=fixture_data.get("revision_type", "UNKNOWN"),
            revision_reason=fixture_data.get("revision_reason"),
            affected_periods=fixture_data.get("affected_periods", []),
            affected_line_items=fixture_data.get("affected_line_items", []),
            magnitude_description=fixture_data.get("magnitude_description"),
            is_material_revision=bool(fixture_data.get("is_material_revision", False)),
            available_from=fixture_data.get("available_from"),
            source_timestamp=fixture_data.get("source_timestamp"),
            fetched_at=now,
            provider_id="mops_official",
            provenance=None,
            warnings=[],
            metadata={},
        )
