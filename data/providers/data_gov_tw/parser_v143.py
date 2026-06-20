"""
data/providers/data_gov_tw/parser_v143.py — Base parser for data.gov.tw v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Routes to format-specific adapter based on detected content type.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataGovTwParser:
    """
    Base parser that dispatches to format-specific adapters.
    Supported: JSON, CSV, XML, ZIP, OAS.
    """

    def parse(
        self,
        content: bytes,
        format_hint: Optional[str] = None,
        encoding: Optional[str] = None,
        schema_contract=None,
    ) -> Dict[str, Any]:
        """Parse content bytes based on format hint or auto-detection."""
        detected_format = self._detect_format(content, format_hint)

        if detected_format == "JSON":
            from data.providers.data_gov_tw.json_adapter_v143 import DataGovTwJsonAdapter
            return DataGovTwJsonAdapter().parse(content, encoding=encoding or "utf-8")

        if detected_format == "CSV":
            from data.providers.data_gov_tw.csv_adapter_v143 import DataGovTwCsvAdapter
            return DataGovTwCsvAdapter().parse(content, encoding=encoding)

        if detected_format == "XML":
            from data.providers.data_gov_tw.xml_adapter_v143 import DataGovTwXmlAdapter
            return DataGovTwXmlAdapter().parse(content)

        if detected_format == "ZIP":
            from data.providers.data_gov_tw.zip_adapter_v143 import DataGovTwZipAdapter
            return DataGovTwZipAdapter().safe_extract_to_memory(content)

        return {
            "success": False,
            "error": f"Unsupported or unrecognized format: {format_hint or 'unknown'}",
            "records": [],
            "record_count": 0,
            "warnings": [f"Format not supported: {detected_format}"],
            "detected_format": detected_format,
        }

    def _detect_format(self, content: bytes, hint: Optional[str]) -> str:
        if hint:
            return hint.upper().strip()
        # Auto-detect from content signature
        stripped = content.lstrip(b"\xef\xbb\xbf \t\r\n")
        if stripped.startswith(b"{") or stripped.startswith(b"["):
            return "JSON"
        if stripped.startswith(b"PK\x03\x04"):
            return "ZIP"
        if stripped.startswith(b"<"):
            return "XML"
        # Try CSV heuristic
        try:
            line = content.split(b"\n", 1)[0].decode("utf-8", errors="ignore")
            if "," in line or "\t" in line:
                return "CSV"
        except Exception:
            pass
        return "UNKNOWN"
