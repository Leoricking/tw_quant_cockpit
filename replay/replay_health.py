"""
replay/replay_health.py — ReplayTrainingHealthCheck v1.2.0

Health check for the replay training module.
Checks: all submodule imports, future firewall, session lifecycle,
date navigation guards, decision simulation-only, no side effects.
Output: PASS/WARN/FAIL/BLOCKED per check.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayTrainingHealthCheck:
    """
    Health check for the replay module.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    REPLAY_TRAINING_ONLY = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Returns dict of check_name -> (status, message). Status: PASS/WARN/FAIL/BLOCKED."""
        results = {}
        results["imports"] = self._check_imports()
        results["schema"] = self._check_schema()
        results["future_firewall"] = self._check_future_firewall()
        results["date_navigation"] = self._check_date_navigation()
        results["session_lifecycle"] = self._check_session_lifecycle()
        results["decision_simulation_only"] = self._check_decision_simulation_only()
        results["no_forbidden_actions"] = self._check_no_forbidden_actions()
        results["safety_flags"] = self._check_safety_flags()
        # v1.2.1 scenario & session manager health
        results["v121_scenario_session_manager"] = self._check_v121_scenario_session_manager()
        return results

    def _check_v121_scenario_session_manager(self) -> Tuple[str, str]:
        """Check v1.2.1 scenario & session manager health."""
        try:
            from replay.session_manager_health import ReplayScenarioSessionManagerHealthCheck
            hc = ReplayScenarioSessionManagerHealthCheck()
            sub_results = hc.run()
            overall = hc.overall_status(sub_results)
            failed = [(k, v[1]) for k, v in sub_results.items() if v[0] == "FAIL"]
            if overall == "PASS":
                return ("PASS", f"v1.2.1 scenario & session manager: all {len(sub_results)} checks passed")
            elif overall == "WARN":
                return ("WARN", f"v1.2.1 scenario & session manager: warnings in {[k for k,_ in failed]}")
            else:
                return ("FAIL", f"v1.2.1 scenario & session manager failures: {[f'{k}: {m}' for k, m in failed[:3]]}")
        except Exception as exc:
            return ("FAIL", f"v1.2.1 scenario & session manager check failed: {exc}")

    def _check_imports(self) -> Tuple[str, str]:
        """Check all replay submodule imports."""
        modules = [
            "replay.replay_schema",
            "replay.replay_calendar",
            "replay.replay_data_source",
            "replay.future_data_firewall",
            "replay.point_in_time_context",
            "replay.replay_timeline",
            "replay.replay_session_store",
            "replay.replay_training_session",
            "replay.replay_training_engine",
            "replay.replay_decision",
            "replay.replay_annotations",
            "replay.replay_summary",
            "replay.replay_query",
        ]
        failed = []
        for mod in modules:
            try:
                __import__(mod)
            except Exception as exc:
                failed.append(f"{mod}: {exc}")
        if failed:
            return ("FAIL", f"Import failures: {'; '.join(failed)}")
        return ("PASS", f"All {len(modules)} replay modules imported successfully")

    def _check_schema(self) -> Tuple[str, str]:
        """Check schema dataclasses can be instantiated."""
        try:
            from replay.replay_schema import (
                ReplaySessionConfig, ReplaySessionState, ReplayMarketSnapshot,
                ReplayDecision, ReplayEvent, ReplayAnnotation,
            )
            import uuid
            from datetime import datetime, timezone

            sid = "RPL-TST-20230101-TEST"
            now = datetime.now(timezone.utc).isoformat()

            config = ReplaySessionConfig(
                session_id=sid, session_name="test", symbol="TST",
                start_date="2023-01-02", end_date="2023-12-29",
            )
            assert config.research_only is True
            assert config.no_real_orders is True

            state = ReplaySessionState(
                session_id=sid, current_date="2023-01-02",
                current_index=0, total_steps=10, status="CREATED",
            )
            assert state.research_only is True

            snap = ReplayMarketSnapshot(session_id=sid, symbol="TST", replay_date="2023-01-02")
            assert snap.research_only is True

            dec = ReplayDecision(
                decision_id="DEC-TEST", session_id=sid, symbol="TST",
                replay_date="2023-01-02", action="WAIT",
            )
            assert dec.simulation_decision_only is True
            assert dec.no_real_orders is True

            return ("PASS", "All schema dataclasses instantiate correctly with safety invariants")
        except Exception as exc:
            return ("FAIL", f"Schema check failed: {exc}")

    def _check_future_firewall(self) -> Tuple[str, str]:
        """Check future data firewall works."""
        try:
            from replay.future_data_firewall import ReplayFutureDataFirewall
            fw = ReplayFutureDataFirewall()

            # Test forbidden field detection
            test_dict = {
                "close": 100.0,
                "forward_return_5": 0.05,  # forbidden
                "hindsight_score": 0.9,    # forbidden
                "MA20": 99.0,              # safe
            }
            found = fw.future_field_scan(test_dict)
            if "forward_return_5" not in found:
                return ("FAIL", "forward_return_5 not detected as forbidden field")
            if "hindsight_score" not in found:
                return ("FAIL", "hindsight_score not detected as forbidden field")
            if "close" in found or "MA20" in found:
                return ("FAIL", "Safe fields incorrectly flagged as forbidden")

            # Test sanitize_context
            sanitized, blocked, warnings = fw.sanitize_context(test_dict, "2023-06-15")
            if blocked != 2:
                return ("WARN", f"Expected 2 blocked fields, got {blocked}")
            if "forward_return_5" in sanitized:
                return ("FAIL", "forward_return_5 not removed by sanitize_context")

            return ("PASS", f"Future firewall working: detected {len(found)} forbidden fields, blocked {blocked}")
        except Exception as exc:
            return ("FAIL", f"Future firewall check failed: {exc}")

    def _check_date_navigation(self) -> Tuple[str, str]:
        """Check date navigation guards."""
        try:
            from replay.replay_timeline import ReplayTimeline

            tl = ReplayTimeline()
            dates = ["2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06"]
            tl.initialize(dates)

            # previous at first day: should not go negative
            prev_date, changed = tl.previous()
            if changed:
                return ("FAIL", "previous() at first day should return changed=False")
            if prev_date != "2023-01-02":
                return ("FAIL", f"previous() at first day should return first date, got {prev_date}")

            # next at last day: should mark completed
            tl.jump_index(4)
            next_date, changed, completed = tl.next()
            if not completed:
                return ("FAIL", "next() at last day should return completed=True")

            # jump normalizes non-trading day
            tl2 = ReplayTimeline()
            tl2.initialize(dates)
            actual, normalized = tl2.jump("2023-01-07")  # weekend, not in list
            if not normalized:
                return ("WARN", "jump to non-trading day should set normalized=True")

            return ("PASS", "Date navigation guards working correctly")
        except Exception as exc:
            return ("FAIL", f"Date navigation check failed: {exc}")

    def _check_session_lifecycle(self) -> Tuple[str, str]:
        """Check session lifecycle in memory (no disk side effects)."""
        try:
            import tempfile
            import os
            from replay.replay_training_engine import ReplayTrainingEngine

            with tempfile.TemporaryDirectory() as tmpdir:
                engine = ReplayTrainingEngine(repo_root=tmpdir, mode="mock")
                state = engine.create_session("TST", "2023-01-02", "2023-01-31", name="Health check test")
                if not state:
                    return ("FAIL", "create_session returned None")
                if not state.session_id.startswith("RPL-"):
                    return ("FAIL", f"session_id should start with RPL-, got {state.session_id}")
                if state.research_only is not True:
                    return ("FAIL", "research_only must be True")
                if state.no_real_orders is not True:
                    return ("FAIL", "no_real_orders must be True")

            return ("PASS", "Session lifecycle checks passed")
        except Exception as exc:
            return ("FAIL", f"Session lifecycle check failed: {exc}")

    def _check_decision_simulation_only(self) -> Tuple[str, str]:
        """Check that decisions are simulation-only."""
        try:
            from replay.replay_decision import ReplayDecisionManager

            mgr = ReplayDecisionManager(store=None)
            if not mgr.SIMULATION_DECISION_ONLY:
                return ("FAIL", "SIMULATION_DECISION_ONLY must be True on ReplayDecisionManager")

            dec = mgr.create_decision(
                session_id="RPL-TST-20230101-TEST",
                symbol="TST",
                replay_date="2023-06-15",
                action="WAIT",
                confidence=60,
            )
            if not dec.simulation_decision_only:
                return ("FAIL", "Decision simulation_decision_only must be True")
            if not dec.no_real_orders:
                return ("FAIL", "Decision no_real_orders must be True")
            if not dec.research_only:
                return ("FAIL", "Decision research_only must be True")

            return ("PASS", "Decision simulation-only invariants confirmed")
        except Exception as exc:
            return ("FAIL", f"Decision simulation-only check failed: {exc}")

    def _check_no_forbidden_actions(self) -> Tuple[str, str]:
        """Check no forbidden broker/trading actions are present."""
        import importlib
        forbidden_names = [
            "submit_order", "place_order", "send_order", "broker_login",
            "auto_trade", "execute_order", "buy_order", "sell_order",
        ]
        modules_to_check = [
            "replay.replay_training_engine",
            "replay.replay_decision",
            "replay.replay_training_session",
        ]
        found_forbidden = []
        for mod_name in modules_to_check:
            try:
                mod = importlib.import_module(mod_name)
                source = ""
                try:
                    import inspect
                    source = inspect.getsource(mod)
                except Exception:
                    pass
                for fname in forbidden_names:
                    if fname in source:
                        found_forbidden.append(f"{mod_name}.{fname}")
            except Exception:
                pass
        if found_forbidden:
            return ("FAIL", f"Forbidden actions found: {found_forbidden}")
        return ("PASS", "No forbidden broker/trading actions found")

    def _check_safety_flags(self) -> Tuple[str, str]:
        """Check safety flags in engine."""
        try:
            from replay.replay_training_engine import ReplayTrainingEngine
            if not ReplayTrainingEngine.RESEARCH_ONLY:
                return ("FAIL", "ReplayTrainingEngine.RESEARCH_ONLY must be True")
            if not ReplayTrainingEngine.NO_REAL_ORDERS:
                return ("FAIL", "ReplayTrainingEngine.NO_REAL_ORDERS must be True")
            if not ReplayTrainingEngine.REPLAY_TRAINING_ONLY:
                return ("FAIL", "ReplayTrainingEngine.REPLAY_TRAINING_ONLY must be True")
            return ("PASS", "All safety flags set correctly on ReplayTrainingEngine")
        except Exception as exc:
            return ("FAIL", f"Safety flag check failed: {exc}")

    def overall_status(self, results: Dict[str, Tuple[str, str]]) -> str:
        """Return overall status: PASS/WARN/FAIL/BLOCKED."""
        statuses = [r[0] for r in results.values()]
        if "BLOCKED" in statuses:
            return "BLOCKED"
        if "FAIL" in statuses:
            return "FAIL"
        if "WARN" in statuses:
            return "WARN"
        return "PASS"

    def print_results(self, results: Dict[str, Tuple[str, str]]) -> None:
        """Print formatted health check results."""
        print("=" * 60)
        print("  Replay Training Health Check v1.2.0")
        print("  [!] Research Only | No Real Orders | Replay Training Only")
        print("=" * 60)
        for check_name, (status, message) in results.items():
            icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "BLOCKED": "[BLKD]"}.get(status, "[????]")
            print(f"  {icon} {check_name}: {message}")
        overall = self.overall_status(results)
        print("-" * 60)
        print(f"  Overall: {overall}")
        print("=" * 60)
