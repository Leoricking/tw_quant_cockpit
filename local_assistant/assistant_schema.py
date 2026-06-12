"""
local_assistant/assistant_schema.py — Schema dataclasses for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Local Research Assistant. No external API. No broker execution.
[!] Local assistant does not enable trading.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------

ALLOWED_ACTIONS = [
    "REVIEW",
    "READ_REPORT",
    "BACKTEST_MORE",
    "PRACTICE_REPLAY",
    "REVIEW_JOURNAL",
    "REVIEW_RISK",
    "REVIEW_EARNINGS",
    "REVIEW_CHIPS",
    "DO_NOT_CHASE",
    "KEEP_OBSERVING",
    "FIX_DATA",
    "WAIT",
]

FORBIDDEN_ACTIONS = [
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
    "LIVE_TRADE",
    "BROKER_ORDER",
]

STATUS_ANSWERED      = "ANSWERED"
STATUS_PARTIAL       = "PARTIAL"
STATUS_NO_RESULTS    = "NO_RESULTS"
STATUS_INSUFFICIENT  = "INSUFFICIENT_CONTEXT"
STATUS_BLOCKED       = "BLOCKED_UNSAFE_QUERY"

CONFIDENCE_LOW          = "LOW"
CONFIDENCE_MEDIUM       = "MEDIUM"
CONFIDENCE_HIGH         = "HIGH"
CONFIDENCE_INSUFFICIENT = "INSUFFICIENT"

UNSAFE_QUERY_PATTERNS: List[str] = [
    "buy",
    "sell",
    "order",
    "purchase",
    "place an order",
    "submit order",
    "execute",
    "trade now",
    "should i buy",
    "should i sell",
    "enter position",
    "open position",
    "auto trade",
    "live trade",
    "real trade",
    "broker order",
    "下單",
    "買進",
    "賣出",
    "買入",
    "進場",
    "出場",
]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ResearchAssistantQuestion:
    """Question schema for Local Research Assistant.

    [!] Research Only. No Real Orders.
    """

    question: str
    category: str = ""
    module_hint: str = ""
    stock: str = ""
    mode: str = "real"
    limit: int = 8
    created_at: str = ""
    research_only: bool = True
    no_real_orders: bool = True
    broker_disabled: bool = True

    def to_dict(self) -> dict:
        return {
            "question":       self.question,
            "category":       self.category,
            "module_hint":    self.module_hint,
            "stock":          self.stock,
            "mode":           self.mode,
            "limit":          self.limit,
            "created_at":     self.created_at,
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
            "broker_disabled": self.broker_disabled,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ResearchAssistantQuestion":
        return cls(
            question=d.get("question", ""),
            category=d.get("category", ""),
            module_hint=d.get("module_hint", ""),
            stock=d.get("stock", ""),
            mode=d.get("mode", "real"),
            limit=int(d.get("limit", 8)),
            created_at=d.get("created_at", ""),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
            broker_disabled=bool(d.get("broker_disabled", True)),
        )


@dataclass
class ResearchAssistantSource:
    """Source document reference in a research answer.

    [!] Research Only. No Real Orders.
    """

    source_id: str
    title: str
    path: str
    category: str
    module: str
    score: float = 0.0
    excerpt: str = ""
    reason: str = ""
    source_type: str = ""

    def to_dict(self) -> dict:
        return {
            "source_id":   self.source_id,
            "title":       self.title,
            "path":        self.path,
            "category":    self.category,
            "module":      self.module,
            "score":       self.score,
            "excerpt":     self.excerpt,
            "reason":      self.reason,
            "source_type": self.source_type,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ResearchAssistantSource":
        return cls(
            source_id=d.get("source_id", ""),
            title=d.get("title", ""),
            path=d.get("path", ""),
            category=d.get("category", ""),
            module=d.get("module", ""),
            score=float(d.get("score", 0.0)),
            excerpt=d.get("excerpt", ""),
            reason=d.get("reason", ""),
            source_type=d.get("source_type", ""),
        )


@dataclass
class ModuleRoute:
    """Module routing suggestion from a research question.

    [!] Research Only. No Real Orders. safe_action must be in ALLOWED_ACTIONS.
    """

    module: str
    reason: str
    suggested_cli: List[str] = field(default_factory=list)
    suggested_gui_tab: str = ""
    safe_action: str = "REVIEW"
    priority: str = "P1"

    def to_dict(self) -> dict:
        return {
            "module":            self.module,
            "reason":            self.reason,
            "suggested_cli":     self.suggested_cli,
            "suggested_gui_tab": self.suggested_gui_tab,
            "safe_action":       self.safe_action,
            "priority":          self.priority,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ModuleRoute":
        return cls(
            module=d.get("module", ""),
            reason=d.get("reason", ""),
            suggested_cli=list(d.get("suggested_cli", [])),
            suggested_gui_tab=d.get("suggested_gui_tab", ""),
            safe_action=d.get("safe_action", "REVIEW"),
            priority=d.get("priority", "P1"),
        )


@dataclass
class SafeNextStep:
    """A safe next step recommendation (no trading actions).

    [!] Research Only. No Real Orders.
    """

    action: str
    description: str
    cli: str = ""
    gui_tab: str = ""
    reason: str = ""
    safety_note: str = ""

    def to_dict(self) -> dict:
        return {
            "action":      self.action,
            "description": self.description,
            "cli":         self.cli,
            "gui_tab":     self.gui_tab,
            "reason":      self.reason,
            "safety_note": self.safety_note,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "SafeNextStep":
        return cls(
            action=d.get("action", ""),
            description=d.get("description", ""),
            cli=d.get("cli", ""),
            gui_tab=d.get("gui_tab", ""),
            reason=d.get("reason", ""),
            safety_note=d.get("safety_note", ""),
        )


@dataclass
class ResearchAssistantAnswer:
    """Full answer from the Local Research Assistant.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Not Investment Advice. Local assistant does not enable trading.
    """

    question: str
    answer: str
    summary: str
    sources: List[ResearchAssistantSource] = field(default_factory=list)
    module_routes: List[ModuleRoute] = field(default_factory=list)
    safe_next_steps: List[SafeNextStep] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    confidence: str = CONFIDENCE_LOW
    status: str = STATUS_ANSWERED
    no_real_orders: bool = True
    broker_disabled: bool = True
    research_only: bool = True
    not_investment_advice: bool = True
    external_api_used: bool = False

    def to_dict(self) -> dict:
        return {
            "question":            self.question,
            "answer":              self.answer,
            "summary":             self.summary,
            "sources":             [s.to_dict() for s in self.sources],
            "module_routes":       [r.to_dict() for r in self.module_routes],
            "safe_next_steps":     [n.to_dict() for n in self.safe_next_steps],
            "limitations":         self.limitations,
            "confidence":          self.confidence,
            "status":              self.status,
            "no_real_orders":      self.no_real_orders,
            "broker_disabled":     self.broker_disabled,
            "research_only":       self.research_only,
            "not_investment_advice": self.not_investment_advice,
            "external_api_used":   self.external_api_used,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ResearchAssistantAnswer":
        sources = [ResearchAssistantSource.from_dict(s) for s in d.get("sources", [])]
        routes = [ModuleRoute.from_dict(r) for r in d.get("module_routes", [])]
        steps = [SafeNextStep.from_dict(n) for n in d.get("safe_next_steps", [])]
        return cls(
            question=d.get("question", ""),
            answer=d.get("answer", ""),
            summary=d.get("summary", ""),
            sources=sources,
            module_routes=routes,
            safe_next_steps=steps,
            limitations=list(d.get("limitations", [])),
            confidence=d.get("confidence", CONFIDENCE_LOW),
            status=d.get("status", STATUS_ANSWERED),
            no_real_orders=bool(d.get("no_real_orders", True)),
            broker_disabled=bool(d.get("broker_disabled", True)),
            research_only=bool(d.get("research_only", True)),
            not_investment_advice=bool(d.get("not_investment_advice", True)),
            external_api_used=bool(d.get("external_api_used", False)),
        )
