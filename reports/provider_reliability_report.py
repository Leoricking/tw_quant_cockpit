"""
reports/provider_reliability_report.py - Provider Reliability Report builder (v0.3.24).

Generates: reports/provider_reliability_report_YYYY-MM-DD.md

[!] Read Only. No Real Orders. Research Only.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProviderReliabilityReportBuilder:
    """
    Generates the Provider Reliability & Fallback Matrix report.

    Parameters
    ----------
    report_date  : YYYY-MM-DD string
    matrix_data  : dict from ProviderReliabilityMatrix.run()
    """

    def __init__(
        self,
        report_date: Optional[str] = None,
        matrix_data: Optional[dict] = None,
    ):
        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")
        self.data        = matrix_data or {}

    def build(self, output_dir: Optional[str] = None) -> str:
        """Build the Markdown report and return the output path."""
        out_dir = output_dir or os.path.join(_BASE_DIR, "reports")
        os.makedirs(out_dir, exist_ok=True)
        fname   = f"provider_reliability_report_{self.report_date}.md"
        fpath   = os.path.join(out_dir, fname)

        lines: List[str] = []
        lines += self._header()
        lines += self._section_overview()
        lines += self._section_provider_reliability()
        lines += self._section_dataset_fallback_matrix()
        lines += self._section_dataset_confidence()
        lines += self._section_fallback_reasons()
        lines += self._section_no_mock_fallback()
        lines += self._section_recommendations()
        lines += self._section_safety()

        content = "\n".join(lines) + "\n"
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Provider reliability report written: %s", fpath)
        except Exception as exc:
            logger.error("Cannot write report: %s", exc)
        return fpath

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _header(self) -> List[str]:
        return [
            f"# Provider Reliability & Fallback Matrix Report",
            f"",
            f"> Date: {self.report_date}  |  Mode: {self.data.get('mode', 'real').upper()}  |  v0.3.24",
            f"> **[!] Read Only | No Real Orders | Production Trading: BLOCKED**",
            f"",
        ]

    def _section_overview(self) -> List[str]:
        summary = self.data.get("reliability_summary", {})
        lines = [
            "## 一、總覽",
            "",
            f"| Item | Value |",
            f"|---|---|",
            f"| Mode | {self.data.get('mode', 'real').upper()} |",
            f"| Read Only | Yes |",
            f"| No Real Orders | Yes |",
            f"| Production Trading | BLOCKED |",
            f"| Mock Fallback | DISABLED |",
            f"| Providers Checked | {summary.get('providers_checked', '?')} |",
            f"| Datasets Covered | {summary.get('datasets_covered', '?')} |",
            f"| Overall Provider Reliability | {summary.get('overall_reliability_score', 'N/A')} |",
            f"| Overall Dataset Confidence | {summary.get('overall_dataset_confidence', 'N/A')} |",
            f"| High Confidence Datasets | {', '.join(summary.get('high_confidence_datasets', [])) or 'None'} |",
            f"| Weak Datasets | {', '.join(summary.get('weak_datasets', [])) or 'None'} |",
            f"| Local Fallback Used | {summary.get('local_fallback_count', 0)} datasets |",
            f"| Mock Fallback Used | {summary.get('mock_fallback_count', 0)} (must be 0) |",
            "",
        ]
        return lines

    def _section_provider_reliability(self) -> List[str]:
        lines = [
            "## 二、Provider Reliability",
            "",
            "| Provider | Status | Token | Success Rate | Latency | Row Coverage | Reliability Score | Recommended Usage |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for p in self.data.get("provider_summary", []):
            sr    = f"{p['success_rate']:.0%}" if isinstance(p.get("success_rate"), float) else "N/A"
            lat   = f"{p['latency_score']:.2f}" if isinstance(p.get("latency_score"), float) else "N/A"
            cov   = f"{p['row_coverage_score']:.2f}" if isinstance(p.get("row_coverage_score"), float) else "N/A"
            rel   = f"{p['reliability_score']:.1f}" if isinstance(p.get("reliability_score"), float) else "N/A"
            token = "Yes" if p.get("token_configured") else "No"
            lines.append(
                f"| {p['provider_name']} | {p['status']} | {token} | {sr} | {lat} | {cov} | {rel} | {p.get('recommended_usage', '')} |"
            )
        lines.append("")
        return lines

    def _section_dataset_fallback_matrix(self) -> List[str]:
        lines = [
            "## 三、Dataset Fallback Matrix",
            "",
            "| Dataset | Primary | Fallback 1 | Fallback 2 | Local Fallback | Last Used | Confidence | Recommendation |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for row in self.data.get("dataset_matrix", []):
            conf = f"{row['confidence_score']:.1f} ({row['confidence_level']})"
            lines.append(
                f"| {row['dataset']} | {row['primary_provider']} | {row['fallback_1']} | {row['fallback_2']} "
                f"| {row['local_fallback']} | {row['provider_used_last_run'] or '—'} | {conf} | {row['recommendation']} |"
            )
        lines.append("")
        return lines

    def _section_dataset_confidence(self) -> List[str]:
        lines = [
            "## 四、Dataset Confidence Score",
            "",
            "| Dataset | Score | Level | Freshness | Coverage | Missing Symbols | Note |",
            "|---|---|---|---|---|---|---|",
        ]
        for dataset, v in self.data.get("dataset_confidence_scores", {}).items():
            score   = f"{v.get('score', 0):.1f}"
            level   = v.get("level", "UNKNOWN")
            fresh   = v.get("freshness_status", "—")
            cov     = f"{v.get('coverage_ratio', 0):.1%}" if isinstance(v.get("coverage_ratio"), float) else "—"
            missing = str(v.get("missing_symbols_count", "—"))
            note    = v.get("cap_reason", "")
            lines.append(f"| {dataset} | {score} | {level} | {fresh} | {cov} | {missing} | {note} |")
        lines.append("")
        return lines

    def _section_fallback_reasons(self) -> List[str]:
        lines = [
            "## 五、Fallback Reason",
            "",
        ]
        for row in self.data.get("fallback_matrix", []):
            reasons = row.get("fallback_reason", {})
            chain   = " -> ".join(row.get("provider_order", []))
            lines.append(f"**{row['dataset']}**: {chain}")
            for pname, reason in reasons.items():
                lines.append(f"  - `{pname}`: {reason}")
            lines.append("")
        return lines

    def _section_no_mock_fallback(self) -> List[str]:
        return [
            "## 六、No Mock Fallback Policy",
            "",
            "- **Real mode**: Mock fallback is strictly DISABLED. Provider failures result in graceful fallback to next real provider or local CSV/XQ.",
            "- **Mock mode**: Used for demo/testing only. Not for production research.",
            "- `mock_fallback_count` in real mode must always be **0**.",
            "",
        ]

    def _section_recommendations(self) -> List[str]:
        lines = [
            "## 七、Recommendations",
            "",
        ]
        for rec in self.data.get("recommendations", []):
            lines.append(f"- {rec}")
        lines.append("")
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## 八、安全聲明",
            "",
            "- **Research Only** — not for live trading",
            "- **Read Only** — no write to broker API",
            "- **No Real Orders** — `no_real_orders=True`",
            "- **Production Trading: BLOCKED** — `REAL_ORDER_READY=False`",
            "- **Mock Fallback: DISABLED** — real mode never falls back to mock",
            "",
        ]
