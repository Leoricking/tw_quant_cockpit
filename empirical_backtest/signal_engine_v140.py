"""
empirical_backtest/signal_engine_v140.py — Signal Engine for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import uuid
from typing import List, Dict, Optional
from .models_v140 import StrategyRule, BacktestSignal, SignalType
from .rule_registry_v140 import StrategyKnowledgeRuleRegistry


def _safe_eval_condition(condition: str, data: dict) -> tuple:
    """
    Safely evaluate a simple condition string like 'close > ma10'.
    Returns (result: bool or None, missing_fields: list).
    """
    # Simple tokenization: split on spaces
    tokens = condition.split()
    missing = []

    if len(tokens) == 3:
        left_tok, op, right_tok = tokens

        # Resolve left value
        left_val = data.get(left_tok)
        if left_val is None:
            missing.append(f"insufficient_data:{left_tok}")

        # Resolve right value (may be a number, field, or expression like "ma10 * 0.99")
        right_val = None
        try:
            right_val = float(right_tok)
        except ValueError:
            right_val = data.get(right_tok)
            if right_val is None:
                missing.append(f"insufficient_data:{right_tok}")

        if missing:
            return None, missing

        try:
            left_val = float(left_val)
            right_val = float(right_val)
            if op == ">":
                return left_val > right_val, []
            elif op == "<":
                return left_val < right_val, []
            elif op == ">=":
                return left_val >= right_val, []
            elif op == "<=":
                return left_val <= right_val, []
            elif op == "==":
                return left_val == right_val, []
            else:
                return None, [f"unknown_operator:{op}"]
        except Exception:
            return None, [f"eval_error:{condition}"]

    elif len(tokens) == 5:
        # e.g. "previous_low >= ma10 * 0.99"
        left_tok = tokens[0]
        op = tokens[1]
        right_a = tokens[2]
        mult_op = tokens[3]
        right_b = tokens[4]

        left_val = data.get(left_tok)
        if left_val is None:
            missing.append(f"insufficient_data:{left_tok}")

        right_a_val = data.get(right_a)
        if right_a_val is None:
            missing.append(f"insufficient_data:{right_a}")

        if missing:
            return None, missing

        try:
            left_val = float(left_val)
            right_a_val = float(right_a_val)
            right_b_val = float(right_b)
            if mult_op == "*":
                right_val = right_a_val * right_b_val
            elif mult_op == "/":
                right_val = right_a_val / right_b_val
            else:
                return None, [f"unknown_operator:{mult_op}"]

            if op == ">":
                return left_val > right_val, []
            elif op == "<":
                return left_val < right_val, []
            elif op == ">=":
                return left_val >= right_val, []
            elif op == "<=":
                return left_val <= right_val, []
            else:
                return None, [f"unknown_operator:{op}"]
        except Exception:
            return None, [f"eval_error:{condition}"]

    else:
        # Can't parse — treat as insufficient data
        return None, [f"insufficient_data:complex_condition:{condition}"]


class StrategyKnowledgeSignalEngine:
    """Generates signals from strategy rules applied to market data."""

    def __init__(self, registry: StrategyKnowledgeRuleRegistry):
        self._registry = registry
        self._warmup_bars = 20
        self._state: Dict = {}

    def validate_required_inputs(self, rule: StrategyRule, data: dict) -> dict:
        """Check all required fields and indicators are present in data."""
        missing = []
        for field in rule.required_fields:
            if field not in data:
                missing.append(field)
        for indicator in rule.required_indicators:
            if indicator not in data:
                missing.append(indicator)
        return {"ok": len(missing) == 0, "missing": missing}

    def evaluate_rule(self, rule: StrategyRule, data: dict, timestamp: str) -> dict:
        """Evaluate a rule against data at a given timestamp."""
        validation = self.validate_required_inputs(rule, data)
        if not validation["ok"]:
            return {
                "signal_type": SignalType.NO_ACTION,
                "quality_status": "insufficient_data",
                "conditions_met": [],
                "conditions_failed": validation["missing"],
                "signal_timestamp": timestamp,
                "decision_timestamp": timestamp,
                "intended_execution_timestamp": "NEXT_OPEN",
                "confidence": 0.0,
                "strength": 0.0,
            }

        conditions_met = []
        conditions_failed = []

        for cond in rule.entry_conditions:
            result, missing_fields = _safe_eval_condition(cond, data)
            if missing_fields:
                conditions_failed.extend(missing_fields)
            elif result is True:
                conditions_met.append(cond)
            elif result is False:
                conditions_failed.append(cond)
            else:
                conditions_failed.append(f"eval_failed:{cond}")

        all_met = len(conditions_failed) == 0 and len(conditions_met) > 0
        signal_type = SignalType.ENTRY if all_met else SignalType.NO_ACTION
        quality_status = "ok" if all_met else ("insufficient_data" if conditions_failed else "no_signal")
        confidence = 1.0 if all_met else 0.0

        return {
            "signal_type": signal_type,
            "quality_status": quality_status,
            "conditions_met": conditions_met,
            "conditions_failed": conditions_failed,
            "signal_timestamp": timestamp,
            "decision_timestamp": timestamp,
            "intended_execution_timestamp": "NEXT_OPEN",
            "confidence": confidence,
            "strength": confidence,
        }

    def evaluate_symbol(self, rule_id: str, symbol: str, bars: list) -> list:
        """Evaluate a rule for all bars of a symbol."""
        rule = self._registry.get(rule_id)
        if rule is None:
            return []
        signals = []
        for bar in bars:
            timestamp = bar.get("date", "")
            result = self.evaluate_rule(rule, bar, timestamp)
            result["rule_id"] = rule_id
            result["symbol"] = symbol
            signals.append(result)
        return signals

    def evaluate_universe(self, rule_id: str, symbols: list, data_map: dict) -> dict:
        """Evaluate a rule for all symbols in the universe."""
        return {
            symbol: self.evaluate_symbol(rule_id, symbol, data_map.get(symbol, []))
            for symbol in symbols
        }

    def build_signal(self, rule: StrategyRule, signal_type: str, timestamp: str, **kwargs) -> BacktestSignal:
        """Build a BacktestSignal object."""
        return BacktestSignal(
            signal_id=str(uuid.uuid4()),
            rule_id=rule.rule_id,
            symbol=kwargs.get("symbol", ""),
            signal_type=signal_type,
            signal_timestamp=timestamp,
            decision_timestamp=timestamp,
            intended_execution_timestamp=kwargs.get("intended_execution_timestamp", "NEXT_OPEN"),
            strength=kwargs.get("strength", 0.0),
            confidence=kwargs.get("confidence", 0.0),
            conditions_met=kwargs.get("conditions_met", []),
            conditions_failed=kwargs.get("conditions_failed", []),
            quality_status=kwargs.get("quality_status", "ok"),
        )

    def explain_signal(self, signal: BacktestSignal) -> str:
        """Return a human-readable explanation of a signal."""
        lines = [
            f"Signal ID: {signal.signal_id}",
            f"Rule: {signal.rule_id}",
            f"Symbol: {signal.symbol}",
            f"Type: {signal.signal_type}",
            f"Timestamp: {signal.signal_timestamp}",
            f"Quality: {signal.quality_status}",
            f"Conditions Met: {signal.conditions_met}",
            f"Conditions Failed: {signal.conditions_failed}",
        ]
        return "\n".join(lines)

    def warmup(self, bars: int) -> None:
        self._warmup_bars = bars

    def reset(self) -> None:
        self._state = {}
