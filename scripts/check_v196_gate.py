"""scripts/check_v196_gate.py - Check strategy_registry_release_gate_v196."""
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
from release.strategy_registry_release_gate_v196 import run_release_gate

result = run_release_gate()
failed = [c for c in result["checks"] if not c["passed"]]
if failed:
    print(f"FAIL: {len(failed)} failed checks:")
    for c in failed:
        print(f"  [{c['name']}]: {c.get('error')}")
    sys.exit(1)
else:
    print(f"OK: {result['passed_count']}/{result['total']} passed, gate_passed={result['gate_passed']}")
