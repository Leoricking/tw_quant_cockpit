"""
replay/scenario_store.py — ReplayScenarioStore v1.2.1

Persists scenario template and instance data.
Output: data/replay_scenarios/
Append-only history. Does NOT store: secrets, future labels, broker credentials.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScenarioStore:
    """
    Persists scenario templates and instances.
    Output: data/replay_scenarios/
    Append-only audit. Does NOT store secrets, future labels, broker credentials.
    """

    OUTPUT_DIR = "data/replay_scenarios"

    def __init__(self, repo_root=None):
        self.base_dir = Path(repo_root or ".") / self.OUTPUT_DIR
        self._ensure_dirs()

    # ------------------------------------------------------------------
    # Template CRUD
    # ------------------------------------------------------------------

    def save_template(self, template) -> None:
        self._ensure_dirs()
        templates_dir = self.base_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        d = template.to_dict() if hasattr(template, "to_dict") else template
        sid = d.get("scenario_id", "")
        if not sid:
            return
        template_path = templates_dir / f"{sid}.json"
        self._atomic_write_json(template_path, d)
        # Append to index
        index_file = self.base_dir / "templates.jsonl"
        self._append_jsonl(index_file, d)

    def update_template(self, template) -> None:
        self.save_template(template)

    def load_template(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        template_path = self.base_dir / "templates" / f"{scenario_id}.json"
        if not template_path.exists():
            return None
        try:
            with open(str(template_path), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("[ReplayScenarioStore] load_template failed %s: %s", scenario_id, exc)
            return None

    def list_templates(self) -> List[Dict[str, Any]]:
        templates_dir = self.base_dir / "templates"
        if not templates_dir.exists():
            return []
        results = []
        for p in sorted(templates_dir.glob("*.json")):
            try:
                with open(str(p), "r", encoding="utf-8") as f:
                    results.append(json.load(f))
            except Exception:
                pass
        return results

    # ------------------------------------------------------------------
    # Instance store
    # ------------------------------------------------------------------

    def save_instance(self, instance) -> None:
        self._ensure_dirs()
        instances_dir = self.base_dir / "instances"
        instances_dir.mkdir(parents=True, exist_ok=True)
        d = instance.to_dict() if hasattr(instance, "to_dict") else instance
        iid = d.get("instance_id", "")
        if not iid:
            return
        instance_path = instances_dir / f"{iid}.json"
        self._atomic_write_json(instance_path, d)
        index_file = self.base_dir / "instances.jsonl"
        self._append_jsonl(index_file, d)

    def load_instance(self, instance_id: str) -> Optional[Dict[str, Any]]:
        instance_path = self.base_dir / "instances" / f"{instance_id}.json"
        if not instance_path.exists():
            return None
        try:
            with open(str(instance_path), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("[ReplayScenarioStore] load_instance failed %s: %s", instance_id, exc)
            return None

    def list_instances(self, scenario_id: Optional[str] = None) -> List[Dict[str, Any]]:
        instances_dir = self.base_dir / "instances"
        if not instances_dir.exists():
            return []
        results = []
        for p in sorted(instances_dir.glob("*.json")):
            try:
                with open(str(p), "r", encoding="utf-8") as f:
                    d = json.load(f)
                    if scenario_id is None or d.get("scenario_id") == scenario_id:
                        results.append(d)
            except Exception:
                pass
        return results

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    def append_audit(self, entry: Dict[str, Any]) -> None:
        audit_file = self.base_dir / "scenario_audit.jsonl"
        self._append_jsonl(audit_file, entry)

    def rebuild_index(self) -> int:
        self._ensure_dirs()
        templates = self.list_templates()
        index_file = self.base_dir / "templates.jsonl"
        with open(str(index_file), "w", encoding="utf-8") as f:
            for t in templates:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")
        return len(templates)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _ensure_dirs(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)
        (self.base_dir / "templates").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "instances").mkdir(parents=True, exist_ok=True)

    def _atomic_write_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = str(path) + ".tmp_" + uuid.uuid4().hex[:8]
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, str(path))
        except Exception as exc:
            logger.warning("[ReplayScenarioStore] Atomic write failed %s: %s", path, exc)
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            raise

    def _append_jsonl(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(str(path), "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[ReplayScenarioStore] Append failed %s: %s", path, exc)

    def _load_jsonl(self, path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            return []
        results = []
        try:
            with open(str(path), "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        results.append(json.loads(line))
                    except json.JSONDecodeError:
                        logger.warning("[ReplayScenarioStore] Corrupted line %d in %s", line_no, path)
        except Exception as exc:
            logger.warning("[ReplayScenarioStore] Failed reading %s: %s", path, exc)
        return results
