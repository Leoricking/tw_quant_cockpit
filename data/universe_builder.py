"""
data/universe_builder.py - Universe builder and manager for TW Quant Cockpit.

Supports building a stock universe from:
  - top50 / top100 / top200 sample templates (config/universe/)
  - User-supplied profile CSV files (XQ / Excel / manual)

Usage:
    from data.universe_builder import UniverseBuilder
    builder = UniverseBuilder()
    result  = builder.build_from_template('top50')

    builder2 = UniverseBuilder()
    result2  = builder2.merge_universe(df, replace=False)
"""

import os
import logging

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_TEMPLATE_PATHS = {
    'top50':  os.path.join(_BASE_DIR, 'config', 'universe', 'top50_sample.csv'),
    'top100': os.path.join(_BASE_DIR, 'config', 'universe', 'top100_sample.csv'),
    'top200': os.path.join(_BASE_DIR, 'config', 'universe', 'top200_sample.csv'),
}

_PROFILE_OUTPUT = os.path.join(_BASE_DIR, 'data', 'import', 'profile', 'stock_profile.csv')

_REQUIRED_COLUMNS = ['symbol', 'name', 'market', 'industry', 'theme_tags', 'is_mainstream_theme', 'sector']
_VALID_MARKETS    = {'TWSE', 'TPEx', ''}


