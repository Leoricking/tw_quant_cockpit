"""
data/xq_export_importer.py - XQ technical-analysis export importer for TW Quant Cockpit.

Reads a single XQ-exported Excel (.xlsx/.xls) or CSV file that contains
multiple data types (daily OHLCV, margin, institutional, trust cost, holder)
in a wide-column layout, and automatically splits + imports each type.

Usage:
    from data.xq_export_importer import XQExportImporter
    importer = XQExportImporter()
    result = importer.import_file('D:/XQ/2454.xlsx', symbol='2454', name='聯發科')
    # dry-run only:
    result = importer.import_file('D:/XQ/2454.xlsx', symbol='2454', dry_run=True)
"""

import os
import logging

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENCODINGS = ['utf-8-sig', 'utf-8', 'big5', 'cp950']

# ---------------------------------------------------------------------------
# XQ column -> standard column mappings
# ---------------------------------------------------------------------------

# Date column candidates (first one found becomes 'date')
_DATE_COLS = ['時間', 'date', 'Date', '日期', 'datetime']

# Daily OHLCV
_DAILY_MAP = {
    '開盤價': 'open',   '開盤': 'open',   'open': 'open',
    '最高價': 'high',   '最高': 'high',   'high': 'high',
    '最低價': 'low',    '最低': 'low',    'low': 'low',
    '收盤價': 'close',  '收盤': 'close',  'close': 'close',
    '成交量': 'volume', '成交量(張)': 'volume', '成交股數': 'volume',
    '成交量(股)': 'volume', 'volume': 'volume',
}

# Margin / short
_MARGIN_MAP = {
    '融資(張)': 'margin_balance',    '融資餘額': 'margin_balance',
    '融資': 'margin_balance',         'margin_balance': 'margin_balance',
    '差額(張)': 'margin_change',      '融資增減': 'margin_change',
    '融資差額': 'margin_change',      'margin_change': 'margin_change',
    '融券(張)': 'short_balance',      '融券餘額': 'short_balance',
    '融券': 'short_balance',          'short_balance': 'short_balance',
    '融券差額': 'short_change',       '融券增減': 'short_change',
    '融券差額(張)': 'short_change',   'short_change': 'short_change',
}

# Institutional net buy
_INST_MAP = {
    '投信買賣超(張)': 'trust_net_buy',   '投信買賣超': 'trust_net_buy',
    '投信淨買': 'trust_net_buy',          'trust_net_buy': 'trust_net_buy',
    '外資買賣超(張)': 'foreign_net_buy', '外資買賣超': 'foreign_net_buy',
    '外資淨買': 'foreign_net_buy',        'foreign_net_buy': 'foreign_net_buy',
    '自營商買賣超(張)': 'dealer_net_buy','自營商買賣超': 'dealer_net_buy',
    '自營淨買': 'dealer_net_buy',         'dealer_net_buy': 'dealer_net_buy',
    # Ambiguous — resolved later
    '買賣超(張)': '__net_buy_ambiguous__',
    '買賣超': '__net_buy_ambiguous__',
}

# Trust cost
_TRUST_MAP = {
    '投信買超張數': 'trust_buy_shares',  '投信買超': 'trust_buy_shares',
    'trust_buy_shares': 'trust_buy_shares',
    '投信買進金額': 'trust_buy_amount',  '投信金額': 'trust_buy_amount',
    'trust_buy_amount': 'trust_buy_amount',
    '投信成本線': 'trust_avg_cost',      '投信平均成本': 'trust_avg_cost',
    '投信成本': 'trust_avg_cost',        'trust_avg_cost': 'trust_avg_cost',
}
# close reused from daily

# Holder
_HOLDER_MAP = {
    '大戶持股比例': 'major_holder_ratio', '大戶比例': 'major_holder_ratio',
    '大戶持股比率': 'major_holder_ratio', 'major_holder_ratio': 'major_holder_ratio',
    '大戶買賣力': 'major_change',          'major_change': 'major_change',
    '散戶持股比例': 'retail_holder_ratio', '散戶比例': 'retail_holder_ratio',
    '散戶持股比率': 'retail_holder_ratio', 'retail_holder_ratio': 'retail_holder_ratio',
    '散戶買賣力': 'retail_change',          'retail_change': 'retail_change',
}

