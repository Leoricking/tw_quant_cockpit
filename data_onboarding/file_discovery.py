"""
data_onboarding/file_discovery.py — ImportFileDiscovery for TW Quant Cockpit v1.1.1.

Discovers importable files (XQ Excel, XQ CSV, standard CSV) in a directory.
Does NOT read file content beyond headers. Does NOT write anything.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
import re
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

from data_onboarding.onboarding_schema import (
    DiscoveredFile,
    FILE_TYPE_XQ_EXCEL, FILE_TYPE_XQ_CSV, FILE_TYPE_STANDARD_CSV,
    FILE_TYPE_EXCEL, FILE_TYPE_UNKNOWN,
)

# XQ Chinese column markers
_XQ_MARKERS = {
    '時間', '開盤價', '開盤', '最高價', '最高', '最低價', '最低',
    '收盤價', '收盤', '成交量', '融資', '融券', '投信', '外資', '自營商',
    '成交量(張)', '融資(張)', '融券(張)',
}

_TAIWAN_STOCK_RE = re.compile(r'^(\d{4})([A-Z]?)$')

_ENCODINGS = ['utf-8-sig', 'utf-8', 'big5', 'cp950']

# Dataset detection column signatures
_DATASET_SIGNATURES = {
    'daily':         {'open', 'high', 'low', 'close', 'volume', '開盤價', '收盤價'},
    'margin':        {'融資', '融券', '融資(張)', '融券(張)', 'margin_balance', 'short_balance'},
    'institutional': {'投信', '外資', '自營商', 'trust_net_buy', 'foreign_net_buy', 'dealer_net_buy'},
    'trust_cost':    {'投信買超張數', '投信成本線', 'trust_buy_shares', 'trust_avg_cost'},
    'holder':        {'大股東持股', 'holder_count', 'holding_ratio'},
}


class ImportFileDiscovery:
    """
    Discovers importable files (XQ Excel, XQ CSV, standard CSV) in a directory.
    Does NOT read file content beyond headers. Does NOT write anything.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    SUPPORTED_EXTENSIONS = ['.xlsx', '.xls', '.csv']

    research_only  = True
    no_real_orders = True

    def discover(self, path: str, recursive: bool = False) -> List[DiscoveredFile]:
        """Scan path for importable files. Returns list of DiscoveredFile."""
        files: List[DiscoveredFile] = []
        if not os.path.exists(path):
            logger.warning("ImportFileDiscovery: path does not exist: %s", path)
            return files

        if os.path.isfile(path):
            df = self._process_file(path)
            if df is not None:
                files.append(df)
            return files

        walker = os.walk(path) if recursive else [(path, [], os.listdir(path))]
        for dirpath, _dirs, filenames in walker:
            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                if ext in self.SUPPORTED_EXTENSIONS:
                    full = os.path.join(dirpath, fn)
                    df = self._process_file(full)
                    if df is not None:
                        files.append(df)
        return files

    def _process_file(self, file_path: str) -> Optional[DiscoveredFile]:
        """Process a single file and return DiscoveredFile or None on hard error."""
        try:
            file_name = os.path.basename(file_path)
            size_bytes = os.path.getsize(file_path)
            file_type = self.detect_file_type(file_path)
            symbol = self.detect_symbol(file_path)
            preview = self.preview_columns(file_path)
            columns_raw = preview.get("columns", [])
            warnings = preview.get("warnings", [])
            errors = preview.get("errors", [])
            dataset = self.detect_dataset(file_path, columns_raw)
            encoding_hint = preview.get("encoding", "utf-8-sig")
            preview_rows = preview.get("rows", 0)

            # Run column mapping detector
            try:
                from data_onboarding.schema_detector import ColumnMappingDetector
                det = ColumnMappingDetector()
                detection = det.detect(columns_raw)
                columns_mapped = detection.get("mapped", {})
                confidence = detection.get("confidence", 0.0)
            except Exception:
                columns_mapped = {}
                confidence = 0.0

            # Sheet count for Excel
            sheet_count = 1
            if file_type in (FILE_TYPE_XQ_EXCEL, FILE_TYPE_EXCEL):
                try:
                    if _PANDAS_AVAILABLE:
                        import openpyxl
                        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
                        sheet_count = len(wb.sheetnames)
                        wb.close()
                except Exception:
                    sheet_count = 1

            return DiscoveredFile(
                file_path=file_path,
                file_name=file_name,
                file_type=file_type,
                size_bytes=size_bytes,
                detected_symbol=symbol,
                detected_dataset=dataset,
                sheet_count=sheet_count,
                encoding_hint=encoding_hint,
                mapping_confidence=confidence,
                columns_raw=columns_raw,
                columns_mapped=columns_mapped,
                preview_rows=preview_rows,
                warnings=warnings,
                errors=errors,
            )
        except Exception as exc:
            logger.warning("ImportFileDiscovery._process_file error on %s: %s", file_path, exc)
            return DiscoveredFile(
                file_path=file_path,
                file_name=os.path.basename(file_path),
                file_type=FILE_TYPE_UNKNOWN,
                size_bytes=0,
                detected_symbol=None,
                detected_dataset=None,
                sheet_count=0,
                encoding_hint="utf-8",
                mapping_confidence=0.0,
                errors=[str(exc)],
            )

    def detect_file_type(self, file_path: str) -> str:
        """Detect XQ_EXCEL / XQ_CSV / STANDARD_CSV / EXCEL / UNKNOWN."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.xlsx', '.xls'):
            # Try to peek at column names to decide XQ vs plain Excel
            try:
                if _PANDAS_AVAILABLE:
                    df = pd.read_excel(file_path, nrows=2)
                    cols = set(str(c) for c in df.columns)
                    if cols & _XQ_MARKERS:
                        return FILE_TYPE_XQ_EXCEL
                    return FILE_TYPE_EXCEL
            except Exception:
                pass
            return FILE_TYPE_EXCEL
        elif ext == '.csv':
            # Read first line to check for XQ markers
            for enc in _ENCODINGS:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        header = f.readline()
                    cols = set(c.strip() for c in header.split(','))
                    if cols & _XQ_MARKERS:
                        return FILE_TYPE_XQ_CSV
                    return FILE_TYPE_STANDARD_CSV
                except Exception:
                    continue
            return FILE_TYPE_UNKNOWN
        return FILE_TYPE_UNKNOWN

    def detect_symbol(self, file_path: str) -> Optional[str]:
        """Guess symbol from filename (e.g. '2454.xlsx' -> '2454')."""
        base = os.path.splitext(os.path.basename(file_path))[0]
        # Strip common suffixes like _daily, _data, etc.
        cleaned = base.split('_')[0].split('-')[0].strip()
        m = _TAIWAN_STOCK_RE.match(cleaned)
        if m:
            return m.group(1)
        # Also try full base if it's 4 digits
        if re.match(r'^\d{4}$', cleaned):
            return cleaned
        return None

    def detect_dataset(self, file_path: str, columns: List[str]) -> Optional[str]:
        """Guess dataset (daily/institutional/margin/...) from columns/filename."""
        col_set = set(columns)
        # Score each dataset
        best = None
        best_score = 0
        for ds, markers in _DATASET_SIGNATURES.items():
            score = len(col_set & markers)
            if score > best_score:
                best_score = score
                best = ds
        if best_score >= 1:
            return best
        # Fallback: filename hints
        fname = os.path.basename(file_path).lower()
        if 'margin' in fname or '融' in fname:
            return 'margin'
        if 'inst' in fname or '投信' in fname or '外資' in fname:
            return 'institutional'
        if 'daily' in fname or '日k' in fname:
            return 'daily'
        return None

    def preview_columns(self, file_path: str, sheet: int = 0) -> dict:
        """Read only the header row. Returns {'columns': [...], 'rows': N, 'warnings': [...], 'errors': [...]}."""
        result = {"columns": [], "rows": 0, "warnings": [], "errors": [], "encoding": "utf-8-sig"}
        if not _PANDAS_AVAILABLE:
            result["warnings"].append("pandas not available — cannot preview columns")
            return result

        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext in ('.xlsx', '.xls'):
                df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
                result["columns"] = [str(c) for c in df.columns.tolist()]
                result["rows"] = len(df)
            else:
                # CSV — try encodings
                for enc in _ENCODINGS:
                    try:
                        df = pd.read_csv(file_path, encoding=enc, nrows=5)
                        result["columns"] = [str(c) for c in df.columns.tolist()]
                        result["rows"] = len(df)
                        result["encoding"] = enc
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as exc2:
                        result["errors"].append(str(exc2))
                        break
        except Exception as exc:
            result["errors"].append(str(exc))
        return result

    def summarize(self, files: List[DiscoveredFile]) -> dict:
        """Return summary counts by file_type and dataset."""
        by_type: dict = {}
        by_dataset: dict = {}
        for f in files:
            by_type[f.file_type] = by_type.get(f.file_type, 0) + 1
            ds = f.detected_dataset or "unknown"
            by_dataset[ds] = by_dataset.get(ds, 0) + 1
        return {
            "total":      len(files),
            "by_type":    by_type,
            "by_dataset": by_dataset,
            "research_only":  True,
            "no_real_orders": True,
        }
