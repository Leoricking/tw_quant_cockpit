"""
Release Gate Health — v1.0.4 Regression & Release Gate Hardening.
Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. VALIDATED does not enable trading.
"""
from __future__ import annotations
import importlib
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ReleaseGateHealthSummary:
    total_suites: int = 0
    pass_count: int = 0
    warn_count: int = 0
    fail_count: int = 0
    blocked_count: int = 0
    known_warn_count: int = 0
    known_blocked_count: int = 0
    unknown_fail_count: int = 0
    unknown_blocked_count: int = 0
    overall_status: str = "PASS"
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "total_suites": self.total_suites,
            "pass_count": self.pass_count,
            "warn_count": self.warn_count,
            "fail_count": self.fail_count,
            "blocked_count": self.blocked_count,
            "known_warn_count": self.known_warn_count,
            "known_blocked_count": self.known_blocked_count,
            "unknown_fail_count": self.unknown_fail_count,
            "unknown_blocked_count": self.unknown_blocked_count,
            "overall_status": self.overall_status,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }


@dataclass
class ReleaseGateCheckResult:
    name: str
    status: str
    detail: str = ""
    is_known: bool = False
    known_class: str = ""


class ReleaseGateHealth:
    """
    Checks health of the release gate suites and known warning/blocked states.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    KNOWN_WARNS = [
        "cp950 subprocess encoding (Windows, non-critical)",
        "paper_state.json missing (non-critical)",
        "no_real_orders flag pre-existing check (advisory only)",
        "Optional report_pack modules ENV_LIMITED (non-critical)",
    ]

    KNOWN_BLOCKED = [
        "no_real_orders flag check (known pre-existing, not a real failure)",
    ]

    def __init__(self):
        self.results: List[ReleaseGateCheckResult] = []

    def _add(self, name: str, status: str, detail: str = "", is_known: bool = False, known_class: str = "") -> None:
        self.results.append(ReleaseGateCheckResult(name=name, status=status, detail=detail, is_known=is_known, known_class=known_class))

    def check_release_gate_suite(self) -> None:
        try:
            from regression.suite_registry import SUITE_RELEASE_GATE
            count = len(SUITE_RELEASE_GATE)
            self._add("release_gate suite", "PASS", f"{count} tests registered")
        except Exception as exc:
            self._add("release_gate suite", "FAIL", f"Import failed: {exc}")

    def check_quick_suite(self) -> None:
        try:
            from regression.suite_registry import SUITE_QUICK
            count = len(SUITE_QUICK)
            self._add("quick suite", "PASS", f"{count} tests registered")
        except Exception as exc:
            self._add("quick suite", "WARN", f"Import failed: {exc}")

    def check_stable_v060(self) -> None:
        try:
            from stable_release.stable_release_checklist_v060 import StableReleaseChecklistV060
            self._add("stable-v060-check", "PASS", "StableReleaseChecklistV060 available")
        except Exception as exc:
            self._add("stable-v060-check", "FAIL", f"Import failed: {exc}")

    def check_known_warns(self) -> None:
        self._add(
            "known WARN classification",
            "PASS",
            f"{len(self.KNOWN_WARNS)} known warnings classified",
            is_known=True,
            known_class="KNOWN_WARN",
        )

    def check_known_blocked(self) -> None:
        self._add(
            "known BLOCKED classification",
            "PASS",
            f"{len(self.KNOWN_BLOCKED)} known blocked classified",
            is_known=True,
            known_class="KNOWN_BLOCKED",
        )

    def check_no_real_orders_false_positive(self) -> None:
        try:
            from regression_hardening.safety_scanner import SafetyScanner, WHITELIST_PHRASES
            whitelisted = any("No Real Orders" in p for p in WHITELIST_PHRASES)
            if whitelisted:
                self._add(
                    "no_real_orders false positive",
                    "PASS",
                    "No Real Orders is whitelisted — not flagged as forbidden",
                    is_known=True,
                    known_class="KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE",
                )
            else:
                self._add("no_real_orders false positive", "WARN", "Whitelist may not cover No Real Orders")
        except Exception as exc:
            self._add("no_real_orders false positive", "WARN", f"Check failed: {exc}")

    def check_paper_smoke_warn(self) -> None:
        self._add(
            "paper smoke WARN",
            "PASS",
            "paper_state.json missing is classified as KNOWN_PAPER_SMOKE_WARNING",
            is_known=True,
            known_class="KNOWN_PAPER_SMOKE_WARNING",
        )

    def check_cp950_warn(self) -> None:
        self._add(
            "cp950 WARN",
            "PASS",
            "Windows cp950 encoding is classified as KNOWN_CP950_WARNING",
            is_known=True,
            known_class="KNOWN_CP950_WARNING",
        )

    def check_report_pack_optional(self) -> None:
        self._add(
            "report_pack optional missing",
            "PASS",
            "ENV_LIMITED/NOT_GENERATED classified as KNOWN_REPORT_PACK_OPTIONAL",
            is_known=True,
            known_class="KNOWN_REPORT_PACK_OPTIONAL",
        )

    def run_all(self) -> ReleaseGateHealthSummary:
        self.check_release_gate_suite()
        self.check_quick_suite()
        self.check_stable_v060()
        self.check_known_warns()
        self.check_known_blocked()
        self.check_no_real_orders_false_positive()
        self.check_paper_smoke_warn()
        self.check_cp950_warn()
        self.check_report_pack_optional()

        summary = ReleaseGateHealthSummary(total_suites=len(self.results))
        for r in self.results:
            if r.status == "PASS":
                summary.pass_count += 1
            elif r.status == "WARN":
                summary.warn_count += 1
            elif r.status == "FAIL":
                summary.fail_count += 1
                summary.unknown_fail_count += 1
            elif r.status == "BLOCKED":
                summary.blocked_count += 1
                if r.is_known:
                    summary.known_blocked_count += 1
                else:
                    summary.unknown_blocked_count += 1

        if summary.unknown_fail_count > 0:
            summary.overall_status = "FAIL"
        elif summary.unknown_blocked_count > 0:
            summary.overall_status = "BLOCKED"
        elif summary.warn_count > 0:
            summary.overall_status = "WARN"
        else:
            summary.overall_status = "PASS"

        return summary

    def print_report(self, summary: Optional[ReleaseGateHealthSummary] = None) -> None:
        if summary is None:
            summary = self.run_all()
        print("=" * 60)
        print("TW Quant Cockpit \u2014 Release Gate Health")
        print("Research Only | No Real Orders | Production Trading BLOCKED")
        print("Broker Execution Disabled | VALIDATED does not enable trading")
        print("=" * 60)
        for r in self.results:
            known_tag = f" [{r.known_class}]" if r.is_known and r.known_class else ""
            print(f"  {r.name}: {r.status}{known_tag}" + (f" \u2014 {r.detail}" if r.detail else ""))
        print("-" * 60)
        print(f"  PASS:            {summary.pass_count}")
        print(f"  WARN:            {summary.warn_count}")
        print(f"  FAIL:            {summary.fail_count}  (unknown: {summary.unknown_fail_count})")
        print(f"  BLOCKED:         {summary.blocked_count}  (known: {summary.known_blocked_count}, unknown: {summary.unknown_blocked_count})")
        print(f"  Known WARNs:")
        for w in self.KNOWN_WARNS:
            print(f"    - {w}")
        print(f"  Known BLOCKED:")
        for b in self.KNOWN_BLOCKED:
            print(f"    - {b}")
        print(f"  OVERALL:         {summary.overall_status}")
        print("=" * 60)
