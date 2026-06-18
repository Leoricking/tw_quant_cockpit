"""
replay/stable_schema.py — Stable rollup schema dataclasses for v1.2.9.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


@dataclass
class StableModuleInfo:
    """Info record for a single replay stable module.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    module_name: str
    introduced_version: str
    current_version: str = "1.2.9"
    status: str = "STABLE"
    health_command: str = ""
    cli_available: bool = True
    gui_available: bool = True
    report_available: bool = True
    backward_compatible: bool = True
    no_real_orders: bool = True
    research_only: bool = True
    notes: str = ""


@dataclass
class StableCapability:
    """A single auditable capability in the stable matrix.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    capability_id: str
    module: str
    introduced_version: str
    current_status: str = "STABLE"   # STABLE | AVAILABLE | LIMITED | OPTIONAL
    health_command: str = ""
    CLI_available: bool = True
    GUI_available: bool = True
    report_available: bool = True
    backward_compatible: bool = True
    safety_qualified: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    notes: str = ""


@dataclass
class StableManifest:
    """Full stable release manifest for v1.2.9.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    release_version: str = "1.2.9"
    release_name: str = "Replay Training Stable Rollup"
    base_release: str = "1.2.8 Replay Dataset & Session Registry"
    generated_at: str = ""
    modules: List[str] = field(default_factory=list)
    capabilities: List[dict] = field(default_factory=list)
    safety_flags: Dict[str, Any] = field(default_factory=dict)
    CLI_commands: List[str] = field(default_factory=list)
    health_checks: List[str] = field(default_factory=list)
    schema_versions: Dict[str, str] = field(default_factory=dict)
    store_paths: List[str] = field(default_factory=list)
    report_types: List[str] = field(default_factory=list)
    GUI_tabs: List[str] = field(default_factory=list)
    backward_compatibility_range: List[str] = field(default_factory=list)
    known_warnings: List[str] = field(default_factory=list)
    no_real_orders: bool = True
    broker_disabled: bool = True
    research_only: bool = True


@dataclass
class StableContractResult:
    """Result of a single cross-module contract check.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    contract_id: str
    status: str          # PASS | WARN | FAIL
    message: str
    no_real_orders: bool = True
    research_only: bool = True


@dataclass
class StableCompatibilityResult:
    """Result of a single backward-compatibility version check.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    version: str
    status: str          # PASS | WARN | FAIL
    message: str
    no_real_orders: bool = True
    research_only: bool = True


@dataclass
class StableAuditResult:
    """Result of a single store/runtime/CLI/GUI audit check.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    audit_id: str
    category: str        # store | runtime | cli | gui | report | safety | regression
    status: str          # PASS | WARN | FAIL
    message: str
    no_real_orders: bool = True
    research_only: bool = True
