"""
data/universe_manifest.py - Universe manifest builder for TW Quant Cockpit.

Manages the 10 / 30 / 50 stock expansion universe.
Builds and updates data/universe/universe_manifest.csv.

Usage:
    from data.universe_manifest import UniverseManifest
    um = UniverseManifest()
    um.build(size=10)
    um.build(size=30, replace=False)
    df = um.load()
    um.update_import_status('2454', import_status='imported', daily_rows=250)
"""

import csv
import logging
import os
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_UNIVERSE_DIR  = os.path.join(_BASE_DIR, 'data', 'universe')
_MANIFEST_PATH = os.path.join(_UNIVERSE_DIR, 'universe_manifest.csv')
_SAMPLE_PATH   = os.path.join(_UNIVERSE_DIR, 'universe_manifest_sample.csv')

# ---------------------------------------------------------------------------
# Stock lists (curated Taiwan equities)
# ---------------------------------------------------------------------------

_UNIVERSE_10 = [
    {'symbol': '2454', 'name': '聯發科',   'sector': '半導體',      'theme_tags': 'IC設計,AI,5G',      'priority': 1},
    {'symbol': '2383', 'name': '台光電',   'sector': '電子零組件',   'theme_tags': 'PCB,AI伺服器',      'priority': 2},
    {'symbol': '6669', 'name': '緯穎',     'sector': '電腦及周邊',   'theme_tags': 'AI伺服器,雲端',     'priority': 3},
    {'symbol': '2345', 'name': '智邦',     'sector': '網路通訊',     'theme_tags': 'AI交換器,雲端',     'priority': 4},
    {'symbol': '2330', 'name': '台積電',   'sector': '半導體',       'theme_tags': '晶圓代工,AI,龍頭',  'priority': 5},
    {'symbol': '2308', 'name': '台達電',   'sector': '電子零組件',   'theme_tags': '電源,散熱,AI伺服器','priority': 6},
    {'symbol': '2317', 'name': '鴻海',     'sector': '電子製造服務', 'theme_tags': 'EMS,iPhone,電動車', 'priority': 7},
    {'symbol': '2382', 'name': '廣達',     'sector': '電腦及周邊',   'theme_tags': 'AI伺服器,雲端',     'priority': 8},
    {'symbol': '3017', 'name': '奇鋐',     'sector': '電子零組件',   'theme_tags': '散熱,AI伺服器',     'priority': 9},
    {'symbol': '3661', 'name': '世芯-KY',  'sector': '半導體',       'theme_tags': 'ASIC,AI加速器',     'priority': 10},
]

_UNIVERSE_30_EXTRA = [
    {'symbol': '2303', 'name': '聯電',     'sector': '半導體',       'theme_tags': '晶圓代工,成熟製程', 'priority': 11},
    {'symbol': '2412', 'name': '中華電',   'sector': '電信',         'theme_tags': '電信龍頭,穩定股息', 'priority': 12},
    {'symbol': '3008', 'name': '大立光',   'sector': '光學',         'theme_tags': '鏡頭,iPhone',       'priority': 13},
    {'symbol': '2357', 'name': '華碩',     'sector': '電腦及周邊',   'theme_tags': 'NB,PC,AI PC',       'priority': 14},
    {'symbol': '2379', 'name': '瑞昱',     'sector': '半導體',       'theme_tags': 'IC設計,網通晶片',   'priority': 15},
    {'symbol': '2395', 'name': '研華',     'sector': '電腦及周邊',   'theme_tags': '工業電腦,AIoT',     'priority': 16},
    {'symbol': '4938', 'name': '和碩',     'sector': '電子製造服務', 'theme_tags': 'EMS,iPhone',        'priority': 17},
    {'symbol': '3711', 'name': '日月光投控','sector': '半導體封測',   'theme_tags': '封測龍頭,先進封裝', 'priority': 18},
    {'symbol': '3037', 'name': '欣興',     'sector': '電子零組件',   'theme_tags': 'ABF載板,AI伺服器',  'priority': 19},
    {'symbol': '6505', 'name': '台塑化',   'sector': '石化',         'theme_tags': '石化,台塑集團',     'priority': 20},
    {'symbol': '1301', 'name': '台塑',     'sector': '塑化',         'theme_tags': '石化,台塑集團',     'priority': 21},
    {'symbol': '1303', 'name': '南亞',     'sector': '塑化',         'theme_tags': '石化,銅箔基板',     'priority': 22},
    {'symbol': '2207', 'name': '和泰車',   'sector': '汽車',         'theme_tags': 'Toyota,汽車',       'priority': 23},
    {'symbol': '8046', 'name': '南電',     'sector': '電子零組件',   'theme_tags': 'ABF載板,AI伺服器',  'priority': 24},
    {'symbol': '3034', 'name': '聯詠',     'sector': '半導體',       'theme_tags': 'IC設計,顯示驅動',   'priority': 25},
    {'symbol': '6415', 'name': '矽力-KY',  'sector': '半導體',       'theme_tags': 'IC設計,電源管理',   'priority': 26},
    {'symbol': '3045', 'name': '台灣大',   'sector': '電信',         'theme_tags': '電信,行動支付',     'priority': 27},
    {'symbol': '2615', 'name': '萬海',     'sector': '航運',         'theme_tags': '貨運,航運',         'priority': 28},
    {'symbol': '5876', 'name': '上海商銀', 'sector': '銀行',         'theme_tags': '銀行,穩定股息',     'priority': 29},
    {'symbol': '2409', 'name': '友達',     'sector': '面板',         'theme_tags': '面板,顯示器',       'priority': 30},
]

