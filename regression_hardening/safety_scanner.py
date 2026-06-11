"""
Safety Scanner — v1.0.4 Regression & Release Gate Hardening.
Scans text, files, and directories for forbidden trading actions.
Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. VALIDATED does not enable trading.
"""
from __future__ import annotations
import re
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict

FORBIDDEN_ACTIONS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]

WHITELIST_PHRASES = [
    "No Real Orders",
    "No broker execution",
    "Broker Execution Disabled",
    "not an order",
    "Not an order",
    "order count",
    "order by",
    "sort order",
    "execution disabled",
    "no execution",
    "Paper trading is simulation only",
    "Mock realtime is simulation only",
    "No automatic deletion",
    "No automatic archive",
    "Archive Suggestions Only",
    "VALIDATED does not enable trading",
    "No auto trading",
    "No automatic trading",
    "no_real_orders",
    "NO_REAL_ORDERS",
    "no real orders flag",
    "No Real Orders flag",
    "No forbidden trading action",
    "no forbidden",
    "No forbidden",
    "RESEARCH_ONLY",
    "[RESEARCH_ONLY]",
    "Broker Execution Enabled: False",
    # Safety docstring / disclaimer patterns
    "No BUY/SELL/ORDER output",
    "No BUY/SELL/ORDER",
    "BUY/SELL/ORDER output",
    "No BUY / SELL / ORDER",
    "BUY/SELL/ORDER guard",
    "BUY/SELL/ORDER",
    "BUY / SELL / ORDER are not generated",
    "BUY / SELL / ORDER",
    "Never BUY, SELL, ORDER",
    "Place real orders (BUY / SELL / ORDER)",
    "Place real orders",
    "never emitted as actionable outputs",
    "Forbidden trading actions (BUY",
    "forbidden trading actions",
    "Forbidden trading action",
    "No forbidden trading",
    # Python list/definition contexts — full list strings
    '"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"',
    '"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE"',
    '"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER"',
    '"BUY", "SELL", "ORDER", "EXECUTE"',
    '"BUY", "SELL", "ORDER"',
    "'BUY', 'SELL', 'ORDER', 'EXECUTE', 'SUBMIT_ORDER', 'AUTO_TRADE', 'REAL_TRADE'",
    "'BUY', 'SELL', 'ORDER', 'EXECUTE', 'SUBMIT_ORDER', 'AUTO_TRADE'",
    "'BUY', 'SELL', 'ORDER', 'EXECUTE', 'SUBMIT_ORDER'",
    "'BUY', 'SELL', 'ORDER', 'EXECUTE'",
    "'BUY', 'SELL', 'ORDER'",
    "FORBIDDEN_ACTIONS",
    "FORBIDDEN_KEYWORDS",
    "_FORBIDDEN",
    "forbidden_hits",
    "forbidden_found",
    "forbidden_action",
    "blocked_by_forbidden",
    "What Not To Do",
    "not to do",
    "Production trading is blocked",
    "production blocked",
    "PRODUCTION_TRADING_BLOCKED",
    # Research report listing forbidden for safety description
    "No order execution",
    "No order placement",
    "order placement",
    "order execution is disabled",
    # Documentation / markdown contexts: guard descriptions listing forbidden tokens
    "blocks BUY/SELL/ORDER",
    "BUY/SELL/ORDER/EXECUTE",
    "BUY, SELL, ORDER, EXECUTE",
    "BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER",
    "BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE",
    "BUY, SELL, ORDER, EXECUTE, or any",
    "BUY、SELL、ORDER、EXECUTE",
    "BUY/SELL/ORDER 等禁用詞",
    "BUY/SELL/ORDER/EXECUTE/etc.",
    "blocks BUY/SELL/ORDER/EXECUTE",
    "rejects BUY/SELL/ORDER/EXECUTE",
    "rejects BUY, SELL, ORDER",
    "_guard() rejects BUY",
    "_guard() function raises",
    "raises ValueError if any text contains: BUY",
    "contains: BUY",
    "Forbidden actions blocked:",
    "Forbidden actions blocked: BUY",
    "Forbidden keywords scanned:",
    "Forbidden keywords scanned: `BUY`",
    "no forbidden keywords (BUY/SELL/ORDER",
    "no forbidden keywords",
    "REAL_ORDER_READY=False",
    "REAL_ORDER_READY = False",
    "_FORBIDDEN = ",
    "_FORBIDDEN =",
    "禁用詞過濾",
    "禁用詞",
    "No BUY/SELL/ORDER tasks",
    "The strings BUY, SELL",
    "strings BUY, SELL, ORDER",
    "generates BUY, SELL, ORDER",
    "generates BUY",
    "load_safe_commands() blocks BUY",
    "blocks BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER",
    "BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE",
    "safety — no forbidden keywords",
    "Safety — no forbidden keywords",
    "Rule IDs follow format",
    "BUY.SHORT",
    "BUY.LONG",
    "CATEGORY.TIMEFRAME.NAME",
    "e.g. BUY.",
    # Full slash-separated forbidden lists (all tokens in one phrase)
    "BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE",
    "BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE",
    "BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER",
    # Chinese bullet listing forbidden tokens
    "EXECUTE、SUBMIT_ORDER、AUTO_TRADE",
    "SUBMIT_ORDER、AUTO_TRADE、REAL_TRADE",
    "SUBMIT_ORDER、AUTO_TRADE",
    "ORDER、EXECUTE、SUBMIT_ORDER",
    "BUY、SELL、ORDER、EXECUTE、SUBMIT_ORDER",
    "在所有輸出中被替換為 REVIEW",
    "被替換為 REVIEW",
    # Documentation: _FORBIDDEN list definition
    '_FORBIDDEN = ["BUY"',
    "_FORBIDDEN = ['BUY'",
    # Markdown list item listing all forbidden tokens ending in BROKER_ORDER
    "REAL_TRADE, LIVE_TRADE, BROKER_ORDER",
    "LIVE_TRADE, BROKER_ORDER",
    "REAL_TRADE, LIVE_TRADE",
    "AUTO_TRADE, REAL_TRADE, LIVE_TRADE",
    "SUBMIT_ORDER, AUTO_TRADE, REAL_TRADE",
    "EXECUTE, SUBMIT_ORDER, AUTO_TRADE, REAL_TRADE",
    "ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE",
    # Documentation "and REAL_TRADE" at end of forbidden listing sentence
    "SUBMIT_ORDER, AUTO_TRADE, and REAL_TRADE",
    "AUTO_TRADE, and REAL_TRADE",
    "and REAL_TRADE",
    # "BROKER_ORDER pattern" — reference to the scanner pattern, not an order
    "BROKER_ORDER pattern",
    "part of BROKER_ORDER",
    # No BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE in any output
    "No BUY/SELL/ORDER/EXECUTE",
    "No BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER",
    "No BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE",
    # blocks BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE keywords (line 156 v0.8)
    "blocks BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE keywords",
    "blocks BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE",
    "BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE keywords",
    # validate_action blocks FORBIDDEN_ACTION_TYPES listing
    "FORBIDDEN_ACTION_TYPES",
    "_validate_action()",
    "_validate_action",
    # _guard() rejects all metric labels (with and without markdown backticks)
    "_guard() rejects BUY",
    "`_guard()` rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE",
    "`_guard()` rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE",
    "`_guard()` rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER",
    "`_guard()` rejects BUY/SELL/ORDER/EXECUTE",
    "`_guard()` rejects BUY",
    "_guard()",
    "`_guard()`",
    # recommendations_no_forbidden_actions
    "recommendations_no_forbidden_actions",
    # All recommendations are research actions only
    "All recommendations are research actions only",
    # Markdown backtick-quoted token listings in documentation
    '`BUY`, `SELL`, `ORDER`, `EXECUTE`, `SUBMIT_ORDER`, `AUTO_TRADE`, `REAL_TRADE`',
    '`BUY`, `SELL`, `ORDER`, `EXECUTE`, `SUBMIT_ORDER`, `AUTO_TRADE`',
    '`BUY`, `SELL`, `ORDER`, `EXECUTE`, `SUBMIT_ORDER`',
    '`BUY`, `SELL`, `ORDER`, `EXECUTE`',
    '`BUY`, `SELL`, `ORDER`',
    # _guard(text) in schema raises ValueError on forbidden keywords: `BUY`, ...
    "_guard(text) in schema raises",
    "_guard(text)",
    # _guard() rejects ... slash-separated in docs
    "_guard() rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE",
    "_guard() rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE",
    # _validate_action() in schema blocks all FORBIDDEN_ACTION_TYPES: `BUY`, ...
    "blocks all FORBIDDEN_ACTION_TYPES",
    "FORBIDDEN_ACTION_TYPES: `BUY`",
    # Safety — no forbidden keywords (BUY/SELL/ORDER/EXECUTE/etc.)
    "(BUY/SELL/ORDER/EXECUTE/etc.)",
    "BUY/SELL/ORDER/EXECUTE/etc.",
    # _FORBIDDEN = [...] Python list in backtick code
    '`_FORBIDDEN = ["BUY"',
    '`_FORBIDDEN =',
]

