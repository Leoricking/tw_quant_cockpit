"""
replay/session_fingerprint.py — ReplaySessionFingerprint v1.2.8

Deterministic fingerprint for replay sessions.
Based on: session_id, dataset info, scenario/challenge ids, replay range,
timeframes, session configuration, seed, PIT policy, future firewall policy.

MUST NOT include: local absolute paths, GUI state, temp timestamps,
cache locations, machine names, usernames.

[!] Research Only. No Real Orders. Session Registry Only. No Broker.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_EXCLUDED_KEYS = {
    "created_at", "updated_at", "archived_at",
    "gui_state", "window_state",
    "cache_path", "cache_dir",
    "machine_name", "username", "hostname",
    "session_fingerprint",  # avoid circularity
}

_FINGERPRINT_KEYS = [
    "session_id",
    "dataset_id",
    "dataset_version",
    "dataset_fingerprint",
    "scenario_id",
    "challenge_id",
    "replay_start",
    "replay_end",
    "primary_timeframe",
    "enabled_timeframes",
    "seed",
    "point_in_time_policy",
    "future_firewall_policy",
    "session_config",
    "mode",
]


class ReplaySessionFingerprint:
    """
    Deterministic fingerprint for replay sessions.

    Same session configuration on any machine => same fingerprint.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def calculate(self, session_config: Dict[str, Any]) -> str:
        """Calculate deterministic session fingerprint."""
        normalized = self._normalize(session_config)
        canonical = json.dumps(normalized, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def verify(self, fingerprint: str, session_config: Dict[str, Any]) -> bool:
        """Return True if computed fingerprint matches."""
        return self.calculate(session_config) == fingerprint

    def compare(self, fp1: str, fp2: str) -> Dict[str, Any]:
        """Compare two fingerprints."""
        return {
            "match": fp1 == fp2,
            "fp1": fp1,
            "fp2": fp2,
        }

    def explain_difference(
        self,
        fp1: str,
        fp2: str,
        config1: Dict[str, Any],
        config2: Dict[str, Any],
    ) -> str:
        """Human-readable explanation of fingerprint difference."""
        if fp1 == fp2:
            return "Session fingerprints are identical."
        n1 = self._normalize(config1)
        n2 = self._normalize(config2)
        lines = ["Session fingerprints differ. Changed fields:"]
        for key in sorted(set(list(n1.keys()) + list(n2.keys()))):
            v1 = n1.get(key)
            v2 = n2.get(key)
            if v1 != v2:
                lines.append(f"  {key}: {v1!r} -> {v2!r}")
        return "\n".join(lines) if len(lines) > 1 else "Difference in sub-fields only."

    # ------------------------------------------------------------------ #

    def _normalize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract only fingerprint-relevant fields, exclude machine-specific data."""
        result: Dict[str, Any] = {}
        for key in _FINGERPRINT_KEYS:
            if key in config:
                val = config[key]
                if isinstance(val, list):
                    val = sorted(val)
                result[key] = val
        # also include any extra non-excluded keys
        for k, v in config.items():
            if k not in _EXCLUDED_KEYS and k not in result:
                if isinstance(v, str) and (":\\") in v:
                    continue  # skip Windows absolute paths
                if isinstance(v, str) and v.startswith("/"):
                    continue  # skip Unix absolute paths
                result[k] = v
        return result
