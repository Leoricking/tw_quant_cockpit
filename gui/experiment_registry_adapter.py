"""
gui/experiment_registry_adapter.py — ExperimentRegistryAdapter: GUI bridge for Experiment Registry (v0.3.29).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""

import datetime
import glob
import json
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ExperimentRegistryAdapter:
    """
    Bridge between Experiment Registry backend and the GUI layer.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        registry_root: str = "experiments",
        report_dir: str = "reports",
    ):
        self._registry_root_rel = registry_root
        self._registry_root = os.path.join(BASE_DIR, registry_root)
        self._report_dir = os.path.join(BASE_DIR, report_dir)

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def create_experiment(
        self,
        name: str = None,
        experiment_type: str = "daily_research",
        mode: str = "real",
        profile: str = "standard",
        tags: list = None,
        notes: str = None,
    ) -> dict:
        """Create a new experiment. Returns status dict."""
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(registry_root=self._registry_root_rel)
            meta = reg.create_experiment(
                name=name,
                experiment_type=experiment_type,
                mode=mode,
                profile=profile,
                tags=tags,
                notes=notes,
            )
            return {
                "status": "ok",
                "experiment_id": meta.experiment_id,
                "experiment_name": meta.experiment_name,
                "created_at": meta.created_at,
                "mode": meta.mode,
                "profile": meta.profile,
                "read_only": True,
                "no_real_orders": True,
                "production_blocked": True,
                "error": None,
            }
        except Exception as exc:
            logger.exception("create_experiment failed")
            return {
                "status": "error",
                "experiment_id": "",
                "experiment_name": "",
                "created_at": "",
                "mode": mode,
                "profile": profile,
                "read_only": True,
                "no_real_orders": True,
                "production_blocked": True,
                "error": str(exc),
            }

    def register_latest_run(self, mode: str = "real") -> dict:
        """Register the latest run. Returns status dict."""
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(registry_root=self._registry_root_rel)
            meta = reg.register_existing_run()
            return {
                "status": "ok",
                "experiment_id": meta.experiment_id,
                "message": f"Registered run for {meta.experiment_id} (status: {meta.status})",
                "error": None,
            }
        except Exception as exc:
            logger.exception("register_latest_run failed")
            return {
                "status": "error",
                "experiment_id": "",
                "message": "",
                "error": str(exc),
            }

    def list_experiments(
        self,
        limit: int = 50,
        status: str = None,
        experiment_type: str = None,
    ) -> dict:
        """List experiments. Returns status dict with list of experiment dicts."""
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(registry_root=self._registry_root_rel)
            experiments = reg.list_experiments(
                limit=limit,
                status=status,
                experiment_type=experiment_type,
            )
            return {
                "status": "ok",
                "experiments": experiments,
                "total": len(experiments),
                "error": None,
            }
        except Exception as exc:
            logger.exception("list_experiments failed")
            return {
                "status": "error",
                "experiments": [],
                "total": 0,
                "error": str(exc),
            }

    def get_experiment_detail(self, experiment_id: str) -> dict:
        """Load full experiment detail including snapshots and reports."""
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(registry_root=self._registry_root_rel)

            resolved_id = experiment_id
            if experiment_id and experiment_id.lower() == "latest":
                entries = reg.list_experiments(limit=1)
                if entries:
                    resolved_id = entries[0]["experiment_id"]
                else:
                    return {
                        "status": "error",
                        "metadata": {},
                        "snapshots": {},
                        "reports": [],
                        "error": "No experiments found",
                    }

            meta = reg.get_experiment(resolved_id)
            if meta is None:
                return {
                    "status": "error",
                    "metadata": {},
                    "snapshots": {},
                    "reports": [],
                    "error": f"Experiment {resolved_id} not found",
                }

            return {
                "status": "ok",
                "metadata": meta.to_dict(),
                "snapshots": meta.snapshots,
                "reports": meta.reports,
                "error": None,
            }
        except Exception as exc:
            logger.exception("get_experiment_detail failed for %s", experiment_id)
            return {
                "status": "error",
                "metadata": {},
                "snapshots": {},
                "reports": [],
                "error": str(exc),
            }

    def build_notebook(self, experiment_id: str) -> dict:
        """Build notebook.md for an experiment."""
        try:
            from experiments.experiment_notebook import ExperimentNotebookBuilder
            builder = ExperimentNotebookBuilder(registry_root=self._registry_root_rel)
            path = builder.build_notebook(experiment_id)
            return {
                "status": "ok" if path else "error",
                "path": path,
                "experiment_id": experiment_id,
                "error": None if path else "build_notebook returned empty path",
            }
        except Exception as exc:
            logger.exception("build_notebook failed for %s", experiment_id)
            return {
                "status": "error",
                "path": "",
                "experiment_id": experiment_id,
                "error": str(exc),
            }

    def generate_report(self) -> dict:
        """Generate the experiment registry Markdown report."""
        try:
            from reports.experiment_registry_report import ExperimentRegistryReportBuilder
            builder = ExperimentRegistryReportBuilder(
                registry_root=self._registry_root_rel,
                report_dir=os.path.relpath(self._report_dir, BASE_DIR),
            )
            path = builder.build()

            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(registry_root=self._registry_root_rel)
            summary = reg.build_registry_summary()

            return {
                "status": "ok" if path else "error",
                "path": path,
                "total_experiments": summary.get("total", 0),
                "error": None if path else "build returned empty path",
            }
        except Exception as exc:
            logger.exception("generate_report failed")
            return {
                "status": "error",
                "path": "",
                "total_experiments": 0,
                "error": str(exc),
            }

    def compare(self, experiment_ids: list) -> dict:
        """Compare a list of experiments."""
        try:
            from experiments.experiment_comparator import ExperimentComparator
            comp = ExperimentComparator(registry_root=self._registry_root_rel)
            comparison = comp.compare(experiment_ids)
            return {
                "status": "ok",
                "comparison": comparison,
                "error": None,
            }
        except Exception as exc:
            logger.exception("compare failed for %s", experiment_ids)
            return {
                "status": "error",
                "comparison": {},
                "error": str(exc),
            }

    def load_latest_report_path(self) -> str | None:
        """Scan reports/ directory for the most recent experiment registry report."""
        try:
            pattern = os.path.join(
                self._report_dir, "experiment_registry_report_*.md"
            )
            files = glob.glob(pattern)
            if not files:
                return None
            return max(files, key=os.path.getmtime)
        except Exception:
            logger.exception("load_latest_report_path failed")
            return None

    def build_snapshots(self, experiment_id: str) -> dict:
        """
        Run ExperimentSnapshotBuilder.build_all() and save results to the
        experiment directory. Returns status dict.
        """
        try:
            from experiments.snapshot_builder import ExperimentSnapshotBuilder
            from experiments.experiment_registry import ExperimentRegistry

            builder = ExperimentSnapshotBuilder()
            reg = ExperimentRegistry(registry_root=self._registry_root_rel)

            resolved_id = experiment_id
            if experiment_id and experiment_id.lower() == "latest":
                entries = reg.list_experiments(limit=1)
                if entries:
                    resolved_id = entries[0]["experiment_id"]

            # Determine universe_name from metadata if possible
            meta = reg.get_experiment(resolved_id)
            universe_name = meta.universe_name if meta else None

            snapshots = builder.build_all(universe_name=universe_name)

            saved_count = 0
            snap_dir = os.path.join(self._registry_root, resolved_id, "snapshots")
            os.makedirs(snap_dir, exist_ok=True)

            for snap_type, snap_data in snapshots.items():
                try:
                    # Write snapshot JSON file
                    snap_file = os.path.join(snap_dir, f"{snap_type}.json")
                    with open(snap_file, "w", encoding="utf-8") as f:
                        json.dump(snap_data, f, indent=2, ensure_ascii=False)

                    # Register on metadata
                    reg.add_snapshot(
                        resolved_id,
                        snap_type,
                        snap_file,
                        summary=snap_data.get("summary", {}),
                    )
                    saved_count += 1
                except Exception:
                    logger.exception("build_snapshots: failed to save %s for %s", snap_type, resolved_id)

            return {
                "status": "ok",
                "experiment_id": resolved_id,
                "snapshots": snapshots,
                "saved_count": saved_count,
                "error": None,
            }

        except Exception as exc:
            logger.exception("build_snapshots failed for %s", experiment_id)
            return {
                "status": "error",
                "experiment_id": experiment_id,
                "snapshots": {},
                "saved_count": 0,
                "error": str(exc),
            }
