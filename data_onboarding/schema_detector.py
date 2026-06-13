"""
data_onboarding/schema_detector.py — ColumnMappingDetector for TW Quant Cockpit v1.1.1.

Maps raw column names to standard schema columns.
Uses same mapping tables as XQExportImporter but as a standalone detector.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

# ---------------------------------------------------------------------------
# Required columns per dataset
# ---------------------------------------------------------------------------
_REQUIRED_COLS = {
    'daily':         {'date', 'open', 'high', 'low', 'close', 'volume'},
    'margin':        {'date', 'margin_balance', 'short_balance'},
    'institutional': {'date', 'trust_net_buy', 'foreign_net_buy', 'dealer_net_buy'},
    'trust_cost':    {'date', 'trust_buy_shares', 'trust_avg_cost'},
    'holder':        {'date'},
}


class ColumnMappingDetector:
    """
    Maps raw column names to standard schema columns.
    Uses same mapping tables as XQExportImporter but as a standalone detector.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    # Date column candidates
    DATE_COLS = ['時間', 'date', 'Date', '日期', 'datetime', 'DateTime', 'DATE']

    # Daily OHLCV
    DAILY_MAP = {
        '開盤價': 'open', '開盤': 'open', 'open': 'open', 'Open': 'open',
        '最高價': 'high', '最高': 'high', 'high': 'high', 'High': 'high',
        '最低價': 'low',  '最低': 'low',  'low': 'low',   'Low': 'low',
        '收盤價': 'close', '收盤': 'close', 'close': 'close', 'Close': 'close',
        '成交量': 'volume', '成交量(張)': 'volume', '成交股數': 'volume',
        '成交量(股)': 'volume', 'volume': 'volume', 'Volume': 'volume',
    }

    # Margin / short
    MARGIN_MAP = {
        '融資(張)': 'margin_balance', '融資餘額': 'margin_balance',
        '融資': 'margin_balance', 'margin_balance': 'margin_balance',
        '融券(張)': 'short_balance', '融券餘額': 'short_balance',
        '融券': 'short_balance', 'short_balance': 'short_balance',
        '融資差額': 'margin_change', '融資增減': 'margin_change',
        '融券差額': 'short_change',  '融券增減': 'short_change',
    }

    # Institutional net buy
    INST_MAP = {
        '投信買賣超(張)': 'trust_net_buy',   '投信買賣超': 'trust_net_buy',
        'trust_net_buy': 'trust_net_buy',
        '外資買賣超(張)': 'foreign_net_buy', '外資買賣超': 'foreign_net_buy',
        'foreign_net_buy': 'foreign_net_buy',
        '自營商買賣超(張)': 'dealer_net_buy', '自營商買賣超': 'dealer_net_buy',
        'dealer_net_buy': 'dealer_net_buy',
    }

    # Trust cost
    TRUST_MAP = {
        '投信買超張數': 'trust_buy_shares', '投信買超': 'trust_buy_shares',
        'trust_buy_shares': 'trust_buy_shares',
        '投信買進金額': 'trust_buy_amount',  '投信金額': 'trust_buy_amount',
        'trust_buy_amount': 'trust_buy_amount',
        '投信成本線': 'trust_avg_cost', '投信平均成本': 'trust_avg_cost',
        '投信成本': 'trust_avg_cost', 'trust_avg_cost': 'trust_avg_cost',
    }

    def detect(self, columns: List[str]) -> dict:
        """
        Returns:
        {
            'mapped': {'原始欄位': 'standard_col'},
            'unmapped': ['col1', 'col2'],
            'datasets': ['daily', 'margin', ...],
            'confidence': 0.85,
            'has_date': True,
            'missing_required': [],
        }
        """
        if not columns:
            return {
                "mapped": {}, "unmapped": [], "datasets": [],
                "confidence": 0.0, "has_date": False, "missing_required": [],
            }

        mapped: dict = {}
        unmapped: List[str] = []
        has_date = False

        # Check for date column
        for col in columns:
            if col in self.DATE_COLS:
                mapped[col] = 'date'
                has_date = True
                break

        # Build combined map
        combined_map = {}
        combined_map.update(self.DAILY_MAP)
        combined_map.update(self.MARGIN_MAP)
        combined_map.update(self.INST_MAP)
        combined_map.update(self.TRUST_MAP)

        for col in columns:
            if col in self.DATE_COLS:
                continue  # already handled
            if col in combined_map:
                mapped[col] = combined_map[col]
            else:
                unmapped.append(col)

        # Detect datasets
        std_vals = set(mapped.values())
        datasets = []
        daily_cols = {'open', 'high', 'low', 'close', 'volume'}
        margin_cols = {'margin_balance', 'short_balance'}
        inst_cols = {'trust_net_buy', 'foreign_net_buy', 'dealer_net_buy'}
        trust_cols = {'trust_buy_shares', 'trust_avg_cost'}

        if std_vals & daily_cols:
            datasets.append('daily')
        if std_vals & margin_cols:
            datasets.append('margin')
        if std_vals & inst_cols:
            datasets.append('institutional')
        if std_vals & trust_cols:
            datasets.append('trust_cost')

        # Confidence
        total = len(columns)
        n_mapped = len(mapped)
        confidence = (n_mapped / total) if total > 0 else 0.0

        # Missing required for primary dataset
        missing_required: List[str] = []
        if datasets:
            primary_ds = datasets[0]
            missing_required = self.validate_required_cols(mapped, primary_ds)

        return {
            "mapped":            mapped,
            "unmapped":          unmapped,
            "datasets":          datasets,
            "confidence":        round(confidence, 3),
            "has_date":          has_date,
            "missing_required":  missing_required,
        }

    def map_columns(self, df, mapping: dict):
        """Apply column mapping to dataframe."""
        if not _PANDAS_AVAILABLE:
            return df
        rename_map = {k: v for k, v in mapping.items() if k in df.columns}
        return df.rename(columns=rename_map)

    def validate_required_cols(self, mapped_cols: dict, dataset: str) -> List[str]:
        """Return list of missing required columns for the given dataset."""
        required = _REQUIRED_COLS.get(dataset, set())
        present = set(mapped_cols.values())
        missing = [c for c in required if c not in present]
        return missing
