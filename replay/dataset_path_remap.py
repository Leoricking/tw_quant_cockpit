"""
replay/dataset_path_remap.py — ReplayDatasetPathRemapper v1.2.8

Handles cross-computer path remapping.
All portable packages use relative paths only.
Path remap operations are explicitly recorded.
Absolute paths must NEVER appear in portable manifests.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetPathRemapper:
    """
    Cross-computer path remapping for portable packages.

    Rules:
    - Relative paths only in portable packages
    - Absolute paths must not be written to portable manifests
    - Path remap operations are explicitly recorded
    - Machine-specific paths are stripped from packages

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self):
        self._remap_history: List[Dict[str, Any]] = []

    def remap_paths(
        self,
        relative_paths: List[str],
        target_base_dir: str,
    ) -> Dict[str, str]:
        """
        Map relative paths to absolute paths on the current machine.
        Returns dict of relative_path -> absolute_path.
        Records the remap operation.
        """
        result: Dict[str, str] = {}
        for rel in relative_paths:
            abs_path = os.path.join(target_base_dir, rel)
            result[rel] = os.path.normpath(abs_path)
        self._remap_history.append({
            "operation":    "REMAP",
            "target_base":  target_base_dir,
            "path_count":   len(relative_paths),
            "paths":        relative_paths[:10],  # first 10 for audit
        })
        return result

    def strip_absolute(self, paths: List[str], base_dir: str = "") -> List[str]:
        """
        Convert absolute paths to relative by stripping base_dir prefix.
        If base_dir not provided, strips drive and root.
        """
        result = []
        for p in paths:
            p = p.replace("\\", "/")
            if base_dir:
                base = base_dir.replace("\\", "/").rstrip("/") + "/"
                if p.startswith(base):
                    p = p[len(base):]
            else:
                # Strip drive letter and root
                import re
                p = re.sub(r'^[A-Za-z]:[/\\]', '', p)
                p = p.lstrip("/\\")
            result.append(p)
        return result

    def validate_no_absolute(self, paths: List[str]) -> Dict[str, Any]:
        """Validate no absolute paths in the list."""
        absolute = []
        for p in paths:
            if os.path.isabs(p) or ":\\" in p or ":/" in p:
                absolute.append(p)
        return {
            "ok": len(absolute) == 0,
            "absolute_found": absolute,
        }

    def preview_remap(
        self,
        relative_paths: List[str],
        target_base_dir: str,
    ) -> List[Dict[str, str]]:
        """Preview path remap without recording."""
        plan = []
        for rel in relative_paths:
            abs_path = os.path.join(target_base_dir, rel)
            plan.append({
                "relative": rel,
                "absolute": os.path.normpath(abs_path),
                "exists":   str(os.path.exists(abs_path)),
            })
        return plan

    def remap_history(self) -> List[Dict[str, Any]]:
        return list(self._remap_history)
