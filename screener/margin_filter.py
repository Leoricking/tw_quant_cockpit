"""
screener/margin_filter.py - Margin balance risk filter for screener pipeline.
"""

import logging

logger = logging.getLogger(__name__)


class MarginFilter:
    """
    Checks margin balance changes to assess risk.

    High risk: margin balance surging while price is near highs.
    Low risk: margin balance declining or stable.
    """

    def filter(self, symbols, margin_data=None):
        """
        Filter symbols by margin risk.

        Parameters
        ----------
        symbols : list of str
        margin_data : dict, optional
            Mapping symbol -> dict with margin_balance_change (%), price_vs_52w_high_pct

        Returns
        -------
        list of dicts, each with:
            symbol, margin_risk_score (0-10), passes, data_missing
        """
        results = []

        for sym in symbols:
            sym_str = str(sym)
            mdata = None
            if margin_data and sym_str in margin_data:
                mdata = margin_data[sym_str]

            if mdata is None:
                results.append({
                    'symbol': sym_str,
                    'margin_risk_score': 5.0,
                    'passes': True,
                    'data_missing': True,
                })
                continue

            try:
                margin_chg = float(mdata.get('margin_balance_change', 0) or 0)
                price_vs_high = float(mdata.get('price_vs_52w_high_pct', 0) or 0)

                # Risk scoring: 0=safe, 10=very risky
                risk = 5.0
                if margin_chg > 10 and price_vs_high > -5:
                    risk = 9.0  # Margin surging at high price = very risky
                elif margin_chg > 5:
                    risk = 7.0
                elif margin_chg > 2:
                    risk = 6.0
                elif margin_chg < -5:
                    risk = 3.0  # Margin declining = healthier
                elif margin_chg < -2:
                    risk = 4.0

                results.append({
                    'symbol': sym_str,
                    'margin_risk_score': round(risk, 1),
                    'passes': risk < 8.0,
                    'data_missing': False,
                })

            except Exception as exc:
                logger.warning("MarginFilter error for %s: %s", sym_str, exc)
                results.append({
                    'symbol': sym_str,
                    'margin_risk_score': 5.0,
                    'passes': True,
                    'data_missing': True,
                })

        return results
