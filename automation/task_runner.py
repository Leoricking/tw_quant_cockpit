"""
automation/task_runner.py - Read-only automation task runner (v0.3.17).

Executes scheduled research tasks by calling existing Python classes directly.
Never places orders, never modifies strategy weights, never writes API keys.

[!] Read Only. Research Only. No Real Orders.
[!] Does NOT call broker.submit_order.
[!] Does NOT modify strategy weights.
[!] Does NOT auto-apply Rule Weight Tuning results.
"""

from __future__ import annotations

import logging
import os
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from automation.task_log import AutomationTaskLog
from automation.scheduler_config import _SAFE_TASK_NAMES, _BLOCKED_KEYWORDS, is_safe_task_name

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_RESULTS_DIR = os.path.join(_BASE_DIR, "data", "backtest_results")
_DEFAULT_REPORTS_DIR = os.path.join(_BASE_DIR, "reports")
_DEFAULT_LOG_DIR     = os.path.join(_BASE_DIR, "logs", "automation")


class AutomationTaskRunner:
    """
    Executes read-only automation tasks.

    Parameters
    ----------
    mode        : 'real' or 'mock'
    results_dir : backtest CSV output folder
    reports_dir : report output folder
    log_dir     : automation log folder
    """

    # Hard-coded safety invariants — cannot be overridden
    read_only     = True
    no_real_orders = True

    def __init__(
        self,
        mode:        str = "real",
        results_dir: Optional[str] = None,
        reports_dir: Optional[str] = None,
        log_dir:     Optional[str] = None,
    ):
        self.mode        = mode
        self.results_dir = results_dir or _DEFAULT_RESULTS_DIR
        self.reports_dir = reports_dir or _DEFAULT_REPORTS_DIR
        self._log        = AutomationTaskLog(log_dir or _DEFAULT_LOG_DIR)

    # ------------------------------------------------------------------
    # Public dispatch
    # ------------------------------------------------------------------

    def run_task(self, task_name: str, **kwargs) -> dict:
        """
        Run a named task and return a task result dict.
        Blocks unsafe task names before executing.
        """
        if not is_safe_task_name(task_name):
            msg = (
                f"[SAFETY] Task '{task_name}' blocked: name contains a disallowed keyword "
                f"({_BLOCKED_KEYWORDS}). Scheduler does not trade or place orders."
            )
            logger.error(msg)
            return self._make_result(task_name, "blocked", errors=[msg])

        _dispatch = {
            "daily_data_update":        self.run_daily_data_update,
            "daily_validation":         self.run_daily_validation,
            "daily_auto_report":        self.run_daily_auto_report,
            "weekly_signal_quality":    self.run_weekly_signal_quality,
            "weekly_rule_weight_tuning":self.run_weekly_rule_weight_tuning,
            "monthly_universe_quality": self.run_monthly_universe_quality,
        }

        fn = _dispatch.get(task_name)
        if fn is None:
            msg = f"Unknown task: '{task_name}'. Valid tasks: {list(_dispatch.keys())}"
            logger.error(msg)
            return self._make_result(task_name, "error", errors=[msg])

        logger.info(
            "[AutomationTaskRunner] Starting task '%s' [mode=%s read_only=True no_real_orders=True]",
            task_name, self.mode,
        )
        try:
            return fn(**kwargs)
        except Exception as exc:
            tb = traceback.format_exc()
            logger.error("Task '%s' raised uncaught exception: %s", task_name, exc)
            return self._make_result(task_name, "failed", errors=[str(exc)], tb=tb)

    # ------------------------------------------------------------------
    # Task: daily_data_update
    # ------------------------------------------------------------------

    def run_daily_data_update(self, **kwargs) -> dict:
        """
        Check data sources and optionally fetch public data.
        Read-only. No order placement.
        """
        task_name = "daily_data_update"
        started   = datetime.now()
        outputs: List[str] = []
        warnings: List[str] = []
        errors:   List[str] = []

        # 1. data-source-status (read-only status check via health_check)
        try:
            from data.providers.public_data_provider import PublicDataProvider
            provider = PublicDataProvider()
            check_fn = getattr(provider, "health_check", None) or getattr(provider, "get_source_status", None)
            if check_fn:
                status = check_fn()
                summary = status.get("summary", "checked") if isinstance(status, dict) else str(status)
                outputs.append(f"data_source_status: {summary}")
            else:
                warnings.append("data-source-status: no health_check method found; skipped")
        except Exception as exc:
            warnings.append(f"data-source-status: {exc}")

        # 2. Attempt fetch-public-data (may require token; gracefully skip if unavailable)
        try:
            from data.providers.public_data_provider import PublicDataProvider
            provider = PublicDataProvider()
            fetch_fn = getattr(provider, "fetch_all", None)
            if fetch_fn:
                result = fetch_fn(dry_run=False)
                fetched = result.get("fetched", 0) if isinstance(result, dict) else 0
                outputs.append(f"fetch_public_data: {fetched} items fetched")
            else:
                warnings.append("fetch-public-data: no fetch_all method found; skipped")
        except Exception as exc:
            msg = str(exc)
            if "token" in msg.lower() or "api" in msg.lower() or "auth" in msg.lower():
                warnings.append(f"fetch-public-data skipped (token/API unavailable): {exc}")
            else:
                warnings.append(f"fetch-public-data: {exc}")

        status_str = "warning" if (warnings and not errors) else ("failed" if errors else "ok")
        result = self._make_result(
            task_name, status_str,
            started=started,
            outputs=outputs,
            warnings=warnings,
            errors=errors,
        )
        self._log.append_run(result)
        self._update_latest_status(result)
        return result

    # ------------------------------------------------------------------
    # Task: daily_validation
    # ------------------------------------------------------------------

    def run_daily_validation(self, **kwargs) -> dict:
        """
        Run universe quality + validation suite + signal quality + portfolio sim.
        """
        task_name = "daily_validation"
        started   = datetime.now()
        outputs: List[str] = []
        warnings: List[str] = []
        errors:   List[str] = []

        # 1. universe-quality
        try:
            from data.universe_quality_checker import UniverseQualityChecker
            checker = UniverseQualityChecker()
            uq_fn = getattr(checker, "run", None) or getattr(checker, "summarize_universe_quality", None)
            if uq_fn:
                uq = uq_fn()
                outputs.append(f"universe_quality: ok")
            else:
                warnings.append("universe-quality: no run() method found; skipped")
        except Exception as exc:
            warnings.append(f"universe-quality: {exc}")

        # 2. run-validation-suite (score + buy-point + screener + strategy-knowledge)
        for name, importer, runner in [
            ("validate_score",     "backtest.score_validation",               "ScoreValidator"),
            ("backtest_buy_points","backtest.buy_point_backtester",            "BuyPointBacktester"),
            ("backtest_screener",  "backtest.screener_backtester",             "ScreenerBacktester"),
            ("backtest_sk",        "backtest.strategy_knowledge_backtester",   "StrategyKnowledgeBacktester"),
        ]:
            try:
                mod = __import__(importer, fromlist=[runner])
                cls = getattr(mod, runner)
                r = cls(mode=self.mode).run()
                outputs.append(f"{name}: ok")
            except Exception as exc:
                warnings.append(f"{name}: {exc}")

        # 3. signal-quality
        try:
            from analysis.signal_quality_engine import SignalQualityEngine
            from reports.signal_quality_report import SignalQualityReport
            engine = SignalQualityEngine(mode=self.mode, results_dir=self.results_dir)
            sq_results = engine.run()
            rpt = SignalQualityReport(sq_results)
            rpt_path = rpt.save(output_dir=self.reports_dir)
            outputs.append(f"signal_quality: report → {rpt_path}")
        except Exception as exc:
            warnings.append(f"signal-quality: {exc}")

        # 4. simulate-portfolio (balanced scenario)
        try:
            from backtest.portfolio_simulator import PortfolioSimulator
            sim = PortfolioSimulator(mode=self.mode)
            sim_result = sim.run()
            total_ret = sim_result.get("metrics", {}).get("total_return")
            ret_str   = f"{total_ret:+.2%}" if total_ret is not None else "N/A"
            outputs.append(f"simulate_portfolio_balanced: return={ret_str}")
        except Exception as exc:
            warnings.append(f"simulate-portfolio: {exc}")

        status_str = "warning" if (warnings and not errors) else ("failed" if errors else "ok")
        result = self._make_result(
            task_name, status_str,
            started=started,
            outputs=outputs,
            warnings=warnings,
            errors=errors,
        )
        self._log.append_run(result)
        self._update_latest_status(result)
        return result

    # ------------------------------------------------------------------
    # Task: daily_auto_report
    # ------------------------------------------------------------------

    def run_daily_auto_report(self, profile: str = "daily", **kwargs) -> dict:
        """
        Run Auto Report Center with the given profile.
        """
        task_name = "daily_auto_report"
        started   = datetime.now()
        outputs: List[str] = []
        warnings: List[str] = []
        errors:   List[str] = []

        try:
            from reports.auto_report_center import AutoReportCenter
            center = AutoReportCenter(
                mode=self.mode,
                profile=profile,
                results_dir=self.results_dir,
            )
            arc_result = center.run()
            gen    = len(arc_result.get("generated", []))
            failed = len(arc_result.get("failed",    []))
            out_dir = arc_result.get("output_dir", "")
            outputs.append(f"auto_report [{profile}]: {gen} generated → {out_dir}")
            for f in arc_result.get("failed", []):
                warnings.append(f"auto_report sub-fail: {f.get('name')} — {f.get('error')}")
            status_str = "warning" if failed > 0 else "ok"
        except Exception as exc:
            errors.append(f"auto-report: {exc}")
            status_str = "failed"

        result = self._make_result(
            task_name, status_str,
            started=started,
            outputs=outputs,
            warnings=warnings,
            errors=errors,
        )
        self._log.append_run(result)
        self._update_latest_status(result)
        return result

    # ------------------------------------------------------------------
    # Task: weekly_signal_quality
    # ------------------------------------------------------------------

    def run_weekly_signal_quality(self, **kwargs) -> dict:
        """
        Run full signal quality analysis and save report.
        """
        task_name = "weekly_signal_quality"
        started   = datetime.now()
        outputs: List[str] = []
        warnings: List[str] = []
        errors:   List[str] = []

        try:
            from analysis.signal_quality_engine import SignalQualityEngine
            from reports.signal_quality_report import SignalQualityReport
            engine = SignalQualityEngine(mode=self.mode, results_dir=self.results_dir)
            sq_results = engine.run()
            rpt = SignalQualityReport(sq_results)
            rpt_path = rpt.save(output_dir=self.reports_dir)
            n = sq_results.get("n_signals", 0)
            outputs.append(f"signal_quality: {n} signals evaluated → {rpt_path}")
            status_str = "ok"
        except Exception as exc:
            errors.append(f"signal-quality: {exc}")
            status_str = "failed"

        result = self._make_result(
            task_name, status_str,
            started=started,
            outputs=outputs,
            warnings=warnings,
            errors=errors,
        )
        self._log.append_run(result)
        self._update_latest_status(result)
        return result

    # ------------------------------------------------------------------
    # Task: weekly_rule_weight_tuning
    # ------------------------------------------------------------------

    def run_weekly_rule_weight_tuning(self, **kwargs) -> dict:
        """
        Run Rule Weight Tuning Lab.
        Does NOT auto-apply the best config to production strategy.
        """
        task_name = "weekly_rule_weight_tuning"
        started   = datetime.now()
        outputs: List[str] = []
        warnings: List[str] = []
        errors:   List[str] = []

        try:
            from tuning.rule_weight_tuner import RuleWeightTuner
            from tuning.rule_weight_report import RuleWeightReport
            tuner = RuleWeightTuner(
                mode=self.mode,
                results_dir=self.results_dir,
                reports_dir=self.reports_dir,
            )
            rw_results = tuner.run()
            best = rw_results.get("best_config")
            best_name = best.name if best else "N/A"
            n = rw_results.get("n_configs", 0)
            outputs.append(f"rule_weight_tuning: {n} configs evaluated, best={best_name}")
            outputs.append("[!] Best config NOT auto-applied. Advisory only.")
            # Generate report
            rpt = RuleWeightReport(rw_results)
            rpt_path = rpt.save(output_dir=self.reports_dir)
            outputs.append(f"rule_weight_report → {rpt_path}")
            status_str = "ok"
        except Exception as exc:
            errors.append(f"tune-rule-weights: {exc}")
            status_str = "failed"

        result = self._make_result(
            task_name, status_str,
            started=started,
            outputs=outputs,
            warnings=warnings,
            errors=errors,
        )
        self._log.append_run(result)
        self._update_latest_status(result)
        return result

    # ------------------------------------------------------------------
    # Task: monthly_universe_quality
    # ------------------------------------------------------------------

    def run_monthly_universe_quality(self, **kwargs) -> dict:
        """
        Run universe quality check and generate report.
        """
        task_name = "monthly_universe_quality"
        started   = datetime.now()
        outputs: List[str] = []
        warnings: List[str] = []
        errors:   List[str] = []

        # Universe quality — summarize and record result
        try:
            from data.universe_quality_checker import UniverseQualityChecker
            checker = UniverseQualityChecker()
            uq_fn = getattr(checker, "run", None) or getattr(checker, "summarize_universe_quality", None)
            if uq_fn:
                uq = uq_fn()
                n_symbols = uq.get("total_symbols", uq.get("n_symbols", "?")) if isinstance(uq, dict) else "?"
                outputs.append(f"universe_quality: {n_symbols} symbols summarized")
            else:
                warnings.append("universe-quality: no run() method found; skipped")
        except Exception as exc:
            warnings.append(f"universe-quality: {exc}")

        # Data source status summary
        try:
            from data.providers.public_data_provider import PublicDataProvider
            provider = PublicDataProvider()
            check_fn = getattr(provider, "health_check", None) or getattr(provider, "get_source_status", None)
            if check_fn:
                ds_status = check_fn()
                summary = ds_status.get("summary", "checked") if isinstance(ds_status, dict) else str(ds_status)
                outputs.append(f"data_source_status: {summary}")
            else:
                warnings.append("data-source-status: no health_check method; skipped")
        except Exception as exc:
            warnings.append(f"data-source-status: {exc}")

        status_str = "warning" if (warnings and not errors) else ("failed" if errors else "ok")
        result = self._make_result(
            task_name, status_str,
            started=started,
            outputs=outputs,
            warnings=warnings,
            errors=errors,
        )
        self._log.append_run(result)
        self._update_latest_status(result)
        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_result(
        self,
        task_name:  str,
        status:     str,
        started:    Optional[datetime] = None,
        outputs:    Optional[List[str]] = None,
        warnings:   Optional[List[str]] = None,
        errors:     Optional[List[str]] = None,
        tb:         Optional[str] = None,
    ) -> dict:
        now       = datetime.now()
        started   = started or now
        duration  = (now - started).total_seconds()
        result = {
            "task_id":          str(uuid.uuid4())[:8],
            "task_name":        task_name,
            "mode":             self.mode,
            "started_at":       started.isoformat(),
            "finished_at":      now.isoformat(),
            "duration_seconds": round(duration, 1),
            "status":           status,
            "generated_outputs": outputs   or [],
            "warnings":          warnings  or [],
            "errors":            errors    or [],
            "read_only":         True,
            "no_real_orders":    True,
        }
        if tb:
            result["traceback"] = tb
        return result

    def _update_latest_status(self, result: dict) -> None:
        """Update latest_status.json with the most recent task result."""
        status = self._log.load_latest_status()
        status["last_task"]       = result.get("task_name")
        status["last_status"]     = result.get("status")
        status["last_run_at"]     = result.get("finished_at")
        status["last_duration"]   = result.get("duration_seconds")
        status["read_only"]       = True
        status["no_real_orders"]  = True
        status["updated_at"]      = datetime.now().isoformat()

        by_task = status.get("tasks", {})
        tname   = result.get("task_name", "unknown")
        by_task[tname] = {
            "last_status":   result.get("status"),
            "last_run_at":   result.get("finished_at"),
            "last_duration": result.get("duration_seconds"),
        }
        status["tasks"] = by_task
        self._log.write_latest_status(status)
