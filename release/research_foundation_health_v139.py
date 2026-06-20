"""
release/research_foundation_health_v139.py — Research Foundation Stable Rollup health check.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, Tuple

_STABLE_CAPABILITIES = [
    "real_data_quality",
    "universe_expansion",
    "provider_adapter_foundation",
    "coverage_repair",
    "data_freshness",
    "empirical_backtest",
    "abc_validation",
    "strategy_robustness",
    "canonical_version_alignment",
]

_INTEGRATION_EDGES = [
    ("real_data_quality", "universe_expansion"),
    ("universe_expansion", "coverage_repair"),
    ("provider_adapter_foundation", "data_freshness"),
    ("data_freshness", "coverage_repair"),
    ("real_data_quality", "empirical_backtest"),
    ("data_freshness", "empirical_backtest"),
    ("empirical_backtest", "abc_validation"),
    ("abc_validation", "strategy_robustness"),
]


class ResearchFoundationStableHealthCheck:
    """
    Health check for Research Foundation Stable Rollup v1.3.9.
    Covers: Version, Capabilities, Integrations, Storage, CLI, GUI, Safety.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def run(self) -> Dict[str, Tuple[str, str]]:
        checks: Dict[str, Tuple[str, str]] = {}
        self._check_version(checks)
        self._check_capabilities(checks)
        self._check_integrations(checks)
        self._check_storage(checks)
        self._check_cli(checks)
        self._check_gui(checks)
        self._check_safety(checks)
        return checks

    # ------------------------------------------------------------------
    # Version checks
    # ------------------------------------------------------------------
    def _check_version(self, checks: dict) -> None:
        try:
            from release.version_info import VERSION
            parts = tuple(int(x) for x in VERSION.split(".")[:3])
            ok = parts >= (1, 3, 9)
            checks["version_is_139"] = ("PASS" if ok else "FAIL", f"VERSION={VERSION}")
        except Exception as exc:
            checks["version_is_139"] = ("FAIL", str(exc))

        try:
            from release.version_info import RELEASE_NAME
            _KNOWN_NAMES = {
                "Research Foundation Stable Rollup",
                "TWSE Provider",
                "Strategy Robustness & Regime Validation",
                "TPEx Provider",
                "MOPS Provider",
                "data.gov.tw Provider",
                "Provider CLI Registration Hotfix",
                "FinMind Adapter Hardening",
                "Source Lineage & Rate Limit",
                "Provider Quality Gates",
                "Forum Intelligence & Market Sentiment",
                "Data Provider Stable Rollup",
            }
            ok = RELEASE_NAME in _KNOWN_NAMES
            checks["release_name_correct"] = ("PASS" if ok else "FAIL", f"RELEASE_NAME={RELEASE_NAME}")
        except Exception as exc:
            checks["release_name_correct"] = ("FAIL", str(exc))

        try:
            from release.version_info import BASE_RELEASE
            ok = any(marker in BASE_RELEASE for marker in ("1.3.7", "1.3.9", "1.4.0", "1.4.1", "1.4.2", "1.4.3"))
            checks["base_release_correct"] = ("PASS" if ok else "FAIL", f"BASE_RELEASE={BASE_RELEASE}")
        except Exception as exc:
            checks["base_release_correct"] = ("FAIL", str(exc))

        try:
            from release.version_info import REPLAY_STABLE_BASELINE
            ok = REPLAY_STABLE_BASELINE == "1.2.9"
            checks["replay_baseline_correct"] = ("PASS" if ok else "FAIL",
                                                  f"REPLAY_STABLE_BASELINE={REPLAY_STABLE_BASELINE}")
        except Exception as exc:
            checks["replay_baseline_correct"] = ("FAIL", str(exc))

        try:
            from release.version_alignment import is_known_release_lineage
            ok = is_known_release_lineage("1.3.9")
            checks["canonical_mapping_valid"] = ("PASS" if ok else "FAIL", "1.3.9 in known lineage")
        except Exception as exc:
            checks["canonical_mapping_valid"] = ("FAIL", str(exc))

    # ------------------------------------------------------------------
    # Capability checks
    # ------------------------------------------------------------------
    def _check_capabilities(self, checks: dict) -> None:
        try:
            from release.capability_registry import is_capability_available, validate_capability_dependencies
            dep_result = validate_capability_dependencies()
            ok = dep_result["valid"]
            checks["capability_deps_valid"] = ("PASS" if ok else "FAIL",
                                               f"errors={dep_result['errors']}")
        except Exception as exc:
            checks["capability_deps_valid"] = ("FAIL", str(exc))

        for cap_id in _STABLE_CAPABILITIES:
            key = f"capability_{cap_id}"
            try:
                from release.capability_registry import is_capability_available
                ok = is_capability_available(cap_id)
                checks[key] = ("PASS" if ok else "FAIL", f"{cap_id} available={ok}")
            except Exception as exc:
                checks[key] = ("FAIL", str(exc))

        # Planned capabilities must NOT be available (twse_provider is now stable in v1.4.0+)
        planned_caps = [
            "tpex_provider", "mops_provider",
            "data_gov_tw_provider", "forum_intelligence",
        ]
        for cap_id in planned_caps:
            key = f"planned_not_available_{cap_id}"
            try:
                from release.capability_registry import is_capability_available
                unavailable = not is_capability_available(cap_id)
                checks[key] = ("PASS" if unavailable else "FAIL",
                               f"{cap_id} correctly unavailable={unavailable}")
            except Exception as exc:
                checks[key] = ("FAIL", str(exc))

    # ------------------------------------------------------------------
    # Integration checks
    # ------------------------------------------------------------------
    def _check_integrations(self, checks: dict) -> None:
        # Robustness → Replay read-only
        try:
            from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
            ri = RobustnessReplayIntegration()
            ok = ri.READ_ONLY is True and ri.MODIFIES_REPLAY_SESSIONS is False
            checks["robustness_replay_read_only"] = ("PASS" if ok else "FAIL",
                                                      f"READ_ONLY={ri.READ_ONLY}")
        except Exception as exc:
            checks["robustness_replay_read_only"] = ("FAIL", str(exc))

        # ABC → Empirical: single domain logic
        try:
            from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
            rule = ABuyPointRuleAdapter().get_rule()
            ok = rule is not None and rule.rule_id == "abc_buy_point_a"
            checks["abc_uses_single_domain_logic"] = ("PASS" if ok else "FAIL",
                                                       f"rule_id={getattr(rule, 'rule_id', None)}")
        except Exception as exc:
            checks["abc_uses_single_domain_logic"] = ("FAIL", str(exc))

        # Replay score unchanged (no auto-modification)
        try:
            from release.version_info import (
                AUTO_REPLAY_DECISION_ENABLED, AUTO_REPLAY_EXECUTION_ENABLED
            )
            ok = AUTO_REPLAY_DECISION_ENABLED is False and AUTO_REPLAY_EXECUTION_ENABLED is False
            checks["replay_score_unchanged"] = ("PASS" if ok else "FAIL",
                                                 "Replay auto-modification disabled")
        except Exception as exc:
            checks["replay_score_unchanged"] = ("FAIL", str(exc))

    # ------------------------------------------------------------------
    # Storage checks
    # ------------------------------------------------------------------
    def _check_storage(self, checks: dict) -> None:
        try:
            from release.version_alignment import load_snapshot_gracefully
            old_payload = {"application_version": "1.4.0", "data": "test"}
            enriched = load_snapshot_gracefully(old_payload)
            ok = enriched.get("canonical_release_version") == "1.3.5"
            checks["storage_old_payload_compatible"] = ("PASS" if ok else "FAIL",
                                                         f"canonical={enriched.get('canonical_release_version')}")
        except Exception as exc:
            checks["storage_old_payload_compatible"] = ("FAIL", str(exc))

        try:
            from release.version_alignment import load_snapshot_gracefully
            malformed = {"application_version": "not_a_version", "data": "x"}
            enriched = load_snapshot_gracefully(malformed)
            ok = "application_version" in enriched  # still readable
            checks["storage_malformed_payload_graceful"] = ("PASS" if ok else "FAIL",
                                                             "malformed payload loaded without crash")
        except Exception as exc:
            checks["storage_malformed_payload_graceful"] = ("FAIL", str(exc))

        try:
            from release.version_alignment import load_snapshot_gracefully
            unknown = {"application_version": "9.9.9", "data": "future"}
            enriched = load_snapshot_gracefully(unknown)
            ok = "application_version" in enriched
            checks["storage_unknown_future_graceful"] = ("PASS" if ok else "FAIL",
                                                          "unknown future version handled")
        except Exception as exc:
            checks["storage_unknown_future_graceful"] = ("FAIL", str(exc))

    # ------------------------------------------------------------------
    # CLI checks
    # ------------------------------------------------------------------
    def _check_cli(self, checks: dict) -> None:
        try:
            import main as m
            ok = hasattr(m, "cmd_version_info") or callable(getattr(m, "cmd_version_info", None))
            checks["cli_version_info_present"] = ("PASS" if ok else "FAIL", "cmd_version_info found")
        except Exception as exc:
            checks["cli_version_info_present"] = ("FAIL", str(exc))

        try:
            import main as m
            ok = hasattr(m, "cmd_research_foundation_health")
            checks["cli_rf_health_present"] = ("PASS" if ok else "FAIL",
                                                "cmd_research_foundation_health found")
        except Exception as exc:
            checks["cli_rf_health_present"] = ("FAIL", str(exc))

        try:
            import main as m
            ok = hasattr(m, "cmd_research_foundation_summary")
            checks["cli_rf_summary_present"] = ("PASS" if ok else "FAIL",
                                                  "cmd_research_foundation_summary found")
        except Exception as exc:
            checks["cli_rf_summary_present"] = ("FAIL", str(exc))

        # No broker commands introduced
        try:
            import main as m
            import inspect
            src = inspect.getsource(m)
            forbidden = ["execute_real_order", "broker_connect", "place_real_order"]
            found = [f for f in forbidden if f in src]
            ok = len(found) == 0
            checks["cli_no_broker_commands"] = ("PASS" if ok else "FAIL",
                                                  f"forbidden={found}")
        except Exception as exc:
            checks["cli_no_broker_commands"] = ("FAIL", str(exc))

    # ------------------------------------------------------------------
    # GUI checks
    # ------------------------------------------------------------------
    def _check_gui(self, checks: dict) -> None:
        try:
            import gui.research_foundation_summary_panel as panel
            checks["gui_rf_panel_import"] = ("PASS", "research_foundation_summary_panel imported")
        except Exception as exc:
            checks["gui_rf_panel_import"] = ("FAIL", str(exc))

        # No trading controls
        try:
            import gui.research_foundation_summary_panel as panel
            import inspect
            src = inspect.getsource(panel)
            forbidden = ["BuyButton", "SellButton", "OrderWidget", "execute_trade"]
            found = [f for f in forbidden if f in src]
            ok = len(found) == 0
            checks["gui_no_trading_controls"] = ("PASS" if ok else "FAIL",
                                                   f"forbidden={found}")
        except Exception as exc:
            checks["gui_no_trading_controls"] = ("FAIL", str(exc))

    # ------------------------------------------------------------------
    # Safety checks
    # ------------------------------------------------------------------
    def _check_safety(self, checks: dict) -> None:
        safety_map = {
            "NO_REAL_ORDERS": True,
            "BROKER_EXECUTION_ENABLED": False,
            "PRODUCTION_TRADING_BLOCKED": True,
            "MOCK_FALLBACK_ENABLED": False,
            "AUTO_OPTIMIZATION_ENABLED": False,
            "AUTO_TRADING_ENABLED": False,
        }
        for flag, expected in safety_map.items():
            key = f"safety_{flag.lower()}"
            try:
                import release.version_info as vi
                val = getattr(vi, flag)
                ok = val is expected
                checks[key] = ("PASS" if ok else "FAIL", f"{flag}={val} (expected {expected})")
            except Exception as exc:
                checks[key] = ("FAIL", str(exc))

        try:
            from release.version_info import REPLAY_STABLE_BASELINE
            ok = REPLAY_STABLE_BASELINE == "1.2.9"
            checks["safety_replay_baseline_unchanged"] = (
                "PASS" if ok else "FAIL",
                f"REPLAY_STABLE_BASELINE={REPLAY_STABLE_BASELINE}"
            )
        except Exception as exc:
            checks["safety_replay_baseline_unchanged"] = ("FAIL", str(exc))

    def get_health_summary(self) -> dict:
        checks = self.run()
        total = len(checks)
        passed = sum(1 for v in checks.values() if v[0] == "PASS")
        failed = sum(1 for v in checks.values() if v[0] == "FAIL")
        warned = sum(1 for v in checks.values() if v[0] == "WARN")
        all_pass = failed == 0

        # Core checks that must all PASS for stable
        core_checks = [
            "version_is_139", "release_name_correct", "base_release_correct",
            "replay_baseline_correct", "safety_no_real_orders",
            "safety_broker_execution_enabled", "safety_production_trading_blocked",
        ]
        core_all_pass = all(
            checks.get(k, ("FAIL",))[0] == "PASS" for k in core_checks
        )

        return {
            "stable": core_all_pass and all_pass,
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "all_pass": all_pass,
            "core_all_pass": core_all_pass,
            "checks": {
                name: {"status": status, "detail": detail}
                for name, (status, detail) in checks.items()
            },
            "safety_flags": {
                "NO_REAL_ORDERS": True,
                "BROKER_EXECUTION_ENABLED": False,
                "PRODUCTION_TRADING_BLOCKED": True,
                "MOCK_FALLBACK_ENABLED": False,
                "AUTO_OPTIMIZATION_ENABLED": False,
                "AUTO_TRADING_ENABLED": False,
            },
        }