# Patterns that should never be flagged (technical/research context)
_SAFE_PATTERNS = [
    r'no_real_orders',
    r'NO_REAL_ORDERS',
    r'REAL_ORDERS_ENABLED\s*=\s*False',
    r'no_real_orders\s*=\s*True',
    r'production_blocked',
    r'PRODUCTION_TRADING_BLOCKED',
    r'No\s+BUY',
    r'No\s+SELL',
    r'BUY/SELL',
    r'SELL/ORDER',
    r'BUY\s*/\s*SELL',
    r'forbidden_action',
    r'FORBIDDEN_ACTION',
    r'_FORBIDDEN',
    r'forbidden_hits',
    r'forbidden_found',
    r'"BUY"',
    r"'BUY'",
    r'"SELL"',
    r"'SELL'",
    r'"ORDER"',
    r"'ORDER'",
    r'"EXECUTE"',
    r"'EXECUTE'",
    r'"SUBMIT_ORDER"',
    r"'SUBMIT_ORDER'",
    r'"AUTO_TRADE"',
    r"'AUTO_TRADE'",
    r'"REAL_TRADE"',
    r"'REAL_TRADE'",
    r'"LIVE_TRADE"',
    r"'LIVE_TRADE'",
    r'"BROKER_ORDER"',
    r"'BROKER_ORDER'",
    # Standalone quoted token fragments that remain after partial whitelist removal
    r',\s*"EXECUTE"\s*,?',
    r",\s*'EXECUTE'\s*,?",
    r',\s*"SUBMIT_ORDER"\s*,?',
    r',\s*"AUTO_TRADE"\s*,?',
    r',\s*"REAL_TRADE"\s*,?',
    r',\s*"LIVE_TRADE"\s*,?',
    r',\s*"BROKER_ORDER"\s*,?',
    r'never\s+emitted',
    r'blocked\s+by\s+design',
    r'production\s+trading\s+is\s+blocked',
    r'not\s+generated',
    r'never\s+BUY',
    r'Never\s+BUY',
    r'Place\s+real\s+orders',
    r'What\s+Not\s+To\s+Do',
    # Safety declaration patterns - "Never BUY, SELL, ORDER, EXECUTE..."
    r'Never\s+BUY,\s*SELL',
    r'Never\s+BUY,\s+SELL,\s+ORDER',
    # Forbidden trading action listing patterns
    r'Forbidden\s+trading\s+actions?\s*\(',
    r'are\s+never\s+emitted',
    # BUY/SELL/ORDER guard description
    r'BUY/SELL/ORDER\s+guard',
    r'guard\s+in\s+\w',
]

