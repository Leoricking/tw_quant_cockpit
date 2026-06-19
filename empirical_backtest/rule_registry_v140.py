"""
empirical_backtest/rule_registry_v140.py — Strategy Knowledge Rule Registry for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, List, Optional
from .models_v140 import StrategyRule, RuleCategory


class StrategyKnowledgeRuleRegistry:
    """Registry for strategy knowledge rules."""

    def __init__(self):
        self._rules: Dict[str, StrategyRule] = {}
        self._register_builtin_rules()

    def register(self, rule: StrategyRule, overwrite: bool = False) -> None:
        if rule.rule_id in self._rules and not overwrite:
            raise ValueError(f"Rule '{rule.rule_id}' already registered. Use overwrite=True to replace.")
        self._rules[rule.rule_id] = rule

    def get(self, rule_id: str) -> Optional[StrategyRule]:
        return self._rules.get(rule_id)

    def list(self) -> List[StrategyRule]:
        return list(self._rules.values())

    def list_backtestable(self) -> List[StrategyRule]:
        return [r for r in self._rules.values() if r.backtestable]

    def list_manual_only(self) -> List[StrategyRule]:
        return [r for r in self._rules.values() if not r.backtestable]

    def _register_builtin_rules(self) -> None:
        self.register(StrategyRule(
            rule_id="abc_buy_point_a",
            rule_name="A Buy Point: MA10 Holds After Pullback",
            rule_version="1.0.0",
            category=RuleCategory.ABC_BUY_POINT,
            description="Price pulls back but does not break MA10, then reverses upward.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["ma10"],
            minimum_history_bars=30,
            entry_conditions=["close > ma10", "previous_low >= ma10 * 0.99"],
            exit_conditions=["close < ma10"],
            backtestable=True,
            tags=["A_POINT", "ma10"],
        ))
        self.register(StrategyRule(
            rule_id="abc_buy_point_b",
            rule_name="B Buy Point: MA5 Not Broken",
            rule_version="1.0.0",
            category=RuleCategory.ABC_BUY_POINT,
            description="Price stays above MA5 after pullback, showing short-term strength.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["ma5", "ma10"],
            minimum_history_bars=20,
            entry_conditions=["close > ma5"],
            exit_conditions=["close < ma5"],
            backtestable=True,
            tags=["B_POINT", "ma5"],
        ))
        self.register(StrategyRule(
            rule_id="abc_buy_point_c",
            rule_name="C Buy Point: Reclaim MA20 After Break",
            rule_version="1.0.0",
            category=RuleCategory.ABC_BUY_POINT,
            description="Price breaks below MA20 then reclaims it.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["ma20"],
            minimum_history_bars=40,
            entry_conditions=["close > ma20", "previous_close < ma20"],
            exit_conditions=["close < ma20"],
            backtestable=True,
            tags=["C_POINT", "ma20"],
        ))
        self.register(StrategyRule(
            rule_id="second_wave_momentum",
            rule_name="Strong Stock Second Wave Momentum",
            rule_version="1.0.0",
            category=RuleCategory.SECOND_WAVE,
            description="After primary momentum, price consolidates then launches second wave.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["ma10", "ma20", "volume_ma20"],
            minimum_history_bars=60,
            entry_conditions=["close > ma20", "volume > volume_ma20", "ma10 > ma20"],
            exit_conditions=["close < ma20"],
            backtestable=True,
            tags=["second_wave"],
        ))
        self.register(StrategyRule(
            rule_id="volume_breakout",
            rule_name="Volume Breakout",
            rule_version="1.0.0",
            category=RuleCategory.BREAKOUT,
            description="Price breaks resistance with volume > 1.5x 20-day average.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["volume_ma20", "resistance_level"],
            minimum_history_bars=40,
            entry_conditions=["volume > volume_ma20 * 1.5", "close > resistance_level"],
            exit_conditions=["close < ma20"],
            backtestable=True,
            tags=["volume", "breakout"],
        ))
        self.register(StrategyRule(
            rule_id="moving_average_bullish_alignment",
            rule_name="Moving Average Bullish Alignment",
            rule_version="1.0.0",
            category=RuleCategory.TREND,
            description="MA5 > MA10 > MA20 > MA60, showing bullish alignment.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["ma5", "ma10", "ma20", "ma60"],
            minimum_history_bars=80,
            entry_conditions=["ma5 > ma10", "ma10 > ma20", "ma20 > ma60"],
            exit_conditions=["ma5 < ma10"],
            backtestable=True,
            tags=["trend", "ma_alignment"],
        ))
        self.register(StrategyRule(
            rule_id="institutional_filter",
            rule_name="Institutional Accumulation Filter",
            rule_version="1.0.0",
            category=RuleCategory.INSTITUTIONAL,
            description="Net institutional buying over 3 consecutive days.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily", "institutional_data"],
            required_indicators=["institutional_net_buy_3d"],
            minimum_history_bars=20,
            entry_conditions=["institutional_net_buy_3d > 0"],
            exit_conditions=["institutional_net_sell_3d > 0"],
            backtestable=False,
            tags=["institutional"],
            metadata={"backtestable_note": "Requires institutional data availability — mark NOT_BACKTESTABLE without verified institutional data"},
        ))
        self.register(StrategyRule(
            rule_id="margin_not_out_of_control",
            rule_name="Margin Balance Not Out of Control",
            rule_version="1.0.0",
            category=RuleCategory.RISK_FILTER,
            description="Margin balance ratio not exceeding safety threshold.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily", "margin_data"],
            required_indicators=["margin_balance_ratio"],
            minimum_history_bars=20,
            entry_conditions=["margin_balance_ratio < 0.3"],
            exit_conditions=[],
            backtestable=False,
            tags=["margin", "risk"],
            metadata={"backtestable_note": "Requires margin data — mark NOT_BACKTESTABLE without verified margin data"},
        ))
        self.register(StrategyRule(
            rule_id="fundamental_turnaround",
            rule_name="Fundamental Turnaround Stock",
            rule_version="1.0.0",
            category=RuleCategory.FUNDAMENTAL_TURNAROUND,
            description="EPS or revenue turning positive after negative period.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily", "financial_reports"],
            required_indicators=["eps_yoy_change", "revenue_yoy_change"],
            minimum_history_bars=60,
            entry_conditions=["eps_yoy_change > 0", "revenue_yoy_change > 0"],
            exit_conditions=["eps_yoy_change < 0"],
            backtestable=False,
            tags=["fundamental", "turnaround"],
            metadata={"backtestable_note": "Requires verified quarterly financial data with release timestamps"},
        ))
        self.register(StrategyRule(
            rule_id="sakata_quantifiable",
            rule_name="Sakata Method Quantifiable Patterns",
            rule_version="1.0.0",
            category=RuleCategory.SAKATA,
            description="Quantifiable subset of Sakata candlestick patterns.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["ma5", "ma20"],
            minimum_history_bars=30,
            entry_conditions=["three_method_pattern_detected"],
            exit_conditions=["bearish_reversal_detected"],
            backtestable=True,
            tags=["sakata", "candlestick"],
            metadata={"note": "Only quantifiable subset — narrative patterns excluded"},
        ))
        self.register(StrategyRule(
            rule_id="high_win_rate_framework_v1",
            rule_name="High Win Rate Stock Framework V1 Quantifiable",
            rule_version="1.0.0",
            category=RuleCategory.COMPOSITE,
            description="Quantifiable conditions from the V1 high win rate judgement framework.",
            source="strategy_knowledge",
            source_reference="",
            required_datasets=["ohlcv_daily"],
            required_indicators=["ma10", "ma20", "ma60", "volume_ma20"],
            minimum_history_bars=80,
            entry_conditions=["close > ma10", "ma10 > ma20", "ma20 > ma60", "volume > volume_ma20 * 1.2"],
            exit_conditions=["close < ma20"],
            backtestable=True,
            tags=["composite", "high_win_rate", "v1"],
            metadata={"note": "Only quantifiable conditions included — non-quantifiable narrative excluded"},
        ))
