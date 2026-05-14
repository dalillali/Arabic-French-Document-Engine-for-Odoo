"""Resolve document rendering preferences without mutating Odoo records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


COMPANY_SENTINELS = {None, "", "company"}


@dataclass(frozen=True)
class RenderingPreferences:
    enabled: bool = False
    numeral_system: str = "western"
    identifier_numerals: str | None = None
    numeral_scope: tuple[str, ...] = ()
    secondary_lang: str | None = None
    bilingual_pair: str = "none"
    font_family: str = "noto"
    currency_format_policy: str = "odoo_default"
    layout_direction: str = "auto"


def _get(source: Any, key: str, default: Any = None) -> Any:
    if source is None:
        return default
    if isinstance(source, Mapping):
        return source.get(key, default)
    return getattr(source, key, default)


def _is_company_sentinel(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value in {"", "company"})


def _first_explicit(*values: Any, default: Any) -> Any:
    for value in values:
        if not _is_company_sentinel(value):
            return value
    return default


def _lang_code(value: Any) -> str | None:
    if _is_company_sentinel(value):
        return None
    return _get(value, "code", value)


def resolve_preferences(
    *,
    company: Any = None,
    report: Any = None,
    partner: Any = None,
    print_selection: Mapping[str, Any] | None = None,
    regulatory: Mapping[str, Any] | None = None,
) -> RenderingPreferences:
    """Return the effective rendering preferences for one document render."""

    company_enabled = bool(_get(company, "arfr_document_engine_enabled", False))
    report_enabled = bool(_get(report, "arfr_enabled", False))
    print_enabled = bool(_get(print_selection, "enabled", False))
    regulatory_enabled = bool(_get(regulatory, "enabled", False))

    enabled = regulatory_enabled or print_enabled or report_enabled or company_enabled

    numeral_system = _first_explicit(
        _get(regulatory, "numeral_system"),
        _get(print_selection, "numeral_system"),
        _get(report, "arfr_numeral_system"),
        _get(partner, "arfr_numeral_system"),
        _get(company, "arfr_default_numeral_system"),
        default="western",
    )
    identifier_numerals = _first_explicit(
        _get(regulatory, "identifier_numerals"),
        default=None,
    )
    numeral_scope = tuple(_get(regulatory, "scope", ()) or ())
    secondary_lang = _first_explicit(
        _lang_code(_get(partner, "arfr_secondary_lang_id")),
        _lang_code(_get(company, "arfr_default_secondary_lang_id")),
        _lang_code(_get(print_selection, "secondary_lang")),
        default=None,
    )
    bilingual_pair = _first_explicit(
        _get(print_selection, "bilingual_pair"),
        _get(report, "arfr_bilingual_pair"),
        _get(partner, "arfr_bilingual_pair"),
        _get(company, "arfr_default_bilingual_pair"),
        default="none",
    )
    font_family = _first_explicit(
        _get(report, "arfr_font_family"),
        _get(company, "arfr_default_font_family"),
        default="noto",
    )
    currency_format_policy = _first_explicit(
        _get(regulatory, "currency_format_policy"),
        _get(print_selection, "currency_format_policy"),
        _get(report, "arfr_currency_format_policy"),
        _get(partner, "arfr_currency_format_policy"),
        _get(company, "arfr_currency_format_policy"),
        default="odoo_default",
    )
    layout_direction = _first_explicit(
        _get(print_selection, "layout_direction"),
        _get(report, "arfr_layout_direction"),
        _get(company, "arfr_rtl_layout_policy"),
        default="auto",
    )

    return RenderingPreferences(
        enabled=enabled,
        numeral_system=numeral_system,
        identifier_numerals=identifier_numerals,
        numeral_scope=numeral_scope,
        secondary_lang=secondary_lang,
        bilingual_pair=bilingual_pair,
        font_family=font_family,
        currency_format_policy=currency_format_policy,
        layout_direction=layout_direction,
    )
