"""
data/providers/data_gov_tw/json_adapter_v143.py — JSON format adapter v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Handles list root, object root, nested records, pagination, null, numeric string,
    ISO date, ROC date, unknown fields (forward-compatible).
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_ROC_DATE_RE = re.compile(r"^(\d{2,3})/(\d{1,2})/(\d{1,2})$")


def _parse_roc_date(s: str) -> Optional[str]:
    """Convert ROC date (e.g. '113/06/01') to ISO '2024-06-01'."""
    m = _ROC_DATE_RE.match(s.strip())
    if m:
        year = int(m.group(1)) + 1911
        month = int(m.group(2))
        day = int(m.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"
    return None


def _normalize_value(v: Any) -> Any:
    """Try to normalize a value: numeric strings → float/int, ROC dates."""
    if v is None:
        return None
    if isinstance(v, (bool, int, float)):
        return v
    if isinstance(v, str):
        stripped = v.strip()
        if not stripped:
            return None
        # Try ROC date
        roc = _parse_roc_date(stripped)
        if roc:
            return roc
        # Try numeric string
        clean = stripped.replace(",", "")
        try:
            if "." in clean:
                return float(clean)
            return int(clean)
        except ValueError:
            return stripped
    return v


class DataGovTwJsonAdapter:
    """
    Parses JSON resources from data.gov.tw datasets.

    Supports:
    - List root: [{...}, {...}]
    - Object root with records key: {"data": [...]} or {"result": {..., "records": [...]}}
    - Nested records
    - Pagination metadata
    - Null, numeric string, ISO date, ROC date
    - Unknown fields (forward compatible)
    - Malformed JSON → returns error, does not crash
    """

    def parse(
        self,
        content: bytes,
        encoding: str = "utf-8",
        normalize_values: bool = True,
        records_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Parse JSON bytes. Returns structured result with records and metadata."""
        try:
            text = content.decode(encoding, errors="replace")
            data = json.loads(text)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
            return {
                "success": False,
                "error": f"JSON parse error: {exc}",
                "records": [],
                "record_count": 0,
                "pagination": {},
                "warnings": [str(exc)],
            }

        return self._extract(data, normalize_values, records_key)

    def parse_str(
        self,
        text: str,
        normalize_values: bool = True,
        records_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Parse JSON string."""
        try:
            data = json.loads(text)
        except (json.JSONDecodeError, ValueError) as exc:
            return {
                "success": False,
                "error": f"JSON parse error: {exc}",
                "records": [],
                "record_count": 0,
                "pagination": {},
                "warnings": [str(exc)],
            }
        return self._extract(data, normalize_values, records_key)

    def _extract(
        self,
        data: Any,
        normalize_values: bool,
        records_key: Optional[str],
    ) -> Dict[str, Any]:
        warnings: List[str] = []
        pagination: Dict[str, Any] = {}

        # List root
        if isinstance(data, list):
            records = data

        # Object root
        elif isinstance(data, dict):
            # Try explicit records_key
            if records_key and records_key in data:
                records = data[records_key]
                if not isinstance(records, list):
                    records = [records]
            # Try common patterns
            elif "records" in data:
                records = data["records"]
                pagination = {k: v for k, v in data.items() if k != "records"}
            elif "data" in data and isinstance(data["data"], list):
                records = data["data"]
                pagination = {k: v for k, v in data.items() if k != "data"}
            elif "result" in data and isinstance(data["result"], dict):
                inner = data["result"]
                if "records" in inner:
                    records = inner["records"]
                    pagination = {k: v for k, v in inner.items() if k != "records"}
                else:
                    records = [inner]
            elif "items" in data and isinstance(data["items"], list):
                records = data["items"]
                pagination = {k: v for k, v in data.items() if k != "items"}
            else:
                # Single object
                records = [data]
        else:
            warnings.append(f"Unexpected JSON root type: {type(data).__name__}")
            records = []

        if not isinstance(records, list):
            warnings.append("Records extracted but not a list — wrapping")
            records = [records] if records else []

        # Normalize values
        if normalize_values:
            processed = []
            for rec in records:
                if isinstance(rec, dict):
                    processed.append({k: _normalize_value(v) for k, v in rec.items()})
                else:
                    processed.append(rec)
                    warnings.append("Non-dict record found in list")
            records = processed

        return {
            "success": True,
            "records": records,
            "record_count": len(records),
            "pagination": pagination,
            "warnings": warnings,
            "error": None,
        }
