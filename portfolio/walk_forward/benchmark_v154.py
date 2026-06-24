"""
portfolio/walk_forward/benchmark_v154.py — Benchmark Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only. PIT-safe.
Missing benchmark → BLOCKED.
"""
from __future__ import annotations
import datetime
from typing import Any, Dict, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
BENCHMARK_VERSION = "1.5.4"


class BenchmarkEngine:
    """Provide benchmark returns for walk-forward windows. Fixture demo mode."""

    def __init__(self):
        self.version = BENCHMARK_VERSION

    def get_benchmark_returns(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        as_of: str,
    ) -> Dict[str, Any]:
        """
        Get benchmark returns for a period. PIT-safe: as_of boundary enforced.
        Missing benchmark → BLOCKED.
        Returns dict with returns_by_date, status.
        """
        if not symbol:
            return {
                "returns_by_date": None,
                "status": "BLOCKED",
                "reason": "No benchmark symbol specified",
                "research_only": True,
            }

        # PIT check: do not return data after as_of
        if end_date > as_of:
            adjusted_end = as_of
        else:
            adjusted_end = end_date

        if start_date >= adjusted_end:
            return {
                "returns_by_date": None,
                "status": "BLOCKED",
                "reason": f"No benchmark data available: start={start_date} >= adjusted_end={adjusted_end}",
                "pit_adjusted": end_date != adjusted_end,
                "research_only": True,
            }

        # Generate demo fixture benchmark returns
        returns_by_date = self._generate_fixture_returns(symbol, start_date, adjusted_end)

        return {
            "returns_by_date": returns_by_date,
            "symbol": symbol,
            "start_date": start_date,
            "end_date": adjusted_end,
            "as_of": as_of,
            "pit_adjusted": end_date != adjusted_end,
            "status": "VALID",
            "fixture_mode": True,
            "research_only": True,
        }

    def _generate_fixture_returns(
        self, symbol: str, start: str, end: str
    ) -> Dict[str, float]:
        """Generate deterministic fixture daily returns."""
        result = {}
        s = datetime.date.fromisoformat(start)
        e = datetime.date.fromisoformat(end)
        value = 10000.0
        cur = s
        day = 0
        while cur <= e:
            if cur.weekday() < 5:
                # Deterministic pseudo-return based on day index
                daily_r = 0.0003 * (1 + (day % 7) * 0.1 - (day % 3) * 0.05)
                value *= (1 + daily_r)
                result[cur.isoformat()] = round(value, 2)
                day += 1
            cur += datetime.timedelta(days=1)
        return result
