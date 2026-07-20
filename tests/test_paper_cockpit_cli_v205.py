"""
tests/test_paper_cockpit_cli_v205.py
v2.0.5 CLI Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


def test_command_registry_importable():
    import cli.command_registry

def test_v205_commands_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-rotate-watchlist" in cmd_names

def test_v205_promote_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-promote-candidates" in cmd_names

def test_v205_demote_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-demote-candidates" in cmd_names

def test_v205_human_review_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-build-human-review-queue" in cmd_names

def test_v205_quarantine_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-build-quarantine-queue" in cmd_names

def test_v205_export_json_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-export-json" in cmd_names

def test_v205_export_md_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-export-md" in cmd_names

def test_v205_export_csv_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-export-csv" in cmd_names

def test_v205_health_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-health" in cmd_names

def test_v205_gate_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v205-gate" in cmd_names

def test_v205_commands_safety_classification():
    from cli.command_registry import PROVIDER_COMMANDS
    v205_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v205")]
    for cmd in v205_cmds:
        assert cmd.safety_classification == "RESEARCH_ONLY"

def test_v205_commands_group():
    from cli.command_registry import PROVIDER_COMMANDS
    v205_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v205")]
    for cmd in v205_cmds:
        assert cmd.group == "paper_cockpit_v205"

def test_v205_commands_introduced_in():
    from cli.command_registry import PROVIDER_COMMANDS
    v205_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v205")]
    for cmd in v205_cmds:
        assert cmd.introduced_in == "2.0.5"

def test_v205_commands_count_10():
    from cli.command_registry import PROVIDER_COMMANDS
    v205_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v205")]
    assert len(v205_cmds) == 10

def test_cmd_rotate_watchlist_callable():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v205_rotate_watchlist")

def test_cmd_promote_candidates_callable():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v205_promote_candidates")

def test_cmd_demote_candidates_callable():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v205_demote_candidates")

def test_cmd_build_human_review_queue_callable():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v205_build_human_review_queue")

def test_cmd_build_quarantine_queue_callable():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v205_build_quarantine_queue")
