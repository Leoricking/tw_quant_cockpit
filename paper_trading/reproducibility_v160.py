"""paper_trading/reproducibility_v160.py — Paper Session Reproducibility v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Same input → same semantic result, same ledger hash, same final snapshot hash.
"""
from __future__ import annotations
import hashlib
import json
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

from .models_v160 import PaperSessionReproducibilityManifest


class ReproducibilityService:
    """Builds and verifies paper session reproducibility manifests."""

    def build_manifest(
        self,
        manifest_id: str,
        session_id: str,
        session_config: Any,
        event_hashes: List[str],
        policy_versions: Optional[Dict[str, str]] = None,
        code_commit: str = "",
        final_ledger_hash: str = "",
        final_snapshot_hash: str = "",
    ) -> PaperSessionReproducibilityManifest:
        config_hash = self._hash_config(session_config)
        return PaperSessionReproducibilityManifest(
            manifest_id=manifest_id,
            session_id=session_id,
            session_config_hash=config_hash,
            initial_cash=str(session_config.initial_cash),
            allowed_symbols=list(session_config.allowed_symbols),
            policies={
                "execution_model": session_config.execution_model_id,
                "slippage_policy": session_config.slippage_policy_id,
                "liquidity_policy": session_config.liquidity_policy_id,
                "risk_policy": session_config.risk_policy_id,
                "sizing_policy": session_config.sizing_policy_id,
            },
            data_mode=session_config.data_mode.value,
            event_hashes=event_hashes,
            event_order=event_hashes,  # ordered list
            execution_model=session_config.execution_model_id,
            latency_model="ZERO_DISCLOSED",
            slippage_model=session_config.slippage_policy_id,
            liquidity_model=session_config.liquidity_policy_id,
            code_commit=code_commit,
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            dependency_versions=policy_versions or {},
            timezone=session_config.timezone,
            calendar_version="v160",
            final_ledger_hash=final_ledger_hash,
            final_snapshot_hash=final_snapshot_hash,
            research_only=True,
            paper_only=True,
        )

    def verify(self, manifest: PaperSessionReproducibilityManifest, result_ledger_hash: str, result_snapshot_hash: str) -> Dict[str, Any]:
        ledger_ok = manifest.final_ledger_hash == result_ledger_hash
        snapshot_ok = manifest.final_snapshot_hash == result_snapshot_hash
        return {
            "ledger_hash_match": ledger_ok,
            "snapshot_hash_match": snapshot_ok,
            "reproducible": ledger_ok and snapshot_ok,
        }

    def _hash_config(self, config: Any) -> str:
        data = {
            "session_id": config.session_id,
            "initial_cash": str(config.initial_cash),
            "currency": config.currency,
            "data_mode": config.data_mode.value,
            "execution_model_id": config.execution_model_id,
            "slippage_policy_id": config.slippage_policy_id,
            "liquidity_policy_id": config.liquidity_policy_id,
            "risk_policy_id": config.risk_policy_id,
            "allowed_symbols": sorted(config.allowed_symbols),
            "timezone": config.timezone,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:32]
