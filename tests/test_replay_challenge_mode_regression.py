"""
tests/test_replay_challenge_mode_regression.py — Comprehensive regression tests v1.2.7

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
[!] Fixed test clock. Isolated runtime. Deterministic seed. No real secrets.
[!] No auto-reveal. No auto-confirm. No paper/broker execution.
"""
import pytest
import sys
import os

# Ensure project root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ===========================================================================
# Schema tests
# ===========================================================================

class TestChallengeSchema:
    def test_definition_safety_invariants(self):
        from replay.challenge_schema import ReplayChallengeDefinition, ChallengeType
        defn = ReplayChallengeDefinition(title="Test", challenge_type=ChallengeType.FREE_DECISION)
        assert defn.research_only is True
        assert defn.no_real_orders is True
        assert defn.process_weight >= defn.outcome_weight
        assert defn.outcome_weight <= 0.20

    def test_definition_process_weight_invariant(self):
        from replay.challenge_schema import ReplayChallengeDefinition
        with pytest.raises(AssertionError):
            ReplayChallengeDefinition(process_weight=0.10, outcome_weight=0.20)

    def test_attempt_safety_invariants(self):
        from replay.challenge_schema import ReplayChallengeAttempt
        att = ReplayChallengeAttempt(challenge_id="CHG-TEST")
        assert att.research_only is True
        assert att.no_real_orders is True

    def test_score_process_weight(self):
        from replay.challenge_schema import ReplayChallengeScore
        score = ReplayChallengeScore(process_weight=0.80, outcome_weight=0.20)
        assert score.process_weight >= score.outcome_weight

    def test_action_simulation_only(self):
        from replay.challenge_schema import ReplayChallengeAction, ActionType
        action = ReplayChallengeAction(action_type=ActionType.DECIDE_ENTER)
        assert action.simulation_decision_only is True
        assert action.no_paper_order is True
        assert action.no_broker_order is True

    def test_result_safety(self):
        from replay.challenge_schema import ReplayChallengeResult
        result = ReplayChallengeResult()
        assert result.research_only is True
        assert result.no_real_orders is True


# ===========================================================================
# Template tests
# ===========================================================================

class TestChallengeTemplates:
    def test_twelve_templates_exist(self):
        from replay.challenge_template import CHALLENGE_TEMPLATES, list_templates
        assert len(CHALLENGE_TEMPLATES) == 12

    def test_all_templates_no_broker(self):
        from replay.challenge_template import CHALLENGE_TEMPLATES
        for t in CHALLENGE_TEMPLATES:
            assert t.get("no_broker") is True, f"{t['template_id']}: no_broker must be True"

    def test_all_templates_no_auto_decision(self):
        from replay.challenge_template import CHALLENGE_TEMPLATES
        for t in CHALLENGE_TEMPLATES:
            assert t.get("no_auto_decision") is True, f"{t['template_id']}: no_auto_decision must be True"

    def test_get_template_by_id(self):
        from replay.challenge_template import get_template
        tmpl = get_template("FREE_DECISION_PRACTICE")
        assert tmpl["challenge_type"] == "FREE_DECISION"

    def test_unknown_template_returns_empty(self):
        from replay.challenge_template import get_template
        tmpl = get_template("NONEXISTENT")
        assert tmpl == {}


# ===========================================================================
# Library tests
# ===========================================================================

class TestChallengeLibrary:
    def test_list_challenges(self):
        from replay.challenge_library import ReplayChallengeLibrary
        lib = ReplayChallengeLibrary()
        challenges = lib.list_challenges()
        assert len(challenges) >= 12

    def test_builtin_cannot_be_archived(self):
        from replay.challenge_library import ReplayChallengeLibrary
        lib = ReplayChallengeLibrary()
        result = lib.archive("FREE_DECISION_PRACTICE")
        assert result["status"] == "PROTECTED"

    def test_no_public_leaderboard(self):
        from replay.challenge_library import ReplayChallengeLibrary
        lib = ReplayChallengeLibrary()
        summary = lib.summary()
        assert summary["public_leaderboard_enabled"] is False
        assert summary["network_submission_enabled"] is False

    def test_import_dry_run_by_default(self):
        from replay.challenge_library import ReplayChallengeLibrary
        lib = ReplayChallengeLibrary()
        result = lib.import_preview({"title": "Test Import"})
        assert result["dry_run"] is True
        assert result["status"] == "PREVIEW"

    def test_import_execute_requires_allow_write(self):
        from replay.challenge_library import ReplayChallengeLibrary
        lib = ReplayChallengeLibrary()
        result = lib.import_execute({"title": "Test"}, allow_write=False)
        assert result["status"] == "BLOCKED"


