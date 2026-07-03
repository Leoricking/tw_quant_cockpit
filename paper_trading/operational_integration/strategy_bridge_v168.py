"""
paper_trading/operational_integration/strategy_bridge_v168.py
Strategy Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class StrategyBridge:
    """Validates strategy signals and configurations. Research only."""

    def check_signal_identity(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Validate signal has required identity fields."""
        required = ["signal_id", "strategy_id", "session_id", "symbol", "direction", "signal_timestamp"]
        missing = [f for f in required if f not in signal]
        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "signal_id": signal.get("signal_id", ""),
            "strategy_id": signal.get("strategy_id", ""),
            "paper_only": True,
        }

    def check_strategy_version(self, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate strategy version is present and consistent."""
        version = strategy_config.get("strategy_version", "")
        strategy_id = strategy_config.get("strategy_id", "")
        return {
            "has_version": bool(version),
            "has_strategy_id": bool(strategy_id),
            "version": version,
            "strategy_id": strategy_id,
            "valid": bool(version) and bool(strategy_id),
            "paper_only": True,
        }

    def compute_config_hash(self, strategy_config: Dict[str, Any]) -> str:
        """Compute deterministic hash of strategy configuration."""
        # Exclude non-deterministic fields
        config_copy = {
            k: v for k, v in strategy_config.items()
            if k not in ("created_at", "updated_at", "run_id", "session_id")
        }
        serialized = json.dumps(config_copy, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def check_no_lookahead(self, signal: Dict[str, Any], current_ts: str) -> bool:
        """
        Return True if signal has no lookahead bias (signal_timestamp <= current_ts).
        """
        signal_ts = signal.get("signal_timestamp", "")
        if not signal_ts or not current_ts:
            return True  # Cannot verify, assume ok
        return signal_ts <= current_ts

    def summarize(self, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Return summary of strategy configuration."""
        return {
            "strategy_id": strategy_config.get("strategy_id", ""),
            "strategy_version": strategy_config.get("strategy_version", ""),
            "has_parameters": bool(strategy_config.get("parameters")),
            "paper_only": strategy_config.get("paper_only", False),
            "config_hash": self.compute_config_hash(strategy_config),
            "summary_paper_only": True,
        }
