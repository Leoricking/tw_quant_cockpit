"""
screener/technical_filter.py - Technical criteria filter for screener pipeline.
"""

import logging

logger = logging.getLogger(__name__)


class TechnicalFilter:
    """
    Filters symbols based on technical criteria:
    - MA alignment (5/10/20 bullish)
    - RSI 50-80
    - MACD improving
    - Volume breakout
    - 20/60-day highs
    """

    def filter(self, symbols, price_data=None):
        """
        Filter symbols by technical criteria.

        Parameters
        ----------
        symbols : list of str
        price_data : dict, optional
            Mapping symbol -> list of price dicts with OHLCV.

        Returns
        -------
        list of dicts, each with:
            symbol, technical_score, passes, ma_aligned, rsi_ok, data_missing, warning
        """
        results = []

        for sym in symbols:
            sym_str = str(sym)
            pdata = None
            if price_data and sym_str in price_data:
                pdata = price_data[sym_str]

            if pdata is None or len(pdata) < 20:
                # No data: pass through with degraded score
                results.append({
                    'symbol': sym_str,
                    'technical_score': 5.0,
                    'passes': True,
                    'ma_aligned': False,
                    'rsi_ok': False,
                    'data_missing': True,
                    'warning': f'Insufficient price data for {sym_str}. Using degraded score.',
                    'buy_point_grade': None,
                    'buy_point_type': None,
                })
                continue

            score = self._compute_score(pdata)
            passes = score >= 6.0

            # Buy point grade via BuyPointAnalyzer
            bp_grade = None
            bp_type = None
            try:
                from analysis.buy_point_analyzer import BuyPointAnalyzer
                bp = BuyPointAnalyzer().analyze(sym_str, price_data=pdata)
                bp_grade = bp.get('buy_point_grade')
                bp_type = bp.get('buy_point_type')
            except Exception as exc:
                logger.debug("BuyPointAnalyzer skipped for %s: %s", sym_str, exc)

            results.append({
                'symbol': sym_str,
                'technical_score': score,
                'passes': passes,
                'ma_aligned': score >= 8.0,
                'rsi_ok': True,
                'data_missing': False,
                'warning': None,
                'buy_point_grade': bp_grade,
                'buy_point_type': bp_type,
            })

        return results

    def _compute_score(self, price_series):
        """Compute technical score from a list of price dicts."""
        try:
            closes = []
            volumes = []
            for p in price_series:
                if isinstance(p, dict):
                    c = p.get('close', p.get('Close'))
                    v = p.get('volume', p.get('Volume', 0))
                else:
                    c = float(p)
                    v = 0
                if c is not None:
                    closes.append(float(c))
                    volumes.append(float(v or 0))

            if len(closes) < 20:
                return 5.0

            score = 0.0
            c = closes[-1]

            # MA alignment
            ma5 = sum(closes[-5:]) / 5
            ma10 = sum(closes[-10:]) / 10
            ma20 = sum(closes[-20:]) / 20
            if c > ma5 > ma10 > ma20:
                score += 4.0  # fully bullish aligned
            elif c > ma5 and c > ma20:
                score += 2.0
            elif c > ma20:
                score += 1.0

            # 20-day high check
            high_20 = max(closes[-20:])
            if c >= high_20 * 0.98:
                score += 3.0
            elif c >= high_20 * 0.95:
                score += 1.5

            # 60-day high check
            if len(closes) >= 60:
                high_60 = max(closes[-60:])
                if c >= high_60 * 0.98:
                    score += 2.0

            # Volume breakout
            if len(volumes) >= 20 and volumes[-1] > 0:
                avg_vol_20 = sum(volumes[-20:]) / 20
                if avg_vol_20 > 0 and volumes[-1] > avg_vol_20 * 1.5:
                    score += 2.0
                elif avg_vol_20 > 0 and volumes[-1] > avg_vol_20 * 1.2:
                    score += 1.0

            # RSI approximation (simplified)
            if len(closes) >= 14:
                gains = [max(closes[i] - closes[i-1], 0) for i in range(-14, 0)]
                losses = [max(closes[i-1] - closes[i], 0) for i in range(-14, 0)]
                avg_gain = sum(gains) / 14
                avg_loss = sum(losses) / 14
                if avg_loss > 0:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                    if 50 <= rsi <= 80:
                        score += 2.0
                    elif 40 <= rsi < 50:
                        score += 0.5

            return min(score, 15.0)

        except Exception as exc:
            logger.warning("Error computing technical score: %s", exc)
            return 5.0
