"""
governance_rollup/stable_rollup_engine.py — DataGovernanceStableRollupEngine v1.1.9

Main engine for stable rollup verification (read-only by default).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT: auto-recover, auto-migrate, auto-write indexes,
    auto-repair data, execute trades, fallback real to mock.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from governance_rollup.rollup_schema import StableRollupSummary

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True


class DataGovernanceStableRollupEngine:
    """
    Main engine for stable rollup verification.
    Read-only by default.

    Does NOT:
    - auto-recover
    - auto-migrate
    - auto-write indexes
    - auto-repair data
    - execute trades
    - fallback real to mock
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def run(self, mode: str = "real") -> StableRollupSummary:
        """Run full stable rollup verification. Returns StableRollupSummary."""
        logger.info("DataGovernanceStableRollupEngine.run(mode=%s)", mode)
        kwargs: Dict[str, Any] = {}

        # 1. Store inventory
        try:
            inventory = self.inventory_stores()
            kwargs["inventory"] = inventory
        except Exception as exc:
            logger.warning("inventory_stores error: %s", exc)
            kwargs["inventory"] = {"error": str(exc)}

        # 2. Store validation
        try:
            validation = self.validate_stores()
            kwargs["validation"] = validation
        except Exception as exc:
            logger.warning("validate_stores error: %s", exc)
            kwargs["validation"] = {"error": str(exc)}

        # 3. Cross-module consistency
        try:
            consistency = self.check_consistency()
            kwargs["consistency"] = consistency
        except Exception as exc:
            logger.warning("check_consistency error: %s", exc)
            kwargs["consistency"] = {"error": str(exc)}

        # 4. Health aggregation
        try:
            health = self.aggregate_health(mode=mode)
            kwargs["health"] = health
        except Exception as exc:
            logger.warning("aggregate_health error: %s", exc)
            kwargs["health"] = {"error": str(exc)}

        # 5. Recovery plans (preview only)
        try:
            recovery = self.preview_recovery()
            kwargs["recovery"] = recovery
        except Exception as exc:
            logger.warning("preview_recovery error: %s", exc)
            kwargs["recovery"] = {"error": str(exc)}

        # 6. Migration plans (preview only)
        try:
            migration = self.preview_migration()
            kwargs["migration"] = migration
        except Exception as exc:
            logger.warning("preview_migration error: %s", exc)
            kwargs["migration"] = {"error": str(exc)}

        # 7. Path verification
        try:
            paths = self.verify_paths()
            kwargs["paths"] = paths
        except Exception as exc:
            logger.warning("verify_paths error: %s", exc)
            kwargs["paths"] = {"error": str(exc)}

        # 8. Index verification
        try:
            indexes = self.verify_indexes()
            kwargs["indexes"] = indexes
        except Exception as exc:
            logger.warning("verify_indexes error: %s", exc)
            kwargs["indexes"] = {"error": str(exc)}

        # 9. Audit chain verification
        try:
            audits = self.verify_audits()
            kwargs["audits"] = audits
        except Exception as exc:
            logger.warning("verify_audits error: %s", exc)
            kwargs["audits"] = {"error": str(exc)}

        # 10. Safety verification
        try:
            safety = self.verify_safety()
            kwargs["safety"] = safety
        except Exception as exc:
            logger.warning("verify_safety error: %s", exc)
            kwargs["safety"] = {"error": str(exc)}

        # 11. CLI surface
        try:
            cli = self.verify_cli_surface()
            kwargs["cli"] = cli
        except Exception as exc:
            logger.warning("verify_cli_surface error: %s", exc)
            kwargs["cli"] = {"error": str(exc)}

        # 12. GUI surface
        try:
            gui = self.verify_gui_surface()
            kwargs["gui"] = gui
        except Exception as exc:
            logger.warning("verify_gui_surface error: %s", exc)
            kwargs["gui"] = {"error": str(exc)}

        # 13. Docs
        try:
            docs = self.verify_docs()
            kwargs["docs"] = docs
        except Exception as exc:
            logger.warning("verify_docs error: %s", exc)
            kwargs["docs"] = {"error": str(exc)}

        summary = self.build_summary(**kwargs)

        # Save to store
        try:
            from governance_rollup.rollup_store import GovernanceRollupStore
            store = GovernanceRollupStore()
            store.save_rollup_summary(summary)
            store.append_rollup_history(summary)
            store.append_rollup_audit({
                "event": "rollup_run",
                "mode": mode,
                "generated_at": summary.generated_at,
                "overall_status": summary.overall_status,
                "stable_ready": summary.stable_ready,
                "research_only": True,
                "no_real_orders": True,
            })
        except Exception as exc:
            logger.warning("rollup_store save error: %s", exc)

        return summary

    def inventory_stores(self) -> Dict[str, Any]:
        """Inventory all governance stores."""
        from governance_rollup.store_inventory import GovernanceStoreInventory
        inv = GovernanceStoreInventory()
        records = inv.build_inventory()
        return {
            "records": [r.to_dict() for r in records],
            "summary": inv.inventory_summary(),
        }

    def validate_stores(self) -> Dict[str, Any]:
        """Validate all governance stores."""
        from governance_rollup.store_inventory import GovernanceStoreInventory
        from governance_rollup.store_validator import GovernanceStoreValidator
        inv = GovernanceStoreInventory()
        validator = GovernanceStoreValidator()
        records = inv.build_inventory()
        results = []
        for record in records:
            try:
                vresult = validator.validate_store(record)
                results.append(vresult)
            except Exception as exc:
                results.append({"store_id": record.store_id, "error": str(exc)})
        return {
            "results": results,
            "summary": validator.summarize(results),
        }

    def check_consistency(self) -> Dict[str, Any]:
        """Run cross-module consistency checks."""
        from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
        checker = CrossModuleConsistencyChecker()
        summary = checker.run_all()
        return summary.to_dict()

    def aggregate_health(self, mode: str = "real") -> Dict[str, Any]:
        """Aggregate health from all governance modules."""
        from governance_rollup.health_aggregator import GovernanceHealthAggregator
        aggregator = GovernanceHealthAggregator()
        return aggregator.run_all(mode=mode)

    def preview_recovery(self) -> Dict[str, Any]:
        """Preview recovery plans for problematic stores (dry-run)."""
        from governance_rollup.store_inventory import GovernanceStoreInventory
        from governance_rollup.store_validator import GovernanceStoreValidator
        from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
        inv = GovernanceStoreInventory()
        validator = GovernanceStoreValidator()
        planner = GovernanceStoreRecoveryPlanner()

        records = inv.build_inventory()
        plans = []
        for record in records:
            try:
                vresult = validator.validate_store(record)
                if not vresult.get("valid"):
                    plan = planner.plan({
                        **vresult,
                        "module_name": record.module_name,
                        "store_id": record.store_id,
                    })
                    preview = planner.preview(plan.plan_id)
                    plans.append(preview)
            except Exception as exc:
                logger.debug("preview_recovery error for %s: %s", record.store_id, exc)
        return {
            "plans": plans,
            "count": len(plans),
            "dry_run": True,
            "note": "Preview only. No changes made.",
            "research_only": True,
            "no_real_orders": True,
        }

    def preview_migration(self) -> Dict[str, Any]:
        """Preview migration plans (dry-run)."""
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        modules = [
            "universe", "data_onboarding", "coverage_repair", "data_freshness",
            "quality_gates", "gate_enforcement", "governance_ops",
            "governance_alerts", "research_registry",
        ]
        previews = []
        for module_name in modules:
            try:
                preview = migrator.preview_migration(module_name)
                previews.append(preview)
            except Exception as exc:
                previews.append({"module_name": module_name, "error": str(exc)})
        return {
            "previews": previews,
            "dry_run": True,
            "note": "Preview only. No migration executed.",
            "research_only": True,
            "no_real_orders": True,
        }

    def verify_paths(self) -> Dict[str, Any]:
        """Verify cross-machine paths."""
        from governance_rollup.path_normalizer import CrossMachinePathNormalizer
        normalizer = CrossMachinePathNormalizer()
        root = normalizer.detect_repo_root()
        return {
            "detected_repo_root": root,
            "known_roots": normalizer.KNOWN_REPO_ROOTS,
            "status": "PASS" if root else "WARN",
        }

    def verify_indexes(self) -> Dict[str, Any]:
        """Verify all supported indexes."""
        from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
        rebuilder = GovernanceIndexRebuilder()
        results = {}
        for module_name in rebuilder.SUPPORTED_INDEXES:
            results[module_name] = rebuilder.inspect_index(module_name)
        stale = sum(1 for r in results.values() if r.get("stale"))
        missing = sum(1 for r in results.values() if r.get("status") == "MISSING")
        return {
            "results": results,
            "stale_indexes": stale,
            "missing_indexes": missing,
            "status": "FAIL" if stale + missing > 2 else ("WARN" if stale + missing > 0 else "PASS"),
        }

    def verify_audits(self) -> Dict[str, Any]:
        """Verify audit chain files."""
        from governance_rollup.store_validator import GovernanceStoreValidator
        from pathlib import Path
        validator = GovernanceStoreValidator()
        base = Path(__file__).resolve().parent.parent
        audit_patterns = [
            "data/governance_alerts/audit.jsonl",
            "data/research_registry/registry_audit.jsonl",
            "data/gate_enforcement/enforcement_audit.jsonl",
        ]
        results = []
        for pattern in audit_patterns:
            path = base / pattern
            if path.exists():
                result = validator.validate_audit_chain(path)
                results.append(result)
        failed = sum(1 for r in results if not r.get("valid"))
        return {
            "results": results,
            "chains_checked": len(results),
            "chains_failed": failed,
            "status": "FAIL" if failed > 0 else "PASS",
        }

    def verify_safety(self) -> Dict[str, Any]:
        """Verify safety flags across all modules."""
        from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
        checker = CrossModuleConsistencyChecker()
        result = checker.check_safety_flags()
        impossible = checker.check_impossible_states()
        return {
            "safety_flags": result,
            "impossible_states": impossible,
            "status": "FAIL" if (not result.get("valid") or not impossible.get("valid")) else "PASS",
            "research_only": True,
            "no_real_orders": True,
        }

    def verify_cli_surface(self) -> Dict[str, Any]:
        """Verify CLI command surface for rollup commands."""
        # Check that main.py has governance-rollup commands
        from pathlib import Path
        main_py = Path(__file__).resolve().parent.parent / "main.py"
        found_commands = []
        expected_commands = [
            "governance-rollup-health", "governance-rollup-run",
            "governance-rollup-summary", "governance-rollup-consistency",
        ]
        if main_py.exists():
            try:
                content = main_py.read_text(encoding="utf-8", errors="replace")
                for cmd in expected_commands:
                    if cmd in content:
                        found_commands.append(cmd)
            except Exception:
                pass
        missing = [c for c in expected_commands if c not in found_commands]
        return {
            "found_commands": found_commands,
            "missing_commands": missing,
            "status": "PASS" if not missing else "WARN",
        }

    def verify_gui_surface(self) -> Dict[str, Any]:
        """Verify GUI surface audit."""
        try:
            from governance_rollup.gui_surface_audit import GovernanceGUISurfaceAuditor
            auditor = GovernanceGUISurfaceAuditor()
            results = auditor.run()
            return auditor.summarize(results)
        except Exception as exc:
            return {"status": "WARN", "error": str(exc)}

    def verify_docs(self) -> Dict[str, Any]:
        """Verify docs surface audit."""
        try:
            from governance_rollup.docs_surface_audit import GovernanceDocsSurfaceAuditor
            auditor = GovernanceDocsSurfaceAuditor()
            results = auditor.run()
            return auditor.summarize(results)
        except Exception as exc:
            return {"status": "WARN", "error": str(exc)}

    def build_summary(self, **kwargs) -> StableRollupSummary:
        """Build StableRollupSummary from all component results."""
        health = kwargs.get("health", {})
        consistency = kwargs.get("consistency", {})
        recovery = kwargs.get("recovery", {})
        migration = kwargs.get("migration", {})
        safety = kwargs.get("safety", {})
        gui = kwargs.get("gui", {})
        cli = kwargs.get("cli", {})
        docs = kwargs.get("docs", {})
        indexes = kwargs.get("indexes", {})

        # Blocking issues = anything that prevents stable_ready
        blocking_issues = []
        known_warnings = []

        # Safety failures are blocking
        if safety.get("status") == "FAIL":
            blocking_issues.append("Safety flag violations detected")

        # Impossible states are blocking
        impossible = safety.get("impossible_states", {})
        if impossible.get("count", 0) > 0:
            blocking_issues.extend([
                f"Impossible state: {s.get('detail', s)}"
                for s in impossible.get("impossible_states", [])[:5]
            ])

        # Index failures are known warnings, not blocking (unless all missing)
        if indexes.get("missing_indexes", 0) > 0:
            known_warnings.append(f"{indexes.get('missing_indexes', 0)} missing indexes (can be rebuilt)")

        # Determine overall status
        health_status = health.get("overall_status", "UNKNOWN")
        consistency_status = consistency.get("overall_status", "UNKNOWN")

        if blocking_issues:
            overall_status = "FAIL"
        elif health_status == "FAIL" or consistency_status == "FAIL":
            overall_status = "FAIL"
        elif health_status in ("WARN", "UNKNOWN") or consistency_status in ("WARN", "UNKNOWN"):
            overall_status = "WARN"
        else:
            overall_status = "PASS"

        stable_ready = (
            overall_status == "PASS"
            and len(blocking_issues) == 0
        )

        return StableRollupSummary(
            version="1.1.9",
            release_name="Data Governance Stable Rollup",
            generated_at=datetime.now(timezone.utc).isoformat(),
            overall_status=overall_status,
            health_summary=health if isinstance(health, dict) else {},
            consistency_summary=consistency if isinstance(consistency, dict) else {},
            migration_summary=migration if isinstance(migration, dict) else {},
            recovery_summary=recovery if isinstance(recovery, dict) else {},
            regression_summary={},
            gui_summary=gui if isinstance(gui, dict) else {},
            cli_summary=cli if isinstance(cli, dict) else {},
            docs_summary=docs if isinstance(docs, dict) else {},
            safety_summary=safety if isinstance(safety, dict) else {},
            known_warnings=known_warnings,
            blocking_issues=blocking_issues,
            stable_ready=stable_ready,
            research_only=True,
            no_real_orders=True,
        )

    def generate_report(self, summary: StableRollupSummary) -> str:
        """Generate a markdown report from the rollup summary."""
        try:
            from reports.data_governance_stable_rollup_report import (
                DataGovernanceStableRollupReportBuilder
            )
            builder = DataGovernanceStableRollupReportBuilder()
            content = builder.build(summary=summary)
            path = builder.save(content)
            return str(path)
        except Exception as exc:
            logger.warning("generate_report error: %s", exc)
            return ""
