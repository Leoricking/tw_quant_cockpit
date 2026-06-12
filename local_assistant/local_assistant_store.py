"""
local_assistant/local_assistant_store.py — LocalResearchAssistantStore for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API.
[!] Local assistant does not enable trading. Output never committed.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import List

from local_assistant.assistant_schema import ResearchAssistantAnswer

logger = logging.getLogger(__name__)

_DEFAULT_OUTPUT_DIR = "data/backtest_results/local_assistant"


class LocalResearchAssistantStore:
    """Persists local assistant answers, sources, and summaries to CSV.

    Output directory: data/backtest_results/local_assistant/ (gitignored).

    [!] Research Only. No Real Orders. No external API.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, output_dir: str = _DEFAULT_OUTPUT_DIR) -> None:
        if not os.path.isabs(output_dir):
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base, output_dir)
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    def save_answer(self, answer: ResearchAssistantAnswer) -> str:
        """Save a single answer to local_assistant_answers.csv (appends row)."""
        return self.save_answers([answer])

    def save_answers(self, answers: List[ResearchAssistantAnswer]) -> str:
        """Save list of answers to local_assistant_answers.csv."""
        path = os.path.join(self._output_dir, "local_assistant_answers.csv")
        fieldnames = [
            "timestamp", "question", "status", "confidence",
            "source_count", "route_count", "answer_excerpt",
            "no_real_orders", "broker_disabled", "research_only",
            "not_investment_advice", "external_api_used",
        ]
        file_exists = os.path.isfile(path)
        try:
            with open(path, "a", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                for ans in answers:
                    writer.writerow({
                        "timestamp":           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "question":            ans.question[:200],
                        "status":              ans.status,
                        "confidence":          ans.confidence,
                        "source_count":        len(ans.sources),
                        "route_count":         len(ans.module_routes),
                        "answer_excerpt":      ans.answer[:300].replace("\n", " "),
                        "no_real_orders":      ans.no_real_orders,
                        "broker_disabled":     ans.broker_disabled,
                        "research_only":       ans.research_only,
                        "not_investment_advice": ans.not_investment_advice,
                        "external_api_used":   ans.external_api_used,
                    })
            return path
        except Exception as exc:
            logger.warning("save_answers failed: %s", exc)
            return path

    def save_sources(self, sources) -> str:
        """Save source records to local_assistant_sources.csv."""
        path = os.path.join(self._output_dir, "local_assistant_sources.csv")
        fieldnames = ["timestamp", "source_id", "title", "path", "category", "module", "score", "source_type"]
        file_exists = os.path.isfile(path)
        try:
            with open(path, "a", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for src in sources:
                    if hasattr(src, "to_dict"):
                        d = src.to_dict()
                    elif isinstance(src, dict):
                        d = src
                    else:
                        d = {}
                    writer.writerow({
                        "timestamp":   ts,
                        "source_id":   d.get("source_id", ""),
                        "title":       d.get("title", ""),
                        "path":        d.get("path", ""),
                        "category":    d.get("category", ""),
                        "module":      d.get("module", ""),
                        "score":       d.get("score", 0.0),
                        "source_type": d.get("source_type", ""),
                    })
            return path
        except Exception as exc:
            logger.warning("save_sources failed: %s", exc)
            return path

    def save_summary(self, summary: dict) -> str:
        """Save a summary dict to local_assistant_summary.csv."""
        path = os.path.join(self._output_dir, "local_assistant_summary.csv")
        fieldnames = list(summary.keys())
        file_exists = os.path.isfile(path)
        try:
            with open(path, "a", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
                if not file_exists:
                    writer.writeheader()
                writer.writerow(summary)
            return path
        except Exception as exc:
            logger.warning("save_summary failed: %s", exc)
            return path

    def load_recent_answers(self, limit: int = 20) -> List[dict]:
        """Load most recent answers from local_assistant_answers.csv."""
        path = os.path.join(self._output_dir, "local_assistant_answers.csv")
        if not os.path.isfile(path):
            return []
        try:
            rows = []
            with open(path, "r", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    rows.append(dict(row))
            return rows[-limit:] if len(rows) > limit else rows
        except Exception as exc:
            logger.warning("load_recent_answers failed: %s", exc)
            return []
