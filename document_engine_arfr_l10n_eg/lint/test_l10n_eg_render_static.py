"""Egypt localization smoke checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ADDON = ROOT / "addons" / "document_engine_arfr_l10n_eg"


def test_egypt_dependencies_are_explicit():
    manifest = (ADDON / "__manifest__.py").read_text(encoding="utf-8")
    assert '"document_engine_arfr_account"' in manifest
    assert '"l10n_eg"' in manifest
    assert '"l10n_eg_edi_eta"' in manifest


if __name__ == "__main__":
    test_egypt_dependencies_are_explicit()
