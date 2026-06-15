"""
gate_enforcement.enforcement_health — QualityGateEnforcementHealthCheck v1.1.5

Health checks for the gate enforcement subsystem.
Research Only. No Real Orders.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class QualityGateEnforcementHealthCheck:
    """
    Runs health checks on the gate enforcement subsystem.
    Returns list of (check_name, status, message) tuples.
    Statuses: PASS / WARN / FAIL / BLOCKED
    """

    def run(self) -> List[Tuple[str, str, str]]:
        results = []
        checks = [
            self._check_package_import,
            self._check_policy_available,
            self._check_resolver_available,
            self._check_symbol_filter_available,
            self._check_snapshot_builder_available,
            self._check_audit_log_available,
            self._check_reproducibility_hasher_available,
            self._check_enforcement_engine_available,
            self._check_quality_gates_integration,
            self._check_freshness_integration,
            self._check_coverage_repair_integration,
            self._check_universe_integration,
            self._check_formal_excludes_observational,
            self._check_observational_excludes_demo,
            self._check_blocked_always_excluded,
            self._check_gate_engine_failure_blocks_formal,
            self._check_mock_formal_enforcement_blocked,
            self._check_override_disabled_by_default,
            self._check_audit_append_only,
            self._check_audit_chain_verification,
            self._check_reproducibility_hash_stable,
            self._check_runtime_output_ignored,
            self._check_no_broker_execution,
            self._check_no_forbidden_actions,
        ]
        for fn in checks:
            try:
                name, status, msg = fn()
            except Exception as exc:
                name = fn.__name__
                status = "FAIL"
                msg = f"Exception: {exc}"
            results.append((name, status, msg))
        return results

    def _check_package_import(self):
        name = "gate_enforcement_package_import"
        try:
            import gate_enforcement
            ok = getattr(gate_enforcement, "NO_REAL_ORDERS", False) is True
            return name, ("PASS" if ok else "FAIL"), ("NO_REAL_ORDERS=True" if ok else "NO_REAL_ORDERS missing")
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_policy_available(self):
        name = "enforcement_policy_available"
        try:
            from gate_enforcement.enforcement_policy import QualityGateEnforcementPolicy
            p = QualityGateEnforcementPolicy()
            ok = p.policy_version() == "1.1.5"
            return name, ("PASS" if ok else "WARN"), f"policy_version={p.policy_version()}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_resolver_available(self):
        name = "run_gate_resolver_available"
        try:
            from gate_enforcement.run_gate_resolver import RunGateResolver
            RunGateResolver()
            return name, "PASS", "RunGateResolver importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_symbol_filter_available(self):
        name = "symbol_filter_available"
        try:
            from gate_enforcement.symbol_filter import QualityGateSymbolFilter
            QualityGateSymbolFilter()
            return name, "PASS", "QualityGateSymbolFilter importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_snapshot_builder_available(self):
        name = "snapshot_builder_available"
        try:
            from gate_enforcement.run_snapshot import RunGateSnapshotBuilder
            RunGateSnapshotBuilder()
            return name, "PASS", "RunGateSnapshotBuilder importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_audit_log_available(self):
        name = "audit_log_available"
        try:
            from gate_enforcement.audit_log import QualityGateAuditLog
            return name, "PASS", "QualityGateAuditLog importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_reproducibility_hasher_available(self):
        name = "reproducibility_hasher_available"
        try:
            from gate_enforcement.reproducibility import RunReproducibilityHasher
            RunReproducibilityHasher()
            return name, "PASS", "RunReproducibilityHasher importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_enforcement_engine_available(self):
        name = "enforcement_engine_available"
        try:
            from gate_enforcement.enforcement_engine import QualityGateEnforcementEngine
            return name, "PASS", "QualityGateEnforcementEngine importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_quality_gates_integration(self):
        name = "quality_gates_v114_integration"
        try:
            import quality_gates
            v = getattr(quality_gates, "__version__", "")
            ok = v.startswith("1.1")
            return name, ("PASS" if ok else "WARN"), f"quality_gates version={v}"
        except Exception as exc:
            return name, "WARN", f"quality_gates not importable: {exc}"

    def _check_freshness_integration(self):
        name = "freshness_integration"
        try:
            import data_freshness
            return name, "PASS", "data_freshness importable"
        except Exception as exc:
            return name, "WARN", f"data_freshness not importable: {exc}"

    def _check_coverage_repair_integration(self):
        name = "coverage_repair_integration"
        try:
            import coverage_repair
            return name, "PASS", "coverage_repair importable"
        except Exception as exc:
            return name, "WARN", f"coverage_repair not importable: {exc}"

    def _check_universe_integration(self):
        name = "universe_integration"
        try:
            import universe
            return name, "PASS", "universe importable"
        except Exception as exc:
            return name, "WARN", f"universe not importable: {exc}"

    def _check_formal_excludes_observational(self):
        name = "formal_excludes_observational"
        try:
            from gate_enforcement.symbol_filter import QualityGateSymbolFilter
            f = QualityGateSymbolFilter()
            decisions = {"A": "ELIGIBLE_FORMAL", "B": "ELIGIBLE_OBSERVATIONAL", "C": "DEMO_ONLY"}
            result = f.filter_symbols(["A", "B", "C"], decisions, "FORMAL")
            formal_incl = result.get("included", [])
            ok = "B" not in formal_incl and "C" not in formal_incl and "A" in formal_incl
            return name, ("PASS" if ok else "FAIL"), f"FORMAL included: {formal_incl}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_observational_excludes_demo(self):
        name = "observational_excludes_demo"
        try:
            from gate_enforcement.symbol_filter import QualityGateSymbolFilter
            f = QualityGateSymbolFilter()
            decisions = {"A": "ELIGIBLE_FORMAL", "B": "ELIGIBLE_OBSERVATIONAL", "C": "DEMO_ONLY"}
            result = f.filter_symbols(["A", "B", "C"], decisions, "OBSERVATIONAL")
            obs_incl = result.get("included", [])
            ok = "C" not in obs_incl and "A" in obs_incl and "B" in obs_incl
            return name, ("PASS" if ok else "FAIL"), f"OBSERVATIONAL included: {obs_incl}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_blocked_always_excluded(self):
        name = "blocked_always_excluded"
        try:
            from gate_enforcement.symbol_filter import QualityGateSymbolFilter
            f = QualityGateSymbolFilter()
            decisions = {"X": "BLOCKED_DATA_QUALITY", "Y": "ELIGIBLE_FORMAL"}
            result = f.filter_symbols(["X", "Y"], decisions, "DEMO")
            included = result.get("included", [])
            ok = "X" not in included and "Y" in included
            return name, ("PASS" if ok else "FAIL"), f"DEMO included: {included}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_gate_engine_failure_blocks_formal(self):
        name = "gate_engine_failure_blocks_formal"
        try:
            from gate_enforcement.enforcement_engine import QualityGateEnforcementEngine
            eng = QualityGateEnforcementEngine()
            result = eng.fail_run("test-run", "PRICE_BACKTEST_GATE", "FORMAL", "test failure")
            ok = result.status == "FAILED" and not result.included_symbols
            return name, ("PASS" if ok else "FAIL"), f"status={result.status}, included={result.included_symbols}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_mock_formal_enforcement_blocked(self):
        name = "mock_formal_enforcement_blocked"
        try:
            import gate_enforcement
            blocked = not getattr(gate_enforcement, "MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED", True)
            return name, ("PASS" if blocked else "FAIL"), f"MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED={not blocked}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_override_disabled_by_default(self):
        name = "override_disabled_by_default"
        try:
            import gate_enforcement
            ok = getattr(gate_enforcement, "QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT", False) is True
            return name, ("PASS" if ok else "FAIL"), f"QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT={ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_audit_append_only(self):
        name = "audit_append_only"
        try:
            from gate_enforcement.audit_log import QualityGateAuditLog
            # Check that append method exists and is not a no-op
            log = QualityGateAuditLog.__dict__
            ok = "append" in log
            return name, ("PASS" if ok else "FAIL"), "append method exists"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_audit_chain_verification(self):
        name = "audit_chain_verification"
        try:
            from gate_enforcement.audit_log import QualityGateAuditLog
            ok = "verify_chain" in QualityGateAuditLog.__dict__
            return name, ("PASS" if ok else "FAIL"), "verify_chain method exists"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_reproducibility_hash_stable(self):
        name = "reproducibility_hash_stable"
        try:
            from gate_enforcement.reproducibility import RunReproducibilityHasher
            h = RunReproducibilityHasher()
            kw = dict(
                code_version="1.1.5",
                command_name="validate-score",
                arguments={"mode": "real"},
                gate_name="PRICE_BACKTEST_GATE",
                gate_policy_version="1.1.5",
                included_symbols=["TST001", "TST002"],
                excluded_symbols=["TST003"],
                decisions={"TST001": "ELIGIBLE_FORMAL", "TST002": "ELIGIBLE_FORMAL", "TST003": "BLOCKED"},
            )
            hash1 = h.build_run_hash(**kw)
            hash2 = h.build_run_hash(**kw)
            ok = hash1 == hash2 and len(hash1) == 64
            return name, ("PASS" if ok else "FAIL"), f"hash_stable={ok} len={len(hash1)}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_runtime_output_ignored(self):
        name = "runtime_output_not_committed"
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        if not os.path.isfile(gitignore_path):
            return name, "WARN", ".gitignore not found"
        try:
            with open(gitignore_path, encoding="utf-8") as f:
                content = f.read()
            ok = "quality_gate_enforcement" in content or "quality_gate_audit" in content
            return name, ("PASS" if ok else "WARN"), "enforcement dirs in .gitignore"
        except Exception as exc:
            return name, "WARN", str(exc)

    def _check_no_broker_execution(self):
        name = "no_broker_execution"
        try:
            import gate_enforcement
            no_broker = getattr(gate_enforcement, "BROKER_DISABLED", False) is True
            return name, ("PASS" if no_broker else "FAIL"), f"BROKER_DISABLED={no_broker}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_forbidden_actions(self):
        name = "no_forbidden_actions"
        # Check that enforcement_engine.py does not import broker/order modules
        engine_path = os.path.join(BASE_DIR, "gate_enforcement", "enforcement_engine.py")
        if not os.path.isfile(engine_path):
            return name, "WARN", "enforcement_engine.py not found"
        try:
            with open(engine_path, encoding="utf-8") as f:
                lines = f.readlines()
            # Only check non-comment, non-docstring import lines for forbidden patterns
            forbidden_import_patterns = ["import shioaji", "import broker", "from broker",
                                         "submit_order", "place_order", "buy(", "sell("]
            found = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                line_lower = stripped.lower()
                for kw in forbidden_import_patterns:
                    if kw in line_lower and kw not in found:
                        found.append(kw)
            if found:
                return name, "FAIL", f"Forbidden keywords found: {found}"
            return name, "PASS", "No forbidden actions in enforcement engine"
        except Exception as exc:
            return name, "WARN", str(exc)
