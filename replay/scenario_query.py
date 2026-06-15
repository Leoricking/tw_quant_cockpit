"""
replay/scenario_query.py — ReplayScenarioQuery v1.2.1

Query interface for replay scenario data.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScenarioQuery:
    """Query interface for replay scenario templates and instances."""

    def __init__(self, library=None, store=None, repo_root=None):
        self._library = library
        self._store = store
        if self._library is None:
            try:
                from replay.scenario_library import ReplayScenarioLibrary
                self._library = ReplayScenarioLibrary(repo_root=repo_root)
            except Exception as exc:
                logger.warning("[ScenarioQuery] Could not init library: %s", exc)
        if self._store is None and self._library is not None:
            self._store = getattr(self._library, "_store", None)

    def list_scenarios(self, limit: int = 100, include_archived: bool = False) -> List[Dict[str, Any]]:
        if self._library is None:
            return []
        return self._library.list_templates(include_archived=include_archived)[:limit]

    def active_scenarios(self) -> List[Dict[str, Any]]:
        return [t for t in self.list_scenarios(limit=1000) if not t.get("archived", False)]

    def archived_scenarios(self) -> List[Dict[str, Any]]:
        return [t for t in self.list_scenarios(limit=1000, include_archived=True) if t.get("archived", False)]

    def get_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        if self._library is None:
            return None
        return self._library.get_template(scenario_id)

    def search(self, query: str) -> List[Dict[str, Any]]:
        if self._library is None:
            return []
        return self._library.search_templates(query)

    def by_category(self, category: str) -> List[Dict[str, Any]]:
        if self._library is None:
            return []
        return self._library.filter_by_category(category)

    def by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        if self._library is None:
            return []
        return self._library.filter_by_difficulty(difficulty)

    def by_tag(self, tag: str) -> List[Dict[str, Any]]:
        if self._library is None:
            return []
        return self._library.filter_by_tag(tag)

    def latest_scenarios(self, limit: int = 20) -> List[Dict[str, Any]]:
        scenarios = self.list_scenarios(limit=1000)
        sorted_sc = sorted(scenarios, key=lambda t: t.get("created_at", ""), reverse=True)
        return sorted_sc[:limit]

    def scenario_instances(self, scenario_id: str) -> List[Dict[str, Any]]:
        if self._store is None:
            return []
        return self._store.list_instances(scenario_id)

    def scenario_summary(self, scenario_id: Optional[str] = None) -> Dict[str, Any]:
        if self._library is None:
            return {"error": "library not available"}
        return self._library.template_summary(scenario_id)
