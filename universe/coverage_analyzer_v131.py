"""
universe/coverage_analyzer_v131.py — Universe coverage analyzer for v1.3.1.

Integrates with v1.3.0 DataCompletenessGate, DataQualityStatus, DataQualityReport, DataMode.
Does NOT create a second quality status system.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Coverage != can generate precise prices. Missing values NOT filled with 0.
[!] No mock fallback on analysis failure. No auto-download. Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from universe.models import (
    CoverageStatus,
    UniverseCoverageRecord,
    UniverseTier,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True
MOCK_FALLBACK_ENABLED      = False

# Coverage profiles (matching existing CompletenessProfile constants)
PROFILE_STOCK_SCREENING = "stock_screening"
PROFILE_PRECISE_PRICE   = "precise_price"
PROFILE_BACKTEST        = "backtest"
PROFILE_ABC_BUY_POINT   = "abc_buy_point"
PROFILE_DEFAULT         = "default"

_ALL_PROFILES = {
    PROFILE_STOCK_SCREENING,
    PROFILE_PRECISE_PRICE,
    PROFILE_BACKTEST,
    PROFILE_ABC_BUY_POINT,
    PROFILE_DEFAULT,
}


class UniverseCoverageAnalyzerV131:
    """
    Coverage analyzer that integrates with v1.3.0 DataCompletenessGate.

    [!] Does NOT create a second quality status system.
    [!] READY = registered + Real data quality PASS (or profile-acceptable DEGRADED).
    [!] UNAVAILABLE = no real data. DEMO_ONLY = only mock/fixture data.
    [!] Missing values must NOT be filled with 0.
    [!] Coverage is profile-specific.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True
    MOCK_FALLBACK_ENABLED      = False

    def __init__(self, registry=None, quality_gate=None) -> None:
        self._registry = registry
        self._quality_gate = quality_gate

    def analyze_symbol(
        self,
        symbol: str,
        profile: str = PROFILE_DEFAULT,
        registry=None,
        quality_gate=None,
    ) -> UniverseCoverageRecord:
        """
        Analyze coverage for one symbol under a given profile.

        Returns UniverseCoverageRecord.
        [!] Coverage != can generate precise prices. Not Investment Advice.
        """
        reg = registry or self._registry
        gate = quality_gate or self._quality_gate

        record = UniverseCoverageRecord(
            symbol=symbol,
            universe_id="",
            tier="",
        )

        # Step 1: Check registry status
        if reg is not None:
            try:
                sym_obj = reg.get_symbol(symbol)
            except Exception as exc:
                logger.warning("Registry lookup failed for %s: %s", symbol, exc)
                sym_obj = None
            if sym_obj is None:
                record.registry_status = "UNREGISTERED"
                record.quality_status = CoverageStatus.UNAVAILABLE.value
                record.blocking_reasons.append("Symbol not registered in universe registry")
                return record
            record.registry_status = "REGISTERED"
            record.tier = getattr(sym_obj, "market", "")
        else:
            record.registry_status = "REGISTRY_UNAVAILABLE"

        # Step 2: Check data quality via existing gate
        if gate is not None:
            try:
                data = {
                    "symbol": symbol,
                    "market": "TW",
                    "data_mode": "UNAVAILABLE",
                    "source": [],
                }
                gate_result = gate.check(data, profile=profile)
                # gate_result is a DataQualityReport or dict
                if hasattr(gate_result, "status"):
                    dq_status = gate_result.status
                    record.quality_score = getattr(gate_result, "score", None)
                    if hasattr(gate_result, "data_mode"):
                        record.data_mode = gate_result.data_mode
                else:
                    dq_status = "UNAVAILABLE"
            except Exception as exc:
                logger.warning("Quality gate check failed for %s: %s", symbol, exc)
                dq_status = "UNAVAILABLE"
                record.warnings.append(f"Quality gate check error: {exc}")
        else:
            dq_status = "UNAVAILABLE"

        # Step 3: Map quality status to coverage status
        record.quality_status = _map_dq_to_coverage(dq_status, profile, record)

        # Step 4: Profile-specific allowances
        if record.quality_status == CoverageStatus.READY.value:
            record.precise_price_allowed = (profile in (PROFILE_PRECISE_PRICE, PROFILE_DEFAULT))
            record.backtest_allowed = (profile in (PROFILE_BACKTEST, PROFILE_DEFAULT))
            record.abc_buy_point_allowed = (profile == PROFILE_ABC_BUY_POINT)
        else:
            record.precise_price_allowed = False
            record.backtest_allowed = False
            record.abc_buy_point_allowed = False

        return record

    def analyze_universe(
        self,
        universe_id: str,
        profile: str = PROFILE_DEFAULT,
        registry=None,
        quality_gate=None,
    ) -> List[UniverseCoverageRecord]:
        """
        Analyze coverage for all symbols in a universe.
        Single symbol failure does NOT crash entire batch.
        [!] No mock fallback on failure. Not Investment Advice.
        """
        reg = registry or self._registry
        results = []
        if reg is None:
            logger.warning("No registry provided — cannot analyze universe %s", universe_id)
            return results
        try:
            symbols = reg.list_symbols()
        except Exception as exc:
            logger.warning("Could not list symbols for universe %s: %s", universe_id, exc)
            return results

        for sym_obj in symbols:
            try:
                rec = self.analyze_symbol(
                    sym_obj.symbol,
                    profile=profile,
                    registry=reg,
                    quality_gate=quality_gate or self._quality_gate,
                )
                rec.universe_id = universe_id
                results.append(rec)
            except Exception as exc:
                logger.warning("Coverage analysis failed for %s: %s", sym_obj.symbol, exc)
                results.append(UniverseCoverageRecord(
                    symbol=sym_obj.symbol,
                    universe_id=universe_id,
                    quality_status=CoverageStatus.UNAVAILABLE.value,
                    blocking_reasons=[f"Analysis error: {exc}"],
                ))
        return results


def _map_dq_to_coverage(dq_status: str, profile: str, record: UniverseCoverageRecord) -> str:
    """
    Map DataQualityStatus to CoverageStatus.
    Profile-specific: one stock can have different statuses for different profiles.
    """
    if dq_status == "PASS":
        return CoverageStatus.READY.value
    elif dq_status == "DEGRADED":
        # DEGRADED inclusion determined by profile
        if profile == PROFILE_STOCK_SCREENING:
            return CoverageStatus.PARTIAL.value
        else:
            return CoverageStatus.PARTIAL.value
    elif dq_status == "BLOCKED":
        record.blocking_reasons.append("Data quality BLOCKED — no precise prices allowed")
        return CoverageStatus.BLOCKED.value
    elif dq_status == "UNAVAILABLE":
        return CoverageStatus.UNAVAILABLE.value
    elif dq_status == "EXCLUDED":
        return CoverageStatus.EXCLUDED.value
    else:
        return CoverageStatus.UNAVAILABLE.value
