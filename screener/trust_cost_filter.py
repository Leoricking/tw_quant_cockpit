"""
screener/trust_cost_filter.py - Investment trust cost support filter.
"""

import logging

logger = logging.getLogger(__name__)


class TrustCostFilter:
    """
    Checks if price is above investment trust average cost.

    When price is near or above trust cost, trust funds tend to
    provide support. When below cost, trust may sell (risk).
    """

    def filter(self, symbols, trust_cost_data=None, price_data=None, mode: str = 'mock'):
        """
        Filter symbols by trust cost support.

        Parameters
        ----------
        symbols : list of str
        trust_cost_data : dict, optional
            Mapping symbol -> dict with investment_trust_avg_cost_5d
        price_data : dict, optional
            Mapping symbol -> current price (float) or price series

        Returns
        -------
        list of dicts, each with:
            symbol, trust_cost_support_score (0-10), passes, data_missing
        """
        results = []

        for sym in symbols:
            sym_str = str(sym)

            # Get current price
            current_price = None
            if price_data and sym_str in price_data:
                pdata = price_data[sym_str]
                if isinstance(pdata, (int, float)):
                    current_price = float(pdata)
                elif isinstance(pdata, list) and pdata:
                    last = pdata[-1]
                    if isinstance(last, dict):
                        current_price = float(last.get('close', last.get('Close', 0)) or 0)
                    else:
                        try:
                            current_price = float(last)
                        except Exception:
                            pass

            # Get trust cost
            trust_cost = None
            if trust_cost_data and sym_str in trust_cost_data:
                tdata = trust_cost_data[sym_str]
                if isinstance(tdata, dict):
                    trust_cost = tdata.get('investment_trust_avg_cost_5d')
                else:
                    try:
                        trust_cost = float(tdata)
                    except Exception:
                        pass

            if trust_cost is None or current_price is None:
                results.append({
                    'symbol': sym_str,
                    'trust_cost_support_score': 5.0,
                    'passes': mode == 'mock',  # real mode: missing = do not pass
                    'data_missing': True,
                })
                continue

            try:
                tc = float(trust_cost)
                cp = float(current_price)
                if tc <= 0:
                    support_score = 5.0
                else:
                    pct_above = (cp - tc) / tc * 100.0
                    if -2 <= pct_above <= 5:
                        support_score = 8.0  # near trust cost, strong support
                    elif 5 < pct_above <= 15:
                        support_score = 6.0
                    elif pct_above > 15:
                        support_score = 4.0  # far above cost, less support
                    else:
                        support_score = 3.0  # below cost, trust may sell

                results.append({
                    'symbol': sym_str,
                    'trust_cost_support_score': round(support_score, 1),
                    'passes': support_score >= 4.0,
                    'data_missing': False,
                })

            except Exception as exc:
                logger.warning("TrustCostFilter error for %s: %s", sym_str, exc)
                results.append({
                    'symbol': sym_str,
                    'trust_cost_support_score': 5.0,
                    'passes': mode == 'mock',
                    'data_missing': True,
                })

        return results
