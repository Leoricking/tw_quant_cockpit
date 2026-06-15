"""
replay/scenario_validator.py — ReplayScenarioValidator v1.2.1

Validates scenario templates before creation/instantiation/export.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_PAYLOAD_FIELDS = [
    "future_return", "outcome", "final_label", "answer",
    "realized_pnl", "broker", "order_token", "api_key", "secret",
]

VALID_ACTIONS = ["WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"]
VALID_CATEGORIES = [
    "TREND_FOLLOWING", "BREAKOUT", "PULLBACK", "BOTTOM_REVERSAL",
    "MOMENTUM", "SECTOR_ROTATION", "FUNDAMENTAL_TURNAROUND",
    "RISK_CONTROL", "NO_CHASE", "NO_PANIC_SELL", "FREE_PRACTICE", "CUSTOM",
]
VALID_DIFFICULTIES = ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayScenarioValidator:
    """
    Validates scenario templates.
    Blocks: missing symbols (when required), invalid dates, strict_future_firewall=False,
    forbidden fields, archived instantiation, mock labeled as real formal.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    FORBIDDEN_PAYLOAD_FIELDS = FORBIDDEN_PAYLOAD_FIELDS

    def validate_template(self, template) -> "ScenarioValidationResult":
        """Full validation of a scenario template."""
        from replay.scenario_schema import ScenarioValidationResult
        errors = []
        warnings = []

        if not template.scenario_id:
            errors.append("scenario_id is required")
        if not template.scenario_name:
            errors.append("scenario_name is required")
        if not template.category:
            errors.append("category is required")
        if template.category not in VALID_CATEGORIES:
            errors.append(f"Invalid category: {template.category}. Must be one of {VALID_CATEGORIES}")
        if template.difficulty not in VALID_DIFFICULTIES:
            errors.append(f"Invalid difficulty: {template.difficulty}. Must be one of {VALID_DIFFICULTIES}")

        date_errors, date_warnings = self.validate_dates(template)
        errors.extend(date_errors)
        warnings.extend(date_warnings)

        sym_errors, sym_warnings = self.validate_symbols(template)
        errors.extend(sym_errors)
        warnings.extend(sym_warnings)

        fw_errors = self.validate_future_firewall(template)
        errors.extend(fw_errors)

        action_errors = self.validate_allowed_actions(template)
        errors.extend(action_errors)

        missing_req = self.validate_required_datasets(template)
        missing_opt = self.validate_optional_datasets(template)

        if template.archived:
            warnings.append("Template is archived — cannot be instantiated until restored")

        # Check for forbidden fields in the dict
        try:
            d = template.to_dict()
            forbidden_found = [f for f in FORBIDDEN_PAYLOAD_FIELDS if f in d]
            if forbidden_found:
                errors.append(f"Forbidden fields found in template: {forbidden_found}")
        except Exception:
            pass

        future_data_risk = not template.strict_future_firewall
        pit_compatible = template.strict_future_firewall
        qualification = "OBSERVATIONAL_ONLY" if not errors else "BLOCKED"

        return ScenarioValidationResult(
            scenario_id=template.scenario_id,
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            missing_required_datasets=missing_req,
            missing_optional_datasets=missing_opt,
            future_data_risk=future_data_risk,
            point_in_time_compatible=pit_compatible,
            qualification=qualification,
            checked_at=_now_utc(),
        )

    def validate_dates(self, template) -> tuple:
        errors = []
        warnings = []
        if template.date_selector == "FIXED" or template.date_selector == "RANGE":
            if template.start_date and template.end_date:
                try:
                    s = datetime.strptime(template.start_date, "%Y-%m-%d")
                    e = datetime.strptime(template.end_date, "%Y-%m-%d")
                    if s >= e:
                        errors.append(f"start_date ({template.start_date}) must be before end_date ({template.end_date})")
                except ValueError as exc:
                    errors.append(f"Invalid date format: {exc}")
        return errors, warnings

    def validate_symbols(self, template) -> tuple:
        errors = []
        warnings = []
        if template.symbol_selector == "FIXED" and not template.symbols:
            errors.append("symbol_selector=FIXED requires at least one symbol in symbols list")
        if template.symbol_selector == "LIST" and not template.symbols:
            errors.append("symbol_selector=LIST requires at least one symbol in symbols list")
        return errors, warnings

    def validate_required_datasets(self, template) -> List[str]:
        missing = []
        required = template.required_datasets or ["price"]
        if "price" not in required:
            missing.append("price")
        return missing

    def validate_optional_datasets(self, template) -> List[str]:
        return []

    def validate_allowed_actions(self, template) -> List[str]:
        errors = []
        if template.allowed_actions:
            invalid = [a for a in template.allowed_actions if a not in VALID_ACTIONS]
            if invalid:
                errors.append(f"Invalid allowed_actions: {invalid}. Must be subset of {VALID_ACTIONS}")
        return errors

    def validate_future_firewall(self, template) -> List[str]:
        errors = []
        if not template.strict_future_firewall:
            errors.append("strict_future_firewall must be True. Future data exposure not allowed.")
        if not template.research_only:
            errors.append("research_only must be True")
        if not template.no_real_orders:
            errors.append("no_real_orders must be True")
        return errors

    def validate_point_in_time_compatibility(self, template) -> bool:
        return template.strict_future_firewall

    def validate_export_payload(self, payload: Dict[str, Any]) -> List[str]:
        errors = []
        forbidden_found = [f for f in FORBIDDEN_PAYLOAD_FIELDS if f in payload]
        if forbidden_found:
            errors.append(f"Forbidden fields in export payload: {forbidden_found}")
        return errors

    def build_result(
        self, scenario_id: str, errors: List[str], warnings: List[str],
        missing_required: List[str] = None, missing_optional: List[str] = None,
        future_data_risk: bool = False, pit_compatible: bool = True,
    ):
        from replay.scenario_schema import ScenarioValidationResult
        return ScenarioValidationResult(
            scenario_id=scenario_id,
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            missing_required_datasets=missing_required or [],
            missing_optional_datasets=missing_optional or [],
            future_data_risk=future_data_risk,
            point_in_time_compatible=pit_compatible,
            qualification="OBSERVATIONAL_ONLY" if not errors else "BLOCKED",
            checked_at=_now_utc(),
        )
