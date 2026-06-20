"""
data/providers/finmind/point_in_time_v144.py — FinMind point-in-time guard v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] UNKNOWN PIT class → formal historical conclusion blocked.
[!] Never infer minute-level PIT from daily data.
[!] as_of validation: blocks if available_from > as_of or UNKNOWN.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from data.providers.finmind.models_v144 import FinMindPITClass

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# FinMind datasets and their PIT classification
_DATASET_PIT_CLASSES = {
    "TaiwanStockPrice": FinMindPITClass.DATE_ONLY,
    "TaiwanStockInstitutionalInvestorsBuySell": FinMindPITClass.DATE_ONLY,
    "TaiwanStockInstitutionalInvestorsBuySellWide": FinMindPITClass.DATE_ONLY,
    "TaiwanStockMarginPurchaseShortSale": FinMindPITClass.DATE_ONLY,
    "TaiwanStockMonthRevenue": FinMindPITClass.DATE_ONLY,
    "TaiwanStockFinancialStatements": FinMindPITClass.DATE_ONLY,
}


class FinMindPITGuard:
    """
    Point-in-time guard for FinMind data.
    UNKNOWN → blocked. Never infer sub-day PIT from daily datasets.
    """

    def classify_pit(self, dataset: str, has_publish_time: bool = False) -> FinMindPITClass:
        """
        Classify PIT for a dataset.
        FinMind daily datasets are DATE_ONLY unless publish time is available.
        Never infer minute-level from daily data.
        """
        base_class = _DATASET_PIT_CLASSES.get(dataset, FinMindPITClass.UNKNOWN)
        if base_class == FinMindPITClass.DATE_ONLY and not has_publish_time:
            return FinMindPITClass.DATE_ONLY
        if base_class == FinMindPITClass.UNKNOWN:
            logger.warning("FinMind PIT class UNKNOWN for dataset=%s. Formal conclusion blocked.", dataset)
            return FinMindPITClass.UNKNOWN
        return base_class

    def validate_as_of(
        self,
        record: Dict[str, Any],
        as_of_date: str,
        pit_class: Optional[FinMindPITClass] = None,
    ) -> bool:
        """
        Validate that a record is valid as of a given date.
        Blocks if: record has available_from > as_of_date, or PIT class is UNKNOWN.
        Returns True if record is valid as-of, False if blocked.
        """
        if pit_class == FinMindPITClass.UNKNOWN:
            logger.warning("PIT class UNKNOWN: blocking as-of validation for as_of=%s", as_of_date)
            return False

        available_from = record.get("available_from") or record.get("trade_date") or record.get("date")
        if available_from is None:
            # No publish time info — conservative: allow for DATE_ONLY
            return pit_class == FinMindPITClass.DATE_ONLY

        # String comparison works for ISO date YYYY-MM-DD
        if str(available_from) > str(as_of_date):
            logger.debug("PIT guard: record available_from=%s > as_of=%s — blocked", available_from, as_of_date)
            return False

        return True

    def get_pit_summary(self, dataset: str) -> Dict[str, Any]:
        """Return PIT classification summary for a dataset."""
        pit_class = self.classify_pit(dataset)
        return {
            "dataset": dataset,
            "pit_class": pit_class.value,
            "formal_historical_conclusion_allowed": pit_class != FinMindPITClass.UNKNOWN,
            "note": "DATE_ONLY: daily close data only, no intraday PIT precision.",
        }
