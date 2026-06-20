"""
data/providers/data_gov_tw/csv_adapter_v143.py — CSV format adapter v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Handles UTF-8, UTF-8 BOM, Big5, quoted comma, multiline, duplicate header,
    empty row, malformed row isolation.
"""
from __future__ import annotations

import csv
import io
from typing import Any, Dict, List, Optional, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_ENCODINGS_TO_TRY = ["utf-8-sig", "utf-8", "big5", "cp950", "gbk"]


def _try_decode(content: bytes, encoding: Optional[str] = None) -> Tuple[str, str]:
    """Attempt to decode bytes. Returns (text, detected_encoding)."""
    if encoding:
        try:
            return content.decode(encoding, errors="strict"), encoding
        except (UnicodeDecodeError, LookupError):
            pass
    for enc in _ENCODINGS_TO_TRY:
        try:
            return content.decode(enc, errors="strict"), enc
        except (UnicodeDecodeError, LookupError):
            pass
    return content.decode("utf-8", errors="replace"), "utf-8-fallback"


class DataGovTwCsvAdapter:
    """
    Parses CSV resources from data.gov.tw datasets.

    Supports:
    - UTF-8, UTF-8 BOM (utf-8-sig), Big5/CP950
    - Quoted comma fields
    - Multiline fields
    - Duplicate header columns → renamed with _N suffix
    - Empty rows → skipped
    - Malformed rows → isolated (counted, not fatal)
    """

    def parse(
        self,
        content: bytes,
        encoding: Optional[str] = None,
        delimiter: str = ",",
        skip_empty: bool = True,
    ) -> Dict[str, Any]:
        """Parse CSV bytes. Returns structured result."""
        warnings: List[str] = []

        text, detected_encoding = _try_decode(content, encoding)

        try:
            reader = csv.reader(io.StringIO(text), delimiter=delimiter)
            rows = list(reader)
        except Exception as exc:
            return {
                "success": False,
                "error": f"CSV parse error: {exc}",
                "records": [],
                "record_count": 0,
                "detected_encoding": detected_encoding,
                "warnings": [str(exc)],
            }

        if not rows:
            return {
                "success": True,
                "records": [],
                "record_count": 0,
                "detected_encoding": detected_encoding,
                "warnings": ["Empty CSV file"],
                "error": None,
            }

        # Extract and deduplicate headers
        raw_headers = rows[0]
        headers = self._deduplicate_headers(raw_headers, warnings)

        records: List[Dict[str, Any]] = []
        malformed: int = 0

        for row_num, row in enumerate(rows[1:], start=2):
            # Skip empty rows
            if skip_empty and not any(cell.strip() for cell in row):
                continue

            if len(row) == len(headers):
                record = {h: (v if v.strip() != "" else None) for h, v in zip(headers, row)}
                records.append(record)
            elif len(row) < len(headers):
                # Pad with None
                padded = row + [None] * (len(headers) - len(row))
                record = {h: (v if v is not None and v.strip() != "" else None)
                          for h, v in zip(headers, padded)}
                records.append(record)
                warnings.append(f"Row {row_num}: fewer columns than header, padded with None")
            else:
                # More columns than headers → malformed, isolate
                malformed += 1
                warnings.append(f"Row {row_num}: more columns than header, row isolated")

        if malformed:
            warnings.append(f"Total malformed rows isolated: {malformed}")

        return {
            "success": True,
            "records": records,
            "record_count": len(records),
            "detected_encoding": detected_encoding,
            "headers": headers,
            "malformed_rows": malformed,
            "warnings": warnings,
            "error": None,
        }

    def _deduplicate_headers(
        self, raw_headers: List[str], warnings: List[str]
    ) -> List[str]:
        """Deduplicate header names by appending _N suffix."""
        seen: Dict[str, int] = {}
        result: List[str] = []
        for h in raw_headers:
            h = h.strip() if h else ""
            if h in seen:
                seen[h] += 1
                new_h = f"{h}_{seen[h]}"
                warnings.append(f"Duplicate header '{h}' renamed to '{new_h}'")
                result.append(new_h)
            else:
                seen[h] = 0
                result.append(h)
        return result
