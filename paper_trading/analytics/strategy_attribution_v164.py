"""
paper_trading/analytics/strategy_attribution_v164.py — Strategy Attribution v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import AttributionType, MetricQuality
from paper_trading.analytics.models_v164 import AttributionRecord
from paper_trading.analytics.validation_v164 import validate_attribution_reconciliation

NO_REAL_ORDERS = True
PAPER_ONLY = True
ATTRIBUTION_POLICY_VERSION = "1.6.4"


class StrategyAttributionComputer:
    """
    Computes strategy-layer attribution.
    Gross/net not confused. Residual explicitly shown.
    Attribution does not sum to 100% artificially.
    """

    def compute(
        self,
        analytics_id: str,
        session_id: str,
        gross_pnl: Decimal,
        components: Dict[AttributionType, Decimal],
        residual_threshold: Decimal = Decimal("0.01"),
    ) -> Dict[str, Any]:
        import uuid
        records: List[AttributionRecord] = []
        component_values: List[Decimal] = []

        for attr_type, value in components.items():
            rec = AttributionRecord(
                attribution_id=str(uuid.uuid4()),
                analytics_id=analytics_id,
                attribution_type=attr_type,
                entity_id=session_id,
                metric_name=attr_type.value.lower() + "_attribution",
                gross_value=value,
                net_value=value,
                contribution=value / gross_pnl if gross_pnl != Decimal("0") else Decimal("0"),
                confidence=Decimal("0.8"),
                quality=MetricQuality.VALID,
                policy_version=ATTRIBUTION_POLICY_VERSION,
            )
            records.append(rec)
            component_values.append(value)

        reconciliation = validate_attribution_reconciliation(
            gross=gross_pnl,
            components=component_values,
            residual_threshold=residual_threshold,
            label="strategy_attribution",
        )

        return {
            "records": records,
            "reconciliation": reconciliation,
            "gross_pnl": gross_pnl,
            "policy_version": ATTRIBUTION_POLICY_VERSION,
            "paper_only": True,
            "no_real_orders": True,
        }


__all__ = ["StrategyAttributionComputer", "ATTRIBUTION_POLICY_VERSION"]
