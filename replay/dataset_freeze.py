"""
replay/dataset_freeze.py — ReplayDatasetFreezeManager v1.2.8

Manages dataset freezing and unfreeze guard.
Frozen datasets are immutable. Any modification detected => CORRUPTED.
Silent updates are not allowed.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayDatasetFreezeManager:
    """
    Manages dataset freeze state.

    Rules:
    - Frozen datasets: immutable=True, manifest_hash locked, content_hash locked
    - Any hash mismatch => CORRUPTED (never silent update)
    - Modifying a frozen dataset requires creating a new version

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def freeze_preview(
        self,
        dataset_id: str,
        version: str,
        current_fingerprint: str,
        current_manifest_hash: str,
    ) -> Dict[str, Any]:
        """Preview freeze operation."""
        return {
            "action":       "FREEZE_PREVIEW",
            "dataset_id":   dataset_id,
            "version":      version,
            "fingerprint":  current_fingerprint[:16] + "...",
            "manifest_hash": current_manifest_hash[:16] + "...",
            "note":         "Run with --execute --allow-write to freeze.",
            "warning":      "Once frozen, this version cannot be modified in place.",
        }

    def freeze(
        self,
        manifest: Any,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Freeze a manifest. Sets frozen_at, immutable=True."""
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
            }
        if hasattr(manifest, "frozen_at") and manifest.frozen_at:
            return {
                "status":     "ALREADY_FROZEN",
                "dataset_id": manifest.dataset_id,
                "frozen_at":  manifest.frozen_at,
            }
        ts = _now_utc()
        manifest.frozen_at = ts
        manifest.status    = "FROZEN"
        return {
            "status":     "FROZEN",
            "dataset_id": manifest.dataset_id,
            "version":    manifest.dataset_version,
            "frozen_at":  ts,
        }

    def verify_frozen(
        self,
        manifest: Any,
        current_fingerprint: str,
    ) -> Dict[str, Any]:
        """Check if a frozen dataset's fingerprint still matches."""
        if not getattr(manifest, "frozen_at", None):
            return {"status": "NOT_FROZEN", "dataset_id": manifest.dataset_id}
        if manifest.fingerprint == current_fingerprint:
            return {
                "status":     "IMMUTABLE_OK",
                "dataset_id": manifest.dataset_id,
            }
        return {
            "status":     "CORRUPTED",
            "dataset_id": manifest.dataset_id,
            "stored_fingerprint":  manifest.fingerprint,
            "current_fingerprint": current_fingerprint,
            "note": "Hash mismatch on frozen dataset.",
        }

    def unfreeze_guard(self, manifest: Any) -> Dict[str, Any]:
        """
        Guard against modifying a frozen dataset.
        Returns BLOCKED if frozen, OK otherwise.
        """
        if getattr(manifest, "frozen_at", None):
            return {
                "blocked":    True,
                "status":     "BLOCKED",
                "dataset_id": manifest.dataset_id,
                "reason":     "Dataset is FROZEN. Create a new version to modify.",
            }
        return {"blocked": False, "status": "OK", "dataset_id": manifest.dataset_id}
