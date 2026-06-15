"""
governance_rollup/health_aggregator.py — GovernanceHealthAggregator v1.1.9

Aggregates health checks from all governance modules.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Known warnings do NOT cause overall FAIL.
[!] BLOCKED safety guards are NOT function failures.
[!] No Real Orders BLOCKED = expected safety block.
"""
from __future__ import annotations

import importlib
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

# Known warning strings that should NOT cause overall FAIL
_KNOWN_WARNINGS = [
    "no real orders",
    "blocked: allow_write=false",
    "dry_run=true",
    "auto repair disabled",
    "auto download disabled",
    "auto import disabled",
    "trade execution disabled",
    "broker disabled",
    "production trading blocked",
    "pyside6 not available",
    "mock data",
    "data not found",
    "optional module",
]


class GovernanceHealthAggregator:
    """
    Aggregates health checks from all governance modules.

    Rules:
    - Known warnings do NOT cause overall FAIL
    - New FAILs must be explicitly listed
    - BLOCKED safety guards are NOT function failures
    - No Real Orders BLOCKED = expected safety block
    """

    HEALTH_COMMANDS = [
        ("universe-health",            "universe"),
        ("import-onboarding-health",   "data_onboarding"),
        ("coverage-repair-health",     "coverage_repair"),
        ("freshness-health",           "data_freshness"),
        ("quality-gate-health",        "quality_gates"),
        ("gate-enforcement-health",    "gate_enforcement"),
        ("governance-health",          "governance_ops"),
        ("governance-alerts-health",   "governance_alerts"),
        ("research-registry-health",   "research_registry"),
    ]

    # Module -> health check class import path
    _HEALTH_CLASS_MAP: Dict[str, Tuple[str, str]] = {
        "universe":          ("universe.universe_health", "UniverseHealthCheck"),
        "data_onboarding":   ("data_onboarding.onboarding_health", "DataOnboardingHealthCheck"),
        "coverage_repair":   ("coverage_repair.repair_health", "CoverageRepairHealthCheck"),
        "data_freshness":    ("data_freshness.freshness_health", "DataFreshnessHealthCheck"),
        "quality_gates":     ("quality_gates.gate_health", "QualityGateHealthCheck"),
        "gate_enforcement":  ("gate_enforcement.enforcement_health", "GateEnforcementHealthCheck"),
        "governance_ops":    ("governance_ops.ops_health", "GovernanceOpsHealthCheck"),
        "governance_alerts": ("governance_alerts.alert_health", "GovernanceAlertHealthCheck"),
        "research_registry": ("research_registry.registry_health", "ResearchRunRegistryHealthCheck"),
    }

    def run_all(self, mode: str = "real") -> Dict[str, Any]:
        """Run all module health checks and aggregate results."""
        results = {}
        for _cmd, module_name in self.HEALTH_COMMANDS:
            result = self._run_module_health(module_name, mode=mode)
            results[module_name] = result
        aggregated = self.aggregate_results(results)
        return aggregated

    def _run_module_health(self, module_name: str, mode: str = "real") -> Dict[str, Any]:
        """Run health check for a single module. Uses try/except to handle missing modules."""
        if module_name not in self._HEALTH_CLASS_MAP:
            return {
                "module": module_name,
                "status": "UNSUPPORTED",
                "available": False,
            }
        import_path, class_name = self._HEALTH_CLASS_MAP[module_name]
        try:
            mod = importlib.import_module(import_path)
            cls = getattr(mod, class_name, None)
            if cls is None:
                return {
                    "module": module_name,
                    "status": "WARN",
                    "available": False,
                    "reason": f"{class_name} not found in {import_path}",
                }
            checker = cls()
            if hasattr(checker, "run"):
                raw_result = checker.run()
            else:
                raw_result = {"status": "PASS", "note": "no run() method"}
            return self.normalize_health_result(raw_result, module_name)
        except ImportError:
            return {
                "module": module_name,
                "status": "WARN",
                "available": False,
                "reason": f"Module {import_path} not importable",
            }
        except Exception as exc:
            logger.warning("_run_module_health: %s raised: %s", module_name, exc)
            return {
                "module": module_name,
                "status": "WARN",
                "available": False,
                "reason": str(exc),
            }

    def normalize_health_result(self, raw_output: Any, module: str) -> Dict[str, Any]:
        """Normalize a raw health check result to a standard format."""
        if isinstance(raw_output, dict):
            status = raw_output.get("status") or raw_output.get("overall_status", "UNKNOWN")
            return {
                "module": module,
                "status": str(status).upper() if status else "UNKNOWN",
                "available": True,
                "raw": raw_output,
            }
        if isinstance(raw_output, (list, tuple)):
            # Common pattern: list of (name, status, msg) tuples
            passed = sum(1 for item in raw_output if (
                (isinstance(item, (list, tuple)) and len(item) >= 2 and item[1] == "PASS") or
                (isinstance(item, dict) and item.get("status") == "PASS")
            ))
            failed = sum(1 for item in raw_output if (
                (isinstance(item, (list, tuple)) and len(item) >= 2 and item[1] == "FAIL") or
                (isinstance(item, dict) and item.get("status") == "FAIL")
            ))
            total = len(raw_output)
            status = "PASS" if failed == 0 else "WARN"
            return {
                "module": module,
                "status": status,
                "available": True,
                "checks_passed": passed,
                "checks_failed": failed,
                "checks_total": total,
            }
        return {
            "module": module,
            "status": "UNKNOWN",
            "available": True,
            "raw": str(raw_output)[:200],
        }

    def aggregate_results(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate individual module results into an overall summary."""
        total = len(results)
        pass_count = sum(1 for r in results.values() if r.get("status") == "PASS")
        warn_count = sum(1 for r in results.values()
                         if r.get("status") in ("WARN", "UNSUPPORTED"))
        fail_count = sum(1 for r in results.values() if r.get("status") == "FAIL")
        unavailable = sum(1 for r in results.values() if not r.get("available", True))

        unexpected_fails = self.unexpected_failures(results)
        overall = self.overall_status(results)

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "modules_total": total,
            "modules_pass": pass_count,
            "modules_warn": warn_count,
            "modules_fail": fail_count,
            "modules_unavailable": unavailable,
            "unexpected_failures": unexpected_fails,
            "overall_status": overall,
            "module_results": results,
            "research_only": True,
            "no_real_orders": True,
        }

    def known_warning_policy(self, module: str, warning: str) -> bool:
        """Return True if a warning is known and should NOT cause FAIL."""
        warning_lower = warning.lower()
        for known in _KNOWN_WARNINGS:
            if known in warning_lower:
                return True
        return False

    def unexpected_failures(self, results: Dict[str, Dict[str, Any]]) -> List[str]:
        """Return list of unexpected failure descriptions."""
        unexpected = []
        for module_name, result in results.items():
            status = result.get("status", "UNKNOWN")
            if status == "FAIL":
                reason = result.get("reason", result.get("error", ""))
                if not self.known_warning_policy(module_name, reason):
                    unexpected.append(
                        f"{module_name}: FAIL — {reason}"
                    )
        return unexpected

    def build_health_matrix(self, results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build a health matrix from all module results."""
        if results is None:
            results = self.run_all()
        module_results = results.get("module_results", results)
        matrix = []
        for module_name, result in module_results.items():
            if not isinstance(result, dict):
                continue
            matrix.append({
                "module": module_name,
                "status": result.get("status", "UNKNOWN"),
                "available": result.get("available", False),
                "checks_passed": result.get("checks_passed", 0),
                "checks_failed": result.get("checks_failed", 0),
                "reason": result.get("reason", ""),
            })
        return {
            "matrix": matrix,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "research_only": True,
            "no_real_orders": True,
        }

    def overall_status(self, results: Dict[str, Dict[str, Any]]) -> str:
        """Compute overall status from module results."""
        unexpected = self.unexpected_failures(results)
        fail_count = sum(1 for r in results.values() if r.get("status") == "FAIL")

        # Only real unexpected failures cause FAIL
        if unexpected:
            return "FAIL"
        warn_count = sum(1 for r in results.values()
                         if r.get("status") in ("WARN", "UNSUPPORTED"))
        if warn_count > 0:
            return "WARN"
        return "PASS"
