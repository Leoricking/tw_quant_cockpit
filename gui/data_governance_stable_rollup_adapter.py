"""
gui/data_governance_stable_rollup_adapter.py — DataGovernanceStableRollupAdapter v1.1.9

Adapter connecting the GUI panel to governance_rollup modules.
Read-only operations only.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No execute recovery, no execute migration, no auto repair, no trading.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class DataGovernanceStableRollupAdapter:
    """
    Adapter connecting GUI panel to governance_rollup modules.
    Read-only operations only.
    """

    NO_REAL_ORDERS = True
    RESEARCH_ONLY = True

    def run_rollup(self, mode: str = "real") -> Dict[str, Any]:
        """Run the full stable rollup engine."""
        try:
            from governance_rollup.stable_rollup_engine import DataGovernanceStableRollupEngine
            engine = DataGovernanceStableRollupEngine()
            summary = engine.run(mode=mode)
            return summary.to_dict()
        except Exception as exc:
            logger.error("run_rollup error: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    def latest_summary(self) -> Optional[Dict[str, Any]]:
        """Return the latest rollup summary."""
        try:
            from governance_rollup.rollup_query import GovernanceRollupQuery
            query = GovernanceRollupQuery()
            return query.latest_summary()
        except Exception as exc:
            logger.error("latest_summary error: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    def validate_stores(self) -> Dict[str, Any]:
        """Validate all governance stores (read-only)."""
        try:
            from governance_rollup.store_inventory import GovernanceStoreInventory
            from governance_rollup.store_validator import GovernanceStoreValidator
            inv = GovernanceStoreInventory()
            validator = GovernanceStoreValidator()
            records = inv.build_inventory()
            results = []
            corrupted = []
            for record in records:
                vresult = validator.validate_store(record)
                results.append(vresult)
                if "CORRUPT" in vresult.get("status", ""):
                    corrupted.append({
                        "store_id": record.store_id,
                        "status": vresult.get("status"),
                        "issues": vresult.get("issues", []),
                    })
            return {
                "total": len(results),
                "valid": sum(1 for r in results if r.get("valid")),
                "invalid": sum(1 for r in results if not r.get("valid")),
                "corrupted": corrupted,
                "results": results,
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.error("validate_stores error: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    def check_consistency(self) -> Dict[str, Any]:
        """Run cross-module consistency check (read-only)."""
        try:
            from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
            checker = CrossModuleConsistencyChecker()
            summary = checker.run_all()
            return summary.to_dict()
        except Exception as exc:
            logger.error("check_consistency error: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    def verify_paths(self) -> Dict[str, Any]:
        """Verify cross-machine paths."""
        try:
            from governance_rollup.path_normalizer import CrossMachinePathNormalizer
            normalizer = CrossMachinePathNormalizer()
            root = normalizer.detect_repo_root()
            return {
                "detected_repo_root": root,
                "known_roots": normalizer.KNOWN_REPO_ROOTS,
                "status": "PASS" if root else "WARN",
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            return {"status": "ERROR", "error": str(exc)}

    def verify_indexes(self) -> Dict[str, Any]:
        """Verify index status for all modules."""
        try:
            from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
            rebuilder = GovernanceIndexRebuilder()
            results = {}
            for module_name in rebuilder.SUPPORTED_INDEXES:
                results[module_name] = rebuilder.inspect_index(module_name)
            return {
                "results": results,
                "stale": sum(1 for r in results.values() if r.get("stale")),
                "missing": sum(1 for r in results.values() if r.get("status") == "MISSING"),
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            return {"status": "ERROR", "error": str(exc)}

    def preview_recovery(self) -> Dict[str, Any]:
        """Preview recovery plans (dry-run, no writes)."""
        try:
            from governance_rollup.stable_rollup_engine import DataGovernanceStableRollupEngine
            engine = DataGovernanceStableRollupEngine()
            return engine.preview_recovery()
        except Exception as exc:
            return {"status": "ERROR", "error": str(exc)}

    def preview_migration(self) -> Dict[str, Any]:
        """Preview migration plans (dry-run, no writes)."""
        try:
            from governance_rollup.stable_rollup_engine import DataGovernanceStableRollupEngine
            engine = DataGovernanceStableRollupEngine()
            return engine.preview_migration()
        except Exception as exc:
            return {"status": "ERROR", "error": str(exc)}

    def build_report(self) -> Dict[str, Any]:
        """Build rollup report (read-only, writes report file only)."""
        try:
            from reports.data_governance_stable_rollup_report import (
                DataGovernanceStableRollupReportBuilder
            )
            builder = DataGovernanceStableRollupReportBuilder()
            content = builder.build()
            path = builder.save(content)
            return {
                "status": "COMPLETED",
                "report_path": str(path),
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            return {"status": "ERROR", "error": str(exc)}

    def store_inventory(self) -> List[Dict[str, Any]]:
        """Return store inventory records."""
        try:
            from governance_rollup.rollup_query import GovernanceRollupQuery
            query = GovernanceRollupQuery()
            return query.store_inventory()
        except Exception as exc:
            return []

    def rollup_history(self) -> List[Dict[str, Any]]:
        """Return rollup history."""
        try:
            from governance_rollup.rollup_query import GovernanceRollupQuery
            query = GovernanceRollupQuery()
            return query.rollup_history()
        except Exception as exc:
            return []

    def module_consistency(self) -> List[Dict[str, Any]]:
        """Return module consistency records."""
        try:
            from governance_rollup.rollup_query import GovernanceRollupQuery
            query = GovernanceRollupQuery()
            return query.module_consistency()
        except Exception as exc:
            return []
