from __future__ import annotations

import re

import pytest

from lib.trigger_id import (
    TRIGGER_ID_PREFIX,
    generate_trigger_id,
    is_valid_trigger_id,
    normalize_trigger_id,
)


def test_generate_trigger_id_format() -> None:
    value = generate_trigger_id()
    assert value.startswith(TRIGGER_ID_PREFIX)
    assert is_valid_trigger_id(value)
    assert re.fullmatch(rf"{re.escape(TRIGGER_ID_PREFIX)}[0-9a-f]{{32}}", value)


def test_generate_trigger_id_is_unique() -> None:
    assert generate_trigger_id() != generate_trigger_id()


def test_normalize_trigger_id_generates_when_missing() -> None:
    assert is_valid_trigger_id(normalize_trigger_id(None))
    assert is_valid_trigger_id(normalize_trigger_id(""))
    assert is_valid_trigger_id(normalize_trigger_id("   "))


def test_normalize_trigger_id_accepts_custom() -> None:
    assert normalize_trigger_id("my-trigger-1") == "my-trigger-1"
    assert normalize_trigger_id("  gap-abc  ") == "gap-abc"


def test_normalize_trigger_id_rejects_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid trigger ID"):
        normalize_trigger_id("bad label with spaces")
    with pytest.raises(ValueError, match="Invalid trigger ID"):
        normalize_trigger_id("-starts-with-dash")
    with pytest.raises(ValueError, match="Invalid trigger ID"):
        normalize_trigger_id("x" * 51)
