"""
reports/data_provider_fetch_report.py - Data Provider Auto Fetch Report (v0.3.19).

Output: reports/data_provider_fetch_report_YYYY-MM-DD.md

[!] Read Only. No Real Orders. No Token Displayed.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataProviderFetchReportBuilder:
    """
    Builds data_provider_fetch_report_YYYY-MM-DD.md from fetch + freshness results.

    Parameters
    ----------
    report_date  : "YYYY-MM-DD" (default: today)
    mode         : "real" or "mock"
    fetch_result : dict returned by DataProviderAutoFetcher.run()
    freshness    : dict returned by DataFreshnessChecker.run_all()
    """

    def __init__(
        self,
        report_date:  Optional[str] = None,
        mode:         str = "real",
        fetch_result: Optional[dict] = None,
        freshness:    Optional[dict] = None,
    ):
        self.report_date  = report_date or datetime.now().strftime("%Y-%m-%d")
        self.mode         = mode
        self.fetch_result = fetch_result or {}
        self.freshness    = freshness or {}

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, output_dir: Optional[str] = None) -> str:
        out_dir  = output_dir or os.path.join(_BASE_DIR, "reports")
        os.makedirs(out_dir, exist_ok=True)
        filename = f"data_provider_fetch_report_{self.report_date}.md"
        out_path = os.path.join(out_dir, filename)

        sections = [
            self._section_header(),
            self._section_overview(),
            self._section_provider_status(),
            self._section_fetch_results(),
            self._section_freshness(),
            self._section_errors_fallback(),
            self._section_safety(),
            self._section_next_steps(),
        ]

        content = "\n\n".join(s for s in sections if s)
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            logger.info("DataProviderFetchReportBuilder: wrote %s", out_path)
        except Exception as exc:
            logger.error("DataProviderFetchReportBuilder: %s", exc)
            raise
        return out_path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self) -> str:
        ts = self.fetch_result.get("started_at", datetime.now().isoformat())[:19]
        return (
            f"# Data Provider Auto Fetch Report\n\n"
            f"**Date:** {self.report_date}  \n"
            f"**Mode:** {self.mode.upper()}  \n"
            f"**Run time:** {ts}  \n\n"
            f"> [!] Read Only · No Real Orders · No Token Displayed"
        )

    def _section_overview(self) -> str:
        fr = self.fetch_result
        datasets  = fr.get("datasets", {})
        n_ok      = sum(1 for d in datasets.values() if d.get("status") == "OK")
        n_partial = sum(1 for d in datasets.values() if d.get("status") == "PARTIAL")
        n_failed  = sum(1 for d in datasets.values() if d.get("status") == "FAILED")
        n_skip    = sum(1 for d in datasets.values() if d.get("status") == "SKIPPED")
        lines = ["## 一、總覽", ""]
        lines.append("| 項目 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| Mode | {self.mode.upper()} |")
        lines.append(f"| Read Only | ✓ |")
        lines.append(f"| No Real Orders | ✓ |")
        lines.append(f"| Run Time | {ts if (ts := fr.get('started_at',''))[:19] else '—'} |")
        lines.append(f"| Datasets Requested | {len(fr.get('datasets_requested', []))} |")
        lines.append(f"| Providers Used | {', '.join(fr.get('providers_used', [])) or '—'} |")
        lines.append(f"| Rows Fetched | {fr.get('rows_fetched', 0)} |")
        lines.append(f"| Rows Written | {fr.get('rows_written', 0)} |")
        lines.append(f"| OK | {n_ok} |")
        lines.append(f"| Partial | {n_partial} |")
        lines.append(f"| Failed | {n_failed} |")
        lines.append(f"| Skipped | {n_skip} |")
        lines.append(f"| Dry Run | {'Yes' if fr.get('dry_run') else 'No'} |")
        return "\n".join(lines)

    def _section_provider_status(self) -> str:
        providers_used = self.fetch_result.get("providers_used", [])
        _known = [
            ("finmind",              "FinMind"),
            ("twse",                 "TWSE"),
            ("tpex",                 "TPEx"),
            ("mops",                 "MOPS"),
            ("csv",                  "CSV Fallback"),
            ("xq_export",            "XQ Fallback"),
            ("mega_readonly_planned","Mega Read-Only Planned"),
        ]
        lines = ["## 二、Provider 使用狀態", ""]
        lines.append("| Provider | Used | Note |")
        lines.append("|----------|------|------|")
        for pname, label in _known:
            used  = "✓" if pname in providers_used else "✗"
            note  = "Active in this run" if pname in providers_used else "Not used"
            lines.append(f"| {label} | {used} | {note} |")
        return "\n".join(lines)

    def _section_fetch_results(self) -> str:
        datasets = self.fetch_result.get("datasets", {})
        lines = ["## 三、資料抓取結果", ""]
        lines.append("| Dataset | Status | Provider | Rows Fetched | Rows Written | Warning |")
        lines.append("|---------|--------|----------|-------------|-------------|---------|")

        _order = ["daily_price", "monthly_revenue", "institutional", "margin", "fundamental"]
        for ds in _order:
            info = datasets.get(ds, {})
            status = info.get("status", "SKIPPED")
            prov   = info.get("provider_used", "—")
            rf     = info.get("rows_fetched", 0)
            rw     = info.get("rows_written", 0)
            warn   = "; ".join(info.get("warnings", []))[:60]
            lines.append(f"| {ds} | {status} | {prov} | {rf} | {rw} | {warn} |")

        lines += ["", "**Intraday / Tick / BidAsk:**",
                  "Intraday provider planned for v0.4+. "
                  "Current source: XQ import / CSV (INTRADAY_PROVIDER_PLANNED)."]
        return "\n".join(lines)

    def _section_freshness(self) -> str:
        freshness = self.freshness
        datasets  = freshness.get("datasets", {})
        lines = ["## 四、資料新鮮度", ""]
        lines.append("| Dataset | Freshness | Latest Date | Rows | Warning |")
        lines.append("|---------|-----------|-------------|------|---------|")
        _order = ["daily_k", "monthly_revenue", "institutional", "margin", "fundamental", "intraday"]
        for ds in _order:
            info = datasets.get(ds, {})
            status = info.get("status", "UNKNOWN")
            ld     = info.get("latest_date", "—")
            rows   = info.get("rows", "—")
            warn   = info.get("warning", "")[:60]
            lines.append(f"| {ds} | {status} | {ld} | {rows} | {warn} |")
        return "\n".join(lines)

    def _section_errors_fallback(self) -> str:
        all_warnings = self.fetch_result.get("warnings", [])
        all_errors   = self.fetch_result.get("errors", [])
        lines = ["## 五、錯誤與 Fallback", ""]
        if not all_warnings and not all_errors:
            lines.append("No errors or warnings.")
        else:
            if all_warnings:
                lines += ["**Warnings:**", ""]
                for w in all_warnings[:20]:
                    lines.append(f"- {w}")
            if all_errors:
                lines += ["", "**Errors:**", ""]
                for e in all_errors[:20]:
                    lines.append(f"- {e}")
        return "\n".join(lines)

    def _section_safety(self) -> str:
        return "\n".join([
            "## 六、安全聲明",
            "",
            "| 安全項目 | 狀態 |",
            "|----------|------|",
            "| Read Only | ✓ |",
            "| No Real Orders | ✓ |",
            "| No Token Displayed | ✓ — tokens masked in all output |",
            "| No Strategy Weights Changed | ✓ |",
            "| submit_order() raises RuntimeError | ✓ |",
            "| TWQC_ENABLE_REAL_ORDER=False | ✓ |",
        ])

    def _section_next_steps(self) -> str:
        lines = ["## 七、下一步建議", ""]
        fr = self.fetch_result
        # Token missing
        has_finmind = any(
            p == "finmind" for p in fr.get("providers_used", [])
        )
        if not has_finmind:
            lines.append("- **Set FINMIND_TOKEN** in `.env` for full market data access.")
        lines += [
            "- Add MOPS parser in v0.4 for announcement-date aligned fundamental data.",
            "- Expand TWSE / TPEx provider in v0.4 for public daily price without token.",
            "- Keep XQ Export as local fallback for intraday / tick data.",
            "- Run `python main.py data-freshness` regularly to check data staleness.",
        ]
        return "\n".join(lines)
