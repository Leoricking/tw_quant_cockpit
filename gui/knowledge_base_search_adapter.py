"""
gui/knowledge_base_search_adapter.py — Adapter for Knowledge Base Search Panel integration.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True


def get_knowledge_base_search_panel_class():
    """Return the KnowledgeBaseSearchPanel class if available, else None."""
    try:
        from gui.knowledge_base_search_panel import KnowledgeBaseSearchPanel
        return KnowledgeBaseSearchPanel
    except Exception:
        return None


def is_knowledge_base_search_available() -> bool:
    """Return True if the Knowledge Base Search panel is available."""
    return get_knowledge_base_search_panel_class() is not None
