"""
monitoring/model_registry.py — Model Registry for v0.4.3 Model Monitoring.

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class ModelMetadata:
    """Metadata for a registered research model."""

    # Identity
    model_id: str
    model_name: str
    model_type: str
    version: str
    created_at: str

    # Data lineage
    feature_snapshot_id: str = ""
    dataset_path: str = ""
    target_label: str = ""
    train_start: str = ""
    train_end: str = ""
    validation_start: str = ""
    validation_end: str = ""

    # Sizes
    feature_count: int = 0
    row_count: int = 0

    # Status
    leakage_status: str = "UNKNOWN"
    training_status: str = "RESEARCH_ONLY"
    monitoring_status: str = "ACTIVE"
    notes: str = ""

    # Safety flags — always True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "model_id":            self.model_id,
            "model_name":          self.model_name,
            "model_type":          self.model_type,
            "version":             self.version,
            "created_at":          self.created_at,
            "feature_snapshot_id": self.feature_snapshot_id,
            "dataset_path":        self.dataset_path,
            "target_label":        self.target_label,
            "train_start":         self.train_start,
            "train_end":           self.train_end,
            "validation_start":    self.validation_start,
            "validation_end":      self.validation_end,
            "feature_count":       self.feature_count,
            "row_count":           self.row_count,
            "leakage_status":      self.leakage_status,
            "training_status":     self.training_status,
            "monitoring_status":   self.monitoring_status,
            "notes":               self.notes,
            "research_only":       self.research_only,
            "no_real_orders":      self.no_real_orders,
        }


class ModelRegistry:
    """
    Registry for research model metadata.

    [!] Monitoring Only. Read Only. No Real Orders.
    Runtime outputs → model_monitoring/ (not committed).
    """

    read_only      = True
    no_real_orders = True

    _SAFETY = {
        "monitoring_only":      True,
        "read_only":            True,
        "no_real_orders":       True,
        "production_blocked":   True,
        "real_order_ready":     False,
    }

    def __init__(self, registry_root: str = "model_monitoring"):
        if os.path.isabs(registry_root):
            self._root = registry_root
        else:
            self._root = os.path.join(_BASE_DIR, registry_root)

        self._models_dir    = os.path.join(self._root, "models")
        self._registry_file = os.path.join(self._root, "registry.json")

        os.makedirs(self._models_dir, exist_ok=True)

        self._index: dict = self._load_index()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load_index(self) -> dict:
        if os.path.isfile(self._registry_file):
            try:
                with open(self._registry_file, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception as exc:
                logger.warning("ModelRegistry._load_index: %s", exc)
        return {"models": {}, "updated_at": ""}

    def _save_index(self):
        self._index["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self._registry_file, "w", encoding="utf-8") as fh:
                json.dump(self._index, fh, indent=2, ensure_ascii=False)
        except Exception as exc:
            logger.error("ModelRegistry._save_index: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_model(self, metadata: ModelMetadata) -> dict:
        """Save metadata and update registry index."""
        d = metadata.to_dict()
        model_path = os.path.join(self._models_dir, f"{metadata.model_id}.json")
        try:
            with open(model_path, "w", encoding="utf-8") as fh:
                json.dump(d, fh, indent=2, ensure_ascii=False)
            self._index.setdefault("models", {})[metadata.model_id] = {
                "model_name":        metadata.model_name,
                "model_type":        metadata.model_type,
                "version":           metadata.version,
                "created_at":        metadata.created_at,
                "monitoring_status": metadata.monitoring_status,
                "leakage_status":    metadata.leakage_status,
                "path":              model_path,
            }
            self._save_index()
            logger.info("ModelRegistry: registered %s", metadata.model_id)
            return {"ok": True, "model_id": metadata.model_id, **self._SAFETY}
        except Exception as exc:
            logger.error("ModelRegistry.register_model: %s", exc)
            return {"ok": False, "error": str(exc), **self._SAFETY}

    def list_models(self) -> list:
        """Return list of metadata dicts from registry."""
        results = []
        for model_id in list(self._index.get("models", {}).keys()):
            d = self.get_model(model_id)
            if d:
                results.append(d)
        return results

    def get_model(self, model_id: str) -> Optional[dict]:
        model_path = os.path.join(self._models_dir, f"{model_id}.json")
        if os.path.isfile(model_path):
            try:
                with open(model_path, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception as exc:
                logger.warning("ModelRegistry.get_model(%s): %s", model_id, exc)
        return None

    def update_status(self, model_id: str, status: str, reason: str = None) -> dict:
        """Update monitoring_status for a model."""
        d = self.get_model(model_id)
        if d is None:
            return {"ok": False, "error": f"model_id not found: {model_id}", **self._SAFETY}
        d["monitoring_status"] = status
        if reason:
            d["notes"] = (d.get("notes", "") + f" | status_update: {reason}").strip(" |")
        model_path = os.path.join(self._models_dir, f"{model_id}.json")
        try:
            with open(model_path, "w", encoding="utf-8") as fh:
                json.dump(d, fh, indent=2, ensure_ascii=False)
            if model_id in self._index.get("models", {}):
                self._index["models"][model_id]["monitoring_status"] = status
            self._save_index()
            return {"ok": True, "model_id": model_id, "status": status, **self._SAFETY}
        except Exception as exc:
            logger.error("ModelRegistry.update_status: %s", exc)
            return {"ok": False, "error": str(exc), **self._SAFETY}

    def summary(self) -> dict:
        """Return model count and status breakdown."""
        models = self._index.get("models", {})
        status_counts: dict = {}
        for info in models.values():
            s = info.get("monitoring_status", "UNKNOWN")
            status_counts[s] = status_counts.get(s, 0) + 1
        return {
            "model_count":    len(models),
            "status_breakdown": status_counts,
            **self._SAFETY,
        }
