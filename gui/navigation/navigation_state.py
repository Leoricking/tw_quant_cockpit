"""
gui/navigation/navigation_state.py — NavigationState for TW Quant Cockpit v0.5.2.

Persists favorites and recently-used tabs to config/gui_navigation_state.json.
Does NOT commit. State is gitignored.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DEFAULT_STATE_PATH = os.path.join(BASE_DIR, "config", "gui_navigation_state.json")
_MAX_RECENT = 20


class NavigationState:
    """Runtime navigation state: favorites and recently-used tabs.

    State is stored in config/gui_navigation_state.json (gitignored).
    load/save never crash on missing file or permission error.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, state_path: str = "") -> None:
        self._state_path = state_path or _DEFAULT_STATE_PATH
        self._state: dict = {
            "favorites": [],
            "recent":    [],
            "saved_at":  "",
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def load(self) -> None:
        """Load state from JSON. No crash if file missing or malformed."""
        try:
            if not os.path.isfile(self._state_path):
                logger.debug("NavigationState: state file not found — using defaults (%s)", self._state_path)
                return
            with open(self._state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                self._state["favorites"] = list(data.get("favorites", []))
                self._state["recent"]    = list(data.get("recent",    []))
                self._state["saved_at"]  = str(data.get("saved_at",   ""))
        except Exception as exc:
            logger.warning("NavigationState.load: could not load state: %s", exc)

    def save(self) -> None:
        """Save state to JSON. No crash on permission error."""
        try:
            self._state["saved_at"] = datetime.now().isoformat()
            os.makedirs(os.path.dirname(self._state_path), exist_ok=True)
            with open(self._state_path, "w", encoding="utf-8") as f:
                json.dump(self._state, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("NavigationState.save: could not save state: %s", exc)

    # ------------------------------------------------------------------
    # Favorites
    # ------------------------------------------------------------------

    def set_favorite(self, tab_id: str, enabled: bool = True) -> None:
        """Add or remove tab_id from favorites."""
        favs: List[str] = self._state.setdefault("favorites", [])
        if enabled:
            if tab_id not in favs:
                favs.append(tab_id)
        else:
            if tab_id in favs:
                favs.remove(tab_id)

    def get_favorites(self) -> List[str]:
        """Return list of favorite tab_ids."""
        return list(self._state.get("favorites", []))

    # ------------------------------------------------------------------
    # Recent
    # ------------------------------------------------------------------

    def record_recent(self, tab_id: str) -> None:
        """Prepend tab_id to recent list, keep max _MAX_RECENT entries."""
        recent: List[str] = self._state.setdefault("recent", [])
        # Remove existing occurrence if present
        if tab_id in recent:
            recent.remove(tab_id)
        recent.insert(0, tab_id)
        # Trim
        self._state["recent"] = recent[:_MAX_RECENT]

    def get_recent_tabs(self, limit: int = 10) -> List[str]:
        """Return list of recent tab_ids (up to limit)."""
        return list(self._state.get("recent", []))[:limit]
