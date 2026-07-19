"""scripts/check_handlers.py - Check that all v1.9.7 handlers resolve."""
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
import importlib
main = importlib.import_module("main")
from cli.command_registry import PROVIDER_COMMANDS

sgd = [s for s in PROVIDER_COMMANDS if getattr(s, "group", None) == "strategy_governance_dashboard"]
unresolved = [s.handler_name for s in sgd if not callable(getattr(main, s.handler_name, None))]

if unresolved:
    print(f"FAIL: {len(unresolved)} unresolved: {unresolved}")
    sys.exit(1)
else:
    print(f"OK: all {len(sgd)} strategy_governance_dashboard handlers resolve")