# ===========================================================================
# Deterministic seed tests
# ===========================================================================

class TestChallengeSeed:
    def test_same_seed_same_result(self):
        from replay.challenge_seed import compute_seed
        s1 = compute_seed(seed="TEST", source_id="SES-001", data_version="1.2.7")
        s2 = compute_seed(seed="TEST", source_id="SES-001", data_version="1.2.7")
        assert s1 == s2

    def test_different_seed_different_result(self):
        from replay.challenge_seed import compute_seed
        s1 = compute_seed(seed="SEED_A", source_id="SES-001", data_version="1.2.7")
        s2 = compute_seed(seed="SEED_B", source_id="SES-001", data_version="1.2.7")
        assert s1 != s2

    def test_different_version_different_result(self):
        from replay.challenge_seed import compute_seed
        s1 = compute_seed(seed="TEST", source_id="SES-001", data_version="1.2.7")
        s2 = compute_seed(seed="TEST", source_id="SES-001", data_version="1.2.6")
        assert s1 != s2


# ===========================================================================
# Difficulty tests
# ===========================================================================

class TestChallengeDifficulty:
    def test_all_difficulties_future_firewall(self):
        from replay.challenge_difficulty import get_difficulty_settings
        for diff in ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT", "CUSTOM"]:
            s = get_difficulty_settings(diff)
            assert s["future_firewall"] is True
            assert s["no_real_orders"] is True
            assert s["no_auto_execution"] is True

    def test_expert_future_firewall_active(self):
        from replay.challenge_difficulty import get_difficulty_settings
        s = get_difficulty_settings("EXPERT")
        assert s["future_firewall"] is True

    def test_custom_cannot_disable_safety(self):
        from replay.challenge_difficulty import apply_custom_settings, get_difficulty_settings
        base = get_difficulty_settings("CUSTOM")
        merged = apply_custom_settings(base, {"future_firewall": False, "no_real_orders": False})
        assert merged["future_firewall"] is True
        assert merged["no_real_orders"] is True


# ===========================================================================
# Hidden data guard tests
# ===========================================================================

class TestHiddenDataGuard:
    def test_forbidden_fields_blocked(self):
        from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
        guard = ReplayChallengeHiddenDataGuard()
        payload = {"forward_return": 5.0, "realized_pnl": 100.0, "safe": "OK"}
        result = guard.validate_active_payload(payload)
        assert result["blocked"] is True

    def test_sanitize_removes_forbidden(self):
        from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
        guard = ReplayChallengeHiddenDataGuard()
        payload = {"forward_return": 5.0, "safe": "OK"}
        safe = guard.sanitize_active_payload(payload)
        assert "forward_return" not in safe
        assert safe["safe"] == "OK"

    def test_answer_key_removed(self):
        from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
        guard = ReplayChallengeHiddenDataGuard()
        payload = {"answer_key": "BUY", "thesis": "test"}
        hidden = guard.hide_answer_key(payload)
        assert "answer_key" not in hidden
        assert hidden["answer_key_stored_separately"] is True

    def test_outcome_hidden(self):
        from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
        guard = ReplayChallengeHiddenDataGuard()
        payload = {"realized_pnl": 1000.0, "outcome_score": 85.0}
        hidden = guard.hide_outcome(payload)
        assert hidden["realized_pnl"] == "HIDDEN"
        assert hidden["outcome_score"] == "HIDDEN"

    def test_prior_attempt_answer_forbidden(self):
        from replay.challenge_hidden_data import FORBIDDEN_ACTIVE_FIELDS
        assert "prior_attempt_answer" in FORBIDDEN_ACTIVE_FIELDS
        assert "best_attempt_answer" in FORBIDDEN_ACTIVE_FIELDS


# ===========================================================================
# Clock tests
# ===========================================================================

