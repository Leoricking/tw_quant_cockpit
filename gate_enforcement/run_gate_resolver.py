"""
gate_enforcement.run_gate_resolver — RunGateResolver v1.1.5

Resolves GateEnforcementRequest from command-line arguments and policy.
Research Only. No Real Orders.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from gate_enforcement.enforcement_schema import GateEnforcementRequest
from gate_enforcement.enforcement_policy import QualityGateEnforcementPolicy

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


class RunGateResolver:
    """
    Resolves a GateEnforcementRequest from args and policy.

    Rules:
    - mode=mock => requested_level=DEMO
    - --quality-gate formal => FORMAL, observational => OBSERVATIONAL,
      demo => DEMO, auto => policy default, off => OFF with warning
    - unknown gate => request.gate_name=UNKNOWN_GATE (caller should treat as FAILED)
    - override only with explicit flag
    """

    def __init__(self):
        self._policy = QualityGateEnforcementPolicy()

    def resolve_request(self, command_name: str, args, mode: str = "real") -> GateEnforcementRequest:
        """Build a GateEnforcementRequest from command and argparse Namespace."""
        run_id = _new_uuid()
        gate_name = self.resolve_gate_name(command_name)
        requested_level = self.resolve_requested_level(args, mode)
        quality_gate_mode = self.resolve_quality_gate_mode(args)
        symbols = self.resolve_symbols(args)
        override_id = self.resolve_override(args)
        tier = getattr(args, "tier", "") or ""
        allow_research_override = getattr(args, "allow_research_override", False)
        arguments = {k: v for k, v in vars(args).items() if not k.startswith("_")} if hasattr(args, "__dict__") else {}

        if quality_gate_mode == "OFF":
            logger.warning(
                "Quality gate mode is OFF for command '%s'. %s",
                command_name,
                self._policy.off_mode_label(),
            )

        return GateEnforcementRequest(
            run_id=run_id,
            command_name=command_name,
            gate_name=gate_name,
            requested_level=requested_level,
            mode=mode,
            tier=tier,
            requested_symbols=symbols,
            quality_gate_mode=quality_gate_mode,
            allow_observational=self._policy.allow_observational(command_name),
            allow_demo=self._policy.allow_demo(command_name),
            allow_research_override=bool(allow_research_override),
            override_id=override_id,
            arguments=arguments,
            created_at=_now_utc(),
        )

    def resolve_gate_name(self, command_name: str, module_name: str = "") -> str:
        gate = self._policy.resolve_gate(command_name)
        if gate == "UNKNOWN_GATE":
            logger.error("Unknown gate for command '%s'. Run will be FAILED.", command_name)
        return gate

    def resolve_requested_level(self, args, mode: str) -> str:
        """Resolve requested quality level from args and mode."""
        if mode == "mock":
            return "DEMO"
        quality_gate = getattr(args, "quality_gate", None) or getattr(args, "quality-gate", None)
        if quality_gate:
            mapping = {
                "formal":        "FORMAL",
                "observational": "OBSERVATIONAL",
                "demo":          "DEMO",
                "auto":          "AUTO",
                "off":           "OFF",
            }
            level = mapping.get(str(quality_gate).lower())
            if level == "OFF":
                logger.warning("--quality-gate off: Gate enforcement disabled. Results NOT formally qualified.")
            if level:
                return level
        # Default from policy
        command_name = getattr(args, "command", "")
        return self._policy.resolve_default_level(command_name, mode)

    def resolve_quality_gate_mode(self, args) -> str:
        """Resolve ENFORCE / AUDIT_ONLY / OFF / AUTO from args."""
        gate_mode = getattr(args, "gate_mode", None)
        if gate_mode:
            mapping = {
                "enforce":    "ENFORCE",
                "audit-only": "AUDIT_ONLY",
                "audit_only": "AUDIT_ONLY",
                "off":        "OFF",
                "auto":       "AUTO",
            }
            mode = mapping.get(str(gate_mode).lower())
            if mode:
                return mode
        return "ENFORCE"

    def resolve_symbols(self, args, universe=None) -> List[str]:
        """Resolve list of symbols from args."""
        # Try --symbols (comma-separated or list)
        symbols_arg = getattr(args, "symbols", None)
        if symbols_arg:
            if isinstance(symbols_arg, list):
                return [str(s).strip() for s in symbols_arg if s]
            return [s.strip() for s in str(symbols_arg).split(",") if s.strip()]
        # Try --stock (single)
        stock = getattr(args, "stock", None)
        if stock:
            return [str(stock).strip()]
        # Fallback to universe if provided
        if universe:
            return list(universe)
        return []

    def resolve_override(self, args) -> Optional[str]:
        """Resolve override ID only if explicit flag is set."""
        allow = getattr(args, "allow_research_override", False)
        if not allow:
            return None
        override_id = getattr(args, "override_id", None)
        return str(override_id) if override_id else None

    def validate_request(self, request: GateEnforcementRequest) -> bool:
        """Validate that the request is well-formed."""
        if not request.run_id:
            logger.error("Request missing run_id")
            return False
        if not request.command_name:
            logger.error("Request missing command_name")
            return False
        if request.gate_name == "UNKNOWN_GATE":
            logger.error("Request has UNKNOWN_GATE — will be FAILED")
            return False
        return True

    def build_request(
        self,
        run_id: str,
        command_name: str,
        gate_name: str,
        requested_level: str,
        mode: str,
        tier: str,
        requested_symbols: List[str],
        quality_gate_mode: str = "ENFORCE",
        allow_observational: bool = True,
        allow_demo: bool = False,
        allow_research_override: bool = False,
        override_id: Optional[str] = None,
        arguments: Optional[dict] = None,
    ) -> GateEnforcementRequest:
        return GateEnforcementRequest(
            run_id=run_id or _new_uuid(),
            command_name=command_name,
            gate_name=gate_name,
            requested_level=requested_level,
            mode=mode,
            tier=tier,
            requested_symbols=requested_symbols,
            quality_gate_mode=quality_gate_mode,
            allow_observational=allow_observational,
            allow_demo=allow_demo,
            allow_research_override=allow_research_override,
            override_id=override_id,
            arguments=arguments or {},
            created_at=_now_utc(),
        )
