"""
abc_validation/validation_result_v141.py — Validation result dataclass for A/B/C v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ABCValidationResult:
    """Full validation result for an A/B/C buy point empirical validation run."""
    validation_id: str
    buy_point_type: str                          # "A", "B", "C"
    rule_snapshot_id: str
    configuration: Dict[str, Any] = field(default_factory=dict)
    universe: str = ""
    symbols_requested: List[str] = field(default_factory=list)
    symbols_tested: List[str] = field(default_factory=list)
    symbols_blocked: List[str] = field(default_factory=list)
    date_range: Dict[str, str] = field(default_factory=dict)
    signal_count: int = 0
    trade_count: int = 0
    no_fill_count: int = 0
    outcome_distribution: Dict[str, int] = field(default_factory=dict)
    holding_period_results: Dict[str, Any] = field(default_factory=dict)
    stop_loss_results: Dict[str, Any] = field(default_factory=dict)
    take_profit_results: Dict[str, Any] = field(default_factory=dict)
    regime_results: Dict[str, Any] = field(default_factory=dict)
    ablation_results: Dict[str, Any] = field(default_factory=dict)
    second_wave_results: Dict[str, Any] = field(default_factory=dict)
    institutional_results: Dict[str, Any] = field(default_factory=dict)
    margin_results: Dict[str, Any] = field(default_factory=dict)
    volume_results: Dict[str, Any] = field(default_factory=dict)
    benchmark_results: Dict[str, Any] = field(default_factory=dict)
    quality_summary: Dict[str, Any] = field(default_factory=dict)
    confidence: str = "INSUFFICIENT"
    formal_conclusion_allowed: bool = False
    limitations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    reproducibility_hash: str = ""
    created_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Safety flags (always set, never override)
    no_real_orders: bool = True
    broker_execution_enabled: bool = False
    production_trading_blocked: bool = True
    mock_formal_conclusion_allowed: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        # Enforce safety flags
        d["no_real_orders"] = True
        d["broker_execution_enabled"] = False
        d["production_trading_blocked"] = True
        d["mock_formal_conclusion_allowed"] = False
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ABCValidationResult":
        """Load gracefully — unknown fields ignored."""
        known = set(cls.__dataclass_fields__)
        filtered = {k: v for k, v in d.items() if k in known}
        obj = cls(**filtered)
        # Safety flags enforced
        obj.no_real_orders = True
        obj.broker_execution_enabled = False
        obj.production_trading_blocked = True
        obj.mock_formal_conclusion_allowed = False
        return obj
