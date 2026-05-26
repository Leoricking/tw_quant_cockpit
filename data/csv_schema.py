"""
data/csv_schema.py - CSV schema definitions for TW Quant Cockpit imports.

Defines supported data types, required columns, Chinese column aliases,
standard output paths, and helper functions for normalization.
"""

SUPPORTED_DATA_TYPES = [
    'profile', 'daily', 'institutional', 'margin',
    'monthly_revenue', 'holder', 'trust_cost',
]

REQUIRED_COLUMNS = {
    'profile': ['symbol', 'name', 'market', 'industry', 'theme_tags', 'is_mainstream_theme', 'sector'],
    'daily': ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume'],
    'institutional': ['date', 'symbol', 'foreign_net_buy', 'trust_net_buy', 'dealer_net_buy'],
    'margin': ['date', 'symbol', 'margin_balance', 'margin_change', 'short_balance', 'short_change'],
    'monthly_revenue': ['month', 'symbol', 'revenue', 'mom', 'yoy', 'accumulated_yoy'],
    'holder': ['date', 'symbol', 'major_holder_ratio', 'retail_holder_ratio', 'major_change', 'retail_change'],
    'trust_cost': ['date', 'symbol', 'trust_buy_shares', 'trust_buy_amount', 'trust_avg_cost', 'close', 'price_vs_trust_cost_pct'],
}

COLUMN_ALIASES = {
    'profile': {
        '股票代號': 'symbol', '代號': 'symbol', '證券代號': 'symbol',
        '股票名稱': 'name', '名稱': 'name',
        '市場': 'market',
        '產業': 'industry', '產業別': 'industry',
        '題材': 'theme_tags', '題材標籤': 'theme_tags',
        '主流題材': 'is_mainstream_theme',
        '類股': 'sector',
    },
    'daily': {
        '日期': 'date',
        '股票代號': 'symbol', '代號': 'symbol',
        '開盤價': 'open', '開盤': 'open',
        '最高價': 'high', '最高': 'high',
        '最低價': 'low', '最低': 'low',
        '收盤價': 'close', '收盤': 'close',
        '成交量': 'volume', '成交股數': 'volume',
    },
    'institutional': {
        '日期': 'date',
        '股票代號': 'symbol', '代號': 'symbol',
        '外資買賣超': 'foreign_net_buy', '外資': 'foreign_net_buy',
        '投信買賣超': 'trust_net_buy', '投信': 'trust_net_buy',
        '自營商買賣超': 'dealer_net_buy', '自營商': 'dealer_net_buy',
    },
    'margin': {
        '日期': 'date',
        '股票代號': 'symbol', '代號': 'symbol',
        '融資餘額': 'margin_balance',
        '融資增減': 'margin_change',
        '融券餘額': 'short_balance',
        '融券增減': 'short_change',
    },
    'monthly_revenue': {
        '年月': 'month', '月份': 'month',
        '股票代號': 'symbol', '代號': 'symbol',
        '營收': 'revenue', '月營收': 'revenue',
        '月增率': 'mom', 'MoM': 'mom',
        '年增率': 'yoy', 'YoY': 'yoy',
        '累計年增率': 'accumulated_yoy', '累計YoY': 'accumulated_yoy',
    },
    'holder': {
        '日期': 'date',
        '股票代號': 'symbol', '代號': 'symbol',
        '大戶持股比率': 'major_holder_ratio', '大戶比率': 'major_holder_ratio',
        '散戶持股比率': 'retail_holder_ratio', '散戶比率': 'retail_holder_ratio',
        '大戶增減': 'major_change',
        '散戶增減': 'retail_change',
    },
    'trust_cost': {
        '日期': 'date',
        '股票代號': 'symbol', '代號': 'symbol',
        '投信買超張數': 'trust_buy_shares', '投信買超': 'trust_buy_shares',
        '投信買進金額': 'trust_buy_amount', '投信金額': 'trust_buy_amount',
        '投信平均成本': 'trust_avg_cost', '投信成本': 'trust_avg_cost',
        '收盤價': 'close', '收盤': 'close',
        '股價距投信成本%': 'price_vs_trust_cost_pct', '距投信成本%': 'price_vs_trust_cost_pct',
    },
}

OUTPUT_PATHS = {
    'profile':         'data/import/profile/stock_profile.csv',
    'daily':           'data/import/daily/daily_k.csv',
    'institutional':   'data/import/institutional/institutional.csv',
    'margin':          'data/import/margin/margin.csv',
    'monthly_revenue': 'data/import/monthly_revenue/monthly_revenue.csv',
    'holder':          'data/import/holder/holder.csv',
    'trust_cost':      'data/import/trust_cost/trust_cost.csv',
}

SAMPLE_PATHS = {
    'profile':         'data/import/profile/stock_profile_sample.csv',
    'daily':           'data/import/daily/daily_k_sample.csv',
    'institutional':   'data/import/institutional/institutional_sample.csv',
    'margin':          'data/import/margin/margin_sample.csv',
    'monthly_revenue': 'data/import/monthly_revenue/monthly_revenue_sample.csv',
    'holder':          'data/import/holder/holder_sample.csv',
    'trust_cost':      'data/import/trust_cost/trust_cost_sample.csv',
}

DATE_COLUMNS = {
    'daily':           ['date'],
    'institutional':   ['date'],
    'margin':          ['date'],
    'monthly_revenue': ['month'],
    'holder':          ['date'],
    'trust_cost':      ['date'],
}

NUMERIC_COLUMNS = {
    'profile':         [],
    'daily':           ['open', 'high', 'low', 'close', 'volume'],
    'institutional':   ['foreign_net_buy', 'trust_net_buy', 'dealer_net_buy'],
    'margin':          ['margin_balance', 'margin_change', 'short_balance', 'short_change'],
    'monthly_revenue': ['revenue', 'mom', 'yoy', 'accumulated_yoy'],
    'holder':          ['major_holder_ratio', 'retail_holder_ratio', 'major_change', 'retail_change'],
    'trust_cost':      ['trust_buy_shares', 'trust_buy_amount', 'trust_avg_cost', 'close', 'price_vs_trust_cost_pct'],
}

# Keys used to deduplicate after merge
DEDUP_KEYS = {
    'profile':         ['symbol'],
    'daily':           ['symbol', 'date'],
    'institutional':   ['symbol', 'date'],
    'margin':          ['symbol', 'date'],
    'monthly_revenue': ['symbol', 'month'],
    'holder':          ['symbol', 'date'],
    'trust_cost':      ['symbol', 'date'],
}


def get_schema(data_type: str) -> dict:
    """Return the full schema dict for a data_type."""
    if data_type not in SUPPORTED_DATA_TYPES:
        raise ValueError(
            f"Unsupported data_type: {data_type!r}. Choose from: {SUPPORTED_DATA_TYPES}"
        )
    return {
        'data_type':       data_type,
        'required_columns': REQUIRED_COLUMNS[data_type],
        'column_aliases':  COLUMN_ALIASES.get(data_type, {}),
        'output_path':     OUTPUT_PATHS[data_type],
        'sample_path':     SAMPLE_PATHS[data_type],
        'date_columns':    DATE_COLUMNS.get(data_type, []),
        'numeric_columns': NUMERIC_COLUMNS.get(data_type, []),
        'dedup_keys':      DEDUP_KEYS[data_type],
    }


def normalize_column_name(data_type: str, column: str) -> str:
    """
    Translate a raw (possibly Chinese) column name to the standard English name.

    Returns the standard name if an alias exists, else returns the original.
    """
    aliases = COLUMN_ALIASES.get(data_type, {})
    return aliases.get(column, column)
