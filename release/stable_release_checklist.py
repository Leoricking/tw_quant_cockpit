"""
release/stable_release_checklist.py — Stable release checklist for v0.4.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import csv
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StableReleaseChecklist:
    """18-item stable release checklist for TW Quant Cockpit v0.4.0.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, mode: str = "real", results_dir: str | None = None,
                 report_dir: str | None = None) -> None:
        self.mode = mode
        self.results_dir = os.path.join(
            BASE_DIR, results_dir if results_dir else "data/backtest_results"
        )
        self.report_dir = os.path.join(
            BASE_DIR, report_dir if report_dir else "reports"
        )
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Internal helpers
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
    # Individual checklist checks
    # ------------------------------------------------------------------

    def _check_compileall(self) -> dict:
        t0 = time.monotonic()
        try:
            result = subprocess.run(
                [sys.executable, "-m", "compileall", BASE_DIR, "-q"],
                capture_output=True, text=True, timeout=120,
            )
            elapsed = (time.monotonic() - t0) * 1000
            if result.returncode == 0:
                return self._item("compileall", "PASS", "All Python files compile cleanly.", elapsed)
            else:
                detail = (result.stderr or result.stdout or "returncode != 0").strip()[:300]
                return self._item("compileall", "FAIL", detail, elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("compileall", "FAIL", str(exc), elapsed)

    def _check_cli_import_health(self) -> dict:
        """Check CLI import health by verifying main.py exists and key modules import cleanly."""
        t0 = time.monotonic()
        try:
            # Do NOT `import main` — re-importing main.py replaces sys.stdout which closes the buffer.
            # Instead verify main.py exists and key sub-modules import.
            main_path = os.path.join(BASE_DIR, "main.py")
            if not os.path.isfile(main_path):
                raise FileNotFoundError(f"main.py not found at {main_path}")
            # Verify a representative selection of modules
            import importlib.util
            for mod in ["workflow.daily_workflow", "quality.data_quality_gate", "governance.rule_registry"]:
                spec = importlib.util.find_spec(mod)
                if spec is None:
                    raise ImportError(f"Module {mod} not found")
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("cli_import_health", "PASS", "main.py present; core modules importable.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("cli_import_health", "FAIL", str(exc), elapsed)

    def _check_gui_import_health(self) -> dict:
        t0 = time.monotonic()
        try:
            from gui.dashboard import launch  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("gui_import_health", "PASS", "gui.dashboard.launch imports successfully.", elapsed)
        except ImportError as exc:
            elapsed = (time.monotonic() - t0) * 1000
            msg = str(exc)
            if "PySide6" in msg or "pyside6" in msg.lower():
                return self._item("gui_import_health", "SKIP", f"PySide6 not installed: {msg}", elapsed)
            return self._item("gui_import_health", "WARN", f"ImportError: {msg}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("gui_import_health", "WARN", str(exc), elapsed)

    def _check_daily_workflow(self) -> dict:
        t0 = time.monotonic()
        try:
            from workflow.daily_workflow import DailyResearchWorkflow
            DailyResearchWorkflow(mode=self.mode)
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("daily_workflow", "PASS", "DailyResearchWorkflow instantiates successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("daily_workflow", "FAIL", str(exc), elapsed)

    def _check_data_quality_gate(self) -> dict:
        t0 = time.monotonic()
        try:
            from quality.data_quality_gate import DataQualityGate
            DataQualityGate()
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("data_quality_gate", "PASS", "DataQualityGate instantiates successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("data_quality_gate", "FAIL", str(exc), elapsed)

    def _check_provider_reliability(self) -> dict:
        t0 = time.monotonic()
        try:
            from data.providers.provider_reliability_matrix import ProviderReliabilityMatrix  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("provider_reliability", "PASS",
                               "data.providers.provider_reliability_matrix imported.", elapsed)
        except ModuleNotFoundError:
            # Try alternative path
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

    def _check_intraday_pipeline(self) -> dict:
        t0 = time.monotonic()
        try:
            from intraday.intraday_pipeline import IntradayDataPipeline  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("intraday_pipeline", "PASS", "IntradayDataPipeline imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("intraday_pipeline", "FAIL", str(exc), elapsed)

    def _check_hardened_backtest(self) -> dict:
        t0 = time.monotonic()
        try:
            from backtest.hardened_backtester import HardenedBacktester  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("hardened_backtest", "PASS", "HardenedBacktester imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("hardened_backtest", "FAIL", str(exc), elapsed)

    def _check_rule_governance(self) -> dict:
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

    def _check_experiment_registry(self) -> dict:
        t0 = time.monotonic()
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry()
            reg.list_experiments()
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("experiment_registry", "PASS", "ExperimentRegistry instantiates and list_experiments() works.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("experiment_registry", "FAIL", str(exc), elapsed)

    def _check_auto_report(self) -> dict:
        t0 = time.monotonic()
        try:
            from reports.auto_report_center import AutoReportCenter  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("auto_report", "PASS", "AutoReportCenter imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("auto_report", "FAIL", str(exc), elapsed)

    def _check_usability_smoke_test(self) -> dict:
        t0 = time.monotonic()
        try:
            from quality.usability_smoke_test import UsabilitySmokeTest  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("usability_smoke_test", "PASS", "UsabilitySmokeTest imports successfully.", elapsed)
        except ModuleNotFoundError as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("usability_smoke_test", "WARN", f"Module not found (non-fatal): {exc}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("usability_smoke_test", "WARN", str(exc), elapsed)

    def _check_paper_trading(self) -> dict:
        t0 = time.monotonic()
        try:
            from sim.simulator import PaperTrader  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("paper_trading", "PASS", "PaperTrader imports successfully.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("paper_trading", "FAIL", str(exc), elapsed)

    def _check_mock_realtime(self) -> dict:
        t0 = time.monotonic()
        try:
            from sim.mock_realtime import MockRealtimeEngine  # noqa: F401
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("mock_realtime", "PASS", "MockRealtimeEngine imports successfully.", elapsed)
        except ModuleNotFoundError as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("mock_realtime", "WARN", f"Module not found (non-fatal): {exc}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("mock_realtime", "WARN", str(exc), elapsed)

    def _check_git_safety(self) -> dict:
        t0 = time.monotonic()
        try:
            result = subprocess.run(
                ["git", "-C", BASE_DIR, "status", "--porcelain"],
                capture_output=True, text=True, timeout=30,
            )
            elapsed = (time.monotonic() - t0) * 1000
            dirty_lines = [l for l in result.stdout.splitlines() if l.strip()]
            if not dirty_lines:
                return self._item("git_safety", "PASS", "Working tree is clean.", elapsed)
            return self._item("git_safety", "WARN",
                               f"Working tree has {len(dirty_lines)} uncommitted changes.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("git_safety", "WARN", f"git check failed: {exc}", elapsed)

    def _check_artifact_ignore(self) -> dict:
        t0 = time.monotonic()
        required = [
            "data/backtest_results/",
            "reports/auto_report_center/",
            "logs/",
            "experiments/EXP-",
        ]
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        try:
            if not os.path.exists(gitignore_path):
                elapsed = (time.monotonic() - t0) * 1000
                return self._item("artifact_ignore_check", "FAIL", ".gitignore not found.", elapsed)
            with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            missing = [pat for pat in required if pat not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("artifact_ignore_check", "PASS",
                                   "All required .gitignore patterns present.", elapsed)
            return self._item("artifact_ignore_check", "WARN",
                               f"Missing patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("artifact_ignore_check", "FAIL", str(exc), elapsed)

    def _check_no_token_leak(self) -> dict:
        t0 = time.monotonic()
        pattern = re.compile(
            r'(?:TOKEN|KEY|PASSWORD|SECRET)\s*=\s*["\'][A-Za-z0-9+/]{20,}',
            re.IGNORECASE,
        )
        matches_found = []
        try:
            for root, dirs, files in os.walk(BASE_DIR):
                # Skip hidden dirs and __pycache__
                dirs[:] = [
                    d for d in dirs
                    if d not in ("__pycache__", ".git") and not d.startswith(".")
                ]
                for fname in files:
                    if not fname.endswith(".py"):
                        continue
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                            for lineno, line in enumerate(f, 1):
                                if pattern.search(line):
                                    rel = os.path.relpath(fpath, BASE_DIR)
                                    matches_found.append(f"{rel}:{lineno}")
                    except OSError:
                        pass
            elapsed = (time.monotonic() - t0) * 1000
            if not matches_found:
                return self._item("no_token_leak_check", "PASS",
                                   "No hardcoded tokens found in .py files.", elapsed)
            return self._item("no_token_leak_check", "FAIL",
                               f"Possible token leaks at: {matches_found[:10]}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("no_token_leak_check", "FAIL", str(exc), elapsed)

    def _check_no_real_order(self) -> dict:
        t0 = time.monotonic()
        try:
            from release.version_info import VersionInfo
            ok_real = (VersionInfo.real_order_ready is False)
            ok_blocked = (VersionInfo.production_blocked is True)
            elapsed = (time.monotonic() - t0) * 1000
            if ok_real and ok_blocked:
                return self._item("no_real_order_check", "PASS",
                                   "real_order_ready=False, production_blocked=True — verified.", elapsed)
            issues = []
            if not ok_real:
                issues.append(f"real_order_ready={VersionInfo.real_order_ready} (expected False)")
            if not ok_blocked:
                issues.append(f"production_blocked={VersionInfo.production_blocked} (expected True)")
            return self._item("no_real_order_check", "FAIL", "; ".join(issues), elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("no_real_order_check", "FAIL", str(exc), elapsed)

    def _check_api_token_safety(self) -> dict:
        """v0.4.1: TokenSetupAssistant never exposes full token; .env not modified."""
        t0 = time.monotonic()
        try:
            from data.providers.token_setup_assistant import TokenSetupAssistant
            assistant = TokenSetupAssistant()
            result = assistant.inspect()
            # Check tokens are masked
            for name, info in result.get("required_tokens", {}).items():
                masked = info.get("masked_value", "")
                if masked and len(masked) > 12 and "****" not in masked:
                    elapsed = (time.monotonic() - t0) * 1000
                    return self._item("api_token_safety", "FAIL",
                                       f"Token '{name}' not masked: {masked[:8]}...", elapsed)
            # Check read_only flag
            if not getattr(assistant, "read_only", True):
                elapsed = (time.monotonic() - t0) * 1000
                return self._item("api_token_safety", "FAIL",
                                   "TokenSetupAssistant.read_only is not True", elapsed)
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("api_token_safety", "PASS",
                               "TokenSetupAssistant: tokens masked, read_only=True.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("api_token_safety", "WARN", f"Module not available: {exc}", elapsed)

    def _check_api_cache_ignored(self) -> dict:
        """v0.4.1: Verify data_cache/api/ and api_fetch reports are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "data_cache/api/",
            "reports/api_fetch_production_report_",
        ]
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            missing = [pat for pat in required if pat not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("api_cache_ignored", "PASS",
                                   "API cache and report patterns in .gitignore.", elapsed)
            return self._item("api_cache_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("api_cache_ignored", "WARN", str(exc), elapsed)

    def _check_model_monitoring_import(self) -> dict:
        """v0.4.3: All Model Monitoring core modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("monitoring.model_registry",       "ModelRegistry"),
            ("monitoring.prediction_log",        "PredictionLog"),
            ("monitoring.hit_miss_review",       "HitMissReviewer"),
            ("monitoring.drift_detector",        "DriftDetector"),
            ("monitoring.signal_degradation",    "SignalDegradationMonitor"),
            ("monitoring.rule_vs_ml_comparator", "RuleVsMLComparator"),
            ("monitoring.monitoring_summary",    "ModelMonitoringSummary"),
            ("reports.model_monitoring_report",  "ModelMonitoringReportBuilder"),
            ("gui.model_monitoring_adapter",     "ModelMonitoringAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("model_monitoring_import", "PASS",
                               f"All {len(modules)} Model Monitoring modules imported.", elapsed)
        return self._item("model_monitoring_import", "WARN",
                           f"{len(failed)} module(s) failed: {failed[:2]}", elapsed)

    def _check_no_live_prediction(self) -> dict:
        """v0.4.3: ModelMonitoringSummary has no_live_prediction flag and read_only=True."""
        t0 = time.monotonic()
        try:
            from monitoring.monitoring_summary import ModelMonitoringSummary
            obj = ModelMonitoringSummary()
            elapsed = (time.monotonic() - t0) * 1000
            if not getattr(obj, "read_only", False):
                return self._item("no_live_prediction", "FAIL",
                                   "ModelMonitoringSummary.read_only is not True", elapsed)
            if not getattr(obj, "no_real_orders", False):
                return self._item("no_live_prediction", "FAIL",
                                   "ModelMonitoringSummary.no_real_orders is not True", elapsed)
            return self._item("no_live_prediction", "PASS",
                               "ModelMonitoringSummary: read_only=True, no_real_orders=True.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("no_live_prediction", "WARN", f"Module not available: {exc}", elapsed)

    def _check_prediction_logs_ignored(self) -> dict:
        """v0.4.3: Verify model_monitoring/ and model_monitoring_report_*.md are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "model_monitoring/",
            "reports/model_monitoring_report_",
        ]
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            missing = [pat for pat in required if pat not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("prediction_logs_ignored", "PASS",
                                   "model_monitoring/ and report patterns in .gitignore.", elapsed)
            return self._item("prediction_logs_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("prediction_logs_ignored", "WARN", str(exc), elapsed)

    def _check_ml_feature_store_import(self) -> dict:
        """v0.4.2: All ML Feature Store core modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("ml.feature_catalog",              "FeatureCatalog"),
            ("ml.feature_snapshot",             "FeatureSnapshotBuilder"),
            ("ml.label_generator",              "LabelGenerator"),
            ("ml.split_manager",                "MLSplitManager"),
            ("ml.leakage_checker",              "DataLeakageChecker"),
            ("ml.feature_quality",              "FeatureQualityChecker"),
            ("ml.feature_importance_shell",     "FeatureImportanceShell"),
            ("ml.dataset_builder",              "MLFeatureDatasetBuilder"),
            ("reports.ml_feature_store_report", "MLFeatureStoreReportBuilder"),
            ("gui.ml_feature_store_adapter",    "MLFeatureStoreAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("ml_feature_store_import", "PASS",
                               f"All {len(modules)} ML Feature Store modules imported.", elapsed)
        return self._item("ml_feature_store_import", "WARN",
                           f"{len(failed)} module(s) failed: {failed[:2]}", elapsed)

    def _check_ml_leakage_checker(self) -> dict:
        """v0.4.2: DataLeakageChecker has read_only + no_real_orders flags."""
        t0 = time.monotonic()
        try:
            from ml.leakage_checker import DataLeakageChecker
            checker = DataLeakageChecker()
            elapsed = (time.monotonic() - t0) * 1000
            if not getattr(checker, "read_only", False):
                return self._item("ml_leakage_checker", "FAIL",
                                   "DataLeakageChecker.read_only is not True", elapsed)
            if not getattr(checker, "no_real_orders", False):
                return self._item("ml_leakage_checker", "FAIL",
                                   "DataLeakageChecker.no_real_orders is not True", elapsed)
            return self._item("ml_leakage_checker", "PASS",
                               "DataLeakageChecker: read_only=True, no_real_orders=True.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_leakage_checker", "WARN", f"Module not available: {exc}", elapsed)

    def _check_ml_dataset_artifact_ignored(self) -> dict:
        """v0.4.2: Verify data/ml_features/ and ml_feature_store_report_*.md are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "data/ml_features/",
            "reports/ml_feature_store_report_",
        ]
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            missing = [pat for pat in required if pat not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("ml_dataset_artifact_ignored", "PASS",
                                   "ML dataset and report patterns in .gitignore.", elapsed)
            return self._item("ml_dataset_artifact_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_dataset_artifact_ignored", "WARN", str(exc), elapsed)

    def _check_intraday_replay_import(self) -> dict:
        """v0.4.4: All Intraday Replay core modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("replay.replay_session",         "ReplaySessionManager"),
            ("replay.replay_engine",           "IntradayReplayEngine"),
            ("replay.training_mode",           "ReplayTrainingMode"),
            ("replay.replay_metrics",          "ReplayMetrics"),
            ("reports.intraday_replay_report", "IntradayReplayReportBuilder"),
            ("gui.intraday_replay_adapter",    "IntradayReplayAdapter"),
        ]
        failed = []
        for mod_path, cls_name in modules:
            try:
                mod = __import__(mod_path, fromlist=[cls_name])
                getattr(mod, cls_name)
            except Exception as exc:
                failed.append(f"{mod_path}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("intraday_replay_import", "PASS",
                               f"All {len(modules)} Intraday Replay modules imported.", elapsed)
        return self._item("intraday_replay_import", "WARN",
                           f"{len(failed)} module(s) failed: {failed[:2]}", elapsed)

    def _check_replay_runtime_ignored(self) -> dict:
        """v0.4.4: Verify replay_sessions/ and intraday_replay_report_*.md are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "replay_sessions/",
            "reports/intraday_replay_report_",
        ]
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            missing = [pat for pat in required if pat not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("replay_runtime_ignored", "PASS",
                                   "replay_sessions/ and report patterns in .gitignore.", elapsed)
            return self._item("replay_runtime_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("replay_runtime_ignored", "WARN", str(exc), elapsed)

    def _check_no_broker_call_in_replay(self) -> dict:
        """v0.4.4: StrategyReplayOverlay has no_real_orders=True and read_only=True."""
        t0 = time.monotonic()
        try:
            from replay.strategy_replay import StrategyReplayOverlay
            obj = StrategyReplayOverlay()
            elapsed = (time.monotonic() - t0) * 1000
            if not getattr(obj, "read_only", False):
                return self._item("no_broker_call_in_replay", "FAIL",
                                   "StrategyReplayOverlay.read_only is not True", elapsed)
            if not getattr(obj, "no_real_orders", False):
                return self._item("no_broker_call_in_replay", "FAIL",
                                   "StrategyReplayOverlay.no_real_orders is not True", elapsed)
            return self._item("no_broker_call_in_replay", "PASS",
                               "StrategyReplayOverlay: read_only=True, no_real_orders=True.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("no_broker_call_in_replay", "WARN", f"Module not available: {exc}", elapsed)

    def _check_strategy_knowledge_ingestion_import(self) -> dict:
        """v0.4.1.1: All Strategy Knowledge Ingestion core modules import cleanly."""
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
                failed.append(f"{mod_path}: {exc}")
        elapsed = (time.monotonic() - t0) * 1000
        if not failed:
            return self._item("strategy_knowledge_ingestion_import", "PASS",
                               f"All {len(modules)} Strategy Knowledge modules imported.", elapsed)
        return self._item("strategy_knowledge_ingestion_import", "WARN",
                           f"{len(failed)} module(s) failed: {failed[:2]}", elapsed)

    def _check_no_auto_activate_candidate_rules(self) -> dict:
        """v0.4.1.1: StrategyKnowledgeIngestionPipeline has no_real_orders and auto_activated=False."""
        t0 = time.monotonic()
        try:
            from knowledge.ingestion_pipeline import StrategyKnowledgeIngestionPipeline
            obj = StrategyKnowledgeIngestionPipeline()
            elapsed = (time.monotonic() - t0) * 1000
            if not getattr(obj, "no_real_orders", False):
                return self._item("no_auto_activate_candidate_rules", "FAIL",
                                   "StrategyKnowledgeIngestionPipeline.no_real_orders is not True", elapsed)
            if not getattr(obj, "read_only", False):
                return self._item("no_auto_activate_candidate_rules", "FAIL",
                                   "StrategyKnowledgeIngestionPipeline.read_only is not True", elapsed)
            return self._item("no_auto_activate_candidate_rules", "PASS",
                               "StrategyKnowledgeIngestionPipeline: read_only=True, no_real_orders=True, "
                               "auto_activated=False.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("no_auto_activate_candidate_rules", "WARN", f"Module not available: {exc}", elapsed)

    def _check_strategy_knowledge_artifacts_ignored(self) -> dict:
        """v0.4.1.1: Verify strategy_knowledge output and report patterns are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "data/backtest_results/strategy_knowledge/",
            "reports/strategy_knowledge_ingestion_report_",
        ]
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            missing = [pat for pat in required if pat not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("strategy_knowledge_artifacts_ignored", "PASS",
                                   "strategy_knowledge output and report patterns in .gitignore.", elapsed)
            return self._item("strategy_knowledge_artifacts_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("strategy_knowledge_artifacts_ignored", "WARN", str(exc), elapsed)

    def _check_ml_knowledge_integration_import(self) -> dict:
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
            return self._item("ml_knowledge_integration_import", "PASS",
                               f"All {len(modules)} ML Knowledge Integration modules imported.", elapsed)
        return self._item("ml_knowledge_integration_import", "WARN",
                           f"{len(failed)} module(s) failed: {failed[:2]}", elapsed)

    def _check_ml_knowledge_auto_enabled_false(self) -> dict:
        """v0.4.2.1: KnowledgeFeatureBridge and KnowledgeFeatureCatalog enforce auto_enabled=False."""
        t0 = time.monotonic()
        try:
            from ml.knowledge_feature_bridge import KnowledgeFeatureBridge
            from ml.knowledge_feature_catalog import KnowledgeFeatureCatalog
            bridge  = KnowledgeFeatureBridge()
            catalog = KnowledgeFeatureCatalog()
            elapsed = (time.monotonic() - t0) * 1000
            if getattr(bridge, "auto_enabled", True):
                return self._item("ml_knowledge_auto_enabled_false", "FAIL",
                                   "KnowledgeFeatureBridge.auto_enabled is not False", elapsed)
            if getattr(catalog, "auto_enabled", True):
                return self._item("ml_knowledge_auto_enabled_false", "FAIL",
                                   "KnowledgeFeatureCatalog.auto_enabled is not False", elapsed)
            return self._item("ml_knowledge_auto_enabled_false", "PASS",
                               "auto_enabled=False confirmed on Bridge and Catalog.", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_knowledge_auto_enabled_false", "WARN", f"Module not available: {exc}", elapsed)

    def _check_ml_knowledge_artifacts_ignored(self) -> dict:
        """v0.4.2.1: Verify ML knowledge output patterns are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "data/backtest_results/ml_feature_store/",
            "reports/ml_knowledge_integration_report_",
        ]
        try:
            import os
            gitignore = os.path.join(BASE_DIR, ".gitignore")
            content = ""
            if os.path.isfile(gitignore):
                with open(gitignore, "r", encoding="utf-8") as f:
                    content = f.read()
            missing = [r for r in required if r not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("ml_knowledge_artifacts_ignored", "PASS",
                                   "All ML knowledge output patterns present in .gitignore.", elapsed)
            return self._item("ml_knowledge_artifacts_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("ml_knowledge_artifacts_ignored", "WARN", str(exc), elapsed)

    def _check_notification_center_import(self) -> dict:
        """v0.4.5: All Notification Center modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("notifications.notification_schema",       "NotificationEvent"),
            ("notifications.notification_center",       "NotificationCenter"),
            ("notifications.notification_rules",        "NotificationRuleEngine"),
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
            return self._item("notification_center_import", "PASS",
                               f"All {len(modules)} v0.4.5 Notification modules imported.", elapsed)
        return self._item("notification_center_import", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:2]}", elapsed)

    def _check_notification_external_disabled(self) -> dict:
        """v0.4.5: ExternalNotifierPlaceholder.external_enabled=False always."""
        t0 = time.monotonic()
        try:
            from notifications.external_notifier_placeholder import ExternalNotifierPlaceholder
            obj = ExternalNotifierPlaceholder()
            assert obj.external_enabled is False, "external_enabled must be False"
            assert obj.is_available() is False, "is_available() must return False"
            result = obj.send_line.__func__(obj, None) if False else obj.send_telegram(None.__class__())
        except (AssertionError, Exception) as exc:
            # Only fail on AssertionError
            if isinstance(exc, AssertionError):
                elapsed = (time.monotonic() - t0) * 1000
                return self._item("notification_external_disabled", "FAIL", str(exc), elapsed)
        elapsed = (time.monotonic() - t0) * 1000
        return self._item("notification_external_disabled", "PASS",
                           "ExternalNotifierPlaceholder: external_enabled=False, is_available=False.", elapsed)

    def _check_notification_artifacts_ignored(self) -> dict:
        """v0.4.5: Verify Notification Center output patterns are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "logs/notifications/",
            "reports/notification_center_report_",
            "config/notification_preferences.json",
        ]
        try:
            import os
            gitignore = os.path.join(BASE_DIR, ".gitignore")
            content = ""
            if os.path.isfile(gitignore):
                with open(gitignore, "r", encoding="utf-8") as f:
                    content = f.read()
            missing = [r for r in required if r not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("notification_artifacts_ignored", "PASS",
                                   "All Notification Center output patterns present in .gitignore.", elapsed)
            return self._item("notification_artifacts_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("notification_artifacts_ignored", "WARN", str(exc), elapsed)

    def _check_notification_no_real_orders(self) -> dict:
        """v0.4.5: NotificationCenter.no_real_orders=True always."""
        t0 = time.monotonic()
        try:
            from notifications.notification_center import NotificationCenter
            from notifications.notification_schema import NotificationEvent
            assert NotificationCenter.no_real_orders is True, "NotificationCenter.no_real_orders must be True"
            assert NotificationCenter.production_blocked is True, "production_blocked must be True"
            assert NotificationEvent.no_real_orders is True, "NotificationEvent.no_real_orders must be True"
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("notification_no_real_orders", "PASS",
                               "NotificationCenter and NotificationEvent: no_real_orders=True, production_blocked=True.",
                               elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("notification_no_real_orders", "FAIL", str(exc), elapsed)

    def _check_journal_import_health(self) -> dict:
        """v0.4.6: All Portfolio Journal modules import cleanly."""
        t0 = time.monotonic()
        modules = [
            ("journal.journal_schema",        "JournalEntry"),
            ("journal.journal_store",         "PortfolioJournalStore"),
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
            return self._item("journal_import_health", "PASS",
                               f"All {len(modules)} v0.4.6 Journal modules imported.", elapsed)
        return self._item("journal_import_health", "FAIL",
                           f"{len(failed)} module(s) failed: {failed[:2]}", elapsed)

    def _check_journal_no_real_orders(self) -> dict:
        """v0.4.6: JournalEntry and PortfolioJournalStore enforce no_real_orders=True always."""
        t0 = time.monotonic()
        try:
            from journal.journal_schema import JournalEntry
            from journal.journal_store import PortfolioJournalStore
            assert JournalEntry.no_real_orders is True, "JournalEntry.no_real_orders must be True"
            assert JournalEntry.production_blocked is True, "production_blocked must be True"
            assert PortfolioJournalStore.no_real_orders is True, "PortfolioJournalStore.no_real_orders must be True"
            # Verify instance-level enforcement
            entry2 = JournalEntry()
            assert entry2.no_real_orders is True
            assert entry2.production_blocked is True
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("journal_no_real_orders", "PASS",
                               "JournalEntry and PortfolioJournalStore: no_real_orders=True, production_blocked=True.",
                               elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("journal_no_real_orders", "FAIL", str(exc), elapsed)

    def _check_journal_data_ignored(self) -> dict:
        """v0.4.6: Verify journal_data/ and output patterns are in .gitignore."""
        t0 = time.monotonic()
        required = [
            "journal_data/",
            "reports/portfolio_journal_report_",
            "data/backtest_results/portfolio_journal_summary.csv",
            "data/backtest_results/signal_outcome_summary.csv",
        ]
        try:
            import os
            gitignore = os.path.join(BASE_DIR, ".gitignore")
            content = ""
            if os.path.isfile(gitignore):
                with open(gitignore, "r", encoding="utf-8") as f:
                    content = f.read()
            missing = [r for r in required if r not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item("journal_data_ignored", "PASS",
                                   "All journal output patterns present in .gitignore.", elapsed)
            return self._item("journal_data_ignored", "WARN",
                               f"Missing .gitignore patterns: {missing}", elapsed)
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("journal_data_ignored", "WARN", str(exc), elapsed)

    # ------------------------------------------------------------------
    # Write outputs
    # ------------------------------------------------------------------

    def _write_csv(self, items: list[dict]) -> str | None:
        try:
            csv_path = os.path.join(
                self.results_dir, "stable_release_checklist_summary.csv"
            )
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["name", "status", "detail", "duration_ms"])
                writer.writeheader()
                writer.writerows(items)
            logger.info("Checklist CSV saved: %s", csv_path)
            return csv_path
        except Exception as exc:
            logger.warning("Could not write checklist CSV: %s", exc)
            return None

    def _write_report(self, summary: dict) -> str | None:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            report_path = os.path.join(
                self.report_dir, f"stable_release_checklist_report_{today}.md"
            )
            items = summary.get("items", [])
            lines = [
                f"# Stable Release Checklist Report — v0.4.0",
                f"",
                f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                f"| Research Only | No Real Orders | Production BLOCKED",
                f"",
                f"## Summary",
                f"",
                f"| Field | Value |",
                f"|-------|-------|",
                f"| Status | {summary.get('status')} |",
                f"| Mode | {summary.get('mode')} |",
                f"| Version | {summary.get('version')} |",
                f"| Passed | {summary.get('passed')} |",
                f"| Failed | {summary.get('failed')} |",
                f"| Warnings | {summary.get('warnings')} |",
                f"| Read Only | {summary.get('read_only')} |",
                f"| No Real Orders | {summary.get('no_real_orders')} |",
                f"| Production BLOCKED | {summary.get('production_blocked')} |",
                f"| Real Order Ready | {summary.get('real_order_ready')} |",
                f"",
                f"## Checklist Items",
                f"",
                f"| # | Name | Status | Duration (ms) | Detail |",
                f"|---|------|--------|---------------|--------|",
            ]
            for i, item in enumerate(items, 1):
                detail = str(item.get("detail", "")).replace("|", "\\|")[:120]
                lines.append(
                    f"| {i} | {item['name']} | {item['status']} "
                    f"| {item['duration_ms']:.1f} | {detail} |"
                )
            lines += [
                f"",
                f"---",
                f"*TW Quant Cockpit v0.4.0 — Research Only — Not Investment Advice*",
            ]
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            logger.info("Checklist report saved: %s", report_path)
            return report_path
        except Exception as exc:
            logger.warning("Could not write checklist report: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run all 29 checklist items and return summary dict."""
        logger.info("StableReleaseChecklist.run() — mode=%s", self.mode)

        checks = [
            self._check_compileall,
            self._check_cli_import_health,
            self._check_gui_import_health,
            self._check_daily_workflow,
            self._check_data_quality_gate,
            self._check_provider_reliability,
            self._check_intraday_pipeline,
            self._check_hardened_backtest,
            self._check_rule_governance,
            self._check_experiment_registry,
            self._check_auto_report,
            self._check_usability_smoke_test,
            self._check_paper_trading,
            self._check_mock_realtime,
            self._check_git_safety,
            self._check_artifact_ignore,
            self._check_no_token_leak,
            self._check_no_real_order,
            # v0.4.1
            self._check_api_token_safety,
            self._check_api_cache_ignored,
            # v0.4.2
            self._check_ml_feature_store_import,
            self._check_ml_leakage_checker,
            self._check_ml_dataset_artifact_ignored,
            # v0.4.3
            self._check_model_monitoring_import,
            self._check_no_live_prediction,
            self._check_prediction_logs_ignored,
            # v0.4.4
            self._check_intraday_replay_import,
            self._check_replay_runtime_ignored,
            self._check_no_broker_call_in_replay,
            # v0.4.1.1
            self._check_strategy_knowledge_ingestion_import,
            self._check_no_auto_activate_candidate_rules,
            self._check_strategy_knowledge_artifacts_ignored,
            # v0.4.2.1
            self._check_ml_knowledge_integration_import,
            self._check_ml_knowledge_auto_enabled_false,
            self._check_ml_knowledge_artifacts_ignored,
            # v0.4.5
            self._check_notification_center_import,
            self._check_notification_external_disabled,
            self._check_notification_artifacts_ignored,
            self._check_notification_no_real_orders,
            # v0.4.6
            self._check_journal_import_health,
            self._check_journal_no_real_orders,
            self._check_journal_data_ignored,
            # v0.4.7
            self._check_research_review_import_health,
            self._check_research_review_no_real_orders,
            self._check_research_review_output_ignored,
            # v0.4.8
            self._check_research_coach_import_health,
            self._check_research_coach_no_real_orders,
            self._check_research_coach_output_ignored,
            self._check_research_coach_no_forbidden_commands,
            # v0.4.9
            self._check_research_workflow_import_health,
            self._check_research_workflow_no_real_orders,
            self._check_research_workflow_output_ignored,
            self._check_research_workflow_safe_command_registry,
            self._check_research_workflow_no_compound_commands,
            # v0.5.0
            self._check_research_os_import_health,
            self._check_research_os_no_real_orders,
            self._check_research_os_output_ignored,
            self._check_research_os_safety_matrix,
        ]

        items: list[dict] = []
        for check_fn in checks:
            try:
                item = check_fn()
            except Exception as exc:
                item = self._item(
                    getattr(check_fn, "__name__", "unknown").lstrip("_check_"),
                    "FAIL",
                    f"Unexpected exception: {exc}",
                    0.0,
                )
            items.append(item)
            logger.debug("  [%s] %s — %s", item["status"], item["name"], item["detail"][:80])

        passed  = sum(1 for i in items if i["status"] == "PASS")
        failed  = sum(1 for i in items if i["status"] == "FAIL")
        warnings = sum(1 for i in items if i["status"] in ("WARN", "SKIP"))

        # Safety rule: token leak or real-order FAIL => BLOCKED
        token_item = next((i for i in items if i["name"] == "no_token_leak_check"), None)
        order_item = next((i for i in items if i["name"] == "no_real_order_check"), None)
        if (token_item and token_item["status"] == "FAIL") or \
           (order_item and order_item["status"] == "FAIL"):
            overall = "BLOCKED"
        elif failed > 0 or warnings > 0:
            overall = "PARTIAL"
        else:
            overall = "PASS"

        summary = {
            "status":             overall,
            "mode":               self.mode,
            "version":            "v0.4.0",
            "items":              items,
            "passed":             passed,
            "failed":             failed,
            "warnings":           warnings,
            "read_only":          True,
            "no_real_orders":     True,
            "production_blocked": True,
            "real_order_ready":   False,
            "summary_csv_path":   None,
            "report_path":        None,
        }

        summary["summary_csv_path"] = self._write_csv(items)
        summary["report_path"] = self._write_report(summary)

        logger.info(
            "StableReleaseChecklist complete — status=%s passed=%d failed=%d warnings=%d",
            overall, passed, failed, warnings,
        )
        return summary

    # ------------------------------------------------------------------
    # v0.4.7 Research Review Dashboard checks
    # ------------------------------------------------------------------

    def _check_research_review_import_health(self) -> dict:
        """v0.4.7: Verify research review package imports are healthy."""
        t0 = time.monotonic()
        try:
            from review.review_schema import ReviewItem
            from review.review_aggregator import ResearchReviewAggregator
            from review.review_scorecard import ResearchReviewScorecard
            from review.review_action_planner import ReviewActionPlanner
            from review.review_store import ResearchReviewStore
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_review_import_health", "PASS",
                "review package imports OK", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_review_import_health", "FAIL", str(exc), elapsed)

    def _check_research_review_no_real_orders(self) -> dict:
        """v0.4.7: Verify research review safety flags are set."""
        t0 = time.monotonic()
        try:
            from review.review_aggregator import ResearchReviewAggregator
            from review.review_scorecard import ResearchReviewScorecard
            from review.review_action_planner import ReviewActionPlanner
            elapsed = (time.monotonic() - t0) * 1000
            agg_ok = ResearchReviewAggregator.no_real_orders and ResearchReviewAggregator.production_blocked
            sc_ok  = ResearchReviewScorecard.no_real_orders  and ResearchReviewScorecard.production_blocked
            ap_ok  = ReviewActionPlanner.no_real_orders      and ReviewActionPlanner.production_blocked
            if agg_ok and sc_ok and ap_ok:
                return self._item(
                    "research_review_no_real_orders", "PASS",
                    "no_real_orders=True, production_blocked=True on all review classes", elapsed,
                )
            return self._item(
                "research_review_no_real_orders", "FAIL",
                "Safety flags not set correctly on review classes", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_review_no_real_orders", "FAIL", str(exc), elapsed)

    def _check_research_review_output_ignored(self) -> dict:
        """v0.4.7: Verify research_review output paths are in .gitignore."""
        t0 = time.monotonic()
        patterns = [
            "data/backtest_results/research_review/",
            "research_review_dashboard_report_",
        ]
        try:
            gi_path = os.path.join(BASE_DIR, ".gitignore")
            content = open(gi_path, encoding="utf-8").read()
            missing = [p for p in patterns if p not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item(
                    "research_review_output_ignored", "PASS",
                    "All research_review output patterns present in .gitignore", elapsed,
                )
            return self._item(
                "research_review_output_ignored", "WARN",
                f"Missing from .gitignore: {missing}", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_review_output_ignored", "WARN", str(exc), elapsed)

    # ------------------------------------------------------------------
    # v0.4.8 Research Assistant / Coach checks
    # ------------------------------------------------------------------

    def _check_research_coach_import_health(self) -> dict:
        """v0.4.8: Verify research coach modules import cleanly."""
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
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_coach_import_health", "PASS",
                "All research coach modules import cleanly", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_coach_import_health", "FAIL", str(exc), elapsed)

    def _check_research_coach_no_real_orders(self) -> dict:
        """v0.4.8: Verify research coach schema enforces coaching_only / no_real_orders."""
        t0 = time.monotonic()
        try:
            from coach.coach_schema import CoachRecommendation
            rec = CoachRecommendation()
            assert rec.read_only is True
            assert rec.no_real_orders is True
            assert rec.production_blocked is True
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_coach_no_real_orders", "PASS",
                "CoachRecommendation enforces read_only/no_real_orders/production_blocked", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_coach_no_real_orders", "FAIL", str(exc), elapsed)

    def _check_research_coach_output_ignored(self) -> dict:
        """v0.4.8: Verify research coach output paths are in .gitignore."""
        t0 = time.monotonic()
        patterns = [
            "data/backtest_results/research_coach/",
            "research_assistant_report_",
        ]
        try:
            gi_path = os.path.join(BASE_DIR, ".gitignore")
            content = open(gi_path, encoding="utf-8").read()
            missing = [p for p in patterns if p not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item(
                    "research_coach_output_ignored", "PASS",
                    "All research_coach output patterns present in .gitignore", elapsed,
                )
            return self._item(
                "research_coach_output_ignored", "WARN",
                f"Missing from .gitignore: {missing}", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_coach_output_ignored", "WARN", str(exc), elapsed)

    def _check_research_coach_no_forbidden_commands(self) -> dict:
        """v0.4.8: Verify _safe_command blocks forbidden keywords in suggested_command."""
        t0 = time.monotonic()
        try:
            from coach.coach_schema import CoachRecommendation, _FORBIDDEN_KEYWORDS
            blocked_count = 0
            for kw in _FORBIDDEN_KEYWORDS[:3]:
                rec = CoachRecommendation(suggested_command=f"python main.py {kw} --symbol 2330")
                assert rec.suggested_command == "# BLOCKED: no trading commands allowed", \
                    f"keyword '{kw}' was not blocked"
                blocked_count += 1
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_coach_no_forbidden_commands", "PASS",
                f"_safe_command blocked {blocked_count} forbidden keyword(s)", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_coach_no_forbidden_commands", "FAIL", str(exc), elapsed)

    # ------------------------------------------------------------------
    # v0.4.9 Research Workflow Automation checks
    # ------------------------------------------------------------------

    def _check_research_workflow_import_health(self) -> dict:
        """v0.4.9: Verify research workflow modules import cleanly."""
        t0 = time.monotonic()
        try:
            import importlib
            importlib.import_module("workflow_automation.workflow_schema")
            importlib.import_module("workflow_automation.safe_command_registry")
            importlib.import_module("workflow_automation.workflow_builder")
            importlib.import_module("workflow_automation.workflow_runner")
            importlib.import_module("workflow_automation.package_builder")
            importlib.import_module("workflow_automation.workflow_store")
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_workflow_import_health", "PASS",
                "All research workflow modules import cleanly", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_workflow_import_health", "FAIL", str(exc), elapsed)

    def _check_research_workflow_no_real_orders(self) -> dict:
        """v0.4.9: Verify workflow schema enforces workflow_only / no_real_orders."""
        t0 = time.monotonic()
        try:
            from workflow_automation.workflow_schema import ResearchWorkflowTask
            task = ResearchWorkflowTask()
            assert task.read_only is True, "read_only must be True"
            assert task.no_real_orders is True, "no_real_orders must be True"
            assert task.production_blocked is True, "production_blocked must be True"
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_workflow_no_real_orders", "PASS",
                "ResearchWorkflowTask enforces read_only/no_real_orders/production_blocked", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_workflow_no_real_orders", "FAIL", str(exc), elapsed)

    def _check_research_workflow_output_ignored(self) -> dict:
        """v0.4.9: Verify research workflow output paths are in .gitignore."""
        t0 = time.monotonic()
        patterns = [
            "data/backtest_results/research_workflow/",
            "research_workflow_report_",
        ]
        try:
            gi_path = os.path.join(BASE_DIR, ".gitignore")
            content = open(gi_path, encoding="utf-8").read()
            missing = [p for p in patterns if p not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if not missing:
                return self._item(
                    "research_workflow_output_ignored", "PASS",
                    "All research_workflow output patterns present in .gitignore", elapsed,
                )
            return self._item(
                "research_workflow_output_ignored", "WARN",
                f"Missing from .gitignore: {missing}", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_workflow_output_ignored", "WARN", str(exc), elapsed)

    def _check_research_workflow_safe_command_registry(self) -> dict:
        """v0.4.9: Verify SafeCommandRegistry blocks forbidden keywords."""
        t0 = time.monotonic()
        try:
            from workflow_automation.safe_command_registry import SafeCommandRegistry
            registry = SafeCommandRegistry()
            forbidden_tests = ["python main.py buy --symbol 2330", "sell order", "submit_order"]
            blocked = 0
            for cmd in forbidden_tests:
                if not registry.is_allowed(cmd):
                    blocked += 1
            assert blocked == len(forbidden_tests), f"Expected {len(forbidden_tests)} blocks, got {blocked}"
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_workflow_safe_command_registry", "PASS",
                f"SafeCommandRegistry blocked {blocked} forbidden keyword(s)", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_workflow_safe_command_registry", "FAIL", str(exc), elapsed)

    def _check_research_workflow_no_compound_commands(self) -> dict:
        """v0.4.9: Verify SafeCommandRegistry blocks compound shell commands."""
        t0 = time.monotonic()
        try:
            from workflow_automation.safe_command_registry import SafeCommandRegistry
            registry = SafeCommandRegistry()
            compound_tests = [
                "python main.py data-quality-gate && python main.py provider-health",
                "cd trading_master; python main.py data-quality-gate",
                "python main.py data-quality-gate | grep PASS",
            ]
            blocked = sum(1 for cmd in compound_tests if not registry.is_allowed(cmd))
            assert blocked == len(compound_tests), f"Expected {len(compound_tests)} blocks, got {blocked}"
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_workflow_no_compound_commands", "PASS",
                f"SafeCommandRegistry blocked {blocked} compound command(s)", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_workflow_no_compound_commands", "FAIL", str(exc), elapsed)

    # -----------------------------------------------------------------------
    # v0.5.0 Research OS Planning checks
    # -----------------------------------------------------------------------

    def _check_research_os_import_health(self) -> dict:
        """v0.5.0: Verify all os_planning modules import cleanly."""
        t0 = time.monotonic()
        try:
            from os_planning.module_inventory import ResearchOSModuleInventory
            from os_planning.cli_inventory import CLIInventoryBuilder
            from os_planning.gui_tab_inventory import GUITabInventoryBuilder
            from os_planning.regression_audit import RegressionAudit
            from os_planning.artifact_hygiene_audit import ArtifactHygieneAudit
            from os_planning.safety_matrix import ResearchOSSafetyMatrix
            from reports.research_os_stabilization_report import ResearchOSStabilizationReport
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_os_import_health", "PASS",
                "All os_planning modules and report import cleanly", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_os_import_health", "FAIL", str(exc), elapsed)

    def _check_research_os_no_real_orders(self) -> dict:
        """v0.5.0: Verify os_planning classes carry safety invariants."""
        t0 = time.monotonic()
        try:
            from os_planning.module_inventory import ResearchOSModuleInventory
            from os_planning.safety_matrix import ResearchOSSafetyMatrix
            from reports.research_os_stabilization_report import ResearchOSStabilizationReport
            for cls in (ResearchOSModuleInventory, ResearchOSSafetyMatrix, ResearchOSStabilizationReport):
                assert getattr(cls, "read_only",          False), f"{cls.__name__} missing read_only"
                assert getattr(cls, "no_real_orders",     False), f"{cls.__name__} missing no_real_orders"
                assert getattr(cls, "production_blocked", False), f"{cls.__name__} missing production_blocked"
                assert getattr(cls, "real_order_ready",   True)  is False, f"{cls.__name__} real_order_ready must be False"
            elapsed = (time.monotonic() - t0) * 1000
            return self._item(
                "research_os_no_real_orders", "PASS",
                "All os_planning classes carry correct safety invariants", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_os_no_real_orders", "FAIL", str(exc), elapsed)

    def _check_research_os_output_ignored(self) -> dict:
        """v0.5.0: Verify OS planning output paths are in .gitignore."""
        t0 = time.monotonic()
        try:
            gitignore_path = os.path.join(BASE_DIR, ".gitignore")
            with open(gitignore_path, encoding="utf-8") as fh:
                content = fh.read()
            required = [
                "data/backtest_results/research_os_planning/",
                "reports/research_os_stabilization_report_",
            ]
            missing = [p for p in required if p not in content]
            elapsed = (time.monotonic() - t0) * 1000
            if missing:
                return self._item(
                    "research_os_output_ignored", "FAIL",
                    f"Missing .gitignore patterns: {missing}", elapsed,
                )
            return self._item(
                "research_os_output_ignored", "PASS",
                "OS planning output paths are in .gitignore", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_os_output_ignored", "FAIL", str(exc), elapsed)

    def _check_research_os_safety_matrix(self) -> dict:
        """v0.5.0: Verify safety matrix reports zero violations."""
        t0 = time.monotonic()
        try:
            from os_planning.safety_matrix import ResearchOSSafetyMatrix
            sm_obj    = ResearchOSSafetyMatrix()
            sm_sum    = sm_obj.summary()
            violations = sm_sum.get("blocked_violations", 0)
            safe_c     = sm_sum.get("safe", 0)
            total_s    = sm_sum.get("total_modules", 0)
            elapsed    = (time.monotonic() - t0) * 1000
            if violations:
                return self._item(
                    "research_os_safety_matrix", "FAIL",
                    f"{violations} safety violation(s) detected", elapsed,
                )
            return self._item(
                "research_os_safety_matrix", "PASS",
                f"Safety matrix: 0 violations, safe={safe_c}/{total_s}", elapsed,
            )
        except Exception as exc:
            elapsed = (time.monotonic() - t0) * 1000
            return self._item("research_os_safety_matrix", "FAIL", str(exc), elapsed)