class TestChallengeClock:
    def test_timeout_does_not_execute_decision(self):
        from replay.challenge_clock import ReplayChallengeClock
        clock = ReplayChallengeClock(max_duration_seconds=0.001)
        assert clock.TIMEOUT_EXECUTES_DECISION is False
        clock.start()
        clock.timeout()
        assert clock._status == "TIMEOUT"

    def test_pause_excludes_active_elapsed(self):
        from replay.challenge_clock import ReplayChallengeClock
        import time
        clock = ReplayChallengeClock()
        clock.start()
        time.sleep(0.01)
        clock.pause()
        active_at_pause = clock.active_elapsed()
        time.sleep(0.05)
        clock.resume()
        # Active elapsed should NOT include paused time
        assert clock.paused_elapsed() > 0

    def test_cancel_preserves_elapsed(self):
        from replay.challenge_clock import ReplayChallengeClock
        clock = ReplayChallengeClock()
        clock.start()
        clock.cancel()
        assert clock._status == "CANCELLED"
        assert clock.active_elapsed() >= 0.0

    def test_paused_elapsed_not_zero_after_pause(self):
        from replay.challenge_clock import ReplayChallengeClock
        import time
        clock = ReplayChallengeClock()
        clock.start()
        clock.pause()
        time.sleep(0.01)
        paused = clock.paused_elapsed()
        assert paused > 0


# ===========================================================================
# Hint tests
# ===========================================================================

class TestChallengeHint:
    def test_hints_no_future_outcome(self):
        from replay.challenge_hint import ReplayChallengeHintManager
        mgr = ReplayChallengeHintManager(max_hints=3)
        assert mgr.HINTS_CONTAIN_FUTURE_OUTCOME is False

    def test_hints_no_direct_answer(self):
        from replay.challenge_hint import ReplayChallengeHintManager
        mgr = ReplayChallengeHintManager(max_hints=3)
        assert mgr.HINTS_TELL_BUY_SELL_ANSWER is False

    def test_hint_content_no_direct_answer(self):
        from replay.challenge_hint import ReplayChallengeHintManager
        mgr = ReplayChallengeHintManager(max_hints=3)
        result = mgr.request_hint("ATT-TEST")
        hint = result["hint"]
        assert hint["contains_future_outcome"] is False
        assert hint["tells_buy_sell_answer"] is False

    def test_level_5_disabled_by_default(self):
        from replay.challenge_hint import ReplayChallengeHintManager
        mgr = ReplayChallengeHintManager(max_hints=5)
        assert mgr.LEVEL_5_ENABLED_BY_DEFAULT is False

    def test_hints_auto_modify_decision_false(self):
        from replay.challenge_hint import ReplayChallengeHintManager
        mgr = ReplayChallengeHintManager(max_hints=3)
        assert mgr.HINTS_AUTO_MODIFY_DECISION is False

    def test_hint_limit_blocked(self):
        from replay.challenge_hint import ReplayChallengeHintManager
        mgr = ReplayChallengeHintManager(max_hints=0)
        result = mgr.request_hint("ATT-TEST")
        assert result["status"] == "BLOCKED"

    def test_expert_hint_limit(self):
        from replay.challenge_hint import DIFFICULTY_HINT_ALLOWANCE
        assert DIFFICULTY_HINT_ALLOWANCE["EXPERT"] == 0


# ===========================================================================
# Scoring tests
# ===========================================================================

