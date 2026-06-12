"""
knowledge_base/kb_health_check.py — KnowledgeBaseHealthCheck for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Search. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

import logging
import os
from typing import List

logger = logging.getLogger(__name__)

_FORBIDDEN_ACTIONS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]


def _mk(check_id: str, name: str, status: str, message: str) -> dict:
    return {
        "check_id": check_id,
        "name":     name,
        "status":   status,
        "message":  message,
    }


class KnowledgeBaseHealthCheck:
    """Health check for the Knowledge Base Search feature v1.0.7.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    no_real_orders     = True
    broker_disabled    = True
    research_only      = True
    production_blocked = True

    def __init__(self, project_root: str = ".") -> None:
        self._root = os.path.abspath(project_root)

    def run(self) -> dict:
        """Run all health checks; return result dict."""
        checks: List[dict] = []

        # 1. knowledge_base_package_import
        checks.append(self._check_kb_package_import())

        # 2. docs_indexed
        checks.append(self._check_dir_exists("docs_indexed", "docs", "docs/ folder exists with .md files"))

        # 3. examples_indexed
        checks.append(self._check_dir_exists("examples_indexed", "docs/examples", "docs/examples/ exists"))

        # 4. templates_indexed
        checks.append(self._check_dir_exists("templates_indexed", "docs/templates", "docs/templates/ exists"))

        # 5. reports_indexed
        checks.append(self._check_dir_exists("reports_indexed", "reports", "reports/ exists"))

        # 6. readme_indexed
        checks.append(self._check_file_exists("readme_indexed", "README.md", "README.md exists"))

        # 7. safety_docs_indexed
        checks.append(self._check_safety_docs())

        # 8. handoff_guide_indexed
        checks.append(self._check_file_exists(
            "handoff_guide_indexed",
            os.path.join("docs", "handoff_guide_v1.0.md"),
            "docs/handoff_guide_v1.0.md exists",
        ))

        # 9. release_notes_indexed
        checks.append(self._check_file_exists(
            "release_notes_indexed",
            os.path.join("docs", "release_notes_v1.0.md"),
            "docs/release_notes_v1.0.md exists",
        ))

        # 10. workflow_templates_indexed
        checks.append(self._check_workflow_templates())

        # 11. search_works
        checks.append(self._check_search_works())

        # 12. safe_summary_works
        checks.append(self._check_safe_summary_works())

        # 13. no_forbidden_action_in_results
        checks.append(self._check_no_forbidden_action_in_results())

        # 14. no_broker_execution
        checks.append(self._check_no_broker_execution())

        # 15. no_external_api_dependency
        checks.append(self._check_no_external_api())

        # 16. output_ignored_by_git
        checks.append(self._check_gitignore())

        total         = len(checks)
        pass_count    = sum(1 for c in checks if c["status"] == "PASS")
        warn_count    = sum(1 for c in checks if c["status"] == "WARN")
        fail_count    = sum(1 for c in checks if c["status"] == "FAIL")
        blocked_count = sum(1 for c in checks if c["status"] == "BLOCKED")

        if blocked_count > 0:
            overall_status = "BLOCKED"
        elif fail_count > 0:
            overall_status = "FAIL"
        elif warn_count > 0:
            overall_status = "WARN"
        else:
            overall_status = "PASS"

        return {
            "checks":        checks,
            "total":         total,
            "pass_count":    pass_count,
            "warn_count":    warn_count,
            "fail_count":    fail_count,
            "blocked_count": blocked_count,
            "overall_status": overall_status,
            "no_real_orders": True,
            "research_only":  True,
        }

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_kb_package_import(self) -> dict:
        try:
            import knowledge_base
            has_flag = getattr(knowledge_base, "NO_REAL_ORDERS", False)
            if has_flag:
                return _mk("knowledge_base_package_import", "knowledge_base_package_import",
                           "PASS", "knowledge_base package imported; NO_REAL_ORDERS=True")
            else:
                return _mk("knowledge_base_package_import", "knowledge_base_package_import",
                           "WARN", "knowledge_base imported but NO_REAL_ORDERS flag missing")
        except Exception as exc:
            return _mk("knowledge_base_package_import", "knowledge_base_package_import",
                       "FAIL", f"Cannot import knowledge_base: {exc}")

    def _check_dir_exists(self, check_id: str, rel_path: str, name: str) -> dict:
        full = os.path.join(self._root, rel_path)
        if os.path.isdir(full):
            # Check for .md files if docs-like
            md_files = [f for f in os.listdir(full) if f.endswith(".md")] if rel_path.startswith("docs") else ["ok"]
            if md_files:
                return _mk(check_id, name, "PASS", f"{rel_path}/ exists ({len(md_files)} files)")
            else:
                return _mk(check_id, name, "WARN", f"{rel_path}/ exists but no .md files found")
        return _mk(check_id, name, "WARN", f"{rel_path}/ not found")

    def _check_file_exists(self, check_id: str, rel_path: str, name: str) -> dict:
        full = os.path.join(self._root, rel_path)
        if os.path.isfile(full):
            return _mk(check_id, name, "PASS", f"{rel_path} exists")
        return _mk(check_id, name, "WARN", f"{rel_path} not found")

    def _check_safety_docs(self) -> dict:
        docs_dir = os.path.join(self._root, "docs")
        if not os.path.isdir(docs_dir):
            return _mk("safety_docs_indexed", "safety_docs_indexed", "WARN", "docs/ not found")
        safety_files = [
            f for f in os.listdir(docs_dir)
            if f.endswith(".md") and any(k in f.lower() for k in ["safety", "safe"])
        ]
        if safety_files:
            return _mk("safety_docs_indexed", "safety_docs_indexed", "PASS",
                       f"Safety docs found: {', '.join(safety_files[:3])}")
        return _mk("safety_docs_indexed", "safety_docs_indexed", "WARN",
                   "No safety-related .md files found in docs/")

    def _check_workflow_templates(self) -> dict:
        docs_dir = os.path.join(self._root, "docs")
        if not os.path.isdir(docs_dir):
            return _mk("workflow_templates_indexed", "workflow_templates_indexed",
                       "WARN", "docs/ not found")
        # Check docs/ for workflow-related content
        workflow_files = []
        tpl_dir = os.path.join(docs_dir, "templates")
        ex_dir = os.path.join(docs_dir, "examples")
        if os.path.isdir(tpl_dir):
            workflow_files += [f for f in os.listdir(tpl_dir) if f.endswith(".md")]
        if os.path.isdir(ex_dir):
            workflow_files += [f for f in os.listdir(ex_dir) if f.endswith(".md")]
        if workflow_files:
            return _mk("workflow_templates_indexed", "workflow_templates_indexed", "PASS",
                       f"Workflow/template content found ({len(workflow_files)} files)")
        return _mk("workflow_templates_indexed", "workflow_templates_indexed", "WARN",
                   "No workflow or template .md files found")

    def _check_search_works(self) -> dict:
        try:
            from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
            engine = KnowledgeBaseSearchEngine()
            results = engine.search("research", limit=5)
            return _mk("search_works", "search_works", "PASS",
                       f"Search returned {len(results)} results for 'research'")
        except Exception as exc:
            return _mk("search_works", "search_works", "WARN",
                       f"Search failed (non-critical): {exc}")

    def _check_safe_summary_works(self) -> dict:
        import re
        # Whitelist phrases that contain forbidden substrings but are safe context
        _WHITELIST = [
            "no real orders", "no broker", "not investment advice",
            "does not enable trading", "broker execution disabled",
            "production trading blocked", "research only",
            "no auto trading", "blocked", "no_real_orders",
        ]
        try:
            from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
            engine = KnowledgeBaseSearchEngine()
            results = engine.search("research", limit=5)
            summary = engine.build_safe_summary(results)
            # Clean whitelist phrases before checking
            cleaned = summary.lower()
            for phrase in _WHITELIST:
                cleaned = cleaned.replace(phrase, " ")
            # Check for standalone forbidden action words
            _STANDALONE_FORBIDDEN = ["\\bbuy\\b", "\\bsell\\b", "\\bsubmit_order\\b",
                                     "\\bauto_trade\\b", "\\breal_trade\\b", "\\blive_trade\\b",
                                     "\\bbroker_order\\b", "\\bexecute\\b"]
            for pat in _STANDALONE_FORBIDDEN:
                if re.search(pat, cleaned):
                    return _mk("safe_summary_works", "safe_summary_works", "FAIL",
                               f"Forbidden pattern '{pat}' found in safe summary after whitelist removal")
            if "no real orders" in summary.lower():
                return _mk("safe_summary_works", "safe_summary_works", "PASS",
                           "Safe summary contains no forbidden actions and has No Real Orders note")
            return _mk("safe_summary_works", "safe_summary_works", "WARN",
                       "Safe summary works but missing 'No Real Orders' note")
        except Exception as exc:
            return _mk("safe_summary_works", "safe_summary_works", "WARN",
                       f"Safe summary check failed (non-critical): {exc}")

    def _check_no_forbidden_action_in_results(self) -> dict:
        from knowledge_base.kb_schema import SAFE_NEXT_STEPS
        try:
            from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
            engine = KnowledgeBaseSearchEngine()
            results = engine.search("strategy", limit=10)
            for r in results:
                step = r.safe_next_step.upper()
                if step not in [s.upper() for s in SAFE_NEXT_STEPS]:
                    return _mk("no_forbidden_action_in_results",
                               "no_forbidden_action_in_results", "WARN",
                               f"safe_next_step '{r.safe_next_step}' not in SAFE_NEXT_STEPS list")
            return _mk("no_forbidden_action_in_results",
                       "no_forbidden_action_in_results", "PASS",
                       "All search result safe_next_steps are in SAFE_NEXT_STEPS list")
        except Exception as exc:
            return _mk("no_forbidden_action_in_results",
                       "no_forbidden_action_in_results", "WARN",
                       f"Check failed (non-critical): {exc}")

    def _check_no_broker_execution(self) -> dict:
        try:
            import knowledge_base
            broker_disabled = getattr(knowledge_base, "BROKER_DISABLED", None)
            if broker_disabled is True:
                return _mk("no_broker_execution", "no_broker_execution", "PASS",
                           "BROKER_DISABLED=True in knowledge_base package")
            return _mk("no_broker_execution", "no_broker_execution", "WARN",
                       "BROKER_DISABLED flag not found or not True")
        except Exception as exc:
            return _mk("no_broker_execution", "no_broker_execution", "WARN",
                       f"Could not verify BROKER_DISABLED: {exc}")

    def _check_no_external_api(self) -> dict:
        kb_dir = os.path.join(self._root, "knowledge_base")
        if not os.path.isdir(kb_dir):
            return _mk("no_external_api_dependency", "no_external_api_dependency",
                       "WARN", "knowledge_base/ directory not found")
        forbidden_imports = ["openai", "anthropic", "faiss", "chromadb", "pinecone", "weaviate"]
        found = []
        try:
            for fname in os.listdir(kb_dir):
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(kb_dir, fname)
                with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read().lower()
                for imp in forbidden_imports:
                    if f"import {imp}" in content:
                        found.append(f"{fname}:{imp}")
            if found:
                return _mk("no_external_api_dependency", "no_external_api_dependency",
                           "FAIL", f"External API imports found: {found}")
            return _mk("no_external_api_dependency", "no_external_api_dependency",
                       "PASS", "No external API imports found in knowledge_base/")
        except Exception as exc:
            return _mk("no_external_api_dependency", "no_external_api_dependency",
                       "WARN", f"Check failed: {exc}")

    def _check_gitignore(self) -> dict:
        gitignore = os.path.join(self._root, ".gitignore")
        if not os.path.isfile(gitignore):
            return _mk("output_ignored_by_git", "output_ignored_by_git",
                       "WARN", ".gitignore not found")
        try:
            with open(gitignore, "r", encoding="utf-8") as fh:
                content = fh.read()
            if "data/backtest_results/knowledge_base" in content:
                return _mk("output_ignored_by_git", "output_ignored_by_git",
                           "PASS", "data/backtest_results/knowledge_base/ is in .gitignore")
            return _mk("output_ignored_by_git", "output_ignored_by_git",
                       "WARN", "data/backtest_results/knowledge_base/ not found in .gitignore")
        except Exception as exc:
            return _mk("output_ignored_by_git", "output_ignored_by_git",
                       "WARN", f"Could not read .gitignore: {exc}")
