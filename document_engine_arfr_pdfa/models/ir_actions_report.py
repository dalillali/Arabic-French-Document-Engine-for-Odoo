from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _arfr_pdfa_postprocess(self, pdf_bytes, records=None):
        """Roadmap hook for future PDF/A-3b conversion.

        The addon is intentionally non-installable until the converter sets
        PDF/A-3b metadata, embeds an sRGB output intent, attaches ZATCA XML
        with /AFRelationship /Source, and passes veraPDF validation.
        """

        return pdf_bytes
