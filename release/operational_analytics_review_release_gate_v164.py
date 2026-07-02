"""
release/operational_analytics_review_release_gate_v164.py — Release Gate v1.6.4
Operational Analytics & Review — 40/40 PASS required.

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict, Tuple

VERSION     = "1.6.4"
GATE_NAME   = "Operational Analytics & Review"
TOTAL_GATES = 40

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
PAPER_ONLY: bool = True

_KNOWN_NAMES = {
    "Research Foundation Stable Rollup",
    "TWSE Provider",
    "Strategy Robustness & Regime Validation",
    "TPEx Provider",
    "MOPS Provider",
    "data.gov.tw Provider",
    "Provider CLI Registration Hotfix",
    "Provider Health Consistency Hotfix",
    "FinMind Adapter Hardening",
    "Source Lineage & Rate Limit",
    "Provider Quality Gates",
    "Forum Intelligence & Market Sentiment",
    "Data Provider Stable Rollup",
    "Full-Suite Collection Integrity Hotfix",
    "Provider Integration Hardening",
    "Provider Integration Test Integrity Hotfix",
    "Provider Stable Rollup",
    "Portfolio Research Foundation",
    "Portfolio Research Foundation Integrity Hotfix",
    "Portfolio Research CLI Completeness Hotfix",
    "Position Sizing",
    "Correlation & Exposure",
    "Correlation & Exposure Integrity Hotfix",
    "Drawdown & Risk Controls",
    "Portfolio Walk-forward Backtest",
    "Portfolio Stable Rollup",
    "Portfolio Stable Rollup Integrity Hotfix",
    "Portfolio Stable Rollup Release Gate Hotfix",
    "Live Paper Trading Foundation",
    "Market Data Session Adapter",
    "Market Data Session Warning Hygiene Hotfix",
    "Paper Strategy Orchestration",
    "Paper Strategy Orchestration Integrity Hotfix",
    "Session Operations & Observability",
    "Session Operations Integrity Hotfix",
    "CLI Registration Health Integrity Hotfix",
    "CLI Handler Resolution Integrity Hotfix",
    "Operational Analytics & Review",
    "Failure Injection & Recovery Validation",
    "Multi-session Coordination",
            "Fixture Governance & Safety Marker Hotfix",
    "Replay Session Lineage Handler Integrity Hotfix",
    "Paper Performance Attribution",
}


class OperationalAnalyticsReviewReleaseGateV164:
    """40-check release gate for v1.6.4 Operational Analytics & Review."""

    def run(self) -> Dict[str, Any]:
        checks: Dict[str, Tuple[str, str]] = {}
        blocked_checks = []

        def _check(name: str, fn, safety: bool = False):
            try:
                ok, msg = fn()
                status = "PASS" if ok else "FAIL"
            except Exception as exc:
                ok, msg, status = False, str(exc), "FAIL"
            checks[name] = (status, msg)
            if not ok and safety:
                blocked_checks.append(name)

        # 1. Version
        _check("VERSION",                      self._version_check)
        # 2. Release name
        _check("RELEASE_NAME",                 self._release_name_check)
        # 3. Base release
        _check("BASE_RELEASE",                 self._base_release_check)
        # 4. Analytics modules
        _check("ANALYTICS_MODULES",            self._analytics_modules_check)
        # 5. Session summary
        _check("SESSION_SUMMARY",              self._session_summary_check)
        # 6. Operational metrics
        _check("OPERATIONAL_METRICS",          self._operational_metrics_check)
        # 7. Performance metrics
        _check("PERFORMANCE_METRICS",          self._performance_metrics_check)
        # 8. Attribution reconcile
        _check("ATTRIBUTION_RECONCILE",        self._attribution_reconcile_check)
        # 9. Signal analysis
        _check("SIGNAL_ANALYSIS",              self._signal_analysis_check)
        # 10. Execution analysis
        _check("EXECUTION_ANALYSIS",           self._execution_analysis_check)
        # 11. Incident analysis
        _check("INCIDENT_ANALYSIS",            self._incident_analysis_check)
        # 12. Recovery analysis
        _check("RECOVERY_ANALYSIS",            self._recovery_analysis_check)
        # 13. Anomaly detection
        _check("ANOMALY_DETECTION",            self._anomaly_detection_check)
        # 14. Scorecard
        _check("SCORECARD",                    self._scorecard_check)
        # 15. Review workflow
        _check("REVIEW_WORKFLOW",              self._review_workflow_check)
        # 16. RCA
        _check("ROOT_CAUSE_ANALYSIS",          self._rca_check)
        # 17. Mistake taxonomy
        _check("MISTAKE_TAXONOMY",             self._mistake_taxonomy_check)
        # 18. Lessons
        _check("LESSON_REGISTRY",              self._lesson_registry_check)
        # 19. Action items
        _check("ACTION_ITEMS",                 self._action_items_check)
        # 20. Snapshot
        _check("SNAPSHOT",                     self._snapshot_check)
        # 21. Replay
        _check("REPLAY",                       self._replay_check)
        # 22. Lineage
        _check("LINEAGE",                      self._lineage_check)
        # 23. Reproducibility
        _check("REPRODUCIBILITY",              self._reproducibility_check)
        # 24. Store
        _check("STORE",                        self._store_check)
        # 25. Query
        _check("QUERY",                        self._query_check)
        # 26. Report
        _check("REPORT",                       self._report_check)
        # 27. CLI registration
        _check("CLI_REGISTRATION",             self._cli_registration_check)
        # 28. Runtime dispatch
        _check("RUNTIME_DISPATCH",             self._runtime_dispatch_check)
        # 29. GUI headless
        _check("GUI_HEADLESS",                 self._gui_headless_check)
        # 30. Fixtures
        _check("FIXTURES",                     self._fixtures_check)
        # 31. PIT safety
        _check("PIT_SAFETY",                   self._pit_safety_check)
        # 32. No leakage
        _check("NO_LEAKAGE",                   self._no_leakage_check)
        # 33. No broker (safety)
        _check("NO_BROKER",                    self._no_broker_check, safety=True)
        # 34. No real account (safety)
        _check("NO_REAL_ACCOUNT",              self._no_real_account_check, safety=True)
        # 35. No real orders (safety)
        _check("NO_REAL_ORDERS",               self._no_real_orders_check, safety=True)
        # 36. No production writes (safety)
        _check("NO_PRODUCTION_WRITES",         self._no_production_writes_check, safety=True)
        # 37. No auto strategy changes (safety)
        _check("NO_AUTO_STRATEGY_CHANGES",     self._no_auto_strategy_check, safety=True)
        # 38. No auto risk changes (safety)
        _check("NO_AUTO_RISK_CHANGES",         self._no_auto_risk_check, safety=True)
        # 39. All previous gates
        _check("ALL_PREVIOUS_GATES",           self._previous_gates_check)
        # 40. Full regression (health check)
        _check("FULL_REGRESSION",              self._full_regression_check)

        passed   = sum(1 for v in checks.values() if v[0] == "PASS")
        failed   = sum(1 for v in checks.values() if v[0] != "PASS")
        all_pass = failed == 0 and not blocked_checks
        status   = "PASS" if all_pass else ("BLOCKED" if blocked_checks else "FAIL")

        return {
            "gate_version":   VERSION,
            "gate_name":      GATE_NAME,
            "total":          TOTAL_GATES,
            "passed":         passed,
            "failed":         failed,
            "all_pass":       all_pass,
            "blocked":        blocked_checks,
            "checks":         checks,
            "paper_only":     True,
            "research_only":  True,
            "no_real_orders": True,
            "status":         status,
        }

    # ── Check implementations ────────────────────────────────────────────
    def _version_check(self):
        from release.version_info import VERSION
        ok = VERSION >= "1.6.4"
        return ok, f"VERSION={VERSION}"

    def _release_name_check(self):
        from release.version_info import RELEASE_NAME
        ok = RELEASE_NAME in _KNOWN_NAMES
        return ok, f"RELEASE_NAME={RELEASE_NAME}"

    def _base_release_check(self):
        from release.version_info import BASE_RELEASE
        ok = any(v in BASE_RELEASE for v in ("1.6.3.3", "1.6.4", "1.6.5", "1.6.6"))
        return ok, f"BASE_RELEASE={BASE_RELEASE}"

    def _analytics_modules_check(self):
        import paper_trading.analytics
        from paper_trading.analytics.enums_v164 import ReviewStatus
        from paper_trading.analytics.models_v164 import OperationalAnalyticsResult
        from paper_trading.analytics.health_v164 import OperationalAnalyticsReviewHealthCheck
        return True, "all analytics modules importable"

    def _session_summary_check(self):
        from paper_trading.analytics.session_summary_v164 import SessionSummaryBuilder
        from datetime import datetime, timezone
        b = SessionSummaryBuilder()
        s = b.build("s1", datetime.now(tz=timezone.utc), {})
        assert s.paper_only is True
        return True, "session summary ok"

    def _operational_metrics_check(self):
        from paper_trading.analytics.operational_metrics_v164 import OperationalMetricsComputer
        c = OperationalMetricsComputer()
        m = c.compute_latency_metrics([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        assert "latency_p50_ms" in m
        return True, "operational metrics ok"

    def _performance_metrics_check(self):
        from paper_trading.analytics.performance_metrics_v164 import PaperPerformanceMetricsComputer
        from decimal import Decimal
        c = PaperPerformanceMetricsComputer()
        m = c.compute("s1", {"gross_pnl": "100", "net_pnl": "85", "max_drawdown": "-10"})
        assert m.paper_only
        return True, "performance metrics ok"

    def _attribution_reconcile_check(self):
        from paper_trading.analytics.validation_v164 import validate_attribution_reconciliation
        from decimal import Decimal
        result = validate_attribution_reconciliation(
            Decimal("100"), [Decimal("60"), Decimal("40")], label="test"
        )
        assert result["valid"] is True
        return True, "attribution reconciliation ok"

    def _signal_analysis_check(self):
        from paper_trading.analytics.signal_quality_v164 import SignalQualityAnalyzer
        a = SignalQualityAnalyzer()
        m = a.analyze("s1", {"signal_count": 50, "accepted_count": 40})
        assert m.auto_strategy_change is False
        return True, "signal analysis ok"

    def _execution_analysis_check(self):
        from paper_trading.analytics.execution_quality_v164 import ExecutionQualityAnalyzer
        a = ExecutionQualityAnalyzer()
        m = a.analyze("s1", {"simulated_orders": 20, "simulated_fills": 18})
        assert not m.broker_execution
        return True, "execution analysis ok"

    def _incident_analysis_check(self):
        from paper_trading.analytics.incident_impact_v164 import IncidentImpactAnalyzer
        a = IncidentImpactAnalyzer()
        r = a.analyze("s1", [{"incident_id": "i1", "estimated_pnl_impact": "5", "duration_seconds": "30"}])
        assert r.records[0].causal_label == "ASSOCIATED"
        return True, "incident analysis ok"

    def _recovery_analysis_check(self):
        from paper_trading.analytics.recovery_impact_v164 import RecoveryImpactAnalyzer
        a = RecoveryImpactAnalyzer()
        r = a.analyze("s1", [{"success": True, "duration_seconds": 60}])
        assert not r.auto_resume
        return True, "recovery analysis ok"

    def _anomaly_detection_check(self):
        from paper_trading.analytics.anomaly_detection_v164 import AnomalyDetector
        from decimal import Decimal
        d = AnomalyDetector()
        a = d.detect_threshold("test_metric", Decimal("0.5"), Decimal("0.2"))
        assert a is not None
        assert a.rule_version == "1.6.4"
        return True, "anomaly detection ok"

    def _scorecard_check(self):
        from paper_trading.analytics.review_scorecard_v164 import ReviewScorecardBuilder
        from paper_trading.analytics.enums_v164 import ScorecardDimension, MetricQuality
        from decimal import Decimal
        b = ReviewScorecardBuilder()
        scores = {d: Decimal("75") for d in ScorecardDimension}
        qualities = {d: MetricQuality.VALID for d in ScorecardDimension}
        sc = b.build("s1", scores, qualities)
        assert sc.overall_score > Decimal("0")
        return True, f"scorecard overall={sc.overall_score}"

    def _review_workflow_check(self):
        from paper_trading.analytics.review_workflow_v164 import ReviewWorkflow
        from paper_trading.analytics.enums_v164 import ReviewStatus, ReviewScope
        wf = ReviewWorkflow()
        r = wf.create("s1", ReviewScope.COMPOSITE, "analyst")
        assert r.status == ReviewStatus.PENDING
        wf.add_evidence(r.review_id, "ev-001")
        wf.transition(r.review_id, ReviewStatus.IN_PROGRESS, "analyst", "Starting review")
        assert r.status == ReviewStatus.IN_PROGRESS
        return True, "review workflow ok"

    def _rca_check(self):
        from paper_trading.analytics.root_cause_analysis_v164 import RootCauseAnalyzer
        a = RootCauseAnalyzer()
        r = a.analyze("test problem", [{"ref": "ev-001"}, {"ref": "ev-002"}], ["data_quality"])
        assert r.rca_id
        return True, f"RCA label={r.causal_label}"

    def _mistake_taxonomy_check(self):
        from paper_trading.analytics.mistake_taxonomy_v164 import MistakeTaxonomyClassifier
        c = MistakeTaxonomyClassifier()
        m = c.classify({"stale_ratio": "0.15"})
        assert len(m) >= 1
        return True, f"taxonomy {len(m)} mistakes"

    def _lesson_registry_check(self):
        from paper_trading.analytics.lesson_registry_v164 import LessonRegistry
        reg = LessonRegistry()
        l = reg.register("lesson1", "DATA", "Check stale data")
        accepted = reg.accept(l.lesson_id)
        from paper_trading.analytics.enums_v164 import LessonStatus
        assert accepted.status == LessonStatus.ACCEPTED
        return True, "lesson registry ok"

    def _action_items_check(self):
        from paper_trading.analytics.action_item_v164 import ActionItemManager
        from paper_trading.analytics.enums_v164 import ActionItemStatus
        mgr = ActionItemManager()
        item = mgr.create("r1", "DATA", "Fix it", "Description", "owner", "HIGH")
        mgr.transition(item.action_item_id, ActionItemStatus.ACCEPTED, "manager", "Accepted")
        assert item.status == ActionItemStatus.ACCEPTED
        assert len(item.history) == 1
        return True, "action items ok"

    def _snapshot_check(self):
        from paper_trading.analytics.snapshot_v164 import AnalyticsSnapshotManager
        from datetime import datetime, timezone
        mgr = AnalyticsSnapshotManager()
        s = mgr.create_snapshot("a1", "s1", {"x": 1}, {"y": 2}, datetime.now(tz=timezone.utc))
        assert s.reproducibility_hash
        return True, "snapshot ok"

    def _replay_check(self):
        from paper_trading.analytics.replay_v164 import AnalyticsReplayer
        from paper_trading.analytics.snapshot_v164 import AnalyticsSnapshotManager
        from paper_trading.analytics.enums_v164 import ReproducibilityStatus
        from datetime import datetime, timezone
        mgr = AnalyticsSnapshotManager()
        snap = mgr.create_snapshot("a1", "s1", {"x": 1}, {"y": 2}, datetime.now(tz=timezone.utc))
        r = AnalyticsReplayer()
        res = r.replay(snap, {"x": 1}, {"y": 2})
        assert res.status == ReproducibilityStatus.MATCH
        return True, "replay match ok"

    def _lineage_check(self):
        from paper_trading.analytics.lineage_v164 import AnalyticsLineageTracker
        from datetime import datetime, timezone
        t = AnalyticsLineageTracker()
        l = t.create_lineage("a1", ["s1"], as_of=datetime.now(tz=timezone.utc))
        assert not t.has_gaps(l)
        return True, "lineage ok"

    def _reproducibility_check(self):
        from paper_trading.analytics.reproducibility_v164 import ReproducibilityChecker
        from paper_trading.analytics.enums_v164 import ReproducibilityStatus
        c = ReproducibilityChecker()
        r1 = c.record("a1", {"x": 1}, {"y": 2})
        r2 = c.record("a1", {"x": 1}, {"y": 2})
        assert c.verify(r1, r2) == ReproducibilityStatus.MATCH
        return True, "reproducibility ok"

    def _store_check(self):
        from paper_trading.analytics.store_v164 import OperationalAnalyticsStore
        s = OperationalAnalyticsStore()
        assert s.list_analytics() == []
        return True, "store ok"

    def _query_check(self):
        from paper_trading.analytics.query_v164 import AnalyticsQueryService
        q = AnalyticsQueryService()
        assert q.summary()["paper_only"] is True
        return True, "query ok"

    def _report_check(self):
        from paper_trading.analytics.report_v164 import AnalyticsReportGenerator, REPORT_SECTIONS
        assert len(REPORT_SECTIONS) >= 16
        assert "Safety Disclaimer" in REPORT_SECTIONS
        return True, f"report {len(REPORT_SECTIONS)} sections"

    def _cli_registration_check(self):
        from cli.command_registry import PROVIDER_COMMANDS
        ops_cmds = [s for s in PROVIDER_COMMANDS if s.name.startswith("ops-")]
        assert len(ops_cmds) >= 30, f"Expected >=30 ops- commands, got {len(ops_cmds)}"
        return True, f"{len(ops_cmds)} ops- commands registered"

    def _runtime_dispatch_check(self):
        import importlib
        main = importlib.import_module("main")
        ops_handlers = [
            "cmd_ops_analytics_run", "cmd_ops_analytics_show", "cmd_ops_review_create",
            "cmd_ops_review_show", "cmd_ops_analytics_health", "cmd_ops_analytics_release_gate",
        ]
        unresolved = [h for h in ops_handlers if not callable(getattr(main, h, None))]
        assert not unresolved, f"Unresolved: {unresolved}"
        return True, "runtime dispatch ok"

    def _gui_headless_check(self):
        from gui.operational_analytics_review_panel import OperationalAnalyticsReviewPanel
        p = OperationalAnalyticsReviewPanel()
        assert p.research_only is True
        assert p.no_broker is True
        return True, "GUI headless ok"

    def _fixtures_check(self):
        import os
        fixture_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "tests", "fixtures", "operational_analytics"
        )
        if not os.path.isdir(fixture_dir):
            return False, "fixtures directory missing"
        files = [f for f in os.listdir(fixture_dir) if f.endswith(".json")]
        assert len(files) >= 50, f"Expected >=50 fixtures, got {len(files)}"
        return True, f"{len(files)} fixtures"

    def _pit_safety_check(self):
        from paper_trading.analytics.validation_v164 import PITViolation, require_pit
        from datetime import datetime, timezone, timedelta
        now = datetime.now(tz=timezone.utc)
        try:
            require_pit(now + timedelta(hours=1), now, "future_field")
            return False, "PIT check did not raise"
        except PITViolation:
            return True, "PIT violation raised correctly"

    def _no_leakage_check(self):
        from paper_trading.analytics.signal_quality_v164 import POST_EVENT_ANALYSIS_ONLY
        assert POST_EVENT_ANALYSIS_ONLY is True
        return True, "no leakage — post-event analysis labelled"

    def _no_broker_check(self):
        assert BROKER_EXECUTION_ENABLED is False
        import paper_trading.analytics
        assert paper_trading.analytics.NO_BROKER is True
        return True, "NO_BROKER confirmed"

    def _no_real_account_check(self):
        from paper_trading.analytics.execution_quality_v164 import BROKER_EXECUTION_CAPABILITY_INCLUDED
        assert BROKER_EXECUTION_CAPABILITY_INCLUDED is False
        return True, "no real account"

    def _no_real_orders_check(self):
        assert NO_REAL_ORDERS is True
        import paper_trading.analytics
        assert paper_trading.analytics.NO_REAL_ORDERS is True
        return True, "NO_REAL_ORDERS confirmed"

    def _no_production_writes_check(self):
        from paper_trading.analytics.store_v164 import PRODUCTION_DB_ENABLED, PORTFOLIO_LEDGER_WRITE_ENABLED
        assert PRODUCTION_DB_ENABLED is False
        assert PORTFOLIO_LEDGER_WRITE_ENABLED is False
        return True, "no production writes"

    def _no_auto_strategy_check(self):
        import paper_trading.analytics
        assert paper_trading.analytics.AUTO_STRATEGY_CHANGE_ENABLED is False
        from paper_trading.analytics.signal_quality_v164 import AUTO_STRATEGY_CHANGE_ENABLED
        assert AUTO_STRATEGY_CHANGE_ENABLED is False
        return True, "no auto strategy changes"

    def _no_auto_risk_check(self):
        import paper_trading.analytics
        assert paper_trading.analytics.AUTO_RISK_LIMIT_CHANGE_ENABLED is False
        return True, "no auto risk changes"

    def _previous_gates_check(self):
        from release.session_operations_observability_release_gate_v163 import (
            SessionOperationsObservabilityReleaseGate
        )
        result = SessionOperationsObservabilityReleaseGate().run()
        ok = result["all_pass"]
        return ok, f"Session Operations Gate: {result['passed']}/{result['total']}"

    def _full_regression_check(self):
        from paper_trading.analytics.health_v164 import OperationalAnalyticsReviewHealthCheck
        result = OperationalAnalyticsReviewHealthCheck().run()
        ok = result["all_pass"]
        return ok, f"Health: {result['passed']}/{result['total']}"
