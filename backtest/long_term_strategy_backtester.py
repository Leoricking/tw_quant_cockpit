"""
backtest/long_term_strategy_backtester.py - Long-term strategy validation backtester (v0.3.11).

Goal: Validate whether v0.3.10's long-term data (>=240 daily bars, EPS, gross_margin,
      monthly revenue) actually improves predictive power for 60/120-day forward returns.

Design:
  - Loads all symbols from the universe profile CSV.
  - For each symbol, loads all daily K bars (no n_bars cap).
  - Samples evaluation dates every 20 trading bars after the first 240 bars.
  - At each evaluation date, runs LongTermAnalyzer with data available up to that date.
  - Computes forward returns at holding_days bars later.
  - Aggregates by factor buckets: EPS, gross_margin, valuation zone, PE, timing quality.
  - Reports statistical confidence via StatConfidence.for_long_term_strategy().

Data leakage note:
  Fundamental data (EPS, gross_margin) is loaded as a static snapshot — the latest available
  from the CSV. We flag timing_estimated=True when announcement_date is estimated.
  A future version should filter fundamental data by announcement_date per evaluation date.

Outputs (saved to data/backtest_results/):
  long_term_signals_<timestamp>.csv    — per-symbol per-date signal rows
  long_term_eps_factor_<timestamp>.csv — EPS bucket analysis
  long_term_gm_factor_<timestamp>.csv  — gross margin bucket analysis
  long_term_val_factor_<timestamp>.csv — valuation zone analysis
  long_term_signal_filter_<timestamp>.csv — BUY_BREAKOUT filter effect

Usage:
    bt = LongTermStrategyBacktester(mode='real', holding_days=60)
    results = bt.run()
    paths = bt.save_results(results)
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(_BASE_DIR, 'data', 'backtest_results')


class LongTermStrategyBacktester:
    """Long-term (3–12 month) strategy validation backtester."""

    EVAL_STEP   = 20   # evaluate every N trading bars
    MIN_BARS    = 250  # symbol must have at least this many bars

    def __init__(
        self,
        mode: str = 'real',
        stock: Optional[str] = None,
        holding_days: int = 60,
        output_dir: Optional[str] = None,
    ):
        self.mode         = mode
        self.stock        = stock
        self.holding_days = holding_days
        self.output_dir   = output_dir or _DEFAULT_OUTPUT_DIR
        self._is_sample   = False

    # ------------------------------------------------------------------
    # Data loading helpers
    # ------------------------------------------------------------------

    def _load_universe(self) -> list:
        """Return symbol list from profile CSV."""
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, is_sample = _resolve_csv('profile')
            if not path:
                return []
            rows = _read_csv_rows(path)
            self._is_sample = is_sample
            syms = [r['symbol'] for r in rows if r.get('symbol')]
            if self.stock:
                syms = [s for s in syms if str(s) == str(self.stock)]
            return syms
        except Exception as exc:
            logger.error("LongTermStrategyBacktester._load_universe: %s", exc)
            return []

    def _load_daily_df(self, symbol: str) -> pd.DataFrame:
        """Load ALL daily K bars for symbol (no n_bars cap)."""
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, _ = _resolve_csv('daily')
            if not path:
                return pd.DataFrame()
            rows = [r for r in _read_csv_rows(path) if r.get('symbol') == str(symbol)]
            if not rows:
                return pd.DataFrame()
            df = pd.DataFrame(rows)
            for col in ['open', 'high', 'low', 'close', 'volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna(subset=['close']).sort_values('date').reset_index(drop=True)
            return df
        except Exception as exc:
            logger.warning("LongTermStrategyBacktester._load_daily_df %s: %s", symbol, exc)
            return pd.DataFrame()

    def _load_fundamental_snapshot(self, symbol: str) -> dict:
        """Load latest fundamental snapshot for symbol."""
        try:
            from data.real_data_loader import RealDataLoader
            loader = RealDataLoader()
            return loader.load_fundamental(symbol) or {}
        except Exception as exc:
            logger.debug("LongTermStrategyBacktester._load_fundamental_snapshot %s: %s", symbol, exc)
            return {}

    def _load_monthly_revenue_rows(self, symbol: str) -> list:
        """Load monthly revenue rows for symbol."""
        try:
            from data.real_data_loader import RealDataLoader
            loader = RealDataLoader()
            rv = loader.load_monthly_revenue(symbol) or {}
            return rv.get('rows', [])
        except Exception as exc:
            logger.debug("LongTermStrategyBacktester._load_monthly_revenue_rows %s: %s", symbol, exc)
            return []

    # ------------------------------------------------------------------
    # Per-symbol backtest
    # ------------------------------------------------------------------

    def backtest_symbol(self, symbol: str) -> tuple:
        """
        Evaluate long-term signals at multiple past dates for one symbol.

        Returns (rows: list[dict], summary: dict).
        Rows have forward returns appended; empty list if insufficient data.
        """
        daily_df = self._load_daily_df(symbol)
        n_bars = len(daily_df)
        if n_bars < self.MIN_BARS:
            logger.debug("LongTermStrategyBacktester: %s only %d bars, skip", symbol, n_bars)
            return [], {}

        fundamental = self._load_fundamental_snapshot(symbol)
        monthly_rev_rows = self._load_monthly_revenue_rows(symbol)

        eps_ttm            = fundamental.get('eps_ttm')
        gross_margin       = fundamental.get('gross_margin')
        operating_margin   = fundamental.get('operating_margin')
        announcement_date  = fundamental.get('announcement_date')
        ann_is_estimated   = bool(fundamental.get('announcement_date_is_estimated', False))
        fundamental_ready  = bool(eps_ttm is not None or gross_margin is not None)

        rows = []
        start_i = 240
        end_i   = n_bars - self.holding_days - 1

        for i in range(start_i, end_i + 1, self.EVAL_STEP):
            slice_df      = daily_df.iloc[:i + 1]
            current_row   = slice_df.iloc[-1]
            current_price = float(current_row.get('close', 0) or 0)
            current_date  = str(current_row.get('date', ''))

            if current_price <= 0:
                continue

            price_data = slice_df[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict('records')

            # Compute long-term signal (use mode for mock/real distinction)
            result = {}
            try:
                from analysis.long_term_analyzer import LongTermAnalyzer
                result = LongTermAnalyzer().analyze(
                    symbol=symbol,
                    price_data=price_data,
                    eps_ttm=eps_ttm,
                    gross_margin=gross_margin,
                    operating_margin=operating_margin,
                    monthly_revenue_rows=monthly_rev_rows,
                    announcement_date=announcement_date,
                    announcement_date_is_estimated=ann_is_estimated,
                    mode=self.mode,
                    fundamental_ready=fundamental_ready,
                )
            except Exception as exc:
                logger.debug("LongTermStrategyBacktester analyze %s@%s: %s", symbol, current_date, exc)
                continue

            # Forward return
            future_i = i + self.holding_days
            forward_return = None
            if future_i < n_bars:
                future_price = float(daily_df.iloc[future_i]['close'] or 0)
                if current_price > 0 and future_price > 0:
                    forward_return = round((future_price - current_price) / current_price, 6)

            fwd_col = f'fwd_{self.holding_days}d'
            row = {
                'symbol':                   symbol,
                'date':                     current_date,
                'close':                    current_price,
                fwd_col:                    forward_return,
                'long_term_score':          result.get('long_term_score'),
                'long_term_signal':         result.get('long_term_signal', result.get('decision')),
                'long_term_buy_allowed':    result.get('long_term_buy_allowed'),
                'long_term_watch_only':     result.get('long_term_watch_only'),
                'long_term_exit_warning':   result.get('long_term_exit_warning'),
                'eps_positive':             result.get('eps_positive'),
                'eps_growth_bucket':        result.get('eps_growth_bucket'),
                'gross_margin_bucket':      result.get('gross_margin_bucket'),
                'operating_margin_bucket':  result.get('operating_margin_bucket'),
                'valuation_zone':           result.get('valuation_zone'),
                'pe_bucket':                result.get('pe_bucket'),
                'timing_quality':           result.get('timing_quality'),
                'timing_estimated':         result.get('timing_estimated'),
                'formal_allowed':           result.get('formal_allowed'),
                'data_completeness':        result.get('data_completeness'),
            }
            rows.append(row)

        summary = {
            'n_rows':        len(rows),
            'n_buy_signals': sum(1 for r in rows if r.get('long_term_signal') == 'BUY_BREAKOUT'),
            'daily_bars':    n_bars,
            'has_eps':       eps_ttm is not None,
            'has_gm':        gross_margin is not None,
            'timing_est':    ann_is_estimated,
        }
        return rows, summary

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------

    def _aggregate_factors(self, df: pd.DataFrame) -> dict:
        """Run factor analysis across all rows with valid forward returns."""
        from backtest.long_term_factor_evaluator import (
            evaluate_boolean_factor, evaluate_zone_factor,
            evaluate_filter_effect, evaluate_numeric_bucket_factor,
        )

        fwd_col = f'fwd_{self.holding_days}d'
        factors = {}

        if fwd_col not in df.columns:
            return factors

        # EPS positive/negative
        if 'eps_positive' in df.columns:
            factors['eps_positive'] = evaluate_boolean_factor(df, 'eps_positive', fwd_col)

        # EPS growth bucket
        if 'eps_growth_bucket' in df.columns:
            factors['eps_growth_bucket'] = evaluate_zone_factor(df, 'eps_growth_bucket', fwd_col)

        # Gross margin bucket
        if 'gross_margin_bucket' in df.columns:
            factors['gross_margin_bucket'] = evaluate_zone_factor(df, 'gross_margin_bucket', fwd_col)

        # Operating margin bucket
        if 'operating_margin_bucket' in df.columns:
            factors['operating_margin_bucket'] = evaluate_zone_factor(df, 'operating_margin_bucket', fwd_col)

        # Valuation zone
        if 'valuation_zone' in df.columns:
            factors['valuation_zone'] = evaluate_zone_factor(df, 'valuation_zone', fwd_col)

        # PE bucket
        if 'pe_bucket' in df.columns:
            factors['pe_bucket'] = evaluate_zone_factor(df, 'pe_bucket', fwd_col)

        # Long-term signal filter: BUY_BREAKOUT vs others
        if 'long_term_signal' in df.columns:
            buy_mask = df['long_term_signal'] == 'BUY_BREAKOUT'
            factors['signal_filter'] = evaluate_filter_effect(df, buy_mask, fwd_col)

        # Timing estimated impact
        if 'timing_estimated' in df.columns:
            factors['timing_estimated'] = evaluate_boolean_factor(df, 'timing_estimated', fwd_col)

        # Long-term score numeric buckets
        if 'long_term_score' in df.columns:
            score_buckets = [
                ('score<0',   -999,  0),
                ('score_0-4',    0,  4),
                ('score_4-7',    4,  7),
                ('score>=7',     7,  999),
            ]
            factors['long_term_score_bucket'] = evaluate_numeric_bucket_factor(
                df, 'long_term_score', fwd_col, score_buckets,
            )

        return factors

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Run the long-term strategy backtest over the universe.

        Returns
        -------
        dict with keys:
          status, mode, holding_days, n_symbols, n_signals,
          signals_df, factors, per_symbol_summary, confidence,
          is_sample, start, end.
        """
        logger.info(
            "LongTermStrategyBacktester.run [mode=%s holding_days=%d stock=%s]",
            self.mode, self.holding_days, self.stock,
        )

        symbols = self._load_universe()
        if not symbols:
            return {
                'status':  'insufficient_data',
                'message': '找不到 universe symbols，請先執行 data-check 或 universe-quality',
                'mode':    self.mode,
            }

        all_rows        = []
        per_sym_summary = {}

        for sym in symbols:
            rows, summary = self.backtest_symbol(sym)
            all_rows.extend(rows)
            if summary:
                per_sym_summary[sym] = summary

        if not all_rows:
            return {
                'status':  'insufficient_data',
                'message': '所有 symbol 資料不足 250 bars，無法計算長線回測',
                'mode':    self.mode,
                'n_symbols': len(symbols),
            }

        df = pd.DataFrame(all_rows)

        # Date range
        _dates = sorted(df['date'].dropna().tolist())
        _start = _dates[0]  if _dates else None
        _end   = _dates[-1] if _dates else None

        # Trading days estimate (unique dates across all symbols)
        trading_days = df['date'].nunique()

        # Aggregate factor analysis
        factors = self._aggregate_factors(df)

        # Confidence
        n_symbols   = df['symbol'].nunique()
        n_signals   = len(df)
        fwd_col     = f'fwd_{self.holding_days}d'
        n_valid_fwd = int(df[fwd_col].notna().sum()) if fwd_col in df.columns else 0

        # Count fundamental rows across symbols
        total_fund_rows = sum(
            1 for s in per_sym_summary.values()
            if s.get('has_eps') or s.get('has_gm')
        ) * 4  # rough estimate: each fundamental-rich symbol ≈ 4 quarters

        # Timing estimated ratio
        if 'timing_estimated' in df.columns:
            n_est = int(df['timing_estimated'].fillna(False).sum())
            timing_ratio = n_est / n_signals if n_signals > 0 else 0.0
        else:
            timing_ratio = None

        from backtest.stat_confidence import StatConfidence
        confidence = StatConfidence.for_long_term_strategy(
            symbol_count=n_symbols,
            signal_count=n_valid_fwd,
            trading_days=trading_days,
            fundamental_rows=total_fund_rows,
            timing_estimated_ratio=timing_ratio,
        )

        return {
            'status':              'ok',
            'mode':                self.mode,
            'holding_days':        self.holding_days,
            'n_symbols':           n_symbols,
            'n_signals':           n_signals,
            'n_valid_fwd':         n_valid_fwd,
            'start':               _start,
            'end':                 _end,
            'trading_days':        trading_days,
            'signals_df':          df,
            'factors':             factors,
            'per_symbol_summary':  per_sym_summary,
            'confidence':          confidence,
            'is_sample':           self._is_sample,
        }

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------

    def save_results(
        self,
        results: dict,
        output_dir: Optional[str] = None,
    ) -> dict:
        """
        Save backtest result DataFrames to CSV files.

        Returns dict of output paths.
        """
        out_dir = output_dir or self.output_dir
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        paths = {}

        # Signals DataFrame
        df = results.get('signals_df')
        if df is not None and not df.empty:
            p = os.path.join(out_dir, f'long_term_signals_{ts}.csv')
            df.to_csv(p, index=False, encoding='utf-8-sig')
            paths['signals_df'] = p
            logger.info("LongTermStrategyBacktester: saved signals to %s", p)

        # Factor tables
        factors = results.get('factors', {})
        factor_csv_map = {
            'eps_growth_bucket':       'long_term_eps_factor',
            'gross_margin_bucket':     'long_term_gm_factor',
            'valuation_zone':          'long_term_val_factor',
            'long_term_score_bucket':  'long_term_score_factor',
        }
        for factor_key, file_prefix in factor_csv_map.items():
            factor_data = factors.get(factor_key)
            if factor_data:
                try:
                    if isinstance(factor_data, list):
                        df_f = pd.DataFrame(factor_data)
                    elif isinstance(factor_data, dict):
                        rows = []
                        for grp, d in factor_data.items():
                            if isinstance(d, dict):
                                rows.append({'group': grp, **d})
                        df_f = pd.DataFrame(rows)
                    else:
                        continue
                    p = os.path.join(out_dir, f'{file_prefix}_{ts}.csv')
                    df_f.to_csv(p, index=False, encoding='utf-8-sig')
                    paths[factor_key] = p
                except Exception as exc:
                    logger.warning("save_results factor %s: %s", factor_key, exc)

        return paths