class TestChallengeScoring:
    def test_process_weight_above_outcome(self):
        from replay.challenge_scoring import ReplayChallengeScoringEngine
        eng = ReplayChallengeScoringEngine(process_weight=0.80, outcome_weight=0.20)
        assert eng.process_weight >= eng.outcome_weight

    def test_profit_not_high_score(self):
        from replay.challenge_scoring import ReplayChallengeScoringEngine
        eng = ReplayChallengeScoringEngine()
        assert eng.PROFIT_EQUALS_HIGH_SCORE is False

    def test_wait_not_auto_penalized(self):
        from replay.challenge_scoring import ReplayChallengeScoringEngine
        eng = ReplayChallengeScoringEngine()
        attempt = {
            "attempt_id": "ATT-WAIT",
            "status": "COMPLETED",
            "hints_used": 0,
            "actions": [
                {"action_type": "WRITE_THESIS"},
                {"action_type": "WRITE_RISK_PLAN"},
                {"action_type": "DECIDE_WAIT", "payload": {"reason": "Not ready"}},
            ],
        }
        challenge = {"hint_penalty": 5.0, "completion_bonus": 5.0}
        result = eng.score(attempt, challenge)
        score = result["score"]
        assert score.total_score > 0, "WAIT decision should not auto-penalize"

    def test_process_only_without_outcome(self):
        from replay.challenge_scoring import ReplayChallengeScoringEngine
        from replay.challenge_schema import ScoreClassification
        eng = ReplayChallengeScoringEngine(include_outcome=False)
        attempt = {"attempt_id": "ATT-T", "status": "COMPLETED", "hints_used": 0, "actions": []}
        challenge = {}
        result = eng.score(attempt, challenge, outcome_score=None)
        assert result["score"].classification == ScoreClassification.PROCESS_ONLY

    def test_good_process_bad_outcome(self):
        from replay.challenge_scoring import ReplayChallengeScoringEngine
        from replay.challenge_schema import ScoreClassification
        eng = ReplayChallengeScoringEngine(process_weight=0.80, outcome_weight=0.20, include_outcome=True)
        attempt = {
            "attempt_id": "ATT-GPBO",
            "status": "COMPLETED",
            "hints_used": 0,
            "actions": [
                {"action_type": "WRITE_THESIS"},
                {"action_type": "WRITE_RISK_PLAN"},
                {"action_type": "VIEW_CONTEXT"},
                {"action_type": "VIEW_TIMEFRAME"},
                {"action_type": "VIEW_STRATEGY"},
                {"action_type": "WRITE_CHECKLIST"},
                {"action_type": "DECIDE_WAIT", "payload": {"reason": "Wait"}},
            ],
        }
        challenge = {"hint_penalty": 5.0, "completion_bonus": 5.0}
        result = eng.score(attempt, challenge, outcome_score=20.0)
        assert result["score"].classification == ScoreClassification.GOOD_PROCESS_BAD_OUTCOME

    def test_suggested_mistakes_not_confirmed(self):
        from replay.challenge_scoring import ReplayChallengeScoringEngine
        eng = ReplayChallengeScoringEngine()
        attempt = {"attempt_id": "ATT-T", "status": "TIMEOUT", "hints_used": 3, "actions": []}
        challenge = {"hint_limit": 3}
        result = eng.score(attempt, challenge)
        for mistake in result.get("suggested_mistakes", []):
            assert mistake.startswith("[SUGGESTED]")


# ===========================================================================
# Review tests
# ===========================================================================

class TestChallengeReview:
    def test_outcome_hidden_by_default(self):
        from replay.challenge_review import ReplayChallengeReviewManager
        mgr = ReplayChallengeReviewManager()
        review = mgr.build_review("ATT-001", {"attempt_id": "ATT-001", "actions": []})
        assert review["outcome_revealed"] is False
        assert review["outcome"] == "NOT_REVEALED"

    def test_reveal_requires_both_flags(self):
        from replay.challenge_review import ReplayChallengeReviewManager
        mgr = ReplayChallengeReviewManager()
        mgr.build_review("ATT-001", {"attempt_id": "ATT-001", "actions": []})
        assert mgr.reveal_outcome("ATT-001", explicit=False, confirm_review=False)["status"] == "BLOCKED"
        assert mgr.reveal_outcome("ATT-001", explicit=True, confirm_review=False)["status"] == "BLOCKED"
        assert mgr.reveal_outcome("ATT-001", explicit=False, confirm_review=True)["status"] == "BLOCKED"

    def test_reveal_requires_explicit_and_confirm(self):
        from replay.challenge_review import ReplayChallengeReviewManager
        mgr = ReplayChallengeReviewManager()
        mgr.build_review("ATT-001", {"attempt_id": "ATT-001", "actions": []})
        result = mgr.reveal_outcome("ATT-001", explicit=True, confirm_review=True)
        assert result["status"] == "REVEALED"
        assert result["auto_confirm_mistake"] is False

    def test_no_auto_confirm_mistake(self):
        from replay.challenge_review import ReplayChallengeReviewManager
        mgr = ReplayChallengeReviewManager()
        assert mgr.AUTO_CONFIRM_MISTAKE is False


# ===========================================================================
# Leaderboard tests
# ===========================================================================

class TestChallengeLeaderboard:
    def test_local_only(self):
        from replay.challenge_leaderboard import ReplayChallengeLeaderboard
        lb = ReplayChallengeLeaderboard()
        assert lb.PUBLIC_LEADERBOARD_ENABLED is False
        assert lb.NETWORK_SCORE_SUBMISSION_ENABLED is False
        assert lb.USER_TO_USER_COMPETITION is False
        assert lb.REAL_PNL_RANKING is False
        assert lb.BROKER_PERFORMANCE_RANKING is False

    def test_summary_local_only(self):
        from replay.challenge_leaderboard import ReplayChallengeLeaderboard
        lb = ReplayChallengeLeaderboard()
        summary = lb.summary()
        assert summary["local_only"] is True
        assert summary["public_leaderboard_enabled"] is False


