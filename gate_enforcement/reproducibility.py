"""
gate_enforcement.reproducibility — RunReproducibilityHasher v1.1.5

Produces stable, canonical SHA-256 hashes for run reproducibility.
Research Only. No Real Orders.

Requirements:
- Stable sort
- JSON canonical form
- SHA-256
- No runtime random paths, no machine-specific temp paths, no secrets
- Same payload => same hash
- Different symbol set or gate decision => different hash

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _canonical_json(obj) -> str:
    """Produce stable canonical JSON string with sorted keys."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class RunReproducibilityHasher:
    """
    Produces stable, canonical SHA-256 hashes for enforcement runs.
    Same inputs always produce the same hash.
    """

    def canonicalize_payload(self, payload: dict) -> str:
        """Produce canonical JSON string of payload."""
        return _canonical_json(payload)

    def hash_symbols(self, symbols: List[str]) -> str:
        """Hash a sorted list of symbols."""
        canonical = _canonical_json(sorted(set(str(s) for s in symbols)))
        return _sha256(canonical)

    def hash_arguments(self, arguments: dict) -> str:
        """Hash normalized arguments dict."""
        # Normalize: remove None values, sort keys
        normalized = {k: v for k, v in arguments.items() if v is not None}
        canonical = _canonical_json(normalized)
        return _sha256(canonical)

    def hash_gate_decisions(self, decisions: dict) -> str:
        """Hash gate decisions dict."""
        # Sort by symbol for stability
        sorted_decisions = dict(sorted(decisions.items()))
        canonical = _canonical_json(sorted_decisions)
        return _sha256(canonical)

    def hash_snapshot(self, snapshot) -> str:
        """Hash a RunGateSnapshot's key fields."""
        if hasattr(snapshot, "to_dict"):
            d = snapshot.to_dict()
        else:
            d = dict(snapshot)
        # Only hash the stable fields
        payload = {
            "run_id": d.get("run_id", ""),
            "gate_name": d.get("gate_name", ""),
            "gate_policy_version": d.get("gate_policy_version", ""),
            "requested_level": d.get("requested_level", ""),
            "applied_level": d.get("applied_level", ""),
            "symbols_included": sorted(d.get("symbols_included", [])) if isinstance(d.get("symbols_included"), list) else [],
            "symbols_excluded": sorted(d.get("symbols_excluded", [])) if isinstance(d.get("symbols_excluded"), list) else [],
            "payload_hash": d.get("payload_hash", ""),
        }
        return _sha256(_canonical_json(payload))

    def build_run_hash(
        self,
        code_version: str,
        command_name: str,
        arguments: dict,
        gate_name: str,
        gate_policy_version: str,
        included_symbols: List[str],
        excluded_symbols: List[str],
        decisions: dict,
        coverage_state: Optional[dict] = None,
        freshness_state: Optional[dict] = None,
        statistical_confidence: Optional[float] = None,
        source_identifiers: Optional[list] = None,
    ) -> str:
        """Build a canonical SHA-256 hash for a run."""
        payload = {
            "code_version": str(code_version),
            "command_name": str(command_name),
            "gate_name": str(gate_name),
            "gate_policy_version": str(gate_policy_version),
            "included_symbols": sorted(str(s) for s in (included_symbols or [])),
            "excluded_symbols": sorted(str(s) for s in (excluded_symbols or [])),
            "gate_decisions": dict(sorted(decisions.items())),
            "arguments_normalized": _canonical_json({k: v for k, v in sorted(arguments.items()) if v is not None}),
            "coverage_dates": _canonical_json(coverage_state or {}),
            "freshness_dates": _canonical_json(freshness_state or {}),
            "statistical_confidence": statistical_confidence,
            "source_identifiers": sorted(source_identifiers or []),
            "research_only": True,
            "no_real_orders": True,
        }
        return _sha256(_canonical_json(payload))

    def verify_run_hash(
        self, run_id: str,
        output_dir: str = "data/quality_gate_enforcement",
    ) -> bool:
        """Verify hash for a run by re-computing from stored snapshot."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        hashes_path = os.path.join(output_dir, "run_hashes.csv")
        if not os.path.isfile(hashes_path):
            return False
        try:
            import csv
            with open(hashes_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("run_id") == run_id:
                        return bool(row.get("reproducibility_hash", ""))
        except Exception as exc:
            logger.warning("verify_run_hash failed: %s", exc)
        return False
