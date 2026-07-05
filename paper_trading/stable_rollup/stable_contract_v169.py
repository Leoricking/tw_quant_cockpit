"""
paper_trading/stable_rollup/stable_contract_v169.py
Stable contract for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict, List


class StableContract:
    """Contract validations for v1.6.9 stable rollup."""

    def validate_contract(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("version_constant", self._check_version_constant))
        checks.append(self._check("release_name_constant", self._check_release_name_constant))
        checks.append(self._check("schema_version", self._check_schema_version))
        checks.append(self._check("policy_version", self._check_policy_version))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "stable_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def validate_capability(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("capability_matrix_importable", self._check_capability_matrix))
        checks.append(self._check("capability_count_gte_19", self._check_capability_count))
        checks.append(self._check("no_production_ready_capability", self._check_no_prod_ready))
        checks.append(self._check("all_paper_only", self._check_all_paper_only))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "capability_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def validate_safety(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("safety_module_importable", self._check_safety_import))
        checks.append(self._check("no_real_orders", self._check_no_real_orders))
        checks.append(self._check("broker_disabled", self._check_broker_disabled))
        checks.append(self._check("production_blocked", self._check_production_blocked))
        checks.append(self._check("is_safe", self._check_is_safe))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "safety_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def validate_release_identity(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("version_is_169", self._check_version_is_169))
        checks.append(self._check("known_release_name", self._check_known_release_name))
        checks.append(self._check("base_release_correct", self._check_base_release))
        checks.append(self._check("minimum_version_met", self._check_min_version))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "release_identity_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def validate_backward_compatibility(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("compatibility_matrix_importable", self._check_compat_import))
        checks.append(self._check("edge_count_correct", self._check_edge_count))
        checks.append(self._check("all_edges_compatible", self._check_all_edges_compatible))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "backward_compatibility_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def validate_determinism(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("manifest_deterministic", self._check_manifest_determinism))
        checks.append(self._check("safety_matrix_deterministic", self._check_safety_matrix_determinism))
        checks.append(self._check("capability_matrix_deterministic", self._check_capability_matrix_determinism))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "determinism_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def validate_read_only(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("read_only_flag", self._check_read_only_flag))
        checks.append(self._check("no_live_execution", self._check_no_live_execution))
        checks.append(self._check("no_write_operations", self._check_no_write_ops))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "read_only_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def validate_no_real_orders(self) -> Dict[str, Any]:
        checks = []
        checks.append(self._check("no_real_orders_flag", self._check_no_real_orders))
        checks.append(self._check("broker_execution_disabled", self._check_broker_disabled))
        checks.append(self._check("production_trading_blocked", self._check_production_blocked))
        passed = sum(1 for c in checks if c["ok"])
        return {
            "name": "no_real_orders_contract",
            "passed": passed == len(checks),
            "checks": checks,
            "status": "PASS" if passed == len(checks) else "FAIL",
        }

    def run(self) -> Dict[str, Any]:
        """Run all contract validations and return combined result."""
        results = [
            self.validate_contract(),
            self.validate_capability(),
            self.validate_safety(),
            self.validate_release_identity(),
            self.validate_backward_compatibility(),
            self.validate_determinism(),
            self.validate_read_only(),
            self.validate_no_real_orders(),
        ]
        total = len(results)
        passed_count = sum(1 for r in results if r["passed"])
        all_pass = passed_count == total
        return {
            "name": "stable_rollup_contract_v169",
            "version": "1.6.9",
            "total_validations": total,
            "passed_validations": passed_count,
            "all_pass": all_pass,
            "status": "PASS" if all_pass else "FAIL",
            "results": results,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    # ── Internal check helpers ────────────────────────────────────────────────

    @staticmethod
    def _check(name: str, fn) -> dict:
        try:
            ok, detail = fn()
            return {"name": name, "ok": ok, "detail": detail}
        except Exception as exc:
            return {"name": name, "ok": False, "detail": str(exc)}

    def _check_version_constant(self):
        from paper_trading.stable_rollup import VERSION
        return (VERSION == "1.6.9", f"VERSION={VERSION!r}")

    def _check_release_name_constant(self):
        from paper_trading.stable_rollup import RELEASE_NAME
        return (RELEASE_NAME == "Live Paper Trading Stable Rollup", f"RELEASE_NAME={RELEASE_NAME!r}")

    def _check_schema_version(self):
        from paper_trading.stable_rollup.version_v169 import SCHEMA_VERSION
        return (SCHEMA_VERSION == "169", f"SCHEMA_VERSION={SCHEMA_VERSION!r}")

    def _check_policy_version(self):
        from paper_trading.stable_rollup.version_v169 import POLICY_VERSION
        ok = POLICY_VERSION == "1.6.9-live-paper-stable-rollup"
        return (ok, f"POLICY_VERSION={POLICY_VERSION!r}")

    def _check_capability_matrix(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) > 0, f"capability_count={len(m)}")

    def _check_capability_count(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        m = get_matrix()
        return (len(m) >= 19, f"count={len(m)} (need >= 19)")

    def _check_no_prod_ready(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        prod = [c["capability"] for c in get_matrix() if c.get("production_ready", True)]
        return (len(prod) == 0, f"production_ready capabilities: {prod}")

    def _check_all_paper_only(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        not_paper = [c["capability"] for c in get_matrix() if not c.get("paper_only", False)]
        return (len(not_paper) == 0, f"non-paper_only: {not_paper}")

    def _check_safety_import(self):
        from paper_trading.stable_rollup import safety_v169
        return (True, "safety_v169 importable")

    def _check_no_real_orders(self):
        from paper_trading.stable_rollup import NO_REAL_ORDERS
        return (NO_REAL_ORDERS is True, f"NO_REAL_ORDERS={NO_REAL_ORDERS!r}")

    def _check_broker_disabled(self):
        from paper_trading.stable_rollup import BROKER_EXECUTION_ENABLED
        return (BROKER_EXECUTION_ENABLED is False, f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED!r}")

    def _check_production_blocked(self):
        from paper_trading.stable_rollup import PRODUCTION_TRADING_BLOCKED
        return (PRODUCTION_TRADING_BLOCKED is True, f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED!r}")

    def _check_is_safe(self):
        from paper_trading.stable_rollup.safety_v169 import is_safe
        safe = is_safe()
        return (safe, f"is_safe()={safe}")

    def _check_version_is_169(self):
        from paper_trading.stable_rollup.version_v169 import VERSION
        return (VERSION == "1.6.9", f"VERSION={VERSION!r}")

    def _check_known_release_name(self):
        from paper_trading.stable_rollup.version_v169 import is_known_release, RELEASE_NAME
        return (is_known_release(RELEASE_NAME), f"is_known_release({RELEASE_NAME!r})")

    def _check_base_release(self):
        from paper_trading.stable_rollup.version_v169 import BASE_RELEASE
        ok = BASE_RELEASE == "1.6.8 Operational Integration Hardening"
        return (ok, f"BASE_RELEASE={BASE_RELEASE!r}")

    def _check_min_version(self):
        from paper_trading.stable_rollup.version_v169 import check_minimum_version, ACCEPTED_MINIMUM_VERSION
        ok = check_minimum_version("1.6.9")
        return (ok, f"1.6.9 >= {ACCEPTED_MINIMUM_VERSION}")

    def _check_compat_import(self):
        from paper_trading.stable_rollup.compatibility_matrix_v169 import get_edges
        edges = get_edges()
        return (len(edges) > 0, f"edge_count={len(edges)}")

    def _check_edge_count(self):
        from paper_trading.stable_rollup.compatibility_matrix_v169 import get_edges
        edges = get_edges()
        return (len(edges) == 11, f"edge_count={len(edges)} (need 11)")

    def _check_all_edges_compatible(self):
        from paper_trading.stable_rollup.compatibility_matrix_v169 import get_edges
        edges = get_edges()
        incompatible = [f"{e['from_version']}->{e['to_version']}" for e in edges if e["overall_status"] != "COMPATIBLE"]
        return (len(incompatible) == 0, f"incompatible_edges={incompatible}")

    def _check_manifest_determinism(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        m1 = get_manifest()
        m2 = get_manifest()
        ok = [r["version"] for r in m1] == [r["version"] for r in m2]
        return (ok, "manifest is deterministic" if ok else "manifest is non-deterministic")

    def _check_safety_matrix_determinism(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import get_matrix
        m1 = get_matrix()
        m2 = get_matrix()
        ok = [r["capability"] for r in m1] == [r["capability"] for r in m2]
        return (ok, "safety_matrix is deterministic")

    def _check_capability_matrix_determinism(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        m1 = get_matrix()
        m2 = get_matrix()
        ok = [r["capability"] for r in m1] == [r["capability"] for r in m2]
        return (ok, "capability_matrix is deterministic")

    def _check_read_only_flag(self):
        from paper_trading.stable_rollup import LIVE_PAPER_STABLE_ROLLUP_READ_ONLY
        return (LIVE_PAPER_STABLE_ROLLUP_READ_ONLY is True, f"READ_ONLY={LIVE_PAPER_STABLE_ROLLUP_READ_ONLY!r}")

    def _check_no_live_execution(self):
        from paper_trading.stable_rollup import LIVE_EXECUTION_ENABLED
        return (LIVE_EXECUTION_ENABLED is False, f"LIVE_EXECUTION_ENABLED={LIVE_EXECUTION_ENABLED!r}")

    def _check_no_write_ops(self):
        from paper_trading.stable_rollup import PRODUCTION_LEDGER_WRITE_ENABLED
        return (PRODUCTION_LEDGER_WRITE_ENABLED is False, f"PRODUCTION_LEDGER_WRITE_ENABLED={PRODUCTION_LEDGER_WRITE_ENABLED!r}")
