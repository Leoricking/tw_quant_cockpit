"""coverage_repair/store.py — CoverageRepairStore for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Lightweight versioned JSON store. Runtime path: data/coverage_repair/ (gitignored).
[!] Graceful on old schema (forward compatible).
"""
from __future__ import annotations

import json
import logging
import os
from typing import List, Optional

from coverage_repair.models_v133 import (
    CoverageRepairTask,
    RepairExecutionResult,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SCHEMA_VERSION = "1.3.3"
_DEFAULT_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "data", "coverage_repair")


class CoverageRepairStore:
    """Lightweight versioned JSON store for coverage repair tasks and execution results.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    schema_version = _SCHEMA_VERSION
    no_real_orders = True
    production_trading_blocked = True

    def __init__(self, base_dir: Optional[str] = None) -> None:
        self._base = base_dir or _DEFAULT_BASE
        self._tasks_dir = os.path.join(self._base, "tasks")
        self._exec_dir = os.path.join(self._base, "executions")
        os.makedirs(self._tasks_dir, exist_ok=True)
        os.makedirs(self._exec_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Task persistence
    # ------------------------------------------------------------------

    def save_task(self, task: CoverageRepairTask) -> None:
        """Save a CoverageRepairTask to disk."""
        try:
            path = os.path.join(self._tasks_dir, f"{task.task_id}.json")
            data = task.to_dict()
            data["_schema_version"] = _SCHEMA_VERSION
            data["_no_real_orders"] = True
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as exc:
            logger.warning("save_task error: %s", exc)

    def load_task(self, task_id: str) -> Optional[CoverageRepairTask]:
        """Load a CoverageRepairTask from disk. Returns None if not found."""
        try:
            path = os.path.join(self._tasks_dir, f"{task_id}.json")
            if not os.path.exists(path):
                return None
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            # Remove store-internal keys
            data.pop("_schema_version", None)
            data.pop("_no_real_orders", None)
            return CoverageRepairTask.from_dict(data)
        except Exception as exc:
            logger.warning("load_task %s error: %s", task_id, exc)
            return None

    def list_task_ids(self) -> List[str]:
        """List all stored task IDs."""
        try:
            return [f.replace(".json", "") for f in os.listdir(self._tasks_dir)
                    if f.endswith(".json")]
        except Exception as exc:
            logger.warning("list_task_ids error: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Execution result persistence
    # ------------------------------------------------------------------

    def save_execution(self, result: RepairExecutionResult) -> None:
        """Save an execution result to disk."""
        try:
            path = os.path.join(self._exec_dir, f"{result.execution_id}.json")
            data = result.to_dict()
            data["_schema_version"] = _SCHEMA_VERSION
            data["_no_real_orders"] = True
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as exc:
            logger.warning("save_execution error: %s", exc)

    def load_execution(self, execution_id: str) -> Optional[RepairExecutionResult]:
        """Load an execution result from disk. Returns None if not found."""
        try:
            path = os.path.join(self._exec_dir, f"{execution_id}.json")
            if not os.path.exists(path):
                return None
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            data.pop("_schema_version", None)
            data.pop("_no_real_orders", None)
            return RepairExecutionResult.from_dict(data)
        except Exception as exc:
            logger.warning("load_execution %s error: %s", execution_id, exc)
            return None

    def list_execution_ids(self) -> List[str]:
        """List all stored execution IDs."""
        try:
            return [f.replace(".json", "") for f in os.listdir(self._exec_dir)
                    if f.endswith(".json")]
        except Exception as exc:
            logger.warning("list_execution_ids error: %s", exc)
            return []
