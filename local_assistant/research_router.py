"""
local_assistant/research_router.py — ResearchRouter for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API. Local assistant does not enable trading.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from local_assistant.assistant_schema import ModuleRoute, ALLOWED_ACTIONS, FORBIDDEN_ACTIONS

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module route definitions
# ---------------------------------------------------------------------------

_MODULE_ROUTE_MAP = [
    {
        "module": "Strategy Validation",
        "keywords": [
            "validation", "validated", "score", "策略驗證", "分數", "有效嗎", "strategy validation",
        ],
        "suggested_cli": [
            "python main.py strategy-validation-summary",
            "python main.py strategy-lab-dashboard-summary",
        ],
        "suggested_gui_tab": "strategy_validation",
        "safe_action": "REVIEW",
        "priority": "P1",
    },
    {
        "module": "Evidence Graph",
        "keywords": [
            "evidence", "graph", "cause", "chain", "證據", "因果", "鏈", "evidence graph",
        ],
        "suggested_cli": [
            "python main.py evidence-graph-summary",
            "python main.py kb-search --query \"evidence graph\"",
        ],
        "suggested_gui_tab": "evidence_graph",
        "safe_action": "REVIEW",
        "priority": "P1",
    },
    {
        "module": "Crash Reversal",
        "keywords": [
            "crash", "reversal", "大跌", "反彈", "破底翻", "風險", "crash reversal",
        ],
        "suggested_cli": [
            "python main.py crash-reversal-summary",
            "python main.py kb-search --query \"crash reversal\"",
        ],
        "suggested_gui_tab": "crash_reversal",
        "safe_action": "REVIEW_RISK",
        "priority": "P1",
    },
    {
        "module": "Data Hygiene",
        "keywords": [
            "data", "report", "csv", "output", "hygiene", "資料", "報告", "清理", "產物", "data hygiene",
        ],
        "suggested_cli": [
            "python main.py data-report-hygiene-summary",
        ],
        "suggested_gui_tab": "data_hygiene",
        "safe_action": "FIX_DATA",
        "priority": "P1",
    },
    {
        "module": "Regression Hardening",
        "keywords": [
            "regression", "release gate", "safety scan", "回歸", "發版", "安全掃描",
            "release gate warning",
        ],
        "suggested_cli": [
            "python main.py release-gate-health --mode real",
            "python main.py safety-scan --target all",
        ],
        "suggested_gui_tab": "regression_hardening",
        "safe_action": "READ_REPORT",
        "priority": "P1",
    },
    {
        "module": "Documentation / Workflow",
        "keywords": [
            "docs", "guide", "template", "sop", "文件", "手冊", "模板", "範例",
            "handoff", "workflow", "daily workflow",
        ],
        "suggested_cli": [
            "python main.py docs-summary",
            "python main.py workflow-templates-summary",
        ],
        "suggested_gui_tab": "documentation_health",
        "safe_action": "REVIEW",
        "priority": "P1",
    },
    {
        "module": "Knowledge Base",
        "keywords": [
            "search", "kb", "knowledge", "找", "搜尋", "知識庫", "knowledge base",
        ],
        "suggested_cli": [
            "python main.py kb-search --query \"\"",
        ],
        "suggested_gui_tab": "knowledge_base_search",
        "safe_action": "READ_REPORT",
        "priority": "P1",
    },
]

# Category → module name mapping
_CATEGORY_MODULE_MAP = {
    "strategy_validation":  "Strategy Validation",
    "evidence_graph":       "Evidence Graph",
    "crash_reversal":       "Crash Reversal",
    "data_hygiene":         "Data Hygiene",
    "regression":           "Regression Hardening",
    "regression_hardening": "Regression Hardening",
    "documentation":        "Documentation / Workflow",
    "workflow":             "Documentation / Workflow",
    "knowledge_base":       "Knowledge Base",
    "knowledge":            "Knowledge Base",
}


class ResearchRouter:
    """Routes research questions to relevant modules.

    [!] Research Only. No Real Orders. No broker commands.
    [!] No forbidden actions in suggested_cli.
    [!] Local assistant does not enable trading.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def route_question(self, question: str, kb_results=None) -> List[ModuleRoute]:
        """Primary routing: combine keyword + result-category routing."""
        return self.infer_module_routes(question=question, kb_results=kb_results)

    def infer_module_routes(self, question: str, kb_results=None) -> List[ModuleRoute]:
        """Combine keyword routing and result-category routing, deduplicated."""
        routes: List[ModuleRoute] = []
        seen_modules: set = set()

        # Keyword-based routes first
        kw_routes = self.route_by_keywords(question)
        for r in kw_routes:
            if r.module not in seen_modules:
                routes.append(r)
                seen_modules.add(r.module)

        # Category-based routes from KB results
        if kb_results:
            cat_routes = self.route_by_result_categories(kb_results)
            for r in cat_routes:
                if r.module not in seen_modules:
                    routes.append(r)
                    seen_modules.add(r.module)

        # Fallback: always include Knowledge Base route if nothing matched
        if not routes:
            routes.append(ModuleRoute(
                module="Knowledge Base",
                reason="No specific module matched — defaulting to Knowledge Base search",
                suggested_cli=["python main.py kb-search --query \"\""],
                suggested_gui_tab="knowledge_base_search",
                safe_action="READ_REPORT",
                priority="P1",
            ))

        # Safety: verify no forbidden actions crept in
        safe_routes = []
        for r in routes:
            if r.safe_action in ALLOWED_ACTIONS:
                safe_routes.append(r)
            else:
                logger.warning("Blocked forbidden safe_action in route: %s -> %s", r.module, r.safe_action)
        return safe_routes

    def route_by_keywords(self, question: str) -> List[ModuleRoute]:
        """Match question tokens against keyword lists in _MODULE_ROUTE_MAP."""
        q_lower = question.lower()
        matched: List[ModuleRoute] = []
        for entry in _MODULE_ROUTE_MAP:
            for kw in entry["keywords"]:
                if kw in q_lower:
                    matched.append(ModuleRoute(
                        module=entry["module"],
                        reason=f"Keyword match: '{kw}' found in question",
                        suggested_cli=list(entry["suggested_cli"]),
                        suggested_gui_tab=entry["suggested_gui_tab"],
                        safe_action=entry["safe_action"],
                        priority=entry["priority"],
                    ))
                    break  # one match per module entry
        return matched

    def route_by_result_categories(self, results) -> List[ModuleRoute]:
        """Derive routes from categories present in KB search results."""
        seen_cats: set = set()
        routes: List[ModuleRoute] = []
        for item in results:
            cat = ""
            if hasattr(item, "category"):
                cat = (item.category or "").lower()
            elif isinstance(item, dict):
                cat = str(item.get("category", "")).lower()
            if not cat or cat in seen_cats:
                continue
            seen_cats.add(cat)
            module_name = _CATEGORY_MODULE_MAP.get(cat)
            if module_name:
                # Find the entry for this module
                for entry in _MODULE_ROUTE_MAP:
                    if entry["module"] == module_name:
                        routes.append(ModuleRoute(
                            module=entry["module"],
                            reason=f"Category match from KB results: '{cat}'",
                            suggested_cli=list(entry["suggested_cli"]),
                            suggested_gui_tab=entry["suggested_gui_tab"],
                            safe_action=entry["safe_action"],
                            priority=entry["priority"],
                        ))
                        break
        return routes

    def build_safe_cli_suggestions(self, routes: List[ModuleRoute]) -> List[str]:
        """Collect all unique safe CLI suggestions from routes.

        [!] No compound commands. No forbidden actions.
        """
        seen: set = set()
        suggestions: List[str] = []
        for r in routes:
            for cli in r.suggested_cli:
                # Safety filter: skip if contains forbidden keywords
                cli_lower = cli.lower()
                is_forbidden = any(fa.lower() in cli_lower for fa in FORBIDDEN_ACTIONS)
                if not is_forbidden and cli not in seen:
                    suggestions.append(cli)
                    seen.add(cli)
        return suggestions

    def build_safe_gui_suggestions(self, routes: List[ModuleRoute]) -> List[str]:
        """Collect all unique GUI tab suggestions from routes."""
        seen: set = set()
        tabs: List[str] = []
        for r in routes:
            if r.suggested_gui_tab and r.suggested_gui_tab not in seen:
                tabs.append(r.suggested_gui_tab)
                seen.add(r.suggested_gui_tab)
        return tabs
