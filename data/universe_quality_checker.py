"""
data/universe_quality_checker.py - Universe data quality checker for v0.3.8.

Extends DataQualityChecker with universe-level quality analysis and
strategy backtest eligibility determination.

Thresholds (stricter than short-term analyzer defaults):
    short_term_ready  : daily >= 60,  institutional >= 5,  margin >= 5
    mid_term_ready    : daily >= 120, institutional >= 20, margin >= 20,
                        holder >= 2,  monthly_revenue >= 6
    long_term_ready   : daily >= 240, holder >= 2, monthly_revenue >= 12
    strategy_bt_ready : daily >= 60 (minimum for backtest rolling window)

Usage:
    from data.universe_quality_checker import UniverseQualityChecker
    uqc = UniverseQualityChecker()
    df  = uqc.check_universe()
    summary = uqc.summarize_universe_quality(df)
    eligible = uqc.get_strategy_backtest_eligible_symbols(df)
"""

import logging
import os
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_IMPORT_REPORTS_DIR = os.path.join(_BASE_DIR, 'data', 'import_reports')

# Readiness thresholds
_SHORT_DAILY_MIN    = 60
_SHORT_INST_MIN     = 5
_SHORT_MARGIN_MIN   = 5
_MID_DAILY_MIN      = 120
_MID_INST_MIN       = 20
_MID_MARGIN_MIN     = 20
_MID_HOLDER_MIN     = 2
_MID_REV_MIN        = 6
_LONG_DAILY_MIN     = 240
_LONG_HOLDER_MIN    = 2
_LONG_REV_MIN       = 12
_BT_DAILY_MIN       = 60   # minimum for strategy knowledge backtest


