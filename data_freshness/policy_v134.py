"""data_freshness/policy_v134.py — v1.3.4 Data Freshness Policy Registry.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from data_freshness.models_v134 import DatasetType, FreshnessPolicy

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataFreshnessPolicyRegistry:
    """Registry of default freshness policies for all DatasetTypes.

    [!] Research Only. Policies define staleness thresholds — not trading signals.
    [!] No auto-refresh, no auto-repair, no mock fallback.
    """

    def __init__(self) -> None:
        self._policies: Dict[str, FreshnessPolicy] = {}
        self._build_defaults()

    def _build_defaults(self) -> None:
        """Build default policies for all known dataset types."""

        # SYMBOL_MASTER — daily refresh, not trading-session-sensitive
        self._policies[DatasetType.SYMBOL_MASTER] = FreshnessPolicy(
            policy_id="default_symbol_master",
            dataset_type=DatasetType.SYMBOL_MASTER,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,
            critical_after=172800.0,
            allowed_market_close_delay=7200.0,
            allowed_non_trading_day_delay=259200.0,
            provider_sla_seconds=3600.0,
            blocking_profiles=[],
        )

        # DAILY_OHLCV — core: stale after 1 day, critical after 2 days
        self._policies[DatasetType.DAILY_OHLCV] = FreshnessPolicy(
            policy_id="default_daily_ohlcv",
            dataset_type=DatasetType.DAILY_OHLCV,
            market="TWSE",
            trading_session_sensitive=True,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,
            critical_after=172800.0,
            allowed_market_close_delay=7200.0,
            allowed_non_trading_day_delay=259200.0,  # allow Fri data on Mon
            provider_sla_seconds=3600.0,
            blocking_profiles=["precise_price", "backtest", "abc"],
        )

        # INTRADAY_OHLCV — stale after 5 min during session, 15 min critical
        self._policies[DatasetType.INTRADAY_OHLCV] = FreshnessPolicy(
            policy_id="default_intraday_ohlcv",
            dataset_type=DatasetType.INTRADAY_OHLCV,
            market="TWSE",
            trading_session_sensitive=True,
            update_frequency="INTRADAY",
            near_stale_ratio=0.8,
            stale_after=300.0,
            critical_after=900.0,
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=86400.0,
            provider_sla_seconds=300.0,
            blocking_profiles=["precise_price"],
        )

        # QUOTE — stale after 60s during trading, 86400 after close
        self._policies[DatasetType.QUOTE] = FreshnessPolicy(
            policy_id="default_quote",
            dataset_type=DatasetType.QUOTE,
            market="TWSE",
            trading_session_sensitive=True,
            update_frequency="REALTIME",
            near_stale_ratio=0.8,
            stale_after=60.0,
            critical_after=300.0,
            allowed_market_close_delay=86400.0,
            allowed_non_trading_day_delay=86400.0,
            provider_sla_seconds=60.0,
            blocking_profiles=["precise_price"],
        )

        # INSTITUTIONAL — 6 hours post-close delay allowed
        self._policies[DatasetType.INSTITUTIONAL] = FreshnessPolicy(
            policy_id="default_institutional",
            dataset_type=DatasetType.INSTITUTIONAL,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,
            critical_after=172800.0,
            allowed_market_close_delay=21600.0,  # 6 hours post-close
            allowed_non_trading_day_delay=259200.0,
            provider_sla_seconds=7200.0,
            blocking_profiles=["backtest"],
        )

        # MARGIN — similar to institutional
        self._policies[DatasetType.MARGIN] = FreshnessPolicy(
            policy_id="default_margin",
            dataset_type=DatasetType.MARGIN,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,
            critical_after=172800.0,
            allowed_market_close_delay=21600.0,
            allowed_non_trading_day_delay=259200.0,
            provider_sla_seconds=7200.0,
            blocking_profiles=["backtest"],
        )

        # MONTHLY_REVENUE — 30 days stale, 60 days critical
        self._policies[DatasetType.MONTHLY_REVENUE] = FreshnessPolicy(
            policy_id="default_monthly_revenue",
            dataset_type=DatasetType.MONTHLY_REVENUE,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="MONTHLY",
            near_stale_ratio=0.8,
            stale_after=2592000.0,   # 30 days
            critical_after=5184000.0,  # 60 days
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=604800.0,  # 7 days
            provider_sla_seconds=86400.0,
            blocking_profiles=["backtest"],
        )

        # FINANCIAL_STATEMENT — 90 days stale, 180 days critical
        self._policies[DatasetType.FINANCIAL_STATEMENT] = FreshnessPolicy(
            policy_id="default_financial_statement",
            dataset_type=DatasetType.FINANCIAL_STATEMENT,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="QUARTERLY",
            near_stale_ratio=0.8,
            stale_after=7776000.0,    # 90 days
            critical_after=15552000.0,  # 180 days
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=604800.0,
            provider_sla_seconds=86400.0,
            blocking_profiles=["backtest"],
        )

        # SHAREHOLDER_DISTRIBUTION — 7 days
        self._policies[DatasetType.SHAREHOLDER_DISTRIBUTION] = FreshnessPolicy(
            policy_id="default_shareholder_distribution",
            dataset_type=DatasetType.SHAREHOLDER_DISTRIBUTION,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="WEEKLY",
            near_stale_ratio=0.8,
            stale_after=604800.0,    # 7 days
            critical_after=1209600.0,  # 14 days
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=172800.0,
            provider_sla_seconds=86400.0,
            blocking_profiles=[],
        )

        # ETF_CONSTITUENTS — daily
        self._policies[DatasetType.ETF_CONSTITUENTS] = FreshnessPolicy(
            policy_id="default_etf_constituents",
            dataset_type=DatasetType.ETF_CONSTITUENTS,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,
            critical_after=172800.0,
            allowed_market_close_delay=7200.0,
            allowed_non_trading_day_delay=259200.0,
            provider_sla_seconds=3600.0,
            blocking_profiles=[],
        )

        # CORPORATE_ACTIONS — 30 days; blocks backtest
        self._policies[DatasetType.CORPORATE_ACTIONS] = FreshnessPolicy(
            policy_id="default_corporate_actions",
            dataset_type=DatasetType.CORPORATE_ACTIONS,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="MONTHLY",
            near_stale_ratio=0.8,
            stale_after=2592000.0,   # 30 days
            critical_after=5184000.0,
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=604800.0,
            provider_sla_seconds=86400.0,
            blocking_profiles=["backtest"],
        )

        # TRADING_CALENDAR — daily
        self._policies[DatasetType.TRADING_CALENDAR] = FreshnessPolicy(
            policy_id="default_trading_calendar",
            dataset_type=DatasetType.TRADING_CALENDAR,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="YEARLY",
            near_stale_ratio=0.8,
            stale_after=2592000.0,   # 30 days
            critical_after=7776000.0,  # 90 days
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=604800.0,
            provider_sla_seconds=86400.0,
            blocking_profiles=[],
        )

        # MARKET_INDEX — daily
        self._policies[DatasetType.MARKET_INDEX] = FreshnessPolicy(
            policy_id="default_market_index",
            dataset_type=DatasetType.MARKET_INDEX,
            market="TWSE",
            trading_session_sensitive=True,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,
            critical_after=172800.0,
            allowed_market_close_delay=7200.0,
            allowed_non_trading_day_delay=259200.0,
            provider_sla_seconds=3600.0,
            blocking_profiles=[],
        )

        # FUTURES_RISK — daily
        self._policies[DatasetType.FUTURES_RISK] = FreshnessPolicy(
            policy_id="default_futures_risk",
            dataset_type=DatasetType.FUTURES_RISK,
            market="TWSE",
            trading_session_sensitive=True,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,
            critical_after=172800.0,
            allowed_market_close_delay=7200.0,
            allowed_non_trading_day_delay=259200.0,
            provider_sla_seconds=3600.0,
            blocking_profiles=["backtest"],
        )

        # INDUSTRY_METADATA — relatively static
        self._policies[DatasetType.INDUSTRY_METADATA] = FreshnessPolicy(
            policy_id="default_industry_metadata",
            dataset_type=DatasetType.INDUSTRY_METADATA,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="MONTHLY",
            near_stale_ratio=0.8,
            stale_after=2592000.0,
            critical_after=7776000.0,
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=604800.0,
            provider_sla_seconds=86400.0,
            blocking_profiles=[],
        )

        # TECHNICAL_INDICATORS — freshness derives from underlying OHLCV
        self._policies[DatasetType.TECHNICAL_INDICATORS] = FreshnessPolicy(
            policy_id="default_technical_indicators",
            dataset_type=DatasetType.TECHNICAL_INDICATORS,
            market="TWSE",
            trading_session_sensitive=True,
            update_frequency="DAILY",
            near_stale_ratio=0.8,
            stale_after=86400.0,    # uses base OHLCV timestamp, not calculation time
            critical_after=172800.0,
            allowed_market_close_delay=7200.0,
            allowed_non_trading_day_delay=259200.0,
            provider_sla_seconds=3600.0,
            blocking_profiles=["abc"],
        )

        # PROVIDER_HEALTH — stale after 1 hour
        self._policies[DatasetType.PROVIDER_HEALTH] = FreshnessPolicy(
            policy_id="default_provider_health",
            dataset_type=DatasetType.PROVIDER_HEALTH,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="HOURLY",
            near_stale_ratio=0.8,
            stale_after=3600.0,
            critical_after=7200.0,
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=7200.0,
            provider_sla_seconds=3600.0,
            blocking_profiles=[],
        )

        # CACHE_ENTRY — stale after 1 hour
        self._policies[DatasetType.CACHE_ENTRY] = FreshnessPolicy(
            policy_id="default_cache_entry",
            dataset_type=DatasetType.CACHE_ENTRY,
            market="TWSE",
            trading_session_sensitive=False,
            update_frequency="HOURLY",
            near_stale_ratio=0.8,
            stale_after=3600.0,
            critical_after=7200.0,
            allowed_market_close_delay=0.0,
            allowed_non_trading_day_delay=7200.0,
            provider_sla_seconds=3600.0,
            blocking_profiles=[],
        )

    def get_policy(self, dataset_type: str, market: str = "TWSE") -> FreshnessPolicy:
        """Return policy for the given dataset_type. Falls back to DAILY_OHLCV default."""
        policy = self._policies.get(dataset_type)
        if policy is None:
            logger.warning("No policy for dataset_type=%s; using DAILY_OHLCV default", dataset_type)
            return self._policies[DatasetType.DAILY_OHLCV]
        return policy

    def list_policies(self) -> List[FreshnessPolicy]:
        """Return all registered policies."""
        return list(self._policies.values())

    def register_policy(self, policy: FreshnessPolicy) -> None:
        """Register a custom policy, overriding any existing for that dataset_type."""
        self._policies[policy.dataset_type] = policy
        logger.debug("Registered policy %s for dataset_type=%s", policy.policy_id, policy.dataset_type)

    def get_blocking_profiles(self, dataset_type: str) -> List[str]:
        """Return list of blocking profile names for the given dataset_type."""
        policy = self.get_policy(dataset_type)
        return policy.blocking_profiles
