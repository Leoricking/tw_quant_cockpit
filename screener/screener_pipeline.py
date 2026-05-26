"""
screener/screener_pipeline.py - 4-layer Taiwan stock screener pipeline.

Layers:
  1. Theme pool filter (~100-200 symbols)
  2. Fundamental filter (~30-60 symbols)
  3. Technical filter (~10-20 symbols)
  4. Chip confirmation (3-8 symbols)

Computes a 0-100 bull stock score and returns top candidates.
"""

import hashlib
import os
import random
import logging
from datetime import datetime


def _stable_seed(key: str) -> int:
    """Return a process-stable integer seed derived from a string via MD5."""
    return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)

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

    def run(self, mock_data=None):
        """
        Run all 4 layers of the screener pipeline.

        Parameters
        ----------
        mock_data : bool or dict, optional
            If True or dict, uses mock data. If False, attempts real data (falls back to mock).

        Returns
        -------
        list of dicts with scored symbols
        """
        use_mock = (mock_data is True) or (mock_data is None)

        logger.info("ScreenerPipeline.run() starting (mock_data=%s).", use_mock)

        # Load theme pools
        from screener.theme_pool import ThemePool
        theme_pool = ThemePool()
        theme_pool.load()

        # Layer 1: Theme pool
        all_theme_symbols = list(theme_pool.get_symbols())
        if not all_theme_symbols:
            # Fallback to hardcoded symbol list
            all_theme_symbols = list(_STOCK_NAMES.keys())
        logger.info("Layer 1 (Theme): %d symbols", len(all_theme_symbols))

        # Generate mock data if needed
        price_data_mock = None
        if use_mock:
            price_data_mock = self._generate_mock_price_data(all_theme_symbols)

        # Layer 2: Fundamental filter
        from screener.fundamental_filter import FundamentalFilter
        fund_results = FundamentalFilter().filter(all_theme_symbols, fundamental_data=None)
        after_fund = [r['symbol'] for r in fund_results if r['passes']]
        logger.info("Layer 2 (Fundamental): %d symbols pass", len(after_fund))

        # Layer 3: Technical filter
        from screener.technical_filter import TechnicalFilter
        tech_results = TechnicalFilter().filter(after_fund, price_data=price_data_mock)
        after_tech = [r['symbol'] for r in tech_results if r['passes']]
        logger.info("Layer 3 (Technical): %d symbols pass", len(after_tech))

        # If too few pass, loosen the constraint for mock mode
        if len(after_tech) < 5 and use_mock:
            after_tech = after_fund[:min(15, len(after_fund))]
            logger.info("Layer 3 loosened (mock): using top %d", len(after_tech))

        # Layer 4: Chip confirmation
        from screener.chip_filter import ChipFilter
        chip_results = ChipFilter().filter(after_tech, chip_data=None)
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
                'name': _STOCK_NAMES.get(sym, sym),
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
