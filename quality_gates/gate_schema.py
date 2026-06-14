"""
quality_gates.gate_schema — Data schemas for Coverage Quality Gates v1.1.4

Research-only. Defines dataclasses for gate inputs, decisions, universe
summaries, and override records. No broker connectivity. No order placement.
"""
from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_DISABLED = True

# ---------------------------------------------------------------------------
# Gate level constants
# ---------------------------------------------------------------------------
GATE_LEVEL_FORMAL = "FORMAL"
GATE_LEVEL_OBSERVATIONAL = "OBSERVATIONAL"
GATE_LEVEL_DEMO = "DEMO"
GATE_LEVEL_BLOCKED = "BLOCKED"

# ---------------------------------------------------------------------------
# Decision constants
# ---------------------------------------------------------------------------
DECISION_ELIGIBLE_FORMAL = "ELIGIBLE_FORMAL"
DECISION_ELIGIBLE_OBSERVATIONAL = "ELIGIBLE_OBSERVATIONAL"
DECISION_DEMO_ONLY = "DEMO_ONLY"
DECISION_BLOCKED_DATA_QUALITY = "BLOCKED_DATA_QUALITY"
DECISION_BLOCKED_FRESHNESS = "BLOCKED_FRESHNESS"
DECISION_BLOCKED_CONFLICT = "BLOCKED_CONFLICT"
DECISION_BLOCKED_INVALID_DATA = "BLOCKED_INVALID_DATA"
DECISION_BLOCKED_MOCK_DATA = "BLOCKED_MOCK_DATA"
DECISION_BLOCKED_INSUFFICIENT_HISTORY = "BLOCKED_INSUFFICIENT_HISTORY"
DECISION_BLOCKED_MISSING_PRICE = "BLOCKED_MISSING_PRICE"
DECISION_BLOCKED_SOURCE_UNKNOWN = "BLOCKED_SOURCE_UNKNOWN"

# ---------------------------------------------------------------------------
# Confidence constants
# ---------------------------------------------------------------------------
CONFIDENCE_RELIABLE = "RELIABLE"
CONFIDENCE_OBSERVATIONAL = "OBSERVATIONAL"
CONFIDENCE_INSUFFICIENT = "INSUFFICIENT"
CONFIDENCE_DEMO_ONLY = "DEMO_ONLY"
CONFIDENCE_UNKNOWN = "UNKNOWN"

# ---------------------------------------------------------------------------
# Reason codes
# ---------------------------------------------------------------------------
RC_PRICE_DATA_MISSING = "PRICE_DATA_MISSING"
RC_HISTORY_INSUFFICIENT = "HISTORY_INSUFFICIENT"
RC_DAILY_COMPLETENESS_LOW = "DAILY_COMPLETENESS_LOW"
RC_INVALID_OHLC = "INVALID_OHLC"
RC_INVALID_VOLUME = "INVALID_VOLUME"
RC_DUPLICATE_ROWS = "DUPLICATE_ROWS"
RC_CONFLICTING_ROWS = "CONFLICTING_ROWS"
RC_FUTURE_DATE = "FUTURE_DATE"
RC_DATE_REGRESSION = "DATE_REGRESSION"
RC_DAILY_PRICE_STALE = "DAILY_PRICE_STALE"
RC_SOURCE_INTERRUPTED = "SOURCE_INTERRUPTED"
RC_SOURCE_UNKNOWN = "SOURCE_UNKNOWN"
RC_CRITICAL_REPAIR_OPEN = "CRITICAL_REPAIR_OPEN"
RC_MANUAL_REVIEW_OPEN = "MANUAL_REVIEW_OPEN"
RC_MOCK_SOURCE = "MOCK_SOURCE"
RC_FIXTURE_SOURCE = "FIXTURE_SOURCE"
RC_CHIPS_MISSING = "CHIPS_MISSING"
RC_REVENUE_MISSING = "REVENUE_MISSING"
RC_FUNDAMENTALS_MISSING = "FUNDAMENTALS_MISSING"
RC_SHORT_INTEREST_MISSING = "SHORT_INTEREST_MISSING"
RC_SECTOR_DATA_MISSING = "SECTOR_DATA_MISSING"
RC_CONFIDENCE_INSUFFICIENT = "CONFIDENCE_INSUFFICIENT"
RC_COVERAGE_UNKNOWN = "COVERAGE_UNKNOWN"
RC_FRESHNESS_UNKNOWN = "FRESHNESS_UNKNOWN"

