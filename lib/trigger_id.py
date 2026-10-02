"""Generate unique trigger IDs for Gated Artifacts Promoter runs."""

from __future__ import annotations

import re
import uuid

TRIGGER_ID_PREFIX = "gap-"
# GitHub labels max length is 50 characters.
MAX_TRIGGER_ID_LENGTH = 50
_LABEL_SAFE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,49}$")


def generate_trigger_id() -> str:
    """Return a unique trigger ID suitable for use as a GitHub label."""
    return f"{TRIGGER_ID_PREFIX}{uuid.uuid4().hex}"


def is_valid_trigger_id(value: str) -> bool:
    """Return True if value is a non-empty GitHub-label-safe trigger ID."""
    text = (value or "").strip()
    if not text or len(text) > MAX_TRIGGER_ID_LENGTH:
        return False
    return bool(_LABEL_SAFE_RE.fullmatch(text))


def normalize_trigger_id(value: str | None) -> str:
    """Return a validated trigger ID, generating one when value is empty."""
    if value is None or not str(value).strip():
        return generate_trigger_id()
    candidate = str(value).strip()
    if not is_valid_trigger_id(candidate):
        raise ValueError(
            f"Invalid trigger ID '{candidate}'. "
            "Use 1-50 characters starting with alphanumeric; "
            "allowed characters: letters, digits, '.', '_', '-'."
        )
    return candidate
