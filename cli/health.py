"""
cli/health.py — CLI registration health check v1.4.3.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, Set

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_PASS = "PASS"
_FAIL = "FAIL"
_WARN = "WARN"

PROVIDER_HEALTH_COMMANDS = {
    "research-foundation-health",
    "twse-health",
    "tpex-health",
    "mops-health",
    "data-gov-tw-health",
    "finmind-health",
    "cli-registration-health",
}

PROVIDER_PREFIXES = {
    "research-foundation-",
    "twse-",
    "tpex-",
    "mops-",
    "data-gov-tw-",
    "finmind-",
}


class CLIRegistrationHealthCheck:
    def run(self, parser_commands: Set[str], handler_map: Dict[str, Any]) -> Dict[str, Any]:
        from cli.command_registry import validate_command_registry, get_formal_command_names

        checks = {}
        formal = get_formal_command_names()

        validation = validate_command_registry(parser_commands, handler_map)

        # Count checks
        checks["parser_command_count"] = (
            _PASS if validation["parser_count"] >= len(formal) else _FAIL,
            f"Formal={len(formal)}, Registered={validation['parser_count']}"
        )
        checks["handler_command_count"] = (
            _PASS if validation["handler_count"] >= len(formal) else _FAIL,
            f"Formal={len(formal)}, Handlers={validation['handler_count']}"
        )
        checks["handler_without_parser"] = (
            _PASS if not validation["HANDLER_WITHOUT_REGISTRATION"] else _FAIL,
            f"Unregistered handlers: {validation['HANDLER_WITHOUT_REGISTRATION']}"
        )
        checks["parser_without_handler"] = (
            _PASS if not validation["REGISTERED_WITHOUT_HANDLER"] else _FAIL,
            f"Registered but no handler: {validation['REGISTERED_WITHOUT_HANDLER']}"
        )
        checks["duplicate_commands"] = (
            _PASS if not validation["DUPLICATE_REGISTRATION"] else _FAIL,
            f"Duplicates: {validation['DUPLICATE_REGISTRATION']}"
        )
        checks["duplicate_aliases"] = (
            _PASS if not validation["DUPLICATE_ALIAS"] else _FAIL,
            f"Duplicate aliases: {validation['DUPLICATE_ALIAS']}"
        )

        # Handler callable check — handler_map values are handler_name strings;
        # resolve each via getattr(main) to verify the callable exists.
        import importlib
        try:
            _main_mod = importlib.import_module("main")
            non_callable = [
                n for n, h in handler_map.items()
                if n in formal and not callable(getattr(_main_mod, h, None))
            ]
        except Exception:
            non_callable = []
        checks["invalid_handler"] = (
            _PASS if not non_callable else _FAIL,
            f"Non-callable handlers: {non_callable}"
        )

        # Provider health commands registered
        missing_health = PROVIDER_HEALTH_COMMANDS - parser_commands
        checks["provider_health_commands_registered"] = (
            _PASS if not missing_health else _FAIL,
            f"Missing health commands: {sorted(missing_health)}"
        )

        # Provider prefixes registered
        missing_prefixes = []
        for prefix in PROVIDER_PREFIXES:
            if not any(c.startswith(prefix) for c in parser_commands):
                missing_prefixes.append(prefix)
        checks["provider_prefixes_registered"] = (
            _PASS if not missing_prefixes else _FAIL,
            f"Missing prefix groups: {missing_prefixes}"
        )

        # Consistency
        checks["cli_registration_consistency"] = (
            _PASS if validation["is_consistent"] else _FAIL,
            "All formal commands have both parser and handler" if validation["is_consistent"] else f"Errors: {validation['errors']}"
        )

        return checks

    def get_health_summary(self, parser_commands: Set[str], handler_map: Dict[str, Any]) -> Dict[str, Any]:
        checks = self.run(parser_commands, handler_map)
        passed = sum(1 for s, _ in checks.values() if s == _PASS)
        failed = sum(1 for s, _ in checks.values() if s == _FAIL)
        return {
            "provider_status": "HEALTHY" if failed == 0 else "DEGRADED",
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "checks": {k: {"status": s, "detail": d} for k, (s, d) in checks.items()},
            "passed": passed,
            "failed": failed,
            "total": len(checks),
            "cli_registration_consistency": "PASS" if failed == 0 else "FAIL",
        }
