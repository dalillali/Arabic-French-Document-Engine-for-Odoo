"""Arabic/French document numeral formatting helpers."""

from __future__ import annotations

from decimal import Decimal
from typing import Any


WESTERN_DIGITS = "0123456789"
ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

TO_ARABIC_INDIC = str.maketrans(WESTERN_DIGITS, ARABIC_INDIC_DIGITS)
TO_WESTERN = str.maketrans(ARABIC_INDIC_DIGITS, WESTERN_DIGITS)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, Decimal):
        return format(value, "f")
    return str(value)


def to_arabic_indic(value: Any) -> str:
    """Convert Western digits in ``value`` to Arabic-Indic digits."""

    return _stringify(value).translate(TO_ARABIC_INDIC)


def to_western(value: Any) -> str:
    """Convert Arabic-Indic digits in ``value`` to Western Arabic digits."""

    return _stringify(value).translate(TO_WESTERN)


def resolve_auto_numeral_system(
    *,
    render_lang: str | None = None,
    partner_lang: str | None = None,
) -> str:
    """Resolve the explicit policy behind ``auto`` numerals."""

    render_lang = render_lang or ""
    partner_lang = partner_lang or ""
    render_is_arabic = render_lang == "ar" or render_lang == "ar_001" or render_lang.startswith("ar_")
    partner_is_arabic = partner_lang.startswith("ar")
    return "arabic_indic" if render_is_arabic and partner_is_arabic else "western"


def format_numerals(
    value: Any,
    numeral_system: str | None = "western",
    *,
    render_lang: str | None = None,
    partner_lang: str | None = None,
) -> str:
    """Format value using the requested numeral system."""

    if numeral_system == "auto":
        numeral_system = resolve_auto_numeral_system(
            render_lang=render_lang,
            partner_lang=partner_lang,
        )
    if numeral_system == "arabic_indic":
        return to_arabic_indic(value)
    if numeral_system == "western":
        return to_western(value)
    return _stringify(value)


def scoped_numeral_system(
    default_numeral_system: str,
    *,
    field_key: str | None = None,
    identifier_numerals: str | None = None,
    scope: tuple[str, ...] | list[str] | None = None,
) -> str:
    """Return the effective numeral system for a formatted field."""

    if field_key and identifier_numerals and field_key in (scope or ()):
        return identifier_numerals
    return default_numeral_system
