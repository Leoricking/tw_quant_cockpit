"""
knowledge_base/kb_schema.py — KnowledgeBase schema dataclasses for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Search. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Category constants
# ---------------------------------------------------------------------------
DOC               = "DOC"
EXAMPLE           = "EXAMPLE"
TEMPLATE          = "TEMPLATE"
REPORT            = "REPORT"
STRATEGY_MEMORY   = "STRATEGY_MEMORY"
EVIDENCE_GRAPH    = "EVIDENCE_GRAPH"
REGRESSION        = "REGRESSION"
GUI               = "GUI"
DATA_HYGIENE      = "DATA_HYGIENE"
WORKFLOW          = "WORKFLOW"
SAFETY            = "SAFETY"
RELEASE           = "RELEASE"
UNKNOWN           = "UNKNOWN"

# ---------------------------------------------------------------------------
# Source type constants
# ---------------------------------------------------------------------------
MARKDOWN          = "MARKDOWN"
REPORT_MD         = "REPORT_MD"
CSV_MANIFEST      = "CSV_MANIFEST"
MEMORY_RECORD     = "MEMORY_RECORD"
EVIDENCE_THREAD   = "EVIDENCE_THREAD"
GUI_REGISTRY      = "GUI_REGISTRY"
CLI_COMMAND       = "CLI_COMMAND"
TEMPLATE_SRC      = "TEMPLATE"
SOURCE_UNKNOWN    = "UNKNOWN"

# ---------------------------------------------------------------------------
# Match type constants
# ---------------------------------------------------------------------------
MATCH_TITLE    = "TITLE"
MATCH_TAG      = "TAG"
MATCH_KEYWORD  = "KEYWORD"
MATCH_CONTENT  = "CONTENT"
MATCH_MODULE   = "MODULE"
MATCH_PATH     = "PATH"

# ---------------------------------------------------------------------------
# Allowed safe next steps (never BUY/SELL/ORDER/EXECUTE etc.)
# ---------------------------------------------------------------------------
SAFE_NEXT_STEPS = [
    "REVIEW",
    "READ_REPORT",
    "KEEP_OBSERVING",
    "MARK_RESEARCH_ONLY",
    "PAPER_ONLY",
    "MOCK_ONLY",
    "WAIT",
    "BACKTEST_MORE",
    "PRACTICE_REPLAY",
    "REVIEW_JOURNAL",
    "REVIEW_RISK",
    "REVIEW_EARNINGS",
    "REVIEW_CHIPS",
    "DO_NOT_CHASE",
    "FIX_DATA",
]

# ---------------------------------------------------------------------------
# Forbidden action keywords — must NEVER appear in output
# ---------------------------------------------------------------------------
FORBIDDEN_ACTIONS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]


@dataclass
class KnowledgeBaseItem:
    """A single indexed item in the knowledge base.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    item_id: str
    path: str
    title: str
    category: str
    source_type: str
    module: str
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    summary: str = ""
    content_excerpt: str = ""
    modified_at: str = ""
    size_bytes: int = 0
    safety_covered: bool = True
    no_real_orders: bool = True
    broker_disabled: bool = True
    research_only: bool = True
    has_forbidden_actions: bool = False
    status: str = "OK"
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "item_id":             self.item_id,
            "path":                self.path,
            "title":               self.title,
            "category":            self.category,
            "source_type":         self.source_type,
            "module":              self.module,
            "tags":                "|".join(self.tags),
            "keywords":            "|".join(self.keywords),
            "summary":             self.summary,
            "content_excerpt":     self.content_excerpt,
            "modified_at":         self.modified_at,
            "size_bytes":          self.size_bytes,
            "safety_covered":      self.safety_covered,
            "no_real_orders":      self.no_real_orders,
            "broker_disabled":     self.broker_disabled,
            "research_only":       self.research_only,
            "has_forbidden_actions": self.has_forbidden_actions,
            "status":              self.status,
            "reason":              self.reason,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "KnowledgeBaseItem":
        tags = [t for t in d.get("tags", "").split("|") if t]
        keywords = [k for k in d.get("keywords", "").split("|") if k]
        return cls(
            item_id=d.get("item_id", ""),
            path=d.get("path", ""),
            title=d.get("title", ""),
            category=d.get("category", UNKNOWN),
            source_type=d.get("source_type", SOURCE_UNKNOWN),
            module=d.get("module", ""),
            tags=tags,
            keywords=keywords,
            summary=d.get("summary", ""),
            content_excerpt=d.get("content_excerpt", ""),
            modified_at=d.get("modified_at", ""),
            size_bytes=int(d.get("size_bytes", 0) or 0),
            safety_covered=str(d.get("safety_covered", "True")).lower() != "false",
            no_real_orders=str(d.get("no_real_orders", "True")).lower() != "false",
            broker_disabled=str(d.get("broker_disabled", "True")).lower() != "false",
            research_only=str(d.get("research_only", "True")).lower() != "false",
            has_forbidden_actions=str(d.get("has_forbidden_actions", "False")).lower() == "true",
            status=d.get("status", "OK"),
            reason=d.get("reason", ""),
        )


