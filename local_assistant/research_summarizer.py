"""
local_assistant/research_summarizer.py — ResearchSummarizer for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API. Local rule-based summarizer only.
"""
from __future__ import annotations

import logging
from typing import List

from local_assistant.assistant_schema import (
    CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, CONFIDENCE_LOW, CONFIDENCE_INSUFFICIENT,
)

logger = logging.getLogger(__name__)

_STANDARD_LIMITATIONS = [
    "Local KB search only — results depend on indexed local files.",
    "No external LLM or embedding API used.",
    "Not investment advice. Research use only.",
    "No real orders. Broker execution disabled.",
    "VALIDATED does not enable trading.",
    "Answers reflect locally indexed document summaries, not live market data.",
    "Confidence is based on number of matching documents, not semantic quality.",
]


class ResearchSummarizer:
    """Local rule-based summarizer. No LLM API. No network. No fabrication.

    [!] Research Only. No Real Orders. No external API.
    [!] Local assistant does not enable trading.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def summarize_results(self, question: str, results) -> str:
        """Build a short readable summary from KB results.

        Returns 'No relevant documents found...' if no results.
        """
        if not results:
            return "No relevant documents found for this query."

        n = len(results)
        titles = []
        for item in results[:5]:
            if hasattr(item, "title"):
                titles.append(item.title)
            elif isinstance(item, dict):
                titles.append(str(item.get("title", "Untitled")))

        title_str = "; ".join(titles) if titles else "(no titles)"
        summary_lines = [
            f"Found {n} relevant document(s) for: '{question}'.",
            f"Top sources: {title_str}.",
            "Review the sources below for research details.",
            "[!] Not investment advice. No real orders. Local documents only.",
        ]
        return " ".join(summary_lines)

    def summarize_sources(self, results) -> List[dict]:
        """Return list of {{title, path, category, module}} dicts from results."""
        sources = []
        for item in results:
            if hasattr(item, "title"):
                sources.append({
                    "title":    getattr(item, "title", ""),
                    "path":     getattr(item, "path", ""),
                    "category": getattr(item, "category", ""),
                    "module":   getattr(item, "module", ""),
                })
            elif isinstance(item, dict):
                sources.append({
                    "title":    str(item.get("title", "")),
                    "path":     str(item.get("path", "")),
                    "category": str(item.get("category", "")),
                    "module":   str(item.get("module", "")),
                })
        return sources

    def summarize_limitations(self, results) -> List[str]:
        """Return standard limitations list."""
        return list(_STANDARD_LIMITATIONS)

    def infer_confidence(self, results) -> str:
        """HIGH if >=5 results, MEDIUM if 2-4, LOW if 1, INSUFFICIENT if 0."""
        n = len(results) if results else 0
        if n >= 5:
            return CONFIDENCE_HIGH
        if n >= 2:
            return CONFIDENCE_MEDIUM
        if n == 1:
            return CONFIDENCE_LOW
        return CONFIDENCE_INSUFFICIENT

    def build_citations(self, results) -> str:
        """Return formatted citation string listing source titles and paths."""
        if not results:
            return "(No sources found)"
        lines = []
        for i, item in enumerate(results, 1):
            if hasattr(item, "title"):
                title = getattr(item, "title", "")
                path = getattr(item, "path", "")
            elif isinstance(item, dict):
                title = str(item.get("title", ""))
                path = str(item.get("path", ""))
            else:
                title = str(item)
                path = ""
            lines.append(f"  [{i}] {title} — {path}")
        return "\n".join(lines)
