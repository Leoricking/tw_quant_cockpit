"""
backtest/score_validation.py - Score effectiveness validation engine.

Validates bull_stock_score sub-components against historical forward returns.
All rolling computations use strictly backward-looking windows (no look-ahead bias).
Forward returns are labels only — look-ahead is intentional for labelling.

Usage:
    from backtest.score_validation import ScoreValidator
    sv = ScoreValidator(mode='real', start='2024-01-01', end='2026-05-01')
    results = sv.run()
    paths = sv.save_results(results)
"""

import os
import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(_BASE_DIR, 'data', 'backtest_results')


class ScoreValidator:
    """
    Core score/factor validation engine.

    Builds per-(symbol, date) records with rolling technical features and
    forward-return labels, then computes:
      - score bucket performance statistics
      - factor correlation with forward returns
      - no-entry condition effectiveness
      - trust-cost support validation
      - margin risk validation
    """

    MIN_BARS = 25   # minimum bars to include a symbol

    def __init__(self, mode: str = 'real', start: str = None, end: str = None, top_n: int = 8):
        self.mode    = mode
        self.start   = start
        self.end     = end
        self.top_n   = top_n
        self._is_sample  = False
        self._data_source = 'unknown'

    # ------------------------------------------------------------------
    # Data loading helpers
    # ------------------------------------------------------------------

    def load_universe(self) -> list:
        """Return symbol list from profile CSV."""
        try:
            from data.real_data_loader import _resolve_csv, _read_csv_rows
            path, is_sample = _resolve_csv('profile')
            if not path:
                logger.warning("ScoreValidator: no profile CSV found")
                return []
            rows = _read_csv_rows(path)
            self._is_sample  = is_sample
            self._data_source = path
            return [r['symbol'] for r in rows if r.get('symbol')]
        except Exception as exc:
            logger.error("ScoreValidator.load_universe: %s", exc)
            return []

    def _load_daily_df(self, symbol: str) -> pd.DataFrame:
        """Load all daily K rows for a symbol into a sorted DataFrame."""
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
            logger.warning("ScoreValidator._load_daily_df %s: %s", symbol, exc)
            return pd.DataFrame()

    # ------------------------------------------------------------------
    # Rolling feature builder (no look-ahead for indicators)
    # ------------------------------------------------------------------

    def _add_rolling_features(
        self, df: pd.DataFrame, symbol: str,
        profile: dict = None, inst: dict = None, margin: dict = None,
        revenue: dict = None, holder: dict = None, trust: dict = None,
    ) -> pd.DataFrame:
        """
        Compute rolling technical indicators and static factor scores.

        Indicators use only past/current data (backward-looking rolling windows).
        Forward returns are computed as labels — intentional look-ahead.
        """
        df = df.copy()
        c  = df['close']
        v  = df.get('volume', pd.Series(0.0, index=df.index))
        h  = df.get('high',   c)
        lo = df.get('low',    c)

        # ---- MAs (backward-looking, no look-ahead) ----
        df['ma5']   = c.rolling(5,  min_periods=5).mean()
        df['ma10']  = c.rolling(10, min_periods=10).mean()
        df['ma20']  = c.rolling(20, min_periods=20).mean()
        df['ma60']  = c.rolling(60, min_periods=60).mean()
        df['vol20'] = v.rolling(20, min_periods=10).mean()

        above_ma5  = df['ma5'].notna()  & (c > df['ma5'])
        above_ma10 = df['ma10'].notna() & (c > df['ma10'])
        above_ma20 = df['ma20'].notna() & (c > df['ma20'])
        above_ma60 = df['ma60'].notna() & (c > df['ma60'])

        # ---- trend_score (0-15) ----
        ts = pd.Series(3.0, index=df.index)
        ts = ts.where(~above_ma20, 6.0)
        ts = ts.where(~(above_ma10 & above_ma20), 9.0)
        ts = ts.where(~(above_ma5 & above_ma10 & above_ma20), 12.0)
        ts = ts.where(~(above_ma5 & above_ma10 & above_ma20 & above_ma60), 15.0)
        ts = ts.where(df['ma20'].notna(), np.nan)          # NaN until 20 bars available
        df['trend_score'] = ts

        # ---- breakout_volume_score (0-15) ----
        vol_ratio = v / df['vol20'].clip(lower=1.0)
        df['vol_ratio'] = vol_ratio
        df['breakout_volume_score'] = np.where(
            vol_ratio >= 2.0, 15.0, np.where(
            vol_ratio >= 1.5, 10.0, np.where(
            vol_ratio >= 1.0,  7.0,  3.0)))

        # ---- Static factor scores (most-recent values used as proxies) ----
        # theme_score (0-20)
        theme = 0.0
        if profile:
            if profile.get('is_mainstream_theme'):
                theme += 12.0
            theme += min(8.0, len(profile.get('theme_tags', [])) * 2.0)
        df['theme_score'] = round(min(20.0, theme), 2)

        # fundamental_score (0-15)
        fs = 4.0
        if revenue:
            yoy     = revenue.get('latest_revenue_yoy', 0.0)
            acc_yoy = revenue.get('accumulated_revenue_yoy', 0.0)
            fs = max(0.0, min(15.0,
                (6.0 if yoy >= 50 else 5.0 if yoy >= 30 else 3.0 if yoy >= 20
                 else 1.5 if yoy >= 10 else -2.0 if yoy < 0 else 0.0) +
                (4.0 if acc_yoy >= 30 else 3.0 if acc_yoy >= 20
                 else 1.5 if acc_yoy >= 10 else 0.0)
            ))
        df['fundamental_score'] = round(fs, 2)

        # institution_score (0-15)
        ins = 0.0
        if inst:
            t3 = inst.get('trust_net_3d', 0)
            f5 = inst.get('foreign_net_5d', 0)
            ins = min(15.0, max(0.0,
                (8.0 if t3 > 1000 else 4.0 if t3 > 0 else 0.0) +
                (5.0 if f5 > 0 else -3.0 if f5 < -5000 else 0.0)
            ))
        df['institution_score'] = round(ins, 2)

        # holder_score (0-10)
        hs = 5.0
        if holder:
            mc = holder.get('major_change', 0.0)
            rc = holder.get('retail_change', 0.0)
            hs = 10.0 if (mc > 0 and rc < 0) else 7.0 if mc > 0 else 2.0 if mc < 0 else 5.0
        df['holder_score'] = round(min(10.0, hs), 2)

        # margin_score (0-5)
        ms = 3.0
        if margin:
            if margin.get('margin_overheat_risk'):
                ms = 0.0
            elif margin.get('margin_increase_pct', 0.0) > 5:
                ms = 1.0
            elif margin.get('margin_increase_pct', 0.0) < 0:
                ms = 5.0
        df['margin_score'] = round(min(5.0, ms), 2)

        # overheat_score (0-5) — rolling price momentum proxy (no look-ahead)
        roc5 = (c - c.shift(5)) / c.shift(5).clip(lower=0.01) * 100
        df['overheat_score'] = np.where(
            roc5 > 15, 1.0, np.where(
            roc5 > 10, 2.0, np.where(
            roc5 >  5, 3.0, np.where(
            roc5 >  0, 4.0,  5.0))))

        # trust_cost_score (bonus 0-5)
        tcs = 0.0
        if trust:
            pct = trust.get('price_vs_trust_cost_pct', 99.0)
            tcs = 3.0 if -2 <= pct <= 5 else (1.0 if pct > 5 else 0.0)
        df['trust_cost_score'] = round(tcs, 2)

        # ---- Combined proxy score (0-100) ----
        df['bull_stock_score'] = (
            df['theme_score'] + df['fundamental_score'] +
            df['trend_score'].fillna(0) + df['breakout_volume_score'] +
            df['institution_score'] + df['holder_score'] +
            df['margin_score'] + df['overheat_score'] + df['trust_cost_score']
        ).clip(0, 100).round(1)

        # ---- Score bucket ----
        df['score_bucket'] = pd.cut(
            df['bull_stock_score'],
            bins=[-0.1, 50, 65, 80, 101],
            labels=['<50', '50-64', '65-79', '80-100'],
        )

        # ---- No-entry condition flags (rolling, no look-ahead) ----
        prev_c   = c.shift(1)
        df['prev_close'] = prev_c
        df['daily_chg_pct'] = (c - prev_c) / prev_c.clip(lower=0.01) * 100
        wick_range = (h - lo).clip(lower=0.01)
        df['upper_wick_pct'] = (h - c) / wick_range

        df['no_entry_below_ma20']       = (df['ma20'].notna()) & (c < df['ma20'])
        df['no_entry_early_surge']      = df['daily_chg_pct'] > 5.0
        df['no_entry_long_upper_wick']  = df['upper_wick_pct'] > 0.6
        df['no_entry_break_ma10_vol']   = (df['ma10'].notna()) & (c < df['ma10']) & (vol_ratio > 1.2)
        df['no_entry_heavy_selling']    = (inst.get('institution_continuous_sell_days', 0) >= 3) if inst else False
        df['no_entry_margin_overheat']  = margin.get('margin_overheat_risk', False) if margin else False
        trust_pct = trust.get('price_vs_trust_cost_pct', 99.0) if trust else 99.0
        df['no_entry_trust_cost_broken']= trust_pct < -3.0

        # ---- Buy point detection (rolling, no look-ahead) ----
        prev20_high = h.rolling(20, min_periods=20).max().shift(1)
        ma10_dist   = (c - df['ma10']).abs() / df['ma10'].clip(lower=0.01)
        ma5_dist    = (c - df['ma5']).abs() / df['ma5'].clip(lower=0.01)

        is_a = df['ma10'].notna() & df['ma20'].notna() & (ma10_dist <= 0.02) & (c >= prev_c) & (c > df['ma20'])
        is_b = df['ma5'].notna()  & df['ma10'].notna() & (ma5_dist <= 0.015) & (c > df['ma10'])
        is_c = prev20_high.notna() & (c > prev20_high) & (vol_ratio >= 1.5)

        df['buy_point_type'] = 'NONE'
        df.loc[is_c, 'buy_point_type'] = 'C_PLATFORM_BREAKOUT'
        df.loc[is_b, 'buy_point_type'] = 'B_PULLBACK_MA5'
        df.loc[is_a, 'buy_point_type'] = 'A_PULLBACK_MA10'

        df['buy_point_grade'] = None
        df.loc[is_c, 'buy_point_grade'] = 'C'
        df.loc[is_b, 'buy_point_grade'] = 'B'
        df.loc[is_a, 'buy_point_grade'] = 'A'
        df['formal_allowed'] = df['ma20'].notna()

        # ---- Trust cost validation flags ----
        tc_avg = trust.get('trust_avg_cost_3d', None) if trust else None
        if tc_avg:
            df['price_above_trust_cost']    = c > tc_avg
            df['price_near_trust_cost']     = (-2.0 <= trust_pct <= 5.0)
            df['trust_cost_broken']         = trust_pct < -3.0
            df['trust_5d_net_buy_positive'] = (trust.get('trust_net_5d_buy', 0) > 0)
        else:
            for col in ['price_above_trust_cost', 'price_near_trust_cost',
                        'trust_cost_broken', 'trust_5d_net_buy_positive']:
                df[col] = False

        # ---- Margin risk flags ----
        if margin:
            inc_pct = margin.get('margin_increase_pct', 0.0)
            m5d     = margin.get('margin_5d_change', 0)
            df['margin_5d_change_positive']    = m5d > 0
            df['margin_increase_pct_high']     = inc_pct > 10.0
            df['margin_overheat_risk_flag']    = margin.get('margin_overheat_risk', False)
            df['price_up_with_margin_surge']   = (c > prev_c) & (inc_pct > 10.0)
        else:
            for col in ['margin_5d_change_positive', 'margin_increase_pct_high',
                        'margin_overheat_risk_flag', 'price_up_with_margin_surge']:
                df[col] = False

        # ---- Forward return labels (intentional look-ahead — labels only) ----
        df['forward_return_5d']  = (c.shift(-5)  / c - 1).round(4)
        df['forward_return_10d'] = (c.shift(-10) / c - 1).round(4)
        df['forward_return_20d'] = (c.shift(-20) / c - 1).round(4)

        # Forward max drawdown: rolling(n).min().shift(-n) = min of next n bars
        df['max_drawdown_5d']  = (c.rolling(5).min().shift(-5)  / c - 1).round(4)
        df['max_drawdown_10d'] = (c.rolling(10).min().shift(-10) / c - 1).round(4)
        df['max_drawdown_20d'] = (c.rolling(20).min().shift(-20) / c - 1).round(4)

        df['hit_5d_3pct']        = df['forward_return_5d']  >= 0.03
        df['hit_10d_5pct']       = df['forward_return_10d'] >= 0.05
        df['hit_20d_8pct']       = df['forward_return_20d'] >= 0.08
        df['stop_loss_5pct_hit'] = df['max_drawdown_5d']    <= -0.05

        df['symbol'] = str(symbol)
        return df

    # ------------------------------------------------------------------
    # Records builder
    # ------------------------------------------------------------------

    def build_records(self) -> pd.DataFrame:
        """Build historical feature records for all universe symbols."""
        symbols = self.load_universe()
        if not symbols:
            return pd.DataFrame()

        from data.real_data_loader import RealDataLoader
        loader = RealDataLoader()

        all_dfs = []
        for sym in symbols:
            try:
                daily_df = self._load_daily_df(sym)
                if daily_df.empty or len(daily_df) < self.MIN_BARS:
                    continue

                if self.start:
                    daily_df = daily_df[daily_df['date'] >= self.start]
                if self.end:
                    daily_df = daily_df[daily_df['date'] <= self.end]
                if len(daily_df) < self.MIN_BARS:
                    continue

                profile = loader.load_profile(sym)         or {}
                inst    = loader.load_institutional(sym)
                margin  = loader.load_margin(sym)
                revenue = loader.load_monthly_revenue(sym)
                holder  = loader.load_holder(sym)
                trust   = loader.load_trust_cost(sym)

                enriched = self._add_rolling_features(
                    daily_df, sym,
                    profile=profile, inst=inst, margin=margin,
                    revenue=revenue, holder=holder, trust=trust,
                )
                enriched = enriched.dropna(subset=['ma20'])
                if not enriched.empty:
                    all_dfs.append(enriched)

            except Exception as exc:
                logger.warning("ScoreValidator: error processing %s — %s", sym, exc)

        if not all_dfs:
            return pd.DataFrame()
        return pd.concat(all_dfs, ignore_index=True)

    # ------------------------------------------------------------------
    # Statistics helpers
    # ------------------------------------------------------------------

    def bucket_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Score bucket → forward return statistics."""
        if df.empty or 'score_bucket' not in df.columns:
            return pd.DataFrame()

        rows = []
        for bucket in ['80-100', '65-79', '50-64', '<50']:
            sub = df[df['score_bucket'] == bucket]
            n   = len(sub)
            row = {'score_bucket': bucket, 'sample_count': n}

            for period, threshold in [('5d', 0.03), ('10d', 0.05), ('20d', 0.08)]:
                ret_col = f'forward_return_{period}'
                dd_col  = f'max_drawdown_{period}'
                hit_col = f'hit_{period}_{int(threshold*100)}pct'
                sub_p   = sub.dropna(subset=[ret_col])
                np_     = len(sub_p)

                row[f'avg_return_{period}']       = round(sub_p[ret_col].mean() * 100, 2)    if np_ >= 3  else None
                row[f'median_return_{period}']    = round(sub_p[ret_col].median() * 100, 2)  if np_ >= 3  else None
                row[f'win_rate_{period}']         = round((sub_p[ret_col] > 0).mean() * 100, 1) if np_ >= 3 else None
                row[f'avg_max_drawdown_{period}'] = round(sub_p[dd_col].mean() * 100, 2)     if np_ >= 3 and dd_col in sub_p.columns else None
                row[f'hit_rate_{period}_{int(threshold*100)}pct'] = round(sub_p[hit_col].mean() * 100, 1) if np_ >= 3 and hit_col in sub_p.columns else None

            sub5 = sub.dropna(subset=['stop_loss_5pct_hit'])
            row['stop_loss_5pct_rate'] = round(sub5['stop_loss_5pct_hit'].mean() * 100, 1) if len(sub5) >= 3 else None

            sub20 = sub.dropna(subset=['forward_return_20d'])
            if len(sub20) >= 10:
                gains  = sub20.loc[sub20['forward_return_20d'] > 0, 'forward_return_20d'].sum()
                losses = sub20.loc[sub20['forward_return_20d'] < 0, 'forward_return_20d'].abs().sum()
                row['profit_factor_20d'] = round(gains / losses, 2) if losses > 0 else None
            else:
                row['profit_factor_20d'] = None

            if n < 10:
                row['sample_note'] = '⚠ 樣本 < 10，不輸出結論'
            elif n < 30:
                row['sample_note'] = '⚠ 樣本不足 30，僅供觀察'
            else:
                row['sample_note'] = ''
            rows.append(row)

        return pd.DataFrame(rows)

    def factor_effectiveness(self, df: pd.DataFrame) -> pd.DataFrame:
        """Factor correlation with 5/10/20d forward returns."""
        if df.empty:
            return pd.DataFrame()

        factors = [
            'theme_score', 'fundamental_score', 'trend_score',
            'breakout_volume_score', 'institution_score', 'holder_score',
            'margin_score', 'overheat_score', 'trust_cost_score',
        ]
        rows = []
        for factor in factors:
            if factor not in df.columns:
                continue
            row = {'factor': factor}
            for period in ['5d', '10d', '20d']:
                ret_col = f'forward_return_{period}'
                valid   = df[[factor, ret_col]].dropna()
                if len(valid) >= 10:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        corr = valid[factor].corr(valid[ret_col])
                    row[f'correlation_with_{period}_return'] = round(float(corr), 3) if not pd.isna(corr) else None
                else:
                    row[f'correlation_with_{period}_return'] = None

            valid20 = df[[factor, 'forward_return_20d']].dropna()
            n20     = len(valid20)
            if n20 >= 20:
                q75 = valid20[factor].quantile(0.75)
                q25 = valid20[factor].quantile(0.25)
                row['top_quantile_avg_return_20d']    = round(valid20[valid20[factor] >= q75]['forward_return_20d'].mean() * 100, 2)
                row['bottom_quantile_avg_return_20d'] = round(valid20[valid20[factor] <= q25]['forward_return_20d'].mean() * 100, 2)
                corr = row.get('correlation_with_20d_return') or 0
                row['effectiveness_label'] = (
                    'insufficient_sample' if n20 < 30 else
                    'strong_positive' if corr >= 0.10 else
                    'weak_positive'   if corr >= 0.03 else
                    'negative'        if corr <= -0.10 else
                    'neutral'
                )
            else:
                row['top_quantile_avg_return_20d']    = None
                row['bottom_quantile_avg_return_20d'] = None
                row['effectiveness_label'] = 'insufficient_sample'
            rows.append(row)

        return pd.DataFrame(rows)

    def no_entry_effectiveness(self, df: pd.DataFrame) -> pd.DataFrame:
        """No-entry condition → subsequent return comparison."""
        if df.empty:
            return pd.DataFrame()

        conditions = {
            'early_surge_over_5_pct':      'no_entry_early_surge',
            'heavy_institutional_selling': 'no_entry_heavy_selling',
            'below_ma20':                  'no_entry_below_ma20',
            'long_upper_wick':             'no_entry_long_upper_wick',
            'break_ma10_with_volume':      'no_entry_break_ma10_vol',
            'margin_overheat':             'no_entry_margin_overheat',
            'trust_cost_broken':           'no_entry_trust_cost_broken',
        }
        base20 = df.dropna(subset=['forward_return_20d'])
        baseline = base20['forward_return_20d'].mean() if len(base20) > 0 else 0.0

        rows = []
        for cond_name, cond_col in conditions.items():
            if cond_col not in df.columns:
                continue
            sub   = df[df[cond_col] == True]
            sub20 = sub.dropna(subset=['forward_return_20d'])
            n     = len(sub20)
            row   = {'condition': cond_name, 'sample_count': n}

            if n >= 5:
                row['avg_return_5d']      = round(sub.dropna(subset=['forward_return_5d'])['forward_return_5d'].mean() * 100, 2)
                row['avg_return_10d']     = round(sub.dropna(subset=['forward_return_10d'])['forward_return_10d'].mean() * 100, 2)
                row['avg_return_20d']     = round(sub20['forward_return_20d'].mean() * 100, 2)
                row['win_rate_20d']       = round((sub20['forward_return_20d'] > 0).mean() * 100, 1)
                row['avg_drawdown_20d']   = round(sub20['max_drawdown_20d'].mean() * 100, 2) if 'max_drawdown_20d' in sub20.columns else None
                row['risk_reduction_effect'] = round((baseline - sub20['forward_return_20d'].mean()) * 100, 2)
                if n < 30:
                    row['recommendation'] = '⚠ 樣本不足，僅供觀察'
                elif row['avg_return_20d'] < -1.0:
                    row['recommendation'] = '建議保留'
                elif row['avg_return_20d'] > 3.0:
                    row['recommendation'] = '建議降權重'
                else:
                    row['recommendation'] = '建議觀察'
            else:
                for k in ['avg_return_5d', 'avg_return_10d', 'avg_return_20d',
                          'win_rate_20d', 'avg_drawdown_20d', 'risk_reduction_effect']:
                    row[k] = None
                row['recommendation'] = '⚠ 樣本不足'
            rows.append(row)

        return pd.DataFrame(rows)

    def trust_cost_validation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Trust cost condition → subsequent return statistics."""
        if df.empty:
            return pd.DataFrame()

        conditions = {
            'price_above_trust_cost':    'price_above_trust_cost',
            'price_near_trust_cost':     'price_near_trust_cost',
            'trust_cost_broken':         'trust_cost_broken',
            'trust_5d_net_buy_positive': 'trust_5d_net_buy_positive',
        }
        return self._condition_stats(df, conditions)

    def margin_risk_validation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Margin risk condition → subsequent return statistics."""
        if df.empty:
            return pd.DataFrame()

        conditions = {
            'margin_5d_change_positive': 'margin_5d_change_positive',
            'margin_increase_pct_high':  'margin_increase_pct_high',
            'margin_overheat_risk':      'margin_overheat_risk_flag',
            'price_up_with_margin_surge':'price_up_with_margin_surge',
        }
        return self._condition_stats(df, conditions)

    def _condition_stats(self, df: pd.DataFrame, conditions: dict) -> pd.DataFrame:
        """Generic condition → forward return statistics table."""
        rows = []
        for cond_name, cond_col in conditions.items():
            if cond_col not in df.columns:
                continue
            sub   = df[df[cond_col] == True]
            sub20 = sub.dropna(subset=['forward_return_20d'])
            n     = len(sub20)
            row   = {'condition': cond_name, 'sample_count': n}
            if n >= 5:
                row['avg_return_5d']    = round(sub.dropna(subset=['forward_return_5d'])['forward_return_5d'].mean() * 100, 2)
                row['avg_return_10d']   = round(sub.dropna(subset=['forward_return_10d'])['forward_return_10d'].mean() * 100, 2)
                row['avg_return_20d']   = round(sub20['forward_return_20d'].mean() * 100, 2)
                row['win_rate_20d']     = round((sub20['forward_return_20d'] > 0).mean() * 100, 1)
                row['avg_drawdown_20d'] = round(sub20['max_drawdown_20d'].mean() * 100, 2) if 'max_drawdown_20d' in sub20.columns else None
            else:
                for k in ['avg_return_5d', 'avg_return_10d', 'avg_return_20d', 'win_rate_20d', 'avg_drawdown_20d']:
                    row[k] = None
            rows.append(row)
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run full score validation. Returns dict with all results and DataFrames."""
        logger.info("ScoreValidator.run() [mode=%s start=%s end=%s]", self.mode, self.start, self.end)

        df = self.build_records()

        if df.empty:
            return {
                'status': 'insufficient_data',
                'message': '資料不足，無法完成可靠統計。',
                'raw_df': df,
            }

        n_sym     = df['symbol'].nunique() if 'symbol' in df.columns else 0
        n_records = len(df)

        if n_sym < 5:
            logger.warning("ScoreValidator: only %d symbols — 樣本不足", n_sym)

        return {
            'status': 'ok',
            'start': df['date'].min() if 'date' in df.columns else self.start,
            'end':   df['date'].max() if 'date' in df.columns else self.end,
            'n_symbols':  n_sym,
            'n_records':  n_records,
            'is_sample':  self._is_sample,
            'data_source': self._data_source,
            'raw_df':            df,
            'score_bucket_df':   self.bucket_performance(df),
            'factor_df':         self.factor_effectiveness(df),
            'no_entry_df':       self.no_entry_effectiveness(df),
            'trust_cost_df':     self.trust_cost_validation(df),
            'margin_df':         self.margin_risk_validation(df),
        }

    def save_results(self, results: dict, output_dir: str = None) -> dict:
        """Save all results to CSV files. Returns dict of output paths."""
        if output_dir is None:
            output_dir = _DEFAULT_OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        paths = {}

        raw_df = results.get('raw_df', pd.DataFrame())
        if not raw_df.empty:
            keep = [
                'date', 'symbol', 'bull_stock_score', 'score_bucket',
                'theme_score', 'fundamental_score', 'trend_score',
                'breakout_volume_score', 'institution_score', 'holder_score',
                'margin_score', 'overheat_score', 'trust_cost_score',
                'buy_point_grade', 'buy_point_type', 'formal_allowed',
                'close',
                'forward_return_5d', 'forward_return_10d', 'forward_return_20d',
                'max_drawdown_5d', 'max_drawdown_10d', 'max_drawdown_20d',
                'hit_5d_3pct', 'hit_10d_5pct', 'hit_20d_8pct', 'stop_loss_5pct_hit',
            ]
            cols = [c for c in keep if c in raw_df.columns]
            p = os.path.join(output_dir, 'score_validation_raw.csv')
            raw_df[cols].to_csv(p, index=False, encoding='utf-8-sig')
            paths['raw'] = p
            logger.info("Saved raw validation → %s", p)

        for key, filename in [
            ('score_bucket_df',  'score_bucket_performance.csv'),
            ('factor_df',        'factor_effectiveness.csv'),
            ('no_entry_df',      'no_entry_condition_performance.csv'),
            ('trust_cost_df',    'trust_cost_validation.csv'),
            ('margin_df',        'margin_risk_validation.csv'),
        ]:
            sub = results.get(key, pd.DataFrame())
            if sub is not None and not sub.empty:
                p = os.path.join(output_dir, filename)
                sub.to_csv(p, index=False, encoding='utf-8-sig')
                paths[key] = p
                logger.info("Saved %s → %s", key, p)

        return paths
