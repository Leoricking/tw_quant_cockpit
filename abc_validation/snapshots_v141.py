"""
abc_validation/snapshots_v141.py — Rule snapshots for A/B/C buy point validation v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Snapshots are deterministic by (rule_id + parameters). Old fields load gracefully.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _make_parameter_hash(rule_id: str, parameters: dict) -> str:
    """Deterministic hash from rule_id + parameters."""
    canonical = json.dumps({"rule_id": rule_id, "parameters": parameters}, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


@dataclass
class ABCBuyPointRuleSnapshot:
    """Immutable snapshot of A/B/C buy point rule at a point in time."""
    snapshot_id: str
    buy_point_type: str              # "A", "B", or "C"
    rule_id: str
    rule_version: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    parameter_hash: str = ""
    required_inputs: List[str] = field(default_factory=list)
    minimum_history: int = 20
    volume_rule: Optional[str] = None
    indicator_rule: Optional[str] = None
    institutional_rule: Optional[str] = None
    margin_rule: Optional[str] = None
    second_wave_rule: Optional[str] = None
    trend_filter: Optional[str] = None
    market_regime_filter: Optional[str] = None
    execution_model: str = "NEXT_OPEN"
    cost_model: str = "FIXED_BPS"
    slippage_model: str = "CONSERVATIVE_FIXED"
    source_commit: str = ""
    application_version: str = "1.4.1"
    created_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.parameter_hash:
            self.parameter_hash = _make_parameter_hash(self.rule_id, self.parameters)

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "buy_point_type": self.buy_point_type,
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "parameters": self.parameters,
            "parameter_hash": self.parameter_hash,
            "required_inputs": self.required_inputs,
            "minimum_history": self.minimum_history,
            "volume_rule": self.volume_rule,
            "indicator_rule": self.indicator_rule,
            "institutional_rule": self.institutional_rule,
            "margin_rule": self.margin_rule,
            "second_wave_rule": self.second_wave_rule,
            "trend_filter": self.trend_filter,
            "market_regime_filter": self.market_regime_filter,
            "execution_model": self.execution_model,
            "cost_model": self.cost_model,
            "slippage_model": self.slippage_model,
            "source_commit": self.source_commit,
            "application_version": self.application_version,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ABCBuyPointRuleSnapshot":
        """Load gracefully — unknown fields ignored, missing fields use defaults."""
        known = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in d.items() if k in known}
        return cls(**filtered)

    @classmethod
    def make_default(cls, buy_point_type: str) -> "ABCBuyPointRuleSnapshot":
        """Create a default snapshot for a buy point type."""
        type_map = {
            "A": ("abc_buy_point_a", "1.0.0", ["ohlcv_daily", "chip_data"], 30),
            "B": ("abc_buy_point_b", "1.0.0", ["ohlcv_daily", "realtime_data"], 20),
            "C": ("abc_buy_point_c", "1.0.0", ["ohlcv_daily", "chip_data"], 40),
        }
        rule_id, rule_version, required_inputs, min_history = type_map.get(
            buy_point_type, ("abc_buy_point_a", "1.0.0", ["ohlcv_daily"], 20)
        )
        snap_id = f"snap_{buy_point_type.lower()}_{_make_parameter_hash(rule_id, {})}"
        return cls(
            snapshot_id=snap_id,
            buy_point_type=buy_point_type,
            rule_id=rule_id,
            rule_version=rule_version,
            required_inputs=required_inputs,
            minimum_history=min_history,
        )
