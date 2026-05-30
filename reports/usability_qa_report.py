"""
reports/usability_qa_report.py - Usability QA Markdown report builder (v0.3.22).

Produces a 7-section Markdown report:
  1. 總覽 (Overview)
  2. CLI UX Test Results
  3. GUI Panel Import Results
  4. Error Message Coverage
  5. Empty State Coverage
  6. 安全訊息 (Safety Message Coverage)
  7. 待改善項目 (Improvement Recommendations)

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class UsabilityQAReportBuilder:
    """
    Builds a Markdown usability QA report from a smoke test result dict.

    Parameters
    ----------
    smoke_result : dict returned by UsabilitySmokeTest.run()
    report_dir   : Output directory (defaults to reports/)
    """

    VERSION            = "v0.3.22"
    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        smoke_result: Optional[dict] = None,
        report_dir: Optional[str] = None,
    ):
        self._result     = smoke_result or {}
        self._base_dir   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._report_dir = report_dir or os.path.join(self._base_dir, "reports")

    def build(self, output_dir: Optional[str] = None) -> str:
        """Build and write the Markdown report. Returns the output file path."""
        out_dir = output_dir or self._report_dir
        os.makedirs(out_dir, exist_ok=True)

        today     = date.today().strftime("%Y-%m-%d")
        filename  = f"usability_smoke_test_report_{today}.md"
        out_path  = os.path.join(out_dir, filename)

        md = self._render()
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)

        logger.info("[UsabilityQAReportBuilder] Report written: %s", out_path)
        return out_path

    def render(self) -> str:
        """Return the rendered Markdown string without writing to disk."""
        return self._render()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self) -> str:
        r      = self._result
        today  = date.today().strftime("%Y-%m-%d")
        run_at = r.get("run_at", today)
        ver    = r.get("version", self.VERSION)

        cases       = r.get("cases", [])
        cli_cases   = [c for c in cases if c.get("category") == "CLI"]
        gui_cases   = [c for c in cases if c.get("category") == "GUI"]

        n_pass = r.get("passed",   0)
        n_fail = r.get("failed",   0)
        n_warn = r.get("warnings", 0)
        n_skip = r.get("skipped",  0)
        n_safe = r.get("safety_banner_coverage", 0)
        overall = r.get("overall_status", "UNKNOWN")

        lines: List[str] = []

        # ----------------------------------------------------------------
        # Header
        # ----------------------------------------------------------------
        lines += [
            f"# Usability QA Report — {today}",
            "",
            f"> **Version:** {ver}  |  **Run at:** {run_at}",
            ">",
            "> **[!] Research Only. Read Only. No Real Orders.**",
            "> **[!] Production Trading: BLOCKED.**",
            "",
        ]

        # ----------------------------------------------------------------
        # Section 1: 總覽
        # ----------------------------------------------------------------
        lines += [
            "## 1. 總覽 (Overview)",
            "",
            f"| Item | Value |",
            f"|------|-------|",
            f"| Overall Status | **{overall}** |",
            f"| Tests Passed | {n_pass} |",
            f"| Tests Failed | {n_fail} |",
            f"| Warnings | {n_warn} |",
            f"| Skipped | {n_skip} |",
            f"| Safety Banner Coverage | {n_safe} CLI tests |",
            "",
        ]

        # ----------------------------------------------------------------
        # Section 2: CLI UX
        # ----------------------------------------------------------------
        lines += ["## 2. CLI UX Test Results", ""]
        if cli_cases:
            lines += [
                "| Test | Status | Duration | Can Ignore | Safety Banner | Note |",
                "|------|--------|----------|-----------|---------------|------|",
            ]
            for c in cli_cases:
                dur = f"{c.get('duration_seconds', 0):.1f}s"
                ci  = "Yes" if c.get("can_ignore") else "No"
                sb  = "Yes" if c.get("safety_banner_present") else "No"
                msg = c.get("message", "")[:80]
                lines.append(
                    f"| {c['name']} | {c['status']} | {dur} | {ci} | {sb} | {msg} |"
                )
        else:
            lines.append("_No CLI tests were run._")
        lines.append("")

        # Failed / warning detail
        for c in cli_cases:
            if c.get("status") in ("FAIL", "WARNING") and c.get("detail"):
                lines += [
                    f"### Detail: `{c['name']}`",
                    "",
                    "```",
                    c["detail"][-400:],
                    "```",
                    "",
                ]

        # ----------------------------------------------------------------
        # Section 3: GUI UX
        # ----------------------------------------------------------------
        lines += ["## 3. GUI Panel Import Results", ""]
        if gui_cases:
            lines += [
                "| Test | Status | Duration | Can Ignore | Note |",
                "|------|--------|----------|-----------|------|",
            ]
            for c in gui_cases:
                dur = f"{c.get('duration_seconds', 0):.2f}s"
                ci  = "Yes" if c.get("can_ignore") else "No"
                msg = c.get("message", "")[:80]
                lines.append(
                    f"| {c['name']} | {c['status']} | {dur} | {ci} | {msg} |"
                )
        else:
            lines.append("_No GUI tests were run._")
        lines.append("")

        # ----------------------------------------------------------------
        # Section 4: Error Message Coverage
        # ----------------------------------------------------------------
        lines += [
            "## 4. Error Message Coverage",
            "",
            "The following error types are handled by `utils/user_facing_errors.py`:",
            "",
            "| Error Type | Handler | Output Fields |",
            "|------------|---------|---------------|",
            "| FileNotFoundError | `_file_not_found` | title, plain_message, likely_cause, next_steps |",
            "| PermissionError | `_permission_error` | title, plain_message, next_steps |",
            "| UnicodeDecodeError | `_unicode_error` | title, plain_message, next_steps |",
            "| pandas ParserError | `_pandas_parser_error` | title, plain_message, next_steps |",
            "| Network Timeout | `_network_timeout` | title, plain_message, can_ignore=True |",
            "| Network Unavailable | `_network_unavailable` | title, plain_message, can_ignore=True |",
            "| Token Not Configured | `_token_not_configured` | title, plain_message, can_ignore=True |",
            "| Data Missing | `_data_missing` | title, plain_message, next_steps |",
            "| Stale Data | `_stale_data` | title, plain_message, next_steps |",
            "| Provider Unsupported | `_provider_unsupported` | title, can_ignore=True |",
            "| GUI Import Error | `_gui_import_error` | title, can_ignore=True |",
            "| ImportError | `_import_error` | title, plain_message, next_steps |",
            "| Generic | `_generic` | title, technical_detail |",
            "",
        ]

        # ----------------------------------------------------------------
        # Section 5: Empty State Coverage
        # ----------------------------------------------------------------
        lines += [
            "## 5. Empty State Coverage",
            "",
            "`EmptyStateWidget` (gui/portfolio_widgets.py) is shown when:",
            "",
            "- Portfolio simulation results are not yet available",
            "- A data table has no rows to display",
            "- A panel's data source is not configured",
            "",
            "The widget always includes:",
            "- A descriptive title",
            "- A plain-language message",
            "- Next steps (actionable instructions)",
            "- Safety reminder (simulation only, no real orders)",
            "",
        ]

        # ----------------------------------------------------------------
        # Section 6: 安全訊息
        # ----------------------------------------------------------------
        cli_with_banner = [c for c in cli_cases if c.get("safety_banner_present")]
        cli_without_banner = [
            c for c in cli_cases
            if not c.get("safety_banner_present") and c.get("status") == "PASS"
        ]

        lines += [
            "## 6. 安全訊息覆蓋率 (Safety Message Coverage)",
            "",
            f"CLI tests with safety banner: **{len(cli_with_banner)}** / {len(cli_cases)}",
            "",
        ]
        if cli_without_banner:
            lines += [
                "Commands without detected safety banner (PASS tests only):",
                "",
            ]
            for c in cli_without_banner:
                lines.append(f"- `{c['name']}`")
            lines.append("")

        # ----------------------------------------------------------------
        # Section 7: 待改善項目
        # ----------------------------------------------------------------
        improvements: List[str] = []
        failed = [c for c in cases if c.get("status") == "FAIL"]
        for c in failed:
            improvements.append(f"Fix failing test: `{c['name']}` — {c.get('message','')}")
        if cli_without_banner:
            improvements.append(
                f"{len(cli_without_banner)} CLI command(s) do not print a safety banner"
            )

        lines += ["## 7. 待改善項目 (Improvement Recommendations)", ""]
        if improvements:
            for item in improvements:
                lines.append(f"- {item}")
        else:
            lines.append("_No improvement items identified at this time._")
        lines.append("")

        # ----------------------------------------------------------------
        # Footer
        # ----------------------------------------------------------------
        lines += [
            "---",
            "",
            f"*Generated by `UsabilityQAReportBuilder` {ver} on {today}.*",
            "",
            "**[!] Read Only. No Real Orders. Production Trading: BLOCKED.**",
            "",
        ]

        return "\n".join(lines)
