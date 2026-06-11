"""
Workflow Template Summary Builder — v1.0.6 Example Workflows & Templates.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Dict
from workflows.workflow_template_indexer import EXAMPLES_DIR, TEMPLATES_DIR, REQUIRED_EXAMPLES, REQUIRED_TEMPLATES


class WorkflowTemplateSummaryBuilder:
    """
    Summarizes workflow templates status for console display.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir

    def list_examples(self) -> List[str]:
        d = Path(self.base_dir) / EXAMPLES_DIR
        if not d.exists():
            return []
        return [p.name for p in sorted(d.glob("*.md"))]

    def list_templates(self) -> List[str]:
        d = Path(self.base_dir) / TEMPLATES_DIR
        if not d.exists():
            return []
        return [p.name for p in sorted(d.glob("*.md"))]

    def build_summary(self) -> dict:
        examples = self.list_examples()
        templates = self.list_templates()
        missing_ex = [f for f in REQUIRED_EXAMPLES if f not in examples]
        missing_tmpl = [f for f in REQUIRED_TEMPLATES if f not in templates]
        return {
            "examples_count": len(examples),
            "templates_count": len(templates),
            "missing_examples": missing_ex,
            "missing_templates": missing_tmpl,
            "research_only": True,
            "no_real_orders": True,
        }

    def summarize_for_console(self) -> str:
        s = self.build_summary()
        lines = [
            "=" * 60,
            "TW Quant Cockpit — Workflow Templates Summary",
            "Research Only | No Real Orders | Production Trading BLOCKED",
            "=" * 60,
            f"  Examples:  {s['examples_count']} found",
            f"  Templates: {s['templates_count']} found",
        ]
        if s["missing_examples"]:
            lines.append(f"  Missing examples:  {s['missing_examples']}")
        if s["missing_templates"]:
            lines.append(f"  Missing templates: {s['missing_templates']}")
        lines.append("=" * 60)
        return "\n".join(lines)
