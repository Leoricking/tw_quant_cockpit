"""portfolio/stable_rollup/integrity_validator_v159.py — Integrity validator v1.5.9."""


class IntegrityValidator:
    """Validates cross-module schema, enum, and CLI consistency."""

    def validate_schema_integrity(self):
        from .schema_registry_v159 import SchemaRegistryV159
        reg = SchemaRegistryV159()
        return reg.validate()

    def validate_enum_integrity(self):
        from .enum_registry_v159 import EnumRegistryV159
        reg = EnumRegistryV159()
        return reg.validate()

    def validate_capability_integrity(self):
        from .capability_registry_v159 import CapabilityRegistryV159
        reg = CapabilityRegistryV159()
        return reg.validate()

    def validate_safety_integrity(self):
        from .safety_contract_v159 import SafetyContractV159
        raw = SafetyContractV159().validate()
        # normalise key to "valid" for run_all aggregation
        return {"valid": raw.get("is_valid", raw.get("valid", False)), **raw}

    def run_all(self):
        results = {
            "schema": self.validate_schema_integrity(),
            "enum": self.validate_enum_integrity(),
            "capability": self.validate_capability_integrity(),
            "safety": self.validate_safety_integrity(),
        }
        all_valid = all(r.get("valid", False) for r in results.values())
        return {"overall": "PASS" if all_valid else "FAIL", "results": results}
