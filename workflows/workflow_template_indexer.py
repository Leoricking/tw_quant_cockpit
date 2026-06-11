"""
Workflow Template Indexer — v1.0.6 Example Workflows & Templates.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import csv
import datetime
import os
from pathlib import Path
from typing import List, Dict, Optional
from workflows.workflow_template_schema import WorkflowTemplateItem, CATEGORIES

EXAMPLES_DIR = "docs/examples"
TEMPLATES_DIR = "docs/templates"
OUTPUT_DIR = "data/backtest_results/workflows"

REQUIRED_EXAMPLES = [
    "daily_operation_example.md",
    "weekend_review_example.md",
    "single_stock_research_example.md",
    "strategy_validation_example.md",
    "crash_reversal_review_example.md",
    "data_hygiene_example.md",
    "gui_operation_example.md",
    "claude_code_maintenance_example.md",
    "troubleshooting_example.md",
    "paper_mock_practice_example.md",
]

REQUIRED_TEMPLATES = [
    "daily_review_template.md",
    "single_stock_research_template.md",
    "strategy_idea_template.md",
    "backtest_review_template.md",
    "weekly_retrospective_template.md",
    "error_report_template.md",
    "release_prompt_template.md",
    "handoff_summary_template.md",
]

CATEGORY_MAP = {
    "daily_operation": "DAILY",
    "weekend_review": "WEEKEND",
    "single_stock": "STOCK_RESEARCH",
    "strategy_validation": "STRATEGY_VALIDATION",
    "crash_reversal": "CRASH_REVERSAL",
    "data_hygiene": "DATA_HYGIENE",
    "gui_operation": "GUI",
    "claude_code": "CLAUDE_CODE",
    "troubleshooting": "TROUBLESHOOTING",
    "paper_mock": "PAPER_MOCK",
    "release_prompt": "RELEASE",
    "handoff": "HANDOFF",
    "daily_review": "DAILY",
    "strategy_idea": "STRATEGY_VALIDATION",
    "backtest_review": "STRATEGY_VALIDATION",
    "weekly_retro": "WEEKEND",
    "error_report": "TROUBLESHOOTING",
}


class WorkflowTemplateIndexer:
    """
    Indexes all workflow examples and templates.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self._manifest: List[WorkflowTemplateItem] = []

    def _p(self, rel: str) -> Path:
        return Path(self.base_dir) / rel

    def _read_safe(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""

    def _extract_title(self, path: Path) -> str:
        for line in self._read_safe(path).splitlines()[:5]:
            if line.startswith("# "):
                return line[2:].strip()
        return path.stem

    def _get_category(self, stem: str) -> str:
        lower = stem.lower()
        for key, cat in CATEGORY_MAP.items():
            if key in lower:
                return cat
        return "DAILY"

    def _build_item(self, path: Path, item_type: str, idx: int) -> WorkflowTemplateItem:
        text = self._read_safe(path)
        return WorkflowTemplateItem(
            template_id=f"{item_type.upper()}-{idx:03d}",
            path=str(path),
            title=self._extract_title(path),
            category=self._get_category(path.stem),
            description=f"{item_type}: {path.stem}",
            safety_covered="Research Only" in text or "No Real Orders" in text,
            no_real_orders=True,
            broker_disabled=True,
            has_allowed_actions=any(a in text for a in ["REVIEW", "WAIT", "BACKTEST_MORE", "READ_REPORT", "KEEP_OBSERVING"]),
            has_forbidden_actions=False,
            has_cli_examples="python main.py" in text,
            has_gui_steps="GUI" in text or "tab" in text.lower(),
            status="PASS",
            reason="",
        )

    def collect_examples(self) -> List[Path]:
        d = self._p(EXAMPLES_DIR)
        if not d.exists():
            return []
        return sorted(d.glob("*.md"))

    def collect_templates(self) -> List[Path]:
        d = self._p(TEMPLATES_DIR)
        if not d.exists():
            return []
        return sorted(d.glob("*.md"))

    def build_manifest(self) -> List[WorkflowTemplateItem]:
        self._manifest = []
        for i, p in enumerate(self.collect_examples(), 1):
            self._manifest.append(self._build_item(p, "EXAMPLE", i))
        for i, p in enumerate(self.collect_templates(), 1):
            self._manifest.append(self._build_item(p, "TEMPLATE", i))
        return self._manifest

    def categorize(self) -> Dict[str, List[str]]:
        if not self._manifest:
            self.build_manifest()
        result: Dict[str, List[str]] = {}
        for item in self._manifest:
            result.setdefault(item.category, []).append(item.title)
        return result

    def detect_missing_required_templates(self) -> List[str]:
        missing = []
        for fname in REQUIRED_EXAMPLES:
            if not self._p(EXAMPLES_DIR + "/" + fname).exists():
                missing.append(fname)
        for fname in REQUIRED_TEMPLATES:
            if not self._p(TEMPLATES_DIR + "/" + fname).exists():
                missing.append(fname)
        return missing

    def detect_unsafe_templates(self) -> List[str]:
        """Return templates missing safety phrases."""
        unsafe = []
        for item in self._manifest:
            if not item.safety_covered:
                unsafe.append(item.path)
        return unsafe

    def save_manifest(self, output_dir: Optional[str] = None) -> str:
        if not self._manifest:
            self.build_manifest()
        out = output_dir or os.path.join(self.base_dir, OUTPUT_DIR)
        os.makedirs(out, exist_ok=True)
        today = datetime.date.today().isoformat()
        path = os.path.join(out, f"workflow_template_manifest_{today}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(WorkflowTemplateItem().to_dict().keys()))
            writer.writeheader()
            for item in self._manifest:
                writer.writerow(item.to_dict())
        return path
