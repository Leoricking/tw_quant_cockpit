"""
analysis/mid_term_analyzer.py - Mid-term (1-3 month) analysis engine.

Uses weekly K, 20/60-day MA, and fundamental trend analysis.
"""

import logging
import random

logger = logging.getLogger(__name__)

_SEED_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0,
}


class MidTermAnalyzer:
    """
    Mid-term (1-3 month) analysis engine.

    Focuses on weekly K trend, 20/60-day MA structure, and
    fundamental improvement trajectory.
    """

    def analyze(self, symbol, price_data=None, weekly_data=None,
                chip_data=None, fundamental_data=None):
        """
        Analyze mid-term opportunity for a symbol.

        Parameters
        ----------
        symbol : str
        price_data : list or None
            Daily price series.
        weekly_data : list or None
            Weekly OHLCV series.
        chip_data : dict or None
        fundamental_data : dict or None

        Returns
        -------
        dict with decision, confidence, price targets, reasoning, completeness, warning
        """
        sym = str(symbol)

        available = set()
        if price_data and len(price_data) >= 60:
            available.add('price_daily_60d')
        if weekly_data and len(weekly_data) >= 12:
            available.add('price_weekly_12w')
        if chip_data:
            available.add('chip_10d')
        if fundamental_data:
            available.add('fundamental_quarterly')

        from analysis.timeframe_requirements import check_data_completeness, DATA_INSUFFICIENT_WARNING
        completeness, missing, can_report = check_data_completeness('mid_term', available)

        warning = None
        if not can_report:
            warning = DATA_INSUFFICIENT_WARNING

        current_price = _SEED_PRICES.get(sym, 100.0)
        rng = random.Random(hash(sym + 'mid') % 44444)

        score = 0.0
        decision_hints = []

        # Analyze daily price if available
        if price_data and len(price_data) >= 60:
            closes = self._extract_closes(price_data)
            if len(closes) >= 60:
                current_price = closes[-1]
                ma20 = sum(closes[-20:]) / 20
                ma60 = sum(closes[-60:]) / 60

                if current_price > ma20 > ma60:
                    score += 4.0
                    decision_hints.append('ma多頭排列')
                elif current_price > ma60:
                    score += 2.0
                    decision_hints.append('站穩60日均')
                else:
                    score -= 2.0
                    decision_hints.append('跌破60日均')

        # Analyze weekly data
        if weekly_data and len(weekly_data) >= 12:
            w_closes = self._extract_closes(weekly_data)
            if len(w_closes) >= 12:
                w_ma5 = sum(w_closes[-5:]) / 5
                w_ma10 = sum(w_closes[-10:]) / 10
                if w_closes[-1] > w_ma5 > w_ma10:
                    score += 3.0
                    decision_hints.append('週K多頭')

        # Mock adjustment
        mock_adj = rng.uniform(-2, 5)
        score += mock_adj

        # Fundamental bonus
        if fundamental_data:
            from features.fundamental_features import FundamentalFeatures
            ff = FundamentalFeatures()
            feat = ff.compute_fundamental_features(sym, fundamental_data)
            score += feat['fundamental_score'] * 0.3
            if not feat['data_missing']:
                decision_hints.append(f"基本面{feat['fundamental_score']:.0f}/15")

        # Determine decision
        no_entry = []
        if score >= 6:
            decision = 'BUY_BREAKOUT'
            confidence = min(85, 55 + int(score * 3))
        elif score >= 3:
            decision = 'WATCH'
            confidence = 50
        elif score < 0:
            decision = 'AVOID'
            confidence = 60
            no_entry.append("中線趨勢偏空")
        else:
            decision = 'HOLD'
            confidence = 45

        add_price = round(current_price * 1.01, 1)
        exit_price = round(current_price * 1.15, 1)
        stop_price = round(current_price * 0.93, 1)

        reasoning = (
            f"中線評分: {score:.1f}，"
            + ('，'.join(decision_hints) if decision_hints else '資料有限')
            + f"，信心度: {confidence}%"
        )

        return {
            'decision': decision,
            'confidence': confidence,
            'add_position_price': add_price,
            'exit_price': exit_price,
            'stop_loss_price': stop_price,
            'no_entry_conditions': no_entry,
            'reasoning': reasoning,
            'data_completeness': completeness,
            'warning': warning,
        }

    def _extract_closes(self, data):
        """Extract close prices from a list."""
        closes = []
        for p in data:
            if isinstance(p, dict):
                c = p.get('close', p.get('Close'))
            else:
                try:
                    c = float(p)
                except Exception:
                    c = None
            if c is not None:
                closes.append(float(c))
        return closes
