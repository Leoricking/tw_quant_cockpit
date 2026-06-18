"""
replay/challenge_engine.py — ReplayChallengeEngine v1.2.7

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
[!] Start creates independent attempt; never modifies original replay session.
[!] Never auto-creates official journal; challenge-local journal draft only.
[!] Export to Decision Journal requires --execute --allow-write.
[!] Challenge actions do NOT execute Paper Order or Broker Order.
[!] No auto-decision. No auto-reveal. No auto-confirm.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
CHALLENGE_TRAINING_ONLY = True
SIMULATION_ONLY = True
AUTO_DECISION_ENABLED = False
AUTO_REVEAL_ENABLED = False
AUTO_CONFIRM_ENABLED = False


class ReplayChallengeEngine:
    """
    Core challenge engine for v1.2.7 Replay Challenge Mode.

    [!] Challenge Training Only. Simulation Only. No Real Orders.
    [!] start_challenge creates an INDEPENDENT attempt.
    [!] Never modifies original replay session.
    [!] Never auto-creates official Decision Journal entries.
    [!] Challenge-local journal draft only.
    [!] Export to Decision Journal requires explicit allow_write=True.
    [!] Challenge actions do NOT execute Paper Order or Broker Order.
    [!] No Public Leaderboard. No Network Submission.
    [!] Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    CHALLENGE_TRAINING_ONLY = True
    SIMULATION_ONLY = True
    AUTO_DECISION_ENABLED = False
    AUTO_REVEAL_ENABLED = False
    AUTO_CONFIRM_ENABLED = False
    MODIFIES_ORIGINAL_REPLAY_SESSION = False
    AUTO_CREATES_OFFICIAL_JOURNAL = False
    EXECUTES_PAPER_ORDER = False
    EXECUTES_BROKER_ORDER = False
    PUBLIC_LEADERBOARD_ENABLED = False
    NETWORK_SUBMISSION_ENABLED = False

    def __init__(self, repo_root: Optional[str] = None) -> None:
        self._repo_root = repo_root or BASE_DIR
        from replay.challenge_library import ReplayChallengeLibrary
        from replay.challenge_attempt import ChallengeAttemptManager
        from replay.challenge_action import ChallengeActionLogManager
        from replay.challenge_clock import ReplayChallengeClock
        from replay.challenge_hint import ReplayChallengeHintManager
        from replay.challenge_scoring import ReplayChallengeScoringEngine
        from replay.challenge_result import ChallengeResultBuilder
        from replay.challenge_review import ReplayChallengeReviewManager
        from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
        from replay.challenge_leaderboard import ReplayChallengeLeaderboard
        from replay.challenge_badges import ChallengeBadgeManager
        from replay.challenge_progress import ReplayChallengeProgressTracker
        from replay.challenge_streak import ReplayChallengeStreakTracker
        from replay.challenge_store import ChallengeStore

        self._library = ReplayChallengeLibrary()
        self._attempt_mgr = ChallengeAttemptManager()
        self._action_log = ChallengeActionLogManager()
        self._scoring = ReplayChallengeScoringEngine()
        self._result_builder = ChallengeResultBuilder()
        self._review_mgr = ReplayChallengeReviewManager()
        self._hidden_guard = ReplayChallengeHiddenDataGuard()
        self._leaderboard = ReplayChallengeLeaderboard()
        self._badge_mgr = ChallengeBadgeManager()
        self._progress = ReplayChallengeProgressTracker()
        self._streak = ReplayChallengeStreakTracker()
        self._store = ChallengeStore(repo_root=self._repo_root)
        self._clocks: Dict[str, ReplayChallengeClock] = {}
        self._hint_managers: Dict[str, ReplayChallengeHintManager] = {}

    # ------------------------------------------------------------------
    # Challenge management
    # ------------------------------------------------------------------

    def create_challenge(
        self,
        template_id: Optional[str] = None,
        definition: Optional[Dict[str, Any]] = None,
        difficulty: str = "INTERMEDIATE",
    ) -> Dict[str, Any]:
        """Create a challenge from a template or custom definition."""
        if template_id:
            from replay.challenge_template import get_template
            tmpl = get_template(template_id)
            if not tmpl:
                return {"status": "NOT_FOUND", "template_id": template_id}
            defn = dict(tmpl)
            defn["difficulty"] = difficulty
        elif definition:
            defn = dict(definition)
        else:
            return {"status": "ERROR", "message": "template_id or definition required"}

        result = self._library.create(defn)
        if result.get("status") == "CREATED":
            self._store.append("challenges", defn)
        return result

    def preview_challenge(self, challenge_id: str) -> Dict[str, Any]:
        """Preview a challenge definition (read-only)."""
        challenge = self._library.show(challenge_id)
        if challenge is None:
            return {"status": "NOT_FOUND", "challenge_id": challenge_id}
        # Sanitize — remove any forbidden fields
        safe = self._hidden_guard.sanitize_active_payload(challenge)
        safe = self._hidden_guard.hide_answer_key(safe)
        return {
            "status": "PREVIEW",
            "challenge": safe,
            "future_data_hidden": True,
            "answer_key_separate": True,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Attempt lifecycle
    # ------------------------------------------------------------------

    def start_challenge(self, challenge_id: str, user_label: str = "") -> Dict[str, Any]:
        """
        Start a challenge — creates an independent attempt.
        NEVER modifies original replay session.
        """
        challenge = self._library.show(challenge_id)
        if challenge is None:
            return {"status": "NOT_FOUND", "challenge_id": challenge_id}

        result = self._attempt_mgr.create(challenge_id, user_label=user_label)
        attempt_id = result["attempt_id"]

        # Set up clock
        from replay.challenge_clock import ReplayChallengeClock
        max_dur = challenge.get("max_duration_seconds") or challenge.get("time_limit")
        clock = ReplayChallengeClock(max_duration_seconds=max_dur)
        clock.start()
        self._clocks[attempt_id] = clock

        # Set up hint manager
        from replay.challenge_hint import ReplayChallengeHintManager
        hint_policy = challenge.get("hint_policy", {})
        max_hints = hint_policy.get("max_hints", challenge.get("hint_limit", 3))
        penalty = hint_policy.get("penalty_per_hint", challenge.get("hint_penalty", 5.0))
        difficulty = challenge.get("difficulty", "INTERMEDIATE")
        self._hint_managers[attempt_id] = ReplayChallengeHintManager(
            max_hints=max_hints,
            penalty_per_hint=penalty,
            difficulty=difficulty,
        )

        # Update attempt state
        attempt = self._attempt_mgr.load(attempt_id)
        from replay.challenge_schema import AttemptStatus, _now_utc
        attempt["status"] = AttemptStatus.RUNNING
        attempt["started_at"] = _now_utc()
        attempt["challenge_type"] = challenge.get("challenge_type", "")
        attempt["difficulty"] = challenge.get("difficulty", "INTERMEDIATE")
        self._attempt_mgr.save(attempt)
        self._store.append("attempts", attempt)

        return {
            "status": "STARTED",
            "attempt_id": attempt_id,
            "challenge_id": challenge_id,
            "modifies_original_session": False,
            "auto_decision": False,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def pause_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Pause an attempt."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND", "attempt_id": attempt_id}
        clock = self._clocks.get(attempt_id)
        if clock:
            clock.pause()
        from replay.challenge_schema import AttemptStatus
        attempt["status"] = AttemptStatus.PAUSED
        attempt["paused_elapsed_seconds"] = clock.paused_elapsed() if clock else 0.0
        self._attempt_mgr.save(attempt)
        return {"status": "PAUSED", "attempt_id": attempt_id}

    def resume_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Resume a paused attempt."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND", "attempt_id": attempt_id}
        clock = self._clocks.get(attempt_id)
        if clock:
            clock.resume()
        from replay.challenge_schema import AttemptStatus
        attempt["status"] = AttemptStatus.RUNNING
        self._attempt_mgr.save(attempt)
        return {"status": "RESUMED", "attempt_id": attempt_id}

    def perform_action(
        self,
        attempt_id: str,
        action_type: str,
        reason: str = "",
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Record a challenge action.
        Trading actions (ENTER/ADD/REDUCE/EXIT) are SIMULATION DECISION ONLY.
        No Paper Order. No Broker Order.
        """
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND", "attempt_id": attempt_id}

        from replay.challenge_schema import ActionType, AttemptStatus
        if attempt.get("status") not in (AttemptStatus.RUNNING,):
            return {"status": "NOT_RUNNING", "attempt_id": attempt_id}

        clock = self._clocks.get(attempt_id)
        elapsed = clock.active_elapsed() if clock else 0.0

        action_payload = payload or {}
        if reason:
            action_payload["reason"] = reason

        action = {
            "attempt_id": attempt_id,
            "action_type": action_type,
            "payload": action_payload,
            "elapsed_since_start": elapsed,
            "simulation_decision_only": True,
            "no_paper_order": True,
            "no_broker_order": True,
        }
        self._action_log.append(attempt_id, action, elapsed=elapsed)

        # Update attempt
        attempt["steps_used"] = attempt.get("steps_used", 0) + 1
        actions = self._action_log.get_log(attempt_id)
        attempt["actions"] = actions
        self._attempt_mgr.save(attempt)

        return {
            "status": "OK",
            "action_type": action_type,
            "elapsed": elapsed,
            "simulation_decision_only": True,
            "no_paper_order": True,
            "no_broker_order": True,
            "research_only": True,
        }

    def request_hint(self, attempt_id: str) -> Dict[str, Any]:
        """Request a hint for an attempt."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        hint_mgr = self._hint_managers.get(attempt_id)
        if hint_mgr is None:
            return {"status": "NO_HINT_MANAGER"}
        result = hint_mgr.request_hint(attempt_id)
        if result.get("status") == "OK":
            attempt["hints_used"] = hint_mgr.hint_history().__len__()
            self._attempt_mgr.save(attempt)
            self._store.append("hints", result.get("hint", {}))
        return result

    def submit_decision(
        self,
        attempt_id: str,
        decision: str,
        reason: str = "",
    ) -> Dict[str, Any]:
        """Submit a final decision (SIMULATION DECISION ONLY)."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        clock = self._clocks.get(attempt_id)
        if clock:
            clock.record_decision()
            attempt["decision_elapsed_seconds"] = clock.decision_elapsed()
        attempt["final_decision"] = decision
        attempt["decision_reason"] = reason
        self._attempt_mgr.save(attempt)
        return {
            "status": "DECISION_RECORDED",
            "attempt_id": attempt_id,
            "decision": decision,
            "simulation_decision_only": True,
            "no_paper_order": True,
            "no_broker_order": True,
            "research_only": True,
        }

    def complete_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Mark attempt as completed and generate result."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        clock = self._clocks.get(attempt_id)
        if clock:
            clock.finish()
            attempt["active_elapsed_seconds"] = clock.active_elapsed()
            attempt["paused_elapsed_seconds"] = clock.paused_elapsed()
        from replay.challenge_schema import AttemptStatus, _now_utc
        attempt["status"] = AttemptStatus.COMPLETED
        attempt["finished_at"] = _now_utc()
        self._attempt_mgr.save(attempt)
        return self.build_result(attempt_id)

    def cancel_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Cancel an attempt. Preserves elapsed time."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        clock = self._clocks.get(attempt_id)
        if clock:
            clock.cancel()
            attempt["active_elapsed_seconds"] = clock.active_elapsed()
            attempt["paused_elapsed_seconds"] = clock.paused_elapsed()
        from replay.challenge_schema import AttemptStatus, _now_utc
        attempt["status"] = AttemptStatus.CANCELLED
        attempt["finished_at"] = _now_utc()
        self._attempt_mgr.save(attempt)
        return {"status": "CANCELLED", "attempt_id": attempt_id, "elapsed_preserved": True}

    def timeout_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Mark attempt as timed out. Does NOT execute decision."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        clock = self._clocks.get(attempt_id)
        if clock:
            clock.timeout()
            attempt["active_elapsed_seconds"] = clock.active_elapsed()
        from replay.challenge_schema import AttemptStatus, _now_utc
        attempt["status"] = AttemptStatus.TIMEOUT
        attempt["finished_at"] = _now_utc()
        self._attempt_mgr.save(attempt)
        return {
            "status": "TIMEOUT",
            "attempt_id": attempt_id,
            "auto_decision_executed": False,
            "research_only": True,
        }

    def build_result(self, attempt_id: str) -> Dict[str, Any]:
        """Build a challenge result for an attempt."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        challenge_id = attempt.get("challenge_id", "")
        challenge = self._library.show(challenge_id) or {}

        hint_mgr = self._hint_managers.get(attempt_id)
        hint_penalty_total = hint_mgr.total_penalty() if hint_mgr else 0.0

        score_result = self._scoring.score(attempt, challenge)
        score_obj = score_result.get("score")
        if score_obj:
            attempt["process_score"] = float(score_obj.process_score)
            attempt["total_score"] = float(score_obj.total_score)

        result = self._result_builder.build_result(
            attempt=attempt,
            challenge=challenge,
            score=score_result,
            suggested_mistakes=score_result.get("suggested_mistakes", []),
        )

        # Awards badges
        total_completed = sum(
            1 for a in self._attempt_mgr.list_attempts()
            if a.get("status") == "COMPLETED" and a.get("attempt_id") != attempt_id
        )
        badges = self._badge_mgr.evaluate(attempt, total_completed=total_completed)
        result["badges_awarded"] = badges

        # Record to leaderboard
        self._leaderboard.record(result, score_result, attempt)

        # Progress and streak
        self._progress.record_attempt(attempt)
        self._streak.record_attempt(attempt)

        # Store
        self._store.append("scores", score_obj.to_dict() if score_obj else {})
        self._store.append("results", result)
        self._attempt_mgr.save(attempt)

        return {
            "status": "OK",
            "attempt_id": attempt_id,
            "result": result,
            "score": score_obj.to_dict() if score_obj else {},
            "badges": badges,
            "research_only": True,
            "no_real_orders": True,
        }

    def review_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Start review for a completed attempt."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        hint_mgr = self._hint_managers.get(attempt_id)
        score_result = None
        challenge_id = attempt.get("challenge_id", "")
        challenge = self._library.show(challenge_id) or {}
        score_result = self._scoring.score(attempt, challenge)
        review = self._review_mgr.build_review(attempt_id, attempt, score_result)
        self._store.append("reviews", review)
        return {
            "status": "REVIEW_STARTED",
            "attempt_id": attempt_id,
            "review": review,
            "outcome_revealed": False,
            "research_only": True,
        }

    def retry_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Create a new attempt from the same challenge."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND"}
        challenge_id = attempt.get("challenge_id", "")
        attempt_number = attempt.get("attempt_number", 1) + 1
        new_result = self._attempt_mgr.create(challenge_id)
        new_attempt = self._attempt_mgr.load(new_result["attempt_id"])
        new_attempt["attempt_number"] = attempt_number
        self._attempt_mgr.save(new_attempt)
        return {"status": "RETRY_CREATED", "new_attempt_id": new_result["attempt_id"]}

    def duplicate_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Duplicate an attempt (for comparison)."""
        return self.retry_attempt(attempt_id)

    def get_attempt(self, attempt_id: str) -> Dict[str, Any]:
        """Get attempt data."""
        attempt = self._attempt_mgr.load(attempt_id)
        if attempt is None:
            return {"status": "NOT_FOUND", "attempt_id": attempt_id}
        clock = self._clocks.get(attempt_id)
        if clock:
            attempt["active_elapsed_seconds"] = clock.active_elapsed()
            attempt["paused_elapsed_seconds"] = clock.paused_elapsed()
            attempt["remaining_seconds"] = clock.remaining_seconds()
        return {"status": "OK", "attempt": attempt, "research_only": True}

    def summary(self) -> Dict[str, Any]:
        """Return engine summary."""
        progress = self._progress.get_summary()
        lb = self._leaderboard.summary()
        badges = self._badge_mgr.summary()
        return {
            "engine": "ReplayChallengeEngine",
            "version": "1.2.7",
            "challenges_in_library": self._library.summary()["total_challenges"],
            "total_attempts": self._attempt_mgr.summary()["total_attempts"],
            "progress": progress,
            "leaderboard": lb,
            "badges": badges,
            "safety": {
                "research_only": True,
                "no_real_orders": True,
                "challenge_training_only": True,
                "simulation_only": True,
                "auto_decision_enabled": False,
                "auto_reveal_enabled": False,
                "auto_confirm_enabled": False,
                "modifies_original_replay_session": False,
                "auto_creates_official_journal": False,
                "executes_paper_order": False,
                "executes_broker_order": False,
                "public_leaderboard_enabled": False,
                "network_submission_enabled": False,
            },
        }
