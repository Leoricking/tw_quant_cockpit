"""
replay/scenario_library.py — ReplayScenarioLibrary v1.2.1

Manages scenario templates. RSC- prefix for IDs.
Archived scenarios cannot be instantiated (must restore first).
Templates never contain future answers, realized returns, or future labels.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayScenarioLibrary:
    """
    Manages scenario templates. RSC- prefix for IDs.
    Archived scenarios cannot be instantiated (must restore first).
    Templates never contain future answers, realized returns, or future labels.
    """

    SCENARIO_ID_PREFIX = "RSC-"
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, validator=None, repo_root=None):
        self._repo_root = repo_root or "."
        if store is None:
            from replay.scenario_store import ReplayScenarioStore
            store = ReplayScenarioStore(repo_root=repo_root)
        if validator is None:
            from replay.scenario_validator import ReplayScenarioValidator
            validator = ReplayScenarioValidator()
        self._store = store
        self._validator = validator
        self._builtin_loaded = False

    def _ensure_builtins(self):
        if not self._builtin_loaded:
            self.load_builtin_templates()
            self._builtin_loaded = True

    def _generate_id(self, name: str = "") -> str:
        short = uuid.uuid4().hex[:8].upper()
        return f"{self.SCENARIO_ID_PREFIX}{short}"

    def create_template(self, name: str, category: str, difficulty: str, **kwargs) -> "ReplayScenarioTemplate":
        from replay.scenario_schema import ReplayScenarioTemplate
        now = _now_utc()
        scenario_id = kwargs.pop("scenario_id", None) or self._generate_id(name)
        template = ReplayScenarioTemplate(
            scenario_id=scenario_id,
            scenario_name=name,
            description=kwargs.pop("description", ""),
            category=category,
            difficulty=difficulty,
            objectives=kwargs.pop("objectives", []),
            instructions=kwargs.pop("instructions", ""),
            rules=kwargs.pop("rules", []),
            symbol_selector=kwargs.pop("symbol_selector", "FREE"),
            symbols=kwargs.pop("symbols", []),
            date_selector=kwargs.pop("date_selector", "FREE"),
            start_date=kwargs.pop("start_date", None),
            end_date=kwargs.pop("end_date", None),
            duration_days=kwargs.pop("duration_days", None),
            initial_visible_history_days=int(kwargs.pop("initial_visible_history_days", 120)),
            required_datasets=kwargs.pop("required_datasets", ["price"]),
            optional_datasets=kwargs.pop("optional_datasets", []),
            strict_future_firewall=bool(kwargs.pop("strict_future_firewall", True)),
            include_quality_gate=bool(kwargs.pop("include_quality_gate", True)),
            include_strategy_knowledge=bool(kwargs.pop("include_strategy_knowledge", True)),
            include_chips=bool(kwargs.pop("include_chips", False)),
            include_fundamental=bool(kwargs.pop("include_fundamental", False)),
            default_playback_speed=int(kwargs.pop("default_playback_speed", 1)),
            allowed_actions=kwargs.pop("allowed_actions", ["WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"]),
            tags=kwargs.pop("tags", []),
            source=kwargs.pop("source", "user"),
            version=str(kwargs.pop("version", "1")),
            archived=False,
            created_at=now,
            updated_at=now,
        )
        self._store.save_template(template)
        self._store.append_audit({"action": "CREATE", "scenario_id": scenario_id, "at": now})
        return template

    def update_template(self, scenario_id: str, **kwargs) -> Optional["ReplayScenarioTemplate"]:
        from replay.scenario_schema import ReplayScenarioTemplate
        d = self._store.load_template(scenario_id)
        if d is None:
            logger.warning("[ScenarioLibrary] update_template: not found %s", scenario_id)
            return None
        d.update(kwargs)
        d["updated_at"] = _now_utc()
        d["research_only"] = True
        d["no_real_orders"] = True
        template = ReplayScenarioTemplate.from_dict(d)
        self._store.update_template(template)
        self._store.append_audit({"action": "UPDATE", "scenario_id": scenario_id, "at": d["updated_at"]})
        return template

    def duplicate_template(self, scenario_id: str, new_name: Optional[str] = None) -> Optional["ReplayScenarioTemplate"]:
        from replay.scenario_schema import ReplayScenarioTemplate
        d = self._store.load_template(scenario_id)
        if d is None:
            return None
        new_id = self._generate_id()
        now = _now_utc()
        d["scenario_id"] = new_id
        d["scenario_name"] = new_name or f"{d.get('scenario_name', '')} (copy)"
        d["created_at"] = now
        d["updated_at"] = now
        d["archived"] = False
        d["source"] = "user"
        template = ReplayScenarioTemplate.from_dict(d)
        self._store.save_template(template)
        self._store.append_audit({"action": "DUPLICATE", "source_id": scenario_id, "new_id": new_id, "at": now})
        return template

    def archive_template(self, scenario_id: str) -> bool:
        d = self._store.load_template(scenario_id)
        if d is None:
            return False
        from replay.scenario_schema import ReplayScenarioTemplate
        d["archived"] = True
        d["updated_at"] = _now_utc()
        template = ReplayScenarioTemplate.from_dict(d)
        self._store.update_template(template)
        self._store.append_audit({"action": "ARCHIVE", "scenario_id": scenario_id, "at": d["updated_at"]})
        return True

    def restore_template(self, scenario_id: str) -> bool:
        d = self._store.load_template(scenario_id)
        if d is None:
            return False
        from replay.scenario_schema import ReplayScenarioTemplate
        d["archived"] = False
        d["updated_at"] = _now_utc()
        template = ReplayScenarioTemplate.from_dict(d)
        self._store.update_template(template)
        self._store.append_audit({"action": "RESTORE", "scenario_id": scenario_id, "at": d["updated_at"]})
        return True

    def list_templates(self, include_archived: bool = False) -> List[Dict[str, Any]]:
        self._ensure_builtins()
        templates = self._store.list_templates()
        if not include_archived:
            templates = [t for t in templates if not t.get("archived", False)]
        return templates

    def search_templates(self, query: str) -> List[Dict[str, Any]]:
        self._ensure_builtins()
        q = query.lower()
        templates = self._store.list_templates()
        results = []
        for t in templates:
            if (q in t.get("scenario_id", "").lower() or
                q in t.get("scenario_name", "").lower() or
                q in t.get("description", "").lower() or
                q in t.get("category", "").lower() or
                any(q in tag.lower() for tag in t.get("tags", []))):
                results.append(t)
        return results

    def filter_by_category(self, category: str) -> List[Dict[str, Any]]:
        self._ensure_builtins()
        return [t for t in self._store.list_templates() if t.get("category") == category and not t.get("archived", False)]

    def filter_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        self._ensure_builtins()
        return [t for t in self._store.list_templates() if t.get("difficulty") == difficulty and not t.get("archived", False)]

    def filter_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        self._ensure_builtins()
        return [t for t in self._store.list_templates() if tag in t.get("tags", []) and not t.get("archived", False)]

    def get_template(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        self._ensure_builtins()
        return self._store.load_template(scenario_id)

    def instantiate(
        self, scenario_id: str, symbol: str,
        start_date: Optional[str] = None, end_date: Optional[str] = None,
        overrides: Optional[Dict] = None,
    ) -> Optional["ReplayScenarioInstance"]:
        from replay.scenario_schema import ReplayScenarioInstance
        d = self._store.load_template(scenario_id)
        if d is None:
            logger.warning("[ScenarioLibrary] instantiate: template not found %s", scenario_id)
            return None
        if d.get("archived", False):
            logger.warning("[ScenarioLibrary] instantiate: template is archived %s. Restore first.", scenario_id)
            return None

        now = _now_utc()
        instance_id = f"RSI-{uuid.uuid4().hex[:8].upper()}"
        resolved_start = start_date or d.get("start_date", "")
        resolved_end = end_date or d.get("end_date", "")
        warnings = []
        if not resolved_start:
            warnings.append("start_date not resolved — FREE date selector, please specify")
        if not resolved_end:
            warnings.append("end_date not resolved — FREE date selector, please specify")

        instance = ReplayScenarioInstance(
            instance_id=instance_id,
            scenario_id=scenario_id,
            scenario_version=str(d.get("version", "1")),
            resolved_symbol=symbol,
            resolved_start_date=resolved_start or "",
            resolved_end_date=resolved_end or "",
            resolved_initial_date=None,
            qualification="OBSERVATIONAL_ONLY",
            data_availability={},
            warnings=warnings,
            generated_at=now,
        )
        self._store.save_instance(instance)
        return instance

    def export_template(self, scenario_id: str, output_path: Optional[str] = None) -> Optional[str]:
        d = self._store.load_template(scenario_id)
        if d is None:
            return None
        # Redact forbidden fields
        for f in ["api_key", "secret", "broker", "order_token"]:
            d.pop(f, None)
        from replay.scenario_validator import FORBIDDEN_PAYLOAD_FIELDS
        for f in FORBIDDEN_PAYLOAD_FIELDS:
            d.pop(f, None)
        if output_path is None:
            import os
            export_dir = Path(self._repo_root) / "data" / "replay_scenarios" / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(export_dir / f"{scenario_id}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        return output_path

    def import_template(self, path: str, dry_run: bool = True) -> Dict[str, Any]:
        from replay.scenario_schema import ReplayScenarioTemplate
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception as exc:
            return {"ok": False, "error": str(exc), "dry_run": dry_run}

        # Validate before importing
        template = ReplayScenarioTemplate.from_dict(d)
        result = self._validator.validate_template(template)
        if not result.valid:
            return {"ok": False, "errors": result.errors, "dry_run": dry_run}

        if not dry_run:
            template.source = "imported"
            self._store.save_template(template)
            self._store.append_audit({"action": "IMPORT", "scenario_id": template.scenario_id, "path": path, "at": _now_utc()})

        return {"ok": True, "scenario_id": template.scenario_id, "dry_run": dry_run, "warnings": result.warnings}

    def template_summary(self, scenario_id: Optional[str] = None) -> Dict[str, Any]:
        self._ensure_builtins()
        if scenario_id:
            d = self._store.load_template(scenario_id)
            if not d:
                return {"error": f"Not found: {scenario_id}"}
            instances = self._store.list_instances(scenario_id)
            return {"template": d, "instance_count": len(instances)}
        templates = self._store.list_templates()
        active = [t for t in templates if not t.get("archived", False)]
        archived = [t for t in templates if t.get("archived", False)]
        return {
            "total": len(templates),
            "active": len(active),
            "archived": len(archived),
            "categories": list({t.get("category") for t in active}),
            "research_only": True,
            "no_real_orders": True,
        }

    def load_builtin_templates(self) -> int:
        templates_dir = Path(self._repo_root) / "replay" / "templates"
        if not templates_dir.exists():
            return 0
        count = 0
        for p in sorted(templates_dir.glob("*.json")):
            try:
                with open(str(p), "r", encoding="utf-8") as f:
                    d = json.load(f)
                from replay.scenario_schema import ReplayScenarioTemplate
                template = ReplayScenarioTemplate.from_dict(d)
                # Only save if not already existing
                existing = self._store.load_template(template.scenario_id)
                if existing is None:
                    template.source = "builtin"
                    self._store.save_template(template)
                    count += 1
            except Exception as exc:
                logger.warning("[ScenarioLibrary] Failed loading builtin %s: %s", p, exc)
        return count
