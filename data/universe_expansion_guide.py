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

        stage = self._stage(symbol_count)

        return {
            'symbol_count':              symbol_count,
            'complete_short_count':      complete_short,
            'complete_mid_count':        complete_mid,
            'complete_long_count':       complete_long,
            'target_min_symbols':        self.TARGET_MIN,
            'target_recommended_symbols': self.TARGET_RECOMMEND,
            'confidence_stage':          stage,
            'missing_summary':           missing_summary,
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
            return 'BETTER_VALIDATION'
        return 'PRODUCTION_LEVEL'

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

        print('')
        print('=' * 60)
        print('  TW Quant Cockpit Universe Expansion Check')
        print('=' * 60)
        print(f'  Current symbols      : {sym}')
        print(f'  Confidence stage     : {stage}')
        print(f'  Min validation target: {result["target_min_symbols"]}')
        print(f'  Recommended target   : {result["target_recommended_symbols"]}-200')
        print('')
        print('  Data completeness:')
        print(f'  Short-term OK : {result["complete_short_count"]} symbols')
        print(f'  Mid-term OK   : {result["complete_mid_count"]} symbols')
        print(f'  Long-term OK  : {result["complete_long_count"]} symbols')
        print('')
        print('  Missing data gaps:')
        for key, count in ms.items():
            status = f'missing in {count} symbols' if count else 'all present'
            print(f'  {key:<20}: {status}')
        print('')
        print('  Import recommendations:')
        for rec in result['recommendations']:
            print(f'  - {rec}')
        print('=' * 60)