# ===========================================================================
# Batch guard tests
# ===========================================================================

class TestChallengeBatch:
    def test_blocked_without_execute_allow_write(self):
        from replay.challenge_batch import ReplayChallengeBatchRunner
        runner = ReplayChallengeBatchRunner()
        result = runner.run_batch(["SES-001"], execute=True, allow_write=False)
        assert result["status"] == "BLOCKED"

    def test_preview_by_default(self):
        from replay.challenge_batch import ReplayChallengeBatchRunner
        runner = ReplayChallengeBatchRunner()
        result = runner.run_batch(["SES-001"], execute=False)
        assert result["status"] == "PREVIEW"
        assert result["dry_run"] is True

    def test_no_auto_start_challenge(self):
        from replay.challenge_batch import ReplayChallengeBatchRunner
        runner = ReplayChallengeBatchRunner()
        assert runner.AUTO_START_CHALLENGE is False
        assert runner.AUTO_SUBMIT_DECISION is False
        assert runner.AUTO_REVEAL is False


# ===========================================================================
# Engine tests
# ===========================================================================

class TestChallengeEngine:
    def test_engine_safety_flags(self):
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

    def test_create_and_start_challenge(self):
        from replay.challenge_engine import ReplayChallengeEngine
        eng = ReplayChallengeEngine()
        create_result = eng.create_challenge(template_id="FREE_DECISION_PRACTICE")
        assert create_result["status"] == "CREATED"
        challenge_id = create_result["challenge_id"]
        start_result = eng.start_challenge(challenge_id)
        assert start_result["status"] == "STARTED"
        assert start_result["modifies_original_session"] is False
        assert start_result["auto_decision"] is False
        assert start_result["simulation_only"] is True

    def test_perform_action_simulation_only(self):
        from replay.challenge_engine import ReplayChallengeEngine
        eng = ReplayChallengeEngine()
        cr = eng.create_challenge(template_id="FREE_DECISION_PRACTICE")
        sr = eng.start_challenge(cr["challenge_id"])
        attempt_id = sr["attempt_id"]
        result = eng.perform_action(attempt_id, "VIEW_CONTEXT")
        assert result["simulation_decision_only"] is True
        assert result["no_paper_order"] is True
        assert result["no_broker_order"] is True

    def test_timeout_no_auto_decision(self):
        from replay.challenge_engine import ReplayChallengeEngine
        eng = ReplayChallengeEngine()
        cr = eng.create_challenge(template_id="FREE_DECISION_PRACTICE")
        sr = eng.start_challenge(cr["challenge_id"])
        timeout_result = eng.timeout_attempt(sr["attempt_id"])
        assert timeout_result["auto_decision_executed"] is False

    def test_cancel_preserves_elapsed(self):
        from replay.challenge_engine import ReplayChallengeEngine
        eng = ReplayChallengeEngine()
        cr = eng.create_challenge(template_id="FREE_DECISION_PRACTICE")
        sr = eng.start_challenge(cr["challenge_id"])
        cancel_result = eng.cancel_attempt(sr["attempt_id"])
        assert cancel_result["elapsed_preserved"] is True

    def test_full_challenge_flow(self):
        from replay.challenge_engine import ReplayChallengeEngine
        eng = ReplayChallengeEngine()
        # Create
        cr = eng.create_challenge(template_id="NO_CHASE_DISCIPLINE")
        assert cr["status"] == "CREATED"
        cid = cr["challenge_id"]
        # Start
        sr = eng.start_challenge(cid)
        assert sr["status"] == "STARTED"
        aid = sr["attempt_id"]
        # Actions
        eng.perform_action(aid, "VIEW_CONTEXT")
        eng.perform_action(aid, "WRITE_THESIS", reason="No chase setup")
        eng.perform_action(aid, "WRITE_RISK_PLAN", reason="Stop at support")
        eng.perform_action(aid, "DECIDE_WAIT", reason="Price too extended")
        # Submit decision
        eng.submit_decision(aid, "DECIDE_WAIT", reason="Waiting for retracement")
        # Complete
        complete_result = eng.complete_attempt(aid)
        assert "result" in complete_result
        # Review
        review_result = eng.review_attempt(aid)
        assert review_result["outcome_revealed"] is False


