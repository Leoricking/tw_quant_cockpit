"""
automation/scheduler_config.py - Scheduler configuration and default task definitions (v0.3.17).

[!] Read Only. Research Only. No Real Orders.
[!] Scheduler does NOT trade. Does NOT modify weights.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_CONFIG_PATH = os.path.join(_BASE_DIR, "config", "scheduler_config.yaml")

# Try PyYAML; fall back to JSON-based load/save
try:
    import yaml as _yaml
    _YAML_AVAILABLE = True
except ImportError:
    _yaml = None
    _YAML_AVAILABLE = False

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------

# Task names containing these keywords are BLOCKED unless explicitly in
# _SAFE_TASK_NAMES.  This prevents accidental order/trade execution.
_BLOCKED_KEYWORDS = {
    "order", "trade", "submit", "buy", "sell",
    "broker", "live", "execute",
}

_SAFE_TASK_NAMES = {
    "daily_data_update",
    "daily_validation",
    "daily_auto_report",
    "weekly_signal_quality",
    "weekly_rule_weight_tuning",
    "monthly_universe_quality",
}


def is_safe_task_name(name: str) -> bool:
    """Return True if the task name is safe to run (no blocked keywords)."""
    if name in _SAFE_TASK_NAMES:
        return True
    lower = name.lower()
    for kw in _BLOCKED_KEYWORDS:
        if kw in lower:
            return False
    return True


# ---------------------------------------------------------------------------
# Task config dataclass
# ---------------------------------------------------------------------------

@dataclass
class TaskConfig:
    """Configuration for a single scheduled task."""

    task_name:            str  = ""
    enabled:              bool = False
    schedule_type:        str  = "daily"     # daily | weekly | monthly | manual
    run_time:             str  = "18:00"     # HH:MM
    weekday:              int  = 5           # 1=Mon … 7=Sun (used for weekly)
    month_day:            int  = 1           # 1-28 (used for monthly)
    command_name:         str  = ""
    profile:              str  = "daily"
    universe_size:        int  = 0           # 0 = use manifest
    stocks:               List[str] = field(default_factory=list)
    top_n:                int  = 8
    max_runtime_seconds:  int  = 1800        # 30 min default
    retry_count:          int  = 0
    retry_delay_seconds:  int  = 60
    read_only:            bool = True
    no_real_orders:       bool = True
    notes:                str  = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "TaskConfig":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in d.items() if k in known})


# ---------------------------------------------------------------------------
# Scheduler-level config
# ---------------------------------------------------------------------------

@dataclass
class SchedulerConfig:
    """Top-level scheduler configuration."""

    enabled:   bool = False
    mode:      str  = "real"
    timezone:  str  = "Asia/Taipei"
    tasks:     Dict[str, TaskConfig] = field(default_factory=dict)

    # Safety invariants — always True regardless of config file
    read_only:     bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "enabled":       self.enabled,
            "mode":          self.mode,
            "timezone":      self.timezone,
            "read_only":     True,
            "no_real_orders": True,
            "tasks": {
                name: task.to_dict()
                for name, task in self.tasks.items()
            },
        }

    @classmethod
    def from_dict(cls, d: dict) -> "SchedulerConfig":
        tasks_raw = d.get("tasks", {})
        tasks = {}
        for name, td in tasks_raw.items():
            if isinstance(td, dict):
                td["task_name"] = name
                tasks[name] = TaskConfig.from_dict(td)
        return cls(
            enabled   = d.get("enabled", False),
            mode      = d.get("mode",    "real"),
            timezone  = d.get("timezone","Asia/Taipei"),
            tasks     = tasks,
            read_only      = True,
            no_real_orders = True,
        )

    # ------------------------------------------------------------------
    # Load / Save
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, path: Optional[str] = None) -> "SchedulerConfig":
        """Load config from YAML or JSON file. Returns default if not found."""
        path = path or _DEFAULT_CONFIG_PATH
        if not os.path.isfile(path):
            logger.info("SchedulerConfig: file not found, using defaults: %s", path)
            return cls.default()

        try:
            with open(path, encoding="utf-8") as f:
                raw = f.read()
            if _YAML_AVAILABLE:
                data = _yaml.safe_load(raw) or {}
            else:
                # Fall back: try JSON, then bare dict parse
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    logger.warning("PyYAML not available and file is not JSON. Using defaults.")
                    return cls.default()
            return cls.from_dict(data)
        except Exception as exc:
            logger.error("SchedulerConfig.load failed: %s", exc)
            return cls.default()

    def save(self, path: Optional[str] = None) -> str:
        """Save config to YAML (or JSON if PyYAML unavailable). Returns path."""
        path = path or _DEFAULT_CONFIG_PATH
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = self.to_dict()
        try:
            if _YAML_AVAILABLE:
                content = _yaml.dump(data, default_flow_style=False, allow_unicode=True)
            else:
                # Write as JSON with .yaml path (still parseable as JSON)
                content = json.dumps(data, ensure_ascii=False, indent=2)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("SchedulerConfig saved: %s", path)
            return path
        except Exception as exc:
            logger.error("SchedulerConfig.save failed: %s", exc)
            return path

    # ------------------------------------------------------------------
    # Default safe config
    # ------------------------------------------------------------------

    @classmethod
    def default(cls) -> "SchedulerConfig":
        """Return a safe, all-disabled default config."""
        tasks = {
            "daily_data_update": TaskConfig(
                task_name           = "daily_data_update",
                enabled             = False,
                schedule_type       = "daily",
                run_time            = "18:00",
                command_name        = "daily-data-update",
                max_runtime_seconds = 1800,
                read_only           = True,
                no_real_orders      = True,
                notes               = "Fetch public data and check data sources. Read-only.",
            ),
            "daily_validation": TaskConfig(
                task_name           = "daily_validation",
                enabled             = False,
                schedule_type       = "daily",
                run_time            = "18:20",
                command_name        = "daily-validation",
                max_runtime_seconds = 1800,
                read_only           = True,
                no_real_orders      = True,
                notes               = "Universe quality + validation suite + signal quality + portfolio sim.",
            ),
            "daily_auto_report": TaskConfig(
                task_name           = "daily_auto_report",
                enabled             = False,
                schedule_type       = "daily",
                run_time            = "18:40",
                command_name        = "auto-report",
                profile             = "daily",
                max_runtime_seconds = 1800,
                read_only           = True,
                no_real_orders      = True,
                notes               = "Auto report center daily profile.",
            ),
            "weekly_signal_quality": TaskConfig(
                task_name           = "weekly_signal_quality",
                enabled             = False,
                schedule_type       = "weekly",
                weekday             = 5,
                run_time            = "19:00",
                command_name        = "signal-quality",
                max_runtime_seconds = 1800,
                read_only           = True,
                no_real_orders      = True,
                notes               = "Weekly signal quality report (Friday).",
            ),
            "weekly_rule_weight_tuning": TaskConfig(
                task_name           = "weekly_rule_weight_tuning",
                enabled             = False,
                schedule_type       = "weekly",
                weekday             = 5,
                run_time            = "19:30",
                command_name        = "tune-rule-weights",
                max_runtime_seconds = 3600,
                read_only           = True,
                no_real_orders      = True,
                notes               = "Weekly rule weight tuning. Does NOT auto-apply weights.",
            ),
            "monthly_universe_quality": TaskConfig(
                task_name           = "monthly_universe_quality",
                enabled             = False,
                schedule_type       = "monthly",
                month_day           = 1,
                run_time            = "20:00",
                command_name        = "universe-quality",
                max_runtime_seconds = 1800,
                read_only           = True,
                no_real_orders      = True,
                notes               = "Monthly universe quality check (1st of month).",
            ),
        }
        return cls(
            enabled        = False,
            mode           = "real",
            timezone       = "Asia/Taipei",
            tasks          = tasks,
            read_only      = True,
            no_real_orders = True,
        )
