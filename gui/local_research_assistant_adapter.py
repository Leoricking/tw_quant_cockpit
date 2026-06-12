"""
gui/local_research_assistant_adapter.py — Adapter for Local Research Assistant Panel.
[!] Research Only. No Real Orders. No external API.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
EXTERNAL_API_DISABLED = True
RESEARCH_ONLY = True


def get_local_research_assistant_panel_class():
    try:
        from gui.local_research_assistant_panel import LocalResearchAssistantPanel
        return LocalResearchAssistantPanel
    except Exception:
        return None


def is_local_research_assistant_available() -> bool:
    return get_local_research_assistant_panel_class() is not None
