"""
screener/fundamental_filter.py - Fundamental criteria filter for screener pipeline.
"""

import logging

logger = logging.getLogger(__name__)


class FundamentalFilter:
    """
    Filters symbols based on fundamental criteria:
    - Monthly revenue YoY > 30%
    - Cumulative YoY > 20%
    - EPS improving (positive YoY or QoQ)
    """

    def filter(self, symbols, fundamental_data=None):
        """
        Filter symbols by fundamental criteria.

        Parameters
        ----------
        symbols : list of str
            Symbols to evaluate.
        fundamental_data : dict, optional
            Mapping of symbol -> fundamental dict. If None, all symbols pass
            with data_missing=True.

        Returns
        -------
        list of dicts, each with:
            symbol, fundamental_score, passes, data_missing, warning
        """
        from features.fundamental_features import FundamentalFeatures
        ff = FundamentalFeatures()
        results = []

        for sym in symbols:
            sym_str = str(sym)
            fund_dict = None
            if fundamental_data and sym_str in fundamental_data:
                fund_dict = fundamental_data[sym_str]

            feat = ff.compute_fundamental_features(sym_str, fund_dict)

            if feat['data_missing']:
                results.append({
                    'symbol': sym_str,
                    'fundamental_score': feat['fundamental_score'],
                    'passes': True,  # Pass through when data missing
                    'data_missing': True,
                    'warning': feat.get('warning', ''),
                })
                continue

            lm_yoy = feat.get('latest_month_revenue_yoy')
            acc_yoy = feat.get('accumulated_revenue_yoy')
            eps_yoy = feat.get('eps_yoy')
            eps_qoq = feat.get('eps_qoq')

            rev_ok = (lm_yoy is None or lm_yoy >= 30) and (acc_yoy is None or acc_yoy >= 20)
            eps_ok = (eps_yoy is None or eps_yoy >= 0) or (eps_qoq is None or eps_qoq >= 0)
            passes = rev_ok or eps_ok or feat['fundamental_score'] >= 8.0

            results.append({
                'symbol': sym_str,
                'fundamental_score': feat['fundamental_score'],
                'passes': passes,
                'data_missing': False,
                'warning': feat.get('warning', ''),
            })

        return results
