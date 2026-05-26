"""
data/csv_cleaner.py - CSV data cleaner for TW Quant Cockpit.

Handles XQ / Excel / manually-prepared CSV normalization:
- Symbol normalization (strip .TW/.TWO, leading zeros)
- Date normalization (ROC/民國 year, multiple formats) -> YYYY-MM-DD
- Month normalization -> YYYY-MM
- Numeric cleaning (千分位, N/A, --, empty)
- Percent cleaning
- Duplicate removal (keep last)
- Sorting
- Anomaly detection (warnings only, no abort)

Usage:
    from data.csv_cleaner import CSVCleaner
    cleaner = CSVCleaner()
    cleaned_df, summary = cleaner.clean_dataframe('daily', df)
    cleaned_df, summary = cleaner.clean_file('daily', 'path/to/file.csv')

summary keys:
    input_rows, output_rows, duplicates_removed, warnings, errors
"""

import re
import logging

import pandas as pd

logger = logging.getLogger(__name__)

_ENCODINGS = ['utf-8-sig', 'utf-8', 'big5', 'cp950']

_DEDUP_KEYS = {
    'profile':         ['symbol'],
    'daily':           ['symbol', 'date'],
    'institutional':   ['symbol', 'date'],
    'margin':          ['symbol', 'date'],
    'monthly_revenue': ['symbol', 'month'],
    'holder':          ['symbol', 'date'],
    'trust_cost':      ['symbol', 'date'],
}

_SORT_KEYS = _DEDUP_KEYS

_DATE_TYPES  = {'daily', 'institutional', 'margin', 'holder', 'trust_cost'}
_MONTH_TYPES = {'monthly_revenue'}

_NA_STRINGS = {'', '-', '--', 'N/A', 'n/a', 'NA', 'null', 'None', 'NaN', 'nan', '#N/A', '#VALUE!'}

_RE_STRIP_PREFIX = re.compile(r'^TWSE:', re.IGNORECASE)
_RE_STRIP_SUFFIX = re.compile(r'\.(TW|TWO)$', re.IGNORECASE)
_RE_FLOAT_SYMBOL = re.compile(r'^\d+\.0+$')


