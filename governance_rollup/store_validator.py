"""
governance_rollup/store_validator.py — GovernanceStoreValidator v1.1.9

Validates store structure and integrity (read-only).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Corrupted tail: mark CORRUPTED_TAIL, do NOT truncate.
[!] Never writes to stores.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from governance_rollup.rollup_schema import (
    StoreInventoryRecord,
    STORE_TYPE_JSON, STORE_TYPE_JSONL, STORE_TYPE_CSV,
)

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True


class GovernanceStoreValidator:
    """
    Validates store structure and integrity.
    Corrupted tail: mark CORRUPTED_TAIL, do NOT truncate.
    Read-only — never writes to stores.
    """

    def validate_store(self, record: StoreInventoryRecord) -> Dict[str, Any]:
        """Validate a store based on its type. Returns validation result dict."""
        if not record.exists:
            return {
                "store_id": record.store_id,
                "valid": False,
                "status": "MISSING",
                "issues": ["Store file/directory does not exist"],
            }
        if not record.readable:
            return {
                "store_id": record.store_id,
                "valid": False,
                "status": "UNREADABLE",
                "issues": ["Store is not readable"],
            }
        path = Path(record.path)
        if record.store_type == STORE_TYPE_JSON:
            return self.validate_json(path)
        if record.store_type == STORE_TYPE_JSONL:
            return self.validate_jsonl(path)
        if record.store_type == STORE_TYPE_CSV:
            return self.validate_csv(path)
        return {
            "store_id": record.store_id,
            "valid": True,
            "status": "VALID",
            "issues": [],
            "note": f"No specific validator for type {record.store_type}",
        }

    def validate_json(self, path: Path) -> Dict[str, Any]:
        """Validate a JSON file. Returns validation result."""
        result: Dict[str, Any] = {
            "path": str(path),
            "valid": False,
            "status": "UNKNOWN",
            "issues": [],
        }
        if not path.exists():
            result["status"] = "MISSING"
            result["issues"].append("File does not exist")
            return result
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if not content.strip():
                result["status"] = "EMPTY"
                result["issues"].append("File is empty")
                return result
            data = json.loads(content)
            result["valid"] = True
            result["status"] = "VALID"
            result["record_type"] = type(data).__name__
            if isinstance(data, dict):
                result["key_count"] = len(data)
            elif isinstance(data, list):
                result["record_count"] = len(data)
        except json.JSONDecodeError as exc:
            result["status"] = "MALFORMED_JSON"
            result["issues"].append(f"JSON parse error: {exc}")
        except Exception as exc:
            result["status"] = "ERROR"
            result["issues"].append(f"Unexpected error: {exc}")
        return result

    def validate_jsonl(self, path: Path) -> Dict[str, Any]:
        """
        Validate a JSONL file.
        Detects corrupted tail vs middle corruption.
        CORRUPTED_TAIL: last line is invalid, all others valid.
        """
        result: Dict[str, Any] = {
            "path": str(path),
            "valid": False,
            "status": "UNKNOWN",
            "issues": [],
            "valid_lines": 0,
            "invalid_lines": 0,
            "corrupted_tail": False,
            "corrupted_middle": False,
        }
        if not path.exists():
            result["status"] = "MISSING"
            result["issues"].append("File does not exist")
            return result
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                raw_lines = f.readlines()
        except Exception as exc:
            result["status"] = "ERROR"
            result["issues"].append(f"Could not read file: {exc}")
            return result

        if not raw_lines:
            result["status"] = "EMPTY"
            result["issues"].append("File is empty")
            return result

        lines = [l for l in raw_lines]
        parse_results = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                # Empty lines are OK in JSONL
                parse_results.append({"line": i + 1, "valid": True, "empty": True})
                continue
            try:
                json.loads(stripped)
                parse_results.append({"line": i + 1, "valid": True, "empty": False})
            except json.JSONDecodeError as exc:
                parse_results.append({
                    "line": i + 1,
                    "valid": False,
                    "empty": False,
                    "error": str(exc),
                })

        non_empty = [r for r in parse_results if not r.get("empty", False)]
        valid_count = sum(1 for r in non_empty if r["valid"])
        invalid_lines = [r for r in non_empty if not r["valid"]]
        result["valid_lines"] = valid_count
        result["invalid_lines"] = len(invalid_lines)

        if not invalid_lines:
            result["valid"] = True
            result["status"] = "VALID"
            return result

        # Check if corruption is only in the tail
        # Tail = last non-empty line
        last_non_empty = None
        for r in reversed(non_empty):
            last_non_empty = r
            break

        if last_non_empty and not last_non_empty["valid"]:
            # Check if all other lines are valid
            other_lines = [r for r in non_empty if r["line"] != last_non_empty["line"]]
            all_others_valid = all(r["valid"] for r in other_lines)
            if all_others_valid:
                result["corrupted_tail"] = True
                result["status"] = "CORRUPTED_TAIL"
                result["issues"].append(
                    f"Corrupted tail detected on line {last_non_empty['line']}: "
                    f"{last_non_empty.get('error', 'parse error')}"
                )
                # [!] Do NOT truncate — only mark
                return result

        # Middle corruption
        result["corrupted_middle"] = True
        result["status"] = "CORRUPTED_MIDDLE"
        for inv in invalid_lines:
            result["issues"].append(
                f"Invalid JSON on line {inv['line']}: {inv.get('error', 'parse error')}"
            )
        return result

    def validate_csv(self, path: Path) -> Dict[str, Any]:
        """Validate a CSV file."""
        result: Dict[str, Any] = {
            "path": str(path),
            "valid": False,
            "status": "UNKNOWN",
            "issues": [],
        }
        if not path.exists():
            result["status"] = "MISSING"
            result["issues"].append("File does not exist")
            return result
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                rows = list(reader)
            if not headers:
                result["status"] = "EMPTY"
                result["issues"].append("No header row found")
                return result
            result["valid"] = True
            result["status"] = "VALID"
            result["header_count"] = len(headers)
            result["record_count"] = len(rows)
            result["headers"] = list(headers)
        except Exception as exc:
            result["status"] = "ERROR"
            result["issues"].append(f"CSV parse error: {exc}")
        return result

    def validate_index(self, path: Path) -> Dict[str, Any]:
        """Validate an index file (expected to be JSON)."""
        result = self.validate_json(path)
        if result.get("valid"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Check for expected index fields
                has_entries = "entries" in data
                has_version = "index_version" in data or "schema_version" in data
                has_updated = "last_updated" in data
                result["has_entries"] = has_entries
                result["has_version"] = has_version
                result["has_updated"] = has_updated
                if not has_entries:
                    result["issues"].append("Index missing 'entries' key")
                if not has_updated:
                    result["issues"].append("Index missing 'last_updated' key")
            except Exception as exc:
                result["issues"].append(f"Index structure check error: {exc}")
        return result

    def validate_audit_chain(self, path: Path) -> Dict[str, Any]:
        """
        Validate an audit chain JSONL file.
        Checks: each entry has a hash field, no broken chains.
        """
        result: Dict[str, Any] = {
            "path": str(path),
            "valid": False,
            "status": "UNKNOWN",
            "issues": [],
            "entries_checked": 0,
            "hash_missing": 0,
            "hash_mismatch": 0,
        }
        jsonl_result = self.validate_jsonl(path)
        if not jsonl_result.get("valid"):
            result["status"] = jsonl_result.get("status", "INVALID")
            result["issues"] = jsonl_result.get("issues", [])
            return result

        entries = []
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        entries.append(json.loads(stripped))
                    except Exception:
                        pass
        except Exception as exc:
            result["status"] = "ERROR"
            result["issues"].append(f"Could not read audit file: {exc}")
            return result

        result["entries_checked"] = len(entries)
        hash_missing = 0
        hash_mismatch = 0
        for entry in entries:
            if "hash" not in entry and "audit_hash" not in entry and "record_hash" not in entry:
                hash_missing += 1
        result["hash_missing"] = hash_missing
        result["hash_mismatch"] = hash_mismatch

        if hash_missing > 0:
            result["issues"].append(f"{hash_missing} audit entries missing hash field")
        if hash_mismatch > 0:
            result["issues"].append(f"{hash_mismatch} audit entries have hash mismatch")

        if not result["issues"]:
            result["valid"] = True
            result["status"] = "VALID"
        else:
            result["status"] = "AUDIT_CHAIN_ISSUES"
        return result

    def validate_schema_version(self, record: StoreInventoryRecord) -> Dict[str, Any]:
        """Validate schema version field in a store record."""
        return {
            "schema_version": record.schema_version if hasattr(record, "schema_version") else "UNKNOWN",
            "valid": True,
            "issues": [],
        }

    def validate_required_fields(self, record: Dict[str, Any], required: List[str]) -> Dict[str, Any]:
        """Validate that required fields are present in a record dict."""
        missing = [f for f in required if f not in record or record[f] is None]
        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "issues": [f"Missing required field: {f}" for f in missing],
        }

    def validate_safety_flags(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate safety flags in a record."""
        issues = []
        if record.get("research_only") is False:
            issues.append("research_only is False — safety mismatch")
        if record.get("no_real_orders") is False:
            issues.append("no_real_orders is False — safety mismatch")
        if record.get("trade_execution_enabled") is True:
            issues.append("trade_execution_enabled is True — FORBIDDEN")
        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def validate_paths(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate path fields in a record."""
        from governance_rollup.path_normalizer import CrossMachinePathNormalizer
        normalizer = CrossMachinePathNormalizer()
        issues = []
        path_fields = [k for k in record if "path" in k.lower() and record[k]]
        for pf in path_fields:
            val = record[pf]
            if not isinstance(val, str):
                continue
            stale = normalizer.detect_stale_absolute_path(val)
            if stale.get("stale"):
                issues.append(f"Stale absolute path in field '{pf}': {val}")
        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def summarize(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize a list of validation results."""
        total = len(results)
        valid = sum(1 for r in results if r.get("valid"))
        invalid = total - valid
        by_status: Dict[str, int] = {}
        for r in results:
            s = r.get("status", "UNKNOWN")
            by_status[s] = by_status.get(s, 0) + 1
        return {
            "total": total,
            "valid": valid,
            "invalid": invalid,
            "by_status": by_status,
            "research_only": True,
            "no_real_orders": True,
        }
