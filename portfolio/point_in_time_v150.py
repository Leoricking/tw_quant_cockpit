"""
portfolio/point_in_time_v150.py — PIT validation for v1.5.0.

All PIT assertions: transaction effective_at <= as_of,
transaction available_from <= as_of,
price available_from <= as_of.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True


def _parse_dt(s: Any) -> Optional[datetime]:
    if s is None:
        return None
    if isinstance(s, datetime):
        return s
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


class PortfolioPITValidator:
    RESEARCH_ONLY = True

    def validate(
        self,
        transactions: List[Dict],
        price_map: Optional[Dict[str, Dict]] = None,
        as_of: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Validate all PIT constraints for the given as_of date.

        Returns:
          {
            "consistent": bool,
            "violations": list of {type, transaction_id/symbol, detail},
            "as_of": str,
            "research_only": True,
          }
        """
        violations: List[Dict] = []
        as_of_dt = _parse_dt(as_of)

        for txn in transactions:
            tid = txn.get("transaction_id", "UNKNOWN")

            eff_dt = _parse_dt(txn.get("effective_at"))
            if eff_dt and as_of_dt and eff_dt > as_of_dt:
                violations.append({
                    "type": "EFFECTIVE_AT_FUTURE",
                    "transaction_id": tid,
                    "detail": f"effective_at={eff_dt.isoformat()} > as_of={as_of_dt.isoformat()}",
                })

            avail_dt = _parse_dt(txn.get("available_from"))
            if avail_dt and as_of_dt and avail_dt > as_of_dt:
                violations.append({
                    "type": "AVAILABLE_FROM_FUTURE",
                    "transaction_id": tid,
                    "detail": f"available_from={avail_dt.isoformat()} > as_of={as_of_dt.isoformat()}",
                })

        if price_map:
            for symbol, price_info in price_map.items():
                price_avail_dt = _parse_dt(price_info.get("available_from"))
                if price_avail_dt and as_of_dt and price_avail_dt > as_of_dt:
                    violations.append({
                        "type": "PRICE_AVAILABLE_FROM_FUTURE",
                        "symbol": symbol,
                        "detail": f"price available_from={price_avail_dt.isoformat()} > as_of={as_of_dt.isoformat()}",
                    })

        return {
            "consistent": len(violations) == 0,
            "violations": violations,
            "as_of": as_of,
            "total_transactions_checked": len(transactions),
            "total_prices_checked": len(price_map) if price_map else 0,
            "research_only": True,
        }
