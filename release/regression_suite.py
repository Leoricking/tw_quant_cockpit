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
        """Run the full 17-test suite (quick + extended + v0.4.1)."""
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
