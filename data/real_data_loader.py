"""
data/real_data_loader.py - Real CSV data loader for TW Quant Cockpit.

Reads structured CSVs from data/import/ subdirectories and computes
derived metrics for scoring. No mock fallback — returns None when absent.

Directory layout:
    data/import/profile/            symbol,name,market,industry,theme_tags,is_mainstream_theme,sector
    data/import/daily/              date,symbol,open,high,low,close,volume
    data/import/institutional/      date,symbol,foreign_net_buy,trust_net_buy,dealer_net_buy
    data/import/margin/             date,symbol,margin_balance,margin_change,short_balance,short_change
    data/import/monthly_revenue/    month,symbol,revenue,mom,yoy,accumulated_yoy
    data/import/holder/             date,symbol,major_holder_ratio,retail_holder_ratio,major_change,retail_change
    data/import/trust_cost/         date,symbol,trust_buy_shares,trust_buy_amount,trust_avg_cost,close,price_vs_trust_cost_pct
"""

import os
import logging
import csv

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_IMPORT_DIR = os.path.join(_BASE_DIR, "import")

# Standard CSV filenames (created by import-csv command)
_STANDARD_FILES = {
    'profile':         'stock_profile.csv',
    'daily':           'daily_k.csv',
    'institutional':   'institutional.csv',
    'margin':          'margin.csv',
    'monthly_revenue': 'monthly_revenue.csv',
    'holder':          'holder.csv',
    'trust_cost':      'trust_cost.csv',
    'fundamental':     'fundamental.csv',
}

# Sample CSV filenames (bundled demo data)
_SAMPLE_FILES = {
    'profile':         'stock_profile_sample.csv',
    'daily':           'daily_k_sample.csv',
    'institutional':   'institutional_sample.csv',
    'margin':          'margin_sample.csv',
    'monthly_revenue': 'monthly_revenue_sample.csv',
    'holder':          'holder_sample.csv',
    'trust_cost':      'trust_cost_sample.csv',
}


def _resolve_csv(subdir: str):
    """
    Return (path, is_sample) for the best available CSV file.

    Prefers the user-imported standard CSV. Falls back to sample CSV.
    Returns (None, None) if neither exists.
    """
    std = os.path.join(_IMPORT_DIR, subdir, _STANDARD_FILES.get(subdir, ''))
    smp = os.path.join(_IMPORT_DIR, subdir, _SAMPLE_FILES.get(subdir, ''))
    if _STANDARD_FILES.get(subdir) and os.path.isfile(std):
        return std, False
    if _SAMPLE_FILES.get(subdir) and os.path.isfile(smp):
        return smp, True
    return None, None


def _read_csv_rows(path: str):
    """Read all rows from a CSV as list of dicts."""
    rows = []
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append({k.strip(): v.strip() for k, v in row.items()})
    except Exception as exc:
        logger.warning("RealDataLoader: cannot read %s — %s", path, exc)
    return rows


def _safe_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


