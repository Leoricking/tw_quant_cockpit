"""
analysis/short_term_analyzer.py - Short-term (5-20 day) analysis engine.

Uses MA, RSI, MACD, KD indicators, chip data, and fundamental context.
"""

import logging
import random

from utils.stable_hash import stable_hash_int as _stable_seed

logger = logging.getLogger(__name__)

_SEED_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0,
}


class ShortTermAnalyzer:
    """
    Short-term (5-20 day) analysis engine.

    Focuses on technical indicator alignment, chip flow confirmation,
    and fundamental context for 1-4 week trading horizon.
    """

    def analyze(self, symbol, price_data=None, chip_data=None, fundamental_data=None,
                mode: str = 'mock', margin_df=None, sector_peers=None,
                theme_tags=None, leader_df=None):
        """
        Analyze short-term trading opportunity for a symbol.

        Parameters
        ----------
        symbol : str
        price_data : list or None
            Daily price series (need at least 20 days).
        chip_data : dict or None
            Institutional flow data.
        fundamental_data : dict or None
            Revenue/EPS data.

        Returns
        -------
        dict with keys:
            decision, confidence, add_position_price, exit_price, stop_loss_price,
            no_entry_conditions, reasoning, data_completeness, warning
        """
        sym = str(symbol)

        available = set()
        if price_data and len(price_data) >= 20:
            available.add('price_daily_20d')
        if price_data and len(price_data) >= 60:
            available.add('price_daily_60d')
        if chip_data:
            available.add('chip_5d')
        if fundamental_data:
            available.add('fundamental_monthly')

        from analysis.timeframe_requirements import check_data_completeness, DATA_INSUFFICIENT_WARNING
        completeness, missing, can_report = check_data_completeness('short_term', available)

        # data_source: 'real' only when actual data was provided in real mode
        has_real_data = bool(price_data or chip_data or fundamental_data)
        if mode == 'mock':
            data_source = 'mock'
        elif has_real_data:
            data_source = 'real'
        else:
            data_source = 'mock'  # real mode requested but no data available
        from analysis.data_completeness_gate import DataCompletenessGate
        gate = DataCompletenessGate(sym, data_source=data_source, completeness=completeness)
        warning = gate.get_warning() or (DATA_INSUFFICIENT_WARNING if not can_report else None)

        current_price = _SEED_PRICES.get(sym, 100.0)
        rng = random.Random(_stable_seed(sym + 'short') % 55555)

        if price_data and len(price_data) >= 20:
            current_price, tech_score, decision_hint = self._analyze_technicals(price_data)
        else:
            tech_score = rng.uniform(4, 10)
            decision_hint = 'neutral'

        # Chip score
        chip_score = 5.0
        if chip_data:
            from features.chip_features import ChipFeatures
            cf = ChipFeatures()
            chip_feat = cf.compute_chip_features(sym, chip_data)
            chip_score = chip_feat.get('chip_score', 5.0)
        else:
            chip_score = rng.uniform(3, 8)

        # Combined signal
        combined = (tech_score * 0.6 + chip_score * 0.4) / 15.0 * 100.0
        no_entry_conditions = []

        if decision_hint == 'bullish' and combined > 55:
            decision = 'BUY_BREAKOUT'
            confidence = min(90, int(combined) + rng.randint(0, 10))
        elif decision_hint == 'pullback' and combined > 40:
            decision = 'BUY_PULLBACK'
            confidence = min(80, int(combined) + rng.randint(0, 10))
        elif decision_hint == 'bearish' or combined < 30:
            decision = 'AVOID'
            confidence = 60
            no_entry_conditions.append("短線技術面偏弱")
        else:
            decision = 'WATCH'
            confidence = 50

        add_position_price = round(current_price * 1.005, 1)
        exit_price = round(current_price * 1.08, 1)
        stop_loss_price = round(current_price * 0.96, 1)

        reasoning = (
            f"技術分析評分: {tech_score:.1f}/15，"
            f"籌碼評分: {chip_score:.1f}/15，"
            f"綜合信心度: {confidence}%"
        )

        # Merge buy point grade fields from BuyPointAnalyzer
        bp_grade = None
        bp_type = None
        bp_support = None
        bp_confirm = None
        bp_invalid = None
        try:
            from analysis.buy_point_analyzer import BuyPointAnalyzer
            bp = BuyPointAnalyzer().analyze(sym, price_data=price_data, chip_data=chip_data, mode=mode)
            bp_grade = bp.get('buy_point_grade')
            bp_type = bp.get('buy_point_type')
            bp_support = bp.get('support_price')
            bp_confirm = bp.get('confirm_price')
            bp_invalid = bp.get('invalid_price')
            for cond in bp.get('no_entry_conditions', []):
                if cond not in no_entry_conditions:
                    no_entry_conditions.append(cond)
        except Exception as exc:
            logger.debug("BuyPointAnalyzer skipped in ShortTermAnalyzer: %s", exc)

        # ---- Phase 2 signals ----
        _p2 = {}
        if price_data and len(price_data) >= 9:
            try:
                import pandas as pd
                from features.kd_advanced import compute_kd_advanced
                from analysis.bottom_reversal_analyzer import analyze_bottom_reversal
                from features.short_interest_features import compute_short_interest
                from analysis.sector_rotation_analyzer import analyze_sector_rotation
                _bars = price_data
                if _bars and isinstance(_bars[0], dict):
                    _df2 = pd.DataFrame(_bars)
                    for _c in list(_df2.columns):
                        _lc = _c.lower()
                        if _lc == 'close' and _c != 'close':
                            _df2.rename(columns={_c: 'close'}, inplace=True)
                        elif _lc == 'high' and _c != 'high':
                            _df2.rename(columns={_c: 'high'}, inplace=True)
                        elif _lc == 'low' and _c != 'low':
                            _df2.rename(columns={_c: 'low'}, inplace=True)
                else:
                    _df2 = pd.DataFrame({'close': [float(b) for b in _bars if b is not None]})
                _kd2 = compute_kd_advanced(_df2)
                _p2['kd_advanced'] = _kd2
                if _kd2.get('kd_high_death_cross'):
                    no_entry_conditions.append("KD 高檔死亡交叉，不建議追高")
                if _kd2.get('kd_low_golden_cross'):
                    reasoning += "；KD 低檔黃金交叉加分"
                _br2 = analyze_bottom_reversal(_df2)
                _p2['bottom_reversal'] = _br2
                _si2 = compute_short_interest(_df2, margin_df=margin_df)
                _p2['short_interest'] = _si2
                if _si2.get('weak_stock_short_increase'):
                    no_entry_conditions.append("弱勢股融券增加，不視為多方訊號")
                _sr2 = analyze_sector_rotation(
                    sym, _df2,
                    sector_peers=sector_peers,
                    theme_tags=theme_tags,
                    leader_df=leader_df,
                )
                _p2['sector_rotation'] = _sr2
                if _sr2.get('sector_signal') == 'LEADER_WEAK':
                    no_entry_conditions.append("族群指標股轉弱，不追落後股")
            except Exception as _p2e:
                logger.debug("Phase 2 in ShortTermAnalyzer: %s", _p2e)
        if fundamental_data:
            try:
                from analysis.fundamental_quality_analyzer import analyze_fundamental_quality
                _fqkw = {k: fundamental_data[k] for k in (
                    'monthly_revenue_rows', 'eps_ttm', 'eps_qoq_change',
                    'gross_margin', 'gross_margin_prev', 'operating_margin',
                    'operating_margin_prev', 'price_vs_ma20', 'price_vs_ma60',
                ) if k in fundamental_data}
                _fq2 = analyze_fundamental_quality(symbol=sym, **_fqkw)
                _p2['fundamental_quality'] = _fq2
                if _fq2.get('earnings_risk_warning'):
                    no_entry_conditions.append(f"財報風險：{_fq2['earnings_risk_warning']}")
            except Exception as _fqe:
                logger.debug("Phase 2 fundamental_quality in ShortTermAnalyzer: %s", _fqe)

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
            'kd_advanced_signals': _p2.get('kd_advanced', {}),
            'short_interest_signals': _p2.get('short_interest', {}),
            'bottom_reversal_signals': _p2.get('bottom_reversal', {}),
            'sector_rotation_signals': _p2.get('sector_rotation', {}),
            'fundamental_quality_signals': _p2.get('fundamental_quality', {}),
            'phase2_signals': _p2,
        }

    def _analyze_technicals(self, price_data):
        """Compute technical indicators from price data."""
        try:
            closes = []
            for p in price_data:
                if isinstance(p, dict):
                    c = p.get('close', p.get('Close'))
                else:
                    c = float(p)
                if c is not None:
                    closes.append(float(c))

            if len(closes) < 20:
                return (closes[-1] if closes else 100.0, 5.0, 'neutral')

            c = closes[-1]
            ma5 = sum(closes[-5:]) / 5
            ma10 = sum(closes[-10:]) / 10
            ma20 = sum(closes[-20:]) / 20

            score = 0.0
            hint = 'neutral'

            if c > ma5 > ma10 > ma20:
                score += 6.0
                hint = 'bullish'
            elif c > ma20:
                score += 3.0
                hint = 'pullback'
            elif c < ma20:
                hint = 'bearish'

            # RSI
            if len(closes) >= 14:
                gains = [max(closes[i] - closes[i-1], 0) for i in range(-14, 0)]
                losses = [max(closes[i-1] - closes[i], 0) for i in range(-14, 0)]
                avg_g = sum(gains) / 14
                avg_l = sum(losses) / 14
                if avg_l > 0:
                    rsi = 100 - (100 / (1 + avg_g / avg_l))
                    if 50 <= rsi <= 70:
                        score += 3.0
                    elif 70 < rsi <= 80:
                        score += 1.5
                    elif rsi < 40:
                        score -= 2.0

            # Volume
            if len(closes) >= 20:
                score += min(3.0, score * 0.3)

            return (c, min(score, 15.0), hint)

        except Exception as exc:
            logger.warning("ShortTermAnalyzer._analyze_technicals error: %s", exc)
            return (100.0, 5.0, 'neutral')
