"""
data/universe_expansion_guide.py - Universe expansion status checker.

Reads the current profile universe, checks per-symbol data completeness,
and generates an actionable import plan to reach 50-200 symbols.

Usage:
    from data.universe_expansion_guide import UniverseExpansionGuide
    guide  = UniverseExpansionGuide()
    result = guide.analyze()
    guide.print_summary()

Return format of analyze():
    {
        "symbol_count": 3,
        "complete_short_count": 3,
        "complete_mid_count": 2,
        "complete_long_count": 1,
        "target_min_symbols": 50,
        "target_recommended_symbols": 100,
        "confidence_stage": "FUNCTIONAL_TEST",
        "missing_summary": {
            "daily": 0,
            "institutional": 0,
            "margin": 0,
            "monthly_revenue": 0,
            "holder": 0,
            "trust_cost": 0,
        },
        "recommendations": [ ... ],
    }
"""

import logging

logger = logging.getLogger(__name__)


class UniverseExpansionGuide:
    """Analyses universe completeness and recommends import steps."""

    TARGET_MIN        = 50
    TARGET_RECOMMEND  = 100

    def analyze(self) -> dict:
        """Return a completeness summary dict for the current universe."""
        from data.data_quality_checker import DataQualityChecker

        checker = DataQualityChecker()
        df = checker.check_universe()

        symbol_count    = 0
        complete_short  = 0
        complete_mid    = 0
        complete_long   = 0
        missing_summary = {
            'daily': 0, 'institutional': 0, 'margin': 0,
            'monthly_revenue': 0, 'holder': 0, 'trust_cost': 0,
        }

        if df is not None and hasattr(df, 'empty') and not df.empty:
            symbol_count   = len(df)
            complete_short = int(df['short_allowed'].sum()) if 'short_allowed' in df.columns else 0
            complete_mid   = int(df['mid_allowed'].sum())   if 'mid_allowed'   in df.columns else 0
            complete_long  = int(df['long_allowed'].sum())  if 'long_allowed'  in df.columns else 0

            col_map = {
                'daily':            'daily_rows',
                'institutional':    'institutional_rows',
                'margin':           'margin_rows',
                'monthly_revenue':  'monthly_revenue_rows',
                'holder':           'holder_rows',
                'trust_cost':       'trust_cost_rows',
            }
            for key, col in col_map.items():
                if col in df.columns:
                    missing_summary[key] = int((df[col] == 0).sum())

        stage    = self._stage(symbol_count)
        coverage = self._compute_data_coverage(df)

        return {
            'symbol_count':              symbol_count,
            'complete_short_count':      complete_short,
            'complete_mid_count':        complete_mid,
            'complete_long_count':       complete_long,
            'target_min_symbols':        self.TARGET_MIN,
            'target_recommended_symbols': self.TARGET_RECOMMEND,
            'confidence_stage':          stage,
            'missing_summary':           missing_summary,
            'data_coverage':             coverage,
            'recommendations':           self.recommend_import_plan(),
        }

    @staticmethod
    def _stage(symbol_count: int) -> str:
        if symbol_count < 10:
            return 'FUNCTIONAL_TEST'
        if symbol_count < 50:
            return 'SMALL_SAMPLE'
        if symbol_count < 100:
            return 'BASIC_VALIDATION'
        if symbol_count < 200:
            return 'GOOD_VALIDATION'
        return 'PRACTICAL_SAMPLE'

    def recommend_import_plan(self) -> list:
        """Return an ordered list of import step recommendations."""
        return [
            (
                f'Step 1: Import profile CSV with at least {self.TARGET_MIN} symbols'
                f' (target: {self.TARGET_RECOMMEND}-200)'
            ),
            'Step 2: Import daily K for each symbol — at least 120 trading days',
            'Step 3: Import institutional data — at least 40 days per symbol',
            'Step 4: Import margin data — at least 40 days per symbol',
            'Step 5: Import monthly revenue — at least 12 months per symbol',
            'Step 6: Import holder data — at least 4 periods per symbol',
            'Step 7: Import trust cost data — at least 20-40 days per symbol',
        ]

    def print_summary(self) -> None:
        """Print a plain-text universe expansion summary to stdout."""
        result = self.analyze()
        sym    = result['symbol_count']
        stage  = result['confidence_stage']
        ms     = result['missing_summary']
        dc     = result.get('data_coverage', {})

        print('')
        print('=' * 65)
        print('  TW Quant Cockpit Universe Expansion Check')
        print('=' * 65)
        print(f'  Current universe symbols : {sym}')
        print(f'  Confidence stage         : {stage}')
        print(f'  Min validation target    : {result["target_min_symbols"]}')
        print(f'  Recommended target       : {result["target_recommended_symbols"]}-200')
        print('')
        print('  Data readiness:')
        print(f'  daily >= 120         : {dc.get("daily_120", 0)} symbols')
        print(f'  institutional >= 40  : {dc.get("institutional_40", 0)} symbols')
        print(f'  margin >= 40         : {dc.get("margin_40", 0)} symbols')
        print(f'  revenue >= 12        : {dc.get("revenue_12", 0)} symbols')
        print(f'  holder >= 4          : {dc.get("holder_4", 0)} symbols')
        print(f'  trust_cost >= 20     : {dc.get("trust_cost_20", 0)} symbols')
        print('')
        print('  Formal analysis allowed:')
        print(f'  Short-term OK        : {result["complete_short_count"]} symbols')
        print(f'  Mid-term OK          : {result["complete_mid_count"]} symbols')
        print(f'  Long-term OK         : {result["complete_long_count"]} symbols')
        print('')
        print('  Missing data gaps:')
        for key, count in ms.items():
            status = f'missing in {count} symbols' if count else 'all present'
            print(f'  {key:<22}: {status}')
        print('')

        # Contextual next-step recommendations based on current stage
        print('  Next steps:')
        if sym < 50:
            print('  - Run: python main.py build-universe --template top50 --replace')
            print('  - Import 120 days of daily K for each symbol')
            print('  - Import 40 days of institutional / margin data')
            print('  - Import 12 months of monthly_revenue')
        elif sym < 100:
            print('  - Run: python main.py build-universe --template top100 to expand')
            print('  - Supplement holder and trust_cost data')
        else:
            print('  - Universe size is adequate for validate-score')
            print('  - Check for industry concentration bias')
            print('  - Supplement missing mid/long-term data as needed')
        print('')
        print('  Import order recommendations:')
        for rec in result['recommendations']:
            print(f'  - {rec}')
        print('=' * 65)

    def _compute_data_coverage(self, df) -> dict:
        """Return counts of symbols meeting key data thresholds."""
        coverage = {
            'daily_120': 0,
            'institutional_40': 0,
            'margin_40': 0,
            'revenue_12': 0,
            'holder_4': 0,
            'trust_cost_20': 0,
        }
        if df is None or (hasattr(df, 'empty') and df.empty):
            return coverage
        col_threshold = {
            'daily_rows':            ('daily_120',        120),
            'institutional_rows':    ('institutional_40',  40),
            'margin_rows':           ('margin_40',         40),
            'monthly_revenue_rows':  ('revenue_12',        12),
            'holder_rows':           ('holder_4',           4),
            'trust_cost_rows':       ('trust_cost_20',     20),
        }
        for col, (key, thr) in col_threshold.items():
            if col in df.columns:
                coverage[key] = int((df[col] >= thr).sum())
        return coverage
