"""
paper_trading/small_capital_strategy/stable_rollup_models_v179.py
Dataclass models for Small Capital Strategy Stable Rollup v1.7.9.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"
_LINEAGE = "paper_trading.small_capital_strategy.stable_rollup_models_v179"


@dataclass
class StableRollupVersionEntry:
    """Version entry for one of the v1.7.x releases."""
    version: str = ""
    release_name: str = ""
    schema_version: str = ""
    policy_version: str = ""
    is_importable: bool = False
    health_pass: bool = False
    gate_pass: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StableRollupCompatResult:
    """Result of a backward-compatibility check."""
    version: str = ""
    module: str = ""
    importable: bool = False
    version_match: bool = False
    safety_ok: bool = False
    error: Optional[str] = None
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StableRollupAuditResult:
    """Generic audit result."""
    audit_name: str = ""
    passed: int = 0
    failed: int = 0
    total: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    checks: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class StableRollupHealthSummary:
    """Health summary for stable rollup v1.7.9."""
    status: str = "FAIL"
    passed: int = 0
    failed: int = 0
    total: int = 0
    all_passed: bool = False
    checks: List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True


@dataclass
class StableRollupReport:
    """Full stable rollup report."""
    version: str = "1.7.9"
    release_name: str = "Small Capital Strategy Stable Rollup"
    sections: List[Dict[str, Any]] = field(default_factory=list)
    health_status: str = "FAIL"
    gate_status: str = "FAIL"
    compat_versions_checked: int = 0
    compat_all_pass: bool = False
    cli_commands_registered: int = 0
    gui_tabs_registered: int = 0
    fixtures_audited: int = 0
    scenarios_audited: int = 0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


def get_all_model_names() -> List[str]:
    return [
        "StableRollupVersionEntry",
        "StableRollupCompatResult",
        "StableRollupAuditResult",
        "StableRollupHealthSummary",
        "StableRollupReport",
    ]
