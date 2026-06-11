"""
Workflow Template Health Check — v1.0.6 Example Workflows & Templates.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from workflows.workflow_template_indexer import (
    EXAMPLES_DIR, TEMPLATES_DIR, REQUIRED_EXAMPLES, REQUIRED_TEMPLATES
)

REQUIRED_SAFETY_PHRASES = ["Research Only", "No Real Orders"]
FORBIDDEN_RECS = [r'`[^`]*&&[^`]*`', r'git add \\.']
FORBIDDEN_HEREDOC = [r'<<EOF', r'cat <<', r'heredoc']


@dataclass
class TemplateHealthResult:
    name: str
    status: str
    detail: str = ""


@dataclass
class TemplateHealthReport:
    results: List[TemplateHealthResult] = field(default_factory=list)

    def add(self, name: str, status: str, detail: str = "") -> None:
        self.results.append(TemplateHealthResult(name=name, status=status, detail=detail))

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


class WorkflowTemplateHealthCheck:
    """
    Checks presence and safety of all v1.0.6 workflow examples and templates.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.report = TemplateHealthReport()

    def _p(self, rel: str) -> Path:
        return Path(self.base_dir) / rel

    def _read(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""

    def check_examples_folder(self) -> None:
        d = self._p(EXAMPLES_DIR)
        if d.exists():
            count = len(list(d.glob("*.md")))
            self.report.add("examples folder", "PASS", f"{count} files")
        else:
            self.report.add("examples folder", "FAIL", f"{EXAMPLES_DIR} not found")

    def check_templates_folder(self) -> None:
        d = self._p(TEMPLATES_DIR)
        if d.exists():
            count = len(list(d.glob("*.md")))
            self.report.add("templates folder", "PASS", f"{count} files")
        else:
            self.report.add("templates folder", "FAIL", f"{TEMPLATES_DIR} not found")

    def check_required_examples(self) -> None:
        missing = [f for f in REQUIRED_EXAMPLES if not self._p(EXAMPLES_DIR + "/" + f).exists()]
        if missing:
            self.report.add("required examples", "WARN", f"Missing: {missing}")
        else:
            self.report.add("required examples", "PASS", f"{len(REQUIRED_EXAMPLES)}/{len(REQUIRED_EXAMPLES)} present")

    def check_required_templates(self) -> None:
        missing = [f for f in REQUIRED_TEMPLATES if not self._p(TEMPLATES_DIR + "/" + f).exists()]
        if missing:
            self.report.add("required templates", "WARN", f"Missing: {missing}")
        else:
            self.report.add("required templates", "PASS", f"{len(REQUIRED_TEMPLATES)}/{len(REQUIRED_TEMPLATES)} present")

    def check_safety_terms(self) -> None:
        issues = []
        for fname in REQUIRED_EXAMPLES + REQUIRED_TEMPLATES:
            for subdir in [EXAMPLES_DIR, TEMPLATES_DIR]:
                p = self._p(subdir + "/" + fname)
                if p.exists():
                    text = self._read(p)
                    for phrase in REQUIRED_SAFETY_PHRASES:
                        if phrase not in text:
                            issues.append(f"{fname}: missing '{phrase}'")
        if issues:
            self.report.add("safety terms", "WARN", f"{len(issues)} issues: {issues[:2]}")
        else:
            self.report.add("safety terms", "PASS", "Safety phrases present in all checked files")

    def check_no_forbidden_actions(self) -> None:
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            results_ex = scanner.scan_directory(EXAMPLES_DIR, patterns=["*.md"])
            results_tmpl = scanner.scan_directory(TEMPLATES_DIR, patterns=["*.md"])
            blocked = [r for r in results_ex + results_tmpl if r.status == "BLOCKED"]
            if blocked:
                self.report.add("no forbidden actions", "BLOCKED",
                                f"{len(blocked)} files blocked: {[r.target for r in blocked[:3]]}")
            else:
                total = len(results_ex) + len(results_tmpl)
                self.report.add("no forbidden actions", "PASS", f"{total} files scanned, 0 blocked")
        except Exception as exc:
            self.report.add("no forbidden actions", "WARN", f"Scan failed: {exc}")

    def check_no_compound_commands(self) -> None:
        bad = []
        for subdir in [EXAMPLES_DIR, TEMPLATES_DIR]:
            d = self._p(subdir)
            if not d.exists():
                continue
            for p in d.glob("*.md"):
                text = self._read(p)
                for pattern in FORBIDDEN_RECS:
                    if re.search(pattern, text):
                        bad.append(p.name)
                        break
        if bad:
            self.report.add("no compound commands", "WARN", f"Found in: {bad}")
        else:
            self.report.add("no compound commands", "PASS", "No compound command examples found")

    def check_no_git_add_dot(self) -> None:
        bad = []
        for subdir in [EXAMPLES_DIR, TEMPLATES_DIR]:
            d = self._p(subdir)
            if not d.exists():
                continue
            for p in d.glob("*.md"):
                text = self._read(p)
                if re.search(r'git add \\.', text) or "git add ." in text:
                    bad.append(p.name)
        if bad:
            self.report.add("no git add .", "WARN", f"Found in: {bad}")
        else:
            self.report.add("no git add .", "PASS", "No git add . found")

    def check_git_c_documented(self) -> None:
        p = self._p(EXAMPLES_DIR + "/claude_code_maintenance_example.md")
        if not p.exists():
            self.report.add("git -C documented", "WARN", "claude_code_maintenance_example.md not found")
            return
        text = self._read(p)
        if "git -C" in text:
            self.report.add("git -C documented", "PASS", "git -C in maintenance example")
        else:
            self.report.add("git -C documented", "WARN", "git -C not found in maintenance example")

    def check_no_heredoc_commit(self) -> None:
        bad = []
        for subdir in [EXAMPLES_DIR, TEMPLATES_DIR]:
            d = self._p(subdir)
            if not d.exists():
                continue
            for p in d.glob("*.md"):
                text = self._read(p)
                for pattern in FORBIDDEN_HEREDOC:
                    if pattern.lower() in text.lower():
                        # Check if it's in a code block as an example to avoid
                        # Only flag if it appears as a positive recommendation
                        if "do not use" not in text.lower() and "avoid" not in text.lower():
                            bad.append(p.name)
                            break
        if bad:
            self.report.add("no heredoc commit", "WARN", f"Possible heredoc in: {bad}")
        else:
            self.report.add("no heredoc commit", "PASS", "No heredoc commit recommendations found")

    def run_all(self) -> TemplateHealthReport:
        self.check_examples_folder()
        self.check_templates_folder()
        self.check_required_examples()
        self.check_required_templates()
        self.check_safety_terms()
        self.check_no_forbidden_actions()
        self.check_no_compound_commands()
        self.check_no_git_add_dot()
        self.check_git_c_documented()
        self.check_no_heredoc_commit()
        return self.report

    def print_report(self) -> None:
        print("=" * 60)
        print("TW Quant Cockpit — Workflow Templates Health Check")
        print("Research Only | No Real Orders | Production Trading BLOCKED")
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
