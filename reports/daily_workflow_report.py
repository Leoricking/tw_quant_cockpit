"""
reports/daily_workflow_report.py - Daily Workflow Report Builder (v0.3.21).

Generates reports/daily_workflow/YYYY-MM-DD/workflow_summary.md

7-section Markdown report covering data quality, research results, outputs,
next actions, and safety declarations.

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DailyWorkflowReportBuilder:
    """
    Builds workflow_summary.md from DailyResearchWorkflow results.

    Parameters
    ----------
    workflow_result : dict from DailyResearchWorkflow._build_result()
    context         : cross-step context dict from the workflow
    report_date     : YYYY-MM-DD string (defaults to today)
    """

    VERSION = "v0.3.21"

    def __init__(
        self,
        workflow_result: dict,
        context: Optional[dict] = None,
        report_date: Optional[str] = None,
    ):
        self.result      = workflow_result
        self.context     = context or {}
        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def build(self, output_dir: Optional[str] = None) -> str:
        """Write workflow_summary.md and return its path."""
        out_dir = output_dir or os.path.join(
            _BASE_DIR, "reports", "daily_workflow",
            self.report_date,
        )
        os.makedirs(out_dir, exist_ok=True)

        content = self._render()
        path    = os.path.join(out_dir, "workflow_summary.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("DailyWorkflowReport written → %s", path)
        return path

    def render(self) -> str:
        return self._render()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self) -> str:
        sections = [
            self._section_header(),
            self._section_overview(),
            self._section_step_results(),
            self._section_data_quality(),
            self._section_research_summary(),
            self._section_generated_outputs(),
            self._section_next_actions(),
            self._section_safety(),
        ]
        return "\n\n".join(sections) + "\n"

    # ---- Section 1: Header -----------------------------------------------

    def _section_header(self) -> str:
        r       = self.result
        mode    = r.get("mode", "unknown").upper()
        profile = r.get("profile", "standard")
        status  = r.get("overall_status", "UNKNOWN")
        started = (r.get("started_at", "") or "")[:19]
        return (
            f"# TW Quant Cockpit — Daily Research Workflow Summary\n"
            f"\n"
            f"> **{self.VERSION}** | {self.report_date} | Mode: {mode} | "
            f"Profile: {profile} | Status: **{status}**\n"
            f">\n"
            f"> [!] Research Only. Read Only. No Real Orders. "
            f"Production Trading: **BLOCKED**.\n"
            f"\n"
            f"---"
        )

    # ---- Section 2: 總覽 --------------------------------------------------

    def _section_overview(self) -> str:
        r        = self.result
        mode     = r.get("mode", "").upper()
        profile  = r.get("profile", "")
        started  = (r.get("started_at", "") or "")[:19]
        finished = (r.get("finished_at", "") or "")[:19]
        dur      = r.get("duration_seconds", 0.0)
        status   = r.get("overall_status", "UNKNOWN")
        ok_n     = len(r.get("ok_steps", []))
        fail_n   = len(r.get("failed_steps", []))
        warn_n   = r.get("warning_count", 0)

        lines = [
            "## 一、總覽",
            "",
            "| 項目 | 值 |",
            "|------|---|",
            f"| Mode | {mode} |",
            f"| Profile | {profile} |",
            f"| Started | {started} |",
            f"| Finished | {finished} |",
            f"| Duration | {dur:.1f}s |",
            f"| Overall Status | **{status}** |",
            f"| OK Steps | {ok_n} |",
            f"| Failed Steps | {fail_n} |",
            f"| Warnings | {warn_n} |",
            f"| Read Only | True |",
            f"| No Real Orders | True |",
            f"| Production Trading | **BLOCKED** |",
        ]
        return "\n".join(lines)

    # ---- Section 3: Step Results -----------------------------------------

    def _section_step_results(self) -> str:
        steps = self.result.get("steps", [])
        lines = [
            "## 二、Step Results",
            "",
            "| Step | Status | Duration | Output | Warnings | Errors |",
            "|------|--------|----------|--------|----------|--------|",
        ]
        for s in steps:
            name     = s.get("step_name", "")
            status   = s.get("status", "")
            dur      = s.get("duration_seconds", 0.0)
            out      = "; ".join(s.get("outputs", []))[:60] or "—"
            warn_n   = len(s.get("warnings", []))
            err_n    = len(s.get("errors", []))
            lines.append(f"| {name} | {status} | {dur:.1f}s | {out} | {warn_n} | {err_n} |")

        if not steps:
            lines.append("| — | No steps executed | | | | |")
        return "\n".join(lines)

    # ---- Section 4: Data Quality -----------------------------------------

    def _section_data_quality(self) -> str:
        qg  = self.result.get("quality_gate_summary", {})
        ctx_qg = self.context.get("quality_gate", {})
        prod  = qg.get("production_readiness_score") or ctx_qg.get("production_readiness_score", "N/A")
        btest = qg.get("backtest_readiness_score")   or ctx_qg.get("backtest_readiness_score",   "N/A")
        p_cls = qg.get("production_classification")  or ctx_qg.get("production_classification",  "N/A")
        gates = qg.get("gates") or ctx_qg.get("gates", {})

        # Freshness
        freshness = self.context.get("freshness", {})
        fresh_dsets = freshness.get("datasets", {})

        # Mock contamination
        scores  = ctx_qg.get("scores", {})
        mock_sc = scores.get("mock_contamination_score", "N/A")

        lines = [
            "## 三、Data Quality Summary",
            "",
            "| 指標 | 值 |",
            "|------|----|",
        ]
        prod_str  = f"{prod:.1f}" if isinstance(prod, float) else str(prod)
        btest_str = f"{btest:.1f}" if isinstance(btest, float) else str(btest)
        mock_str  = f"{mock_sc:.1f}" if isinstance(mock_sc, float) else str(mock_sc)

        lines += [
            f"| Production Readiness Score | **{prod_str}** ({p_cls}) |",
            f"| Backtest Readiness Score   | **{btest_str}** |",
            f"| Production BLOCKED         | **True** |",
            f"| Mock Contamination Score   | {mock_str} |",
        ]

        if fresh_dsets:
            lines += ["", "**Freshness:**", ""]
            for ds, info in fresh_dsets.items():
                if ds == "intraday":
                    continue
                status = info.get("status", "?") if isinstance(info, dict) else str(info)
                lines.append(f"- {ds}: {status}")

        if gates:
            lines += ["", "**Gate Decisions:**", ""]
            _labels = {
                "BACKTEST_READY": "Backtest Ready",
                "PAPER_TRADING_READY": "Paper Trading Ready",
                "PRODUCTION_BLOCKED": "Production Blocked",
                "INTRADAY_READY": "Intraday Ready",
                "REAL_ORDER_READY": "Real Order Ready",
            }
            for key, label in _labels.items():
                val = gates.get(key)
                status_str = "YES" if val is True else "NO" if val is False else str(val)
                lines.append(f"- {label}: {status_str}")

        return "\n".join(lines)

    # ---- Section 5: Research Summary -------------------------------------

    def _section_research_summary(self) -> str:
        sq  = self.context.get("signal_quality", {})
        pt  = self.context.get("portfolio", {})
        rw  = self.context.get("rule_weight", {})

        # Signal quality
        n_boost  = sq.get("boost_count",  sq.get("n_boost",  0))
        n_reduce = sq.get("reduce_count", sq.get("n_reduce", 0))
        n_total  = sq.get("n_signals", 0)

        # Portfolio
        metrics     = pt.get("metrics", {}) if isinstance(pt, dict) else {}
        total_ret   = metrics.get("total_return")
        best_scen   = pt.get("scenario", "balanced")
        ret_str     = f"{total_ret:+.2%}" if total_ret is not None else "N/A"

        # Rule weight
        best_cfg = rw.get("best_config")
        rw_best  = best_cfg.name if best_cfg else "N/A"

        lines = [
            "## 四、Research Summary",
            "",
            f"- Signal Quality: {n_total} signals evaluated | "
            f"BOOST={n_boost} | REDUCE={n_reduce}",
            f"- Portfolio ({best_scen}): return={ret_str}",
            f"- Rule Weight Best Config: {rw_best}",
            "",
            "> [!] Do not chase signals. Do not trade automatically. Research reference only.",
        ]
        return "\n".join(lines)

    # ---- Section 6: Generated Outputs ------------------------------------

    def _section_generated_outputs(self) -> str:
        ar = self.context.get("auto_report", {})
        ar_dir   = ar.get("output_dir", self.result.get("auto_report_dir", ""))
        ar_count = ar.get("generated", [])
        ar_n     = len(ar_count) if isinstance(ar_count, list) else self.result.get("auto_report_count", 0)

        # Quality gate report path
        qg_report = ""
        try:
            from datetime import datetime as _dt
            qg_report_dir = os.path.join(_BASE_DIR, "reports")
            qg_candidate  = os.path.join(
                qg_report_dir,
                f"data_quality_gate_report_{self.report_date}.md"
            )
            if os.path.exists(qg_candidate):
                qg_report = qg_candidate
        except Exception:
            pass

        # Step-level report paths
        step_reports = []
        for s in self.result.get("steps", []):
            for key in ("signal_quality_report", "rule_weight_report",
                        "auto_report_dir", "auto_report_count"):
                val = s.get(key, "")
                if val and isinstance(val, str):
                    step_reports.append(f"{s.get('step_name', '')}: {val}")

        lines = [
            "## 五、Generated Outputs",
            "",
        ]
        if ar_dir:
            lines.append(f"- Auto Report folder: `{ar_dir}` ({ar_n} reports)")
        if qg_report:
            lines.append(f"- Data Quality Gate Report: `{qg_report}`")
        for r in step_reports[:6]:
            lines.append(f"- {r}")
        if not ar_dir and not qg_report and not step_reports:
            lines.append("*No reports generated in this run.*")
        return "\n".join(lines)

    # ---- Section 7: Next Actions -----------------------------------------

    def _section_next_actions(self) -> str:
        failed = self.result.get("failed_steps", [])
        gates  = self.result.get("quality_gate_summary", {}).get("gates", {})

        lines = ["## 六、Next Actions", ""]

        if gates.get("BACKTEST_READY") is False:
            lines.append("- Fix data quality issues before running backtests")
        if gates.get("INTRADAY_READY") is False:
            lines.append("- Import intraday data if needed (`python main.py import-intraday`)")
        if failed:
            lines.append(f"- Review failed steps: {', '.join(failed)}")
        lines += [
            "- Open cockpit to review research: `python main.py open-cockpit --mode real`",
            "- Review auto report: see Generated Outputs above",
            "",
            "> **Do NOT trade automatically. Do NOT auto-apply weights.**",
            "> Research Only. Production Trading: BLOCKED.",
        ]
        return "\n".join(lines)

    # ---- Section 8: Safety -----------------------------------------------

    def _section_safety(self) -> str:
        return (
            "## 七、安全聲明\n"
            "\n"
            "- Research Only\n"
            "- Read Only\n"
            "- No Real Orders\n"
            "- No Auto Trading\n"
            "- No Automatic Weight Application\n"
            "- Does NOT call broker.submit_order\n"
            "- Does NOT connect Shioaji or Mega in trading mode\n"
            "- Production Trading: **BLOCKED** (always True in v1)\n"
            "- REAL_ORDER_READY: **False** (never allowed)\n"
            "\n"
            f"_Generated by TW Quant Cockpit {self.VERSION} — {self.report_date}_"
        )