class RealDataLoader:
    """
    Loads real CSV data and computes derived metrics.
    All methods return None when data is absent. No mock fallback.
    """

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------

    def load_profile(self, symbol: str):
        """
        Load stock profile (name, market, industry, theme_tags, is_mainstream_theme, sector).

        Prefers user-imported standard CSV over bundled sample CSV.
        Returns dict or None.
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("profile")
        if not path:
            return None
        for row in _read_csv_rows(path):
            if row.get("symbol") == sym:
                tags_raw = row.get("theme_tags", "")
                tags = [t.strip() for t in tags_raw.split("/") if t.strip()]
                return {
                    "symbol": sym,
                    "name": row.get("name", sym),
                    "market": row.get("market", ""),
                    "industry": row.get("industry", ""),
                    "theme_tags": tags,
                    "is_mainstream_theme": row.get("is_mainstream_theme", "0") in ("1", "true", "True"),
                    "sector": row.get("sector", ""),
                    "source_file": path,
                    "is_sample": is_sample,
                }
        return None

    # ------------------------------------------------------------------
    # Daily K
    # ------------------------------------------------------------------

    def load_daily_k(self, symbol: str, n_bars: int = 120):
        """
        Load daily OHLCV bars (newest last) with bar count metadata.

        Prefers user-imported standard CSV over bundled sample CSV.
        Returns dict or None:
            bars (list of dict), n_bars (int), has_60d (bool), has_20d (bool),
            source_file (str), is_sample (bool)
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("daily")
        if not path:
            return None
        rows = []
        for row in _read_csv_rows(path):
            if row.get("symbol") == sym:
                try:
                    rows.append({
                        "date":   row.get("date", ""),
                        "open":   _safe_float(row.get("open")),
                        "high":   _safe_float(row.get("high")),
                        "low":    _safe_float(row.get("low")),
                        "close":  _safe_float(row.get("close")),
                        "volume": _safe_float(row.get("volume")),
                    })
                except Exception as exc:
                    logger.debug("load_daily_k parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        bars = rows[-n_bars:]
        n = len(bars)
        return {
            "bars": bars,
            "n_bars": n,
            "has_20d": n >= 20,
            "has_60d": n >= 60,
            "has_120d": n >= 120,
            "source_file": path,
            "is_sample": is_sample,
        }

    # ------------------------------------------------------------------
    # Institutional flow
    # ------------------------------------------------------------------

    def load_institutional(self, symbol: str):
        """
        Load institutional net buy/sell with 3d/5d rolling sums and sell streak.

        Prefers user-imported standard CSV over bundled sample CSV.
        Returns dict or None:
            foreign_net_3d, foreign_net_5d,
            trust_net_3d, trust_net_5d,
            dealer_net_3d, dealer_net_5d,
            institution_continuous_sell_days,
            rows, source_file, is_sample
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("institutional")
        if not path:
            return None
        rows = []
        for row in _read_csv_rows(path):
            if row.get("symbol") == sym:
                try:
                    rows.append({
                        "date":            row.get("date", ""),
                        "foreign_net_buy": _safe_float(row.get("foreign_net_buy")),
                        "trust_net_buy":   _safe_float(row.get("trust_net_buy")),
                        "dealer_net_buy":  _safe_float(row.get("dealer_net_buy")),
                    })
                except Exception as exc:
                    logger.debug("load_institutional parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        last5 = rows[-5:]
        last3 = rows[-3:]

        # Continuous institutional sell days (foreign + trust combined)
        sell_days = 0
        for r in reversed(rows):
            if r["foreign_net_buy"] + r["trust_net_buy"] < 0:
                sell_days += 1
            else:
                break

        return {
            "foreign_net_3d":  sum(r["foreign_net_buy"] for r in last3),
            "foreign_net_5d":  sum(r["foreign_net_buy"] for r in last5),
            "trust_net_3d":    sum(r["trust_net_buy"]   for r in last3),
            "trust_net_5d":    sum(r["trust_net_buy"]   for r in last5),
            "dealer_net_3d":   sum(r["dealer_net_buy"]  for r in last3),
            "dealer_net_5d":   sum(r["dealer_net_buy"]  for r in last5),
            "institution_continuous_sell_days": sell_days,
            "rows": rows,
            "source_file": path,
            "is_sample": is_sample,
        }

    # ------------------------------------------------------------------
    # Margin
    # ------------------------------------------------------------------

    def load_margin(self, symbol: str):
        """
        Load margin balance with 3d/5d change and overheat risk.

        Prefers user-imported standard CSV over bundled sample CSV.
        Returns dict or None:
            margin_balance, margin_3d_change, margin_5d_change,
            margin_increase_pct, margin_overheat_risk (bool),
            short_balance, rows, source_file, is_sample
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("margin")
        if not path:
            return None
        rows = []
        for row in _read_csv_rows(path):
            if row.get("symbol") == sym:
                try:
                    rows.append({
                        "date":           row.get("date", ""),
                        "margin_balance": _safe_float(row.get("margin_balance")),
                        "margin_change":  _safe_float(row.get("margin_change")),
                        "short_balance":  _safe_float(row.get("short_balance")),
                        "short_change":   _safe_float(row.get("short_change")),
                    })
                except Exception as exc:
                    logger.debug("load_margin parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        latest = rows[-1]
        last3 = rows[-3:]
        last5 = rows[-5:]

        margin_3d = sum(r["margin_change"] for r in last3)
        margin_5d = sum(r["margin_change"] for r in last5)
        base_balance = rows[-6]["margin_balance"] if len(rows) >= 6 else rows[0]["margin_balance"]
        margin_increase_pct = (latest["margin_balance"] - base_balance) / max(base_balance, 1) * 100

        # Overheat: margin surged > 10% in 5 days
        margin_overheat_risk = margin_increase_pct > 10.0 and margin_5d > 0

        return {
            "margin_balance":       latest["margin_balance"],
            "margin_3d_change":     margin_3d,
            "margin_5d_change":     margin_5d,
            "margin_increase_pct":  round(margin_increase_pct, 2),
            "margin_overheat_risk": margin_overheat_risk,
            "short_balance":        latest["short_balance"],
            "short_change":         latest["short_change"],
            "rows": rows,
            "source_file": path,
            "is_sample": is_sample,
        }

    # ------------------------------------------------------------------
    # Monthly revenue
    # ------------------------------------------------------------------

    def load_monthly_revenue(self, symbol: str):
        """
        Load monthly revenue with growth metrics.

        Prefers user-imported standard CSV over bundled sample CSV.
        Returns dict or None:
            latest_revenue, latest_revenue_yoy, latest_revenue_mom,
            accumulated_revenue_yoy, revenue_growth_pass (bool),
            rows, source_file, is_sample
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("monthly_revenue")
        if not path:
            return None
        rows = []
        for row in _read_csv_rows(path):
            if row.get("symbol") == sym:
                try:
                    rows.append({
                        "month":           row.get("month", ""),
                        "revenue":         _safe_float(row.get("revenue")),
                        "mom":             _safe_float(row.get("mom")),
                        "yoy":             _safe_float(row.get("yoy")),
                        "accumulated_yoy": _safe_float(row.get("accumulated_yoy")),
                    })
                except Exception as exc:
                    logger.debug("load_monthly_revenue parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["month"])
        latest = rows[-1]
        yoy = latest["yoy"]
        acc_yoy = latest["accumulated_yoy"]
        mom = latest["mom"]

        # Pass rule: yoy > 30% and accumulated > 20%
        revenue_growth_pass = (yoy >= 30.0) and (acc_yoy >= 20.0)

        return {
            "latest_revenue":          latest["revenue"],
            "latest_revenue_yoy":      yoy,
            "latest_revenue_mom":      mom,
            "accumulated_revenue_yoy": acc_yoy,
            "revenue_growth_pass":     revenue_growth_pass,
            # Keys expected by FundamentalFeatures
            "yoy":             yoy,
            "accumulated_yoy": acc_yoy,
            "rows": rows,
            "source_file": path,
            "is_sample": is_sample,
        }

    # ------------------------------------------------------------------
    # Fundamental (EPS, gross_margin, operating_margin)
    # ------------------------------------------------------------------

    @staticmethod
    def _estimate_announcement_date(year: str, quarter: str):
        """
        Return conservative estimated announcement_date for a TW-listed company
        based on statutory deadlines, or None if year/quarter are invalid.
        Q1 → year-05-15, Q2 → year-08-14, Q3 → year-11-14, Q4 → next_year-03-31
        """
        _map = {"Q1": "-05-15", "Q2": "-08-14", "Q3": "-11-14", "Q4": "-03-31"}
        suffix = _map.get(str(quarter).strip())
        if not suffix or not str(year).strip().isdigit():
            return None
        y = int(str(year).strip())
        if quarter == "Q4":
            y += 1
        return f"{y}{suffix}"

    def load_fundamental(self, symbol: str):
        """
        Load quarterly fundamental data (EPS, gross_margin, operating_margin)
        from fundamental.csv. Returns flat dict with computed TTM/latest-quarter
        metrics suitable for FundamentalFeatures.compute_fundamental_features().
        Returns None when data is absent.
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("fundamental")
        if not path:
            return None

        def _nullable_float(val):
            if val is None:
                return None
            s = str(val).strip().lower()
            if s in ('', 'none', 'nan'):
                return None
            try:
                return float(s)
            except ValueError:
                return None

        rows = []
        for row in _read_csv_rows(path):
            if str(row.get("symbol", "")).strip() == sym:
                try:
                    rows.append({
                        "year":             str(row.get("year", "")).strip(),
                        "quarter":          str(row.get("quarter", "")).strip(),
                        "eps":              _nullable_float(row.get("eps")),
                        "gross_margin":     _nullable_float(row.get("gross_margin")),
                        "operating_margin": _nullable_float(row.get("operating_margin")),
                        "net_income":       _nullable_float(row.get("net_income")),
                        "announcement_date": row.get("announcement_date") or None,
                    })
                except Exception:
                    continue

        if not rows:
            return None

        _q_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
        rows.sort(key=lambda r: (r["year"], _q_order.get(r["quarter"], 0)))

        latest = rows[-1]
        prev = rows[-2] if len(rows) >= 2 else None

        latest_eps = latest.get("eps")
        latest_gm = latest.get("gross_margin")
        latest_om = latest.get("operating_margin")

        # TTM EPS: sum of last 4 quarters
        eps_vals = [r["eps"] for r in rows[-4:] if r["eps"] is not None]
        eps_ttm = sum(eps_vals) if eps_vals else None

        # EPS YoY: vs same quarter 4 periods back
        eps_yoy = None
        if len(rows) >= 5 and latest_eps is not None:
            prior = rows[-5].get("eps")
            if prior and prior != 0:
                eps_yoy = (latest_eps / prior - 1.0) * 100.0

        # EPS QoQ
        eps_qoq = None
        if prev is not None and latest_eps is not None:
            prev_eps = prev.get("eps")
            if prev_eps and prev_eps != 0:
                eps_qoq = (latest_eps / prev_eps - 1.0) * 100.0

        # Gross margin change
        gm_change = None
        if prev is not None and latest_gm is not None:
            prev_gm = prev.get("gross_margin")
            if prev_gm is not None:
                gm_change = latest_gm - prev_gm

        _ann_date = latest.get("announcement_date") or None
        _ann_is_estimated = False
        _ann_source = None
        if _ann_date:
            _ann_source = "MOPS"
        else:
            _est = self._estimate_announcement_date(
                latest.get("year", ""), latest.get("quarter", "")
            )
            if _est:
                _ann_date = _est
                _ann_source = "ESTIMATED_TW_FINANCIAL_DEADLINE"
                _ann_is_estimated = True

        return {
            "eps":                          latest_eps,
            "eps_ttm":                      eps_ttm,
            "eps_yoy":                      eps_yoy,
            "eps_qoq":                      eps_qoq,
            "gross_margin":                 latest_gm,
            "gross_margin_change":          gm_change,
            "operating_margin":             latest_om,
            "announcement_date":            _ann_date,
            "announcement_date_source":     _ann_source,
            "announcement_date_is_estimated": _ann_is_estimated,
            "latest_quarter":               f"{latest.get('year', '')} {latest.get('quarter', '')}",
            "rows":                         rows,
            "source_file":                  path,
            "is_sample":                    is_sample,
        }

    # ------------------------------------------------------------------
    # Holder structure
    # ------------------------------------------------------------------

    def load_holder(self, symbol: str):
        """
        Load major/retail holder data with trend and concentration score.

        Prefers user-imported standard CSV over bundled sample CSV.
        Returns dict or None:
            major_holder_ratio, retail_holder_ratio,
            major_holder_trend (+1 rising, -1 falling, 0 flat),
            retail_holder_trend, chip_concentration_score (0-10),
            rows, source_file, is_sample
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("holder")
        if not path:
            return None
        rows = []
        for row in _read_csv_rows(path):
            if row.get("symbol") == sym:
                try:
                    rows.append({
                        "date":                row.get("date", ""),
                        "major_holder_ratio":  _safe_float(row.get("major_holder_ratio")),
                        "retail_holder_ratio": _safe_float(row.get("retail_holder_ratio")),
                        "major_change":        _safe_float(row.get("major_change")),
                        "retail_change":       _safe_float(row.get("retail_change")),
                    })
                except Exception as exc:
                    logger.debug("load_holder parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        latest = rows[-1]

        # Trend: average change over last 3 periods
        last3 = rows[-3:]
        avg_major_chg = sum(r["major_change"] for r in last3) / len(last3)
        avg_retail_chg = sum(r["retail_change"] for r in last3) / len(last3)

        major_trend = 1 if avg_major_chg > 0.1 else (-1 if avg_major_chg < -0.1 else 0)
        retail_trend = 1 if avg_retail_chg > 0.1 else (-1 if avg_retail_chg < -0.1 else 0)

        # Chip concentration score (0-10):
        # Major rising + retail falling = bullish chip flow
        score = 5.0
        if major_trend == 1 and retail_trend == -1:
            score = 8.0 + min(2.0, avg_major_chg)
        elif major_trend == -1 and retail_trend == 1:
            score = 2.0
        elif major_trend == 1:
            score = 6.5
        elif retail_trend == -1:
            score = 6.0

        return {
            "major_holder_ratio":       latest["major_holder_ratio"],
            "retail_holder_ratio":      latest["retail_holder_ratio"],
            "major_change":             latest["major_change"],
            "retail_change":            latest["retail_change"],
            "major_holder_trend":       major_trend,
            "retail_holder_trend":      retail_trend,
            "chip_concentration_score": round(score, 1),
            "rows": rows,
            "source_file": path,
            "is_sample": is_sample,
        }

    # ------------------------------------------------------------------
    # Trust cost
    # ------------------------------------------------------------------

    def load_trust_cost(self, symbol: str):
        """
        Load investment trust average cost and price proximity.

        Prefers user-imported standard CSV over bundled sample CSV.
        Returns dict or None:
            trust_avg_cost_3d, trust_avg_cost_5d,
            latest_close, price_vs_trust_cost_pct (latest),
            trust_cost_support (bool: price is within 3% above avg cost),
            trust_cost_broken (bool: price fell below avg cost),
            rows, source_file, is_sample
        """
        sym = str(symbol)
        path, is_sample = _resolve_csv("trust_cost")
        if not path:
            return None
        rows = []
        for row in _read_csv_rows(path):
            if row.get("symbol") == sym:
                try:
                    rows.append({
                        "date":                    row.get("date", ""),
                        "trust_buy_shares":        _safe_float(row.get("trust_buy_shares")),
                        "trust_buy_amount":        _safe_float(row.get("trust_buy_amount")),
                        "trust_avg_cost":          _safe_float(row.get("trust_avg_cost")),
                        "close":                   _safe_float(row.get("close")),
                        "price_vs_trust_cost_pct": _safe_float(row.get("price_vs_trust_cost_pct")),
                    })
                except Exception as exc:
                    logger.debug("load_trust_cost parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        last5 = rows[-5:]
        last3 = rows[-3:]
        latest = rows[-1]

        # Weighted average cost (weight by shares)
        def _wavg_cost(subset):
            total_shares = sum(r["trust_buy_shares"] for r in subset)
            if total_shares <= 0:
                return sum(r["trust_avg_cost"] for r in subset) / len(subset)
            return sum(r["trust_avg_cost"] * r["trust_buy_shares"] for r in subset) / total_shares

        avg_cost_3d = _wavg_cost(last3)
        avg_cost_5d = _wavg_cost(last5)
        latest_close = latest["close"]
        pct = latest["price_vs_trust_cost_pct"]

        trust_cost_support = -3.0 <= pct <= 5.0   # price near or slightly above cost
        trust_cost_broken = pct < -3.0             # fell more than 3% below cost

        return {
            "trust_avg_cost_3d":       round(avg_cost_3d, 1),
            "trust_avg_cost_5d":       round(avg_cost_5d, 1),
            "latest_close":            round(latest_close, 1),
            "price_vs_trust_cost_pct": round(pct, 2),
            "trust_cost_support":      trust_cost_support,
            "trust_cost_broken":       trust_cost_broken,
            "rows": rows,
            "source_file": path,
            "is_sample": is_sample,
        }

    # ------------------------------------------------------------------
    # Convenience: load all
    # ------------------------------------------------------------------

    def load_all(self, symbol: str):
        """
        Load all available data for a symbol from CSV files.

        Returns dict with keys:
            profile, daily_k, institutional, margin, monthly_revenue, holder, trust_cost
        Each value is a dict/list or None when data is absent.
        Also includes '_sources' key with per-type source file paths and is_sample flags.
        """
        profile         = self.load_profile(symbol)
        daily_k         = self.load_daily_k(symbol, n_bars=9999)
        institutional   = self.load_institutional(symbol)
        margin          = self.load_margin(symbol)
        monthly_revenue = self.load_monthly_revenue(symbol)
        fundamental     = self.load_fundamental(symbol)
        holder          = self.load_holder(symbol)
        trust_cost      = self.load_trust_cost(symbol)

        # Collect per-type source metadata
        sources = {}
        for key, data in (
            ('profile',         profile),
            ('daily',           daily_k),
            ('institutional',   institutional),
            ('margin',          margin),
            ('monthly_revenue', monthly_revenue),
            ('fundamental',     fundamental),
            ('holder',          holder),
            ('trust_cost',      trust_cost),
        ):
            if data is not None:
                sources[key] = {
                    'source_file': data.get('source_file', ''),
                    'is_sample':   data.get('is_sample', True),
                }
            else:
                sources[key] = None

        return {
            "profile":         profile,
            "daily_k":         daily_k,
            "institutional":   institutional,
            "margin":          margin,
            "monthly_revenue": monthly_revenue,
            "fundamental":     fundamental,
            "holder":          holder,
            "trust_cost":      trust_cost,
            "_sources":        sources,
        }