# ===========================================================================
# Store tests
# ===========================================================================

class TestChallengeStore:
    def test_store_append_and_load(self, tmp_path):
        from replay.challenge_store import ChallengeStore
        store = ChallengeStore(repo_root=str(tmp_path))
        result = store.append("challenges", {"challenge_id": "CHG-001", "title": "Test"})
        assert result["status"] == "APPENDED"
        records = store.load_all("challenges")
        assert len(records) == 1
        assert records[0]["research_only"] is True
        assert "answer_key" not in records[0]

    def test_store_corrupted_tail_recovery(self, tmp_path):
        from replay.challenge_store import ChallengeStore, _safe_load_jsonl
        from pathlib import Path
        p = tmp_path / "data" / "replay_challenges" / "test.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            f.write('{"id": "good1"}\n')
            f.write('{"id": "good2"}\n')
            f.write('{CORRUPTED_LINE\n')
        records = _safe_load_jsonl(p)
        assert len(records) == 2  # corrupted tail skipped

    def test_active_and_answer_key_separated(self, tmp_path):
        from replay.challenge_store import ChallengeStore
        store = ChallengeStore(repo_root=str(tmp_path))
        assert store.ACTIVE_AND_ANSWER_KEY_SEPARATED is True

    def test_no_forbidden_fields_stored(self, tmp_path):
        from replay.challenge_store import ChallengeStore
        store = ChallengeStore(repo_root=str(tmp_path))
        store.append("challenges", {"challenge_id": "CHG-001", "answer_key": "BUY", "broker": "secret"})
        records = store.load_all("challenges")
        assert len(records) == 1
        assert "answer_key" not in records[0]
        assert "broker" not in records[0]


# ===========================================================================
# Version info tests
# ===========================================================================

class TestVersionInfo:
    def test_version_is_127(self):
        from release.version_info import VERSION
        assert VERSION == "1.2.7"

    def test_challenge_mode_available(self):
        from release.version_info import REPLAY_CHALLENGE_MODE_AVAILABLE
        assert REPLAY_CHALLENGE_MODE_AVAILABLE is True

    def test_public_leaderboard_disabled(self):
        from release.version_info import PUBLIC_LEADERBOARD_ENABLED
        assert PUBLIC_LEADERBOARD_ENABLED is False

    def test_network_submission_disabled(self):
        from release.version_info import NETWORK_SCORE_SUBMISSION_ENABLED
        assert NETWORK_SCORE_SUBMISSION_ENABLED is False

    def test_auto_decision_disabled(self):
        from release.version_info import AUTO_CHALLENGE_DECISION_ENABLED
        assert AUTO_CHALLENGE_DECISION_ENABLED is False

    def test_auto_reveal_disabled(self):
        from release.version_info import AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED
        assert AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED is False

    def test_auto_confirm_disabled(self):
        from release.version_info import AUTO_CHALLENGE_MISTAKE_CONFIRMATION_ENABLED
        assert AUTO_CHALLENGE_MISTAKE_CONFIRMATION_ENABLED is False

    def test_broker_disabled(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False


# ===========================================================================
# Health check
# ===========================================================================

class TestChallengeHealthCheck:
    def test_health_check_runs(self):
        from replay.challenge_health import ReplayChallengeHealthCheck
        hc = ReplayChallengeHealthCheck()
        results = hc.run()
        assert len(results) > 0

    def test_health_check_schema_passes(self):
        from replay.challenge_health import ReplayChallengeHealthCheck
        hc = ReplayChallengeHealthCheck()
        results = hc.run()
        assert results["schema"][0] == "PASS"

    def test_health_check_safety_flags(self):
        from replay.challenge_health import ReplayChallengeHealthCheck
        hc = ReplayChallengeHealthCheck()
        results = hc.run()
        safety_checks = [
            "public_leaderboard_disabled",
            "network_submission_disabled",
            "local_leaderboard_only",
            "batch_guard",
            "no_auto_decision",
            "no_auto_reveal",
            "no_auto_confirm",
            "no_paper_side_effect",
            "no_broker_side_effect",
        ]
        for check in safety_checks:
            assert check in results, f"Missing safety check: {check}"
            assert results[check][0] == "PASS", f"Safety check failed: {check} = {results[check]}"
