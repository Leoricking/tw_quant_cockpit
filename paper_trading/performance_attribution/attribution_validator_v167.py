"""
paper_trading/performance_attribution/attribution_validator_v167.py
Input validator for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Comprehensive validation: duplicates, timestamps, invalid values, real markers, secrets.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Set

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

# Fields that indicate real/live/production attribution (must be absent or False)
_REAL_FIELDS = frozenset({
    "broker_session", "real_account_token", "api_secret", "password",
    "credential", "real_order_handle", "production_db_connection",
    "bank_account", "real_capital_control", "live_execution",
    "is_live", "is_real", "is_production", "live_mode", "real_mode",
    "production_mode", "broker_mode", "production_trading_enabled",
    "broker_execution_enabled", "real_order_creation_enabled",
    "real_order_execution_enabled", "live_account_sync_enabled",
    "shioaji_login", "broker_api_key",
})


class AttributionValidator:
    """
    Validates attribution inputs, models, and fixtures.
    Returns validation results with explicit error/warning lists.
    Never silently passes real-order or production fields.
    """

    def validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Full validation of an attribution input dict."""
        errors: List[str] = []
        warnings: List[str] = []
        blocked: bool = False

        # Real/live/production fields
        for field in _REAL_FIELDS:
            if field in data and data[field] not in (None, False, ""):
                errors.append(f"blocked_real_field: {field}={data[field]!r}")
                blocked = True

        # Timestamp validation
        for ts_field in ("attribution_period_start", "attribution_period_end", "created_at"):
            val = data.get(ts_field)
            if val is not None:
                try:
                    from datetime import datetime
                    if isinstance(val, str) and len(val) >= 10:
                        datetime.fromisoformat(val[:10])
                except (ValueError, TypeError):
                    errors.append(f"invalid_timestamp: {ts_field}={val!r}")

        # Period reversal
        start = data.get("attribution_period_start", "")
        end = data.get("attribution_period_end", "")
        if start and end and start > end:
            errors.append(f"reversed_period: {start} > {end}")

        # Duplicate check for trade IDs
        trades = data.get("trades", [])
        if isinstance(trades, list):
            seen: Set[str] = set()
            for t in trades:
                tid = t.get("trade_id") if isinstance(t, dict) else None
                if tid:
                    if tid in seen:
                        errors.append(f"duplicate_trade_id: {tid}")
                    seen.add(tid)

        # Duplicate check for execution IDs
        execs = data.get("executions", [])
        if isinstance(execs, list):
            seen_execs: Set[str] = set()
            for e in execs:
                eid = e.get("execution_id") if isinstance(e, dict) else None
                if eid:
                    if eid in seen_execs:
                        errors.append(f"duplicate_execution_id: {eid}")
                    seen_execs.add(eid)

        # Invalid quantities
        for t in (trades if isinstance(trades, list) else []):
            qty = t.get("quantity") if isinstance(t, dict) else None
            if qty is not None and (not isinstance(qty, (int, float)) or qty == 0):
                errors.append(f"invalid_quantity: trade={t.get('trade_id')} qty={qty}")

        # Initial equity
        init_eq = data.get("initial_equity")
        if init_eq is not None and isinstance(init_eq, (int, float)) and init_eq <= 0:
            errors.append(f"invalid_initial_equity: {init_eq}")

        # Benchmark mode + missing benchmark
        bm_mode = data.get("benchmark_mode", "NONE")
        bm_id = data.get("benchmark_id")
        if bm_mode in ("MARKET_BENCHMARK", "POLICY_BASELINE") and not bm_id:
            errors.append(f"missing_benchmark_id: mode={bm_mode} requires benchmark_id")

        # Safety marker check
        for marker in ("paper_only", "research_only", "no_real_orders", "not_for_production"):
            if data.get(marker) is not True:
                errors.append(f"missing_safety_marker: {marker} must be True")

        valid = len(errors) == 0
        return {
            "valid": valid,
            "blocked": blocked or not valid,
            "errors": errors,
            "warnings": warnings,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    def validate_trade(self, trade: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single trade record."""
        errors: List[str] = []
        if not trade.get("trade_id"):
            errors.append("missing_trade_id")
        qty = trade.get("quantity")
        if qty is None or not isinstance(qty, (int, float)) or qty == 0:
            errors.append(f"invalid_quantity: {qty}")
        fp = trade.get("fill_price")
        if fp is None or not isinstance(fp, (int, float)) or fp <= 0:
            errors.append(f"invalid_fill_price: {fp}")
        if not trade.get("simulated", True):
            errors.append("blocked: simulated must be True for paper attribution")
        return {"valid": len(errors) == 0, "errors": errors}

    def validate_execution(self, execution: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single execution record."""
        errors: List[str] = []
        if not execution.get("execution_id"):
            errors.append("missing_execution_id")
        if not execution.get("simulated", True):
            errors.append("blocked: simulated must be True for paper attribution")
        if not execution.get("model_version"):
            errors.append("missing_model_version: paper execution must record model_version")
        return {"valid": len(errors) == 0, "errors": errors}

    def validate_fixture(self, fixture: Dict[str, Any]) -> Dict[str, Any]:
        """Validate fixture safety markers and required fields."""
        errors: List[str] = []
        required_markers = {
            "test_fixture": True,
            "demo_only": True,
            "paper_only": True,
            "research_only": True,
            "not_live": True,
            "no_broker": True,
            "no_real_account": True,
            "no_real_orders": True,
            "not_for_production": True,
            "paper_attribution_only": True,
        }
        for key, expected in required_markers.items():
            if key not in fixture:
                errors.append(f"missing_marker: {key}")
            elif fixture[key] is not True:
                errors.append(f"invalid_marker: {key}={fixture[key]!r} expected True")
        if not fixture.get("fixture_id"):
            errors.append("missing_fixture_id")
        if not fixture.get("purpose"):
            errors.append("missing_purpose")
        return {"valid": len(errors) == 0, "errors": errors}
