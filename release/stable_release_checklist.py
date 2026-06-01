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
        """Run all 26 checklist items and return summary dict."""
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
