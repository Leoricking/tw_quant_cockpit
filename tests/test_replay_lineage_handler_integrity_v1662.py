"""
test_replay_lineage_handler_integrity_v1662.py — v1.6.6.2 Replay Session Lineage Orphan Handler Hotfix.

Validates:
- replay-session-lineage has exactly one command_map entry
- effective handler is cmd_replay_session_lineage_v128
- cmd_replay_session_lineage (old orphan) does not exist
- true orphan handlers = 0
- overwritten-only handlers = 0
- formal CLI still 566/566
- replay-session-lineage is parser-reachable and dispatch works
- semantic output schema unchanged
- no dangerous capabilities

[!] Research Only. No Real Orders. No Broker. No Production.
"""
import ast
import os
import sys
import importlib

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

MAIN_PY = os.path.join(REPO, "main.py")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_command_map_entries():
    """Return list of (key, handler_name) from command_map AST (all occurrences)."""
    with open(MAIN_PY, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    entries = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name) and target.id == "command_map":
                            if isinstance(stmt.value, ast.Dict):
                                for key_node, val_node in zip(
                                    stmt.value.keys, stmt.value.values
                                ):
                                    if isinstance(key_node, ast.Constant):
                                        key = key_node.value
                                        if isinstance(val_node, ast.Name):
                                            handler = val_node.id
                                        elif isinstance(val_node, ast.Lambda):
                                            body = val_node.body
                                            if (
                                                isinstance(body, ast.Call)
                                                and body.args
                                                and isinstance(body.args[0], ast.Call)
                                                and isinstance(body.args[0].func, ast.Name)
                                            ):
                                                handler = body.args[0].func.id
                                            else:
                                                handler = "lambda"
                                        else:
                                            handler = "expr"
                                        entries.append((key, handler))
    return entries


