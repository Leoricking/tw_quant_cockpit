"""
replay/replay_data_source.py — ReplayDataSource v1.2.0

Loads historical data sliced to replay_date.
real mode: does NOT fallback to mock.
mock mode: marks DEMO_ONLY.
Missing optional data (chips, fundamental): shows unavailable, does NOT crash.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Section status constants
STATUS_AVAILABLE = "AVAILABLE"
STATUS_PARTIAL = "PARTIAL"
STATUS_APPROXIMATE = "APPROXIMATE"
STATUS_UNAVAILABLE = "UNAVAILABLE"
STATUS_BLOCKED = "BLOCKED"


class ReplayDataSource:
    """
    Loads historical data sliced to replay_date.
    real mode: does NOT fallback to mock.
    mock mode: must mark DEMO_ONLY.
    Missing optional data (chips, fundamental): show unavailable, don't crash.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root=None, mode: str = "real"):
        self.repo_root = Path(repo_root) if repo_root else Path(".")
        self.mode = mode
        self._section_status: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # Daily price data
    # ------------------------------------------------------------------

    def load_daily(self, symbol: str, start: Optional[str] = None, end: Optional[str] = None, mode: Optional[str] = None) -> Optional[Any]:
        """Load daily OHLCV data. Returns DataFrame or None."""
        try:
            import pandas as pd
        except ImportError:
            logger.warning("[ReplayDataSource] pandas not available")
            return None

        _mode = mode or self.mode
        fpath = self._find_price_file(symbol)
        if fpath is None:
            self._section_status["price"] = STATUS_UNAVAILABLE
            if _mode == "real":
                logger.warning("[ReplayDataSource] No real price data for %s", symbol)
                return None
            else:
                logger.info("[ReplayDataSource] DEMO_ONLY mock — no real price file for %s", symbol)
                return None

        try:
            df = pd.read_csv(str(fpath))
            df = self._normalize_columns(df)
            if df is None or df.empty:
                self._section_status["price"] = STATUS_UNAVAILABLE
                return None
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df = df.dropna(subset=["date"])
                df = df.sort_values("date")
                df["date"] = df["date"].dt.strftime("%Y-%m-%d")
            if start:
                df = df[df["date"] >= start]
            if end:
                df = df[df["date"] <= end]
            self._section_status["price"] = STATUS_AVAILABLE
            return df.reset_index(drop=True)
        except Exception as exc:
            logger.warning("[ReplayDataSource] Error loading price for %s: %s", symbol, exc)
            self._section_status["price"] = STATUS_UNAVAILABLE
            return None

    def load_price_history(self, symbol: str, replay_date: str) -> Optional[Any]:
        """Load price history up to and including replay_date only."""
        return self.load_daily(symbol, end=replay_date)

    # ------------------------------------------------------------------
    # Chips / institutional data
    # ------------------------------------------------------------------

    def load_chips_history(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Load chips/institutional data up to replay_date. Returns dict or None."""
        try:
            import pandas as pd
        except ImportError:
            self._section_status["chips"] = STATUS_UNAVAILABLE
            return None

        fpath = self._find_chips_file(symbol)
        if fpath is None:
            self._section_status["chips"] = STATUS_UNAVAILABLE
            return None

        try:
            df = pd.read_csv(str(fpath))
            df = self._normalize_columns(df)
            if df is None or df.empty:
                self._section_status["chips"] = STATUS_UNAVAILABLE
                return None
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df = df.dropna(subset=["date"])
                df["date"] = df["date"].dt.strftime("%Y-%m-%d")
                df = df[df["date"] <= replay_date].sort_values("date")
            self._section_status["chips"] = STATUS_AVAILABLE
            return {"data": df.to_dict("records"), "symbol": symbol, "replay_date": replay_date}
        except Exception as exc:
            logger.warning("[ReplayDataSource] Error loading chips for %s: %s", symbol, exc)
            self._section_status["chips"] = STATUS_UNAVAILABLE
            return None

    # ------------------------------------------------------------------
    # Fundamental data
    # ------------------------------------------------------------------

    def load_fundamental_history(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Load fundamental data with announcement_date <= replay_date."""
        try:
            import pandas as pd
        except ImportError:
            self._section_status["fundamental"] = STATUS_UNAVAILABLE
            return None

        fpath = self._find_fundamental_file(symbol)
        if fpath is None:
            self._section_status["fundamental"] = STATUS_UNAVAILABLE
            return None

        try:
            df = pd.read_csv(str(fpath))
            df = self._normalize_columns(df)
            if df is None or df.empty:
                self._section_status["fundamental"] = STATUS_UNAVAILABLE
                return None

            timing_approximate = False
            if "announcement_date" in df.columns:
                df["announcement_date"] = pd.to_datetime(df["announcement_date"], errors="coerce")
                # Include rows where announcement_date is missing (timing approximate) or <= replay_date
                mask_known = df["announcement_date"].notna() & (df["announcement_date"].dt.strftime("%Y-%m-%d") <= replay_date)
                mask_unknown = df["announcement_date"].isna()
                if mask_unknown.any():
                    timing_approximate = True
                df = df[mask_known | mask_unknown]
            else:
                timing_approximate = True
                self._section_status["fundamental"] = STATUS_APPROXIMATE

            if not timing_approximate:
                self._section_status["fundamental"] = STATUS_AVAILABLE
            else:
                self._section_status["fundamental"] = STATUS_APPROXIMATE

            return {
                "data": df.to_dict("records"),
                "symbol": symbol,
                "replay_date": replay_date,
                "timing_approximate": timing_approximate,
            }
        except Exception as exc:
            logger.warning("[ReplayDataSource] Error loading fundamental for %s: %s", symbol, exc)
            self._section_status["fundamental"] = STATUS_UNAVAILABLE
            return None

    def load_revenue_history(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Load revenue data with announcement_date <= replay_date."""
        return self.load_fundamental_history(symbol, replay_date)

    # ------------------------------------------------------------------
    # Quality and strategy context
    # ------------------------------------------------------------------

    def load_quality_context(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Load quality gate context at replay_date."""
        try:
            from data_freshness.freshness_store import FreshnessStore
            store = FreshnessStore(repo_root=str(self.repo_root))
            result = store.load_symbol(symbol)
            if result:
                self._section_status["quality"] = STATUS_AVAILABLE
                return {"symbol": symbol, "replay_date": replay_date, "freshness": result}
        except Exception:
            pass

        self._section_status["quality"] = STATUS_UNAVAILABLE
        return {"symbol": symbol, "replay_date": replay_date, "status": STATUS_UNAVAILABLE}

    def load_strategy_context(self, symbol: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Load strategy knowledge at replay_date."""
        try:
            from strategy_knowledge.knowledge_store import KnowledgeStore
            store = KnowledgeStore(repo_root=str(self.repo_root))
            result = store.load_symbol(symbol)
            if result:
                self._section_status["strategy"] = STATUS_AVAILABLE
                return {"symbol": symbol, "replay_date": replay_date, "knowledge": result}
        except Exception:
            pass

        self._section_status["strategy"] = STATUS_UNAVAILABLE
        return {"symbol": symbol, "replay_date": replay_date, "status": STATUS_UNAVAILABLE}

    # ------------------------------------------------------------------
    # Status and availability
    # ------------------------------------------------------------------

    def source_status(self, symbol: str) -> Dict[str, str]:
        """Returns dict of section -> status."""
        return dict(self._section_status)

    def available_sections(self, symbol: str, replay_date: str) -> List[str]:
        """Returns list of available section names."""
        return [k for k, v in self._section_status.items() if v in (STATUS_AVAILABLE, STATUS_PARTIAL, STATUS_APPROXIMATE)]

    def data_limitations(self, symbol: str, replay_date: str) -> List[str]:
        """Returns list of limitation strings."""
        limitations = []
        for section, status in self._section_status.items():
            if status == STATUS_UNAVAILABLE:
                limitations.append(f"{section.upper()}_UNAVAILABLE")
            elif status == STATUS_APPROXIMATE:
                limitations.append(f"{section.upper()}_TIMING_APPROXIMATE")
            elif status == STATUS_PARTIAL:
                limitations.append(f"{section.upper()}_PARTIAL")
            elif status == STATUS_BLOCKED:
                limitations.append(f"{section.upper()}_BLOCKED")
        return limitations

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _normalize_columns(self, df) -> Optional[Any]:
        """Lowercase all column names."""
        if df is None:
            return None
        df.columns = [c.lower().strip() for c in df.columns]
        return df

    def _find_price_file(self, symbol: str) -> Optional[Path]:
        """Find price CSV file for symbol."""
        candidates = [
            self.repo_root / "data" / f"{symbol}.csv",
            self.repo_root / "data" / f"{symbol}_daily.csv",
            self.repo_root / "data" / "market" / f"{symbol}.csv",
            self.repo_root / "data" / "price" / f"{symbol}.csv",
            self.repo_root / "data" / "daily" / f"{symbol}.csv",
        ]
        for p in candidates:
            if p.exists():
                return p
        import glob
        patterns = [
            str(self.repo_root / "data" / f"{symbol}*.csv"),
            str(self.repo_root / "data" / "market" / f"{symbol}*.csv"),
        ]
        for pattern in patterns:
            matches = glob.glob(pattern)
            if matches:
                return Path(matches[0])
        return None

    def _find_chips_file(self, symbol: str) -> Optional[Path]:
        """Find chips CSV file for symbol."""
        candidates = [
            self.repo_root / "data" / "chips" / f"{symbol}.csv",
            self.repo_root / "data" / f"{symbol}_chips.csv",
            self.repo_root / "data" / "institutional" / f"{symbol}.csv",
        ]
        for p in candidates:
            if p.exists():
                return p
        return None

    def _find_fundamental_file(self, symbol: str) -> Optional[Path]:
        """Find fundamental CSV file for symbol."""
        candidates = [
            self.repo_root / "data" / "fundamental" / f"{symbol}.csv",
            self.repo_root / "data" / f"{symbol}_fundamental.csv",
            self.repo_root / "data" / "financials" / f"{symbol}.csv",
        ]
        for p in candidates:
            if p.exists():
                return p
        return None
