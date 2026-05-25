"""
data/updater.py - Daily incremental data update logic.

Orchestrates the incremental download, validates the new data, and logs a
summary.  Intended to be called from the daily pipeline or the CLI.
"""

import logging
from datetime import date, datetime, timedelta
from typing import List, Optional

import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from data.database import initialize_db, load_prices, get_latest_date
from data.downloader import download_incremental, download_stock, _get_finmind_api

logger = logging.getLogger(__name__)


def run_daily_update(
    stock_ids: Optional[List[str]] = None,
    db_path: str = config.DB_PATH,
) -> dict:
    """
    Run the daily data update: fetch new price data for all stocks in the
    universe and store it in the database.

    Parameters
    ----------
    stock_ids : list of str, optional
        Subset of stocks to update.  Defaults to the full universe.
    db_path : str
        Path to the SQLite database.

    Returns
    -------
    dict
        Summary dictionary with keys:
        - ``date``: today's date string
        - ``stocks_updated``: number of stocks that received new data
        - ``rows_added``: total new rows inserted
        - ``failed_stocks``: list of stock IDs that failed
    """
    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE

    initialize_db(db_path)
    today = date.today().strftime("%Y-%m-%d")

    logger.info("Starting daily update for %d stocks (target date: %s).", len(stock_ids), today)

    rows_added = download_incremental(
        stock_ids=stock_ids,
        end_date=today,
        db_path=db_path,
    )

    # Verify which stocks now have data up to (or close to) today
    updated = []
    failed = []
    for sid in stock_ids:
        latest = get_latest_date(sid, db_path=db_path)
        if latest is None:
            failed.append(sid)
        else:
            # Allow up to 5 calendar days lag (weekends, holidays)
            lag = (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(latest, "%Y-%m-%d")).days
            if lag <= 7:
                updated.append(sid)
            else:
                failed.append(sid)

    summary = {
        "date": today,
        "stocks_updated": len(updated),
        "rows_added": rows_added,
        "failed_stocks": failed,
    }

    logger.info(
        "Daily update complete: %d stocks updated, %d rows added, %d stocks failed.",
        len(updated), rows_added, len(failed),
    )
    return summary


def validate_data_quality(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
) -> pd.DataFrame:
    """
    Perform basic data quality checks on stored price data.

    Checks performed for each stock:
    - Number of trading days available
    - Latest date in database
    - Count of rows with NaN close price
    - Count of rows with zero volume

    Parameters
    ----------
    stock_ids : list of str, optional
        Stocks to validate.  Defaults to the full universe.
    start_date : str, optional
        Only look at data from this date onward.
    db_path : str
        Path to the SQLite database.

    Returns
    -------
    pd.DataFrame
        One row per stock with quality metrics.
    """
    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE

    if start_date is None:
        start_date = config.DEFAULT_START_DATE

    records = []
    for sid in stock_ids:
        df = load_prices([sid], start_date=start_date, db_path=db_path)
        if df.empty:
            records.append(
                {
                    "stock_id": sid,
                    "n_rows": 0,
                    "latest_date": None,
                    "nan_close": 0,
                    "zero_volume": 0,
                    "status": "NO_DATA",
                }
            )
            continue

        latest = df["date"].max()
        nan_close = df["close"].isna().sum()
        zero_vol = (df["volume"] == 0).sum()
        status = "OK" if nan_close == 0 and zero_vol < len(df) * 0.05 else "WARNING"

        records.append(
            {
                "stock_id": sid,
                "n_rows": len(df),
                "latest_date": str(latest)[:10],
                "nan_close": int(nan_close),
                "zero_volume": int(zero_vol),
                "status": status,
            }
        )

    return pd.DataFrame(records)


def repair_missing_data(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
) -> int:
    """
    Re-download data for stocks that have no records or are significantly
    behind (more than 30 calendar days stale).

    Parameters
    ----------
    stock_ids : list of str, optional
        Stocks to check and potentially repair.
    start_date : str, optional
        Fallback start date for stocks with no data.
    end_date : str, optional
        End date for re-download.
    db_path : str

    Returns
    -------
    int
        Total rows saved during repair.
    """
    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE

    if start_date is None:
        start_date = config.DEFAULT_START_DATE

    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")

    today = datetime.strptime(end_date, "%Y-%m-%d")
    api = _get_finmind_api()
    total_saved = 0

    for sid in stock_ids:
        latest = get_latest_date(sid, db_path=db_path)
        needs_repair = False

        if latest is None:
            needs_repair = True
            fetch_start = start_date
        else:
            lag_days = (today - datetime.strptime(latest, "%Y-%m-%d")).days
            if lag_days > 30:
                needs_repair = True
                fetch_start = latest

        if needs_repair:
            logger.info("Repairing data for stock %s (start: %s).", sid, fetch_start)
            from data.downloader import download_stock
            df = download_stock(
                stock_id=sid,
                start_date=fetch_start,
                end_date=end_date,
                api=api,
            )
            if not df.empty:
                from data.database import save_prices
                saved = save_prices(df, db_path=db_path)
                total_saved += saved

    logger.info("Repair complete. Total rows saved: %d", total_saved)
    return total_saved
