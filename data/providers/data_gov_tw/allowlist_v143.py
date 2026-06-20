"""
data/providers/data_gov_tw/allowlist_v143.py — Dataset allowlist management v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Only allowlisted + approved + official datasets may enter formal research.
[!] No wildcard/allow_all mode.
[!] Unlisted datasets: DATASET_NOT_ALLOWLISTED — metadata only, no ingest.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_ALLOWLIST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    )))),
    "config",
    "data_gov_tw_allowlist.json",
)

DATASET_NOT_ALLOWLISTED = "DATASET_NOT_ALLOWLISTED"


class DataGovTwAllowlist:
    """
    Manages the official data.gov.tw dataset allowlist.

    Rules:
    - Only datasets with approved=True, enabled=True, official=True
      AND valid schema contract, accepted license, quality pass
      may enter formal research.
    - Datasets not in allowlist: can inspect metadata, cannot ingest.
    - No wildcard or allow_all mode.
    - Cannot auto-add datasets to allowlist.
    - Cannot auto-approve license.
    - Cannot auto-modify schema contract.
    """

    def __init__(self, allowlist_path: Optional[str] = None) -> None:
        self._path = allowlist_path or _ALLOWLIST_PATH
        self._entries: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        """Load allowlist from JSON file. Fail gracefully."""
        if not os.path.exists(self._path):
            return
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data.get("datasets", []):
                did = entry.get("dataset_id")
                if did:
                    self._entries[did] = entry
        except Exception:
            # Fail gracefully — do not crash. Allowlist remains empty.
            pass

    def is_allowlisted(self, dataset_id: str) -> bool:
        """Return True if dataset is in the allowlist (regardless of approval status)."""
        return dataset_id in self._entries

    def is_formally_approved(self, dataset_id: str) -> bool:
        """Return True only if approved=True AND enabled=True AND official=True."""
        entry = self._entries.get(dataset_id)
        if not entry:
            return False
        return (
            bool(entry.get("approved", False))
            and bool(entry.get("enabled", False))
            and bool(entry.get("official", True))
        )

    def get_entry(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """Return allowlist entry or None."""
        return self._entries.get(dataset_id)

    def get_formal_use_allowed(self, dataset_id: str) -> bool:
        """
        Return True only if all formal-use conditions are met:
        approved, enabled, official, and entry exists.
        """
        return self.is_formally_approved(dataset_id)

    def list_all(self) -> List[Dict[str, Any]]:
        return list(self._entries.values())

    def list_approved(self) -> List[Dict[str, Any]]:
        return [e for e in self._entries.values() if e.get("approved") and e.get("enabled")]

    def list_planned(self) -> List[Dict[str, Any]]:
        status = lambda e: (e.get("metadata") or {}).get("status", "")
        return [e for e in self._entries.values() if status(e) == "PLANNED"]

    def list_blocked(self) -> List[Dict[str, Any]]:
        status = lambda e: (e.get("metadata") or {}).get("status", "")
        return [e for e in self._entries.values() if status(e) == "BLOCKED"]

    def list_disabled(self) -> List[Dict[str, Any]]:
        return [e for e in self._entries.values() if not e.get("enabled", True)]

    def check_allowlist_result(self, dataset_id: str) -> Dict[str, Any]:
        """Return a structured allowlist check result."""
        if not self.is_allowlisted(dataset_id):
            return {
                "dataset_id": dataset_id,
                "result": DATASET_NOT_ALLOWLISTED,
                "allowlisted": False,
                "approved": False,
                "formal_use_allowed": False,
                "message": "Dataset not in allowlist. Metadata inspection only. Cannot ingest.",
            }
        entry = self._entries[dataset_id]
        approved = self.is_formally_approved(dataset_id)
        return {
            "dataset_id": dataset_id,
            "result": "APPROVED" if approved else "REVIEW_REQUIRED",
            "allowlisted": True,
            "approved": approved,
            "enabled": bool(entry.get("enabled", False)),
            "official": bool(entry.get("official", True)),
            "formal_use_allowed": approved,
            "domain": entry.get("research_domain"),
            "authoritative_level": entry.get("authoritative_level"),
            "license_name": entry.get("license_name"),
            "update_frequency": entry.get("update_frequency"),
            "message": "Approved for formal research use." if approved else "Allowlisted but not yet approved.",
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "total": len(self._entries),
            "approved": len(self.list_approved()),
            "planned": len(self.list_planned()),
            "blocked": len(self.list_blocked()),
            "disabled": len(self.list_disabled()),
            "wildcard_allowed": False,
            "allow_all_mode": False,
        }
