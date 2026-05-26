"""
screener/screener_pipeline.py - 4-layer Taiwan stock screener pipeline.

Layers:
  1. Theme pool filter (~100-200 symbols)
  2. Fundamental filter (~30-60 symbols)
  3. Technical filter (~10-20 symbols)
  4. Chip confirmation (3-8 symbols)

Computes a 0-100 bull stock score and returns top candidates.
"""

import os
import random
import logging
from datetime import datetime

from utils.stable_hash import stable_hash_int as _stable_seed

logger = logging.getLogger(__name__)

# Score weights
_WEIGHTS = {
    'theme_score': 20,
    'fundamental_score': 15,
    'ma_score': 15,
    'breakout_score': 15,
    'chip_score': 15,
    'holder_score': 10,
    'margin_score': 5,
    'overheat_score': 5,
}

_SEED_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0, '3231': 95.0, '2356': 55.0,
    '3661': 2100.0, '3443': 980.0, '3035': 210.0, '2368': 75.0,
    '3037': 135.0, '6213': 110.0, '3324': 320.0, '3653': 400.0,
    '2421': 85.0, '2301': 95.0, '6412': 260.0, '2359': 210.0,
    '8374': 155.0, '1593': 55.0, '2464': 75.0, '2327': 580.0,
    '3036': 55.0, '3702': 50.0, '6196': 180.0,
}

_STOCK_NAMES = {
    '2330': '台積電', '2454': '聯發科', '2382': '廣達', '2317': '鴻海',
    '6669': '緯穎', '3661': '世芯-KY', '2345': '智邦', '3017': '奇鋐',
    '2308': '台達電', '2383': '台光電', '3231': '緯創', '2356': '英業達',
    '3443': '創意', '3035': '智原', '2368': '金像電', '3037': '欣興',
    '6213': '聯茂', '3324': '雙鴻', '3653': '健策', '2421': '建準',
    '2301': '光寶科', '6412': '群電', '2359': '所羅門', '8374': '羅昇',
    '1593': '祺驊', '2464': '盟立', '2327': '國巨', '3036': '文曄',
    '3702': '大聯大', '6196': '帆宣',
}


