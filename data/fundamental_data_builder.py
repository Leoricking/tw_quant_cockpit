"""
data/fundamental_data_builder.py - Build standardized fundamental CSV files.

Takes data from public providers and merges into TW Quant Cockpit standard CSVs:
    data/import/monthly_revenue/monthly_revenue.csv
    data/import/fundamental/fundamental.csv
    data/import/institutional/institutional.csv
    data/import/margin/margin.csv

Standard columns:
    monthly_revenue: month,symbol,name,revenue,revenue_mom,revenue_yoy,
                     accumulated_revenue,accumulated_yoy,source,fetched_at
    fundamental:     year,quarter,symbol,eps,gross_margin,operating_margin,
                     operating_income,net_income,announcement_date,source,fetched_at
    institutional:   date,symbol,foreign_net_buy,trust_net_buy,dealer_net_buy,
                     foreign_buy,foreign_sell,trust_buy,trust_sell,dealer_buy,
                     dealer_sell,source,fetched_at
    margin:          date,symbol,margin_balance,margin_change,short_balance,
                     short_change,sbl_short_balance,source,fetched_at

Features:
    - append or replace mode
    - deduplication
    - date sorting
    - source lineage preserved
    - does not overwrite user data unless --replace
    - dry-run support
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Standard column schemas
_MONTHLY_REV_COLS = [
    "month", "symbol", "name", "revenue", "revenue_mom", "revenue_yoy",
    "accumulated_revenue", "accumulated_yoy", "source", "fetched_at",
]
_FUNDAMENTAL_COLS = [
    "year", "quarter", "symbol", "eps", "gross_margin", "operating_margin",
    "operating_income", "net_income", "announcement_date", "source", "fetched_at",
]
_INSTITUTIONAL_COLS = [
    "date", "symbol", "foreign_net_buy", "trust_net_buy", "dealer_net_buy",
    "foreign_buy", "foreign_sell", "trust_buy", "trust_sell", "dealer_buy",
    "dealer_sell", "source", "fetched_at",
]
_MARGIN_COLS = [
    "date", "symbol", "margin_balance", "margin_change", "short_balance",
    "short_change", "sbl_short_balance", "source", "fetched_at",
]

_DAILY_K_COLS = ["date", "symbol", "open", "high", "low", "close", "volume"]

_OUTPUT_PATHS = {
    "monthly_revenue": os.path.join("data", "import", "monthly_revenue", "monthly_revenue.csv"),
    "fundamental":     os.path.join("data", "import", "fundamental", "fundamental.csv"),
    "institutional":   os.path.join("data", "import", "institutional", "institutional.csv"),
    "margin":          os.path.join("data", "import", "margin", "margin.csv"),
    "daily_k":         os.path.join("data", "import", "daily", "daily_k.csv"),
}


def _abs_path(rel: str) -> str:
    return os.path.join(_BASE_DIR, rel)


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _load_existing(path: str, date_col: Optional[str] = None) -> pd.DataFrame:
    """Load existing CSV if present, else return empty DataFrame."""
    if not os.path.isfile(path):
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, dtype=str)
        if date_col and date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        return df
    except Exception as exc:
        logger.warning("FundamentalDataBuilder: cannot read %s: %s", path, exc)
        return pd.DataFrame()


def _standardize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Ensure all standard columns exist (fill missing with None), drop extras."""
    for col in columns:
        if col not in df.columns:
            df[col] = None
    return df[columns].copy()


def _merge_append(existing: pd.DataFrame, new: pd.DataFrame, dedup_keys: list) -> pd.DataFrame:
    """Append new rows to existing, deduplicate by keys, sort by first key."""
    if existing.empty:
        combined = new.copy()
    elif new.empty:
        combined = existing.copy()
    else:
        combined = pd.concat([existing, new], ignore_index=True)
    # Dedup: keep last (new data overrides old)
    if dedup_keys:
        valid_keys = [k for k in dedup_keys if k in combined.columns]
        if valid_keys:
            combined = combined.drop_duplicates(subset=valid_keys, keep="last")
    # Sort
    sort_col = dedup_keys[0] if dedup_keys else None
    if sort_col and sort_col in combined.columns:
        combined = combined.sort_values(sort_col)
    return combined.reset_index(drop=True)