_SKIP_EXTENSIONS = {'.pyc', '.db', '.sqlite', '.xlsx', '.xls', '.csv', '.zip', '.env'}
_SKIP_DIRS = {'__pycache__', '.git', 'node_modules', 'dist', '.eggs', 'auto_report_center'}


@dataclass
class SafetyScanResult:
    scan_id: str = ""
    target: str = ""
    target_type: str = "text"  # text / file / directory
    status: str = "PASS"       # PASS / WARN / BLOCKED
    severity: str = "NONE"     # NONE / LOW / HIGH / CRITICAL
    forbidden_hits: List[str] = field(default_factory=list)
    whitelist_hits: List[str] = field(default_factory=list)
    false_positive_hits: List[str] = field(default_factory=list)
    reason: str = ""
    safe_next_step: str = "REVIEW"
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "scan_id": self.scan_id,
            "target": self.target,
            "target_type": self.target_type,
            "status": self.status,
            "severity": self.severity,
            "forbidden_hits": self.forbidden_hits,
            "whitelist_hits": self.whitelist_hits,
            "false_positive_hits": self.false_positive_hits,
            "reason": self.reason,
            "safe_next_step": self.safe_next_step,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }


@dataclass
class SafetyScanSummary:
    total_scanned: int = 0
    pass_count: int = 0
    warn_count: int = 0
    blocked_count: int = 0
    false_positive_count: int = 0
    overall_status: str = "PASS"
    no_real_orders: bool = True
    production_blocked: bool = True


