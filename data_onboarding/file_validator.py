"""
data_onboarding/file_validator.py — ImportFileValidator for TW Quant Cockpit v1.1.1.

Validates a discovered file before import.
Checks: required columns, date validity, OHLC logic, duplicates, conflicts.
Does NOT write anything.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

from data_onboarding.onboarding_schema import (
    FileValidationResult,
    VALIDATION_OK, VALIDATION_WARNING, VALIDATION_FAIL, VALIDATION_BLOCKED,
)
from data_onboarding.schema_detector import ColumnMappingDetector

_ENCODINGS = ['utf-8-sig', 'utf-8', 'big5', 'cp950']
_REQUIRED_COLS_DAILY = {'date', 'open', 'high', 'low', 'close', 'volume'}
_REQUIRED_COLS_MAP = {
    'daily':         {'date', 'open', 'high', 'low', 'close', 'volume'},
    'margin':        {'date', 'margin_balance', 'short_balance'},
    'institutional': {'date', 'trust_net_buy', 'foreign_net_buy', 'dealer_net_buy'},
    'trust_cost':    {'date', 'trust_avg_cost'},
    'holder':        {'date'},
}


class ImportFileValidator:
    """
    Validates a discovered file before import.
    Checks: required columns, date validity, OHLC logic, duplicates, conflicts.
    Does NOT write anything.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def validate(self, file_path: str, symbol: Optional[str], dataset: str = 'daily') -> FileValidationResult:
        """Validate a file. Returns FileValidationResult."""
        warnings: List[str] = []
        errors: List[str] = []

        if not _PANDAS_AVAILABLE:
            return FileValidationResult(
                file_path=file_path, symbol=symbol, dataset=dataset,
                status=VALIDATION_BLOCKED, row_count=0, valid_rows=0,
                invalid_rows=0, duplicate_count=0, conflict_count=0,
                errors=["pandas not available — cannot validate"],
            )

        # Load file
        df = self._load_file(file_path, warnings, errors)
        if df is None:
            return FileValidationResult(
                file_path=file_path, symbol=symbol, dataset=dataset,
                status=VALIDATION_FAIL, row_count=0, valid_rows=0,
                invalid_rows=0, duplicate_count=0, conflict_count=0,
                errors=errors, warnings=warnings,
            )

        # Map columns
        det = ColumnMappingDetector()
        detection = det.detect(df.columns.tolist())
        df = det.map_columns(df, detection["mapped"])

        # Check required columns
        missing_required = self._check_required_columns(df, dataset)
        if missing_required:
            errors.append(f"Missing required columns: {missing_required}")

        row_count = len(df)
        date_info: dict = {}
        ohlc_info: dict = {}
        dup_info: dict = {}
        invalid_rows = 0

        # Check dates if date column exists
        if 'date' in df.columns:
            date_info = self._check_dates(df)
            invalid_rows += date_info.get("invalid_count", 0)
            warnings.extend(date_info.get("warnings", []))
            errors.extend(date_info.get("errors", []))
        else:
            warnings.append("No 'date' column found after mapping.")

        # Check OHLC logic
        ohlc_cols = {'open', 'high', 'low', 'close', 'volume'}
        if ohlc_cols & set(df.columns):
            ohlc_info = self._check_ohlc(df)
            invalid_rows += ohlc_info.get("invalid_count", 0)
            warnings.extend(ohlc_info.get("warnings", []))
            errors.extend(ohlc_info.get("errors", []))

        # Check duplicates within file
        if 'date' in df.columns:
            dup_info = self._check_duplicates(df)
            warnings.extend(dup_info.get("warnings", []))

        duplicate_count = dup_info.get("count", 0)
        conflict_count  = dup_info.get("conflicts", 0)
        valid_rows = max(0, row_count - invalid_rows)

        # Date range
        date_range_start = date_info.get("date_min")
        date_range_end   = date_info.get("date_max")

        # Optional columns
        optional_cols_present = set(df.columns)
        all_known = {'open', 'high', 'low', 'close', 'volume', 'date',
                     'margin_balance', 'short_balance', 'trust_net_buy',
                     'foreign_net_buy', 'dealer_net_buy'}
        missing_optional = [c for c in all_known if c not in optional_cols_present]

        status = self._classify_status(missing_required, invalid_rows, errors)

        return FileValidationResult(
            file_path=file_path,
            symbol=symbol,
            dataset=dataset,
            status=status,
            row_count=row_count,
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
            duplicate_count=duplicate_count,
            conflict_count=conflict_count,
            missing_required_cols=missing_required,
            missing_optional_cols=[],
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            warnings=warnings,
            errors=errors,
        )

    def _load_file(self, file_path: str, warnings: List[str], errors: List[str]):
        """Load file into DataFrame."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.xlsx', '.xls'):
            try:
                return pd.read_excel(file_path)
            except Exception as exc:
                errors.append(f"Excel load error: {exc}")
                return None
        elif ext == '.csv':
            for enc in _ENCODINGS:
                try:
                    df = pd.read_csv(file_path, encoding=enc)
                    return df
                except UnicodeDecodeError:
                    continue
                except Exception as exc:
                    errors.append(f"CSV load error ({enc}): {exc}")
                    return None
            errors.append("Could not decode CSV with any known encoding")
            return None
        else:
            errors.append(f"Unsupported extension: {ext}")
            return None

    def _check_required_columns(self, df, dataset: str) -> List[str]:
        """Returns list of missing required columns."""
        required = _REQUIRED_COLS_MAP.get(dataset, _REQUIRED_COLS_DAILY)
        present = set(df.columns)
        return [c for c in required if c not in present]

    def _check_dates(self, df) -> dict:
        """Check date column: parseable, no future dates > today + 1, etc."""
        result = {"warnings": [], "errors": [], "invalid_count": 0,
                  "date_min": None, "date_max": None}
        try:
            dates = pd.to_datetime(df['date'], errors='coerce')
            n_invalid = int(dates.isna().sum())
            result["invalid_count"] = n_invalid
            if n_invalid > 0:
                result["warnings"].append(f"{n_invalid} rows have unparseable date values")
            valid_dates = dates.dropna()
            if len(valid_dates) > 0:
                future_limit = pd.Timestamp(datetime.now() + timedelta(days=1))
                n_future = int((valid_dates > future_limit).sum())
                if n_future > 0:
                    result["warnings"].append(f"{n_future} rows have future dates (> today+1)")
                result["date_min"] = str(valid_dates.min().date())
                result["date_max"] = str(valid_dates.max().date())
        except Exception as exc:
            result["errors"].append(f"Date check error: {exc}")
        return result

    def _check_ohlc(self, df) -> dict:
        """Check high >= low, close > 0, open > 0, volume >= 0."""
        result = {"warnings": [], "errors": [], "invalid_count": 0}
        try:
            invalid_mask = pd.Series([False] * len(df), index=df.index)
            if 'high' in df.columns and 'low' in df.columns:
                try:
                    high = pd.to_numeric(df['high'], errors='coerce')
                    low  = pd.to_numeric(df['low'],  errors='coerce')
                    bad_hl = (high < low).fillna(False)
                    n_bad = int(bad_hl.sum())
                    if n_bad > 0:
                        result["warnings"].append(f"{n_bad} rows have high < low (invalid OHLC)")
                        invalid_mask |= bad_hl
                except Exception:
                    pass
            if 'close' in df.columns:
                try:
                    close = pd.to_numeric(df['close'], errors='coerce')
                    bad_close = (close <= 0).fillna(False)
                    n_bad = int(bad_close.sum())
                    if n_bad > 0:
                        result["warnings"].append(f"{n_bad} rows have close <= 0")
                        invalid_mask |= bad_close
                except Exception:
                    pass
            if 'volume' in df.columns:
                try:
                    vol = pd.to_numeric(df['volume'], errors='coerce')
                    bad_vol = (vol < 0).fillna(False)
                    n_bad = int(bad_vol.sum())
                    if n_bad > 0:
                        result["warnings"].append(f"{n_bad} rows have volume < 0")
                        invalid_mask |= bad_vol
                except Exception:
                    pass
            result["invalid_count"] = int(invalid_mask.sum())
        except Exception as exc:
            result["errors"].append(f"OHLC check error: {exc}")
        return result

    def _check_duplicates(self, df, existing_df=None) -> dict:
        """
        Identify duplicate dates within the file.
        If existing_df provided, also detect conflicts with existing data.
        """
        result = {"count": 0, "conflicts": 0, "warnings": []}
        try:
            if 'date' not in df.columns:
                return result
            date_counts = df['date'].value_counts()
            duplicates = date_counts[date_counts > 1]
            n_dup = int(duplicates.sum()) - len(duplicates)
            result["count"] = n_dup
            if n_dup > 0:
                result["warnings"].append(f"{n_dup} duplicate date rows found within file")

            if existing_df is not None and 'date' in existing_df.columns:
                existing_dates = set(existing_df['date'].astype(str))
                incoming_dates = set(df['date'].astype(str))
                overlap = incoming_dates & existing_dates
                if overlap:
                    result["conflicts"] = len(overlap)
                    result["warnings"].append(f"{len(overlap)} dates conflict with existing data")
        except Exception as exc:
            result["warnings"].append(f"Duplicate check error: {exc}")
        return result

    def _classify_status(self, missing_required: List[str], invalid_rows: int, errors: List[str]) -> str:
        """OK / WARNING / FAIL / BLOCKED"""
        if errors and any('blocked' in e.lower() for e in errors):
            return VALIDATION_BLOCKED
        if missing_required:
            return VALIDATION_FAIL
        if errors:
            return VALIDATION_FAIL
        if invalid_rows > 0:
            return VALIDATION_WARNING
        return VALIDATION_OK
