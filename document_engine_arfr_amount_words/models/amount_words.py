from decimal import Decimal, ROUND_HALF_UP

from num2words import num2words
from odoo import api, models


class ArfrAmountWords(models.AbstractModel):
    _name = "arfr.amount.words"
    _description = "Arabic/French Amount in Words"

    @api.model
    def arfr_amount_in_words(self, amount, currency, lang="en"):
        value = Decimal(str(amount or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        unit = int(value)
        subunit = int((value - unit) * 100)
        currency_name = getattr(currency, "name", "") or ""
        unit_words = num2words(unit, lang=lang)
        subunit_words = num2words(subunit, lang=lang)
        if lang.startswith("ar"):
            return f"{unit_words} {currency_name} و {subunit_words} جزء"
        if lang.startswith("fr"):
            return f"{unit_words} {currency_name} et {subunit_words} centimes"
        return f"{unit_words} {currency_name} and {subunit_words} cents"
