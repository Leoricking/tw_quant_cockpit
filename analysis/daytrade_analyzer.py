"""
analysis/daytrade_analyzer.py - Intraday (daytrade) analysis and decision engine.

Analyzes 5-level bid/ask, tick momentum, and intraday patterns to
generate buy/sell/hold decisions with price targets.
"""

import logging
import random

from utils.stable_hash import stable_hash_int as _stable_seed

logger = logging.getLogger(__name__)

_DECISIONS = ['BUY_BREAKOUT', 'BUY_PULLBACK', 'HOLD', 'REDUCE', 'EXIT', 'WATCH', 'AVOID']

_SEED_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0,
}


class DaytradeAnalyzer:
    """
    Intraday analysis engine.

    Produces BUY/HOLD/EXIT decisions with add_position, exit, and stop_loss prices.
    Uses order book features for 5-level bid/ask analysis.
    """

    def analyze(self, symbol, price_data=None, bidask_data=None, realtime_data=None,
                mode: str = 'mock'):
        """
        Analyze intraday trading opportunity for a symbol.

        Parameters
        ----------
        symbol : str
        price_data : list or None
            Recent price series (daily or minute-level).
        bidask_data : dict or None
            5-level bid/ask snapshot.
        realtime_data : dict or None
            Latest tick data (price, volume, change_pct).

        Returns
        -------
        dict with keys:
            decision, confidence, add_position_price, exit_price, stop_loss_price,
            no_entry_conditions, reasoning, data_completeness, warning
        """
        sym = str(symbol)

        # Determine data completeness
        available = set()
        if price_data and len(price_data) >= 5:
            available.add('price_daily_20d')
        if bidask_data:
            available.add('bidask_realtime')
        if realtime_data:
            available.add('tick_stream')

        from analysis.timeframe_requirements import check_data_completeness, DATA_INSUFFICIENT_WARNING
        completeness, missing, can_report = check_data_completeness('daytrade', available)

        # data_source: 'real' only when actual data was provided in real mode
        has_real_data = bool(price_data or bidask_data or realtime_data)
        if mode == 'mock':
            data_source = 'mock'
        elif has_real_data:
            data_source = 'real'
        else:
            data_source = 'mock'  # real mode requested but no data available
        from analysis.data_completeness_gate import DataCompletenessGate
        gate = DataCompletenessGate(sym, data_source=data_source, completeness=completeness)
        warning = gate.get_warning() or (DATA_INSUFFICIENT_WARNING if not can_report else None)

        # Get order book features
        ob_state = 'UNKNOWN'
        ob_imbalance = 0.0
        if bidask_data:
            try:
                from features.orderbook_features import OrderbookFeatures
                ob_feat = OrderbookFeatures().compute_orderbook_features(bidask_data)
                ob_state = ob_feat.get('orderbook_state', 'UNKNOWN')
                ob_imbalance = ob_feat.get('orderbook_imbalance', 0.0)
            except Exception as exc:
                logger.warning("OrderbookFeatures error: %s", exc)

        # Get current price estimate
        current_price = self._get_price(sym, price_data, realtime_data)
        if current_price <= 0:
            current_price = _SEED_PRICES.get(sym, 100.0)

        # Mock decision logic when data is limited (stable seed, process-independent)
        rng = random.Random(_stable_seed(sym) % 77777)
        change_pct = 0.0
        if realtime_data and isinstance(realtime_data, dict):
            change_pct = float(realtime_data.get('change_pct', 0) or 0)

        # Decision logic
        no_entry_conditions = []
        if abs(change_pct) > 9:
            no_entry_conditions.append("漲跌停板附近，不追價")
        if ob_state == 'DISTRIBUTION':
            no_entry_conditions.append("盤口出現假買壓，籌碼不健康")
        if ob_state == 'PRESSURE':
            no_entry_conditions.append("賣壓偏重，不宜追高")

        # Determine decision
        if no_entry_conditions:
            decision = 'AVOID'
            confidence = 30
        elif ob_state in ('SUPPORT', 'ACCUMULATION') and change_pct > 0.5:
            decision = 'BUY_BREAKOUT'
            confidence = 70 + rng.randint(0, 15)
        elif ob_state == 'SUPPORT' and change_pct > -0.5:
            decision = 'BUY_PULLBACK'
            confidence = 60 + rng.randint(0, 15)
        elif ob_state == 'PRESSURE' or change_pct < -2:
            decision = 'REDUCE'
            confidence = 55 + rng.randint(0, 15)
        elif change_pct > 2:
            decision = 'WATCH'
            confidence = 50
        else:
            decision = 'HOLD'
            confidence = 50 + rng.randint(-10, 20)

        confidence = min(100, max(0, confidence))

        # Price targets
        tick_size = self._get_tick_size(current_price)
        if decision in ('BUY_BREAKOUT', 'BUY_PULLBACK'):
            add_position_price = round(current_price * 1.003, 1)
            exit_price = round(current_price * 1.015, 1)
            stop_loss_price = round(current_price * 0.992, 1)
        elif decision == 'REDUCE':
            add_position_price = None
            exit_price = round(current_price * 0.998, 1)
            stop_loss_price = round(current_price * 0.985, 1)
        else:
            add_position_price = round(current_price * 0.998, 1)
            exit_price = round(current_price * 1.012, 1)
            stop_loss_price = round(current_price * 0.990, 1)

        # Generate reasoning
        reasoning_parts = [f"盤口狀態: {ob_state}"]
        if ob_imbalance != 0:
            reasoning_parts.append(f"買賣比: {ob_imbalance:+.2f}")
        if change_pct != 0:
            reasoning_parts.append(f"漲跌幅: {change_pct:+.2f}%")
        reasoning_parts.append(f"決策: {decision} (信心度 {confidence}%)")
        reasoning = '，'.join(reasoning_parts)

        # Merge buy point grade fields from BuyPointAnalyzer
        bp_grade = None
        bp_type = None
        bp_support = None
        bp_confirm = None
        bp_invalid = None
        try:
            from analysis.buy_point_analyzer import BuyPointAnalyzer
            bp = BuyPointAnalyzer().analyze(
                sym, price_data=price_data, realtime_data=realtime_data
            )
            bp_grade = bp.get('buy_point_grade')
            bp_type = bp.get('buy_point_type')
            bp_support = bp.get('support_price')
            bp_confirm = bp.get('confirm_price')
            bp_invalid = bp.get('invalid_price')
            # Supplement no_entry_conditions from buy point analyzer
            for cond in bp.get('no_entry_conditions', []):
                if cond not in no_entry_conditions:
                    no_entry_conditions.append(cond)
        except Exception as exc:
            logger.debug("BuyPointAnalyzer skipped in DaytradeAnalyzer: %s", exc)

        return {
            'decision': decision,
            'confidence': confidence,
            'add_position_price': add_position_price,
            'exit_price': exit_price,
            'stop_loss_price': stop_loss_price,
            'no_entry_conditions': no_entry_conditions,
            'reasoning': reasoning,
            'data_completeness': completeness,
            'data_source': data_source,
            'prices_are_estimates': not gate.is_formal_analysis_allowed(),
            'warning': warning,
            'buy_point_grade': bp_grade,
            'buy_point_type': bp_type,
            'support_price': bp_support,
            'confirm_price': bp_confirm,
            'invalid_price': bp_invalid,
        }

    def _get_price(self, symbol, price_data, realtime_data):
        """Extract best available current price."""
        if realtime_data and isinstance(realtime_data, dict):
            p = realtime_data.get('price', 0)
            if p and float(p) > 0:
                return float(p)
        if price_data and len(price_data) > 0:
            last = price_data[-1]
            if isinstance(last, dict):
                p = last.get('close', last.get('Close', 0))
                if p:
                    return float(p)
            else:
                try:
                    return float(last)
                except Exception:
                    pass
        return 0.0

    def _get_tick_size(self, price):
        """Taiwan exchange tick size."""
        if price < 10:
            return 0.01
        elif price < 50:
            return 0.05
        elif price < 100:
            return 0.1
        elif price < 500:
            return 0.5
        elif price < 1000:
            return 1.0
        else:
            return 5.0
