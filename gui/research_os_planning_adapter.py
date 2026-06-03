"""
gui/research_os_planning_adapter.py — Bridge between GUI and os_planning subsystem (v0.5.0).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchOSPlanningAdapter:
    """Thin adapter between ResearchOSPlanningPanel and os_planning package."""

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    # ------------------------------------------------------------------
    def run_audit(self) -> dict:
        """Run full OS audit and return consolidated dict for the GUI."""
        result: dict = {}

        # Module inventory
        try:
            from os_planning.module_inventory import ResearchOSModuleInventory
            modules               = ResearchOSModuleInventory().build_inventory()
            result["modules"]     = modules
            result["total_modules"] = len(modules)
            result["mature_count"] = sum(1 for m in modules if m.get("maturity") == "STABLE")
            result["beta_count"]   = sum(1 for m in modules if m.get("maturity") == "USABLE")
            result["alpha_count"]  = sum(1 for m in modules if m.get("maturity") not in ("STABLE", "USABLE"))
        except Exception as exc:
            logger.warning("module_inventory failed: %s", exc)
            result["modules"] = []
            result["total_modules"] = 0

        # CLI inventory
        try:
            from os_planning.cli_inventory import CLIInventoryBuilder
            bld                       = CLIInventoryBuilder()
            commands                  = bld.build_inventory()
            result["cli_commands"]    = commands
            result["total_commands"]  = len(commands)
            try:
                issues = bld.detect_naming_inconsistency()
                result["naming_issues"] = issues
            except Exception:
                result["naming_issues"] = []
        except Exception as exc:
            logger.warning("cli_inventory failed: %s", exc)
            result["cli_commands"]   = []
            result["total_commands"] = 0

        # GUI tab inventory
        try:
            from os_planning.gui_tab_inventory import GUITabInventoryBuilder
            bld2                    = GUITabInventoryBuilder()
            tabs                    = bld2.build_inventory()
            result["gui_tabs"]      = tabs
            result["total_tabs"]    = len(tabs)
            groups = {t.get("suggested_group", t.get("group", "")) for t in tabs}
            result["tab_groups"]    = len(groups)
            try:
                result["grouping_suggestions"] = bld2.suggest_tab_groups()
            except Exception:
                result["grouping_suggestions"] = {}
        except Exception as exc:
            logger.warning("gui_tab_inventory failed: %s", exc)
            result["gui_tabs"]   = []
            result["total_tabs"] = 0

        # Regression audit
        try:
            from os_planning.regression_audit import RegressionAudit
            ra                        = RegressionAudit().run()
            covered                   = ra.get("fully_covered", 0)
            total_ra                  = ra.get("total_modules", 1)
            pct                       = round(covered / total_ra * 100) if total_ra else 0
            result["coverage_score"]  = f"{pct}% ({covered}/{total_ra})"
            result["gap_count"]       = ra.get("missing_any", 0)
            result["regression_rows"] = [
                {"module": k, "status": str(v)}
                for k, v in ra.items()
                if k not in ("status", "total_modules", "fully_covered", "missing_any",
                             "read_only", "no_real_orders", "production_blocked")
                and not isinstance(v, list)
            ]
        except Exception as exc:
            logger.warning("regression_audit failed: %s", exc)
            result["regression_rows"] = []
            result["coverage_score"]  = "N/A"
            result["gap_count"]       = 0

        # Safety matrix
        try:
            from os_planning.safety_matrix import ResearchOSSafetyMatrix
            sm_obj               = ResearchOSSafetyMatrix()
            rows                 = sm_obj.build()
            sm_summary           = sm_obj.summary()
            result["safety_rows"] = rows
            safe_count            = sm_summary.get("safe", 0)
            total_sm              = sm_summary.get("total_modules", 1)
            pct_s                 = round(safe_count / total_sm * 100) if total_sm else 0
            violations            = sm_summary.get("blocked_violations", 0)
            result["safety_score"]    = f"{pct_s}% ({safe_count}/{total_sm})"
            result["violation_count"] = violations
        except Exception as exc:
            logger.warning("safety_matrix failed: %s", exc)
            result["safety_rows"]     = []
            result["safety_score"]    = "N/A"
            result["violation_count"] = 0

        # Artifact hygiene
        try:
            from os_planning.artifact_hygiene_audit import ArtifactHygieneAudit
            aa                       = ArtifactHygieneAudit().run()
            covered_p                = aa.get("covered", 0)
            total_p                  = aa.get("total_patterns", 1)
            pct_h                    = round(covered_p / total_p * 100) if total_p else 0
            result["hygiene_score"]    = f"{pct_h}% ({covered_p}/{total_p})"
            result["missing_patterns"] = aa.get("critical_missing", []) + aa.get("high_missing", [])
        except Exception as exc:
            logger.warning("artifact_hygiene_audit failed: %s", exc)

        return result

    # ------------------------------------------------------------------
    def generate_report(self, mode: str = "real") -> str | None:
        """Generate the OS Stabilization report and return path."""
        try:
            data = self.run_audit()
            from reports.research_os_stabilization_report import ResearchOSStabilizationReport
            reporter = ResearchOSStabilizationReport()
            path     = reporter.generate(
                module_inventory={
                    "total_modules": data.get("total_modules", 0),
                    "total_layers":  6,
                    "mature_count":  data.get("mature_count", 0),
                    "beta_count":    data.get("beta_count", 0),
                    "alpha_count":   data.get("alpha_count", 0),
                    "modules":       data.get("modules", []),
                },
                cli_inventory={
                    "total_commands": data.get("total_commands", 0),
                    "categories":     data.get("tab_groups", 0),
                    "naming_issues":  data.get("naming_issues", []),
                },
                gui_inventory={
                    "total_tabs":          data.get("total_tabs", 0),
                    "tab_groups":          data.get("tab_groups", 0),
                    "grouping_suggestions": data.get("grouping_suggestions", []),
                },
                regression_audit={
                    "modules_audited": data.get("total_modules", 0),
                    "coverage_score":  data.get("coverage_score", "N/A"),
                    "gap_count":       data.get("gap_count", 0),
                    "covered_count":   0,
                    "coverage_gaps":   [],
                },
                artifact_audit={
                    "hygiene_score":    data.get("hygiene_score", "N/A"),
                    "patterns_missing": len(data.get("missing_patterns", [])),
                    "patterns_checked": 15,
                    "missing_patterns": data.get("missing_patterns", []),
                },
                safety_matrix={
                    "safety_score":    data.get("safety_score", "N/A"),
                    "modules_checked": data.get("total_modules", 0),
                    "violation_count": data.get("violation_count", 0),
                },
                mode=mode,
            )
            return path
        except Exception as exc:
            logger.error("generate_report failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    def load_latest_summary(self) -> dict:
        """Load lightweight OS summary (no full re-run)."""
        try:
            from os_planning.module_inventory import ResearchOSModuleInventory
            modules = ResearchOSModuleInventory().build_inventory()
            return {
                "total_modules":  len(modules),
                "total_commands": 106,
                "total_tabs":     31,
                "coverage_score": "N/A",
                "safety_score":   "N/A",
            }
        except Exception as exc:
            logger.warning("load_latest_summary failed: %s", exc)
            return {}
