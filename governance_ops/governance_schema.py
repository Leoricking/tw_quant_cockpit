"""
governance_ops.governance_schema — Data schemas for Data Governance Operations Dashboard v1.1.6

Research-only. Defines dataclasses for module status, symbol status, action items,
governance summary, and run summaries.
No broker connectivity. No order placement.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Dashboard does NOT auto-repair, auto-download, override gates, or enable trading.
"""
from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _to_json_str(value) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value) if value is not None else ""


def _from_json_list(value, default=None) -> list:
    if default is None:
        default = []
    if isinstance(value, list):
        return value
    if not value:
        return default
    try:
        result = json.loads(value)
        return result if isinstance(result, list) else default
    except (json.JSONDecodeError, TypeError):
        return default


def _from_json_dict(value, default=None) -> dict:
    if default is None:
        default = {}
    if isinstance(value, dict):
        return value
    if not value:
        return default
    try:
        result = json.loads(value)
        return result if isinstance(result, dict) else default
    except (json.JSONDecodeError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class GovernanceModuleStatus:
    """Status of a single governance module."""

    module_name: str  # UNIVERSE/ONBOARDING/COVERAGE_REPAIR/FRESHNESS/QUALITY_GATES/GATE_ENFORCEMENT/REPORT_PACK/KNOWLEDGE_BASE/LOCAL_ASSISTANT/RELEASE_GATE
    available: bool
    health_status: str  # PASS/WARN/FAIL/BLOCKED/UNAVAILABLE
    pass_count: int = 0
    warn_count: int = 0
    fail_count: int = 0
    blocked_count: int = 0
    latest_run_at: Optional[str] = None
    latest_output: Optional[str] = None
    reason: str = ""
    version: str = ""
    stale: bool = False
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "module_name": self.module_name,
            "available": self.available,
            "health_status": self.health_status,
            "pass_count": self.pass_count,
            "warn_count": self.warn_count,
            "fail_count": self.fail_count,
            "blocked_count": self.blocked_count,
            "latest_run_at": self.latest_run_at or "",
            "latest_output": self.latest_output or "",
            "reason": self.reason,
            "version": self.version,
            "stale": self.stale,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GovernanceModuleStatus":
        return cls(
            module_name=d.get("module_name", "UNKNOWN"),
            available=bool(d.get("available", False)),
            health_status=d.get("health_status", "UNAVAILABLE"),
            pass_count=int(d.get("pass_count", 0)),
            warn_count=int(d.get("warn_count", 0)),
            fail_count=int(d.get("fail_count", 0)),
            blocked_count=int(d.get("blocked_count", 0)),
            latest_run_at=d.get("latest_run_at") or None,
            latest_output=d.get("latest_output") or None,
            reason=d.get("reason", ""),
            version=d.get("version", ""),
            stale=bool(d.get("stale", False)),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class GovernanceSymbolStatus:
    """Governance status for a single symbol."""

    symbol: str
    name: str = ""
    tier: str = ""
    coverage_status: str = "UNKNOWN"
    freshness_status: str = "UNKNOWN"
    quality_gate_level: str = "UNKNOWN"
    qualification: str = "NOT_QUALIFIED"
    source_health: str = "UNKNOWN"
    open_repair_issues: int = 0
    critical_repair_issues: int = 0
    manual_review_count: int = 0
    source_required_count: int = 0
    import_failure_count: int = 0
    conflict_count: int = 0
    invalid_count: int = 0
    latest_data_date: Optional[str] = None
    trading_day_lag: int = 0
    formal_eligible: bool = False
    observational_eligible: bool = False
    blocked: bool = False
    top_reason_codes: List[str] = dc_field(default_factory=list)
    priority: str = "P3"
    required_actions: List[str] = dc_field(default_factory=list)
    updated_at: str = ""

    def __post_init__(self):
        if not self.updated_at:
            self.updated_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "tier": self.tier,
            "coverage_status": self.coverage_status,
            "freshness_status": self.freshness_status,
            "quality_gate_level": self.quality_gate_level,
            "qualification": self.qualification,
            "source_health": self.source_health,
            "open_repair_issues": self.open_repair_issues,
            "critical_repair_issues": self.critical_repair_issues,
            "manual_review_count": self.manual_review_count,
            "source_required_count": self.source_required_count,
            "import_failure_count": self.import_failure_count,
            "conflict_count": self.conflict_count,
            "invalid_count": self.invalid_count,
            "latest_data_date": self.latest_data_date or "",
            "trading_day_lag": self.trading_day_lag,
            "formal_eligible": self.formal_eligible,
            "observational_eligible": self.observational_eligible,
            "blocked": self.blocked,
            "top_reason_codes": _to_json_str(self.top_reason_codes),
            "priority": self.priority,
            "required_actions": _to_json_str(self.required_actions),
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GovernanceSymbolStatus":
        return cls(
            symbol=d.get("symbol", ""),
            name=d.get("name", ""),
            tier=d.get("tier", ""),
            coverage_status=d.get("coverage_status", "UNKNOWN"),
            freshness_status=d.get("freshness_status", "UNKNOWN"),
            quality_gate_level=d.get("quality_gate_level", "UNKNOWN"),
            qualification=d.get("qualification", "NOT_QUALIFIED"),
            source_health=d.get("source_health", "UNKNOWN"),
            open_repair_issues=int(d.get("open_repair_issues", 0)),
            critical_repair_issues=int(d.get("critical_repair_issues", 0)),
            manual_review_count=int(d.get("manual_review_count", 0)),
            source_required_count=int(d.get("source_required_count", 0)),
            import_failure_count=int(d.get("import_failure_count", 0)),
            conflict_count=int(d.get("conflict_count", 0)),
            invalid_count=int(d.get("invalid_count", 0)),
            latest_data_date=d.get("latest_data_date") or None,
            trading_day_lag=int(d.get("trading_day_lag", 0)),
            formal_eligible=bool(d.get("formal_eligible", False)),
            observational_eligible=bool(d.get("observational_eligible", False)),
            blocked=bool(d.get("blocked", False)),
            top_reason_codes=_from_json_list(d.get("top_reason_codes", "[]")),
            priority=d.get("priority", "P3"),
            required_actions=_from_json_list(d.get("required_actions", "[]")),
            updated_at=d.get("updated_at", ""),
        )


@dataclass
class GovernanceActionItem:
    """A prioritized action item for governance operations."""

    action_id: str
    priority: str  # P0/P1/P2/P3
    action_type: str  # IMPORT_RETRY/FIX_MAPPING/REVIEW_CONFLICT/REVIEW_INVALID_DATA/PROVIDE_SOURCE_DATA/...
    symbol: Optional[str]
    dataset: str = ""
    source: str = ""
    title: str = ""
    description: str = ""
    reason_codes: List[str] = dc_field(default_factory=list)
    source_module: str = ""
    source_record_id: str = ""
    status: str = "OPEN"  # OPEN/ACKNOWLEDGED/IN_PROGRESS/RESOLVED/BLOCKED/DEFERRED/WONT_FIX
    safe_action: str = "REVIEW"  # REVIEW/FIX_DATA/READ_REPORT/PROVIDE_SOURCE_DATA/REFRESH_COVERAGE/RETRY_IMPORT/VERIFY_AUDIT/BACKTEST_MORE/KEEP_OBSERVING/WAIT
    suggested_command: str = ""
    executable: bool = False
    requires_manual_review: bool = True
    requires_source_data: bool = False
    blocked: bool = False
    created_at: str = ""
    updated_at: str = ""
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.action_id:
            self.action_id = _new_uuid()
        if not self.created_at:
            self.created_at = _now_utc()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict:
        return {
            "action_id": self.action_id,
            "priority": self.priority,
            "action_type": self.action_type,
            "symbol": self.symbol or "",
            "dataset": self.dataset,
            "source": self.source,
            "title": self.title,
            "description": self.description,
            "reason_codes": _to_json_str(self.reason_codes),
            "source_module": self.source_module,
            "source_record_id": self.source_record_id,
            "status": self.status,
            "safe_action": self.safe_action,
            "suggested_command": self.suggested_command,
            "executable": self.executable,
            "requires_manual_review": self.requires_manual_review,
            "requires_source_data": self.requires_source_data,
            "blocked": self.blocked,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GovernanceActionItem":
        return cls(
            action_id=d.get("action_id", ""),
            priority=d.get("priority", "P3"),
            action_type=d.get("action_type", "REVIEW_INVALID_DATA"),
            symbol=d.get("symbol") or None,
            dataset=d.get("dataset", ""),
            source=d.get("source", ""),
            title=d.get("title", ""),
            description=d.get("description", ""),
            reason_codes=_from_json_list(d.get("reason_codes", "[]")),
            source_module=d.get("source_module", ""),
            source_record_id=d.get("source_record_id", ""),
            status=d.get("status", "OPEN"),
            safe_action=d.get("safe_action", "REVIEW"),
            suggested_command=d.get("suggested_command", ""),
            executable=bool(d.get("executable", False)),
            requires_manual_review=bool(d.get("requires_manual_review", True)),
            requires_source_data=bool(d.get("requires_source_data", False)),
            blocked=bool(d.get("blocked", False)),
            created_at=d.get("created_at", ""),
            updated_at=d.get("updated_at", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class GovernanceSummary:
    """Top-level governance summary across all modules and symbols."""

    generated_at: str
    mode: str
    tier: str
    module_statuses: Dict[str, Any] = dc_field(default_factory=dict)
    registered_symbols: int = 0
    evaluated_symbols: int = 0
    ready_symbols: int = 0
    partial_symbols: int = 0
    stale_symbols: int = 0
    missing_symbols: int = 0
    formal_eligible: int = 0
    observational_eligible: int = 0
    demo_only: int = 0
    blocked_symbols: int = 0
    critical_alerts: int = 0
    open_actions: int = 0
    p0_actions: int = 0
    p1_actions: int = 0
    source_interruptions: int = 0
    audit_chain_failures: int = 0
    non_qualified_runs: int = 0
    overall_status: str = "UNKNOWN"  # HEALTHY/DEGRADED/ATTENTION_REQUIRED/CRITICAL/UNKNOWN
    confidence: float = 0.0
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "generated_at": self.generated_at,
            "mode": self.mode,
            "tier": self.tier,
            "module_statuses": _to_json_str(self.module_statuses),
            "registered_symbols": self.registered_symbols,
            "evaluated_symbols": self.evaluated_symbols,
            "ready_symbols": self.ready_symbols,
            "partial_symbols": self.partial_symbols,
            "stale_symbols": self.stale_symbols,
            "missing_symbols": self.missing_symbols,
            "formal_eligible": self.formal_eligible,
            "observational_eligible": self.observational_eligible,
            "demo_only": self.demo_only,
            "blocked_symbols": self.blocked_symbols,
            "critical_alerts": self.critical_alerts,
            "open_actions": self.open_actions,
            "p0_actions": self.p0_actions,
            "p1_actions": self.p1_actions,
            "source_interruptions": self.source_interruptions,
            "audit_chain_failures": self.audit_chain_failures,
            "non_qualified_runs": self.non_qualified_runs,
            "overall_status": self.overall_status,
            "confidence": self.confidence,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GovernanceSummary":
        return cls(
            generated_at=d.get("generated_at", ""),
            mode=d.get("mode", "real"),
            tier=d.get("tier", ""),
            module_statuses=_from_json_dict(d.get("module_statuses", "{}")),
            registered_symbols=int(d.get("registered_symbols", 0)),
            evaluated_symbols=int(d.get("evaluated_symbols", 0)),
            ready_symbols=int(d.get("ready_symbols", 0)),
            partial_symbols=int(d.get("partial_symbols", 0)),
            stale_symbols=int(d.get("stale_symbols", 0)),
            missing_symbols=int(d.get("missing_symbols", 0)),
            formal_eligible=int(d.get("formal_eligible", 0)),
            observational_eligible=int(d.get("observational_eligible", 0)),
            demo_only=int(d.get("demo_only", 0)),
            blocked_symbols=int(d.get("blocked_symbols", 0)),
            critical_alerts=int(d.get("critical_alerts", 0)),
            open_actions=int(d.get("open_actions", 0)),
            p0_actions=int(d.get("p0_actions", 0)),
            p1_actions=int(d.get("p1_actions", 0)),
            source_interruptions=int(d.get("source_interruptions", 0)),
            audit_chain_failures=int(d.get("audit_chain_failures", 0)),
            non_qualified_runs=int(d.get("non_qualified_runs", 0)),
            overall_status=d.get("overall_status", "UNKNOWN"),
            confidence=float(d.get("confidence", 0.0)),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class GovernanceRunSummary:
    """Summary of a single gate enforcement run."""

    run_id: str
    command_name: str
    qualification: str
    included_count: int
    excluded_count: int
    override_used: bool
    audit_chain_valid: bool
    reproducibility_verified: bool
    report_output: str
    created_at: str

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "command_name": self.command_name,
            "qualification": self.qualification,
            "included_count": self.included_count,
            "excluded_count": self.excluded_count,
            "override_used": self.override_used,
            "audit_chain_valid": self.audit_chain_valid,
            "reproducibility_verified": self.reproducibility_verified,
            "report_output": self.report_output,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GovernanceRunSummary":
        return cls(
            run_id=d.get("run_id", ""),
            command_name=d.get("command_name", ""),
            qualification=d.get("qualification", ""),
            included_count=int(d.get("included_count", 0)),
            excluded_count=int(d.get("excluded_count", 0)),
            override_used=bool(d.get("override_used", False)),
            audit_chain_valid=bool(d.get("audit_chain_valid", True)),
            reproducibility_verified=bool(d.get("reproducibility_verified", False)),
            report_output=d.get("report_output", ""),
            created_at=d.get("created_at", ""),
        )
