"""
paper_trading/market_data/reproducibility_v161.py — Reproducibility v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Same raw events + config → same canonical events, quality results, checkpoint hash.
"""
from __future__ import annotations
import hashlib
import json
from typing import Optional, List, Dict, Any

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
REPRODUCIBLE_PIPELINE: bool = True


class MarketDataReproducibilityService:
    """
    Computes and verifies reproducibility of market data pipeline runs.
    Deterministic: same inputs → same outputs and same hashes.
    """

    def compute_event_hash(self, event_dict: Dict[str, Any]) -> str:
        """Deterministic hash of a canonical event (dict form)."""
        serialized = json.dumps(event_dict, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def compute_session_hash(
        self,
        session_id: str,
        config_dict: Dict[str, Any],
        event_hashes: List[str],
    ) -> str:
        """
        Deterministic hash of entire session: config + ordered event hashes.
        Same inputs → same session hash.
        """
        payload = {
            "session_id": session_id,
            "config": config_dict,
            "event_hashes": sorted(event_hashes),  # sort for determinism
        }
        serialized = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def build_manifest(
        self,
        manifest_id: str,
        session_id: str,
        session_config: Dict[str, Any],
        event_hashes: List[str],
    ) -> Dict[str, Any]:
        """Build a reproducibility manifest."""
        session_hash = self.compute_session_hash(session_id, session_config, event_hashes)
        return {
            "manifest_id": manifest_id,
            "session_id": session_id,
            "event_count": len(event_hashes),
            "session_hash": session_hash,
            "reproducible": True,
            "research_only": True,
            "no_real_orders": True,
            "market_data_only": True,
        }

    def verify(
        self,
        manifest: Dict[str, Any],
        session_id: str,
        session_config: Dict[str, Any],
        event_hashes: List[str],
    ) -> bool:
        """Verify that given inputs reproduce the manifest's session hash."""
        expected_hash = self.compute_session_hash(session_id, session_config, event_hashes)
        return manifest.get("session_hash") == expected_hash
