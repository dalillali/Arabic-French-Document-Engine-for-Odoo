from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _arfr_regulatory_context(self, record):
        context = super()._arfr_regulatory_context(record)
        if not record or record._name != "account.move":
            return context
        if not self._arfr_l10n_sa_edi_active():
            return context

        return {
            **context,
            "enabled": True,
            "identifier_numerals": "western",
            "scope": [
                *context.get("scope", []),
                "invoice_number",
                "vat_id",
                "qr_visible",
            ],
        }

    def _arfr_l10n_sa_edi_active(self):
        module = self.env["ir.module.module"].sudo().search(
            [("name", "=", "l10n_sa_edi"), ("state", "=", "installed")],
            limit=1,
        )
        return bool(module)

