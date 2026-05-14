from odoo import api, fields, models


class ArfrLabelDictionary(models.Model):
    _name = "arfr.label.dictionary"
    _description = "Arabic/French Label Dictionary"
    _rec_name = "source"

    source = fields.Char(required=True, index=True)
    lang_code = fields.Char(required=True, index=True)
    translation = fields.Char(required=True, translate=True)

    _sql_constraints = [
        (
            "source_lang_unique",
            "unique(source, lang_code)",
            "Each source label can have only one translation per language.",
        )
    ]

    def _arfr_label_map(self):
        return {
            (label.source, label.lang_code): label.translation
            for label in self.search([])
        }

    @api.model
    def translate_label(self, source, lang_code):
        if not source or not lang_code:
            return source
        return self._arfr_label_map().get((source, lang_code), source)
