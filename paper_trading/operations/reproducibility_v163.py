"""
Reproducibility v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.operations.models_v163 import _semantic_hash


EXCLUDED_FROM_HASH = {
    "generated_at", "local_machine_path", "tmp_filename",
    "runtime_uuid", "display_only", "tmp_path",
}


@dataclass
class ReproducibilityManifest:
    manifest_id:    str
    session_id:     str
    inputs_hash:    str
    outputs_hash:   str
    matches:        bool
    divergence_count: int        = 0
    differing_keys: List[str]   = field(default_factory=list)
    excluded_keys:  List[str]   = field(default_factory=list)
    version:        str          = "1.6.3"
    paper_only:     bool         = True
    research_only:  bool         = True


def compute_semantic_hash(data: Dict[str, Any]) -> str:
    """Exclude non-deterministic fields before hashing."""
    cleaned = {k: v for k, v in data.items() if k not in EXCLUDED_FROM_HASH}
    return _semantic_hash(cleaned)


def verify_reproducibility(
    run_a: Dict[str, Any],
    run_b: Dict[str, Any],
    session_id: str = "",
) -> ReproducibilityManifest:
    from paper_trading.operations.models_v163 import _new_id
    hash_a = compute_semantic_hash(run_a)
    hash_b = compute_semantic_hash(run_b)
    matches = hash_a == hash_b

    differing = []
    if not matches:
        for k in set(run_a) | set(run_b):
            if k in EXCLUDED_FROM_HASH:
                continue
            if run_a.get(k) != run_b.get(k):
                differing.append(k)

    return ReproducibilityManifest(
        manifest_id=_new_id("rep_"),
        session_id=session_id,
        inputs_hash=hash_a,
        outputs_hash=hash_b,
        matches=matches,
        divergence_count=len(differing),
        differing_keys=differing,
        excluded_keys=sorted(EXCLUDED_FROM_HASH),
    )


__all__ = ["ReproducibilityManifest", "compute_semantic_hash", "verify_reproducibility", "EXCLUDED_FROM_HASH"]