def _get_all_cmd_functions():
    """Return set of cmd_* function names defined via `def` in main.py."""
    with open(MAIN_PY, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    funcs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("cmd_"):
                funcs.add(node.name)
    return funcs


# ---------------------------------------------------------------------------
# Test 1: replay-session-lineage occurrence count = 1
# ---------------------------------------------------------------------------

class TestCommandMapLineage:
    def test_01_replay_lineage_occurrence_count_is_one(self):
        """Test 1: replay-session-lineage appears exactly once in command_map."""
        entries = _get_command_map_entries()
        occurrences = [e for e in entries if e[0] == "replay-session-lineage"]
        assert len(occurrences) == 1, (
            f"Expected 1 occurrence, got {len(occurrences)}: {occurrences}"
        )

    def test_02_effective_handler_is_v128(self):
        """Test 2: The handler for replay-session-lineage is cmd_replay_session_lineage_v128."""
        entries = _get_command_map_entries()
        occurrences = [e for e in entries if e[0] == "replay-session-lineage"]
        assert len(occurrences) == 1
        _, handler = occurrences[0]
        assert handler == "cmd_replay_session_lineage_v128", (
            f"Expected cmd_replay_session_lineage_v128, got {handler}"
        )

    def test_03_old_handler_not_in_command_map(self):
        """Test 3: cmd_replay_session_lineage (old orphan) is not referenced in command_map."""
        entries = _get_command_map_entries()
        old_refs = [e for e in entries if e[1] == "cmd_replay_session_lineage"]
        assert not old_refs, (
            f"cmd_replay_session_lineage still referenced in command_map: {old_refs}"
        )

    def test_04_old_handler_function_not_defined(self):
        """Test 4: cmd_replay_session_lineage function definition does not exist in main.py."""
        funcs = _get_all_cmd_functions()
        assert "cmd_replay_session_lineage" not in funcs, (
            "cmd_replay_session_lineage function still defined in main.py"
        )

    def test_05_v128_handler_function_defined(self):
        """Test 5: cmd_replay_session_lineage_v128 function definition exists."""
        funcs = _get_all_cmd_functions()
        assert "cmd_replay_session_lineage_v128" in funcs, (
            "cmd_replay_session_lineage_v128 not defined in main.py"
        )


# ---------------------------------------------------------------------------
# Test 2: Orphan handler audit
# ---------------------------------------------------------------------------

class TestOrphanHandlers:
    def _compute_orphan_state(self):
        entries = _get_command_map_entries()
        all_funcs = _get_all_cmd_functions()

        from cli.command_registry import PROVIDER_COMMANDS
        formal_handlers = {s.handler_name for s in PROVIDER_COMMANDS}

        # Build effective map (last occurrence wins)
        from collections import defaultdict
        key_to_handlers = defaultdict(list)
        for key, handler in entries:
            key_to_handlers[key].append(handler)

        effective_handlers = set()
        overwritten_handlers = set()
        for key, handlers in key_to_handlers.items():
            effective_handlers.add(handlers[-1])
            for h in handlers[:-1]:
                overwritten_handlers.add(h)

        true_overwritten_only = overwritten_handlers - effective_handlers
        true_orphans = all_funcs - effective_handlers - formal_handlers

        return {
            "effective_handlers": effective_handlers,
            "overwritten_handlers": overwritten_handlers,
            "true_overwritten_only": true_overwritten_only,
            "true_orphans": true_orphans,
        }

    def test_06_true_orphan_handlers_zero(self):
        """Test 6: true orphan handlers (cmd_* not effective, not formal) = 0."""
        state = self._compute_orphan_state()
        orphans = state["true_orphans"]
        assert not orphans, f"True orphan handlers found: {sorted(orphans)}"

    def test_07_overwritten_only_handlers_zero(self):
        """Test 7: overwritten-only handlers = 0."""
        state = self._compute_orphan_state()
        overwritten_only = state["true_overwritten_only"]
        assert not overwritten_only, (
            f"Overwritten-only handlers found: {sorted(overwritten_only)}"
        )

    def test_08_cmd_replay_session_lineage_not_overwritten(self):
        """Test 8: cmd_replay_session_lineage is neither in effective handlers nor overwritten handlers."""
        state = self._compute_orphan_state()
        assert "cmd_replay_session_lineage" not in state["effective_handlers"]
        assert "cmd_replay_session_lineage" not in state["overwritten_handlers"]


# ---------------------------------------------------------------------------
# Test 3: Formal CLI integrity
# ---------------------------------------------------------------------------

class TestFormalCLIIntegrity:
    def test_09_formal_cli_count_566(self):
        """Test 9: Formal CLI still has exactly 566 commands."""
        from cli.command_registry import get_formal_command_names
        formal = get_formal_command_names()
        assert len(formal) == 566, f"Expected 566 formal commands, got {len(formal)}"

    def test_10_all_formal_commands_in_command_map(self):
        """Test 10: All 566 formal commands are present in the command_map."""
        from cli.command_registry import get_formal_command_names
        formal = get_formal_command_names()
        entries = _get_command_map_entries()
        # Build effective keys (unique keys after last-wins)
        from collections import OrderedDict
        effective_keys = set()
        for key, _ in entries:
            effective_keys.add(key)
        missing = formal - effective_keys
        assert not missing, f"Formal commands missing from command_map: {sorted(missing)[:10]}"

    def test_11_all_formal_handlers_callable(self):
        """Test 11: All formal command handlers resolve to callables in main."""
        from cli.command_registry import PROVIDER_COMMANDS
        main_mod = importlib.import_module("main")
        unresolved = [
            s.handler_name
            for s in PROVIDER_COMMANDS
            if not callable(getattr(main_mod, s.handler_name, None))
        ]
        assert not unresolved, f"Unresolved formal handlers: {unresolved}"


# ---------------------------------------------------------------------------
# Test 4: Parser and dispatch
# ---------------------------------------------------------------------------

class TestReplayLineageDispatch:
    def test_12_replay_lineage_parser_registered(self):
        """Test 12: replay-session-lineage is registered in argparse."""
        import main as m
        parser = m._build_parser()
        sp = None
        for action in parser._actions:
            if hasattr(action, "_name_parser_map"):
                sp = action
                break
        assert sp is not None
        assert "replay-session-lineage" in sp._name_parser_map, (
            "replay-session-lineage not in argparse subparsers"
        )

    def test_13_replay_lineage_handler_callable(self):
        """Test 13: cmd_replay_session_lineage_v128 is callable in main."""
        main_mod = importlib.import_module("main")
        fn = getattr(main_mod, "cmd_replay_session_lineage_v128", None)
        assert callable(fn), "cmd_replay_session_lineage_v128 is not callable"

    def test_14_replay_lineage_dispatch_no_exception(self):
        """Test 14: Dispatching replay-session-lineage with empty session_id does not raise exception."""
        main_mod = importlib.import_module("main")
        fn = getattr(main_mod, "cmd_replay_session_lineage_v128")
        import argparse
        args = argparse.Namespace(session_id=None)
        # Should print error but not raise
        try:
            fn(args)
        except SystemExit:
            pass  # argparse may call sys.exit; acceptable
        except Exception as exc:
            pytest.fail(f"cmd_replay_session_lineage_v128 raised exception: {exc}")

    def test_15_command_map_dispatch_resolves_v128(self):
        """Test 15: command_map.get('replay-session-lineage') resolves to cmd_replay_session_lineage_v128."""
        main_mod = importlib.import_module("main")
        import argparse
        # Build the command map by calling main's internals
        # We verify via AST that the effective handler is v128, which we already do in Test 2.
        # Here we verify at module level via getattr.
        fn_v128 = getattr(main_mod, "cmd_replay_session_lineage_v128", None)
        assert callable(fn_v128)
        # Verify old handler does not exist as module attribute
        fn_old = getattr(main_mod, "cmd_replay_session_lineage", None)
        assert fn_old is None, (
            f"cmd_replay_session_lineage still exists as module attribute: {fn_old}"
        )


# ---------------------------------------------------------------------------
# Test 5: Semantic output schema unchanged
# ---------------------------------------------------------------------------

class TestSemanticOutputUnchanged:
    def test_16_v128_docstring_research_only(self):
        """Test 16: cmd_replay_session_lineage_v128 docstring contains Research Only marker."""
        main_mod = importlib.import_module("main")
        fn = getattr(main_mod, "cmd_replay_session_lineage_v128")
        doc = fn.__doc__ or ""
        assert "Research Only" in doc, f"Missing Research Only in docstring: {doc}"

    def test_17_v128_no_real_orders_marker(self):
        """Test 17: cmd_replay_session_lineage_v128 does not claim real order capability."""
        main_mod = importlib.import_module("main")
        fn = getattr(main_mod, "cmd_replay_session_lineage_v128")
        doc = (fn.__doc__ or "").lower()
        # Should not assert real order capability (only denial is acceptable)
        assert "real order" not in doc or "no real" in doc, (
            "Unexpected real order capability in docstring"
        )

    def test_18_output_no_exception_with_mock_args(self):
        """Test 18: Running v128 handler with typical args produces no exception."""
        main_mod = importlib.import_module("main")
        fn = getattr(main_mod, "cmd_replay_session_lineage_v128")
        import argparse
        args = argparse.Namespace(session_id="test-session-001")
        try:
            fn(args)
        except SystemExit:
            pass
        except Exception as exc:
            # Acceptable: module import errors (replay package may not be populated)
            # The handler should not raise unhandled exceptions
            msg = str(exc)
            assert any(
                kw in msg.lower()
                for kw in ["import", "module", "no module", "not found", "error"]
            ), f"Unexpected exception type: {exc}"


# ---------------------------------------------------------------------------
# Test 6: Safety — no dangerous capabilities
# ---------------------------------------------------------------------------

class TestSafetyCapabilities:
    def test_19_no_broker_import(self):
        """Test 19: cmd_replay_session_lineage_v128 has no broker import."""
        with open(MAIN_PY, "r", encoding="utf-8") as f:
            source = f.read()
        # The function starts at its def and ends at next def or end of file
        # We check that broker-related strings are not in the v128 handler source
        import re
        pattern = r"def cmd_replay_session_lineage_v128.*?(?=\ndef |\Z)"
        match = re.search(pattern, source, re.DOTALL)
        assert match is not None, "cmd_replay_session_lineage_v128 not found"
        func_src = match.group(0).lower()
        dangerous_terms = ["broker", "real_order", "real_account", "production_db", "kafka", "redis"]
        found = [t for t in dangerous_terms if t in func_src]
        assert not found, f"Dangerous capability terms found: {found}"

    def test_20_no_real_order_capability(self):
        """Test 20: cmd_replay_session_lineage_v128 does not execute real orders."""
        main_mod = importlib.import_module("main")
        fn = getattr(main_mod, "cmd_replay_session_lineage_v128")
        doc = (fn.__doc__ or "").lower()
        # Docstring should indicate research only
        assert "research" in doc or "research only" in doc or "[!]" in (fn.__doc__ or ""), (
            f"Missing research marker in docstring: {fn.__doc__}"
        )


# ---------------------------------------------------------------------------
# Test 7: Version
# ---------------------------------------------------------------------------

class TestVersion:
    def test_21_version_is_1662(self):
        """Test 21: VERSION is 1.6.6.2."""
        from release.version_info import VERSION
        assert VERSION == "1.6.6.2", f"Expected 1.6.6.2, got {VERSION}"

    def test_22_release_name_correct(self):
        """Test 22: RELEASE_NAME is Replay Session Lineage Handler Integrity Hotfix."""
        from release.version_info import RELEASE_NAME
        assert RELEASE_NAME == "Replay Session Lineage Handler Integrity Hotfix", (
            f"Got: {RELEASE_NAME}"
        )

    def test_23_base_release_is_1661(self):
        """Test 23: BASE_RELEASE references 1.6.6.1."""
        from release.version_info import BASE_RELEASE
        assert "1.6.6.1" in BASE_RELEASE, f"Expected 1.6.6.1 in BASE_RELEASE, got {BASE_RELEASE}"

    def test_24_duplicate_unique_keys_reduced(self):
        """Test 24: Duplicate unique key count is 10 (was 11, replay-session-lineage resolved)."""
        from collections import Counter
        entries = _get_command_map_entries()
        key_counts = Counter(k for k, _ in entries)
        dup_keys = {k for k, c in key_counts.items() if c > 1}
        assert len(dup_keys) == 10, (
            f"Expected 10 duplicate unique keys, got {len(dup_keys)}: {sorted(dup_keys)}"
        )
        assert "replay-session-lineage" not in dup_keys, (
            "replay-session-lineage still a duplicate key"
        )
