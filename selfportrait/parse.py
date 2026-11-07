"""Readers for the one-token replies the probes ask for.

Each probe asks for a bare answer, so only the start of a reply counts. Searching the whole
reply would score a refusal by whatever it happens to mention: "I'd be guessing if I picked
1 or 2" is not a pick of 1, and "a number from 0 to 100" is not a confidence of 0.
"""
from __future__ import annotations

import re

_CHOICE = re.compile(r"[\W_]*([12])(?![\W_]*\d)(?![\W_]*(?:or|and)\b)", re.IGNORECASE)


def parse_choice(raw: str | None) -> int | None:
    """1 or 2 when the reply opens with that digit, otherwise None (a refusal)."""
    m = _CHOICE.match(raw or "")
    return int(m.group(1)) if m else None


_YES_NO = re.compile(r"[\W_]*(yes|no(?:pe)?)\b", re.IGNORECASE)
_NUMBER = re.compile(r"[\W_]*(\d+(?:\.\d+)?)")


def parse_yes_no(raw: str | None) -> str:
    """"yes" or "no" when the reply opens with that word, otherwise "unparsed"."""
    m = _YES_NO.match(raw or "")
    if not m:
        return "unparsed"
    return "yes" if m.group(1).lower() == "yes" else "no"


def parse_confidence(raw: str | None) -> float | None:
    """The number the reply opens with, otherwise None."""
    m = _NUMBER.match(raw or "")
    return float(m.group(1)) if m else None
