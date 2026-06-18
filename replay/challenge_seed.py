"""
replay/challenge_seed.py — Deterministic seed computation v1.2.7

[!] Same seed + same data version = same challenge (deterministic).
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

DATA_VERSION = "1.2.7"


def compute_seed(
    seed: Optional[str] = None,
    source_id: Optional[str] = None,
    data_version: str = DATA_VERSION,
    extra: Optional[str] = None,
) -> str:
    """
    Compute a deterministic seed string.
    Same seed + source_id + data_version = same challenge.

    If seed is provided and non-empty, derive from it.
    Otherwise generate from source_id + data_version.
    """
    if seed and seed.strip():
        base = f"{seed}::{data_version}"
    elif source_id:
        base = f"{source_id}::{data_version}"
    else:
        ts = datetime.now(timezone.utc).isoformat()
        base = f"random::{data_version}::{ts}"
    if extra:
        base = f"{base}::{extra}"
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()[:16].upper()
    return h


def build_seed_metadata(
    seed: str,
    source_id: Optional[str] = None,
    data_version: str = DATA_VERSION,
) -> Dict[str, Any]:
    """Return metadata dict for a seed."""
    return {
        "seed":         seed,
        "source_id":    source_id,
        "data_version": data_version,
        "deterministic": True,
        "same_seed_same_challenge": True,
        "research_only": True,
        "no_real_orders": True,
    }


def verify_seed(
    seed: str,
    source_id: Optional[str],
    data_version: str = DATA_VERSION,
    extra: Optional[str] = None,
) -> bool:
    """Verify that a seed matches the deterministic computation."""
    expected = compute_seed(seed=None, source_id=source_id, data_version=data_version, extra=extra)
    # Check if seed equals expected (when generated from source_id)
    return seed == expected
