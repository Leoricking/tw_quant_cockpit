"""
portfolio/walk_forward/store_v154.py — Walk-forward Store v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
In-memory store for demo/fixture mode. No formal ledger write. No broker credentials.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
STORE_VERSION = "1.5.4"


def _hash(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class WalkForwardStore:
    """In-memory walk-forward store. Immutable once saved. No formal ledger write."""

    def __init__(self):
        self.version = STORE_VERSION
        self._configs: Dict[str, Dict[str, Any]] = {}
        self._runs: Dict[str, Dict[str, Any]] = {}
        self._config_hashes: Dict[str, str] = {}
        self._run_hashes: Dict[str, str] = {}

    def save_config(self, config) -> str:
        """Save config. Idempotent by content hash. Returns config_id."""
        config_id = getattr(config, "config_id", "unknown")
        data = {
            "config_id": config_id,
            "name": getattr(config, "name", ""),
            "version": getattr(config, "version", "1.5.4"),
            "portfolio_id": getattr(config, "portfolio_id", ""),
            "research_only": getattr(config, "research_only", True),
        }
        content_hash = _hash(data)

        # Idempotent: if same hash exists, return existing
        if config_id in self._configs:
            if self._config_hashes.get(config_id) == content_hash:
                return config_id

        self._configs[config_id] = {**data, "content_hash": content_hash}
        self._config_hashes[config_id] = content_hash
        return config_id

    def save_run(
        self,
        run_id: str,
        summary,
        windows: List[Any],
        transactions: List[Any],
    ) -> bool:
        """Save run. Immutable — hash check prevents mutation. Returns True if saved."""
        run_data = {
            "run_id": run_id,
            "config_id": getattr(summary, "config_id", "unknown") if summary else "unknown",
            "total_windows": len(windows),
            "research_only": True,
            "formal_ledger_persisted": False,
        }
        content_hash = _hash(run_data)

        # Immutability check
        if run_id in self._runs:
            if self._run_hashes.get(run_id) != content_hash:
                raise ValueError(f"Run {run_id!r} already exists with different hash — immutable")
            return False  # Already saved

        self._runs[run_id] = {**run_data, "content_hash": content_hash}
        self._run_hashes[run_id] = content_hash
        return True

    def get_config(self, config_id: str) -> Optional[Dict[str, Any]]:
        return self._configs.get(config_id)

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self._runs.get(run_id)

    def list_configs(self) -> List[Dict[str, Any]]:
        return list(self._configs.values())

    def list_runs(self) -> List[Dict[str, Any]]:
        return list(self._runs.values())
