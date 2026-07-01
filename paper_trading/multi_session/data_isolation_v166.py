"""
paper_trading/multi_session/data_isolation_v166.py — Data Isolation v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Cross-session write contamination count must be 0.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
REQUIRED_CONTAMINATION_COUNT = 0


class SessionIsolationStore:
    """Per-session isolated state store. Shared items must be explicitly declared."""

    ISOLATED_NAMESPACES = [
        "mutable_state",
        "event_cursor",
        "checkpoint",
        "analytics",
        "review",
        "recovery_state",
        "alerts",
        "incidents",
        "reports",
        "temp_store",
    ]

    def __init__(self) -> None:
        self._stores: Dict[str, Dict[str, Any]] = {}
        self._shared: Dict[str, Any] = {}
        self._shared_declarations: set = set()

    def init_session(self, session_id: str) -> None:
        self._stores[session_id] = {ns: {} for ns in self.ISOLATED_NAMESPACES}

    def write(self, session_id: str, namespace: str, key: str, value: Any) -> None:
        if session_id not in self._stores:
            raise KeyError(f"Session {session_id} not initialized")
        if namespace not in self._stores[session_id]:
            raise KeyError(f"Namespace {namespace} not valid")
        self._stores[session_id][namespace][key] = value

    def read(self, session_id: str, namespace: str, key: str) -> Any:
        if session_id not in self._stores:
            raise KeyError(f"Session {session_id} not initialized")
        return self._stores[session_id][namespace].get(key)

    def declare_shared(self, key: str) -> None:
        self._shared_declarations.add(key)

    def write_shared(self, key: str, value: Any) -> None:
        if key not in self._shared_declarations:
            raise ValueError(f"Key '{key}' not declared as shared")
        self._shared[key] = value

    def read_shared(self, key: str) -> Any:
        return self._shared.get(key)

    def detect_cross_session_contamination(
        self,
        session_a: str,
        session_b: str,
    ) -> List[str]:
        """Check that session_a's isolated state does not appear in session_b's store."""
        contamination = []
        store_a = self._stores.get(session_a, {})
        store_b = self._stores.get(session_b, {})
        for ns in self.ISOLATED_NAMESPACES:
            a_keys = set(store_a.get(ns, {}).keys())
            b_keys = set(store_b.get(ns, {}).keys())
            # Cross-check: same key with same value is contamination
            for k in a_keys & b_keys:
                if store_a[ns][k] is store_b[ns][k]:
                    contamination.append(f"{ns}/{k} shared object reference")
        return contamination