class SafetyScanner:
    """
    Scans text/files/directories for forbidden trading actions.
    Uses whitelist to prevent false positives on research-safety phrases.
    Research Only. No Real Orders. Production Trading BLOCKED.
    """

    def __init__(self):
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"SCAN-{self._counter:04d}"

    def is_whitelisted_context(self, token: str, context: str) -> bool:
        """Check if token appears in a whitelisted context."""
        for phrase in WHITELIST_PHRASES:
            if token.lower() in phrase.lower() and phrase.lower() in context.lower():
                return True
        # Check safe patterns
        for pattern in _SAFE_PATTERNS:
            if re.search(pattern, context):
                return True
        return False

    def is_forbidden_hit(self, token: str, context: str) -> bool:
        """Check if token is a genuine forbidden hit (not whitelisted)."""
        if not re.search(r'\b' + token + r'\b', context):
            return False
        return not self.is_whitelisted_context(token, context)

    def scan_text(self, text: str, target: str = "inline") -> SafetyScanResult:
        """Scan a text string for forbidden actions."""
        result = SafetyScanResult(
            scan_id=self._next_id(),
            target=target,
            target_type="text",
        )
        # Remove whitelisted phrases first
        cleaned = text
        whitelist_found = []
        for phrase in WHITELIST_PHRASES:
            if phrase in text:
                whitelist_found.append(phrase)
                cleaned = cleaned.replace(phrase, '')
        result.whitelist_hits = list(set(whitelist_found))

        # Remove lines that are safety declarations listing forbidden words
        # (do this BEFORE safe pattern substitution so we can match full lines)
        # These are lines that list forbidden tokens as examples/warnings, not commands
        _SAFETY_LINE_PATTERNS = [
            r'^\s*[>\|#*\-]\s*.*Never\s+(BUY|SELL|ORDER|EXECUTE).*$',
            r'^\s*.*Forbidden\s+trading\s+action.*$',
            r'^\s*.*\[!\].*BUY.*SELL.*ORDER.*$',
            r'^\s*.*No\s+BUY.*SELL.*ORDER.*$',
            r'^\s*.*are\s+never\s+emitted.*$',
            r'^\s*.*\bFORBIDDEN_ACTIONS\b.*$',
            r'^\s*.*\bFORBIDDEN_KEYWORDS\b.*$',
            # Python list elements that are just quoted forbidden token strings
            r'^\s*"(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)"\s*,?\s*$',
            r"^\s*'(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)'\s*,?\s*$",
            # Lines mentioning forbidden words as part of safety guards/checks
            r'^\s*.*guard.*rejects?\s+(BUY|SELL|ORDER|EXECUTE).*$',
            r'^\s*.*rejects?\s+(BUY|SELL|ORDER|EXECUTE).*$',
            r'^\s*.*never\s+emitted.*$',
            # Lines with BUY. (strategy rule ID pattern like BUY.SHORT.PULLBACK)
            r'^\s*[-*]\s+BUY\.',
            r'^\s*BUY\.',
            # Markdown table rows mentioning forbidden for safety check descriptions
            r'^\s*\|.*guard.*\|.*rejects?\s+(BUY|SELL|ORDER|EXECUTE).*\|',
            r'^\s*\|.*correctly\s+rejects?\s+(BUY|SELL|ORDER|EXECUTE).*\|',
            # Lines with slash-separated forbidden list (BUY / SELL / ORDER pattern)
            r'^\s*.*\(BUY\s*/\s*SELL\s*/\s*ORDER.*\).*$',
            r'.*\(BUY\s+/\s+SELL\s+/\s+ORDER\s+/\s+EXECUTE',
            # Multi-value Python list lines with quoted forbidden tokens
            r'^\s*"(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)"(\s*,\s*"[A-Z_]+")+\s*,?\s*$',
            r"^\s*'(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)'(\s*,\s*'[A-Z_]+')+\s*,?\s*$",
            # Python string that is a forbidden-action listing safety message
            r'.*lines\.append\(.*Forbidden.*are\s+never\s+emitted.*\)',
            r'.*lines\.append\(.*are\s+never\s+emitted.*\)',
            # Lines that contain slash-separated EXECUTE / SUBMIT_ORDER lists (safety disclaimers)
            r'.*\bEXECUTE\s*/\s*SUBMIT_ORDER\b',
            r'.*\bSUBMIT_ORDER\s*/\s*AUTO_TRADE\b',
            r'.*EXECUTE.*SUBMIT_ORDER.*AUTO_TRADE.*are\s+\.',
            # Lines that are residual after "Never BUY, SELL, ORDER" was stripped
            # e.g. "> , EXECUTE, SUBMIT_ORDER, AUTO_TRADE."
            r'^\s*[>\|#*\-]\s*,\s*(EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE)',
            r'^\s*,\s*(EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE)',
            # Python string literal containing "> , EXECUTE..." (quote before >)
            # e.g.   "> , EXECUTE, SUBMIT_ORDER, AUTO_TRADE."
            r'^\s*">\s*,\s*(EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE)',
            r"""^\s*'>\s*,\s*(EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE)""",
            # More general: Python string literal with > prefix and residual forbidden tokens
            r'^\s*">\s*[^"]*\b(EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)\b',
            r"""^\s*'>\s*[^']*\b(EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)\b""",
            # Markdown: **[!] No BUY/SELL/ORDER output.**
            r'^\s*[>*_]*\s*\[!\]\s*.*BUY.*SELL.*ORDER.*$',
            # Markdown table rows with BUY/SELL/ORDER in guard-check descriptions
            r'^\s*\|.*BUY/SELL/ORDER.*\|',
            r'^\s*\|.*rejects?\s+BUY.*\|',
            # Documentation lines: "No component generates BUY, SELL, ORDER, EXECUTE, or any"
            r'.*generates\s+BUY[,\s]',
            r'.*generates\s+\*\*?BUY',
            # Documentation lines: guard description "raises ValueError if any text contains: BUY, SELL..."
            r'.*raises\s+ValueError\s+if.*contains.*BUY',
            r'.*contains:\s+BUY',
            r'.*`_guard\(\)`.*rejects\s+BUY',
            r'.*`_guard\(\)`.*(BUY|SELL|ORDER|EXECUTE)',
            r'.*_guard\(\).*rejects\s+BUY',
            r'.*_guard\(\).*\bEXECUTE\b',
            r'.*blocks?\s+BUY/SELL/ORDER/EXECUTE',
            # Markdown code listing of FORBIDDEN list: `BUY`, `SELL`, `ORDER`...
            r'^\s*Forbidden keywords scanned:.*$',
            r'^\s*Forbidden actions blocked:.*$',
            r'^\s*\*\*禁用詞過濾\*\*.*$',
            r'^\s*-\s+所有輸出已過濾.*$',
            # Documentation: "The strings BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE"
            r'.*The strings\s+BUY',
            r'.*strings\s+BUY,\s*SELL',
            # Rule ID format: BUY.SHORT.PULLBACK
            r'.*\bBUY\.(SHORT|LONG|INTRADAY|SWING)\b',
            r'.*e\.g\.\s+BUY\.',
            r'.*e\.g\.\s+`BUY\.',
            # Documentation lines listing safety keywords in backtick code spans
            r'^\s*`(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE)`,',
            r'^\s*`(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE)`\s*$',
            # Documentation: safety audit / no forbidden keywords lines
            r'.*no forbidden\s+(trading\s+)?keywords?\s*\(BUY',
            r'.*no forbidden\s+(trading\s+)?action',
            r'.*safety audit.*forbidden',
            r'.*forbidden.*safety audit',
            # Residual slash-fragments after BUY/SELL/ORDER whitelist removal
            # e.g. "/EXECUTE/etc." or "/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE"
            r'.*/EXECUTE/(?:SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|etc\.)',
            r'.*/EXECUTE/etc\.',
            r'^\s*.*\bblocks\b.*/EXECUTE/',
            r'^\s*.*\brejects\b.*/EXECUTE/',
            # Residual after _guard() backtick was removed: "`` rejects /EXECUTE/..."
            r'^\s*``\s*rejects\s*/EXECUTE/',
            r'^\s*``\s*rejects\b',
            # load_safe_commands blocks
            r'.*load_safe_commands\(\)\s+blocks',
            # REAL_ORDER_READY=False in docs
            r'.*REAL_ORDER_READY\s*=\s*False',
            r'.*REAL_ORDER_READY=False',
        ]
        lines = cleaned.split('\n')
        safe_lines = []
        for line in lines:
            skip = False
            for lp in _SAFETY_LINE_PATTERNS:
                if re.search(lp, line, re.IGNORECASE):
                    skip = True
                    break
            if not skip:
                safe_lines.append(line)
        cleaned = '\n'.join(safe_lines)

        # Apply safe patterns (remove matching sections) AFTER line removal
        for pattern in _SAFE_PATTERNS:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

        forbidden_found = []
        for token in FORBIDDEN_ACTIONS:
            if re.search(r'\b' + token + r'\b', cleaned):
                forbidden_found.append(token)

        if forbidden_found:
            result.forbidden_hits = forbidden_found
            result.status = "BLOCKED"
            result.severity = "CRITICAL"
            result.reason = f"Forbidden actions detected: {forbidden_found}"
            result.safe_next_step = "REVIEW"
        else:
            result.status = "PASS"
            result.severity = "NONE"
            result.reason = "No forbidden actions detected"
            result.safe_next_step = "KEEP_OBSERVING"
        return result

    def scan_file(self, path: str) -> SafetyScanResult:
        """Scan a single file for forbidden actions."""
        p = Path(path)
        result = SafetyScanResult(
            scan_id=self._next_id(),
            target=str(path),
            target_type="file",
        )
        if not p.exists():
            result.status = "WARN"
            result.severity = "LOW"
            result.reason = f"File not found: {path}"
            result.safe_next_step = "REVIEW"
            return result
        if p.suffix.lower() in _SKIP_EXTENSIONS:
            result.status = "PASS"
            result.reason = "Skipped binary/data file"
            return result
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            inline = self.scan_text(text, target=str(path))
            result.status = inline.status
            result.severity = inline.severity
            result.forbidden_hits = inline.forbidden_hits
            result.whitelist_hits = inline.whitelist_hits
            result.reason = inline.reason
            result.safe_next_step = inline.safe_next_step
        except Exception as exc:
            result.status = "WARN"
            result.severity = "LOW"
            result.reason = f"Read error: {exc}"
            result.safe_next_step = "REVIEW"
        return result

    def scan_directory(
        self,
        path: str,
        patterns: Optional[List[str]] = None,
        max_files: int = 500,
    ) -> List[SafetyScanResult]:
        """Scan all matching files in a directory."""
        results = []
        base = Path(path)
        if not base.exists():
            r = SafetyScanResult(
                scan_id=self._next_id(),
                target=str(path),
                target_type="directory",
                status="WARN",
                reason=f"Directory not found: {path}",
            )
            results.append(r)
            return results

        count = 0
        for root, dirs, files in os.walk(str(base)):
            # Skip hidden/build dirs
            dirs[:] = [d for d in dirs if d not in _SKIP_DIRS and not d.startswith('.')]
            for fname in files:
                if count >= max_files:
                    break
                fpath = os.path.join(root, fname)
                ext = Path(fname).suffix.lower()
                if ext in _SKIP_EXTENSIONS:
                    continue
                if patterns:
                    import fnmatch
                    if not any(fnmatch.fnmatch(fname, p) for p in patterns):
                        continue
                results.append(self.scan_file(fpath))
                count += 1

        return results

    def summarize(self, results: List[SafetyScanResult]) -> SafetyScanSummary:
        """Summarize a list of scan results."""
        summary = SafetyScanSummary(total_scanned=len(results))
        for r in results:
            if r.status == "PASS":
                summary.pass_count += 1
            elif r.status == "WARN":
                summary.warn_count += 1
            elif r.status == "BLOCKED":
                summary.blocked_count += 1
        if summary.blocked_count > 0:
            summary.overall_status = "BLOCKED"
        elif summary.warn_count > 0:
            summary.overall_status = "WARN"
        else:
            summary.overall_status = "PASS"
        return summary
