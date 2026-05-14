"""Shared functional render test helpers for AR/FR document reports."""

from __future__ import annotations

from io import BytesIO
import re

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import TransactionCase


try:
    from pdfminer.high_level import extract_text
except ImportError:  # pragma: no cover - exercised by the Odoo test runner env
    extract_text = None


ARABIC_RANGE = "\u0600-\u06ff"
ARABIC_QUESTION_RUN = re.compile(rf"[{ARABIC_RANGE}]\?+[{ARABIC_RANGE}]")


class ArfrRenderCase(TransactionCase):
    """Base case for tests that must exercise Odoo's real PDF pipeline."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        for code in ("ar_001", "fr_FR", "en_US"):
            cls.ensure_language(code)
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "ARFR Demo Customer",
                "lang": "ar_001",
                "vat": "SA123456789012345",
            }
        )

    def render_report_pdf(self, report_xmlid, record):
        pdf_bytes, _content_type = self.env["ir.actions.report"]._render_qweb_pdf(
            report_xmlid,
            res_ids=[record.id],
        )
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)
        if not pdf_bytes.startswith(b"%PDF"):
            # In Odoo's post-install test phase, _render_qweb_pdf can return the
            # rendered HTML body when wkhtmltopdf is not run by the report
            # wrapper. Keep the test on the real wkhtmltopdf path instead of
            # accepting HTML as a successful render.
            pdf_bytes = self.env["ir.actions.report"]._run_wkhtmltopdf(
                [pdf_bytes.decode("utf-8")],
                report_ref=report_xmlid,
            )
            self.assertIsInstance(pdf_bytes, bytes)
            self.assertGreater(len(pdf_bytes), 0)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"), pdf_bytes[:80])
        return pdf_bytes

    def extract_pdf_text(self, pdf_bytes):
        if extract_text is None:
            self.skipTest("pdfminer.six is required for functional PDF text tests")
        return extract_text(BytesIO(pdf_bytes)) or ""

    def render_report_text(self, report_xmlid, record):
        pdf_bytes = self.render_report_pdf(report_xmlid, record)
        self.assert_no_missing_glyphs(pdf_bytes)
        return self.extract_pdf_text(pdf_bytes)

    def assert_no_missing_glyphs(self, pdf_bytes):
        text = self.extract_pdf_text(pdf_bytes)
        self.assertNotIn("\ufffd", text)
        self.assertNotIn("\u25a1", text)
        self.assertIsNone(ARABIC_QUESTION_RUN.search(text))

    def _demo_sale_journal(self):
        Journal = self.env["account.journal"]
        journal = Journal.search(
            [("type", "=", "sale"), ("company_id", "=", self.company.id)],
            limit=1,
        )
        if journal:
            return journal
        return Journal.create(
            {
                "name": "ARFR Sales Journal",
                "code": "ARFRS",
                "type": "sale",
                "company_id": self.company.id,
            }
        )

    def _demo_income_account(self):
        Account = self.env["account.account"]
        account = Account.search([("account_type", "=", "income")], limit=1)
        if account:
            return account

        vals = {
            "name": "ARFR Sales",
            "code": "ARFRSALES",
            "account_type": "income",
        }
        if "company_ids" in Account._fields:
            vals["company_ids"] = [Command.link(self.company.id)]
        elif "company_id" in Account._fields:
            vals["company_id"] = self.company.id
        return Account.create(vals)

    def make_demo_invoice(self, **overrides):
        try:
            AccountMove = self.env["account.move"]
        except KeyError:
            self.skipTest("account is required for invoice render tests")

        invoice_vals = {
            "move_type": "out_invoice",
            "partner_id": self.partner.id,
            "invoice_date": "2026-05-11",
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": "خدمة استشارية / Service conseil",
                        "quantity": 2.0,
                        "price_unit": 617.28,
                        "account_id": self._demo_income_account().id,
                    },
                )
            ],
            "journal_id": self._demo_sale_journal().id,
        }
        invoice_vals.update(overrides)
        try:
            return AccountMove.create(invoice_vals)
        except (UserError, ValueError) as error:
            self.skipTest(f"account demo invoice setup is unavailable: {error}")

    @classmethod
    def ensure_language(cls, code):
        Lang = cls.env["res.lang"]
        lang = Lang._activate_lang(code)
        if not lang:
            lang = Lang._create_lang(code)
        return lang
