"""
paper_trading/operational_integration/integration_validator_v168.py
Integration Validator for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from .models_v168 import IntegrationContext

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class IntegrationValidator:
    """Validates all integration artifacts. Research only."""

    def validate_context(self, ctx: IntegrationContext) -> Dict[str, Any]:
        """Validate integration context."""
        errors = []
        if not ctx.run_id:
            errors.append("missing run_id")
        if not ctx.session_id:
            errors.append("missing session_id")
        if ctx.period_start > ctx.period_end:
            errors.append("reversed period")
        if not ctx.paper_only:
            errors.append("paper_only must be True")
        if not ctx.research_only:
            errors.append("research_only must be True")
        if not ctx.read_only:
            errors.append("read_only must be True")
        return {"valid": len(errors) == 0, "errors": errors, "paper_only": True}

    def validate_contracts(self, registry, payloads: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all payloads against their contracts."""
        results = {}
        errors = []
        for contract_name, payload in payloads.items():
            try:
                result = registry.validate_payload(contract_name, payload)
                results[contract_name] = result
                if not result.get("valid"):
                    errors.extend(result.get("errors", []))
            except Exception as e:
                results[contract_name] = {"valid": False, "errors": [str(e)]}
                errors.append(f"{contract_name}: {e}")
        return {
            "valid": len(errors) == 0,
            "contract_count": len(payloads),
            "errors": errors,
            "details": results,
            "paper_only": True,
        }

    def validate_safety(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate safety constraints."""
        from .safety_v168 import validate_integration_safety
        return validate_integration_safety(data)

    def validate_lineage(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate lineage records."""
        errors = []
        for rec in records:
            if not rec.get("lineage_id"):
                errors.append("missing lineage_id")
            if not rec.get("component_id"):
                errors.append("missing component_id")
        return {
            "valid": len(errors) == 0,
            "total_records": len(records),
            "errors": errors,
            "paper_only": True,
        }

    def validate_timestamps(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate timestamp records."""
        from .timestamp_bridge_v168 import TimestampBridge
        bridge = TimestampBridge()
        result = bridge.audit_timestamps(records)
        return {
            "valid": result.get("issue_count", 0) == 0,
            "issue_count": result.get("issue_count", 0),
            "details": result,
            "paper_only": True,
        }

    def validate_identities(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate identity records."""
        errors = []
        for rec in records:
            if not rec.get("identity_id"):
                errors.append("missing identity_id")
            if not rec.get("component_id"):
                errors.append("missing component_id")
        return {
            "valid": len(errors) == 0,
            "total_records": len(records),
            "errors": errors,
            "paper_only": True,
        }

    def validate_all(
        self,
        ctx: IntegrationContext,
        registry,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run all validations."""
        ctx_result = self.validate_context(ctx)
        safety_result = self.validate_safety(data)
        lineage_records = data.get("lineage_records", [])
        ts_records = data.get("timestamp_records", [])
        id_records = data.get("identity_records", [])
        payloads = data.get("contract_payloads", {})

        lineage_result = self.validate_lineage(lineage_records)
        ts_result = self.validate_timestamps(ts_records)
        id_result = self.validate_identities(id_records)
        contract_result = self.validate_contracts(registry, payloads)

        all_valid = all([
            ctx_result["valid"],
            safety_result["safe"],
            lineage_result["valid"],
            ts_result["valid"],
            id_result["valid"],
            contract_result["valid"],
        ])
        return {
            "valid": all_valid,
            "context": ctx_result,
            "safety": safety_result,
            "lineage": lineage_result,
            "timestamps": ts_result,
            "identities": id_result,
            "contracts": contract_result,
            "paper_only": True,
        }
