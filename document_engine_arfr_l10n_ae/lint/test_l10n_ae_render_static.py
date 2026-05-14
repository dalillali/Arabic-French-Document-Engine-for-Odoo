"""UAE localization smoke checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ADDON = ROOT / "addons" / "document_engine_arfr_l10n_ae"


def test_uae_dependencies_are_explicit():
    manifest = (ADDON / "__manifest__.py").read_text(encoding="utf-8")
    assert '"document_engine_arfr_l10n_gcc"' in manifest
    assert '"l10n_ae"' in manifest
    assert '"document_engine_arfr_account"' not in manifest


if __name__ == "__main__":
    test_uae_dependencies_are_explicit()
