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
                monthly_data=None, fundamental_data=None, mode: str = 'mock',
                monthly_revenue_rows=None, eps_ttm=None,
                gross_margin=None, operating_margin=None,
                fundamental_ready: bool = False,
                announcement_date: str = None,
                announcement_date_is_estimated: bool = False):
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

        # Real mode firewall: no real data → block mock prices/conclusions
        has_real_data = bool(price_data or monthly_data or fundamental_data)
        if mode == 'real' and not has_real_data:
            return {
                'decision': 'WATCH',
                'confidence': 0,
                'add_position_price': None,
                'exit_price': None,
                'stop_loss_price': None,
                'no_entry_conditions': ['缺少真實資料，禁止正式進場判斷'],
                'reasoning': 'REAL MODE 缺真實資料，無法給出長線結論',
                'data_completeness': completeness,
                'data_source': 'mock',
                'prices_are_estimates': True,
                'formal_allowed': False,
                'warning': 'REAL MODE 缺真實資料，禁止使用 mock 長線判斷',
            }

        current_price = _SEED_PRICES.get(sym, 100.0)
        from utils.stable_hash import stable_hash_int as _stable_seed
        rng = random.Random(_stable_seed(sym + 'long') % 33333)

        data_source = 'real' if (mode == 'real' and has_real_data) else 'mock'
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

        # Mock adjustment (only in mock mode)
        if mode == 'mock':
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

        prices_are_estimates = not (mode == 'real' and has_real_data and price_data and len(price_data) >= 60)
        formal_allowed = not prices_are_estimates

        # ---- Phase 2: fundamental quality + valuation + EPS/margin guards ----
        _fq_signals = {}
        _val_signals = {}
        _p2 = {}
        try:
            from analysis.fundamental_quality_analyzer import analyze_fundamental_quality
            _fq_data = fundamental_data or {}
            _fqkw = {k: _fq_data[k] for k in (
                'monthly_revenue_rows', 'eps_ttm', 'eps_qoq_change',
                'gross_margin', 'gross_margin_prev', 'operating_margin',
                'operating_margin_prev', 'price_vs_ma20', 'price_vs_ma60',
            ) if k in _fq_data}
            if monthly_revenue_rows is not None:
                _fqkw.setdefault('monthly_revenue_rows', monthly_revenue_rows)
            if eps_ttm is not None:
                _fqkw.setdefault('eps_ttm', eps_ttm)
            if gross_margin is not None:
                _fqkw.setdefault('gross_margin', gross_margin)
            if operating_margin is not None:
                _fqkw.setdefault('operating_margin', operating_margin)
            _fq_result = analyze_fundamental_quality(symbol=sym, **_fqkw)
            _fq_signals = _fq_result
            _p2['fundamental_quality'] = _fq_result
            if _fq_result.get('earnings_risk_warning'):
                no_entry.append(f"財報風險：{_fq_result['earnings_risk_warning']}")
            # EPS / 毛利率 / 月營收 guard: 缺這些不允許正式長線價位
            _missing_fundamental = (
                eps_ttm is None
                and gross_margin is None
                and monthly_revenue_rows is None
                and not _fq_data
            )
            if _missing_fundamental:
                formal_allowed = False
                warning = (warning or '') + ' 缺 EPS / 毛利率 / 月營收，長線不允許正式價位判斷'
                warning = warning.strip()
            # v0.3.9: fundamental_ready gate
            if not fundamental_ready and has_real_data:
                formal_allowed = False
                warning = (warning or '') + ' fundamental_ready=False，長線正式判斷降為 PARTIAL'
                warning = warning.strip()
            if announcement_date is not None and announcement_date_is_estimated:
                warning = (warning or '') + f' [TIMING_ESTIMATED] announcement_date 為估計值 ({announcement_date}) — 使用法定申報期限推算，非 MOPS 實際公告日'
                warning = warning.strip()
            elif announcement_date is None and (eps_ttm is not None or gross_margin is not None):
                warning = (warning or '') + ' [WARN] announcement_date 未知 — fundamental timing may be approximate'
                warning = warning.strip()
        except Exception as _fqe:
            logger.debug("Phase 2 fundamental_quality in LongTermAnalyzer: %s", _fqe)

        if eps_ttm is not None:
            try:
                from analysis.valuation_river_analyzer import analyze_valuation_river
                _val_signals = analyze_valuation_river(
                    current_price=current_price,
                    estimated_eps=eps_ttm,
                )
                _p2['valuation'] = _val_signals
            except Exception as _ve:
                logger.debug("Phase 2 valuation_river in LongTermAnalyzer: %s", _ve)

        # ---- Stable backtest output fields (v0.3.11) ----
        _eps_positive = None
        if eps_ttm is not None:
            _eps_positive = eps_ttm > 0

        def _eps_bucket(v):
            if v is None:
                return 'EPS_UNKNOWN'
            if v <= 0:
                return 'EPS_NEGATIVE'
            if v <= 3:
                return 'EPS_LOW'
            if v <= 10:
                return 'EPS_MED'
            return 'EPS_HIGH'

        def _gm_bucket(v):
            if v is None:
                return 'GM_UNKNOWN'
            if v < 0.20:
                return 'GM_LOW'
            if v < 0.40:
                return 'GM_MED'
            if v < 0.60:
                return 'GM_HIGH'
            return 'GM_VERY_HIGH'

        def _om_bucket(v):
            if v is None:
                return 'OM_UNKNOWN'
            if v < 0:
                return 'OM_NEG'
            if v < 0.10:
                return 'OM_LOW'
            if v < 0.20:
                return 'OM_MED'
            return 'OM_HIGH'

        _timing_quality = 'UNKNOWN'
        if announcement_date is not None:
            _timing_quality = 'ESTIMATED' if announcement_date_is_estimated else 'MOPS'

        _val_zone = _val_signals.get('valuation_zone', 'UNAVAILABLE')
        _pe_bucket = _val_signals.get('pe_bucket', 'NO_EPS')

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
            'fundamental_quality_signals': _fq_signals,
            'valuation_signals': _val_signals,
            'phase2_signals': _p2,
            # --- Stable backtest fields (v0.3.11) ---
            'long_term_score':           round(score, 2),
            'long_term_signal':          decision,
            'long_term_buy_allowed':     decision == 'BUY_BREAKOUT' and formal_allowed,
            'long_term_watch_only':      decision in ('WATCH', 'HOLD'),
            'long_term_exit_warning':    decision == 'AVOID' or score < 0,
            'eps_positive':              _eps_positive,
            'eps_growth_bucket':         _eps_bucket(eps_ttm),
            'gross_margin_bucket':       _gm_bucket(gross_margin),
            'operating_margin_bucket':   _om_bucket(operating_margin),
            'valuation_zone':            _val_zone,
            'pe_bucket':                 _pe_bucket,
            'timing_quality':            _timing_quality,
            'timing_estimated':          announcement_date_is_estimated,
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
