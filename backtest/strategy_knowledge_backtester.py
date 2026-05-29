"""
backtest/strategy_knowledge_backtester.py - Strategy Knowledge Engine backtest validator.

v0.3.7: Validates each Phase 2 strategy knowledge module against historical
forward returns. Uses strictly backward-looking signal detection and
intentional-look-ahead forward return labels.

Modules validated:
  KD Advanced         — kd_low_golden_cross, kd_high_death_cross,
                        kd_mid_noise_cross, kd_high_sticky_trend
  Short Interest      — short_squeeze_fuel_score, price_up_short_balance_up,
                        limit_up_short_balance_up, weak_stock_short_increase
  Bottom Reversal     — bottom_reversal_detected, is_speculative_rebound
  Sector Rotation     — unavailable without peer data (marked in report)
  Fundamental Quality — unavailable without time-series fundamental data (marked)
  No Chase            — kd_high_death_cross proxy, overextension proxy
  No Panic Sell       — volume shrinkage proxy

Data leakage rules
------------------
1. All signal detection uses only past bars (no look-ahead).
2. Forward returns are labels only — never written back into features.
3. Mode=mock produces MOCK DEMO ONLY conclusions.
4. sample_count < min_samples → confidence = INSUFFICIENT.

Usage
-----
    bt = StrategyKnowledgeBacktester(mode='real', holding_days=20)
    results = bt.run()
    paths = bt.save_results(results)
"""

import logging
import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from backtest.stat_confidence import StatConfidence
from backtest.strategy_signal_evaluator import (
    evaluate_binary_signal,
    evaluate_bucket_signal,
    evaluate_warning_filter,
    calculate_profit_factor,
)

logger = logging.getLogger(__name__)

_sc = StatConfidence()
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(_BASE_DIR, 'data', 'backtest_results')

# Minimum bars to process a symbol (need enough history for KD + forward window)
_MIN_BARS = 40


# ---------------------------------------------------------------------------
# Mock data generator
# ---------------------------------------------------------------------------

