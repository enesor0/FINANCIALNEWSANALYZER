"""Support-request validation and safe email-draft generation."""

import re
from urllib.parse import urlencode


SUPPORT_EMAIL = "enesor8@gmail.com"
_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_support_request(name: str, email: str, message: str) -> str | None:
    """Return a user-facing validation message, or ``None`` for a valid request."""
    if len(name.strip()) < 2:
        return "Please enter your name."
    if not _EMAIL_PATTERN.fullmatch(email.strip()):
        return "Please enter a valid email address."
    if len(message.strip()) < 20:
        return "Please provide at least 20 characters so the request can be understood."
    return None


def build_support_mailto(topic: str, name: str, email: str, message: str) -> str:
    """Build a mailto URL without sending or storing any user-provided data."""
    subject = f"Financial News Analyzer — {topic.strip() or 'Support request'}"
    body = (
        f"Name: {name.strip()}\n"
        f"Reply-to email: {email.strip()}\n"
        f"Topic: {topic.strip()}\n\n"
        f"Message:\n{message.strip()}"
    )
    return f"mailto:{SUPPORT_EMAIL}?{urlencode({'subject': subject, 'body': body})}"
