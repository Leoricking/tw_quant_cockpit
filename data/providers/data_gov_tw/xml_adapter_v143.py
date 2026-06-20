"""
data/providers/data_gov_tw/xml_adapter_v143.py — XML format adapter v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Handles namespace, repeated item, nested element, attribute, encoding,
    empty element, malformed XML (isolation, not crash).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _strip_ns(tag: str) -> str:
    """Remove XML namespace from tag name."""
    if "{" in tag:
        return tag.split("}", 1)[1]
    return tag


def _element_to_dict(elem: Any) -> Any:
    """Recursively convert an XML element to a dict."""
    tag = _strip_ns(elem.tag)
    result: Dict[str, Any] = {}

    # Attributes
    if elem.attrib:
        result.update({f"@{_strip_ns(k)}": v for k, v in elem.attrib.items()})

    # Children
    children = list(elem)
    if children:
        child_dict: Dict[str, Any] = {}
        for child in children:
            child_tag = _strip_ns(child.tag)
            child_value = _element_to_dict(child)
            if child_tag in child_dict:
                existing = child_dict[child_tag]
                if not isinstance(existing, list):
                    child_dict[child_tag] = [existing]
                child_dict[child_tag].append(child_value)
            else:
                child_dict[child_tag] = child_value
        result.update(child_dict)
    else:
        # Leaf element
        text = (elem.text or "").strip()
        if result:
            if text:
                result["#text"] = text
        else:
            return text if text else None

    return result if result else None


class DataGovTwXmlAdapter:
    """
    Parses XML resources from data.gov.tw datasets.

    Supports:
    - Namespaced elements
    - Repeated item elements → list
    - Nested elements → dict
    - Attributes → @attr_name keys
    - Encoding detection
    - Empty elements → None
    - Malformed XML → error dict, not crash
    """

    def parse(
        self,
        content: bytes,
        record_tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Parse XML bytes. Returns structured result."""
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            return {
                "success": False,
                "error": "xml.etree.ElementTree not available",
                "records": [],
                "record_count": 0,
                "warnings": [],
            }

        try:
            root = ET.fromstring(content)
        except ET.ParseError as exc:
            return {
                "success": False,
                "error": f"XML parse error: {exc}",
                "records": [],
                "record_count": 0,
                "warnings": [str(exc)],
            }

        root_tag = _strip_ns(root.tag)
        children = list(root)

        # If a record_tag is specified, extract matching children
        if record_tag:
            records_raw = [c for c in root.iter() if _strip_ns(c.tag) == record_tag]
        elif children:
            # Try to detect repeated record-like elements
            child_tags = [_strip_ns(c.tag) for c in children]
            if len(set(child_tags)) == 1:
                # All children are same tag → treat as records
                records_raw = children
            else:
                records_raw = [root]
        else:
            records_raw = [root]

        records = []
        warnings: List[str] = []

        for elem in records_raw:
            try:
                rec = _element_to_dict(elem)
                if rec is not None:
                    if not isinstance(rec, dict):
                        rec = {"value": rec}
                    records.append(rec)
            except Exception as exc:
                warnings.append(f"Error converting element: {exc}")

        return {
            "success": True,
            "records": records,
            "record_count": len(records),
            "root_tag": root_tag,
            "warnings": warnings,
            "error": None,
        }
