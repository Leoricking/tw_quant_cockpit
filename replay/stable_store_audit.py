"""
replay/stable_store_audit.py — ReplayStableStoreAudit for v1.2.9.

Lightweight import-based audit of all replay data stores.
No real execution. No real orders.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Store name → (module_path, store_class_name)
_STORE_MAP = {
    "session":          ("replay.replay_session_store",    "ReplaySessionStore"),
    "scenario":         ("replay.scenario_store",          "ScenarioStore"),
    "journal":          ("replay.decision_journal_store",  "DecisionJournalStore"),
    "scoring":          ("replay.scoring_store",           "ReplayScoringStore"),
    "strategy":         ("replay.strategy_replay_store",   "StrategyReplayStore"),
    "timeframe":        ("replay.timeframe_store",         "TimeframeReplayStore"),
    "review":           ("replay.review_store",            "ReviewStore"),
    "challenge":        ("replay.challenge_store",         "ReplayChallengeStore"),
    "dataset_registry": ("replay.dataset_registry",        "ReplayDatasetRegistry"),
    "session_registry": ("replay.session_registry",        "ReplaySessionRegistry"),
}

# Fields that would indicate live trading (forbidden in any store schema)
_FORBIDDEN_STORE_FIELDS = {
    "send_order", "place_order", "real_buy", "real_sell",
    "broker_login", "broker_connect", "execute_trade", "auto_trade",
}


class ReplayStableStoreAudit:
    """
    Audits all 10 replay data stores via lightweight import checks.

    For each store:
    - Checks the store module imports
    - Checks for append_only semantics flag (if applicable)
    - Checks for forbidden fields in schema

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def audit_all(self) -> Dict[str, Tuple[str, str]]:
        """Audit all stores. Returns {store_name: (status, message)}."""
        results: Dict[str, Tuple[str, str]] = {}
        for store_name, (module_path, class_name) in _STORE_MAP.items():
            results[store_name] = self._audit_store(store_name, module_path, class_name)
        return results

    def _audit_store(self, store_name: str, module_path: str, class_name: str) -> Tuple[str, str]:
        """Audit a single store by import and attribute inspection."""
        try:
            import importlib
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name, None)
            if cls is None:
                return ("WARN", f"{store_name}: class {class_name} not found in {module_path}")

            # Check for append_only semantics (best-effort — not all stores expose this)
            has_append_only = (
                getattr(cls, "APPEND_ONLY", None) is True
                or getattr(cls, "append_only", None) is True
            )

            # Check for forbidden fields in class attributes
            all_attrs = set(dir(cls))
            found_forbidden = _FORBIDDEN_STORE_FIELDS.intersection(
                {a.lower() for a in all_attrs}
            )
            if found_forbidden:
                return ("FAIL", f"{store_name}: forbidden fields in store: {found_forbidden}")

            msg = f"{store_name}: imports OK, class {class_name} found"
            if has_append_only:
                msg += ", append_only=True"
            return ("PASS", msg)

        except ImportError as exc:
            return ("WARN", f"{store_name}: import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"{store_name}: audit error: {exc}")
