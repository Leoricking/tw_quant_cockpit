"""
maintenance/data_report_hygiene_engine.py — DataReportHygieneEngine for v1.0.2.

Scans the project for runtime outputs, report files, gitignore coverage,
and tracked runtime outputs. Review-only — never deletes, moves, or archives files.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Cleanup is Review Only. Archive Suggestions Only.
[!] No automatic deletion. No automatic archive. No file moves.
"""
from __future__ import annotations

import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from maintenance.data_report_hygiene_schema import (
    HygieneInventoryItem, HygieneReportManifest, HygieneSummary,
    CATEGORY_REPORT, CATEGORY_BACKTEST_RESULT, CATEGORY_IMPORT_DATA,
    CATEGORY_LOG, CATEGORY_CACHE, CATEGORY_EXPERIMENT_OUTPUT,
    CATEGORY_DATABASE, CATEGORY_SPREADSHEET, CATEGORY_JSON_OUTPUT,
    CATEGORY_UNKNOWN,
    ACTION_REVIEW, ACTION_READ_REPORT, ACTION_ARCHIVE_REVIEW,
    ACTION_CLEANUP_REVIEW, ACTION_KEEP_OBSERVING, ACTION_WAIT,
    SEV_INFO, SEV_LOW, SEV_MEDIUM, SEV_HIGH, SEV_BLOCKED,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_STALE_DAYS    = 30
_LARGE_BYTES   = 5 * 1024 * 1024  # 5 MB

_SCAN_EXTENSIONS = {".md", ".csv", ".json", ".db", ".sqlite", ".xlsx",
                    ".xls", ".log", ".zip", ".pkl"}

_SCAN_DIRS = [
    "reports",
    "data/backtest_results",
    "logs",
    "experiments",
    "data_cache",
    "journal_data",
]

_KEY_GITIGNORE_PATTERNS = [
    "data/backtest_results/",
    "*.db",
    "*.sqlite",
    "*.csv",
    "*.xlsx",
    "*.xls",
    "*.json",
    "__pycache__",
    "*.pyc",
    ".env",
]


def _classify_category(path: str) -> str:
    rel = path.lower()
    if rel.endswith(".md") and "reports" in rel:
        return CATEGORY_REPORT
    if "backtest_results" in rel:
        return CATEGORY_BACKTEST_RESULT
    if rel.endswith(".db") or rel.endswith(".sqlite"):
        return CATEGORY_DATABASE
    if rel.endswith(".xlsx") or rel.endswith(".xls"):
        return CATEGORY_SPREADSHEET
    if rel.endswith(".json"):
        return CATEGORY_JSON_OUTPUT
    if "log" in rel:
        return CATEGORY_LOG
    if "cache" in rel:
        return CATEGORY_CACHE
    if "experiment" in rel:
        return CATEGORY_EXPERIMENT_OUTPUT
    return CATEGORY_UNKNOWN


def _is_runtime_output(path: str) -> bool:
    rel = path.lower()
    return any(pat in rel for pat in [
        "backtest_results", "reports/", "logs/", "data_cache",
        "journal_data", "experiments",
    ])


class DataReportHygieneEngine:
    """Scans the project for data and report hygiene issues.

    Review-only. Never deletes, moves, or archives any files.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Data Cleanup is Review Only. Archive Suggestions Only.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    review_only        = True
    data_cleanup_review_only  = True
    archive_suggestions_only  = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/maintenance",
    ) -> None:
        if os.path.isabs(project_root):
            self._root = project_root
        else:
            self._root = os.path.join(BASE_DIR, project_root)
        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)

    def run(self, mode: str = "real") -> Tuple[
        List[HygieneInventoryItem],
        List[HygieneReportManifest],
        HygieneSummary,
        List[Dict[str, Any]],
    ]:
        """Run the full hygiene scan. Returns (inventory, manifests, summary, suggestions).

        [!] Review Only — no files deleted, moved, or archived.
        """
        inventory  = self.scan_inventory()
        manifests  = self.build_report_manifest()
        summary    = self.build_summary(inventory, manifests)
        suggestions = self.suggest_actions(inventory)
        return inventory, manifests, summary, suggestions

    def scan_inventory(self) -> List[HygieneInventoryItem]:
        """Scan configured directories for runtime output files."""
        items: List[HygieneInventoryItem] = []
        now = datetime.now(timezone.utc)

        for scan_dir in _SCAN_DIRS:
            abs_dir = os.path.join(self._root, scan_dir)
            if not os.path.isdir(abs_dir):
                continue
            for dirpath, _dirs, files in os.walk(abs_dir):
                for fname in files:
                    ext = os.path.splitext(fname)[1].lower()
                    if ext not in _SCAN_EXTENSIONS:
                        continue
                    fpath = os.path.join(dirpath, fname)
                    try:
                        stat = os.stat(fpath)
                    except OSError:
                        continue
                    size_bytes  = stat.st_size
                    mtime       = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
                    age_days    = (now - mtime).total_seconds() / 86400.0
                    modified_at = mtime.strftime("%Y-%m-%d %H:%M:%S")

                    rel_path    = os.path.relpath(fpath, self._root).replace("\\", "/")
                    category    = _classify_category(rel_path)
                    is_runtime  = _is_runtime_output(rel_path)
                    is_ignored  = self._is_gitignored(rel_path)
                    is_tracked  = False  # filled later if needed
                    should_ignore = is_runtime

                    severity, action, reason = self._assess(
                        rel_path, category, age_days, size_bytes,
                        is_runtime, is_ignored, is_tracked,
                    )

                    item_id = re.sub(r"[^a-zA-Z0-9_]", "_", rel_path)[:80]
                    items.append(HygieneInventoryItem(
                        item_id=item_id,
                        path=rel_path,
                        category=category,
                        file_type=ext,
                        size_bytes=size_bytes,
                        modified_at=modified_at,
                        age_days=round(age_days, 1),
                        is_runtime_output=is_runtime,
                        is_git_ignored=is_ignored,
                        is_git_tracked=is_tracked,
                        should_be_ignored=should_ignore,
                        action_hint=action,
                        severity=severity,
                        reason=reason,
                        no_real_orders=True,
                        production_blocked=True,
                        review_only=True,
                    ))
        return items

    def scan_reports(self) -> List[Dict[str, Any]]:
        """Scan reports/ for *.md files; group by type; find latest."""
        reports_dir = os.path.join(self._root, "reports")
        if not os.path.isdir(reports_dir):
            return []

        by_type: Dict[str, List[Dict[str, Any]]] = {}
        now = datetime.now(timezone.utc)

        for fname in os.listdir(reports_dir):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(reports_dir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                stat = os.stat(fpath)
                mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
                age_days = (now - mtime).total_seconds() / 86400.0
            except OSError:
                continue

            # Infer report type from filename
            base = os.path.splitext(fname)[0]
            # Strip trailing _YYYY-MM-DD or _YYYYMMDD
            report_type = re.sub(r"_\d{4}-\d{2}-\d{2}$", "", base)
            report_type = re.sub(r"_\d{8}$", "", report_type)

            entry = {
                "fname": fname,
                "fpath": fpath,
                "report_type": report_type,
                "mtime": mtime,
                "age_days": age_days,
                "size_bytes": stat.st_size,
            }
            by_type.setdefault(report_type, []).append(entry)

        result = []
        for rtype, entries in by_type.items():
            entries_sorted = sorted(entries, key=lambda x: x["mtime"], reverse=True)
            for i, e in enumerate(entries_sorted):
                e["is_latest"] = (i == 0)
                result.append(e)
        return result

    def scan_gitignore_coverage(self) -> Dict[str, bool]:
        """Read .gitignore and check if key patterns are covered."""
        gitignore_path = os.path.join(self._root, ".gitignore")
        coverage: Dict[str, bool] = {}
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except OSError:
            return {p: False for p in _KEY_GITIGNORE_PATTERNS}

        for pattern in _KEY_GITIGNORE_PATTERNS:
            coverage[pattern] = pattern in content
        return coverage

    def scan_git_tracked_runtime_outputs(self) -> List[str]:
        """Run git ls-files to find tracked runtime outputs."""
        try:
            result = subprocess.run(
                ["git", "-C", self._root, "ls-files", "--",
                 "data/backtest_results/", "reports/"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                return []
            lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
            return lines
        except Exception as exc:
            logger.warning("scan_git_tracked_runtime_outputs error: %s", exc)
            return []

    def build_report_manifest(self) -> List[HygieneReportManifest]:
        """Build HygieneReportManifest list from scan_reports."""
        scan = self.scan_reports()
        coverage = self.scan_gitignore_coverage()
        manifests: List[HygieneReportManifest] = []
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for entry in scan:
            rel_path = os.path.relpath(entry["fpath"], self._root).replace("\\", "/")
            is_ignored = self._is_gitignored(rel_path)
            should_ignore = True  # reports/ md files are runtime outputs

            try:
                from release.version_info import VERSION as _ver
            except Exception:
                _ver = "1.0.2"

            module = entry["report_type"].replace("_report", "").replace("_", " ").strip()
            summary = (
                f"age={round(entry['age_days'], 1)}d, "
                f"size={entry['size_bytes']}B, "
                f"latest={entry['is_latest']}, "
                f"ignored={is_ignored}"
            )

            rid = re.sub(r"[^a-zA-Z0-9_]", "_", entry["fname"])[:80]
            manifests.append(HygieneReportManifest(
                report_id=rid,
                report_path=rel_path,
                report_type=entry["report_type"],
                generated_at=entry["mtime"].strftime("%Y-%m-%d %H:%M:%S"),
                module=module,
                version=_ver,
                is_latest=entry["is_latest"],
                is_runtime_output=True,
                is_git_ignored=is_ignored,
                should_be_ignored=should_ignore,
                summary=summary,
                no_real_orders=True,
                review_only=True,
            ))
        return manifests

    def build_summary(
        self,
        inventory: List[HygieneInventoryItem],
        manifests: List[HygieneReportManifest],
    ) -> HygieneSummary:
        """Build aggregate HygieneSummary from inventory and manifests."""
        try:
            from release.version_info import VERSION as _ver
        except Exception:
            _ver = "1.0.2"

        coverage   = self.scan_gitignore_coverage()
        tracked    = self.scan_git_tracked_runtime_outputs()
        missing_ig = sum(1 for v in coverage.values() if not v)

        runtime_outputs = sum(1 for i in inventory if i.is_runtime_output)
        ignored_outputs = sum(1 for i in inventory if i.is_git_ignored)
        blocked_count   = sum(1 for i in inventory if i.severity == SEV_BLOCKED)
        warning_count   = sum(1 for i in inventory if i.severity in (SEV_HIGH, SEV_MEDIUM))
        stale_reports   = sum(
            1 for i in inventory
            if i.category == CATEGORY_REPORT and i.age_days > _STALE_DAYS
        )
        stale_csv   = sum(
            1 for i in inventory
            if i.file_type == ".csv" and i.age_days > _STALE_DAYS
        )
        stale_json  = sum(
            1 for i in inventory
            if i.file_type == ".json" and i.age_days > _STALE_DAYS
        )
        large_files = sum(1 for i in inventory if i.size_bytes > _LARGE_BYTES)
        db_files    = sum(1 for i in inventory if i.category == CATEGORY_DATABASE)
        ss_files    = sum(1 for i in inventory if i.category == CATEGORY_SPREADSHEET)

        report_count  = len(manifests)
        latest_count  = sum(1 for m in manifests if m.is_latest)

        return HygieneSummary(
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            version=_ver,
            total_items=len(inventory),
            runtime_outputs=runtime_outputs,
            git_tracked_runtime_outputs=len(tracked),
            ignored_outputs=ignored_outputs,
            missing_gitignore_rules=missing_ig,
            stale_reports=stale_reports,
            stale_csv_outputs=stale_csv,
            stale_json_outputs=stale_json,
            large_files=large_files,
            database_files=db_files,
            spreadsheet_files=ss_files,
            blocked_count=blocked_count,
            warning_count=warning_count,
            report_count=report_count,
            latest_reports=latest_count,
            no_real_orders=True,
            production_blocked=True,
            review_only=True,
        )

    def suggest_actions(self, inventory: List[HygieneInventoryItem]) -> List[Dict[str, Any]]:
        """Suggest review actions. Does NOT delete, move, or archive files.

        [!] Suggestions only. No automatic actions.
        """
        suggestions: List[Dict[str, Any]] = []
        for item in inventory:
            if item.severity in (SEV_HIGH, SEV_BLOCKED, SEV_MEDIUM):
                suggestion = {
                    "item_id": item.item_id,
                    "action": item.action_hint,
                    "reason": item.reason,
                    "suggestion": self._make_suggestion_text(item),
                    "no_real_orders": True,
                    "review_only": True,
                    "data_cleanup_review_only": True,
                }
                suggestions.append(suggestion)
        return suggestions

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _assess(
        self,
        rel_path: str,
        category: str,
        age_days: float,
        size_bytes: int,
        is_runtime: bool,
        is_ignored: bool,
        is_tracked: bool,
    ) -> Tuple[str, str, str]:
        """Return (severity, action_hint, reason)."""
        if is_tracked and is_runtime:
            return SEV_HIGH, ACTION_REVIEW, "Runtime output is git-tracked — consider adding to .gitignore"
        if category == CATEGORY_DATABASE:
            return SEV_MEDIUM, ACTION_REVIEW, "Database file found — should be in .gitignore"
        if category == CATEGORY_SPREADSHEET:
            return SEV_MEDIUM, ACTION_REVIEW, "Spreadsheet file found — should be in .gitignore"
        if size_bytes > _LARGE_BYTES:
            return SEV_MEDIUM, ACTION_REVIEW, f"Large file ({size_bytes // 1024}KB) — review if needed"
        if age_days > _STALE_DAYS and category == CATEGORY_REPORT:
            return SEV_LOW, ACTION_ARCHIVE_REVIEW, f"Report is {round(age_days, 0)}d old — review if still relevant"
        if age_days > _STALE_DAYS and is_runtime:
            return SEV_LOW, ACTION_CLEANUP_REVIEW, f"Stale runtime output ({round(age_days, 0)}d old)"
        if is_runtime and not is_ignored:
            return SEV_LOW, ACTION_REVIEW, "Runtime output not covered by .gitignore"
        return SEV_INFO, ACTION_KEEP_OBSERVING, "Normal runtime output"

    def _is_gitignored(self, rel_path: str) -> bool:
        """Rough check: is the path covered by .gitignore patterns?"""
        gitignore_path = os.path.join(self._root, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except OSError:
            return False
        # Check top-level dirs
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Directory pattern
            if line.endswith("/"):
                prefix = line.rstrip("/")
                if rel_path.startswith(prefix + "/") or rel_path == prefix:
                    return True
            # Wildcard extension
            if line.startswith("*."):
                ext = line[1:]
                if rel_path.endswith(ext):
                    return True
            # Exact or partial match
            if line in rel_path:
                return True
        return False

    def _make_suggestion_text(self, item: HygieneInventoryItem) -> str:
        if item.severity == SEV_HIGH:
            return (
                f"REVIEW: {item.path} is a runtime output and may need .gitignore coverage. "
                "Data Cleanup is Review Only — no automatic action."
            )
        if item.severity == SEV_MEDIUM:
            return (
                f"REVIEW: {item.path} ({item.category}) — verify it is in .gitignore "
                "and not accidentally committed. Archive Suggestions Only."
            )
        return (
            f"REVIEW: {item.path} — {item.reason}. "
            "Data Cleanup is Review Only. No automatic deletion."
        )
