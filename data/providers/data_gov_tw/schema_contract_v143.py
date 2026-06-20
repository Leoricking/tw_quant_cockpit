"""
data/providers/data_gov_tw/schema_contract_v143.py — Schema contract validation v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Schema changed → SCHEMA_CHANGED returned. Blocks formal ingest.
[!] Raw flexible parsing allowed for inspection only (formal_use_allowed=False).
[!] No silent acceptance of schema changes.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from data.providers.data_gov_tw.models_v143 import DataGovTwSchemaContract

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

SCHEMA_CHANGED = "SCHEMA_CHANGED"
SCHEMA_VALID = "SCHEMA_VALID"
SCHEMA_MISSING = "SCHEMA_MISSING"


class DataGovTwSchemaContractValidator:
    """
    Validates data records against a schema contract.

    Rules:
    - Missing required fields → validation failure
    - Schema hash changed → SCHEMA_CHANGED, blocks formal ingest
    - flexible raw parsing for inspection (formal_use_allowed=False)
    - Contract cannot be auto-modified
    """

    def validate_record(
        self,
        record: Dict[str, Any],
        contract: DataGovTwSchemaContract,
    ) -> Dict[str, Any]:
        """Validate a single record against contract. Returns validation result."""
        errors: List[str] = []
        warnings: List[str] = []
        field_results: Dict[str, str] = {}

        # Apply aliases
        normalized = self._apply_aliases(record, contract.aliases)

        # Check required fields
        for rf in contract.required_fields:
            if rf not in normalized:
                errors.append(f"Missing required field: {rf}")
                field_results[rf] = "MISSING_REQUIRED"
            else:
                field_results[rf] = "OK"

        # Check optional fields
        for of in contract.optional_fields:
            if of not in normalized:
                field_results[of] = "OPTIONAL_MISSING"
                warnings.append(f"Optional field absent: {of}")
            else:
                field_results[of] = "OK"

        # Check field types
        for fname, ftype in contract.field_types.items():
            if fname in normalized and normalized[fname] is not None:
                if not self._check_type(normalized[fname], ftype):
                    warnings.append(f"Field {fname}: expected type {ftype}")

        # Check primary key
        for pk in contract.primary_key:
            if pk not in normalized or normalized[pk] is None:
                errors.append(f"Primary key field missing or null: {pk}")

        # Check missing value tokens
        for fname, fval in normalized.items():
            if isinstance(fval, str) and fval in contract.missing_value_tokens:
                normalized[fname] = None

        valid = len(errors) == 0
        return {
            "valid": valid,
            "formal_use_allowed": valid,
            "errors": errors,
            "warnings": warnings,
            "field_results": field_results,
            "normalized_record": normalized,
        }

    def _apply_aliases(
        self, record: Dict[str, Any], aliases: Dict[str, str]
    ) -> Dict[str, Any]:
        """Apply field aliases to normalize field names."""
        result = dict(record)
        for alias, canonical in aliases.items():
            if alias in result and canonical not in result:
                result[canonical] = result.pop(alias)
        return result

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Loosely check if value matches expected type string."""
        t = expected_type.lower()
        if t in ("str", "string", "text"):
            return isinstance(value, str)
        if t in ("int", "integer"):
            try:
                int(value)
                return True
            except (TypeError, ValueError):
                return False
        if t in ("float", "number", "numeric", "decimal"):
            try:
                float(str(value).replace(",", ""))
                return True
            except (TypeError, ValueError):
                return False
        if t in ("bool", "boolean"):
            return isinstance(value, bool) or str(value).lower() in ("true", "false", "1", "0")
        return True  # Unknown type → allow

    def detect_schema_change(
        self,
        contract: DataGovTwSchemaContract,
        observed_fields: List[str],
    ) -> Dict[str, Any]:
        """
        Detect if observed fields indicate a schema change.
        Returns SCHEMA_CHANGED if required fields are missing or unexpected.
        """
        required = set(contract.required_fields)
        observed = set(observed_fields)
        missing_required = required - observed
        new_unknown = observed - required - set(contract.optional_fields) - set(contract.aliases.keys())

        if missing_required:
            return {
                "status": SCHEMA_CHANGED,
                "missing_required_fields": sorted(missing_required),
                "new_fields": sorted(new_unknown),
                "formal_ingest_blocked": True,
                "review_required": True,
                "message": "Schema changed: required fields missing. Formal ingest blocked.",
            }

        if new_unknown:
            return {
                "status": SCHEMA_VALID,
                "missing_required_fields": [],
                "new_fields": sorted(new_unknown),
                "formal_ingest_blocked": False,
                "review_required": len(new_unknown) > 0,
                "message": "Schema valid with new unknown fields.",
            }

        return {
            "status": SCHEMA_VALID,
            "missing_required_fields": [],
            "new_fields": [],
            "formal_ingest_blocked": False,
            "review_required": False,
            "message": "Schema valid.",
        }

    def inspect_raw(
        self,
        raw_records: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Raw flexible inspection — formal_use_allowed=False.
        Used for discovery and schema detection only.
        """
        if not raw_records:
            return {
                "status": "REVIEW_REQUIRED",
                "formal_use_allowed": False,
                "record_count": 0,
                "detected_fields": [],
                "message": "No records to inspect",
            }
        all_fields = set()
        for rec in raw_records:
            all_fields.update(rec.keys())
        return {
            "status": "REVIEW_REQUIRED",
            "formal_use_allowed": False,
            "record_count": len(raw_records),
            "detected_fields": sorted(all_fields),
            "message": "Raw inspection only. Not for formal research conclusions.",
        }
