"""
data/real_data_loader.py - Real CSV data loader for TW Quant Cockpit.

Reads structured CSVs from data/import/ subdirectories.
No mock fallback — returns None when data is absent.

Directory layout expected:
    data/import/profile/stock_profile_sample.csv
    data/import/daily/daily_k_sample.csv
    data/import/institutional/institutional_sample.csv
    data/import/margin/margin_sample.csv
    data/import/monthly_revenue/monthly_revenue_sample.csv
    data/import/holder/holder_sample.csv
"""

import os
import logging
import csv

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_IMPORT_DIR = os.path.join(_BASE_DIR, "import")


def _glob_csvs(subdir: str):
    """Return all *.csv paths under data/import/<subdir>/."""
    folder = os.path.join(_IMPORT_DIR, subdir)
    if not os.path.isdir(folder):
        return []
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".csv")
    ]


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


class RealDataLoader:
    """
    Loads real data from CSV files under data/import/.

    All methods return None when data is unavailable.
    No mock fallback is ever applied.
    """

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------

    def load_profile(self, symbol: str):
        """
        Load stock profile (name, market, industry, theme_tags).

        Returns
        -------
        dict or None
            Keys: symbol, name, market, industry, theme_tags (list)
        """
        sym = str(symbol)
        for path in _glob_csvs("profile"):
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
                    }
        return None

    # ------------------------------------------------------------------
    # Daily K
    # ------------------------------------------------------------------

    def load_daily_k(self, symbol: str, n_bars: int = 120):
        """
        Load daily OHLCV bars (newest last).

        Returns
        -------
        list of dict or None
            Each dict: date, open, high, low, close, volume (floats)
        """
        sym = str(symbol)
        rows = []
        for path in _glob_csvs("daily"):
            for row in _read_csv_rows(path):
                if row.get("symbol") == sym:
                    try:
                        rows.append({
                            "date":   row.get("date", ""),
                            "open":   float(row["open"]),
                            "high":   float(row["high"]),
                            "low":    float(row["low"]),
                            "close":  float(row["close"]),
                            "volume": float(row["volume"]),
                        })
                    except (KeyError, ValueError) as exc:
                        logger.debug("load_daily_k parse error for %s: %s", sym, exc)

        if not rows:
            return None
        # Sort by date ascending, return newest n_bars
        rows.sort(key=lambda r: r["date"])
        return rows[-n_bars:]

    # ------------------------------------------------------------------
    # Institutional
    # ------------------------------------------------------------------

    def load_institutional(self, symbol: str):
        """
        Load institutional net buy/sell data.

        Returns
        -------
        dict or None
            Keys: foreign_net_3d, trust_net_3d, dealer_net_3d (sums of last 3 days),
                  rows (list of raw dicts)
        """
        sym = str(symbol)
        rows = []
        for path in _glob_csvs("institutional"):
            for row in _read_csv_rows(path):
                if row.get("symbol") == sym:
                    try:
                        rows.append({
                            "date":           row.get("date", ""),
                            "foreign_net_buy": float(row.get("foreign_net_buy", 0) or 0),
                            "trust_net_buy":   float(row.get("trust_net_buy", 0) or 0),
                            "dealer_net_buy":  float(row.get("dealer_net_buy", 0) or 0),
                        })
                    except (ValueError, KeyError) as exc:
                        logger.debug("load_institutional parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        last3 = rows[-3:]
        return {
            "foreign_net_3d": sum(r["foreign_net_buy"] for r in last3),
            "trust_net_3d":   sum(r["trust_net_buy"]   for r in last3),
            "dealer_net_3d":  sum(r["dealer_net_buy"]  for r in last3),
            "rows": rows,
        }

    # ------------------------------------------------------------------
    # Margin
    # ------------------------------------------------------------------

    def load_margin(self, symbol: str):
        """
        Load margin balance data.

        Returns
        -------
        dict or None
            Keys: margin_balance, margin_change, short_balance, short_change (latest row)
        """
        sym = str(symbol)
        rows = []
        for path in _glob_csvs("margin"):
            for row in _read_csv_rows(path):
                if row.get("symbol") == sym:
                    try:
                        rows.append({
                            "date":           row.get("date", ""),
                            "margin_balance": float(row.get("margin_balance", 0) or 0),
                            "margin_change":  float(row.get("margin_change", 0) or 0),
                            "short_balance":  float(row.get("short_balance", 0) or 0),
                            "short_change":   float(row.get("short_change", 0) or 0),
                        })
                    except (ValueError, KeyError) as exc:
                        logger.debug("load_margin parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        latest = rows[-1]
        return {
            "margin_balance": latest["margin_balance"],
            "margin_change":  latest["margin_change"],
            "short_balance":  latest["short_balance"],
            "short_change":   latest["short_change"],
            "rows": rows,
        }

    # ------------------------------------------------------------------
    # Monthly revenue
    # ------------------------------------------------------------------

    def load_monthly_revenue(self, symbol: str):
        """
        Load monthly revenue data.

        Returns
        -------
        dict or None
            Keys: latest_revenue, mom, yoy, accumulated_yoy, rows
        """
        sym = str(symbol)
        rows = []
        for path in _glob_csvs("monthly_revenue"):
            for row in _read_csv_rows(path):
                if row.get("symbol") == sym:
                    try:
                        rows.append({
                            "month":           row.get("month", ""),
                            "revenue":         float(row.get("revenue", 0) or 0),
                            "mom":             float(row.get("mom", 0) or 0),
                            "yoy":             float(row.get("yoy", 0) or 0),
                            "accumulated_yoy": float(row.get("accumulated_yoy", 0) or 0),
                        })
                    except (ValueError, KeyError) as exc:
                        logger.debug("load_monthly_revenue parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["month"])
        latest = rows[-1]
        return {
            "latest_revenue":  latest["revenue"],
            "mom":             latest["mom"],
            "yoy":             latest["yoy"],
            "accumulated_yoy": latest["accumulated_yoy"],
            "rows": rows,
        }

    # ------------------------------------------------------------------
    # Holder structure
    # ------------------------------------------------------------------

    def load_holder(self, symbol: str):
        """
        Load major/retail holder ratio data.

        Returns
        -------
        dict or None
            Keys: major_holder_ratio, retail_holder_ratio, major_change, retail_change
        """
        sym = str(symbol)
        rows = []
        for path in _glob_csvs("holder"):
            for row in _read_csv_rows(path):
                if row.get("symbol") == sym:
                    try:
                        rows.append({
                            "date":               row.get("date", ""),
                            "major_holder_ratio": float(row.get("major_holder_ratio", 0) or 0),
                            "retail_holder_ratio": float(row.get("retail_holder_ratio", 0) or 0),
                            "major_change":       float(row.get("major_change", 0) or 0),
                            "retail_change":      float(row.get("retail_change", 0) or 0),
                        })
                    except (ValueError, KeyError) as exc:
                        logger.debug("load_holder parse error for %s: %s", sym, exc)

        if not rows:
            return None
        rows.sort(key=lambda r: r["date"])
        latest = rows[-1]
        return {
            "major_holder_ratio":  latest["major_holder_ratio"],
            "retail_holder_ratio": latest["retail_holder_ratio"],
            "major_change":        latest["major_change"],
            "retail_change":       latest["retail_change"],
            "rows": rows,
        }

    # ------------------------------------------------------------------
    # Convenience: load all
    # ------------------------------------------------------------------

    def load_all(self, symbol: str):
        """
        Load all available data for a symbol from CSV files.

        Returns
        -------
        dict with keys:
            profile, daily_k, institutional, margin, monthly_revenue, holder
            Each value is a dict/list or None when data is absent.
        """
        return {
            "profile":         self.load_profile(symbol),
            "daily_k":         self.load_daily_k(symbol),
            "institutional":   self.load_institutional(symbol),
            "margin":          self.load_margin(symbol),
            "monthly_revenue": self.load_monthly_revenue(symbol),
            "holder":          self.load_holder(symbol),
        }
