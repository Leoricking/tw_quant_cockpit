"""
reports/research_os_stabilization_report.py — v0.5.0 Research OS Stabilization Report.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import logging
import os
from datetime import date

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchOSStabilizationReport:
    """Generate v0.5.0 Research OS Stabilization Report."""

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, output_dir: str | None = None):
        self.output_dir = output_dir or os.path.join(BASE_DIR, "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    def generate(
        self,
        module_inventory: dict | None = None,
        cli_inventory: dict | None = None,
        gui_inventory: dict | None = None,
        regression_audit: dict | None = None,
        artifact_audit: dict | None = None,
        safety_matrix: dict | None = None,
        mode: str = "real",
    ) -> str:
        """Generate the report and return the output file path."""
        mi   = module_inventory   or {}
        ci   = cli_inventory      or {}
        gi   = gui_inventory      or {}
        ra   = regression_audit   or {}
        aa   = artifact_audit     or {}
        sm   = safety_matrix      or {}

        today    = date.today().isoformat()
        filename = f"research_os_stabilization_report_{today}.md"
        filepath = os.path.join(self.output_dir, filename)

        lines: list[str] = []
        lines += self._header(today, mode)
        lines += self._section_module_inventory(mi)
        lines += self._section_cli_inventory(ci)
        lines += self._section_gui_inventory(gi)
        lines += self._section_regression_audit(ra)
        lines += self._section_artifact_hygiene(aa)
        lines += self._section_safety_matrix(sm)
        lines += self._section_recommendations(mi, ci, gi, ra, aa, sm)
        lines += self._footer()

        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

        logger.info("ResearchOSStabilizationReport → %s", filepath)
        return filepath

    # ------------------------------------------------------------------
    def _header(self, today: str, mode: str) -> list[str]:
        return [
            "# Research OS Stabilization Report — v0.5.0",
            "",
            f"> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**",
            f"> **[!] REAL_ORDER_READY=False | Mode: {mode}**",
            "",
            f"**Date:** {today}  ",
            "**Version:** v0.5.0 — Research OS Planning / Stabilization  ",
            "",
            "---",
            "",
            "## Overview",
            "",
            "This report provides a comprehensive inventory and audit of the v0.5.0 Research OS:",
            "all modules, CLI commands, GUI tabs, regression coverage, artifact hygiene, and safety flags.",
            "",
        ]

    # ------------------------------------------------------------------
    def _section_module_inventory(self, mi: dict) -> list[str]:
        lines = ["## 1. Module Inventory", ""]
        total   = mi.get("total_modules",    "N/A")
        layers  = mi.get("total_layers",     "N/A")
        mature  = mi.get("mature_count",     "N/A")
        beta    = mi.get("beta_count",       "N/A")
        alpha   = mi.get("alpha_count",      "N/A")
        modules = mi.get("modules",          [])

        lines += [
            f"- **Total Modules:** {total}",
            f"- **Layers:** {layers}",
            f"- **Mature:** {mature} | **Beta:** {beta} | **Alpha:** {alpha}",
            "",
        ]
        if modules:
            lines += [
                "| Module | Package | Category | Maturity | CLI | GUI | Report |",
                "|--------|---------|----------|----------|-----|-----|--------|",
            ]
            for m in modules[:30]:
                cli_flag = "Y" if m.get("cli_commands") else "—"
                gui_flag = "Y" if m.get("gui_tab")      else "—"
                rpt_flag = "Y" if m.get("report")       else "—"
                lines.append(
                    f"| {m.get('module_name','?')} "
                    f"| {m.get('package','?')} "
                    f"| {m.get('category','?')} "
                    f"| {m.get('maturity','?')} "
                    f"| {cli_flag} | {gui_flag} | {rpt_flag} |"
                )
        lines += [""]
        return lines

    # ------------------------------------------------------------------
    def _section_cli_inventory(self, ci: dict) -> list[str]:
        lines = ["## 2. CLI Command Inventory", ""]
        total      = ci.get("total_commands",  "N/A")
        categories = ci.get("categories",      "N/A")
        issues     = ci.get("naming_issues",   [])

        lines += [
            f"- **Total Commands:** {total}",
            f"- **Categories:** {categories}",
            f"- **Naming Issues Detected:** {len(issues) if isinstance(issues, list) else 'N/A'}",
            "",
        ]
        if isinstance(issues, list) and issues:
            lines.append("**Naming Issues:**")
            for issue in issues[:10]:
                lines.append(f"  - {issue}")
            lines.append("")
        lines += [""]
        return lines

    # ------------------------------------------------------------------
    def _section_gui_inventory(self, gi: dict) -> list[str]:
        lines = ["## 3. GUI Tab Inventory", ""]
        total  = gi.get("total_tabs",  "N/A")
        groups = gi.get("tab_groups",  "N/A")

        lines += [
            f"- **Total Tabs:** {total}",
            f"- **Tab Groups:** {groups}",
            "",
        ]
        suggestions = gi.get("grouping_suggestions", {})
        if suggestions:
            lines.append("**Grouping Suggestions:**")
            if isinstance(suggestions, dict):
                for grp, tab_list in list(suggestions.items())[:8]:
                    lines.append(f"  - **{grp}**: {', '.join(tab_list[:4])}")
            elif isinstance(suggestions, list):
                for s in suggestions[:8]:
                    lines.append(f"  - {s}")
            lines.append("")
        lines += [""]
        return lines

    # ------------------------------------------------------------------
    def _section_regression_audit(self, ra: dict) -> list[str]:
        lines = ["## 4. Regression Coverage Audit", ""]
        total     = ra.get("modules_audited",    "N/A")
        covered   = ra.get("covered_count",      "N/A")
        gaps      = ra.get("gap_count",          "N/A")
        score     = ra.get("coverage_score",     "N/A")
        gap_list  = ra.get("coverage_gaps",      [])

        lines += [
            f"- **Modules Audited:** {total}",
            f"- **Covered:** {covered}",
            f"- **Gaps:** {gaps}",
            f"- **Coverage Score:** {score}",
            "",
        ]
        if isinstance(gap_list, list) and gap_list:
            lines.append("**Coverage Gaps:**")
            for g in gap_list[:10]:
                lines.append(f"  - {g}")
            lines.append("")
        lines += [""]
        return lines

    # ------------------------------------------------------------------
    def _section_artifact_hygiene(self, aa: dict) -> list[str]:
        lines = ["## 5. Artifact Hygiene Audit", ""]
        patterns_checked = aa.get("patterns_checked", "N/A")
        patterns_missing = aa.get("patterns_missing", "N/A")
        hygiene_score    = aa.get("hygiene_score",    "N/A")
        missing_list     = aa.get("missing_patterns", [])

        lines += [
            f"- **Patterns Checked:** {patterns_checked}",
            f"- **Patterns Missing:** {patterns_missing}",
            f"- **Hygiene Score:** {hygiene_score}",
            "",
        ]
        if isinstance(missing_list, list) and missing_list:
            lines.append("**Missing .gitignore Patterns:**")
            for p in missing_list:
                lines.append(f"  - `{p}`")
            lines.append("")
        lines += [""]
        return lines

    # ------------------------------------------------------------------
    def _section_safety_matrix(self, sm: dict) -> list[str]:
        lines = ["## 6. Safety Matrix", ""]
        total        = sm.get("modules_checked",   "N/A")
        compliant    = sm.get("compliant_count",   "N/A")
        violations   = sm.get("violation_count",   0)
        safety_score = sm.get("safety_score",      "N/A")
        viol_list    = sm.get("violations",        [])

        lines += [
            f"- **Modules Checked:** {total}",
            f"- **Compliant:** {compliant}",
            f"- **Violations:** {violations}",
            f"- **Safety Score:** {safety_score}",
            "",
        ]
        if violations and isinstance(viol_list, list) and viol_list:
            lines.append("**Violations:**")
            for v in viol_list[:10]:
                lines.append(f"  - {v}")
            lines.append("")
        else:
            lines.append("All checked modules pass safety invariants.")
            lines.append("")
        lines += [""]
        return lines

    # ------------------------------------------------------------------
    def _section_recommendations(
        self, mi: dict, ci: dict, gi: dict,
        ra: dict, aa: dict, sm: dict
    ) -> list[str]:
        lines = ["## 7. Recommendations", ""]
        recs: list[str] = []

        gap_count = ra.get("gap_count", 0)
        if isinstance(gap_count, int) and gap_count > 0:
            recs.append(
                f"Regression: {gap_count} module(s) lack test coverage "
                "— add import + summary tests (v0.5.1+)."
            )

        naming_issues = ci.get("naming_issues", [])
        if isinstance(naming_issues, list) and naming_issues:
            recs.append(
                f"CLI: {len(naming_issues)} naming inconsistencies detected "
                "— standardise prefixes in v0.5.1 CLI Alias Polish."
            )

        missing_pats = aa.get("patterns_missing", 0)
        if isinstance(missing_pats, int) and missing_pats > 0:
            recs.append(
                f"Artifacts: {missing_pats} .gitignore pattern(s) missing "
                "— add during v0.5.4 Report Pack."
            )

        tab_count = gi.get("total_tabs", 0)
        if isinstance(tab_count, int) and tab_count > 20:
            recs.append(
                f"GUI: {tab_count} tabs detected — implement tab grouping in v0.5.2."
            )

        violations = sm.get("violation_count", 0)
        if isinstance(violations, int) and violations > 0:
            recs.append(
                f"Safety: {violations} violation(s) — review immediately before v0.5.x progression."
            )

        if not recs:
            recs.append("No critical issues found. Proceed with v0.5.x roadmap.")

        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. {rec}")
        lines += [""]
        return lines

    # ------------------------------------------------------------------
    def _footer(self) -> list[str]:
        return [
            "---",
            "",
            "## Safety Summary",
            "",
            "| Invariant | Value |",
            "|-----------|-------|",
            "| Read Only | **True** |",
            "| No Real Orders | **True** |",
            "| Production Trading | **BLOCKED** |",
            "| REAL_ORDER_READY | **False (never)** |",
            "",
            "*Generated by ResearchOSStabilizationReport — v0.5.0 Research OS Planning.*",
        ]
