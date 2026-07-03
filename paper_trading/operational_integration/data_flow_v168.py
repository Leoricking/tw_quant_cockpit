"""
paper_trading/operational_integration/data_flow_v168.py
Data Flow Tracker for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import DataFlowRecord
from .enums_v168 import DataFlowStatus, FORBIDDEN_INTEGRATION_FIELDS

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DataFlowTracker:
    """Tracks data flow between components. Research only."""

    def __init__(self) -> None:
        self._flows: List[DataFlowRecord] = []
        self._flow_index: Dict[str, List[DataFlowRecord]] = {}

    def record_flow(
        self,
        source: str,
        destination: str,
        payload_hash: str,
        lineage_id: str,
        timestamp: str,
        sequence_number: int,
        contract_version: str,
        validation_status: str = "VALID",
    ) -> DataFlowRecord:
        """Record a data flow event."""
        flow_id = f"flow_{source}_{destination}_{sequence_number}"
        record = DataFlowRecord(
            flow_id=flow_id,
            source_component=source,
            destination_component=destination,
            payload_hash=payload_hash,
            lineage_id=lineage_id,
            timestamp=timestamp,
            sequence_number=sequence_number,
            contract_version=contract_version,
            validation_status=validation_status,
        )
        self._flows.append(record)
        key = f"{source}->{destination}"
        if key not in self._flow_index:
            self._flow_index[key] = []
        self._flow_index[key].append(record)
        return record

    def check_sequence_gaps(self, component_id: str) -> List[Dict[str, Any]]:
        """Check for sequence number gaps in flows involving component_id."""
        relevant = [f for f in self._flows if f.source_component == component_id]
        relevant.sort(key=lambda f: f.sequence_number)
        gaps = []
        for i in range(1, len(relevant)):
            prev_seq = relevant[i - 1].sequence_number
            curr_seq = relevant[i].sequence_number
            if curr_seq != prev_seq + 1:
                gaps.append({
                    "component_id": component_id,
                    "expected_seq": prev_seq + 1,
                    "actual_seq": curr_seq,
                    "gap_size": curr_seq - prev_seq - 1,
                })
        return gaps

    def check_duplicates(self, component_id: str) -> List[Dict[str, Any]]:
        """Check for duplicate sequence numbers or payload hashes."""
        relevant = [f for f in self._flows if f.source_component == component_id]
        seen_seq: Dict[int, str] = {}
        seen_hash: Dict[str, str] = {}
        duplicates = []
        for f in relevant:
            if f.sequence_number in seen_seq:
                duplicates.append({
                    "flow_id": f.flow_id,
                    "type": "duplicate_sequence",
                    "sequence_number": f.sequence_number,
                })
            else:
                seen_seq[f.sequence_number] = f.flow_id
            if f.payload_hash in seen_hash:
                duplicates.append({
                    "flow_id": f.flow_id,
                    "type": "duplicate_hash",
                    "payload_hash": f.payload_hash,
                })
            else:
                seen_hash[f.payload_hash] = f.flow_id
        return duplicates

    def check_stale(self, component_id: str, max_age_seconds: float) -> List[Dict[str, Any]]:
        """Return flows that are older than max_age_seconds."""
        stale = []
        now = datetime.now(timezone.utc)
        for f in self._flows:
            if f.source_component != component_id and f.destination_component != component_id:
                continue
            try:
                ts = datetime.fromisoformat(f.timestamp.replace("Z", "+00:00"))
                age = (now - ts).total_seconds()
                if age > max_age_seconds:
                    stale.append({"flow_id": f.flow_id, "age_seconds": age, "max_age": max_age_seconds})
            except Exception:
                stale.append({"flow_id": f.flow_id, "age_seconds": -1, "error": "parse_error"})
        return stale

    def check_reordering(self, component_id: str) -> List[Dict[str, Any]]:
        """Check for out-of-order flows."""
        relevant = [f for f in self._flows if f.source_component == component_id]
        relevant_sorted = sorted(relevant, key=lambda f: f.sequence_number)
        reordered = []
        for i, f in enumerate(self._flows):
            if f.source_component != component_id:
                continue
            # Check if timestamp ordering matches sequence ordering
        for i in range(1, len(relevant_sorted)):
            f_prev = relevant_sorted[i - 1]
            f_curr = relevant_sorted[i]
            if f_prev.timestamp > f_curr.timestamp:
                reordered.append({
                    "flow_id": f_curr.flow_id,
                    "type": "out_of_order_timestamp",
                    "prev_ts": f_prev.timestamp,
                    "curr_ts": f_curr.timestamp,
                })
        return reordered

    def check_schema_drift(
        self, flow_id: str, expected_schema: Dict[str, Any], actual_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check for schema drift between expected and actual schemas."""
        expected_keys = set(expected_schema.keys())
        actual_keys = set(actual_schema.keys())
        added = actual_keys - expected_keys
        removed = expected_keys - actual_keys
        drifted = len(added) > 0 or len(removed) > 0
        return {
            "flow_id": flow_id,
            "drifted": drifted,
            "added_fields": list(added),
            "removed_fields": list(removed),
            "paper_only": True,
        }

    def check_forbidden_field_leakage(self, flow_id: str, payload: Dict[str, Any]) -> List[str]:
        """Check if any forbidden fields leaked into payload."""
        leaked = []
        for key in FORBIDDEN_INTEGRATION_FIELDS:
            if key in payload:
                leaked.append(key)
        return leaked

    def get_flow_history(self, component_id: str) -> List[DataFlowRecord]:
        """Return all flow records involving component_id."""
        return [
            f for f in self._flows
            if f.source_component == component_id or f.destination_component == component_id
        ]

    def summarize(self) -> Dict[str, Any]:
        """Return summary statistics of all tracked flows."""
        total = len(self._flows)
        valid = sum(1 for f in self._flows if f.validation_status == "VALID")
        invalid = total - valid
        forbidden_leaked = sum(1 for f in self._flows if len(f.forbidden_fields_found) > 0)
        return {
            "total_flows": total,
            "valid_flows": valid,
            "invalid_flows": invalid,
            "forbidden_leaked_count": forbidden_leaked,
            "component_pairs": len(self._flow_index),
            "paper_only": True,
            "research_only": True,
        }
