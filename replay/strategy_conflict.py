"""
replay/strategy_conflict.py — Conflict analyzer for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Conflict detection NEVER auto-blocks a Decision.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
CONFLICT_NEVER_AUTO_BLOCKS_DECISION = True


class StrategyConflictAnalyzer:
    """
    Detects conflicts between strategy module signals.
    NEVER auto-blocks a Decision — conflicts are informational only.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    CONFLICT_NEVER_AUTO_BLOCKS_DECISION = True

    CONFLICT_TYPES = [
        "TECHNICAL_BULLISH_FUNDAMENTAL_WARNING",
        "BREAKOUT_WITH_NO_CHASE_WARNING",
        "BOTTOM_REVERSAL_WITH_SPECULATIVE_WARNING",
        "SECTOR_SUPPORT_WITH_KD_HIGH_DEATH_CROSS",
        "SHORT_SQUEEZE_WITH_WEAK_PRICE_STRUCTURE",
        "ABC_BUY_POINT_WITH_FUNDAMENTAL_WARNING",
        "ABC_BUY_POINT_WITH_NO_CHASE_WARNING",
        "PANIC_SELL_WARNING_WITH_SUPPORT_PRESENT",
        "REBUY_SIGNAL_WITH_DO_NOT_REBUY_YET",
        "DATA_QUALITY_CONFLICT",
        "TIMING_APPROXIMATE_CONFLICT",
        "UNKNOWN",
    ]

    def detect(self, snapshot) -> List[Dict[str, Any]]:
        """
        Returns list of detected conflicts.
        NEVER blocks Decision automatically.
        """
        snap_dict = snapshot.to_dict() if hasattr(snapshot, "to_dict") else snapshot
        modules: Dict[str, Dict] = {}
        for mod in snap_dict.get("modules", []):
            modules[mod.get("module_name", "")] = mod

        conflicts = []

        def get_signal(name: str) -> str:
            return str(modules.get(name, {}).get("signal", "")).lower()

        def is_available(name: str) -> bool:
            return bool(modules.get(name, {}).get("available", False))

        def has_warning(name: str) -> bool:
            return bool(modules.get(name, {}).get("warning", ""))

        # KD bullish + FUNDAMENTAL warning
        if (is_available("KD_ADVANCED") and is_available("FUNDAMENTAL_QUALITY")
                and "cross" in get_signal("KD_ADVANCED")
                and ("warning" in get_signal("FUNDAMENTAL_QUALITY")
                     or "negative" in get_signal("FUNDAMENTAL_QUALITY"))):
            conflicts.append(self._build(
                "TECHNICAL_BULLISH_FUNDAMENTAL_WARNING",
                "KD_ADVANCED", get_signal("KD_ADVANCED"),
                "FUNDAMENTAL_QUALITY", get_signal("FUNDAMENTAL_QUALITY"),
                snap_dict,
            ))

        # Bullish signal with NO_CHASE warning
        if (is_available("NO_CHASE") and "chase_warning" in get_signal("NO_CHASE")
                and (("kd_advanced" in [m.lower() for m in snap_dict.get("bullish_modules", [])])
                     or any(is_available(m) and ("cross" in get_signal(m) or "valid" in get_signal(m))
                            for m in ["KD_ADVANCED", "ABC_BUY_POINT"]))):
            conflicts.append(self._build(
                "BREAKOUT_WITH_NO_CHASE_WARNING",
                "KD_ADVANCED", get_signal("KD_ADVANCED"),
                "NO_CHASE", get_signal("NO_CHASE"),
                snap_dict,
            ))

        # ABC_BUY_POINT with FUNDAMENTAL warning
        if (is_available("ABC_BUY_POINT") and is_available("FUNDAMENTAL_QUALITY")
                and "valid" in get_signal("ABC_BUY_POINT")
                and ("warning" in get_signal("FUNDAMENTAL_QUALITY")
                     or "negative" in get_signal("FUNDAMENTAL_QUALITY"))):
            conflicts.append(self._build(
                "ABC_BUY_POINT_WITH_FUNDAMENTAL_WARNING",
                "ABC_BUY_POINT", get_signal("ABC_BUY_POINT"),
                "FUNDAMENTAL_QUALITY", get_signal("FUNDAMENTAL_QUALITY"),
                snap_dict,
            ))

        # ABC_BUY_POINT with NO_CHASE warning
        if (is_available("ABC_BUY_POINT") and is_available("NO_CHASE")
                and "valid" in get_signal("ABC_BUY_POINT")
                and "chase_warning" in get_signal("NO_CHASE")):
            conflicts.append(self._build(
                "ABC_BUY_POINT_WITH_NO_CHASE_WARNING",
                "ABC_BUY_POINT", get_signal("ABC_BUY_POINT"),
                "NO_CHASE", get_signal("NO_CHASE"),
                snap_dict,
            ))

        # DO_NOT_REBUY vs bullish signal
        if (is_available("DO_NOT_REBUY_YET")
                and "do_not_rebuy" in get_signal("DO_NOT_REBUY_YET")
                and (is_available("BOTTOM_REVERSAL") and "confirmed" in get_signal("BOTTOM_REVERSAL"))):
            conflicts.append(self._build(
                "REBUY_SIGNAL_WITH_DO_NOT_REBUY_YET",
                "BOTTOM_REVERSAL", get_signal("BOTTOM_REVERSAL"),
                "DO_NOT_REBUY_YET", get_signal("DO_NOT_REBUY_YET"),
                snap_dict,
            ))

        # Timing approximate conflicts
        for mod_name, mod_data in modules.items():
            if mod_data.get("timing_warning") and "approximate" in str(mod_data.get("timing_warning", "")).lower():
                conflicts.append(self._build(
                    "TIMING_APPROXIMATE_CONFLICT",
                    mod_name, get_signal(mod_name),
                    "TIMING", "approximate",
                    snap_dict,
                ))

        return conflicts

    def _build(
        self, conflict_type: str, module_a: str, signal_a: str,
        module_b: str, signal_b: str, snap_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "conflict_type": conflict_type,
            "module_a": module_a,
            "signal_a": signal_a,
            "module_b": module_b,
            "signal_b": signal_b,
            "severity": self.severity(conflict_type),
            "replay_date": snap_dict.get("replay_date", ""),
            "session_id": snap_dict.get("session_id", ""),
            "auto_blocks_decision": False,  # INVARIANT
            "note": "Informational only. Does not auto-block decision.",
        }

    def classify(
        self, module_a: str, signal_a: str, module_b: str, signal_b: str
    ) -> str:
        """Classify conflict type from module/signal pairs."""
        pair = {module_a, module_b}
        if pair == {"KD_ADVANCED", "FUNDAMENTAL_QUALITY"}:
            return "TECHNICAL_BULLISH_FUNDAMENTAL_WARNING"
        if module_b == "NO_CHASE" or module_a == "NO_CHASE":
            return "BREAKOUT_WITH_NO_CHASE_WARNING"
        if pair == {"ABC_BUY_POINT", "FUNDAMENTAL_QUALITY"}:
            return "ABC_BUY_POINT_WITH_FUNDAMENTAL_WARNING"
        if pair == {"ABC_BUY_POINT", "NO_CHASE"}:
            return "ABC_BUY_POINT_WITH_NO_CHASE_WARNING"
        if "DO_NOT_REBUY_YET" in pair:
            return "REBUY_SIGNAL_WITH_DO_NOT_REBUY_YET"
        return "UNKNOWN"

    def severity(self, conflict_type: str) -> str:
        """Returns: LOW, MEDIUM, HIGH"""
        high = [
            "TECHNICAL_BULLISH_FUNDAMENTAL_WARNING",
            "SHORT_SQUEEZE_WITH_WEAK_PRICE_STRUCTURE",
            "DATA_QUALITY_CONFLICT",
        ]
        medium = [
            "BREAKOUT_WITH_NO_CHASE_WARNING",
            "ABC_BUY_POINT_WITH_FUNDAMENTAL_WARNING",
            "SECTOR_SUPPORT_WITH_KD_HIGH_DEATH_CROSS",
            "REBUY_SIGNAL_WITH_DO_NOT_REBUY_YET",
        ]
        if conflict_type in high:
            return "HIGH"
        if conflict_type in medium:
            return "MEDIUM"
        return "LOW"

    def evidence(self, conflict: Dict[str, Any]) -> List[str]:
        """Extract evidence from conflict dict."""
        return [
            f"{conflict.get('module_a')}: {conflict.get('signal_a')}",
            f"{conflict.get('module_b')}: {conflict.get('signal_b')}",
        ]

    def explain(self, conflict: Dict[str, Any]) -> str:
        """Generate human-readable explanation."""
        return (
            f"Conflict [{conflict.get('severity', 'LOW')}]: "
            f"{conflict.get('conflict_type', 'UNKNOWN')} — "
            f"{conflict.get('module_a')} ({conflict.get('signal_a')}) vs "
            f"{conflict.get('module_b')} ({conflict.get('signal_b')}). "
            "Informational only. Does not auto-block decision."
        )

    def summary(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize a list of conflicts."""
        by_severity: Dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for c in conflicts:
            sev = c.get("severity", "LOW")
            by_severity[sev] = by_severity.get(sev, 0) + 1
        return {
            "total": len(conflicts),
            "by_severity": by_severity,
            "conflict_types": [c.get("conflict_type") for c in conflicts],
            "auto_blocks_decision": False,  # INVARIANT
            "research_only": True,
        }