_UNIVERSE_50_EXTRA = [
    {'symbol': '2603', 'name': '長榮',     'sector': '航運',         'theme_tags': '貨運,航運',         'priority': 31},
    {'symbol': '2882', 'name': '國泰金',   'sector': '金融',         'theme_tags': '壽險,金控',         'priority': 32},
    {'symbol': '2886', 'name': '兆豐金',   'sector': '金融',         'theme_tags': '銀行,金控',         'priority': 33},
    {'symbol': '2891', 'name': '中信金',   'sector': '金融',         'theme_tags': '銀行,金控',         'priority': 34},
    {'symbol': '2344', 'name': '華邦電',   'sector': '半導體',       'theme_tags': 'DRAM,記憶體',       'priority': 35},
    {'symbol': '2337', 'name': '旺宏',     'sector': '半導體',       'theme_tags': 'Flash,記憶體',      'priority': 36},
    {'symbol': '4904', 'name': '遠傳',     'sector': '電信',         'theme_tags': '電信,5G',           'priority': 37},
    {'symbol': '2408', 'name': '南亞科',   'sector': '半導體',       'theme_tags': 'DRAM,記憶體',       'priority': 38},
    {'symbol': '3231', 'name': '緯創',     'sector': '電腦及周邊',   'theme_tags': 'NB,伺服器',         'priority': 39},
    {'symbol': '2353', 'name': '宏碁',     'sector': '電腦及周邊',   'theme_tags': 'NB,PC',             'priority': 40},
    {'symbol': '2610', 'name': '華航',     'sector': '航空',         'theme_tags': '航空,旅遊',         'priority': 41},
    {'symbol': '2912', 'name': '統一超',   'sector': '零售',         'theme_tags': '便利商店,消費',     'priority': 42},
    {'symbol': '1402', 'name': '遠東新',   'sector': '紡織',         'theme_tags': '紡織,尼龍',         'priority': 43},
    {'symbol': '3533', 'name': '嘉澤',     'sector': '電子零組件',   'theme_tags': '連接器,AI伺服器',   'priority': 44},
    {'symbol': '6414', 'name': '樺漢',     'sector': '電腦及周邊',   'theme_tags': '工業電腦,嵌入式',   'priority': 45},
    {'symbol': '2456', 'name': '奇力新',   'sector': '電子零組件',   'theme_tags': '被動元件',          'priority': 46},
    {'symbol': '2105', 'name': '正新',     'sector': '橡膠',         'theme_tags': '輪胎,汽車零件',     'priority': 47},
    {'symbol': '6274', 'name': '台燿',     'sector': '電子零組件',   'theme_tags': 'CCL,銅箔基板',      'priority': 48},
    {'symbol': '3706', 'name': '神達',     'sector': '電腦及周邊',   'theme_tags': '車載,IoT',          'priority': 49},
    {'symbol': '2498', 'name': '宏達電',   'sector': '通訊網路',     'theme_tags': 'VR,元宇宙',         'priority': 50},
]

