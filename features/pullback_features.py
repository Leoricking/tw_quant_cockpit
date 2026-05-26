"""
features/pullback_features.py - Pullback and buy point feature computation.

Computes MA, KD stochastic, volume, VWAP, and platform box features
needed for the BuyPointAnalyzer (A/B/C grade buy point detection).
"""

import logging

logger = logging.getLogger(__name__)


def compute_pullback_features(price_data, chip_data=None, realtime_data=None):
    """
    Compute pullback-related features from price data.

    Parameters
    ----------
    price_data : list of dict
        Each dict has keys: open, high, low, close, volume (case-insensitive).
    chip_data : dict or None
        Institutional flow data; keys: foreign_net_3d, trust_net_3d.
    realtime_data : dict or None
        Intraday data; keys: current_price, vwap, orderbook_imbalance, change_pct.

    Returns
    -------
    dict with computed features.
    """
    result = {
        'ma5': None, 'ma10': None, 'ma20': None,
        'k': None, 'd': None,
        'current_price': None,
        'today_low': None, 'today_high': None,
        'avg_volume_5d': None, 'today_volume': None,
        'avg_volume_20d': None,
        'vwap': None, 'orderbook_imbalance': None,
        'box_high': None, 'box_low': None, 'box_range_pct': None,
        'upper_shadow_pct': None,
        'foreign_net_3d': None, 'trust_net_3d': None,
        'data_bars': 0,
    }

    if not price_data or len(price_data) < 5:
        return result

    # Parse OHLCV
    opens, highs, lows, closes, volumes = [], [], [], [], []
    for p in price_data:
        if isinstance(p, dict):
            o = p.get('open', p.get('Open'))
            h = p.get('high', p.get('High'))
            l = p.get('low', p.get('Low'))
            c = p.get('close', p.get('Close'))
            v = p.get('volume', p.get('Volume', 0))
        else:
            o = h = l = c = float(p)
            v = 0
        if c is not None:
            opens.append(float(o or c))
            highs.append(float(h or c))
            lows.append(float(l or c))
            closes.append(float(c))
            volumes.append(float(v or 0))

    n = len(closes)
    result['data_bars'] = n

    if n < 5:
        return result

    # Moving averages
    result['ma5'] = sum(closes[-5:]) / 5
    if n >= 10:
        result['ma10'] = sum(closes[-10:]) / 10
    if n >= 20:
        result['ma20'] = sum(closes[-20:]) / 20

    result['current_price'] = closes[-1]
    result['today_low'] = lows[-1]
    result['today_high'] = highs[-1]

    # Volume averages (5d uses prior 5 bars excluding today; 20d includes today)
    if n >= 6:
        result['avg_volume_5d'] = sum(volumes[-6:-1]) / 5
    elif n >= 5:
        result['avg_volume_5d'] = sum(volumes[-5:]) / 5
    if n >= 20:
        result['avg_volume_20d'] = sum(volumes[-20:]) / 20
    result['today_volume'] = volumes[-1]

    # Upper shadow (long wick ratio)
    today_open = opens[-1]
    today_close = closes[-1]
    today_high = highs[-1]
    today_low_val = lows[-1]
    body_top = max(today_open, today_close)
    candle_range = today_high - today_low_val
    result['upper_shadow_pct'] = ((today_high - body_top) / candle_range) if candle_range > 0 else 0.0

    # KD stochastic (9-period simplified Wilder smoothing)
    kd_period = min(9, n)
    if n >= kd_period:
        k = 50.0
        d = 50.0
        for i in range(-kd_period, 0):
            start = max(0, n + i - kd_period + 1)
            end = n + i + 1
            ph = max(highs[start:end]) if highs[start:end] else highs[i]
            pl = min(lows[start:end]) if lows[start:end] else lows[i]
            rsv_i = (closes[i] - pl) / (ph - pl) * 100 if ph != pl else 50.0
            k = k * (2 / 3) + rsv_i * (1 / 3)
            d = d * (2 / 3) + k * (1 / 3)
        result['k'] = round(k, 2)
        result['d'] = round(d, 2)

    # Platform box detection (last 10-20 bars, excluding today)
    box_bars = min(20, n - 1)
    if box_bars >= 10:
        box_closes = closes[-(box_bars + 1):-1]
        box_high = max(box_closes)
        box_low = min(box_closes)
        if box_low > 0:
            result['box_high'] = box_high
            result['box_low'] = box_low
            result['box_range_pct'] = (box_high - box_low) / box_low

    # Realtime / intraday overrides
    if realtime_data and isinstance(realtime_data, dict):
        vwap = realtime_data.get('vwap')
        if vwap:
            result['vwap'] = float(vwap)
        ob = realtime_data.get('orderbook_imbalance')
        if ob is not None:
            result['orderbook_imbalance'] = float(ob)
        cp = realtime_data.get('current_price') or realtime_data.get('price')
        if cp:
            result['current_price'] = float(cp)
        low_rt = realtime_data.get('today_low') or realtime_data.get('low')
        if low_rt:
            result['today_low'] = float(low_rt)

    # Institutional chip data
    if chip_data and isinstance(chip_data, dict):
        result['foreign_net_3d'] = chip_data.get('foreign_net_3d', chip_data.get('foreign_net'))
        result['trust_net_3d'] = chip_data.get('trust_net_3d', chip_data.get('trust_net'))

    return result
