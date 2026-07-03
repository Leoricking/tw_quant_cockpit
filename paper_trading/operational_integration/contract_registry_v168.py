"""
paper_trading/operational_integration/contract_registry_v168.py
Contract Registry for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .integration_contract_v168 import (
    INTEGRATION_CONTRACTS, validate_contract_payload, check_schema_compatibility,
)

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class ContractRegistry:
    """Registry for all integration contracts. Read-only. Research only."""

    def __init__(self) -> None:
        self._contracts: Dict[str, Dict[str, Any]] = dict(INTEGRATION_CONTRACTS)

    def register(self, name: str, contract: dict) -> None:
        """Register a contract. Raises ValueError if name already registered."""
        if name in self._contracts:
            raise ValueError(f"Contract already registered: {name!r}")
        if not name:
            raise ValueError("Contract name cannot be empty")
        self._contracts[name] = contract

    def get(self, name: str) -> Dict[str, Any]:
        """Return contract by name. Raises KeyError if not found."""
        if name not in self._contracts:
            raise KeyError(f"Contract not found: {name!r}")
        return self._contracts[name]

    def list_names(self) -> List[str]:
        """Return all registered contract names."""
        return sorted(self._contracts.keys())

    def validate_all(self) -> Dict[str, Any]:
        """Validate all registered contracts for structural completeness."""
        results = {}
        required_keys = {"required_fields", "optional_fields", "forbidden_fields", "paper_only"}
        for name, contract in self._contracts.items():
            missing = required_keys - set(contract.keys())
            results[name] = {
                "valid": len(missing) == 0,
                "missing_keys": list(missing),
                "paper_only": contract.get("paper_only", True),
            }
        all_valid = all(v["valid"] for v in results.values())
        return {
            "all_valid": all_valid,
            "total": len(results),
            "valid_count": sum(1 for v in results.values() if v["valid"]),
            "details": results,
            "paper_only": True,
        }

    def check_compatibility(self, from_component: str, to_component: str) -> Dict[str, Any]:
        """Check if a contract exists for this component pair."""
        matching = []
        for name, contract in self._contracts.items():
            if (contract.get("from_component", "") == from_component and
                    contract.get("to_component", "") == to_component):
                matching.append(name)
        # Also look by name pattern
        key = f"{from_component}To{to_component}"
        if key in self._contracts:
            matching.append(key)
        matching = list(set(matching))
        return {
            "compatible": len(matching) > 0,
            "contracts": matching,
            "from_component": from_component,
            "to_component": to_component,
            "paper_only": True,
        }

    def validate_payload(self, contract_name: str, payload: dict) -> Dict[str, Any]:
        """Validate payload against contract spec."""
        if contract_name not in self._contracts:
            return {
                "valid": False,
                "errors": [f"unknown_contract: {contract_name}"],
                "warnings": [],
                "forbidden_found": [],
                "missing_required": [],
                "paper_only": True,
            }
        contract = self._contracts[contract_name]
        errors: list = []
        warnings: list = []
        missing_required = []
        forbidden_found = []

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

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "forbidden_found": forbidden_found,
            "missing_required": missing_required,
            "paper_only": True,
        }

    def count(self) -> int:
        """Return total number of registered contracts."""
        return len(self._contracts)
