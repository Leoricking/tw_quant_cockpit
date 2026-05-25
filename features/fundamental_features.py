"""
features/fundamental_features.py - Fundamental data feature computation.

Computes revenue growth, margin, EPS, and composite fundamental score.
"""

import logging

logger = logging.getLogger(__name__)


class FundamentalFeatures:
    """Computes fundamental features from revenue and EPS data."""

    def compute_fundamental_features(self, symbol, fundamental_data=None):
        """
        Compute fundamental features for a given symbol.

        Parameters
        ----------
        symbol : str
            Stock symbol.
        fundamental_data : dict or None
            Dict containing optional keys:
                latest_month_revenue_yoy (float): monthly revenue YoY %
                accumulated_revenue_yoy (float): accumulated YoY %
                gross_margin (float): gross margin %
                gross_margin_change (float): change in gross margin %
                eps (float): trailing EPS
                eps_yoy (float): EPS YoY %
                eps_qoq (float): EPS QoQ %
                industry_outlook_score (float 0-10)

        Returns
        -------
        dict with keys:
            latest_month_revenue_yoy, accumulated_revenue_yoy, gross_margin,
            gross_margin_change, eps, eps_yoy, eps_qoq, industry_outlook_score,
            fundamental_score (0-15 float),
            data_missing (bool), data_completeness (0-100 float),
            warning (str or None)
        """
        neutral = {
            'latest_month_revenue_yoy': None,
            'accumulated_revenue_yoy': None,
            'gross_margin': None,
            'gross_margin_change': None,
            'eps': None,
            'eps_yoy': None,
            'eps_qoq': None,
            'industry_outlook_score': 5.0,
            'fundamental_score': 5.0,
            'data_missing': True,
            'data_completeness': 0.0,
            'warning': f'No fundamental data available for {symbol}. Using neutral score.',
        }

        if fundamental_data is None or not fundamental_data:
            return neutral

        try:
            d = fundamental_data
            fields_present = 0
            total_fields = 7

            lm_rev_yoy = d.get('latest_month_revenue_yoy')
            acc_rev_yoy = d.get('accumulated_revenue_yoy')
            gross_margin = d.get('gross_margin')
            gm_change = d.get('gross_margin_change')
            eps = d.get('eps')
            eps_yoy = d.get('eps_yoy')
            eps_qoq = d.get('eps_qoq')
            industry_score = d.get('industry_outlook_score', 5.0)

            # Count completeness
            for val in [lm_rev_yoy, acc_rev_yoy, gross_margin, gm_change, eps, eps_yoy, eps_qoq]:
                if val is not None:
                    fields_present += 1

            data_completeness = (fields_present / total_fields) * 100.0

            if fields_present == 0:
                return neutral

            # Compute fundamental score (0-15)
            score = 0.0

            # Revenue YoY component (0-4)
            if lm_rev_yoy is not None:
                if lm_rev_yoy >= 50:
                    score += 4.0
                elif lm_rev_yoy >= 30:
                    score += 3.0
                elif lm_rev_yoy >= 20:
                    score += 2.0
                elif lm_rev_yoy >= 10:
                    score += 1.0
                elif lm_rev_yoy >= 0:
                    score += 0.5

            # Accumulated YoY (0-2)
            if acc_rev_yoy is not None:
                if acc_rev_yoy >= 30:
                    score += 2.0
                elif acc_rev_yoy >= 20:
                    score += 1.5
                elif acc_rev_yoy >= 10:
                    score += 1.0
                elif acc_rev_yoy >= 0:
                    score += 0.5

            # Gross margin (0-3)
            if gross_margin is not None:
                if gross_margin >= 50:
                    score += 3.0
                elif gross_margin >= 35:
                    score += 2.0
                elif gross_margin >= 20:
                    score += 1.0
                else:
                    score += 0.5

            if gm_change is not None:
                if gm_change > 2:
                    score += 1.0
                elif gm_change > 0:
                    score += 0.5
                elif gm_change < -3:
                    score -= 1.0

            # EPS (0-3)
            if eps_yoy is not None:
                if eps_yoy >= 30:
                    score += 3.0
                elif eps_yoy >= 15:
                    score += 2.0
                elif eps_yoy >= 5:
                    score += 1.0
                elif eps_yoy >= 0:
                    score += 0.5

            if eps_qoq is not None:
                if eps_qoq > 10:
                    score += 1.0
                elif eps_qoq > 0:
                    score += 0.5
                elif eps_qoq < -10:
                    score -= 0.5

            # Industry outlook (0-2)
            industry_s = float(industry_score) if industry_score is not None else 5.0
            score += (industry_s / 10.0) * 2.0

            fundamental_score = min(max(score, 0.0), 15.0)

            warning = None
            if data_completeness < 50:
                warning = f'Partial fundamental data for {symbol} ({data_completeness:.0f}% complete). Score may be inaccurate.'

            return {
                'latest_month_revenue_yoy': lm_rev_yoy,
                'accumulated_revenue_yoy': acc_rev_yoy,
                'gross_margin': gross_margin,
                'gross_margin_change': gm_change,
                'eps': eps,
                'eps_yoy': eps_yoy,
                'eps_qoq': eps_qoq,
                'industry_outlook_score': industry_s,
                'fundamental_score': round(fundamental_score, 2),
                'data_missing': False,
                'data_completeness': round(data_completeness, 1),
                'warning': warning,
            }

        except Exception as exc:
            logger.warning("Error computing fundamental features for %s: %s", symbol, exc)
            neutral['warning'] = f'Error computing fundamental features: {exc}'
            return neutral
