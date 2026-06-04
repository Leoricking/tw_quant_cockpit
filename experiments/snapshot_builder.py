"""
experiments/snapshot_builder.py — ExperimentSnapshotBuilder: build point-in-time snapshots (v0.3.29).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""

import datetime
import glob
import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_VERSION = "v0.3.29"


def _now_iso() -> str:
    return datetime.datetime.now().isoformat()


def _empty_snapshot(snapshot_type: str, source_files: list = None, warnings: list = None) -> dict:
    return {
        "snapshot_type": snapshot_type,
        "generated_at": _now_iso(),
        "source_files": source_files or [],
        "summary": {},
        "warnings": warnings or [],
        "version_info": {"version": _VERSION},
    }


class ExperimentSnapshotBuilder:
    """
    Builds point-in-time JSON snapshots of the research environment.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        results_dir: str = "data/backtest_results",
        report_dir: str = "reports",
        import_root: str = "data/import",
    ):
        self._results_dir = os.path.join(BASE_DIR, results_dir)
        self._report_dir = os.path.join(BASE_DIR, report_dir)
        self._import_root = os.path.join(BASE_DIR, import_root)

    # ------------------------------------------------------------------
    # Public builders
    # ------------------------------------------------------------------

    def build_config_snapshot(self) -> dict:
        """Snapshot type: config. Records mode, git, python version."""
        snap = _empty_snapshot("config")
        try:
            import subprocess

            # git commit
            git_commit = ""
            try:
                r = subprocess.run(
                    ["git", "-C", BASE_DIR, "rev-parse", "--short", "HEAD"],
                    capture_output=True, text=True, timeout=5,
                )
                if r.returncode == 0:
                    git_commit = r.stdout.strip()
            except Exception:
                pass

            # git tag
            git_tag = ""
            try:
                r = subprocess.run(
                    ["git", "-C", BASE_DIR, "describe", "--tags", "--exact-match", "HEAD"],
                    capture_output=True, text=True, timeout=5,
                )
                if r.returncode == 0:
                    git_tag = r.stdout.strip()
            except Exception:
                pass

            mode = os.environ.get("TW_MODE", "real")

            snap["summary"] = {
                "mode": mode,
                "git_commit": git_commit,
                "git_tag": git_tag,
                "timestamp": _now_iso(),
                "python_version": sys.version,
            }
            snap["source_files"] = [os.path.join(BASE_DIR, "config.py")]

        except Exception:
            logger.exception("build_config_snapshot failed")
            snap["warnings"].append("build_config_snapshot raised an exception")

        return snap

    def build_universe_snapshot(self, universe_name: str = None) -> dict:
        """Snapshot type: universe. Captures universe composition summary."""
        source_files = []
        snap = _empty_snapshot("universe", source_files)
        try:
            universe_dir = os.path.join(BASE_DIR, "universe")
            source_files.append(universe_dir)

            from universe.universe_registry import UniverseRegistry
            reg = UniverseRegistry()
            universes = reg.list_universes()

            target = None
            if universe_name:
                for u in universes:
                    if u.get("name") == universe_name or u.get("universe_name") == universe_name:
                        target = u
                        break
            if target is None and universes:
                target = universes[0]

            if target is not None:
                u_name = target.get("name") or target.get("universe_name") or universe_name or ""
                symbols = target.get("symbols", [])
                sectors = target.get("sectors", target.get("sector_map", {}))
                themes = target.get("themes", target.get("theme_map", {}))
                snap["summary"] = {
                    "universe_name": u_name,
                    "universe_size": len(symbols),
                    "sector_count": len(sectors),
                    "theme_count": len(themes),
                    "symbols_preview": symbols[:10],
                }
            else:
                snap["summary"] = {
                    "universe_name": universe_name or "",
                    "universe_size": 0,
                    "sector_count": 0,
                    "theme_count": 0,
                    "symbols_preview": [],
                }
                snap["warnings"].append("No universe data found")

        except Exception:
            logger.exception("build_universe_snapshot failed")
            snap["warnings"].append("build_universe_snapshot raised an exception")

        snap["source_files"] = source_files
        return snap

    def build_data_quality_snapshot(self) -> dict:
        """Snapshot type: data_quality. Runs DataQualityGate and captures score."""
        snap = _empty_snapshot("data_quality")
        try:
            from quality.data_quality_gate import DataQualityGate
            gate = DataQualityGate()
            result = gate.run()

            snap["summary"] = {
                "production_readiness_score": result.get("production_readiness_score",
                                                          result.get("score", 0)),
                "backtest_readiness_score": result.get("backtest_readiness_score", 0),
                "production_blocked": True,
                "data_freshness_summary": result.get("data_freshness_summary",
                                                      result.get("freshness_summary", [])),
                "overall_status": result.get("overall_status", result.get("status", "UNKNOWN")),
            }
            snap["source_files"] = [os.path.join(BASE_DIR, "quality")]

        except Exception:
            logger.exception("build_data_quality_snapshot failed")
            snap["warnings"].append("build_data_quality_snapshot raised an exception")

        return snap

    def build_provider_reliability_snapshot(self) -> dict:
        """Snapshot type: provider_reliability. Captures provider score summary."""
        snap = _empty_snapshot("provider_reliability")
        try:
            from data.providers.provider_reliability import ProviderReliabilityMatrix
            matrix = ProviderReliabilityMatrix()
            result = matrix.build()

            providers = result.get("providers", result.get("provider_scores", {}))
            scores = []
            if isinstance(providers, dict):
                scores = [v for v in providers.values() if isinstance(v, (int, float))]
            elif isinstance(providers, list):
                scores = [p.get("score", 0) for p in providers if isinstance(p, dict)]

            avg_score = sum(scores) / len(scores) if scores else 0.0

            snap["summary"] = {
                "provider_reliability_score": round(avg_score, 4),
                "weak_datasets": result.get("weak_datasets", []),
                "fallback_count": result.get("fallback_count", 0),
                "provider_count": len(scores),
            }
            snap["source_files"] = [os.path.join(BASE_DIR, "data", "providers")]

        except Exception:
            logger.exception("build_provider_reliability_snapshot failed")
            snap["warnings"].append("build_provider_reliability_snapshot raised an exception")

        return snap

    def build_rule_governance_snapshot(self) -> dict:
        """Snapshot type: rule_governance. Captures rule registry summary."""
        snap = _empty_snapshot("rule_governance")
        try:
            from governance.rule_registry import RuleRegistry
            reg = RuleRegistry()
            reg.load_builtin_rules()
            s = reg.build_rule_summary()

            high_confidence = 0
            unknown_confidence = 0
            try:
                from governance.rule_confidence_scorer import RuleConfidenceScorer
                scorer = RuleConfidenceScorer()
                confidence_result = scorer.score_all(reg)
                high_confidence = confidence_result.get("high_confidence", 0)
                unknown_confidence = confidence_result.get("unknown_confidence", 0)
            except Exception:
                logger.warning("RuleConfidenceScorer not available for rule snapshot")

            snap["summary"] = {
                "total_rules": s.get("total_rules", s.get("total", 0)),
                "active": s.get("active", 0),
                "experimental": s.get("experimental", 0),
                "needs_review": s.get("needs_review", 0),
                "high_confidence": high_confidence,
                "unknown_confidence": unknown_confidence,
            }
            snap["source_files"] = [os.path.join(BASE_DIR, "governance")]

        except Exception:
            logger.exception("build_rule_governance_snapshot failed")
            snap["warnings"].append("build_rule_governance_snapshot raised an exception")

        return snap

    def build_backtest_snapshot(self) -> dict:
        """Snapshot type: backtest. Loads most recent backtest result JSON."""
        snap = _empty_snapshot("backtest")
        found_files = []
        hardened = None
        portfolio = None
        try:
            if os.path.isdir(self._results_dir):
                # Hardened backtest
                patterns = [
                    os.path.join(self._results_dir, "hardened_backtest_result_*.json"),
                    os.path.join(self._results_dir, "*_metrics.json"),
                ]
                backtest_files = []
                for pat in patterns:
                    backtest_files.extend(glob.glob(pat))

                if backtest_files:
                    latest_bt = max(backtest_files, key=os.path.getmtime)
                    found_files.append(latest_bt)
                    with open(latest_bt, "r", encoding="utf-8") as f:
                        bt_data = json.load(f)
                    hardened = {
                        "net_return": bt_data.get("net_return", bt_data.get("total_return", None)),
                        "sharpe": bt_data.get("sharpe", bt_data.get("sharpe_ratio", None)),
                        "max_drawdown": bt_data.get("max_drawdown", None),
                        "validation_score": bt_data.get("validation_score", None),
                        "confidence_grade": bt_data.get("confidence_grade", None),
                        "source_file": os.path.basename(latest_bt),
                    }

                # Portfolio simulation
                port_patterns = [
                    os.path.join(self._results_dir, "portfolio_simulation_*.json"),
                    os.path.join(self._results_dir, "portfolio_*.json"),
                ]
                port_files = []
                for pat in port_patterns:
                    port_files.extend(glob.glob(pat))

                if port_files:
                    latest_port = max(port_files, key=os.path.getmtime)
                    found_files.append(latest_port)
                    with open(latest_port, "r", encoding="utf-8") as f:
                        port_data = json.load(f)
                    portfolio = {
                        "sharpe": port_data.get("sharpe", port_data.get("sharpe_ratio", None)),
                        "max_drawdown": port_data.get("max_drawdown", None),
                        "profit_factor": port_data.get("profit_factor", None),
                        "trade_count": port_data.get("trade_count", port_data.get("total_trades", None)),
                        "source_file": os.path.basename(latest_port),
                    }
            else:
                snap["warnings"].append(f"results_dir not found: {self._results_dir}")

            snap["summary"] = {
                "hardened_backtest": hardened,
                "portfolio": portfolio,
                "found_files": [os.path.basename(f) for f in found_files],
            }
            snap["source_files"] = found_files

        except Exception:
            logger.exception("build_backtest_snapshot failed")
            snap["warnings"].append("build_backtest_snapshot raised an exception")

        return snap

    def build_signal_quality_snapshot(self) -> dict:
        """Snapshot type: signal_quality. Loads most recent signal quality JSON."""
        snap = _empty_snapshot("signal_quality")
        try:
            if os.path.isdir(self._results_dir):
                patterns = [
                    os.path.join(self._results_dir, "signal_quality_result_*.json"),
                    os.path.join(self._results_dir, "signal_quality_*.json"),
                ]
                files = []
                for pat in patterns:
                    files.extend(glob.glob(pat))

                if files:
                    latest = max(files, key=os.path.getmtime)
                    snap["source_files"] = [latest]
                    with open(latest, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    snap["summary"] = {
                        "boost_count": data.get("boost_count", 0),
                        "keep_count": data.get("keep_count", 0),
                        "reduce_count": data.get("reduce_count", 0),
                        "disable_count": data.get("disable_count", 0),
                        "total_signals": data.get("total_signals", 0),
                        "generated_at": data.get("generated_at", ""),
                    }
                else:
                    snap["warnings"].append("No signal quality result files found")
                    snap["summary"] = {
                        "boost_count": 0, "keep_count": 0,
                        "reduce_count": 0, "disable_count": 0,
                        "total_signals": 0, "generated_at": "",
                    }
            else:
                snap["warnings"].append(f"results_dir not found: {self._results_dir}")

        except Exception:
            logger.exception("build_signal_quality_snapshot failed")
            snap["warnings"].append("build_signal_quality_snapshot raised an exception")

        return snap

    def build_portfolio_snapshot(self) -> dict:
        """Snapshot type: portfolio. Loads most recent portfolio simulation JSON."""
        snap = _empty_snapshot("portfolio")
        try:
            if os.path.isdir(self._results_dir):
                patterns = [
                    os.path.join(self._results_dir, "portfolio_simulation_*.json"),
                    os.path.join(self._results_dir, "portfolio_*.json"),
                ]
                files = []
                for pat in patterns:
                    files.extend(glob.glob(pat))

                if files:
                    latest = max(files, key=os.path.getmtime)
                    snap["source_files"] = [latest]
                    with open(latest, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    snap["summary"] = {
                        "scenario": data.get("scenario", data.get("scenario_name", "")),
                        "sharpe": data.get("sharpe", data.get("sharpe_ratio", None)),
                        "max_drawdown": data.get("max_drawdown", None),
                        "profit_factor": data.get("profit_factor", None),
                        "trade_count": data.get("trade_count", data.get("total_trades", None)),
                    }
                else:
                    snap["warnings"].append("No portfolio simulation files found")
                    snap["summary"] = {
                        "scenario": "", "sharpe": None,
                        "max_drawdown": None, "profit_factor": None, "trade_count": None,
                    }
            else:
                snap["warnings"].append(f"results_dir not found: {self._results_dir}")

        except Exception:
            logger.exception("build_portfolio_snapshot failed")
            snap["warnings"].append("build_portfolio_snapshot raised an exception")

        return snap

    def build_intraday_snapshot(self) -> dict:
        """Snapshot type: intraday. Runs IntradayQualityChecker."""
        snap = _empty_snapshot("intraday")
        try:
            from intraday.intraday_quality import IntradayQualityChecker
            checker = IntradayQualityChecker()
            result = checker.run()

            snap["summary"] = {
                "overall_quality_score": result.get("overall_quality_score",
                                                     result.get("quality_score", 0)),
                "symbol_count": result.get("symbol_count", 0),
                "fake_breakout_warnings": len(result.get("fake_breakout_warnings",
                                               result.get("fake_breakouts", []))),
                "tick_bidask_ready": False,
                "intraday_status": result.get("status", result.get("intraday_status", "UNKNOWN")),
            }
            snap["source_files"] = [os.path.join(BASE_DIR, "intraday")]

        except Exception:
            logger.exception("build_intraday_snapshot failed")
            snap["warnings"].append("build_intraday_snapshot raised an exception")

        return snap

    def build_generated_reports_snapshot(self) -> dict:
        """Snapshot type: reports. Scans reports dir for markdown files."""
        snap = _empty_snapshot("reports")
        try:
            report_files = []
            if os.path.isdir(self._report_dir):
                report_files = glob.glob(os.path.join(self._report_dir, "*.md"))

            most_recent = ""
            if report_files:
                most_recent = os.path.basename(max(report_files, key=os.path.getmtime))

            snap["summary"] = {
                "report_count": len(report_files),
                "report_paths": [os.path.basename(p) for p in report_files],
                "failed_reports": 0,
                "most_recent": most_recent,
            }
            snap["source_files"] = [self._report_dir]

        except Exception:
            logger.exception("build_generated_reports_snapshot failed")
            snap["warnings"].append("build_generated_reports_snapshot raised an exception")

        return snap

    def build_ml_feature_snapshot(self) -> dict:
        """Snapshot type: ml_feature_store. Loads ML Feature Store catalog summary (v0.4.2)."""
        snap = _empty_snapshot("ml_feature_store")
        try:
            from ml.feature_catalog import FeatureCatalog
            catalog = FeatureCatalog()
            summary = catalog.summary()
            snap["summary"] = {
                "total_features":       summary.get("total_features", 0),
                "enabled_features":     summary.get("enabled_features", 0),
                "experimental_features": summary.get("experimental_features", 0),
                "high_leakage_risk":    summary.get("high_leakage_risk", 0),
                "categories":           summary.get("categories", {}),
                "research_only":        True,
                "no_real_orders":       True,
                "production_blocked":   True,
            }
            snap["status"] = "OK"
        except Exception:
            logger.exception("build_ml_feature_snapshot failed")
            snap["warnings"].append("build_ml_feature_snapshot raised an exception")
        return snap

    def build_model_monitoring_snapshot(self) -> dict:
        """Snapshot type: model_monitoring. Loads Model Monitoring summary (v0.4.3)."""
        snap = _empty_snapshot("model_monitoring")
        try:
            from monitoring.monitoring_summary import ModelMonitoringSummary
            summary = ModelMonitoringSummary().run()
            snap["summary"] = {
                "model_count":       summary.get("model_count", 0),
                "prediction_count":  summary.get("prediction_count", 0),
                "reviewed_count":    summary.get("reviewed_count", 0),
                "hit_rate":          summary.get("hit_rate"),
                "drift_status":      summary.get("drift_status", "—"),
                "degradation_status": summary.get("degradation_status", "—"),
                "rule_vs_ml_status": summary.get("rule_vs_ml_status", "—"),
                "research_only":     True,
                "no_real_orders":    True,
                "monitoring_only":   True,
            }
            snap["status"] = "OK"
        except Exception:
            logger.exception("build_model_monitoring_snapshot failed")
            snap["warnings"].append("build_model_monitoring_snapshot raised an exception")
        return snap

    def build_intraday_replay_snapshot(self) -> dict:
        """Snapshot type: intraday_replay. Loads Intraday Replay session summary (v0.4.4)."""
        snap = _empty_snapshot("intraday_replay")
        try:
            from replay.replay_session import ReplaySessionManager
            mgr = ReplaySessionManager()
            summary = mgr.summary()
            sessions = mgr.list_sessions(limit=1000)
            completed_count = sum(1 for s in sessions if s.get("status") == "COMPLETED")
            snap["summary"] = {
                "total_sessions":           summary.get("total", 0),
                "sessions_completed":       completed_count,
                "by_status":                summary.get("by_status", {}),
                "research_only":            True,
                "no_real_orders":           True,
                "replay_training_only":     True,
            }
            snap["status"] = "OK"
        except Exception:
            logger.exception("build_intraday_replay_snapshot failed")
            snap["warnings"].append("build_intraday_replay_snapshot raised an exception")
        return snap

    def build_strategy_knowledge_snapshot(self) -> dict:
        """
        Snapshot type: strategy_knowledge. Loads knowledge store summary (v0.4.1.1).
        [!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        [!] auto_activated=False. Transcript-only confidence <= PARTIAL.
        """
        snap = _empty_snapshot("strategy_knowledge")
        try:
            from knowledge.knowledge_store import StrategyKnowledgeStore
            store = StrategyKnowledgeStore()
            summary = store.build_summary()
            snap["summary"] = {
                "sources_count":           summary.get("sources_count", 0),
                "knowledge_items_count":   summary.get("total_items", 0),
                "rule_candidates_count":   summary.get("rule_candidates_count", 0),
                "avoid_conditions_count":  summary.get("avoid_conditions_count", 0),
                "risk_conditions_count":   summary.get("risk_conditions_count", 0),
                "factor_candidates_count": summary.get("factor_candidates_count", 0),
                "latest_ingestion_at":     summary.get("latest_ingestion_at", ""),
                "knowledge_only":          True,
                "research_only":           True,
                "no_real_orders":          True,
                "auto_activated":          False,
            }
            snap["status"] = "OK"
        except Exception:
            logger.exception("build_strategy_knowledge_snapshot failed")
            snap["warnings"].append("build_strategy_knowledge_snapshot raised an exception")
        return snap

    def build_ml_knowledge_integration_snapshot(self) -> dict:
        """
        Snapshot type: ml_knowledge_integration. Loads ML knowledge integration summary (v0.4.2.1).
        [!] ML Research Only. No Real Orders. auto_enabled=False.
        """
        snap = _empty_snapshot("ml_knowledge_integration")
        try:
            from ml.knowledge_dataset_exporter import KnowledgeDatasetExporter
            exporter = KnowledgeDatasetExporter()
            summary = exporter.load_latest_summary()
            if not summary:
                snap["warnings"].append(
                    "No ml_knowledge_integration_summary.json found — run ml-knowledge-integrate first"
                )
                snap["summary"] = {
                    "total_features":    0,
                    "model_ready":       0,
                    "auto_enabled":      0,
                    "leakage_findings":  0,
                    "status":            "NO_DATA",
                }
                return snap
            snap["summary"] = {
                "total_features":    summary.get("total_features", 0),
                "model_ready":       summary.get("model_ready_features", 0),
                "auto_enabled":      0,
                "leakage_findings":  summary.get("leakage_findings", 0),
                "critical_leakage":  summary.get("critical_leakage", 0),
                "ml_research_only":  True,
                "no_real_orders":    True,
                "generated_at":      summary.get("generated_at", ""),
            }
            snap["status"] = "OK"
        except Exception:
            logger.exception("build_ml_knowledge_integration_snapshot failed")
            snap["warnings"].append("build_ml_knowledge_integration_snapshot raised an exception")
        return snap

    def build_notification_snapshot(self) -> dict:
        """
        Snapshot type: notification_center. Loads notification summary (v0.4.5).
        [!] Notification Only. Research Only. No Real Orders.
        """
        snap = _empty_snapshot("notification_center")
        try:
            from gui.notification_center_adapter import NotificationCenterAdapter
            adapter = NotificationCenterAdapter()
            summary = adapter.get_summary()
            snap["summary"] = {
                "total_events":      summary.get("total_events", 0),
                "unread_count":      summary.get("unread_count", 0),
                "critical_count":    summary.get("critical_count", 0),
                "error_count":       summary.get("error_count", 0),
                "warning_count":     summary.get("warning_count", 0),
                "external_enabled":  False,
                "notification_only": True,
                "no_real_orders":    True,
            }
            snap["status"] = "OK"
        except Exception:
            logger.exception("build_notification_snapshot failed")
            snap["warnings"].append("build_notification_snapshot raised an exception")
        return snap

    def build_portfolio_journal_snapshot(self) -> dict:
        """
        Snapshot type: portfolio_journal. Loads journal summary (v0.4.6).
        [!] Journal Only. Research Only. No Real Orders.
        """
        snap = _empty_snapshot("portfolio_journal")
        try:
            from gui.portfolio_journal_adapter import PortfolioJournalAdapter
            adapter = PortfolioJournalAdapter()
            summary = adapter.build_summary()
            snap["summary"] = {
                "entries_count":        summary.get("entries_count", 0),
                "reviewed_count":       summary.get("reviewed_count", 0),
                "review_required_count": summary.get("review_required_count", 0),
                "most_common_mistake":  summary.get("most_common_mistake", ""),
                "latest_entry_at":      summary.get("latest_entry_at", ""),
                "journal_only":         True,
                "no_real_orders":       True,
            }
            snap["status"] = "OK"
        except Exception:
            logger.exception("build_portfolio_journal_snapshot failed")
            snap["warnings"].append("build_portfolio_journal_snapshot raised an exception")
        return snap

    def build_all(self, universe_name: str = None) -> dict:
        """
        Build all available snapshots. Each builder is called independently;
        failures in one do not prevent others from running.
        Returns a dict mapping snapshot_type -> snapshot dict.
        """
        result = {}
        builders = [
            ("config", lambda: self.build_config_snapshot()),
            ("universe", lambda: self.build_universe_snapshot(universe_name)),
            ("data_quality", lambda: self.build_data_quality_snapshot()),
            ("provider_reliability", lambda: self.build_provider_reliability_snapshot()),
            ("rule_governance", lambda: self.build_rule_governance_snapshot()),
            ("backtest", lambda: self.build_backtest_snapshot()),
            ("signal_quality", lambda: self.build_signal_quality_snapshot()),
            ("portfolio", lambda: self.build_portfolio_snapshot()),
            ("intraday", lambda: self.build_intraday_snapshot()),
            ("reports", lambda: self.build_generated_reports_snapshot()),
            ("ml_feature_store",       lambda: self.build_ml_feature_snapshot()),
            ("model_monitoring",       lambda: self.build_model_monitoring_snapshot()),
            ("intraday_replay",        lambda: self.build_intraday_replay_snapshot()),
            ("strategy_knowledge",          lambda: self.build_strategy_knowledge_snapshot()),
            ("ml_knowledge_integration",    lambda: self.build_ml_knowledge_integration_snapshot()),
            ("notification_center",         lambda: self.build_notification_snapshot()),
            ("portfolio_journal",           lambda: self.build_portfolio_journal_snapshot()),
            ("research_review",             lambda: self.build_research_review_snapshot()),
            ("research_coach",              lambda: self.build_research_coach_snapshot()),
            ("research_workflow",           lambda: self.build_research_workflow_snapshot()),
            ("research_os_planning",        lambda: self.build_research_os_planning_snapshot()),
            ("cli_ux",                      lambda: self.build_cli_ux_snapshot()),
            ("gui_navigation",              lambda: self.build_gui_navigation_snapshot()),
            ("regression_suite",            lambda: self.build_regression_snapshot()),
            ("data_stabilization",          lambda: self.build_data_stabilization_snapshot()),
        ]
        for snap_type, fn in builders:
            try:
                snap = fn()
                result[snap_type] = snap
            except Exception:
                logger.exception("build_all: %s snapshot raised uncaught exception", snap_type)
                result[snap_type] = _empty_snapshot(snap_type, warnings=[f"{snap_type} snapshot failed"])

        return result

    # ------------------------------------------------------------------
    # v0.4.7 Research Review Dashboard snapshot
    # ------------------------------------------------------------------

    def build_research_review_snapshot(self) -> dict:
        """
        Build a point-in-time snapshot of the Research Review Dashboard state.

        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap: dict = {
            "snapshot_type":    "research_review",
            "generated_at":     _now_iso(),
            "source_files":     [],
            "summary":          {},
            "warnings":         [],
            "version_info":     {"version": _VERSION},
        }
        try:
            store_dir = os.path.join(self.results_dir, "research_review")
            summary_csv = os.path.join(store_dir, "review_summary.csv")
            scorecard_csv = os.path.join(store_dir, "review_scorecard.csv")

            summary_data: dict = {}
            scorecard_data: dict = {}

            if os.path.exists(summary_csv):
                snap["source_files"].append(summary_csv)
                import csv as _csv
                with open(summary_csv, newline="", encoding="utf-8") as f:
                    rows = list(_csv.DictReader(f))
                    if rows:
                        summary_data = rows[0]
            else:
                snap["warnings"].append("review_summary.csv not found — run research-review first")

            if os.path.exists(scorecard_csv):
                snap["source_files"].append(scorecard_csv)
                import csv as _csv
                with open(scorecard_csv, newline="", encoding="utf-8") as f:
                    rows = list(_csv.DictReader(f))
                    if rows:
                        scorecard_data = rows[0]

            snap["summary"] = {
                "overall_score":      scorecard_data.get("overall_review_score", "UNKNOWN"),
                "overall_grade":      scorecard_data.get("overall_grade", "UNKNOWN"),
                "open_items":         summary_data.get("open_items", 0),
                "critical_count":     summary_data.get("critical_items", 0),
                "warnings_count":     summary_data.get("warning_items", 0),
                "top_mistake":        summary_data.get("most_common_mistake", ""),
                "action_items_count": summary_data.get("action_items_count", 0),
                "latest_review_at":   summary_data.get("generated_at", ""),
                "read_only":          True,
                "no_real_orders":     True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("build_research_review_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    # ------------------------------------------------------------------
    # v0.4.8 Research Assistant / Coach snapshot
    # ------------------------------------------------------------------

    def build_research_coach_snapshot(self) -> dict:
        """
        Build a point-in-time snapshot of the Research Assistant / Coach state.

        [!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap: dict = {
            "snapshot_type": "research_coach",
            "generated_at":  _now_iso(),
            "source_files":  [],
            "summary":       {},
            "warnings":      [],
            "version_info":  {"version": _VERSION},
        }
        try:
            store_dir  = os.path.join(self.results_dir, "research_coach")
            summary_csv = os.path.join(store_dir, "coach_summary.csv")
            recs_csv    = os.path.join(store_dir, "coach_recommendations.csv")

            summary_data: dict = {}

            if os.path.exists(summary_csv):
                snap["source_files"].append(summary_csv)
                import csv as _csv
                with open(summary_csv, newline="", encoding="utf-8") as f:
                    rows = list(_csv.DictReader(f))
                    if rows:
                        summary_data = rows[-1]
            else:
                snap["warnings"].append("coach_summary.csv not found — run research-coach first")

            recommendations_count = 0
            if os.path.exists(recs_csv):
                snap["source_files"].append(recs_csv)
                import csv as _csv
                with open(recs_csv, newline="", encoding="utf-8") as f:
                    recommendations_count = sum(1 for _ in _csv.DictReader(f))

            latest_at = summary_data.get("generated_at", "")
            snap["summary"] = {
                "recommendations_count": recommendations_count,
                "p0_count":              summary_data.get("p0_count", 0),
                "p1_count":              summary_data.get("p1_count", 0),
                "replay_tasks_count":    summary_data.get("replay_tasks_count", 0),
                "rule_reviews_count":    summary_data.get("rule_review_count", 0),
                "data_repair_count":     summary_data.get("data_repair_count", 0),
                "latest_coach_at":       latest_at,
                "coaching_only":         True,
                "no_real_orders":        True,
                "production_blocked":    True,
            }
        except Exception as exc:
            logger.warning("build_research_coach_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    # ------------------------------------------------------------------
    # v0.4.9 Research Workflow Automation snapshot
    # ------------------------------------------------------------------

    def build_research_workflow_snapshot(self) -> dict:
        """
        Build a point-in-time snapshot of the Research Workflow Automation state.

        [!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap: dict = {
            "snapshot_type": "research_workflow",
            "generated_at":  _now_iso(),
            "source_files":  [],
            "summary":       {},
            "warnings":      [],
            "version_info":  {"version": "v0.4.9"},
        }
        try:
            from workflow_automation.workflow_store import ResearchWorkflowStore
            store = ResearchWorkflowStore()
            summary = store.load_latest_summary()
            if not summary:
                snap["warnings"].append("No workflow summary found")
                return snap
            latest_at = summary.get("created_at", "")
            snap["source_files"] = ["data/backtest_results/research_workflow/workflow_summary.csv"]
            snap["summary"] = {
                "latest_workflow_id":   summary.get("workflow_id", ""),
                "tasks_total":          summary.get("tasks_total", 0),
                "passed_count":         summary.get("tasks_passed", 0),
                "failed_count":         summary.get("tasks_failed", 0),
                "blocked_count":        summary.get("tasks_skipped", 0),
                "package_path":         summary.get("output_package_path", ""),
                "latest_workflow_at":   latest_at,
                "workflow_only":        True,
                "no_real_orders":       True,
                "production_blocked":   True,
            }
        except Exception as exc:
            logger.warning("build_research_workflow_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    # ------------------------------------------------------------------
    # v0.5.0 Research OS Planning snapshot
    # ------------------------------------------------------------------

    def build_research_os_planning_snapshot(self) -> dict:
        snap = {
            "snapshot_type":          "research_os_planning",
            "read_only":              True,
            "no_real_orders":         True,
            "production_blocked":     True,
            "real_order_ready":       False,
            "total_modules":          0,
            "total_commands":         0,
            "total_tabs":             0,
            "mature_count":           0,
            "safety_score":           "N/A",
            "coverage_score":         "N/A",
            "warnings":               [],
        }
        try:
            from os_planning.module_inventory import ResearchOSModuleInventory
            from os_planning.cli_inventory import CLIInventoryBuilder
            from os_planning.gui_tab_inventory import GUITabInventoryBuilder
            modules  = ResearchOSModuleInventory().build_inventory()
            commands = CLIInventoryBuilder().build_inventory()
            tabs     = GUITabInventoryBuilder().build_inventory()
            snap["total_modules"]  = len(modules)
            snap["mature_count"]   = sum(1 for m in modules if m.get("maturity") == "STABLE")
            snap["total_commands"] = len(commands)
            snap["total_tabs"]     = len(tabs)
        except Exception as exc:
            logger.warning("build_research_os_planning_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    # ------------------------------------------------------------------
    # v0.5.1 CLI UX snapshot
    # ------------------------------------------------------------------

    def build_cli_ux_snapshot(self) -> dict:
        snap = {
            "snapshot_type":       "cli_ux",
            "read_only":           True,
            "no_real_orders":      True,
            "production_blocked":  True,
            "real_order_ready":    False,
            "commands_count":      0,
            "alias_count":         0,
            "categories_count":    0,
            "conflict_count":      0,
            "missing_examples":    0,
            "latest_cli_ux_at":    "",
            "warnings":            [],
        }
        try:
            from cli.cli_ux_report import CLIUXReportBuilder
            from datetime import datetime
            data = CLIUXReportBuilder().build()
            snap["commands_count"]    = data.get("commands_count",  0)
            snap["alias_count"]       = data.get("alias_count",     0)
            snap["categories_count"]  = data.get("categories_count", 0)
            snap["conflict_count"]    = data.get("conflict_count",  0)
            snap["missing_examples"]  = len(data.get("missing_examples", []))
            snap["latest_cli_ux_at"]  = datetime.now().strftime("%Y-%m-%d")
        except Exception as exc:
            logger.warning("build_cli_ux_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    def build_gui_navigation_snapshot(self) -> dict:
        """
        Build a point-in-time snapshot of the GUI Navigation state (v0.5.2).

        [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap = {
            "snapshot_type":       "gui_navigation",
            "read_only":           True,
            "no_real_orders":      True,
            "production_blocked":  True,
            "real_order_ready":    False,
            "tabs_count":          0,
            "groups_count":        0,
            "favorite_count":      0,
            "recent_count":        0,
            "safety_status":       "PASS",
            "latest_gui_nav_at":   "",
            "warnings":            [],
        }
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            from gui.navigation.navigation_report_data import GUINavigationReportData
            from gui.navigation.navigation_state import NavigationState
            from datetime import datetime
            reg     = GUITabRegistry()
            data    = GUINavigationReportData(registry=reg)
            summary = data.build_summary()
            state   = NavigationState()
            state.load()
            snap["tabs_count"]       = summary.get("total_tabs",   0)
            snap["groups_count"]     = summary.get("groups_count", 0)
            snap["favorite_count"]   = len(state.get_favorites())
            snap["recent_count"]     = len(state.get_recent_tabs())
            snap["safety_status"]    = summary.get("safety_status", "PASS")
            snap["latest_gui_nav_at"] = datetime.now().strftime("%Y-%m-%d")
        except Exception as exc:
            logger.warning("build_gui_navigation_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    # ------------------------------------------------------------------
    # v0.5.3 Regression Suite Consolidation snapshot
    # ------------------------------------------------------------------

    def build_regression_snapshot(self) -> dict:
        """Build a point-in-time snapshot of the Regression Suite Consolidation state.

        [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap: dict = {
            "snapshot_type": "regression_suite",
            "generated_at":  _now_iso(),
            "source_files":  [],
            "summary":       {},
            "warnings":      [],
            "version_info":  {"version": _VERSION},
        }
        try:
            from regression.regression_store import RegressionStore
            store = RegressionStore()
            summary = store.load_latest_summary()
            coverage = store.load_latest_coverage_matrix()
            snap["summary"]         = summary
            snap["coverage_count"]  = len(coverage)
            snap["suite"]           = summary.get("suite", "")
            snap["status"]          = summary.get("status", "UNKNOWN")
            snap["total_tests"]     = summary.get("total", 0)
            snap["passed"]          = summary.get("passed", 0)
            snap["failed"]          = summary.get("failed", 0)
            snap["warnings_count"]  = summary.get("warnings", 0)
            if not summary:
                snap["warnings"].append("No regression summary found — run regression-run first")
        except Exception as exc:
            logger.warning("build_regression_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    def build_data_stabilization_snapshot(self) -> dict:
        """Build a point-in-time snapshot of Data / Feature Store Stabilization state.

        [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap: dict = {
            "snapshot_type":             "data_stabilization",
            "generated_at":              _now_iso(),
            "source_files":              [],
            "summary":                   {},
            "warnings":                  [],
            "version_info":              {"version": _VERSION},
            "datasets_checked":          0,
            "readiness_score":           0.0,
            "health_score":              0.0,
            "leakage_warnings":          0,
            "overall_status":            "UNKNOWN",
            "latest_data_stabilization_at": "",
        }
        try:
            from gui.data_stabilization_adapter import DataStabilizationAdapter
            adapter = DataStabilizationAdapter()
            summary = adapter.load_latest_summary()
            if summary:
                snap["datasets_checked"]          = int(summary.get("datasets_checked", 0) or 0)
                snap["readiness_score"]           = float(summary.get("readiness_score", 0.0) or 0.0)
                snap["health_score"]              = float(summary.get("health_score", 0.0) or 0.0)
                snap["leakage_warnings"]          = int(summary.get("leakage_warnings", 0) or 0)
                snap["overall_status"]            = summary.get("overall_status", "UNKNOWN")
                snap["latest_data_stabilization_at"] = summary.get("generated_at", "")
                snap["summary"]                   = summary
            else:
                snap["warnings"].append(
                    "No data stabilization summary found — run: python main.py data-stabilization --mode real"
                )
        except Exception as exc:
            logger.warning("build_data_stabilization_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    def build_replay_training_snapshot(self) -> dict:
        """Build a point-in-time snapshot of the TW Replay Training Cockpit state.

        Returns dict with: latest_session_id, latest_symbol, latest_score,
        mistakes_count, drills_count, hidden_future_data, latest_replay_training_at.

        [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap: dict = {
            "snapshot_type":              "replay_training",
            "generated_at":               _now_iso(),
            "source_files":               [],
            "summary":                    {},
            "warnings":                   [],
            "version_info":               {"version": _VERSION},
            "latest_session_id":          "",
            "latest_symbol":              "",
            "latest_score":               0.0,
            "mistakes_count":             0,
            "drills_count":               0,
            "hidden_future_data":         True,
            "latest_replay_training_at":  "",
            "read_only":                  True,
            "no_real_orders":             True,
            "production_blocked":         True,
        }
        try:
            from replay_training.replay_training_store import ReplayTrainingStore
            store  = ReplayTrainingStore()
            result = store.load_latest_summary()
            if result.get("ok"):
                s = result.get("summary", {})
                snap["latest_session_id"]         = s.get("latest_session_id", "")
                snap["latest_symbol"]             = s.get("latest_symbol", "")
                snap["latest_score"]              = float(s.get("latest_score", 0.0) or 0.0)
                snap["mistakes_count"]            = int(s.get("mistakes_count", 0) or 0)
                snap["drills_count"]              = int(s.get("drills_count", 0) or 0)
                snap["hidden_future_data"]        = True
                snap["latest_replay_training_at"] = s.get("latest_replay_training_at", "")
                snap["summary"]                   = s
            else:
                snap["warnings"].append(
                    "No replay training summary found — run: python main.py replay-training --symbol 2454"
                )
        except Exception as exc:
            logger.warning("build_replay_training_snapshot: %s", exc)
            snap["warnings"].append(f"snapshot error: {exc}")
        return snap

    def build_stable_release_snapshot(self) -> dict:
        """Snapshot type: stable_release. Captures v0.6.0 capability and checklist summary.

        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        snap = _empty_snapshot("stable_release")
        snap.update({
            "version":             "v0.6.0",
            "capabilities":        0,
            "checklist_status":    "UNKNOWN",
            "safety_status":       "BLOCKED — Research Only",
            "report_path":         "",
            "manifest_path":       "",
            "latest_stable_release_at": "",
            "no_real_orders":      True,
            "production_blocked":  True,
        })
        try:
            from stable_release.capability_matrix import StableCapabilityMatrix
            matrix = StableCapabilityMatrix()
            matrix.build()
            caps = matrix.list_capabilities()
            by_status: dict = {}
            for c in caps:
                by_status[c.status] = by_status.get(c.status, 0) + 1
            snap["capabilities"] = len(caps)
            snap["by_status"]    = by_status
            snap["stable_count"] = by_status.get("STABLE", 0)
            snap["summary"]      = {
                "total":             len(caps),
                "stable_count":      by_status.get("STABLE", 0),
                "usable_count":      by_status.get("USABLE", 0),
                "no_real_orders":    True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("build_stable_release_snapshot (capability): %s", exc)
            snap["warnings"].append(f"capability load error: {exc}")
        try:
            import glob
            import os
            report_dir = os.path.join(BASE_DIR, "reports")
            pattern = os.path.join(report_dir, "stable_release_v0.6.0_report_*.md")
            files = glob.glob(pattern)
            if files:
                snap["report_path"] = max(files, key=os.path.getmtime)
        except Exception as exc:
            logger.warning("build_stable_release_snapshot (report path): %s", exc)
        try:
            import glob
            import os
            manifest_dir = os.path.join(BASE_DIR, "data", "backtest_results", "stable_release")
            pattern = os.path.join(manifest_dir, "release_manifest_*.json")
            files = glob.glob(pattern)
            if files:
                snap["manifest_path"] = max(files, key=os.path.getmtime)
        except Exception as exc:
            logger.warning("build_stable_release_snapshot (manifest path): %s", exc)
        snap["latest_stable_release_at"] = _now_iso()
        snap["checklist_status"] = "See stable-v060-check CLI command"
        return snap
