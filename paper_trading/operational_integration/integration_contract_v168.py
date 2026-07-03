"""
paper_trading/operational_integration/integration_contract_v168.py
Integration contracts for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_FORBIDDEN = [
    "broker_session", "real_account_token", "api_secret", "password",
    "credential", "real_order_handle", "production_db_connection",
    "bank_account", "real_capital_control", "live_execution",
    "shioaji_login", "broker_api_key", "production_ledger",
]

INTEGRATION_CONTRACTS: Dict[str, Dict[str, Any]] = {
    "MarketDataToSession": {
        "required_fields": ["symbol", "timestamp", "open", "high", "low", "close", "volume", "source_lineage"],
        "optional_fields": ["vwap", "bid", "ask", "trade_count"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["FLOWING", "STALE", "DROPPED"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "SessionToStrategy": {
        "required_fields": ["session_id", "run_id", "period_start", "period_end", "market_data_lineage"],
        "optional_fields": ["benchmark", "universe", "timezone"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["ACTIVE", "PAUSED", "HALTED", "COMPLETE"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "StrategyToPortfolio": {
        "required_fields": ["strategy_id", "session_id", "signal_id", "symbol", "direction", "signal_timestamp"],
        "optional_fields": ["confidence", "weight", "target_price"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["APPROVED", "DENIED", "PENDING"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "PortfolioToExecution": {
        "required_fields": ["portfolio_id", "session_id", "symbol", "quantity", "direction", "order_type"],
        "optional_fields": ["limit_price", "stop_price", "time_in_force"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["SUBMITTED", "PENDING", "REJECTED"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "ExecutionToAnalytics": {
        "required_fields": ["execution_id", "session_id", "symbol", "fill_price", "fill_quantity", "simulated"],
        "optional_fields": ["commission", "slippage", "transaction_tax"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["FILLED", "PARTIAL_FILL", "REJECTED"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "AnalyticsToAttribution": {
        "required_fields": ["run_id", "session_id", "period_start", "period_end", "pnl", "return_rate"],
        "optional_fields": ["benchmark_return", "alpha", "sharpe", "max_drawdown"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["COMPLETE", "DEGRADED", "INSUFFICIENT_DATA"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "AttributionToCoordination": {
        "required_fields": ["attribution_run_id", "session_id", "attribution_status", "score"],
        "optional_fields": ["degraded_reasons", "warnings"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["COMPLETE", "DEGRADED", "FAILED"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "CoordinationToRecovery": {
        "required_fields": ["coordination_id", "sessions", "conflict_status"],
        "optional_fields": ["priority_order", "resource_map"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["COORDINATED", "CONFLICT", "DEGRADED"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "RecoveryToHealth": {
        "required_fields": ["recovery_id", "component_id", "recovery_status", "evidence"],
        "optional_fields": ["recovery_time_sec", "degraded_after_recovery"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["RECOVERED", "PARTIAL", "FAILED", "NOT_ATTEMPTED"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
    "HealthToReport": {
        "required_fields": ["component_id", "health_status", "health_score", "check_timestamp"],
        "optional_fields": ["degraded_reasons", "failures", "warnings"],
        "forbidden_fields": _FORBIDDEN,
        "supported_statuses": ["PASS", "DEGRADED", "FAIL"],
        "deterministic": True,
        "read_only": True,
        "paper_only": True,
        "schema_version": "1.6.8",
    },
}

_dynamic_contracts: Dict[str, Dict[str, Any]] = {}


def get_contract(name: str) -> Dict[str, Any]:
    """Return contract by name. Raises KeyError if not found."""
    if name in _dynamic_contracts:
        return _dynamic_contracts[name]
    if name not in INTEGRATION_CONTRACTS:
        raise KeyError(f"Unknown integration contract: {name!r}")
    return INTEGRATION_CONTRACTS[name]


def validate_contract_payload(contract_name: str, payload: dict) -> Dict[str, Any]:
    """
    Validate payload against contract spec.
    Returns {valid, errors, warnings, forbidden_found, missing_required}.
    Unknown contracts return valid=False with an error.
    """
    if contract_name not in INTEGRATION_CONTRACTS and contract_name not in _dynamic_contracts:
        return {
            "valid": False,
            "errors": [f"unknown_contract: {contract_name}"],
            "warnings": [],
            "forbidden_found": [],
            "missing_required": [],
            "paper_only": True,
            "research_only": True,
        }
    contract = get_contract(contract_name)
    errors: List[str] = []
    warnings: List[str] = []
    missing_required: List[str] = []
    forbidden_found: List[str] = []

    for req in contract.get("required_fields", []):
        if req not in payload:
            missing_required.append(req)
            errors.append(f"missing_required: {req}")

    for forb in contract.get("forbidden_fields", []):
        if forb in payload:
            forbidden_found.append(forb)
            errors.append(f"forbidden_field: {forb}")

    for opt in contract.get("optional_fields", []):
        if opt not in payload:
            warnings.append(f"optional_missing: {opt}")

    valid = len(errors) == 0
    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "forbidden_found": forbidden_found,
        "missing_required": missing_required,
        "paper_only": True,
        "research_only": True,
    }


def check_schema_compatibility(contract_name: str, payload_schema: dict) -> Dict[str, Any]:
    """Check if payload_schema is compatible with contract spec.
    Unknown contracts return compatible=False."""
    if contract_name not in INTEGRATION_CONTRACTS and contract_name not in _dynamic_contracts:
        return {
            "compatible": False,
            "missing_required": [],
            "extra_fields": [],
            "error": f"unknown_contract: {contract_name}",
            "paper_only": True,
        }
    contract = get_contract(contract_name)
    required = set(contract.get("required_fields", []))
    provided = set(payload_schema.keys())
    missing = required - provided
    extra = provided - required - set(contract.get("optional_fields", []))
    compatible = len(missing) == 0
    return {
        "compatible": compatible,
        "missing_required": list(missing),
        "extra_fields": list(extra),
        "paper_only": True,
    }


def list_contracts() -> List[str]:
    """Return all contract names."""
    all_names = list(INTEGRATION_CONTRACTS.keys()) + list(_dynamic_contracts.keys())
    return all_names


def register_contract(name: str, contract: dict) -> None:
    """Register a new contract dynamically."""
    if not name:
        raise ValueError("Contract name cannot be empty")
    _dynamic_contracts[name] = contract
