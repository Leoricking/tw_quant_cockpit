"""
data/downloader.py - Download Taiwan stock OHLCV data via the FinMind API.

Uses the ``FinMind`` Python package which wraps the FinMind REST API.
A free-tier account provides limited daily requests; set FINMIND_TOKEN in
config.py or the environment variable FINMIND_TOKEN for higher limits.
"""

import logging
import time
from datetime import datetime, date, timedelta
from typing import List, Optional

import pandas as pd
from tqdm import tqdm

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from data.database import initialize_db, save_prices, get_latest_date

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# FinMind client initialisation
# ---------------------------------------------------------------------------

def _get_finmind_api():
    """
    Return an authenticated FinMind DataLoader instance.

    Raises
    ------
    ImportError
        If the ``FinMind`` package is not installed.
    """
    try:
        from FinMind.data import DataLoader
    except ImportError as exc:
        raise ImportError(
            "FinMind package not found. Install with: pip install FinMind"
        ) from exc

    api = DataLoader()
    token = config.FINMIND_TOKEN
    if token:
        api.login_by_token(api_token=token)
        logger.info("FinMind authenticated with token.")
    else:
        logger.warning(
            "FINMIND_TOKEN not set – using unauthenticated access (rate-limited)."
        )
    return api


# ---------------------------------------------------------------------------
# Core download function
# ---------------------------------------------------------------------------

def download_stock(
    stock_id: str,
    start_date: str,
    end_date: str,
    api=None,
    max_retries: int = 3,
    sleep_seconds: float = 1.0,
) -> pd.DataFrame:
    """
    Download daily OHLCV data for a single Taiwan stock.

    Parameters
    ----------
    stock_id : str
        TWSE stock ticker, e.g. ``"2330"``.
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    api : FinMind DataLoader, optional
        Re-use an existing authenticated instance.
    max_retries : int
        Number of retry attempts on transient errors.
    sleep_seconds : float
        Pause between requests to respect rate limits.

    Returns
    -------
    pd.DataFrame
        Columns: date, stock_id, open, high, low, close, volume.
        Returns an empty DataFrame on failure.
    """
    if api is None:
        api = _get_finmind_api()

    for attempt in range(1, max_retries + 1):
        try:
            raw = api.taiwan_stock_daily(
                stock_id=stock_id,
                start_date=start_date,
                end_date=end_date,
            )
            if raw is None or raw.empty:
                logger.debug("No data returned for %s (%s → %s).", stock_id, start_date, end_date)
                return pd.DataFrame()

            # Normalise column names from FinMind format
            rename_map = {
                "date": "date",
                "stock_id": "stock_id",
                "open": "open",
                "max": "high",
                "min": "low",
                "close": "close",
                "Trading_Volume": "volume",
                "volume": "volume",
            }
            raw = raw.rename(columns={k: v for k, v in rename_map.items() if k in raw.columns})

            # Some FinMind versions use different casing
            raw.columns = [c.lower() for c in raw.columns]
            if "max" in raw.columns:
                raw = raw.rename(columns={"max": "high", "min": "low"})
            if "trading_volume" in raw.columns:
                raw = raw.rename(columns={"trading_volume": "volume"})

            required = {"date", "open", "high", "low", "close", "volume"}
            missing = required - set(raw.columns)
            if missing:
                logger.warning("Stock %s missing columns %s – skipping.", stock_id, missing)
                return pd.DataFrame()

            raw["stock_id"] = str(stock_id)
            raw["date"] = pd.to_datetime(raw["date"]).dt.strftime("%Y-%m-%d")

            for col in ["open", "high", "low", "close", "volume"]:
                raw[col] = pd.to_numeric(raw[col], errors="coerce")

            result = raw[["date", "stock_id", "open", "high", "low", "close", "volume"]].dropna(
                subset=["close"]
            )
            time.sleep(sleep_seconds)
            return result

        except Exception as exc:  # pylint: disable=broad-except
            logger.warning(
                "Attempt %d/%d failed for stock %s: %s",
                attempt, max_retries, stock_id, exc,
            )
            if attempt < max_retries:
                time.sleep(sleep_seconds * 2 ** attempt)

    return pd.DataFrame()


# ---------------------------------------------------------------------------
# Batch download
# ---------------------------------------------------------------------------

def download_all_stocks(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    batch_size: int = 10,
    sleep_between_batches: float = 2.0,
    db_path: str = config.DB_PATH,
) -> int:
    """
    Download OHLCV data for a list of Taiwan stocks and persist to SQLite.

    Parameters
    ----------
    stock_ids : list of str, optional
        Stocks to download.  Defaults to ``config.STOCK_UNIVERSE``.
    start_date : str, optional
        Start date.  Defaults to ``config.DEFAULT_START_DATE``.
    end_date : str, optional
        End date.  Defaults to today.
    batch_size : int
        Number of stocks to process before a longer pause.
    sleep_between_batches : float
        Extra sleep (seconds) between batches.
    db_path : str
        Path to the SQLite database.

    Returns
    -------
    int
        Total number of rows saved.
    """
    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE

    if start_date is None:
        start_date = config.DEFAULT_START_DATE

    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")

    initialize_db(db_path)
    api = _get_finmind_api()

    total_saved = 0
    failed = []

    for i, stock_id in enumerate(tqdm(stock_ids, desc="Downloading stocks")):
        df = download_stock(
            stock_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            api=api,
        )

        if df.empty:
            failed.append(stock_id)
            continue

        saved = save_prices(df, db_path=db_path)
        total_saved += saved

        if (i + 1) % batch_size == 0:
            logger.info(
                "Batch complete (%d/%d). Total rows saved so far: %d",
                i + 1, len(stock_ids), total_saved,
            )
            time.sleep(sleep_between_batches)

    if failed:
        logger.warning("Failed to download %d stocks: %s", len(failed), failed)

    logger.info("Download complete. Total rows saved: %d", total_saved)
    return total_saved


# ---------------------------------------------------------------------------
# Incremental download (only missing dates)
# ---------------------------------------------------------------------------

def download_incremental(
    stock_ids: Optional[List[str]] = None,
    end_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
) -> int:
    """
    Download only the data that is newer than what is already in the database.

    For each stock, checks the latest date in the DB and downloads from
    (latest_date + 1 day) onward.  Stocks with no data at all are downloaded
    from ``config.DEFAULT_START_DATE``.

    Parameters
    ----------
    stock_ids : list of str, optional
        Defaults to ``config.STOCK_UNIVERSE``.
    end_date : str, optional
        Defaults to today.
    db_path : str
        Path to the SQLite database.

    Returns
    -------
    int
        Total number of new rows saved.
    """
    if stock_ids is None:
        stock_ids = config.STOCK_UNIVERSE

    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")

    initialize_db(db_path)
    api = _get_finmind_api()
    total_saved = 0

    for stock_id in tqdm(stock_ids, desc="Incremental update"):
        latest = get_latest_date(stock_id, db_path=db_path)

        if latest is None:
            start = config.DEFAULT_START_DATE
        else:
            next_day = (datetime.strptime(latest, "%Y-%m-%d") + timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
            if next_day > end_date:
                logger.debug("Stock %s is already up to date.", stock_id)
                continue
            start = next_day

        df = download_stock(
            stock_id=stock_id,
            start_date=start,
            end_date=end_date,
            api=api,
        )

        if not df.empty:
            saved = save_prices(df, db_path=db_path)
            total_saved += saved

    logger.info("Incremental update complete. New rows saved: %d", total_saved)
    return total_saved
