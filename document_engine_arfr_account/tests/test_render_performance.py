"""Functional render-performance guard for opt-in invoice reports."""

from __future__ import annotations

import statistics
import time

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestInvoiceRenderPerformance(ArfrRenderCase):
    def _make_hundred_line_invoice(self):
        account = self._demo_income_account()
        lines = [
            (
                0,
                0,
                {
                    "name": f"Service line {index + 1}",
                    "quantity": 1.0,
                    "price_unit": 10 + index,
                    "account_id": account.id,
                },
            )
            for index in range(100)
        ]
        return self.make_demo_invoice(invoice_line_ids=lines)

    def _median_pdf_runtime(self, report_xmlid, record, rounds=3):
        timings = []
        for _round in range(rounds):
            start = time.perf_counter()
            self.env["ir.actions.report"]._render_qweb_pdf(report_xmlid, res_ids=[record.id])
            timings.append(time.perf_counter() - start)
        return statistics.median(timings)

    def test_opt_in_invoice_overhead_stays_under_15_percent(self):
        baseline = self.env.ref("account.account_invoices", raise_if_not_found=False)
        if not baseline:
            self.skipTest("standard account invoice report action is unavailable")

        invoice = self._make_hundred_line_invoice()
        opt_in_xmlid = "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr"
        baseline_time = self._median_pdf_runtime("account.account_invoices", invoice)
        opt_in_time = self._median_pdf_runtime(opt_in_xmlid, invoice)

        self.assertLessEqual(
            opt_in_time,
            baseline_time * 1.15,
            f"opt-in report took {opt_in_time:.3f}s vs standard {baseline_time:.3f}s",
        )