class ScreenerPipeline:
    """
    4-layer Taiwan stock screener pipeline.

    Usage:
        pipeline = ScreenerPipeline()
        pipeline.run(mock_data=True)
        top = pipeline.get_top_candidates(n=8)
    """

    def __init__(self):
        """Initialize the screener pipeline."""
        self._results = []
        self._top_candidates = None
        self._ran = False

    def run(self, mock_data=None, mode: str = 'mock'):
        """
        Run all 4 layers of the screener pipeline.

        Parameters
        ----------
        mock_data : bool or dict, optional
            Legacy parameter. If provided, overrides *mode*.
        mode : str
            ``'mock'`` — use stable synthetic data (default).
            ``'real'`` — use DB / FinMind; missing data → passes=False.

        Returns
        -------
        list of dicts with scored symbols
        """
        # Legacy compatibility: mock_data=True → mode='mock', False → mode='real'
        if mock_data is True:
            mode = 'mock'
        elif mock_data is False:
            mode = 'real'
        use_mock = (mode == 'mock')

        logger.info("ScreenerPipeline.run() starting (mode=%s).", mode)

        # In real mode, build universe from profile CSV first
        profile_universe = {}  # sym -> name (from CSV)
        if not use_mock:
            try:
                from data.real_data_loader import RealDataLoader
                import os as _os
                _profile_dir = _os.path.join(
                    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                    "data", "import", "profile"
                )
                _loader = RealDataLoader()
                import csv as _csv
                for _fname in _os.listdir(_profile_dir) if _os.path.isdir(_profile_dir) else []:
                    if _fname.endswith(".csv"):
                        _fpath = _os.path.join(_profile_dir, _fname)
                        with open(_fpath, "r", encoding="utf-8-sig") as _fh:
                            for _row in _csv.DictReader(_fh):
                                _s = _row.get("symbol", "").strip()
                                _n = _row.get("name", "").strip()
                                if _s:
                                    profile_universe[_s] = _n or _s
                logger.info("Real mode: loaded %d symbols from profile CSV", len(profile_universe))
            except Exception as _exc:
                logger.warning("Failed to load profile CSV in real mode: %s", _exc)

        # Load theme pools
        from screener.theme_pool import ThemePool
        theme_pool = ThemePool()
        theme_pool.load()

        # Layer 1: Theme pool
        if not use_mock and profile_universe:
            # Real mode: universe = profile CSV symbols only
            all_theme_symbols = list(profile_universe.keys())
            logger.info("Layer 1 (Theme, real CSV): %d symbols", len(all_theme_symbols))
        else:
            all_theme_symbols = list(theme_pool.get_symbols())
            if not all_theme_symbols:
                # Fallback to hardcoded symbol list
                all_theme_symbols = list(_STOCK_NAMES.keys())
            logger.info("Layer 1 (Theme): %d symbols", len(all_theme_symbols))

        # Load price data and real CSV data
        from data.data_source_router import DataSourceRouter
        router = DataSourceRouter(mode=mode)
        price_data_mock = {}
        for sym in all_theme_symbols:
            pdata = router.get_price_data(sym, n_bars=120)
            if pdata is not None:
                price_data_mock[sym] = pdata
        if not price_data_mock:
            price_data_mock = None

        # In real mode, load fundamental and chip data from CSVs
        real_fundamental_map = {}  # sym -> fundamental dict
        real_chip_map = {}         # sym -> chip dict
        if not use_mock:
            try:
                from data.real_data_loader import RealDataLoader
                _loader = RealDataLoader()
                for sym in all_theme_symbols:
                    _rev = _loader.load_monthly_revenue(sym)
                    if _rev:
                        # Map RealDataLoader keys → FundamentalFeatures keys
                        real_fundamental_map[sym] = {
                            'latest_month_revenue_yoy': _rev.get('yoy'),
                            'accumulated_revenue_yoy': _rev.get('accumulated_yoy'),
                            'gross_margin': None,
                            'gross_margin_change': None,
                            'eps': None,
                            'eps_yoy': None,
                            'eps_qoq': None,
                            'industry_outlook_score': 5.0,
                        }
                    _chip = _loader.load_institutional(sym)
                    if _chip:
                        # Map RealDataLoader keys → ChipFeatures keys
                        real_chip_map[sym] = {
                            'foreign_3d_net_buy': _chip.get('foreign_net_3d', 0),
                            'foreign_5d_net_buy': _chip.get('foreign_net_3d', 0),
                            'investment_trust_3d_net_buy': _chip.get('trust_net_3d', 0),
                            'investment_trust_5d_net_buy': _chip.get('trust_net_3d', 0),
                            'dealer_3d_net_buy': _chip.get('dealer_net_3d', 0),
                            'dealer_5d_net_buy': _chip.get('dealer_net_3d', 0),
                        }
                logger.info("Real mode: loaded fundamental=%d, chip=%d from CSV",
                            len(real_fundamental_map), len(real_chip_map))
            except Exception as _exc:
                logger.warning("Failed to load real CSV data for screener: %s", _exc)

        # Layer 2: Fundamental filter
        from screener.fundamental_filter import FundamentalFilter
        _fund_data_arg = real_fundamental_map if (not use_mock and real_fundamental_map) else None
        fund_results = FundamentalFilter().filter(
            all_theme_symbols, fundamental_data=_fund_data_arg, mode=mode)
        after_fund = [r['symbol'] for r in fund_results if r['passes']]
        logger.info("Layer 2 (Fundamental): %d symbols pass", len(after_fund))

        # Layer 3: Technical filter
        from screener.technical_filter import TechnicalFilter
        tech_results = TechnicalFilter().filter(
            after_fund, price_data=price_data_mock, mode=mode)
        after_tech = [r['symbol'] for r in tech_results if r['passes']]
        logger.info("Layer 3 (Technical): %d symbols pass", len(after_tech))

        # If too few pass in mock mode, loosen the constraint
        if len(after_tech) < 5 and use_mock:
            after_tech = after_fund[:min(15, len(after_fund))]
            logger.info("Layer 3 loosened (mock): using top %d", len(after_tech))

        # Layer 4: Chip confirmation
        from screener.chip_filter import ChipFilter
        _chip_data_arg = real_chip_map if (not use_mock and real_chip_map) else None
        chip_results = ChipFilter().filter(after_tech, chip_data=_chip_data_arg, mode=mode)
        after_chip = [r['symbol'] for r in chip_results if r['passes']]
        logger.info("Layer 4 (Chip): %d symbols pass", len(after_chip))

        # Build index for quick lookup
        fund_idx = {r['symbol']: r for r in fund_results}
        tech_idx = {r['symbol']: r for r in tech_results}
        chip_idx = {r['symbol']: r for r in chip_results}

        # Breakout scan
        from screener.breakout_screener import BreakoutScreener
        breakout_results = BreakoutScreener().scan(after_chip or after_tech, price_data=price_data_mock)
        breakout_idx = {r['symbol']: r for r in breakout_results}

        # Theme features for scoring
        from features.theme_features import ThemeFeatures
        tf = ThemeFeatures()
        theme_pools_data = tf.load_theme_pools()

        # Assemble final scored list
        scored = []
        candidate_symbols = after_chip if after_chip else after_tech[:15]

        for sym in candidate_symbols:
            theme_feat = tf.compute_theme_features(sym, theme_pools_data)
            fund_r = fund_idx.get(sym, {'fundamental_score': 5.0, 'data_missing': True})
            tech_r = tech_idx.get(sym, {'technical_score': 5.0, 'data_missing': True})
            chip_r = chip_idx.get(sym, {'chip_score': 5.0, 'data_missing': True})
            bo_r = breakout_idx.get(sym, {'breakout_score': 3.0, 'is_breakout': False})

            # Add mock boost for demo variety (stable across processes)
            if use_mock:
                rng = random.Random(_stable_seed(sym) % 99999)
                mock_boost = rng.uniform(0, 20)
            else:
                mock_boost = 0

            score_data = {
                'theme_score': theme_feat['theme_score'],
                'fundamental_score': fund_r.get('fundamental_score', 5.0),
                'ma_score': tech_r.get('technical_score', 5.0),
                'breakout_score': bo_r.get('breakout_score', 3.0),
                'chip_score': chip_r.get('chip_score', 5.0),
                'holder_score': 5.0,
                'margin_score': 5.0,
                'overheat_score': 5.0,
            }

            bull_score = self.compute_bull_stock_score(score_data)
            if use_mock:
                bull_score = min(100.0, bull_score + mock_boost)

            themes = theme_feat.get('theme_tags', [])
            theme_str = '/'.join(themes[:3]) if themes else '未分類'

            # Generate reason/risk summary
            reason_parts = []
            if theme_feat['is_mainstream_theme']:
                reason_parts.append(f"主流主題({theme_str})")
            if bo_r.get('is_breakout'):
                reason_parts.append("突破型態")
            if tech_r.get('ma_aligned'):
                reason_parts.append("均線多頭排列")
            if not fund_r.get('data_missing'):
                reason_parts.append("基本面佐證")
            reason_summary = '，'.join(reason_parts) if reason_parts else '待觀察'

            risk_parts = []
            if chip_r.get('data_missing'):
                risk_parts.append("籌碼資料不足")
            if fund_r.get('data_missing'):
                risk_parts.append("基本面資料不足")
            risk_summary = '；'.join(risk_parts) if risk_parts else '風險可控'

            is_bull = bull_score >= 80
            is_second_wave = 65 <= bull_score < 80

            scored.append({
                'symbol': sym,
                'name': profile_universe.get(sym) or _STOCK_NAMES.get(sym, sym),
                'theme_tags': themes,
                'data_source': 'mock' if use_mock else 'real',
                'bull_stock_score': round(bull_score, 1),
                'theme_score': round(theme_feat['theme_score'], 2),
                'fundamental_score': round(fund_r.get('fundamental_score', 5.0), 2),
                'technical_score': round(tech_r.get('technical_score', 5.0), 2),
                'chip_score': round(chip_r.get('chip_score', 5.0), 2),
                'breakout_score': round(bo_r.get('breakout_score', 3.0), 2),
                'margin_risk_score': round(5.0, 2),
                'overheat_risk_score': round(100 - bull_score, 1),
                'is_bull_candidate': is_bull,
                'is_second_wave_buy_point': is_second_wave,
                'reason_summary': reason_summary,
                'risk_summary': risk_summary,
            })

        # Sort by score descending
        scored.sort(key=lambda x: x['bull_stock_score'], reverse=True)
        self._results = scored
        self._ran = True

        logger.info("ScreenerPipeline complete: %d scored symbols.", len(scored))
        return scored

    def compute_bull_stock_score(self, score_data):
        """
        Compute 0-100 composite bull stock score.

        Parameters
        ----------
        score_data : dict
            Keys: theme_score (0-20), fundamental_score (0-15), ma_score (0-15),
                  breakout_score (0-15), chip_score (0-15), holder_score (0-10),
                  margin_score (0-5), overheat_score (0-5)

        Returns
        -------
        float (0-100)
        """
        # Normalize each component to 0-1 and apply weight
        components = {
            'theme_score': (score_data.get('theme_score', 0), 20),
            'fundamental_score': (score_data.get('fundamental_score', 0), 15),
            'ma_score': (score_data.get('ma_score', 0), 15),
            'breakout_score': (score_data.get('breakout_score', 0), 15),
            'chip_score': (score_data.get('chip_score', 0), 15),
            'holder_score': (score_data.get('holder_score', 0), 10),
            'margin_score': (score_data.get('margin_score', 0), 5),
            'overheat_score': (score_data.get('overheat_score', 0), 5),
        }

        total = 0.0
        for key, (value, max_val) in components.items():
            if max_val > 0:
                normalized = min(float(value or 0) / max_val, 1.0)
                total += normalized * max_val

        return round(min(max(total, 0.0), 100.0), 2)

    def get_top_candidates(self, n=8):
        """
        Get the top N candidates as a DataFrame.

        Parameters
        ----------
        n : int
            Number of top candidates to return.

        Returns
        -------
        pandas.DataFrame with columns:
            symbol, name, theme_tags, bull_stock_score, theme_score,
            fundamental_score, technical_score, chip_score, margin_risk_score,
            overheat_risk_score, is_bull_candidate, is_second_wave_buy_point,
            reason_summary, risk_summary
        """
        try:
            import pandas as pd
        except ImportError:
            logger.error("pandas not available.")
            return None

        if not self._ran:
            self.run(mock_data=True)

        if not self._results:
            return pd.DataFrame()

        top = self._results[:n]
        df = pd.DataFrame(top)

        # Ensure all required columns exist
        required_cols = [
            'symbol', 'name', 'theme_tags', 'bull_stock_score', 'theme_score',
            'fundamental_score', 'technical_score', 'chip_score', 'margin_risk_score',
            'overheat_risk_score', 'is_bull_candidate', 'is_second_wave_buy_point',
            'reason_summary', 'risk_summary',
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = None

        return df[required_cols]

    def _generate_mock_price_data(self, symbols):
        """Generate mock price time series for testing."""
        import random as rand_mod

        price_data = {}
        for sym in symbols:
            sym_str = str(sym)
            base = _SEED_PRICES.get(sym_str, 100.0)
            rng = rand_mod.Random(_stable_seed(sym_str) % 88888)
            prices = []
            price = base * rng.uniform(0.7, 0.9)  # start below current

            for i in range(120):
                # Trending up with noise
                change = rng.gauss(0.003, 0.015)
                price = price * (1 + change)
                price = max(price, 1.0)
                volume = rng.randint(100, 10000) * 1000
                prices.append({
                    'close': round(price, 1),
                    'high': round(price * rng.uniform(1.001, 1.02), 1),
                    'low': round(price * rng.uniform(0.98, 0.999), 1),
                    'open': round(price * rng.uniform(0.99, 1.01), 1),
                    'volume': volume,
                })

            price_data[sym_str] = prices

        return price_data
