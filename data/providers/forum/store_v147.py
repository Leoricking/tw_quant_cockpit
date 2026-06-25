"""
data/providers/forum/store_v147.py — ForumStore SQLite backend v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No full IP stored. No credentials stored. SUPPLEMENTARY authority only.
[!] Additive migration only. Idempotent DDL. No personal identity columns.
"""
from __future__ import annotations

import contextlib
import logging
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_FULL_IP_STORED = False  # ALWAYS FALSE

_DDL: List[str] = [
    # 1. forum_sources
    """
    CREATE TABLE IF NOT EXISTS forum_sources (
        source_id       TEXT PRIMARY KEY,
        display_name    TEXT NOT NULL,
        base_url        TEXT NOT NULL,
        board_id        TEXT,
        authority_level TEXT NOT NULL DEFAULT 'SUPPLEMENTARY',
        is_public       INTEGER NOT NULL DEFAULT 1,
        is_private      INTEGER NOT NULL DEFAULT 0,
        allowlisted     INTEGER NOT NULL DEFAULT 1,
        max_pages       INTEGER DEFAULT 10,
        max_articles    INTEGER DEFAULT 100,
        rate_limit_sec  REAL DEFAULT 2.0,
        notes           TEXT,
        registered_at   TEXT
    )
    """,
    # 2. forum_articles
    """
    CREATE TABLE IF NOT EXISTS forum_articles (
        article_id          TEXT PRIMARY KEY,
        source_id           TEXT NOT NULL,
        canonical_url       TEXT,
        board_id            TEXT,
        category            TEXT,
        title               TEXT,
        author_display_id   TEXT,
        published_at        TEXT,
        published_at_precision TEXT DEFAULT 'MINUTE',
        first_seen_at       TEXT,
        last_seen_at        TEXT,
        body_hash           TEXT,
        body_length         INTEGER DEFAULT 0,
        duplicate_status    TEXT DEFAULT 'UNIQUE',
        is_deleted          INTEGER NOT NULL DEFAULT 0,
        deletion_type       TEXT,
        formal_standalone   INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (source_id) REFERENCES forum_sources(source_id)
    )
    """,
    # 3. forum_article_versions (immutable append)
    """
    CREATE TABLE IF NOT EXISTS forum_article_versions (
        version_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        version_seq     INTEGER NOT NULL DEFAULT 1,
        captured_at     TEXT NOT NULL,
        body_hash       TEXT,
        title           TEXT,
        change_type     TEXT DEFAULT 'INITIAL',
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 4. forum_comments
    """
    CREATE TABLE IF NOT EXISTS forum_comments (
        comment_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id          TEXT NOT NULL,
        sequence            INTEGER,
        author_display_id   TEXT,
        tag                 TEXT DEFAULT 'NEUTRAL',
        text                TEXT,
        comment_time        TEXT,
        time_precision      TEXT DEFAULT 'MINUTE',
        first_seen_at       TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 5. forum_edit_events (append-only)
    """
    CREATE TABLE IF NOT EXISTS forum_edit_events (
        edit_id         INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        edited_at       TEXT,
        edit_seq        INTEGER DEFAULT 1,
        note            TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 6. forum_deletion_events (append-only)
    """
    CREATE TABLE IF NOT EXISTS forum_deletion_events (
        deletion_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        detected_at     TEXT NOT NULL,
        deletion_type   TEXT,
        prior_title     TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 7. forum_symbol_mentions
    """
    CREATE TABLE IF NOT EXISTS forum_symbol_mentions (
        mention_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        symbol          TEXT NOT NULL,
        match_confidence TEXT DEFAULT 'MEDIUM',
        context_snippet TEXT,
        mentioned_at    TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 8. forum_topic_signals
    """
    CREATE TABLE IF NOT EXISTS forum_topic_signals (
        topic_signal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        topic_label     TEXT,
        evidence_terms  TEXT,
        model_version   TEXT,
        scored_at       TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 9. forum_sentiment_signals
    """
    CREATE TABLE IF NOT EXISTS forum_sentiment_signals (
        sentiment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        target_symbol   TEXT,
        polarity        TEXT DEFAULT 'UNKNOWN',
        stance          TEXT DEFAULT 'UNKNOWN',
        confidence      REAL DEFAULT 0.0,
        sarcasm_risk    TEXT DEFAULT 'UNKNOWN',
        model_version   TEXT,
        scored_at       TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 10. forum_engagement_signals
    """
    CREATE TABLE IF NOT EXISTS forum_engagement_signals (
        engagement_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id          TEXT NOT NULL,
        total_comments      INTEGER DEFAULT 0,
        unique_commenters   INTEGER DEFAULT 0,
        push_count          INTEGER DEFAULT 0,
        boo_count           INTEGER DEFAULT 0,
        neutral_count       INTEGER DEFAULT 0,
        velocity_1h         REAL DEFAULT 0.0,
        computed_at         TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 11. forum_credibility_signals
    """
    CREATE TABLE IF NOT EXISTS forum_credibility_signals (
        credibility_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id          TEXT NOT NULL,
        has_official_link   INTEGER DEFAULT 0,
        has_concrete_numbers INTEGER DEFAULT 0,
        has_unsupported_claim INTEGER DEFAULT 0,
        has_rumor_terms     INTEGER DEFAULT 0,
        has_guaranteed_profit INTEGER DEFAULT 0,
        edit_risk           TEXT DEFAULT 'LOW',
        deletion_risk       TEXT DEFAULT 'LOW',
        content_credibility TEXT DEFAULT 'UNVERIFIED',
        scored_at           TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 12. forum_coordination_risks
    """
    CREATE TABLE IF NOT EXISTS forum_coordination_risks (
        coord_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        risk_level      TEXT DEFAULT 'LOW',
        risk_signals    TEXT,
        assessed_at     TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 13. forum_manipulation_risks
    """
    CREATE TABLE IF NOT EXISTS forum_manipulation_risks (
        manip_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id      TEXT NOT NULL,
        risk_level      TEXT DEFAULT 'LOW',
        risk_signals    TEXT,
        assessed_at     TEXT,
        FOREIGN KEY (article_id) REFERENCES forum_articles(article_id)
    )
    """,
    # 14. market_sentiment_snapshots
    """
    CREATE TABLE IF NOT EXISTS market_sentiment_snapshots (
        snapshot_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        window          TEXT NOT NULL,
        dimension       TEXT NOT NULL,
        dimension_value TEXT,
        article_count   INTEGER DEFAULT 0,
        bullish_count   INTEGER DEFAULT 0,
        bearish_count   INTEGER DEFAULT 0,
        neutral_count   INTEGER DEFAULT 0,
        disagreement    REAL DEFAULT 0.0,
        confidence      REAL DEFAULT 0.0,
        formal_standalone INTEGER NOT NULL DEFAULT 0,
        computed_at     TEXT NOT NULL
    )
    """,
    # 15. forum_fetch_runs
    """
    CREATE TABLE IF NOT EXISTS forum_fetch_runs (
        run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id       TEXT NOT NULL,
        started_at      TEXT NOT NULL,
        completed_at    TEXT,
        articles_found  INTEGER DEFAULT 0,
        pages_fetched   INTEGER DEFAULT 0,
        dry_run         INTEGER NOT NULL DEFAULT 1,
        status          TEXT DEFAULT 'PENDING',
        notes           TEXT,
        FOREIGN KEY (source_id) REFERENCES forum_sources(source_id)
    )
    """,
    # Indexes
    "CREATE INDEX IF NOT EXISTS idx_articles_source ON forum_articles(source_id)",
    "CREATE INDEX IF NOT EXISTS idx_articles_published ON forum_articles(published_at)",
    "CREATE INDEX IF NOT EXISTS idx_comments_article ON forum_comments(article_id)",
    "CREATE INDEX IF NOT EXISTS idx_symbol_mentions_symbol ON forum_symbol_mentions(symbol)",
    "CREATE INDEX IF NOT EXISTS idx_sentiment_symbol ON forum_sentiment_signals(target_symbol)",
    "CREATE INDEX IF NOT EXISTS idx_snapshots_window ON market_sentiment_snapshots(window, computed_at)",
]


class ForumStore:
    """
    SQLite-backed store for Forum Intelligence v1.4.7.
    [!] No full IP stored. No credentials. Additive migration only.
    [!] SUPPLEMENTARY authority. Research Only.
    """

    SCHEMA_VERSION = 1
    TABLE_COUNT = 15

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)
            ))))
            db_path = os.path.join(base, "data", "forum_intelligence.db")
        self._db_path = db_path
        self._ensure_dir()
        self._apply_migrations()

    def _ensure_dir(self) -> None:
        d = os.path.dirname(self._db_path)
        if d:
            os.makedirs(d, exist_ok=True)

    @contextlib.contextmanager
    def _conn(self):
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _apply_migrations(self) -> None:
        """Idempotent DDL — additive only, never drops columns."""
        with self._conn() as conn:
            for stmt in _DDL:
                conn.execute(stmt)

    # ------------------------------------------------------------------
    # Forum Sources
    # ------------------------------------------------------------------

    def upsert_source(self, source: Dict[str, Any]) -> None:
        sql = """
        INSERT OR REPLACE INTO forum_sources
            (source_id, display_name, base_url, board_id, authority_level,
             is_public, is_private, allowlisted, max_pages, max_articles,
             rate_limit_sec, notes, registered_at)
        VALUES
            (:source_id, :display_name, :base_url, :board_id, :authority_level,
             :is_public, :is_private, :allowlisted, :max_pages, :max_articles,
             :rate_limit_sec, :notes, :registered_at)
        """
        with self._conn() as conn:
            conn.execute(sql, source)

    def get_source(self, source_id: str) -> Optional[Dict]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM forum_sources WHERE source_id = ?", (source_id,)
            ).fetchone()
        return dict(row) if row else None

    def list_sources(self) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM forum_sources").fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Forum Articles
    # ------------------------------------------------------------------

    def upsert_article(self, article: Dict[str, Any]) -> None:
        sql = """
        INSERT OR REPLACE INTO forum_articles
            (article_id, source_id, canonical_url, board_id, category, title,
             author_display_id, published_at, published_at_precision,
             first_seen_at, last_seen_at, body_hash, body_length,
             duplicate_status, is_deleted, deletion_type, formal_standalone)
        VALUES
            (:article_id, :source_id, :canonical_url, :board_id, :category,
             :title, :author_display_id, :published_at, :published_at_precision,
             :first_seen_at, :last_seen_at, :body_hash, :body_length,
             :duplicate_status, :is_deleted, :deletion_type, :formal_standalone)
        """
        with self._conn() as conn:
            conn.execute(sql, article)

    def get_article(self, article_id: str) -> Optional[Dict]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM forum_articles WHERE article_id = ?", (article_id,)
            ).fetchone()
        return dict(row) if row else None

    def append_article_version(self, version: Dict[str, Any]) -> None:
        """Append-only version record. Never updates existing rows."""
        sql = """
        INSERT INTO forum_article_versions
            (article_id, version_seq, captured_at, body_hash, title, change_type)
        VALUES
            (:article_id, :version_seq, :captured_at, :body_hash, :title, :change_type)
        """
        with self._conn() as conn:
            conn.execute(sql, version)

    def get_article_versions(self, article_id: str) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_article_versions WHERE article_id = ? ORDER BY version_seq",
                (article_id,)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Forum Comments
    # ------------------------------------------------------------------

    def insert_comment(self, comment: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_comments
            (article_id, sequence, author_display_id, tag, text,
             comment_time, time_precision, first_seen_at)
        VALUES
            (:article_id, :sequence, :author_display_id, :tag, :text,
             :comment_time, :time_precision, :first_seen_at)
        """
        with self._conn() as conn:
            conn.execute(sql, comment)

    def get_comments(self, article_id: str) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_comments WHERE article_id = ? ORDER BY sequence",
                (article_id,)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Edit / Deletion Events (append-only)
    # ------------------------------------------------------------------

    def append_edit_event(self, event: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_edit_events (article_id, edited_at, edit_seq, note)
        VALUES (:article_id, :edited_at, :edit_seq, :note)
        """
        with self._conn() as conn:
            conn.execute(sql, event)

    def append_deletion_event(self, event: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_deletion_events (article_id, detected_at, deletion_type, prior_title)
        VALUES (:article_id, :detected_at, :deletion_type, :prior_title)
        """
        with self._conn() as conn:
            conn.execute(sql, event)

    # ------------------------------------------------------------------
    # Symbol Mentions / Signals
    # ------------------------------------------------------------------

    def insert_symbol_mention(self, mention: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_symbol_mentions
            (article_id, symbol, match_confidence, context_snippet, mentioned_at)
        VALUES (:article_id, :symbol, :match_confidence, :context_snippet, :mentioned_at)
        """
        with self._conn() as conn:
            conn.execute(sql, mention)

    def insert_topic_signal(self, signal: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_topic_signals
            (article_id, topic_label, evidence_terms, model_version, scored_at)
        VALUES (:article_id, :topic_label, :evidence_terms, :model_version, :scored_at)
        """
        with self._conn() as conn:
            conn.execute(sql, signal)

    def insert_sentiment_signal(self, signal: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_sentiment_signals
            (article_id, target_symbol, polarity, stance, confidence,
             sarcasm_risk, model_version, scored_at)
        VALUES (:article_id, :target_symbol, :polarity, :stance, :confidence,
                :sarcasm_risk, :model_version, :scored_at)
        """
        with self._conn() as conn:
            conn.execute(sql, signal)

    def insert_engagement_signal(self, signal: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_engagement_signals
            (article_id, total_comments, unique_commenters, push_count,
             boo_count, neutral_count, velocity_1h, computed_at)
        VALUES (:article_id, :total_comments, :unique_commenters, :push_count,
                :boo_count, :neutral_count, :velocity_1h, :computed_at)
        """
        with self._conn() as conn:
            conn.execute(sql, signal)

    def insert_credibility_signal(self, signal: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_credibility_signals
            (article_id, has_official_link, has_concrete_numbers, has_unsupported_claim,
             has_rumor_terms, has_guaranteed_profit, edit_risk, deletion_risk,
             content_credibility, scored_at)
        VALUES (:article_id, :has_official_link, :has_concrete_numbers, :has_unsupported_claim,
                :has_rumor_terms, :has_guaranteed_profit, :edit_risk, :deletion_risk,
                :content_credibility, :scored_at)
        """
        with self._conn() as conn:
            conn.execute(sql, signal)

    def insert_coordination_risk(self, risk: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_coordination_risks (article_id, risk_level, risk_signals, assessed_at)
        VALUES (:article_id, :risk_level, :risk_signals, :assessed_at)
        """
        with self._conn() as conn:
            conn.execute(sql, risk)

    def insert_manipulation_risk(self, risk: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO forum_manipulation_risks (article_id, risk_level, risk_signals, assessed_at)
        VALUES (:article_id, :risk_level, :risk_signals, :assessed_at)
        """
        with self._conn() as conn:
            conn.execute(sql, risk)

    # ------------------------------------------------------------------
    # Market Sentiment Snapshots
    # ------------------------------------------------------------------

    def insert_market_sentiment_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """formal_standalone is always 0 (False)."""
        snap = dict(snapshot)
        snap["formal_standalone"] = 0  # NEVER True
        sql = """
        INSERT INTO market_sentiment_snapshots
            (window, dimension, dimension_value, article_count, bullish_count,
             bearish_count, neutral_count, disagreement, confidence,
             formal_standalone, computed_at)
        VALUES (:window, :dimension, :dimension_value, :article_count, :bullish_count,
                :bearish_count, :neutral_count, :disagreement, :confidence,
                :formal_standalone, :computed_at)
        """
        with self._conn() as conn:
            conn.execute(sql, snap)

    # ------------------------------------------------------------------
    # Fetch Runs
    # ------------------------------------------------------------------

    def start_fetch_run(self, source_id: str, dry_run: bool = True) -> int:
        sql = """
        INSERT INTO forum_fetch_runs (source_id, started_at, dry_run, status)
        VALUES (?, ?, ?, 'RUNNING')
        """
        with self._conn() as conn:
            cur = conn.execute(sql, (source_id, datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z', int(dry_run)))
            return cur.lastrowid

    def complete_fetch_run(self, run_id: int, articles_found: int,
                           pages_fetched: int, status: str = "COMPLETE",
                           notes: str = "") -> None:
        sql = """
        UPDATE forum_fetch_runs
        SET completed_at = ?, articles_found = ?, pages_fetched = ?, status = ?, notes = ?
        WHERE run_id = ?
        """
        with self._conn() as conn:
            conn.execute(sql, (
                datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
                articles_found, pages_fetched, status, notes, run_id
            ))

    def list_fetch_runs(self, source_id: Optional[str] = None) -> List[Dict]:
        with self._conn() as conn:
            if source_id:
                rows = conn.execute(
                    "SELECT * FROM forum_fetch_runs WHERE source_id = ? ORDER BY run_id DESC",
                    (source_id,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM forum_fetch_runs ORDER BY run_id DESC LIMIT 100"
                ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Health / introspection
    # ------------------------------------------------------------------

    def get_table_count(self) -> int:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT COUNT(*) as cnt FROM sqlite_master WHERE type='table'"
            ).fetchone()
        return rows["cnt"] if rows else 0

    def health_check(self) -> Dict[str, Any]:
        table_count = self.get_table_count()
        return {
            "db_path": self._db_path,
            "table_count": table_count,
            "expected_tables": self.TABLE_COUNT,
            "ok": table_count >= self.TABLE_COUNT,
            "full_ip_stored": False,
            "formal_standalone_allowed": False,
            "authority": "SUPPLEMENTARY",
        }
