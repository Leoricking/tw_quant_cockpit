"""
gui/replay_scenario_library_adapter.py — ReplayScenarioLibraryAdapter v1.2.1

Adapter connecting the scenario library panel to the backend.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Execute Strategy, No Auto Decision, No Start Trading, No Send Order.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReplayScenarioLibraryAdapter:
    """
    Adapter for scenario library GUI panel.
    [!] Research Only. No Real Orders. No Auto Decision. No Auto Scoring.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self._repo_root = repo_root or BASE_DIR
        self._library = None
        self._query = None
        self._validator = None
        self._initialized = False

    def _ensure_init(self):
        if self._initialized:
            return
        try:
            from replay.scenario_library import ReplayScenarioLibrary
            from replay.scenario_query import ReplayScenarioQuery
            from replay.scenario_validator import ReplayScenarioValidator
            self._library = ReplayScenarioLibrary(repo_root=self._repo_root)
            self._query = ReplayScenarioQuery(library=self._library, repo_root=self._repo_root)
            self._validator = ReplayScenarioValidator()
            self._initialized = True
        except Exception as exc:
            logger.warning("[ScenarioLibraryAdapter] Init failed: %s", exc)

    def list_scenarios(self, include_archived: bool = False) -> List[Dict[str, Any]]:
        self._ensure_init()
        if self._query:
            return self._query.list_scenarios(limit=200, include_archived=include_archived)
        return []

    def get_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        self._ensure_init()
        if self._query:
            return self._query.get_scenario(scenario_id)
        return None

    def search_scenarios(self, query: str) -> List[Dict[str, Any]]:
        self._ensure_init()
        if self._query:
            return self._query.search(query)
        return []

    def filter_by_category(self, category: str) -> List[Dict[str, Any]]:
        self._ensure_init()
        if self._query:
            return self._query.by_category(category)
        return []

    def filter_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        self._ensure_init()
        if self._query:
            return self._query.by_difficulty(difficulty)
        return []

    def validate_scenario(self, scenario_id: str) -> Dict[str, Any]:
        self._ensure_init()
        d = self.get_scenario(scenario_id)
        if not d:
            return {"valid": False, "error": f"Not found: {scenario_id}"}
        try:
            from replay.scenario_schema import ReplayScenarioTemplate
            template = ReplayScenarioTemplate.from_dict(d)
            result = self._validator.validate_template(template)
            return result.to_dict()
        except Exception as exc:
            return {"valid": False, "error": str(exc)}

    def archive_scenario(self, scenario_id: str) -> bool:
        self._ensure_init()
        if self._library:
            return self._library.archive_template(scenario_id)
        return False

    def restore_scenario(self, scenario_id: str) -> bool:
        self._ensure_init()
        if self._library:
            return self._library.restore_template(scenario_id)
        return False

    def export_scenario(self, scenario_id: str, output_path: Optional[str] = None) -> Optional[str]:
        self._ensure_init()
        if self._library:
            return self._library.export_template(scenario_id, output_path)
        return None

    def create_session_from_scenario(
        self, scenario_id: str, symbol: str,
        start_date: Optional[str] = None, end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a session from a scenario template."""
        self._ensure_init()
        try:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=self._repo_root)
            state = mgr.create_from_scenario(scenario_id, symbol, start_date, end_date)
            if state:
                return {"ok": True, "session_id": state.session_id}
            return {"ok": False, "error": "Session creation failed"}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def preview_batch(
        self, scenario_id: str, symbols: List[str],
    ) -> Dict[str, Any]:
        """Preview batch — dry run only."""
        self._ensure_init()
        try:
            from replay.batch_session_builder import ReplayBatchSessionBuilder
            builder = ReplayBatchSessionBuilder(repo_root=self._repo_root)
            return builder.preview_batch(scenario_id, symbols)
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def summary(self) -> Dict[str, Any]:
        self._ensure_init()
        if self._library:
            return self._library.template_summary()
        return {"error": "not available", "research_only": True}
