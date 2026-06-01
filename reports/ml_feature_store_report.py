"""
reports/ml_feature_store_report.py — ML Feature Store Report Builder (v0.4.2).

Generates: reports/ml_feature_store_report_YYYY-MM-DD.md

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] Not investment advice. Do not commit this report.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MLFeatureStoreReportBuilder:
    """
    ML Feature Store Report Builder.

    Parameters
    ----------
    report_dir : Output directory (default: reports/)
    mode       : "real" or "mock"
    """

    VERSION = "v0.4.2"

    _SAFETY_FLAGS = {
        "research_only":              True,
        "ml_research_only":           True,
        "no_real_orders":             True,
        "production_trading_blocked": True,
        "no_live_prediction":         True,
        "no_auto_trading":            True,
    }

    def __init__(self, report_dir: str = "reports", mode: str = "real"):
        self.mode       = mode
        self._report_dir = os.path.join(_BASE_DIR, report_dir) if not os.path.isabs(report_dir) else report_dir
        os.makedirs(self._report_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def build(
        self,
        catalog_summary:   Optional[dict] = None,
        snapshot_summary:  Optional[dict] = None,
        label_summary:     Optional[dict] = None,
        split_summary:     Optional[dict] = None,
        leakage_result:    Optional[dict] = None,
        quality_result:    Optional[dict] = None,
        importance_result: Optional[dict] = None,
        lineage_summary:   Optional[dict] = None,
    ) -> str:
        """Build and save the report. Returns output file path."""
        today = datetime.now().strftime("%Y-%m-%d")
        sections = self._build_sections(
            today, catalog_summary, snapshot_summary, label_summary,
            split_summary, leakage_result, quality_result,
            importance_result, lineage_summary,
        )
        content = "\n\n".join(sections)
        out_path = os.path.join(self._report_dir, f"ml_feature_store_report_{today}.md")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as exc:
            logger.warning("MLFeatureStoreReportBuilder: cannot write %s: %s", out_path, exc)
        return out_path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _build_sections(self, today, catalog_summary, snapshot_summary, label_summary,
                        split_summary, leakage_result, quality_result, importance_result, lineage_summary):
        sections = []
        # Header
        sections.append(
            f"# ML Feature Store Report\n\n"
            f"**Version:** {self.VERSION}  \n"
            f"**Date:** {today}  \n"
            f"**Mode:** {self.mode}  \n"
            f"**Generated:** {datetime.now().isoformat()}"
        )
        sections.append(self._section_overview(snapshot_summary, quality_result, leakage_result))
        sections.append(self._section_catalog(catalog_summary))
        sections.append(self._section_labels(label_summary))
        sections.append(self._section_split(split_summary))
        sections.append(self._section_leakage(leakage_result))
        sections.append(self._section_quality(quality_result))
        sections.append(self._section_importance(importance_result))
        sections.append(self._section_lineage(lineage_summary))
        sections.append(self._section_safety())
        return sections

    def _section_overview(self, snapshot_summary, quality_result, leakage_result):
        s = snapshot_summary or {}
        q = quality_result or {}
        l = leakage_result or {}
        lines = [
            "## 一、總覽", "",
            f"- **Mode:** {self.mode}",
            "- **Research Only:** True",
            "- **ML Research Only:** True",
            "- **No Real Orders:** True",
            f"- **Feature count:** {s.get('feature_count', q.get('feature_count', '—'))}",
            f"- **Row count:** {s.get('row_count', q.get('row_count', '—'))}",
            f"- **Symbol count:** {s.get('symbol_count', q.get('symbol_count', '—'))}",
            f"- **Date range:** {s.get('date_range', q.get('date_range', ('—', '—')))}",
            f"- **Dataset status:** {s.get('status', '—')}",
            f"- **Leakage status:** {l.get('status', '—')}",
            f"- **Feature quality score:** {q.get('feature_quality_score', '—')}",
        ]
        return "\n".join(lines)

    def _section_catalog(self, catalog_summary):
        c = catalog_summary or {}
        lines = ["## 二、Feature Catalog", ""]
        lines.append(f"- **Total features:** {c.get('total_features', '—')}")
        lines.append(f"- **Enabled features:** {c.get('enabled_features', '—')}")
        lines.append(f"- **Experimental features:** {c.get('experimental_features', '—')}")
        lines.append(f"- **High leakage risk features:** {c.get('high_leakage_risk', '—')}")
        cats = c.get("categories", {})
        if cats:
            lines.append("")
            lines.append("| Category | Count |")
            lines.append("|---|---|")
            for cat, count in sorted(cats.items()):
                lines.append(f"| {cat} | {count} |")
        return "\n".join(lines)

    def _section_labels(self, label_summary):
        l = label_summary or {}
        lines = ["## 三、Label Generation", ""]
        horizons = l.get("horizons", [])
        label_cols = l.get("label_columns", [])
        lines.append(f"- **Horizons:** {horizons}")
        lines.append(f"- **Label columns:** {len(label_cols)}")
        balance = l.get("label_balance", {})
        if balance:
            lines.append("")
            lines.append("**Label Balance:**")
            lines.append("")
            lines.append("| Label | Class | Ratio |")
            lines.append("|---|---|---|")
            for col, dist in list(balance.items())[:10]:
                if isinstance(dist, dict):
                    for cls, ratio in dist.items():
                        if isinstance(ratio, float):
                            lines.append(f"| {col} | {cls} | {ratio:.2%} |")
        return "\n".join(lines)

    def _section_split(self, split_summary):
        s = split_summary or {}
        lines = ["## 四、Train / Validation / Test Split", ""]
        lines.append(f"- **Method:** {s.get('method', 'time_series')}")
        lines.append(f"- **Train ratio:** {s.get('train_ratio', '—')}")
        lines.append(f"- **Validation ratio:** {s.get('validation_ratio', '—')}")
        lines.append(f"- **Test ratio:** {s.get('test_ratio', '—')}")
        tr = s.get("train_date_range", ("", ""))
        vr = s.get("validation_date_range", ("", ""))
        tsr = s.get("test_date_range", ("", ""))
        lines.append(f"- **Train date range:** {tr[0]} — {tr[1]}")
        lines.append(f"- **Validation date range:** {vr[0]} — {vr[1]}")
        lines.append(f"- **Test date range:** {tsr[0]} — {tsr[1]}")
        counts = s.get("split_row_counts", {})
        if counts:
            lines.append("")
            lines.append("| Split | Rows |")
            lines.append("|---|---|")
            for split_name, count in counts.items():
                lines.append(f"| {split_name} | {count} |")
        return "\n".join(lines)

    def _section_leakage(self, leakage_result):
        l = leakage_result or {}
        lines = ["## 五、No Leakage Check", ""]
        status = l.get("status", "—")
        score  = l.get("score", "—")
        lines.append(f"- **Status:** {status}")
        lines.append(f"- **Score:** {score}")
        if status == "BLOCKED_FOR_TRAINING":
            lines.append("")
            lines.append("**[!] DATASET BLOCKED FOR TRAINING — Leakage detected. See findings below.**")
        findings = l.get("findings", [])
        if findings:
            lines.append("")
            lines.append("| Finding | Severity | Column | Reason |")
            lines.append("|---|---|---|---|")
            for f in findings[:20]:
                reason = str(f.get("reason", ""))[:60]
                lines.append(f"| {f.get('finding','')} | {f.get('severity','')} | {f.get('column','')} | {reason} |")
        else:
            lines.append("- *No leakage findings.*")
        recs = l.get("recommended_actions", [])
        if recs:
            lines.append("")
            lines.append("**Recommended Actions:**")
            for r in recs:
                lines.append(f"- {r}")
        return "\n".join(lines)

    def _section_quality(self, quality_result):
        q = quality_result or {}
        lines = ["## 六、Feature Quality", ""]
        lines.append(f"- **Feature quality score:** {q.get('feature_quality_score', '—')}")
        lines.append(f"- **Constant features:** {q.get('constant_feature_count', 0)}")
        high_missing = q.get("high_missing_features", [])
        lines.append(f"- **High missing (>50%) features:** {len(high_missing)}")
        if high_missing:
            lines.append(f"  - {', '.join(high_missing[:10])}")
        for w in q.get("warnings", []):
            lines.append(f"- **⚠** {w}")
        return "\n".join(lines)

    def _section_importance(self, importance_result):
        i = importance_result or {}
        lines = ["## 七、Feature Importance Shell", ""]
        lines.append(f"- **Method:** {i.get('method', '—')}")
        lines.append(f"- **Target label:** {i.get('target_label', '—')}")
        lines.append(f"- **sklearn available:** {i.get('sklearn_available', '—')}")
        lines.append("")
        lines.append("> [!] Importance scores are exploratory only — not investment advice.")
        top = i.get("top_features", [])
        if top:
            lines.append("")
            lines.append("| # | Feature | Correlation | Direction |")
            lines.append("|---|---|---|---|")
            for j, f in enumerate(top[:15], 1):
                lines.append(f"| {j} | {f.get('feature','')} | {f.get('score',0):.4f} | {f.get('direction','')} |")
        else:
            lines.append("*No importance data available.*")
        return "\n".join(lines)

    def _section_lineage(self, lineage_summary):
        l = lineage_summary or {}
        lines = ["## 八、Data Lineage", ""]
        if not l:
            lines.append("*No lineage data recorded.*")
            return "\n".join(lines)
        lines.append(f"- **Source datasets:** {l.get('source_datasets', '—')}")
        lines.append(f"- **Provider lineage:** {l.get('provider_lineage', '—')}")
        return "\n".join(lines)

    def _section_safety(self):
        return (
            "## 九、安全聲明\n\n"
            "- **Research Only:** True\n"
            "- **ML Research Only:** True\n"
            "- **No Real Orders:** True\n"
            "- **No Live Prediction:** True\n"
            "- **No Auto-Trading:** True\n"
            "- **Production Trading:** BLOCKED\n"
            "- **REAL_ORDER_READY:** False\n"
            "- **Auto weight apply:** DISABLED\n\n"
            "> This report is generated for ML research purposes only.  \n"
            "> It does not constitute investment advice.  \n"
            "> Do not use model outputs for real trading decisions.  \n"
            "> All production trading is permanently blocked."
        )
