"""
paper_trading/market_data/quality_v161.py — Data Quality Gate v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Aggregates sequence, freshness, deduplication results into DataQualityStatus.
"""
from __future__ import annotations
from typing import Optional, Dict, Any

from paper_trading.market_data.enums_v161 import (
    DataQualityStatus, FreshnessStatus, SequenceStatus,
)

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class DataQualityGate:
    """
    Aggregates freshness, sequence, and deduplication results into a
    single DataQualityStatus for a canonical event.
    BLOCKED conditions: duplicate events, bid>ask violations (handled in models).
    """

    def assess(
        self,
        freshness: FreshnessStatus,
        sequence: SequenceStatus,
        is_duplicate: bool = False,
        bid_ask_violated: bool = False,
        extra_flags: Optional[Dict[str, Any]] = None,
    ) -> DataQualityStatus:
        """
        Assess overall quality of an event.
        BLOCKED: duplicate or bid>ask violation.
        FAIL: GAP_DETECTED or EXPIRED freshness.
        WARN: OUT_OF_ORDER, DELAYED freshness, or STALE.
        PASS: all good.
        """
        if bid_ask_violated:
            return DataQualityStatus.BLOCKED

        if is_duplicate:
            return DataQualityStatus.BLOCKED

        if freshness == FreshnessStatus.EXPIRED:
            return DataQualityStatus.FAIL

        if sequence == SequenceStatus.GAP_DETECTED:
            return DataQualityStatus.FAIL

        if sequence in (SequenceStatus.OUT_OF_ORDER,):
            return DataQualityStatus.WARN

        if freshness in (FreshnessStatus.DELAYED, FreshnessStatus.STALE):
            return DataQualityStatus.WARN

        return DataQualityStatus.PASS

    def assess_batch(self, assessments: list) -> DataQualityStatus:
        """
        Given a list of DataQualityStatus values, return the worst.
        BLOCKED > FAIL > WARN > PASS.
        """
        order = [DataQualityStatus.PASS, DataQualityStatus.WARN,
                 DataQualityStatus.FAIL, DataQualityStatus.BLOCKED]
        worst = DataQualityStatus.PASS
        for s in assessments:
            if order.index(s) > order.index(worst):
                worst = s
        return worst