class FundamentalDataBuilder:
    """
    Builds and merges standardized fundamental CSV files from public provider data.
    """

    def __init__(self, replace: bool = False, dry_run: bool = False):
        self.replace = replace
        self.dry_run = dry_run

    # ------------------------------------------------------------------
    # Monthly revenue
    # ------------------------------------------------------------------

    def build_monthly_revenue(
        self,
        df_new: pd.DataFrame,
    ) -> dict:
        """
        Merge new monthly revenue data into monthly_revenue.csv.

        Returns result dict with: path, rows_added, total_rows, dry_run.
        """
        path = _abs_path(_OUTPUT_PATHS["monthly_revenue"])
        _ensure_dir(path)

        df_new = _standardize(df_new, _MONTHLY_REV_COLS)
        if "month" in df_new.columns:
            df_new["month"] = pd.to_datetime(df_new["month"], errors="coerce")

        if self.replace:
            merged = df_new
        else:
            existing = _load_existing(path, date_col="month")
            merged = _merge_append(existing, df_new, dedup_keys=["month", "symbol"])

        rows_added = len(df_new)
        total_rows = len(merged)

        if not self.dry_run:
            merged.to_csv(path, index=False, encoding="utf-8-sig")
            logger.info("FundamentalDataBuilder: wrote %d rows to %s", total_rows, path)
        else:
            logger.info("FundamentalDataBuilder: DRY-RUN monthly_revenue — would write %d rows", total_rows)

        return {
            "path": path,
            "rows_added": rows_added,
            "total_rows": total_rows,
            "dry_run": self.dry_run,
        }

    # ------------------------------------------------------------------
    # Fundamental (financial statement)
    # ------------------------------------------------------------------

    def build_fundamental(
        self,
        df_new: pd.DataFrame,
    ) -> dict:
        """
        Merge new financial statement data into fundamental.csv.
        """
        path = _abs_path(_OUTPUT_PATHS["fundamental"])
        _ensure_dir(path)

        df_new = _standardize(df_new, _FUNDAMENTAL_COLS)

        if self.replace:
            merged = df_new
        else:
            existing = _load_existing(path)
            merged = _merge_append(existing, df_new, dedup_keys=["year", "quarter", "symbol"])

        rows_added = len(df_new)
        total_rows = len(merged)

        if not self.dry_run:
            merged.to_csv(path, index=False, encoding="utf-8-sig")
            logger.info("FundamentalDataBuilder: wrote %d rows to %s", total_rows, path)
        else:
            logger.info("FundamentalDataBuilder: DRY-RUN fundamental — would write %d rows", total_rows)

        return {
            "path": path,
            "rows_added": rows_added,
            "total_rows": total_rows,
            "dry_run": self.dry_run,
        }

    # ------------------------------------------------------------------
    # Institutional
    # ------------------------------------------------------------------

    def build_institutional(
        self,
        df_new: pd.DataFrame,
    ) -> dict:
        """
        Merge new institutional detail data into institutional.csv.
        """
        path = _abs_path(_OUTPUT_PATHS["institutional"])
        _ensure_dir(path)

        if "date" in df_new.columns:
            df_new["date"] = pd.to_datetime(df_new["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df_new = _standardize(df_new, _INSTITUTIONAL_COLS)

        if self.replace:
            merged = df_new
        else:
            existing = _load_existing(path, date_col="date")
            merged = _merge_append(existing, df_new, dedup_keys=["date", "symbol"])

        rows_added = len(df_new)
        total_rows = len(merged)

        if not self.dry_run:
            merged.to_csv(path, index=False, encoding="utf-8-sig")
            logger.info("FundamentalDataBuilder: wrote %d rows to %s", total_rows, path)
        else:
            logger.info("FundamentalDataBuilder: DRY-RUN institutional — would write %d rows", total_rows)

        return {
            "path": path,
            "rows_added": rows_added,
            "total_rows": total_rows,
            "dry_run": self.dry_run,
        }

    # ------------------------------------------------------------------
    # Margin / short
    # ------------------------------------------------------------------

    def build_margin(
        self,
        df_new: pd.DataFrame,
    ) -> dict:
        """
        Merge new margin/short data into margin.csv.
        """
        path = _abs_path(_OUTPUT_PATHS["margin"])
        _ensure_dir(path)

        if "date" in df_new.columns:
            df_new["date"] = pd.to_datetime(df_new["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df_new = _standardize(df_new, _MARGIN_COLS)

        if self.replace:
            merged = df_new
        else:
            existing = _load_existing(path, date_col="date")
            merged = _merge_append(existing, df_new, dedup_keys=["date", "symbol"])

        rows_added = len(df_new)
        total_rows = len(merged)

        if not self.dry_run:
            merged.to_csv(path, index=False, encoding="utf-8-sig")
            logger.info("FundamentalDataBuilder: wrote %d rows to %s", total_rows, path)
        else:
            logger.info("FundamentalDataBuilder: DRY-RUN margin — would write %d rows", total_rows)

        return {
            "path": path,
            "rows_added": rows_added,
            "total_rows": total_rows,
            "dry_run": self.dry_run,
        }

    # ------------------------------------------------------------------
    # Daily K (historical daily price)
    # ------------------------------------------------------------------

    def build_daily_k(
        self,
        df_new: pd.DataFrame,
    ) -> dict:
        """
        Merge new daily OHLCV data into daily_k.csv.
        Deduplicates by [date, symbol]. Does not overwrite unless replace=True.
        """
        path = _abs_path(_OUTPUT_PATHS["daily_k"])
        _ensure_dir(path)

        if "date" in df_new.columns:
            df_new["date"] = pd.to_datetime(df_new["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df_new = _standardize(df_new, _DAILY_K_COLS)

        if self.replace:
            merged = df_new
        else:
            existing = _load_existing(path)  # load as str; date already formatted above
            merged = _merge_append(existing, df_new, dedup_keys=["date", "symbol"])

        rows_added = len(df_new)
        total_rows = len(merged)

        if not self.dry_run:
            merged.to_csv(path, index=False, encoding="utf-8-sig")
            logger.info("FundamentalDataBuilder: wrote %d rows to %s", total_rows, path)
        else:
            logger.info("FundamentalDataBuilder: DRY-RUN daily_k — would write %d rows", total_rows)

        return {
            "path": path,
            "rows_added": rows_added,
            "total_rows": total_rows,
            "dry_run": self.dry_run,
        }

    # ------------------------------------------------------------------
    # Convenience: fetch + build for one symbol
    # ------------------------------------------------------------------

    def fetch_and_build(
        self,
        symbol: str,
        months: int = 24,
        source: str = "auto",
    ) -> dict:
        """
        Fetch public data for one symbol and write to standard CSVs.

        Returns summary dict with per-datatype results and warnings.
        """
        from data.providers.public_data_provider import PublicDataProvider
        provider = PublicDataProvider(source=source)
        sym = str(symbol).strip()

        results = {
            "symbol": sym,
            "monthly_revenue": None,
            "fundamental": None,
            "institutional": None,
            "margin": None,
            "warnings": [],
        }

        # Monthly revenue
        try:
            df_rev = provider.get_monthly_revenue(sym, months=months)
            if df_rev is not None and not df_rev.empty:
                results["monthly_revenue"] = self.build_monthly_revenue(df_rev)
            else:
                results["warnings"].append(f"{sym}: monthly_revenue unavailable from all sources")
        except Exception as exc:
            results["warnings"].append(f"{sym}: monthly_revenue error — {exc}")

        # Financial statement
        try:
            df_fin = provider.get_financial_statement(sym, years=5)
            if df_fin is not None and not df_fin.empty:
                results["fundamental"] = self.build_fundamental(df_fin)
            else:
                results["warnings"].append(f"{sym}: fundamental unavailable from all sources")
        except Exception as exc:
            results["warnings"].append(f"{sym}: fundamental error — {exc}")

        # Institutional detail
        try:
            df_inst = provider.get_institutional_detail(sym)
            if df_inst is not None and not df_inst.empty:
                results["institutional"] = self.build_institutional(df_inst)
            else:
                results["warnings"].append(f"{sym}: institutional unavailable from all sources")
        except Exception as exc:
            results["warnings"].append(f"{sym}: institutional error — {exc}")

        # Margin / short
        try:
            df_margin = provider.get_margin_short(sym)
            if df_margin is not None and not df_margin.empty:
                results["margin"] = self.build_margin(df_margin)
            else:
                results["warnings"].append(f"{sym}: margin_short unavailable from all sources")
        except Exception as exc:
            results["warnings"].append(f"{sym}: margin_short error — {exc}")

        return results
