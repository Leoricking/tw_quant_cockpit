"""tests/test_mistake_taxonomy_cli_v176.py — v1.7.6 CLI command registration tests."""
import pytest
from cli.command_registry import PROVIDER_COMMANDS


_MT_CMDS = [c for c in PROVIDER_COMMANDS if c.name.startswith("mistake-taxonomy")]


class TestMistakeTaxonomyCommands:
    def test_mt_commands_ge_14(self):
        assert len(_MT_CMDS) >= 14

    def test_mt_version_exists(self):
        assert any(c.name == "mistake-taxonomy-version" for c in _MT_CMDS)

    def test_mt_classify_exists(self):
        assert any(c.name == "mistake-taxonomy-classify" for c in _MT_CMDS)

    def test_mt_cost_exists(self):
        assert any(c.name == "mistake-taxonomy-cost" for c in _MT_CMDS)

    def test_mt_repeat_exists(self):
        assert any(c.name == "mistake-taxonomy-repeat" for c in _MT_CMDS)

    def test_mt_weekly_review_exists(self):
        assert any(c.name == "mistake-taxonomy-weekly-review" for c in _MT_CMDS)

    def test_mt_monthly_review_exists(self):
        assert any(c.name == "mistake-taxonomy-monthly-review" for c in _MT_CMDS)

    def test_mt_behavior_score_exists(self):
        assert any(c.name == "mistake-taxonomy-behavior-score" for c in _MT_CMDS)

    def test_mt_dashboard_exists(self):
        assert any(c.name == "mistake-taxonomy-dashboard" for c in _MT_CMDS)

    def test_mt_actions_exists(self):
        assert any(c.name == "mistake-taxonomy-actions" for c in _MT_CMDS)

    def test_mt_scenarios_exists(self):
        assert any(c.name == "mistake-taxonomy-scenarios" for c in _MT_CMDS)

    def test_mt_fixtures_exists(self):
        assert any(c.name == "mistake-taxonomy-fixtures" for c in _MT_CMDS)

    def test_mt_health_exists(self):
        assert any(c.name == "mistake-taxonomy-health" for c in _MT_CMDS)

    def test_mt_gate_exists(self):
        assert any(c.name == "mistake-taxonomy-gate" for c in _MT_CMDS)

    def test_mt_safety_audit_exists(self):
        assert any(c.name == "mistake-taxonomy-safety-audit" for c in _MT_CMDS)

    def test_all_research_only(self):
        assert all(c.safety_classification == "RESEARCH_ONLY" for c in _MT_CMDS)

    def test_all_introduced_in_176(self):
        assert all(c.introduced_in == "1.7.6" for c in _MT_CMDS)

    def test_all_have_group_mistake_taxonomy(self):
        assert all(c.group == "mistake_taxonomy" for c in _MT_CMDS)
