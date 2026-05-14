"""Country-aware Arabic locale strategy tests."""

from __future__ import annotations

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestArabicLocaleStrategy(TransactionCase):
    def test_country_locale_mapping_is_explicit(self):
        report = self.env["ir.actions.report"].create(
            {
                "name": "ARFR Locale Probe",
                "model": "res.partner",
                "report_type": "qweb-pdf",
                "report_name": "base.report_irmodulereference",
            }
        )
        self.assertEqual(report._arfr_pick_arabic_locale("SA"), "ar_SA")
        self.assertEqual(report._arfr_pick_arabic_locale("AE"), "ar_AE")
        self.assertEqual(report._arfr_pick_arabic_locale("MA"), "ar_MA")
        self.assertEqual(report._arfr_pick_arabic_locale("EG"), "ar_EG")
        self.assertEqual(report._arfr_pick_arabic_locale("US"), "ar_001")
