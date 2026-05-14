"""Currency display helpers for opt-in Arabic/French report templates."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Mapping

from .numeral_format import format_numerals


@dataclass(frozen=True)
class CurrencySpec:
    name: str
    symbol: str
    position: str = "before"
    thousands: str = ","
    decimal: str = "."


def _currency_name(currency: Any) -> str:
    return str(getattr(currency, "name", currency or "")).upper()


def _currency_symbol(currency: Any, fallback: str) -> str:
    return str(getattr(currency, "symbol", None) or fallback)


def _quantize(amount: Any) -> Decimal:
    return Decimal(str(amount or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _format_number(amount: Any, thousands: str, decimal: str) -> str:
    value = _quantize(amount)
    sign = "-" if value < 0 else ""
    whole, fraction = f"{abs(value):,.2f}".split(".")
    return f"{sign}{whole.replace(',', thousands)}{decimal}{fraction}"


def _rule_map(env=None, rules: Mapping[str, Mapping[str, str]] | None = None):
    if rules is not None:
        return rules
    if env is None:
        return {}
    return env["arfr.currency.format.rule"].sudo()._arfr_rule_map()


def resolve_currency_spec(
    currency: Any,
    policy: str = "odoo_default",
    *,
    env=None,
    rules: Mapping[str, Mapping[str, str]] | None = None,
) -> CurrencySpec:
    """Resolve display metadata while delegating unknown currencies to Odoo data."""

    name = _currency_name(currency)
    regional_rules = _rule_map(env=env, rules=rules)
    if policy == "regional" and name in regional_rules:
        rule = regional_rules[name]
        return CurrencySpec(
            name=name,
            symbol=_currency_symbol(currency, rule["symbol"]),
            position=rule["position"],
            thousands=rule["thousands"],
            decimal=rule["decimal"],
        )
    return CurrencySpec(
        name=name,
        symbol=_currency_symbol(currency, name),
        position=str(getattr(currency, "position", "before") or "before"),
    )


def format_currency(
    amount: Any,
    currency: Any,
    *,
    numeral_system: str = "western",
    policy: str = "odoo_default",
    render_lang: str | None = None,
    partner_lang: str | None = None,
    env=None,
    rules: Mapping[str, Mapping[str, str]] | None = None,
) -> str:
    """Format an amount for opt-in templates without changing stored data."""

    spec = resolve_currency_spec(currency, policy, env=env, rules=rules)
    number = _format_number(amount, spec.thousands, spec.decimal)
    if policy == "force_western":
        numeral_system = "western"
    number = format_numerals(
        number,
        numeral_system,
        render_lang=render_lang,
        partner_lang=partner_lang,
    )
    if spec.position == "after":
        return f"{number} {spec.symbol}".strip()
    return f"{spec.symbol} {number}".strip()