def _generate_mock_df(symbol: str, n_days: int = 300, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic daily OHLCV data for mock mode.

    Embeds deliberate KD golden cross / death cross and bottom reversal patterns
    so that mock validation exercises all code paths.
    """
    rng = random.Random(seed)
    np.random.seed(seed)

    start_date = datetime(2023, 1, 1)
    dates = []
    current = start_date
    for _ in range(n_days):
        while current.weekday() >= 5:  # skip weekends
            current += timedelta(days=1)
        dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)

    # Price simulation: trending + mean-reverting + noise
    price = 100.0
    prices = []
    for i in range(n_days):
        # Add a cyclical component to ensure KD crossovers
        cycle = 5.0 * np.sin(2 * np.pi * i / 60)
        shock = np.random.normal(0, 0.8)
        trend = 0.02 if i < n_days // 2 else -0.02
        price = max(10.0, price + trend + cycle * 0.1 + shock)
        prices.append(round(price, 2))

    closes = np.array(prices)
    opens  = np.array([max(0.5, c * (1 + np.random.uniform(-0.01, 0.01))) for c in closes])
    highs  = np.array([c * (1 + abs(np.random.uniform(0, 0.015))) for c in closes])
    lows   = np.array([c * (1 - abs(np.random.uniform(0, 0.015))) for c in closes])
    volumes = np.array([int(abs(np.random.normal(1_000_000, 300_000))) + 100_000
                        for _ in range(n_days)])

    df = pd.DataFrame({
        'symbol': symbol,
        'date':   dates[:len(closes)],
        'open':   opens,
        'high':   highs,
        'low':    lows,
        'close':  closes,
        'volume': volumes,
    })
    return df


# ---------------------------------------------------------------------------
# Vectorized signal detection (no look-ahead)
# ---------------------------------------------------------------------------

def _detect_kd_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute KD signals for all rows using vectorized stochastic calculation.

    Strictly backward-looking: each row only uses data up to and including
    that row (exponential moving averages carry no future information).
    """
    close = df['close'].astype(float)
    high  = df['high'].astype(float)  if 'high'  in df.columns else close
    low   = df['low'].astype(float)   if 'low'   in df.columns else close

    # Stochastic %K
    period = 9
    lowest  = low.rolling(period, min_periods=1).min()
    highest = high.rolling(period, min_periods=1).max()
    denom   = (highest - lowest).replace(0, np.nan)
    raw_k   = (close - lowest) / denom * 100.0
    raw_k   = raw_k.fillna(50.0)

    # Smooth K (3-period EMA) → D (3-period EMA of K)
    K = raw_k.ewm(com=2, min_periods=1).mean()
    D = K.ewm(com=2, min_periods=1).mean()

    # Crossover detection
    k_prev = K.shift(1).fillna(50.0)
    d_prev = D.shift(1).fillna(50.0)
    golden = (K > D) & (k_prev <= d_prev)
    death  = (K < D) & (k_prev >= d_prev)

    # Sticky high: K >= 80 for 3+ consecutive bars
    sticky_mask  = (K >= 80).astype(int)
    sticky_3     = sticky_mask.rolling(3, min_periods=3).sum()
    sticky_trend = sticky_3 >= 3

    out = pd.DataFrame(index=df.index)
    out['kd_k']                = K.values
    out['kd_d']                = D.values
    out['kd_low_golden_cross']  = (golden & (K < 25) & (D < 25)).values
    out['kd_high_death_cross']  = (death  & (K > 75) & (D > 75)).values
    out['kd_mid_noise_cross']   = ((golden | death) & (K >= 25) & (K <= 75)).values
    out['kd_high_sticky_trend'] = sticky_trend.values
    return out


def _detect_bottom_reversal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect bottom reversal / breakdown-reversal patterns for all rows.

    Signal date = confirmation day (one day after reversal candle).
    No look-ahead: uses only data available at each point.

    Criteria (simplified for vectorized detection):
      bottom_reversal_detected:
        - Price declined >= 20% from recent 60-bar high (previous day)
        - Today: close > prior close (recovery)
        - Today: low > prior low (higher low)
        - Today: volume >= 0.8x 20-day average (not volume collapse)
      is_speculative_rebound:
        - Same decline threshold but weaker confirmation
        (recovery close without full volume + higher-low confirmation)
    """
    close  = df['close'].astype(float)
    low    = df['low'].astype(float)   if 'low'    in df.columns else close
    high   = df['high'].astype(float)  if 'high'   in df.columns else close
    volume = df['volume'].astype(float) if 'volume' in df.columns else pd.Series(
        np.ones(len(df)), index=df.index)

    # Recent high (60-bar rolling, backwards-looking)
    recent_high = high.rolling(60, min_periods=20).max()
    decline_pct = (close - recent_high) / recent_high.replace(0, np.nan)  # negative

    # Conditions checked on PREVIOUS day (shift=1) to avoid look-ahead
    deep_decline_prev  = (decline_pct.shift(1) <= -0.20)
    recovery_close     = close > close.shift(1)
    higher_low         = low > low.shift(1)
    avg_vol_20         = volume.rolling(20, min_periods=5).mean()
    vol_confirm        = volume >= avg_vol_20 * 0.8

    # Confirmed bottom reversal
    confirmed = deep_decline_prev & recovery_close & higher_low & vol_confirm
    # Speculative: decline + recovery but weaker signals
    speculative = deep_decline_prev & recovery_close & ~(higher_low & vol_confirm)

    out = pd.DataFrame(index=df.index)
    out['bottom_reversal_detected'] = confirmed.fillna(False).values
    out['is_speculative_rebound']   = speculative.fillna(False).values
    return out


def _detect_short_interest_proxy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Proxy short interest signals derived from price and volume only.

    When margin_df is unavailable, we use price/volume proxies.

    price_up_short_balance_up_proxy:
        price rose 3%+ in 3 days while volume was above average → potential squeeze
    limit_up_proxy:
        single-day gain > 6.9% (Taiwan limit-up threshold)
    weak_stock_signal_proxy:
        price below 20-day SMA with volume declining
    """
    close  = df['close'].astype(float)
    volume = df['volume'].astype(float) if 'volume' in df.columns else pd.Series(
        np.ones(len(df)), index=df.index)

    ret_3d     = close.pct_change(3).fillna(0)
    ret_1d     = close.pct_change(1).fillna(0)
    avg_vol_20 = volume.rolling(20, min_periods=5).mean().replace(0, np.nan)
    sma_20     = close.rolling(20, min_periods=5).mean()
    above_avg  = volume > avg_vol_20

    out = pd.DataFrame(index=df.index)
    out['short_squeeze_fuel_score']     = np.where(
        (ret_3d > 0.03) & above_avg, np.clip(ret_3d * 10, 0, 1.0), 0.0)
    out['price_up_short_balance_up']    = ((ret_3d > 0.03) & above_avg).values
    out['limit_up_short_balance_up']    = (ret_1d >= 0.069).values
    out['weak_stock_short_increase']    = (
        (close < sma_20) & (volume < avg_vol_20 * 0.8)).fillna(False).values
    return out


# ---------------------------------------------------------------------------
# Main backtest class
# ---------------------------------------------------------------------------

class StrategyKnowledgeBacktester:
    """
    Backtester for Strategy Knowledge Engine Phase 2 modules.

    Parameters
    ----------
    mode          : 'real' or 'mock'
    start         : optional start date string 'YYYY-MM-DD'
    end           : optional end date string 'YYYY-MM-DD'
    stock         : optional single symbol to backtest
    holding_days  : forward return window (default 20)
    min_samples   : minimum signals required for OBSERVATIONAL/RELIABLE rating
    output_dir    : CSV output directory
    strict_real_mode : True → real mode never falls back to mock
    """

    def __init__(
        self,
        mode: str = 'real',
        start: str = None,
        end: str = None,
        stock: str = None,
        holding_days: int = 20,
        min_samples: int = 30,
        output_dir: str = None,
        strict_real_mode: bool = True,
    ):
        self.mode             = mode
        self.start            = start
        self.end              = end
        self.stock            = stock
        self.holding_days     = holding_days
        self.min_samples      = min_samples
        self.output_dir       = output_dir or _DEFAULT_OUTPUT_DIR
        self.strict_real_mode = strict_real_mode
        self._is_sample       = False
        self._data_source     = 'unknown'

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_universe(self) -> list:
        """Return list of symbols to backtest."""
        if self.mode == 'mock':
            return ['SIM_A', 'SIM_B', 'SIM_C']
        if self.stock:
            return [str(self.stock)]
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, is_sample = _resolve_csv('profile')
            if not path:
                logger.warning("StrategyKnowledgeBacktester: no profile CSV found")
                return []
            rows = _read_csv_rows(path)
            self._is_sample   = is_sample
            self._data_source = path
            return [r['symbol'] for r in rows if r.get('symbol')]
        except Exception as exc:
            logger.warning("_load_universe: %s", exc)
            return []

    def _load_daily_df(self, symbol: str) -> pd.DataFrame:
        """Load and filter daily K data for one symbol."""
        if self.mode == 'mock':
            df = _generate_mock_df(symbol, seed=hash(symbol) % 100)
            if self.start:
                df = df[df['date'] >= self.start]
            if self.end:
                df = df[df['date'] <= self.end]
            return df.reset_index(drop=True)

        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, _ = _resolve_csv('daily')
            if not path:
                return pd.DataFrame()
            rows = [r for r in _read_csv_rows(path) if str(r.get('symbol', '')) == str(symbol)]
            if not rows:
                return pd.DataFrame()
            df = pd.DataFrame(rows)
            for col in ['open', 'high', 'low', 'close', 'volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna(subset=['close']).sort_values('date').reset_index(drop=True)
            if self.start:
                df = df[df['date'] >= self.start]
            if self.end:
                df = df[df['date'] <= self.end]
            return df
        except Exception as exc:
            logger.warning("_load_daily_df %s: %s", symbol, exc)
            return pd.DataFrame()

    # ------------------------------------------------------------------
    # Per-symbol backtest
    # ------------------------------------------------------------------

    def backtest_symbol(
        self,
        symbol: str,
        daily_df: pd.DataFrame,
        context: dict,
    ) -> list:
        """
        Compute all strategy signals for each day in daily_df using
        vectorized, backward-looking signal detection.

        For each day with sufficient history (>= _MIN_BARS bars), records:
          - KD signals
          - Short interest proxy signals
          - Bottom reversal signals
          - Forward returns (intentional look-ahead, labels only)
          - Max drawdown / runup after signal

        Parameters
        ----------
        symbol    : stock symbol string
        daily_df  : daily OHLCV DataFrame, sorted ascending
        context   : optional dict with 'margin_df' etc. (may be empty)

        Returns
        -------
        list of dicts, one per qualifying day
        """
        if len(daily_df) < _MIN_BARS:
            return []

        # Detect signals on full series (vectorized, no look-ahead)
        kd_df  = _detect_kd_signals(daily_df)
        br_df  = _detect_bottom_reversal(daily_df)
        si_df  = _detect_short_interest_proxy(daily_df)

        closes = daily_df['close'].values.astype(float)
        dates  = (daily_df['date'].values
                  if 'date' in daily_df.columns
                  else [str(i) for i in range(len(daily_df))])

        n     = len(daily_df)
        hd    = self.holding_days
        records = []

        for i in range(_MIN_BARS - 1, n):
            close = closes[i]
            date  = dates[i]

            # Forward returns (labels — intentional look-ahead)
            fwd_5, fwd_10, fwd_20, fwd_n = None, None, None, None
            max_dd, max_ru = None, None

            if close > 0:
                if i + 5  < n: fwd_5  = (closes[i + 5]  - close) / close * 100.0
                if i + 10 < n: fwd_10 = (closes[i + 10] - close) / close * 100.0
                if i + 20 < n: fwd_20 = (closes[i + 20] - close) / close * 100.0
                if i + hd < n:
                    fwd_n  = (closes[i + hd] - close) / close * 100.0
                    window_fut = closes[i:i + hd + 1]
                    max_dd = float((np.nanmin(window_fut) - close) / close * 100.0)
                    max_ru = float((np.nanmax(window_fut) - close) / close * 100.0)

            # Build the record
            rec = {
                'symbol': symbol,
                'date':   date,
                'close':  close,
                # KD
                'kd_k':                   float(kd_df['kd_k'].iat[i]),
                'kd_d':                   float(kd_df['kd_d'].iat[i]),
                'kd_low_golden_cross':    bool(kd_df['kd_low_golden_cross'].iat[i]),
                'kd_high_death_cross':    bool(kd_df['kd_high_death_cross'].iat[i]),
                'kd_mid_noise_cross':     bool(kd_df['kd_mid_noise_cross'].iat[i]),
                'kd_high_sticky_trend':   bool(kd_df['kd_high_sticky_trend'].iat[i]),
                # Short interest proxy
                'short_squeeze_fuel_score':    float(si_df['short_squeeze_fuel_score'].iat[i]),
                'price_up_short_balance_up':   bool(si_df['price_up_short_balance_up'].iat[i]),
                'limit_up_short_balance_up':   bool(si_df['limit_up_short_balance_up'].iat[i]),
                'weak_stock_short_increase':   bool(si_df['weak_stock_short_increase'].iat[i]),
                # Bottom reversal
                'bottom_reversal_detected':    bool(br_df['bottom_reversal_detected'].iat[i]),
                'is_speculative_rebound':      bool(br_df['is_speculative_rebound'].iat[i]),
                # Forward returns (labels)
                'forward_return_5d':   fwd_5,
                'forward_return_10d':  fwd_10,
                'forward_return_20d':  fwd_20,
                f'forward_return_{hd}d': fwd_n,
                'max_drawdown_after_signal': max_dd,
                'max_runup_after_signal':    max_ru,
            }
            records.append(rec)

        return records

    def evaluate_signal_forward_return(
        self,
        df: pd.DataFrame,
        signal_col: str,
        holding_days: int = 20,
    ) -> dict:
        """Evaluate a binary signal column against the N-day forward return."""
        fwd_col = f'forward_return_{holding_days}d'
        return evaluate_binary_signal(
            df, signal_col, fwd_col,
            min_samples=self.min_samples,
            holding_days=holding_days,
        )

    # ------------------------------------------------------------------
    # Aggregation and evaluation
    # ------------------------------------------------------------------

    def _build_module_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Evaluate all signal columns and build a module performance table."""
        hd      = self.holding_days
        fwd_col = f'forward_return_{hd}d'
        rows    = []

        signals_to_eval = [
            # (signal_col, module_name, signal_label)
            ('kd_low_golden_cross',      'KD Advanced',      'kd_low_golden_cross (buy)'),
            ('kd_high_death_cross',      'KD Advanced',      'kd_high_death_cross (sell/no-chase)'),
            ('kd_mid_noise_cross',       'KD Advanced',      'kd_mid_noise_cross (noise)'),
            ('kd_high_sticky_trend',     'KD Advanced',      'kd_high_sticky_trend (hold)'),
            ('price_up_short_balance_up', 'Short Interest',  'price_up_short_balance_up (proxy)'),
            ('limit_up_short_balance_up', 'Short Interest',  'limit_up_short_balance_up (proxy)'),
            ('weak_stock_short_increase', 'Short Interest',  'weak_stock_short_increase (risk)'),
            ('bottom_reversal_detected', 'Bottom Reversal',  'bottom_reversal_detected'),
            ('is_speculative_rebound',   'Bottom Reversal',  'is_speculative_rebound'),
        ]

        for sig_col, module, label in signals_to_eval:
            stats = evaluate_binary_signal(
                df, sig_col, fwd_col,
                min_samples=self.min_samples,
                holding_days=hd,
            )
            rows.append({
                'module':        module,
                'signal':        label,
                'sample_count':  stats.get('sample_count', 0),
                'win_rate':      stats.get('win_rate'),
                'avg_return':    stats.get('avg_return'),
                'median_return': stats.get('median_return'),
                'profit_factor': stats.get('profit_factor'),
                'avg_max_drawdown': stats.get('avg_max_drawdown'),
                'avg_max_runup':    stats.get('avg_max_runup'),
                'confidence':    stats.get('confidence', 'INSUFFICIENT'),
            })

        # Short interest bucket analysis
        si_buckets = evaluate_bucket_signal(
            df, 'short_squeeze_fuel_score', fwd_col,
            buckets=[
                ('low  [0, 0.3)',    0.0,  0.3),
                ('mid  [0.3, 0.6)',  0.3,  0.6),
                ('high [0.6, 1.0+)', 0.6,  float('inf')),
            ],
            min_samples=self.min_samples,
        )
        for bkt in si_buckets:
            rows.append({
                'module':        'Short Interest',
                'signal':        f"squeeze_fuel {bkt.get('bucket', '')}",
                'sample_count':  bkt.get('sample_count', 0),
                'win_rate':      bkt.get('win_rate'),
                'avg_return':    bkt.get('avg_return'),
                'median_return': bkt.get('median_return'),
                'profit_factor': bkt.get('profit_factor'),
                'avg_max_drawdown': None,
                'avg_max_runup':    None,
                'confidence':    bkt.get('confidence', 'INSUFFICIENT'),
            })

        return pd.DataFrame(rows)

    def _build_filter_comparison(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare forward returns for:
          - All rows (baseline)
          - Rows filtered by no-chase warnings (kd_high_death_cross)
          - Rows with weak short increase removed
          - Rows with bottom reversal signal
        """
        hd      = self.holding_days
        fwd_col = f'forward_return_{hd}d'
        if fwd_col not in df.columns:
            return pd.DataFrame()

        def _stats_row(label, sub_df, note=''):
            returns = sub_df[fwd_col].dropna()
            n       = int(len(returns))
            conf    = _sc.evaluate_bucket(n)['level']
            if n > 0:
                wins = int((returns > 0).sum())
                wr   = round(float(wins / n * 100.0), 2)
                avg  = round(float(returns.mean()), 3)
                pf   = calculate_profit_factor(returns)
                pf_s = 'INF' if pf == float('inf') else round(pf, 3)
                dd_col = 'max_drawdown_after_signal'
                dd = round(float(sub_df[dd_col].dropna().mean()), 3) if dd_col in sub_df.columns and not sub_df[dd_col].dropna().empty else None
            else:
                wr, avg, pf_s, dd = None, None, None, None
            return {
                'filter_name':    label,
                'signal_count':   n,
                'avg_return_20d': avg,
                'win_rate_20d':   wr,
                'profit_factor':  pf_s,
                'max_drawdown_avg': dd,
                'confidence':     conf,
                'note':           note,
            }

        rows = []

        # Baseline: all rows with forward return available
        rows.append(_stats_row('All rows (baseline)', df))

        # Remove rows with KD high death cross (no-chase filter)
        if 'kd_high_death_cross' in df.columns:
            filtered = df[df['kd_high_death_cross'] != True]
            rows.append(_stats_row(
                'Remove kd_high_death_cross',
                filtered,
                note='no-chase: KD death cross removed',
            ))

        # Remove rows with weak short increase (risk filter)
        if 'weak_stock_short_increase' in df.columns:
            filtered = df[df['weak_stock_short_increase'] != True]
            rows.append(_stats_row(
                'Remove weak_stock_short_increase',
                filtered,
                note='risk filter: weak-stock short removed',
            ))

        # Only rows with bottom reversal
        if 'bottom_reversal_detected' in df.columns:
            sub = df[df['bottom_reversal_detected'] == True]
            rows.append(_stats_row(
                'Bottom reversal only',
                sub,
                note='rebound strategy subset',
            ))

        # Only rows with KD golden cross
        if 'kd_low_golden_cross' in df.columns:
            sub = df[df['kd_low_golden_cross'] == True]
            rows.append(_stats_row(
                'KD low golden cross only',
                sub,
                note='KD buy signal subset',
            ))

        return pd.DataFrame(rows)

    def _build_no_chase_validation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate the no-chase rule (kd_high_death_cross as proxy)."""
        hd      = self.holding_days
        fwd_col = f'forward_return_{hd}d'
        rows    = []
        for sig_col, label in [
            ('kd_high_death_cross',    'kd_high_death_cross (no-chase proxy)'),
            ('weak_stock_short_increase', 'weak_stock_short_increase (risk proxy)'),
        ]:
            res = evaluate_warning_filter(df, sig_col, fwd_col, min_samples=self.min_samples)
            for cond, d in [('with_warning', res['with_warning']),
                            ('without_warning', res['without_warning'])]:
                rows.append({
                    'signal':        label,
                    'condition':     cond,
                    'sample_count':  d.get('sample_count', 0),
                    'win_rate':      d.get('win_rate'),
                    'avg_return':    d.get('avg_return'),
                    'profit_factor': d.get('profit_factor'),
                    'confidence':    d.get('confidence', 'INSUFFICIENT'),
                })
        return pd.DataFrame(rows)

    def _build_rebound_validation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate bottom reversal signal forward returns."""
        hd      = self.holding_days
        fwd_col = f'forward_return_{hd}d'
        rows    = []
        for sig_col, label in [
            ('bottom_reversal_detected', 'Bottom Reversal Confirmed'),
            ('is_speculative_rebound',   'Speculative Rebound'),
        ]:
            stats = evaluate_binary_signal(
                df, sig_col, fwd_col,
                min_samples=self.min_samples,
                holding_days=hd,
            )
            rows.append({
                'signal':        label,
                'sample_count':  stats.get('sample_count', 0),
                'win_rate':      stats.get('win_rate'),
                'avg_return':    stats.get('avg_return'),
                'profit_factor': stats.get('profit_factor'),
                'avg_max_drawdown': stats.get('avg_max_drawdown'),
                'avg_max_runup':    stats.get('avg_max_runup'),
                'confidence':    stats.get('confidence', 'INSUFFICIENT'),
            })
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Run the full Strategy Knowledge backtest.

        Returns
        -------
        dict with keys:
            mode, status, data_source, is_sample, is_mock_demo,
            n_symbols, n_records, n_signals, start, end, holding_days,
            confidence, signals_df, module_performance, filter_comparison,
            no_chase_validation, rebound_validation,
            sector_validation (empty — no peer data),
            fundamental_guard_validation (empty — no fundamental time-series),
            module_summary
        """
        is_mock_demo = (self.mode == 'mock')
        logger.info(
            "StrategyKnowledgeBacktester.run [mode=%s stock=%s start=%s end=%s hd=%d]",
            self.mode, self.stock, self.start, self.end, self.holding_days,
        )

        symbols = self._load_universe()
        if not symbols:
            return {
                'mode': self.mode,
                'status': 'insufficient_data',
                'message': f'[WARN] No symbols loaded (mode={self.mode}). '
                           'Import data or use --mode mock.',
                'is_mock_demo': is_mock_demo,
                'n_symbols': 0,
                'n_records': 0,
                'n_signals': 0,
            }

        all_records = []
        processed_symbols = []
        skipped_symbols   = []

        for symbol in symbols:
            daily_df = self._load_daily_df(symbol)
            if len(daily_df) < _MIN_BARS:
                logger.info("Skipping %s: only %d bars", symbol, len(daily_df))
                skipped_symbols.append(symbol)
                continue
            try:
                recs = self.backtest_symbol(symbol, daily_df, context={})
                if recs:
                    all_records.extend(recs)
                    processed_symbols.append(symbol)
                    logger.info("  %s: %d records", symbol, len(recs))
            except Exception as exc:
                logger.warning("backtest_symbol %s failed: %s", symbol, exc)
                skipped_symbols.append(symbol)

        if not all_records:
            return {
                'mode': self.mode,
                'status': 'insufficient_data',
                'message': '[WARN] No signal records produced. '
                           'Symbols may have insufficient data.',
                'is_mock_demo': is_mock_demo,
                'n_symbols': 0,
                'n_records': 0,
                'n_signals': 0,
            }

        # Build signals DataFrame
        df = pd.DataFrame(all_records)

        # Determine period
        start_actual = str(df['date'].min()) if 'date' in df.columns else self.start or '—'
        end_actual   = str(df['date'].max()) if 'date' in df.columns else self.end   or '—'

        # Count trading days
        try:
            dates = pd.to_datetime(df['date']).sort_values().unique()
            trading_days = int(len(dates))
        except Exception:
            trading_days = len(df)

        # Count total signals (rows with any True signal)
        signal_cols = [
            'kd_low_golden_cross', 'kd_high_death_cross', 'kd_high_sticky_trend',
            'price_up_short_balance_up', 'limit_up_short_balance_up',
            'bottom_reversal_detected', 'is_speculative_rebound',
        ]
        existing_sig_cols = [c for c in signal_cols if c in df.columns]
        if existing_sig_cols:
            n_signals = int(df[existing_sig_cols].any(axis=1).sum())
        else:
            n_signals = 0

        # Statistical confidence
        confidence = _sc.for_strategy_module(
            symbol_count=len(processed_symbols),
            signal_count=n_signals,
            trading_days=trading_days,
        )
        universe_conf = _sc.evaluate_universe(len(processed_symbols))

        # Build evaluation tables
        module_perf    = self._build_module_performance(df)
        filter_comp    = self._build_filter_comparison(df)
        no_chase_valid = self._build_no_chase_validation(df)
        rebound_valid  = self._build_rebound_validation(df)

        # Module summary for console
        def _mod_summary(module_name, sig_col):
            sub = module_perf[module_perf['module'] == module_name]
            if sub.empty:
                return 'N/A'
            total = sub['sample_count'].sum()
            best  = sub.dropna(subset=['avg_return'])
            if best.empty:
                return f'signals={total}, INSUFFICIENT'
            top = best.sort_values('avg_return', ascending=False).iloc[0]
            conf = top.get('confidence', 'INSUFFICIENT')
            avg  = top.get('avg_return')
            avg_s = f"{avg:+.2f}%" if avg is not None else '—'
            return f"signals={total}, best_avg={avg_s}, {conf}"

        module_summary = {
            'KD Advanced':        _mod_summary('KD Advanced',      'kd_low_golden_cross'),
            'Short Interest':     _mod_summary('Short Interest',   'price_up_short_balance_up'),
            'Bottom Reversal':    _mod_summary('Bottom Reversal',  'bottom_reversal_detected'),
            'Sector Rotation':    'UNAVAILABLE — no peer data',
            'Fundamental Quality': 'UNAVAILABLE — no fundamental time-series',
            'No Chase / No Panic Sell': (
                'see no_chase_validation table'
            ),
        }

        return {
            'mode':              self.mode,
            'status':            'ok',
            'is_mock_demo':      is_mock_demo,
            'data_source':       self._data_source,
            'is_sample':         self._is_sample,
            'n_symbols':         len(processed_symbols),
            'n_records':         len(df),
            'n_signals':         n_signals,
            'trading_days':      trading_days,
            'start':             start_actual,
            'end':               end_actual,
            'holding_days':      self.holding_days,
            'confidence':        confidence,
            'universe_confidence': universe_conf,
            'processed_symbols': processed_symbols,
            'skipped_symbols':   skipped_symbols,
            'signals_df':        df,
            'module_performance':       module_perf,
            'filter_comparison':        filter_comp,
            'no_chase_validation':      no_chase_valid,
            'rebound_validation':       rebound_valid,
            'sector_validation':        pd.DataFrame(),  # requires peer data
            'fundamental_guard_validation': pd.DataFrame(),  # requires time-series data
            'module_summary':    module_summary,
        }

    # ------------------------------------------------------------------
    # CSV export
    # ------------------------------------------------------------------

    def save_results(self, results: dict, output_dir: str = None) -> dict:
        """
        Save backtest results to CSV files.

        Returns dict mapping result_name → file_path.
        """
        out_dir = output_dir or self.output_dir
        os.makedirs(out_dir, exist_ok=True)
        paths = {}

        csv_map = [
            ('signals_df',                   'strategy_knowledge_signals.csv'),
            ('module_performance',           'strategy_knowledge_module_performance.csv'),
            ('filter_comparison',            'strategy_knowledge_factor_performance.csv'),
            ('no_chase_validation',          'strategy_knowledge_no_chase_validation.csv'),
            ('rebound_validation',           'strategy_knowledge_rebound_validation.csv'),
            ('sector_validation',            'strategy_knowledge_sector_validation.csv'),
            ('fundamental_guard_validation', 'strategy_knowledge_fundamental_guard_validation.csv'),
        ]
        # Also save filter_comparison under the no_panic_sell name
        csv_map.append(('filter_comparison', 'strategy_knowledge_no_panic_sell_validation.csv'))

        for key, filename in csv_map:
            df = results.get(key)
            if df is not None and isinstance(df, pd.DataFrame):
                fpath = os.path.join(out_dir, filename)
                try:
                    df.to_csv(fpath, index=False, encoding='utf-8-sig')
                    paths[key] = fpath
                    logger.info("Saved %s → %s", key, fpath)
                except Exception as exc:
                    logger.warning("Could not save %s: %s", filename, exc)

        return paths
