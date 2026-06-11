"""
GUI Safety helpers — Research Only, No Real Orders, Production Trading BLOCKED.
Provides safety banners, forbidden text scanner, and safe label builders.
"""

SAFE_BANNER_TEXT = (
    "Research Only | No Real Orders | Production Trading BLOCKED | "
    "Broker Execution Disabled | VALIDATED does not enable trading"
)

FORBIDDEN_ACTIONS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]

# Whitelist phrases — remove before scanning
_WHITELIST_PHRASES = [
    "No Real Orders",
    "Broker Execution Disabled",
    "No broker execution",
    "Not an order",
    "No automatic deletion",
    "No automatic archive",
    "Archive Suggestions Only",
    "No auto trading",
    "No automatic trading",
    "VALIDATED does not enable trading",
    "No forbidden trading action",
]

SAFE_NEXT_STEPS = [
    "REVIEW",
    "FIX_DATA",
    "READ_REPORT",
    "ARCHIVE_REVIEW",
    "CLEANUP_REVIEW",
    "KEEP_OBSERVING",
    "MARK_RESEARCH_ONLY",
    "PAPER_ONLY",
    "MOCK_ONLY",
    "WAIT",
    "BACKTEST_MORE",
    "PRACTICE_REPLAY",
    "REVIEW_JOURNAL",
    "REVIEW_RISK",
    "REVIEW_EARNINGS",
    "REVIEW_CHIPS",
    "DO_NOT_CHASE",
]


def sanitize_gui_text(text: str) -> str:
    """Remove or mask forbidden trading actions from GUI text."""
    result = text
    for forbidden in FORBIDDEN_ACTIONS:
        # Replace standalone uppercase forbidden words
        import re
        result = re.sub(r'\b' + forbidden + r'\b', '[RESEARCH_ONLY]', result)
    return result


def assert_no_forbidden_gui_text(text: str) -> None:
    """Raise ValueError if text contains forbidden trading actions (after whitelist removal)."""
    import re
    cleaned = text
    for phrase in _WHITELIST_PHRASES:
        cleaned = cleaned.replace(phrase, '')
    for forbidden in FORBIDDEN_ACTIONS:
        if re.search(r'\b' + forbidden + r'\b', cleaned):
            raise ValueError(
                f"Forbidden GUI text detected: '{forbidden}' in: {text[:80]!r}"
            )


def build_research_only_banner() -> str:
    """Return the standard research-only safety banner string."""
    return SAFE_BANNER_TEXT


def build_no_real_orders_label() -> str:
    """Return a short 'No Real Orders' label string."""
    return "No Real Orders — Research Only"
