"""
paper_trading/failure_validation/config_drift_v165.py — Configuration drift simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class ConfigDriftResult:
    component: str = ""
    drifted_keys: List[str] = field(default_factory=list)
    detected: bool = False
    alert_generated: bool = False

    @property
    def has_drift(self) -> bool:
        return len(self.drifted_keys) > 0

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "drifted_keys": self.drifted_keys,
            "has_drift": self.has_drift,
            "detected": self.detected,
            "alert_generated": self.alert_generated,
        }


def simulate_config_drift(component: str, expected: Dict[str, Any],
                          actual: Dict[str, Any], seed: int = 42) -> ConfigDriftResult:
    import random
    rng = random.Random(seed)
    drifted = [k for k in expected if expected.get(k) != actual.get(k)]
    result = ConfigDriftResult(component=component, drifted_keys=drifted)
    if drifted:
        result.detected = rng.random() > 0.15
        result.alert_generated = result.detected and rng.random() > 0.2
    return result
