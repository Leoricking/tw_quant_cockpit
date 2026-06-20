"""
data/providers/finmind/schema_drift_v144.py — FinMind schema drift detection v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Additive → ADDITIVE+WARN. Missing required → BLOCKING. Type change → BLOCKING.
[!] Key change → BLOCKING. Save revision hash for tracking.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Dict, List, Optional, Set

from data.providers.finmind.models_v144 import FinMindSchemaDriftStatus
from data.providers.finmind.schema_registry_v144 import FinMindSchemaRegistry

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class FinMindSchemaDriftDetector:
    """
    Detects schema drift in FinMind API responses.
    Missing required fields or type changes are BLOCKING.
    Additive-only drift is WARN (not BLOCKING).
    """

    def __init__(self) -> None:
        self._registry = FinMindSchemaRegistry()
        self._revisions: Dict[str, List[Dict[str, Any]]] = {}

    def detect_drift(
        self,
        dataset: str,
        actual_fields: List[str],
        actual_types: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Detect drift between expected schema and actual response fields.

        Returns dict with:
            status (FinMindSchemaDriftStatus value str),
            added_fields, missing_required, type_changes,
            blocked, drift_hash
        """
        schema = self._registry.get_schema(dataset)
        if schema is None:
            return {
                "dataset": dataset,
                "status": FinMindSchemaDriftStatus.UNKNOWN.value,
                "added_fields": [],
                "missing_required": [],
                "type_changes": [],
                "blocked": True,
                "drift_hash": None,
                "message": "Dataset not in schema registry",
            }

        expected_required: Set[str] = set(schema.get("required_fields", []))
        expected_types: Dict[str, str] = schema.get("field_types", {})
        actual_set: Set[str] = set(actual_fields)
        actual_types = actual_types or {}

        added_fields = sorted(actual_set - set(schema.get("required_fields", [])) - set(schema.get("optional_fields", [])))
        missing_required = sorted(expected_required - actual_set)

        type_changes = []
        for field_name in actual_set:
            if field_name in expected_types and field_name in actual_types:
                if expected_types[field_name] != actual_types[field_name]:
                    type_changes.append({
                        "field": field_name,
                        "expected": expected_types[field_name],
                        "actual": actual_types[field_name],
                    })

        # Determine primary key changes (subset of type_changes + missing_required)
        primary_key_fields = set(schema.get("primary_key", []))
        has_key_change = bool(set(missing_required) & primary_key_fields) or any(
            tc["field"] in primary_key_fields for tc in type_changes
        )

        # Determine status
        if missing_required:
            status = FinMindSchemaDriftStatus.BREAKING_MISSING_FIELD
            blocked = True
        elif type_changes:
            status = FinMindSchemaDriftStatus.BREAKING_TYPE_CHANGE
            blocked = True
        elif has_key_change:
            status = FinMindSchemaDriftStatus.BREAKING_KEY_CHANGE
            blocked = True
        elif added_fields:
            status = FinMindSchemaDriftStatus.ADDITIVE
            blocked = False
            logger.warning("FinMind schema drift ADDITIVE for %s: %s", dataset, added_fields)
        else:
            status = FinMindSchemaDriftStatus.NO_CHANGE
            blocked = False

        # Compute drift hash
        drift_data = {
            "dataset": dataset,
            "actual_fields": sorted(actual_fields),
            "actual_types": {k: actual_types.get(k) for k in sorted(actual_types.keys())},
        }
        drift_hash = hashlib.sha256(
            json.dumps(drift_data, sort_keys=True).encode("utf-8")
        ).hexdigest()[:16]

        return {
            "dataset": dataset,
            "status": status.value,
            "added_fields": added_fields,
            "missing_required": missing_required,
            "type_changes": type_changes,
            "blocked": blocked,
            "drift_hash": drift_hash,
        }

    def save_revision(self, dataset: str, drift_result: Dict[str, Any]) -> None:
        """Save a drift revision for historical tracking."""
        if dataset not in self._revisions:
            self._revisions[dataset] = []
        self._revisions[dataset].append({
            "drift_hash": drift_result.get("drift_hash"),
            "status": drift_result.get("status"),
            "blocked": drift_result.get("blocked"),
        })

    def get_revisions(self, dataset: str) -> List[Dict[str, Any]]:
        """Return revision history for a dataset."""
        return list(self._revisions.get(dataset, []))
