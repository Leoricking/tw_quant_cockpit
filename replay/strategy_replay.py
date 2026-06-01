"""replay/strategy_replay.py — Strategy signal overlay for replay (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice.
[!] NEVER triggers orders. NEVER calls submit_order. Training annotations only."""
from __future__ import annotations

import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyReplayOverlay:
    """Reads existing research signals and displays them as training overlays.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    All signals are labeled as training annotations only.
    NEVER triggers orders. NEVER calls submit_order.
    """

    read_only = True
    no_real_orders = True

    def __init__(self):
        self._overlay_cache: Optional[dict] = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _find_rule_governance_snapshot(self, symbol: Optional[str], date: Optional[str]) -> Optional[str]:
        """Locate a rule governance snapshot file if available."""
        candidates = [
            os.path.join(BASE_DIR, "governance", "rule_governance_snapshot.json"),
            os.path.join(BASE_DIR, "governance", "snapshots", f"rules_{date}.json") if date else "",
            os.path.join(BASE_DIR, "governance", f"rules_{symbol}.json") if symbol else "",
        ]
        for path in candidates:
            if path and os.path.exists(path):
                return path
        return None

    def _find_signal_quality_json(self) -> Optional[str]:
        """Locate latest signal quality JSON if available."""
        candidates = [
            os.path.join(BASE_DIR, "governance", "signal_quality_latest.json"),
            os.path.join(BASE_DIR, "governance", "signal_quality.json"),
            os.path.join(BASE_DIR, "quality", "signal_quality_latest.json"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def load_rule_signals(
        self, symbol: Optional[str] = None, date: Optional[str] = None
    ) -> list:
        """Read rule governance snapshot if available. Returns list of signal dicts.
        No crash if file is missing.
        """
        path = self._find_rule_governance_snapshot(symbol, date)
        if path is None:
            logger.info("[StrategyReplayOverlay] no rule governance snapshot found")
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            signals = []
            rules = data if isinstance(data, list) else data.get("rules", [])
            for rule in rules:
                signals.append(
                    {
                        "rule_id": rule.get("rule_id", ""),
                        "rule_name": rule.get("rule_name", rule.get("name", "")),
                        "signal_type": rule.get("signal_type", "RESEARCH"),
                        "direction": rule.get("direction", ""),
                        "weight": rule.get("weight", 0),
                        "enabled": rule.get("enabled", True),
                        "training_annotation": True,
                        "research_only": True,
                        "no_real_orders": True,
                        "not_investment_advice": True,
                    }
                )
            return signals
        except Exception as exc:
            logger.warning("[StrategyReplayOverlay] load_rule_signals error: %s", exc)
            return []

    def load_signal_quality(self) -> dict:
        """Read latest signal quality JSON. No crash if missing."""
        path = self._find_signal_quality_json()
        if path is None:
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("[StrategyReplayOverlay] load_signal_quality error: %s", exc)
            return {}

    def build_overlay(
        self,
        visible_df,
        symbol: Optional[str] = None,
        date: Optional[str] = None,
    ) -> dict:
        """Combine available signals into training overlay. NEVER triggers orders."""
        rule_signals = self.load_rule_signals(symbol=symbol, date=date)
        signal_quality = self.load_signal_quality()

        # Filter to enabled signals only
        active_signals = [s for s in rule_signals if s.get("enabled", True)]

        overlay = {
            "rule_signals": rule_signals,
            "signal_quality_summary": signal_quality,
            "active_signal_count": len(active_signals),
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
            "training_annotation_only": True,
            "label": "Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED",
        }
        self._overlay_cache = overlay
        return overlay

    def get_active_signals(self, current_time: str) -> list:
        """Return signals relevant to current_time from cached overlay.
        All signals are training annotations only — no order intent.
        """
        if self._overlay_cache is None:
            return []
        rule_signals = self._overlay_cache.get("rule_signals", [])
        active = []
        for sig in rule_signals:
            if not sig.get("enabled", True):
                continue
            sig_copy = dict(sig)
            sig_copy["current_time"] = current_time
            sig_copy["training_annotation"] = True
            sig_copy["research_only"] = True
            sig_copy["no_real_orders"] = True
            active.append(sig_copy)
        return active
