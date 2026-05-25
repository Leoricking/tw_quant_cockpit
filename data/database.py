"""
data/database.py - SQLite persistence layer.

Provides read/write helpers for stock prices, features, predictions, and
daily reports.  All operations use the standard-library `sqlite3` module so
there are no extra dependencies.
"""

import sqlite3
import logging
import json
from datetime import datetime
from typing import List, Optional

import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------

CREATE_STOCK_PRICES = """
CREATE TABLE IF NOT EXISTS stock_prices (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    date      TEXT    NOT NULL,
    stock_id  TEXT    NOT NULL,
    open      REAL,
    high      REAL,
    low       REAL,
    close     REAL,
    volume    REAL,
    UNIQUE (date, stock_id)
);
"""

CREATE_FEATURES = """
CREATE TABLE IF NOT EXISTS features (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    date      TEXT    NOT NULL,
    stock_id  TEXT    NOT NULL,
    feature_json TEXT NOT NULL,
    UNIQUE (date, stock_id)
);
"""

CREATE_PREDICTIONS = """
CREATE TABLE IF NOT EXISTS predictions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    date                TEXT    NOT NULL,
    stock_id            TEXT    NOT NULL,
    predicted_return    REAL,
    up_probability      REAL,
    predicted_volatility REAL,
    UNIQUE (date, stock_id)
);
"""

CREATE_REPORTS = """
CREATE TABLE IF NOT EXISTS reports (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    date      TEXT    NOT NULL UNIQUE,
    content   TEXT    NOT NULL
);
"""


