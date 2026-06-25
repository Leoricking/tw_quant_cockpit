"""
paper_trading/market_data/lineage_v161.py — Data Lineage v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Tracks event lineage: raw → canonical → paper event bus.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class LineageRecord:
    def __init__(
        self,
        lineage_id: str,
        session_id: str,
        raw_event_id: str,
        canonical_event_id: Optional[str],
        adapter_id: str,
        source_class: str,
        symbol: str,
        timestamp_utc: str,
        pipeline_stage: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.lineage_id = lineage_id
        self.session_id = session_id
        self.raw_event_id = raw_event_id
        self.canonical_event_id = canonical_event_id
        self.adapter_id = adapter_id
        self.source_class = source_class
        self.symbol = symbol
        self.timestamp_utc = timestamp_utc
        self.pipeline_stage = pipeline_stage
        self.metadata = metadata or {}


class MarketDataLineageTracker:
    """
    Records the lineage of market data events through the pipeline.
    Traceability: raw → normalized → quality-gated → published.
    """

    def __init__(self) -> None:
        self._records: Dict[str, LineageRecord] = {}
        self._by_session: Dict[str, List[str]] = {}

    def record(
        self,
        session_id: str,
        raw_event_id: str,
        adapter_id: str,
        source_class: str,
        symbol: str,
        timestamp_utc: str,
        pipeline_stage: str,
        canonical_event_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> LineageRecord:
        lineage_id = str(uuid.uuid4())
        rec = LineageRecord(
            lineage_id=lineage_id,
            session_id=session_id,
            raw_event_id=raw_event_id,
            canonical_event_id=canonical_event_id,
            adapter_id=adapter_id,
            source_class=source_class,
            symbol=symbol,
            timestamp_utc=timestamp_utc,
            pipeline_stage=pipeline_stage,
            metadata=metadata,
        )
        self._records[lineage_id] = rec
        self._by_session.setdefault(session_id, []).append(lineage_id)
        return rec

    def get_for_session(self, session_id: str) -> List[LineageRecord]:
        ids = self._by_session.get(session_id, [])
        return [self._records[i] for i in ids if i in self._records]

    def get(self, lineage_id: str) -> Optional[LineageRecord]:
        return self._records.get(lineage_id)

    def count(self) -> int:
        return len(self._records)

    def summarize_session(self, session_id: str) -> Dict[str, Any]:
        records = self.get_for_session(session_id)
        stages: Dict[str, int] = {}
        for r in records:
            stages[r.pipeline_stage] = stages.get(r.pipeline_stage, 0) + 1
        return {
            "session_id": session_id,
            "total_records": len(records),
            "by_stage": stages,
        }
