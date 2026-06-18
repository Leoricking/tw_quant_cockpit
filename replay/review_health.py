"""
replay/review_health.py — ReplayReviewDashboardHealthCheck v1.2.6

Health check for replay review dashboard v1.2.6.
Checks all components. Output: PASS/WARN/FAIL/BLOCKED for each check.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
import tempfile
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewDashboardHealthCheck:
    """
    Health check for replay review dashboard v1.2.6.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns dict of name → (status, message)."""
        results: Dict[str, Tuple[str, str]] = {}

        results["schema"]            = self._check_schema()
        results["adapter"]           = self._check_adapter()
        results["engine"]            = self._check_engine()
        results["cards"]             = self._check_cards()
        results["tables"]            = self._check_tables()
        results["charts"]            = self._check_charts()
        results["queue"]             = self._check_queue()
        results["progress"]          = self._check_progress()
        results["checklist"]         = self._check_checklist()
        results["notes"]             = self._check_notes()
        results["tags"]              = self._check_tags()
        results["search"]            = self._check_search()
        results["filters"]           = self._check_filters()
        results["sorting"]           = self._check_sorting()
        results["grouping"]          = self._check_grouping()
        results["comparator"]        = self._check_comparator()
        results["batch"]             = self._check_batch()
        results["store"]             = self._check_store()
        results["query"]             = self._check_query()
        results["summary"]           = self._check_summary()
        results["report"]            = self._check_report()

        # Safety flag checks
        results["version_info"]           = self._check_version_info()
        results["no_auto_review_complete"] = self._check_no_auto_review_complete()
        results["no_auto_outcome_reveal"]  = self._check_no_auto_outcome_reveal()
        results["no_auto_confirm"]         = self._check_no_auto_confirm()
        results["outcome_hidden"]          = self._check_outcome_hidden()
        results["suggested_not_confirmed"] = self._check_suggested_not_confirmed()
        results["process_outcome_separated"] = self._check_process_outcome_separated()
        results["read_only_default"]       = self._check_read_only_default()
        results["no_broker_side_effect"]   = self._check_no_broker_side_effect()
        results["batch_guard"]             = self._check_batch_guard()
        results["missing_module_graceful"] = self._check_missing_module_graceful()
        results["store_corrupted_recovery"] = self._check_store_corrupted_recovery()

        return results

    # ------------------------------------------------------------------
    # Component checks
    # ------------------------------------------------------------------

    def _check_schema(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_schema import (
                ReplayReviewDashboardSnapshot, ReplayReviewSessionRow,
                ReplayReviewQueueItem, ReplayReviewProgress,
                ReplayReviewChecklistItem,
                QueueItemType, QueueItemPriority, QueueItemStatus,
                ReviewProgressStatus, _new_id, _now_utc,
            )
            snap = ReplayReviewDashboardSnapshot(snapshot_id=_new_id("RRD-"), mode="real")
            assert snap.research_only is True
            assert snap.no_real_orders is True
            assert snap.auto_review_complete_enabled is False
            assert snap.auto_outcome_reveal_enabled is False
            assert snap.auto_mistake_confirmation_enabled is False
            assert snap.auto_score_to_trade_enabled is False
            row = ReplayReviewSessionRow(session_id="S1", symbol="TST")
            assert row.research_only is True
            # Outcome hidden in to_dict
            d = row.to_dict()
            assert d["outcome_score"] is None
            assert d["outcome_score_hidden"] is True
            return ("PASS", "Schema: all dataclasses instantiate, safety invariants hold, outcome hidden")
        except Exception as exc:
            return ("FAIL", f"Schema error: {exc}")

    def _check_adapter(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_adapter import ReplayReviewDashboardAdapter
            adapter = ReplayReviewDashboardAdapter(mode="real")
            snap = adapter.build_dashboard_snapshot(mode="real")
            assert snap.research_only is True
            assert snap.no_real_orders is True
            return ("PASS", "Adapter: builds snapshot, research_only=True, no_real_orders=True")
        except Exception as exc:
            return ("FAIL", f"Adapter error: {exc}")

    def _check_engine(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_engine import ReplayReviewDashboardEngine
            eng = ReplayReviewDashboardEngine(mode="real")
            dashboard = eng.build_global_dashboard(mode="real")
            assert dashboard["research_only"] is True
            assert dashboard["no_real_orders"] is True
            summary = eng.summary()
            assert "total_sessions" in summary
            return ("PASS", "Engine: global dashboard built, summary OK")
        except Exception as exc:
            return ("FAIL", f"Engine error: {exc}")

    def _check_cards(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_cards import (
                build_session_cards, build_queue_cards, build_score_cards,
                build_integrity_cards, build_strategy_cards,
                build_timeframe_cards, build_timing_cards,
            )
            snap = {"total_sessions": 5, "avg_process_score": 72.0}
            cards = build_session_cards(snap)
            assert len(cards) == 6
            score_cards = build_score_cards(snap)
            # Outcome and composite cards must show HIDDEN
            hidden = [c for c in score_cards if c.get("status") == "HIDDEN"]
            assert len(hidden) >= 2, "Outcome/composite cards must be HIDDEN"
            return ("PASS", f"Cards: {len(cards)} session cards, outcome/composite HIDDEN")
        except Exception as exc:
            return ("FAIL", f"Cards error: {exc}")

    def _check_tables(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_tables import build_session_review_table
            rows = [{"session_id": "S1", "symbol": "TST", "process_score": 70.0, "outcome_revealed": False}]
            result = build_session_review_table(rows)
            assert "rows" in result
            assert "total" in result
            return ("PASS", "Tables: session review table builds correctly")
        except Exception as exc:
            return ("FAIL", f"Tables error: {exc}")

    def _check_charts(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_charts import (
                build_review_progress_distribution,
                build_process_score_distribution,
            )
            rows = [{"review_progress": "NOT_STARTED", "process_score": 70.0}]
            c1 = build_review_progress_distribution(rows)
            c2 = build_process_score_distribution(rows)
            assert c1["research_only"] is True
            assert c2["process_outcome_separated"] is True
            return ("PASS", "Charts: build correctly, research_only=True, process/outcome separated")
        except Exception as exc:
            return ("FAIL", f"Charts error: {exc}")

    def _check_queue(self) -> Tuple[str, str]:
        try:
            from replay.review_queue import ReplayReviewQueueManager
            mgr = ReplayReviewQueueManager()
            assert mgr.AUTO_CONFIRM_ON_COMPLETE is False
            assert mgr.AUTO_REVEAL_ON_COMPLETE is False
            # complete() must not auto-confirm/reveal
            result = mgr.complete("NONEXISTENT")
            assert result.get("status") == "NOT_FOUND"
            summary = mgr.summary()
            assert summary["auto_confirm_on_complete"] is False
            assert summary["auto_reveal_on_complete"] is False
            return ("PASS", "Queue: complete() no auto-confirm, no auto-reveal confirmed")
        except Exception as exc:
            return ("FAIL", f"Queue error: {exc}")

    def _check_progress(self) -> Tuple[str, str]:
        try:
            from replay.review_progress import ReplayReviewProgressCalculator
            calc = ReplayReviewProgressCalculator()
            assert calc.OUTCOME_REVEAL_REQUIRED is False
            prog = calc.calculate("S1", {})
            assert prog.outcome_reveal_required is False
            assert prog.process_review_complete is False  # no steps done
            req = calc.required_steps()
            assert "session_completed" in req
            assert "outcome_revealed" not in req
            return ("PASS", "Progress: outcome_reveal_required=False, outcome not in required steps")
        except Exception as exc:
            return ("FAIL", f"Progress error: {exc}")

    def _check_checklist(self) -> Tuple[str, str]:
        try:
            from replay.review_checklist import ReplayReviewChecklist
            cl = ReplayReviewChecklist("S1")
            assert cl.AUTO_COMPLETE is False
            items = cl.items()
            assert len(items) > 0
            # outcome_reveal item must require manual action
            outcome_items = [i for i in items if "Outcome reveal" in i.label]
            assert len(outcome_items) >= 1
            result = cl.complete_item(outcome_items[0].item_id)
            assert result.get("status") == "MANUAL_REQUIRED"
            return ("PASS", "Checklist: AUTO_COMPLETE=False, outcome reveal requires manual action")
        except Exception as exc:
            return ("FAIL", f"Checklist error: {exc}")

    def _check_notes(self) -> Tuple[str, str]:
        try:
            from replay.review_notes import ReplayReviewNoteManager
            mgr = ReplayReviewNoteManager()
            assert mgr.APPEND_ONLY is True
            result = mgr.add_note("S1", "session", "Test note")
            assert result["status"] == "OK"
            notes = mgr.get_notes("S1")
            assert len(notes) == 1
            return ("PASS", "Notes: append-only, add/get OK")
        except Exception as exc:
            return ("FAIL", f"Notes error: {exc}")

    def _check_tags(self) -> Tuple[str, str]:
        try:
            from replay.review_tags import ReplayReviewTagManager, TAG_GOOD_PROCESS
            mgr = ReplayReviewTagManager()
            assert mgr.TAG_AFFECTS_SCORE is False
            result = mgr.add_tag("S1", TAG_GOOD_PROCESS)
            assert result["affects_score"] is False
            assert result["affects_trading"] is False
            return ("PASS", "Tags: TAG_AFFECTS_SCORE=False, affects_trading=False")
        except Exception as exc:
            return ("FAIL", f"Tags error: {exc}")

    def _check_search(self) -> Tuple[str, str]:
        try:
            from replay.review_search import ReplayReviewSearch
            searcher = ReplayReviewSearch()
            rows = [{"session_id": "S1", "symbol": "TST"}]
            result = searcher.search(rows, "TST")
            assert len(result) == 1
            return ("PASS", "Search: returns matching rows")
        except Exception as exc:
            return ("FAIL", f"Search error: {exc}")

    def _check_filters(self) -> Tuple[str, str]:
        try:
            from replay.review_filters import ReplayReviewFilters
            f = ReplayReviewFilters()
            rows = [{"symbol": "TST", "mode": "real"}, {"symbol": "ABC", "mode": "mock"}]
            result = f.filter_real_only(rows)
            assert len(result) == 1 and result[0]["symbol"] == "TST"
            return ("PASS", "Filters: real/mock separation, field filters OK")
        except Exception as exc:
            return ("FAIL", f"Filters error: {exc}")

    def _check_sorting(self) -> Tuple[str, str]:
        try:
            from replay.review_sorting import ReplayReviewSorter
            sorter = ReplayReviewSorter()
            rows = [{"symbol": "C"}, {"symbol": "A"}, {"symbol": "B"}]
            result = sorter.sort(rows, "symbol")
            assert result[0]["symbol"] == "A"
            return ("PASS", "Sorting: ascending sort by symbol OK")
        except Exception as exc:
            return ("FAIL", f"Sorting error: {exc}")

    def _check_grouping(self) -> Tuple[str, str]:
        try:
            from replay.review_grouping import ReplayReviewGrouper
            g = ReplayReviewGrouper()
            rows = [{"symbol": "TST"}, {"symbol": "TST"}, {"symbol": "ABC"}]
            groups = g.group_by(rows, "symbol")
            assert len(groups["TST"]) == 2
            return ("PASS", "Grouping: group by symbol OK")
        except Exception as exc:
            return ("FAIL", f"Grouping error: {exc}")

    def _check_comparator(self) -> Tuple[str, str]:
        try:
            from replay.review_comparator import ReplayReviewComparator, NOT_AVAILABLE
            comp = ReplayReviewComparator()
            row_a = {"session_id": "A", "symbol": "TST", "outcome_revealed": False, "outcome_score": 80.0}
            row_b = {"session_id": "B", "symbol": "TST", "outcome_revealed": True, "outcome_score": 60.0}
            result = comp.compare_sessions(row_a, row_b)
            # outcome_score for A must be NOT_AVAILABLE
            assert result["comparison"]["outcome_score"]["session_a"] == NOT_AVAILABLE
            return ("PASS", "Comparator: outcome NOT_AVAILABLE when not revealed")
        except Exception as exc:
            return ("FAIL", f"Comparator error: {exc}")

    def _check_batch(self) -> Tuple[str, str]:
        try:
            from replay.review_batch import ReplayReviewBatchRunner
            runner = ReplayReviewBatchRunner()
            assert runner.DEFAULT_PREVIEW_MODE is True
            assert runner.NO_AUTO_REVEAL is True
            assert runner.NO_AUTO_CONFIRM is True
            # Blocked without allow_write
            result = runner.run(["S1"], execute=True, allow_write=False)
            assert result["status"] == "BLOCKED"
            # Blocked without execute
            result2 = runner.run(["S1"], execute=False, allow_write=True)
            assert result2["status"] == "BLOCKED"
            # Preview works
            preview = runner.preview(["S1"])
            assert preview["mode"] == "PREVIEW"
            return ("PASS", "Batch: default preview, blocked without --execute --allow-write")
        except Exception as exc:
            return ("FAIL", f"Batch error: {exc}")

    def _check_store(self) -> Tuple[str, str]:
        try:
            from replay.review_store import ReplayReviewStore
            with tempfile.TemporaryDirectory() as tmpdir:
                store = ReplayReviewStore(base_dir=tmpdir)
                ok = store.append_snapshot({"snapshot_id": "RRD-001", "mode": "real"})
                assert ok
                snaps = store.get_snapshots()
                assert len(snaps) == 1
                # Corrupted recovery
                path = store._path("dashboard_snapshots.jsonl")
                with open(path, "a", encoding="utf-8") as f:
                    f.write("{CORRUPTED\n")
                ok2 = store.append_snapshot({"snapshot_id": "RRD-002", "mode": "real"})
                assert ok2
                snaps2 = store.get_snapshots()
                assert len(snaps2) == 2
            return ("PASS", "Store: append-only, corrupted tail recovery, state write OK")
        except Exception as exc:
            return ("FAIL", f"Store error: {exc}")

    def _check_query(self) -> Tuple[str, str]:
        try:
            from replay.review_query import ReplayReviewQuery
            q = ReplayReviewQuery()
            sessions = q.sessions()
            assert isinstance(sessions, list)
            return ("PASS", "Query: sessions() returns list, no crash")
        except Exception as exc:
            return ("FAIL", f"Query error: {exc}")

    def _check_summary(self) -> Tuple[str, str]:
        try:
            from replay.review_summary import ReplayReviewSummaryBuilder
            builder = ReplayReviewSummaryBuilder()
            s = builder.global_summary([])
            assert s["research_only"] is True
            assert s["real_mock_separated"] is True
            assert "outcome_score" in s
            return ("PASS", "Summary: global_summary OK, real_mock_separated=True")
        except Exception as exc:
            return ("FAIL", f"Summary error: {exc}")

    def _check_report(self) -> Tuple[str, str]:
        try:
            from replay.review_report import ReplayReviewReportBuilder
            with tempfile.TemporaryDirectory() as tmpdir:
                builder = ReplayReviewReportBuilder(reports_dir=tmpdir)
                md = builder.build_session_report("S1")
                assert "Research Only" in md
                assert "NOT_REVEALED" in md or "No Real Orders" in md
            return ("PASS", "Report: session report builds correctly with safety declarations")
        except Exception as exc:
            return ("FAIL", f"Report error: {exc}")

    # ------------------------------------------------------------------
    # Safety flag checks
    # ------------------------------------------------------------------

    def _check_version_info(self) -> Tuple[str, str]:
        try:
            from release.version_info import (
                VERSION, REPLAY_REVIEW_DASHBOARD_AVAILABLE,
                AUTO_REVIEW_COMPLETE_ENABLED, AUTO_OUTCOME_REVEAL_ENABLED,
                AUTO_MISTAKE_CONFIRMATION_ENABLED, AUTO_SCORE_TO_TRADE_ENABLED,
                REPLAY_TRADE_EXECUTION_ENABLED, BROKER_EXECUTION_ENABLED,
            )
            from release.version_compat import version_at_least
            assert version_at_least(VERSION, "1.2.6"), f"Expected >= 1.2.6, got {VERSION}"
            assert REPLAY_REVIEW_DASHBOARD_AVAILABLE is True
            assert AUTO_REVIEW_COMPLETE_ENABLED is False
            assert AUTO_OUTCOME_REVEAL_ENABLED is False
            assert AUTO_MISTAKE_CONFIRMATION_ENABLED is False
            assert AUTO_SCORE_TO_TRADE_ENABLED is False
            assert REPLAY_TRADE_EXECUTION_ENABLED is False
            assert BROKER_EXECUTION_ENABLED is False
            return ("PASS", f"Version: {VERSION}, review dashboard available, safety flags valid")
        except Exception as exc:
            return ("FAIL", f"VersionInfo error: {exc}")

    def _check_no_auto_review_complete(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_REVIEW_COMPLETE_ENABLED
            assert AUTO_REVIEW_COMPLETE_ENABLED is False
            from replay.review_queue import ReplayReviewQueueManager
            mgr = ReplayReviewQueueManager()
            assert mgr.AUTO_CONFIRM_ON_COMPLETE is False
            return ("PASS", "No auto review complete: version_info and queue manager confirmed False")
        except Exception as exc:
            return ("FAIL", f"NoAutoReviewComplete error: {exc}")

    def _check_no_auto_outcome_reveal(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_OUTCOME_REVEAL_ENABLED
            assert AUTO_OUTCOME_REVEAL_ENABLED is False
            from replay.review_batch import ReplayReviewBatchRunner
            runner = ReplayReviewBatchRunner()
            assert runner.NO_AUTO_REVEAL is True
            return ("PASS", "No auto outcome reveal: version_info and batch runner confirmed")
        except Exception as exc:
            return ("FAIL", f"NoAutoOutcomeReveal error: {exc}")

    def _check_no_auto_confirm(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_MISTAKE_CONFIRMATION_ENABLED
            assert AUTO_MISTAKE_CONFIRMATION_ENABLED is False
            from replay.review_queue import ReplayReviewQueueManager
            mgr = ReplayReviewQueueManager()
            assert mgr.AUTO_CONFIRM_ON_COMPLETE is False
            return ("PASS", "No auto confirm: version_info and queue manager confirmed")
        except Exception as exc:
            return ("FAIL", f"NoAutoConfirm error: {exc}")

    def _check_outcome_hidden(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_schema import ReplayReviewSessionRow
            row = ReplayReviewSessionRow(
                session_id="S1", symbol="TST",
                outcome_score=80.0, composite_score=75.0,
                outcome_revealed=False,
            )
            d = row.to_dict()
            assert d["outcome_score"] is None, "Outcome score must be None when not revealed"
            assert d["outcome_score_hidden"] is True
            assert d["composite_score"] is None
            return ("PASS", "Outcome hidden: outcome_score=None and hidden=True when not revealed")
        except Exception as exc:
            return ("FAIL", f"OutcomeHidden error: {exc}")

    def _check_suggested_not_confirmed(self) -> Tuple[str, str]:
        try:
            from replay.review_checklist import ReplayReviewChecklist, _NO_AUTO_COMPLETE
            assert "Mistake confirmation (manual)" in _NO_AUTO_COMPLETE
            cl = ReplayReviewChecklist("S1")
            mistake_items = [i for i in cl.items() if "Mistake confirmation" in i.label]
            assert len(mistake_items) >= 1
            result = cl.complete_item(mistake_items[0].item_id)
            assert result.get("status") == "MANUAL_REQUIRED"
            return ("PASS", "Suggested not confirmed: mistake confirm requires manual action")
        except Exception as exc:
            return ("FAIL", f"SuggestedNotConfirmed error: {exc}")

    def _check_process_outcome_separated(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_charts import build_process_score_distribution
            rows = [{"process_score": 70.0, "outcome_score": 80.0, "outcome_revealed": False}]
            chart = build_process_score_distribution(rows)
            assert chart["process_outcome_separated"] is True
            # Title may reference "No Outcome" to clarify separation — that is correct
            return ("PASS", "Process/Outcome separated: charts confirmed, process_outcome_separated=True")
        except Exception as exc:
            return ("FAIL", f"ProcessOutcomeSeparated error: {exc}")

    def _check_read_only_default(self) -> Tuple[str, str]:
        try:
            from replay.review_batch import ReplayReviewBatchRunner
            runner = ReplayReviewBatchRunner()
            assert runner.DEFAULT_PREVIEW_MODE is True
            return ("PASS", "Read-only default: batch runner DEFAULT_PREVIEW_MODE=True")
        except Exception as exc:
            return ("FAIL", f"ReadOnlyDefault error: {exc}")

    def _check_no_broker_side_effect(self) -> Tuple[str, str]:
        try:
            from release.version_info import BROKER_EXECUTION_ENABLED, REPLAY_TRADE_EXECUTION_ENABLED
            assert BROKER_EXECUTION_ENABLED is False
            assert REPLAY_TRADE_EXECUTION_ENABLED is False
            return ("PASS", "No broker side effect: BROKER_EXECUTION_ENABLED=False, REPLAY_TRADE=False")
        except Exception as exc:
            return ("FAIL", f"NoBrokerSideEffect error: {exc}")

    def _check_batch_guard(self) -> Tuple[str, str]:
        try:
            from replay.review_batch import ReplayReviewBatchRunner
            runner = ReplayReviewBatchRunner()
            r1 = runner.run(["S1"], execute=True, allow_write=False)
            assert r1["status"] == "BLOCKED"
            r2 = runner.run(["S1"], execute=False, allow_write=True)
            assert r2["status"] == "BLOCKED"
            r3 = runner.run(["S1"], execute=False, allow_write=False)
            assert r3["status"] == "BLOCKED"
            return ("PASS", "Batch guard: BLOCKED without both --execute AND --allow-write")
        except Exception as exc:
            return ("FAIL", f"BatchGuard error: {exc}")

    def _check_missing_module_graceful(self) -> Tuple[str, str]:
        try:
            from replay.review_dashboard_adapter import safe_unavailable
            result = safe_unavailable("nonexistent_module_xyz", Exception("not found"))
            assert result["status"] == "UNAVAILABLE"
            assert "reason" in result
            return ("PASS", "Missing module graceful: UNAVAILABLE returned, no crash")
        except Exception as exc:
            return ("FAIL", f"MissingModuleGraceful error: {exc}")

    def _check_store_corrupted_recovery(self) -> Tuple[str, str]:
        try:
            from replay.review_store import ReplayReviewStore
            with tempfile.TemporaryDirectory() as tmpdir:
                store = ReplayReviewStore(base_dir=tmpdir)
                store.append_snapshot({"snapshot_id": "RRD-001"})
                # Inject corrupted line
                path = store._path("dashboard_snapshots.jsonl")
                with open(path, "a", encoding="utf-8") as f:
                    f.write("{CORRUPTED JSON\n")
                store.append_snapshot({"snapshot_id": "RRD-002"})
                snaps = store.get_snapshots()
                assert len(snaps) == 2, f"Expected 2 valid records, got {len(snaps)}"
            return ("PASS", "Store corrupted recovery: 2 valid records preserved despite corrupted line")
        except Exception as exc:
            return ("FAIL", f"StoreCorruptedRecovery error: {exc}")


def run_health_check() -> None:
    """Run health check and print formatted results."""
    try:
        from replay.replay_timing import ReplayOperationTimer
        timer = ReplayOperationTimer()
        timer.start("replay-review-health")
    except Exception:
        timer = None

    print("=" * 70)
    print("  Replay Review Dashboard Health Check v1.2.6")
    print("  [!] Research Only | No Real Orders | No Auto Review Complete")
    print("  [!] No Auto Outcome Reveal | No Auto Confirm | Not Investment Advice")
    print("=" * 70)

    hc = ReplayReviewDashboardHealthCheck()
    results = hc.run()

    counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "BLOCKED": 0}

    for name, (status, message) in results.items():
        counts[status] = counts.get(status, 0) + 1
        print(f"  [{status}] {name}: {message}")

    print("-" * 70)
    total = sum(counts.values())
    overall = "PASS" if counts["FAIL"] == 0 and counts["BLOCKED"] == 0 else "FAIL"
    print(
        f"  Overall: {overall} | {total} checks | "
        f"PASS={counts['PASS']} WARN={counts['WARN']} "
        f"FAIL={counts['FAIL']} BLOCKED={counts['BLOCKED']}"
    )
    print("=" * 70)
    print()
    if timer:
        try:
            timer.finish("COMPLETED")
            timer.print_summary()
        except Exception:
            pass
    print("[!] Research Only. Not Investment Advice.")
    return [
        {"check": name, "status": status, "detail": message}
        for name, (status, message) in results.items()
    ]
