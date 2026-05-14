"""Multi-company preference isolation tests."""

from __future__ import annotations

from odoo import Command
from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestMultiCompanyPreferences(ArfrRenderCase):
    def test_each_company_uses_its_own_numeral_policy(self):
        company_a = self.company
        company_b = self.env["res.company"].create({"name": "ARFR Western Company"})
        company_a.write(
            {
                "arfr_document_engine_enabled": True,
                "arfr_default_numeral_system": "arabic_indic",
            }
        )
        company_b.write(
            {
                "arfr_document_engine_enabled": True,
                "arfr_default_numeral_system": "western",
            }
        )

        partner_b = self.partner.copy({"company_id": False})
        account = self._demo_income_account()
        if "company_ids" in account._fields:
            account.write({"company_ids": [Command.link(company_b.id)]})

        invoice_a = self.make_demo_invoice()
        invoice_b = self.make_demo_invoice(company_id=company_b.id, partner_id=partner_b.id)

        report = self.env.ref("document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr")
        text_a = self.extract_pdf_text(report.with_company(company_a)._render_qweb_pdf(report.xml_id, [invoice_a.id])[0])
        text_b = self.extract_pdf_text(report.with_company(company_b)._render_qweb_pdf(report.xml_id, [invoice_b.id])[0])

        self.assertRegex(text_a, r"[٠١٢٣٤٥٦٧٨٩]")
        self.assertRegex(text_b, r"[0-9]")
