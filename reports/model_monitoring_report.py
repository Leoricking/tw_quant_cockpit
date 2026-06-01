"""
reports/model_monitoring_report.py — Model Monitoring Report Builder (v0.4.3).

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
import os
from datetime import date

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_FLAGS = {
    "read_only":            True,
    "no_real_orders":       True,
    "production_blocked":   True,
    "real_order_ready":     False,
    "monitoring_only":      True,
    "research_only":        True,
    "live_prediction":      False,
    "auto_trading":         False,
}


class ModelMonitoringReportBuilder:
    """
    Build a Markdown monitoring report for v0.4.3.

    Output: reports/model_monitoring_report_YYYY-MM-DD.md
    [!] Monitoring Only / No Real Orders / Production Trading BLOCKED.
    """

    VERSION = "v0.4.3"

    read_only      = True
    no_real_orders = True

    def __init__(self, report_dir: str = "reports", mode: str = "real"):
        self._report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(_BASE_DIR, report_dir)
        )
        self._mode = mode
        os.makedirs(self._report_dir, exist_ok=True)

    def build(
        self,
        monitoring_summary:  dict = None,
        registry_summary:    dict = None,
        prediction_summary:  dict = None,
        hit_miss_result:     dict = None,
        drift_result:        dict = None,
        degradation_result:  dict = None,
        rule_vs_ml_result:   dict = None,
    ) -> str:
        """Build and save report. Returns file path."""
        monitoring_summary  = monitoring_summary  or {}
        registry_summary    = registry_summary    or {}
        prediction_summary  = prediction_summary  or {}
        hit_miss_result     = hit_miss_result     or {}
        drift_result        = drift_result        or {}
        degradation_result  = degradation_result  or {}
        rule_vs_ml_result   = rule_vs_ml_result   or {}

        today    = date.today().isoformat()
        filename = f"model_monitoring_report_{today}.md"
        out_path = os.path.join(self._report_dir, filename)

        lines = []
        _h = lines.append

        # ── Header ────────────────────────────────────────────────────
        _h(f"# Model Monitoring Report — {today}")
        _h(f"")
        _h(f"**Version:** {self.VERSION}  |  **Mode:** {self._mode}  |  "
           f"**Status:** Monitoring Only / No Real Orders / Production Trading BLOCKED")
        _h(f"")
        _h(f"> [!] All outputs are research-only monitoring data.  ")
        _h(f"> [!] No live prediction. No auto-trading. No broker connections.")
        _h(f"")
        _h("---")
        _h("")

        # ── 一、總覽 ───────────────────────────────────────────────────
        _h("## 一、總覽")
        _h("")
        _h(f"| 項目 | 值 |")
        _h(f"|---|---|")
        _h(f"| Mode | `{self._mode}` |")
        _h(f"| Research Only | `{_SAFETY_FLAGS['research_only']}` |")
        _h(f"| Monitoring Only | `{_SAFETY_FLAGS['monitoring_only']}` |")
        _h(f"| No Real Orders | `{_SAFETY_FLAGS['no_real_orders']}` |")
        _h(f"| Production Blocked | `{_SAFETY_FLAGS['production_blocked']}` |")
        _h(f"| Model Count | `{monitoring_summary.get('model_count', 0)}` |")
        _h(f"| Prediction Count | `{monitoring_summary.get('prediction_count', 0)}` |")
        _h(f"| Reviewed Count | `{monitoring_summary.get('reviewed_count', 0)}` |")
        hit_rate = monitoring_summary.get("hit_rate")
        hit_rate_str = f"{hit_rate:.1%}" if hit_rate is not None else "N/A"
        _h(f"| Hit Rate | `{hit_rate_str}` |")
        _h(f"| Drift Status | `{monitoring_summary.get('drift_status', 'N/A')}` |")
        _h(f"| Degradation Status | `{monitoring_summary.get('degradation_status', 'N/A')}` |")
        _h(f"| Monitoring Status | Monitoring Only — No Real Orders |")
        _h("")

        warnings = monitoring_summary.get("warnings", [])
        if warnings:
            _h("**Warnings:**")
            for w in warnings:
                _h(f"- {w}")
            _h("")

        next_actions = monitoring_summary.get("next_actions", [])
        if next_actions:
            _h("**Next Actions:**")
            for a in next_actions:
                _h(f"- {a}")
            _h("")

        _h("---")
        _h("")

        # ── 二、Model Registry ─────────────────────────────────────────
        _h("## 二、Model Registry")
        _h("")
        model_count      = registry_summary.get("model_count", 0)
        status_breakdown = registry_summary.get("status_breakdown", {})
        _h(f"**Registered Models:** {model_count}")
        _h("")
        if status_breakdown:
            _h("**Status Breakdown:**")
            _h("")
            _h("| Monitoring Status | Count |")
            _h("|---|---|")
            for status, cnt in status_breakdown.items():
                _h(f"| {status} | {cnt} |")
            _h("")

        # Model table from registry details
        detail = monitoring_summary.get("details", {})
        reg_models = []
        try:
            from monitoring.model_registry import ModelRegistry
            reg = ModelRegistry()
            reg_models = reg.list_models()
        except Exception:
            pass

        if reg_models:
            _h("| Model ID | Name | Type | Target | Feature Snapshot | Leakage Status | Monitoring Status |")
            _h("|---|---|---|---|---|---|---|")
            for m in reg_models[:50]:
                _h(
                    f"| {m.get('model_id','')} "
                    f"| {m.get('model_name','')} "
                    f"| {m.get('model_type','')} "
                    f"| {m.get('target_label','')} "
                    f"| {m.get('feature_snapshot_id','')} "
                    f"| {m.get('leakage_status','')} "
                    f"| {m.get('monitoring_status','')} |"
                )
            _h("")
        else:
            _h("_No models registered yet._")
            _h("")

        _h("---")
        _h("")

        # ── 三、Prediction Tracking ────────────────────────────────────
        _h("## 三、Prediction Tracking")
        _h("")
        _h(f"| 項目 | 值 |")
        _h(f"|---|---|")
        _h(f"| Total Predictions | `{prediction_summary.get('total_predictions', 0)}` |")
        _h(f"| Reviewed Count | `{prediction_summary.get('reviewed_count', 0)}` |")
        dr = prediction_summary.get("date_range", {})
        _h(f"| Date Range | `{dr.get('min','—')} – {dr.get('max','—')}` |")
        _h("")

        sources = prediction_summary.get("sources", {})
        if sources:
            _h("**By Source:**")
            _h("")
            _h("| Source | Count |")
            _h("|---|---|")
            for src, cnt in sources.items():
                _h(f"| {src} | {cnt} |")
            _h("")

        horizons = prediction_summary.get("horizons", {})
        if horizons:
            _h("**By Horizon:**")
            _h("")
            _h("| Horizon | Count |")
            _h("|---|---|")
            for hz, cnt in sorted(horizons.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
                _h(f"| {hz} days | {cnt} |")
            _h("")

        _h("---")
        _h("")

        # ── 四、Hit / Miss Review ──────────────────────────────────────
        _h("## 四、Hit / Miss Review")
        _h("")
        hm_status = hit_miss_result.get("status", "N/A")
        _h(f"**Status:** `{hm_status}`")
        _h("")

        _h("| 項目 | 值 |")
        _h("|---|---|")
        hr_val = hit_miss_result.get("hit_rate")
        hr_str = f"{hr_val:.1%}" if hr_val is not None else "N/A"
        _h(f"| Hit Rate | `{hr_str}` |")
        avg_ret = hit_miss_result.get("avg_actual_return")
        avg_ret_str = f"{avg_ret:.4f}" if avg_ret is not None else "N/A"
        _h(f"| Avg Actual Return | `{avg_ret_str}` |")
        prec = hit_miss_result.get("precision")
        prec_str = f"{prec:.3f}" if prec is not None else "N/A"
        _h(f"| Precision | `{prec_str}` |")
        rec = hit_miss_result.get("recall")
        rec_str = f"{rec:.3f}" if rec is not None else "N/A"
        _h(f"| Recall | `{rec_str}` |")
        f1 = hit_miss_result.get("f1")
        f1_str = f"{f1:.3f}" if f1 is not None else "N/A"
        _h(f"| F1 | `{f1_str}` |")
        _h(f"| Total Predictions | `{hit_miss_result.get('total_predictions', 0)}` |")
        _h(f"| Reviewed | `{hit_miss_result.get('reviewed_predictions', 0)}` |")
        _h("")

        # by_model
        by_model = hit_miss_result.get("by_model", {})
        if by_model:
            _h("**By Model:**")
            _h("")
            _h("| Model ID | Hit Rate | Hits | Total |")
            _h("|---|---|---|---|")
            for mid, metrics in list(by_model.items())[:20]:
                hr2 = metrics.get("hit_rate")
                hr2s = f"{hr2:.1%}" if hr2 is not None else "N/A"
                _h(f"| {mid} | {hr2s} | {metrics.get('hits', 0)} | {metrics.get('total', 0)} |")
            _h("")

        # by_rule
        by_rule = hit_miss_result.get("by_rule", {})
        if by_rule:
            _h("**By Rule:**")
            _h("")
            _h("| Rule ID | Hit Rate | Hits | Total |")
            _h("|---|---|---|---|")
            for rid, metrics in list(by_rule.items())[:20]:
                hr2 = metrics.get("hit_rate")
                hr2s = f"{hr2:.1%}" if hr2 is not None else "N/A"
                _h(f"| {rid} | {hr2s} | {metrics.get('hits', 0)} | {metrics.get('total', 0)} |")
            _h("")

        # by_source
        by_source = hit_miss_result.get("by_source", {})
        if by_source:
            _h("**By Source:**")
            _h("")
            _h("| Source | Hit Rate | Hits | Total |")
            _h("|---|---|---|---|")
            for src, metrics in by_source.items():
                hr2 = metrics.get("hit_rate")
                hr2s = f"{hr2:.1%}" if hr2 is not None else "N/A"
                _h(f"| {src} | {hr2s} | {metrics.get('hits', 0)} | {metrics.get('total', 0)} |")
            _h("")

        for w in hit_miss_result.get("warnings", []):
            _h(f"> ⚠ {w}")
        _h("")

        _h("---")
        _h("")

        # ── 五、Drift Detection ────────────────────────────────────────
        _h("## 五、Drift Detection")
        _h("")
        drift_status = drift_result.get("status", "N/A")
        _h(f"**Overall Drift Status:** `{drift_status}`")
        _h("")

        # Feature drift table
        fd = drift_result.get("feature_drift", {})
        pf = fd.get("per_feature", {}) if fd else {}
        if pf:
            _h("**Feature Distribution Drift:**")
            _h("")
            _h("| Feature | Baseline Mean | Current Mean | Mean Change | Status |")
            _h("|---|---|---|---|---|")
            for col, d in list(pf.items())[:30]:
                chg  = d.get("mean_change", 0) or 0
                chgs = f"{chg:.1%}"
                st   = "CRITICAL" if chg >= 0.5 else ("WARNING" if chg >= 0.25 else ("WATCH" if chg >= 0.10 else "STABLE"))
                _h(
                    f"| {col} | {d.get('baseline_mean', 0):.4f} "
                    f"| {d.get('current_mean', 0):.4f} | {chgs} | {st} |"
                )
            _h("")

        # Missing drift
        md = drift_result.get("missing_drift", {})
        pm = md.get("per_feature", {}) if md else {}
        if pm:
            _h("**Missing Ratio Drift:**")
            _h("")
            _h("| Feature | Baseline Missing% | Current Missing% | Change |")
            _h("|---|---|---|---|")
            for col, d in list(pm.items())[:20]:
                _h(
                    f"| {col} | {d.get('baseline_missing_ratio', 0):.1%} "
                    f"| {d.get('current_missing_ratio', 0):.1%} "
                    f"| {d.get('change', 0):.1%} |"
                )
            _h("")

        # Label drift
        ld = drift_result.get("label_drift", {})
        if ld and ld.get("label_col"):
            _h("**Label Distribution Drift:**")
            _h("")
            _h(f"| Label Column | Drift Value | Max Class Change |")
            _h("|---|---|---|")
            dv = ld.get("drift_value", 0) or 0
            mc = ld.get("max_class_change", 0) or 0
            _h(f"| {ld.get('label_col', 'N/A')} | {dv:.1%} | {mc:.1%} |")
            _h("")

        # Score drift
        sd = drift_result.get("score_drift", {})
        if sd and sd.get("drift_value") is not None:
            _h("**Prediction Score Drift:**")
            _h("")
            _h(f"| Metric | Value |")
            _h("|---|---|")
            _h(f"| Baseline Mean Confidence | `{sd.get('baseline_mean_confidence', 0):.4f}` |")
            _h(f"| Current Mean Confidence | `{sd.get('current_mean_confidence', 0):.4f}` |")
            _h(f"| Drift Value | `{sd.get('drift_value', 0):.1%}` |")
            _h("")

        for w in drift_result.get("warnings", []):
            _h(f"> ⚠ {w}")
        _h("")

        _h("---")
        _h("")

        # ── 六、Signal Degradation ─────────────────────────────────────
        _h("## 六、Signal Degradation")
        _h("")
        deg_status = degradation_result.get("status", "N/A")
        _h(f"**Overall Degradation Status:** `{deg_status}`")
        _h("")

        # Rule degradation
        rd = degradation_result.get("rule_degradation", {})
        if rd:
            _h(f"**Rule Degradation:** `{rd.get('status', 'N/A')}` "
               f"({rd.get('total_rules', 0)} rules, "
               f"{len(rd.get('degraded_rules', []))} degraded)")
            _h("")
            degs = rd.get("degraded_rules", [])
            if degs:
                _h("| Rule ID | Confidence | Status |")
                _h("|---|---|---|")
                for r in degs[:20]:
                    _h(f"| {r.get('rule_id', '?')} | {r.get('confidence', 0):.2f} | LOW |")
                _h("")

        # Signal quality degradation
        sqd = degradation_result.get("signal_quality_degradation", {})
        if sqd:
            _h(f"**Signal Quality:** `{sqd.get('status', 'N/A')}` "
               f"(boost={sqd.get('boost_count', 0)}, "
               f"reduce={sqd.get('reduce_count', 0)}, "
               f"disable={sqd.get('disable_count', 0)})")
            _h("")

        # Portfolio degradation
        pd2 = degradation_result.get("portfolio_degradation", {})
        if pd2 and pd2.get("status"):
            _h(f"**Portfolio:** `{pd2.get('status', 'N/A')}` "
               f"(baseline={pd2.get('baseline_avg', 0):.4f}, "
               f"recent={pd2.get('recent_avg', 0):.4f}, "
               f"change={pd2.get('relative_change', 0):.1%})")
            _h("")

        for w in degradation_result.get("warnings", []):
            _h(f"> ⚠ {w}")
        _h("")

        _h("---")
        _h("")

        # ── 七、Rule vs ML Comparison ──────────────────────────────────
        _h("## 七、Rule vs ML Comparison")
        _h("")
        recommendation = rule_vs_ml_result.get("recommendation", "N/A")
        ml_available   = rule_vs_ml_result.get("ml_available", False)
        _h(f"**Recommendation:** `{recommendation}`")
        _h(f"**ML Available:** `{ml_available}`")
        _h("")

        if not ml_available:
            _h("> ML predictions not available — only rule-based signals analyzed.")
            _h("> Rule vs ML comparison requires logged ML predictions in PredictionLog.")
            _h("")
        else:
            agr = rule_vs_ml_result.get("agreement_rate")
            agr_str = f"{agr:.1%}" if agr is not None else "N/A"
            _h(f"| 項目 | 值 |")
            _h(f"|---|---|")
            _h(f"| Agreement Rate | `{agr_str}` |")
            _h(f"| Rule Hit Rate | `{rule_vs_ml_result.get('rule_hit_rate', 'N/A')}` |")
            _h(f"| ML Hit Rate | `{rule_vs_ml_result.get('ml_hit_rate', 'N/A')}` |")
            _h(f"| Both Hits | `{rule_vs_ml_result.get('both_hits', 0)}` |")
            _h(f"| Both Misses | `{rule_vs_ml_result.get('both_misses', 0)}` |")
            _h(f"| Rule Only Hits | `{rule_vs_ml_result.get('rule_only_hits', 0)}` |")
            _h(f"| ML Only Hits | `{rule_vs_ml_result.get('ml_only_hits', 0)}` |")
            _h("")

            # Disagreement symbols
            dis = rule_vs_ml_result.get("disagreement_symbols", [])
            if dis:
                _h(f"**Disagreement Symbols ({len(dis)}):** " + ", ".join(str(s) for s in dis[:20]))
                _h("")

        for w in rule_vs_ml_result.get("warnings", []):
            _h(f"> ⚠ {w}")
        _h("")

        _h("---")
        _h("")

        # ── 八、安全聲明 ───────────────────────────────────────────────
        _h("## 八、安全聲明")
        _h("")
        _h("| 安全旗標 | 值 |")
        _h("|---|---|")
        for flag, val in _SAFETY_FLAGS.items():
            _h(f"| {flag} | `{val}` |")
        _h("")
        _h("> **[!] Monitoring Only / No Real Orders / Production Trading BLOCKED**")
        _h("> This report is for research monitoring purposes only.")
        _h("> No live prediction, no auto-trading, no broker connections.")
        _h("> All outputs are research-only monitoring data.")
        _h("")
        _h(f"_Generated: {today} | Version: {self.VERSION} | Mode: {self._mode}_")
        _h("")

        # Write file
        content = "\n".join(lines)
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(content)
            logger.info("ModelMonitoringReportBuilder: saved %s", out_path)
        except Exception as exc:
            logger.error("ModelMonitoringReportBuilder.build: %s", exc)

        return out_path
