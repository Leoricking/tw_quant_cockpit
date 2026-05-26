"""
data/data_quality_checker.py - Data completeness checker for TW Quant Cockpit.

Usage:
    from data.data_quality_checker import DataQualityChecker
    checker = DataQualityChecker()
    result = checker.check_stock('2383')
    df = checker.check_universe()

Formal analysis rules:
    daytrade_allowed  : requires intraday + bidask (Phase 4 unsupported → always False)
    short_allowed     : daily >= 20, institutional >= 5, margin >= 5
    mid_allowed       : daily >= 60, monthly_revenue >= 6, institutional >= 5,
                        margin >= 5, holder >= 2
    long_allowed      : daily >= 120, monthly_revenue >= 12, holder >= 2
"""

import os
import logging

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataQualityChecker:
    """Check data completeness for one stock or the entire profile universe."""

    def check_stock(self, symbol: str) -> dict:
        """
        Check data completeness for a single stock.

        Returns a dict with row counts, formal analysis flags,
        missing data list, and recommendations.
        """
        from data.real_data_loader import RealDataLoader

        sym = str(symbol)
        loader = RealDataLoader()
        all_data = loader.load_all(sym)

        profile = all_data.get('profile')
        daily_k = all_data.get('daily_k')
        institutional = all_data.get('institutional')
        margin = all_data.get('margin')
        monthly_revenue = all_data.get('monthly_revenue')
        holder = all_data.get('holder')
        trust_cost = all_data.get('trust_cost')

        profile_ok = profile is not None
        name = profile.get('name', sym) if profile else sym

        # Count rows from each data type
        if daily_k and 'bars' in daily_k:
            daily_rows = len(daily_k['bars'])
        elif daily_k and 'n_bars' in daily_k:
            daily_rows = daily_k['n_bars']
        else:
            daily_rows = 0

        inst_rows = len(institutional.get('rows', [])) if institutional else 0
        margin_rows = len(margin.get('rows', [])) if margin else 0
        rev_rows = len(monthly_revenue.get('rows', [])) if monthly_revenue else 0
        holder_rows = len(holder.get('rows', [])) if holder else 0
        tc_rows = len(trust_cost.get('rows', [])) if trust_cost else 0

        # Formal analysis rules
        daytrade_allowed = False  # Phase 4: intraday/bidask not yet supported

        short_allowed = (
            daily_rows >= 20
            and inst_rows >= 5
            and margin_rows >= 5
        )

        mid_allowed = (
            daily_rows >= 60
            and rev_rows >= 6
            and inst_rows >= 5
            and margin_rows >= 5
            and holder_rows >= 2
        )

        long_allowed = (
            daily_rows >= 120
            and rev_rows >= 12
            and holder_rows >= 2
        )

        # Missing data list
        missing = []
        if not profile_ok:
            missing.append('profile')
        if daily_rows == 0:
            missing.append('daily_k')
        if inst_rows == 0:
            missing.append('institutional')
        if margin_rows == 0:
            missing.append('margin')
        if rev_rows == 0:
            missing.append('monthly_revenue')
        if holder_rows == 0:
            missing.append('holder')
        if tc_rows == 0:
            missing.append('trust_cost')
        # Phase 4 always missing intraday/bidask for daytrade
        missing.extend(['intraday', 'bidask'])

        # Recommendations
        recommendations = []
        recommendations.append("若要正式當沖判斷，請匯入分時與五檔資料")
        if daily_rows < 20:
            recommendations.append(
                f"請匯入更多日K資料（目前 {daily_rows} 筆，短線需 ≥20 筆）"
            )
        elif daily_rows < 60:
            recommendations.append(
                f"中線正式判斷需 60 筆日K（目前 {daily_rows} 筆）"
            )
        elif daily_rows < 120:
            recommendations.append(
                f"長線正式判斷需 120 筆日K（目前 {daily_rows} 筆）"
            )
        if inst_rows < 5:
            recommendations.append(
                f"請匯入法人資料（目前 {inst_rows} 筆，短/中線需 ≥5 筆）"
            )
        if margin_rows < 5:
            recommendations.append(
                f"請匯入融資融券資料（目前 {margin_rows} 筆，短/中線需 ≥5 筆）"
            )
        if rev_rows < 6:
            recommendations.append(
                f"請匯入月營收資料（目前 {rev_rows} 筆，中線需 ≥6 筆）"
            )
        elif rev_rows < 12:
            recommendations.append(
                f"長線正式判斷需 12 期月營收（目前 {rev_rows} 筆）"
            )
        if holder_rows < 2:
            recommendations.append(
                f"請匯入大戶散戶資料（目前 {holder_rows} 筆，中/長線需 ≥2 筆）"
            )

        return {
            'symbol': sym,
            'name': name,
            'profile_ok': profile_ok,
            'daily_rows': daily_rows,
            'institutional_rows': inst_rows,
            'margin_rows': margin_rows,
            'monthly_revenue_rows': rev_rows,
            'holder_rows': holder_rows,
            'trust_cost_rows': tc_rows,
            'daytrade_allowed': daytrade_allowed,
            'short_allowed': short_allowed,
            'mid_allowed': mid_allowed,
            'long_allowed': long_allowed,
            'missing': missing,
            'recommendations': recommendations,
        }

    def check_universe(self):
        """
        Check data completeness for all stocks in the profile universe.

        Returns a pandas DataFrame with one row per stock, sorted by symbol.
        """
        import pandas as pd
        import csv as _csv

        from data.csv_schema import OUTPUT_PATHS, SAMPLE_PATHS

        # Resolve profile CSV (standard first, then sample)
        std_profile = os.path.join(
            _BASE_DIR, OUTPUT_PATHS['profile'].replace('/', os.sep)
        )
        smp_profile = os.path.join(
            _BASE_DIR, SAMPLE_PATHS['profile'].replace('/', os.sep)
        )

        profile_path = None
        for path in (std_profile, smp_profile):
            if os.path.isfile(path):
                profile_path = path
                break

        symbols = []
        if profile_path:
            try:
                with open(profile_path, 'r', encoding='utf-8-sig') as fh:
                    reader = _csv.DictReader(fh)
                    for row in reader:
                        sym = row.get('symbol', '').strip()
                        if sym and sym not in symbols:
                            symbols.append(sym)
            except Exception as exc:
                logger.warning("check_universe: cannot read profile %s: %s", profile_path, exc)

        if not symbols:
            logger.warning("check_universe: no stocks found in profile CSV")
            return pd.DataFrame()

        rows = []
        for sym in symbols:
            try:
                rows.append(self.check_stock(sym))
            except Exception as exc:
                logger.warning("check_universe error for %s: %s", sym, exc)

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows)

        # Add convenience columns aligned with spec
        df['short_ready'] = df['short_allowed']
        df['mid_ready']   = df['mid_allowed']
        df['long_ready']  = df['long_allowed']

        # Count of missing data types per row (excluding intraday/bidask)
        def _missing_count(row):
            return len([m for m in row.get('missing', []) if m not in ('intraday', 'bidask')])

        def _missing_summary(row):
            items = [m for m in row.get('missing', []) if m not in ('intraday', 'bidask')]
            return ', '.join(items) if items else ''

        df['missing_count']   = df.apply(_missing_count,   axis=1)
        df['missing_summary'] = df.apply(_missing_summary, axis=1)

        df.attrs['symbol_count'] = len(df)
        return df

    def get_audit_summary(self) -> dict:
        """
        Return a brief audit summary for integration into data-check output.

        Uses DataAuditor for a fast structural check of all data types.
        Returns dict with: invalid_daily_rows, duplicate_rows,
        missing_data_types, readiness_stage, import_recommendation.
        """
        try:
            from data.data_auditor import DataAuditor
            auditor = DataAuditor()
            audit   = auditor.audit_all()
            readiness = audit.get('readiness', {})

            daily_info = audit.get('daily', {})
            invalid_ohlc = (
                daily_info.get('invalid_close', 0)
                + daily_info.get('high_lt_low', 0)
            )
            dup_rows = sum(
                audit.get(dt, {}).get('duplicate_rows', 0)
                for dt in ['daily', 'institutional', 'margin',
                           'monthly_revenue', 'holder', 'trust_cost']
            )
            missing_types = [
                dt for dt in ['daily', 'institutional', 'margin',
                               'monthly_revenue', 'holder', 'trust_cost']
                if not audit.get(dt, {}).get('found', False)
            ]

            stage = readiness.get('validation_stage', 'FUNCTIONAL_TEST')
            short_ct = readiness.get('short_ready_count', 0)
            if short_ct == 0:
                rec = "Run: python main.py data-audit and import-plan for guidance."
            elif readiness.get('mid_ready_count', 0) == 0:
                rec = "Import institutional/margin/revenue/holder for mid-term readiness."
            else:
                rec = "Data coverage adequate. Run: python main.py validate-score --mode real"

            return {
                'invalid_daily_rows':   invalid_ohlc,
                'duplicate_rows':       dup_rows,
                'missing_data_types':   missing_types,
                'readiness_stage':      stage,
                'import_recommendation': rec,
            }
        except Exception as exc:
            logger.debug("get_audit_summary failed: %s", exc)
            return {
                'invalid_daily_rows': 0,
                'duplicate_rows': 0,
                'missing_data_types': [],
                'readiness_stage': 'UNKNOWN',
                'import_recommendation': 'Run: python main.py data-audit',
            }
