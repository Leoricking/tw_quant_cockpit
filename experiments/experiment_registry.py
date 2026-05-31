"""
experiments/experiment_registry.py — ExperimentRegistry: manages local experiment records (v0.3.29).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""

import datetime
import json
import logging
import os
import subprocess

from experiments.experiment_metadata import (
    ExperimentMetadata,
    generate_experiment_id,
    CREATED,
    RUNNING,
    COMPLETED,
    PARTIAL,
    FAILED,
    ARCHIVED,
    DAILY_RESEARCH,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_REGISTRY_FILE = "registry.json"


class ExperimentRegistry:
    """
    Local filesystem-backed registry for research experiments.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        registry_root: str = "experiments",
        results_dir: str = "data/backtest_results",
        report_dir: str = "reports",
    ):
        self._registry_root = os.path.join(BASE_DIR, registry_root)
        self._results_dir = os.path.join(BASE_DIR, results_dir)
        self._report_dir = os.path.join(BASE_DIR, report_dir)
        self._registry_path = os.path.join(self._registry_root, _REGISTRY_FILE)
        os.makedirs(self._registry_root, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_experiment(
        self,
        name: str = None,
        experiment_type: str = DAILY_RESEARCH,
        mode: str = "real",
        profile: str = "standard",
        tags: list = None,
        notes: str = None,
        source_command: str = "",
    ) -> ExperimentMetadata:
        """Create a new experiment entry and return its metadata."""
        try:
            experiment_id = generate_experiment_id()

            git_commit = self._get_git_commit()
            git_tag = self._get_git_tag()

            meta = ExperimentMetadata(
                experiment_id=experiment_id,
                experiment_name=name or "",
                experiment_type=experiment_type,
                status=CREATED,
                mode=mode,
                profile=profile,
                created_at=datetime.datetime.now().isoformat(),
                created_by="TW Quant Cockpit",
                git_commit=git_commit,
                git_tag=git_tag,
                tags=list(tags) if tags else [],
                notes=notes or "",
                source_command=source_command,
            )

            # Create directory structure
            exp_dir = os.path.join(self._registry_root, experiment_id)
            os.makedirs(os.path.join(exp_dir, "snapshots"), exist_ok=True)
            os.makedirs(os.path.join(exp_dir, "reports"), exist_ok=True)

            # Write metadata.json
            meta_path = os.path.join(exp_dir, "metadata.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta.to_dict(), f, indent=2, ensure_ascii=False)

            # Write notes.md
            notes_path = os.path.join(exp_dir, "notes.md")
            with open(notes_path, "w", encoding="utf-8") as f:
                f.write(f"# Notes: {experiment_id}\n\n")
                if notes:
                    f.write(f"{notes}\n")

            # Update registry.json
            entries = self._load_registry()
            entries.append({
                "experiment_id": experiment_id,
                "experiment_name": meta.experiment_name,
                "experiment_type": meta.experiment_type,
                "status": meta.status,
                "mode": meta.mode,
                "profile": meta.profile,
                "created_at": meta.created_at,
                "universe_name": meta.universe_name,
                "tags": meta.tags,
            })
            self._save_registry(entries)

            logger.info("Created experiment %s (%s)", experiment_id, experiment_type)
            return meta

        except Exception:
            logger.exception("create_experiment failed")
            raise

    def register_existing_run(
        self,
        experiment_id: str = None,
        source_command: str = None,
    ) -> ExperimentMetadata:
        """Register a run against an existing (or the latest) experiment."""
        try:
            if not experiment_id:
                experiments = self.list_experiments(limit=1)
                if not experiments:
                    raise ValueError("No experiments found in registry.")
                experiment_id = experiments[0]["experiment_id"]

            experiment_id = self._resolve_id(experiment_id)
            meta = self.get_experiment(experiment_id)
            if meta is None:
                raise ValueError(f"Experiment {experiment_id} not found.")

            if source_command:
                meta.source_command = source_command
            meta.status = COMPLETED

            self._save_metadata(meta)
            self._update_registry_entry(experiment_id, {"status": COMPLETED, "source_command": meta.source_command})
            logger.info("Registered run for experiment %s", experiment_id)
            return meta

        except Exception:
            logger.exception("register_existing_run failed")
            raise

    def list_experiments(
        self,
        limit: int = 50,
        status: str = None,
        experiment_type: str = None,
    ) -> list:
        """Return experiments sorted by created_at DESC, with optional filters."""
        try:
            entries = self._load_registry()

            if status:
                entries = [e for e in entries if e.get("status") == status]
            if experiment_type:
                entries = [e for e in entries if e.get("experiment_type") == experiment_type]

            # Sort descending by created_at
            entries.sort(key=lambda e: e.get("created_at", ""), reverse=True)

            return entries[:limit]

        except Exception:
            logger.exception("list_experiments failed")
            return []

    def get_experiment(self, experiment_id: str) -> ExperimentMetadata | None:
        """Load and return ExperimentMetadata for the given id, or None."""
        try:
            experiment_id = self._resolve_id(experiment_id)
            meta_path = os.path.join(self._registry_root, experiment_id, "metadata.json")
            if not os.path.exists(meta_path):
                return None
            with open(meta_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ExperimentMetadata.from_dict(data)
        except Exception:
            logger.exception("get_experiment failed for %s", experiment_id)
            return None

    def update_status(
        self,
        experiment_id: str,
        status: str,
        reason: str = None,
    ) -> bool:
        """Update the status of an experiment."""
        try:
            experiment_id = self._resolve_id(experiment_id)
            meta = self.get_experiment(experiment_id)
            if meta is None:
                logger.warning("update_status: experiment %s not found", experiment_id)
                return False

            meta.status = status
            if reason:
                meta.notes = meta.notes + f"\n[Status update to {status}]: {reason}"

            self._save_metadata(meta)
            self._update_registry_entry(experiment_id, {"status": status})
            logger.info("Updated status of %s to %s", experiment_id, status)
            return True

        except Exception:
            logger.exception("update_status failed for %s", experiment_id)
            return False

    def add_snapshot(
        self,
        experiment_id: str,
        snapshot_type: str,
        snapshot_path: str,
        summary: dict = None,
    ) -> bool:
        """Record a snapshot reference on the experiment metadata."""
        try:
            experiment_id = self._resolve_id(experiment_id)
            meta = self.get_experiment(experiment_id)
            if meta is None:
                logger.warning("add_snapshot: experiment %s not found", experiment_id)
                return False

            meta.snapshots[snapshot_type] = {
                "path": snapshot_path,
                "summary": summary or {},
                "generated_at": datetime.datetime.now().isoformat(),
            }
            self._save_metadata(meta)
            logger.info("Added snapshot %s to %s", snapshot_type, experiment_id)
            return True

        except Exception:
            logger.exception("add_snapshot failed for %s / %s", experiment_id, snapshot_type)
            return False

    def add_report(
        self,
        experiment_id: str,
        report_name: str,
        report_path: str,
        summary: str = None,
    ) -> bool:
        """Append a report reference to the experiment metadata."""
        try:
            experiment_id = self._resolve_id(experiment_id)
            meta = self.get_experiment(experiment_id)
            if meta is None:
                logger.warning("add_report: experiment %s not found", experiment_id)
                return False

            meta.reports.append({
                "name": report_name,
                "path": report_path,
                "summary": summary or "",
                "generated_at": datetime.datetime.now().isoformat(),
            })
            self._save_metadata(meta)
            logger.info("Added report %s to %s", report_name, experiment_id)
            return True

        except Exception:
            logger.exception("add_report failed for %s / %s", experiment_id, report_name)
            return False

    def archive_experiment(self, experiment_id: str) -> bool:
        """Archive an experiment."""
        return self.update_status(experiment_id, ARCHIVED)

    def build_registry_summary(self) -> dict:
        """Return aggregate statistics over all registered experiments."""
        try:
            entries = self._load_registry()

            by_status: dict = {}
            by_type: dict = {}
            for e in entries:
                s = e.get("status", "UNKNOWN")
                t = e.get("experiment_type", "UNKNOWN")
                by_status[s] = by_status.get(s, 0) + 1
                by_type[t] = by_type.get(t, 0) + 1

            sorted_entries = sorted(entries, key=lambda e: e.get("created_at", ""), reverse=True)
            latest = sorted_entries[0] if sorted_entries else {}

            return {
                "total": len(entries),
                "by_status": by_status,
                "by_type": by_type,
                "latest_experiment_id": latest.get("experiment_id", ""),
                "latest_created_at": latest.get("created_at", ""),
                "read_only": True,
                "no_real_orders": True,
                "production_blocked": True,
            }

        except Exception:
            logger.exception("build_registry_summary failed")
            return {
                "total": 0,
                "by_status": {},
                "by_type": {},
                "latest_experiment_id": "",
                "latest_created_at": "",
                "read_only": True,
                "no_real_orders": True,
                "production_blocked": True,
            }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_registry(self) -> list:
        """Load registry.json and return list of entry dicts."""
        try:
            if not os.path.exists(self._registry_path):
                return []
            with open(self._registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            logger.exception("_load_registry failed")
            return []

    def _save_registry(self, entries: list) -> None:
        """Write registry.json."""
        try:
            with open(self._registry_path, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        except Exception:
            logger.exception("_save_registry failed")

    def _save_metadata(self, meta: ExperimentMetadata) -> None:
        """Persist metadata.json for a given experiment."""
        try:
            exp_dir = os.path.join(self._registry_root, meta.experiment_id)
            os.makedirs(exp_dir, exist_ok=True)
            meta_path = os.path.join(exp_dir, "metadata.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception:
            logger.exception("_save_metadata failed for %s", meta.experiment_id)

    def _update_registry_entry(self, experiment_id: str, updates: dict) -> None:
        """Patch a single registry.json entry in place."""
        try:
            entries = self._load_registry()
            for entry in entries:
                if entry.get("experiment_id") == experiment_id:
                    entry.update(updates)
                    break
            self._save_registry(entries)
        except Exception:
            logger.exception("_update_registry_entry failed for %s", experiment_id)

    def _resolve_id(self, experiment_id: str) -> str:
        """Resolve 'latest' to the most-recent experiment_id; otherwise pass through."""
        if experiment_id and experiment_id.lower() == "latest":
            entries = self.list_experiments(limit=1)
            if entries:
                return entries[0]["experiment_id"]
        return experiment_id

    def _get_git_commit(self) -> str:
        """Return short HEAD commit hash, or empty string on failure."""
        try:
            result = subprocess.run(
                ["git", "-C", BASE_DIR, "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            logger.warning("Could not retrieve git commit hash")
        return ""

    def _get_git_tag(self) -> str:
        """Return exact git tag at HEAD, or empty string on failure."""
        try:
            result = subprocess.run(
                ["git", "-C", BASE_DIR, "describe", "--tags", "--exact-match", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            logger.warning("Could not retrieve git tag")
        return ""
