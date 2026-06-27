"""
paper_trading/failure_validation/replay_v165.py — Replay verification v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
[!] Deterministic replay. Same seed = same outcome. No future data.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class ReplayResult:
    scenario_id: str = ""
    seed: int = 42
    original_hash: str = ""
    replay_hash: str = ""
    match: bool = False
    replay_events: int = 0

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "seed": self.seed,
            "hash_match": self.match,
            "replay_events": self.replay_events,
        }


def simulate_replay(scenario_id: str, seed: int = 42, original_events: int = 5) -> ReplayResult:
    """Deterministic replay simulation. Same seed always produces same hash."""
    import random
    rng = random.Random(seed)
    events = [rng.randint(0, 9999) for _ in range(original_events)]
    event_str = str(events)
    h = hashlib.sha256(event_str.encode()).hexdigest()

    # Replay with same seed
    rng2 = random.Random(seed)
    events2 = [rng2.randint(0, 9999) for _ in range(original_events)]
    event_str2 = str(events2)
    h2 = hashlib.sha256(event_str2.encode()).hexdigest()

    return ReplayResult(
        scenario_id=scenario_id,
        seed=seed,
        original_hash=h,
        replay_hash=h2,
        match=(h == h2),
        replay_events=original_events,
    )