class UniverseQualityChecker:
    """
    Checks data completeness for all symbols in the universe manifest
    or the current profile CSV, applying strategy-backtest-grade thresholds.
    """

    def check_symbol(self, symbol: str, profile_data: dict = None) -> dict:
        """
        Check readiness of one symbol.

        Parameters
        ----------
        symbol       : stock symbol string
        profile_data : optional pre-loaded profile dict (to avoid repeated IO)

        Returns
        -------
        dict with readiness flags and row counts
        """
        from data.real_data_loader import RealDataLoader

        sym    = str(symbol)
        loader = RealDataLoader()
        data   = loader.load_all(sym)

        profile = data.get('profile') or {}
        name    = profile.get('name', sym)

        daily_k         = data.get('daily_k') or {}
        institutional   = data.get('institutional') or {}
        margin          = data.get('margin') or {}
        monthly_revenue = data.get('monthly_revenue') or {}
        holder          = data.get('holder') or {}
        trust_cost      = data.get('trust_cost') or {}

        if 'bars' in daily_k:
            daily_rows = len(daily_k['bars'])
        elif 'n_bars' in daily_k:
            daily_rows = daily_k['n_bars']
        else:
            daily_rows = 0

        inst_rows  = len(institutional.get('rows', []))
        margin_rows= len(margin.get('rows', []))
        rev_rows   = len(monthly_revenue.get('rows', []))
        holder_rows= len(holder.get('rows', []))
        tc_rows    = len(trust_cost.get('rows', []))

        # Readiness with v0.3.8 thresholds
        short_term_ready = (
            daily_rows  >= _SHORT_DAILY_MIN
            and inst_rows   >= _SHORT_INST_MIN
            and margin_rows >= _SHORT_MARGIN_MIN
        )
        mid_term_ready = (
            daily_rows  >= _MID_DAILY_MIN
            and inst_rows   >= _MID_INST_MIN
            and margin_rows >= _MID_MARGIN_MIN
            and holder_rows >= _MID_HOLDER_MIN
            and rev_rows    >= _MID_REV_MIN
        )
        long_term_ready = (
            daily_rows  >= _LONG_DAILY_MIN
            and holder_rows >= _LONG_HOLDER_MIN
            and rev_rows    >= _LONG_REV_MIN
        )
        strategy_bt_ready = (daily_rows >= _BT_DAILY_MIN)

        warnings = []
        if daily_rows < _BT_DAILY_MIN:
            warnings.append(f'daily {daily_rows} < {_BT_DAILY_MIN} (bt threshold)')
        if inst_rows < _SHORT_INST_MIN:
            warnings.append(f'institutional {inst_rows} < {_SHORT_INST_MIN}')
        if margin_rows < _SHORT_MARGIN_MIN:
            warnings.append(f'margin {margin_rows} < {_SHORT_MARGIN_MIN}')

        return {
            'symbol':              sym,
            'name':                name,
            'daily_rows':          daily_rows,
            'institutional_rows':  inst_rows,
            'margin_rows':         margin_rows,
            'monthly_revenue_rows': rev_rows,
            'holder_rows':         holder_rows,
            'trust_cost_rows':     tc_rows,
            'short_term_ready':    short_term_ready,
            'mid_term_ready':      mid_term_ready,
            'long_term_ready':     long_term_ready,
            'strategy_bt_ready':   strategy_bt_ready,
            'warning':             '; '.join(warnings) if warnings else '',
        }

    def check_universe(
        self,
        symbols: list = None,
        manifest_path: str = None,
    ) -> pd.DataFrame:
        """
        Check data quality for all symbols.

        Parameters
        ----------
        symbols       : explicit list of symbols (overrides other sources)
        manifest_path : path to universe_manifest.csv (preferred over profile CSV)

        Returns
        -------
        pd.DataFrame with one row per symbol
        """
        # Resolve symbol list
        if symbols:
            sym_list = [str(s) for s in symbols]
        elif manifest_path and os.path.isfile(manifest_path):
            try:
                mdf = pd.read_csv(manifest_path, dtype=str)
                sym_list = list(mdf['symbol'].dropna().astype(str).unique())
            except Exception as exc:
                logger.warning("check_universe: cannot read manifest %s: %s", manifest_path, exc)
                sym_list = []
        else:
            # Fall back to existing DataQualityChecker.check_universe
            try:
                from data.data_quality_checker import DataQualityChecker
                base_df = DataQualityChecker().check_universe()
                if base_df.empty:
                    return pd.DataFrame()
                sym_list = list(base_df['symbol'].astype(str).unique())
            except Exception as exc:
                logger.warning("check_universe fallback failed: %s", exc)
                return pd.DataFrame()

        if not sym_list:
            return pd.DataFrame()

        rows = []
        for sym in sym_list:
            try:
                rows.append(self.check_symbol(sym))
            except Exception as exc:
                logger.warning("check_symbol %s failed: %s", sym, exc)
                rows.append({
                    'symbol': sym, 'name': sym,
                    'daily_rows': 0, 'institutional_rows': 0,
                    'margin_rows': 0, 'monthly_revenue_rows': 0,
                    'holder_rows': 0, 'trust_cost_rows': 0,
                    'short_term_ready': False, 'mid_term_ready': False,
                    'long_term_ready': False, 'strategy_bt_ready': False,
                    'warning': f'check failed: {exc}',
                })

        return pd.DataFrame(rows)

    def summarize_universe_quality(self, df: pd.DataFrame = None) -> dict:
        """
        Produce a summary dict from a quality DataFrame.

        If df is None, runs check_universe() first.
        """
        if df is None or df.empty:
            df = self.check_universe()
        if df is None or df.empty:
            return {
                'universe_size': 0, 'imported_count': 0,
                'short_ready_count': 0, 'mid_ready_count': 0,
                'long_ready_count': 0, 'strategy_bt_ready_count': 0,
                'missing_daily': [], 'missing_institutional': [],
                'missing_margin': [], 'next_steps': [],
            }

        n               = len(df)
        imported        = int((df['daily_rows'].astype(int) > 0).sum())
        short_ready     = int(df['short_term_ready'].astype(bool).sum())
        mid_ready       = int(df['mid_term_ready'].astype(bool).sum())
        long_ready      = int(df['long_term_ready'].astype(bool).sum())
        bt_ready        = int(df['strategy_bt_ready'].astype(bool).sum())

        missing_daily   = list(df[df['daily_rows'].astype(int) == 0]['symbol'])
        missing_inst    = list(df[df['institutional_rows'].astype(int) < _SHORT_INST_MIN]['symbol'])
        missing_margin  = list(df[df['margin_rows'].astype(int) < _SHORT_MARGIN_MIN]['symbol'])
        missing_rev     = list(df[df['monthly_revenue_rows'].astype(int) < _MID_REV_MIN]['symbol'])
        missing_holder  = list(df[df['holder_rows'].astype(int) < _MID_HOLDER_MIN]['symbol'])

        # Confidence expectation
        from backtest.stat_confidence import StatConfidence
        conf = StatConfidence.for_universe(symbol_count=bt_ready)

        next_steps = []
        if missing_daily:
            next_steps.append(f"Priority: import daily K for {', '.join(missing_daily[:5])}")
        if missing_inst:
            next_steps.append(f"Import institutional data for {len(missing_inst)} symbols")
        if missing_margin:
            next_steps.append(f"Import margin data for {len(missing_margin)} symbols")
        if bt_ready < 10:
            next_steps.append(
                f"Need {10 - bt_ready} more symbols with daily >= {_BT_DAILY_MIN} "
                f"to reach OBSERVATIONAL confidence"
            )
        elif bt_ready < 30:
            next_steps.append(
                f"Need {30 - bt_ready} more symbols to reach RELIABLE confidence"
            )

        return {
            'universe_size':          n,
            'imported_count':         imported,
            'short_ready_count':      short_ready,
            'mid_ready_count':        mid_ready,
            'long_ready_count':       long_ready,
            'strategy_bt_ready_count': bt_ready,
            'missing_daily':          missing_daily,
            'missing_institutional':  missing_inst,
            'missing_margin':         missing_margin,
            'missing_monthly_revenue': missing_rev,
            'missing_holder':         missing_holder,
            'confidence':             conf,
            'next_steps':             next_steps,
        }

    def get_strategy_backtest_eligible_symbols(self, df: pd.DataFrame = None) -> list:
        """
        Return symbols eligible for strategy knowledge backtest.
        Threshold: daily_rows >= _BT_DAILY_MIN.
        """
        if df is None or df.empty:
            df = self.check_universe()
        if df is None or df.empty:
            return []
        eligible = df[df['strategy_bt_ready'].astype(bool)]
        return list(eligible['symbol'].astype(str))

    def save_quality_report_csv(
        self,
        df: pd.DataFrame,
        output_dir: str = None,
    ) -> str:
        """Save quality DataFrame to CSV. Returns file path."""
        out_dir = output_dir or _IMPORT_REPORTS_DIR
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, 'universe_quality_report.csv')
        try:
            df.to_csv(path, index=False, encoding='utf-8-sig')
        except Exception as exc:
            logger.warning("Could not save quality CSV: %s", exc)
        return path
