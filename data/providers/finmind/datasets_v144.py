"""
data/providers/finmind/datasets_v144.py — FinMind dataset allowlist v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No wildcard allowlist. No auto-approve. No auto-discovery.
[!] All datasets explicitly listed in config/finmind_dataset_allowlist.json.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FINMIND_WILDCARD_ALLOWLIST_ENABLED = False
FINMIND_AUTO_APPROVE_ENABLED = False
FINMIND_AUTO_DISCOVERY_ENABLED = False

_DEFAULT_ALLOWLIST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    )))),
    "config", "finmind_dataset_allowlist.json"
)


class FinMindDatasetAllowlist:
    """
    Dataset allowlist for FinMind. Loads from config/finmind_dataset_allowlist.json.
    No wildcard, no auto-approve, no auto-discovery.
    """

    def __init__(self, config_path: Optional[str] = None) -> None:
        self._path = config_path or _DEFAULT_ALLOWLIST_PATH
        self._meta: Dict[str, Any] = {}
        self._datasets: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self._meta = data.get("_meta", {})
            self._datasets = data.get("datasets", [])
        except FileNotFoundError:
            self._meta = {"error": "allowlist file not found", "path": self._path}
            self._datasets = []
        except json.JSONDecodeError as exc:
            self._meta = {"error": f"JSON parse error: {exc}"}
            self._datasets = []

    def is_allowed(self, dataset: str) -> bool:
        """Return True if dataset is in allowlist, enabled, and approved."""
        assert self._meta.get("wildcard_allowlist_enabled", False) is False, "Wildcard not allowed"
        assert self._meta.get("auto_approve_enabled", False) is False, "Auto-approve not allowed"
        for ds in self._datasets:
            if ds.get("dataset") == dataset:
                return ds.get("enabled", False) and ds.get("approved", False)
        return False

    def is_formal_allowed(self, dataset: str) -> bool:
        """Return True if dataset allows formal use (SECONDARY_SUPPLEMENT_ONLY is not formal)."""
        for ds in self._datasets:
            if ds.get("dataset") == dataset:
                policy = ds.get("formal_use_policy", "BLOCKED_BY_DEFAULT")
                return policy not in ("BLOCKED_BY_DEFAULT", "SECONDARY_SUPPLEMENT_ONLY", "EXPERIMENTAL_ONLY")
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """Return all dataset entries."""
        return list(self._datasets)

    def get_supported(self) -> List[Dict[str, Any]]:
        """Return only enabled and approved datasets."""
        return [d for d in self._datasets if d.get("enabled", False) and d.get("approved", False)]

    def get_entry(self, dataset: str) -> Optional[Dict[str, Any]]:
        """Return a single dataset entry or None."""
        for ds in self._datasets:
            if ds.get("dataset") == dataset:
                return ds
        return None

    def summary(self) -> Dict[str, Any]:
        return {
            "total": len(self._datasets),
            "supported": len(self.get_supported()),
            "wildcard_allowlist_enabled": False,
            "auto_approve_enabled": False,
            "auto_discovery_enabled": False,
            "formal_use_policy": self._meta.get("formal_use_policy", "BLOCKED_BY_DEFAULT"),
            "schema_version": self._meta.get("schema_version", "unknown"),
        }
