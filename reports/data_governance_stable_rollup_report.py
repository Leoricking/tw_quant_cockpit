"""
reports/data_governance_stable_rollup_report.py — DataGovernanceStableRollupReportBuilder v1.1.9

Builds stable rollup report as markdown.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent


class DataGovernanceStableRollupReportBuilder:
    """
    Builds stable rollup report as markdown.
    Output: reports/data_governance_stable_rollup_report_YYYY-MM-DD.md
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def build(self, summary: Any = None, mode: str = "real") -> str:
        """Build the full report markdown. Returns content string."""
        if summary is None:
            try:
                from governance_rollup.rollup_store import GovernanceRollupStore
                store = GovernanceRollupStore()
                summary = store.load_latest_summary()
            except Exception:
                pass

        sections = []
        sections.append(self._section_safety_declaration())
        sections.append(self._section_executive_summary(summary))
        sections.append(self._section_module_health_matrix(summary))
        sections.append(self._section_cross_module_consistency(summary))
        sections.append(self._section_store_inventory(summary))
        sections.append(self._section_audit_integrity(summary))
        sections.append(self._section_indexes(summary))
        sections.append(self._section_cross_machine_paths(summary))
        sections.append(self._section_migration(summary))
        sections.append(self._section_recovery_plans(summary))
        sections.append(self._section_regression_release_gate(summary))
        sections.append(self._section_known_warnings(summary))
        sections.append(self._section_stable_freeze_decision(summary))

        return "\n\n".join(s for s in sections if s)

    def _section_safety_declaration(self) -> str:
        return """# Safety Declaration

**[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
**[!] VALIDATED does not enable trading. Broker Execution Disabled.**
**[!] Not Investment Advice.**
**[!] Data Governance Stable Rollup v1.1.9 — Audit Report**
"""

    def _section_executive_summary(self, summary: Any) -> str:
        if summary is None:
            return "## Executive Summary\n\n_No rollup summary available._"
        if hasattr(summary, "to_dict"):
            d = summary.to_dict()
        else:
            d = summary if isinstance(summary, dict) else {}

        overall = d.get("overall_status", "UNKNOWN")
        stable_ready = d.get("stable_ready", False)
        generated_at = d.get("generated_at", "")
        blocking = d.get("blocking_issues", [])
        warnings = d.get("known_warnings", [])

        lines = [
            "## Executive Summary",
            "",
            f"- **Version**: {d.get('version', '1.1.9')}",
            f"- **Release**: {d.get('release_name', 'Data Governance Stable Rollup')}",
            f"- **Overall Status**: {overall}",
            f"- **Stable Ready**: {stable_ready}",
            f"- **Generated At**: {generated_at}",
            f"- **Research Only**: True",
            f"- **No Real Orders**: True",
        ]
        if blocking:
            lines.append("")
            lines.append("### Blocking Issues")
            for issue in blocking:
                lines.append(f"- {issue}")
        if warnings:
            lines.append("")
            lines.append("### Known Warnings")
            for w in warnings:
                lines.append(f"- {w}")
        return "\n".join(lines)

    def _section_module_health_matrix(self, summary: Any) -> str:
        d = self._to_dict(summary)
        health = d.get("health_summary", {})
        if not health:
            return "## Module Health Matrix\n\n_Health data not available._"
        matrix = health.get("module_results", health.get("matrix", {}))
        lines = [
            "## Module Health Matrix",
            "",
            "| Module | Status | Available | Checks Passed | Checks Failed |",
            "|--------|--------|-----------|---------------|---------------|",
        ]
        if isinstance(matrix, dict):
            for module_name, result in matrix.items():
                if not isinstance(result, dict):
                    continue
                status = result.get("status", "UNKNOWN")
                avail = result.get("available", "")
                passed = result.get("checks_passed", "")
                failed = result.get("checks_failed", "")
                lines.append(f"| {module_name} | {status} | {avail} | {passed} | {failed} |")
        return "\n".join(lines)

    def _section_cross_module_consistency(self, summary: Any) -> str:
        d = self._to_dict(summary)
        consistency = d.get("consistency_summary", {})
        if not consistency:
            return "## Cross-Module Consistency\n\n_Consistency data not available._"
        lines = [
            "## Cross-Module Consistency",
            "",
            f"- **Modules Checked**: {consistency.get('modules_checked', 0)}",
            f"- **Modules Pass**: {consistency.get('modules_pass', 0)}",
            f"- **Modules Warn**: {consistency.get('modules_warn', 0)}",
            f"- **Modules Fail**: {consistency.get('modules_fail', 0)}",
            f"- **Safety Mismatches**: {consistency.get('safety_mismatches', 0)}",
            f"- **Qualification Mismatches**: {consistency.get('qualification_mismatches', 0)}",
            f"- **Overall Status**: {consistency.get('overall_status', 'UNKNOWN')}",
        ]
        return "\n".join(lines)

    def _section_store_inventory(self, summary: Any) -> str:
        return "## Store Inventory\n\nStore inventory is written to `data/governance_rollup/store_inventory.csv`.\nSee that file for full details."

    def _section_audit_integrity(self, summary: Any) -> str:
        d = self._to_dict(summary)
        safety = d.get("safety_summary", {})
        audits = safety.get("audits", {})
        if not audits:
            return "## Audit Chain Integrity\n\n_Audit data not available._"
        lines = [
            "## Audit Chain Integrity",
            "",
            f"- **Chains Checked**: {audits.get('chains_checked', 0)}",
            f"- **Chains Failed**: {audits.get('chains_failed', 0)}",
            f"- **Status**: {audits.get('status', 'UNKNOWN')}",
        ]
        return "\n".join(lines)

    def _section_indexes(self, summary: Any) -> str:
        return "## Index Status\n\nIndex status is written to `data/governance_rollup/index_status.csv`.\nSee that file for full details."

    def _section_cross_machine_paths(self, summary: Any) -> str:
        return (
            "## Cross-Machine Path Normalization\n\n"
            "- Known repo roots:\n"
            "  - `D:/code/Claude/tw_quant_cockpit` (Computer A)\n"
            "  - `C:/Users/Rossi/Documents/Claude/trading_master` (Computer B)\n"
            "- Artifact registry uses repo-relative paths.\n"
            "- Missing local path does NOT mean artifact is gone.\n"
            "- Stale absolute paths are flagged WARN, not FAIL."
        )

    def _section_migration(self, summary: Any) -> str:
        d = self._to_dict(summary)
        migration = d.get("migration_summary", {})
        return (
            "## Metadata Migration\n\n"
            "Migration plans are preview-only by default (dry_run=True).\n"
            "Pass `--allow-write` to execute migration.\n"
            "Original files are NEVER overwritten — migrated copies use `.migrated_v119` suffix.\n"
            f"Preview count: {len(migration.get('previews', []))}"
        )

    def _section_recovery_plans(self, summary: Any) -> str:
        d = self._to_dict(summary)
        recovery = d.get("recovery_summary", {})
        plans = recovery.get("plans", [])
        return (
            "## Recovery Plans\n\n"
            f"Recovery plans found: {len(plans)}\n\n"
            "All recovery actions require `--allow-write` to execute.\n"
            "Default: dry_run=True (preview only).\n"
            "NEVER modifies original append-only history.\n"
            "Backup is always created before any write."
        )

    def _section_regression_release_gate(self, summary: Any) -> str:
        return (
            "## Regression & Release Gate\n\n"
            "Run `python main.py governance-rollup-run` to verify stable rollup.\n"
            "Run `python main.py governance-rollup-consistency` for consistency check.\n"
            "Run `python main.py governance-rollup-health` for health check.\n"
            "Stable release requires: overall_status=PASS, no blocking_issues, stable_ready=True."
        )

    def _section_known_warnings(self, summary: Any) -> str:
        d = self._to_dict(summary)
        warnings = d.get("known_warnings", [])
        if not warnings:
            return "## Known Warnings\n\n_No known warnings._"
        lines = ["## Known Warnings", ""]
        for w in warnings:
            lines.append(f"- {w}")
        return "\n".join(lines)

    def _section_stable_freeze_decision(self, summary: Any) -> str:
        d = self._to_dict(summary)
        overall = d.get("overall_status", "UNKNOWN")
        stable_ready = d.get("stable_ready", False)
        blocking = d.get("blocking_issues", [])

        decision = "STABLE" if stable_ready and overall == "PASS" else "NOT STABLE"
        lines = [
            "## Stable Freeze Decision",
            "",
            f"**Decision: {decision}**",
            "",
            f"- Overall Status: {overall}",
            f"- Stable Ready: {stable_ready}",
            f"- Blocking Issues: {len(blocking)}",
            "",
            "**Stable freeze criteria:**",
            "1. overall_status = PASS",
            "2. No blocking_issues",
            "3. No safety mismatches",
            "4. No impossible states",
            "5. All P0 modules available",
        ]
        return "\n".join(lines)

    def save(self, content: str) -> Path:
        """Save report to reports/ directory."""
        reports_dir = _BASE_DIR / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        path = reports_dir / f"data_governance_stable_rollup_report_{date_str}.md"
        path.write_text(content, encoding="utf-8")
        logger.info("save: wrote report to %s", path)
        return path

    def _to_dict(self, summary: Any) -> Dict[str, Any]:
        if summary is None:
            return {}
        if hasattr(summary, "to_dict"):
            return summary.to_dict()
        if isinstance(summary, dict):
            return summary
        return {}
