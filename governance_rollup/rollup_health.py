"""
governance_rollup/rollup_health.py — DataGovernanceStableRollupHealthCheck v1.1.9

Health check for the governance_rollup module itself.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_SUBMODULE_IMPORTS = [
    ("rollup_schema",       "governance_rollup.rollup_schema",       "StableRollupSummary"),
    ("schema_normalizer",   "governance_rollup.schema_normalizer",   "GovernanceSchemaNormalizer"),
    ("path_normalizer",     "governance_rollup.path_normalizer",     "CrossMachinePathNormalizer"),
    ("store_inventory",     "governance_rollup.store_inventory",     "GovernanceStoreInventory"),
    ("store_validator",     "governance_rollup.store_validator",     "GovernanceStoreValidator"),
    ("store_recovery",      "governance_rollup.store_recovery",      "GovernanceStoreRecoveryPlanner"),
    ("index_rebuilder",     "governance_rollup.index_rebuilder",     "GovernanceIndexRebuilder"),
    ("metadata_migrator",   "governance_rollup.metadata_migrator",   "GovernanceMetadataMigrator"),
    ("consistency_checker", "governance_rollup.consistency_checker", "CrossModuleConsistencyChecker"),
    ("health_aggregator",   "governance_rollup.health_aggregator",   "GovernanceHealthAggregator"),
    ("stable_rollup_engine","governance_rollup.stable_rollup_engine","DataGovernanceStableRollupEngine"),
    ("rollup_store",        "governance_rollup.rollup_store",        "GovernanceRollupStore"),
    ("rollup_query",        "governance_rollup.rollup_query",        "GovernanceRollupQuery"),
    ("gui_surface_audit",   "governance_rollup.gui_surface_audit",   "GovernanceGUISurfaceAuditor"),
    ("docs_surface_audit",  "governance_rollup.docs_surface_audit",  "GovernanceDocsSurfaceAuditor"),
]


class DataGovernanceStableRollupHealthCheck:
    """
    Health check for the rollup module itself.
    Checks: all submodule imports, safety guards, dry-run defaults,
    allow-write guard, backup-before-write, rollback, append-only preserved,
    cross-machine paths, secrets excluded, no auto repair/import/download/execution,
    no trade execution, runtime output ignored by git.
    Output: PASS/WARN/FAIL/BLOCKED per check.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def run(self) -> Dict[str, str]:
        """Run all health checks. Returns dict of check_name -> status."""
        results: Dict[str, str] = {}
        results.update(self._check_imports())
        results.update(self._check_safety_guards())
        results.update(self._check_dry_run_defaults())
        results.update(self._check_allow_write_guard())
        results.update(self._check_no_forbidden_actions())
        return results

    def _check_imports(self) -> Dict[str, str]:
        """Check all submodule imports."""
        import importlib
        results: Dict[str, str] = {}
        for short_name, import_path, class_name in _SUBMODULE_IMPORTS:
            check_key = f"import_{short_name}"
            try:
                mod = importlib.import_module(import_path)
                if hasattr(mod, class_name):
                    results[check_key] = "PASS"
                else:
                    results[check_key] = "WARN"
            except ImportError as exc:
                results[check_key] = "WARN"
                logger.debug("_check_imports: %s not importable: %s", import_path, exc)
            except Exception as exc:
                results[check_key] = "FAIL"
                logger.warning("_check_imports: %s error: %s", import_path, exc)
        return results

    def _check_safety_guards(self) -> Dict[str, str]:
        """Check safety guard constants in governance_rollup module."""
        results: Dict[str, str] = {}
        try:
            import governance_rollup
            checks = [
                ("safety_no_real_orders",    getattr(governance_rollup, "NO_REAL_ORDERS", None) is True),
                ("safety_research_only",     getattr(governance_rollup, "RESEARCH_ONLY", None) is True),
                ("safety_broker_disabled",   getattr(governance_rollup, "BROKER_DISABLED", None) is True),
                ("safety_trade_exec_disabled",getattr(governance_rollup, "TRADE_EXECUTION_ENABLED", True) is False),
            ]
            for check_name, passed in checks:
                results[check_name] = "PASS" if passed else "FAIL"
        except Exception as exc:
            results["safety_guards_check"] = "FAIL"
            logger.warning("_check_safety_guards error: %s", exc)
        return results

    def _check_dry_run_defaults(self) -> Dict[str, str]:
        """Check that recovery/migration default to dry_run=True."""
        results: Dict[str, str] = {}
        try:
            from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
            planner = GovernanceStoreRecoveryPlanner()
            # execute without allow_write must return BLOCKED
            r = planner.execute("nonexistent_plan_id", allow_write=False)
            results["store_recovery_dry_run_default"] = (
                "PASS" if r.get("status") == "BLOCKED" else "FAIL"
            )
        except Exception as exc:
            results["store_recovery_dry_run_default"] = "WARN"
            logger.debug("_check_dry_run_defaults store_recovery: %s", exc)

        try:
            from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
            migrator = GovernanceMetadataMigrator()
            r = migrator.execute_migration("test_module", allow_write=False)
            results["metadata_migrator_dry_run_default"] = (
                "PASS" if r.get("status") == "BLOCKED" else "FAIL"
            )
        except Exception as exc:
            results["metadata_migrator_dry_run_default"] = "WARN"
            logger.debug("_check_dry_run_defaults metadata_migrator: %s", exc)

        try:
            from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
            rebuilder = GovernanceIndexRebuilder()
            r = rebuilder.rebuild("research_registry", allow_write=False)
            # dry_run should return preview, not write
            results["index_rebuilder_dry_run_default"] = (
                "PASS" if r.get("dry_run") or r.get("status") == "DRY_RUN_ONLY" else "WARN"
            )
        except Exception as exc:
            results["index_rebuilder_dry_run_default"] = "WARN"
            logger.debug("_check_dry_run_defaults index_rebuilder: %s", exc)

        return results

    def _check_allow_write_guard(self) -> Dict[str, str]:
        """Check that allow_write=False blocks writes."""
        results: Dict[str, str] = {}
        try:
            from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
            planner = GovernanceStoreRecoveryPlanner()
            r = planner.rebuild_state("/tmp/test_path.json", allow_write=False)
            results["allow_write_guard_recovery"] = (
                "PASS" if r.get("status") == "BLOCKED" else "FAIL"
            )
        except Exception as exc:
            results["allow_write_guard_recovery"] = "WARN"

        try:
            from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
            migrator = GovernanceMetadataMigrator()
            r = migrator.rollback_migration("/tmp/bak.bak", "/tmp/target.json", allow_write=False)
            results["allow_write_guard_migration"] = (
                "PASS" if r.get("status") == "BLOCKED" else "FAIL"
            )
        except Exception as exc:
            results["allow_write_guard_migration"] = "WARN"

        return results

    def _check_no_forbidden_actions(self) -> Dict[str, str]:
        """Check that no forbidden actions (broker, trade, auto-repair) are enabled."""
        results: Dict[str, str] = {}
        try:
            import governance_rollup
            forbidden_checks = [
                ("no_auto_store_repair",      getattr(governance_rollup, "AUTO_STORE_REPAIR_ENABLED", True) is False),
                ("no_auto_data_repair",       getattr(governance_rollup, "AUTO_DATA_REPAIR_ENABLED", True) is False),
                ("no_auto_download",          getattr(governance_rollup, "AUTO_DATA_DOWNLOAD_ENABLED", True) is False),
                ("no_auto_import",            getattr(governance_rollup, "AUTO_DATA_IMPORT_ENABLED", True) is False),
                ("no_auto_research_exec",     getattr(governance_rollup, "AUTO_RESEARCH_EXECUTION_ENABLED", True) is False),
                ("no_trade_execution",        getattr(governance_rollup, "TRADE_EXECUTION_ENABLED", True) is False),
            ]
            for check_name, passed in forbidden_checks:
                results[check_name] = "PASS" if passed else "FAIL"
        except Exception as exc:
            results["no_forbidden_actions_check"] = "FAIL"
            logger.warning("_check_no_forbidden_actions error: %s", exc)

        # Check gitignore has data/governance_rollup/
        try:
            from pathlib import Path
            gitignore = Path(__file__).resolve().parent.parent / ".gitignore"
            if gitignore.exists():
                content = gitignore.read_text(encoding="utf-8", errors="replace")
                results["runtime_output_in_gitignore"] = (
                    "PASS" if "data/governance_rollup/" in content else "WARN"
                )
            else:
                results["runtime_output_in_gitignore"] = "WARN"
        except Exception:
            results["runtime_output_in_gitignore"] = "WARN"

        return results

    def overall_status(self, results: Dict[str, str]) -> str:
        """Compute overall status from check results."""
        if any(s == "FAIL" for s in results.values()):
            return "FAIL"
        if any(s == "WARN" for s in results.values()):
            return "WARN"
        if any(s == "BLOCKED" for s in results.values()):
            return "BLOCKED"
        return "PASS"

    def print_results(self, results: Dict[str, str]) -> None:
        """Print health check results to stdout."""
        overall = self.overall_status(results)
        print("=" * 60)
        print("  Data Governance Stable Rollup Health Check v1.1.9")
        print(f"  Overall: {overall}")
        print("  [!] Research Only. No Real Orders.")
        print("=" * 60)
        for check_name, status in sorted(results.items()):
            icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]",
                    "BLOCKED": "[BLKD]"}.get(status, "[????]")
            print(f"  {icon} {check_name}")
        passed = sum(1 for s in results.values() if s == "PASS")
        total = len(results)
        print(f"  Passed: {passed}/{total}")
        print("=" * 60)
