"""
workflow/daily_workflow.py - Daily Research Workflow Engine (v0.3.22).

Combines update-data, run-research, and daily-workflow flows into
a single high-level engine.

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED. Does NOT auto-apply weights.
[!] Does NOT call broker.submit_order. Does NOT connect Shioaji or Mega.
"""

from __future__ import annotations

import json
import logging
import os
import traceback
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_REPORT_DIR  = os.path.join(_BASE_DIR, "reports")
_DEFAULT_RESULTS_DIR = os.path.join(_BASE_DIR, "data", "backtest_results")
_DEFAULT_IMPORT_ROOT = os.path.join(_BASE_DIR, "data", "import")
_DEFAULT_LOG_DIR     = os.path.join(_BASE_DIR, "logs", "workflow")
_DEFAULT_WORKFLOW_REPORT_DIR = os.path.join(_BASE_DIR, "reports", "daily_workflow")


class DailyResearchWorkflow:
    """
    Daily Research Workflow Engine.

    Orchestrates update-data → run-research → summary in a single run.
    All operations are read-only. No orders placed. No weights modified.

    Parameters
    ----------
    mode        : 'real' or 'mock'
    profile     : 'quick' | 'standard' | 'full' | 'gui_only'
    stocks      : optional list of symbols for stock reports
    top_n       : number of top candidates
    report_dir  : reports root folder
    results_dir : data/backtest_results folder
    import_root : data/import folder
    log_dir     : logs/workflow folder
    dry_run     : if True, skip writes in data fetch step
    """

    VERSION = "v0.3.21"

    # Hard-coded safety invariants — cannot be overridden
    read_only       = True
    no_real_orders  = True
    production_blocked = True

    def __init__(
        self,
        mode:        str = "real",
        profile:     str = "standard",
        stocks:      Optional[List[str]] = None,
        top_n:       int = 8,
        report_dir:  Optional[str] = None,
        results_dir: Optional[str] = None,
        import_root: Optional[str] = None,
        log_dir:     Optional[str] = None,
        dry_run:     bool = False,
    ):
        self.mode        = mode
        self.profile     = profile
        self.stocks      = stocks or []
        self.top_n       = top_n
        self.report_dir  = report_dir  or _DEFAULT_REPORT_DIR
        self.results_dir = results_dir or _DEFAULT_RESULTS_DIR
        self.import_root = import_root or _DEFAULT_IMPORT_ROOT
        self.log_dir     = log_dir     or _DEFAULT_LOG_DIR
        self.dry_run     = dry_run

        from workflow.workflow_profiles import WorkflowProfileRegistry
        self._profile_obj = WorkflowProfileRegistry.get(profile)

        from workflow.workflow_status import WorkflowStatus
        self._status = WorkflowStatus(
            workflow_name="daily_workflow",
            mode=self.mode,
            profile=self.profile,
        )

        self._context: dict = {}   # shared cross-step data

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def run_update_data(self) -> dict:
        """
        Run data update phase (provider health → fetch → freshness → quality gate).
        Does NOT open GUI. Does NOT run research reports.
        """
        logger.info(
            "[DailyResearchWorkflow] run_update_data [mode=%s profile=%s dry_run=%s]",
            self.mode, self.profile, self.dry_run,
        )
        self._status.start()

        for step_name in self._profile_obj.update_data_steps:
            self._run_step(step_name)

        self._status.finish()
        result = self._build_result("update_data")
        self._write_workflow_log(result)
        return result

    def run_research(self) -> dict:
        """
        Run research phase (quality gate → signal quality → portfolio → auto report).
        Does NOT open GUI. Does NOT modify weights.
        """
        logger.info(
            "[DailyResearchWorkflow] run_research [mode=%s profile=%s]",
            self.mode, self.profile,
        )
        self._status.start()

        for step_name in self._profile_obj.research_steps:
            self._run_step(step_name)

        self._status.finish()
        result = self._build_result("run_research")
        self._write_workflow_log(result)
        return result

    def run_full_workflow(self) -> dict:
        """
        Run full daily workflow: update_data + research.
        Does NOT open GUI unless explicitly called.
        """
        logger.info(
            "[DailyResearchWorkflow] run_full_workflow [mode=%s profile=%s]",
            self.mode, self.profile,
        )
        self._status.start()

        all_steps = self._profile_obj.all_steps()
        for step_name in all_steps:
            self._run_step(step_name)

        self._status.finish()
        result = self._build_result("daily_workflow")
        self._write_workflow_log(result)
        self._write_workflow_summary(result)
        return result

    def open_cockpit(self) -> dict:
        """
        Open the PySide6 cockpit GUI. (Alias for cockpit command.)
        """
        result = {
            "action":   "open_cockpit",
            "status":   "ok",
            "mode":     self.mode,
            "read_only":           self.read_only,
            "no_real_orders":      self.no_real_orders,
            "production_blocked":  self.production_blocked,
        }
        try:
            from gui.dashboard import launch
            launch(mode=self.mode)
            result["gui_launched"] = True
        except Exception as exc:
            result["status"]  = "failed"
            result["error"]   = str(exc)
            result["gui_launched"] = False
        return result

    def build_summary(self) -> dict:
        """Return workflow summary dict from current status."""
        return self._status.to_dict()

    def write_workflow_log(self) -> Optional[str]:
        """Append current status to logs/workflow/daily_workflow_runs.jsonl."""
        result = self._build_result("daily_workflow")
        return self._write_workflow_log(result)

    # ------------------------------------------------------------------
    # Step dispatcher
    # ------------------------------------------------------------------

    _STEP_HANDLERS = None   # populated lazily

    def _run_step(self, step_name: str) -> None:
        from workflow.workflow_status import WorkflowStepResult
        step = WorkflowStepResult(step_name)

        handler = getattr(self, f"_step_{step_name}", None)
        if handler is None:
            step.mark_skipped(f"No handler for step '{step_name}'")
            self._status.add_step(step)
            return

        with step:
            try:
                handler(step)
                # Auto-finalize: if handler ran without exception, set OK/PARTIAL
                # (preserve FAILED/BLOCKED if handler set them explicitly)
                if step.status not in (WorkflowStepResult.FAILED, WorkflowStepResult.BLOCKED):
                    if step.errors:
                        step.status = WorkflowStepResult.PARTIAL
                    elif step.warnings:
                        step.status = WorkflowStepResult.PARTIAL
                    else:
                        step.status = WorkflowStepResult.OK
            except Exception as exc:
                step.mark_failed(str(exc))
                logger.warning("[DailyResearchWorkflow] step '%s' failed: %s", step_name, exc)
                # Attach user-facing error metadata (v0.3.22)
                try:
                    from utils.user_facing_errors import UserFacingErrorFormatter
                    _err = UserFacingErrorFormatter.from_exception(exc, source=step_name)
                    step.extra.setdefault("user_message",  _err.plain_message)
                    step.extra.setdefault("likely_cause",  _err.likely_cause)
                    step.extra.setdefault("can_ignore",    _err.can_ignore)
                    step.extra.setdefault("next_steps",    _err.next_steps)
                    step.extra.setdefault("technical_detail", _err.technical_detail)
                except Exception:
                    pass

        self._status.add_step(step)

    # ------------------------------------------------------------------
    # Individual step handlers
    # ------------------------------------------------------------------

    def _step_provider_health(self, step):
        from data.providers.provider_health import ProviderHealthChecker
        health = ProviderHealthChecker().run_all()
        summary = health.get("summary", {})
        self._context["provider_health"] = health
        step.outputs.append(
            f"provider_health: ok={summary.get('OK', 0)} "
            f"partial={summary.get('PARTIAL', 0)} "
            f"not_configured={summary.get('NOT_CONFIGURED', 0)} "
            f"failed={summary.get('FAILED', 0)}"
        )
        step.extra["health_summary"] = summary

    def _step_provider_auto_fetch(self, step):
        from data.providers.auto_fetcher import DataProviderAutoFetcher
        fetcher = DataProviderAutoFetcher(mode=self.mode, dry_run=self.dry_run)
        result  = fetcher.run()
        self._context["auto_fetch"] = result
        step.outputs.append(
            f"auto_fetch: status={result.get('status','')} "
            f"rows_fetched={result.get('rows_fetched',0)} "
            f"rows_written={result.get('rows_written',0)}"
        )
        step.warnings.extend(result.get("warnings", []))
        step.extra["auto_fetch_status"] = result.get("status", "")

    def _step_data_freshness(self, step):
        from data.providers.data_freshness import DataFreshnessChecker
        result = DataFreshnessChecker(import_root=self.import_root).run_all()
        self._context["freshness"] = result
        datasets = result.get("datasets", {})
        fresh_str = " ".join(
            f"{ds}:{info.get('status','?')}"
            for ds, info in datasets.items()
            if ds != "intraday"
        )
        step.outputs.append(f"freshness: {fresh_str}")
        step.extra["freshness_datasets"] = {
            ds: info.get("status", "") for ds, info in datasets.items()
        }

    def _step_data_quality_gate(self, step):
        from quality.data_quality_gate import DataQualityGate
        freshness = self._context.get("freshness")
        health    = self._context.get("provider_health")
        gate = DataQualityGate(
            mode=self.mode,
            import_root=self.import_root,
            results_dir=self.results_dir,
            freshness_result=freshness,
            health_result=health,
        )
        result = gate.run()
        self._context["quality_gate"] = result
        step.outputs.append(
            f"quality_gate: production={result.get('production_readiness_score', 0):.1f}"
            f" ({result.get('production_classification', '')})"
            f" backtest={result.get('backtest_readiness_score', 0):.1f}"
        )
        step.warnings.extend(result.get("warnings", []))
        step.extra["production_readiness_score"] = result.get("production_readiness_score")
        step.extra["backtest_readiness_score"]   = result.get("backtest_readiness_score")
        step.extra["production_classification"]  = result.get("production_classification")
        step.extra["gates"] = {
            k: v for k, v in result.get("gates", {}).items()
            if not k.startswith("_")
        }

    def _step_data_source_status(self, step):
        from data.providers.public_data_provider import PublicDataProvider
        provider = PublicDataProvider()
        fn = getattr(provider, "health_check", None) or getattr(provider, "get_source_status", None)
        if fn:
            status = fn()
            summary = status.get("summary", "checked") if isinstance(status, dict) else str(status)
            step.outputs.append(f"data_source_status: {summary}")
        else:
            step.warnings.append("data_source_status: no health_check method; skipped")

    def _step_universe_quality(self, step):
        from data.universe_quality_checker import UniverseQualityChecker
        checker = UniverseQualityChecker()
        fn = getattr(checker, "run", None) or getattr(checker, "summarize_universe_quality", None)
        if fn:
            uq = fn()
            usize = uq.get("universe_size", "?") if isinstance(uq, dict) else "?"
            step.outputs.append(f"universe_quality: size={usize}")
            self._context["universe_quality"] = uq
        else:
            step.warnings.append("universe_quality: no run() method; skipped")

    def _step_signal_quality(self, step):
        from analysis.signal_quality_engine import SignalQualityEngine
        from reports.signal_quality_report import SignalQualityReport
        engine  = SignalQualityEngine(mode=self.mode, results_dir=self.results_dir)
        results = engine.run()
        rpt     = SignalQualityReport(results)
        path    = rpt.save(output_dir=self.report_dir)
        n       = results.get("n_signals", 0)
        step.outputs.append(f"signal_quality: {n} signals → {path}")
        self._context["signal_quality"] = results
        step.extra["signal_quality_report"] = path

    def _step_portfolio_simulation(self, step):
        from backtest.portfolio_simulator import PortfolioSimulator
        sim = PortfolioSimulator(mode=self.mode)
        result = sim.run()
        total_ret = result.get("metrics", {}).get("total_return")
        ret_str = f"{total_ret:+.2%}" if total_ret is not None else "N/A"
        step.outputs.append(f"portfolio_simulation: return={ret_str}")
        self._context["portfolio"] = result
        step.extra["portfolio_return"] = total_ret

    def _step_rule_weight_tuning(self, step):
        from tuning.rule_weight_tuner import RuleWeightTuner
        from tuning.rule_weight_report import RuleWeightReport
        tuner = RuleWeightTuner(mode=self.mode, results_dir=self.results_dir)
        results = tuner.run()
        rpt     = RuleWeightReport(results)
        path    = rpt.save(output_dir=self.report_dir)
        best    = results.get("best_config")
        step.outputs.append(
            f"rule_weight_tuning: best={best.name if best else 'N/A'} → {path}"
        )
        self._context["rule_weight"] = results
        step.extra["rule_weight_report"] = path

    def _step_backtest_long_term(self, step):
        from backtest.long_term_strategy_backtester import LongTermStrategyBacktester
        bt = LongTermStrategyBacktester(mode=self.mode)
        results = bt.run()
        step.outputs.append(f"backtest_long_term: status={results.get('status', 'ok')}")
        self._context["long_term"] = results

    def _step_backtest_strategy_knowledge(self, step):
        from backtest.strategy_knowledge_backtester import StrategyKnowledgeBacktester
        bt = StrategyKnowledgeBacktester(mode=self.mode)
        results = bt.run()
        step.outputs.append(f"backtest_strategy_knowledge: status={results.get('status', 'ok')}")
        self._context["strategy_knowledge"] = results

    def _step_run_validation_suite(self, step):
        for name, importer, runner in [
            ("validate_score",      "backtest.score_validation",             "ScoreValidator"),
            ("backtest_buy_points", "backtest.buy_point_backtester",         "BuyPointBacktester"),
            ("backtest_screener",   "backtest.screener_backtester",          "ScreenerBacktester"),
        ]:
            try:
                import importlib
                mod = importlib.import_module(importer)
                cls = getattr(mod, runner)
                cls(mode=self.mode).run()
                step.outputs.append(f"{name}: ok")
            except Exception as exc:
                step.warnings.append(f"{name}: {exc}")

    def _step_auto_report(self, step):
        from reports.auto_report_center import AutoReportCenter
        profile = self._profile_obj.auto_report_profile
        center  = AutoReportCenter(
            mode=self.mode,
            profile=profile,
            results_dir=self.results_dir,
        )
        result  = center.run()
        gen     = len(result.get("generated", []))
        out_dir = result.get("output_dir", "")
        step.outputs.append(f"auto_report [{profile}]: {gen} generated → {out_dir}")
        for f in result.get("failed", []):
            step.warnings.append(f"auto_report sub-fail: {f.get('name')} — {f.get('error')}")
        self._context["auto_report"] = result
        step.extra["auto_report_dir"]   = out_dir
        step.extra["auto_report_count"] = gen

    # ------------------------------------------------------------------
    # Result builder
    # ------------------------------------------------------------------

    def _build_result(self, phase: str) -> dict:
        status_dict = self._status.to_dict()
        result = {
            "phase":               phase,
            "version":             self.VERSION,
            "mode":                self.mode,
            "profile":             self.profile,
            "dry_run":             self.dry_run,
            "overall_status":      status_dict["overall_status"],
            "started_at":          status_dict.get("started_at"),
            "finished_at":         status_dict.get("finished_at"),
            "duration_seconds":    status_dict.get("duration_seconds", 0.0),
            "ok_steps":            status_dict["ok_steps"],
            "failed_steps":        status_dict["failed_steps"],
            "warning_count":       status_dict["warning_count"],
            "steps":               status_dict["steps"],
            "context_keys":        list(self._context.keys()),
            "read_only":           self.read_only,
            "no_real_orders":      self.no_real_orders,
            "production_blocked":  self.production_blocked,
        }
        # Attach quality gate summary if available
        qg = self._context.get("quality_gate", {})
        if qg:
            result["quality_gate_summary"] = {
                "production_readiness_score": qg.get("production_readiness_score"),
                "backtest_readiness_score":   qg.get("backtest_readiness_score"),
                "production_classification":  qg.get("production_classification"),
                "gates": {
                    k: v for k, v in qg.get("gates", {}).items()
                    if not k.startswith("_")
                },
            }
        # Attach auto report path if available
        ar = self._context.get("auto_report", {})
        if ar:
            result["auto_report_dir"]   = ar.get("output_dir", "")
            result["auto_report_count"] = len(ar.get("generated", []))
        return result

    # ------------------------------------------------------------------
    # Output writers
    # ------------------------------------------------------------------

    def _write_workflow_log(self, result: dict) -> Optional[str]:
        """Append result to logs/workflow/daily_workflow_runs.jsonl."""
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            log_path = os.path.join(self.log_dir, "daily_workflow_runs.jsonl")
            record = {
                "logged_at": datetime.now().isoformat(),
                **result,
            }
            # Remove large nested 'steps' list to keep log manageable
            compact = {
                k: v for k, v in record.items()
                if k != "steps"
            }
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(compact, ensure_ascii=False) + "\n")
            return log_path
        except Exception as exc:
            logger.warning("Cannot write workflow log: %s", exc)
            return None

    def _write_workflow_summary(self, result: dict) -> Optional[str]:
        """Write workflow_summary.md to reports/daily_workflow/YYYY-MM-DD/."""
        try:
            from reports.daily_workflow_report import DailyWorkflowReportBuilder
            date_str = datetime.now().strftime("%Y-%m-%d")
            out_dir  = os.path.join(_DEFAULT_WORKFLOW_REPORT_DIR, date_str)
            os.makedirs(out_dir, exist_ok=True)
            builder  = DailyWorkflowReportBuilder(
                workflow_result=result,
                context=self._context,
                report_date=date_str,
            )
            return builder.build(output_dir=out_dir)
        except Exception as exc:
            logger.warning("Cannot write workflow summary: %s", exc)
            return None
