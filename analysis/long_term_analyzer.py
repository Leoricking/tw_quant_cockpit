"""
analysis/long_term_analyzer.py - Long-term (3-12 month) analysis engine.

Uses monthly K, 60/120/240-day MA, and multi-quarter fundamental analysis.
"""

import logging
import random

logger = logging.getLogger(__name__)

_SEED_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0,
}


class LongTermAnalyzer:
    """
    Long-term (3-12 month) analysis engine.

    Focuses on 60/120/240-day MA structure, monthly K trend,
    and multi-quarter fundamental trajectory.
    """

    def analyze(self, symbol, price_data=None, weekly_data=None,
                monthly_data=None, fundamental_data=None):
        """
        Analyze long-term opportunity for a symbol.

        Parameters
        ----------
        symbol : str
        price_data : list or None
            Daily price series (need at least 240 days ideally).
        weekly_data : list or None
            Weekly OHLCV series.
        monthly_data : list or None
            Monthly OHLCV series.
        fundamental_data : dict or None
            Multi-quarter fundamental data.

        Returns
        -------
        dict with decision, confidence, price targets, reasoning, completeness, warning
        """
        sym = str(symbol)

        available = set()
        if price_data and len(price_data) >= 240:
            available.add('price_daily_240d')
        if monthly_data and len(monthly_data) >= 12:
            available.add('price_monthly_12m')
        if fundamental_data:
            available.add('fundamental_annual')

        from analysis.timeframe_requirements import check_data_completeness, DATA_INSUFFICIENT_WARNING
        completeness, missing, can_report = check_data_completeness('long_term', available)

        warning = None
        if not can_report:
            warning = DATA_INSUFFICIENT_WARNING

        current_price = _SEED_PRICES.get(sym, 100.0)
        rng = random.Random(hash(sym + 'long') % 33333)

        score = 0.0
        decision_hints = []

        # Long-term MA analysis
        if price_data and len(price_data) >= 60:
            closes = self._extract_closes(price_data)
            if len(closes) >= 60:
                current_price = closes[-1]
                ma60 = sum(closes[-60:]) / 60
                if current_price > ma60:
                    score += 3.0
                    decision_hints.append('站穩60日均')
                else:
                    score -= 2.0

            if len(closes) >= 120:
                ma120 = sum(closes[-120:]) / 120
                if current_price > ma120:
                    score += 2.0
                    decision_hints.append('站穩120日均')

            if len(closes) >= 240:
                ma240 = sum(closes[-240:]) / 240
                if current_price > ma240:
                    score += 2.0
                    decision_hints.append('站穩年線')
                else:
                    score -= 1.0
                    decision_hints.append('跌破年線，長線謹慎')

        # Monthly data analysis
        if monthly_data and len(monthly_data) >= 6:
            m_closes = self._extract_closes(monthly_data)
            if len(m_closes) >= 6:
                if all(m_closes[i] <= m_closes[i+1] for i in range(-6, -1)):
                    score += 3.0
                    decision_hints.append('月K連漲趨勢')
                elif m_closes[-1] > m_closes[-3]:
                    score += 1.5

        # Mock adjustment
        mock_adj = rng.uniform(-1, 4)
        score += mock_adj

        # Fundamental analysis for long term
        if fundamental_data:
            from features.fundamental_features import FundamentalFeatures
            ff = FundamentalFeatures()
            feat = ff.compute_fundamental_features(sym, fundamental_data)
            score += feat['fundamental_score'] * 0.5
            if not feat['data_missing']:
                decision_hints.append(f"長線基本面{feat['fundamental_score']:.0f}/15")

        # Determine decision
        no_entry = []
        if score >= 7:
            decision = 'BUY_BREAKOUT'
            confidence = min(80, 50 + int(score * 3))
        elif score >= 4:
            decision = 'WATCH'
            confidence = 45
        elif score < 0:
            decision = 'AVOID'
            confidence = 65
            no_entry.append("長線趨勢向下")
        else:
            decision = 'HOLD'
            confidence = 40

        add_price = round(current_price * 1.02, 1)
        exit_price = round(current_price * 1.30, 1)
        stop_price = round(current_price * 0.88, 1)

        reasoning = (
            f"長線評分: {score:.1f}，"
            + ('，'.join(decision_hints) if decision_hints else '歷史資料不足')
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
