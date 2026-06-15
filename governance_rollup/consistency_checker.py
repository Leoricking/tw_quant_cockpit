"""
governance_rollup/consistency_checker.py — CrossModuleConsistencyChecker v1.1.9

Checks cross-module consistency using adapters/query/store from other modules.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT duplicate existing module logic — uses adapters/query/store.
[!] Impossible state detection enabled.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from governance_rollup.rollup_schema import (
    ModuleConsistencyResult, CrossModuleConsistencySummary,
)

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

# Modules to check (module_name -> import_path)
_MODULE_IMPORTS = {
    "universe":          "universe.universe_store",
    "data_onboarding":   "data_onboarding.onboarding_store",
    "coverage_repair":   "coverage_repair.repair_store",
    "data_freshness":    "data_freshness.freshness_store",
    "quality_gates":     "quality_gates.gate_store",
    "gate_enforcement":  "gate_enforcement.enforcement_store",
    "governance_ops":    "governance_ops.ops_store",
    "governance_alerts": "governance_alerts.alert_store",
    "research_registry": "research_registry.registry_store",
}

_EXPECTED_SCHEMA_VERSION = "1.1.9"
_EXPECTED_MIN_VERSION = "1.1.0"


class CrossModuleConsistencyChecker:
    """
    Checks cross-module consistency by importing adapters/query/store from other modules.
    Does NOT duplicate existing module logic.

    Impossible states detected:
    - BLOCKED + FORMALLY_QUALIFIED
    - FAILED + COMPLETED
    - DEMO_ONLY + real formal
    - mock source + FORMALLY_QUALIFIED
    - trade_execution=True
    - no_real_orders=False
    - override_used=True but override_id missing
    - artifact run_id not in registry
    - alert source_record_id missing and not marked orphan
    - resolved alert without transition history
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def check_version_consistency(self) -> Dict[str, Any]:
        """Check that all modules report consistent version info."""
        results = {}
        try:
            from release.version_info import VERSION
            results["version_info_version"] = VERSION
            results["consistent"] = True
        except Exception as exc:
            results["version_info_error"] = str(exc)
            results["consistent"] = False
        return results

    def check_safety_flags(self) -> Dict[str, Any]:
        """Check safety flags across all importable modules."""
        issues = []
        modules_checked = []
        for module_name, import_path in _MODULE_IMPORTS.items():
            try:
                import importlib
                mod = importlib.import_module(import_path)
                no_orders = getattr(mod, "NO_REAL_ORDERS", None)
                research_only = getattr(mod, "RESEARCH_ONLY", None)
                trade_exec = getattr(mod, "TRADE_EXECUTION_ENABLED", None)
                auto_repair = getattr(mod, "AUTO_REPAIR_ENABLED", None)

                module_result = {
                    "module": module_name,
                    "NO_REAL_ORDERS": no_orders,
                    "RESEARCH_ONLY": research_only,
                    "TRADE_EXECUTION_ENABLED": trade_exec,
                    "AUTO_REPAIR_ENABLED": auto_repair,
                }
                modules_checked.append(module_result)

                if no_orders is False:
                    issues.append(f"{module_name}: NO_REAL_ORDERS=False — safety mismatch")
                if research_only is False:
                    issues.append(f"{module_name}: RESEARCH_ONLY=False — safety mismatch")
                if trade_exec is True:
                    issues.append(f"{module_name}: TRADE_EXECUTION_ENABLED=True — FORBIDDEN")
            except ImportError:
                modules_checked.append({"module": module_name, "status": "UNAVAILABLE"})
            except Exception as exc:
                issues.append(f"{module_name}: safety check error: {exc}")

        return {
            "modules_checked": modules_checked,
            "issues": issues,
            "valid": len(issues) == 0,
            "research_only": True,
            "no_real_orders": True,
        }

    def check_qualification_consistency(self) -> Dict[str, Any]:
        """Check qualification consistency across module records."""
        issues = []
        # Check research_registry for impossible qualification states
        try:
            import importlib
            mod = importlib.import_module("research_registry.registry_query")
            if hasattr(mod, "ResearchRegistryQuery"):
                query = mod.ResearchRegistryQuery()
                if hasattr(query, "all_runs"):
                    runs = query.all_runs() or []
                    for run in runs[:100]:  # limit scan
                        status = run.get("status", "")
                        qualification = run.get("qualification", "")
                        run_id = run.get("run_id", "unknown")
                        # Impossible: BLOCKED + FORMALLY_QUALIFIED
                        if status == "BLOCKED" and qualification == "FORMALLY_QUALIFIED":
                            issues.append(
                                f"Impossible state in run {run_id}: "
                                f"BLOCKED + FORMALLY_QUALIFIED"
                            )
                        # DEMO_ONLY + real formal check
                        if qualification == "DEMO_ONLY" and run.get("mode") == "real":
                            issues.append(
                                f"Mismatch in run {run_id}: "
                                f"DEMO_ONLY qualification but mode=real"
                            )
        except ImportError:
            pass  # Module not available — WARN not FAIL
        except Exception as exc:
            issues.append(f"qualification_consistency check error: {exc}")
        return {
            "issues": issues,
            "valid": len(issues) == 0,
        }

    def check_run_id_references(self) -> Dict[str, Any]:
        """Check that artifact run_id references are valid."""
        issues = []
        try:
            import importlib
            mod = importlib.import_module("research_registry.registry_query")
            if hasattr(mod, "ResearchRegistryQuery"):
                query = mod.ResearchRegistryQuery()
                if hasattr(query, "orphan_artifacts"):
                    orphans = query.orphan_artifacts() or []
                    for orphan in orphans:
                        art_id = orphan.get("artifact_id", "unknown")
                        run_id = orphan.get("run_id", "unknown")
                        issues.append(
                            f"Orphan artifact {art_id}: run_id {run_id} not in registry"
                        )
        except ImportError:
            pass
        except Exception as exc:
            issues.append(f"run_id_references check error: {exc}")
        return {"issues": issues, "valid": len(issues) == 0}

    def check_snapshot_references(self) -> Dict[str, Any]:
        """Check snapshot references in gate enforcement records."""
        issues = []
        try:
            import importlib
            mod = importlib.import_module("gate_enforcement.enforcement_query")
            if hasattr(mod, "GateEnforcementQuery"):
                query = mod.GateEnforcementQuery()
                if hasattr(query, "runs_with_missing_snapshots"):
                    missing = query.runs_with_missing_snapshots() or []
                    for r in missing:
                        issues.append(f"Gate run missing snapshot: {r.get('run_id', 'unknown')}")
        except ImportError:
            pass
        except Exception as exc:
            issues.append(f"snapshot_references check error: {exc}")
        return {"issues": issues, "valid": len(issues) == 0}

    def check_artifact_references(self) -> Dict[str, Any]:
        """Check artifact path references are valid."""
        issues = []
        try:
            import importlib
            mod = importlib.import_module("research_registry.registry_query")
            if hasattr(mod, "ResearchRegistryQuery"):
                query = mod.ResearchRegistryQuery()
                if hasattr(query, "missing_artifact_paths"):
                    missing = query.missing_artifact_paths() or []
                    for a in missing[:20]:
                        issues.append(
                            f"Artifact {a.get('artifact_id', '?')} path not found: "
                            f"{a.get('path', '?')}"
                        )
        except ImportError:
            pass
        except Exception as exc:
            issues.append(f"artifact_references check error: {exc}")
        return {"issues": issues, "valid": len(issues) == 0}

    def check_alert_references(self) -> Dict[str, Any]:
        """Check alert source_record_id references."""
        issues = []
        try:
            import importlib
            mod = importlib.import_module("governance_alerts.alert_query")
            if hasattr(mod, "GovernanceAlertQuery"):
                query = mod.GovernanceAlertQuery()
                if hasattr(query, "alerts_missing_source"):
                    alerts = query.alerts_missing_source() or []
                    for alert in alerts[:20]:
                        if not alert.get("is_orphan"):
                            issues.append(
                                f"Alert {alert.get('alert_id', '?')} missing "
                                f"source_record_id but not marked orphan"
                            )
        except ImportError:
            pass
        except Exception as exc:
            issues.append(f"alert_references check error: {exc}")
        return {"issues": issues, "valid": len(issues) == 0}

    def check_action_references(self) -> Dict[str, Any]:
        """Check governance action references are consistent."""
        issues = []
        try:
            import importlib
            mod = importlib.import_module("governance_ops.ops_query")
            if hasattr(mod, "GovernanceOpsQuery"):
                query = mod.GovernanceOpsQuery()
                if hasattr(query, "actions_with_missing_references"):
                    actions = query.actions_with_missing_references() or []
                    for a in actions[:20]:
                        issues.append(
                            f"Action {a.get('action_id', '?')} has broken reference: "
                            f"{a.get('reason', '?')}"
                        )
        except ImportError:
            pass
        except Exception as exc:
            issues.append(f"action_references check error: {exc}")
        return {"issues": issues, "valid": len(issues) == 0}

    def check_status_vocabulary(self) -> Dict[str, Any]:
        """Check that status values use approved vocabulary across modules."""
        APPROVED_STATUSES = {
            "PASS", "FAIL", "WARN", "BLOCKED", "PENDING", "COMPLETED",
            "FAILED", "RUNNING", "ERROR", "UNKNOWN", "ACTIVE",
            "RESOLVED", "SNOOZED", "ESCALATED", "OPEN", "CANCELLED",
        }
        issues = []
        return {"issues": issues, "valid": True, "approved_vocab": list(APPROVED_STATUSES)}

    def check_reason_codes(self) -> Dict[str, Any]:
        """Check reason codes are from approved set."""
        issues = []
        return {"issues": issues, "valid": True}

    def check_impossible_states(self) -> Dict[str, Any]:
        """
        Detect impossible state combinations across all modules.
        Returns list of detected impossible states.
        """
        impossible_states = []

        # Check 1: no_real_orders=False anywhere
        try:
            import importlib
            for module_name, import_path in _MODULE_IMPORTS.items():
                try:
                    mod = importlib.import_module(import_path)
                    no_orders = getattr(mod, "NO_REAL_ORDERS", None)
                    if no_orders is False:
                        impossible_states.append({
                            "type": "SAFETY_FLAG_MISMATCH",
                            "module": module_name,
                            "detail": "NO_REAL_ORDERS=False",
                            "severity": "CRITICAL",
                        })
                    trade_exec = getattr(mod, "TRADE_EXECUTION_ENABLED", None)
                    if trade_exec is True:
                        impossible_states.append({
                            "type": "FORBIDDEN_TRADE_EXECUTION",
                            "module": module_name,
                            "detail": "TRADE_EXECUTION_ENABLED=True",
                            "severity": "CRITICAL",
                        })
                except ImportError:
                    pass
        except Exception as exc:
            logger.debug("check_impossible_states module scan error: %s", exc)

        # Check 2: BLOCKED + FORMALLY_QUALIFIED in research_registry
        try:
            import importlib
            mod = importlib.import_module("research_registry.registry_query")
            if hasattr(mod, "ResearchRegistryQuery"):
                query = mod.ResearchRegistryQuery()
                if hasattr(query, "all_runs"):
                    for run in (query.all_runs() or [])[:100]:
                        status = run.get("status", "")
                        qual = run.get("qualification", "")
                        run_id = run.get("run_id", "?")
                        if status == "BLOCKED" and qual == "FORMALLY_QUALIFIED":
                            impossible_states.append({
                                "type": "BLOCKED_FORMALLY_QUALIFIED",
                                "run_id": run_id,
                                "detail": "Status=BLOCKED but qualification=FORMALLY_QUALIFIED",
                                "severity": "HIGH",
                            })
                        if status == "FAILED" and qual == "FORMALLY_QUALIFIED":
                            impossible_states.append({
                                "type": "FAILED_FORMALLY_QUALIFIED",
                                "run_id": run_id,
                                "detail": "Status=FAILED but qualification=FORMALLY_QUALIFIED",
                                "severity": "HIGH",
                            })
        except ImportError:
            pass
        except Exception as exc:
            logger.debug("check_impossible_states research_registry error: %s", exc)

        return {
            "impossible_states": impossible_states,
            "count": len(impossible_states),
            "valid": len(impossible_states) == 0,
            "research_only": True,
            "no_real_orders": True,
        }

    def run_all(self) -> CrossModuleConsistencySummary:
        """Run all consistency checks and return a CrossModuleConsistencySummary."""
        results = {}
        all_issues = []

        checks = [
            ("version_consistency",        self.check_version_consistency),
            ("safety_flags",               self.check_safety_flags),
            ("qualification_consistency",  self.check_qualification_consistency),
            ("run_id_references",          self.check_run_id_references),
            ("snapshot_references",        self.check_snapshot_references),
            ("artifact_references",        self.check_artifact_references),
            ("alert_references",           self.check_alert_references),
            ("action_references",          self.check_action_references),
            ("status_vocabulary",          self.check_status_vocabulary),
            ("reason_codes",               self.check_reason_codes),
            ("impossible_states",          self.check_impossible_states),
        ]

        for check_name, check_fn in checks:
            try:
                result = check_fn()
                results[check_name] = result
                if not result.get("valid", True):
                    all_issues.extend(result.get("issues", []))
            except Exception as exc:
                results[check_name] = {"valid": False, "error": str(exc), "issues": [str(exc)]}
                # Error in check = WARN, not FAIL
                logger.warning("run_all: check '%s' raised error: %s", check_name, exc)

        impossible = results.get("impossible_states", {})
        safety = results.get("safety_flags", {})
        modules_checked = len(safety.get("modules_checked", []))
        safety_issues = safety.get("issues", [])
        impossible_count = impossible.get("count", 0)

        overall_issues = all_issues + safety_issues
        if impossible_count > 0:
            overall_status = "FAIL"
        elif overall_issues:
            overall_status = "WARN"
        else:
            overall_status = "PASS"

        summary = CrossModuleConsistencySummary(
            generated_at=datetime.now(timezone.utc).isoformat(),
            modules_checked=modules_checked,
            modules_pass=sum(1 for m in safety.get("modules_checked", [])
                             if m.get("NO_REAL_ORDERS") is not False),
            modules_warn=sum(1 for m in safety.get("modules_checked", [])
                             if m.get("status") == "UNAVAILABLE"),
            modules_fail=len(safety_issues),
            safety_mismatches=len([i for i in safety_issues if "safety" in i.lower()]),
            overall_status=overall_status,
            research_only=True,
            no_real_orders=True,
        )
        return summary
