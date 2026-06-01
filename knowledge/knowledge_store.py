"""
knowledge/knowledge_store.py — StrategyKnowledgeStore: CSV persistence for knowledge items (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Never writes token/password/env vars to CSV.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/strategy_knowledge"

# Fields that must never be written to CSV (security)
_BLOCKED_FIELD_NAMES = {
    "token", "password", "secret", "api_key", "access_key",
    "env", "credential", "private_key", "auth",
}


def _sanitize_row(row: dict) -> dict:
    """Remove any fields whose names match blocked security patterns."""
    return {
        k: v for k, v in row.items()
        if not any(blocked in k.lower() for blocked in _BLOCKED_FIELD_NAMES)
    }


def _write_csv(path: str, rows: list, fieldnames: Optional[list] = None) -> None:
    """Write a list of dicts to a CSV file."""
    if not rows:
        # Write empty file with headers if fieldnames provided
        if fieldnames:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()
        return
    sanitized = [_sanitize_row(r) for r in rows]
    keys = fieldnames or list(sanitized[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sanitized)


def _read_csv(path: str) -> list:
    """Read a CSV file into a list of dicts. Returns empty list if file not found."""
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return list(reader)
    except Exception as exc:
        logger.warning("StrategyKnowledgeStore._read_csv: cannot read %s — %s", path, exc)
        return []


class StrategyKnowledgeStore:
    """
    CSV-based persistence layer for strategy knowledge items.

    Safety invariants:
      read_only = True
      no_real_orders = True
      Never writes token/password/env vars to CSV.
    """

    read_only: bool = True
    no_real_orders: bool = True

    def __init__(self, output_dir: str = _DEFAULT_OUTPUT_DIR):
        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._output_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._output_dir, filename)

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_items(self, items: list) -> str:
        """
        Write knowledge items to knowledge_items.csv.
        Returns path to written file.
        """
        path = self._path("knowledge_items.csv")
        rows = [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
        _write_csv(path, rows)
        logger.info("StrategyKnowledgeStore: saved %d items → %s", len(rows), path)
        return path

    def save_sources(self, sources: list) -> str:
        """Write transcript sources to sources.csv. Returns path."""
        path = self._path("sources.csv")
        rows = [s.to_dict() if hasattr(s, "to_dict") else s for s in sources]
        _write_csv(path, rows)
        logger.info("StrategyKnowledgeStore: saved %d sources → %s", len(rows), path)
        return path

    def save_rule_candidates(self, rule_candidates: list) -> str:
        """Write rule candidates to rule_candidates.csv. Returns path."""
        path = self._path("rule_candidates.csv")
        _write_csv(path, rule_candidates)
        logger.info("StrategyKnowledgeStore: saved %d rule_candidates → %s", len(rule_candidates), path)
        return path

    def save_avoid_conditions(self, items: list) -> str:
        """Write avoid condition items to avoid_conditions.csv. Returns path."""
        path = self._path("avoid_conditions.csv")
        rows = [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
        _write_csv(path, rows)
        logger.info("StrategyKnowledgeStore: saved %d avoid_conditions → %s", len(rows), path)
        return path

    def save_risk_conditions(self, items: list) -> str:
        """Write risk condition items to risk_conditions.csv. Returns path."""
        path = self._path("risk_conditions.csv")
        rows = [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
        _write_csv(path, rows)
        logger.info("StrategyKnowledgeStore: saved %d risk_conditions → %s", len(rows), path)
        return path

    def save_factor_candidates(self, items: list) -> str:
        """Write factor candidate items to factor_candidates.csv. Returns path."""
        path = self._path("factor_candidates.csv")
        rows = [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
        _write_csv(path, rows)
        logger.info("StrategyKnowledgeStore: saved %d factor_candidates → %s", len(rows), path)
        return path

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_items(self) -> list:
        """
        Load knowledge items from knowledge_items.csv.
        Returns list of dicts. Returns empty list if file not found — no crash.
        """
        return _read_csv(self._path("knowledge_items.csv"))

    def load_sources(self) -> list:
        """Load sources from sources.csv. Returns list of dicts."""
        return _read_csv(self._path("sources.csv"))

    def load_rule_candidates(self) -> list:
        """Load rule candidates from rule_candidates.csv. Returns list of dicts."""
        return _read_csv(self._path("rule_candidates.csv"))

    def load_avoid_conditions(self) -> list:
        """Load avoid conditions from avoid_conditions.csv. Returns list of dicts."""
        return _read_csv(self._path("avoid_conditions.csv"))

    def load_risk_conditions(self) -> list:
        """Load risk conditions from risk_conditions.csv. Returns list of dicts."""
        return _read_csv(self._path("risk_conditions.csv"))

    def load_factor_candidates(self) -> list:
        """Load factor candidates from factor_candidates.csv. Returns list of dicts."""
        return _read_csv(self._path("factor_candidates.csv"))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_summary(self) -> dict:
        """
        Build a summary dict with item counts per category and latest ingestion timestamp.

        Returns dict with:
          total_items, by_category (dict), latest_ingestion_at, output_dir
        """
        items = self.load_items()
        by_category: dict[str, int] = {}
        for row in items:
            cat = row.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1

        # Try to find latest ingestion time from created_at field
        latest_at = ""
        for row in items:
            ts = row.get("created_at", "")
            if ts and ts > latest_at:
                latest_at = ts

        sources = self.load_sources()
        rule_candidates = self.load_rule_candidates()
        factor_candidates = self.load_factor_candidates()
        avoid_conditions = self.load_avoid_conditions()
        risk_conditions = self.load_risk_conditions()

        return {
            "total_items": len(items),
            "by_category": by_category,
            "latest_ingestion_at": latest_at,
            "output_dir": self._output_dir,
            "sources_count": len(sources),
            "rule_candidates_count": len(rule_candidates),
            "factor_candidates_count": len(factor_candidates),
            "avoid_conditions_count": len(avoid_conditions),
            "risk_conditions_count": len(risk_conditions),
            "research_only": True,
            "no_real_orders": True,
        }
