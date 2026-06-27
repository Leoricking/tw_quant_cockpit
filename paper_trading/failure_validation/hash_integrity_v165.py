"""
paper_trading/failure_validation/hash_integrity_v165.py — Hash integrity verification v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, Optional

PAPER_ONLY = True
RESEARCH_ONLY = True


def compute_content_hash(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


def verify_hash(data: Any, expected_hash: str) -> bool:
    return compute_content_hash(data) == expected_hash


def compute_chain_hash(hashes: list) -> str:
    combined = "|".join(str(h) for h in hashes)
    return hashlib.sha256(combined.encode()).hexdigest()


class HashIntegrityChecker:
    """Verifies hash integrity for checkpoints and snapshots."""

    def check_checkpoint(self, data: Any, stored_hash: str) -> Dict[str, Any]:
        computed = compute_content_hash(data)
        match = (computed == stored_hash)
        return {"match": match, "computed": computed, "stored": stored_hash,
                "result": "PASS" if match else "HASH_MISMATCH"}

    def check_snapshot(self, data: Any, stored_hash: str) -> Dict[str, Any]:
        return self.check_checkpoint(data, stored_hash)
