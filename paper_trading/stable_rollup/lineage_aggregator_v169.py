"""
paper_trading/stable_rollup/lineage_aggregator_v169.py
Lineage aggregator for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict, List

VERSION = "1.6.9"

EXPECTED_CHAIN = [
    "1.6.0", "1.6.1", "1.6.1.1", "1.6.2", "1.6.3", "1.6.4",
    "1.6.5", "1.6.6", "1.6.6.1", "1.6.6.2", "1.6.7", "1.6.8", "1.6.9",
]


def run() -> Dict[str, Any]:
    """Build version chain from registry and verify lineage."""
    try:
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()

        # Build version chain by walking parent links from v1.6.9
        chain: List[str] = []
        current = "1.6.9"
        visited = set()
        cycles: List[str] = []

        while current is not None:
            if current in visited:
                cycles.append(current)
                break
            visited.add(current)
            chain.append(current)
            entry = reg.get_release(current)
            if entry is None:
                break
            current = entry.get("parent_version")

        chain.reverse()  # root first

        # Check broken links
        broken_links: List[str] = []
        for i, v in enumerate(chain):
            entry = reg.get_release(v)
            if entry is None:
                broken_links.append(f"Missing release: {v!r}")
                continue
            parent_v = entry.get("parent_version")
            if parent_v is not None:
                if i > 0 and chain[i - 1] != parent_v:
                    broken_links.append(f"Chain break at {v!r}: expected parent {chain[i-1]!r}, got {parent_v!r}")
                if parent_v not in visited:
                    broken_links.append(f"Parent {parent_v!r} of {v!r} not in chain")

        intact = len(broken_links) == 0 and len(cycles) == 0

        status = "PASS" if intact and len(chain) >= 13 else "FAIL"

        return {
            "name": "lineage_aggregator_v169",
            "version": VERSION,
            "version_chain": chain,
            "chain_length": len(chain),
            "intact": intact,
            "broken_links": broken_links,
            "cycles": cycles,
            "status": status,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
    except Exception as exc:
        return {
            "name": "lineage_aggregator_v169",
            "version": VERSION,
            "version_chain": [],
            "chain_length": 0,
            "intact": False,
            "broken_links": [str(exc)],
            "cycles": [],
            "status": "DEGRADED",
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
