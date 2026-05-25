"""
screener/breakout_screener.py - Breakout pattern detection screener.
"""

import logging

logger = logging.getLogger(__name__)


class BreakoutScreener:
    """
    Detects breakout patterns in price data:
    - New 20-day high
    - New 60-day high
    - Volume breakout
    - Bollinger Band squeeze breakout
    """

    def scan(self, symbols, price_data=None):
        """
        Scan symbols for breakout patterns.

        Parameters
        ----------
        symbols : list of str
        price_data : dict, optional
            Mapping symbol -> list of OHLCV dicts or close price list.

        Returns
        -------
        list of dicts, each with:
            symbol, breakout_score (0-15), is_breakout, breakout_types, data_missing
        """
        results = []

        for sym in symbols:
            sym_str = str(sym)
            pdata = None
            if price_data and sym_str in price_data:
                pdata = price_data[sym_str]

            if pdata is None or len(pdata) < 20:
                results.append({
                    'symbol': sym_str,
                    'breakout_score': 3.0,
                    'is_breakout': False,
                    'breakout_types': [],
                    'data_missing': True,
                })
                continue

            result = self._scan_symbol(sym_str, pdata)
            results.append(result)

        return results

    def _scan_symbol(self, symbol, pdata):
        """Compute breakout metrics for a single symbol."""
        try:
            closes = []
            highs = []
            volumes = []

            for p in pdata:
                if isinstance(p, dict):
                    c = p.get('close', p.get('Close'))
                    h = p.get('high', p.get('High', c))
                    v = p.get('volume', p.get('Volume', 0))
                else:
                    c = float(p)
                    h = c
                    v = 0
                if c is not None:
                    closes.append(float(c))
                    highs.append(float(h or c))
                    volumes.append(float(v or 0))

            if len(closes) < 20:
                return {
                    'symbol': symbol,
                    'breakout_score': 3.0,
                    'is_breakout': False,
                    'breakout_types': [],
                    'data_missing': True,
                }

            score = 0.0
            breakout_types = []
            c_now = closes[-1]
            h_now = highs[-1]

            # 20-day high breakout
            high_20 = max(highs[-21:-1]) if len(highs) > 20 else max(highs[:-1])
            if h_now > high_20:
                score += 5.0
                breakout_types.append('20d_high')

            # 60-day high breakout
            if len(highs) >= 60:
                high_60 = max(highs[-61:-1])
                if h_now > high_60:
                    score += 4.0
                    breakout_types.append('60d_high')

            # Volume breakout
            if len(volumes) >= 20:
                avg_vol = sum(volumes[-21:-1]) / 20
                if avg_vol > 0:
                    if volumes[-1] > avg_vol * 2.0:
                        score += 4.0
                        breakout_types.append('vol_breakout_2x')
                    elif volumes[-1] > avg_vol * 1.5:
                        score += 2.0
                        breakout_types.append('vol_breakout_1.5x')

            # Bollinger Band squeeze breakout
            if len(closes) >= 20:
                ma20 = sum(closes[-20:]) / 20
                std20 = (sum((x - ma20)**2 for x in closes[-20:]) / 20) ** 0.5
                upper_bb = ma20 + 2 * std20
                if std20 > 0 and c_now > upper_bb:
                    score += 3.0
                    breakout_types.append('bb_breakout')
                # Squeeze detection: narrow band width
                if len(closes) >= 60:
                    ma20_old = sum(closes[-40:-20]) / 20
                    std20_old = (sum((x - ma20_old)**2 for x in closes[-40:-20]) / 20) ** 0.5
                    if std20_old > 0 and std20 < std20_old * 0.5:
                        score += 2.0
                        breakout_types.append('bb_squeeze')

            is_breakout = len(breakout_types) >= 1 and score >= 5.0

            return {
                'symbol': symbol,
                'breakout_score': round(min(score, 15.0), 2),
                'is_breakout': is_breakout,
                'breakout_types': breakout_types,
                'data_missing': False,
            }

        except Exception as exc:
            logger.warning("BreakoutScreener error for %s: %s", symbol, exc)
            return {
                'symbol': symbol,
                'breakout_score': 3.0,
                'is_breakout': False,
                'breakout_types': [],
                'data_missing': True,
            }
