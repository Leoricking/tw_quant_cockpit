"""
paper_trading/multi_session/reproducibility_v166.py — Reproducibility v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Same input → same output hash. Silent mismatch forbidden.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, List

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_SILENT_MISMATCH = True


def compute_input_hash(
    session_ids: List[str],
    policy_id: str,
    virtual_clock: str,
    seed: int,
    events: List[str] = None,
    failures: List[str] = None,
) -> str:
    payload = {
        "sessions": sorted(session_ids),
        "policy": policy_id,
        "clock": virtual_clock,
        "seed": seed,
        "events": sorted(events or []),
        "failures": sorted(failures or []),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


def compute_output_hash(
    sessions_admitted: List[str],
    sessions_blocked: List[str],
    conflicts: int,
    final_state: Dict[str, Any],
) -> str:
    payload = {
        "admitted": sorted(sessions_admitted),
        "blocked": sorted(sessions_blocked),
        "conflicts": conflicts,
        "final_state": final_state,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]


def validate_reproducibility(
    input_hash: str,
    output_hash_1: str,
    output_hash_2: str,
) -> Dict[str, Any]:
    match = output_hash_1 == output_hash_2
    return {
        "reproducible": match,
        "input_hash": input_hash,
        "output_hash_1": output_hash_1,
        "output_hash_2": output_hash_2,
        "mismatch": not match,
    }