# ---------------------------------------------------------------------------
# Reason code metadata
# ---------------------------------------------------------------------------
REASON_CODE_METADATA = {
    RC_PRICE_DATA_MISSING: {
        "severity": "CRITICAL",
        "blocking_by_default": True,
        "explanation": "No daily price data found",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_HISTORY_INSUFFICIENT: {
        "severity": "HIGH",
        "blocking_by_default": True,
        "explanation": "Insufficient trading day history for formal backtest",
        "safe_action": "WAIT",
    },
    RC_DAILY_COMPLETENESS_LOW: {
        "severity": "HIGH",
        "blocking_by_default": True,
        "explanation": "Daily price completeness below required minimum",
        "safe_action": "FIX_DATA",
    },
    RC_INVALID_OHLC: {
        "severity": "CRITICAL",
        "blocking_by_default": True,
        "explanation": "Invalid OHLC data detected (e.g. high < low)",
        "safe_action": "FIX_DATA",
    },
    RC_INVALID_VOLUME: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Invalid or missing volume data",
        "safe_action": "FIX_DATA",
    },
    RC_DUPLICATE_ROWS: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Duplicate date rows detected",
        "safe_action": "FIX_DATA",
    },
    RC_CONFLICTING_ROWS: {
        "severity": "CRITICAL",
        "blocking_by_default": True,
        "explanation": "Conflicting price rows for same date",
        "safe_action": "REVIEW",
    },
    RC_FUTURE_DATE: {
        "severity": "CRITICAL",
        "blocking_by_default": True,
        "explanation": "Future date detected in data",
        "safe_action": "FIX_DATA",
    },
    RC_DATE_REGRESSION: {
        "severity": "CRITICAL",
        "blocking_by_default": True,
        "explanation": "Date regression detected (latest date moved backward)",
        "safe_action": "FIX_DATA",
    },
    RC_DAILY_PRICE_STALE: {
        "severity": "HIGH",
        "blocking_by_default": True,
        "explanation": "Daily price is stale beyond SLA threshold",
        "safe_action": "REFRESH_COVERAGE",
    },
    RC_SOURCE_INTERRUPTED: {
        "severity": "HIGH",
        "blocking_by_default": True,
        "explanation": "Data source interruption detected",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_SOURCE_UNKNOWN: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Data source is unknown",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_CRITICAL_REPAIR_OPEN: {
        "severity": "HIGH",
        "blocking_by_default": True,
        "explanation": "Critical coverage repair issue unresolved",
        "safe_action": "FIX_DATA",
    },
    RC_MANUAL_REVIEW_OPEN: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Manual review issue pending",
        "safe_action": "REVIEW",
    },
    RC_MOCK_SOURCE: {
        "severity": "CRITICAL",
        "blocking_by_default": True,
        "explanation": "Mock/simulated data source — not formal-eligible",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_FIXTURE_SOURCE: {
        "severity": "CRITICAL",
        "blocking_by_default": True,
        "explanation": "Test fixture data — not formal-eligible",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_CHIPS_MISSING: {
        "severity": "LOW",
        "blocking_by_default": False,
        "explanation": "Chips (institutional flow) data missing",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_REVENUE_MISSING: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Revenue data missing",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_FUNDAMENTALS_MISSING: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Fundamental data missing",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_SHORT_INTEREST_MISSING: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Short interest data missing",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_SECTOR_DATA_MISSING: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Sector classification data missing",
        "safe_action": "PROVIDE_SOURCE_DATA",
    },
    RC_CONFIDENCE_INSUFFICIENT: {
        "severity": "MEDIUM",
        "blocking_by_default": False,
        "explanation": "Statistical confidence is insufficient for formal use",
        "safe_action": "BACKTEST_MORE",
    },
    RC_COVERAGE_UNKNOWN: {
        "severity": "LOW",
        "blocking_by_default": False,
        "explanation": "Coverage status unknown — run universe-coverage",
        "safe_action": "REFRESH_COVERAGE",
    },
    RC_FRESHNESS_UNKNOWN: {
        "severity": "LOW",
        "blocking_by_default": False,
        "explanation": "Freshness status unknown — run freshness-scan",
        "safe_action": "REFRESH_COVERAGE",
    },
}

SAFE_ACTIONS = [
    "REVIEW",
    "FIX_DATA",
    "READ_REPORT",
    "BACKTEST_MORE",
    "KEEP_OBSERVING",
    "WAIT",
    "PROVIDE_SOURCE_DATA",
    "REFRESH_COVERAGE",
]


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _to_json_str(value) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value)
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
class QualityGateInput:
    """Input data bundle for a single symbol quality gate evaluation."""

    symbol: str
    name: str = ""
    tier: str = "unknown"
    mode: str = "real"
    source_type: str = "unknown"

    # Daily price coverage
    daily_status: str = "UNKNOWN"
    daily_rows: int = 0
    daily_completeness: float = 0.0
    first_date: str = ""
    last_date: str = ""
    trading_days: int = 0
    missing_ratio: float = 0.0

    # Integrity
    duplicate_count: int = 0
    conflict_count: int = 0
    invalid_ohlc_count: int = 0
    invalid_volume_count: int = 0
    future_date_detected: bool = False
    date_regression_detected: bool = False

    # Freshness
    freshness_status: str = "UNKNOWN"
    trading_day_lag: int = -1
    source_health: str = "UNKNOWN"

    # Optional datasets
    chips_status: str = "UNKNOWN"
    revenue_status: str = "UNKNOWN"
    fundamental_status: str = "UNKNOWN"

    # Repair / review
    open_repair_issue_count: int = 0
    critical_repair_issue_count: int = 0
    unresolved_manual_review_count: int = 0

    # Statistical
    statistical_confidence: str = "UNKNOWN"
    data_origin: str = "UNKNOWN"
    mock_detected: bool = False

    # Evidence notes
    evidence: str = dc_field(default="", metadata={"description": "evidence notes"})

    # Safety constants
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "tier": self.tier,
            "mode": self.mode,
            "source_type": self.source_type,
            "daily_status": self.daily_status,
            "daily_rows": self.daily_rows,
            "daily_completeness": self.daily_completeness,
            "first_date": self.first_date,
            "last_date": self.last_date,
            "trading_days": self.trading_days,
            "missing_ratio": self.missing_ratio,
            "duplicate_count": self.duplicate_count,
            "conflict_count": self.conflict_count,
            "invalid_ohlc_count": self.invalid_ohlc_count,
            "invalid_volume_count": self.invalid_volume_count,
            "future_date_detected": self.future_date_detected,
            "date_regression_detected": self.date_regression_detected,
            "freshness_status": self.freshness_status,
            "trading_day_lag": self.trading_day_lag,
            "source_health": self.source_health,
            "chips_status": self.chips_status,
            "revenue_status": self.revenue_status,
            "fundamental_status": self.fundamental_status,
            "open_repair_issue_count": self.open_repair_issue_count,
            "critical_repair_issue_count": self.critical_repair_issue_count,
            "unresolved_manual_review_count": self.unresolved_manual_review_count,
            "statistical_confidence": self.statistical_confidence,
            "data_origin": self.data_origin,
            "mock_detected": self.mock_detected,
            "evidence": self.evidence,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "QualityGateInput":
        return cls(
            symbol=d.get("symbol", ""),
            name=d.get("name", ""),
            tier=d.get("tier", "unknown"),
            mode=d.get("mode", "real"),
            source_type=d.get("source_type", "unknown"),
            daily_status=d.get("daily_status", "UNKNOWN"),
            daily_rows=int(d.get("daily_rows", 0)),
            daily_completeness=float(d.get("daily_completeness", 0.0)),
            first_date=d.get("first_date", ""),
            last_date=d.get("last_date", ""),
            trading_days=int(d.get("trading_days", 0)),
            missing_ratio=float(d.get("missing_ratio", 0.0)),
            duplicate_count=int(d.get("duplicate_count", 0)),
            conflict_count=int(d.get("conflict_count", 0)),
            invalid_ohlc_count=int(d.get("invalid_ohlc_count", 0)),
            invalid_volume_count=int(d.get("invalid_volume_count", 0)),
            future_date_detected=bool(d.get("future_date_detected", False)),
            date_regression_detected=bool(d.get("date_regression_detected", False)),
            freshness_status=d.get("freshness_status", "UNKNOWN"),
            trading_day_lag=int(d.get("trading_day_lag", -1)),
            source_health=d.get("source_health", "UNKNOWN"),
            chips_status=d.get("chips_status", "UNKNOWN"),
            revenue_status=d.get("revenue_status", "UNKNOWN"),
            fundamental_status=d.get("fundamental_status", "UNKNOWN"),
            open_repair_issue_count=int(d.get("open_repair_issue_count", 0)),
            critical_repair_issue_count=int(d.get("critical_repair_issue_count", 0)),
            unresolved_manual_review_count=int(d.get("unresolved_manual_review_count", 0)),
            statistical_confidence=d.get("statistical_confidence", "UNKNOWN"),
            data_origin=d.get("data_origin", "UNKNOWN"),
            mock_detected=bool(d.get("mock_detected", False)),
            evidence=d.get("evidence", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


@dataclass
class QualityGateDecision:
    """Result of a quality gate evaluation for a single symbol."""

    symbol: str
    gate_name: str
    decision_id: str = dc_field(default="")
    gate_level: str = GATE_LEVEL_BLOCKED
    eligible: bool = False
    decision: str = DECISION_BLOCKED_DATA_QUALITY
    confidence: str = CONFIDENCE_UNKNOWN
    reason_codes: list = dc_field(default_factory=list)
    reasons: list = dc_field(default_factory=list)
    warnings: list = dc_field(default_factory=list)
    required_actions: list = dc_field(default_factory=list)
    blocking_issues: list = dc_field(default_factory=list)
    optional_issues: list = dc_field(default_factory=list)
    evaluated_at: str = ""
    policy_version: str = "1.1.4"
    overridden: bool = False
    override_reason: str = ""
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.decision_id:
            self.decision_id = _new_uuid()
        if not self.evaluated_at:
            self.evaluated_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "decision_id": self.decision_id,
            "symbol": self.symbol,
            "gate_name": self.gate_name,
            "gate_level": self.gate_level,
            "eligible": self.eligible,
            "decision": self.decision,
            "confidence": self.confidence,
            "reason_codes": _to_json_str(self.reason_codes),
            "reasons": _to_json_str(self.reasons),
            "warnings": _to_json_str(self.warnings),
            "required_actions": _to_json_str(self.required_actions),
            "blocking_issues": _to_json_str(self.blocking_issues),
            "optional_issues": _to_json_str(self.optional_issues),
            "evaluated_at": self.evaluated_at,
            "policy_version": self.policy_version,
            "overridden": self.overridden,
            "override_reason": self.override_reason,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "QualityGateDecision":
        obj = cls(
            symbol=d.get("symbol", ""),
            gate_name=d.get("gate_name", ""),
            decision_id=d.get("decision_id", ""),
            gate_level=d.get("gate_level", GATE_LEVEL_BLOCKED),
            eligible=str(d.get("eligible", "False")).lower() in ("true", "1"),
            decision=d.get("decision", DECISION_BLOCKED_DATA_QUALITY),
            confidence=d.get("confidence", CONFIDENCE_UNKNOWN),
            reason_codes=_from_json_list(d.get("reason_codes", "[]")),
            reasons=_from_json_list(d.get("reasons", "[]")),
            warnings=_from_json_list(d.get("warnings", "[]")),
            required_actions=_from_json_list(d.get("required_actions", "[]")),
            blocking_issues=_from_json_list(d.get("blocking_issues", "[]")),
            optional_issues=_from_json_list(d.get("optional_issues", "[]")),
            evaluated_at=d.get("evaluated_at", ""),
            policy_version=d.get("policy_version", "1.1.4"),
            overridden=str(d.get("overridden", "False")).lower() in ("true", "1"),
            override_reason=d.get("override_reason", ""),
            research_only=str(d.get("research_only", "True")).lower() in ("true", "1"),
            no_real_orders=str(d.get("no_real_orders", "True")).lower() in ("true", "1"),
        )
        return obj


@dataclass
class UniverseGateSummary:
    """Aggregated quality gate summary for a universe tier."""

    universe_id: str = ""
    tier: str = "unknown"
    registered_symbols: int = 0
    evaluated_symbols: int = 0
    formal_eligible: int = 0
    observational_eligible: int = 0
    demo_only: int = 0
    blocked: int = 0
    ready_ratio: float = 0.0
    formal_ratio: float = 0.0
    critical_issue_count: int = 0
    gate_level: str = GATE_LEVEL_BLOCKED
    statistical_confidence: str = CONFIDENCE_UNKNOWN
    reasons: list = dc_field(default_factory=list)
    generated_at: str = ""
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = _now_utc()
        if not self.universe_id:
            self.universe_id = _new_uuid()

    def to_dict(self) -> dict:
        return {
            "universe_id": self.universe_id,
            "tier": self.tier,
            "registered_symbols": self.registered_symbols,
            "evaluated_symbols": self.evaluated_symbols,
            "formal_eligible": self.formal_eligible,
            "observational_eligible": self.observational_eligible,
            "demo_only": self.demo_only,
            "blocked": self.blocked,
            "ready_ratio": self.ready_ratio,
            "formal_ratio": self.formal_ratio,
            "critical_issue_count": self.critical_issue_count,
            "gate_level": self.gate_level,
            "statistical_confidence": self.statistical_confidence,
            "reasons": _to_json_str(self.reasons),
            "generated_at": self.generated_at,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseGateSummary":
        obj = cls(
            universe_id=d.get("universe_id", ""),
            tier=d.get("tier", "unknown"),
            registered_symbols=int(d.get("registered_symbols", 0)),
            evaluated_symbols=int(d.get("evaluated_symbols", 0)),
            formal_eligible=int(d.get("formal_eligible", 0)),
            observational_eligible=int(d.get("observational_eligible", 0)),
            demo_only=int(d.get("demo_only", 0)),
            blocked=int(d.get("blocked", 0)),
            ready_ratio=float(d.get("ready_ratio", 0.0)),
            formal_ratio=float(d.get("formal_ratio", 0.0)),
            critical_issue_count=int(d.get("critical_issue_count", 0)),
            gate_level=d.get("gate_level", GATE_LEVEL_BLOCKED),
            statistical_confidence=d.get("statistical_confidence", CONFIDENCE_UNKNOWN),
            reasons=_from_json_list(d.get("reasons", "[]")),
            generated_at=d.get("generated_at", ""),
            research_only=str(d.get("research_only", "True")).lower() in ("true", "1"),
            no_real_orders=str(d.get("no_real_orders", "True")).lower() in ("true", "1"),
        )
        return obj


@dataclass
class GateOverrideRecord:
    """Audit record for a gate override request."""

    override_id: str = dc_field(default="")
    decision_id: str = ""
    symbol: str = ""
    original_decision: str = ""
    requested_decision: str = ""
    requested_by: str = "researcher"
    requested_at: str = ""
    reason: str = ""
    approved: bool = False
    approval_note: str = ""
    expires_at: str = ""
    audit_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def __post_init__(self):
        if not self.override_id:
            self.override_id = _new_uuid()
        if not self.requested_at:
            self.requested_at = _now_utc()

    def to_dict(self) -> dict:
        return {
            "override_id": self.override_id,
            "decision_id": self.decision_id,
            "symbol": self.symbol,
            "original_decision": self.original_decision,
            "requested_decision": self.requested_decision,
            "requested_by": self.requested_by,
            "requested_at": self.requested_at,
            "reason": self.reason,
            "approved": self.approved,
            "approval_note": self.approval_note,
            "expires_at": self.expires_at,
            "audit_only": self.audit_only,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GateOverrideRecord":
        return cls(
            override_id=d.get("override_id", ""),
            decision_id=d.get("decision_id", ""),
            symbol=d.get("symbol", ""),
            original_decision=d.get("original_decision", ""),
            requested_decision=d.get("requested_decision", ""),
            requested_by=d.get("requested_by", "researcher"),
            requested_at=d.get("requested_at", ""),
            reason=d.get("reason", ""),
            approved=str(d.get("approved", "False")).lower() in ("true", "1"),
            approval_note=d.get("approval_note", ""),
            expires_at=d.get("expires_at", ""),
            audit_only=str(d.get("audit_only", "True")).lower() in ("true", "1"),
            research_only=str(d.get("research_only", "True")).lower() in ("true", "1"),
            no_real_orders=str(d.get("no_real_orders", "True")).lower() in ("true", "1"),
        )
