"""
dataset/feature_snapshot_builder.py - Point-in-time feature snapshot builder.

Builds a complete feature dict for a single symbol at a specific datetime.
"""

import logging

logger = logging.getLogger(__name__)


class FeatureSnapshotBuilder:
    """
    Builds complete feature snapshots for ML training and inference.

    Combines technical, chip, fundamental, and orderbook features
    into a single flat feature dict for a given symbol and datetime.
    """

    def build_snapshot(self, symbol, datetime_pt, price_data=None,
                       chip_data=None, fundamental_data=None, bidask_data=None):
        """
        Build a feature snapshot for a single point in time.

        Parameters
        ----------
        symbol : str
        datetime_pt : str or datetime
            The point in time for this snapshot.
        price_data : list, optional
            Historical price series up to datetime_pt.
        chip_data : dict, optional
        fundamental_data : dict, optional
        bidask_data : dict, optional
            5-level bid/ask snapshot.

        Returns
        -------
        dict with all available features, None for missing ones.
            Includes: data_completeness (0-100), symbol, datetime
        """
        sym = str(symbol)
        features = {
            'symbol': sym,
            'datetime': str(datetime_pt),
            'data_completeness': 0.0,
        }

        total_feature_groups = 4
        complete_groups = 0

        # Technical features
        tech_feats = self._compute_technical(price_data)
        features.update(tech_feats)
        if not tech_feats.get('tech_data_missing', True):
            complete_groups += 1

        # Chip features
        from features.chip_features import ChipFeatures
        chip_feat = ChipFeatures().compute_chip_features(sym, chip_data)
        chip_subset = {
            'foreign_3d_net_buy': chip_feat.get('foreign_3d_net_buy'),
            'investment_trust_3d_net_buy': chip_feat.get('investment_trust_3d_net_buy'),
            'chip_score': chip_feat.get('chip_score'),
            'margin_risk_score': chip_feat.get('margin_risk_score'),
        }
        features.update(chip_subset)
        if not chip_feat.get('data_missing', True):
            complete_groups += 1

        # Fundamental features
        from features.fundamental_features import FundamentalFeatures
        fund_feat = FundamentalFeatures().compute_fundamental_features(sym, fundamental_data)
        fund_subset = {
            'latest_month_revenue_yoy': fund_feat.get('latest_month_revenue_yoy'),
            'eps_yoy': fund_feat.get('eps_yoy'),
            'fundamental_score': fund_feat.get('fundamental_score'),
        }
        features.update(fund_subset)
        if not fund_feat.get('data_missing', True):
            complete_groups += 1

        # Orderbook features
        from features.orderbook_features import OrderbookFeatures
        ob_feat = OrderbookFeatures().compute_orderbook_features(bidask_data)
        ob_subset = {
            'orderbook_imbalance': ob_feat.get('orderbook_imbalance'),
            'orderbook_state': ob_feat.get('orderbook_state'),
            'bid_sum_5': ob_feat.get('bid_sum_5'),
            'ask_sum_5': ob_feat.get('ask_sum_5'),
        }
        features.update(ob_subset)
        if not ob_feat.get('data_missing', True):
            complete_groups += 1

        features['data_completeness'] = round((complete_groups / total_feature_groups) * 100.0, 1)
        return features

    def _compute_technical(self, price_data):
        """Compute basic technical features from price data."""
        feats = {'tech_data_missing': True}

        if not price_data or len(price_data) < 5:
            feats.update({
                'close': None, 'volume': None,
                'ma5': None, 'ma10': None, 'ma20': None,
                'ret_1d': None, 'ret_5d': None, 'ret_20d': None,
                'rsi_14': None, 'vol_ratio': None,
            })
            return feats

        try:
            closes = []
            volumes = []
            for p in price_data:
                if isinstance(p, dict):
                    c = p.get('close', p.get('Close'))
                    v = p.get('volume', p.get('Volume', 0))
                else:
                    c = float(p)
                    v = 0
                if c is not None:
                    closes.append(float(c))
                    volumes.append(float(v or 0))

            if len(closes) < 5:
                return feats

            c = closes[-1]
            ma5 = sum(closes[-5:]) / 5
            ma10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else None
            ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
            ret_1d = (closes[-1] - closes[-2]) / closes[-2] if len(closes) >= 2 else None
            ret_5d = (closes[-1] - closes[-6]) / closes[-6] if len(closes) >= 6 else None
            ret_20d = (closes[-1] - closes[-21]) / closes[-21] if len(closes) >= 21 else None

            # RSI
            rsi_14 = None
            if len(closes) >= 14:
                gains = [max(closes[i] - closes[i-1], 0) for i in range(-14, 0)]
                losses = [max(closes[i-1] - closes[i], 0) for i in range(-14, 0)]
                avg_g = sum(gains) / 14
                avg_l = sum(losses) / 14
                if avg_l > 0:
                    rsi_14 = 100 - (100 / (1 + avg_g / avg_l))

            # Volume ratio
            vol_ratio = None
            if len(volumes) >= 20 and sum(volumes[-20:]) > 0:
                avg_vol = sum(volumes[-20:]) / 20
                vol_ratio = volumes[-1] / avg_vol if avg_vol > 0 else None

            feats.update({
                'close': round(c, 2),
                'volume': volumes[-1] if volumes else None,
                'ma5': round(ma5, 2),
                'ma10': round(ma10, 2) if ma10 else None,
                'ma20': round(ma20, 2) if ma20 else None,
                'ret_1d': round(ret_1d, 4) if ret_1d is not None else None,
                'ret_5d': round(ret_5d, 4) if ret_5d is not None else None,
                'ret_20d': round(ret_20d, 4) if ret_20d is not None else None,
                'rsi_14': round(rsi_14, 2) if rsi_14 is not None else None,
                'vol_ratio': round(vol_ratio, 2) if vol_ratio is not None else None,
                'tech_data_missing': False,
            })

        except Exception as exc:
            logger.warning("FeatureSnapshotBuilder technical compute error: %s", exc)

        return feats
