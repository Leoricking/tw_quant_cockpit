"""
reports/auto_report_index.py - Auto Report Center index and manifest builder (v0.3.16).

Generates:
  reports/auto_report_center/YYYY-MM-DD/index.md
  reports/auto_report_center/YYYY-MM-DD/manifest.json

[!] Research Only. Simulation Only. No Real Orders.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AutoReportIndexBuilder:
    """
    Builds index.md and manifest.json for a dated Auto Report Center output folder.

    Parameters
    ----------
    report_date : YYYY-MM-DD string
    mode        : 'real' or 'mock'
    generated   : list of dicts from AutoReportCenter._generated
    failed      : list of dicts from AutoReportCenter._failed
    context     : cross-report context dict from AutoReportCenter._context
    """

    VERSION = "v0.3.16"

    # Safety flags written into every manifest
    _SAFETY_FLAGS = {
        "research_only": True,
        "simulation_only": True,
        "no_real_orders": True,
        "does_not_auto_apply_weights": True,
        "does_not_connect_broker_api": True,
    }

    def __init__(
        self,
        report_date: str,
        mode: str = "real",
        generated: Optional[List[dict]] = None,
        failed: Optional[List[dict]] = None,
        context: Optional[dict] = None,
    ):
        self.report_date = report_date
        self.mode        = mode
        self.generated   = generated or []
        self.failed      = failed or []
        self.context     = context or {}

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def build(self, output_dir: str) -> dict:
        """
        Build index.md and manifest.json in output_dir.

        Returns dict:
            index_path    : path to index.md (or None on failure)
            manifest_path : path to manifest.json (or None on failure)
        """
        os.makedirs(output_dir, exist_ok=True)

        index_path    = self._build_index(output_dir)
        manifest_path = self._build_manifest(output_dir)

        return {
            "index_path":    index_path,
            "manifest_path": manifest_path,
        }

    # ------------------------------------------------------------------
    # index.md
    # ------------------------------------------------------------------

    def _build_index(self, output_dir: str) -> Optional[str]:
        try:
            lines: List[str] = []
            lines += self._section_overview()
            lines += self._section_key_findings()
            lines += self._section_report_links()
            lines += self._section_limitations()

            content = "\n".join(lines) + "\n"
            path = os.path.join(output_dir, "index.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("index.md written → %s", path)
            return path
        except Exception as exc:
            logger.error("AutoReportIndexBuilder: index.md failed: %s", exc)
            return None

    # ---- Section 一: 今日總覽 ----------------------------------------

    def _section_overview(self) -> List[str]:
        ctx = self.context
        gen_count  = len(self.generated)
        fail_count = len(self.failed)
        usize      = ctx.get("universe_size", "N/A")
        readiness  = ctx.get("data_readiness", "UNKNOWN")
        confidence = ctx.get("confidence", "OBSERVATIONAL")

        lines = [
            f"# TW Quant Cockpit — Daily Research Report Center",
            f"",
            f"> **{self.VERSION}** | Report Date: {self.report_date} | Mode: {self.mode.upper()}",
            f">",
            f"> [!] Advisory Only. Simulation Only. No Real Orders.",
            f"",
            f"---",
            f"",
            f"## 一、今日總覽",
            f"",
            f"| 項目 | 值 |",
            f"|------|---|",
            f"| Report Date | {self.report_date} |",
            f"| Mode | {self.mode.upper()} |",
            f"| Universe Size | {usize} symbols |",
            f"| Data Readiness | {readiness} |",
            f"| Confidence Level | {confidence} |",
            f"| Generated Reports | {gen_count} |",
            f"| Failed Reports | {fail_count} |",
            f"| Safety Status | Research Only / Simulation Only / No Real Orders |",
            f"",
        ]

        # Generated report list
        if self.generated:
            lines.append("**Generated:**")
            lines.append("")
            for g in self.generated:
                name = g.get("name", "unknown")
                path = g.get("path", "")
                rel  = self._rel(path, output_dir=None)
                lines.append(f"- ✓ **{name}** → `{rel}`")
            lines.append("")

        # Failed report list
        if self.failed:
            lines.append("**Failed:**")
            lines.append("")
            for f in self.failed:
                name = f.get("name", "unknown")
                err  = f.get("error", "")
                lines.append(f"- ✗ **{name}** — {err}")
            lines.append("")

        return lines

    # ---- Section 二: 重點結論 ----------------------------------------

    def _section_key_findings(self) -> List[str]:
        ctx = self.context
        lines = [
            "---",
            "",
            "## 二、重點結論",
            "",
        ]

        # Top candidate stocks
        top_candidates = ctx.get("top_candidates", [])
        if top_candidates:
            lines.append("### 今日候選股票")
            lines.append("")
            lines.append("| Rank | Symbol | Score |")
            lines.append("|------|--------|-------|")
            for i, c in enumerate(top_candidates[:8], 1):
                sym   = c.get("symbol", c) if isinstance(c, dict) else c
                score = c.get("score", "—") if isinstance(c, dict) else "—"
                lines.append(f"| {i} | {sym} | {score} |")
            lines.append("")
        else:
            lines.append("### 今日候選股票")
            lines.append("")
            lines.append("*未執行 / 資料不足*")
            lines.append("")

        # Portfolio best scenario
        port_best = ctx.get("portfolio_best_scenario")
        port_return = ctx.get("portfolio_best_return")
        port_sharpe = ctx.get("portfolio_best_sharpe")
        if port_best:
            lines.append("### 投資組合模擬")
            lines.append("")
            lines.append(f"- Best Scenario: **{port_best}**")
            if port_return is not None:
                lines.append(f"- Best Return: **{port_return:+.2%}**")
            if port_sharpe is not None:
                lines.append(f"- Best Sharpe: **{port_sharpe:.2f}**")
            lines.append("")
        else:
            lines.append("### 投資組合模擬")
            lines.append("")
            lines.append("*未執行 / 無結果*")
            lines.append("")

        # Signal Quality BOOST / REDUCE
        sq_boost  = ctx.get("signal_quality_boost_count", 0)
        sq_reduce = ctx.get("signal_quality_reduce_count", 0)
        sq_total  = ctx.get("signal_quality_total", 0)
        lines.append("### Signal Quality")
        lines.append("")
        lines.append(f"- Total Signals Evaluated: **{sq_total}**")
        lines.append(f"- BOOST: **{sq_boost}** | REDUCE: **{sq_reduce}**")
        lines.append("")

        # Rule Weight best config
        rw_best   = ctx.get("rule_weight_best_config")
        rw_bscore = ctx.get("rule_weight_best_balanced_score")
        if rw_best:
            lines.append("### Rule Weight Tuning")
            lines.append("")
            lines.append(f"- Best Config: **{rw_best}**")
            if rw_bscore is not None:
                lines.append(f"- Balanced Score: **{rw_bscore:.4f}**")
            lines.append("")
        else:
            lines.append("### Rule Weight Tuning")
            lines.append("")
            lines.append("*未執行 / 無結果*")
            lines.append("")

        # Long-term validation note
        lt_note = ctx.get("long_term_note", "")
        lines.append("### 長期策略驗證")
        lines.append("")
        lines.append(lt_note if lt_note else "*未執行 / 無結果*")
        lines.append("")

        # Risk warnings
        risk_warnings = ctx.get("risk_warnings", [])
        lines.append("### 風險警示")
        lines.append("")
        if risk_warnings:
            for w in risk_warnings:
                lines.append(f"- ⚠️  {w}")
        else:
            lines.append("*無特殊風險警示*")
        lines.append("")

        return lines

    # ---- Section 三: 報告連結 ----------------------------------------

    def _section_report_links(self) -> List[str]:
        lines = [
            "---",
            "",
            "## 三、報告連結",
            "",
        ]

        # Group generated reports by category
        categories = {
            "Stock Reports":          [],
            "Universe Quality":       [],
            "Signal Quality":         [],
            "Portfolio Simulation":   [],
            "Rule Weight Tuning":     [],
            "Long-Term Strategy":     [],
            "Strategy Knowledge":     [],
            "Daily Market Summary":   [],
            "Other":                  [],
        }

        _cat_map = {
            "stock_reports":         "Stock Reports",
            "universe_quality":      "Universe Quality",
            "signal_quality":        "Signal Quality",
            "portfolio":             "Portfolio Simulation",
            "rule_weight":           "Rule Weight Tuning",
            "long_term":             "Long-Term Strategy",
            "strategy_knowledge":    "Strategy Knowledge",
            "daily_market_summary":  "Daily Market Summary",
        }

        for g in self.generated:
            name = g.get("name", "")
            path = g.get("path", "")
            cat  = "Other"
            for key, label in _cat_map.items():
                if key in name.lower().replace(" ", "_").replace("-", "_"):
                    cat = label
                    break
            categories[cat].append((name, path))

        for cat_label, items in categories.items():
            if not items:
                continue
            lines.append(f"### {cat_label}")
            lines.append("")
            for name, path in items:
                rel = self._rel(path)
                lines.append(f"- [{name}]({rel})")
            lines.append("")

        if not self.generated:
            lines.append("*無已生成的報告*")
            lines.append("")

        return lines

    # ---- Section 四: 限制 --------------------------------------------

    def _section_limitations(self) -> List[str]:
        ctx = self.context
        usize = ctx.get("universe_size", 14)
        confidence = ctx.get("confidence", "OBSERVATIONAL")

        return [
            "---",
            "",
            "## 四、限制",
            "",
            "| 項目 | 說明 |",
            "|------|------|",
            "| Research Only | 本系統僅供研究與模擬，不構成投資建議 |",
            "| Simulation Only | 所有回測為歷史模擬，不代表未來績效 |",
            "| No Real Orders | 系統不連接券商 API，不自動下單 |",
            f"| Universe Size | 目前 universe 約 {usize} 支股票，樣本有限 |",
            f"| Confidence | {confidence} — 僅為觀察性，非預測性 |",
            "| TIMING_ESTIMATED | 部分訊號時機為估算，非精確時間點 |",
            "",
            "---",
            "",
            f"*Generated by TW Quant Cockpit {self.VERSION} — {self.report_date}*",
            "",
        ]

    # ------------------------------------------------------------------
    # manifest.json
    # ------------------------------------------------------------------

    def _build_manifest(self, output_dir: str) -> Optional[str]:
        try:
            ctx = self.context
            manifest = {
                "version":      self.VERSION,
                "report_date":  self.report_date,
                "generated_at": datetime.now().isoformat(),
                "mode":         self.mode,
                "safety_flags": self._SAFETY_FLAGS,
                "version_info": {
                    "auto_report_center": self.VERSION,
                    "framework":          "TW Quant Cockpit",
                },
                "data_readiness": ctx.get("data_readiness", "UNKNOWN"),
                "confidence":     ctx.get("confidence", "OBSERVATIONAL"),
                "universe_size":  ctx.get("universe_size", 0),
                "generated_count": len(self.generated),
                "failed_count":    len(self.failed),
                "generated": [
                    {
                        "name": g.get("name"),
                        "path": self._rel(g.get("path", "")),
                    }
                    for g in self.generated
                ],
                "failed": [
                    {
                        "name":  f.get("name"),
                        "error": f.get("error", ""),
                    }
                    for f in self.failed
                ],
                "key_metrics": {
                    "portfolio_best_scenario":      ctx.get("portfolio_best_scenario"),
                    "portfolio_best_return":        ctx.get("portfolio_best_return"),
                    "portfolio_best_sharpe":        ctx.get("portfolio_best_sharpe"),
                    "signal_quality_boost_count":   ctx.get("signal_quality_boost_count", 0),
                    "signal_quality_reduce_count":  ctx.get("signal_quality_reduce_count", 0),
                    "rule_weight_best_config":      ctx.get("rule_weight_best_config"),
                    "rule_weight_best_balanced_score": ctx.get("rule_weight_best_balanced_score"),
                },
                "data_quality_gate": _extract_quality_gate_fields(ctx),
                "provider_reliability": _extract_reliability_fields(ctx),
                "universe_name": ctx.get("universe_name", "default"),
                "intraday_quality_score": ctx.get("intraday_quality_score"),
                "intraday_status":        ctx.get("intraday_status"),
                "tick_bidask_readiness":  ctx.get("tick_bidask_readiness", False),
                "rule_governance_summary":    ctx.get("rule_governance_summary"),
                "rules_needing_review":       ctx.get("rules_needing_review"),
                "experimental_rule_count":    ctx.get("experimental_rule_count"),
                "high_confidence_rule_count": ctx.get("high_confidence_rule_count"),
                # v0.4.2 ML Feature Store
                "ml_feature_count":           ctx.get("ml_feature_count"),
                "ml_dataset_status":          ctx.get("ml_dataset_status"),
                "ml_leakage_status":          ctx.get("ml_leakage_status"),
                "ml_feature_quality_score":   ctx.get("ml_feature_quality_score"),
                # v0.4.3 Model Monitoring
                "model_monitoring_status":    ctx.get("model_monitoring_status"),
                "prediction_count":           ctx.get("prediction_count"),
                "drift_status":               ctx.get("drift_status"),
                "degradation_status":         ctx.get("degradation_status"),
                # v0.4.4 Intraday Replay Cockpit
                "intraday_replay_session_count":  ctx.get("intraday_replay_session_count"),
                "intraday_replay_training_score": ctx.get("intraday_replay_training_score"),
                "intraday_replay_event_count":    ctx.get("intraday_replay_event_count"),
                # v0.4.1.1 Strategy Knowledge Ingestion
                "strategy_knowledge_items_count":   ctx.get("strategy_knowledge_items_count"),
                "strategy_rule_candidates_count":   ctx.get("strategy_rule_candidates_count"),
                "strategy_avoid_conditions_count":  ctx.get("strategy_avoid_conditions_count"),
                "strategy_risk_conditions_count":   ctx.get("strategy_risk_conditions_count"),
                # v0.4.2.1 ML Knowledge Integration
                "ml_knowledge_features_count":   ctx.get("ml_knowledge_features_count"),
                "ml_knowledge_model_ready":      ctx.get("ml_knowledge_model_ready"),
                "ml_knowledge_auto_enabled":     ctx.get("ml_knowledge_auto_enabled", 0),
                "ml_knowledge_leakage_findings": ctx.get("ml_knowledge_leakage_findings"),
                "ml_knowledge_critical_leakage": ctx.get("ml_knowledge_critical_leakage"),
                # v0.4.5 Notification Center
                "notification_total":    ctx.get("notification_total"),
                "notification_unread":   ctx.get("notification_unread"),
                "notification_critical": ctx.get("notification_critical"),
                "notification_external_enabled": False,
                # v0.4.6 Portfolio Journal
                "journal_entries_count":        ctx.get("journal_entries_count"),
                "journal_review_required_count": ctx.get("journal_review_required_count"),
                "journal_latest_entry":         ctx.get("journal_latest_entry"),
                "journal_most_common_mistake":  ctx.get("journal_most_common_mistake"),
                # v0.4.7 Research Review Dashboard
                **_extract_research_review_fields(ctx),
                # v0.4.8 Research Assistant / Coach
                **_extract_research_coach_fields(ctx),
                # v0.4.9 Research Workflow Automation
                **_extract_research_workflow_fields(ctx),
                # v0.5.0 Research OS Planning
                **_extract_research_os_fields(ctx),
                # v0.5.1 CLI UX
                **_extract_cli_ux_fields(ctx),
                # v0.5.2 GUI Navigation
                **_extract_gui_navigation_fields(ctx),
                # v0.5.3 Regression Suite Consolidation
                "regression_latest_suite":     ctx.get("regression_consolidation", {}).get("suite", ""),
                "regression_total_tests":      ctx.get("regression_consolidation", {}).get("total", 0),
                "regression_failed_count":     ctx.get("regression_consolidation", {}).get("failed", 0),
                "regression_warning_count":    ctx.get("regression_consolidation", {}).get("warnings", 0),
                "regression_coverage_score":   ctx.get("regression_consolidation", {}).get("coverage_score", 0),
                # v0.5.4 Report Pack Consolidation
                "report_pack_latest_type":     ctx.get("report_pack", {}).get("pack_type", ""),
                "report_pack_items_total":     ctx.get("report_pack", {}).get("ready_count", 0),
                "report_pack_missing_count":   ctx.get("report_pack", {}).get("missing_count", 0),
                "report_pack_health_score":    ctx.get("report_pack", {}).get("health_score", 0.0),
                "report_pack_index_path":      ctx.get("report_pack", {}).get("index_path", ""),
                # v0.5.5 Data / Feature Store Stabilization
                "data_stabilization_status":   ctx.get("data_stabilization", {}).get("overall_status", ""),
                "feature_readiness_score":     ctx.get("data_stabilization", {}).get("readiness_score", 0.0),
                "feature_store_health_score":  ctx.get("data_stabilization", {}).get("health_score", 0.0),
                "leakage_warning_count":       ctx.get("data_stabilization", {}).get("leakage_warnings", 0),
                "data_lineage_records":        ctx.get("data_stabilization", {}).get("datasets_checked", 0),
                # v0.5.6 TW Replay Training Cockpit
                "replay_training_score":       ctx.get("replay_training", {}).get("latest_score", 0.0),
                "replay_training_mistakes":    ctx.get("replay_training", {}).get("mistakes_count", 0),
                "replay_training_drills":      ctx.get("replay_training", {}).get("drills_count", 0),
                "replay_training_report_path": ctx.get("replay_training_report_path", ""),
            }

            path = os.path.join(output_dir, "manifest.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            logger.info("manifest.json written → %s", path)
            return path
        except Exception as exc:
            logger.error("AutoReportIndexBuilder: manifest.json failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _rel(self, path: str, output_dir: Optional[str] = None) -> str:
        """Return a path relative to the project base (for readability in links)."""
        if not path:
            return ""
        try:
            return os.path.relpath(path, _BASE_DIR).replace("\\", "/")
        except ValueError:
            return path


# ---------------------------------------------------------------------------
# Module-level helper
# ---------------------------------------------------------------------------

def _extract_reliability_fields(ctx: dict) -> dict:
    """Extract provider reliability summary fields for manifest.json (v0.3.24)."""
    rel = ctx.get("provider_reliability_summary", {})
    if not rel:
        return {}
    weak = rel.get("weak_datasets", [])
    fallback_used = rel.get("local_fallback_count", 0) > 0
    return {
        "provider_reliability_score":  rel.get("overall_reliability_score"),
        "dataset_confidence_score":    rel.get("overall_dataset_confidence"),
        "weak_datasets":               weak,
        "fallback_used":               fallback_used,
        "mock_fallback_count":         rel.get("mock_fallback_count", 0),
        "production_blocked":          True,
        "read_only":                   True,
        "no_real_orders":              True,
    }


def _extract_quality_gate_fields(ctx: dict) -> dict:
    """Extract data quality gate summary fields for manifest.json."""
    gate = ctx.get("data_quality_gate_result", {})
    if not gate:
        return {}
    return {
        "production_readiness_score": gate.get("production_readiness_score"),
        "backtest_readiness_score":   gate.get("backtest_readiness_score"),
        "production_classification":  gate.get("production_classification"),
        "backtest_classification":    gate.get("backtest_classification"),
        "production_blocked":         gate.get("production_blocked", True),
        "real_order_ready":           gate.get("real_order_ready", False),
        "gates": {
            k: v for k, v in gate.get("gates", {}).items()
            if not k.startswith("_")
        },
    }


def _extract_research_review_fields(ctx: dict) -> dict:
    """Extract Research Review Dashboard summary fields for manifest.json (v0.4.7)."""
    return {
        "research_review_score":        ctx.get("research_review_score", "UNKNOWN"),
        "research_review_open_items":   ctx.get("research_review_open_items", 0),
        "research_review_critical_count": ctx.get("research_review_critical_count", 0),
        "research_review_action_items": ctx.get("research_review_action_items", 0),
        "research_review_top_mistake":  ctx.get("research_review_top_mistake", ""),
    }


def _extract_research_coach_fields(ctx: dict) -> dict:
    """Extract Research Assistant / Coach summary fields for manifest.json (v0.4.8)."""
    return {
        "research_coach_recommendations": ctx.get("research_coach_recommendations", 0),
        "research_coach_p0":              ctx.get("research_coach_p0", 0),
        "research_coach_p1":              ctx.get("research_coach_p1", 0),
        "research_coach_replay_tasks":    ctx.get("research_coach_replay_tasks", 0),
        "research_coach_rule_reviews":    ctx.get("research_coach_rule_reviews", 0),
        "research_coach_data_repairs":    ctx.get("research_coach_data_repairs", 0),
    }


def _extract_research_workflow_fields(ctx: dict) -> dict:
    """Extract Research Workflow Automation summary fields for manifest.json (v0.4.9)."""
    return {
        "research_workflow_latest_id":      ctx.get("research_workflow_latest_id", ""),
        "research_workflow_tasks_total":    ctx.get("research_workflow_tasks_total", 0),
        "research_workflow_failed_count":   ctx.get("research_workflow_failed_count", 0),
        "research_workflow_blocked_count":  ctx.get("research_workflow_blocked_count", 0),
        "research_workflow_package_path":   ctx.get("research_workflow_package_path", ""),
    }


def _extract_research_os_fields(ctx: dict) -> dict:
    """Extract Research OS Planning summary fields for manifest.json (v0.5.0)."""
    return {
        "research_os_total_modules":  ctx.get("research_os_total_modules",  0),
        "research_os_total_commands": ctx.get("research_os_total_commands", 0),
        "research_os_total_tabs":     ctx.get("research_os_total_tabs",     0),
        "research_os_mature_count":   ctx.get("research_os_mature_count",   0),
        "research_os_safety_score":   ctx.get("research_os_safety_score",   "N/A"),
    }


def _extract_cli_ux_fields(ctx: dict) -> dict:
    """Extract CLI UX summary fields for manifest.json (v0.5.1)."""
    return {
        "cli_commands_count":  ctx.get("cli_commands_count",  0),
        "cli_aliases_count":   ctx.get("cli_aliases_count",   0),
        "cli_alias_conflicts": ctx.get("cli_alias_conflicts", 0),
        "cli_safety_status":   ctx.get("cli_safety_status",   "N/A"),
    }


def _extract_gui_navigation_fields(ctx: dict) -> dict:
    """Extract GUI Navigation summary fields for manifest.json (v0.5.2)."""
    return {
        "gui_tabs_count":               ctx.get("gui_tabs_count",              0),
        "gui_groups_count":             ctx.get("gui_groups_count",            0),
        "gui_navigation_safety_status": ctx.get("gui_navigation_safety_status", "N/A"),
        "gui_navigation_report":        ctx.get("gui_navigation_report",        ""),
    }
