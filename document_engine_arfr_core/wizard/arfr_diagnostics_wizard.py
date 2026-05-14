from odoo import fields, models


class ArfrDiagnosticsWizard(models.TransientModel):
    _name = "arfr.diagnostics.wizard"
    _description = "AR/FR Diagnostics"

    record_ref = fields.Reference(
        selection=[
            ("account.move", "Invoice"),
            ("sale.order", "Sale Order"),
            ("pos.config", "POS Configuration"),
        ],
        readonly=True,
    )
    resolved_preferences = fields.Text(readonly=True)

    def action_show_for_record(self):
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        record = self.env[active_model].browse(active_id) if active_model and active_id else None
        resolved = self.env["arfr.formatter"].resolve(record if record and record.exists() else None)
        wizard = self.create(
            {
                "record_ref": f"{record._name},{record.id}" if record and record.exists() else False,
                "resolved_preferences": "\n".join(
                    f"{field}: {getattr(resolved, field)}"
                    for field in resolved.__dataclass_fields__
                ),
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Resolved AR/FR Preferences",
            "res_model": "arfr.diagnostics.wizard",
            "view_mode": "form",
            "target": "new",
            "res_id": wizard.id,
        }
