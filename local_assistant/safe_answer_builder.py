"""
local_assistant/safe_answer_builder.py — SafeAnswerBuilder for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API. Safe answer builder only.
[!] Local assistant does not enable trading.
"""
from __future__ import annotations

import logging
from typing import List

from local_assistant.assistant_schema import (
    ResearchAssistantAnswer,
    ResearchAssistantSource,
    ModuleRoute,
    SafeNextStep,
    ALLOWED_ACTIONS,
    FORBIDDEN_ACTIONS,
    UNSAFE_QUERY_PATTERNS,
    STATUS_ANSWERED,
    STATUS_NO_RESULTS,
    STATUS_BLOCKED,
    CONFIDENCE_LOW,
    CONFIDENCE_INSUFFICIENT,
)
from local_assistant.research_summarizer import ResearchSummarizer

logger = logging.getLogger(__name__)

_SAFETY_NOTICES = [
    "Not Investment Advice.",
    "No Real Orders.",
    "Broker Execution Disabled.",
    "VALIDATED does not enable trading.",
]

_BLOCKED_SAFE_ALTERNATIVES = [
    SafeNextStep(
        action="REVIEW_RISK",
        description="Review risk parameters in the research system instead of placing orders.",
        cli="python main.py crash-reversal-summary",
        gui_tab="crash_reversal",
        reason="Safe alternative to trading queries.",
        safety_note="No real orders. No broker execution.",
    ),
    SafeNextStep(
        action="READ_REPORT",
        description="Read existing research reports for context.",
        cli="python main.py kb-search --query \"research report\"",
        gui_tab="knowledge_base_search",
        reason="Safe alternative: read before acting.",
        safety_note="No real orders. No broker execution.",
    ),
    SafeNextStep(
        action="WAIT",
        description="Do not act. Observe and wait for more data.",
        cli="",
        gui_tab="",
        reason="Safe default when query involves potential trading action.",
        safety_note="No real orders. No broker execution.",
    ),
    SafeNextStep(
        action="BACKTEST_MORE",
        description="Run more backtests before making any decisions.",
        cli="python main.py strategy-validation-summary",
        gui_tab="strategy_validation",
        reason="Safe alternative: backtest first.",
        safety_note="Backtesting does not enable real trading.",
    ),
]


