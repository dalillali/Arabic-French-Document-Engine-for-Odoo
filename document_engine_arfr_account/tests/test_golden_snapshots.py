"""Golden extracted-text checks for opt-in reports."""

from __future__ import annotations

import difflib
from pathlib import Path
import re

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


FIXTURES = Path(__file__).parent / "fixtures" / "golden"
CURRENT_YEAR_LINE = re.compile(r"\b20\d{2}\b")
SPACE_RUN = re.compile(r"\s+")


@tagged("post_install", "-at_install")
class TestGoldenSnapshots(ArfrRenderCase):
    def setUp(self):
        super().setUp()
        self.company.write(
            {
                "arfr_document_engine_enabled": True,
                "arfr_default_numeral_system": "arabic_indic",
                "arfr_currency_format_policy": "regional",
            }
        )

    def _normalize(self, text):
        lines = []
        for line in text.splitlines():
            if CURRENT_YEAR_LINE.search(line):
                continue
            line = SPACE_RUN.sub(" ", line).strip()
            if line:
                lines.append(line)
        return "\n".join(lines) + "\n"

    def _assert_golden_text(self, name, rendered_text):
        fixture = FIXTURES / f"{name}.txt"
        expected = self._normalize(fixture.read_text(encoding="utf-8"))
        actual = self._normalize(rendered_text)
        if expected != actual:
            diff = "\n".join(
                difflib.unified_diff(
                    expected.splitlines(),
                    actual.splitlines(),
                    fromfile=f"{name}.golden",
                    tofile=f"{name}.rendered",
                    lineterm="",
                )
            )
            self.fail(f"{name} golden snapshot changed:\n{diff}")

    def test_invoice_ar_fr_text_snapshot(self):
        invoice = self.make_demo_invoice()
        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )
        self._assert_golden_text("invoice_ar_fr", text)

    def test_invoice_ar_en_text_snapshot(self):
        invoice = self.make_demo_invoice()
        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_en",
            invoice,
        )
        self._assert_golden_text("invoice_ar_en", text)
