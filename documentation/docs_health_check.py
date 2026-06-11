"""
Documentation Health Check — v1.0.5 Documentation & User Guide Polish.
Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. VALIDATED does not enable trading.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

DOCS_DIR = "docs"
README_PATH = "README.md"

CORE_DOCS = {
    "README": README_PATH,
    "docs/index": "docs/index.md",
    "user_guide": "docs/user_guide_v1.0.md",
    "gui_user_guide": "docs/gui_user_guide_v1.0.md",
    "cli_cookbook": "docs/cli_cookbook_v1.0.md",
    "daily_workflow_sop": "docs/daily_workflow_sop_v1.0.md",
    "troubleshooting": "docs/troubleshooting_v1.0.md",
    "safety_guide": "docs/safety_guide_v1.0.md",
    "version_map": "docs/version_map_v1.0.md",
    "handoff_guide": "docs/handoff_guide_v1.0.md",
    "release_notes_v1.0": "docs/release_notes_v1.0.md",
    "roadmap": "docs/roadmap.md",
}

REQUIRED_SAFETY_PHRASES = [
    "Research Only",
    "No Real Orders",
    "Broker Execution Disabled",
    "VALIDATED does not enable trading",
]

FORBIDDEN_RECOMMENDATIONS = [
    "git add .",
    "cd xxx &&",
    "&&",
]


@dataclass
class DocHealthResult:
    name: str
    status: str  # PASS / WARN / FAIL / BLOCKED
    detail: str = ""


@dataclass
class DocHealthReport:
    results: List[DocHealthResult] = field(default_factory=list)

    def add(self, name: str, status: str, detail: str = "") -> None:
        self.results.append(DocHealthResult(name=name, status=status, detail=detail))

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results if r.status == "PASS")

    @property
    def warn_count(self) -> int:
        return sum(1 for r in self.results if r.status == "WARN")

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if r.status == "FAIL")

    @property
    def blocked_count(self) -> int:
        return sum(1 for r in self.results if r.status == "BLOCKED")

    @property
    def overall(self) -> str:
        if self.blocked_count > 0:
            return "BLOCKED"
        if self.fail_count > 0:
            return "FAIL"
        if self.warn_count > 0:
            return "WARN"
        return "PASS"


class DocumentationHealthCheck:
    """
    Checks presence and safety of all v1.0.5 documentation.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.report = DocHealthReport()

    def _path(self, rel: str) -> Path:
        return Path(self.base_dir) / rel

    def _read_safe(self, path: Path) -> Optional[str]:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None

    def check_core_docs_exist(self) -> None:
        missing = []
        present = []
        for name, rel in CORE_DOCS.items():
            p = self._path(rel)
            if p.exists():
                present.append(name)
            else:
                missing.append(name)
        if missing:
            self.report.add("Core Docs", "WARN", f"Missing: {missing}")
        else:
            self.report.add("Core Docs", "PASS", f"{len(present)}/{len(CORE_DOCS)} present")

    def check_safety_phrases_in_readme(self) -> None:
        p = self._path(README_PATH)
        if not p.exists():
            self.report.add("README safety phrases", "WARN", "README not found")
            return
        text = self._read_safe(p) or ""
        missing = [ph for ph in REQUIRED_SAFETY_PHRASES if ph not in text]
        if missing:
            self.report.add("README safety phrases", "WARN", f"Missing: {missing}")
        else:
            self.report.add("README safety phrases", "PASS", "All safety phrases present")

    def check_safety_phrases_in_user_guide(self) -> None:
        p = self._path("docs/user_guide_v1.0.md")
        if not p.exists():
            self.report.add("User Guide safety phrases", "WARN", "user_guide not found")
            return
        text = self._read_safe(p) or ""
        missing = [ph for ph in REQUIRED_SAFETY_PHRASES if ph not in text]
        if missing:
            self.report.add("User Guide safety phrases", "WARN", f"Missing: {missing}")
        else:
            self.report.add("User Guide safety phrases", "PASS", "All safety phrases present")

    def check_no_forbidden_actions_in_docs(self) -> None:
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            results = scanner.scan_directory("docs", patterns=["*.md"])
            blocked = [r for r in results if r.status == "BLOCKED"]
            if blocked:
                self.report.add(
                    "Docs forbidden actions",
                    "BLOCKED",
                    f"{len(blocked)} docs have forbidden actions: {[r.target for r in blocked[:3]]}",
                )
            else:
                self.report.add("Docs forbidden actions", "PASS", f"{len(results)} docs scanned, 0 blocked")
        except Exception as exc:
            self.report.add("Docs forbidden actions", "WARN", f"Scan failed: {exc}")

    def check_no_compound_command_recommendations(self) -> None:
        # Scan docs for compound command examples (&&, ;)
        bad_docs = []
        docs_dir = self._path("docs")
        if not docs_dir.exists():
            self.report.add("No compound commands in docs", "WARN", "docs/ not found")
            return
        for md_file in docs_dir.glob("*.md"):
            text = self._read_safe(md_file) or ""
            # Only flag if it looks like a shell command example, not a description
            import re
            if re.search(r'`[^`]*&&[^`]*`', text) or re.search(r'^\s*\$.*&&', text, re.MULTILINE):
                bad_docs.append(md_file.name)
        if bad_docs:
            self.report.add("No compound commands in docs", "WARN", f"Compound commands in: {bad_docs}")
        else:
            self.report.add("No compound commands in docs", "PASS", "No compound command examples found")

    def check_git_c_rule_documented(self) -> None:
        p = self._path("docs/handoff_guide_v1.0.md")
        if not p.exists():
            self.report.add("git -C rule documented", "WARN", "handoff_guide not found")
            return
        text = self._read_safe(p) or ""
        if "git -C" in text:
            self.report.add("git -C rule documented", "PASS", "git -C rule in handoff guide")
        else:
            self.report.add("git -C rule documented", "WARN", "git -C rule not found in handoff guide")

    def check_release_notes_updated(self) -> None:
        p = self._path("docs/release_notes_v1.0.md")
        if not p.exists():
            self.report.add("Release notes updated", "WARN", "release_notes_v1.0.md not found")
            return
        text = self._read_safe(p) or ""
        if "1.0.5" in text:
            self.report.add("Release notes updated", "PASS", "v1.0.5 present in release notes")
        else:
            self.report.add("Release notes updated", "WARN", "v1.0.5 not found in release notes")

    def check_roadmap_updated(self) -> None:
        p = self._path("docs/roadmap.md")
        if not p.exists():
            self.report.add("Roadmap updated", "WARN", "roadmap.md not found")
            return
        text = self._read_safe(p) or ""
        if "1.0.5" in text:
            self.report.add("Roadmap updated", "PASS", "v1.0.5 present in roadmap")
        else:
            self.report.add("Roadmap updated", "WARN", "v1.0.5 not found in roadmap")

    def run_all(self) -> DocHealthReport:
        self.check_core_docs_exist()
        self.check_safety_phrases_in_readme()
        self.check_safety_phrases_in_user_guide()
        self.check_no_forbidden_actions_in_docs()
        self.check_no_compound_command_recommendations()
        self.check_git_c_rule_documented()
        self.check_release_notes_updated()
        self.check_roadmap_updated()
        return self.report

    def print_report(self) -> None:
        print("=" * 60)
        print("TW Quant Cockpit — Documentation Health Check")
        print("Research Only | No Real Orders | Production Trading BLOCKED")
        print("Broker Execution Disabled | VALIDATED does not enable trading")
        print("=" * 60)
        for r in self.report.results:
            print(f"  {r.name}: {r.status}" + (f" — {r.detail}" if r.detail else ""))
        print("-" * 60)
        print(f"  PASS:    {self.report.pass_count}")
        print(f"  WARN:    {self.report.warn_count}")
        print(f"  FAIL:    {self.report.fail_count}")
        print(f"  BLOCKED: {self.report.blocked_count}")
        print(f"  OVERALL: {self.report.overall}")
        print("=" * 60)
