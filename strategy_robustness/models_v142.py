"""
strategy_robustness/models_v142.py — Data models for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED = False


# ---------------------------------------------------------------------------
# String constant classes (not Enum)
# ---------------------------------------------------------------------------

class RobustnessStatus:
    ROBUST = "ROBUST"
    ACCEPTABLE = "ACCEPTABLE"
    FRAGILE = "FRAGILE"
    REGIME_DEPENDENT = "REGIME_DEPENDENT"
    PARAMETER_SENSITIVE = "PARAMETER_SENSITIVE"
    COST_SENSITIVE = "COST_SENSITIVE"
    CONCENTRATED = "CONCENTRATED"
    DECAYING = "DECAYING"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    BLOCKED = "BLOCKED"
    DEMO_ONLY = "DEMO_ONLY"
    FAILED = "FAILED"


class RobustnessDimension:
    TIME = "TIME"
    SYMBOL = "SYMBOL"
    INDUSTRY = "INDUSTRY"
    REGIME = "REGIME"
    PARAMETER = "PARAMETER"
    COST = "COST"
    SLIPPAGE = "SLIPPAGE"
    TRADE_CONCENTRATION = "TRADE_CONCENTRATION"
    SAMPLE_SPLIT = "SAMPLE_SPLIT"
    WALK_FORWARD = "WALK_FORWARD"
    BOOTSTRAP = "BOOTSTRAP"
    MONTE_CARLO = "MONTE_CARLO"
    DECAY = "DECAY"
    DATA_QUALITY = "DATA_QUALITY"
    FRESHNESS = "FRESHNESS"
    SURVIVORSHIP = "SURVIVORSHIP"
    CORPORATE_ACTION = "CORPORATE_ACTION"


class DecayStatus:
    NO_DECAY = "NO_DECAY"
    POSSIBLE_DECAY = "POSSIBLE_DECAY"
    SIGNIFICANT_DECAY = "SIGNIFICANT_DECAY"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class RobustnessMetric:
    dimension: str
    metric_name: str
    value: float
    normalized_score: float
    threshold: float
    status: str
    sample_size: int
    confidence: str
    reasons: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "dimension": self.dimension,
            "metric_name": self.metric_name,
            "value": self.value,
            "normalized_score": self.normalized_score,
            "threshold": self.threshold,
            "status": self.status,
            "sample_size": self.sample_size,
            "confidence": self.confidence,
            "reasons": list(self.reasons),
            "warnings": list(self.warnings),
            "metadata": copy.deepcopy(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RobustnessMetric":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class RobustnessConfiguration:
    rule_id: str
    source_result_ids: list = field(default_factory=list)
    universe: str = "core"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    minimum_symbols: int = 5
    minimum_trades: int = 30
    minimum_industries: int = 2
    minimum_regimes: int = 2
    rolling_window_size: int = 60
    rolling_step_size: int = 20
    bootstrap_iterations: int = 1000
    monte_carlo_iterations: int = 1000
    random_seed: int = 42
    parameter_neighborhood: float = 0.1
    cost_multipliers: list = field(default_factory=lambda: [1.0, 1.25, 1.5, 2.0])
    slippage_multipliers: list = field(default_factory=lambda: [0, 0.0002, 0.0005, 0.001, 0.002])
    concentration_cutoffs: list = field(default_factory=lambda: [1, 3, 5])
    stress_scenarios: list = field(default_factory=list)
    data_mode: str = "REAL"
    dry_run: bool = True
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "source_result_ids": list(self.source_result_ids),
            "universe": self.universe,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "minimum_symbols": self.minimum_symbols,
            "minimum_trades": self.minimum_trades,
            "minimum_industries": self.minimum_industries,
            "minimum_regimes": self.minimum_regimes,
            "rolling_window_size": self.rolling_window_size,
            "rolling_step_size": self.rolling_step_size,
            "bootstrap_iterations": self.bootstrap_iterations,
            "monte_carlo_iterations": self.monte_carlo_iterations,
            "random_seed": self.random_seed,
            "parameter_neighborhood": self.parameter_neighborhood,
            "cost_multipliers": list(self.cost_multipliers),
            "slippage_multipliers": list(self.slippage_multipliers),
            "concentration_cutoffs": list(self.concentration_cutoffs),
            "stress_scenarios": list(self.stress_scenarios),
            "data_mode": self.data_mode,
            "dry_run": self.dry_run,
            "metadata": copy.deepcopy(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RobustnessConfiguration":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class StrategyRobustnessResult:
    robustness_id: str
    rule_id: str
    universe: str
    start_date: Optional[str]
    end_date: Optional[str]
    status: str = RobustnessStatus.BLOCKED
    overall_score: float = 0.0
    robustness_status: str = RobustnessStatus.BLOCKED
    formal_conclusion_allowed: bool = False
    trade_count: int = 0
    symbol_count: int = 0
    date_range: dict = field(default_factory=dict)
    time_robustness: dict = field(default_factory=dict)
    cross_sectional: dict = field(default_factory=dict)
    industry_robustness: dict = field(default_factory=dict)
    regime_robustness: dict = field(default_factory=dict)
    parameter_sensitivity: dict = field(default_factory=dict)
    cost_stress: dict = field(default_factory=dict)
    trade_concentration: dict = field(default_factory=dict)
    bootstrap: dict = field(default_factory=dict)
    monte_carlo: dict = field(default_factory=dict)
    rolling_stability: dict = field(default_factory=dict)
    decay: dict = field(default_factory=dict)
    stress_scenarios: dict = field(default_factory=dict)
    failure_modes: list = field(default_factory=list)
    score_detail: dict = field(default_factory=dict)
    dimension_scores: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    blocked_reasons: list = field(default_factory=list)
    data_mode: str = "REAL"
    dry_run: bool = True
    reproducibility_hash: str = ""
    created_at: str = ""
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.reproducibility_hash:
            self.reproducibility_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = json.dumps(
            {
                "rule_id": self.rule_id,
                "universe": self.universe,
                "start_date": self.start_date,
                "end_date": self.end_date,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "robustness_id": self.robustness_id,
            "rule_id": self.rule_id,
            "universe": self.universe,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "overall_score": self.overall_score,
            "robustness_status": self.robustness_status,
            "formal_conclusion_allowed": self.formal_conclusion_allowed,
            "trade_count": self.trade_count,
            "symbol_count": self.symbol_count,
            "date_range": copy.deepcopy(self.date_range),
            "time_robustness": copy.deepcopy(self.time_robustness),
            "cross_sectional": copy.deepcopy(self.cross_sectional),
            "industry_robustness": copy.deepcopy(self.industry_robustness),
            "regime_robustness": copy.deepcopy(self.regime_robustness),
            "parameter_sensitivity": copy.deepcopy(self.parameter_sensitivity),
            "cost_stress": copy.deepcopy(self.cost_stress),
            "trade_concentration": copy.deepcopy(self.trade_concentration),
            "bootstrap": copy.deepcopy(self.bootstrap),
            "monte_carlo": copy.deepcopy(self.monte_carlo),
            "rolling_stability": copy.deepcopy(self.rolling_stability),
            "decay": copy.deepcopy(self.decay),
            "stress_scenarios": copy.deepcopy(self.stress_scenarios),
            "failure_modes": list(self.failure_modes),
            "score_detail": copy.deepcopy(self.score_detail),
            "dimension_scores": copy.deepcopy(self.dimension_scores),
            "warnings": list(self.warnings),
            "blocked_reasons": list(self.blocked_reasons),
            "data_mode": self.data_mode,
            "dry_run": self.dry_run,
            "reproducibility_hash": self.reproducibility_hash,
            "created_at": self.created_at,
            "metadata": copy.deepcopy(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyRobustnessResult":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)
