"""
Documentation Summary Builder — v1.0.5 Documentation & User Guide Polish.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Dict

CORE_DOC_NAMES = [
    "README.md",
    "docs/index.md",
    "docs/user_guide_v1.0.md",
    "docs/gui_user_guide_v1.0.md",
    "docs/cli_cookbook_v1.0.md",
    "docs/daily_workflow_sop_v1.0.md",
    "docs/troubleshooting_v1.0.md",
    "docs/safety_guide_v1.0.md",
    "docs/version_map_v1.0.md",
    "docs/handoff_guide_v1.0.md",
]

DOC_CATEGORIES_LABELS = {
    "start_here": "Start Here (User-facing guides)",
    "operation": "Operation (CLI, GUI, Troubleshooting)",
    "release": "Release (Notes, Maps, Roadmap, Handoff)",
    "system": "System (Module docs)",
    "other": "Other",
}


class DocumentationSummaryBuilder:
    """
    Summarizes documentation status for console display.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir

    def list_core_docs(self) -> Dict[str, bool]:
        """Return {doc_name: exists} for all core docs."""
        return {
            name: (Path(self.base_dir) / name).exists()
            for name in CORE_DOC_NAMES
        }

    def list_missing_docs(self) -> List[str]:
        return [name for name, exists in self.list_core_docs().items() if not exists]

    def list_docs_by_category(self) -> Dict[str, List[str]]:
        try:
            from documentation.docs_indexer import DocumentationIndexer
            indexer = DocumentationIndexer(self.base_dir)
            indexer.build_doc_manifest()
            return indexer.categorize_docs()
        except Exception:
            return {}

    def build_summary(self) -> dict:
        core_docs = self.list_core_docs()
        present = sum(1 for v in core_docs.values() if v)
        missing = self.list_missing_docs()
        by_cat = self.list_docs_by_category()
        total_docs = sum(len(v) for v in by_cat.values())
        return {
            "core_docs_present": present,
            "core_docs_total": len(CORE_DOC_NAMES),
            "core_docs_missing": missing,
            "total_docs_indexed": total_docs,
            "docs_by_category": by_cat,
            "research_only": True,
            "no_real_orders": True,
        }

    def summarize_for_console(self) -> str:
        summary = self.build_summary()
        lines = [
            "=" * 60,
            "TW Quant Cockpit — Documentation Summary",
            "Research Only | No Real Orders | Production Trading BLOCKED",
            "=" * 60,
            f"  Core Docs:    {summary['core_docs_present']}/{summary['core_docs_total']} present",
            f"  Total Docs:   {summary['total_docs_indexed']} indexed",
        ]
        if summary["core_docs_missing"]:
            lines.append(f"  Missing:      {summary['core_docs_missing']}")
        else:
            lines.append("  Missing:      none")
        lines.append("-" * 60)
        for cat, docs in summary["docs_by_category"].items():
            label = DOC_CATEGORIES_LABELS.get(cat, cat)
            lines.append(f"  {label}: {len(docs)}")
        lines.append("=" * 60)
        return "\n".join(lines)