def get_connection(db_path: str = config.DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection with WAL mode enabled for concurrency."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db(db_path: str = config.DB_PATH) -> None:
    """Create all tables if they do not already exist."""
    with get_connection(db_path) as conn:
        conn.execute(CREATE_STOCK_PRICES)
        conn.execute(CREATE_FEATURES)
        conn.execute(CREATE_PREDICTIONS)
        conn.execute(CREATE_REPORTS)
        conn.commit()
    logger.info("Database initialised at %s", db_path)


# ---------------------------------------------------------------------------
# Stock prices
# ---------------------------------------------------------------------------

def save_prices(df: pd.DataFrame, db_path: str = config.DB_PATH) -> int:
    """
    Persist OHLCV data to the ``stock_prices`` table.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: date, stock_id, open, high, low, close, volume.
    db_path : str
        Path to the SQLite database file.

    Returns
    -------
    int
        Number of rows inserted/replaced.
    """
    if df.empty:
        logger.warning("save_prices called with empty DataFrame – skipping.")
        return 0

    required = {"date", "stock_id", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing columns: {missing}")

    rows = df[list(required)].copy()
    rows["date"] = rows["date"].astype(str)

    with get_connection(db_path) as conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO stock_prices (date, stock_id, open, high, low, close, volume)
            VALUES (:date, :stock_id, :open, :high, :low, :close, :volume)
            """,
            rows.to_dict(orient="records"),
        )
        conn.commit()

    logger.info("Saved %d price rows to database.", len(rows))
    return len(rows)


def load_prices(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
) -> pd.DataFrame:
    """
    Load OHLCV data from the database.

    Parameters
    ----------
    stock_ids : list of str, optional
        Filter to these stock IDs.  If None, all stocks are returned.
    start_date : str, optional
        Inclusive lower bound in 'YYYY-MM-DD' format.
    end_date : str, optional
        Inclusive upper bound in 'YYYY-MM-DD' format.
    db_path : str
        Path to the SQLite database file.

    Returns
    -------
    pd.DataFrame
        Columns: date, stock_id, open, high, low, close, volume.
    """
    initialize_db(db_path)

    conditions = []
    params: list = []

    if stock_ids:
        placeholders = ",".join("?" * len(stock_ids))
        conditions.append(f"stock_id IN ({placeholders})")
        params.extend(stock_ids)
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    query = f"SELECT date, stock_id, open, high, low, close, volume FROM stock_prices {where} ORDER BY stock_id, date"

    with get_connection(db_path) as conn:
        df = pd.read_sql_query(query, conn, params=params)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    logger.debug("Loaded %d price rows from database.", len(df))
    return df


def get_latest_date(stock_id: str, db_path: str = config.DB_PATH) -> Optional[str]:
    """Return the most recent date available for a given stock, or None."""
    initialize_db(db_path)
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT MAX(date) as latest FROM stock_prices WHERE stock_id = ?",
            (stock_id,),
        ).fetchone()
    return row["latest"] if row and row["latest"] else None


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------

def save_features(df: pd.DataFrame, db_path: str = config.DB_PATH) -> int:
    """
    Persist computed features to the ``features`` table.

    The DataFrame must contain ``date`` and ``stock_id`` columns.  All other
    columns are serialised as JSON.
    """
    if df.empty:
        return 0

    required = {"date", "stock_id"}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns: {required}")

    rows = []
    for _, row in df.iterrows():
        feature_dict = {
            k: (None if pd.isna(v) else v)
            for k, v in row.items()
            if k not in ("date", "stock_id")
        }
        rows.append(
            {
                "date": str(row["date"])[:10],
                "stock_id": row["stock_id"],
                "feature_json": json.dumps(feature_dict),
            }
        )

    with get_connection(db_path) as conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO features (date, stock_id, feature_json)
            VALUES (:date, :stock_id, :feature_json)
            """,
            rows,
        )
        conn.commit()

    logger.info("Saved %d feature rows to database.", len(rows))
    return len(rows)


def load_features(
    stock_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db_path: str = config.DB_PATH,
) -> pd.DataFrame:
    """Load feature rows and expand the stored JSON back into columns."""
    initialize_db(db_path)

    conditions = []
    params: list = []

    if stock_ids:
        placeholders = ",".join("?" * len(stock_ids))
        conditions.append(f"stock_id IN ({placeholders})")
        params.extend(stock_ids)
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    query = f"SELECT date, stock_id, feature_json FROM features {where} ORDER BY stock_id, date"

    with get_connection(db_path) as conn:
        raw = pd.read_sql_query(query, conn, params=params)

    if raw.empty:
        return pd.DataFrame()

    expanded = raw["feature_json"].apply(json.loads).apply(pd.Series)
    df = pd.concat([raw[["date", "stock_id"]], expanded], axis=1)
    df["date"] = pd.to_datetime(df["date"])
    return df


# ---------------------------------------------------------------------------
# Predictions
# ---------------------------------------------------------------------------

def save_predictions(df: pd.DataFrame, db_path: str = config.DB_PATH) -> int:
    """
    Persist model predictions to the ``predictions`` table.

    Expected columns: date, stock_id, predicted_return, up_probability,
    predicted_volatility.
    """
    if df.empty:
        return 0

    required = {"date", "stock_id"}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain: {required}")

    rows = df.copy()
    rows["date"] = rows["date"].astype(str).str[:10]
    for col in ["predicted_return", "up_probability", "predicted_volatility"]:
        if col not in rows.columns:
            rows[col] = None

    with get_connection(db_path) as conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO predictions
                (date, stock_id, predicted_return, up_probability, predicted_volatility)
            VALUES (:date, :stock_id, :predicted_return, :up_probability, :predicted_volatility)
            """,
            rows[
                ["date", "stock_id", "predicted_return", "up_probability", "predicted_volatility"]
            ].to_dict(orient="records"),
        )
        conn.commit()

    logger.info("Saved %d prediction rows.", len(rows))
    return len(rows)


def load_predictions(
    date: Optional[str] = None,
    stock_ids: Optional[List[str]] = None,
    db_path: str = config.DB_PATH,
) -> pd.DataFrame:
    """Load predictions, optionally filtered by date and/or stock IDs."""
    initialize_db(db_path)

    conditions = []
    params: list = []

    if date:
        conditions.append("date = ?")
        params.append(date)
    if stock_ids:
        placeholders = ",".join("?" * len(stock_ids))
        conditions.append(f"stock_id IN ({placeholders})")
        params.extend(stock_ids)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    query = (
        f"SELECT date, stock_id, predicted_return, up_probability, predicted_volatility "
        f"FROM predictions {where} ORDER BY date DESC, up_probability DESC"
    )

    with get_connection(db_path) as conn:
        df = pd.read_sql_query(query, conn, params=params)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    return df


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

def save_report(date: str, content: str, db_path: str = config.DB_PATH) -> None:
    """Persist a daily report string keyed by date (YYYY-MM-DD)."""
    initialize_db(db_path)
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO reports (date, content) VALUES (?, ?)",
            (date[:10], content),
        )
        conn.commit()
    logger.info("Report saved for date %s.", date)


def load_report(date: str, db_path: str = config.DB_PATH) -> Optional[str]:
    """Return the report string for the given date, or None if not found."""
    initialize_db(db_path)
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT content FROM reports WHERE date = ?", (date[:10],)
        ).fetchone()
    return row["content"] if row else None


def list_report_dates(db_path: str = config.DB_PATH) -> List[str]:
    """Return a sorted list of all dates that have saved reports."""
    initialize_db(db_path)
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT date FROM reports ORDER BY date DESC"
        ).fetchall()
    return [r["date"] for r in rows]
