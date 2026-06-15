"""
governance_rollup/schema_normalizer.py — GovernanceSchemaNormalizer v1.1.9

Normalizes schema values across governance modules for migration/output copies only.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT modify original formal stores.
[!] Does NOT normalize DEMO_ONLY to FORMAL.
[!] Does NOT normalize BLOCKED to COMPLETED.
[!] Does NOT treat missing boolean as True.
[!] UNKNOWN stays UNKNOWN — never guessed.
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

# ---------------------------------------------------------------------------
# Tier mappings
# ---------------------------------------------------------------------------
_TIER_MAP = {
    "research30":  "research30",
    "research_30": "research30",
    "top30":       "research30",
    "research50":  "research50",
    "research_50": "research50",
    "top50":       "research50",
    "universe":    "universe",
    "full":        "universe",
}

# ---------------------------------------------------------------------------
# Qualification mappings — NEVER map DEMO_ONLY or BLOCKED to higher status
# ---------------------------------------------------------------------------
_QUALIFICATION_MAP = {
    "formally_qualified":   "FORMALLY_QUALIFIED",
    "formallyqualified":    "FORMALLY_QUALIFIED",
    "formal":               "FORMALLY_QUALIFIED",
    "not_qualified":        "NOT_QUALIFIED",
    "notqualified":         "NOT_QUALIFIED",
    "not qualified":        "NOT_QUALIFIED",
    "unqualified":          "NOT_QUALIFIED",
    "demo_only":            "DEMO_ONLY",
    "demoonly":             "DEMO_ONLY",
    "demo":                 "DEMO_ONLY",
    "unknown":              "UNKNOWN",
}

# ---------------------------------------------------------------------------
# Priority mappings
# ---------------------------------------------------------------------------
_PRIORITY_MAP = {
    "p0": "P0", "0": "P0",
    "p1": "P1", "1": "P1",
    "p2": "P2", "2": "P2",
    "p3": "P3", "3": "P3",
}

# ---------------------------------------------------------------------------
# Severity mappings
# ---------------------------------------------------------------------------
_SEVERITY_MAP = {
    "critical": "CRITICAL",
    "high":     "HIGH",
    "medium":   "MEDIUM",
    "med":      "MEDIUM",
    "low":      "LOW",
    "info":     "INFO",
    "information": "INFO",
}

# ---------------------------------------------------------------------------
# Reason code normalization
# ---------------------------------------------------------------------------
_KNOWN_REASON_CODES = {
    "NO_DATA", "STALE_DATA", "MISSING_SYMBOL", "CONFLICT", "INVALID_OHLC",
    "IMPORT_FAILURE", "SOURCE_INTERRUPTION", "FORMAL_GATE_BLOCKED",
    "MOCK_DATA", "SYNTHETIC_DATA", "FUTURE_DATE", "DATE_REGRESSION",
    "SCHEMA_MISMATCH", "MISSING_ARTIFACT", "ORPHAN_ARTIFACT",
    "CORRUPTED_STORE", "INDEX_STALE", "AUDIT_CHAIN_BROKEN",
    "SAFETY_MISMATCH", "QUALIFICATION_MISMATCH", "UNKNOWN",
}


class GovernanceSchemaNormalizer:
    """
    Normalizes schema values across governance modules.

    Rules:
    - Does NOT modify original formal stores
    - Only used in migration/output copy
    - Unknown values marked UNKNOWN
    - Does NOT normalize DEMO_ONLY to FORMAL
    - Does NOT normalize BLOCKED to COMPLETED
    - Does NOT treat missing boolean as True
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def normalize_symbol(self, value: Any) -> str:
        """Normalize symbol: strip whitespace, uppercase. Empty -> UNKNOWN."""
        if value is None:
            return "UNKNOWN"
        s = str(value).strip().upper()
        if not s:
            return "UNKNOWN"
        return s

    def normalize_tier(self, value: Any) -> str:
        """Normalize tier to research30/research50/universe/UNKNOWN."""
        if value is None:
            return "UNKNOWN"
        key = str(value).strip().lower().replace("-", "_").replace(" ", "_")
        return _TIER_MAP.get(key, "UNKNOWN")

    def normalize_mode(self, value: Any) -> str:
        """Normalize mode to real/mock/UNKNOWN."""
        if value is None:
            return "UNKNOWN"
        v = str(value).strip().lower()
        if v in ("real", "live", "production"):
            return "real"
        if v in ("mock", "simulation", "demo", "test"):
            return "mock"
        return "UNKNOWN"

    def normalize_status(self, value: Any, domain: str = "general") -> str:
        """Normalize status to uppercase or UNKNOWN. Never promotes BLOCKED."""
        if value is None:
            return "UNKNOWN"
        s = str(value).strip().upper()
        if not s:
            return "UNKNOWN"
        # Never reclassify these
        passthrough = {
            "BLOCKED", "FAILED", "PASS", "WARN", "FAIL", "PENDING",
            "COMPLETED", "CANCELLED", "RUNNING", "ERROR", "UNKNOWN",
            "ACTIVE", "RESOLVED", "SNOOZED", "ESCALATED", "OPEN",
        }
        if s in passthrough:
            return s
        return s  # uppercase fallback for custom values

    def normalize_qualification(self, value: Any) -> str:
        """
        Normalize qualification.
        DEMO_ONLY stays DEMO_ONLY, BLOCKED stays BLOCKED.
        Never promotes lower status to FORMALLY_QUALIFIED.
        """
        if value is None:
            return "UNKNOWN"
        key = str(value).strip().lower().replace("-", "_").replace(" ", "")
        # Special case: BLOCKED is not a qualification, keep as-is
        if key == "blocked":
            return "BLOCKED"
        return _QUALIFICATION_MAP.get(key, "UNKNOWN")

    def normalize_priority(self, value: Any) -> str:
        """Normalize priority to P0/P1/P2/P3/UNKNOWN."""
        if value is None:
            return "UNKNOWN"
        key = str(value).strip().lower().replace("p", "", 1) if str(value).strip().lower().startswith("p") else str(value).strip().lower()
        full_key = str(value).strip().lower()
        return _PRIORITY_MAP.get(full_key, _PRIORITY_MAP.get(key, "UNKNOWN"))

    def normalize_severity(self, value: Any) -> str:
        """Normalize severity to CRITICAL/HIGH/MEDIUM/LOW/INFO/UNKNOWN."""
        if value is None:
            return "UNKNOWN"
        key = str(value).strip().lower()
        return _SEVERITY_MAP.get(key, "UNKNOWN")

    def normalize_reason_codes(self, values: Any) -> List[str]:
        """Normalize a list of reason codes. Unknown codes get UNKNOWN appended."""
        if values is None:
            return []
        if isinstance(values, str):
            values = [values]
        result = []
        for v in values:
            code = str(v).strip().upper()
            if code in _KNOWN_REASON_CODES:
                result.append(code)
            else:
                result.append(f"UNKNOWN:{code}")
        return result

    def normalize_timestamp(self, value: Any) -> Optional[str]:
        """
        Normalize timestamp to ISO-8601 string, or None if unparseable.
        Does not guess missing timestamps.
        """
        if value is None:
            return None
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return value.isoformat()
        s = str(value).strip()
        if not s:
            return None
        # Try common formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(s, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.isoformat()
            except ValueError:
                continue
        logger.debug("normalize_timestamp: could not parse %r", s)
        return None

    def normalize_bool(self, value: Any) -> Optional[bool]:
        """
        Strict bool normalization: True/False/None.
        Missing is NOT treated as True.
        """
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        s = str(value).strip().lower()
        if s in ("true", "1", "yes", "on"):
            return True
        if s in ("false", "0", "no", "off"):
            return False
        return None  # ambiguous — do not guess

    def normalize_identifier(self, value: Any, prefix: str = "") -> str:
        """Normalize an identifier: strip, replace spaces with underscores."""
        if value is None:
            return ""
        s = str(value).strip()
        if not s:
            return ""
        # Remove only clearly invalid chars; keep hyphens and underscores
        s = re.sub(r"[^\w\-.]", "_", s)
        if prefix and not s.startswith(prefix):
            s = f"{prefix}{s}"
        return s

    def normalize_record(self, record: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """
        Normalize a record's fields based on schema_name.
        Unknown fields are preserved as-is with a warning.
        Does not drop unknown fields.
        """
        result = dict(record)
        known_normalizers = {
            "symbol":        self.normalize_symbol,
            "tier":          self.normalize_tier,
            "mode":          lambda v: self.normalize_mode(v),
            "status":        lambda v: self.normalize_status(v),
            "qualification": self.normalize_qualification,
            "priority":      self.normalize_priority,
            "severity":      self.normalize_severity,
        }
        for field_name, normalizer in known_normalizers.items():
            if field_name in result:
                original = result[field_name]
                normalized = normalizer(original)
                if normalized != original:
                    result[field_name] = normalized
                    result[f"_original_{field_name}"] = original

        # Normalize timestamps
        for ts_field in ("created_at", "updated_at", "checked_at", "resolved_at",
                         "last_modified", "timestamp"):
            if ts_field in result:
                original = result[ts_field]
                normalized = self.normalize_timestamp(original)
                if normalized != original:
                    result[ts_field] = normalized
                    result[f"_original_{ts_field}"] = original

        # Normalize booleans — but do NOT set missing to True
        for bool_field in ("research_only", "no_real_orders", "trade_execution_enabled",
                           "auto_repair_enabled", "dry_run"):
            if bool_field in result:
                result[bool_field] = self.normalize_bool(result[bool_field])

        result["_normalized_by"] = "GovernanceSchemaNormalizer"
        result["_schema_name"] = schema_name
        return result

    def validate_normalized(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a normalized record. Returns a dict with:
        - valid: bool
        - issues: list of issue strings
        """
        issues = []
        # Safety flags must not be False
        if record.get("research_only") is False:
            issues.append("research_only is False — safety mismatch")
        if record.get("no_real_orders") is False:
            issues.append("no_real_orders is False — safety mismatch")
        if record.get("trade_execution_enabled") is True:
            issues.append("trade_execution_enabled is True — FORBIDDEN")
        # Impossible states
        status = record.get("status", "")
        qualification = record.get("qualification", "")
        if status == "BLOCKED" and qualification == "FORMALLY_QUALIFIED":
            issues.append("Impossible state: BLOCKED + FORMALLY_QUALIFIED")
        if status == "FAILED" and qualification == "FORMALLY_QUALIFIED":
            issues.append("Impossible state: FAILED + FORMALLY_QUALIFIED")
        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }
