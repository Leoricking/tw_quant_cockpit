"""paper_trading/lineage_v160.py — Paper Trading Lineage v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Complete lineage chain: Report → Snapshot → Ledger → Fills → Orders → Risk → Signals → Events → Provider.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PaperLineageRecord:
    lineage_id: str
    session_id: str
    entity_type: str  # order, fill, ledger, snapshot, event, report
    entity_id: str
    parent_ids: List[str] = field(default_factory=list)
    event_hashes: List[str] = field(default_factory=list)
    order_hashes: List[str] = field(default_factory=list)
    fill_hashes: List[str] = field(default_factory=list)
    ledger_hashes: List[str] = field(default_factory=list)
    snapshot_hashes: List[str] = field(default_factory=list)
    policy_versions: Dict[str, str] = field(default_factory=dict)
    code_commit: str = ""
    data_mode: str = ""
    provider_source: str = ""
    available_from: str = ""
    received_timestamp: str = ""
    research_only: bool = True
    paper_only: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class PaperLineageService:
    """Tracks paper trading lineage chain."""

    def __init__(self, session_id: str, code_commit: str = "") -> None:
        self._session_id = session_id
        self._code_commit = code_commit
        self._records: List[PaperLineageRecord] = []

    def record(
        self,
        lineage_id: str,
        entity_type: str,
        entity_id: str,
        parent_ids: Optional[List[str]] = None,
        event_hashes: Optional[List[str]] = None,
        order_hashes: Optional[List[str]] = None,
        fill_hashes: Optional[List[str]] = None,
        ledger_hashes: Optional[List[str]] = None,
        snapshot_hashes: Optional[List[str]] = None,
        policy_versions: Optional[Dict[str, str]] = None,
        data_mode: str = "",
        provider_source: str = "",
        available_from: str = "",
        received_timestamp: str = "",
    ) -> PaperLineageRecord:
        rec = PaperLineageRecord(
            lineage_id=lineage_id,
            session_id=self._session_id,
            entity_type=entity_type,
            entity_id=entity_id,
            parent_ids=parent_ids or [],
            event_hashes=event_hashes or [],
            order_hashes=order_hashes or [],
            fill_hashes=fill_hashes or [],
            ledger_hashes=ledger_hashes or [],
            snapshot_hashes=snapshot_hashes or [],
            policy_versions=policy_versions or {},
            code_commit=self._code_commit,
            data_mode=data_mode,
            provider_source=provider_source,
            available_from=available_from,
            received_timestamp=received_timestamp,
        )
        self._records.append(rec)
        return rec

    def get_records(self) -> List[PaperLineageRecord]:
        return list(self._records)

    def get_chain(self, entity_id: str) -> List[PaperLineageRecord]:
        """Return all lineage records connected to entity_id."""
        result = []
        for r in self._records:
            if r.entity_id == entity_id or entity_id in r.parent_ids:
                result.append(r)
        return result

    def count(self) -> int:
        return len(self._records)
