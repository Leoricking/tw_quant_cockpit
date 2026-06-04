"""reports/stable_release_v060_report.py — StableReleaseV060Report.

Generates a 9-section Markdown report for Research OS Stable Release v0.6.0.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_REPORT_DIR = os.path.join(BASE_DIR, "reports")


class StableReleaseV060Report:
    """Generates the v0.6.0 Research OS Stable Release Markdown report.

    Console output:
        Research OS Stable Release v0.6.0 | Research Only | No Real Orders | Production BLOCKED

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.6.0"

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def run(self, mode: str = "real") -> dict:
        """Generate and save the stable release report.

        Returns dict with report_path, status, no_real_orders, production_blocked.
        """
        print("=" * 60)
        print("  Research OS Stable Release v0.6.0 | Research Only | No Real Orders | Production BLOCKED")
        print("=" * 60)

        capability_summary = self._load_capability_summary()
        checklist_result   = self._load_checklist_result(mode)
        limitations        = self._load_limitations()

        content = self._build_report(
            mode=mode,
            capability_summary=capability_summary,
            checklist_result=checklist_result,
            limitations=limitations,
        )

        report_path = self._save_report(content)
        status = "PASS" if not checklist_result.get("fail_count", 0) else "WARNING"

        print(f"  Report saved: {report_path}")
        print(f"  Status      : {status}")
        print("=" * 60)

        return {
            "report_path":      report_path,
            "status":           status,
            "no_real_orders":   True,
            "production_blocked": True,
            "version":          self.VERSION,
            "mode":             mode,
        }

    # ------------------------------------------------------------------
    # Data loaders
    # ------------------------------------------------------------------

    def _load_capability_summary(self) -> dict:
        try:
            from stable_release.capability_matrix import StableCapabilityMatrix
            matrix = StableCapabilityMatrix()
            matrix.build()
            caps = matrix.list_capabilities()
            by_status: dict[str, int] = {}
            by_category: dict[str, int] = {}
            for c in caps:
                by_status[c.status] = by_status.get(c.status, 0) + 1
                by_category[c.category] = by_category.get(c.category, 0) + 1
            return {
                "total":              len(caps),
                "stable_count":       by_status.get("STABLE", 0),
                "usable_count":       by_status.get("USABLE", 0),
                "partial_count":      by_status.get("PARTIAL", 0),
                "experimental_count": by_status.get("EXPERIMENTAL", 0),
                "blocked_count":      by_status.get("BLOCKED", 0),
                "by_category":        by_category,
                "capabilities":       [c.to_dict() for c in caps],
            }
        except Exception as exc:
            logger.warning("[StableReleaseV060Report] capability load error: %s", exc)
            return {}

    def _load_checklist_result(self, mode: str) -> dict:
        try:
            from stable_release.stable_release_checklist_v060 import StableReleaseChecklistV060
            return StableReleaseChecklistV060().run(mode=mode)
        except Exception as exc:
            logger.warning("[StableReleaseV060Report] checklist error: %s", exc)
            return {}

    def _load_limitations(self) -> List[dict]:
        try:
            from stable_release.known_limitations import _LIMITATIONS
            return list(_LIMITATIONS)
        except Exception as exc:
            logger.warning("[StableReleaseV060Report] limitations error: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Build report
    # ------------------------------------------------------------------

    def _build_report(
        self,
        mode: str,
        capability_summary: dict,
        checklist_result: dict,
        limitations: List[dict],
    ) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        now   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines: List[str] = []
        lines += self._section_header(today, mode, now)
        lines += self._section_release_overview(capability_summary)
        lines += self._section_capability_matrix(capability_summary)
        lines += self._section_checklist(checklist_result)
        lines += self._section_coverage(capability_summary)
        lines += self._section_safety()
        lines += self._section_limitations(limitations)
        lines += self._section_v05x_completion()
        lines += self._section_roadmap()
        lines += self._section_safety_declaration()
        return "\n".join(lines) + "\n"

    def _section_header(self, today: str, mode: str, now: str) -> List[str]:
        return [
            f"# TW Quant Cockpit — Research OS Stable Release v0.6.0",
            "",
            f"> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**",
            f"> **Report Date:** {today} | **Mode:** {mode.upper()} | **Generated:** {now}",
            "",
            "---",
            "",
        ]

    def _section_release_overview(self, caps: dict) -> List[str]:
        total = caps.get("total", "N/A")
        stable = caps.get("stable_count", "N/A")
        usable = caps.get("usable_count", "N/A")
        lines = [
            "## 1. Release Overview",
            "",
            "| Field | Value |",
            "|-------|-------|",
            "| Version | v0.6.0 |",
            "| Release Name | Research OS Stable Release |",
            "| Previous Version | v0.5.6.2 |",
            "| Release Type | Stable Consolidation |",
            f"| Total Capabilities | {total} |",
            f"| STABLE Capabilities | {stable} |",
            f"| USABLE Capabilities | {usable} |",
            "| Safety Status | Research Only / No Real Orders / Production BLOCKED |",
            "| Real Order Ready | False |",
            "",
            "This release consolidates v0.5.x modules into a stable research OS. "
            "No new trading features. All outputs are research-only.",
            "",
        ]
        return lines

    def _section_capability_matrix(self, caps: dict) -> List[str]:
        capabilities = caps.get("capabilities", [])
        lines = [
            "## 2. Capability Matrix",
            "",
            "| Capability | Category | Status | CLI | GUI | Reports | Regression | Safety |",
            "|------------|----------|--------|-----|-----|---------|------------|--------|",
        ]
        for c in capabilities:
            cli = "Yes" if c.get("cli_commands") else "No"
            gui = "Yes" if c.get("gui_tabs") else "No"
            rpt = "Yes" if c.get("reports") else "No"
            reg = "Yes" if c.get("regression_coverage") else "No"
            safety = c.get("safety_status", "OK")
            lines.append(
                f"| {c['name']} | {c['category']} | {c['status']} "
                f"| {cli} | {gui} | {rpt} | {reg} | {safety} |"
            )
        lines.append("")
        return lines

    def _section_checklist(self, checklist: dict) -> List[str]:
        checks = checklist.get("checks", [])
        overall = checklist.get("overall_status", "UNKNOWN")
        lines = [
            "## 3. Stable Release Checklist",
            "",
            f"**Overall Status: {overall}**",
            "",
            f"| Check | Category | Status | Detail |",
            f"|-------|----------|--------|--------|",
        ]
        for c in checks:
            detail = (c.get("detail", "") or "")[:60].replace("|", "/")
            lines.append(
                f"| {c['name']} | {c['category']} | {c['status']} | {detail} |"
            )
        lines += [
            "",
            f"- Total: {checklist.get('total_checks', 0)}",
            f"- Passed: {checklist.get('pass_count', 0)}",
            f"- Warnings: {checklist.get('warning_count', 0)}",
            f"- Failed: {checklist.get('fail_count', 0)}",
            "",
        ]
        return lines

    def _section_coverage(self, caps: dict) -> List[str]:
        by_cat = caps.get("by_category", {})
        lines = [
            "## 4. CLI / GUI / Report Coverage",
            "",
            "| Category | Capabilities |",
            "|----------|-------------|",
        ]
        for cat, count in sorted(by_cat.items()):
            lines.append(f"| {cat} | {count} |")
        lines.append("")
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## 5. Safety Matrix",
            "",
            "| Safety Check | Status |",
            "|--------------|--------|",
            "| No Real Orders | BLOCKED |",
            "| Production Trading | BLOCKED |",
            "| Broker API | NOT CONNECTED |",
            "| Auto Weight Apply | DISABLED |",
            "| Shioaji Integration | DISABLED |",
            "| Real Order Ready | False |",
            "| Research Only | True |",
            "",
        ]

    def _section_limitations(self, limitations: List[dict]) -> List[str]:
        lines = [
            "## 6. Known Limitations",
            "",
            "| ID | Name | Impact | Workaround |",
            "|----|------|--------|------------|",
        ]
        for lim in limitations:
            wk = (lim.get("workaround", "") or "")[:60].replace("|", "/")
            lines.append(
                f"| {lim['id']} | {lim['name']} | {lim['impact']} | {wk} |"
            )
        lines.append("")
        return lines

    def _section_v05x_completion(self) -> List[str]:
        return [
            "## 7. v0.5.x Completion Summary",
            "",
            "| Version | Feature | Status |",
            "|---------|---------|--------|",
            "| v0.5.0 | Research OS Planning / Stabilization | Done |",
            "| v0.5.1 | CLI Alias / Command UX Polish | Done |",
            "| v0.5.1.1 | Strategy Filter Pack — Financial Turnaround | Done |",
            "| v0.5.2 | GUI Tab Grouping / Navigation Polish | Done |",
            "| v0.5.2.1 | Strategy Filter GUI Navigation Integration | Done |",
            "| v0.5.3 | Regression Suite Consolidation | Done |",
            "| v0.5.4 | Report Pack Consolidation | Done |",
            "| v0.5.5 | Data / Feature Store Stabilization | Done |",
            "| v0.5.6 | TW Replay Training Cockpit — AI Review & Tape Reading | Done |",
            "| v0.5.6.2 | Stabilize Data and Feature Store Health | Done |",
            "",
        ]

    def _section_roadmap(self) -> List[str]:
        return [
            "## 8. Next Roadmap",
            "",
            "| Version | Feature | Priority |",
            "|---------|---------|---------|",
            "| v0.6.1 | Stable UX Polish — empty states, error messages, tab icons | P1 |",
            "| v0.6.2 | Data Coverage Expansion — more symbols, sectors, timeframes | P1 |",
            "| v0.6.3 | Replay Training UI Enhancement — chart rendering, drill UI | P1 |",
            "| v0.7.0 | Research Intelligence Upgrade — smarter AI review, pattern library | P2 |",
            "",
        ]

    def _section_safety_declaration(self) -> List[str]:
        return [
            "## 9. Safety Declaration",
            "",
            "> **[!] Research Only / No Real Orders / Production Trading BLOCKED**",
            ">",
            "> This system is a research and simulation platform only.",
            "> - No real broker API connections",
            "> - No automatic order placement",
            "> - No auto-apply of strategy weights",
            "> - All backtests are historical simulations",
            "> - Not investment advice",
            "> - production_blocked=True | real_order_ready=False",
            "",
            "---",
            "",
            f"*Generated by TW Quant Cockpit v0.6.0 — Research Only / No Real Orders / Production Trading BLOCKED*",
            "",
        ]

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def _save_report(self, content: str) -> str:
        try:
            os.makedirs(_REPORT_DIR, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            path  = os.path.join(_REPORT_DIR, f"stable_release_v0.6.0_report_{today}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("[StableReleaseV060Report] saved → %s", path)
            return path
        except Exception as exc:
            logger.error("[StableReleaseV060Report] save error: %s", exc)
            return ""
