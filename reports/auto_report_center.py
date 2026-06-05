"""
reports/auto_report_center.py - Auto Report Center main engine (v0.3.16).

Orchestrates all research report generators in a single daily run.
Calls existing classes directly — no subprocess.
Each sub-report failure is recorded and does not abort the overall run.

Output folder: reports/auto_report_center/YYYY-MM-DD/

[!] Research Only. Simulation Only. No Real Orders.
[!] Does NOT auto-apply weights. Does NOT modify strategy.
[!] Does NOT place real orders. Does NOT connect to broker API.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import traceback
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_ROOT = os.path.join(_BASE_DIR, "reports", "auto_report_center")
_DEFAULT_RESULTS_DIR = os.path.join(_BASE_DIR, "data", "backtest_results")

# ---------------------------------------------------------------------------
# Profile definitions: which sub-reports to include per profile
# ---------------------------------------------------------------------------

_PROFILE_FLAGS: Dict[str, dict] = {
    "full": dict(
        include_stock_reports=True,
        include_universe_quality=True,
        include_signal_quality=True,
        include_portfolio=True,
        include_rule_weight=True,
        include_long_term=True,
        include_strategy_knowledge=True,
        include_strategy_knowledge_ingestion=True,
        include_ml_knowledge_integration=True,
        include_daily_summary=True,
        include_data_quality_gate=True,
        include_provider_reliability=True,
        include_hardened_backtest=True,
        include_intraday_pipeline=True,
        include_rule_governance=True,
        include_experiment_registry=True,
        include_api_fetch_production=True,
        include_ml_feature_store=True,
        include_model_monitoring=True,
        include_intraday_replay=True,
        include_notification_center=True,
        include_portfolio_journal=True,
        include_regression_consolidation=True,
        include_report_pack=True,
        include_data_stabilization=True,
        include_replay_training=True,
        include_stable_release_v060=True,
        # v0.6.2 Data Coverage Expansion (optional in full profile)
        include_data_coverage=True,
        # v0.7.0 Research Intelligence (optional in full profile)
        include_research_intelligence=True,
        # v0.7.2 Strategy Research Memory (optional in full profile)
        include_strategy_memory=True,
        # v0.7.3 Backtest-to-Coach Loop (optional in full profile)
        include_backtest_coach=True,
        # v0.8.0 Research Intelligence Stable (optional in full profile)
        include_intelligence_stable=True,
    ),
    "daily": dict(
        include_stock_reports=False,
        include_universe_quality=True,
        include_signal_quality=True,
        include_portfolio=True,
        include_rule_weight=False,
        include_long_term=False,
        include_strategy_knowledge=False,
        include_strategy_knowledge_ingestion=True,
        include_ml_knowledge_integration=True,
        include_daily_summary=True,
        include_data_quality_gate=True,
        include_provider_reliability=True,
        include_intraday_pipeline=True,
        include_api_fetch_production=True,
        include_ml_feature_store=True,
        include_model_monitoring=True,
        include_intraday_replay=False,
        include_notification_center=True,
        include_portfolio_journal=True,
        include_regression_consolidation=False,
        include_report_pack=False,
        include_data_stabilization=True,
        include_replay_training=False,
        # v0.7.0 Research Intelligence in daily profile
        include_research_intelligence=True,
        # v0.7.2 Strategy Research Memory in daily profile
        include_strategy_memory=True,
        # v0.7.3 Backtest-to-Coach Loop in daily profile
        include_backtest_coach=True,
        # v0.8.0 Research Intelligence Stable summary in daily profile
        include_intelligence_stable=True,
    ),
    "portfolio": dict(
        include_stock_reports=False,
        include_universe_quality=False,
        include_signal_quality=False,
        include_portfolio=True,
        include_rule_weight=False,
        include_long_term=False,
        include_strategy_knowledge=False,
        include_daily_summary=False,
    ),
    "signal": dict(
        include_stock_reports=False,
        include_universe_quality=False,
        include_signal_quality=True,
        include_portfolio=False,
        include_rule_weight=False,
        include_long_term=False,
        include_strategy_knowledge=True,
        include_daily_summary=False,
    ),
    "stock": dict(
        include_stock_reports=True,
        include_universe_quality=False,
        include_signal_quality=False,
        include_portfolio=False,
        include_rule_weight=False,
        include_long_term=False,
        include_strategy_knowledge=False,
        include_daily_summary=False,
    ),
    "universe": dict(
        include_stock_reports=False,
        include_universe_quality=True,
        include_signal_quality=False,
        include_portfolio=False,
        include_rule_weight=False,
        include_long_term=False,
        include_strategy_knowledge=False,
        include_daily_summary=False,
    ),
}


class AutoReportCenter:
    """
    One-stop engine that runs all research report generators and assembles
    a dated output folder.

    Parameters
    ----------
    mode : 'real' or 'mock'
    profile : 'full' | 'daily' | 'portfolio' | 'signal' | 'stock' | 'universe'
    stocks : optional list of symbol strings for stock reports
    top_n : how many top candidates to include in summaries
    output_dir : root folder (default: reports/auto_report_center)
    results_dir : backtest CSV folder (default: data/backtest_results)
    report_date : YYYY-MM-DD string; defaults to today
    include_* : fine-grained overrides (override profile defaults)
    """

    VERSION = "v0.3.16"

    def __init__(
        self,
        mode: str = "real",
        profile: str = "full",
        stocks: Optional[List[str]] = None,
        top_n: int = 8,
        output_dir: Optional[str] = None,
        results_dir: Optional[str] = None,
        report_date: Optional[str] = None,
        include_stock_reports: bool = True,
        include_universe_quality: bool = True,
        include_signal_quality: bool = True,
        include_portfolio: bool = True,
        include_rule_weight: bool = True,
        include_long_term: bool = True,
        include_strategy_knowledge: bool = True,
        include_daily_summary: bool = True,
        include_data_quality_gate: bool = False,
        include_provider_reliability: bool = False,
        universe_name: Optional[str] = None,
        include_hardened_backtest: bool = False,
        include_intraday_pipeline: bool = False,
        include_rule_governance: bool = False,
        include_experiment_registry: bool = False,
        include_api_fetch_production: bool = False,
        include_ml_feature_store: bool = False,
        include_model_monitoring: bool = False,
        include_intraday_replay: bool = False,
        include_strategy_knowledge_ingestion: bool = False,
        include_ml_knowledge_integration: bool = False,
        include_notification_center: bool = False,
        include_portfolio_journal: bool = False,
        include_regression_consolidation: bool = False,
        include_report_pack: bool = False,
        include_data_stabilization: bool = False,
        include_replay_training: bool = False,
        include_stable_release_v060: bool = False,
        include_data_coverage: bool = False,
        include_research_intelligence: bool = False,
        include_strategy_memory: bool = False,
        include_backtest_coach: bool = False,
        include_intelligence_stable: bool = False,
    ):
        self.mode        = mode
        self.profile     = profile
        self.stocks      = stocks or []
        self.top_n       = top_n
        self.output_root = output_dir or _DEFAULT_OUTPUT_ROOT
        self.results_dir = results_dir or _DEFAULT_RESULTS_DIR

        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")

        # Apply profile defaults first, then allow explicit overrides
        flags = _PROFILE_FLAGS.get(profile, _PROFILE_FLAGS["full"])
        self.include_stock_reports        = flags.get("include_stock_reports",        include_stock_reports)
        self.include_universe_quality     = flags.get("include_universe_quality",     include_universe_quality)
        self.include_signal_quality       = flags.get("include_signal_quality",       include_signal_quality)
        self.include_portfolio            = flags.get("include_portfolio",            include_portfolio)
        self.include_rule_weight          = flags.get("include_rule_weight",          include_rule_weight)
        self.include_long_term            = flags.get("include_long_term",            include_long_term)
        self.include_strategy_knowledge   = flags.get("include_strategy_knowledge",   include_strategy_knowledge)
        self.include_daily_summary        = flags.get("include_daily_summary",        include_daily_summary)
        self.include_data_quality_gate    = flags.get("include_data_quality_gate",    include_data_quality_gate)
        self.include_provider_reliability = flags.get("include_provider_reliability", include_provider_reliability)
        self.include_hardened_backtest    = flags.get("include_hardened_backtest",    include_hardened_backtest)
        self.include_intraday_pipeline    = flags.get("include_intraday_pipeline",    include_intraday_pipeline)
        self.include_rule_governance       = flags.get("include_rule_governance",       include_rule_governance)
        self.include_experiment_registry   = flags.get("include_experiment_registry",   include_experiment_registry)
        self.include_api_fetch_production  = flags.get("include_api_fetch_production",  include_api_fetch_production)
        self.include_ml_feature_store      = flags.get("include_ml_feature_store",      include_ml_feature_store)
        self.include_model_monitoring      = flags.get("include_model_monitoring",      include_model_monitoring)
        self.include_intraday_replay       = flags.get("include_intraday_replay",       include_intraday_replay)
        self.include_strategy_knowledge_ingestion = flags.get(
            "include_strategy_knowledge_ingestion", include_strategy_knowledge_ingestion
        )
        self.include_ml_knowledge_integration = flags.get(
            "include_ml_knowledge_integration", include_ml_knowledge_integration
        )
        self.include_notification_center = flags.get(
            "include_notification_center", include_notification_center
        )
        self.include_portfolio_journal = flags.get(
            "include_portfolio_journal", include_portfolio_journal
        )
        self.include_regression_consolidation = flags.get(
            "include_regression_consolidation", include_regression_consolidation
        )
        self.include_report_pack = flags.get(
            "include_report_pack", include_report_pack
        )
        self.include_data_stabilization = flags.get(
            "include_data_stabilization", include_data_stabilization
        )
        self.include_replay_training = flags.get(
            "include_replay_training", include_replay_training
        )
        self.include_stable_release_v060 = flags.get(
            "include_stable_release_v060", include_stable_release_v060
        )
        self.include_data_coverage = flags.get(
            "include_data_coverage", include_data_coverage
        )
        self.include_research_intelligence = flags.get(
            "include_research_intelligence", include_research_intelligence
        )
        self.include_strategy_memory = flags.get(
            "include_strategy_memory", include_strategy_memory
        )
        self.include_backtest_coach = flags.get(
            "include_backtest_coach", include_backtest_coach
        )
        self.include_intelligence_stable = flags.get(
            "include_intelligence_stable", include_intelligence_stable
        )
        self.universe_name = universe_name

        # Runtime state (populated during run)
        self._out_dir: str = os.path.join(self.output_root, self.report_date)
        self._generated: List[dict] = []
        self._failed: List[dict] = []
        self._context: dict = {"universe_name": universe_name or "default"}   # cross-report data shared across builders

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Run all enabled sub-reports.

        Returns dict with:
            status, output_dir, generated, failed, manifest_path,
            index_path, executive_summary_path, daily_summary_path
        """
        logger.info(
            "AutoReportCenter.run [mode=%s profile=%s date=%s]",
            self.mode, self.profile, self.report_date,
        )

        # Create output tree
        self._make_output_dirs()

        # Sub-reports (each wrapped in try/except)
        if self.include_stock_reports:
            self.run_stock_reports()

        if self.include_universe_quality:
            self.run_universe_quality()

        if self.include_signal_quality:
            self.run_signal_quality()

        if self.include_portfolio:
            self.run_portfolio_report()

        if self.include_rule_weight:
            self.run_rule_weight_report()

        if self.include_long_term:
            self.run_long_term_report()

        if self.include_strategy_knowledge:
            self.run_strategy_knowledge_report()

        if self.include_data_quality_gate:
            self.run_data_quality_gate_report()

        if self.include_provider_reliability:
            self.run_provider_reliability_report()

        if self.include_hardened_backtest:
            self.run_hardened_backtest_report()

        if self.include_intraday_pipeline:
            self.run_intraday_pipeline_report()

        if self.include_rule_governance:
            self.run_rule_governance_report()

        if self.include_experiment_registry:
            self.run_experiment_registry_report()

        if self.include_api_fetch_production:
            self.run_api_fetch_production_report()

        if self.include_ml_feature_store:
            self.run_ml_feature_store_report()

        if self.include_model_monitoring:
            self.run_model_monitoring_report()

        if self.include_intraday_replay:
            self.run_intraday_replay_report()

        if self.include_strategy_knowledge_ingestion:
            self.run_strategy_knowledge_ingestion_summary()

        if self.include_ml_knowledge_integration:
            self.run_ml_knowledge_integration_summary()

        if self.include_notification_center:
            self.run_notification_center_report()

        if self.include_portfolio_journal:
            self.run_portfolio_journal_summary()

        # v0.4.7 Research Review Dashboard summary (always optional, never crashes)
        self.run_research_review_summary()

        # v0.4.8 Research Assistant / Coach summary (always optional, never crashes)
        self.run_research_coach_summary()

        # v0.4.9 Research Workflow Automation summary (always optional, never crashes)
        self.run_research_workflow_summary()

        # v0.5.0 Research OS Planning summary (always optional, never crashes)
        self.run_research_os_summary()

        # v0.5.1 CLI UX summary (always optional, never crashes)
        self.run_cli_ux_summary()

        # v0.5.2 GUI Navigation summary (always optional, never crashes)
        self.run_gui_navigation_summary()

        # v0.5.1.1 Strategy Filter summary (always optional, never crashes)
        self.run_strategy_filter_summary()

        # v0.5.3 Regression Suite Consolidation summary (always optional, never crashes)
        if self.include_regression_consolidation:
            self.run_regression_consolidation_summary()

        # v0.5.4 Report Pack Consolidation summary (always optional, never crashes)
        # IMPORTANT: does NOT call auto_report_center full — avoids recursive loop
        if self.include_report_pack:
            self.run_report_pack_summary()

        # v0.5.5 Data / Feature Store Stabilization summary (always optional, never crashes)
        # IMPORTANT: summary only — does NOT call auto_report_center full — avoids recursive loop
        if self.include_data_stabilization:
            self.run_data_stabilization_summary()

        # v0.5.6 Replay Training Cockpit summary (always optional, never crashes)
        if self.include_replay_training:
            self.run_replay_training_summary()

        # v0.6.0 Stable Release summary (always optional, never crashes, avoids recursive loop)
        if getattr(self, "include_stable_release_v060", False):
            self.run_stable_release_v060_summary()

        # v0.6.2 Data Coverage Expansion (optional, failure should not crash)
        if getattr(self, "include_data_coverage", False):
            try:
                from reports.data_coverage_report import DataCoverageReport
                dc_reporter = DataCoverageReport(
                    project_root=_BASE_DIR,
                    report_dir=os.path.join(self._out_dir, "data_coverage"),
                )
                dc_path = dc_reporter.run(mode=self.mode)
                self._generated.append({
                    "name": "data_coverage_report",
                    "path": dc_path,
                    "section": "data_coverage",
                })
                logger.info("DataCoverageReport generated: %s", dc_path)
            except Exception as _dc_exc:
                logger.warning("DataCoverageReport failed (non-blocking): %s", _dc_exc)
                self._failed.append({
                    "name": "data_coverage_report",
                    "error": str(_dc_exc),
                })

        # v0.7.0 Research Intelligence (optional, failure should not crash)
        if getattr(self, "include_research_intelligence", False):
            try:
                from research_intelligence.research_intelligence_engine import ResearchIntelligenceEngine
                from reports.research_intelligence_report import ResearchIntelligenceReport
                ri_engine = ResearchIntelligenceEngine(project_root=_BASE_DIR)
                ri_result = ri_engine.run(mode=self.mode)
                ri_reporter = ResearchIntelligenceReport()
                ri_content = ri_reporter.generate(
                    summary=ri_result.get("summary", {}),
                    signals=ri_result.get("signals", []),
                    recommendations=ri_result.get("recommendations", []),
                    priority_board={"rows": ri_result.get("priority_board", [])},
                    daily_plan=ri_result.get("daily_plan", []),
                    weekly_plan=ri_result.get("weekly_plan", []),
                    mode=self.mode,
                )
                ri_path = ri_reporter.save(ri_content, report_dir=os.path.join(self._out_dir, "research_intelligence"))
                self._generated.append({
                    "name": "research_intelligence_report",
                    "path": ri_path,
                    "section": "research_intelligence",
                })
                logger.info("ResearchIntelligenceReport generated: %s", ri_path)
            except Exception as _ri_exc:
                logger.warning("ResearchIntelligenceReport failed (non-blocking): %s", _ri_exc)
                self._failed.append({
                    "name": "research_intelligence_report",
                    "error": str(_ri_exc),
                })

        # v0.7.2 Strategy Research Memory (optional, failure should not crash)
        if getattr(self, "include_strategy_memory", False):
            try:
                from strategy_memory.strategy_memory_engine import StrategyMemoryEngine
                from reports.strategy_memory_report import StrategyMemoryReportBuilder
                sm_dir = os.path.join(_BASE_DIR, "data", "backtest_results", "strategy_memory")
                sm_engine = StrategyMemoryEngine(project_root=_BASE_DIR, output_dir=sm_dir)
                sm_engine.run(mode=self.mode)
                sm_reporter = StrategyMemoryReportBuilder()
                sm_path = sm_reporter.build(
                    mode=self.mode,
                    output_dir=os.path.join(self._out_dir, "strategy_memory"),
                    memory_output_dir=sm_dir,
                )
                self._generated.append({
                    "name": "strategy_memory_report",
                    "path": sm_path,
                    "section": "strategy_memory",
                })
                logger.info("StrategyMemoryReport generated: %s", sm_path)
            except Exception as _sm_exc:
                logger.warning("StrategyMemoryReport failed (non-blocking): %s", _sm_exc)
                self._failed.append({
                    "name": "strategy_memory_report",
                    "error": str(_sm_exc),
                })

        # v0.7.3 Backtest-to-Coach Loop (optional, failure should not crash)
        if getattr(self, "include_backtest_coach", False):
            try:
                from backtest_coach.backtest_coach_engine import BacktestCoachEngine
                from reports.backtest_coach_report import BacktestCoachReportBuilder
                bc_dir = os.path.join(_BASE_DIR, "data", "backtest_results", "backtest_coach")
                bc_engine = BacktestCoachEngine(project_root=_BASE_DIR, output_dir=bc_dir)
                bc_engine.run(mode=self.mode, period="daily")
                bc_reporter = BacktestCoachReportBuilder()
                bc_path = bc_reporter.build(
                    mode=self.mode,
                    output_dir=os.path.join(self._out_dir, "backtest_coach"),
                    coach_output_dir=bc_dir,
                )
                self._generated.append({
                    "name": "backtest_coach_report",
                    "path": bc_path,
                    "section": "backtest_coach",
                })
                logger.info("BacktestCoachReport generated: %s", bc_path)
            except Exception as _bc_exc:
                logger.warning("BacktestCoachReport failed (non-blocking): %s", _bc_exc)
                self._failed.append({
                    "name": "backtest_coach_report",
                    "error": str(_bc_exc),
                })

        # v0.8.0 Research Intelligence Stable (optional, failure should not crash)
        if getattr(self, "include_intelligence_stable", False):
            try:
                self.run_intelligence_stable_summary()
            except Exception as _is_exc:
                logger.warning("intelligence_stable_summary failed (non-blocking): %s", _is_exc)
                self._failed.append({
                    "name": "intelligence_stable_summary",
                    "error": str(_is_exc),
                })

        # Aggregated outputs
        if self.include_daily_summary:
            self.build_daily_market_summary()

        exec_path = self.build_executive_summary()
        index_path = self.build_report_index()
        manifest_path = self.write_manifest()

        # Write failed_reports.json
        failed_path = os.path.join(self._out_dir, "failed_reports.json")
        try:
            with open(failed_path, "w", encoding="utf-8") as f:
                json.dump(self._failed, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("Cannot write failed_reports.json: %s", exc)

        logger.info(
            "AutoReportCenter done: %d generated, %d failed",
            len(self._generated), len(self._failed),
        )

        return {
            "status":                 "ok",
            "mode":                   self.mode,
            "profile":                self.profile,
            "report_date":            self.report_date,
            "output_dir":             self._out_dir,
            "generated":              self._generated,
            "failed":                 self._failed,
            "manifest_path":          manifest_path,
            "index_path":             index_path,
            "executive_summary_path": exec_path,
            "daily_summary_path":     self._context.get("daily_summary_path"),
        }

    # ------------------------------------------------------------------
    # Sub-report runners
    # ------------------------------------------------------------------

    def run_stock_reports(self):
        """Generate individual stock analysis reports."""
        sub_dir = os.path.join(self._out_dir, "stock_reports")
        os.makedirs(sub_dir, exist_ok=True)

        # Determine which symbols to report
        symbols = list(self.stocks)
        if not symbols:
            symbols = self._load_universe_symbols()

        if not symbols:
            self._record_fail("stock_reports", "No symbols found in universe")
            return

        try:
            from analysis.stock_report_builder import StockReportBuilder
            builder = StockReportBuilder()
        except Exception as exc:
            self._record_fail("stock_reports", str(exc))
            return

        generated_paths = []
        for sym in symbols[:self.top_n]:
            try:
                data_sources = None
                if self.mode == "real":
                    try:
                        from data.real_data_loader import RealDataLoader
                        all_data = RealDataLoader().load_all(sym)
                        data_sources = all_data.get("_sources")
                    except Exception:
                        pass

                report_text = builder.build(
                    symbol=sym,
                    name=sym,
                    bull_score_data={},
                    mode=self.mode,
                    data_sources=data_sources,
                )
                path = os.path.join(sub_dir, f"{sym}_report.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(report_text)
                generated_paths.append(path)
                logger.debug("Stock report saved: %s", path)
            except Exception as exc:
                self._record_fail(f"stock_report_{sym}", str(exc))

        if generated_paths:
            self._record_success(
                "stock_reports",
                generated_paths[0],
                extra={"count": len(generated_paths), "paths": generated_paths},
            )

    def run_universe_quality(self):
        """Run universe quality check and save report."""
        sub_dir = os.path.join(self._out_dir, "universe_quality")
        os.makedirs(sub_dir, exist_ok=True)
        try:
            from data.universe_quality_checker import UniverseQualityChecker
            from reports.universe_quality_report import UniverseQualityReport

            uqc = UniverseQualityChecker()
            df = uqc.check_universe()
            summary = uqc.summarize_universe_quality(df)
            self._context["universe_quality_summary"] = summary
            self._context["universe_quality_df"] = df

            rpt = UniverseQualityReport(df, summary)
            path = rpt.save(output_dir=sub_dir)
            self._record_success("universe_quality", path,
                                 extra={"summary": summary})
        except Exception as exc:
            self._record_fail("universe_quality", str(exc))

    def run_signal_quality(self):
        """Run signal quality engine and save report."""
        sub_dir = os.path.join(self._out_dir, "signal_quality")
        os.makedirs(sub_dir, exist_ok=True)
        try:
            from analysis.signal_quality_engine import SignalQualityEngine
            from reports.signal_quality_report import SignalQualityReport

            engine = SignalQualityEngine(
                results_dir=self.results_dir,
                reports_dir=sub_dir,
                mode=self.mode,
            )
            results = engine.run()
            self._context["signal_quality_results"] = results

            rpt = SignalQualityReport(results)
            path = rpt.save(output_dir=sub_dir)
            self._record_success("signal_quality", path,
                                 extra={"counts": _sq_counts(results)})
        except Exception as exc:
            self._record_fail("signal_quality", str(exc))

    def run_portfolio_report(self):
        """Run portfolio simulation (all scenarios) and save report."""
        sub_dir = os.path.join(self._out_dir, "portfolio")
        os.makedirs(sub_dir, exist_ok=True)
        try:
            from backtest.portfolio_scenarios import PortfolioScenarios
            from reports.portfolio_simulation_report import PortfolioSimulationReport

            runner = PortfolioScenarios(mode=self.mode)
            all_results = runner.run_all()
            comp_path = runner.save_comparison(all_results, output_dir=self.results_dir)

            primary = all_results.get("balanced") or next(
                (r for r in all_results.values() if r.get("status") == "ok"), {}
            )
            self._context["portfolio_results"] = {
                "primary": primary,
                "all_results": all_results,
            }

            rpt = PortfolioSimulationReport(primary, all_scenario_results=all_results)
            path = rpt.save(output_dir=sub_dir)
            self._record_success("portfolio", path,
                                 extra={"metrics": primary.get("metrics", {})})
        except Exception as exc:
            self._record_fail("portfolio", str(exc))

    def run_rule_weight_report(self):
        """Run rule weight tuner and save report."""
        sub_dir = os.path.join(self._out_dir, "rule_weight")
        os.makedirs(sub_dir, exist_ok=True)
        try:
            from tuning.rule_weight_tuner import RuleWeightTuner
            from tuning.rule_weight_report import RuleWeightReport

            tuner = RuleWeightTuner(
                mode=self.mode,
                results_dir=self.results_dir,
                reports_dir=sub_dir,
            )
            results = tuner.run()
            self._context["rule_weight_results"] = results

            rpt = RuleWeightReport(results)
            path = rpt.save(output_dir=sub_dir)
            best = results.get("best_config")
            self._record_success("rule_weight", path,
                                 extra={"best_config": best.name if best else None})
        except Exception as exc:
            self._record_fail("rule_weight", str(exc))

    def run_long_term_report(self):
        """Run long-term strategy backtester and save report."""
        sub_dir = os.path.join(self._out_dir, "long_term")
        os.makedirs(sub_dir, exist_ok=True)
        try:
            from backtest.long_term_strategy_backtester import LongTermStrategyBacktester
            from reports.long_term_validation_report import LongTermValidationReport

            bt = LongTermStrategyBacktester(mode=self.mode)
            results = bt.run()
            self._context["long_term_results"] = results

            rpt = LongTermValidationReport(results)
            path = rpt.save(output_dir=sub_dir)
            self._record_success("long_term", path)
        except Exception as exc:
            self._record_fail("long_term", str(exc))

    def run_strategy_knowledge_report(self):
        """Run strategy knowledge backtester and save report."""
        sub_dir = os.path.join(self._out_dir, "strategy_knowledge")
        os.makedirs(sub_dir, exist_ok=True)
        try:
            from backtest.strategy_knowledge_backtester import StrategyKnowledgeBacktester

            bt = StrategyKnowledgeBacktester(mode=self.mode)
            results = bt.run()
            self._context["strategy_knowledge_results"] = results

            # Try to call report generator if it exists
            try:
                from reports.strategy_knowledge_validation_report import (
                    StrategyKnowledgeValidationReport,
                )
                rpt = StrategyKnowledgeValidationReport(results)
                path = rpt.save(output_dir=sub_dir)
            except ImportError:
                # Fallback: write basic text summary
                path = os.path.join(sub_dir, "strategy_knowledge_summary.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"Strategy Knowledge Backtest Results\n")
                    f.write(f"Status: {results.get('status', 'ok')}\n")
                    conf = results.get("confidence", {})
                    f.write(f"Confidence: {conf.get('overall', 'INSUFFICIENT')}\n")

            self._record_success("strategy_knowledge", path)
        except Exception as exc:
            self._record_fail("strategy_knowledge", str(exc))

    def run_data_quality_gate_report(self):
        """Run data quality gate and save report (v0.3.20)."""
        sub_dir = os.path.join(self._out_dir, "data_quality_gate")
        os.makedirs(sub_dir, exist_ok=True)
        try:
            from quality.data_quality_gate import DataQualityGate
            from reports.data_quality_gate_report import DataQualityGateReportBuilder

            gate = DataQualityGate(mode=self.mode, results_dir=self.results_dir)
            gate_result = gate.run()
            self._context["data_quality_gate_result"] = gate_result

            builder = DataQualityGateReportBuilder(
                gate_result=gate_result,
                report_date=self.report_date,
            )
            path = builder.build(output_dir=sub_dir)
            self._record_success(
                "data_quality_gate",
                path,
                extra={
                    "production_readiness_score": gate_result.get("production_readiness_score"),
                    "backtest_readiness_score":   gate_result.get("backtest_readiness_score"),
                    "production_classification":  gate_result.get("production_classification"),
                },
            )
        except Exception as exc:
            self._record_fail("data_quality_gate", str(exc))

    def run_provider_reliability_report(self):
        """Run provider reliability matrix and save report (v0.3.24)."""
        try:
            from data.providers.reliability_matrix import ProviderReliabilityMatrix
            from reports.provider_reliability_report import ProviderReliabilityReportBuilder

            matrix = ProviderReliabilityMatrix(
                results_dir=self.results_dir,
                report_dir=self._out_dir,
                mode=self.mode,
            )
            rel_result = matrix.run()
            self._context["provider_reliability_result"] = rel_result
            self._context["provider_reliability_summary"] = rel_result.get("reliability_summary", {})

            builder = ProviderReliabilityReportBuilder(
                report_date=self.report_date,
                matrix_data=rel_result,
            )
            path = builder.build(output_dir=self._out_dir)
            self._record_success(
                "provider_reliability",
                path,
                extra={
                    "overall_reliability":  rel_result.get("reliability_summary", {}).get("overall_reliability_score"),
                    "overall_confidence":   rel_result.get("reliability_summary", {}).get("overall_dataset_confidence"),
                    "weak_datasets":        rel_result.get("reliability_summary", {}).get("weak_datasets", []),
                    "mock_fallback_count":  0,
                },
            )
        except Exception as exc:
            self._record_fail("provider_reliability", str(exc))

    def run_hardened_backtest_report(self):
        """Run hardened backtest and save report (v0.3.26)."""
        try:
            from backtest.hardened_backtester import HardenedBacktester
            from reports.hardened_backtest_report import HardenedBacktestReportBuilder

            bt = HardenedBacktester(
                mode=self.mode,
                results_dir=self.results_dir,
                report_dir=self._out_dir,
            )
            bt_result = bt.run()
            self._context["hardened_backtest_result"] = bt_result

            builder = HardenedBacktestReportBuilder(
                report_date=self.report_date,
                backtest_result=bt_result,
                mode=self.mode,
            )
            path = builder.build(output_dir=self._out_dir)
            self._record_success(
                "hardened_backtest",
                path,
                extra={
                    "confidence_grade": bt_result.get("confidence_grade", "D"),
                    "trade_count":      bt_result.get("trade_count", 0),
                    "net_return":       bt_result.get("net_return"),
                    "sharpe":           bt_result.get("sharpe"),
                },
            )
        except Exception as exc:
            self._record_fail("hardened_backtest", str(exc))

    def run_rule_governance_report(self):
        """Run rule governance analysis and save report (v0.3.28)."""
        try:
            from gui.rule_governance_adapter import RuleGovernanceAdapter
            adapter = RuleGovernanceAdapter(
                results_dir=self.results_dir,
                report_dir=self._out_dir,
            )
            gov_result = adapter.run_governance(mode=self.mode)
            reg_summary = gov_result.get("registry_summary", {})
            conf_result = gov_result.get("confidence_result", {})
            self._context["rule_governance_summary"] = reg_summary
            self._context["rules_needing_review"] = gov_result.get("review_queue", [])
            self._context["experimental_rule_count"] = reg_summary.get("experimental_count", 0)
            self._context["high_confidence_rule_count"] = len(conf_result.get("high_confidence", []))

            path = adapter.generate_report(mode=self.mode)
            self._record_success(
                "rule_governance",
                path,
                extra={
                    "total_rules":          reg_summary.get("total_rules", 0),
                    "experimental_count":   reg_summary.get("experimental_count", 0),
                    "needs_review_count":   reg_summary.get("needs_review_count", 0),
                    "high_confidence":      len(conf_result.get("high_confidence", [])),
                },
            )
        except Exception as exc:
            self._record_fail("rule_governance", str(exc))

    def run_intraday_pipeline_report(self):
        """Run intraday pipeline quality check and save report (v0.3.27)."""
        try:
            from intraday.intraday_quality import IntradayQualityChecker
            from reports.intraday_pipeline_report import IntradayPipelineReportBuilder

            checker = IntradayQualityChecker()
            quality_result = checker.run()
            self._context["intraday_quality_result"] = quality_result
            self._context["intraday_quality_score"] = quality_result.get("overall_quality_score", 0.0)
            self._context["intraday_status"] = quality_result.get("status", "NO_DATA")
            self._context["tick_bidask_readiness"] = False   # planned v0.4+

            builder = IntradayPipelineReportBuilder(
                report_date=self.report_date,
                quality_result=quality_result,
                mode=self.mode,
            )
            path = builder.build(output_dir=self._out_dir)
            self._record_success(
                "intraday_pipeline",
                path,
                extra={
                    "intraday_quality_score": quality_result.get("overall_quality_score", 0.0),
                    "intraday_status":        quality_result.get("status", "NO_DATA"),
                    "symbols_found":          len(quality_result.get("symbols", [])),
                    "tick_bidask_ready":      False,
                },
            )
        except Exception as exc:
            self._record_fail("intraday_pipeline", str(exc))

    def run_experiment_registry_report(self):
        """Generate experiment registry report (v0.3.29). Optional — failure does not abort run."""
        try:
            from reports.experiment_registry_report import ExperimentRegistryReportBuilder
            builder = ExperimentRegistryReportBuilder(report_dir=self._out_dir)
            path    = builder.build()
            self._context["experiment_registry_report"] = path
            self._record_success("experiment_registry", path)
        except Exception as exc:
            self._record_fail("experiment_registry", str(exc))

    def run_api_fetch_production_report(self):
        """Generate API Fetch Productionization report (v0.4.1). Optional — failure does not abort run."""
        try:
            from gui.api_fetch_status_adapter import APIFetchStatusAdapter
            result = APIFetchStatusAdapter(report_dir=self._out_dir).generate_report(mode=self.mode)
            if result.get("ok"):
                path = result.get("report_path", "")
                self._context["api_fetch_production_report"] = path
                self._record_success("api_fetch_production", path)
            else:
                self._record_fail("api_fetch_production", result.get("error", "unknown"))
        except Exception as exc:
            self._record_fail("api_fetch_production", str(exc))

    def run_intraday_replay_report(self):
        """Generate Intraday Replay Cockpit report (v0.4.4). Optional — failure does not abort run."""
        try:
            from gui.intraday_replay_adapter import IntradayReplayAdapter
            result = IntradayReplayAdapter(report_dir=self._out_dir).generate_report(mode=self.mode)
            if result.get("ok"):
                path = result.get("report_path", "")
                self._context["intraday_replay_report"] = path
                self._record_success("intraday_replay", path)
            else:
                self._record_fail("intraday_replay", result.get("error", "unknown"))
        except Exception as exc:
            self._record_fail("intraday_replay", str(exc))

    def run_strategy_knowledge_ingestion_summary(self):
        """
        Include Strategy Knowledge Ingestion summary in context (v0.4.1.1).
        Does NOT force a new ingestion run — reads existing store output.
        Optional — failure does not abort overall run.
        """
        try:
            from gui.strategy_knowledge_ingestion_adapter import (
                StrategyKnowledgeIngestionAdapter,
            )
            adapter = StrategyKnowledgeIngestionAdapter(report_dir=self._out_dir)
            result = adapter.load_latest_summary()
            summary = result.get("summary", {})
            self._context["strategy_knowledge_items_count"] = summary.get("total_items", 0)
            self._context["strategy_rule_candidates_count"] = summary.get("rule_candidates_count", 0)
            self._context["strategy_avoid_conditions_count"] = summary.get("avoid_conditions_count", 0)
            self._context["strategy_risk_conditions_count"] = summary.get("risk_conditions_count", 0)
            self._context["strategy_knowledge_latest_at"] = summary.get("latest_ingestion_at", "")
            self._record_success(
                "strategy_knowledge_ingestion",
                f"items={summary.get('total_items', 0)} "
                f"rules={summary.get('rule_candidates_count', 0)} "
                f"avoid={summary.get('avoid_conditions_count', 0)} "
                f"risk={summary.get('risk_conditions_count', 0)}",
            )
        except Exception as exc:
            logger.warning("run_strategy_knowledge_ingestion_summary failed: %s", exc)
            self._record_fail("strategy_knowledge_ingestion", str(exc))

    def run_ml_knowledge_integration_summary(self):
        """
        Include ML Knowledge Integration summary in context (v0.4.2.1).
        Reads existing output — does NOT force a new integration run.
        Optional — failure does not abort overall run.
        """
        try:
            from ml.knowledge_dataset_exporter import KnowledgeDatasetExporter
            exporter = KnowledgeDatasetExporter()
            summary  = exporter.load_latest_summary()
            if not summary:
                self._record_fail(
                    "ml_knowledge_integration",
                    "No ml_knowledge_integration_summary.json found — run ml-knowledge-integrate first",
                )
                return
            self._context["ml_knowledge_features_count"]  = summary.get("total_features", 0)
            self._context["ml_knowledge_model_ready"]      = summary.get("model_ready_features", 0)
            self._context["ml_knowledge_auto_enabled"]     = 0
            self._context["ml_knowledge_leakage_findings"] = summary.get("leakage_findings", 0)
            self._context["ml_knowledge_critical_leakage"] = summary.get("critical_leakage", 0)
            self._record_success(
                "ml_knowledge_integration",
                f"features={summary.get('total_features', 0)} "
                f"model_ready={summary.get('model_ready_features', 0)} "
                f"leakage={summary.get('leakage_findings', 0)} "
                f"auto_enabled=0",
            )
        except Exception as exc:
            logger.warning("run_ml_knowledge_integration_summary failed: %s", exc)
            self._record_fail("ml_knowledge_integration", str(exc))

    def run_notification_center_report(self):
        """
        Generate Notification Center report (v0.4.5).
        Reads existing notification log — does NOT force a new scan.
        Optional — failure does not abort overall run.
        """
        try:
            from gui.notification_center_adapter import NotificationCenterAdapter
            adapter = NotificationCenterAdapter(mode=self.mode, report_dir=self._out_dir)
            result  = adapter.generate_report(dry_run=False)
            path    = result.get("report_path", "")
            if result.get("status") == "OK" and path:
                self._context["notification_center_report"] = path
                self._generated.append({"type": "notification_center", "path": path})
            summary = adapter.get_summary()
            self._context["notification_total"]   = summary.get("total_events", 0)
            self._context["notification_unread"]  = summary.get("unread_count", 0)
            self._context["notification_critical"] = summary.get("critical_count", 0)
            self._record_success(
                "notification_center",
                f"total={summary.get('total_events', 0)} "
                f"unread={summary.get('unread_count', 0)} "
                f"critical={summary.get('critical_count', 0)} "
                f"external_enabled=False",
            )
        except Exception as exc:
            logger.warning("run_notification_center_report failed: %s", exc)
            self._record_fail("notification_center", str(exc))

    def run_portfolio_journal_summary(self):
        """
        Include Portfolio Journal summary in context (v0.4.6).
        Reads existing journal log — does NOT force a new report.
        Optional — failure does not abort overall run.
        """
        try:
            from gui.portfolio_journal_adapter import PortfolioJournalAdapter
            adapter = PortfolioJournalAdapter(mode=self.mode)
            summary = adapter.build_summary()
            self._context["journal_entries_count"]       = summary.get("entries_count", 0)
            self._context["journal_review_required_count"] = summary.get("review_required_count", 0)
            self._context["journal_latest_entry"]        = summary.get("latest_entry_at", "")
            self._context["journal_most_common_mistake"] = summary.get("most_common_mistake", "")
            self._record_success(
                "portfolio_journal",
                f"entries={summary.get('entries_count', 0)} "
                f"review_required={summary.get('review_required_count', 0)} "
                f"most_common_mistake={summary.get('most_common_mistake', '')}",
            )
        except Exception as exc:
            logger.warning("run_portfolio_journal_summary failed: %s", exc)
            self._record_fail("portfolio_journal", str(exc))

    def run_research_review_summary(self):
        """
        Include Research Review Dashboard summary in context (v0.4.7).
        Reads persisted review_summary.csv — does NOT run a full review.
        Optional — failure does not abort overall run.
        """
        try:
            from review.review_store import ResearchReviewStore
            store   = ResearchReviewStore()
            summary = store.load_latest_summary()
            if summary:
                self._context["research_review_score"]        = summary.get("overall_review_score", "")
                self._context["research_review_open_items"]   = summary.get("open_items", 0)
                self._context["research_review_critical_count"] = summary.get("critical_items", 0)
                self._context["research_review_action_items"] = summary.get("action_items_count", 0)
                self._context["research_review_top_mistake"]  = summary.get("most_common_mistake", "")
                self._record_success(
                    "research_review",
                    f"open={summary.get('open_items', 0)} "
                    f"critical={summary.get('critical_items', 0)}",
                )
            else:
                self._context["research_review_score"] = "UNKNOWN"
                self._record_success("research_review", "no persisted summary found")
        except Exception as exc:
            logger.warning("run_research_review_summary failed: %s", exc)

    def run_research_coach_summary(self):
        """
        Include Research Assistant / Coach summary in context (v0.4.8).
        Reads persisted coach_summary.csv — does NOT run a full coach session.
        Optional — failure does not abort overall run.
        """
        try:
            from coach.coach_store import ResearchCoachStore
            store   = ResearchCoachStore()
            summary = store.load_latest_summary()
            if summary:
                self._context["research_coach_recommendations"] = summary.get("total_recommendations", 0)
                self._context["research_coach_p0"]              = summary.get("p0_count", 0)
                self._context["research_coach_p1"]              = summary.get("p1_count", 0)
                self._context["research_coach_replay_tasks"]    = summary.get("replay_tasks_count", 0)
                self._context["research_coach_rule_reviews"]    = summary.get("rule_review_count", 0)
                self._context["research_coach_data_repairs"]    = summary.get("data_repair_count", 0)
                self._record_success(
                    "research_coach",
                    f"total={summary.get('total_recommendations', 0)} "
                    f"p0={summary.get('p0_count', 0)}",
                )
            else:
                self._context["research_coach_recommendations"] = 0
                self._record_success("research_coach", "no persisted coach summary found")
        except Exception as exc:
            logger.warning("run_research_coach_summary failed: %s", exc)

    def run_research_workflow_summary(self):
        """
        Include Research Workflow Automation summary in context (v0.4.9).
        Reads persisted workflow_summary.csv — does NOT run a full workflow.
        Optional — failure does not abort overall run.
        """
        try:
            from workflow_automation.workflow_store import ResearchWorkflowStore
            store   = ResearchWorkflowStore()
            summary = store.load_latest_summary()
            if summary:
                self._context["research_workflow_tasks_total"]   = summary.get("tasks_total", 0)
                self._context["research_workflow_failed_count"]  = summary.get("tasks_failed", 0)
                self._context["research_workflow_blocked_count"] = summary.get("tasks_skipped", 0)
                self._context["research_workflow_latest_id"]     = summary.get("workflow_id", "")
                self._context["research_workflow_package_path"]  = summary.get("output_package_path", "")
                self._record_success(
                    "research_workflow",
                    f"tasks={summary.get('tasks_total', 0)} "
                    f"failed={summary.get('tasks_failed', 0)}",
                )
            else:
                self._context["research_workflow_tasks_total"] = 0
                self._record_success("research_workflow", "no persisted workflow summary found")
        except Exception as exc:
            logger.warning("run_research_workflow_summary failed: %s", exc)

    def run_research_os_summary(self):
        """Collect Research OS Planning summary context (v0.5.0). Optional — failure does not abort run."""
        try:
            from os_planning.module_inventory import ResearchOSModuleInventory
            from os_planning.cli_inventory import CLIInventoryBuilder
            from os_planning.gui_tab_inventory import GUITabInventoryBuilder
            modules  = ResearchOSModuleInventory().build_inventory()
            commands = CLIInventoryBuilder().build_inventory()
            tabs     = GUITabInventoryBuilder().build_inventory()
            mature   = sum(1 for m in modules if m.get("maturity") == "STABLE")
            self._context["research_os_total_modules"]  = len(modules)
            self._context["research_os_total_commands"] = len(commands)
            self._context["research_os_total_tabs"]     = len(tabs)
            self._context["research_os_mature_count"]   = mature
            self._context["research_os_safety_score"]   = "N/A"
            self._record_success(
                "research_os",
                f"modules={len(modules)} cli={len(commands)} tabs={len(tabs)}",
            )
        except Exception as exc:
            logger.warning("run_research_os_summary failed: %s", exc)

    def run_cli_ux_summary(self):
        """Collect CLI UX summary context (v0.5.1). Optional — failure does not abort run."""
        try:
            from cli.cli_ux_report import CLIUXReportBuilder
            data = CLIUXReportBuilder().build()
            self._context["cli_commands_count"]  = data.get("commands_count",  0)
            self._context["cli_aliases_count"]   = data.get("alias_count",     0)
            self._context["cli_alias_conflicts"] = data.get("conflict_count",  0)
            self._context["cli_safety_status"]   = data.get("safety_status",   "N/A")
            self._record_success(
                "cli_ux",
                f"cmds={data.get('commands_count',0)} "
                f"aliases={data.get('alias_count',0)} "
                f"safety={data.get('safety_status','N/A')}",
            )
        except Exception as exc:
            logger.warning("run_cli_ux_summary failed: %s", exc)

    def run_gui_navigation_summary(self):
        """Collect GUI Navigation summary context (v0.5.2). Optional — failure does not abort run."""
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            from gui.navigation.navigation_report_data import GUINavigationReportData
            reg     = GUITabRegistry()
            data    = GUINavigationReportData(registry=reg)
            summary = data.build_summary()
            self._context["gui_tabs_count"]            = summary.get("total_tabs",    0)
            self._context["gui_groups_count"]          = summary.get("groups_count",  0)
            self._context["gui_navigation_safety_status"] = summary.get("safety_status", "PASS")
            self._record_success(
                "gui_navigation",
                f"tabs={summary.get('total_tabs', 0)} "
                f"groups={summary.get('groups_count', 0)} "
                f"safety={summary.get('safety_status', 'PASS')}",
            )
        except Exception as exc:
            logger.warning("run_gui_navigation_summary failed: %s", exc)

    def run_strategy_filter_summary(self):
        """Collect Strategy Filter Pack summary context (v0.5.1.1). Optional — failure does not abort run."""
        try:
            from strategy_filters.strategy_filter_pack import StrategyFilterPack
            pack = StrategyFilterPack(mode=self.mode)
            # Run on a minimal mock stock to confirm import and instantiation
            _demo = pack.run_financial_turnaround({"symbol": "DEMO"})
            self._context["strategy_filter_pack_version"] = pack.VERSION
            self._context["strategy_filter_research_only"] = True
            self._context["strategy_filter_no_real_orders"] = True
            self._record_success(
                "strategy_filter_pack",
                f"version={pack.VERSION} research_only=True no_real_orders=True",
            )
        except Exception as exc:
            logger.warning("run_strategy_filter_summary failed: %s", exc)

    def run_model_monitoring_report(self):
        """Generate Model Monitoring report (v0.4.3). Optional — failure does not abort run."""
        try:
            from gui.model_monitoring_adapter import ModelMonitoringAdapter
            result = ModelMonitoringAdapter(report_dir=self._out_dir).generate_report(mode=self.mode)
            if result.get("ok"):
                path = result.get("report_path", "")
                self._context["model_monitoring_report"] = path
                self._record_success("model_monitoring", path)
            else:
                self._record_fail("model_monitoring", result.get("error", "unknown"))
        except Exception as exc:
            self._record_fail("model_monitoring", str(exc))

    def run_ml_feature_store_report(self):
        """Generate ML Feature Store report (v0.4.2). Optional — failure does not abort run."""
        try:
            from gui.ml_feature_store_adapter import MLFeatureStoreAdapter
            result = MLFeatureStoreAdapter(report_dir=self._out_dir).generate_report(mode=self.mode)
            if result.get("ok"):
                path = result.get("report_path", "")
                self._context["ml_feature_store_report"] = path
                self._record_success("ml_feature_store", path)
            else:
                self._record_fail("ml_feature_store", result.get("error", "unknown"))
        except Exception as exc:
            self._record_fail("ml_feature_store", str(exc))

    def build_daily_market_summary(self):
        """Build daily market summary from all available context."""
        try:
            from reports.daily_market_summary import DailyMarketSummaryBuilder
            builder = DailyMarketSummaryBuilder(
                mode=self.mode,
                report_date=self.report_date,
                context=self._context,
                top_n=self.top_n,
            )
            path = builder.build(output_dir=self._out_dir)
            self._context["daily_summary_path"] = path
            self._record_success("daily_market_summary", path)
        except Exception as exc:
            self._record_fail("daily_market_summary", str(exc))

    def build_executive_summary(self) -> Optional[str]:
        """Build executive_summary.md from all available context."""
        try:
            path = os.path.join(self._out_dir, "executive_summary.md")
            lines = self._render_executive_summary()
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self._record_success("executive_summary", path)
            return path
        except Exception as exc:
            self._record_fail("executive_summary", str(exc))
            return None

    def build_report_index(self) -> Optional[str]:
        """Build index.md."""
        try:
            from reports.auto_report_index import AutoReportIndexBuilder
            builder = AutoReportIndexBuilder(
                report_date=self.report_date,
                mode=self.mode,
                generated=self._generated,
                failed=self._failed,
                context=self._context,
            )
            path = builder.build(output_dir=self._out_dir)
            return path
        except Exception as exc:
            self._record_fail("report_index", str(exc))
            return None

    def write_manifest(self) -> Optional[str]:
        """Write manifest.json."""
        try:
            # Data readiness from context
            uq = self._context.get("universe_quality_summary", {})
            conf_obj = uq.get("confidence", {})
            confidence = conf_obj.get("overall", "INSUFFICIENT") if isinstance(conf_obj, dict) else str(conf_obj)

            manifest = {
                "report_date":    self.report_date,
                "mode":           self.mode,
                "profile":        self.profile,
                "generated_at":   datetime.now().isoformat(),
                "output_dir":     self._out_dir,
                "version":        self.VERSION,
                "reports": [
                    {"name": r["name"], "path": r.get("path"), "status": "ok"}
                    for r in self._generated
                ],
                "failed_reports": [
                    {"name": r["name"], "error": r.get("error")}
                    for r in self._failed
                ],
                "data_readiness": {
                    "universe_size":    uq.get("universe_size", 0),
                    "short_ready":      uq.get("short_ready_count", uq.get("short_term_ready_count", 0)),
                    "mid_ready":        uq.get("mid_ready_count",   uq.get("mid_term_ready_count",   0)),
                    "long_ready":       uq.get("long_ready_count",  uq.get("long_term_ready_count",  0)),
                },
                "confidence":   confidence,
                "safety_flags": {
                    "research_only":          True,
                    "simulation_only":        True,
                    "no_real_orders":         True,
                    "does_not_auto_apply_weights": True,
                    "does_not_connect_broker_api": True,
                },
                "version_info": {
                    "auto_report_center": self.VERSION,
                    "cockpit":            "v0.3.16",
                },
            }
            path = os.path.join(self._out_dir, "manifest.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            logger.info("Manifest written: %s", path)
            return path
        except Exception as exc:
            logger.error("write_manifest failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Executive summary renderer
    # ------------------------------------------------------------------

    def _render_executive_summary(self) -> List[str]:
        uq  = self._context.get("universe_quality_summary", {})
        sq  = self._context.get("signal_quality_results", {})
        pf  = self._context.get("portfolio_results", {})
        rw  = self._context.get("rule_weight_results", {})
        conf_obj = uq.get("confidence", {})
        confidence = conf_obj.get("overall", "OBSERVATIONAL") if isinstance(conf_obj, dict) else str(conf_obj) or "OBSERVATIONAL"

        lines = [
            f"# Executive Summary — TW Quant Cockpit {self.VERSION}",
            "",
            f"> **Generated**: {self.report_date}  ",
            f"> **Mode**: {self.mode}  ",
            f"> **Profile**: {self.profile}  ",
            "",
            "> **[!] Research Only. Simulation Only. No Real Orders.**  ",
            "> **[!] Does NOT auto-apply weights. Does NOT modify strategy.**  ",
            "> Not investment advice.",
            "",
            "---",
            "",
            "## Summary",
            "",
        ]

        # Data readiness
        lines += [
            "### Data Readiness",
            "",
            f"- Universe size     : {uq.get('universe_size', '—')}",
            f"- Short-term ready  : {uq.get('short_ready_count', uq.get('short_term_ready_count', '—'))}",
            f"- Mid-term ready    : {uq.get('mid_ready_count',   uq.get('mid_term_ready_count',   '—'))}",
            f"- Long-term ready   : {uq.get('long_ready_count',  uq.get('long_term_ready_count',  '—'))}",
            f"- Statistical conf  : **{confidence}**",
            "",
        ]

        # Portfolio
        primary_m = (pf.get("primary") or {}).get("metrics", {}) if pf else {}
        if primary_m:
            lines += [
                "### Portfolio Simulation (balanced scenario)",
                "",
                f"- Total return  : {_pct(primary_m.get('total_return'))}",
                f"- Sharpe        : {primary_m.get('sharpe', '—')}",
                f"- Max drawdown  : {_pct(primary_m.get('max_drawdown'))}",
                f"- Profit factor : {primary_m.get('profit_factor', '—')}",
                f"- Trade count   : {primary_m.get('trade_count', '—')}",
                "",
            ]

        # Signal quality
        sq_df = sq.get("summary_df") if sq else None
        if sq_df is not None and hasattr(sq_df, "empty") and not sq_df.empty:
            try:
                counts = sq_df["recommendation"].value_counts().to_dict() if "recommendation" in sq_df.columns else {}
                lines += [
                    "### Signal Quality",
                    "",
                    f"- BOOST         : {counts.get('BOOST', 0)}",
                    f"- KEEP          : {counts.get('KEEP', 0)}",
                    f"- REDUCE        : {counts.get('REDUCE', 0)}",
                    f"- DISABLE       : {counts.get('DISABLE', 0)}",
                    f"- INSUFFICIENT  : {counts.get('INSUFFICIENT_SAMPLE', 0)}",
                    "",
                ]
            except Exception:
                pass

        # Rule weight
        rw_best = rw.get("best_config") if rw else None
        if rw_best:
            lines += [
                "### Rule Weight Tuning",
                "",
                f"- Best config   : `{rw_best.name}`",
                f"- Description   : {rw_best.description[:80]}",
                "",
            ]

        # Reports generated / failed
        lines += [
            "### Report Generation",
            "",
            f"- Generated : {len(self._generated)}",
            f"- Failed    : {len(self._failed)}",
        ]
        if self._failed:
            lines.append("")
            for f in self._failed:
                lines.append(f"  - [FAIL] {f['name']}: {str(f.get('error',''))[:80]}")
        lines.append("")

        # Not-recommended section
        lines += [
            "---",
            "",
            "## Advisory — Do NOT",
            "",
            "- Do NOT chase stocks with no_chase_warning",
            "- Do NOT auto-apply rule weight tuning results",
            "- Do NOT place real orders based on this report",
            "- Do NOT treat OBSERVATIONAL confidence as RELIABLE",
            "- Do NOT use TIMING_ESTIMATED announcement dates as fact",
            "",
            "---",
            "",
            "## Next Steps",
            "",
            "- Expand universe to ≥ 30 symbols for OBSERVATIONAL → RELIABLE",
            "- Import actual MOPS announcement dates (reduce timing_estimated)",
            "- Add more intraday history for microstructure signal quality",
            "- Review rule weight tuning results before any manual adjustment",
            "",
            "---",
            "",
            "*TW Quant Cockpit — Research Only / Simulation Only / No Real Orders*",
        ]
        return lines

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_output_dirs(self):
        for sub in ["stock_reports", "signal_quality", "portfolio",
                    "rule_weight", "long_term", "strategy_knowledge",
                    "universe_quality"]:
            os.makedirs(os.path.join(self._out_dir, sub), exist_ok=True)

    def _load_universe_symbols(self) -> List[str]:
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, _ = _resolve_csv("profile")
            if path:
                rows = _read_csv_rows(path)
                return [r["symbol"] for r in rows if r.get("symbol")]
        except Exception:
            pass
        return []

    def run_regression_consolidation_summary(self) -> None:
        """v0.5.3: Run quick regression suite and record summary (never crashes)."""
        try:
            from gui.regression_suite_adapter import RegressionSuiteAdapter
            adapter = RegressionSuiteAdapter()
            result  = adapter.run_suite("quick", mode=self.mode)
            self._context["regression_consolidation"] = {
                "suite":          result.get("suite", "quick"),
                "status":         result.get("status", "UNKNOWN"),
                "total":          result.get("total", 0),
                "passed":         result.get("passed", 0),
                "failed":         result.get("failed", 0),
                "warnings":       result.get("warnings", 0),
                "coverage_score": adapter.get_coverage_score(),
            }
            self._record_success("regression_consolidation_summary", None)
        except Exception as exc:
            logger.warning("AutoReportCenter.run_regression_consolidation_summary: %s", exc)
            self._context["regression_consolidation"] = {}

    def run_data_stabilization_summary(self) -> None:
        """v0.5.5: Load data stabilization summary (never crashes, no recursive loop)."""
        try:
            from gui.data_stabilization_adapter import DataStabilizationAdapter
            adapter = DataStabilizationAdapter()
            # Load latest saved summary only — does NOT run full stabilization engine
            summary = adapter.load_latest_summary()
            self._context["data_stabilization"] = {
                "overall_status":   summary.get("overall_status", "UNKNOWN"),
                "health_score":     summary.get("health_score", 0.0),
                "readiness_score":  summary.get("readiness_score", 0.0),
                "leakage_warnings": summary.get("leakage_warnings", 0),
                "datasets_checked": summary.get("datasets_checked", 0),
                "feature_groups":   summary.get("feature_groups_checked", 0),
            }
            report_path = adapter.load_latest_report_path()
            self._record_success("data_stabilization_summary", report_path)
        except Exception as exc:
            logger.warning("AutoReportCenter.run_data_stabilization_summary: %s", exc)
            self._context["data_stabilization"] = {}

    def run_replay_training_summary(self) -> None:
        """v0.5.6: Load replay training summary (never crashes, no recursive loop).

        [!] Replay Training Only. Research Only. No Real Orders.
        """
        try:
            from gui.replay_training_adapter import ReplayTrainingAdapter
            adapter = ReplayTrainingAdapter()
            result  = adapter.load_latest_summary()
            summary = result.get("summary", {}) if result.get("ok") else {}
            self._context["replay_training"] = {
                "latest_session_id":        summary.get("latest_session_id", ""),
                "latest_symbol":            summary.get("latest_symbol", ""),
                "latest_score":             summary.get("latest_score", 0.0),
                "mistakes_count":           summary.get("mistakes_count", 0),
                "drills_count":             summary.get("drills_count", 0),
                "hidden_future_data":       True,
                "latest_replay_training_at": summary.get("latest_replay_training_at", ""),
                "no_real_orders":           True,
            }
            report_path = adapter.load_latest_report_path()
            self._record_success("replay_training_summary", report_path)
        except Exception as exc:
            logger.warning("AutoReportCenter.run_replay_training_summary: %s", exc)
            self._context["replay_training"] = {}

    def run_stable_release_v060_summary(self) -> None:
        """v0.6.0: Load stable release summary (never crashes, no recursive loop).

        IMPORTANT: Does NOT call auto_report_center full — avoids recursive loop.
        Reads capability matrix summary only.

        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        try:
            from stable_release.capability_matrix import StableCapabilityMatrix
            matrix = StableCapabilityMatrix()
            matrix.build()
            caps = matrix.list_capabilities()
            by_status: dict = {}
            for c in caps:
                by_status[c.status] = by_status.get(c.status, 0) + 1
            self._context["stable_release_v060"] = {
                "version":            "v0.6.0",
                "capability_count":   len(caps),
                "stable_count":       by_status.get("STABLE", 0),
                "usable_count":       by_status.get("USABLE", 0),
                "no_real_orders":     True,
                "production_blocked": True,
            }
            self._record_success(
                "stable_release_v060_summary",
                "",  # no file path — summary only
            )
        except Exception as exc:
            logger.warning("AutoReportCenter.run_stable_release_v060_summary: %s", exc)
            self._context["stable_release_v060"] = {}

    def run_report_pack_summary(self) -> None:
        """v0.5.4: Build daily report pack summary (never crashes, no recursive loop)."""
        try:
            from gui.report_pack_adapter import ReportPackAdapter
            adapter = ReportPackAdapter()
            # Build daily pack only — does NOT call auto_report_center full (avoids recursive loop)
            result = adapter.build_pack(pack_type="daily", generate_missing=False)
            self._context["report_pack"] = {
                "pack_type":    result.get("pack_type", "daily"),
                "status":       result.get("status", "UNKNOWN"),
                "health_score": result.get("health_score", 0.0),
                "ready_count":  result.get("ready_count", 0),
                "missing_count": result.get("missing_count", 0),
            }
            self._record_success("report_pack_summary", result.get("index_path"))
        except Exception as exc:
            logger.warning("AutoReportCenter.run_report_pack_summary: %s", exc)
            self._context["report_pack"] = {}

    def run_intelligence_stable_summary(self) -> None:
        """v0.8.0: Load intelligence stable summary (never crashes, no recursive loop).

        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        try:
            from gui.intelligence_stable_adapter import IntelligenceStableAdapter
            adapter = IntelligenceStableAdapter()
            summary = adapter.load_latest_summary()
            self._context["intelligence_stable"] = {
                "version":            summary.get("version", "v0.8.0"),
                "overall_status":     summary.get("overall_status", "UNKNOWN"),
                "total_capabilities": summary.get("total_capabilities", 0),
                "stable_count":       summary.get("stable_count", 0),
                "pass_count":         summary.get("pass_count", 0),
                "warn_count":         summary.get("warn_count", 0),
                "fail_count":         summary.get("fail_count", 0),
                "forbidden_action_count": summary.get("forbidden_action_count", 0),
                "no_real_orders":     True,
                "production_blocked": True,
            }
            report_path = adapter.load_latest_report_path()
            self._record_success("intelligence_stable_summary", report_path or "")
        except Exception as exc:
            logger.warning("AutoReportCenter.run_intelligence_stable_summary: %s", exc)
            self._context["intelligence_stable"] = {}

    def _record_success(self, name: str, path: Optional[str], extra: dict = None):
        entry = {
            "name": name,
            "status": "ok",
            "path": path,
            "generated_at": datetime.now().isoformat(),
        }
        if extra:
            entry.update(extra)
        self._generated.append(entry)
        logger.info("AutoReportCenter: [OK] %s -> %s", name, path)

    def _record_fail(self, name: str, error: str, tb_short: str = ""):
        entry = {
            "name":           name,
            "status":         "failed",
            "error":          error,
            "traceback_short": tb_short or traceback.format_exc()[-400:],
            "timestamp":      datetime.now().isoformat(),
        }
        self._failed.append(entry)
        logger.warning("AutoReportCenter: [FAIL] %s — %s", name, error)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _pct(v, sign=True) -> str:
    if v is None:
        return "—"
    try:
        f = float(v)
        return f"{f*100:+.2f}%" if sign else f"{f*100:.2f}%"
    except Exception:
        return str(v)


def _sq_counts(results: dict) -> dict:
    df = results.get("summary_df")
    if df is None or not hasattr(df, "empty") or df.empty:
        return {}
    if "recommendation" not in df.columns:
        return {}
    return df["recommendation"].value_counts().to_dict()