class SafeAnswerBuilder:
    """Builds safe research-only answers from KB results and module routes.

    Safety invariants:
    - Never outputs BUY/SELL/ORDER/EXECUTE etc.
    - Every answer includes safety notices.
    - Unsafe queries → BLOCKED_UNSAFE_QUERY.
    - All safe_next_steps actions must be in ALLOWED_ACTIONS.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Local assistant does not enable trading.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        self._summarizer = ResearchSummarizer()

    def is_unsafe_query(self, question: str) -> bool:
        """Return True if question matches any UNSAFE_QUERY_PATTERNS."""
        q_lower = question.lower()
        for pattern in UNSAFE_QUERY_PATTERNS:
            if pattern in q_lower:
                return True
        return False

    def build_answer(
        self,
        question: str,
        kb_results,
        routes: List[ModuleRoute],
    ) -> ResearchAssistantAnswer:
        """Build a full research answer from KB results and module routes."""
        # Safety check first
        if self.is_unsafe_query(question):
            return self.build_unsafe_query_answer(question)

        summary_text = self._summarizer.summarize_results(question, kb_results)
        confidence = self._summarizer.infer_confidence(kb_results)
        limitations = self._summarizer.summarize_limitations(kb_results)
        citations = self._summarizer.build_citations(kb_results)

        # Build answer text
        answer_lines = [
            summary_text,
            "",
            "Sources:",
            citations,
            "",
        ]
        for notice in _SAFETY_NOTICES:
            answer_lines.append(f"[!] {notice}")

        answer_text = self.sanitize_answer_text("\n".join(answer_lines))

        # Build sources
        sources: List[ResearchAssistantSource] = []
        for i, item in enumerate(kb_results or []):
            if hasattr(item, "title"):
                src = ResearchAssistantSource(
                    source_id=getattr(item, "item_id", f"src_{i}"),
                    title=getattr(item, "title", ""),
                    path=getattr(item, "path", ""),
                    category=getattr(item, "category", ""),
                    module=getattr(item, "module", ""),
                    score=float(getattr(item, "score", 0.0)),
                    excerpt=getattr(item, "summary", "")[:200],
                    source_type=getattr(item, "source_type", ""),
                )
            elif isinstance(item, dict):
                src = ResearchAssistantSource(
                    source_id=str(item.get("item_id", f"src_{i}")),
                    title=str(item.get("title", "")),
                    path=str(item.get("path", "")),
                    category=str(item.get("category", "")),
                    module=str(item.get("module", "")),
                    score=float(item.get("score", 0.0)),
                    excerpt=str(item.get("summary", ""))[:200],
                    source_type=str(item.get("source_type", "")),
                )
            else:
                continue
            sources.append(src)

        # Build safe next steps
        safe_steps = self.build_safe_next_steps(routes)

        # Determine status
        if not kb_results:
            status = STATUS_NO_RESULTS
        else:
            status = STATUS_ANSWERED

        answer = ResearchAssistantAnswer(
            question=question,
            answer=answer_text,
            summary=summary_text,
            sources=sources,
            module_routes=routes,
            safe_next_steps=safe_steps,
            limitations=limitations,
            confidence=confidence,
            status=status,
            no_real_orders=True,
            broker_disabled=True,
            research_only=True,
            not_investment_advice=True,
            external_api_used=False,
        )

        # Final validation
        self.validate_answer(answer)
        return answer

    def build_no_result_answer(self, question: str) -> ResearchAssistantAnswer:
        """Build an answer for when KB returns no results."""
        if self.is_unsafe_query(question):
            return self.build_unsafe_query_answer(question)

        answer_text = (
            f"No relevant documents found for: '{question}'.\n"
            "Try refining your query or running kb-index to rebuild the index.\n"
            "[!] Not Investment Advice. No Real Orders. Broker Execution Disabled.\n"
            "[!] VALIDATED does not enable trading."
        )
        return ResearchAssistantAnswer(
            question=question,
            answer=answer_text,
            summary="No results found.",
            sources=[],
            module_routes=[],
            safe_next_steps=[],
            limitations=ResearchSummarizer().summarize_limitations([]),
            confidence=CONFIDENCE_INSUFFICIENT,
            status=STATUS_NO_RESULTS,
            no_real_orders=True,
            broker_disabled=True,
            research_only=True,
            not_investment_advice=True,
            external_api_used=False,
        )

    def build_unsafe_query_answer(self, question: str) -> ResearchAssistantAnswer:
        """Return BLOCKED_UNSAFE_QUERY answer with safe alternatives."""
        answer_text = (
            f"[BLOCKED] This query contains patterns that suggest a trading action.\n"
            f"Query: '{question}'\n\n"
            "[!] Local Research Assistant is for RESEARCH ONLY.\n"
            "[!] No Real Orders. Broker Execution Disabled.\n"
            "[!] Production Trading BLOCKED.\n"
            "[!] This assistant does not enable trading.\n"
            "[!] Not Investment Advice.\n\n"
            "Safe alternatives are listed below."
        )
        return ResearchAssistantAnswer(
            question=question,
            answer=answer_text,
            summary="Query blocked: contains unsafe trading-action patterns.",
            sources=[],
            module_routes=[],
            safe_next_steps=list(_BLOCKED_SAFE_ALTERNATIVES),
            limitations=ResearchSummarizer().summarize_limitations([]),
            confidence=CONFIDENCE_INSUFFICIENT,
            status=STATUS_BLOCKED,
            no_real_orders=True,
            broker_disabled=True,
            research_only=True,
            not_investment_advice=True,
            external_api_used=False,
        )

    def sanitize_answer_text(self, text: str) -> str:
        """Remove any forbidden action words from answer text."""
        result = text
        for action in FORBIDDEN_ACTIONS:
            # Replace exact word (case-insensitive) with [REMOVED]
            import re
            result = re.sub(
                r'\b' + re.escape(action) + r'\b',
                "[REMOVED]",
                result,
                flags=re.IGNORECASE,
            )
        return result

    def validate_answer(self, answer: ResearchAssistantAnswer) -> bool:
        """Check that no forbidden actions appear in safe_next_steps."""
        for step in answer.safe_next_steps:
            if step.action in FORBIDDEN_ACTIONS:
                logger.error(
                    "SAFETY VIOLATION: forbidden action '%s' found in safe_next_steps for question: %s",
                    step.action, answer.question,
                )
                return False
        return True

    def build_safe_next_steps(self, routes: List[ModuleRoute]) -> List[SafeNextStep]:
        """Build SafeNextStep list from module routes."""
        steps: List[SafeNextStep] = []
        seen_actions: set = set()
        for route in routes:
            action = route.safe_action
            if action not in ALLOWED_ACTIONS:
                logger.warning("Skipping forbidden safe_action: %s", action)
                continue
            if action in seen_actions:
                continue
            seen_actions.add(action)
            cli = route.suggested_cli[0] if route.suggested_cli else ""
            steps.append(SafeNextStep(
                action=action,
                description=f"Review {route.module}: {route.reason}",
                cli=cli,
                gui_tab=route.suggested_gui_tab,
                reason=route.reason,
                safety_note="No real orders. No broker execution. Research only.",
            ))
        return steps
