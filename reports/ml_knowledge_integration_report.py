"""
reports/ml_knowledge_integration_report.py — ML Knowledge Integration Report (v0.4.2.1).

Generates a 7-section Markdown report integrating transcript-derived knowledge
with the ML Feature Store.

Sections:
  1. Header / Safety Banner
  2. Integration Summary
  3. Feature Catalog Table
  4. Readiness Distribution
  5. Leakage Findings
  6. Model-Ready Schema Summary
  7. Recommendations

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Knowledge Only.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MLKnowledgeIntegrationReport:
    """
    Markdown report generator for v0.4.2.1 ML Knowledge Integration.

    [!] ML Research Only. No Real Orders.
    """

    read_only: bool = True
    no_real_orders: bool = True
    auto_enabled: bool = False

    def __init__(self, report_dir: str = "reports"):
        if os.path.isabs(report_dir):
            self._report_dir = report_dir
        else:
            self._report_dir = os.path.join(BASE_DIR, report_dir)
        os.makedirs(self._report_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def generate(
        self,
        integration_summary: dict,
        catalog_features:    List[dict],
        readiness_results:   List[dict],
        leakage_result:      dict,
        schema_summary:      dict,
        mode:                str = "real",
        dry_run:             bool = False,
    ) -> str:
        """
        Generate and write the Markdown report.
        Returns path to report file.
        """
        now = datetime.now()
        ts  = now.strftime("%Y%m%d_%H%M%S")
        filename = f"ml_knowledge_integration_report_{ts}.md"
        path = os.path.join(self._report_dir, filename)

        sections = [
            self._section_header(now, mode),
            self._section_integration_summary(integration_summary),
            self._section_feature_catalog(catalog_features),
            self._section_readiness_distribution(readiness_results),
            self._section_leakage_findings(leakage_result),
            self._section_model_ready_schema(schema_summary),
            self._section_recommendations(leakage_result, readiness_results, integration_summary),
        ]
        content = "\n\n".join(sections)

        if not dry_run:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            logger.info("MLKnowledgeIntegrationReport: report written → %s", path)
        else:
            logger.info("MLKnowledgeIntegrationReport: dry_run — report not written")

        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self, now: datetime, mode: str) -> str:
        return f"""# ML Knowledge Integration Report — v0.4.2.1

> **[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] No live prediction. No auto-trading. Knowledge Only. auto_enabled=False.**
> **[!] Transcript-only confidence capped at PARTIAL. Long-cycle risk = Metadata Only.**