# Trust-holding columns that hint the ambiguous buy-sell column is trust-related
_TRUST_HINT_COLS = {
    '投信持股(張)', '投信持股比例', '投信持股張數', '投信持股',
    'trust_buy_shares', 'trust_buy_amount', 'trust_avg_cost',
    '投信成本線', '投信平均成本',
}


class XQExportImporter:
    """Parse and split XQ technical-analysis export files into TWQC data types."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def read_xq_file(self, file_path: str, sheet=0) -> pd.DataFrame:
        """
        Read an XQ-exported file (.xlsx/.xls/.csv).

        Returns a raw DataFrame with all columns as strings,
        or raises RuntimeError on failure.
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext in ('.xlsx', '.xls'):
            return self._read_excel(file_path, sheet)
        elif ext == '.csv':
            return self._read_csv(file_path)
        else:
            # Try CSV fallback
            return self._read_csv(file_path)

    def normalize_xq_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Strip whitespace from column names and deduplicate them."""
        cols = [str(c).strip() for c in df.columns]
        # Deduplicate by appending suffix
        seen = {}
        result = []
        for c in cols:
            if c in seen:
                seen[c] += 1
                result.append(f"{c}.{seen[c]}")
            else:
                seen[c] = 0
                result.append(c)
        df.columns = result
        return df

    def split(self, file_path: str, symbol: str, name: str = "", sheet=0) -> dict:
        """
        Read and split an XQ file into per-type DataFrames.

        Returns:
            {
                'symbol': str,
                'name': str,
                'columns_detected': [str, ...],
                'daily':         (df or None, warnings),
                'margin':        (df or None, warnings),
                'institutional': (df or None, warnings),
                'trust_cost':    (df or None, warnings),
                'holder':        (df or None, warnings),
                'errors':        [str, ...],
            }
        """
        result = {
            'symbol':            symbol,
            'name':              name,
            'columns_detected':  [],
            'daily':             (None, []),
            'margin':            (None, []),
            'institutional':     (None, []),
            'trust_cost':        (None, []),
            'holder':            (None, []),
            'errors':            [],
        }

        try:
            raw = self.read_xq_file(file_path, sheet=sheet)
        except Exception as exc:
            result['errors'].append(f"Cannot read file: {exc}")
            return result

        raw = self.normalize_xq_columns(raw)
        result['columns_detected'] = list(raw.columns)

        # Locate the date column
        date_col = self._find_date_col(raw)
        if date_col is None:
            result['errors'].append(
                "Cannot find a date/time column. Expected: 時間, 日期, date, ..."
            )
            return result

        # Convert date column
        from data.csv_cleaner import CSVCleaner
        cleaner = CSVCleaner()
        date_series = raw[date_col].apply(cleaner.normalize_date)

        result['daily']         = self._split_daily(raw, date_series, symbol, cleaner)
        result['margin']        = self._split_margin(raw, date_series, symbol, cleaner)
        result['institutional'] = self._split_institutional(raw, date_series, symbol, cleaner)
        result['trust_cost']    = self._split_trust_cost(raw, date_series, symbol, cleaner)
        result['holder']        = self._split_holder(raw, date_series, symbol, cleaner)

        return result

    def import_file(
        self,
        file_path: str,
        symbol: str,
        name: str = "",
        replace: bool = False,
        dry_run: bool = False,
        sheet=0,
    ) -> dict:
        """
        Read, split, and import an XQ file into the standard data/import/ paths.

        Parameters
        ----------
        file_path : str
        symbol    : str   Stock code, e.g. '2454'
        name      : str   Stock name, optional
        replace   : bool  Replace existing standard CSV (default: append)
        dry_run   : bool  Do not write any files
        sheet     : Excel sheet name or index

        Returns dict with per-type import results.
        """
        split_result = self.split(file_path, symbol=symbol, name=name, sheet=sheet)

        outcome = {
            'symbol':   symbol,
            'name':     name,
            'file':     file_path,
            'dry_run':  dry_run,
            'errors':   list(split_result.get('errors', [])),
            'results':  {},
        }

        if split_result['errors']:
            return outcome

        types_to_import = ['daily', 'margin', 'institutional', 'trust_cost', 'holder']

        for dt in types_to_import:
            df, warnings = split_result.get(dt, (None, []))
            if df is None or df.empty:
                outcome['results'][dt] = {
                    'success': False,
                    'rows': 0,
                    'warnings': warnings,
                    'skipped': True,
                }
                continue

            if dry_run:
                outcome['results'][dt] = {
                    'success': True,
                    'rows': len(df),
                    'warnings': warnings,
                    'dry_run': True,
                }
                continue

            # Real import via save_standard_csv
            try:
                from data.csv_importer import CSVImporter
                importer = CSVImporter()
                out_file = importer.save_standard_csv(dt, df, append=not replace)
                outcome['results'][dt] = {
                    'success':   out_file is not None,
                    'rows':      len(df),
                    'output':    out_file,
                    'warnings':  warnings,
                }
            except Exception as exc:
                outcome['results'][dt] = {
                    'success': False,
                    'rows':    0,
                    'warnings': warnings + [str(exc)],
                }

        # Auto-fill profile
        if not dry_run and symbol:
            self._ensure_profile(symbol, name)

        return outcome

    def export_split_csvs(self, split_result: dict, output_dir: str) -> dict:
        """
        Export each split DataFrame to a separate CSV in output_dir.

        Returns dict mapping data_type -> file_path.
        """
        os.makedirs(output_dir, exist_ok=True)
        symbol = split_result.get('symbol', 'unknown')
        out = {}

        for dt in ['daily', 'margin', 'institutional', 'trust_cost', 'holder']:
            df, _ = split_result.get(dt, (None, []))
            if df is not None and not df.empty:
                fname = f"{symbol}_{dt}.csv"
                fpath = os.path.join(output_dir, fname)
                df.to_csv(fpath, index=False, encoding='utf-8-sig')
                out[dt] = fpath

        return out

    # ------------------------------------------------------------------
    # Split helpers
    # ------------------------------------------------------------------

    def _split_daily(self, raw, date_series, symbol, cleaner) -> tuple:
        warnings = []
        needed = ['open', 'high', 'low', 'close', 'volume']
        col_map = self._map_columns(raw, _DAILY_MAP)

        missing = [c for c in needed if c not in col_map]
        if missing:
            warnings.append(f"Missing daily columns: {missing}")
            # Allow partial: if at least date + close we can still output
            if 'open' not in col_map and 'close' not in col_map:
                return None, warnings

        df = pd.DataFrame()
        df['date']   = date_series
        df['symbol'] = symbol

        for std, raw_col in col_map.items():
            if std in needed:
                df[std] = pd.to_numeric(
                    raw[raw_col].apply(cleaner._clean_numeric), errors='coerce'
                )

        # Fill missing numeric cols with NaN
        for col in needed:
            if col not in df.columns:
                df[col] = float('nan')

        df = df[['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']]
        df = df[df['date'].notna() & (df['date'] != '')].reset_index(drop=True)
        return df, warnings

    def _split_margin(self, raw, date_series, symbol, cleaner) -> tuple:
        warnings = []
        col_map = self._map_columns(raw, _MARGIN_MAP)

        if 'margin_balance' not in col_map:
            return None, ['No margin columns found; skipping margin.']

        df = pd.DataFrame()
        df['date']   = date_series
        df['symbol'] = symbol

        for std in ['margin_balance', 'margin_change', 'short_balance', 'short_change']:
            if std in col_map:
                df[std] = pd.to_numeric(
                    raw[col_map[std]].apply(cleaner._clean_numeric), errors='coerce'
                )
            else:
                df[std] = float('nan')
                if std in ('short_balance', 'short_change'):
                    warnings.append(
                        f"Short balance/change not found; margin import will contain financing fields only."
                    )

        df = df[['date', 'symbol', 'margin_balance', 'margin_change',
                 'short_balance', 'short_change']]
        df = df[df['date'].notna() & (df['date'] != '')].reset_index(drop=True)
        return df, warnings

    def _split_institutional(self, raw, date_series, symbol, cleaner) -> tuple:
        warnings = []
        col_map = self._map_columns(raw, _INST_MAP)

        # Resolve ambiguous buy/sell column
        if '__net_buy_ambiguous__' in col_map:
            raw_col = col_map.pop('__net_buy_ambiguous__')
            # Check if trust-hint columns exist
            has_trust_hint = any(
                c in raw.columns for c in _TRUST_HINT_COLS
            )
            if has_trust_hint:
                col_map['trust_net_buy'] = raw_col
                warnings.append(
                    "Single net-buy column inferred as trust_net_buy "
                    "because trust holding columns exist."
                )
            else:
                col_map['foreign_net_buy'] = raw_col
                warnings.append(
                    "Single net-buy column inferred as foreign_net_buy."
                )

        if not any(k in col_map for k in ('trust_net_buy', 'foreign_net_buy', 'dealer_net_buy')):
            return None, ['No institutional net-buy columns found; skipping institutional.']

        df = pd.DataFrame()
        df['date']   = date_series
        df['symbol'] = symbol

        for std in ['foreign_net_buy', 'trust_net_buy', 'dealer_net_buy']:
            if std in col_map:
                df[std] = pd.to_numeric(
                    raw[col_map[std]].apply(cleaner._clean_numeric), errors='coerce'
                )
            else:
                df[std] = float('nan')

        df = df[['date', 'symbol', 'foreign_net_buy', 'trust_net_buy', 'dealer_net_buy']]
        df = df[df['date'].notna() & (df['date'] != '')].reset_index(drop=True)

        if 'foreign_net_buy' not in col_map:
            warnings.append("foreign_net_buy not found in source; column will be empty.")
        if 'dealer_net_buy' not in col_map:
            warnings.append("dealer_net_buy not found in source; column will be empty.")

        return df, warnings

    def _split_trust_cost(self, raw, date_series, symbol, cleaner) -> tuple:
        warnings = []
        col_map = self._map_columns(raw, _TRUST_MAP)

        # close may come from daily section
        close_col = self._find_col(raw, ['收盤價', '收盤', 'close'])

        if 'trust_avg_cost' not in col_map:
            return None, ['trust_avg_cost not found; skipping trust_cost.']

        df = pd.DataFrame()
        df['date']   = date_series
        df['symbol'] = symbol

        for std in ['trust_buy_shares', 'trust_buy_amount', 'trust_avg_cost']:
            if std in col_map:
                df[std] = pd.to_numeric(
                    raw[col_map[std]].apply(cleaner._clean_numeric), errors='coerce'
                )
            else:
                df[std] = float('nan')
                if std == 'trust_buy_shares':
                    warnings.append("trust_buy_shares not found; column will be empty.")
                if std == 'trust_buy_amount':
                    warnings.append("trust_buy_amount not found; column will be empty.")

        if close_col:
            df['close'] = pd.to_numeric(
                raw[close_col].apply(cleaner._clean_numeric), errors='coerce'
            )
        else:
            df['close'] = float('nan')
            warnings.append("close not found for trust_cost; price_vs_trust_cost_pct cannot be computed.")

        # Compute price_vs_trust_cost_pct
        if 'trust_avg_cost' in col_map and close_col:
            try:
                df['price_vs_trust_cost_pct'] = (
                    (df['close'] - df['trust_avg_cost']) / df['trust_avg_cost'] * 100
                )
            except Exception:
                df['price_vs_trust_cost_pct'] = float('nan')
        else:
            df['price_vs_trust_cost_pct'] = float('nan')

        df = df[['date', 'symbol', 'trust_buy_shares', 'trust_buy_amount',
                 'trust_avg_cost', 'close', 'price_vs_trust_cost_pct']]
        df = df[df['date'].notna() & (df['date'] != '')].reset_index(drop=True)
        return df, warnings

    def _split_holder(self, raw, date_series, symbol, cleaner) -> tuple:
        warnings = []
        col_map = self._map_columns(raw, _HOLDER_MAP)

        has_any = any(
            k in col_map for k in (
                'major_holder_ratio', 'retail_holder_ratio',
                'major_change', 'retail_change'
            )
        )
        if not has_any:
            return None, ['No holder columns found; skipping holder.']

        df = pd.DataFrame()
        df['date']   = date_series
        df['symbol'] = symbol

        for std in ['major_holder_ratio', 'retail_holder_ratio', 'major_change', 'retail_change']:
            if std in col_map:
                df[std] = pd.to_numeric(
                    raw[col_map[std]].apply(cleaner._clean_numeric), errors='coerce'
                )
            else:
                df[std] = float('nan')

        if 'major_holder_ratio' not in col_map:
            warnings.append("Major holder ratio not found; holder import is partial.")
        if 'retail_holder_ratio' not in col_map:
            warnings.append("Retail holder ratio not found; holder import is partial.")

        df = df[['date', 'symbol', 'major_holder_ratio', 'retail_holder_ratio',
                 'major_change', 'retail_change']]
        df = df[df['date'].notna() & (df['date'] != '')].reset_index(drop=True)
        return df, warnings

    # ------------------------------------------------------------------
    # Profile auto-fill
    # ------------------------------------------------------------------

    def _ensure_profile(self, symbol: str, name: str = "") -> None:
        """Ensure the profile CSV contains this symbol."""
        from data.csv_schema import OUTPUT_PATHS
        import csv as _csv

        profile_path = os.path.join(
            _BASE_DIR, OUTPUT_PATHS['profile'].replace('/', os.sep)
        )
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)

        existing = {}
        fieldnames = ['symbol', 'name', 'market', 'industry', 'theme_tags',
                      'is_mainstream_theme', 'sector']

        if os.path.isfile(profile_path):
            try:
                for enc in _ENCODINGS:
                    try:
                        with open(profile_path, 'r', encoding=enc, newline='') as fh:
                            reader = _csv.DictReader(fh)
                            for row in reader:
                                sym = str(row.get('symbol', '')).strip()
                                if sym:
                                    existing[sym] = dict(row)
                        break
                    except UnicodeDecodeError:
                        continue
            except Exception as exc:
                logger.warning("_ensure_profile: cannot read profile: %s", exc)

        if symbol in existing:
            row = existing[symbol]
            if not row.get('name') and name:
                row['name'] = name
                existing[symbol] = row
            # Already present; no overwrite needed
        else:
            existing[symbol] = {
                'symbol':             symbol,
                'name':               name or '',
                'market':             'TWSE',
                'industry':           '',
                'theme_tags':         '',
                'is_mainstream_theme': '',
                'sector':             '',
            }

        # Write back
        try:
            with open(profile_path, 'w', encoding='utf-8-sig', newline='') as fh:
                writer = _csv.DictWriter(fh, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                for row in existing.values():
                    writer.writerow(row)
            logger.info("_ensure_profile: updated profile for %s", symbol)
        except Exception as exc:
            logger.warning("_ensure_profile: cannot write profile: %s", exc)

    # ------------------------------------------------------------------
    # File readers
    # ------------------------------------------------------------------

    def _read_excel(self, file_path: str, sheet=0) -> pd.DataFrame:
        """Read Excel file, keeping all values as strings."""
        try:
            import openpyxl  # noqa: F401 — check availability
        except ImportError:
            raise RuntimeError(
                "openpyxl is required to read .xlsx files. "
                "Run: pip install openpyxl"
            )

        df = pd.read_excel(file_path, sheet_name=sheet, dtype=str, header=0)
        df.columns = [str(c).strip() for c in df.columns]
        return df

    def _read_csv(self, file_path: str) -> pd.DataFrame:
        """Read CSV with multi-encoding fallback."""
        for enc in _ENCODINGS:
            try:
                df = pd.read_csv(file_path, encoding=enc, dtype=str)
                df.columns = [str(c).strip() for c in df.columns]
                return df
            except UnicodeDecodeError:
                continue
            except Exception as exc:
                raise RuntimeError(f"Cannot read CSV {file_path}: {exc}")
        raise RuntimeError(f"Cannot read {file_path} with any encoding.")

    # ------------------------------------------------------------------
    # Column helpers
    # ------------------------------------------------------------------

    def _find_date_col(self, df: pd.DataFrame):
        """Return the name of the date/time column, or None."""
        for candidate in _DATE_COLS:
            if candidate in df.columns:
                return candidate
        return None

    def _find_col(self, df: pd.DataFrame, candidates: list):
        """Return first matching column name from candidates list."""
        for c in candidates:
            if c in df.columns:
                return c
        return None

    def _map_columns(self, df: pd.DataFrame, mapping: dict) -> dict:
        """
        Build a {standard_name: raw_col_name} dict for columns present in df.
        If multiple raw cols map to the same standard name, the first wins.
        """
        result = {}
        for raw_col in df.columns:
            std = mapping.get(raw_col)
            if std and std not in result:
                result[std] = raw_col
        return result
