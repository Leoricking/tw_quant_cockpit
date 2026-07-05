"""
paper_trading/stable_rollup/stable_validator_v169.py
Validation module for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Dict, Any, List

from paper_trading.stable_rollup.models_v169 import StableRollupValidationResult
from paper_trading.stable_rollup.enums_v169 import ValidationSeverity

VERSION = "1.6.9"


class StableValidator:
    """Run structured validation checks for v1.6.9."""

    def validate_version(self) -> StableRollupValidationResult:
        issues = []
        try:
            from paper_trading.stable_rollup import VERSION as PKG_VERSION, RELEASE_NAME
            from paper_trading.stable_rollup.version_v169 import VERSION as V_VERSION, SCHEMA_VERSION, POLICY_VERSION
            if PKG_VERSION != "1.6.9":
                issues.append(f"package VERSION={PKG_VERSION!r}")
            if V_VERSION != "1.6.9":
                issues.append(f"version_v169 VERSION={V_VERSION!r}")
            if SCHEMA_VERSION != "169":
                issues.append(f"SCHEMA_VERSION={SCHEMA_VERSION!r}")
            if POLICY_VERSION != "1.6.9-live-paper-stable-rollup":
                issues.append(f"POLICY_VERSION={POLICY_VERSION!r}")
            if RELEASE_NAME != "Live Paper Trading Stable Rollup":
                issues.append(f"RELEASE_NAME={RELEASE_NAME!r}")
        except Exception as exc:
            issues.append(str(exc))
        return StableRollupValidationResult(
            validator_name="version_validator",
            passed=len(issues) == 0,
            severity=ValidationSeverity.CRITICAL if issues else ValidationSeverity.INFO,
            issues=issues,
        )

    def validate_safety(self) -> StableRollupValidationResult:
        issues = []
        try:
            from paper_trading.stable_rollup.safety_v169 import validate_safety, is_safe
            result = validate_safety()
            if result["failed"] > 0:
                for c in result["checks"]:
                    if not c["ok"]:
                        issues.append(f"safety flag failed: {c['flag']}")
            if not is_safe():
                issues.append("is_safe() returned False")
        except Exception as exc:
            issues.append(str(exc))
        return StableRollupValidationResult(
            validator_name="safety_validator",
            passed=len(issues) == 0,
            severity=ValidationSeverity.CRITICAL if issues else ValidationSeverity.INFO,
            issues=issues,
        )

    def validate_manifest(self) -> StableRollupValidationResult:
        issues = []
        try:
            from paper_trading.stable_rollup.release_manifest_v169 import validate_manifest, get_all_versions
            result = validate_manifest()
            if result["status"] != "PASS":
                issues.extend(result["issues"])
            versions = get_all_versions()
            if len(versions) < 13:
                issues.append(f"manifest has {len(versions)} releases, need >= 13")
            if "1.6.9" not in versions:
                issues.append("v1.6.9 not in manifest")
            if "1.6.0" not in versions:
                issues.append("v1.6.0 not in manifest")
        except Exception as exc:
            issues.append(str(exc))
        return StableRollupValidationResult(
            validator_name="manifest_validator",
            passed=len(issues) == 0,
            severity=ValidationSeverity.HIGH if issues else ValidationSeverity.INFO,
            issues=issues,
        )

    def validate_lineage(self) -> StableRollupValidationResult:
        issues = []
        try:
            from paper_trading.stable_rollup.release_registry_v169 import get_registry
            reg = get_registry()
            chain_result = reg.validate_parent_chain()
            if chain_result["status"] != "PASS":
                issues.extend(chain_result["issues"])
            unique_result = reg.validate_unique_versions()
            if unique_result["status"] != "PASS":
                issues.extend([f"dup version: {d}" for d in unique_result["duplicates"]])
        except Exception as exc:
            issues.append(str(exc))
        return StableRollupValidationResult(
            validator_name="lineage_validator",
            passed=len(issues) == 0,
            severity=ValidationSeverity.HIGH if issues else ValidationSeverity.INFO,
            issues=issues,
        )

    def validate_all(self) -> List[StableRollupValidationResult]:
        return [
            self.validate_version(),
            self.validate_safety(),
            self.validate_manifest(),
            self.validate_lineage(),
        ]


def run_all_validations() -> Dict[str, Any]:
    """Run all validations and return a combined result dict."""
    validator = StableValidator()
    results = validator.validate_all()
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    return {
        "name": "stable_rollup_validator_v169",
        "version": VERSION,
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "all_pass": failed == 0,
        "status": "PASS" if failed == 0 else "FAIL",
        "results": [
            {
                "validator_name": r.validator_name,
                "passed": r.passed,
                "severity": r.severity.value,
                "issues": r.issues,
            }
            for r in results
        ],
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
    }
