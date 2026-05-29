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
                chip_data=None, fundamental_data=None, mode: str = 'mock',
                sector_peers=None, theme_tags=None, leader_df=None,
                eps_ttm=None, gross_margin=None, operating_margin=None):
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

        # Real mode firewall: no real data → block mock prices/conclusions
        has_real_data = bool(price_data or weekly_data or fundamental_data)
        if mode == 'real' and not has_real_data:
            return {
                'decision': 'WATCH',
                'confidence': 0,
                'add_position_price': None,
                'exit_price': None,
                'stop_loss_price': None,
                'no_entry_conditions': ['缺少真實資料，禁止正式進場判斷'],
                'reasoning': 'REAL MODE 缺真實資料，無法給出中線結論',
                'data_completeness': completeness,
                'data_source': 'mock',
                'prices_are_estimates': True,
                'formal_allowed': False,
                'warning': 'REAL MODE 缺真實資料，禁止使用 mock 中線判斷',
            }

        current_price = _SEED_PRICES.get(sym, 100.0)
        from utils.stable_hash import stable_hash_int as _stable_seed
        rng = random.Random(_stable_seed(sym + 'mid') % 44444)

        data_source = 'real' if (mode == 'real' and has_real_data) else 'mock'
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

        # Mock adjustment (only in mock mode)
        if mode == 'mock':
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

        # In real mode with real data, prices are based on actual closes → not estimates
        prices_are_estimates = not (mode == 'real' and has_real_data and price_data and len(price_data) >= 20)
        formal_allowed = not prices_are_estimates

        # ---- Phase 2 signals ----
        _p2 = {}
        if price_data and len(price_data) >= 20:
            try:
                import pandas as pd
                from analysis.sector_rotation_analyzer import analyze_sector_rotation
                _bars = price_data
                if _bars and isinstance(_bars[0], dict):
                    _df2 = pd.DataFrame(_bars)
                    for _c in list(_df2.columns):
                        _lc = _c.lower()
                        if _lc == 'close' and _c != 'close':
                            _df2.rename(columns={_c: 'close'}, inplace=True)
                else:
                    _df2 = pd.DataFrame({'close': [float(b) for b in _bars if b is not None]})
                _sr2 = analyze_sector_rotation(
                    sym, _df2,
                    sector_peers=sector_peers,
                    theme_tags=theme_tags,
                    leader_df=leader_df,
                )
                _p2['sector_rotation'] = _sr2
                if _sr2.get('sector_signal') == 'LEADER_WEAK':
                    no_entry.append("族群指標股轉弱，中線不宜追落後補漲")
            except Exception as _p2e:
                logger.debug("Phase 2 sector_rotation in MidTermAnalyzer: %s", _p2e)

        # Fundamental quality gate for mid-term formal analysis
        _fq_score = 0.5  # neutral default
        _fq_signals = {}
        try:
            from analysis.fundamental_quality_analyzer import analyze_fundamental_quality
            _fq_data = fundamental_data or {}
            _fqkw = {k: _fq_data[k] for k in (
                'monthly_revenue_rows', 'eps_ttm', 'eps_qoq_change',
                'gross_margin', 'gross_margin_prev', 'operating_margin',
                'operating_margin_prev', 'price_vs_ma20', 'price_vs_ma60',
            ) if k in _fq_data}
            # Also accept direct kwargs
            if eps_ttm is not None:
                _fqkw.setdefault('eps_ttm', eps_ttm)
            if gross_margin is not None:
                _fqkw.setdefault('gross_margin', gross_margin)
            if operating_margin is not None:
                _fqkw.setdefault('operating_margin', operating_margin)
            _fq_result = analyze_fundamental_quality(symbol=sym, **_fqkw)
            _fq_signals = _fq_result
            _fq_score = _fq_result.get('fundamental_quality_score', 0.5)
            _p2['fundamental_quality'] = _fq_result
            if _fq_result.get('earnings_risk_warning'):
                no_entry.append(f"財報風險：{_fq_result['earnings_risk_warning']}")
            # Gate formal_allowed when fundamental data insufficient or quality too low
            if not _fq_data and eps_ttm is None and gross_margin is None:
                formal_allowed = False
                warning = (warning or '') + ' 缺基本面資料，中線不允許正式判斷'
                warning = warning.strip()
        except Exception as _fqe:
            logger.debug("Phase 2 fundamental_quality in MidTermAnalyzer: %s", _fqe)

        # Valuation signal via valuation_river when EPS available
        _val_signals = {}
        if eps_ttm is not None:
            try:
                from analysis.valuation_river_analyzer import analyze_valuation_river
                _val_signals = analyze_valuation_river(
                    current_price=current_price,
                    estimated_eps=eps_ttm,
                )
                _p2['valuation'] = _val_signals
            except Exception as _ve:
                logger.debug("Phase 2 valuation_river in MidTermAnalyzer: %s", _ve)

        return {
            'decision': decision,
            'confidence': confidence,
            'add_position_price': add_price,
            'exit_price': exit_price,
            'stop_loss_price': stop_price,
            'no_entry_conditions': no_entry,
            'reasoning': reasoning,
            'data_completeness': completeness,
            'data_source': data_source,
            'prices_are_estimates': prices_are_estimates,
            'formal_allowed': formal_allowed,
            'warning': warning,
            'sector_rotation_signals': _p2.get('sector_rotation', {}),
            'fundamental_quality_signals': _fq_signals,
            'fundamental_quality_score': _fq_score,
            'valuation_signals': _val_signals,
            'phase2_signals': _p2,
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