@dataclass
class KnowledgeBaseSearchResult:
    """A single search result from the knowledge base.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    query: str
    item_id: str
    title: str
    path: str
    category: str
    module: str
    score: float
    match_type: str
    matched_terms: List[str] = field(default_factory=list)
    excerpt: str = ""
    safe_next_step: str = "REVIEW"
    no_real_orders: bool = True
    research_only: bool = True

    def to_dict(self) -> dict:
        return {
            "query":          self.query,
            "item_id":        self.item_id,
            "title":          self.title,
            "path":           self.path,
            "category":       self.category,
            "module":         self.module,
            "score":          self.score,
            "match_type":     self.match_type,
            "matched_terms":  "|".join(self.matched_terms),
            "excerpt":        self.excerpt,
            "safe_next_step": self.safe_next_step,
            "no_real_orders": self.no_real_orders,
            "research_only":  self.research_only,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "KnowledgeBaseSearchResult":
        matched_terms = [t for t in d.get("matched_terms", "").split("|") if t]
        return cls(
            query=d.get("query", ""),
            item_id=d.get("item_id", ""),
            title=d.get("title", ""),
            path=d.get("path", ""),
            category=d.get("category", UNKNOWN),
            module=d.get("module", ""),
            score=float(d.get("score", 0.0) or 0.0),
            match_type=d.get("match_type", MATCH_CONTENT),
            matched_terms=matched_terms,
            excerpt=d.get("excerpt", ""),
            safe_next_step=d.get("safe_next_step", "REVIEW"),
            no_real_orders=str(d.get("no_real_orders", "True")).lower() != "false",
            research_only=str(d.get("research_only", "True")).lower() != "false",
        )


@dataclass
class KnowledgeBaseSummary:
    """Summary of the knowledge base index.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    generated_at: str
    version: str
    total_items: int
    docs_count: int
    examples_count: int
    templates_count: int
    reports_count: int
    safety_docs_count: int
    modules_count: int
    indexed_paths: List[str] = field(default_factory=list)
    missing_indexes: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    blocked: bool = False
    no_real_orders: bool = True
    broker_disabled: bool = True
    research_only: bool = True

    def to_dict(self) -> dict:
        return {
            "generated_at":    self.generated_at,
            "version":         self.version,
            "total_items":     self.total_items,
            "docs_count":      self.docs_count,
            "examples_count":  self.examples_count,
            "templates_count": self.templates_count,
            "reports_count":   self.reports_count,
            "safety_docs_count": self.safety_docs_count,
            "modules_count":   self.modules_count,
            "indexed_paths":   "|".join(self.indexed_paths),
            "missing_indexes": "|".join(self.missing_indexes),
            "warnings":        "|".join(self.warnings),
            "blocked":         self.blocked,
            "no_real_orders":  self.no_real_orders,
            "broker_disabled": self.broker_disabled,
            "research_only":   self.research_only,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "KnowledgeBaseSummary":
        return cls(
            generated_at=d.get("generated_at", ""),
            version=d.get("version", "1.0.7"),
            total_items=int(d.get("total_items", 0) or 0),
            docs_count=int(d.get("docs_count", 0) or 0),
            examples_count=int(d.get("examples_count", 0) or 0),
            templates_count=int(d.get("templates_count", 0) or 0),
            reports_count=int(d.get("reports_count", 0) or 0),
            safety_docs_count=int(d.get("safety_docs_count", 0) or 0),
            modules_count=int(d.get("modules_count", 0) or 0),
            indexed_paths=[p for p in d.get("indexed_paths", "").split("|") if p],
            missing_indexes=[m for m in d.get("missing_indexes", "").split("|") if m],
            warnings=[w for w in d.get("warnings", "").split("|") if w],
            blocked=str(d.get("blocked", "False")).lower() == "true",
            no_real_orders=str(d.get("no_real_orders", "True")).lower() != "false",
            broker_disabled=str(d.get("broker_disabled", "True")).lower() != "false",
            research_only=str(d.get("research_only", "True")).lower() != "false",
        )
