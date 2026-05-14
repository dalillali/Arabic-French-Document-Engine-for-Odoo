"""Migration hook smoke tests."""

from __future__ import annotations

from pathlib import Path
import runpy

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestMigrationSafety(TransactionCase):
    def test_noop_migration_hooks_are_importable(self):
        root = Path(__file__).resolve().parents[3] / "addons"
        for addon in ("document_engine_arfr_core", "document_engine_arfr_account", "document_engine_arfr_pos"):
            for hook in ("pre-migrate.py", "post-migrate.py"):
                module = runpy.run_path(str(root / addon / "migrations" / "19.0.1.1.0" / hook))
                self.assertIn("migrate", module)
