"""
reports/source_lineage_rate_limit_report.py — Source Lineage & Rate Limit Report v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No secrets. No token output. No auth header output.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
RATE_LIMIT_AUTO_BYPASS_ENABLED = False


class SourceLineageRateLimitReport:
    """
    12-section Markdown report for Source Lineage & Rate Limit governance v1.4.5.
    [!] No secrets. No token output. No auth header output.
    """

    TITLE = "Source Lineage & Rate Limit Governance Report v1.4.5"
    VERSION = "1.4.5"
    RELEASE_NAME = "Source Lineage & Rate Limit"
    SECTIONS = 12

    def render(self) -> str:
        lines = []
        lines.append(f"# {self.TITLE}")
        lines.append("")
        lines.append("> **[!] Research Only. No Real Orders. Not Investment Advice.**")
        lines.append("> **[!] No secrets. No token output. No auth header output.**")
        lines.append("> **[!] No rate bypass. No proxy rotation. No token rotation.**")
        lines.append("")

        # Section 1: Overview
        lines.append("## 1. Overview")
        lines.append("")
        lines.append(f"- Version: {self.VERSION}")
        lines.append(f"- Release: {self.RELEASE_NAME}")
        lines.append("- Package: `data/governance/`")
        lines.append("- Modules: 20 governance modules + 5 provider bridges")
        lines.append("- CLI Commands: 21 source_governance commands")
        lines.append("- Tests: 177 offline tests")
        lines.append("")

        # Section 2: Source Authority Hierarchy
        lines.append("## 2. Source Authority Hierarchy")
        lines.append("")
        lines.append("| Level | Providers | Formal Use |")
        lines.append("|-------|-----------|------------|")
        lines.append("| PRIMARY_OFFICIAL | TWSE, TPEx, MOPS | Allowed |")
        lines.append("| PRIMARY_DOMAIN_OFFICIAL | data.gov.tw | Allowed |")
        lines.append("| SECONDARY_OFFICIAL | (none registered) | Allowed |")
        lines.append("| SECONDARY_AGGREGATOR | FinMind | Requires primary validation |")
        lines.append("| TEST_FIXTURE | fixture | NOT ALLOWED |")
        lines.append("| MOCK | mock | NOT ALLOWED |")
        lines.append("| UNKNOWN | (unknown) | NOT ALLOWED |")
        lines.append("")
        lines.append("**Rules:**")
        lines.append("- Lower authority cannot override higher authority.")
        lines.append("- PRIMARY always wins in conflict resolution.")
        lines.append("- No auto-repair. No silent fallback.")
        lines.append("")

        # Section 3: Source Identity & Lineage Registry
        lines.append("## 3. Source Identity & Lineage Registry")
        lines.append("")
        lines.append("- `SourceIdentity`: Identifies each data source with authority metadata.")
        lines.append("- `SourceLineageRecord`: Full audit trail for each data record.")
        lines.append("- Registry: in-memory for tests, SQLite optional for runtime (gitignored).")
        lines.append("- `trace_to_root()`: BFS traversal of lineage chain.")
        lines.append("")

        # Section 4: Provenance Completeness Gate
        lines.append("## 4. Provenance Completeness Gate")
        lines.append("")
        lines.append("**PASS requires all:**")
        lines.append("- provider_id, source_id, authority_level, dataset")
        lines.append("- request_fingerprint, fetched_at, source_content_hash")
        lines.append("- normalized_content_hash, schema_version, parser_version")
        lines.append("- observation_date OR reporting_period")
        lines.append("- quality_status, freshness_status")
        lines.append("- real mode, no mock fallback")
        lines.append("")
        lines.append("**BLOCKED:**")
        lines.append("- Mock in real mode")
        lines.append("- Fixture in formal conclusion")
        lines.append("- PIT required + unknown available_from")
        lines.append("")

        # Section 5: Request Fingerprint
        lines.append("## 5. Request Fingerprint")
        lines.append("")
        lines.append("- SHA-256, deterministic, parameter order independent (sorted keys).")
        lines.append("- Secrets removed: token, key, cookie, auth.")
        lines.append("- Real/mock modes produce different fingerprints.")
        lines.append("- No random `hash()` — SHA-256 only.")
        lines.append("")

        # Section 6: Request Ledger & Fetch Run Audit
        lines.append("## 6. Request Ledger & Fetch Run Audit")
        lines.append("")
        lines.append("- `RequestLedger`: Append-only. No token stored. Auth headers redacted.")
        lines.append("- `FetchRunAudit`: Invariants: records_written <= records_valid.")
        lines.append("- Dry run default: `dry_run=True`.")
        lines.append("")

        # Section 7: Rate Limit Manager
        lines.append("## 7. Rate Limit Manager")
        lines.append("")
        lines.append("- Central rate limiting for all providers.")
        lines.append("- Per-host token bucket with minimum interval enforcement.")
        lines.append("- Injectable clock for deterministic tests.")
        lines.append("- **RATE_LIMIT_AUTO_BYPASS_ENABLED=False**")
        lines.append("- **No proxy rotation. No token rotation.**")
        lines.append("")

        # Section 8: Host Policies & Provider Budgets
        lines.append("## 8. Host Policies & Provider Budgets")
        lines.append("")
        lines.append("| Provider | Host | Min Interval | RPM | Confidence |")
        lines.append("|----------|------|-------------|-----|------------|")
        lines.append("| TWSE | www.twse.com.tw | 3000ms | 20 | LOW |")
        lines.append("| TPEx | www.tpex.org.tw | 3000ms | 20 | LOW |")
        lines.append("| MOPS | mops.twse.com.tw | 4000ms | 15 | LOW |")
        lines.append("| data.gov.tw | data.gov.tw | 2000ms | 30 | LOW |")
        lines.append("| FinMind | api.finmindtrade.com | 6000ms | 10 | LOW |")
        lines.append("")
        lines.append("All policies are conservative defaults (confidence=LOW).")
        lines.append("Unknown quota → block large batch.")
        lines.append("")

        # Section 9: Quota & Retry Evidence
        lines.append("## 9. Quota & Retry Evidence")
        lines.append("")
        lines.append("**Quota Evidence:**")
        lines.append("- Allowlisted headers only: X-RateLimit-*, X-Quota-*, RateLimit-*, Retry-After.")
        lines.append("- Never store auth headers, cookies.")
        lines.append("- FinMind status=402 → QUOTA_EXCEEDED evidence.")
        lines.append("")
        lines.append("**Retry Evidence:**")
        lines.append("- Exponential backoff with optional jitter.")
        lines.append("- Injectable clock for tests — no real sleep.")
        lines.append("- Retry-After header parsed (seconds and HTTP-date formats).")
        lines.append("")

        # Section 10: Cache & Conflict Lineage
        lines.append("## 10. Cache & Conflict Lineage")
        lines.append("")
        lines.append("**Cache Lineage:**")
        lines.append("- Corrupt cache → invalid lineage.")
        lines.append("- Mock cache → no real lineage.")
        lines.append("- Stale → no fresh status.")
        lines.append("")
        lines.append("**Conflict Lineage:**")
        lines.append("- Primary always wins. No auto-repair.")
        lines.append("- Resolution auditable. Old record preserved.")
        lines.append("- `formal_use_blocked=True` for unresolved conflicts.")
        lines.append("")

        # Section 11: Safety Invariants
        lines.append("## 11. Safety Invariants")
        lines.append("")
        lines.append("| Invariant | Status |")
        lines.append("|-----------|--------|")
        lines.append("| NO_REAL_ORDERS | True |")
        lines.append("| BROKER_EXECUTION_ENABLED | False |")
        lines.append("| PRODUCTION_TRADING_BLOCKED | True |")
        lines.append("| RATE_LIMIT_AUTO_BYPASS_ENABLED | False |")
        lines.append("| TOKEN_ROTATION_ENABLED | False |")
        lines.append("| PROXY_ROTATION_ENABLED | False |")
        lines.append("| PRIMARY_SOURCE_OVERRIDE_ENABLED | False |")
        lines.append("| MULTI_ACCOUNT_LIMIT_BYPASS_ENABLED | False |")
        lines.append("")

        # Section 12: CLI Commands
        lines.append("## 12. CLI Commands (21)")
        lines.append("")
        commands = [
            "source-governance-health", "source-lineage-sources", "source-lineage-show",
            "source-lineage-trace", "source-lineage-record", "source-lineage-incomplete",
            "request-ledger-list", "request-ledger-show", "fetch-run-list", "fetch-run-show",
            "rate-limit-status", "rate-limit-host", "rate-limit-provider", "rate-limit-endpoint",
            "request-budget-status", "quota-evidence-list", "retry-evidence-list",
            "cache-lineage-show", "conflict-lineage-list", "conflict-lineage-show",
            "source-governance-report",
        ]
        for cmd in commands:
            lines.append(f"- `{cmd}` — Research Only")
        lines.append("")
        lines.append("---")
        lines.append("*[!] Research Only. No Real Orders. Not Investment Advice.*")
        lines.append("*[!] No secrets in this report. No token output.*")

        return "\n".join(lines)
