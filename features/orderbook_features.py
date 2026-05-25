"""
features/orderbook_features.py - Order book (5-level bid/ask) feature computation.

Computes order book imbalance, wall detection, spread, and market state classification.
"""

import logging

logger = logging.getLogger(__name__)

_NEUTRAL_RESULT = {
    'bid_sum_5': 0.0,
    'ask_sum_5': 0.0,
    'orderbook_imbalance': 0.0,
    'bid_wall_ratio': 0.0,
    'ask_wall_ratio': 0.0,
    'spread_pct': 0.0,
    'mid_price': 0.0,
    'fake_bid_risk': False,
    'fake_ask_risk': False,
    'orderbook_state': 'UNKNOWN',
    'data_missing': True,
    'warning': 'No orderbook data provided.',
}


class OrderbookFeatures:
    """Computes 5-level order book features."""

    def compute_orderbook_features(self, bidask_data=None):
        """
        Compute order book features from 5-level bid/ask data.

        Parameters
        ----------
        bidask_data : dict or None
            Dict with keys: bid_price_1..5, bid_volume_1..5, ask_price_1..5, ask_volume_1..5

        Returns
        -------
        dict with order book feature keys and orderbook_state.
        """
        if bidask_data is None or not bidask_data:
            return dict(_NEUTRAL_RESULT)

        try:
            # Extract bid/ask prices and volumes
            bid_prices = []
            bid_volumes = []
            ask_prices = []
            ask_volumes = []

            for i in range(1, 6):
                bp = bidask_data.get(f'bid_price_{i}', 0) or 0
                bv = bidask_data.get(f'bid_volume_{i}', 0) or 0
                ap = bidask_data.get(f'ask_price_{i}', 0) or 0
                av = bidask_data.get(f'ask_volume_{i}', 0) or 0
                bid_prices.append(float(bp))
                bid_volumes.append(float(bv))
                ask_prices.append(float(ap))
                ask_volumes.append(float(av))

            bid_sum_5 = sum(bid_volumes)
            ask_sum_5 = sum(ask_volumes)

            total = bid_sum_5 + ask_sum_5
            if total == 0:
                result = dict(_NEUTRAL_RESULT)
                result['data_missing'] = False
                result['warning'] = 'All orderbook volumes are zero.'
                return result

            # Order book imbalance: positive = bid heavy, negative = ask heavy
            orderbook_imbalance = (bid_sum_5 - ask_sum_5) / total

            # Wall detection: a "wall" is a single level > 40% of total side volume
            bid_wall_ratio = max(bid_volumes) / bid_sum_5 if bid_sum_5 > 0 else 0.0
            ask_wall_ratio = max(ask_volumes) / ask_sum_5 if ask_sum_5 > 0 else 0.0

            # Spread and mid price
            best_bid = bid_prices[0] if bid_prices[0] > 0 else None
            best_ask = ask_prices[0] if ask_prices[0] > 0 else None

            if best_bid and best_ask and best_bid > 0 and best_ask > 0:
                mid_price = (best_bid + best_ask) / 2.0
                spread_pct = (best_ask - best_bid) / mid_price * 100.0
            elif best_bid:
                mid_price = best_bid
                spread_pct = 0.0
            elif best_ask:
                mid_price = best_ask
                spread_pct = 0.0
            else:
                mid_price = 0.0
                spread_pct = 0.0

            # Fake order risk: large wall at far price levels (levels 4-5)
            # Bid fake: bid_volume_4 or 5 is significantly larger than level 1
            far_bid_vol = sum(bid_volumes[3:5])
            far_ask_vol = sum(ask_volumes[3:5])
            fake_bid_risk = (far_bid_vol > bid_volumes[0] * 2) and (far_bid_vol > bid_sum_5 * 0.4)
            fake_ask_risk = (far_ask_vol > ask_volumes[0] * 2) and (far_ask_vol > ask_sum_5 * 0.4)

            # Determine order book state
            state = self._classify_state(
                orderbook_imbalance, bid_wall_ratio, ask_wall_ratio,
                spread_pct, fake_bid_risk, fake_ask_risk
            )

            return {
                'bid_sum_5': round(bid_sum_5, 0),
                'ask_sum_5': round(ask_sum_5, 0),
                'orderbook_imbalance': round(orderbook_imbalance, 4),
                'bid_wall_ratio': round(bid_wall_ratio, 4),
                'ask_wall_ratio': round(ask_wall_ratio, 4),
                'spread_pct': round(spread_pct, 4),
                'mid_price': round(mid_price, 2),
                'fake_bid_risk': fake_bid_risk,
                'fake_ask_risk': fake_ask_risk,
                'orderbook_state': state,
                'data_missing': False,
                'warning': None,
            }

        except Exception as exc:
            logger.warning("Error computing orderbook features: %s", exc)
            result = dict(_NEUTRAL_RESULT)
            result['warning'] = f'Error computing orderbook features: {exc}'
            return result

    def _classify_state(self, imbalance, bid_wall, ask_wall, spread_pct,
                        fake_bid, fake_ask):
        """Classify the overall order book state."""
        # DISTRIBUTION: fake bid (large wall being pulled) + ask heavy
        if fake_bid and imbalance < -0.1:
            return 'DISTRIBUTION'
        # ACCUMULATION: genuine large bid wall + bid heavy + not fake
        if bid_wall > 0.5 and imbalance > 0.2 and not fake_bid:
            return 'ACCUMULATION'
        # SUPPORT: moderate bid imbalance
        if imbalance > 0.15 and not fake_bid:
            return 'SUPPORT'
        # PRESSURE: ask heavy
        if imbalance < -0.15 and not fake_ask:
            return 'PRESSURE'
        # BALANCED
        if abs(imbalance) <= 0.15:
            return 'BALANCED'
        return 'UNKNOWN'
