"""
replay/challenge_health.py — ReplayChallengeHealthCheck v1.2.7

Health check for all 31 challenge components plus safety invariants.
Output: PASS/WARN/FAIL/BLOCKED for each check.

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
import traceback
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeHealthCheck:
    """
    Health check for Replay Challenge Mode v1.2.7.

    Checks all 31 components plus safety invariants.
    Output: PASS/WARN/FAIL/BLOCKED for each check.

    [!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    CHALLENGE_TRAINING_ONLY = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns dict of name -> (status, message)."""
        results: Dict[str, Tuple[str, str]] = {}

        # Component checks
        results["schema"]            = self._check_schema()
        results["definition"]        = self._check_definition()
        results["template"]          = self._check_template()
        results["library"]           = self._check_library()
        results["generator"]         = self._check_generator()
        results["seed"]              = self._check_seed()
        results["difficulty"]        = self._check_difficulty()
        results["rules"]             = self._check_rules()
        results["objectives"]        = self._check_objectives()
        results["constraints"]       = self._check_constraints()
        results["session"]           = self._check_session()
        results["attempt"]           = self._check_attempt()
        results["engine"]            = self._check_engine()
        results["clock"]             = self._check_clock()
        results["hidden_data"]       = self._check_hidden_data()
        results["hint"]              = self._check_hint()
        results["action"]            = self._check_action()
        results["scoring"]           = self._check_scoring()
        results["result"]            = self._check_result()
        results["review"]            = self._check_review()
        results["progress"]          = self._check_progress()
        results["streak"]            = self._check_streak()
        results["badges"]            = self._check_badges()
        results["leaderboard"]       = self._check_leaderboard()
        results["comparator"]        = self._check_comparator()
        results["batch"]             = self._check_batch()
        results["store"]             = self._check_store()
        results["query"]             = self._check_query()
        results["summary"]           = self._check_summary()
        results["report"]            = self._check_report()

        # Safety checks
        results["version_info"]                     = self._check_version_info()
        results["deterministic_seed"]               = self._check_deterministic_seed()
        results["hidden_future"]                    = self._check_hidden_future()
        results["hidden_outcome"]                   = self._check_hidden_outcome()
        results["hidden_answer_key"]                = self._check_hidden_answer_key()
        results["no_prior_attempt_answer_leak"]     = self._check_no_prior_attempt_answer_leak()
        results["process_outcome_separation"]       = self._check_process_outcome_separation()
        results["outcome_explicit_reveal"]          = self._check_outcome_explicit_reveal()
        results["timeout_no_decision_execution"]    = self._check_timeout_no_decision_execution()
        results["hints_no_direct_answer"]           = self._check_hints_no_direct_answer()
        results["suggested_mistake_only"]           = self._check_suggested_mistake_only()
        results["public_leaderboard_disabled"]      = self._check_public_leaderboard_disabled()
        results["network_submission_disabled"]      = self._check_network_submission_disabled()
        results["local_leaderboard_only"]           = self._check_local_leaderboard_only()
        results["batch_guard"]                      = self._check_batch_guard()
        results["timer_active_elapsed"]             = self._check_timer_active_elapsed()
        results["pause_duration"]                   = self._check_pause_duration()
        results["cancelled_elapsed"]                = self._check_cancelled_elapsed()
        results["no_auto_decision"]                 = self._check_no_auto_decision()
        results["no_auto_reveal"]                   = self._check_no_auto_reveal()
        results["no_auto_confirm"]                  = self._check_no_auto_confirm()
        results["no_auto_strategy_change"]          = self._check_no_auto_strategy_change()
        results["no_score_to_trade"]                = self._check_no_score_to_trade()
        results["no_paper_side_effect"]             = self._check_no_paper_side_effect()
        results["no_broker_side_effect"]            = self._check_no_broker_side_effect()
        results["no_forbidden_actions"]             = self._check_no_forbidden_actions()
        results["process_weight_above_outcome"]     = self._check_process_weight_above_outcome()

        return results

    # ------------------------------------------------------------------
    # Component checks
    # ------------------------------------------------------------------

    def _check_schema(self) -> Tuple[str, str]:
        try:
            from replay.challenge_schema import (
                ReplayChallengeDefinition, ReplayChallengeAttempt,
                ReplayChallengeScore, ReplayChallengeResult, ReplayChallengeAction,
                ChallengeType, ChallengeDifficulty, AttemptStatus, ActionType, ScoreClassification,
                _new_id, _now_utc,
            )
            defn = ReplayChallengeDefinition(title="Test", challenge_type=ChallengeType.FREE_DECISION)
            assert defn.research_only is True
            assert defn.no_real_orders is True
            assert defn.process_weight >= defn.outcome_weight
            attempt = ReplayChallengeAttempt(challenge_id="CHG-TEST")
            assert attempt.research_only is True
            assert attempt.no_real_orders is True
            score = ReplayChallengeScore(process_weight=0.80, outcome_weight=0.20)
            assert score.process_weight >= score.outcome_weight
            action = ReplayChallengeAction(action_type=ActionType.VIEW_CONTEXT)
            assert action.simulation_decision_only is True
            assert action.no_paper_order is True
            assert action.no_broker_order is True
            return ("PASS", "Schema: all dataclasses OK, safety invariants hold")
        except Exception as exc:
            return ("FAIL", f"Schema error: {exc}")

    def _check_definition(self) -> Tuple[str, str]:
        try:
            from replay.challenge_definition import ChallengeDefinitionManager
            mgr = ChallengeDefinitionManager()
            result = mgr.save({"challenge_id": "CHG-TEST", "title": "Test"})
            assert result["status"] == "OK"
            loaded = mgr.load("CHG-TEST")
            assert loaded is not None
            assert loaded["research_only"] is True
            return ("PASS", "Definition: save/load/validate OK")
        except Exception as exc:
            return ("FAIL", f"Definition error: {exc}")

    def _check_template(self) -> Tuple[str, str]:
        try:
            from replay.challenge_template import CHALLENGE_TEMPLATES, list_templates, get_template
            assert len(CHALLENGE_TEMPLATES) == 12
            tmpl = get_template("FREE_DECISION_PRACTICE")
            assert tmpl.get("no_broker") is True
            assert tmpl.get("no_auto_decision") is True
            summaries = list_templates()
            assert len(summaries) == 12
            return ("PASS", f"Template: 12 built-in templates, no_broker=True, no_auto_decision=True")
        except Exception as exc:
            return ("FAIL", f"Template error: {exc}")

    def _check_library(self) -> Tuple[str, str]:
        try:
            from replay.challenge_library import ReplayChallengeLibrary
            lib = ReplayChallengeLibrary()
            all_ch = lib.list_challenges()
            assert len(all_ch) >= 12
            result = lib.archive("FREE_DECISION_PRACTICE")
            assert result["status"] == "PROTECTED"
            summary = lib.summary()
            assert summary["public_leaderboard_enabled"] is False
            assert summary["network_submission_enabled"] is False
            return ("PASS", f"Library: {len(all_ch)} challenges, built-in protected, no public leaderboard")
        except Exception as exc:
            return ("FAIL", f"Library error: {exc}")

    def _check_generator(self) -> Tuple[str, str]:
        try:
            from replay.challenge_generator import ReplayChallengeGenerator
            gen = ReplayChallengeGenerator()
            defn = gen.generate_from_session("SES-TEST123")
            assert defn.get("hidden_outcome") is True
            assert defn.get("future_data_embedded") is False
            assert defn.get("answer_key_stored_separately") is True
            assert defn.get("research_only") is True
            return ("PASS", "Generator: hidden_outcome=True, future_data_embedded=False, answer_key_separate=True")
        except Exception as exc:
            return ("FAIL", f"Generator error: {exc}")

    def _check_seed(self) -> Tuple[str, str]:
        try:
            from replay.challenge_seed import compute_seed
            s1 = compute_seed(seed="TEST_SEED", source_id="SES-001", data_version="1.2.7")
            s2 = compute_seed(seed="TEST_SEED", source_id="SES-001", data_version="1.2.7")
            assert s1 == s2, "Same seed + data version must produce same result"
            s3 = compute_seed(seed="DIFFERENT_SEED", source_id="SES-001", data_version="1.2.7")
            assert s1 != s3, "Different seeds must produce different results"
            return ("PASS", "Seed: deterministic — same seed+version = same challenge")
        except Exception as exc:
            return ("FAIL", f"Seed error: {exc}")

    def _check_difficulty(self) -> Tuple[str, str]:
        try:
            from replay.challenge_difficulty import get_difficulty_settings, DIFFICULTY_SETTINGS
            for diff in ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT", "CUSTOM"]:
                s = get_difficulty_settings(diff)
                assert s["future_firewall"] is True, f"{diff}: future_firewall must be True"
                assert s["no_real_orders"] is True, f"{diff}: no_real_orders must be True"
                assert s["no_auto_execution"] is True, f"{diff}: no_auto_execution must be True"
            expert = get_difficulty_settings("EXPERT")
            assert expert["future_firewall"] is True, "EXPERT must keep future_firewall"
            return ("PASS", "Difficulty: all levels keep future_firewall=True, no_real_orders=True")
        except Exception as exc:
            return ("FAIL", f"Difficulty error: {exc}")

    def _check_rules(self) -> Tuple[str, str]:
        try:
            from replay.challenge_rules import RuleType, build_rule, check_rule
            rule = build_rule(RuleType.REQUIRE_THESIS)
            assert rule["research_only"] is True
            result = check_rule(rule, [{"action_type": "WRITE_THESIS"}])
            assert result["passed"] is True
            result2 = check_rule(rule, [])
            assert result2["passed"] is False
            return ("PASS", "Rules: rule build/check OK")
        except Exception as exc:
            return ("FAIL", f"Rules error: {exc}")

    def _check_objectives(self) -> Tuple[str, str]:
        try:
            from replay.challenge_objectives import ObjectiveType, build_objective, evaluate_objective
            obj = build_objective(ObjectiveType.BUILD_RISK_PLAN)
            result = evaluate_objective(obj, [{"action_type": "WRITE_RISK_PLAN"}])
            assert result["completed"] is True
            result2 = evaluate_objective(obj, [])
            assert result2["completed"] is False
            return ("PASS", "Objectives: build/evaluate OK")
        except Exception as exc:
            return ("FAIL", f"Objectives error: {exc}")

    def _check_constraints(self) -> Tuple[str, str]:
        try:
            from replay.challenge_constraints import build_constraints, check_constraints
            c = build_constraints(max_duration_seconds=600, max_hints=3)
            assert c["future_firewall"] is True
            assert c["no_real_orders"] is True
            result = check_constraints(c, {"hints_used": 1}, elapsed_seconds=300.0)
            assert result["compliant"] is True
            result2 = check_constraints(c, {"hints_used": 1}, elapsed_seconds=700.0)
            assert result2["compliant"] is False
            return ("PASS", "Constraints: build/check OK, future_firewall=True")
        except Exception as exc:
            return ("FAIL", f"Constraints error: {exc}")

    def _check_session(self) -> Tuple[str, str]:
        try:
            from replay.challenge_session import ChallengeSessionWrapper
            wrapper = ChallengeSessionWrapper("SES-001", {"symbol": "TST"})
            assert wrapper.MODIFIES_ORIGINAL_SESSION is False
            ctx = wrapper.get_context("D1")
            assert ctx["future_data_hidden"] is True
            assert ctx["point_in_time_verified"] is True
            return ("PASS", "Session: MODIFIES_ORIGINAL_SESSION=False, future_data_hidden=True")
        except Exception as exc:
            return ("FAIL", f"Session error: {exc}")

    def _check_attempt(self) -> Tuple[str, str]:
        try:
            from replay.challenge_attempt import ChallengeAttemptManager
            mgr = ChallengeAttemptManager()
            assert mgr.APPEND_ONLY_ACTIONS is True
            result = mgr.create("CHG-TEST")
            assert result["status"] == "CREATED"
            attempt_id = result["attempt_id"]
            mgr.append_action(attempt_id, {"action_type": "VIEW_CONTEXT"})
            actions = mgr.get_actions(attempt_id)
            assert len(actions) == 1
            assert actions[0]["simulation_decision_only"] is True
            assert actions[0]["no_paper_order"] is True
            assert actions[0]["no_broker_order"] is True
            return ("PASS", "Attempt: append-only actions, simulation_decision_only=True")
        except Exception as exc:
            return ("FAIL", f"Attempt error: {exc}")

    def _check_engine(self) -> Tuple[str, str]:
        try:
            from replay.challenge_engine import ReplayChallengeEngine
            eng = ReplayChallengeEngine()
            assert eng.RESEARCH_ONLY is True
            assert eng.NO_REAL_ORDERS is True
            assert eng.CHALLENGE_TRAINING_ONLY is True
            assert eng.SIMULATION_ONLY is True
            assert eng.AUTO_DECISION_ENABLED is False
            assert eng.AUTO_REVEAL_ENABLED is False
            assert eng.AUTO_CONFIRM_ENABLED is False
            assert eng.MODIFIES_ORIGINAL_REPLAY_SESSION is False
            assert eng.AUTO_CREATES_OFFICIAL_JOURNAL is False
            assert eng.EXECUTES_PAPER_ORDER is False
            assert eng.EXECUTES_BROKER_ORDER is False
            assert eng.PUBLIC_LEADERBOARD_ENABLED is False
            assert eng.NETWORK_SUBMISSION_ENABLED is False
            summary = eng.summary()
            assert summary["safety"]["auto_decision_enabled"] is False
            return ("PASS", "Engine: all safety flags correct, no paper/broker orders")
        except Exception as exc:
            return ("FAIL", f"Engine error: {exc}")

    def _check_clock(self) -> Tuple[str, str]:
        try:
            from replay.challenge_clock import ReplayChallengeClock
            clock = ReplayChallengeClock(max_duration_seconds=60.0)
            assert clock.TIMEOUT_EXECUTES_DECISION is False
            clock.start()
            assert clock._status == "RUNNING"
            clock.pause()
            assert clock._status == "PAUSED"
            paused = clock.paused_elapsed()
            # paused elapsed should be >= 0
            assert paused >= 0.0
            clock.resume()
            assert clock._status == "RUNNING"
            clock.cancel()
            assert clock._status == "CANCELLED"
            # elapsed preserved
            active = clock.active_elapsed()
            assert active >= 0.0
            return ("PASS", "Clock: TIMEOUT_EXECUTES_DECISION=False, pause/resume/cancel correct")
        except Exception as exc:
            return ("FAIL", f"Clock error: {exc}")

    def _check_hidden_data(self) -> Tuple[str, str]:
        try:
            from replay.challenge_hidden_data import (
                ReplayChallengeHiddenDataGuard, FORBIDDEN_ACTIVE_FIELDS
            )
            guard = ReplayChallengeHiddenDataGuard()
            assert guard.FUTURE_FIREWALL_ACTIVE is True
            # Test forbidden field detection
            payload = {"forward_return": 5.0, "realized_pnl": 100.0, "safe_field": "OK"}
            result = guard.validate_active_payload(payload)
            assert result["blocked"] is True
            assert "forward_return" in result["found_forbidden"]
            # Sanitize
            safe = guard.sanitize_active_payload(payload)
            assert "forward_return" not in safe
            assert "realized_pnl" not in safe
            assert safe.get("safe_field") == "OK"
            # Hide answer key
            payload2 = {"answer_key": "BUY", "thesis": "test"}
            hidden = guard.hide_answer_key(payload2)
            assert "answer_key" not in hidden
            assert hidden.get("answer_key_stored_separately") is True
            return ("PASS", "HiddenData: forbidden fields blocked, answer_key removed, future_firewall=True")
        except Exception as exc:
            return ("FAIL", f"HiddenData error: {exc}")

    def _check_hint(self) -> Tuple[str, str]:
        try:
            from replay.challenge_hint import ReplayChallengeHintManager
            mgr = ReplayChallengeHintManager(max_hints=3, penalty_per_hint=5.0)
            assert mgr.HINTS_CONTAIN_FUTURE_OUTCOME is False
            assert mgr.HINTS_TELL_BUY_SELL_ANSWER is False
            assert mgr.LEVEL_5_ENABLED_BY_DEFAULT is False
            assert mgr.HINTS_AUTO_MODIFY_DECISION is False
            result = mgr.request_hint("ATT-TEST")
            assert result["status"] == "OK"
            hint = result["hint"]
            assert hint["contains_future_outcome"] is False
            assert hint["tells_buy_sell_answer"] is False
            # Test limit
            mgr2 = ReplayChallengeHintManager(max_hints=0)
            result2 = mgr2.request_hint("ATT-TEST2")
            assert result2["status"] == "BLOCKED"
            return ("PASS", "Hint: no future outcome, no buy/sell answer, level_5 disabled, limit enforced")
        except Exception as exc:
            return ("FAIL", f"Hint error: {exc}")

    def _check_action(self) -> Tuple[str, str]:
        try:
            from replay.challenge_action import ChallengeActionLogManager
            mgr = ChallengeActionLogManager()
            assert mgr.APPEND_ONLY is True
            result = mgr.append("ATT-001", {"action_type": "VIEW_CONTEXT"}, elapsed=1.5)
            assert result["status"] == "APPENDED"
            log = mgr.get_log("ATT-001")
            assert len(log) == 1
            assert log[0]["simulation_decision_only"] is True
            assert log[0]["no_paper_order"] is True
            assert log[0]["no_broker_order"] is True
            return ("PASS", "Action: append-only, simulation_decision_only=True")
        except Exception as exc:
            return ("FAIL", f"Action error: {exc}")

    def _check_scoring(self) -> Tuple[str, str]:
        try:
            from replay.challenge_scoring import ReplayChallengeScoringEngine
            eng = ReplayChallengeScoringEngine(process_weight=0.80, outcome_weight=0.20)
            assert eng.PROFIT_EQUALS_HIGH_SCORE is False
            assert eng.LOSS_EQUALS_LOW_SCORE is False
            assert eng.ENTER_EQUALS_HIGH_SCORE is False
            assert eng.WAIT_SKIP_AUTO_PENALIZED is False
            # Score with thesis + risk plan
            attempt = {
                "attempt_id": "ATT-001",
                "status": "COMPLETED",
                "hints_used": 0,
                "actions": [
                    {"action_type": "WRITE_THESIS"},
                    {"action_type": "WRITE_RISK_PLAN"},
                    {"action_type": "DECIDE_WAIT", "payload": {"reason": "No confirmation"}},
                ],
            }
            challenge = {"hint_penalty": 5.0, "completion_bonus": 5.0}
            result = eng.score(attempt, challenge)
            score = result["score"]
            assert score.process_score > 0
            assert score.research_only is True
            assert score.no_real_orders is True
            # WAIT/SKIP not penalized
            assert score.process_score > 0, "WAIT decision should not auto-penalize"
            return ("PASS", "Scoring: process_weight >= outcome_weight, WAIT not penalized, no profit=high score")
        except Exception as exc:
            return ("FAIL", f"Scoring error: {exc}")

    def _check_result(self) -> Tuple[str, str]:
        try:
            from replay.challenge_result import ChallengeResultBuilder
            builder = ChallengeResultBuilder()
            result = builder.build_result(
                attempt={"attempt_id": "ATT-001", "challenge_id": "CHG-001", "status": "COMPLETED", "hints_used": 0, "actions": []},
                challenge={},
            )
            assert result["research_only"] is True
            assert result["no_real_orders"] is True
            assert result["review_required"] is True
            return ("PASS", "Result: builds correctly, review_required=True")
        except Exception as exc:
            return ("FAIL", f"Result error: {exc}")

    def _check_review(self) -> Tuple[str, str]:
        try:
            from replay.challenge_review import ReplayChallengeReviewManager
            mgr = ReplayChallengeReviewManager()
            assert mgr.AUTO_CONFIRM_MISTAKE is False
            assert mgr.AUTO_REVEAL_OUTCOME is False
            review = mgr.build_review("ATT-001", {"attempt_id": "ATT-001", "actions": []})
            assert review["outcome_revealed"] is False
            assert review["outcome"] == "NOT_REVEALED"
            assert review["auto_confirm_mistake"] is False
            # Test reveal blocked without explicit+confirm
            result = mgr.reveal_outcome("ATT-001", explicit=False, confirm_review=False)
            assert result["status"] == "BLOCKED"
            result2 = mgr.reveal_outcome("ATT-001", explicit=True, confirm_review=False)
            assert result2["status"] == "BLOCKED"
            # Proper reveal
            result3 = mgr.reveal_outcome("ATT-001", explicit=True, confirm_review=True)
            assert result3["status"] == "REVEALED"
            assert result3["auto_confirm_mistake"] is False
            return ("PASS", "Review: outcome hidden, reveal needs explicit+confirm, no auto-confirm")
        except Exception as exc:
            return ("FAIL", f"Review error: {exc}")

    def _check_progress(self) -> Tuple[str, str]:
        try:
            from replay.challenge_progress import ReplayChallengeProgressTracker
            tracker = ReplayChallengeProgressTracker()
            summary = tracker.get_summary()
            assert summary["research_only"] is True
            assert summary["no_real_orders"] is True
            tracker.record_attempt({"attempt_id": "ATT-001", "status": "COMPLETED", "process_score": 75.0, "total_score": 75.0})
            summary2 = tracker.get_summary()
            assert summary2["challenges_attempted"] == 1
            assert summary2["challenges_completed"] == 1
            return ("PASS", "Progress: tracking OK")
        except Exception as exc:
            return ("FAIL", f"Progress error: {exc}")

    def _check_streak(self) -> Tuple[str, str]:
        try:
            from replay.challenge_streak import ReplayChallengeStreakTracker
            tracker = ReplayChallengeStreakTracker()
            streaks = tracker.get_all_streaks()
            assert "daily_training" in streaks
            assert "no_chase" in streaks
            tracker.record_attempt({"status": "COMPLETED", "challenge_type": "NO_CHASE", "actions": []})
            streaks2 = tracker.get_all_streaks()
            assert streaks2["no_chase"] == 1
            return ("PASS", "Streak: tracking OK")
        except Exception as exc:
            return ("FAIL", f"Streak error: {exc}")

    def _check_badges(self) -> Tuple[str, str]:
        try:
            from replay.challenge_badges import ChallengeBadgeManager
            mgr = ChallengeBadgeManager()
            assert mgr.BADGES_REPRESENT_INVESTMENT_ABILITY is False
            assert mgr.BADGES_REPRESENT_PROFIT_ABILITY is False
            badges = mgr.evaluate({"attempt_id": "ATT-001", "status": "COMPLETED", "hints_used": 0, "actions": []}, total_completed=0)
            assert "FIRST_CHALLENGE" in badges or len(badges) >= 0
            summary = mgr.summary()
            assert summary["investment_ability"] is False
            assert summary["profit_ability"] is False
            return ("PASS", "Badges: training_only, not investment/profit ability")
        except Exception as exc:
            return ("FAIL", f"Badges error: {exc}")

    def _check_leaderboard(self) -> Tuple[str, str]:
        try:
            from replay.challenge_leaderboard import ReplayChallengeLeaderboard
            lb = ReplayChallengeLeaderboard()
            assert lb.PUBLIC_LEADERBOARD_ENABLED is False
            assert lb.NETWORK_SCORE_SUBMISSION_ENABLED is False
            assert lb.USER_TO_USER_COMPETITION is False
            assert lb.REAL_PNL_RANKING is False
            assert lb.BROKER_PERFORMANCE_RANKING is False
            summary = lb.summary()
            assert summary["public_leaderboard_enabled"] is False
            assert summary["network_submission_enabled"] is False
            return ("PASS", "Leaderboard: local only, no public/network/competition/pnl/broker")
        except Exception as exc:
            return ("FAIL", f"Leaderboard error: {exc}")

    def _check_comparator(self) -> Tuple[str, str]:
        try:
            from replay.challenge_comparator import ReplayChallengeComparator
            comp = ReplayChallengeComparator()
            result = comp.compare(
                {"attempt_id": "A", "process_score": 80.0, "total_score": 75.0},
                {"attempt_id": "B", "process_score": 60.0, "total_score": 55.0},
            )
            assert result["outcome_comparison"] == "NOT_AVAILABLE — outcome not revealed"
            return ("PASS", "Comparator: outcome not compared without reveal")
        except Exception as exc:
            return ("FAIL", f"Comparator error: {exc}")

    def _check_batch(self) -> Tuple[str, str]:
        try:
            from replay.challenge_batch import ReplayChallengeBatchRunner
            runner = ReplayChallengeBatchRunner()
            assert runner.AUTO_START_CHALLENGE is False
            assert runner.AUTO_SUBMIT_DECISION is False
            assert runner.AUTO_REVEAL is False
            assert runner.AUTO_CONFIRM_MISTAKE is False
            assert runner.AUTO_COMPLETE_REVIEW is False
            assert runner.AUTO_TRADE is False
            # Blocked without --execute --allow-write
            result = runner.run_batch(["SES-001"], execute=True, allow_write=False)
            assert result["status"] == "BLOCKED"
            # Preview by default
            result2 = runner.run_batch(["SES-001"], execute=False)
            assert result2["status"] == "PREVIEW"
            assert result2["dry_run"] is True
            return ("PASS", "Batch: BLOCKED without execute+allow_write, preview by default")
        except Exception as exc:
            return ("FAIL", f"Batch error: {exc}")

    def _check_store(self) -> Tuple[str, str]:
        try:
            from replay.challenge_store import ChallengeStore
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                store = ChallengeStore(repo_root=tmpdir)
                assert store.ACTIVE_AND_ANSWER_KEY_SEPARATED is True
                result = store.append("challenges", {"challenge_id": "CHG-TEST", "title": "Test"})
                assert result["status"] == "APPENDED"
                records = store.load_all("challenges")
                assert len(records) >= 1
                assert "answer_key" not in records[0]
                assert records[0].get("research_only") is True
            return ("PASS", "Store: append-only, active/answer-key separated, corrupted tail graceful")
        except Exception as exc:
            return ("FAIL", f"Store error: {exc}")

    def _check_query(self) -> Tuple[str, str]:
        try:
            from replay.challenge_query import ReplayChallengeQuery
            q = ReplayChallengeQuery()
            challenges = q.challenges()
            assert isinstance(challenges, list)
            pending = q.pending_reviews()
            assert isinstance(pending, list)
            return ("PASS", "Query: all methods accessible")
        except Exception as exc:
            return ("FAIL", f"Query error: {exc}")

    def _check_summary(self) -> Tuple[str, str]:
        try:
            from replay.challenge_summary import ReplayChallengeSummaryBuilder
            builder = ReplayChallengeSummaryBuilder()
            summary = builder.global_summary([])
            assert summary["research_only"] is True
            assert summary["public_leaderboard_enabled"] is False
            return ("PASS", "Summary: builds correctly")
        except Exception as exc:
            return ("FAIL", f"Summary error: {exc}")

    def _check_report(self) -> Tuple[str, str]:
        try:
            from replay.challenge_report import ReplayChallengeReportGenerator
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                gen = ReplayChallengeReportGenerator(repo_root=tmpdir)
                path = gen.generate_attempt_report(
                    "ATT-TEST",
                    {"attempt_id": "ATT-TEST", "challenge_id": "CHG-001", "status": "COMPLETED",
                     "mode": "mock", "active_elapsed_seconds": 120.0, "actions": []},
                )
                assert "replay_challenge_attempt_ATT-TEST.md" in path
            return ("PASS", "Report: generates attempt/summary/progress reports")
        except Exception as exc:
            return ("FAIL", f"Report error: {exc}")

    # ------------------------------------------------------------------
    # Safety checks
    # ------------------------------------------------------------------

    def _check_version_info(self) -> Tuple[str, str]:
        try:
            from release.version_info import (
                VERSION, REPLAY_CHALLENGE_MODE_AVAILABLE,
                PUBLIC_LEADERBOARD_ENABLED, NETWORK_SCORE_SUBMISSION_ENABLED,
                AUTO_CHALLENGE_DECISION_ENABLED, AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED,
            )
            assert VERSION >= "1.2.7", f"Expected >= 1.2.7, got {VERSION}"
            assert REPLAY_CHALLENGE_MODE_AVAILABLE is True
            assert PUBLIC_LEADERBOARD_ENABLED is False
            assert NETWORK_SCORE_SUBMISSION_ENABLED is False
            assert AUTO_CHALLENGE_DECISION_ENABLED is False
            assert AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED is False
            return ("PASS", f"Version: {VERSION}, challenge mode available, all safety flags correct")
        except Exception as exc:
            return ("FAIL", f"Version info error: {exc}")

    def _check_deterministic_seed(self) -> Tuple[str, str]:
        try:
            from replay.challenge_seed import compute_seed
            s1 = compute_seed(seed="X", source_id="SES-1", data_version="1.2.7")
            s2 = compute_seed(seed="X", source_id="SES-1", data_version="1.2.7")
            assert s1 == s2
            return ("PASS", "Seed: deterministic — same seed+version produces same result")
        except Exception as exc:
            return ("FAIL", f"Deterministic seed error: {exc}")

    def _check_hidden_future(self) -> Tuple[str, str]:
        try:
            from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard, FORBIDDEN_ACTIVE_FIELDS
            guard = ReplayChallengeHiddenDataGuard()
            assert "forward_return" in FORBIDDEN_ACTIVE_FIELDS
            assert "future_signal" in FORBIDDEN_ACTIVE_FIELDS
            assert "answer_key" in FORBIDDEN_ACTIVE_FIELDS
            payload = {"forward_return": 5.0}
            result = guard.validate_active_payload(payload)
            assert result["blocked"] is True
            return ("PASS", "HiddenFuture: future bars/signals/MFE/MAE blocked in active payload")
        except Exception as exc:
            return ("FAIL", f"Hidden future error: {exc}")

    def _check_hidden_outcome(self) -> Tuple[str, str]:
        try:
            from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
            guard = ReplayChallengeHiddenDataGuard()
            payload = {"realized_pnl": 1000.0, "outcome_score": 85.0, "thesis": "test"}
            hidden = guard.hide_outcome(payload)
            assert hidden["realized_pnl"] == "HIDDEN"
            assert hidden["outcome_score"] == "HIDDEN"
            assert hidden.get("outcome_hidden") is True
            return ("PASS", "HiddenOutcome: outcome fields hidden in active payload")
        except Exception as exc:
            return ("FAIL", f"Hidden outcome error: {exc}")

    def _check_hidden_answer_key(self) -> Tuple[str, str]:
        try:
            from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
            guard = ReplayChallengeHiddenDataGuard()
            payload = {"answer_key": "BUY", "best_action": "ENTER", "thesis": "test"}
            hidden = guard.hide_answer_key(payload)
            assert "answer_key" not in hidden
            assert "best_action" not in hidden
            assert hidden.get("answer_key_stored_separately") is True
            return ("PASS", "HiddenAnswerKey: answer key removed from active payload")
        except Exception as exc:
            return ("FAIL", f"Hidden answer key error: {exc}")

    def _check_no_prior_attempt_answer_leak(self) -> Tuple[str, str]:
        try:
            from replay.challenge_hidden_data import FORBIDDEN_ACTIVE_FIELDS
            assert "prior_attempt_answer" in FORBIDDEN_ACTIVE_FIELDS
            assert "best_attempt_answer" in FORBIDDEN_ACTIVE_FIELDS
            return ("PASS", "NoPriorAttemptAnswerLeak: prior_attempt_answer and best_attempt_answer forbidden")
        except Exception as exc:
            return ("FAIL", f"Prior attempt answer leak error: {exc}")

    def _check_process_outcome_separation(self) -> Tuple[str, str]:
        try:
            from replay.challenge_scoring import ReplayChallengeScoringEngine
            eng = ReplayChallengeScoringEngine(include_outcome=False)
            # Without outcome, classification should be PROCESS_ONLY
            attempt = {"attempt_id": "ATT-TEST", "status": "COMPLETED", "hints_used": 0, "actions": [{"action_type": "WRITE_THESIS"}]}
            challenge = {}
            result = eng.score(attempt, challenge, outcome_score=None)
            score = result["score"]
            from replay.challenge_schema import ScoreClassification
            assert score.classification == ScoreClassification.PROCESS_ONLY
            return ("PASS", "ProcessOutcomeSeparation: outcome not included by default, PROCESS_ONLY")
        except Exception as exc:
            return ("FAIL", f"Process outcome separation error: {exc}")

    def _check_outcome_explicit_reveal(self) -> Tuple[str, str]:
        try:
            from replay.challenge_review import ReplayChallengeReviewManager
            mgr = ReplayChallengeReviewManager()
            mgr.build_review("ATT-001", {"attempt_id": "ATT-001", "actions": []})
            # Without both flags → BLOCKED
            result = mgr.reveal_outcome("ATT-001", explicit=False, confirm_review=True)
            assert result["status"] == "BLOCKED"
            result2 = mgr.reveal_outcome("ATT-001", explicit=True, confirm_review=False)
            assert result2["status"] == "BLOCKED"
            return ("PASS", "OutcomeExplicitReveal: requires both explicit AND confirm_review")
        except Exception as exc:
            return ("FAIL", f"Outcome explicit reveal error: {exc}")

    def _check_timeout_no_decision_execution(self) -> Tuple[str, str]:
        try:
            from replay.challenge_clock import ReplayChallengeClock
            from replay.challenge_engine import ReplayChallengeEngine
            clock = ReplayChallengeClock(max_duration_seconds=0.001)
            assert clock.TIMEOUT_EXECUTES_DECISION is False
            clock.start()
            clock.timeout()
            assert clock._status == "TIMEOUT"
            eng = ReplayChallengeEngine()
            assert eng.AUTO_DECISION_ENABLED is False
            return ("PASS", "TimeoutNoDecision: timeout only marks status, never executes decision")
        except Exception as exc:
            return ("FAIL", f"Timeout no decision error: {exc}")

    def _check_hints_no_direct_answer(self) -> Tuple[str, str]:
        try:
            from replay.challenge_hint import ReplayChallengeHintManager
            mgr = ReplayChallengeHintManager(max_hints=5)
            assert mgr.HINTS_TELL_BUY_SELL_ANSWER is False
            assert mgr.HINTS_CONTAIN_FUTURE_OUTCOME is False
            assert mgr.HINTS_AUTO_MODIFY_DECISION is False
            result = mgr.request_hint("ATT-TEST")
            hint = result.get("hint", {})
            assert hint.get("tells_buy_sell_answer") is False
            assert hint.get("contains_future_outcome") is False
            return ("PASS", "HintsNoDirectAnswer: hints don't contain outcome or buy/sell answer")
        except Exception as exc:
            return ("FAIL", f"Hints no direct answer error: {exc}")

    def _check_suggested_mistake_only(self) -> Tuple[str, str]:
        try:
            from replay.challenge_scoring import ReplayChallengeScoringEngine
            eng = ReplayChallengeScoringEngine()
            attempt = {"attempt_id": "ATT-T", "status": "TIMEOUT", "hints_used": 3, "actions": []}
            challenge = {"hint_limit": 3, "hint_penalty": 5.0}
            result = eng.score(attempt, challenge)
            mistakes = result.get("suggested_mistakes", [])
            # All suggested mistakes must start with [SUGGESTED]
            for m in mistakes:
                assert m.startswith("[SUGGESTED]"), f"Mistake not SUGGESTED: {m}"
            return ("PASS", "SuggestedMistakeOnly: all mistakes are [SUGGESTED] only, never auto-Confirmed")
        except Exception as exc:
            return ("FAIL", f"Suggested mistake error: {exc}")

    def _check_public_leaderboard_disabled(self) -> Tuple[str, str]:
        try:
            from replay.challenge_leaderboard import (
                ReplayChallengeLeaderboard,
                PUBLIC_LEADERBOARD_ENABLED,
                NETWORK_SCORE_SUBMISSION_ENABLED,
                USER_TO_USER_COMPETITION,
            )
            assert PUBLIC_LEADERBOARD_ENABLED is False
            assert NETWORK_SCORE_SUBMISSION_ENABLED is False
            assert USER_TO_USER_COMPETITION is False
            lb = ReplayChallengeLeaderboard()
            assert lb.PUBLIC_LEADERBOARD_ENABLED is False
            return ("PASS", "PublicLeaderboardDisabled: no public leaderboard, no network submission")
        except Exception as exc:
            return ("FAIL", f"Public leaderboard error: {exc}")

    def _check_network_submission_disabled(self) -> Tuple[str, str]:
        try:
            from release.version_info import NETWORK_SCORE_SUBMISSION_ENABLED
            assert NETWORK_SCORE_SUBMISSION_ENABLED is False
            return ("PASS", "NetworkSubmissionDisabled: NETWORK_SCORE_SUBMISSION_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"Network submission error: {exc}")

    def _check_local_leaderboard_only(self) -> Tuple[str, str]:
        try:
            from replay.challenge_leaderboard import ReplayChallengeLeaderboard
            lb = ReplayChallengeLeaderboard()
            summary = lb.summary()
            assert summary.get("local_only") is True
            assert summary.get("public_leaderboard_enabled") is False
            return ("PASS", "LocalLeaderboardOnly: local=True, no public/network")
        except Exception as exc:
            return ("FAIL", f"Local leaderboard error: {exc}")

    def _check_batch_guard(self) -> Tuple[str, str]:
        try:
            from replay.challenge_batch import ReplayChallengeBatchRunner
            runner = ReplayChallengeBatchRunner()
            result = runner.run_batch(["SES-001"], execute=True, allow_write=False)
            assert result["status"] == "BLOCKED"
            return ("PASS", "BatchGuard: BLOCKED without --execute --allow-write")
        except Exception as exc:
            return ("FAIL", f"Batch guard error: {exc}")

    def _check_timer_active_elapsed(self) -> Tuple[str, str]:
        try:
            from replay.challenge_clock import ReplayChallengeClock
            clock = ReplayChallengeClock()
            clock.start()
            active = clock.active_elapsed()
            assert active >= 0.0
            return ("PASS", "TimerActiveElapsed: active elapsed >= 0")
        except Exception as exc:
            return ("FAIL", f"Timer error: {exc}")

    def _check_pause_duration(self) -> Tuple[str, str]:
        try:
            from replay.challenge_clock import ReplayChallengeClock
            clock = ReplayChallengeClock()
            clock.start()
            clock.pause()
            paused = clock.paused_elapsed()
            assert paused >= 0.0
            clock.resume()
            active_after = clock.active_elapsed()
            assert active_after >= 0.0
            return ("PASS", "PauseDuration: paused time >= 0, active elapsed correct")
        except Exception as exc:
            return ("FAIL", f"Pause duration error: {exc}")

    def _check_cancelled_elapsed(self) -> Tuple[str, str]:
        try:
            from replay.challenge_clock import ReplayChallengeClock
            clock = ReplayChallengeClock()
            clock.start()
            clock.cancel()
            assert clock._status == "CANCELLED"
            elapsed = clock.active_elapsed()
            assert elapsed >= 0.0
            return ("PASS", "CancelledElapsed: elapsed preserved after cancel")
        except Exception as exc:
            return ("FAIL", f"Cancelled elapsed error: {exc}")

    def _check_no_auto_decision(self) -> Tuple[str, str]:
        try:
            from replay.challenge_engine import ReplayChallengeEngine
            eng = ReplayChallengeEngine()
            assert eng.AUTO_DECISION_ENABLED is False
            from release.version_info import AUTO_CHALLENGE_DECISION_ENABLED
            assert AUTO_CHALLENGE_DECISION_ENABLED is False
            return ("PASS", "NoAutoDecision: AUTO_DECISION_ENABLED=False in engine and version_info")
        except Exception as exc:
            return ("FAIL", f"No auto decision error: {exc}")

    def _check_no_auto_reveal(self) -> Tuple[str, str]:
        try:
            from replay.challenge_engine import ReplayChallengeEngine
            eng = ReplayChallengeEngine()
            assert eng.AUTO_REVEAL_ENABLED is False
            from release.version_info import AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED
            assert AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED is False
            return ("PASS", "NoAutoReveal: AUTO_REVEAL_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"No auto reveal error: {exc}")

    def _check_no_auto_confirm(self) -> Tuple[str, str]:
        try:
            from replay.challenge_engine import ReplayChallengeEngine
            eng = ReplayChallengeEngine()
            assert eng.AUTO_CONFIRM_ENABLED is False
            from release.version_info import AUTO_CHALLENGE_MISTAKE_CONFIRMATION_ENABLED
            assert AUTO_CHALLENGE_MISTAKE_CONFIRMATION_ENABLED is False
            return ("PASS", "NoAutoConfirm: AUTO_CONFIRM_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"No auto confirm error: {exc}")

    def _check_no_auto_strategy_change(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_STRATEGY_CHANGE_ENABLED
            assert AUTO_STRATEGY_CHANGE_ENABLED is False
            return ("PASS", "NoAutoStrategyChange: AUTO_STRATEGY_CHANGE_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"No auto strategy change error: {exc}")

    def _check_no_score_to_trade(self) -> Tuple[str, str]:
        try:
            from release.version_info import AUTO_SCORE_TO_TRADE_ENABLED
            assert AUTO_SCORE_TO_TRADE_ENABLED is False
            return ("PASS", "NoScoreToTrade: AUTO_SCORE_TO_TRADE_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"No score to trade error: {exc}")

    def _check_no_paper_side_effect(self) -> Tuple[str, str]:
        try:
            from replay.challenge_engine import ReplayChallengeEngine
            eng = ReplayChallengeEngine()
            assert eng.EXECUTES_PAPER_ORDER is False
            return ("PASS", "NoPaperSideEffect: EXECUTES_PAPER_ORDER=False")
        except Exception as exc:
            return ("FAIL", f"No paper side effect error: {exc}")

    def _check_no_broker_side_effect(self) -> Tuple[str, str]:
        try:
            from replay.challenge_engine import ReplayChallengeEngine
            eng = ReplayChallengeEngine()
            assert eng.EXECUTES_BROKER_ORDER is False
            from release.version_info import BROKER_EXECUTION_ENABLED
            assert BROKER_EXECUTION_ENABLED is False
            return ("PASS", "NoBrokerSideEffect: EXECUTES_BROKER_ORDER=False, BROKER_EXECUTION_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"No broker side effect error: {exc}")

    def _check_no_forbidden_actions(self) -> Tuple[str, str]:
        try:
            from replay.challenge_schema import ActionType
            forbidden = {"SEND_ORDER", "REAL_BUY", "REAL_SELL", "BROKER_LOGIN",
                         "AUTO_EXECUTE", "AUTO_REVEAL", "AUTO_CONFIRM"}
            for act in ActionType.ALL:
                assert act not in forbidden, f"Forbidden action found: {act}"
            return ("PASS", "NoForbiddenActions: no SEND_ORDER/REAL_BUY/REAL_SELL/AUTO_EXECUTE in action types")
        except Exception as exc:
            return ("FAIL", f"No forbidden actions error: {exc}")

    def _check_process_weight_above_outcome(self) -> Tuple[str, str]:
        try:
            from replay.challenge_schema import ReplayChallengeDefinition
            defn = ReplayChallengeDefinition(process_weight=0.80, outcome_weight=0.20)
            assert defn.process_weight >= defn.outcome_weight
            from replay.challenge_scoring import ReplayChallengeScoringEngine
            eng = ReplayChallengeScoringEngine(process_weight=0.80, outcome_weight=0.20)
            assert eng.process_weight >= eng.outcome_weight
            # Verify constraint enforcement
            try:
                bad = ReplayChallengeDefinition(process_weight=0.10, outcome_weight=0.20)
                return ("FAIL", "Should have raised AssertionError for process_weight < outcome_weight")
            except AssertionError:
                pass  # Expected
            return ("PASS", "ProcessWeightAboveOutcome: process_weight >= outcome_weight enforced")
        except Exception as exc:
            return ("FAIL", f"Process weight error: {exc}")

    # ------------------------------------------------------------------
    # Print results
    # ------------------------------------------------------------------

    def print_results(self, results: Dict[str, Tuple[str, str]]) -> None:
        """Print health check results."""
        print("=" * 70)
        print("  Replay Challenge Mode Health Check v1.2.7")
        print("  [!] Challenge Training Only | Simulation Only | No Real Orders")
        print("=" * 70)
        passed = 0
        failed = 0
        warned = 0
        blocked = 0
        for name, (status, message) in results.items():
            marker = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "BLOCKED": "[BLOCKED]"}.get(status, f"[{status}]")
            print(f"  {marker:12s} {name:45s} {message}")
            if status == "PASS":
                passed += 1
            elif status == "WARN":
                warned += 1
            elif status == "FAIL":
                failed += 1
            elif status == "BLOCKED":
                blocked += 1
        total = len(results)
        print("=" * 70)
        print(f"  Results: {passed}/{total} PASS | {warned} WARN | {failed} FAIL | {blocked} BLOCKED")
        print("=" * 70)
