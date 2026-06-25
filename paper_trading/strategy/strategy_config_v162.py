"""
paper_trading/strategy/strategy_config_v162.py — Config builder/loader for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Optional

from paper_trading.strategy.enums_v162 import ApprovalMode, ConflictPolicy, SignalType
from paper_trading.strategy.models_v162 import StrategyConfig
from paper_trading.strategy.validation_v162 import validate_strategy_config_dict

logger = logging.getLogger(__name__)

# Default safety flags — cannot be overridden to unsafe values
_SAFETY_DEFAULTS: Dict[str, Any] = {
    "paper_only": True,
    "research_only": True,
    "simulation_only": True,
    "not_a_real_order": True,
    "no_broker_call": True,
    "no_real_account": True,
    "no_formal_portfolio_ledger_write": True,
}

_DEFAULT_ALLOWED_SIGNAL_TYPES = [
    SignalType.ENTRY_LONG.value,
    SignalType.EXIT_LONG.value,
    SignalType.HOLD.value,
    SignalType.REDUCE_RESEARCH.value,
    SignalType.BLOCK.value,
    SignalType.ALERT.value,
]


def build_default_config(
    strategy_name: str = "unnamed_strategy",
    strategy_version: str = "0.0.1",
    description: str = "",
    author: str = "research",
    approval_mode: ApprovalMode = ApprovalMode.MANUAL_REQUIRED,
    conflict_policy: ConflictPolicy = ConflictPolicy.MOST_CONSERVATIVE,
    max_signals_per_minute: int = 10,
    cooldown_seconds: int = 60,
    max_open_proposals: int = 5,
    tags: Optional[list] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> StrategyConfig:
    """Build a StrategyConfig with all safety flags enforced."""
    return StrategyConfig(
        strategy_name=strategy_name,
        strategy_version=strategy_version,
        description=description,
        author=author,
        approval_mode=approval_mode,
        conflict_policy=conflict_policy,
        max_signals_per_minute=max_signals_per_minute,
        cooldown_seconds=cooldown_seconds,
        max_open_proposals=max_open_proposals,
        allowed_signal_types=list(_DEFAULT_ALLOWED_SIGNAL_TYPES),
        tags=tags or [],
        extra=extra or {},
        **_SAFETY_DEFAULTS,
    )


def config_from_dict(d: Dict[str, Any]) -> StrategyConfig:
    """
    Create a StrategyConfig from a raw dict.
    Safety flags are always overridden to the safe values — callers cannot disable them.
    """
    merged = dict(d)
    merged.update(_SAFETY_DEFAULTS)

    # Normalize enum fields
    if isinstance(merged.get("approval_mode"), str):
        merged["approval_mode"] = ApprovalMode(merged["approval_mode"])
    if isinstance(merged.get("conflict_policy"), str):
        merged["conflict_policy"] = ConflictPolicy(merged["conflict_policy"])

    ok, errors = validate_strategy_config_dict({**merged,
                                                **{k: True for k in _SAFETY_DEFAULTS}})
    if not ok:
        logger.warning("[v1.6.2] config_from_dict validation errors: %s", errors)

    # Remove unknown keys that StrategyConfig doesn't accept
    known_fields = {f.name for f in StrategyConfig.__dataclass_fields__.values()}
    filtered = {k: v for k, v in merged.items() if k in known_fields}

    return StrategyConfig(**filtered)


def config_from_json_file(path: str) -> StrategyConfig:
    """Load a StrategyConfig from a JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Strategy config not found: {path}")
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    logger.info("[v1.6.2] Loaded strategy config from %s", path)
    return config_from_dict(d)


def config_to_dict(cfg: StrategyConfig) -> Dict[str, Any]:
    """Serialize a StrategyConfig to a plain dict (safe for JSON)."""
    return {
        "strategy_id": cfg.strategy_id,
        "strategy_name": cfg.strategy_name,
        "strategy_version": cfg.strategy_version,
        "description": cfg.description,
        "author": cfg.author,
        "approval_mode": cfg.approval_mode.value,
        "conflict_policy": cfg.conflict_policy.value,
        "max_signals_per_minute": cfg.max_signals_per_minute,
        "cooldown_seconds": cfg.cooldown_seconds,
        "max_open_proposals": cfg.max_open_proposals,
        "allowed_signal_types": cfg.allowed_signal_types,
        "tags": cfg.tags,
        "extra": cfg.extra,
        # Safety flags — always serialized so they're visible/auditable
        "paper_only": cfg.paper_only,
        "research_only": cfg.research_only,
        "simulation_only": cfg.simulation_only,
        "not_a_real_order": cfg.not_a_real_order,
        "no_broker_call": cfg.no_broker_call,
        "no_real_account": cfg.no_real_account,
        "no_formal_portfolio_ledger_write": cfg.no_formal_portfolio_ledger_write,
    }


def save_config_to_json(cfg: StrategyConfig, path: str) -> None:
    """Save a StrategyConfig to a JSON file."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(config_to_dict(cfg), fh, indent=2, ensure_ascii=False)
    logger.info("[v1.6.2] Saved strategy config to %s", path)
