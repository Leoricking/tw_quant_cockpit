"""
paper_trading/strategy/validation_v162.py — Input validation for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from paper_trading.strategy.enums_v162 import SignalType, ApprovalMode, ConflictPolicy


# ---------------------------------------------------------------------------
# Signal validation
# ---------------------------------------------------------------------------

_ALLOWED_SIGNAL_TYPES = {st.value for st in SignalType}
_FORBIDDEN_SIGNAL_TYPES = {"ENTRY_SHORT", "SELL_SHORT", "MARGIN_LONG", "MARGIN_SHORT"}


def validate_signal_type(signal_type: str) -> Tuple[bool, str]:
    """Return (ok, reason). Permanently rejects SHORT/MARGIN types."""
    if signal_type in _FORBIDDEN_SIGNAL_TYPES:
        return False, f"Signal type permanently forbidden: {signal_type}"
    if signal_type not in _ALLOWED_SIGNAL_TYPES:
        return False, f"Unknown signal type: {signal_type}"
    return True, ""


def validate_confidence(confidence: Any) -> Tuple[bool, str]:
    try:
        c = float(confidence)
    except (TypeError, ValueError):
        return False, f"confidence must be numeric, got {type(confidence).__name__}"
    if not (0.0 <= c <= 1.0):
        return False, f"confidence must be in [0.0, 1.0], got {c}"
    return True, ""


def validate_ticker(ticker: Any) -> Tuple[bool, str]:
    if not isinstance(ticker, str) or not ticker.strip():
        return False, f"ticker must be a non-empty string, got {ticker!r}"
    return True, ""


def validate_paper_signal_dict(d: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a raw dict representing a PaperSignal. Returns (ok, errors)."""
    errors: List[str] = []

    ok, msg = validate_ticker(d.get("ticker", ""))
    if not ok:
        errors.append(msg)

    ok, msg = validate_signal_type(d.get("signal_type", ""))
    if not ok:
        errors.append(msg)

    ok, msg = validate_confidence(d.get("confidence", 0.0))
    if not ok:
        errors.append(msg)

    # Safety labels must be True
    for flag in ("paper_only", "research_only", "not_a_real_order"):
        if d.get(flag) is not True:
            errors.append(f"Safety flag must be True: {flag}")

    return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Strategy config validation
# ---------------------------------------------------------------------------

def validate_strategy_config_dict(d: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a raw dict representing a StrategyConfig."""
    errors: List[str] = []

    name = d.get("strategy_name", "")
    if not isinstance(name, str) or not name.strip():
        errors.append("strategy_name must be a non-empty string")

    approval = d.get("approval_mode", ApprovalMode.MANUAL_REQUIRED.value)
    if approval not in {m.value for m in ApprovalMode}:
        errors.append(f"Unknown approval_mode: {approval}")

    conflict = d.get("conflict_policy", ConflictPolicy.MOST_CONSERVATIVE.value)
    if conflict not in {p.value for p in ConflictPolicy}:
        errors.append(f"Unknown conflict_policy: {conflict}")

    max_spm = d.get("max_signals_per_minute", 10)
    if not isinstance(max_spm, int) or max_spm < 1:
        errors.append(f"max_signals_per_minute must be a positive int, got {max_spm!r}")

    cooldown = d.get("cooldown_seconds", 60)
    if not isinstance(cooldown, int) or cooldown < 0:
        errors.append(f"cooldown_seconds must be a non-negative int, got {cooldown!r}")

    # Safety flags
    for flag in ("paper_only", "research_only", "simulation_only",
                 "not_a_real_order", "no_broker_call", "no_real_account",
                 "no_formal_portfolio_ledger_write"):
        if d.get(flag) is not True:
            errors.append(f"Safety flag must be True: {flag}")

    return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Proposal validation
# ---------------------------------------------------------------------------

def validate_proposal_dict(d: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a raw dict representing a PaperOrderProposal."""
    errors: List[str] = []

    ok, msg = validate_ticker(d.get("ticker", ""))
    if not ok:
        errors.append(msg)

    ok, msg = validate_signal_type(d.get("signal_type", ""))
    if not ok:
        errors.append(msg)

    size = d.get("proposed_size", None)
    if size is None or not isinstance(size, (int, float)) or float(size) < 0:
        errors.append(f"proposed_size must be a non-negative number, got {size!r}")

    for flag in ("paper_only", "research_only", "simulation_only",
                 "not_a_real_order", "no_broker_call", "no_real_account",
                 "no_formal_portfolio_ledger_write"):
        if d.get(flag) is not True:
            errors.append(f"Safety flag must be True: {flag}")

    return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Safety invariant check
# ---------------------------------------------------------------------------

def assert_safety_invariants(obj: Any) -> None:
    """
    Raise AssertionError if any safety flag on obj is incorrect.
    Works for StrategyConfig, PaperSignal, PaperOrderProposal, DecisionResult.
    """
    for flag in ("paper_only", "research_only", "not_a_real_order", "no_broker_call"):
        val = getattr(obj, flag, None)
        if val is not None:
            assert val is True, f"Safety invariant violated: {flag} must be True, got {val!r}"
    for flag in ("broker_enabled", "real_order_creation_enabled",
                 "real_order_execution_enabled"):
        val = getattr(obj, flag, None)
        if val is not None:
            assert val is False, f"Safety invariant violated: {flag} must be False, got {val!r}"
