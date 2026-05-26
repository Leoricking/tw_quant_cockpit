"""
data/data_auditor.py - Data quality auditor for TW Quant Cockpit.

Audits all imported data types in data/import/ and produces:
- Per data-type coverage statistics
- Per-symbol row counts
- Duplicate and OHLC anomaly counts
- Readiness summary (short/mid/long-term)
- Audit export (CSV + Markdown)

Usage:
    from data.data_auditor import DataAuditor
    auditor = DataAuditor()
    result  = auditor.audit_all()
    auditor.export_audit_report()
    auditor.export_audit_report(output_dir='data/import_reports')
"""

import os
import logging
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENCODINGS = ['utf-8-sig', 'utf-8', 'big5', 'cp950']

_DATA_TYPES = [
    'profile', 'daily', 'institutional', 'margin',
    'monthly_revenue', 'holder', 'trust_cost',
]


class DataAuditor:
    """Audit imported CSV data for completeness and quality."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def audit_all(self) -> dict:
        """
        Full audit of all data types.

        Returns dict with keys:
            audit_date, profile, daily, institutional, margin,
            monthly_revenue, holder, trust_cost, readiness
        """
        result = {
            'audit_date': datetime.now().strftime('%Y-%m-%d'),
        }
        for dt in _DATA_TYPES:
            result[dt] = self.audit_data_type(dt)
        result['readiness'] = self._compute_readiness(result)
        return result

    def audit_data_type(self, data_type: str) -> dict:
        """
        Audit a single data type.

        Loads the standard CSV (falls back to sample CSV if not present).
        Returns dict with coverage statistics.
        """
        from data.csv_schema import OUTPUT_PATHS, SAMPLE_PATHS

        std_path = os.path.join(
            _BASE_DIR, OUTPUT_PATHS[data_type].replace('/', os.sep)
        )
        smp_path = os.path.join(
            _BASE_DIR, SAMPLE_PATHS[data_type].replace('/', os.sep)
        )

        df = None
        used_path = None
        for path in (std_path, smp_path):
            if os.path.isfile(path):
                used_path = path
                df = self._read_csv(path)
                if df is not None:
                    break

        if df is None or df.empty:
            return {
                'data_type': data_type,
                'found': False,
                'path': used_path,
                'total_rows': 0,
                'symbol_count': 0,
            }

        if 'symbol' in df.columns:
            df['symbol'] = df['symbol'].astype(str).str.strip()

        base = {
            'data_type': data_type,
            'found': True,
            'path': used_path,
            'total_rows': len(df),
        }

        if data_type == 'profile':
            base.update(self._audit_profile(df))
        elif data_type == 'daily':
            base.update(self._audit_daily(df))
        elif data_type == 'institutional':
            base.update(self._audit_timeseries(df, 'date', [5, 40]))
        elif data_type == 'margin':
            base.update(self._audit_margin(df))
        elif data_type == 'monthly_revenue':
            base.update(self._audit_monthly_revenue(df))
        elif data_type == 'holder':
            base.update(self._audit_timeseries(df, 'date', [2, 4]))
        elif data_type == 'trust_cost':
            base.update(self._audit_timeseries(df, 'date', [3, 20, 40]))

        return base

    def audit_symbol(self, symbol: str) -> dict:
        """Audit all data types for a single symbol."""
        result = {'symbol': symbol}
        for dt in _DATA_TYPES:
            audit = self.audit_data_type(dt)
            per_sym = audit.get('per_symbol', {})
            result[dt] = per_sym.get(str(symbol), {'rows': 0})
        return result

    def check_date_coverage(self, data_type: str, symbol: str) -> dict:
        """Check date / month coverage for a specific symbol and data type."""
        from data.csv_schema import OUTPUT_PATHS, SAMPLE_PATHS

        for path_key in (OUTPUT_PATHS, SAMPLE_PATHS):
            raw = path_key[data_type]
            path = os.path.join(_BASE_DIR, raw.replace('/', os.sep))
            if not os.path.isfile(path):
                continue
            df = self._read_csv(path)
            if df is None or 'symbol' not in df.columns:
                continue
            df['symbol'] = df['symbol'].astype(str).str.strip()
            sym_df = df[df['symbol'] == str(symbol)]
            date_col = 'month' if data_type == 'monthly_revenue' else 'date'
            if date_col not in sym_df.columns:
                return {'symbol': symbol, 'data_type': data_type, 'rows': len(sym_df)}
            return {
                'symbol':    symbol,
                'data_type': data_type,
                'rows':      len(sym_df),
                'min_date':  sym_df[date_col].min() if len(sym_df) else None,
                'max_date':  sym_df[date_col].max() if len(sym_df) else None,
            }
        return {'symbol': symbol, 'data_type': data_type, 'rows': 0}

    def check_required_lengths(self, symbol: str) -> dict:
        """
        Check per-timeframe data length requirements for a single symbol.

        Returns dict with row counts and short/mid/long_ready flags.
        """
        daily  = self.check_date_coverage('daily', symbol).get('rows', 0)
        inst   = self.check_date_coverage('institutional', symbol).get('rows', 0)
        margin = self.check_date_coverage('margin', symbol).get('rows', 0)
        rev    = self.check_date_coverage('monthly_revenue', symbol).get('rows', 0)
        holder = self.check_date_coverage('holder', symbol).get('rows', 0)
        tc     = self.check_date_coverage('trust_cost', symbol).get('rows', 0)

        return {
            'symbol':               symbol,
            'daily_rows':           daily,
            'institutional_rows':   inst,
            'margin_rows':          margin,
            'monthly_revenue_rows': rev,
            'holder_rows':          holder,
            'trust_cost_rows':      tc,
            'short_ready':  daily >= 20 and inst >= 5 and margin >= 5,
            'mid_ready':    daily >= 60 and rev >= 6 and inst >= 5 and margin >= 5 and holder >= 2,
            'long_ready':   daily >= 120 and rev >= 12 and holder >= 2,
        }

    def export_audit_report(self, output_dir: str = "data/import_reports") -> dict:
        """
        Export audit report to Markdown and CSV.

        Creates:
            data/import_reports/data_audit_report_{date}.md
            data/import_reports/data_audit_summary.csv

        Returns dict with file paths and the raw audit result.
        """
        from data.import_reporter import ImportReporter

        result = self.audit_all()
        abs_dir = os.path.join(_BASE_DIR, output_dir.replace('/', os.sep))
        os.makedirs(abs_dir, exist_ok=True)

        date_str = datetime.now().strftime('%Y%m%d')
        md_file  = os.path.join(abs_dir, f'data_audit_report_{date_str}.md')
        csv_file = os.path.join(abs_dir, 'data_audit_summary.csv')

        reporter = ImportReporter()
        reporter.write_audit_report(result, md_file)

        rows = []
        for dt in _DATA_TYPES:
            audit = result.get(dt, {})
            rows.append({
                'data_type':    dt,
                'found':        audit.get('found', False),
                'total_rows':   audit.get('total_rows', 0),
                'symbol_count': audit.get('symbol_count', 0),
            })
        pd.DataFrame(rows).to_csv(csv_file, index=False, encoding='utf-8-sig')

        logger.info("DataAuditor: exported audit to %s", abs_dir)
        return {'markdown': md_file, 'csv': csv_file, 'audit': result}

    # ------------------------------------------------------------------
    # Internal audit helpers
    # ------------------------------------------------------------------

    def _audit_profile(self, df) -> dict:
        symbols = df['symbol'].dropna().unique().tolist() if 'symbol' in df.columns else []
        dupes   = int(df['symbol'].duplicated().sum()) if 'symbol' in df.columns else 0
        missing_names  = self._count_empty(df, 'name')
        missing_sector = self._count_empty(df, 'sector')
        missing_theme  = self._count_empty(df, 'theme_tags')
        return {
            'symbol_count':       len(symbols),
            'duplicate_symbols':  dupes,
            'missing_names':      missing_names,
            'missing_sector':     missing_sector,
            'missing_theme_tags': missing_theme,
            'per_symbol':         {s: {'rows': 1} for s in symbols},
        }

    def _audit_daily(self, df) -> dict:
        if 'symbol' not in df.columns:
            return {'symbol_count': 0}

        per_sym = df.groupby('symbol').size()
        result = {
            'symbol_count':          len(per_sym),
            'symbols_less_than_20d': int((per_sym < 20).sum()),
            'symbols_less_than_60d': int((per_sym < 60).sum()),
            'symbols_less_than_120d': int((per_sym < 120).sum()),
        }

        dedup_cols = ['symbol', 'date'] if 'date' in df.columns else ['symbol']
        result['duplicate_rows'] = int(df.duplicated(subset=dedup_cols).sum())

        for col in ['open', 'high', 'low', 'close']:
            if col in df.columns:
                num = pd.to_numeric(df[col], errors='coerce')
                result[f'null_{col}'] = int(num.isna().sum())
                if col == 'close':
                    result['invalid_close'] = int(((num <= 0) & num.notna()).sum())

        if 'high' in df.columns and 'low' in df.columns:
            high = pd.to_numeric(df['high'], errors='coerce')
            low  = pd.to_numeric(df['low'],  errors='coerce')
            result['high_lt_low'] = int(((high < low) & high.notna() & low.notna()).sum())

        if 'volume' in df.columns:
            vol = pd.to_numeric(df['volume'], errors='coerce')
            result['negative_volume'] = int(((vol < 0) & vol.notna()).sum())

        result['per_symbol'] = {sym: {'rows': int(n)} for sym, n in per_sym.items()}
        return result

    def _audit_timeseries(self, df, date_col: str, thresholds: list) -> dict:
        if 'symbol' not in df.columns:
            return {'symbol_count': 0}

        per_sym = df.groupby('symbol').size()
        result = {'symbol_count': len(per_sym)}

        dedup_cols = ['symbol', date_col] if date_col in df.columns else ['symbol']
        result['duplicate_rows'] = int(df.duplicated(subset=dedup_cols).sum())

        for thr in thresholds:
            key = f'symbols_less_than_{thr}d'
            result[key] = int((per_sym < thr).sum())

        result['per_symbol'] = {sym: {'rows': int(n)} for sym, n in per_sym.items()}
        return result

    def _audit_margin(self, df) -> dict:
        result = self._audit_timeseries(df, 'date', [5, 40])
        for col in ['margin_balance', 'short_balance']:
            if col in df.columns:
                num = pd.to_numeric(df[col], errors='coerce')
                result[f'negative_{col}'] = int(((num < 0) & num.notna()).sum())
        return result

    def _audit_monthly_revenue(self, df) -> dict:
        if 'symbol' not in df.columns:
            return {'symbol_count': 0}

        per_sym = df.groupby('symbol').size()
        result = {
            'symbol_count':          len(per_sym),
            'symbols_less_than_6m':  int((per_sym < 6).sum()),
            'symbols_less_than_12m': int((per_sym < 12).sum()),
        }

        date_col = 'month' if 'month' in df.columns else None
        if date_col:
            result['duplicate_rows'] = int(df.duplicated(
                subset=['symbol', date_col]
            ).sum())

        if 'revenue' in df.columns:
            num = pd.to_numeric(df['revenue'], errors='coerce')
            result['negative_revenue'] = int(((num < 0) & num.notna()).sum())

        result['per_symbol'] = {sym: {'rows': int(n)} for sym, n in per_sym.items()}
        return result

    def _compute_readiness(self, result: dict) -> dict:
        """Compute readiness summary across all data types."""
        daily_info  = result.get('daily', {})
        inst_info   = result.get('institutional', {})
        margin_info = result.get('margin', {})
        rev_info    = result.get('monthly_revenue', {})
        holder_info = result.get('holder', {})
        tc_info     = result.get('trust_cost', {})

        daily_sym  = daily_info.get('symbol_count', 0)
        inst_sym   = inst_info.get('symbol_count', 0)
        margin_sym = margin_info.get('symbol_count', 0)
        rev_sym    = rev_info.get('symbol_count', 0)
        holder_sym = holder_info.get('symbol_count', 0)
        tc_sym     = tc_info.get('symbol_count', 0)

        d120 = max(daily_sym  - daily_info.get('symbols_less_than_120d', daily_sym), 0)
        i40  = max(inst_sym   - inst_info.get('symbols_less_than_40d', inst_sym), 0)
        m40  = max(margin_sym - margin_info.get('symbols_less_than_40d', margin_sym), 0)
        r12  = max(rev_sym    - rev_info.get('symbols_less_than_12m', rev_sym), 0)
        h4   = max(holder_sym - holder_info.get('symbols_less_than_4d', holder_sym), 0)
        tc20 = max(tc_sym     - tc_info.get('symbols_less_than_20d', tc_sym), 0)

        short_ready = min(d120, i40, m40) if daily_sym else 0
        mid_ready   = min(d120, i40, m40, r12, h4) if daily_sym else 0
        long_ready  = min(d120, r12, h4) if daily_sym else 0

        profile_count = result.get('profile', {}).get('symbol_count', 0)

        try:
            from backtest.stat_confidence import StatConfidence
            sc_result = StatConfidence().evaluate_universe(profile_count)
            confidence = sc_result.get('level', 'INSUFFICIENT')
            stage      = sc_result.get('stage', 'FUNCTIONAL_TEST')
        except Exception:
            confidence = 'INSUFFICIENT' if profile_count < 50 else 'OBSERVATIONAL'
            stage      = 'FUNCTIONAL_TEST' if profile_count < 10 else 'SMALL_SAMPLE'

        return {
            'profile_count':          profile_count,
            'short_ready_count':      max(short_ready, 0),
            'mid_ready_count':        max(mid_ready, 0),
            'long_ready_count':       max(long_ready, 0),
            'validation_stage':       stage,
            'statistical_confidence': confidence,
            'daily_120':              d120,
            'institutional_40':       i40,
            'margin_40':              m40,
            'revenue_12':             r12,
            'holder_4':               h4,
            'trust_cost_20':          tc20,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _read_csv(self, path: str):
        for enc in _ENCODINGS:
            try:
                df = pd.read_csv(path, encoding=enc, dtype=str)
                df.columns = [c.strip() for c in df.columns]
                return df
            except UnicodeDecodeError:
                continue
            except Exception as exc:
                logger.warning("DataAuditor._read_csv failed for %s: %s", path, exc)
                return None
        return None

    @staticmethod
    def _count_empty(df, col: str) -> int:
        if col not in df.columns:
            return 0
        return int((df[col].isna() | (df[col].astype(str).str.strip() == '')).sum())
