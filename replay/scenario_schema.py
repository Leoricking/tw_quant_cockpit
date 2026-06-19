"""
replay/scenario_schema.py — Scenario Template schemas for v1.2.1

[!] Research Only. No Real Orders. Replay Training Only.
[!] Templates never contain future answers, realized returns, or future labels.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SCENARIO_CATEGORIES = [
    "TREND_FOLLOWING", "BREAKOUT", "PULLBACK", "BOTTOM_REVERSAL",
    "MOMENTUM", "SECTOR_ROTATION", "FUNDAMENTAL_TURNAROUND",
    "RISK_CONTROL", "NO_CHASE", "NO_PANIC_SELL", "FREE_PRACTICE", "CUSTOM",
]

SCENARIO_DIFFICULTIES = ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]
SYMBOL_SELECTORS = ["FREE", "FIXED", "LIST"]
DATE_SELECTORS = ["FREE", "FIXED", "RANGE"]
QUALIFICATION_VALUES = ["OBSERVATIONAL_ONLY", "DEMO_ONLY", "BLOCKED", "UNKNOWN", "DATA_UNAVAILABLE"]

FORBIDDEN_TEMPLATE_FIELDS = [
    "future_return", "outcome", "final_label", "answer",
    "realized_pnl", "broker", "order_token", "api_key", "secret",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ReplayScenarioTemplate:
    """
    A scenario template for replay training.
    [!] Research Only. No Real Orders. No future data.
    """
    scenario_id: str
    scenario_name: str
    description: str
    category: str
    difficulty: str
    objectives: List[str] = field(default_factory=list)
    instructions: str = ""
    rules: List[str] = field(default_factory=list)
    symbol_selector: str = "FREE"
    symbols: List[str] = field(default_factory=list)
    date_selector: str = "FREE"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: Optional[int] = None
    initial_visible_history_days: int = 120
    required_datasets: List[str] = field(default_factory=lambda: ["price"])
    optional_datasets: List[str] = field(default_factory=list)
    strict_future_firewall: bool = True
    include_quality_gate: bool = True
    include_strategy_knowledge: bool = True
    include_chips: bool = False
    include_fundamental: bool = False
    default_playback_speed: int = 1
    allowed_actions: List[str] = field(default_factory=lambda: [
        "WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"
    ])
    tags: List[str] = field(default_factory=list)
    source: str = "user"
    version: str = "1"
    archived: bool = False
    created_at: str = field(default_factory=_now_utc)
    updated_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True
    # Extra fields from raw dict preserved for validation (e.g. forbidden field detection)
    _extra_fields: Dict[str, Any] = field(default_factory=dict, repr=False)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "scenario_id": self.scenario_id,
            "scenario_name": self.scenario_name,
            "description": self.description,
            "category": self.category,
            "difficulty": self.difficulty,
            "objectives": self.objectives,
            "instructions": self.instructions,
            "rules": self.rules,
            "symbol_selector": self.symbol_selector,
            "symbols": self.symbols,
            "date_selector": self.date_selector,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "duration_days": self.duration_days,
            "initial_visible_history_days": self.initial_visible_history_days,
            "required_datasets": self.required_datasets,
            "optional_datasets": self.optional_datasets,
            "strict_future_firewall": self.strict_future_firewall,
            "include_quality_gate": self.include_quality_gate,
            "include_strategy_knowledge": self.include_strategy_knowledge,
            "include_chips": self.include_chips,
            "include_fundamental": self.include_fundamental,
            "default_playback_speed": self.default_playback_speed,
            "allowed_actions": self.allowed_actions,
            "tags": self.tags,
            "source": self.source,
            "version": self.version,
            "archived": self.archived,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "research_only": True,
            "no_real_orders": True,
        }
        # Include extra fields so validators can detect forbidden fields
        if self._extra_fields:
            d.update(self._extra_fields)
        return d

    # Known field names used by from_dict for detecting extra/unknown fields
    _KNOWN_FIELDS = {
        "scenario_id", "scenario_name", "description", "category", "difficulty",
        "objectives", "instructions", "rules", "symbol_selector", "symbols",
        "date_selector", "start_date", "end_date", "duration_days",
        "initial_visible_history_days", "required_datasets", "optional_datasets",
        "strict_future_firewall", "include_quality_gate", "include_strategy_knowledge",
        "include_chips", "include_fundamental", "default_playback_speed",
        "allowed_actions", "tags", "source", "version", "archived",
        "created_at", "updated_at", "research_only", "no_real_orders",
    }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayScenarioTemplate":
        # Capture any fields not in the known schema for validation purposes
        extra = {k: v for k, v in d.items() if k not in cls._KNOWN_FIELDS}
        return cls(
            scenario_id=d.get("scenario_id", ""),
            scenario_name=d.get("scenario_name", ""),
            description=d.get("description", ""),
            category=d.get("category", "CUSTOM"),
            difficulty=d.get("difficulty", "BEGINNER"),
            objectives=d.get("objectives", []),
            instructions=d.get("instructions", ""),
            rules=d.get("rules", []),
            symbol_selector=d.get("symbol_selector", "FREE"),
            symbols=d.get("symbols", []),
            date_selector=d.get("date_selector", "FREE"),
            start_date=d.get("start_date"),
            end_date=d.get("end_date"),
            duration_days=d.get("duration_days"),
            initial_visible_history_days=int(d.get("initial_visible_history_days", 120)),
            required_datasets=d.get("required_datasets", ["price"]),
            optional_datasets=d.get("optional_datasets", []),
            strict_future_firewall=bool(d.get("strict_future_firewall", True)),
            include_quality_gate=bool(d.get("include_quality_gate", True)),
            include_strategy_knowledge=bool(d.get("include_strategy_knowledge", True)),
            include_chips=bool(d.get("include_chips", False)),
            include_fundamental=bool(d.get("include_fundamental", False)),
            default_playback_speed=int(d.get("default_playback_speed", 1)),
            allowed_actions=d.get("allowed_actions", ["WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"]),
            tags=d.get("tags", []),
            source=d.get("source", "user"),
            version=str(d.get("version", "1")),
            archived=bool(d.get("archived", False)),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
            _extra_fields=extra,
        )


@dataclass
class ReplayScenarioInstance:
    """
    A resolved scenario instance with specific symbol/dates.
    [!] Research Only. No Real Orders.
    """
    instance_id: str
    scenario_id: str
    scenario_version: str
    resolved_symbol: str
    resolved_start_date: str
    resolved_end_date: str
    resolved_initial_date: Optional[str]
    qualification: str
    data_availability: Dict[str, Any]
    warnings: List[str]
    generated_at: str
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "scenario_id": self.scenario_id,
            "scenario_version": self.scenario_version,
            "resolved_symbol": self.resolved_symbol,
            "resolved_start_date": self.resolved_start_date,
            "resolved_end_date": self.resolved_end_date,
            "resolved_initial_date": self.resolved_initial_date,
            "qualification": self.qualification,
            "data_availability": self.data_availability,
            "warnings": self.warnings,
            "generated_at": self.generated_at,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayScenarioInstance":
        return cls(
            instance_id=d.get("instance_id", ""),
            scenario_id=d.get("scenario_id", ""),
            scenario_version=str(d.get("scenario_version", "1")),
            resolved_symbol=d.get("resolved_symbol", ""),
            resolved_start_date=d.get("resolved_start_date", ""),
            resolved_end_date=d.get("resolved_end_date", ""),
            resolved_initial_date=d.get("resolved_initial_date"),
            qualification=d.get("qualification", "UNKNOWN"),
            data_availability=d.get("data_availability", {}),
            warnings=d.get("warnings", []),
            generated_at=d.get("generated_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
        )


@dataclass
class ScenarioValidationResult:
    """Result of scenario template validation."""
    scenario_id: str
    valid: bool
    errors: List[str]
    warnings: List[str]
    missing_required_datasets: List[str]
    missing_optional_datasets: List[str]
    future_data_risk: bool
    point_in_time_compatible: bool
    qualification: str
    checked_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "missing_required_datasets": self.missing_required_datasets,
            "missing_optional_datasets": self.missing_optional_datasets,
            "future_data_risk": self.future_data_risk,
            "point_in_time_compatible": self.point_in_time_compatible,
            "qualification": self.qualification,
            "checked_at": self.checked_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ScenarioValidationResult":
        return cls(
            scenario_id=d.get("scenario_id", ""),
            valid=bool(d.get("valid", False)),
            errors=d.get("errors", []),
            warnings=d.get("warnings", []),
            missing_required_datasets=d.get("missing_required_datasets", []),
            missing_optional_datasets=d.get("missing_optional_datasets", []),
            future_data_risk=bool(d.get("future_data_risk", False)),
            point_in_time_compatible=bool(d.get("point_in_time_compatible", True)),
            qualification=d.get("qualification", "UNKNOWN"),
            checked_at=d.get("checked_at", _now_utc()),
        )
