"""
paper_trading/multi_session/session_capability_v166.py — Session Capability Declaration v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Capabilities must be explicitly declared. Coordinator cannot guess capabilities.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True

STANDARD_CAPABILITIES = [
    "checkpoint",
    "replay",
    "recovery",
    "pause",
    "resume",
    "degraded_mode",
    "market_data_sharing",
    "event_stream",
    "symbol_lock",
    "risk_reporting",
    "capital_reporting",
    "lineage",
    "reproducibility",
    "scorecard",
]


@dataclass
class SessionCapabilityDeclaration:
    session_id: str
    supported_session_type: str
    supported_symbols: List[str]
    strategies: List[str]
    data_dependencies: List[str]
    event_sources: List[str]
    resource_requirements: Dict[str, Any]
    risk_requirements: Dict[str, Any]
    checkpoint_capable: bool
    replay_capable: bool
    recovery_capable: bool
    pause_capable: bool
    resume_capable: bool
    degraded_mode_capable: bool

    def declared_capabilities(self) -> List[str]:
        caps = []
        if self.checkpoint_capable:
            caps.append("checkpoint")
        if self.replay_capable:
            caps.append("replay")
        if self.recovery_capable:
            caps.append("recovery")
        if self.pause_capable:
            caps.append("pause")
        if self.resume_capable:
            caps.append("resume")
        if self.degraded_mode_capable:
            caps.append("degraded_mode")
        return caps

    def check_capability(self, capability: str) -> bool:
        return capability in self.declared_capabilities()

    def missing_capabilities(self, required: List[str]) -> List[str]:
        declared = self.declared_capabilities()
        return [c for c in required if c not in declared]


def validate_capability_declaration(decl: SessionCapabilityDeclaration) -> List[str]:
    violations: List[str] = []
    if not decl.session_id:
        violations.append("session_id required")
    if not decl.supported_session_type:
        violations.append("supported_session_type required")
    return violations