_UNIVERSE_10_SYMBOLS  = [r['symbol'] for r in _UNIVERSE_10]
_UNIVERSE_30_SYMBOLS  = _UNIVERSE_10_SYMBOLS + [r['symbol'] for r in _UNIVERSE_30_EXTRA]
_UNIVERSE_50_SYMBOLS  = _UNIVERSE_30_SYMBOLS + [r['symbol'] for r in _UNIVERSE_50_EXTRA]

_ALL_STOCKS = _UNIVERSE_10 + _UNIVERSE_30_EXTRA + _UNIVERSE_50_EXTRA

_MANIFEST_COLS = [
    'symbol', 'name', 'sector', 'theme_tags', 'priority',
    'xq_file', 'import_status',
    'daily_rows', 'margin_rows', 'institutional_rows',
    'holder_rows', 'trust_cost_rows', 'monthly_revenue_rows',
    'short_term_ready', 'mid_term_ready', 'long_term_ready',
    'last_checked', 'warning',
]


def get_universe_symbols(size: int) -> list:
    """Return symbol list for the requested universe size (10 / 30 / 50)."""
    if size <= 10:
        return list(_UNIVERSE_10_SYMBOLS)
    if size <= 30:
        return list(_UNIVERSE_30_SYMBOLS)
    return list(_UNIVERSE_50_SYMBOLS)


def get_universe_stocks(size: int) -> list:
    """Return stock metadata dicts for the requested universe size."""
    if size <= 10:
        return list(_UNIVERSE_10)
    if size <= 30:
        return _UNIVERSE_10 + _UNIVERSE_30_EXTRA
    return _ALL_STOCKS


