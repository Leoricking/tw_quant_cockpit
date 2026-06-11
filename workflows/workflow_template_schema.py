"""
Workflow Template Schema — v1.0.6 Example Workflows & Templates.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

CATEGORIES = [
    "DAILY", "WEEKEND", "STOCK_RESEARCH", "STRATEGY_VALIDATION",
    "CRASH_REVERSAL", "DATA_HYGIENE", "GUI", "CLAUDE_CODE",
    "TROUBLESHOOTING", "PAPER_MOCK", "RELEASE", "HANDOFF",
]


@dataclass
class WorkflowTemplateItem:
    template_id: str = ""
    path: str = ""
    title: str = ""
    category: str = ""
    description: str = ""
    safety_covered: bool = False
    no_real_orders: bool = True
    broker_disabled: bool = True
    has_allowed_actions: bool = False
    has_forbidden_actions: bool = False
    has_cli_examples: bool = False
    has_gui_steps: bool = False
    status: str = "PASS"
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "template_id": self.template_id,
            "path": self.path,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "safety_covered": self.safety_covered,
            "no_real_orders": self.no_real_orders,
            "broker_disabled": self.broker_disabled,
            "has_allowed_actions": self.has_allowed_actions,
            "has_forbidden_actions": self.has_forbidden_actions,
            "has_cli_examples": self.has_cli_examples,
            "has_gui_steps": self.has_gui_steps,
            "status": self.status,
            "reason": self.reason,
        }
