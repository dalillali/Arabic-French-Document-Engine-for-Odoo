from odoo import fields, models


class ArfrCurrencyFormatRule(models.Model):
    _name = "arfr.currency.format.rule"
    _description = "Arabic/French Currency Format Rule"
    _rec_name = "currency_code"

    currency_code = fields.Char(required=True, index=True)
    symbol = fields.Char(required=True)
    position = fields.Selection(
        [("before", "Before Amount"), ("after", "After Amount")],
        required=True,
        default="after",
    )
    thousands_separator = fields.Char(required=True, default=",")
    decimal_separator = fields.Char(required=True, default=".")

    _sql_constraints = [
        (
            "currency_code_unique",
            "unique(currency_code)",
            "Each currency can have only one AR/FR formatting rule.",
        )
    ]

    def _arfr_rule_map(self):
        return {
            rule.currency_code.upper(): {
                "symbol": rule.symbol,
                "position": rule.position,
                "thousands": rule.thousands_separator,
                "decimal": rule.decimal_separator,
            }
            for rule in self.search([])
        }
