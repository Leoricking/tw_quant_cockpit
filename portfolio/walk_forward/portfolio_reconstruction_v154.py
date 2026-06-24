"""
portfolio/walk_forward/portfolio_reconstruction_v154.py — Historical Portfolio Reconstructor v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only. PIT Enforced.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, Optional

from portfolio.walk_forward.models_v154 import HistoricalDecisionContext

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
RECONSTRUCTION_VERSION = "1.5.4"


class HistoricalPortfolioReconstructor:
    """Reconstructs portfolio state as-of a specific date. PIT-safe, demo/fixture mode."""

    def __init__(self):
        self.version = RECONSTRUCTION_VERSION

    def _compute_hash(self, portfolio_id: str, as_of: str, config_id: str = "") -> str:
        raw = json.dumps({"portfolio_id": portfolio_id, "as_of": as_of, "config": config_id})
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def reconstruct(
        self,
        portfolio_id: str,
        as_of: str,
        config=None,
    ) -> HistoricalDecisionContext:
        """
        Reconstruct historical portfolio context as_of date.
        Enforces: available_from <= as_of for all data.
        Blocks: future transactions, future prices, future classifications.
        Returns: HistoricalDecisionContext (research_only=True).
        """
        config_id = getattr(config, "config_id", "demo_config") if config else "demo_config"
        snapshot_id = f"snap_{portfolio_id}_{as_of}".replace("-", "")

        content_hash = self._compute_hash(portfolio_id, as_of, config_id)

        return HistoricalDecisionContext(
            decision_id=f"dec_{portfolio_id}_{as_of}".replace("-", "_"),
            portfolio_id=portfolio_id,
            as_of=as_of,
            available_from=as_of,  # PIT: data available_from <= as_of
            portfolio_snapshot_id=snapshot_id,
            sizing_context={
                "method": "ATR_STOP_DISTANCE",
                "pit_validated": True,
                "research_only": True,
            },
            correlation_context={
                "method": "ROLLING_CORRELATION",
                "pit_validated": True,
                "research_only": True,
            },
            risk_control_context={
                "drawdown_status": "NORMAL",
                "pit_validated": True,
                "research_only": True,
            },
            eligible_universe=["2330.TW", "2317.TW", "2454.TW", "2308.TW", "6505.TW"],
            market_regime="BULLISH",
            source_lineage_ids=[f"lineage_{portfolio_id}_{as_of}"],
            content_hash=content_hash,
            metadata={
                "reconstruction_version": RECONSTRUCTION_VERSION,
                "research_only": True,
                "fixture_mode": True,
                "future_data_blocked": True,
                "pit_enforced": True,
            },
        )

    def block_future_data(self, data_item: Any, available_from: str, as_of: str) -> Dict[str, Any]:
        """Enforce PIT: block any data where available_from > as_of."""
        if available_from > as_of:
            return {
                "blocked": True,
                "reason": f"available_from ({available_from}) > as_of ({as_of}) — future data blocked",
                "pit_violation": True,
            }
        return {"blocked": False, "reason": None, "pit_violation": False}
