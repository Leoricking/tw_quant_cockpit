"""
portfolio/correlation/point_in_time_v152.py — Point-in-Time Validator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] fetched_at is NEVER a substitute for available_from.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class CorrelationExposurePITValidator:
    """
    Validates that all data inputs respect the as_of point-in-time boundary.
    fetched_at is NEVER treated as a substitute for available_from.
    """

    RESEARCH_ONLY = True

    def validate_price_data(
        self,
        prices_by_symbol: Dict[str, Dict[str, float]],
        as_of: str,
    ) -> Dict[str, Any]:
        """
        Check all price dates <= as_of.
        Returns {valid, violations, status}
        """
        violations: List[str] = []
        for sym, price_map in prices_by_symbol.items():
            for date in price_map:
                if date > as_of:
                    violations.append(f"{sym}:{date} > as_of:{as_of}")
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "status": "VALID" if not violations else "PIT_VIOLATION",
        }

    def validate_classification(
        self,
        classifications: Dict[str, Dict[str, Any]],
        as_of: str,
    ) -> Dict[str, Any]:
        """
        Check classification effective_from <= as_of for each symbol.
        Returns {valid, violations, status}
        """
        violations: List[str] = []
        for sym, cls in classifications.items():
            effective_from = cls.get("effective_from", "")
            available_from = cls.get("available_from", "")
            # Use available_from if present (stricter PIT boundary)
            check_date = available_from or effective_from
            if check_date and check_date > as_of:
                violations.append(
                    f"{sym}: available_from/effective_from={check_date} > as_of:{as_of}"
                )
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "status": "VALID" if not violations else "PIT_VIOLATION",
        }

    def validate_etf_holdings(
        self,
        holdings_data: Dict[str, Dict[str, Any]],
        as_of: str,
    ) -> Dict[str, Any]:
        """
        Check holdings_available_from <= as_of for each ETF.
        Returns {valid, violations, status}
        """
        violations: List[str] = []
        for etf_sym, holding_info in holdings_data.items():
            available_from = holding_info.get("available_from", "")
            if available_from and available_from > as_of:
                violations.append(
                    f"{etf_sym}: holdings_available_from={available_from} > as_of:{as_of}"
                )
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "status": "VALID" if not violations else "STALE_HOLDINGS",
        }

    def validate_benchmark(
        self,
        benchmark_prices: Dict[str, float],
        as_of: str,
    ) -> Dict[str, Any]:
        """
        Check all benchmark price dates <= as_of.
        Returns {valid, violations, status}
        """
        violations: List[str] = []
        for date in benchmark_prices:
            if date > as_of:
                violations.append(f"benchmark_date:{date} > as_of:{as_of}")
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "status": "VALID" if not violations else "PIT_VIOLATION",
        }
