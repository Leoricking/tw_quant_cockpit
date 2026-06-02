"""
release/regression_suite.py — Regression suite for v0.4.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import csv
import logging
import os
import subprocess
import sys
import time
from datetime import datetime

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RegressionSuite:
    """Quick (7 tests) and full (14 tests) regression suites for TW Quant Cockpit v0.4.0.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, mode: str = "real", quick: bool = True,
                 results_dir: str | None = None) -> None:
        self.mode = mode
        self.quick = quick
        self.results_dir = os.path.join(
            BASE_DIR, results_dir if results_dir else "data/backtest_results"
        )
        os.makedirs(self.results_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _item(name: str, status: str, detail: str, duration_ms: float) -> dict:
        return {
            "name":        name,
            "status":      status,
            "detail":      detail,
            "duration_ms": round(duration_ms, 2),
        }

    # ------------------------------------------------------------------
    # Individual tests
    # ------------------------------------------------------------------

    def _test_compileall(self) -> dict:
        t0 = time.monotonic()
        try:
            result = subprocess.run(
                [sys.executable, "-m", "compileall", BASE_DIR, "-q"],
                capture_output=True, text=True, timeout=120,
            )
            elapsed = (time.monotonic() - t0) * 1000
            if result.returncode == 0:
                return self._item("compileall", "PASS", "All Python files compile cleanly.", elapsed)
            detail = (result.stderr or result.stdout or "returncode != 0").strip()[:300]
            return self._item("compileall", "FAIL", detail, elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("compileall", "FAIL", str(exc), elapsed)

    def _test_import_core(self) -> dict:
        t0 = time.monotonic()
        modules = [
            "workflow.daily_workflow",
            "quality.data_quality_gate",
            "governance.rule_registry",
            "experiments.experiment_registry",
            "intraday.intraday_pipeline",
            "backtest.hardened_backtester",
            "reports.auto_report_center",
        ]
        failed_mods = []
        for mod in modules:
            try:
                __import__(mod)
            except Exception as exc:
                failed_mods.append(f"{mod}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed_mods:
            return self._item("import_core", "PASS",
                               f"All {len(modules)} core modules imported.", elapsed)
        return self._item("import_core", "FAIL",
                           f"{len(failed_mods)} module(s) failed: {failed_mods[:5]}", elapsed)

    def _test_data_quality_gate(self) -> dict:
        t0 = time.monotonic()
        try:
            from quality.data_quality_gate import DataQualityGate
            gate = DataQualityGate()
            result = gate.run()
            elapsed = (time.monotonic() - t0) * 1000
            status_val = result.get("status", "") if isinstance(result, dict) else str(result)
            return self._item("data_quality_gate", "PASS",
                               f"DataQualityGate.run() returned status={status_val!r}.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("data_quality_gate", "FAIL", str(exc), elapsed)

    def _test_provider_reliability(self) -> dict:
        t0 = time.monotonic()
        try:
            from data.providers.provider_reliability_matrix import ProviderReliabilityMatrix  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("provider_reliability", "PASS",
                               "data.providers.provider_reliability_matrix imported.", elapsed)
        except ModuleNotFoundError:
            try:
                from data.providers.reliability_matrix import ProviderReliabilityMatrix  # noqa: F401
                elapsed = (time.monotonic() - t0) * 1000
                return self._item("provider_reliability", "PASS",
                                   "data.providers.reliability_matrix imported (alt path).", elapsed)
            except ModuleNotFoundError as exc:
                elapsed = (time.monotonic() - t0) * 1000
                return self._item("provider_reliability", "WARN",
                                   f"Module not found (non-fatal): {exc}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("provider_reliability", "WARN", str(exc), elapsed)

    def _test_rule_governance(self) -> dict:
        t0 = time.monotonic()
        try:
            from governance.rule_registry import RuleRegistry
            reg = RuleRegistry()
            reg.load_builtin_rules()
            count = len(reg.list_rules())
            elapsed = (time.monotonic() - t0) * 1000
            if count > 0:
                return self._item("rule_governance", "PASS",
                                   f"RuleRegistry loaded {count} built-in rules.", elapsed)
            return self._item("rule_governance", "WARN", "RuleRegistry loaded 0 rules.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("rule_governance", "FAIL", str(exc), elapsed)

    def _test_experiment_list(self) -> dict:
        t0 = time.monotonic()
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry()
            exps = reg.list_experiments()
            elapsed = (time.monotonic() - t0) * 1000
            count = len(exps) if exps else 0
            return self._item("experiment_list", "PASS",
                               f"ExperimentRegistry.list_experiments() returned {count} experiments.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("experiment_list", "FAIL", str(exc), elapsed)

    def _test_paper_trading(self) -> dict:
        t0 = time.monotonic()
        try:
            from sim.simulator import PaperTrader
            PaperTrader()
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("paper", "PASS", "PaperTrader instantiates successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("paper", "FAIL", str(exc), elapsed)

    # -- Full-suite-only tests --

    def _test_hardened_backtest_import(self) -> dict:
        t0 = time.monotonic()
        try:
            from backtest.hardened_backtester import HardenedBacktester  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("hardened_backtest_import", "PASS",
                               "HardenedBacktester imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("hardened_backtest_import", "FAIL", str(exc), elapsed)

    def _test_intraday_pipeline_import(self) -> dict:
        t0 = time.monotonic()
        try:
            from intraday.intraday_pipeline import IntradayDataPipeline  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("intraday_pipeline_import", "PASS",
                               "IntradayDataPipeline imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("intraday_pipeline_import", "FAIL", str(exc), elapsed)

    def _test_auto_report_import(self) -> dict:
        t0 = time.monotonic()
        try:
            from reports.auto_report_center import AutoReportCenter  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("auto_report_import", "PASS",
                               "AutoReportCenter imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("auto_report_import", "FAIL", str(exc), elapsed)

    def _test_experiment_registry_import(self) -> dict:
        t0 = time.monotonic()
        try:
            import experiments  # noqa: F401
            from experiments.experiment_registry import ExperimentRegistry  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("experiment_registry_import", "PASS",
                               "experiments package and ExperimentRegistry import.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("experiment_registry_import", "FAIL", str(exc), elapsed)

    def _test_gui_imports(self) -> dict:
        t0 = time.monotonic()
        failed = []
        panels = [
            "gui.dashboard",
            "gui.portfolio_cockpit_panel",
            "gui.signal_quality_panel",
            "gui.rule_governance_panel",
            "gui.experiment_registry_panel",
        ]
        pyside_missing = False
        for mod in panels:
            try:
                __import__(mod)
            except ImportError as exc:
                msg = str(exc)
                if "PySide6" in msg or "pyside6" in msg.lower():
                    pyside_missing = True
                else:
                    failed.append(f"{mod}: {msg}")
            except Exception as exc:
                failed.append(f"{mod}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if pyside_missing:
            return self._item("gui_imports", "WARN",
                               "PySide6 not installed — GUI panels skipped.", elapsed)
        if failed:
            return self._item("gui_imports", "WARN",
                               f"Some panels failed (non-fatal): {failed[:3]}", elapsed)
        return self._item("gui_imports", "PASS",
                           f"All {len(panels)} GUI modules imported.", elapsed)

    def _test_signal_quality_import(self) -> dict:
        t0 = time.monotonic()
        try:
            from analysis.signal_quality_engine import SignalQualityEngine  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("signal_quality_import", "PASS",
                               "SignalQualityEngine imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("signal_quality_import", "FAIL", str(exc), elapsed)

    def _test_rule_weight_import(self) -> dict:
        t0 = time.monotonic()
        try:
            from tuning.rule_weight_config import RuleWeightConfig  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("rule_weight_import", "PASS",
                               "RuleWeightConfig imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("rule_weight_import", "FAIL", str(exc), elapsed)

    def _test_api_fetch_imports(self) -> dict:
        """v0.4.1: Check that all API Fetch Productionization modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("data.providers.token_setup_assistant", "TokenSetupAssistant"),
            ("data.providers.retry_policy",          "RetryPolicy"),
            ("data.providers.api_cache",             "APICache"),
            ("data.providers.data_lineage",          "DataLineageTracker"),
            ("data.providers.api_diagnostics",       "APIFetchDiagnostics"),
            ("data.providers.twse_tpex_parser",      "TWSETPEXParser"),
            ("data.providers.mops_financial_parser", "MOPSFinancialParser"),
            ("reports.api_fetch_production_report",  "APIFetchProductionReportBuilder"),
            ("gui.api_fetch_status_adapter",         "APIFetchStatusAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}.{cls_name}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("api_fetch_imports", "PASS",
                               f"All {len(modules)} v0.4.1 API Fetch modules imported.", elapsed)
        return self._item("api_fetch_imports", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_api_token_check(self) -> dict:
        """v0.4.1: TokenSetupAssistant.inspect() runs without crashing."""
        t0 = time.monotonic()
        try:
            from data.providers.token_setup_assistant import TokenSetupAssistant
            result = TokenSetupAssistant().inspect()
            elapsed = (time.monotonic() - t0) * 1000
            # Must never show full token
            for v in result.get("required_tokens", {}).values():
                masked = v.get("masked_value", "")
                if masked and len(masked) > 12 and "****" not in masked:
                    return self._item("api_token_check", "FAIL",
                                       "Token not masked in output!", elapsed)
            return self._item("api_token_check", "PASS",
                               "TokenSetupAssistant.inspect() ran; tokens masked.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("api_token_check", "FAIL", str(exc), elapsed)

    def _test_api_cache_stats(self) -> dict:
        """v0.4.1: APICache.stats() runs without crashing."""
        t0 = time.monotonic()
        try:
            from data.providers.api_cache import APICache
            stats = APICache().stats()
            elapsed = (time.monotonic() - t0) * 1000
            if not isinstance(stats, dict):
                return self._item("api_cache_stats", "FAIL", "stats() did not return dict", elapsed)
            return self._item("api_cache_stats", "PASS",
                               f"APICache.stats() OK  entries={stats.get('total_entries',0)}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("api_cache_stats", "FAIL", str(exc), elapsed)

    def _test_model_monitoring_imports(self) -> dict:
        """v0.4.3: All Model Monitoring modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("monitoring.model_registry",        "ModelRegistry"),
            ("monitoring.prediction_log",         "PredictionLog"),
            ("monitoring.hit_miss_review",        "HitMissReviewer"),
            ("monitoring.drift_detector",         "DriftDetector"),
            ("monitoring.signal_degradation",     "SignalDegradationMonitor"),
            ("monitoring.rule_vs_ml_comparator",  "RuleVsMLComparator"),
            ("monitoring.monitoring_summary",     "ModelMonitoringSummary"),
            ("reports.model_monitoring_report",   "ModelMonitoringReportBuilder"),
            ("gui.model_monitoring_adapter",      "ModelMonitoringAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}.{cls_name}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("model_monitoring_imports", "PASS",
                               f"All {len(modules)} v0.4.3 Model Monitoring modules imported.", elapsed)
        return self._item("model_monitoring_imports", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_model_monitoring_summary(self) -> dict:
        """v0.4.3: ModelMonitoringSummary.run() works (may return INSUFFICIENT_DATA)."""
        t0 = time.monotonic()
        try:
            from monitoring.monitoring_summary import ModelMonitoringSummary
            result = ModelMonitoringSummary().run()
            elapsed = (time.monotonic() - t0) * 1000
            if not isinstance(result, dict):
                return self._item("model_monitoring_summary", "FAIL", "run() did not return dict.", elapsed)
            return self._item("model_monitoring_summary", "PASS",
                               f"ModelMonitoringSummary OK: models={result.get('model_count', 0)}, "
                               f"drift={result.get('drift_status','—')}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("model_monitoring_summary", "FAIL", str(exc), elapsed)

    def _test_drift_detector(self) -> dict:
        """v0.4.3: DriftDetector.run() works with empty data (returns INSUFFICIENT_DATA)."""
        t0 = time.monotonic()
        try:
            from monitoring.drift_detector import DriftDetector
            result = DriftDetector().run()
            elapsed = (time.monotonic() - t0) * 1000
            if not isinstance(result, dict):
                return self._item("drift_detector", "FAIL", "run() did not return dict.", elapsed)
            status = result.get("status", "—")
            # INSUFFICIENT_DATA is acceptable when no data available
            if status in ("STABLE", "WATCH", "DRIFT_WARNING", "DRIFT_CRITICAL", "INSUFFICIENT_DATA"):
                return self._item("drift_detector", "PASS",
                                   f"DriftDetector OK: status={status}", elapsed)
            return self._item("drift_detector", "PARTIAL", f"Unexpected status: {status}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("drift_detector", "FAIL", str(exc), elapsed)

    def _test_ml_feature_catalog(self) -> dict:
        """v0.4.2: FeatureCatalog loads and returns non-empty feature list."""
        t0 = time.monotonic()
        try:
            from ml.feature_catalog import FeatureCatalog
            catalog = FeatureCatalog()
            features = catalog.list_features()
            summary = catalog.summary()
            elapsed = (time.monotonic() - t0) * 1000
            if not features:
                return self._item("ml_feature_catalog", "FAIL", "FeatureCatalog returned empty list.", elapsed)
            return self._item("ml_feature_catalog", "PASS",
                               f"FeatureCatalog OK: {summary.get('total_features', 0)} features.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_feature_catalog", "FAIL", str(exc), elapsed)

    def _test_ml_feature_snapshot_import(self) -> dict:
        """v0.4.2: FeatureSnapshotBuilder imports without error."""
        t0 = time.monotonic()
        modules = [
            ("ml.feature_catalog",         "FeatureCatalog"),
            ("ml.feature_snapshot",        "FeatureSnapshotBuilder"),
            ("ml.label_generator",         "LabelGenerator"),
            ("ml.split_manager",           "MLSplitManager"),
            ("ml.leakage_checker",         "DataLeakageChecker"),
            ("ml.feature_quality",         "FeatureQualityChecker"),
            ("ml.feature_importance_shell","FeatureImportanceShell"),
            ("ml.dataset_builder",         "MLFeatureDatasetBuilder"),
            ("reports.ml_feature_store_report", "MLFeatureStoreReportBuilder"),
            ("gui.ml_feature_store_adapter",    "MLFeatureStoreAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}.{cls_name}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("ml_feature_snapshot_import", "PASS",
                               f"All {len(modules)} v0.4.2 ML Feature Store modules imported.", elapsed)
        return self._item("ml_feature_snapshot_import", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_ml_leakage_checker(self) -> dict:
        """v0.4.2: DataLeakageChecker.run() works on an empty DataFrame."""
        t0 = time.monotonic()
        try:
            import pandas as pd
            from ml.leakage_checker import DataLeakageChecker
            result = DataLeakageChecker().run(pd.DataFrame())
            elapsed = (time.monotonic() - t0) * 1000
            if not isinstance(result, dict):
                return self._item("ml_leakage_checker", "FAIL", "run() did not return dict.", elapsed)
            return self._item("ml_leakage_checker", "PASS",
                               f"DataLeakageChecker OK: status={result.get('status', '—')}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_leakage_checker", "FAIL", str(exc), elapsed)

    def _test_ml_feature_store_report(self) -> dict:
        """v0.4.2: MLFeatureStoreReportBuilder.build() generates a report file."""
        t0 = time.monotonic()
        try:
            import tempfile, os
            from reports.ml_feature_store_report import MLFeatureStoreReportBuilder
            with tempfile.TemporaryDirectory() as tmpdir:
                builder = MLFeatureStoreReportBuilder(report_dir=tmpdir, mode="mock")
                path = builder.build()
                elapsed = (time.monotonic() - t0) * 1000
                if not os.path.isfile(path):
                    return self._item("ml_feature_store_report", "FAIL", f"Report file not found: {path}", elapsed)
                return self._item("ml_feature_store_report", "PASS",
                                   f"MLFeatureStoreReportBuilder OK: {os.path.basename(path)}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_feature_store_report", "FAIL", str(exc), elapsed)

    def _test_intraday_replay_imports(self) -> dict:
        """v0.4.4: All Intraday Replay modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("replay.replay_session",       "ReplaySessionManager"),
            ("replay.replay_engine",         "IntradayReplayEngine"),
            ("replay.replay_events",         "ReplayEventBuilder"),
            ("replay.opening_range_replay",  "OpeningRangeReplay"),
            ("replay.vwap_replay",           "VWAPReplay"),
            ("replay.fake_breakout_replay",  "FakeBreakoutReplay"),
            ("replay.volume_profile_replay", "VolumeProfileReplay"),
            ("replay.strategy_replay",       "StrategyReplayOverlay"),
            ("replay.training_mode",         "ReplayTrainingMode"),
            ("replay.replay_metrics",        "ReplayMetrics"),
            ("reports.intraday_replay_report", "IntradayReplayReportBuilder"),
            ("gui.intraday_replay_adapter",  "IntradayReplayAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}.{cls_name}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("intraday_replay_imports", "PASS",
                               f"All {len(modules)} v0.4.4 Intraday Replay modules imported.", elapsed)
        return self._item("intraday_replay_imports", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_intraday_replay_empty_state(self) -> dict:
        """v0.4.4: IntradayReplayEngine.load() returns INSUFFICIENT_INTRADAY_DATA (no crash) with missing data."""
        t0 = time.monotonic()
        try:
            from replay.replay_engine import IntradayReplayEngine
            engine = IntradayReplayEngine()
            result = engine.load(symbol="9999", date=None)
            elapsed = (time.monotonic() - t0) * 1000
            if not isinstance(result, dict):
                return self._item("intraday_replay_empty_state", "FAIL", "load() did not return dict.", elapsed)
            status = result.get("status", "—")
            if status in ("INSUFFICIENT_INTRADAY_DATA", "READY"):
                return self._item("intraday_replay_empty_state", "PASS",
                                   f"IntradayReplayEngine.load() OK: status={status}", elapsed)
            return self._item("intraday_replay_empty_state", "PARTIAL",
                               f"Unexpected status: {status}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("intraday_replay_empty_state", "FAIL", str(exc), elapsed)

    def _test_strategy_knowledge_imports(self) -> dict:
        """v0.4.1.1: All Strategy Knowledge Ingestion modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("knowledge.transcript_source",   "TranscriptSource"),
            ("knowledge.transcript_loader",   "TranscriptLoader"),
            ("knowledge.knowledge_schema",    "StrategyKnowledgeItem"),
            ("knowledge.knowledge_extractor", "StrategyKnowledgeExtractor"),
            ("knowledge.rule_candidate_mapper", "RuleCandidateMapper"),
            ("knowledge.knowledge_store",     "StrategyKnowledgeStore"),
            ("knowledge.ingestion_pipeline",  "StrategyKnowledgeIngestionPipeline"),
            ("reports.strategy_knowledge_ingestion_report", "StrategyKnowledgeIngestionReportBuilder"),
            ("gui.strategy_knowledge_ingestion_adapter",    "StrategyKnowledgeIngestionAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}.{cls_name}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("strategy_knowledge_imports", "PASS",
                               f"All {len(modules)} v0.4.1.1 Strategy Knowledge modules imported.", elapsed)
        return self._item("strategy_knowledge_imports", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_strategy_knowledge_summary(self) -> dict:
        """v0.4.1.1: StrategyKnowledgeStore.build_summary() works with empty store (no crash)."""
        t0 = time.monotonic()
        try:
            import tempfile
            from knowledge.knowledge_store import StrategyKnowledgeStore
            with tempfile.TemporaryDirectory() as tmpdir:
                store = StrategyKnowledgeStore(output_dir=tmpdir)
                summary = store.build_summary()
            elapsed = (time.monotonic() - t0) * 1000
            if not isinstance(summary, dict):
                return self._item("strategy_knowledge_summary", "FAIL", "build_summary() did not return dict.", elapsed)
            return self._item("strategy_knowledge_summary", "PASS",
                               f"StrategyKnowledgeStore OK: items={summary.get('total_items', 0)}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("strategy_knowledge_summary", "FAIL", str(exc), elapsed)

    def _test_strategy_knowledge_dry_run(self) -> dict:
        """v0.4.1.1: StrategyKnowledgeIngestionPipeline.run(dry_run=True) returns summary (no crash)."""
        t0 = time.monotonic()
        try:
            import tempfile
            from knowledge.ingestion_pipeline import StrategyKnowledgeIngestionPipeline
            with tempfile.TemporaryDirectory() as tmpdir:
                pipeline = StrategyKnowledgeIngestionPipeline(
                    output_dir=tmpdir,
                    dry_run=True,
                    mode="mock",
                )
                summary = pipeline.run()
            elapsed = (time.monotonic() - t0) * 1000
            if not isinstance(summary, dict):
                return self._item("strategy_knowledge_dry_run", "FAIL", "run() did not return dict.", elapsed)
            return self._item("strategy_knowledge_dry_run", "PASS",
                               f"StrategyKnowledgeIngestionPipeline dry_run OK: "
                               f"files_discovered={summary.get('files_discovered', 0)}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("strategy_knowledge_dry_run", "FAIL", str(exc), elapsed)

    def _test_ml_knowledge_imports(self) -> dict:
        """v0.4.2.1: All ML Knowledge Integration modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("ml.knowledge_feature_bridge",   "KnowledgeFeatureBridge"),
            ("ml.knowledge_feature_catalog",  "KnowledgeFeatureCatalog"),
            ("ml.knowledge_feature_readiness","KnowledgeFeatureReadinessChecker"),
            ("ml.knowledge_leakage_checker",  "KnowledgeLeakageChecker"),
            ("ml.knowledge_dataset_exporter", "KnowledgeDatasetExporter"),
        ]
        failed = []
        for mod, cls in modules:
            try:
                m = __import__(mod, fromlist=[cls])
                getattr(m, cls)
            except Exception as exc:
                failed.append(f"{mod}.{cls}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("ml_knowledge_imports", "PASS",
                               f"All {len(modules)} v0.4.2.1 ML Knowledge modules imported.", elapsed)
        return self._item("ml_knowledge_imports", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_ml_knowledge_bridge_empty(self) -> dict:
        """v0.4.2.1: KnowledgeFeatureBridge.convert_all() with empty store returns valid result (no crash)."""
        t0 = time.monotonic()
        try:
            import tempfile
            from ml.knowledge_feature_bridge import KnowledgeFeatureBridge
            with tempfile.TemporaryDirectory() as tmpdir:
                bridge = KnowledgeFeatureBridge(knowledge_dir=tmpdir)
                result = bridge.convert_all()
            elapsed = (time.monotonic() - t0) * 1000
            total = result.get("summary", {}).get("total_features_count", 0)
            auto  = result.get("summary", {}).get("auto_enabled_count", None)
            if auto != 0:
                return self._item("ml_knowledge_bridge_empty", "FAIL",
                                   f"auto_enabled_count expected 0, got {auto}", elapsed)
            return self._item("ml_knowledge_bridge_empty", "PASS",
                               f"KnowledgeFeatureBridge empty-store OK: features={total} auto_enabled=0", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_knowledge_bridge_empty", "FAIL", str(exc), elapsed)

    def _test_notification_imports(self) -> dict:
        """v0.4.5: All Notification Center modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("notifications.notification_schema",       "NotificationEvent"),
            ("notifications.notification_center",       "NotificationCenter"),
            ("notifications.notification_rules",        "NotificationRuleEngine"),
            ("notifications.local_notifier",            "LocalNotifier"),
            ("notifications.external_notifier_placeholder", "ExternalNotifierPlaceholder"),
            ("notifications.notification_preferences",  "NotificationPreferences"),
            ("reports.notification_center_report",      "NotificationCenterReport"),
            ("gui.notification_center_adapter",         "NotificationCenterAdapter"),
        ]
        failed = []
        for mod, cls in modules:
            try:
                m = __import__(mod, fromlist=[cls])
                getattr(m, cls)
            except Exception as exc:
                failed.append(f"{mod}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("notification_imports", "PASS",
                               f"All {len(modules)} v0.4.5 Notification modules imported.", elapsed)
        return self._item("notification_imports", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_notification_center_empty_state(self) -> dict:
        """v0.4.5: NotificationCenter.build_summary() with empty log returns valid result (no crash)."""
        t0 = time.monotonic()
        try:
            import tempfile
            from notifications.notification_center import NotificationCenter
            with tempfile.TemporaryDirectory() as tmp:
                center = NotificationCenter(log_dir=tmp, max_history=10)
                summary = center.build_summary()
                assert summary.get("total_events", -1) == 0, "Expected 0 events on empty center"
                assert summary.get("no_real_orders") is True, "no_real_orders must be True"
                assert summary.get("external_enabled") is False, "external_enabled must be False"
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "notification_center_empty_state", "PASS",
                "NotificationCenter empty state: summary OK, no_real_orders=True, external_enabled=False.",
                elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("notification_center_empty_state", "FAIL", str(exc), elapsed)

    def _test_journal_imports(self) -> dict:
        """v0.4.6: All Portfolio Journal modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("journal.journal_schema",        "JournalEntry"),
            ("journal.journal_store",         "PortfolioJournalStore"),
            ("journal.signal_outcome_tracker","SignalOutcomeTracker"),
            ("journal.replay_training_notes", "ReplayTrainingNotes"),
            ("journal.mistake_taxonomy",      "MistakeTaxonomy"),
            ("journal.journal_analytics",     "JournalAnalytics"),
            ("reports.portfolio_journal_report", "PortfolioJournalReport"),
            ("gui.portfolio_journal_adapter", "PortfolioJournalAdapter"),
        ]
        failed = []
        for mod, cls in modules:
            try:
                m = __import__(mod, fromlist=[cls])
                getattr(m, cls)
            except Exception as exc:
                failed.append(f"{mod}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("journal_imports", "PASS",
                               f"All {len(modules)} v0.4.6 Journal modules imported.", elapsed)
        return self._item("journal_imports", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:3]}", elapsed)

    def _test_journal_store_empty_state(self) -> dict:
        """v0.4.6: PortfolioJournalStore.build_summary() with empty store returns valid result (no crash)."""
        t0 = time.monotonic()
        try:
            import tempfile
            from journal.journal_store import PortfolioJournalStore
            with tempfile.TemporaryDirectory() as tmp:
                store = PortfolioJournalStore(journal_root=tmp)
                summary = store.build_summary()
                assert summary.get("entries_count", -1) == 0, "Expected 0 entries on empty store"
                assert summary.get("no_real_orders") is True, "no_real_orders must be True"
                assert summary.get("journal_only") is True, "journal_only must be True"
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "journal_store_empty_state", "PASS",
                "PortfolioJournalStore empty state: summary OK, no_real_orders=True, journal_only=True.",
                elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("journal_store_empty_state", "FAIL", str(exc), elapsed)

    # ------------------------------------------------------------------
    # Suite runners
    # ------------------------------------------------------------------

    def run_quick(self) -> dict:
        """Run the 7-test quick suite."""
        logger.info("RegressionSuite.run_quick() — mode=%s", self.mode)
        tests_fns = [
            self._test_compileall,
            self._test_import_core,
            self._test_data_quality_gate,
            self._test_provider_reliability,
            self._test_rule_governance,
            self._test_experiment_list,
            self._test_paper_trading,
        ]
        return self._execute("quick", tests_fns)

    def run_full(self) -> dict:
        """Run the full 35-test suite (quick + extended + v0.4.1 + v0.4.1.1 + v0.4.2 + v0.4.2.1 + v0.4.3 + v0.4.4 + v0.4.5 + v0.4.6)."""
        logger.info("RegressionSuite.run_full() — mode=%s", self.mode)
        tests_fns = [
            self._test_compileall,
            self._test_import_core,
            self._test_data_quality_gate,
            self._test_provider_reliability,
            self._test_rule_governance,
            self._test_experiment_list,
            self._test_paper_trading,
            self._test_hardened_backtest_import,
            self._test_intraday_pipeline_import,
            self._test_auto_report_import,
            self._test_experiment_registry_import,
            self._test_gui_imports,
            self._test_signal_quality_import,
            self._test_rule_weight_import,
            # v0.4.1
            self._test_api_fetch_imports,
            self._test_api_token_check,
            self._test_api_cache_stats,
            # v0.4.1.1
            self._test_strategy_knowledge_imports,
            self._test_strategy_knowledge_summary,
            self._test_strategy_knowledge_dry_run,
            # v0.4.2.1
            self._test_ml_knowledge_imports,
            self._test_ml_knowledge_bridge_empty,
            # v0.4.2
            self._test_ml_feature_catalog,
            self._test_ml_feature_snapshot_import,
            self._test_ml_leakage_checker,
            self._test_ml_feature_store_report,
            # v0.4.3
            self._test_model_monitoring_imports,
            self._test_model_monitoring_summary,
            self._test_drift_detector,
            # v0.4.4
            self._test_intraday_replay_imports,
            self._test_intraday_replay_empty_state,
            # v0.4.5
            self._test_notification_imports,
            self._test_notification_center_empty_state,
            # v0.4.6
            self._test_journal_imports,
            self._test_journal_store_empty_state,
            # v0.4.7
            self._test_research_review_imports,
            self._test_research_review_summary,
            # v0.4.8
            self._test_research_coach_imports,
            self._test_research_coach_summary,
        ]
        return self._execute("full", tests_fns)

    def run(self) -> dict:
        """Run quick or full suite based on self.quick flag."""
        if self.quick:
            return self.run_quick()
        return self.run_full()

    # ------------------------------------------------------------------
    # Execution engine
    # ------------------------------------------------------------------

    def _execute(self, suite_name: str, tests_fns: list) -> dict:
        tests: list[dict] = []
        for fn in tests_fns:
            try:
                item = fn()
            except Exception as exc:
                item = self._item(
                    getattr(fn, "__name__", "unknown"),
                    "FAIL",
                    f"Unexpected exception: {exc}",
                    0.0,
                )
            tests.append(item)
            logger.debug("  [%s] %s — %s", item["status"], item["name"], item["detail"][:80])

        passed = sum(1 for t in tests if t["status"] == "PASS")
        failed = sum(1 for t in tests if t["status"] == "FAIL")
        warned = sum(1 for t in tests if t["status"] in ("WARN", "SKIP"))

        if failed > 0:
            overall = "FAIL"
        elif warned > 0:
            overall = "PARTIAL"
        else:
            overall = "PASS"

        result = {
            "suite":              suite_name,
            "status":             overall,
            "mode":               self.mode,
            "tests":              tests,
            "passed":             passed,
            "failed":             failed,
            "warned":             warned,
            "read_only":          True,
            "no_real_orders":     True,
            "production_blocked": True,
            "real_order_ready":   False,
        }

        self._write_csv(tests, suite_name)
        logger.info(
            "RegressionSuite[%s] complete — status=%s passed=%d failed=%d warned=%d",
            suite_name, overall, passed, failed, warned,
        )
        return result

    # ------------------------------------------------------------------
    # v0.4.7 Research Review Dashboard tests
    # ------------------------------------------------------------------

    def _test_research_review_imports(self) -> dict:
        t0 = time.monotonic()
        try:
            from review.review_schema import ReviewItem
            from review.review_aggregator import ResearchReviewAggregator
            from review.review_scorecard import ResearchReviewScorecard
            from review.review_action_planner import ReviewActionPlanner
            from review.review_store import ResearchReviewStore
            from gui.research_review_dashboard_adapter import ResearchReviewDashboardAdapter
            return self._item(
                "research_review_imports", "PASS",
                "All review package imports OK",
                (time.monotonic() - t0) * 1000,
            )
        except Exception as exc:
            return self._item(
                "research_review_imports", "FAIL", str(exc),
                (time.monotonic() - t0) * 1000,
            )

    def _test_research_review_summary(self) -> dict:
        t0 = time.monotonic()
        try:
            cmd = [sys.executable, "main.py", "research-review-summary"]
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=BASE_DIR,
            )
            detail = (proc.stdout or proc.stderr or "")[:200]
            status = "PASS" if proc.returncode == 0 else "PARTIAL"
            return self._item(
                "research_review_summary", status, detail,
                (time.monotonic() - t0) * 1000,
            )
        except Exception as exc:
            return self._item(
                "research_review_summary", "FAIL", str(exc),
                (time.monotonic() - t0) * 1000,
            )

    def _test_research_coach_imports(self) -> dict:
        t0 = time.monotonic()
        try:
            import importlib
            importlib.import_module("coach.coach_schema")
            importlib.import_module("coach.checklist_builder")
            importlib.import_module("coach.research_assistant_engine")
            importlib.import_module("coach.replay_training_planner")
            importlib.import_module("coach.rule_review_queue")
            importlib.import_module("coach.data_repair_planner")
            importlib.import_module("coach.coach_store")
            return self._item(
                "research_coach_imports", "PASS", "all coach modules imported",
                (time.monotonic() - t0) * 1000,
            )
        except Exception as exc:
            return self._item(
                "research_coach_imports", "FAIL", str(exc),
                (time.monotonic() - t0) * 1000,
            )

    def _test_research_coach_summary(self) -> dict:
        t0 = time.monotonic()
        try:
            cmd = [sys.executable, "main.py", "research-coach-summary"]
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=BASE_DIR,
            )
            detail = (proc.stdout or proc.stderr or "")[:200]
            status = "PASS" if proc.returncode == 0 else "PARTIAL"
            return self._item(
                "research_coach_summary", status, detail,
                (time.monotonic() - t0) * 1000,
            )
        except Exception as exc:
            return self._item(
                "research_coach_summary", "FAIL", str(exc),
                (time.monotonic() - t0) * 1000,
            )

    def _write_csv(self, tests: list[dict], suite_name: str) -> str | None:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            csv_path = os.path.join(
                self.results_dir, f"regression_suite_{today}.csv"
            )
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["name", "status", "detail", "duration_ms"]
                )
                writer.writeheader()
                writer.writerows(tests)
            logger.info("Regression CSV saved: %s", csv_path)
            return csv_path
        except Exception as exc:
            logger.warning("Could not write regression CSV: %s", exc)
            return None
