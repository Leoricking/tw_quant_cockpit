"""
dataset/dataset_builder.py - Full labeled dataset builder for ML training.

Builds a DataFrame with features + labels for all symbols and date range.
Works with mock data when no real data is available.
"""

import os
import random
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

_SEED_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0,
}


class DatasetBuilder:
    """
    Builds complete labeled datasets for ML model training.

    Each row represents a single symbol on a single date with:
    - Technical features
    - Chip features
    - Fundamental features
    - Orderbook features
    - Daytrade and swing trade labels
    - Forward return metrics
    """

    def build(self, symbols, start_date, end_date, price_data=None):
        """
        Build a labeled dataset for all symbols in the date range.

        Parameters
        ----------
        symbols : list of str
        start_date : str ('YYYY-MM-DD')
        end_date : str ('YYYY-MM-DD')
        price_data : dict, optional
            Mapping symbol -> list of OHLCV dicts. If None, uses mock data.

        Returns
        -------
        pandas.DataFrame with all features and labels.
        """
        try:
            import pandas as pd
        except ImportError:
            logger.error("pandas not available. Cannot build dataset.")
            return None

        rows = []
        use_mock = price_data is None

        for sym in symbols:
            sym_str = str(sym)
            if use_mock:
                pdata = self._generate_mock_prices(sym_str, start_date, end_date)
            else:
                pdata = price_data.get(sym_str, [])

            if not pdata:
                continue

            closes = []
            dates = []
            for p in pdata:
                if isinstance(p, dict):
                    c = p.get('close', p.get('Close'))
                    d = p.get('date', p.get('Date', ''))
                else:
                    c = float(p)
                    d = ''
                if c is not None:
                    closes.append(float(c))
                    dates.append(str(d))

            if len(closes) < 25:
                continue

            from dataset.labeler import Labeler
            labeler = Labeler()
            daytrade_labels = labeler.label_daytrade(closes)
            swing_labels = labeler.label_swing(closes)

            from dataset.feature_snapshot_builder import FeatureSnapshotBuilder
            builder = FeatureSnapshotBuilder()

            for i in range(20, len(closes)):
                dt = dates[i] if i < len(dates) else f'T{i}'
                feats = builder.build_snapshot(
                    sym_str, dt,
                    price_data=pdata[:i+1],
                )

                # Future returns
                future_15m = 0.0
                future_5d = 0.0
                future_max_dd = 0.0

                if i + 1 < len(closes):
                    future_15m = (closes[i+1] - closes[i]) / closes[i]
                if i + 5 < len(closes):
                    future_5d = (closes[i+5] - closes[i]) / closes[i]
                if i + 5 < len(closes):
                    window = closes[i:i+6]
                    peak = max(window)
                    future_max_dd = max((peak - min(window[j:]) ) / peak
                                       for j in range(len(window)) if peak > 0)

                label_dt = daytrade_labels[i] if i < len(daytrade_labels) else 0
                label_sw = swing_labels[i] if i < len(swing_labels) else 0

                row = dict(feats)
                row.update({
                    'label_daytrade': label_dt,
                    'label_swing': label_sw,
                    'future_return_15m': round(future_15m, 4),
                    'future_return_5d': round(future_5d, 4),
                    'future_max_drawdown': round(future_max_dd, 4),
                    'sim_trade_result': label_sw,
                })
                rows.append(row)

        if not rows:
            logger.warning("DatasetBuilder: no rows generated.")
            return pd.DataFrame()

        df = pd.DataFrame(rows)
        logger.info("DatasetBuilder: built %d rows for %d symbols.", len(df), len(symbols))
        return df

    def save(self, df, output_path):
        """
        Save dataset to parquet format.

        Parameters
        ----------
        df : pandas.DataFrame
        output_path : str
        """
        try:
            import pandas as pd
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_parquet(output_path, index=False)
            logger.info("Dataset saved to %s (%d rows).", output_path, len(df))
        except ImportError:
            logger.error("pyarrow not available. Cannot save to parquet.")
        except Exception as exc:
            logger.error("Failed to save dataset: %s", exc)

    def _generate_mock_prices(self, symbol, start_date, end_date):
        """Generate a mock price series between dates."""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        except Exception:
            start = datetime(2024, 1, 1)
            end = datetime(2024, 12, 31)

        base = _SEED_PRICES.get(symbol, 100.0)
        rng = random.Random(hash(symbol) % 77777)

        prices = []
        price = base * rng.uniform(0.75, 0.95)
        current = start

        while current <= end:
            if current.weekday() < 5:  # Skip weekends
                change = rng.gauss(0.001, 0.015)
                price = max(price * (1 + change), 1.0)
                vol = rng.randint(500, 50000) * 1000
                prices.append({
                    'date': current.strftime('%Y-%m-%d'),
                    'close': round(price, 1),
                    'high': round(price * rng.uniform(1.001, 1.025), 1),
                    'low': round(price * rng.uniform(0.975, 0.999), 1),
                    'open': round(price * rng.uniform(0.99, 1.01), 1),
                    'volume': vol,
                })
            current += timedelta(days=1)

        return prices
