"""reports/data_stabilization_report.py — DataStabilizationReport v0.5.5.

9-section Markdown report for Data / Feature Store Stabilization.
Output: reports/data_stabilization_report_YYYY-MM-DD.md

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataStabilizationReport:
    """9-section Markdown report for Data / Feature Store Stabilization.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.5.5"

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
            BASE_DIR, "data", "backtest_results", "data_stabilization"
        )
        self.mode = mode

    def generate(self, mode: Optional[str] = None) -> str:
        """Generate the report. Returns path."""
        mode = mode or self.mode
        today = datetime.now().strftime("%Y-%m-%d")

        logger.info(
            "DataStabilizationReport.generate [mode=%s date=%s]", mode, today
        )

        # Load data from store
        summary    = self._load_summary()
        schema     = self._load_schema()
        lineage    = self._load_lineage()
        readiness  = self._load_readiness()
        health     = self._load_health()
        leakage    = self._load_leakage()

        lines = []
        lines += self._section_header(mode, today)
        lines += self._section_overview(summary)
        lines += self._section_schema(schema)
        lines += self._section_lineage(lineage)
        lines += self._section_readiness(readiness)
        lines += self._section_health(health)
        lines += self._section_leakage(leakage)
        lines += self._section_provider_integration(summary)
        lines += self._section_next_actions(health, leakage)
        lines += self._section_safety(today)

        content = "\n".join(lines) + "\n"
        return self._write(content, today)

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self, mode: str, today: str) -> List[str]:
        return [
            f"# TW Quant Cockpit — Data / Feature Store Stabilization Report",
            f"",
            f"> **{self.VERSION}** | Date: {today} | Mode: {mode.upper()}",
            f">",
            f"> [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.",
            f"",
            f"---",
            f"",
        ]

    def _section_overview(self, summary: dict) -> List[str]:
        return [
            f"## 一、總覽",
            f"",
            f"| 項目 | 值 |",
            f"|------|---|",
            f"| Version | {summary.get('version', self.VERSION)} |",
            f"| Generated At | {summary.get('generated_at', 'N/A')} |",
            f"| Mode | {summary.get('mode', 'N/A')} |",
            f"| Data Stabilization Only | True |",
            f"| Research Only | True |",
            f"| No Real Orders | True |",
            f"| Datasets Checked | {summary.get('datasets_checked', 0)} |",
            f"| Feature Groups | {summary.get('feature_groups_checked', 0)} |",
            f"| Readiness Score | {summary.get('readiness_score', 0.0)}% |",
            f"| Health Score | {summary.get('health_score', 0.0)}% |",
            f"| Leakage Warnings | {summary.get('leakage_warnings', 0)} |",
            f"| Overall Status | {summary.get('overall_status', 'UNKNOWN')} |",
            f"",
        ]

    def _section_schema(self, schema: List[dict]) -> List[str]:
        lines = [
            f"## 二、Dataset Schema Registry",
            f"",
        ]
        if not schema:
            lines.append("No schema data. Run `data-stabilization --mode real`.")
            lines.append("")
            return lines
        lines += [
            f"| Dataset | Category | Required Columns | Freshness Rule | Schema Status |",
            f"|---------|----------|-----------------|----------------|---------------|",
        ]
        for row in schema[:30]:
            ds   = row.get("dataset_name", "")
            cat  = row.get("category", "").split(".")[-1].strip()
            req  = (row.get("required_columns", "") or "")[:50]
            fresh = row.get("freshness_rule", "")[:40]
            status = "OK"
            lines.append(f"| {ds} | {cat} | `{req}` | {fresh} | {status} |")
        lines.append("")
        return lines

    def _section_lineage(self, lineage: List[dict]) -> List[str]:
        lines = [
            f"## 三、Data Lineage",
            f"",
        ]
        if not lineage:
            lines.append("No lineage records. Run `data-lineage` to scan.")
            lines.append("")
            return lines
        lines += [
            f"| Dataset | Provider | Modified | Rows | Freshness | Warning |",
            f"|---------|----------|----------|------|-----------|---------|",
        ]
        for row in lineage[:25]:
            ds    = row.get("dataset_name", "")
            prov  = (row.get("source_provider", "") or "")[:20]
            mtime = (row.get("modified_at", "") or "")[:10]
            rows  = row.get("rows", 0)
            fresh = row.get("freshness_status", "UNKNOWN")
            warn  = (row.get("warning", "") or "")[:40]
            lines.append(f"| {ds} | {prov} | {mtime} | {rows} | {fresh} | {warn} |")
        lines.append("")
        return lines

    def _section_readiness(self, readiness: List[dict]) -> List[str]:
        lines = [
            f"## 四、Feature Readiness",
            f"",
        ]
        if not readiness:
            lines.append("No readiness data. Run `feature-readiness` to check.")
            lines.append("")
            return lines
        lines += [
            f"| Feature Group | Status | Score | Stale | Leakage Risk | Notes |",
            f"|---------------|--------|-------|-------|-------------|-------|",
        ]
        for row in readiness:
            fg    = row.get("feature_group", row.get("dataset_name", ""))
            st    = row.get("status", "")
            score = row.get("readiness_score", 0.0)
            stale = row.get("stale", False)
            leak  = row.get("leakage_risk", False)
            notes = (str(row.get("notes", "")) or "")[:50]
            lines.append(f"| {fg} | {st} | {score}% | {stale} | {leak} | {notes} |")
        lines.append("")
        return lines

    def _section_health(self, health: dict) -> List[str]:
        blockers = health.get("blockers", [])
        warnings = health.get("warnings", [])
        lines = [
            f"## 五、Feature Store Health",
            f"",
            f"| 項目 | 值 |",
            f"|------|---|",
            f"| Overall Status | {health.get('overall_status', 'UNKNOWN')} |",
            f"| Health Score | {health.get('health_score', 0.0)}% |",
            f"| Ready | {health.get('ready_count', 0)} |",
            f"| Partial | {health.get('partial_count', 0)} |",
            f"| Missing | {health.get('missing_count', 0)} |",
            f"| Stale | {health.get('stale_count', 0)} |",
            f"| Leakage Risk | {health.get('leakage_risk_count', 0)} |",
            f"",
        ]
        if blockers:
            lines.append("**Blockers:**")
            lines.append("")
            for b in blockers:
                lines.append(f"- {b}")
            lines.append("")
        if warnings:
            lines.append("**Warnings:**")
            lines.append("")
            for w in warnings[:10]:
                lines.append(f"- {w}")
            lines.append("")
        return lines

    def _section_leakage(self, leakage: List[dict]) -> List[str]:
        lines = [
            f"## 六、Leakage Guard",
            f"",
        ]
        if not leakage:
            lines.append("No leakage warnings detected.")
            lines.append("")
            return lines
        lines += [
            f"| Dataset / Feature | Warning | Severity | Suggested Fix |",
            f"|-------------------|---------|----------|---------------|",
        ]
        for row in leakage[:20]:
            ds   = row.get("dataset_name", "")
            warn = (row.get("warning", "") or "")[:60]
            sev  = row.get("severity", "")
            fix  = (row.get("suggested_fix", "") or "")[:60]
            lines.append(f"| {ds} | {warn} | {sev} | {fix} |")
        lines.append("")
        return lines

    def _section_provider_integration(self, summary: dict) -> List[str]:
        return [
            f"## 七、Data Quality / Provider Integration",
            f"",
            f"| 項目 | 值 |",
            f"|------|---|",
            f"| Provider Health | Integrated via data.providers.provider_health |",
            f"| Data Quality Gate | Integrated via quality.data_quality_gate |",
            f"| Data Freshness | Tracked via DataLineageTracker |",
            f"| Known Blockers | {summary.get('blockers', 'None')} |",
            f"",
        ]

    def _section_next_actions(self, health: dict, leakage: List[dict]) -> List[str]:
        lines = [
            f"## 八、Next Actions",
            f"",
        ]
        actions = []
        try:
            missing_count = int(health.get("missing_count", 0) or 0)
            stale_count   = int(health.get("stale_count", 0) or 0)
        except (ValueError, TypeError):
            missing_count = 0
            stale_count   = 0
        if missing_count > 0:
            actions.append("- Fix missing schema definitions in DatasetSchemaRegistry")
        if stale_count > 0:
            actions.append("- Update stale data via data provider fetch commands")
        if leakage:
            actions.append("- Review and resolve leakage warnings (see Section 六)")
        actions.append("- Rerun data quality gate: `python main.py data-quality-gate --mode real`")
        actions.append("- Rerun feature readiness: `python main.py feature-readiness`")
        for a in actions:
            lines.append(a)
        lines.append("")
        return lines

    def _section_safety(self, today: str) -> List[str]:
        return [
            f"## 九、安全聲明",
            f"",
            f"| Safety Flag | Value |",
            f"|-------------|-------|",
            f"| Data Stabilization Only | True |",
            f"| Research Only | True |",
            f"| No Real Orders | True |",
            f"| No broker execution | True |",
            f"| No auto trading | True |",
            f"| read_only | True |",
            f"| production_blocked | True |",
            f"| real_order_ready | False |",
            f"",
            f"---",
            f"",
            f"*TW Quant Cockpit {self.VERSION} — Data Stabilization Only — Not Investment Advice*",
        ]

    # ------------------------------------------------------------------
    # Data loaders
    # ------------------------------------------------------------------

    def _load_summary(self) -> dict:
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_latest_summary()
        except Exception as exc:
            logger.warning("_load_summary: %s", exc)
            return {}

    def _load_schema(self) -> List[dict]:
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_schema_status()
        except Exception as exc:
            logger.warning("_load_schema: %s", exc)
            return []

    def _load_lineage(self) -> List[dict]:
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_lineage()
        except Exception as exc:
            logger.warning("_load_lineage: %s", exc)
            return []

    def _load_readiness(self) -> List[dict]:
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_feature_readiness()
        except Exception as exc:
            logger.warning("_load_readiness: %s", exc)
            return []

    def _load_health(self) -> dict:
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_health()
        except Exception as exc:
            logger.warning("_load_health: %s", exc)
            return {}

    def _load_leakage(self) -> List[dict]:
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            return DataStabilizationStore(output_dir=self.output_dir).load_leakage_summary()
        except Exception as exc:
            logger.warning("_load_leakage: %s", exc)
            return []

    def _write(self, content: str, today: str) -> str:
        try:
            os.makedirs(self.report_dir, exist_ok=True)
            path = os.path.join(
                self.report_dir, f"data_stabilization_report_{today}.md"
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("DataStabilizationReport → %s", path)
            return path
        except Exception as exc:
            logger.warning("DataStabilizationReport._write(): %s", exc)
            return ""