class UniverseManifest:
    """
    Builds and manages the universe_manifest.csv.

    The manifest tracks import status and data completeness for each symbol
    in the 10 / 30 / 50 expansion universe.
    """

    def __init__(self, manifest_path: str = None):
        self.manifest_path = manifest_path or _MANIFEST_PATH

    # ------------------------------------------------------------------

    def build(self, size: int = 10, replace: bool = False) -> pd.DataFrame:
        """
        Build (or extend) the universe manifest CSV.

        Parameters
        ----------
        size    : 10, 30, or 50 — determines the stock list
        replace : True → overwrite existing entries; False → preserve existing data

        Returns
        -------
        pd.DataFrame with one row per symbol
        """
        os.makedirs(os.path.dirname(self.manifest_path), exist_ok=True)

        stocks  = get_universe_stocks(size)
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

        # Load existing manifest if present and not replacing
        existing: dict = {}
        if not replace and os.path.isfile(self.manifest_path):
            try:
                existing_df = pd.read_csv(self.manifest_path, dtype=str)
                for _, row in existing_df.iterrows():
                    sym = str(row.get('symbol', '')).strip()
                    if sym:
                        existing[sym] = row.to_dict()
                logger.info("Loaded %d existing manifest entries", len(existing))
            except Exception as exc:
                logger.warning("Could not read existing manifest: %s", exc)

        rows = []
        for stock in stocks:
            sym = stock['symbol']
            ex  = existing.get(sym, {})
            row = {
                'symbol':               sym,
                'name':                 stock.get('name', sym),
                'sector':               stock.get('sector', ''),
                'theme_tags':           stock.get('theme_tags', ''),
                'priority':             stock.get('priority', 99),
                'xq_file':              ex.get('xq_file', ''),
                'import_status':        ex.get('import_status', 'pending'),
                'daily_rows':           ex.get('daily_rows', 0),
                'margin_rows':          ex.get('margin_rows', 0),
                'institutional_rows':   ex.get('institutional_rows', 0),
                'holder_rows':          ex.get('holder_rows', 0),
                'trust_cost_rows':      ex.get('trust_cost_rows', 0),
                'monthly_revenue_rows': ex.get('monthly_revenue_rows', 0),
                'short_term_ready':     ex.get('short_term_ready', False),
                'mid_term_ready':       ex.get('mid_term_ready', False),
                'long_term_ready':      ex.get('long_term_ready', False),
                'last_checked':         ex.get('last_checked', ''),
                'warning':              ex.get('warning', ''),
            }
            rows.append(row)

        df = pd.DataFrame(rows, columns=_MANIFEST_COLS)
        df.to_csv(self.manifest_path, index=False, encoding='utf-8-sig')
        logger.info("Manifest saved (%d symbols, size=%d): %s", len(df), size, self.manifest_path)
        return df

    def load(self) -> pd.DataFrame:
        """Load the existing manifest CSV. Returns empty DataFrame if not found."""
        if not os.path.isfile(self.manifest_path):
            logger.warning("Manifest not found: %s", self.manifest_path)
            return pd.DataFrame(columns=_MANIFEST_COLS)
        try:
            return pd.read_csv(self.manifest_path, dtype=str)
        except Exception as exc:
            logger.warning("Cannot load manifest: %s", exc)
            return pd.DataFrame(columns=_MANIFEST_COLS)

    def update_import_status(
        self,
        symbol: str,
        import_status: str = 'imported',
        xq_file: str = None,
        daily_rows: int = None,
        margin_rows: int = None,
        institutional_rows: int = None,
        holder_rows: int = None,
        trust_cost_rows: int = None,
        monthly_revenue_rows: int = None,
        warning: str = None,
    ) -> None:
        """Update a symbol's row in the manifest after a successful import."""
        if not os.path.isfile(self.manifest_path):
            logger.warning("Manifest not found, cannot update %s", symbol)
            return
        try:
            df = pd.read_csv(self.manifest_path, dtype=str)
            mask = df['symbol'] == str(symbol)
            if not mask.any():
                logger.warning("Symbol %s not in manifest", symbol)
                return
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            df.loc[mask, 'import_status'] = import_status
            df.loc[mask, 'last_checked']  = now_str
            if xq_file              is not None: df.loc[mask, 'xq_file']              = xq_file
            if daily_rows           is not None: df.loc[mask, 'daily_rows']           = daily_rows
            if margin_rows          is not None: df.loc[mask, 'margin_rows']          = margin_rows
            if institutional_rows   is not None: df.loc[mask, 'institutional_rows']   = institutional_rows
            if holder_rows          is not None: df.loc[mask, 'holder_rows']          = holder_rows
            if trust_cost_rows      is not None: df.loc[mask, 'trust_cost_rows']      = trust_cost_rows
            if monthly_revenue_rows is not None: df.loc[mask, 'monthly_revenue_rows'] = monthly_revenue_rows
            if warning              is not None: df.loc[mask, 'warning']              = warning
            df.to_csv(self.manifest_path, index=False, encoding='utf-8-sig')
        except Exception as exc:
            logger.warning("update_import_status failed for %s: %s", symbol, exc)

    def build_sample(self) -> None:
        """Write the sample manifest (committed to git, no user data)."""
        os.makedirs(os.path.dirname(_SAMPLE_PATH), exist_ok=True)
        stocks = get_universe_stocks(10)
        rows = []
        for stock in stocks:
            rows.append({
                'symbol':               stock['symbol'],
                'name':                 stock['name'],
                'sector':               stock['sector'],
                'theme_tags':           stock['theme_tags'],
                'priority':             stock['priority'],
                'xq_file':              f"{stock['symbol']}.xlsx",
                'import_status':        'sample',
                'daily_rows':           0,
                'margin_rows':          0,
                'institutional_rows':   0,
                'holder_rows':          0,
                'trust_cost_rows':      0,
                'monthly_revenue_rows': 0,
                'short_term_ready':     False,
                'mid_term_ready':       False,
                'long_term_ready':      False,
                'last_checked':         '',
                'warning':              '',
            })
        df = pd.DataFrame(rows, columns=_MANIFEST_COLS)
        df.to_csv(_SAMPLE_PATH, index=False, encoding='utf-8-sig')
        logger.info("Sample manifest written: %s", _SAMPLE_PATH)