| Field | Value |
|-------|-------|
| Generated | {now.strftime("%Y-%m-%d %H:%M:%S")} |
| Mode | {mode} |
| Version | v0.4.2.1 |
| ML Research Only | True |
| No Real Orders | True |
| auto_enabled Count | 0 |"""

    def _section_integration_summary(self, summary: dict) -> str:
        if not summary:
            return "## Integration Summary\n\n_No integration summary available._"

        total  = summary.get("total_features_count", summary.get("total_features", 0))
        auto   = 0  # always 0
        mr     = summary.get("model_ready_features", 0)
        src    = summary.get("source_rows", {})
        lines  = [
            "## Integration Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Knowledge Features | {total} |",
            f"| Auto Enabled | {auto} |",
            f"| Model-Ready (Optional) | {mr} |",
            f"| Factor Candidates | {src.get('factor_candidates', 0)} |",
            f"| Rule Candidates | {src.get('rule_candidates', 0)} |",
            f"| Avoid Conditions | {src.get('avoid_conditions', 0)} |",
            f"| Risk Conditions | {src.get('risk_conditions', 0)} |",
        ]
        if summary.get("leakage_findings"):
            lines.append(f"| Leakage Findings | {summary['leakage_findings']} |")
        if summary.get("critical_leakage"):
            lines.append(f"| Critical Leakage | {summary['critical_leakage']} |")
        return "\n".join(lines)

    def _section_feature_catalog(self, features: List[dict]) -> str:
        if not features:
            return (
                "## Feature Catalog\n\n"
                "_No transcript-derived features found. "
                "Run `strategy-knowledge-ingest` first to populate knowledge CSVs._"
            )
        lines = [
            "## Feature Catalog",
            "",
            "| Feature ID | Name | Source | Type | Readiness | Confidence | Auto Enabled |",
            "|------------|------|--------|------|-----------|------------|--------------|",
        ]
        for f in features[:50]:  # cap table at 50 rows for report
            lines.append(
                f"| `{f.get('feature_id','')}` "
                f"| {f.get('feature_name','')} "
                f"| {f.get('feature_source','')} "
                f"| {f.get('feature_type','')} "
                f"| {f.get('readiness','')} "
                f"| {f.get('confidence','')} "
                f"| False |"
            )
        if len(features) > 50:
            lines.append(f"\n_... {len(features) - 50} more features not shown._")
        return "\n".join(lines)

    def _section_readiness_distribution(self, readiness_results: List[dict]) -> str:
        if not readiness_results:
            return "## Readiness Distribution\n\n_No readiness results._"
        by_readiness: Dict[str, int] = {}
        for r in readiness_results:
            rd = r.get("readiness", "UNKNOWN")
            by_readiness[rd] = by_readiness.get(rd, 0) + 1

        lines = [
            "## Readiness Distribution",
            "",
            "| Readiness | Count | Meaning |",
            "|-----------|-------|---------|",
        ]
        readiness_desc = {
            "READY":             "Validated, no leakage — optional use in model schema",
            "PARTIAL":           "Partially validated — needs confirmation",
            "METADATA_ONLY":     "Regime/cycle metadata only — NOT for short-term labels",
            "NEEDS_MAPPING":     "Factor candidate — needs column mapping to data source",
            "NEEDS_BACKTEST":    "Rule candidate — requires empirical backtest first",
            "LEAKAGE_RISK":      "Leakage risk detected — requires manual review",
            "BLOCKED":           "Blocked — critical leakage or pattern incomplete",
            "INSUFFICIENT_DATA": "Insufficient data to assess",
        }
        for rd, cnt in sorted(by_readiness.items(), key=lambda x: -x[1]):
            desc = readiness_desc.get(rd, "")
            lines.append(f"| {rd} | {cnt} | {desc} |")
        return "\n".join(lines)

    def _section_leakage_findings(self, leakage_result: dict) -> str:
        status  = leakage_result.get("status", "UNKNOWN")
        total   = leakage_result.get("total_findings", 0)
        critical = leakage_result.get("critical_count", 0)
        warnings = leakage_result.get("warning_count", 0)
        summary = leakage_result.get("summary", {})
        by_type = summary.get("by_leakage_type", {})

        lines = [
            "## Leakage Findings",
            "",
            f"**Overall Status: {status}**",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Findings | {total} |",
            f"| Critical | {critical} |",
            f"| Warning | {warnings} |",
        ]
        if by_type:
            lines.extend(["", "### By Leakage Type", "",
                          "| Type | Count |", "|------|-------|"])
            for lt, cnt in sorted(by_type.items(), key=lambda x: -x[1]):
                lines.append(f"| {lt} | {cnt} |")

        recs = summary.get("recommendations", [])
        if recs:
            lines.extend(["", "### Leakage Recommendations", ""])
            for rec in recs:
                lines.append(f"- {rec}")

        return "\n".join(lines)

    def _section_model_ready_schema(self, schema_summary: dict) -> str:
        if not schema_summary:
            return "## Model-Ready Schema\n\n_No schema summary available._"
        total_mr = schema_summary.get("total_model_ready", 0)
        lines = [
            "## Model-Ready Schema Summary",
            "",
            f"> Features in model-ready schema are **OPTIONAL** and **auto_enabled=False**.",
            f"> Include with `--include-knowledge-features` flag (default: False).",
            f"> Long-cycle / regime features are **excluded** from model-ready schema.",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Model-Ready Features | {total_mr} |",
            f"| Include by Default | False |",
            f"| Auto Enabled | 0 |",
            f"| Enable Flag | --include-knowledge-features |",
        ]
        feats = schema_summary.get("features", [])
        if feats:
            lines.extend(["", "### Model-Ready Feature List", "",
                          "| Feature ID | Name | Type | Readiness |",
                          "|------------|------|------|-----------|"])
            for f in feats[:20]:
                lines.append(
                    f"| `{f.get('feature_id','')}` "
                    f"| {f.get('feature_name','')} "
                    f"| {f.get('feature_type','')} "
                    f"| {f.get('readiness','')} |"
                )
        return "\n".join(lines)

    def _section_recommendations(
        self,
        leakage_result: dict,
        readiness_results: List[dict],
        integration_summary: dict,
    ) -> str:
        lines = ["## Recommendations", ""]
        recs = []

        # Auto-enabled check (always 0)
        recs.append(
            "auto_enabled=False for all transcript-derived features — "
            "explicit opt-in required via --include-knowledge-features"
        )

        # Check leakage
        leakage_recs = leakage_result.get("summary", {}).get("recommendations", [])
        recs.extend(leakage_recs)

        # Check needs-backtest
        nb_count = sum(1 for r in readiness_results if r.get("readiness") == "NEEDS_BACKTEST")
        if nb_count:
            recs.append(
                f"{nb_count} rule candidates require backtest validation "
                "before they can be used as ML features"
            )

        # Check needs-mapping
        nm_count = sum(1 for r in readiness_results if r.get("readiness") == "NEEDS_MAPPING")
        if nm_count:
            recs.append(
                f"{nm_count} factor candidates need column mapping to actual data sources"
            )

        for rec in recs:
            lines.append(f"- {rec}")

        lines.extend([
            "",
            "---",
            "",
            "_ML Knowledge Integration v0.4.2.1 — Research Only. No Real Orders._",
        ])
        return "\n".join(lines)
