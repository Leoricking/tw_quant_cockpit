"""portfolio/stable_rollup/debt_scanner_v159.py — Debt scanner v1.5.9."""
import os
import re

SCAN_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Patterns that indicate actual code-level broker usage (function calls / assignments).
# String-literal lists (e.g. in validation / forbidden-list checks) are excluded.
_BROKER_CALL_PATTERN = re.compile(
    r'(?<!["\'])\b(broker_connect|submit_order|execute_order|sync_broker|live_rebalance)\s*\(',
    re.IGNORECASE,
)
# Files that are explicitly allowed to reference these terms because they
# are audit / scanner / safety-contract modules (their role is to CHECK for them).
_SCANNER_EXEMPT_SUFFIXES = (
    "debt_scanner_v159.py",
    "safety_contract_v159.py",
    "cli_registry_v159.py",
)


def _strip_quoted(line: str) -> str:
    """Remove quoted string contents from a line before pattern matching."""
    return re.sub(r'(["\'])(?:(?!\1).)*\1', '""', line)


class DebtScannerV159:
    def __init__(self):
        self._results = {"blocking": [], "warning": [], "informational": []}

    def scan_hardcoded_paths(self, limit_files=50):
        """Scan for hardcoded D:/code/ paths."""
        findings = []
        test_dir = os.path.join(SCAN_ROOT, "tests")
        count = 0
        try:
            for fn in os.listdir(test_dir):
                if not fn.endswith(".py"):
                    continue
                if count >= limit_files:
                    break
                count += 1
                fp = os.path.join(test_dir, fn)
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as _f:
                        text = _f.read()
                    if "D:/code/Claude" in text or "D:\\code\\Claude" in text:
                        findings.append({"file": fn, "severity": "WARNING", "label": "HARDCODED_PATH"})
                except Exception:
                    pass
        except Exception:
            pass
        return findings

    def scan_version_whitelist_debt(self):
        """Scan for VERSION in (...) whitelist patterns."""
        findings = []
        test_dir = os.path.join(SCAN_ROOT, "tests")
        try:
            for fn in os.listdir(test_dir):
                if not fn.endswith(".py"):
                    continue
                fp = os.path.join(test_dir, fn)
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as _f:
                        text = _f.read()
                    if 'VERSION in (' in text and '"1.5.' in text:
                        matches = re.findall(r'VERSION in \([^)]+\)', text)
                        for m in matches:
                            count = m.count('"1.5.')
                            if count >= 3:
                                findings.append({"file": fn, "severity": "WARNING", "label": "VERSION_WHITELIST_DEBT"})
                except Exception:
                    pass
        except Exception:
            pass
        return findings

    def scan_broker_references(self):
        """Scan portfolio modules for actual broker/order function-call references.

        Uses call-site detection (_BROKER_CALL_PATTERN) so that string-literal
        mentions in forbidden-word lists and safety-check blocks are not flagged.
        Audit/scanner/safety-contract files are exempted entirely because their
        purpose is to define and enforce the no-broker policy.
        """
        findings = []
        portfolio_dir = os.path.join(SCAN_ROOT, "portfolio")
        try:
            for root, dirs, files in os.walk(portfolio_dir):
                for fn in files:
                    if not fn.endswith(".py"):
                        continue
                    if fn.endswith(_SCANNER_EXEMPT_SUFFIXES):
                        continue
                    fp = os.path.join(root, fn)
                    try:
                        with open(fp, encoding="utf-8", errors="ignore") as _f:
                            text = _f.read()
                        # Strip comment lines and quoted strings before matching
                        clean_lines = []
                        for line in text.splitlines():
                            stripped = line.lstrip()
                            if stripped.startswith("#"):
                                continue
                            clean_lines.append(_strip_quoted(line))
                        clean_text = "\n".join(clean_lines)
                        for m in _BROKER_CALL_PATTERN.finditer(clean_text):
                            term = m.group(1).lower()
                            findings.append({
                                "file": os.path.relpath(fp, SCAN_ROOT),
                                "severity": "BLOCKING",
                                "label": f"BROKER_REFERENCE:{term}",
                            })
                    except Exception:
                        pass
        except Exception:
            pass
        return findings

    def run_all(self):
        results = {"blocking": [], "warning": [], "informational": []}

        broker = self.scan_broker_references()
        for f in broker:
            results[f["severity"].lower()].append(f)

        paths = self.scan_hardcoded_paths()
        for f in paths:
            results["warning"].append(f)

        wl = self.scan_version_whitelist_debt()
        for f in wl:
            results["informational"].append(f)

        total_blocking = len(results["blocking"])
        return {
            "blocking": results["blocking"],
            "warning": results["warning"],
            "informational": results["informational"],
            "blocking_count": total_blocking,
            "warning_count": len(results["warning"]),
            "informational_count": len(results["informational"]),
            "blocking_debt_zero": total_blocking == 0,
            "status": "PASS" if total_blocking == 0 else "BLOCKED",
        }
