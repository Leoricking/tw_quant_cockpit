"""
knowledge_base/kb_indexer.py — KnowledgeBaseIndexer for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Indexer. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

import hashlib
import logging
import os
from datetime import datetime
from typing import List

from knowledge_base.kb_schema import (
    KnowledgeBaseItem,
    KnowledgeBaseSummary,
    DOC, EXAMPLE, TEMPLATE, REPORT, GUI, WORKFLOW, SAFETY, RELEASE, UNKNOWN,
    STRATEGY_MEMORY, EVIDENCE_GRAPH,
    MARKDOWN, REPORT_MD, GUI_REGISTRY, CLI_COMMAND, SOURCE_UNKNOWN,
    TEMPLATE_SRC,
)

logger = logging.getLogger(__name__)

_SAFETY_KEYWORDS = [
    "safety", "no real orders", "blocked", "research only", "forbidden",
    "no broker", "not investment advice",
]
_MAX_MD_LINES = 200


class KnowledgeBaseIndexer:
    """Build an index of all knowledge base items.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    no_real_orders     = True
    broker_disabled    = True
    research_only      = True
    production_blocked = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/knowledge_base",
    ) -> None:
        self._root = os.path.abspath(project_root)
        self._output_dir = output_dir if os.path.isabs(output_dir) else os.path.join(self._root, output_dir)
        self._items: List[KnowledgeBaseItem] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_index(self) -> List[KnowledgeBaseItem]:
        """Run all collect_* methods and return the complete item list."""
        self._items = []
        self.collect_docs()
        self.collect_examples()
        self.collect_templates()
        self.collect_reports()
        self.collect_gui_registry()
        self.collect_cli_commands()
        self.collect_strategy_memory_metadata()
        self.collect_evidence_graph_metadata()
        return list(self._items)

    def build_summary(self, items: List[KnowledgeBaseItem]) -> KnowledgeBaseSummary:
        """Build a KnowledgeBaseSummary from the given item list."""
        docs_count      = sum(1 for i in items if i.category == DOC)
        examples_count  = sum(1 for i in items if i.category == EXAMPLE)
        templates_count = sum(1 for i in items if i.category == TEMPLATE)
        reports_count   = sum(1 for i in items if i.category == REPORT)
        safety_count    = sum(1 for i in items if i.category == SAFETY)
        modules_set     = {i.module for i in items if i.module}
        indexed_paths   = sorted({i.path for i in items if i.path})

        missing = []
        for chk in ["docs", "docs/examples", "docs/templates", "reports"]:
            p = os.path.join(self._root, chk)
            if not os.path.isdir(p):
                missing.append(chk)

        return KnowledgeBaseSummary(
            generated_at=datetime.now().isoformat(),
            version="1.0.7",
            total_items=len(items),
            docs_count=docs_count,
            examples_count=examples_count,
            templates_count=templates_count,
            reports_count=reports_count,
            safety_docs_count=safety_count,
            modules_count=len(modules_set),
            indexed_paths=indexed_paths[:50],
            missing_indexes=missing,
            warnings=[],
            blocked=False,
            no_real_orders=True,
            broker_disabled=True,
            research_only=True,
        )

    # ------------------------------------------------------------------
    # Collectors
    # ------------------------------------------------------------------

    def collect_docs(self) -> None:
        """Scan README.md and docs/*.md."""
        # README.md
        readme = os.path.join(self._root, "README.md")
        if os.path.isfile(readme):
            item = self._make_item(readme, RELEASE, MARKDOWN, "release", ["readme", "overview"])
            self._items.append(item)

        docs_dir = os.path.join(self._root, "docs")
        if not os.path.isdir(docs_dir):
            return
        for fname in os.listdir(docs_dir):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(docs_dir, fname)
            if not os.path.isfile(fpath):
                continue
            # Determine category
            flower = fname.lower()
            if any(k in flower for k in ["safety", "safe"]):
                cat = SAFETY
            elif any(k in flower for k in ["release", "version", "roadmap"]):
                cat = RELEASE
            elif any(k in flower for k in ["workflow"]):
                cat = WORKFLOW
            else:
                cat = DOC
            tags = self._infer_tags(fname)
            item = self._make_item(fpath, cat, MARKDOWN, "docs", tags)
            self._items.append(item)

    def collect_examples(self) -> None:
        """Scan docs/examples/."""
        ex_dir = os.path.join(self._root, "docs", "examples")
        if not os.path.isdir(ex_dir):
            return
        for fname in os.listdir(ex_dir):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(ex_dir, fname)
            if not os.path.isfile(fpath):
                continue
            tags = self._infer_tags(fname) + ["example"]
            item = self._make_item(fpath, EXAMPLE, MARKDOWN, "docs.examples", tags)
            self._items.append(item)

    def collect_templates(self) -> None:
        """Scan docs/templates/."""
        tpl_dir = os.path.join(self._root, "docs", "templates")
        if not os.path.isdir(tpl_dir):
            return
        for fname in os.listdir(tpl_dir):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(tpl_dir, fname)
            if not os.path.isfile(fpath):
                continue
            tags = self._infer_tags(fname) + ["template"]
            item = self._make_item(fpath, TEMPLATE, TEMPLATE_SRC, "docs.templates", tags)
            self._items.append(item)

    def collect_reports(self) -> None:
        """Scan reports/*.py (report builders, NOT generated .md files)."""
        rep_dir = os.path.join(self._root, "reports")
        if not os.path.isdir(rep_dir):
            return
        for fname in os.listdir(rep_dir):
            if not fname.endswith(".py"):
                continue
            if fname.startswith("__"):
                continue
            fpath = os.path.join(rep_dir, fname)
            if not os.path.isfile(fpath):
                continue
            tags = self._infer_tags(fname) + ["report_builder"]
            item = self._make_item(fpath, REPORT, REPORT_MD, "reports", tags)
            self._items.append(item)

    def collect_gui_registry(self) -> None:
        """Scan gui/navigation/tab_registry.py."""
        reg_path = os.path.join(self._root, "gui", "navigation", "tab_registry.py")
        if not os.path.isfile(reg_path):
            return
        item = self._make_item(reg_path, GUI, GUI_REGISTRY, "gui.navigation", ["tab_registry", "gui"])
        self._items.append(item)

    def collect_cli_commands(self) -> None:
        """Read main.py docstring section to extract command names."""
        main_path = os.path.join(self._root, "main.py")
        if not os.path.isfile(main_path):
            return
        try:
            commands = []
            with open(main_path, "r", encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh):
                    if i > 200:
                        break
                    stripped = line.strip()
                    if stripped.startswith("def cmd_"):
                        cmd_name = stripped[len("def cmd_"):].split("(")[0].replace("_", "-")
                        commands.append(cmd_name)
            item_id = self._make_id("main.py_cli")
            item = KnowledgeBaseItem(
                item_id=item_id,
                path=os.path.relpath(main_path, self._root).replace("\\", "/"),
                title="CLI Commands (main.py)",
                category=DOC,
                source_type=CLI_COMMAND,
                module="cli",
                tags=["cli", "commands", "main"],
                keywords=commands[:50],
                summary="CLI command entry point. All commands are research-only.",
                content_excerpt="",
                modified_at=self._mtime(main_path),
                size_bytes=os.path.getsize(main_path),
                no_real_orders=True,
                broker_disabled=True,
                research_only=True,
            )
            self._items.append(item)
        except Exception as exc:
            logger.debug("collect_cli_commands: %s", exc)

    def collect_strategy_memory_metadata(self) -> None:
        """Try to find strategy_memory metadata files; graceful if missing."""
        sm_dir = os.path.join(self._root, "strategy_memory")
        if not os.path.isdir(sm_dir):
            return
        try:
            for fname in os.listdir(sm_dir):
                if fname.endswith(".py") and not fname.startswith("__"):
                    fpath = os.path.join(sm_dir, fname)
                    tags = self._infer_tags(fname) + ["strategy_memory"]
                    item = self._make_item(fpath, STRATEGY_MEMORY, MEMORY_RECORD if False else SOURCE_UNKNOWN, "strategy_memory", tags)
                    self._items.append(item)
                    break  # index only the first module file as representative
        except Exception as exc:
            logger.debug("collect_strategy_memory_metadata: %s", exc)

    def collect_evidence_graph_metadata(self) -> None:
        """Try to find evidence_graph metadata; graceful if missing."""
        eg_dir = os.path.join(self._root, "evidence_graph")
        if not os.path.isdir(eg_dir):
            return
        try:
            for fname in os.listdir(eg_dir):
                if fname.endswith(".py") and not fname.startswith("__"):
                    fpath = os.path.join(eg_dir, fname)
                    tags = self._infer_tags(fname) + ["evidence_graph"]
                    item = self._make_item(fpath, EVIDENCE_GRAPH, SOURCE_UNKNOWN, "evidence_graph", tags)
                    self._items.append(item)
                    break  # index only the first module file as representative
        except Exception as exc:
            logger.debug("collect_evidence_graph_metadata: %s", exc)

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------

    def extract_metadata(self, path: str) -> dict:
        """Read first 200 lines of an MD file; extract title and keywords."""
        result = {"title": "", "keywords": [], "summary": "", "excerpt": ""}
        if not os.path.isfile(path):
            return result
        try:
            lines = []
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh):
                    if i >= _MAX_MD_LINES:
                        break
                    lines.append(line.rstrip())
            # Title: first line starting with #
            for line in lines:
                stripped = line.lstrip()
                if stripped.startswith("#"):
                    result["title"] = stripped.lstrip("#").strip()
                    break
            text = "\n".join(lines)
            result["keywords"] = self.extract_keywords(text)
            result["summary"] = result["title"]
            result["excerpt"] = text[:500]
        except Exception as exc:
            logger.debug("extract_metadata(%s): %s", path, exc)
        return result

    def extract_keywords(self, text: str) -> List[str]:
        """Simple keyword extraction from text."""
        import re
        words = re.findall(r"[a-zA-Z\u4e00-\u9fff]{3,}", text.lower())
        stop = {
            "the", "and", "for", "that", "this", "with", "from", "are",
            "has", "was", "not", "all", "can", "its", "use", "you", "your",
        }
        seen = set()
        result = []
        for w in words:
            if w not in stop and w not in seen:
                seen.add(w)
                result.append(w)
            if len(result) >= 30:
                break
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _make_item(
        self,
        fpath: str,
        category: str,
        source_type: str,
        module: str,
        extra_tags: List[str],
    ) -> KnowledgeBaseItem:
        rel_path = os.path.relpath(fpath, self._root).replace("\\", "/")
        fname = os.path.basename(fpath)
        item_id = self._make_id(rel_path)

        if fpath.endswith(".md") or fpath.endswith(".MD"):
            meta = self.extract_metadata(fpath)
            title = meta["title"] or fname
            keywords = meta["keywords"]
            summary = meta["summary"]
            excerpt = meta["excerpt"][:500]
        else:
            title = fname
            keywords = self.extract_keywords(fname.replace("_", " ").replace("-", " "))
            summary = f"{category}: {fname}"
            excerpt = ""

        tags = list(set(self._infer_tags(fname) + extra_tags))
        safety = any(k in (title + " " + summary + " " + excerpt).lower() for k in _SAFETY_KEYWORDS)

        return KnowledgeBaseItem(
            item_id=item_id,
            path=rel_path,
            title=title,
            category=category,
            source_type=source_type,
            module=module,
            tags=tags,
            keywords=keywords[:30],
            summary=summary[:200],
            content_excerpt=excerpt[:500],
            modified_at=self._mtime(fpath),
            size_bytes=self._fsize(fpath),
            safety_covered=safety,
            no_real_orders=True,
            broker_disabled=True,
            research_only=True,
            has_forbidden_actions=False,
            status="OK",
            reason="",
        )

    def _make_id(self, path: str) -> str:
        return hashlib.md5(path.encode("utf-8")).hexdigest()[:12]

    def _mtime(self, path: str) -> str:
        try:
            ts = os.path.getmtime(path)
            return datetime.fromtimestamp(ts).isoformat()
        except Exception:
            return ""

    def _fsize(self, path: str) -> int:
        try:
            return os.path.getsize(path)
        except Exception:
            return 0

    def _infer_tags(self, fname: str) -> List[str]:
        name = os.path.splitext(fname)[0].lower().replace("_", " ").replace("-", " ")
        parts = name.split()
        tags = []
        for part in parts:
            if len(part) >= 3:
                tags.append(part)
        # version tag
        import re
        vm = re.search(r"v\d+\.\d+", name)
        if vm:
            tags.append(vm.group())
        return tags[:10]
