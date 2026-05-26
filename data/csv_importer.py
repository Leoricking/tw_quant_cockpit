"""
data/csv_importer.py - CSV importer for TW Quant Cockpit real data.

Supports importing XQ / Excel / manually prepared CSV files into the
standardized data/import/ directory structure.

Usage:
    from data.csv_importer import CSVImporter
    importer = CSVImporter()
    result = importer.import_csv('daily', 'D:/data/xq_daily.csv')
    result = importer.import_csv('daily', 'D:/data/xq_daily.csv', append=False)  # replace
"""

import os
import logging

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENCODINGS = ['utf-8-sig', 'utf-8', 'big5', 'cp950']


class CSVImporter:
    """
    Import user CSV files into the standard data/import/ structure.

    Handles:
    - Multiple encodings (UTF-8-SIG, UTF-8, Big5, CP950)
    - Chinese to English column name translation
    - Required column validation
    - Numeric type normalization
    - Date column standardization
    - Symbol zero-padding preservation
    - Append (deduplicated) or replace modes
    """

    def import_csv(self, data_type: str, file_path: str, append: bool = True) -> dict:
        """
        Import a CSV file into the standard format.

        Parameters
        ----------
        data_type : str
            One of: profile, daily, institutional, margin,
            monthly_revenue, holder, trust_cost
        file_path : str
            Path to the input CSV file.
        append : bool
            True = merge into existing standard CSV (default).
            False = replace existing standard CSV.

        Returns
        -------
        dict
            Import summary with keys: success, data_type, input_file,
            output_file, rows_imported, rows_total, duplicates_removed,
            missing_columns, warnings, errors, clean_summary.
        """
        from data.csv_schema import get_schema, SUPPORTED_DATA_TYPES

        result = {
            'success': False,
            'data_type': data_type,
            'input_file': file_path,
            'output_file': '',
            'rows_imported': 0,
            'rows_total': 0,
            'duplicates_removed': 0,
            'missing_columns': [],
            'warnings': [],
            'errors': [],
            'clean_summary': {},
        }

        if data_type not in SUPPORTED_DATA_TYPES:
            result['warnings'].append(
                f"Unsupported data type: {data_type}. Supported: {SUPPORTED_DATA_TYPES}"
            )
            return result

        schema = get_schema(data_type)
        result['output_file'] = schema['output_path']

        try:
            import pandas as pd
        except ImportError:
            result['warnings'].append("pandas not installed. Run: pip install pandas")
            return result

        # 1. Read input file (multi-encoding)
        df = self._read_with_encoding(file_path, result['warnings'])
        if df is None:
            return result

        result['rows_total'] = len(df)

        # 2. Normalize column names (Chinese -> English)
        df = self.normalize_columns(data_type, df)

        # 3. Validate required columns
        validation = self.validate_columns(data_type, df)
        if not validation['ok']:
            result['missing_columns'] = validation['missing']
            result['errors'].append(
                f"Missing required columns: {validation['missing']} — import aborted."
            )
            result['warnings'] = result['errors']  # keep backward compat
            return result

        if validation.get('extra'):
            result['warnings'].append(f"Ignoring unknown columns: {validation['extra']}")

        # 4. CSVCleaner: normalize symbols, dates, numerics, dedup, sort, anomalies
        try:
            from data.csv_cleaner import CSVCleaner
            cleaner = CSVCleaner()
            df, clean_summary = cleaner.clean_dataframe(data_type, df)
            result['clean_summary'] = clean_summary
            result['duplicates_removed'] = clean_summary.get('duplicates_removed', 0)
            result['warnings'].extend(clean_summary.get('warnings', []))
            result['errors'].extend(clean_summary.get('errors', []))
            # Abort on critical errors (empty symbol)
            if clean_summary.get('errors') and df.empty:
                result['errors'].append("No valid rows remain after cleaning — import aborted.")
                return result
        except ImportError:
            # Fallback: basic type normalization only
            df = self.normalize_types(data_type, df)

        # 5. Validate cleaned DataFrame has required columns
        validation2 = self.validate_columns(data_type, df)
        if not validation2['ok']:
            result['missing_columns'] = validation2['missing']
            result['errors'].append(
                f"After cleaning, missing columns: {validation2['missing']} — import aborted."
            )
            return result

        # 6. Save to standard CSV
        out_file = self.save_standard_csv(data_type, df, append=append)
        if out_file is None:
            result['errors'].append("Failed to save standard CSV.")
            result['warnings'].append("Failed to save standard CSV.")
            return result

        result['success'] = True
        result['rows_imported'] = len(df)
        result['output_file'] = out_file
        return result

    def validate_columns(self, data_type: str, df) -> dict:
        """
        Check that all required columns are present after alias normalization.

        Returns dict with keys: ok (bool), missing (list), extra (list).
        """
        from data.csv_schema import REQUIRED_COLUMNS
        required = set(REQUIRED_COLUMNS[data_type])
        present = set(df.columns.tolist())
        missing = sorted(required - present)
        extra = sorted(present - required)
        return {'ok': len(missing) == 0, 'missing': missing, 'extra': extra}

    def normalize_columns(self, data_type: str, df) -> object:
        """Rename Chinese or alias column names to standard English names."""
        from data.csv_schema import COLUMN_ALIASES
        aliases = COLUMN_ALIASES.get(data_type, {})
        df = df.rename(columns=aliases)
        df.columns = [c.strip() for c in df.columns]
        return df

    def normalize_types(self, data_type: str, df) -> object:
        """Normalize symbol, numeric, and date column types."""
        import pandas as pd
        from data.csv_schema import NUMERIC_COLUMNS, DATE_COLUMNS

        # Symbol → str, preserve leading zeros
        if 'symbol' in df.columns:
            df['symbol'] = df['symbol'].astype(str).str.strip().str.zfill(4)

        # Numeric columns
        for col in NUMERIC_COLUMNS.get(data_type, []):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Date/month columns — keep as string, strip whitespace
        for col in DATE_COLUMNS.get(data_type, []):
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        return df

    def save_standard_csv(self, data_type: str, df, append: bool = True) -> str:
        """
        Save DataFrame to the standard CSV path.

        If append=True and the standard CSV already exists, merge and deduplicate.
        Returns the output file path on success, or None on error.
        """
        import pandas as pd
        from data.csv_schema import get_schema

        schema = get_schema(data_type)
        output_path = os.path.join(
            _BASE_DIR, schema['output_path'].replace('/', os.sep)
        )
        dedup_keys = schema['dedup_keys']
        required_cols = schema['required_columns']

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            if append and os.path.isfile(output_path):
                existing = self._read_with_encoding(output_path, [])
                if existing is not None and not existing.empty:
                    if 'symbol' in existing.columns:
                        existing['symbol'] = (
                            existing['symbol'].astype(str).str.strip().str.zfill(4)
                        )
                    combined = pd.concat([existing, df], ignore_index=True)
                else:
                    combined = df.copy()
            else:
                combined = df.copy()

            # Deduplicate: keep last occurrence (new data wins)
            dedup_cols = [c for c in dedup_keys if c in combined.columns]
            if dedup_cols:
                combined = combined.drop_duplicates(subset=dedup_cols, keep='last')

            # Sort by dedup keys
            sort_cols = [c for c in dedup_keys if c in combined.columns]
            if sort_cols:
                combined = combined.sort_values(sort_cols).reset_index(drop=True)

            # Keep only required columns (in spec order)
            out_cols = [c for c in required_cols if c in combined.columns]
            combined = combined[out_cols]

            combined.to_csv(output_path, index=False, encoding='utf-8-sig')
            logger.info("CSVImporter: saved %d rows to %s", len(combined), output_path)
            return output_path

        except Exception as exc:
            logger.error("CSVImporter.save_standard_csv failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_with_encoding(self, file_path: str, warnings: list):
        """Try multiple encodings to read a CSV. Returns DataFrame or None."""
        import pandas as pd

        if not os.path.isfile(file_path):
            if warnings is not None:
                warnings.append(f"找不到檔案：{file_path}")
            return None

        for enc in _ENCODINGS:
            try:
                df = pd.read_csv(file_path, encoding=enc, dtype=str)
                df.columns = [c.strip() for c in df.columns]
                return df
            except UnicodeDecodeError:
                continue
            except Exception as exc:
                if warnings is not None:
                    warnings.append(f"讀取失敗（{enc}）：{exc}")
                return None

        if warnings is not None:
            warnings.append(f"無法以任何編碼讀取：{file_path}")
        return None
