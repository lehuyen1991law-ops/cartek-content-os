"""Text helpers for Vietnamese content: cleaning, comparison keys, slugs."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

_WS = re.compile(r"\s+")
_NON_ALNUM = re.compile(r"[^0-9a-z]+")
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def clean(value: Any) -> str:
    """Return a trimmed NFC string with internal whitespace collapsed.

    ``None`` becomes an empty string. Non-string values are converted with ``str``.
    """
    if value is None:
        return ""
    text = value if isinstance(value, str) else str(value)
    return _WS.sub(" ", nfc(text)).strip()


def is_blank(value: Any) -> bool:
    return clean(value) == ""


def key(value: Any) -> str:
    """Case-insensitive comparison key that keeps Vietnamese accents."""
    return clean(value).casefold()


def deaccent(text: str) -> str:
    """Strip Vietnamese diacritics: 'Đèn báo lỗi' -> 'Den bao loi'."""
    text = text.replace("đ", "d").replace("Đ", "D")
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", stripped)


def match_text(value: Any) -> str:
    """Lower-cased, accent-free text used for policy pattern matching."""
    return deaccent(clean(value)).casefold()


def loose_key(value: Any) -> str:
    """Accent-, case- and punctuation-insensitive key for near-duplicate detection."""
    return _NON_ALNUM.sub("", match_text(value))


def slugify(value: Any, max_len: int = 60) -> str:
    """ASCII slug for folder names: 'Lỗi P0300 - Ác Mộng' -> 'loi-p0300-ac-mong'."""
    slug = _NON_ALNUM.sub("-", match_text(value)).strip("-")
    if len(slug) > max_len:
        cut = slug[:max_len]
        slug = cut.rsplit("-", 1)[0] if "-" in cut else cut
    return slug or "untitled"


def strip_html_comments(text: str) -> str:
    return _HTML_COMMENT.sub("", text)


def count_syllables(text: str) -> int:
    """Approximate spoken syllables in Vietnamese narration.

    Vietnamese writes one syllable per space-separated token. Tokens with digits
    or short upper-case acronyms are read character by character, so each letter
    or digit counts as one syllable ("P0300" -> 5, "OBD2" -> 4, "ECU" -> 3).
    This is an estimate; calibrate the speech rate in config/production.yaml.
    """
    total = 0
    for token in clean(text).split(" "):
        core = re.sub(r"[^\w]", "", token, flags=re.UNICODE)
        if not core:
            continue
        if any(ch.isdigit() for ch in core):
            total += sum(1 for ch in core if ch.isalnum())
        elif core.isupper() and 2 <= len(core) <= 5:
            total += len(core)
        else:
            total += 1
    return total
