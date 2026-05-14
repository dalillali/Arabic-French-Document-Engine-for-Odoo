"""Public API stability tests for the AR/FR formatter service."""

from __future__ import annotations

from inspect import signature

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestArfrFormatterPublicApi(TransactionCase):
    def test_public_method_signatures_are_stable(self):
        formatter = self.env["arfr.formatter"]

        self.assertIn("value", signature(formatter.format_numerals).parameters)
        self.assertIn("amount", signature(formatter.format_currency).parameters)
        self.assertIn("currency", signature(formatter.format_currency).parameters)
        self.assertIn("record", signature(formatter.resolve).parameters)
        self.assertIn("record", signature(formatter.regulatory_context).parameters)
