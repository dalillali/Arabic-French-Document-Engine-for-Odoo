from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAmountWords(TransactionCase):
    def test_amount_words_cover_large_values_and_subunits(self):
        currency = self.env.company.currency_id
        service = self.env["arfr.amount.words"]

        self.assertIn("thousand", service.arfr_amount_in_words(1234, currency, lang="en"))
        self.assertIn("million", service.arfr_amount_in_words(1234567, currency, lang="en"))
        self.assertIn("five cents", service.arfr_amount_in_words(0.05, currency, lang="en"))

    def test_amount_words_cover_french_and_arabic(self):
        currency = self.env.company.currency_id
        service = self.env["arfr.amount.words"]

        self.assertIn("mille", service.arfr_amount_in_words(1234, currency, lang="fr"))
        self.assertIn("جزء", service.arfr_amount_in_words(0.05, currency, lang="ar"))
