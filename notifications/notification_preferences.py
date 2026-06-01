"""
notifications/notification_preferences.py — NotificationPreferences (v0.4.5).

User preferences for the Notification Center.
Stored in memory only. Example config file: config/notification_preferences.example.json
Real preferences file (config/notification_preferences.json) is gitignored.

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT contain tokens. Does NOT connect to external services.
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from notifications.notification_schema import (
    SEV_INFO, SEV_NOTICE, ALL_CATEGORIES,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_EXAMPLE_CONFIG_PATH = os.path.join(BASE_DIR, "config", "notification_preferences.example.json")
_RUNTIME_CONFIG_PATH = os.path.join(BASE_DIR, "config", "notification_preferences.json")


@dataclass
class NotificationPreferences:
    """
    Notification Center preferences.

    Defaults:
      local_enabled     = True
      external_enabled  = False  (always False first version)
      min_severity      = INFO
      categories_enabled = all categories

    [!] external_enabled stays False — first version placeholder only.
    """
    local_enabled:            bool            = True
    external_enabled:         bool            = False   # always False first version
    min_severity:             str             = SEV_INFO
    categories_enabled:       List[str]       = field(default_factory=lambda: list(ALL_CATEGORIES))
    quiet_hours_enabled:      bool            = False
    quiet_hours_start:        str             = "22:00"
    quiet_hours_end:          str             = "08:00"
    daily_summary_enabled:    bool            = True
    replay_reminder_enabled:  bool            = True

    def __post_init__(self):
        # external_enabled is always False in first version
        self.external_enabled = False
        if not self.categories_enabled:
            self.categories_enabled = list(ALL_CATEGORIES)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["external_enabled"] = False  # enforce
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "NotificationPreferences":
        safe = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        obj = cls(**safe)
        obj.external_enabled = False  # enforce
        return obj

    # ------------------------------------------------------------------
    # Load / Save
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, path: Optional[str] = None) -> "NotificationPreferences":
        """Load preferences from JSON file. Falls back to defaults on any error."""
        p = path or _RUNTIME_CONFIG_PATH
        if not os.path.isfile(p):
            return cls()
        try:
            with open(p, "r", encoding="utf-8") as fh:
                d = json.load(fh)
            return cls.from_dict(d)
        except Exception as exc:
            logger.warning("NotificationPreferences.load: %s — using defaults", exc)
            return cls()

    def save(self, path: Optional[str] = None) -> str:
        """Save preferences to JSON file. Returns path."""
        p = path or _RUNTIME_CONFIG_PATH
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(self.to_dict(), fh, indent=2, ensure_ascii=False)
        except Exception as exc:
            logger.warning("NotificationPreferences.save: %s", exc)
        return p

    def is_category_enabled(self, category: str) -> bool:
        return category in self.categories_enabled

    def should_notify(self, severity: str, category: str) -> bool:
        from notifications.notification_schema import severity_gte
        if not self.local_enabled:
            return False
        if not severity_gte(severity, self.min_severity):
            return False
        if not self.is_category_enabled(category):
            return False
        return True


def write_example_config() -> str:
    """Write the example preferences file to config/. Returns path."""
    prefs = NotificationPreferences()
    os.makedirs(os.path.dirname(_EXAMPLE_CONFIG_PATH), exist_ok=True)
    try:
        with open(_EXAMPLE_CONFIG_PATH, "w", encoding="utf-8") as fh:
            d = prefs.to_dict()
            d["_note"] = (
                "Copy to config/notification_preferences.json to customize. "
                "Do NOT commit notification_preferences.json (gitignored). "
                "external_enabled is always False in v0.4.5."
            )
            json.dump(d, fh, indent=2, ensure_ascii=False)
        logger.info("NotificationPreferences: example config written → %s", _EXAMPLE_CONFIG_PATH)
    except Exception as exc:
        logger.warning("write_example_config: %s", exc)
    return _EXAMPLE_CONFIG_PATH
