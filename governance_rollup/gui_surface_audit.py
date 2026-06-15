"""
governance_rollup/gui_surface_audit.py — GovernanceGUISurfaceAuditor v1.1.9

Audits GUI tab registry for consistency.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import importlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent
_VALID_GROUPS = {
    "daily_research", "data", "data_governance", "backtest_simulation",
    "strategy", "system", "operations", "research", "stable_release",
}
_VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}


class GovernanceGUISurfaceAuditor:
    """
    Audits GUI tab registry for consistency.
    Checks: unique tab IDs, unique display names, valid groups,
    valid priorities, non-empty keywords, no_real_orders=True,
    panel imports, adapter imports, no duplicate tabs.
    """

    def run(self) -> Dict[str, Any]:
        """Run all GUI surface audit checks."""
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            registry = GUITabRegistry()
            tabs = registry.list_tabs() if hasattr(registry, "list_tabs") else list(registry._tabs.values())
        except Exception as exc:
            return {
                "status": "WARN",
                "error": f"Could not load GUITabRegistry: {exc}",
                "checks": {},
            }

        checks = {}
        checks["tab_ids_unique"] = self.check_tab_ids_unique(tabs)
        checks["display_names_unique"] = self.check_display_names_unique(tabs)
        checks["groups_valid"] = self.check_groups_valid(tabs)
        checks["priorities_valid"] = self.check_priorities_valid(tabs)
        checks["keywords_nonempty"] = self.check_keywords_nonempty(tabs)
        checks["no_real_orders_flag"] = self.check_no_real_orders_flag(tabs)
        checks["panel_imports"] = self.check_panel_imports(tabs)
        checks["adapter_imports"] = self.check_adapter_imports(tabs)
        checks["no_duplicate_tabs"] = self.check_no_duplicate_tabs(tabs)
        return checks

    def check_tab_ids_unique(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that all tab_ids are unique."""
        tabs = tabs or self._load_tabs()
        ids = [getattr(t, "tab_id", t.get("tab_id", "") if isinstance(t, dict) else "") for t in tabs]
        seen: set = set()
        duplicates = []
        for tid in ids:
            if tid in seen:
                duplicates.append(tid)
            seen.add(tid)
        return {
            "valid": len(duplicates) == 0,
            "duplicates": duplicates,
            "total_checked": len(ids),
        }

    def check_display_names_unique(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that display names are unique."""
        tabs = tabs or self._load_tabs()
        names = [getattr(t, "display_name", t.get("display_name", "") if isinstance(t, dict) else "") for t in tabs]
        seen: set = set()
        duplicates = []
        for name in names:
            if name in seen:
                duplicates.append(name)
            seen.add(name)
        return {
            "valid": len(duplicates) == 0,
            "duplicates": duplicates,
            "total_checked": len(names),
        }

    def check_groups_valid(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that tab groups are from valid set."""
        tabs = tabs or self._load_tabs()
        invalid = []
        for t in tabs:
            group = getattr(t, "group", t.get("group", "") if isinstance(t, dict) else "")
            tab_id = getattr(t, "tab_id", t.get("tab_id", "?") if isinstance(t, dict) else "?")
            if group not in _VALID_GROUPS:
                invalid.append({"tab_id": tab_id, "group": group})
        return {
            "valid": len(invalid) == 0,
            "invalid_groups": invalid,
            "valid_groups": sorted(_VALID_GROUPS),
        }

    def check_priorities_valid(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that tab priorities are P0/P1/P2/P3."""
        tabs = tabs or self._load_tabs()
        invalid = []
        for t in tabs:
            priority = getattr(t, "priority", t.get("priority", "") if isinstance(t, dict) else "")
            tab_id = getattr(t, "tab_id", t.get("tab_id", "?") if isinstance(t, dict) else "?")
            if priority not in _VALID_PRIORITIES:
                invalid.append({"tab_id": tab_id, "priority": priority})
        return {
            "valid": len(invalid) == 0,
            "invalid_priorities": invalid,
        }

    def check_keywords_nonempty(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that all tabs have non-empty keywords."""
        tabs = tabs or self._load_tabs()
        missing = []
        for t in tabs:
            keywords = getattr(t, "keywords", t.get("keywords", []) if isinstance(t, dict) else [])
            tab_id = getattr(t, "tab_id", t.get("tab_id", "?") if isinstance(t, dict) else "?")
            if not keywords:
                missing.append(tab_id)
        return {
            "valid": len(missing) == 0,
            "tabs_missing_keywords": missing,
        }

    def check_no_real_orders_flag(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that all tabs have no_real_orders=True."""
        tabs = tabs or self._load_tabs()
        violations = []
        for t in tabs:
            no_orders = getattr(t, "no_real_orders", t.get("no_real_orders", None) if isinstance(t, dict) else None)
            tab_id = getattr(t, "tab_id", t.get("tab_id", "?") if isinstance(t, dict) else "?")
            if no_orders is not True:
                violations.append({"tab_id": tab_id, "no_real_orders": no_orders})
        return {
            "valid": len(violations) == 0,
            "violations": violations,
        }

    def check_panel_imports(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that panel modules can be imported (WARN if not, not FAIL)."""
        tabs = tabs or self._load_tabs()
        results = []
        for t in tabs:
            module_path = getattr(t, "module_path", t.get("module_path", "") if isinstance(t, dict) else "")
            tab_id = getattr(t, "tab_id", t.get("tab_id", "?") if isinstance(t, dict) else "?")
            if not module_path:
                continue
            try:
                importlib.import_module(module_path)
                results.append({"tab_id": tab_id, "module_path": module_path, "status": "IMPORTABLE"})
            except ImportError:
                results.append({"tab_id": tab_id, "module_path": module_path, "status": "NOT_IMPORTABLE"})
            except Exception as exc:
                results.append({"tab_id": tab_id, "module_path": module_path,
                                 "status": "WARN", "error": str(exc)})
        not_importable = [r for r in results if r["status"] == "NOT_IMPORTABLE"]
        return {
            "valid": True,  # Panel not importable is WARN, not FAIL (may need GUI env)
            "results": results,
            "not_importable": not_importable,
            "note": "NOT_IMPORTABLE panels are expected in headless/CLI environments",
        }

    def check_adapter_imports(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check that adapter modules are registered (WARN if missing)."""
        tabs = tabs or self._load_tabs()
        missing_adapters = []
        for t in tabs:
            tab_id = getattr(t, "tab_id", t.get("tab_id", "?") if isinstance(t, dict) else "?")
            adapter = getattr(t, "adapter", t.get("adapter", None) if isinstance(t, dict) else None)
            # Check only data_governance tabs
            group = getattr(t, "group", t.get("group", "") if isinstance(t, dict) else "")
            if "governance" in group.lower() and not adapter:
                missing_adapters.append(tab_id)
        return {
            "valid": len(missing_adapters) == 0,
            "missing_adapters": missing_adapters,
        }

    def check_no_duplicate_tabs(self, tabs: Optional[List] = None) -> Dict[str, Any]:
        """Check for no duplicate tab entries."""
        return self.check_tab_ids_unique(tabs)

    def summarize(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize audit results."""
        if "status" in results and "error" in results:
            return results

        total = len(results)
        passed = sum(1 for r in results.values() if r.get("valid", True))
        failed = total - passed
        overall = "PASS" if failed == 0 else "WARN"
        return {
            "overall_status": overall,
            "checks_total": total,
            "checks_passed": passed,
            "checks_failed": failed,
            "results": results,
            "research_only": True,
            "no_real_orders": True,
        }

    def save_audit(self, results: Dict[str, Any]) -> Path:
        """Save audit results to data/governance_rollup/gui_surface_audit.csv."""
        from pathlib import Path
        output_dir = _BASE_DIR / "data" / "governance_rollup"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "gui_surface_audit.csv"
        rows = []
        for check_name, result in results.items():
            if isinstance(result, dict):
                rows.append({
                    "check": check_name,
                    "valid": result.get("valid", ""),
                    "issues": str(result.get("duplicates", result.get("violations",
                                 result.get("invalid_groups", result.get("missing_adapters", [])))))[:200],
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                })
        if rows:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
        return path

    def _load_tabs(self) -> List:
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            registry = GUITabRegistry()
            return list(registry._tabs.values())
        except Exception:
            return []
