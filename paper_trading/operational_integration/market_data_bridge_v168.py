"""
paper_trading/operational_integration/market_data_bridge_v168.py
Market Data Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_REQUIRED_MD_FIELDS = ["symbol", "timestamp", "open", "high", "low", "close", "volume"]


class MarketDataBridge:
    """Validates and maps market data across integration. Research only."""

    def check_freshness(self, data_record: Dict[str, Any], max_age_seconds: float) -> Dict[str, Any]:
        """Check if market data is fresh enough."""
        ts = data_record.get("timestamp", "")
        if not ts:
            return {"fresh": False, "reason": "missing_timestamp", "paper_only": True}
        now = datetime.now(timezone.utc)
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age = (now - dt).total_seconds()
            fresh = age <= max_age_seconds
            return {
                "fresh": fresh,
                "age_seconds": age,
                "max_age_seconds": max_age_seconds,
                "timestamp": ts,
                "paper_only": True,
            }
        except Exception as e:
            return {"fresh": False, "reason": f"parse_error: {e}", "paper_only": True}

    def check_provider_lineage(self, data_record: Dict[str, Any]) -> Dict[str, Any]:
        """Verify that data record has valid provider lineage."""
        provider = data_record.get("provider", "")
        lineage = data_record.get("source_lineage", "") or data_record.get("lineage_id", "")
        return {
            "has_provider": bool(provider),
            "has_lineage": bool(lineage),
            "provider": provider,
            "lineage": lineage,
            "valid": bool(provider) and bool(lineage),
            "paper_only": True,
        }

    def check_session_compatibility(
        self, data_record: Dict[str, Any], session_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check if market data is compatible with session configuration."""
        issues = []
        data_tz = data_record.get("timezone", "Asia/Taipei")
        session_tz = session_config.get("timezone", "Asia/Taipei")
        if data_tz != session_tz:
            issues.append(f"timezone_mismatch: data={data_tz} session={session_tz}")

        data_symbol = data_record.get("symbol", "")
        session_universe = session_config.get("universe", [])
        if session_universe and data_symbol not in session_universe:
            issues.append(f"symbol_not_in_universe: {data_symbol}")

        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "paper_only": True,
        }

    def map_schema(
        self, source_record: Dict[str, Any], target_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map source record fields to target schema, returning mapped record."""
        mapped = {}
        missing = []
        for target_field, source_field in target_schema.items():
            if isinstance(source_field, str) and source_field in source_record:
                mapped[target_field] = source_record[source_field]
            elif target_field in source_record:
                mapped[target_field] = source_record[target_field]
            else:
                missing.append(target_field)
        return {
            "mapped": mapped,
            "missing_fields": missing,
            "complete": len(missing) == 0,
            "paper_only": True,
        }

    def handle_missing_fields(
        self, data_record: Dict[str, Any], required_fields: List[str]
    ) -> Dict[str, Any]:
        """Identify and report missing required fields."""
        missing = [f for f in required_fields if f not in data_record]
        return {
            "missing": missing,
            "complete": len(missing) == 0,
            "total_required": len(required_fields),
            "found_required": len(required_fields) - len(missing),
            "paper_only": True,
        }

    def summarize(self, data_record: Dict[str, Any]) -> Dict[str, Any]:
        """Return a summary of market data record completeness."""
        present = [f for f in _REQUIRED_MD_FIELDS if f in data_record]
        missing = [f for f in _REQUIRED_MD_FIELDS if f not in data_record]
        return {
            "symbol": data_record.get("symbol", ""),
            "timestamp": data_record.get("timestamp", ""),
            "required_fields_present": len(present),
            "required_fields_missing": missing,
            "has_source_lineage": bool(data_record.get("source_lineage")),
            "paper_only": True,
        }
