"""data_freshness/models_v134.py — v1.3.4 Data Freshness Monitor models.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Auto Refresh DISABLED. Auto Repair DISABLED. Mock Fallback DISABLED.
[!] Future timestamp does not count as fresh.
[!] Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FRESHNESS_AUTO_REFRESH_ENABLED = False
FRESHNESS_AUTO_REPAIR_ENABLED = False
FRESHNESS_MOCK_FALLBACK_ENABLED = False


class FreshnessStatus:
    FRESH = "FRESH"
    NEAR_STALE = "NEAR_STALE"
    STALE = "STALE"
    CRITICALLY_STALE = "CRITICALLY_STALE"
    NEVER_RECEIVED = "NEVER_RECEIVED"
    FUTURE_TIMESTAMP = "FUTURE_TIMESTAMP"
    INVALID_TIMESTAMP = "INVALID_TIMESTAMP"
    MARKET_CLOSED_VALID = "MARKET_CLOSED_VALID"
    NON_TRADING_DAY_VALID = "NON_TRADING_DAY_VALID"
    PROVIDER_DELAYED = "PROVIDER_DELAYED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    DEMO_ONLY = "DEMO_ONLY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def is_ok(cls, s: str) -> bool:
        return s in {cls.FRESH, cls.NEAR_STALE, cls.MARKET_CLOSED_VALID, cls.NON_TRADING_DAY_VALID}

    @classmethod
    def is_stale(cls, s: str) -> bool:
        return s in {cls.STALE, cls.CRITICALLY_STALE}

    @classmethod
    def is_blocking(cls, s: str) -> bool:
        return s in {
            cls.CRITICALLY_STALE, cls.NEVER_RECEIVED, cls.FUTURE_TIMESTAMP,
            cls.INVALID_TIMESTAMP, cls.BLOCKED,
        }


class DatasetType:
    SYMBOL_MASTER = "SYMBOL_MASTER"
    DAILY_OHLCV = "DAILY_OHLCV"
    INTRADAY_OHLCV = "INTRADAY_OHLCV"
    QUOTE = "QUOTE"
    INSTITUTIONAL = "INSTITUTIONAL"
    MARGIN = "MARGIN"
    MONTHLY_REVENUE = "MONTHLY_REVENUE"
    FINANCIAL_STATEMENT = "FINANCIAL_STATEMENT"
    SHAREHOLDER_DISTRIBUTION = "SHAREHOLDER_DISTRIBUTION"
    ETF_CONSTITUENTS = "ETF_CONSTITUENTS"
    CORPORATE_ACTIONS = "CORPORATE_ACTIONS"
    TRADING_CALENDAR = "TRADING_CALENDAR"
    MARKET_INDEX = "MARKET_INDEX"
    FUTURES_RISK = "FUTURES_RISK"
    INDUSTRY_METADATA = "INDUSTRY_METADATA"
    TECHNICAL_INDICATORS = "TECHNICAL_INDICATORS"
    PROVIDER_HEALTH = "PROVIDER_HEALTH"
    CACHE_ENTRY = "CACHE_ENTRY"

    CAPABILITY_MAP = {
        "DAILY_OHLCV": "DAILY_OHLCV",
        "INTRADAY_OHLCV": "INTRADAY_OHLCV",
        "QUOTE": "QUOTE",
        "INSTITUTIONAL": "INSTITUTIONAL",
        "MARGIN": "MARGIN",
        "MONTHLY_REVENUE": "MONTHLY_REVENUE",
        "FINANCIAL_STATEMENT": "FINANCIAL_STATEMENT",
        "SHAREHOLDER_DISTRIBUTION": "SHAREHOLDER_DISTRIBUTION",
        "ETF_CONSTITUENTS": "ETF_CONSTITUENTS",
        "CORPORATE_ACTIONS": "CORPORATE_ACTIONS",
        "TRADING_CALENDAR": "TRADING_CALENDAR",
        "MARKET_INDEX": "MARKET_INDEX",
        "FUTURES_RISK": "FUTURES_RISK",
        "INDUSTRY_METADATA": "INDUSTRY_METADATA",
        "SYMBOL_MASTER": "SYMBOL_MASTER",
    }

    @classmethod
    def all_types(cls) -> List[str]:
        return [v for k, v in cls.__dict__.items() if not k.startswith("_") and isinstance(v, str)]


class FreshnessSeverity:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ProviderSLAStatus:
    HEALTHY = "HEALTHY"
    DELAYED = "DELAYED"
    DEGRADED = "DEGRADED"
    BREACHED = "BREACHED"
    UNAVAILABLE = "UNAVAILABLE"
    DISABLED = "DISABLED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    UNKNOWN = "UNKNOWN"


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


@dataclass
class FreshnessRecord:
    record_id: str = ""
    symbol: str = ""
    market: str = ""
    dataset_type: str = DatasetType.DAILY_OHLCV
    provider_id: Optional[str] = None
    data_mode: str = "REAL"
    observed_timestamp: Optional[str] = None
    source_timestamp: Optional[str] = None
    fetched_at: Optional[str] = None
    evaluated_at: str = field(default_factory=_now_iso)
    expected_latest_timestamp: Optional[str] = None
    age_seconds: Optional[float] = None
    age_trading_days: Optional[float] = None
    freshness_status: str = FreshnessStatus.UNKNOWN
    severity: str = FreshnessSeverity.INFO
    policy_id: str = ""
    stale_after_seconds: Optional[float] = None
    critical_after_seconds: Optional[float] = None
    near_stale_threshold_seconds: Optional[float] = None
    market_open: bool = False
    trading_day: bool = False
    previous_trading_day: Optional[str] = None
    next_trading_day: Optional[str] = None
    provider_status: Optional[str] = None
    cache_status: Optional[str] = None
    quality_status: Optional[str] = None
    coverage_status: Optional[str] = None
    blocks_analysis: bool = False
    precise_price_allowed: bool = False
    backtest_allowed: bool = False
    abc_buy_point_allowed: bool = False
    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FreshnessRecord":
        known = {f.name for f in __import__("dataclasses").fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class FreshnessPolicy:
    policy_id: str = ""
    dataset_type: str = DatasetType.DAILY_OHLCV
    market: str = "TWSE"
    trading_session_sensitive: bool = True
    update_frequency: str = "DAILY"
    near_stale_ratio: float = 0.8
    stale_after: float = 86400.0
    critical_after: float = 172800.0
    allowed_market_close_delay: float = 7200.0
    allowed_non_trading_day_delay: float = 259200.0
    provider_sla_seconds: float = 3600.0
    blocking_profiles: List[str] = field(default_factory=list)
    enabled: bool = True
    source: str = "DEFAULT"
    version: str = "1.3.4"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FreshnessPolicy":
        known = {f.name for f in __import__("dataclasses").fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class ProviderSLARecord:
    provider_id: str = ""
    capability: str = ""
    market: str = ""
    expected_interval: float = 86400.0
    last_success_at: Optional[str] = None
    last_failure_at: Optional[str] = None
    consecutive_failures: int = 0
    latency_seconds: Optional[float] = None
    data_delay_seconds: Optional[float] = None
    availability_ratio: float = 1.0
    status: str = ProviderSLAStatus.UNKNOWN
    severity: str = FreshnessSeverity.INFO
    breached: bool = False
    breach_reasons: List[str] = field(default_factory=list)
    evaluated_at: str = field(default_factory=_now_iso)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ProviderSLARecord":
        known = {f.name for f in __import__("dataclasses").fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class FreshnessAlert:
    alert_id: str = ""
    dedup_key: str = ""
    symbol: str = ""
    dataset_type: str = ""
    provider_id: Optional[str] = None
    status: str = "OPEN"
    severity: str = FreshnessSeverity.WARNING
    title: str = ""
    message: str = ""
    first_seen_at: str = field(default_factory=_now_iso)
    last_seen_at: str = field(default_factory=_now_iso)
    occurrence_count: int = 1
    acknowledged: bool = False
    resolved: bool = False
    blocks_analysis: bool = False
    repair_task_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def build_dedup_key(self) -> str:
        parts = [self.symbol, self.dataset_type, self.provider_id or "", self.status, ""]
        return "|".join(str(p) for p in parts)

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FreshnessAlert":
        known = {f.name for f in __import__("dataclasses").fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class DailyFreshnessSummary:
    generated_at: str = field(default_factory=_now_iso)
    trading_day: bool = False
    market_open: bool = False
    symbols_scanned: int = 0
    datasets_scanned: int = 0
    fresh_count: int = 0
    near_stale_count: int = 0
    stale_count: int = 0
    critically_stale_count: int = 0
    never_received_count: int = 0
    provider_delayed_count: int = 0
    blocked_count: int = 0
    core_symbols_affected: int = 0
    precise_price_blocked_count: int = 0
    backtest_blocked_count: int = 0
    abc_blocked_count: int = 0
    providers_healthy: int = 0
    providers_delayed: int = 0
    providers_breached: int = 0
    active_alerts: int = 0
    repair_candidates: int = 0
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)
