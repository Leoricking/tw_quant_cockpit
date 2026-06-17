"""
replay/scoring_health.py — ReplayScoringHealthCheck for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Health check verifies all scoring invariants.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScoringHealthCheck:
    """
    Health check for the replay scoring module.
    Checks: imports, schema, safety flags, process score, outcome reveal,
    composite score, mistake taxonomy, mistake review, scoring store.

    [!] Research Only. No Real Orders.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Returns dict of check_name -> (status, message)."""
        results: Dict[str, Tuple[str, str]] = {}
        results["imports"] = self._check_imports()
        results["scoring_schema"] = self._check_scoring_schema()
        results["process_score_engine"] = self._check_process_score_engine()
        results["outcome_reveal_blocked"] = self._check_outcome_reveal_blocked()
        results["composite_score_process_only"] = self._check_composite_process_only()
        results["mistake_taxonomy"] = self._check_mistake_taxonomy()
        results["mistake_detector_no_auto_confirm"] = self._check_mistake_no_auto_confirm()
        results["mistake_review_no_auto_confirm"] = self._check_mistake_review_no_auto_confirm()
        results["scoring_store"] = self._check_scoring_store()
        results["safety_flags"] = self._check_safety_flags()
        results["wait_skip_not_mistake"] = self._check_wait_skip_not_mistake()
        results["planned_stop_not_panic"] = self._check_planned_stop_not_panic()
        results["score_confidence"] = self._check_score_confidence()
        return results

    def _check_imports(self) -> Tuple[str, str]:
        modules = [
            "replay.scoring_schema",
            "replay.process_score_engine",
            "replay.outcome_score_engine",
            "replay.composite_score_engine",
            "replay.score_confidence",
            "replay.score_explainer",
            "replay.outcome_reveal",
            "replay.plan_adherence",
            "replay.mistake_taxonomy",
            "replay.mistake_detector",
            "replay.mistake_review",
            "replay.scoring_store",
            "replay.scoring_query",
            "replay.scoring_summary",
        ]
        failed = []
        for mod in modules:
            try:
                __import__(mod)
            except Exception as exc:
                failed.append(f"{mod}: {exc}")
        if failed:
            return ("FAIL", f"Import failures: {'; '.join(failed[:3])}")
        return ("PASS", f"All {len(modules)} scoring modules imported successfully")

    def _check_scoring_schema(self) -> Tuple[str, str]:
        try:
            from replay.scoring_schema import (
                ScoreComponent, ReplayProcessScore, ReplayOutcomeScore,
                ReplayCompositeScore, MistakeRecord, MistakeReviewRecord,
                OutcomeRevealRecord, SCORE_ID_PREFIX, MISTAKE_ID_PREFIX,
            )
            # Instantiate each
            sc = ScoreComponent(dimension="test", raw_score=0.8, weight=10, weighted_score=8.0)
            assert sc.simulation_only is True
            assert sc.no_real_orders is True

            ps = ReplayProcessScore(score_id="PSC-TEST", session_id="SID-TEST")
            assert ps.no_real_orders is True
            assert ps.scoring_triggers_no_orders is True

            os_ = ReplayOutcomeScore(score_id="OSC-TEST", session_id="SID-TEST", reveal_id="REV-TEST")
            assert os_.status == "BLOCKED"
            assert os_.auto_outcome_reveal_enabled is False

            cs = ReplayCompositeScore(score_id="CSC-TEST", session_id="SID-TEST")
            assert cs.classification == "BLOCKED"

            mr = MistakeRecord(mistake_id="MIS-TEST", session_id="SID-TEST")
            assert mr.auto_confirmed is False

            mrv = MistakeReviewRecord(review_id="MRV-TEST", mistake_id="MIS-TEST", session_id="SID-TEST")
            assert mrv.auto_confirmed is False

            orr = OutcomeRevealRecord(reveal_id="REV-TEST", session_id="SID-TEST")
            assert orr.auto_outcome_reveal_enabled is False
            assert orr.original_snapshot_unchanged is True

            return ("PASS", "All scoring schema dataclasses instantiate with correct safety invariants")
        except Exception as exc:
            return ("FAIL", f"Scoring schema check failed: {exc}")

    def _check_process_score_engine(self) -> Tuple[str, str]:
        try:
            from replay.process_score_engine import ReplayProcessScoreEngine
            engine = ReplayProcessScoreEngine()
            assert engine.RESEARCH_ONLY is True
            assert engine.SCORING_TRIGGERS_NO_ORDERS is True

            score = engine.score(
                session_id="RPL-TST-20230101-TEST",
                journal_entry={
                    "journal_entry_id": "DJR-TEST",
                    "action": "WAIT",
                    "decision_reason": "No valid setup present.",
                    "symbol": "TST",
                    "replay_date": "2023-01-02",
                },
                session_state={"status": "COMPLETED", "completed": True, "available_records": 30},
            )
            # WAIT with reason should get reasonable score
            assert score.total_score > 0
            assert score.no_real_orders is True
            assert score.scoring_triggers_no_orders is True

            # Check WAIT/SKIP doesn't get low thesis quality
            thesis_comp = next((c for c in score.components if c.dimension == "thesis_quality"), None)
            if thesis_comp:
                assert thesis_comp.raw_score >= 0.6, (
                    f"WAIT with reason should have thesis >= 0.6, got {thesis_comp.raw_score}"
                )

            return ("PASS", f"Process score engine works correctly, WAIT score={score.total_score:.1f}")
        except Exception as exc:
            return ("FAIL", f"Process score engine check failed: {exc}")

    def _check_outcome_reveal_blocked(self) -> Tuple[str, str]:
        try:
            from replay.outcome_reveal import ReplayOutcomeRevealManager
            mgr = ReplayOutcomeRevealManager()
            assert mgr.AUTO_OUTCOME_REVEAL_ENABLED is False

            # Without flags → BLOCKED
            record = mgr.reveal(
                session_id="RPL-TST-TEST",
                session_state={"status": "COMPLETED", "completed": True},
                reveal_flag=False,
                confirm_review_flag=False,
            )
            assert record.status == "BLOCKED", f"Expected BLOCKED, got {record.status}"
            assert record.auto_outcome_reveal_enabled is False

            # With only one flag → BLOCKED
            record2 = mgr.reveal(
                session_id="RPL-TST-TEST",
                session_state={"status": "COMPLETED", "completed": True},
                reveal_flag=True,
                confirm_review_flag=False,
            )
            assert record2.status == "BLOCKED"

            return ("PASS", "Outcome reveal correctly BLOCKED without both flags")
        except Exception as exc:
            return ("FAIL", f"Outcome reveal check failed: {exc}")

    def _check_composite_process_only(self) -> Tuple[str, str]:
        try:
            from replay.composite_score_engine import ReplayCompositeScoreEngine
            engine = ReplayCompositeScoreEngine()

            # Without outcome → PROCESS_ONLY
            result = engine.build(
                session_id="RPL-TST-TEST",
                process_score={"score_id": "PSC-TEST", "total_score": 75.0, "status": "SCORED"},
                outcome_score=None,
            )
            assert result.status == "PROCESS_ONLY", f"Expected PROCESS_ONLY, got {result.status}"
            assert result.classification == "PROCESS_ONLY"

            # outcome_weight > 0.5 warns
            result2 = engine.build(
                session_id="RPL-TST-TEST",
                process_score={"score_id": "PSC-TEST", "total_score": 75.0, "status": "SCORED"},
                outcome_score=None,
                process_weight=0.3,
                outcome_weight=0.7,
            )
            assert any("outcome_weight" in w for w in result2.warnings), "Expected outcome_weight warning"

            return ("PASS", "Composite score correctly PROCESS_ONLY without outcome; weight warning fires")
        except Exception as exc:
            return ("FAIL", f"Composite score check failed: {exc}")

    def _check_mistake_taxonomy(self) -> Tuple[str, str]:
        try:
            from replay.mistake_taxonomy import MistakeTaxonomy, MistakeType
            assert MistakeTaxonomy.RESEARCH_ONLY is True
            assert len(MistakeTaxonomy.ALL_TYPES) >= 20

            # PANIC_SELL requires planned exception check
            assert MistakeTaxonomy.requires_planned_exception_check(MistakeType.PANIC_SELL)
            assert MistakeTaxonomy.requires_planned_exception_check(MistakeType.EXITED_TOO_EARLY)

            # Emotional types are flagged
            assert MistakeTaxonomy.is_emotional(MistakeType.FOMO_ENTRY)
            assert MistakeTaxonomy.is_emotional(MistakeType.REVENGE_TRADE)

            return ("PASS", f"Mistake taxonomy: {len(MistakeTaxonomy.ALL_TYPES)} types, planned exception checks correct")
        except Exception as exc:
            return ("FAIL", f"Mistake taxonomy check failed: {exc}")

    def _check_mistake_no_auto_confirm(self) -> Tuple[str, str]:
        try:
            from replay.mistake_detector import ReplayMistakeDetector
            detector = ReplayMistakeDetector()
            assert detector.AUTO_MISTAKE_CONFIRMATION_ENABLED is False

            mistakes = detector.detect(
                session_id="RPL-TST-TEST",
                journal_entry={"action": "ENTER", "symbol": "TST", "replay_date": "2023-01-02"},
                session_state={"status": "COMPLETED", "completed": True},
            )
            for m in mistakes:
                assert m.auto_confirmed is False, f"Mistake {m.mistake_type} must not be auto-confirmed"
                assert m.status in ("SUGGESTED", "NEEDS_REVIEW"), (
                    f"Mistake {m.mistake_type} status must be SUGGESTED or NEEDS_REVIEW, got {m.status}"
                )

            return ("PASS", f"Mistake detector: {len(mistakes)} detected, none auto-confirmed")
        except Exception as exc:
            return ("FAIL", f"Mistake detector check failed: {exc}")

    def _check_mistake_review_no_auto_confirm(self) -> Tuple[str, str]:
        try:
            from replay.mistake_review import ReplayMistakeReviewManager
            mgr = ReplayMistakeReviewManager()
            assert mgr.AUTO_MISTAKE_CONFIRMATION_ENABLED is False

            # System_review cannot confirm
            record = mgr.confirm(
                mistake={"mistake_id": "MIS-TEST", "session_id": "SID-TEST"},
                reviewer="SYSTEM_REVIEW",
            )
            assert record.auto_confirmed is False
            assert record.new_status != "CONFIRMED", (
                f"SYSTEM_REVIEW must not set status to CONFIRMED, got {record.new_status}"
            )

            return ("PASS", "Mistake review: SYSTEM cannot auto-confirm")
        except Exception as exc:
            return ("FAIL", f"Mistake review check failed: {exc}")

    def _check_scoring_store(self) -> Tuple[str, str]:
        try:
            import tempfile
            from replay.scoring_store import ReplayScoringStore

            with tempfile.TemporaryDirectory() as tmpdir:
                store = ReplayScoringStore(repo_root=tmpdir)
                assert store.RESEARCH_ONLY is True

                # Append and load
                store.append("process_score", {"score_id": "PSC-TEST", "session_id": "SID", "total_score": 75.0})
                records = store.load_all("process_score")
                assert len(records) == 1
                assert records[0]["score_id"] == "PSC-TEST"

                # Test corrupted line tolerance
                path = store.store_path("process_score")
                with open(path, "a", encoding="utf-8") as f:
                    f.write("CORRUPTED JSON LINE\n")
                records2 = store.load_all("process_score")
                assert len(records2) == 1, "Corrupted line should be skipped, not crash"

            return ("PASS", "Scoring store: append/load works, corrupted lines skipped")
        except Exception as exc:
            return ("FAIL", f"Scoring store check failed: {exc}")

    def _check_safety_flags(self) -> Tuple[str, str]:
        try:
            from replay.scoring_schema import (
                NO_REAL_ORDERS, SCORING_TRIGGERS_NO_ORDERS,
                AUTO_OUTCOME_REVEAL_ENABLED, AUTO_MISTAKE_CONFIRMATION_ENABLED,
                AUTO_SCORE_TO_TRADE_ENABLED,
            )
            assert NO_REAL_ORDERS is True
            assert SCORING_TRIGGERS_NO_ORDERS is True
            assert AUTO_OUTCOME_REVEAL_ENABLED is False
            assert AUTO_MISTAKE_CONFIRMATION_ENABLED is False
            assert AUTO_SCORE_TO_TRADE_ENABLED is False
            return ("PASS", "All scoring safety flags correct")
        except Exception as exc:
            return ("FAIL", f"Safety flags check failed: {exc}")

    def _check_wait_skip_not_mistake(self) -> Tuple[str, str]:
        try:
            from replay.mistake_detector import ReplayMistakeDetector
            detector = ReplayMistakeDetector()

            # WAIT with documented reason should produce no mistakes
            mistakes = detector.detect(
                session_id="RPL-TST-TEST",
                journal_entry={
                    "action": "WAIT",
                    "symbol": "TST",
                    "replay_date": "2023-01-02",
                    "decision_reason": "No valid breakout confirmation.",
                },
            )
            assert len(mistakes) == 0, (
                f"Well-reasoned WAIT should NOT produce mistakes, got {len(mistakes)}"
            )

            # SKIP with no_trade_conditions should produce no mistakes
            mistakes2 = detector.detect(
                session_id="RPL-TST-TEST",
                journal_entry={
                    "action": "SKIP",
                    "symbol": "TST",
                    "replay_date": "2023-01-02",
                    "no_trade_conditions": ["Volume too low"],
                },
            )
            assert len(mistakes2) == 0, (
                f"SKIP with no_trade_conditions should NOT produce mistakes, got {len(mistakes2)}"
            )

            return ("PASS", "WAIT/SKIP with documented rationale produces no mistakes")
        except Exception as exc:
            return ("FAIL", f"WAIT/SKIP mistake check failed: {exc}")

    def _check_planned_stop_not_panic(self) -> Tuple[str, str]:
        try:
            from replay.mistake_detector import ReplayMistakeDetector
            detector = ReplayMistakeDetector()

            # STOP with risk_plan_id → should NOT flag as PANIC_SELL
            mistakes = detector.detect(
                session_id="RPL-TST-TEST",
                journal_entry={
                    "action": "STOP",
                    "symbol": "TST",
                    "replay_date": "2023-01-02",
                    "risk_plan_id": "RSK-PLANNED",
                    "fallback_action": "STOP",
                },
            )
            panic_sells = [m for m in mistakes if m.mistake_type == "PANIC_SELL"]
            assert len(panic_sells) == 0, (
                f"Planned stop (risk_plan_id present) should NOT be PANIC_SELL, got {len(panic_sells)}"
            )

            return ("PASS", "Planned stop correctly NOT classified as PANIC_SELL")
        except Exception as exc:
            return ("FAIL", f"Planned stop check failed: {exc}")

    def _check_score_confidence(self) -> Tuple[str, str]:
        try:
            from replay.score_confidence import ReplayScoreConfidence
            sc = ReplayScoreConfidence()

            # Mock → DEMO_ONLY
            level, _ = sc.assess(entry_count=100, is_mock=True)
            assert level == "DEMO_ONLY", f"Mock should be DEMO_ONLY, got {level}"

            # < 10 → INSUFFICIENT
            level2, _ = sc.assess(entry_count=5)
            assert level2 == "INSUFFICIENT", f"< 10 entries should be INSUFFICIENT, got {level2}"

            # 10-29 → OBSERVATIONAL
            level3, _ = sc.assess(entry_count=15)
            assert level3 == "OBSERVATIONAL", f"10-29 entries should be OBSERVATIONAL, got {level3}"

            # >= 30, sessions >= 10 → RELIABLE
            level4, _ = sc.assess(entry_count=35, session_count=12)
            assert level4 == "RELIABLE", f">= 30 + >= 10 sessions should be RELIABLE, got {level4}"

            return ("PASS", "Score confidence levels correct: DEMO_ONLY/INSUFFICIENT/OBSERVATIONAL/RELIABLE")
        except Exception as exc:
            return ("FAIL", f"Score confidence check failed: {exc}")

    def overall_status(self, results: Dict[str, Tuple[str, str]]) -> str:
        statuses = [r[0] for r in results.values()]
        if "BLOCKED" in statuses:
            return "BLOCKED"
        if "FAIL" in statuses:
            return "FAIL"
        if "WARN" in statuses:
            return "WARN"
        return "PASS"

    def print_results(self, results: Dict[str, Tuple[str, str]]) -> None:
        print("=" * 65)
        print("  Replay Scoring & Mistake Taxonomy Health Check v1.2.3")
        print("  [!] Research Only | No Real Orders | Scoring Triggers No Orders")
        print("=" * 65)
        for check_name, (status, message) in results.items():
            icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "BLOCKED": "[BLKD]"}.get(status, "[????]")
            print(f"  {icon} {check_name}: {message}")
        overall = self.overall_status(results)
        print("-" * 65)
        print(f"  Overall: {overall}")
        print("=" * 65)
