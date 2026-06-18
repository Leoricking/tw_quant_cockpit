"""
replay/challenge_generator.py — ReplayChallengeGenerator v1.2.7

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
[!] Answer key stored separately. Active challenge cannot query answer key directly.
[!] Never embeds future results. Same seed + data version = same challenge.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeGenerator:
    """
    Generate challenge definitions from sessions, scenarios, mistakes, etc.

    [!] Never embeds future results in the active payload.
    [!] Answer key stored separately — active challenge cannot query it directly.
    [!] Deterministic seed: same seed + data version = same challenge.
    [!] Records source session/scenario/snapshot references.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        pass

    def generate_from_session(
        self,
        session_id: str,
        difficulty: str = "INTERMEDIATE",
        seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a challenge from a replay session."""
        from replay.challenge_schema import _new_id, _now_utc, ChallengeType, ChallengeDifficulty
        from replay.challenge_seed import compute_seed
        computed_seed = compute_seed(seed=seed, source_id=session_id)
        return {
            "challenge_id": _new_id("CHG-"),
            "title": f"Session Challenge: {session_id[:12]}",
            "description": f"Challenge generated from session {session_id}",
            "challenge_type": ChallengeType.FREE_DECISION,
            "difficulty": difficulty,
            "source_session_id": session_id,
            "seed": computed_seed,
            "hidden_outcome": True,
            "answer_key_stored_separately": True,
            "future_data_embedded": False,
            "created_at": _now_utc(),
            "research_only": True,
            "no_real_orders": True,
            "process_weight": 0.80,
            "outcome_weight": 0.20,
        }

    def generate_from_scenario(
        self,
        scenario_id: str,
        difficulty: str = "INTERMEDIATE",
        seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a challenge from a scenario."""
        from replay.challenge_schema import _new_id, _now_utc, ChallengeType
        from replay.challenge_seed import compute_seed
        computed_seed = compute_seed(seed=seed, source_id=scenario_id)
        return {
            "challenge_id": _new_id("CHG-"),
            "title": f"Scenario Challenge: {scenario_id[:12]}",
            "description": f"Challenge generated from scenario {scenario_id}",
            "challenge_type": ChallengeType.FREE_DECISION,
            "difficulty": difficulty,
            "source_scenario_id": scenario_id,
            "seed": computed_seed,
            "hidden_outcome": True,
            "answer_key_stored_separately": True,
            "future_data_embedded": False,
            "created_at": _now_utc(),
            "research_only": True,
            "no_real_orders": True,
            "process_weight": 0.80,
            "outcome_weight": 0.20,
        }

    def generate_from_mistake(
        self,
        mistake_id: str,
        difficulty: str = "INTERMEDIATE",
        seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a challenge from a mistake record."""
        from replay.challenge_schema import _new_id, _now_utc, ChallengeType
        from replay.challenge_seed import compute_seed
        computed_seed = compute_seed(seed=seed, source_id=mistake_id)
        return {
            "challenge_id": _new_id("CHG-"),
            "title": f"Mistake Challenge: {mistake_id[:12]}",
            "description": f"Practice correcting mistake pattern {mistake_id}",
            "challenge_type": ChallengeType.MISTAKE_CORRECTION,
            "difficulty": difficulty,
            "source_mistake_id": mistake_id,
            "seed": computed_seed,
            "hidden_outcome": True,
            "original_mistake_conclusion_hidden": True,
            "answer_key_stored_separately": True,
            "future_data_embedded": False,
            "created_at": _now_utc(),
            "research_only": True,
            "no_real_orders": True,
            "process_weight": 0.85,
            "outcome_weight": 0.15,
        }

    def generate_from_strategy_conflict(
        self,
        session_id: str,
        difficulty: str = "ADVANCED",
        seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a strategy conflict challenge."""
        from replay.challenge_schema import _new_id, _now_utc, ChallengeType
        from replay.challenge_seed import compute_seed
        computed_seed = compute_seed(seed=seed, source_id=session_id)
        return {
            "challenge_id": _new_id("CHG-"),
            "title": "Strategy Conflict Challenge",
            "description": "Identify and navigate a strategy signal conflict.",
            "challenge_type": ChallengeType.STRATEGY_CONFLICT,
            "difficulty": difficulty,
            "source_session_id": session_id,
            "seed": computed_seed,
            "hidden_outcome": True,
            "answer_key_stored_separately": True,
            "future_data_embedded": False,
            "created_at": _now_utc(),
            "research_only": True,
            "no_real_orders": True,
            "process_weight": 0.85,
            "outcome_weight": 0.15,
        }

    def generate_from_timeframe_conflict(
        self,
        session_id: str,
        difficulty: str = "ADVANCED",
        seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a timeframe conflict challenge."""
        from replay.challenge_schema import _new_id, _now_utc, ChallengeType
        from replay.challenge_seed import compute_seed
        computed_seed = compute_seed(seed=seed, source_id=session_id)
        return {
            "challenge_id": _new_id("CHG-"),
            "title": "Multi-Timeframe Conflict Challenge",
            "description": "Navigate conflicting signals across timeframes.",
            "challenge_type": ChallengeType.TIMEFRAME_CONFLICT,
            "difficulty": difficulty,
            "source_session_id": session_id,
            "seed": computed_seed,
            "hidden_outcome": True,
            "answer_key_stored_separately": True,
            "future_data_embedded": False,
            "created_at": _now_utc(),
            "research_only": True,
            "no_real_orders": True,
            "process_weight": 0.85,
            "outcome_weight": 0.15,
        }

    def generate_random(
        self,
        challenge_type: Optional[str] = None,
        difficulty: str = "INTERMEDIATE",
        seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a random challenge (mock/demo)."""
        import random
        from replay.challenge_schema import _new_id, _now_utc, ChallengeType
        from replay.challenge_seed import compute_seed
        ctype = challenge_type or random.choice(ChallengeType.ALL)
        computed_seed = compute_seed(seed=seed, source_id=ctype)
        return {
            "challenge_id": _new_id("CHG-"),
            "title": f"Random {ctype} Challenge",
            "description": f"Randomly generated {ctype} challenge",
            "challenge_type": ctype,
            "difficulty": difficulty,
            "seed": computed_seed,
            "hidden_outcome": True,
            "answer_key_stored_separately": True,
            "future_data_embedded": False,
            "created_at": _now_utc(),
            "research_only": True,
            "no_real_orders": True,
            "process_weight": 0.80,
            "outcome_weight": 0.20,
        }

    def preview(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Preview a generated challenge definition (read-only)."""
        return {
            "status": "PREVIEW",
            "challenge_id": definition.get("challenge_id", "PENDING"),
            "title": definition.get("title", ""),
            "challenge_type": definition.get("challenge_type", ""),
            "difficulty": definition.get("difficulty", ""),
            "seed": definition.get("seed", ""),
            "hidden_outcome": definition.get("hidden_outcome", True),
            "future_data_embedded": definition.get("future_data_embedded", False),
            "answer_key_stored_separately": definition.get("answer_key_stored_separately", True),
            "research_only": True,
            "no_real_orders": True,
        }

    def validate(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a generated challenge definition."""
        errors = []
        if not definition.get("title"):
            errors.append("title required")
        if not definition.get("challenge_type"):
            errors.append("challenge_type required")
        if not definition.get("hidden_outcome", True):
            errors.append("hidden_outcome must be True")
        if definition.get("future_data_embedded", False):
            errors.append("future_data_embedded must be False")
        if not definition.get("research_only", True):
            errors.append("research_only must be True")
        if definition.get("no_real_orders") is False:
            errors.append("no_real_orders must be True")
        return {"valid": len(errors) == 0, "errors": errors}

    def estimate_difficulty(self, definition: Dict[str, Any]) -> str:
        """Estimate difficulty from definition parameters."""
        tl = definition.get("max_duration_seconds")
        hints = definition.get("hint_limit", 3)
        if tl is None and hints >= 5:
            return "BEGINNER"
        if tl is not None and tl <= 300 and hints == 0:
            return "EXPERT"
        if tl is not None and tl <= 600 and hints <= 1:
            return "ADVANCED"
        if hints <= 2:
            return "INTERMEDIATE"
        return "BEGINNER"

    def build_definition(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Build a challenge definition from parameters."""
        from replay.challenge_schema import _new_id, _now_utc
        return {
            "challenge_id": params.get("challenge_id") or _new_id("CHG-"),
            "title": params.get("title", "Custom Challenge"),
            "description": params.get("description", ""),
            "challenge_type": params.get("challenge_type", "FREE_DECISION"),
            "difficulty": params.get("difficulty", "INTERMEDIATE"),
            "hidden_outcome": True,
            "answer_key_stored_separately": True,
            "future_data_embedded": False,
            "created_at": _now_utc(),
            "research_only": True,
            "no_real_orders": True,
            "process_weight": params.get("process_weight", 0.80),
            "outcome_weight": params.get("outcome_weight", 0.20),
        }
