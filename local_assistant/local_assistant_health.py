"""
local_assistant/local_assistant_health.py — LocalResearchAssistantHealthCheck for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API.
[!] Local assistant does not enable trading.
"""
from __future__ import annotations

import importlib
import logging
import os
from typing import List

logger = logging.getLogger(__name__)

_FORBIDDEN_IMPORTS = ["openai", "anthropic", "faiss", "chromadb", "pinecone"]


def _mk(name: str, status: str, message: str) -> dict:
    return {"name": name, "status": status, "message": message}


class LocalResearchAssistantHealthCheck:
    """Health check for the local_assistant package (v1.0.8).

    Checks: import, kb_engine, answer_builder, router, safe_scanner,
    local_only, external_api_disabled, no_forbidden_actions,
    unsafe_query_blocked, answer_generation_works, output_ignored_by_git.

    [!] Research Only. No Real Orders. No external API.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = ".") -> None:
        if not os.path.isabs(project_root):
            project_root = os.path.abspath(project_root)
        self._root = project_root

    def run(self) -> dict:
        """Run all health checks. Returns result dict. Never crashes."""
        checks: List[dict] = []

        # 1. package_import
        try:
            import local_assistant as _la
            checks.append(_mk("package_import", "PASS", "local_assistant importable"))
        except Exception as exc:
            checks.append(_mk("package_import", "FAIL", f"local_assistant import failed: {exc}"))

        # 2. kb_engine_available
        try:
            mod = importlib.import_module("knowledge_base.kb_search_engine")
            if hasattr(mod, "KnowledgeBaseSearchEngine"):
                checks.append(_mk("kb_engine_available", "PASS",
                                  "KnowledgeBaseSearchEngine importable"))
            else:
                checks.append(_mk("kb_engine_available", "WARN",
                                  "kb_search_engine imported but KnowledgeBaseSearchEngine not found"))
        except Exception as exc:
            checks.append(_mk("kb_engine_available", "WARN",
                               f"kb_search_engine: {exc}"))

        # 3. answer_builder_available
        try:
            from local_assistant.safe_answer_builder import SafeAnswerBuilder
            checks.append(_mk("answer_builder_available", "PASS",
                               "SafeAnswerBuilder importable"))
        except Exception as exc:
            checks.append(_mk("answer_builder_available", "FAIL",
                               f"SafeAnswerBuilder import failed: {exc}"))

        # 4. router_available
        try:
            from local_assistant.research_router import ResearchRouter
            checks.append(_mk("router_available", "PASS", "ResearchRouter importable"))
        except Exception as exc:
            checks.append(_mk("router_available", "FAIL",
                               f"ResearchRouter import failed: {exc}"))

        # 5. safe_scanner_available
        try:
            mod = importlib.import_module("regression_hardening.safety_scanner")
            if hasattr(mod, "SafetyScanner"):
                checks.append(_mk("safe_scanner_available", "PASS",
                                  "SafetyScanner importable from regression_hardening"))
            else:
                checks.append(_mk("safe_scanner_available", "WARN",
                                  "safety_scanner imported but SafetyScanner not found"))
        except Exception as exc:
            checks.append(_mk("safe_scanner_available", "WARN",
                               f"regression_hardening.safety_scanner: {exc}"))

        # 6. local_only
        try:
            import local_assistant as _la2
            ext_api_disabled = getattr(_la2, "EXTERNAL_API_DISABLED", None)
            if ext_api_disabled is True:
                checks.append(_mk("local_only", "PASS",
                                  "EXTERNAL_API_DISABLED=True in local_assistant"))
            else:
                checks.append(_mk("local_only", "FAIL",
                                  f"EXTERNAL_API_DISABLED={ext_api_disabled} (expected True)"))
        except Exception as exc:
            checks.append(_mk("local_only", "FAIL", f"local_assistant safety flags: {exc}"))

        # 7. external_api_disabled — scan source files
        la_dir = os.path.join(self._root, "local_assistant")
        if os.path.isdir(la_dir):
            found_external = []
            try:
                for fname in os.listdir(la_dir):
                    if not fname.endswith(".py"):
                        continue
                    fpath = os.path.join(la_dir, fname)
                    with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read().lower()
                    for imp in _FORBIDDEN_IMPORTS:
                        if f"import {imp}" in content:
                            found_external.append(f"{fname}:{imp}")
                if found_external:
                    checks.append(_mk("external_api_disabled", "FAIL",
                                      f"External API imports found: {found_external}"))
                else:
                    checks.append(_mk("external_api_disabled", "PASS",
                                      "No external API imports in local_assistant/"))
            except Exception as exc:
                checks.append(_mk("external_api_disabled", "WARN",
                                   f"External API file scan failed: {exc}"))
        else:
            checks.append(_mk("external_api_disabled", "WARN",
                               "local_assistant/ directory not found"))

        # 8. no_forbidden_actions
        try:
            from local_assistant.assistant_schema import ALLOWED_ACTIONS, FORBIDDEN_ACTIONS
            overlap = [a for a in ALLOWED_ACTIONS if a in FORBIDDEN_ACTIONS]
            if overlap:
                checks.append(_mk("no_forbidden_actions", "FAIL",
                                   f"ALLOWED_ACTIONS contains FORBIDDEN: {overlap}"))
            else:
                checks.append(_mk("no_forbidden_actions", "PASS",
                                   "ALLOWED_ACTIONS contains no FORBIDDEN_ACTIONS"))
        except Exception as exc:
            checks.append(_mk("no_forbidden_actions", "FAIL",
                               f"Schema import failed: {exc}"))

        # 9. unsafe_query_blocked
        try:
            from local_assistant.safe_answer_builder import SafeAnswerBuilder
            from local_assistant.assistant_schema import STATUS_BLOCKED
            builder = SafeAnswerBuilder()
            is_blocked = builder.is_unsafe_query("should i buy")
            answer = builder.build_unsafe_query_answer("should i buy")
            if is_blocked and answer.status == STATUS_BLOCKED:
                checks.append(_mk("unsafe_query_blocked", "PASS",
                                   "SafeAnswerBuilder correctly blocks 'should i buy'"))
            else:
                checks.append(_mk("unsafe_query_blocked", "FAIL",
                                   f"is_blocked={is_blocked}, status={answer.status} (expected BLOCKED_UNSAFE_QUERY)"))
        except Exception as exc:
            checks.append(_mk("unsafe_query_blocked", "FAIL",
                               f"Unsafe query blocking check failed: {exc}"))

        # 10. answer_generation_works
        try:
            from local_assistant.local_assistant_engine import LocalResearchAssistantEngine
            engine = LocalResearchAssistantEngine()
            answer = engine.ask(question="strategy validation", limit=3)
            if answer is not None and hasattr(answer, "status"):
                checks.append(_mk("answer_generation_works", "PASS",
                                   f"Answer generated: status={answer.status}, confidence={answer.confidence}"))
            else:
                checks.append(_mk("answer_generation_works", "WARN",
                                   "Answer generated but missing fields"))
        except Exception as exc:
            checks.append(_mk("answer_generation_works", "WARN",
                               f"Answer generation: {exc}"))

        # 11. output_ignored_by_git
        gitignore_path = os.path.join(self._root, ".gitignore")
        if os.path.isfile(gitignore_path):
            try:
                with open(gitignore_path, "r", encoding="utf-8") as fh:
                    content = fh.read()
                if "data/backtest_results/local_assistant/" in content:
                    checks.append(_mk("output_ignored_by_git", "PASS",
                                      "data/backtest_results/local_assistant/ is in .gitignore"))
                else:
                    checks.append(_mk("output_ignored_by_git", "WARN",
                                      "data/backtest_results/local_assistant/ not found in .gitignore"))
            except Exception as exc:
                checks.append(_mk("output_ignored_by_git", "WARN",
                                   f".gitignore read failed: {exc}"))
        else:
            checks.append(_mk("output_ignored_by_git", "WARN", ".gitignore not found"))

        # Summary
        total       = len(checks)
        pass_count  = sum(1 for c in checks if c["status"] == "PASS")
        warn_count  = sum(1 for c in checks if c["status"] == "WARN")
        fail_count  = sum(1 for c in checks if c["status"] == "FAIL")
        block_count = sum(1 for c in checks if c["status"] == "BLOCKED")

        if fail_count > 0:
            overall = "FAIL"
        elif warn_count > 0:
            overall = "WARNING"
        else:
            overall = "PASS"

        return {
            "checks":         checks,
            "total":          total,
            "pass_count":     pass_count,
            "warn_count":     warn_count,
            "fail_count":     fail_count,
            "blocked_count":  block_count,
            "overall_status": overall,
        }
