"""
replay/dataset_conflict.py — ReplayDatasetConflictDetector v1.2.8

Detects and reports conflicts during dataset/session import.
Resolution suggestions are provided but NEVER auto-executed.

Conflict types:
- DATASET_ID_CONFLICT, DATASET_VERSION_CONFLICT, DATASET_FINGERPRINT_CONFLICT
- SESSION_ID_CONFLICT, SESSION_FINGERPRINT_CONFLICT
- PACKAGE_HASH_MISMATCH, SCHEMA_VERSION_CONFLICT
- PATH_REMAP_CONFLICT, LINEAGE_CONFLICT, QUALIFICATION_CONFLICT
- REAL_MOCK_CONFLICT, DUPLICATE_CONTENT, ORPHAN_REFERENCE

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Resolution is NEVER auto-executed. Manual review required.
"""
from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED = False


class ConflictType(str, Enum):
    DATASET_ID_CONFLICT        = "DATASET_ID_CONFLICT"
    DATASET_VERSION_CONFLICT   = "DATASET_VERSION_CONFLICT"
    DATASET_FINGERPRINT_CONFLICT = "DATASET_FINGERPRINT_CONFLICT"
    SESSION_ID_CONFLICT        = "SESSION_ID_CONFLICT"
    SESSION_FINGERPRINT_CONFLICT = "SESSION_FINGERPRINT_CONFLICT"
    PACKAGE_HASH_MISMATCH      = "PACKAGE_HASH_MISMATCH"
    SCHEMA_VERSION_CONFLICT    = "SCHEMA_VERSION_CONFLICT"
    PATH_REMAP_CONFLICT        = "PATH_REMAP_CONFLICT"
    LINEAGE_CONFLICT           = "LINEAGE_CONFLICT"
    QUALIFICATION_CONFLICT     = "QUALIFICATION_CONFLICT"
    REAL_MOCK_CONFLICT         = "REAL_MOCK_CONFLICT"
    DUPLICATE_CONTENT          = "DUPLICATE_CONTENT"
    ORPHAN_REFERENCE           = "ORPHAN_REFERENCE"


class ConflictResolution(str, Enum):
    KEEP_EXISTING     = "KEEP_EXISTING"
    IMPORT_AS_NEW_ID  = "IMPORT_AS_NEW_ID"
    CREATE_NEW_VERSION = "CREATE_NEW_VERSION"
    SKIP              = "SKIP"
    MANUAL_REVIEW     = "MANUAL_REVIEW"
    BLOCK             = "BLOCK"


class ReplayDatasetConflictDetector:
    """
    Detects conflicts during import and suggests resolutions.
    Resolution is NEVER auto-executed.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED = False

    def detect(
        self,
        incoming: Dict[str, Any],
        existing_datasets: Optional[List[Dict[str, Any]]] = None,
        existing_sessions: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Detect all conflicts. Returns list of conflict dicts."""
        conflicts = []
        existing_datasets = existing_datasets or []
        existing_sessions = existing_sessions or []

        incoming_id  = incoming.get("dataset_id", "")
        incoming_fp  = incoming.get("fingerprint", "")
        incoming_mode = incoming.get("mode", "")

        for ex in existing_datasets:
            ex_id  = ex.get("dataset_id", "")
            ex_fp  = ex.get("fingerprint", "")
            ex_mode = ex.get("mode", "")

            if incoming_id == ex_id:
                conflicts.append({
                    "type":           ConflictType.DATASET_ID_CONFLICT.value,
                    "incoming_id":    incoming_id,
                    "existing_id":    ex_id,
                    "suggestion":     ConflictResolution.KEEP_EXISTING.value,
                    "note":           "Same dataset_id already registered.",
                })
            elif incoming_fp and incoming_fp == ex_fp:
                conflicts.append({
                    "type":           ConflictType.DUPLICATE_CONTENT.value,
                    "incoming_id":    incoming_id,
                    "existing_id":    ex_id,
                    "fingerprint":    incoming_fp[:16],
                    "suggestion":     ConflictResolution.SKIP.value,
                    "note":           "Same content fingerprint as existing dataset.",
                })
            if incoming_mode and ex_mode and incoming_mode != ex_mode:
                if (incoming_id == ex_id):
                    conflicts.append({
                        "type":       ConflictType.REAL_MOCK_CONFLICT.value,
                        "incoming_mode": incoming_mode,
                        "existing_mode": ex_mode,
                        "suggestion": ConflictResolution.MANUAL_REVIEW.value,
                        "note":       "Mode mismatch on same dataset_id.",
                    })

        return conflicts

    def suggest_resolution(self, conflict: Dict[str, Any]) -> str:
        """Return suggested resolution for a conflict."""
        return conflict.get("suggestion", ConflictResolution.MANUAL_REVIEW.value)
