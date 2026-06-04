"""reports/report_pack_consolidation_report.py — ReportPackConsolidationReport v0.5.4.

Generates an 8-section Markdown report summarising the Report Pack.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReportPackConsolidationReport:
    """8-section Markdown report for Report Pack Consolidation.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.5.4"

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        report_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        mode: str = "real",
    ) -> None:
        self.report_dir = report_dir or os.path.join(BASE_DIR, "reports")
        self.output_dir = output_dir or os.path.join(
            BASE_DIR, "data", "backtest_results", "report_pack"
        )
        self.mode = mode

    def generate(
        self,
        pack_type: str = "daily",
        mode: Optional[str] = None,
    ) -> str:
        """Generate the consolidation report. Returns the path to the written file."""
        mode = mode or self.mode
        today = datetime.now().strftime("%Y-%m-%d")

        logger.info(
            "ReportPackConsolidationReport.generate [pack=%s mode=%s date=%s]",
            pack_type, mode, today,
        )

        # Gather data
        pack_summary   = self._load_pack_summary()
        pack_items     = self._load_pack_items(pack_type)
        health_data    = self._load_health()
        registry_info  = self._load_registry(pack_type)

        lines = []
        lines += self._section_header(pack_type, mode, today)
        lines += self._section_pack_overview(pack_summary, pack_type)
        lines += self._section_report_items(pack_items)
        lines += self._section_health(health_data)
        lines += self._section_registry(registry_info, pack_type)
        lines += self._section_link_index()
        lines += self._section_store_paths()
        lines += self._section_footer(today)

        content = "\n".join(lines) + "\n"
        path = self._write(content, today)
        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self, pack_type: str, mode: str, today: str):
        return [
            f"# TW Quant Cockpit — Report Pack Consolidation Report",
            f"",
            f"> **{self.VERSION}** | Date: {today} | Pack: {pack_type.upper()} | Mode: {mode.upper()}",
            f">",
            f"> [!] Research Only. No Real Orders. Production Trading: BLOCKED.",
            f"",
            f"---",
            f"",
        ]

    def _section_pack_overview(self, summary: dict, pack_type: str):
        lines = [
            f"## 一、Pack Overview",
            f"",
            f"| 項目 | 值 |",
            f"|------|---|",
            f"| Pack Type | {summary.get('pack_type', pack_type).upper()} |",
            f"| Report Date | {summary.get('report_date', 'N/A')} |",
            f"| Status | {summary.get('status', 'MISSING')} |",
            f"| Health Score | {summary.get('health_score', '0.0')}% |",
            f"| Ready Count | {summary.get('ready_count', 0)} |",
            f"| Missing Count | {summary.get('missing_count', 0)} |",
            f"| Failed Count | {summary.get('failed_count', 0)} |",
            f"| Generated At | {summary.get('generated_at', 'N/A')} |",
            f"",
        ]
        return lines

    def _section_report_items(self, items: list):
        lines = [
            f"## 二、Report Items",
            f"",
        ]
        if not items:
            lines.append("No report items found. Run `report-pack --pack-type daily` to generate.")
            lines.append("")
            return lines
        lines += [
            f"| Report Type | Status | Size (bytes) |",
            f"|-------------|--------|-------------|",
        ]
        for item in items:
            rt     = item.get("report_type", "")
            status = item.get("status", "")
            size   = item.get("size_bytes", 0)
            lines.append(f"| {rt} | {status} | {size} |")
        lines.append("")
        return lines

    def _section_health(self, health: dict):
        lines = [
            f"## 三、Health Check",
            f"",
            f"| 項目 | 值 |",
            f"|------|---|",
            f"| Health Label | {health.get('health_label', 'UNKNOWN')} |",
            f"| Health Score | {health.get('health_score', 0.0)}% |",
            f"| Critical Missing | {', '.join(health.get('critical_missing', [])) or 'None'} |",
            f"| Recommendation | {health.get('recommendation', 'N/A')} |",
            f"",
        ]
        return lines

    def _section_registry(self, info: dict, pack_type: str):
        lines = [
            f"## 四、Registry Definitions",
            f"",
            f"Pack type **{pack_type.upper()}** includes {info.get('count', 0)} report types:",
            f"",
        ]
        for rt in info.get("report_types", []):
            lines.append(f"- `{rt}`")
        lines.append("")
        return lines

    def _section_link_index(self):
        lines = [
            f"## 五、CLI / GUI Link Index",
            f"",
            f"| Report Type | CLI Commands | GUI Tab |",
            f"|-------------|-------------|---------|",
        ]
        try:
            from report_pack.report_link_registry import ReportLinkRegistry
            reg = ReportLinkRegistry()
            for entry in reg.build_link_index():
                rt   = entry["report_type"]
                cmds = ", ".join(f"`{c}`" for c in entry["cli_commands"])
                tab  = entry["gui_tab"]
                lines.append(f"| {rt} | {cmds} | {tab} |")
        except Exception as exc:
            lines.append(f"| (unavailable) | {exc} | |")
        lines.append("")
        return lines

    def _section_store_paths(self):
        lines = [
            f"## 六、Storage Paths",
            f"",
            f"| Output | Path |",
            f"|--------|------|",
            f"| Pack output root | `data/backtest_results/report_pack/` |",
            f"| Summary CSV | `data/backtest_results/report_pack/report_pack_summary_YYYY-MM-DD.csv` |",
            f"| Items CSV | `data/backtest_results/report_pack/report_pack_items_*.csv` |",
            f"| Health CSV | `data/backtest_results/report_pack/report_pack_health_*.csv` |",
            f"| Consolidation Report | `reports/report_pack_consolidation_report_YYYY-MM-DD.md` |",
            f"",
        ]
        return lines

    def _section_footer(self, today: str):
        return [
            f"## 七、Safety Attestation",
            f"",
            f"| Safety Flag | Value |",
            f"|-------------|-------|",
            f"| read_only | True |",
            f"| no_real_orders | True |",
            f"| production_blocked | True |",
            f"| real_order_ready | False |",
            f"",
            f"---",
            f"",
            f"## 八、Version History",
            f"",
            f"| Version | Date | Notes |",
            f"|---------|------|-------|",
            f"| v0.5.4 | {today} | Report Pack Consolidation — initial release |",
            f"",
            f"---",
            f"",
            f"*TW Quant Cockpit {self.VERSION} — Research Only — Not Investment Advice*",
        ]

    # ------------------------------------------------------------------
    # Data loaders
    # ------------------------------------------------------------------

    def _load_pack_summary(self) -> dict:
        try:
            from report_pack.report_pack_store import ReportPackStore
            store = ReportPackStore()
            return store.load_latest_summary()
        except Exception as exc:
            logger.warning("_load_pack_summary: %s", exc)
            return {}

    def _load_pack_items(self, pack_type: str) -> list:
        try:
            from report_pack.report_pack_store import ReportPackStore
            store = ReportPackStore()
            return store.load_latest_items(pack_type)
        except Exception as exc:
            logger.warning("_load_pack_items: %s", exc)
            return []

    def _load_health(self) -> dict:
        try:
            from report_pack.report_pack_store import ReportPackStore
            store = ReportPackStore()
            return store.load_latest_health()
        except Exception as exc:
            logger.warning("_load_health: %s", exc)
            return {}

    def _load_registry(self, pack_type: str) -> dict:
        try:
            from report_pack.report_registry import ReportRegistry
            reg = ReportRegistry()
            rts = reg.get_report_types(pack_type)
            return {"count": len(rts), "report_types": rts}
        except Exception as exc:
            logger.warning("_load_registry: %s", exc)
            return {"count": 0, "report_types": []}

    def _write(self, content: str, today: str) -> str:
        try:
            os.makedirs(self.report_dir, exist_ok=True)
            path = os.path.join(
                self.report_dir,
                f"report_pack_consolidation_report_{today}.md",
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("ReportPackConsolidationReport → %s", path)
            return path
        except Exception as exc:
            logger.warning("ReportPackConsolidationReport._write() failed: %s", exc)
            return ""
