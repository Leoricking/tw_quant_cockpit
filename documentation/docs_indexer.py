"""
Documentation Indexer — v1.0.5 Documentation & User Guide Polish.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import csv
import datetime
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional

DOCS_DIR = "docs"
OUTPUT_DIR = "data/backtest_results/documentation"

DOC_CATEGORIES = {
    "start_here": ["user_guide", "daily_workflow_sop", "safety_guide"],
    "operation": ["gui_user_guide", "cli_cookbook", "troubleshooting"],
    "release": ["release_notes", "version_map", "roadmap", "handoff_guide"],
    "system": ["research_trading_cockpit_stable", "strategy_lab", "strategy_validation",
               "evidence_graph", "crash_reversal", "data_report_hygiene",
               "gui_stability", "regression_hardening", "documentation"],
}


@dataclass
class DocManifestEntry:
    filename: str
    title: str = ""
    category: str = "uncategorized"
    size_bytes: int = 0
    has_safety_banner: bool = False
    has_research_only: bool = False
    last_modified: str = ""


class DocumentationIndexer:
    """
    Indexes all documentation files.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self._manifest: List[DocManifestEntry] = []

    def _docs_path(self) -> Path:
        return Path(self.base_dir) / DOCS_DIR

    def collect_docs(self) -> List[Path]:
        docs_dir = self._docs_path()
        if not docs_dir.exists():
            return []
        return sorted(docs_dir.glob("*.md"))

    def _extract_title(self, path: Path) -> str:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for line in lines[:5]:
                if line.startswith("# "):
                    return line[2:].strip()
        except Exception:
            pass
        return path.stem

    def _categorize(self, filename: str) -> str:
        lower = filename.lower()
        for cat, keywords in DOC_CATEGORIES.items():
            for kw in keywords:
                if kw.replace("_", "") in lower.replace("_", ""):
                    return cat
        return "other"

    def _has_safety_phrase(self, text: str, phrase: str) -> bool:
        return phrase in text

    def build_doc_manifest(self) -> List[DocManifestEntry]:
        self._manifest = []
        for doc_path in self.collect_docs():
            try:
                text = doc_path.read_text(encoding="utf-8", errors="replace")
                size = doc_path.stat().st_size
                mtime = datetime.datetime.fromtimestamp(doc_path.stat().st_mtime).date().isoformat()
            except Exception:
                text, size, mtime = "", 0, ""
            entry = DocManifestEntry(
                filename=doc_path.name,
                title=self._extract_title(doc_path),
                category=self._categorize(doc_path.stem),
                size_bytes=size,
                has_safety_banner="Research Only" in text or "No Real Orders" in text,
                has_research_only="Research Only" in text,
                last_modified=mtime,
            )
            self._manifest.append(entry)
        return self._manifest

    def categorize_docs(self) -> Dict[str, List[str]]:
        if not self._manifest:
            self.build_doc_manifest()
        result: Dict[str, List[str]] = {}
        for entry in self._manifest:
            result.setdefault(entry.category, []).append(entry.filename)
        return result

    def detect_missing_links(self) -> List[str]:
        """Return list of core doc names that are missing."""
        from documentation.docs_health_check import CORE_DOCS
        missing = []
        for name, rel in CORE_DOCS.items():
            if not (Path(self.base_dir) / rel).exists():
                missing.append(rel)
        return missing

    def detect_stale_docs(self, days_threshold: int = 365) -> List[str]:
        """Return docs not modified in over days_threshold days."""
        stale = []
        cutoff = datetime.date.today() - datetime.timedelta(days=days_threshold)
        for entry in self._manifest:
            if entry.last_modified:
                try:
                    mod_date = datetime.date.fromisoformat(entry.last_modified)
                    if mod_date < cutoff:
                        stale.append(entry.filename)
                except ValueError:
                    pass
        return stale

    def detect_duplicate_titles(self) -> List[str]:
        """Return titles that appear more than once."""
        from collections import Counter
        titles = [e.title for e in self._manifest if e.title]
        return [t for t, c in Counter(titles).items() if c > 1]

    def build_navigation_map(self) -> Dict[str, str]:
        """Return {filename: category} navigation map."""
        if not self._manifest:
            self.build_doc_manifest()
        return {e.filename: e.category for e in self._manifest}

    def save_manifest_csv(self, output_dir: Optional[str] = None) -> str:
        if not self._manifest:
            self.build_doc_manifest()
        out_dir = output_dir or os.path.join(self.base_dir, OUTPUT_DIR)
        os.makedirs(out_dir, exist_ok=True)
        today = datetime.date.today().isoformat()
        path = os.path.join(out_dir, f"docs_manifest_{today}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "filename", "title", "category", "size_bytes",
                "has_safety_banner", "has_research_only", "last_modified",
            ])
            writer.writeheader()
            for entry in self._manifest:
                writer.writerow({
                    "filename": entry.filename,
                    "title": entry.title,
                    "category": entry.category,
                    "size_bytes": entry.size_bytes,
                    "has_safety_banner": entry.has_safety_banner,
                    "has_research_only": entry.has_research_only,
                    "last_modified": entry.last_modified,
                })
        return path