class UniverseBuilder:
    """Build and manage the stock universe / profile CSV."""

    def __init__(self, base_dir: str = None):
        self._output = _PROFILE_OUTPUT
        if base_dir:
            self._output = os.path.join(base_dir, 'stock_profile.csv')

    # ------------------------------------------------------------------
    # Load helpers
    # ------------------------------------------------------------------

    def load_profile(self):
        """Load current stock_profile.csv; return empty DataFrame if missing."""
        import pandas as pd
        if os.path.isfile(self._output):
            try:
                df = pd.read_csv(self._output, dtype={'symbol': str})
                df['symbol'] = df['symbol'].astype(str).str.strip()
                return df
            except Exception as exc:
                logger.warning("load_profile: %s", exc)
        return pd.DataFrame(columns=_REQUIRED_COLUMNS)

    def load_universe_file(self, file_path: str):
        """Load a user-supplied profile CSV; try multiple encodings."""
        import pandas as pd
        encodings = ['utf-8-sig', 'utf-8', 'big5', 'cp950']
        last_exc = None
        for enc in encodings:
            try:
                df = pd.read_csv(file_path, dtype={'symbol': str}, encoding=enc)
                df['symbol'] = df['symbol'].astype(str).str.strip()
                return df
            except UnicodeDecodeError as exc:
                last_exc = exc
            except Exception as exc:
                last_exc = exc
                break
        raise ValueError(f"Cannot read {file_path}: {last_exc}")

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_universe(self, df) -> dict:
        """
        Validate a universe DataFrame.

        Returns:
            {
                "success": bool,
                "rows": int,
                "duplicate_symbols": list,
                "missing_columns": list,
                "missing_names": list,
                "warnings": list,
            }
        """
        warnings = []

        # Missing columns
        missing_cols = [c for c in _REQUIRED_COLUMNS if c not in df.columns]

        if missing_cols:
            return {
                'success': False,
                'rows': len(df),
                'duplicate_symbols': [],
                'missing_columns': missing_cols,
                'missing_names': [],
                'warnings': [f"Missing required columns: {missing_cols}"],
            }

        # Symbol null/empty
        sym_null = df['symbol'].isna() | (df['symbol'].astype(str).str.strip() == '')
        if sym_null.any():
            warnings.append(f"{sym_null.sum()} rows have empty symbol; will be dropped")
            df = df[~sym_null].copy()

        # Duplicate symbols
        dupes = df['symbol'][df['symbol'].duplicated()].tolist()
        if dupes:
            warnings.append(f"Duplicate symbols: {dupes}")

        # Missing names
        missing_names = df.loc[
            df['name'].isna() | (df['name'].astype(str).str.strip() == ''), 'symbol'
        ].tolist()
        if missing_names:
            warnings.append(f"{len(missing_names)} symbols have no name")

        # Market values
        if 'market' in df.columns:
            bad_market = df.loc[
                ~df['market'].fillna('').isin(_VALID_MARKETS), 'symbol'
            ].tolist()
            if bad_market:
                warnings.append(f"Unusual market value for: {bad_market[:10]}")

        # is_mainstream_theme coercibility
        if 'is_mainstream_theme' in df.columns:
            coerce_fail = 0
            for v in df['is_mainstream_theme'].dropna():
                if str(v).strip().lower() not in ('0', '1', 'true', 'false', ''):
                    coerce_fail += 1
            if coerce_fail:
                warnings.append(f"{coerce_fail} rows have non-boolean is_mainstream_theme")

        return {
            'success': True,
            'rows': len(df),
            'duplicate_symbols': dupes,
            'missing_columns': [],
            'missing_names': missing_names,
            'warnings': warnings,
        }

    # ------------------------------------------------------------------
    # Merge / export
    # ------------------------------------------------------------------

    def merge_universe(self, df, replace: bool = False) -> dict:
        """
        Merge df into the current profile CSV.

        replace=True  → overwrite entire file with df
        replace=False → append and deduplicate by symbol (new data wins)

        Returns summary dict with counts.
        """
        import pandas as pd

        val = self.validate_universe(df)
        if not val['success']:
            return {'success': False, 'rows_added': 0, 'total_rows': 0,
                    'warnings': val['warnings']}

        # Ensure output directory exists
        os.makedirs(os.path.dirname(self._output), exist_ok=True)

        if replace:
            out_df = df[_REQUIRED_COLUMNS].copy()
        else:
            existing = self.load_profile()
            if existing.empty:
                out_df = df.copy()
            else:
                # Append then drop duplicates keeping last (new data wins)
                combined = pd.concat([existing, df], ignore_index=True)
                out_df = combined.drop_duplicates(subset=['symbol'], keep='last')

        # Ensure required columns present
        for col in _REQUIRED_COLUMNS:
            if col not in out_df.columns:
                out_df[col] = ''

        out_df = out_df[_REQUIRED_COLUMNS].copy()
        out_df['symbol'] = out_df['symbol'].astype(str)
        out_df.sort_values('symbol', inplace=True)
        out_df.to_csv(self._output, index=False, encoding='utf-8-sig')

        return {
            'success': True,
            'rows_added': len(df),
            'total_rows': len(out_df),
            'warnings': val['warnings'],
        }

    def export_profile(self, df, output_file: str = None) -> str:
        """Export a DataFrame to a profile CSV; returns path written."""
        if output_file is None:
            output_file = self._output
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        for col in _REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = ''
        df[_REQUIRED_COLUMNS].to_csv(output_file, index=False, encoding='utf-8-sig')
        return output_file

    # ------------------------------------------------------------------
    # Build from template
    # ------------------------------------------------------------------

    def build_from_template(self, template: str = 'top50') -> dict:
        """
        Build profile from a sample template.

        template: 'top50' | 'top100' | 'top200'
        Writes to data/import/profile/stock_profile.csv.
        Returns summary dict.
        """
        if template not in _TEMPLATE_PATHS:
            return {'success': False, 'error': f"Unknown template: {template}. "
                    f"Valid: {list(_TEMPLATE_PATHS.keys())}"}

        tpath = _TEMPLATE_PATHS[template]
        if not os.path.isfile(tpath):
            return {'success': False, 'error': f"Template file not found: {tpath}"}

        try:
            df = self.load_universe_file(tpath)
        except Exception as exc:
            return {'success': False, 'error': str(exc)}

        result = self.merge_universe(df, replace=True)
        result['template'] = template
        result['source'] = tpath
        result['output'] = self._output
        return result
