"""portfolio/stable_rollup/cli_registry_v159.py — CLI registry v1.5.9."""
from .models_v159 import StableCLIRecord


def build_cli_registry():
    """Dynamically build from actual command registry."""
    try:
        from cli.command_registry import PROVIDER_COMMANDS
        records = []
        for spec in PROVIDER_COMMANDS:
            cmd = spec.name
            records.append(StableCLIRecord(
                command=cmd,
                handler=getattr(spec, 'handler_name', str(spec)),
                module="main",
                introduced_version=getattr(spec, 'introduced_in', "1.5.x"),
                stable_version="1.5.9",
                category=(
                    "portfolio"
                    if any(k in cmd for k in ["portfolio", "walk", "risk", "sizing", "correlation", "drawdown", "stable"])
                    else "provider"
                ),
                research_only=True,
                broker_related=not cmd.startswith("paper-") and any(b in cmd for b in ["broker", "execute", "submit", "live"]),
                formal_ledger_write=False,
            ))
        return records
    except Exception:
        return []


class CLIRegistryV159:
    def __init__(self):
        self._records = build_cli_registry()

    def get_all(self):
        return list(self._records)

    def get_count(self):
        return len(self._records)

    def validate(self):
        issues = []
        forbidden = [
            "submit-order", "execute-order", "broker-connect", "broker-sync",
            "live-rebalance", "auto-rebalance", "auto-stop", "auto-reduce",
            "live-hedge", "apply-live", "production-trading",
        ]
        cmds = [r.command for r in self._records]
        for f in forbidden:
            if f in cmds:
                issues.append(f"FORBIDDEN_COMMAND:{f}")
        for r in self._records:
            if r.broker_related:
                issues.append(f"BROKER_RELATED_COMMAND:{r.command}")
        return {"valid": len(issues) == 0, "issues": issues, "count": len(self._records)}
