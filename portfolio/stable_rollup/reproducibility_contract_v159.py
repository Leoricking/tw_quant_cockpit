"""portfolio/stable_rollup/reproducibility_contract_v159.py — Reproducibility contract v1.5.9."""
from .models_v159 import StableContractRecord

REPRODUCIBILITY_CONTRACT = StableContractRecord(
    contract_id="portfolio_reproducibility_contract_v159",
    contract_type="REPRODUCIBILITY",
    version="1.5.9",
    rules=[
        "deterministic ordering in all collections",
        "deterministic IDs where applicable",
        "fixed seed for any random operations",
        "code commit must be recorded",
        "Python version must be recorded",
        "dependency versions must be recorded",
        "timezone must be recorded (Asia/Taipei)",
        "calendar version must be recorded",
        "config hash must be recorded",
        "input data hashes must be recorded",
        "policy versions must be recorded",
        "result hashes must be recorded",
        "rerun with same inputs must produce same semantic result",
        "mutation must be detected via hash mismatch",
        "generated_at must NOT affect canonical result hash",
        "temp paths must NOT affect canonical result hash",
        "machine-specific paths must NOT be in canonical hash",
        "unordered dict serialization is forbidden",
        "runtime UUID must be separated from semantic content hash",
    ],
    blocking_violations=[
        "nondeterministic_hash",
        "missing_code_commit",
        "hash_mismatch_undetected",
    ],
    status="VALID",
)


class ReproducibilityContractV159:
    def get_contract(self):
        return REPRODUCIBILITY_CONTRACT

    def validate_manifest(self, manifest):
        violations = []
        if not manifest.get("config_hash"):
            violations.append("MISSING_CONFIG_HASH")
        if not manifest.get("timezone"):
            violations.append("MISSING_TIMEZONE")
        if not manifest.get("calendar_version"):
            violations.append("MISSING_CALENDAR_VERSION")
        return {"is_valid": len(violations) == 0, "violations": violations}

    def check_drift(self):
        return []
