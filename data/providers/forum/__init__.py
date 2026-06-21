"""
data/providers/forum/__init__.py — Forum Intelligence & Market Sentiment v1.4.7 package init.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SUPPLEMENTARY authority only. Cannot override official sources.
[!] No BUY/SELL generation. No broker. No private board access.
[!] No login bypass. No CAPTCHA bypass. No proxy rotation. No auto-posting.
[!] No author real identity inference. No full IP storage.
[!] Public board only (PTT Stock board). Formal standalone conclusion: DISABLED.
"""

# ---------------------------------------------------------------------------
# Safety constants — MUST NOT be changed
# ---------------------------------------------------------------------------
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE = False
FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED = False
FORUM_PRIVATE_BOARD_ACCESS_ENABLED = False
FORUM_LOGIN_BYPASS_ENABLED = False
FORUM_CAPTCHA_BYPASS_ENABLED = False
FORUM_PROXY_ROTATION_ENABLED = False
FORUM_AUTO_POSTING_ENABLED = False
FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED = False
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

__all__ = [
    "FORUM_CAN_GENERATE_BUY_SELL",
    "FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE",
    "FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED",
    "FORUM_PRIVATE_BOARD_ACCESS_ENABLED",
    "FORUM_LOGIN_BYPASS_ENABLED",
    "FORUM_CAPTCHA_BYPASS_ENABLED",
    "FORUM_PROXY_ROTATION_ENABLED",
    "FORUM_AUTO_POSTING_ENABLED",
    "FORUM_AUTHOR_IDENTITY_INFERENCE_ENABLED",
    "NO_REAL_ORDERS",
    "BROKER_EXECUTION_ENABLED",
    "PRODUCTION_TRADING_BLOCKED",
]