class CSVCleaner:
    """Normalize and clean CSV data for TWQC standard format."""

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def clean_file(self, data_type: str, file_path: str) -> tuple:
        """
        Read file (multi-encoding) then clean.

        Returns (cleaned_df, summary).
        """
        import os
        if not os.path.isfile(file_path):
            return pd.DataFrame(), {
                'input_rows': 0, 'output_rows': 0, 'duplicates_removed': 0,
                'warnings': [], 'errors': [f'File not found: {file_path}'],
            }

        df = None
        for enc in _ENCODINGS:
            try:
                df = pd.read_csv(file_path, encoding=enc, dtype=str)
                df.columns = [c.strip() for c in df.columns]
                break
            except UnicodeDecodeError:
                continue
            except Exception as exc:
                return pd.DataFrame(), {
                    'input_rows': 0, 'output_rows': 0, 'duplicates_removed': 0,
                    'warnings': [], 'errors': [f'Cannot read file: {exc}'],
                }

        if df is None:
            return pd.DataFrame(), {
                'input_rows': 0, 'output_rows': 0, 'duplicates_removed': 0,
                'warnings': [], 'errors': [f'Cannot read with any encoding: {file_path}'],
            }

        return self.clean_dataframe(data_type, df)

    def clean_dataframe(self, data_type: str, df: pd.DataFrame) -> tuple:
        """
        Clean a DataFrame for the given data_type.

        Returns (cleaned_df, summary dict).
        """
        df = df.copy()
        summary = {
            'input_rows': len(df),
            'output_rows': 0,
            'duplicates_removed': 0,
            'warnings': [],
            'errors': [],
        }

        # --- symbol ---
        if 'symbol' in df.columns:
            df['symbol'] = df['symbol'].apply(self.normalize_symbol)
            bad_sym = df['symbol'].isna() | (df['symbol'] == '')
            if bad_sym.any():
                summary['errors'].append(
                    f"{int(bad_sym.sum())} row(s) have invalid/empty symbol and will be dropped."
                )
                df = df[~bad_sym].reset_index(drop=True)

        # --- date ---
        if data_type in _DATE_TYPES and 'date' in df.columns:
            df['date'] = df['date'].apply(self.normalize_date)
            bad_date = df['date'].isna() | (df['date'] == '')
            if bad_date.any():
                summary['warnings'].append(
                    f"{int(bad_date.sum())} row(s) have unparseable date value."
                )

        # --- month ---
        if data_type in _MONTH_TYPES and 'month' in df.columns:
            df['month'] = df['month'].apply(self.normalize_month)
            bad_month = df['month'].isna() | (df['month'] == '')
            if bad_month.any():
                summary['warnings'].append(
                    f"{int(bad_month.sum())} row(s) have unparseable month value."
                )

        # --- numeric columns ---
        try:
            from data.csv_schema import NUMERIC_COLUMNS
            for col in NUMERIC_COLUMNS.get(data_type, []):
                if col in df.columns:
                    df[col] = df[col].apply(self._clean_numeric)
        except ImportError:
            pass

        # --- duplicates ---
        df, dupes = self.drop_duplicate_rows(data_type, df)
        summary['duplicates_removed'] = dupes

        # --- sort ---
        df = self.sort_rows(data_type, df)

        # --- anomalies ---
        anomaly_warnings = self.detect_anomalies(data_type, df)
        summary['warnings'].extend(anomaly_warnings)

        summary['output_rows'] = len(df)
        return df, summary

    # ------------------------------------------------------------------
    # Symbol normalization
    # ------------------------------------------------------------------

    def normalize_symbol(self, value) -> str:
        """
        Normalize stock symbol to plain digit string.

        Rules:
        - 2330.0  -> '2330'
        - 2330.TW -> '2330'
        - TWSE:2330 -> '2330'
        - '0050'  -> '0050' (preserve leading zeros)
        - empty / non-digit -> ''
        """
        if value is None:
            return ''
        if isinstance(value, float):
            if pd.isna(value):
                return ''
            # e.g. 2330.0
            value = str(int(value)) if value == int(value) else str(value)
        s = str(value).strip()
        if not s or s.lower() in ('nan', 'none', 'null'):
            return ''
        s = _RE_STRIP_PREFIX.sub('', s).strip()
        s = _RE_STRIP_SUFFIX.sub('', s).strip()
        if _RE_FLOAT_SYMBOL.match(s):
            s = s.split('.')[0]
        if not re.match(r'^\d+$', s):
            return ''
        return s

    # ------------------------------------------------------------------
    # Date normalization
    # ------------------------------------------------------------------

    def normalize_date(self, value) -> str:
        """
        Normalize date to YYYY-MM-DD.

        Supports:
        - 2024-01-02  or  2024/01/02
        - 20240102
        - 113/01/02  (ROC year)
        - 1130102    (ROC compact 7 digits)
        """
        if value is None:
            return ''
        if isinstance(value, float) and pd.isna(value):
            return ''
        s = str(value).strip()
        if not s or s.lower() in ('nan', 'none', 'null'):
            return ''

        # ROC compact 7 digits: 1130102
        m = re.match(r'^(\d{3})(\d{2})(\d{2})$', s)
        if m:
            y = int(m.group(1)) + 1911
            return f"{y}-{m.group(2)}-{m.group(3)}"

        # ROC slash: 113/01/02
        m = re.match(r'^(\d{2,3})/(\d{1,2})/(\d{1,2})$', s)
        if m and int(m.group(1)) < 200:
            y = int(m.group(1)) + 1911
            return f"{y}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

        # YYYYMMDD compact
        m = re.match(r'^(\d{4})(\d{2})(\d{2})$', s)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

        # YYYY-MM-DD or YYYY/MM/DD
        m = re.match(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$', s)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

        return ''

    # ------------------------------------------------------------------
    # Month normalization
    # ------------------------------------------------------------------

    def normalize_month(self, value) -> str:
        """
        Normalize month to YYYY-MM.

        Supports:
        - 2024-01  or  2024/01
        - 202401
        - 113/01  (ROC year)
        - 11301   (ROC compact 5 digits)
        """
        if value is None:
            return ''
        if isinstance(value, float) and pd.isna(value):
            return ''
        s = str(value).strip()
        if not s or s.lower() in ('nan', 'none', 'null'):
            return ''

        # ROC compact 5 digits: 11301
        m = re.match(r'^(\d{3})(\d{2})$', s)
        if m and int(m.group(1)) < 200:
            y = int(m.group(1)) + 1911
            return f"{y}-{m.group(2)}"

        # ROC slash: 113/01
        m = re.match(r'^(\d{2,3})/(\d{1,2})$', s)
        if m and int(m.group(1)) < 200:
            y = int(m.group(1)) + 1911
            return f"{y}-{int(m.group(2)):02d}"

        # YYYYMM compact
        m = re.match(r'^(\d{4})(\d{2})$', s)
        if m:
            return f"{m.group(1)}-{m.group(2)}"

        # YYYY-MM or YYYY/MM
        m = re.match(r'^(\d{4})[-/](\d{1,2})$', s)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}"

        return ''

    # ------------------------------------------------------------------
    # Numeric cleaning
    # ------------------------------------------------------------------

    def normalize_numeric(self, value):
        """Remove thousand separators, convert N/A variants to NaN."""
        return self._clean_numeric(value)

    def normalize_percent(self, value):
        """
        Normalize percentage value.

        '12.3%'  -> 12.3
        '+12.3%' -> 12.3
        '-5.6%'  -> -5.6
        '12.3'   -> 12.3
        Returns float or NaN.
        """
        if value is None:
            return float('nan')
        if isinstance(value, float) and pd.isna(value):
            return float('nan')
        s = str(value).strip()
        if s in _NA_STRINGS:
            return float('nan')
        s = s.replace(',', '')
        if s.endswith('%'):
            s = s[:-1]
        try:
            return float(s)
        except ValueError:
            return float('nan')

    def remove_thousand_separator(self, value):
        """Remove thousand separators (commas) from a string number."""
        if value is None:
            return value
        if isinstance(value, float) and pd.isna(value):
            return value
        return str(value).replace(',', '')

    # ------------------------------------------------------------------
    # Duplicate removal
    # ------------------------------------------------------------------

    def drop_duplicate_rows(self, data_type: str, df: pd.DataFrame) -> tuple:
        """
        Remove duplicate rows keyed by data_type dedup keys. Keep last occurrence.

        Returns (deduplicated_df, count_removed).
        """
        keys = _DEDUP_KEYS.get(data_type, [])
        valid_keys = [k for k in keys if k in df.columns]
        if not valid_keys:
            return df, 0
        before = len(df)
        df = df.drop_duplicates(subset=valid_keys, keep='last').reset_index(drop=True)
        return df, before - len(df)

    # ------------------------------------------------------------------
    # Sorting
    # ------------------------------------------------------------------

    def sort_rows(self, data_type: str, df: pd.DataFrame) -> pd.DataFrame:
        """Sort DataFrame by sort keys for the given data_type."""
        keys = _SORT_KEYS.get(data_type, [])
        valid_keys = [k for k in keys if k in df.columns]
        if valid_keys:
            df = df.sort_values(valid_keys).reset_index(drop=True)
        return df

    # ------------------------------------------------------------------
    # Anomaly detection
    # ------------------------------------------------------------------

    def detect_anomalies(self, data_type: str, df: pd.DataFrame) -> list:
        """
        Detect anomalous values. Returns list of warning strings.
        Does not modify the DataFrame or abort import.
        """
        warnings = []

        if data_type == 'daily':
            for col in ['open', 'high', 'low', 'close']:
                if col in df.columns:
                    nulls = int(pd.to_numeric(df[col], errors='coerce').isna().sum())
                    if nulls:
                        warnings.append(f"daily.{col}: {nulls} null value(s)")
            if 'close' in df.columns:
                close = pd.to_numeric(df['close'], errors='coerce')
                bad = int(((close <= 0) & close.notna()).sum())
                if bad:
                    warnings.append(f"daily.close: {bad} row(s) with close <= 0")
            if 'volume' in df.columns:
                vol = pd.to_numeric(df['volume'], errors='coerce')
                bad = int(((vol < 0) & vol.notna()).sum())
                if bad:
                    warnings.append(f"daily.volume: {bad} row(s) with volume < 0")
            if 'high' in df.columns and 'low' in df.columns:
                high = pd.to_numeric(df['high'], errors='coerce')
                low  = pd.to_numeric(df['low'],  errors='coerce')
                bad  = int(((high < low) & high.notna() & low.notna()).sum())
                if bad:
                    warnings.append(f"daily: {bad} row(s) with high < low")

        elif data_type == 'institutional':
            try:
                from data.csv_schema import NUMERIC_COLUMNS
                for col in NUMERIC_COLUMNS.get('institutional', []):
                    if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                        warnings.append(
                            f"institutional.{col}: non-numeric values detected"
                        )
            except ImportError:
                pass

        elif data_type == 'margin':
            for col in ['margin_balance', 'short_balance']:
                if col in df.columns:
                    num = pd.to_numeric(df[col], errors='coerce')
                    bad = int(((num < 0) & num.notna()).sum())
                    if bad:
                        warnings.append(f"margin.{col}: {bad} row(s) with {col} < 0")

        elif data_type == 'monthly_revenue':
            if 'revenue' in df.columns:
                num = pd.to_numeric(df['revenue'], errors='coerce')
                bad = int(((num < 0) & num.notna()).sum())
                if bad:
                    warnings.append(
                        f"monthly_revenue.revenue: {bad} row(s) with revenue < 0"
                    )

        elif data_type == 'holder':
            for col in ['major_holder_ratio', 'retail_holder_ratio']:
                if col in df.columns:
                    num = pd.to_numeric(df[col], errors='coerce')
                    bad_lo = int(((num < 0) & num.notna()).sum())
                    bad_hi = int(((num > 100) & num.notna()).sum())
                    if bad_lo:
                        warnings.append(f"holder.{col}: {bad_lo} row(s) with value < 0")
                    if bad_hi:
                        warnings.append(f"holder.{col}: {bad_hi} row(s) with value > 100")

        elif data_type == 'trust_cost':
            for col in ['trust_avg_cost', 'close']:
                if col in df.columns:
                    num = pd.to_numeric(df[col], errors='coerce')
                    bad = int(((num <= 0) & num.notna()).sum())
                    if bad:
                        warnings.append(
                            f"trust_cost.{col}: {bad} row(s) with {col} <= 0"
                        )

        return warnings

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _clean_numeric(self, value):
        """Clean a single numeric value: remove commas, convert NA to NaN."""
        if value is None:
            return float('nan')
        if isinstance(value, (int, float)):
            try:
                if pd.isna(value):
                    return float('nan')
            except Exception:
                pass
            return value
        s = str(value).strip()
        if s in _NA_STRINGS:
            return float('nan')
        s = s.replace(',', '').replace('%', '')
        try:
            return float(s)
        except ValueError:
            return float('nan')
