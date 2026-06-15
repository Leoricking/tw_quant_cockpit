"""
governance_rollup/path_normalizer.py — CrossMachinePathNormalizer v1.1.9

Supports dual-computer paths for the trading_master repository.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT auto-move files.
[!] Does NOT auto-overwrite paths.
[!] Path migration defaults dry-run.
[!] Repo-external artifacts marked EXTERNAL_LOCAL_PATH.
[!] Missing local path does NOT mean artifact is gone.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True


class CrossMachinePathNormalizer:
    """
    Supports dual-computer paths:
    - D:/code/Claude/tw_quant_cockpit
    - C:/Users/Rossi/Documents/Claude/trading_master

    Rules:
    - Artifact registry prefers repo-relative paths
    - Does NOT auto-move files
    - Does NOT auto-overwrite paths
    - Path migration defaults dry-run
    - Repo-external artifacts marked EXTERNAL_LOCAL_PATH
    - Missing local path does NOT mean artifact is gone
    """

    KNOWN_REPO_ROOTS = [
        "D:/code/Claude/tw_quant_cockpit",
        "C:/Users/Rossi/Documents/Claude/trading_master",
    ]

    def __init__(self, repo_root: Optional[str] = None) -> None:
        self._explicit_root = repo_root

    def detect_repo_root(self) -> Optional[str]:
        """Detect current repo root by checking known locations."""
        if self._explicit_root:
            return self._explicit_root
        # Check explicit known roots first
        for root in self.KNOWN_REPO_ROOTS:
            norm_root = self.normalize_windows_path(root)
            if Path(norm_root).exists():
                return norm_root
        # Try to infer from this file's location
        this_file = Path(__file__).resolve()
        candidate = this_file.parent.parent  # governance_rollup/../
        if (candidate / "main.py").exists():
            return str(candidate).replace("\\", "/")
        return None

    def to_repo_relative(self, path: Any) -> Dict[str, Any]:
        """
        Convert an absolute path to a repo-relative path if possible.
        Returns a dict with: relative_path, original_path, classification
        """
        if path is None:
            return {
                "relative_path": None,
                "original_path": None,
                "classification": "NULL_PATH",
            }
        p = str(path).strip()
        norm = self.normalize_separator(p)
        repo_root = self.detect_repo_root()

        if repo_root:
            repo_norm = self.normalize_separator(repo_root).rstrip("/")
            if norm.lower().startswith(repo_norm.lower()):
                rel = norm[len(repo_norm):].lstrip("/")
                return {
                    "relative_path": rel,
                    "original_path": p,
                    "classification": "REPO_RELATIVE",
                }

        # Check if it's a known repo root from the other machine
        for known_root in self.KNOWN_REPO_ROOTS:
            norm_known = self.normalize_separator(known_root).rstrip("/")
            if norm.lower().startswith(norm_known.lower()):
                rel = norm[len(norm_known):].lstrip("/")
                return {
                    "relative_path": rel,
                    "original_path": p,
                    "classification": "CROSS_MACHINE_REPO_RELATIVE",
                }

        # Already relative
        if not (norm.startswith("C:/") or norm.startswith("D:/") or norm.startswith("/")):
            return {
                "relative_path": norm,
                "original_path": p,
                "classification": "ALREADY_RELATIVE",
            }

        # External absolute path
        return {
            "relative_path": None,
            "original_path": p,
            "classification": "EXTERNAL_LOCAL_PATH",
        }

    def resolve_repo_relative(self, path: str, repo_root: Optional[str] = None) -> Optional[str]:
        """Resolve a repo-relative path to absolute using the given or detected root."""
        root = repo_root or self.detect_repo_root()
        if not root:
            return None
        norm_root = self.normalize_separator(root).rstrip("/")
        norm_path = self.normalize_separator(path).lstrip("/")
        full = f"{norm_root}/{norm_path}"
        return full

    def normalize_windows_path(self, path: Any) -> str:
        """Normalize Windows path separators and drive letter casing."""
        if path is None:
            return ""
        p = str(path).strip()
        # Convert backslashes to forward slashes
        p = p.replace("\\", "/")
        # Normalize drive letter to uppercase C:/ D:/
        if len(p) >= 2 and p[1] == ":":
            p = p[0].upper() + p[1:]
        return p

    def normalize_separator(self, path: Any) -> str:
        """Normalize path separator to forward slash."""
        if path is None:
            return ""
        return str(path).strip().replace("\\", "/")

    def detect_stale_absolute_path(self, path: Any) -> Dict[str, Any]:
        """
        Detect if an absolute path is stale (points to a repo root that doesn't exist locally).
        A stale path does NOT mean the artifact is gone — it may exist on the other machine.
        """
        if path is None:
            return {"stale": False, "reason": "null_path", "path": None}
        norm = self.normalize_windows_path(str(path))
        # Check if it's a known repo root path that doesn't exist
        for known_root in self.KNOWN_REPO_ROOTS:
            norm_known = self.normalize_separator(known_root).rstrip("/")
            if norm.lower().startswith(norm_known.lower()):
                if not Path(self.normalize_separator(norm)).exists():
                    return {
                        "stale": True,
                        "reason": f"known_repo_root_path_not_found_locally: {known_root}",
                        "path": norm,
                        "note": "artifact may exist on the other machine",
                    }
                return {"stale": False, "reason": "path_exists", "path": norm}
        # Generic absolute path check
        if Path(self.normalize_separator(norm)).exists():
            return {"stale": False, "reason": "path_exists", "path": norm}
        if norm.startswith("C:/") or norm.startswith("D:/") or norm.startswith("/"):
            return {
                "stale": True,
                "reason": "absolute_path_not_found_locally",
                "path": norm,
                "note": "may exist on another machine or be deleted",
            }
        return {"stale": False, "reason": "relative_or_unknown", "path": norm}

    def map_known_repo_roots(self, path: Any) -> Dict[str, Any]:
        """
        Map a path across known repo roots (computer A <-> computer B).
        Returns candidate equivalent paths on each known machine.
        """
        if path is None:
            return {"mapped": [], "original": None}
        norm = self.normalize_windows_path(str(path))
        candidates = []
        for known_root in self.KNOWN_REPO_ROOTS:
            norm_known = self.normalize_separator(known_root).rstrip("/")
            if norm.lower().startswith(norm_known.lower()):
                rel = norm[len(norm_known):].lstrip("/")
                # Map to all other roots
                for other_root in self.KNOWN_REPO_ROOTS:
                    if other_root != known_root:
                        other_norm = self.normalize_separator(other_root).rstrip("/")
                        candidates.append({
                            "mapped_path": f"{other_norm}/{rel}",
                            "from_root": known_root,
                            "to_root": other_root,
                        })
                break
        return {"mapped": candidates, "original": norm}

    def validate_artifact_path(self, path: Any) -> Dict[str, Any]:
        """
        Validate an artifact path record.
        Returns: valid, classification, exists_locally, is_repo_relative, is_external
        """
        if path is None:
            return {
                "valid": False,
                "classification": "NULL_PATH",
                "exists_locally": False,
                "is_repo_relative": False,
                "is_external": False,
                "reason": "path is None",
            }
        norm = self.normalize_windows_path(str(path))
        result = self.to_repo_relative(norm)
        classification = result["classification"]
        is_repo_relative = classification in ("REPO_RELATIVE", "ALREADY_RELATIVE",
                                               "CROSS_MACHINE_REPO_RELATIVE")
        is_external = classification == "EXTERNAL_LOCAL_PATH"
        exists = False
        try:
            if result.get("relative_path"):
                resolved = self.resolve_repo_relative(result["relative_path"])
                if resolved:
                    exists = Path(self.normalize_separator(resolved)).exists()
            if not exists:
                exists = Path(self.normalize_separator(norm)).exists()
        except Exception:
            exists = False
        return {
            "valid": True,
            "classification": classification,
            "exists_locally": exists,
            "is_repo_relative": is_repo_relative,
            "is_external": is_external,
            "relative_path": result.get("relative_path"),
            "reason": "",
        }

    def compare_paths(self, path_a: Any, path_b: Any) -> Dict[str, Any]:
        """Compare two paths for logical equivalence across machines."""
        norm_a = self.normalize_windows_path(str(path_a)) if path_a else ""
        norm_b = self.normalize_windows_path(str(path_b)) if path_b else ""
        rel_a = self.to_repo_relative(norm_a)
        rel_b = self.to_repo_relative(norm_b)
        # Compare by relative path if available
        rp_a = rel_a.get("relative_path")
        rp_b = rel_b.get("relative_path")
        if rp_a and rp_b:
            equivalent = rp_a.lower() == rp_b.lower()
            return {
                "equivalent": equivalent,
                "method": "relative_path_compare",
                "relative_a": rp_a,
                "relative_b": rp_b,
            }
        return {
            "equivalent": norm_a.lower() == norm_b.lower(),
            "method": "normalized_absolute_compare",
        }

    def portable_path_record(self, path: Any) -> Dict[str, Any]:
        """
        Build a portable path record for storage in the artifact registry.
        Prefers repo-relative representation.
        """
        if path is None:
            return {"path": None, "relative_path": None, "classification": "NULL_PATH",
                    "portable": False}
        norm = self.normalize_windows_path(str(path))
        result = self.to_repo_relative(norm)
        stale = self.detect_stale_absolute_path(norm)
        return {
            "path": norm,
            "relative_path": result.get("relative_path"),
            "original_path": norm,
            "classification": result["classification"],
            "stale": stale.get("stale", False),
            "exists_locally": not stale.get("stale", True),
            "portable": result["classification"] in (
                "REPO_RELATIVE", "ALREADY_RELATIVE", "CROSS_MACHINE_REPO_RELATIVE"
            ),
        }
