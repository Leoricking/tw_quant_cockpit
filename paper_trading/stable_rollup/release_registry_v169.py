"""
paper_trading/stable_rollup/release_registry_v169.py
Release registry for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Dict, List, Optional

from paper_trading.stable_rollup.release_manifest_v169 import get_manifest


class ReleaseRegistry:
    """Registry for managing and validating v1.6.x releases."""

    def __init__(self) -> None:
        self._releases: Dict[str, dict] = {}
        self._commit_index: Dict[str, str] = {}  # commit -> version
        for entry in get_manifest():
            self._add_entry(entry)

    def _add_entry(self, entry: dict) -> None:
        v = entry["version"]
        commit = entry.get("commit", "")
        self._releases[v] = dict(entry)
        if commit and commit != "SEALED":
            self._commit_index[commit] = v

    def register_release(self, descriptor: dict) -> None:
        """Register a new release entry. Raises ValueError on duplicate version."""
        v = descriptor.get("version", "")
        if not v:
            raise ValueError("descriptor must have a 'version' field")
        if v in self._releases:
            raise ValueError(f"Duplicate version: {v!r}")
        commit = descriptor.get("commit", "")
        if commit and commit not in ("SEALED",) and commit in self._commit_index:
            raise ValueError(f"Duplicate commit: {commit!r}")
        self._add_entry(descriptor)

    def get_release(self, version: str) -> Optional[dict]:
        """Return release entry for version, or None."""
        entry = self._releases.get(version)
        return dict(entry) if entry else None

    def list_releases(self) -> List[dict]:
        """Return all registered releases in insertion order."""
        return [dict(v) for v in self._releases.values()]

    def get_release_by_commit(self, commit: str) -> Optional[dict]:
        """Return release entry matching commit, or None."""
        v = self._commit_index.get(commit)
        if v:
            return self.get_release(v)
        return None

    def get_parent_release(self, version: str) -> Optional[dict]:
        """Return the parent release, or None."""
        entry = self._releases.get(version)
        if not entry:
            return None
        parent_v = entry.get("parent_version")
        if parent_v is None:
            return None
        return self.get_release(parent_v)

    def get_children(self, version: str) -> List[dict]:
        """Return all releases whose parent_version equals version."""
        return [
            dict(e) for e in self._releases.values()
            if e.get("parent_version") == version
        ]

    def validate_release(self, version: str) -> dict:
        """Validate a specific release entry."""
        entry = self._releases.get(version)
        if not entry:
            return {"version": version, "valid": False, "issues": [f"Version {version!r} not found"]}
        issues = []
        if not entry.get("release_name"):
            issues.append("missing release_name")
        if not entry.get("release_category"):
            issues.append("missing release_category")
        parent_v = entry.get("parent_version")
        if parent_v and parent_v not in self._releases:
            issues.append(f"parent_version {parent_v!r} not registered")
        return {
            "version": version,
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def validate_parent_chain(self) -> dict:
        """Detect cycles and missing parents in the release chain."""
        issues = []
        visited = set()

        def detect_cycle(v, path):
            if v in path:
                issues.append(f"Cycle detected: {' -> '.join(path + [v])}")
                return
            if v in visited:
                return
            visited.add(v)
            path = path + [v]
            for child_entry in self.get_children(v):
                detect_cycle(child_entry["version"], path)

        # Find roots (no parent)
        roots = [v for v, e in self._releases.items() if e.get("parent_version") is None]
        for root in roots:
            detect_cycle(root, [])

        # Check for missing parents
        for v, entry in self._releases.items():
            parent_v = entry.get("parent_version")
            if parent_v and parent_v not in self._releases:
                issues.append(f"Missing parent {parent_v!r} for {v!r}")

        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "roots": roots,
        }

    def validate_unique_versions(self) -> dict:
        """Validate no duplicate version strings."""
        seen = set()
        dupes = []
        for v in self._releases:
            if v in seen:
                dupes.append(v)
            seen.add(v)
        return {
            "status": "PASS" if not dupes else "FAIL",
            "duplicates": dupes,
            "total": len(self._releases),
        }

    def validate_unique_commits(self) -> dict:
        """Validate no duplicate non-SEALED commits."""
        commit_map: Dict[str, List[str]] = {}
        for v, entry in self._releases.items():
            commit = entry.get("commit", "")
            if commit and commit != "SEALED":
                commit_map.setdefault(commit, []).append(v)
        dupes = {c: vs for c, vs in commit_map.items() if len(vs) > 1}
        return {
            "status": "PASS" if not dupes else "FAIL",
            "duplicates": dupes,
        }

    def validate_sealed_status(self) -> dict:
        """Validate that historical releases are sealed, current is not."""
        issues = []
        current_version = "1.6.9"
        for v, entry in self._releases.items():
            sealed = entry.get("sealed_status", "")
            if v == current_version:
                if sealed == "SEALED":
                    issues.append(f"{v!r} should NOT be SEALED (current release)")
            else:
                if sealed not in ("SEALED",):
                    issues.append(f"{v!r} should be SEALED (historical release), got {sealed!r}")
        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
        }

    def release_summary(self) -> dict:
        """Return summary statistics of registered releases."""
        total = len(self._releases)
        sealed = sum(1 for e in self._releases.values() if e.get("sealed_status") == "SEALED")
        hotfixes = sum(1 for e in self._releases.values() if e.get("release_category") == "hotfix")
        return {
            "total": total,
            "sealed": sealed,
            "hotfixes": hotfixes,
            "versions": list(self._releases.keys()),
        }


_REGISTRY_SINGLETON: Optional[ReleaseRegistry] = None


def get_registry() -> ReleaseRegistry:
    """Return singleton ReleaseRegistry instance."""
    global _REGISTRY_SINGLETON
    if _REGISTRY_SINGLETON is None:
        _REGISTRY_SINGLETON = ReleaseRegistry()
    return _REGISTRY_SINGLETON
