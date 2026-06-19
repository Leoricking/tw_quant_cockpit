"""
abc_validation/rule_adapters_v141.py — Adapters for A/B/C buy point domain logic v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Wraps existing BuyPointAnalyzer and empirical_backtest rule registry.
No new A/B/C logic is defined here.
"""
from __future__ import annotations
from typing import Optional


class ABuyPointRuleAdapter:
    """Adapter for A buy point: delegates to existing BuyPointAnalyzer and rule registry."""
    rule_id = "abc_buy_point_a"
    buy_point_type = "A"
    support_ma = "MA10"

    def get_rule(self):
        from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
        reg = StrategyKnowledgeRuleRegistry()
        return reg.get("abc_buy_point_a")

    def analyze(self, symbol, price_data=None, chip_data=None, realtime_data=None, mode='mock'):
        from analysis.buy_point_analyzer import BuyPointAnalyzer
        result = BuyPointAnalyzer().analyze(symbol, price_data, chip_data, realtime_data, mode=mode)
        return result

    def is_a_signal(self, result: dict) -> Optional[str]:
        """Returns signal subtype or None."""
        if result.get('buy_point_grade') == 'A':
            return 'A_STRICT'
        return None


class BBuyPointRuleAdapter:
    """Adapter for B buy point."""
    rule_id = "abc_buy_point_b"
    buy_point_type = "B"
    support_ma = "MA5"

    def get_rule(self):
        from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
        reg = StrategyKnowledgeRuleRegistry()
        return reg.get("abc_buy_point_b")

    def analyze(self, symbol, price_data=None, chip_data=None, realtime_data=None, mode='mock'):
        from analysis.buy_point_analyzer import BuyPointAnalyzer
        result = BuyPointAnalyzer().analyze(symbol, price_data, chip_data, realtime_data, mode=mode)
        return result

    def is_b_signal(self, result: dict) -> Optional[str]:
        if result.get('buy_point_grade') == 'B':
            return 'B_STRICT'
        return None


class CBuyPointRuleAdapter:
    """Adapter for C buy point."""
    rule_id = "abc_buy_point_c"
    buy_point_type = "C"
    support_ma = "MA20"

    def get_rule(self):
        from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
        reg = StrategyKnowledgeRuleRegistry()
        return reg.get("abc_buy_point_c")

    def analyze(self, symbol, price_data=None, chip_data=None, realtime_data=None, mode='mock'):
        from analysis.buy_point_analyzer import BuyPointAnalyzer
        result = BuyPointAnalyzer().analyze(symbol, price_data, chip_data, realtime_data, mode=mode)
        return result

    def is_c_signal(self, result: dict) -> Optional[str]:
        if result.get('buy_point_grade') == 'C':
            return 'C_STRICT_RECLAIM'
        return None
