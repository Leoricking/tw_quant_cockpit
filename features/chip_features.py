"""
features/chip_features.py - Chip/institutional flow feature computation.

Computes foreign investor, investment trust, dealer, and retail flow features.
"""

import logging

logger = logging.getLogger(__name__)


class ChipFeatures:
    """Computes chip/institutional flow features."""

    def compute_chip_features(self, symbol, chip_data=None):
        """
        Compute chip features for a given symbol.

        Parameters
        ----------
        symbol : str
            Stock symbol.
        chip_data : dict or None
            Dict with optional institutional/chip flow data.

        Returns
        -------
        dict with all chip feature keys and scores.
        """
        neutral = {
            'foreign_3d_net_buy': 0.0,
            'foreign_5d_net_buy': 0.0,
            'investment_trust_3d_net_buy': 0.0,
            'investment_trust_5d_net_buy': 0.0,
            'dealer_3d_net_buy': 0.0,
            'dealer_5d_net_buy': 0.0,
            'major_holder_ratio_change': 0.0,
            'retail_holder_ratio_change': 0.0,
            'margin_balance_change': 0.0,
            'short_balance_change': 0.0,
            'investment_trust_avg_cost_3d': None,
            'investment_trust_avg_cost_5d': None,
            'price_vs_trust_cost_pct': 0.0,
            'chip_score': 5.0,
            'institution_score': 5.0,
            'retail_risk_score': 5.0,
            'margin_risk_score': 5.0,
            'trust_cost_support_score': 5.0,
            'data_missing': True,
            'data_completeness': 0.0,
            'warning': f'No chip data available for {symbol}. Using neutral score.',
        }

        if chip_data is None or not chip_data:
            return neutral

        try:
            d = chip_data
            fields_defined = [
                'foreign_3d_net_buy', 'foreign_5d_net_buy',
                'investment_trust_3d_net_buy', 'investment_trust_5d_net_buy',
                'dealer_3d_net_buy', 'dealer_5d_net_buy',
                'major_holder_ratio_change', 'retail_holder_ratio_change',
                'margin_balance_change', 'short_balance_change',
            ]

            fields_present = sum(1 for f in fields_defined if d.get(f) is not None)
            data_completeness = (fields_present / len(fields_defined)) * 100.0

            if fields_present == 0:
                return neutral

            # Extract values with defaults
            foreign_3d = float(d.get('foreign_3d_net_buy', 0) or 0)
            foreign_5d = float(d.get('foreign_5d_net_buy', 0) or 0)
            trust_3d = float(d.get('investment_trust_3d_net_buy', 0) or 0)
            trust_5d = float(d.get('investment_trust_5d_net_buy', 0) or 0)
            dealer_3d = float(d.get('dealer_3d_net_buy', 0) or 0)
            dealer_5d = float(d.get('dealer_5d_net_buy', 0) or 0)
            major_ratio_chg = float(d.get('major_holder_ratio_change', 0) or 0)
            retail_ratio_chg = float(d.get('retail_holder_ratio_change', 0) or 0)
            margin_chg = float(d.get('margin_balance_change', 0) or 0)
            short_chg = float(d.get('short_balance_change', 0) or 0)
            trust_cost_3d = d.get('investment_trust_avg_cost_3d')
            trust_cost_5d = d.get('investment_trust_avg_cost_5d')
            current_price = d.get('current_price')

            # Price vs trust cost
            price_vs_trust_cost = 0.0
            if trust_cost_5d and current_price:
                try:
                    price_vs_trust_cost = (float(current_price) - float(trust_cost_5d)) / float(trust_cost_5d) * 100.0
                except Exception:
                    pass

            # Institution score (0-15)
            inst_score = 5.0
            # Foreign flow
            if foreign_3d > 0:
                inst_score += min(foreign_3d / 1000.0, 3.0)
            elif foreign_3d < 0:
                inst_score -= min(abs(foreign_3d) / 1000.0, 3.0)
            # Trust flow
            if trust_3d > 0:
                inst_score += min(trust_3d / 500.0, 2.0)
            elif trust_3d < 0:
                inst_score -= min(abs(trust_3d) / 500.0, 2.0)
            # Dealer flow
            if dealer_3d > 0:
                inst_score += min(dealer_3d / 200.0, 1.0)
            inst_score = min(max(inst_score, 0.0), 15.0)

            # Retail risk score (lower = better, 0 = no risk, 10 = high risk)
            retail_risk = 5.0
            if retail_ratio_chg > 2:
                retail_risk += 2.0  # retail piling in, risk up
            elif retail_ratio_chg < -2:
                retail_risk -= 2.0  # retail exiting, risk down
            if major_ratio_chg > 1:
                retail_risk -= 2.0  # majors buying, lower risk
            elif major_ratio_chg < -1:
                retail_risk += 2.0
            retail_risk = min(max(retail_risk, 0.0), 10.0)

            # Margin risk score (0=low risk, 10=high risk)
            margin_risk = 5.0
            if margin_chg > 5:
                margin_risk += 3.0
            elif margin_chg > 2:
                margin_risk += 1.5
            elif margin_chg < -3:
                margin_risk -= 2.0
            margin_risk = min(max(margin_risk, 0.0), 10.0)

            # Trust cost support score (0-10)
            trust_cost_support = 5.0
            if price_vs_trust_cost > 5:
                trust_cost_support = 3.0  # price well above cost, less support
            elif -2 <= price_vs_trust_cost <= 5:
                trust_cost_support = 8.0  # price near or slightly above cost, good support
            elif price_vs_trust_cost < -2:
                trust_cost_support = 2.0  # price below cost, trust may sell

            # Overall chip score (0-15): blend inst, retail, margin
            chip_score = (
                inst_score * 0.5
                + (10.0 - retail_risk) * 0.3
                + (10.0 - margin_risk) * 0.2
            )
            chip_score = min(max(chip_score, 0.0), 15.0)

            warning = None
            if data_completeness < 50:
                warning = f'Partial chip data for {symbol} ({data_completeness:.0f}% complete). Score may be inaccurate.'

            return {
                'foreign_3d_net_buy': foreign_3d,
                'foreign_5d_net_buy': foreign_5d,
                'investment_trust_3d_net_buy': trust_3d,
                'investment_trust_5d_net_buy': trust_5d,
                'dealer_3d_net_buy': dealer_3d,
                'dealer_5d_net_buy': dealer_5d,
                'major_holder_ratio_change': major_ratio_chg,
                'retail_holder_ratio_change': retail_ratio_chg,
                'margin_balance_change': margin_chg,
                'short_balance_change': short_chg,
                'investment_trust_avg_cost_3d': trust_cost_3d,
                'investment_trust_avg_cost_5d': trust_cost_5d,
                'price_vs_trust_cost_pct': round(price_vs_trust_cost, 2),
                'chip_score': round(chip_score, 2),
                'institution_score': round(inst_score, 2),
                'retail_risk_score': round(retail_risk, 2),
                'margin_risk_score': round(margin_risk, 2),
                'trust_cost_support_score': round(trust_cost_support, 2),
                'data_missing': False,
                'data_completeness': round(data_completeness, 1),
                'warning': warning,
            }

        except Exception as exc:
            logger.warning("Error computing chip features for %s: %s", symbol, exc)
            neutral['warning'] = f'Error computing chip features: {exc}'
            return neutral
